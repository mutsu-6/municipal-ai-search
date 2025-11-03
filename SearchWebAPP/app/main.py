# app/main.py
import logging
import time
import uuid
from typing import Dict, Any, List, Tuple

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from conversation_graph import workflow, feedback_workflow
from catalog_utils import CatalogSearchEngine
from embed_utils import embed_text
from llm_utils import ServiceSelector
from db_utils import (
    save_conversation, get_conversation_history,
    save_search_query, save_feedback, save_service_click,
    test_db_connection
)

# -----------------------------------------------------------------------------
# 初期設定
# -----------------------------------------------------------------------------
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="自治体サービス検索", layout="wide")
st.title("自治体サービス検索システム")

# -----------------------------------------------------------------------------
# データベース接続確認
# -----------------------------------------------------------------------------
db_enabled = True
try:
    db_enabled = test_db_connection()
    if db_enabled:
        logger.info("Database connection successful")
    else:
        logger.warning("Database connection failed, continuing without persistence")
except Exception as e:
    logger.warning("Database not available: %s, continuing without persistence", e)
    db_enabled = False

# -----------------------------------------------------------------------------
# セッションID生成
# -----------------------------------------------------------------------------
if "session_id" not in st.session_state:
    # 一意のセッションIDを生成
    st.session_state.session_id = str(uuid.uuid4())
    logger.info("Generated session_id: %s", st.session_state.session_id)

# -----------------------------------------------------------------------------
# セッション状態
# -----------------------------------------------------------------------------
if "history" not in st.session_state:
    # データベースから履歴を読み込む
    if db_enabled:
        try:
            db_history = get_conversation_history(st.session_state.session_id)
            st.session_state.history = db_history if db_history else []
            if db_history:
                logger.info("Loaded %d messages from database", len(db_history))
        except Exception as e:
            logger.warning("Failed to load history from database: %s", e)
            st.session_state.history: List[Tuple[str, str]] = []
    else:
        st.session_state.history: List[Tuple[str, str]] = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""
if "awaiting_feedback" not in st.session_state:
    st.session_state.awaiting_feedback = False
if "refine_loops" not in st.session_state:
    st.session_state.refine_loops = 0
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_labels" not in st.session_state:
    st.session_state.last_labels = ([], [])
# ユーザープロフィール情報（会話を通じて収集）
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "年齢層": None,
        "家族構成": None,
        "関心事": [],
        "急ぎの要件": None,
        "収入状況": None,
        "居住環境": None
    }

# -----------------------------------------------------------------------------
# ユーティリティ
# -----------------------------------------------------------------------------
def extract_url(val) -> str:
    """service_catalog.json の URL 形式ゆらぎに耐える抽出器"""
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, list):
        if val and isinstance(val[0], str):
            return val[0].strip()
        return ""
    if isinstance(val, dict):
        for k in ("items", "item", "url", "URL", "link", "links"):
            if k in val:
                v = val[k]
                if isinstance(v, str):
                    return v.strip()
                if isinstance(v, list) and v and isinstance(v[0], str):
                    return v[0].strip()
    return ""

def series_get(row, key, default=None):
    try:
        if hasattr(row, "get"):
            return row.get(key, default)
        return row[key] if key in row else default
    except Exception:
        return default

def row_to_title_url(row) -> Tuple[str, str]:
    title = series_get(row, "タイトル", "")
    url_field = series_get(row, "URL", "")
    url = extract_url(url_field)
    title = str(title).strip() if title is not None else ""
    return title, url

# -----------------------------------------------------------------------------
# 検索エンジン/セレクタ
# -----------------------------------------------------------------------------
searcher = CatalogSearchEngine()
selector = ServiceSelector()

# -----------------------------------------------------------------------------
# チャット履歴の表示
# -----------------------------------------------------------------------------
for role, msg in st.session_state.history:
    st.chat_message("user" if role == "user" else "assistant").write(msg)

# -----------------------------------------------------------------------------
# 入力フォーム
# -----------------------------------------------------------------------------
with st.form("chat-form", clear_on_submit=True):
    user_msg = st.text_input("質問を入力してください", "")
    submitted = st.form_submit_button("送信")

# -----------------------------------------------------------------------------
# 送信処理
# -----------------------------------------------------------------------------
if submitted and user_msg:
    # 1) store user message
    st.session_state.history.append(("user", user_msg))
    logger.info("Received user message: %s", user_msg)
    
    # データベースに保存
    if db_enabled:
        try:
            save_conversation(st.session_state.session_id, "user", user_msg)
        except Exception as e:
            logger.warning("Failed to save user message to database: %s", e)

    # combine with pending question if we previously asked for target/intent info
    combined_question = f"{st.session_state.pending_question} {user_msg}".strip()
    logger.info("Combined question: '%s' (pending='%s')",
                combined_question, st.session_state.pending_question)
    # 直近入力を保存
    st.session_state.last_query = combined_question

    # 2) LangGraph workflow
    try:
        state = workflow.invoke(
            {"question": combined_question, "target_labels": [], "service_labels": []}
        )
        logger.info("Workflow output: %s", state)
    except ValueError as e:
        # APIキー関連のエラー
        logger.exception("APIキーの設定エラー")
        error_msg = str(e)
        if "OPENAI_API_KEY" in error_msg:
            st.session_state.history.append(
                ("assistant", "APIキーが正しく設定されていません。管理者にお問い合わせください。")
            )
        else:
            st.session_state.history.append(
                ("assistant", f"設定エラーが発生しました: {error_msg}")
            )
        st.rerun()
    except Exception as e:
        logger.exception("workflow failed: %s", str(e))
        error_type = type(e).__name__
        error_msg = str(e)
        
        # OpenAI API関連のエラーを詳しく表示
        if "AuthenticationError" in error_type or "401" in error_msg or "api key" in error_msg.lower():
            st.session_state.history.append(
                ("assistant", "OpenAI APIの認証エラーが発生しました。APIキーが無効か、設定が正しくありません。")
            )
        elif "RateLimitError" in error_type or "429" in error_msg:
            st.session_state.history.append(
                ("assistant", "APIのリクエスト制限に達しました。しばらく時間を置いて再度お試しください。")
            )
        elif "InvalidRequestError" in error_type or "400" in error_msg:
            st.session_state.history.append(
                ("assistant", f"リクエストエラーが発生しました: {error_msg[:100]}")
            )
        else:
            st.session_state.history.append(
                ("assistant", f"内部エラーが発生しました: {error_type} - {error_msg[:200]}")
            )
        st.rerun()

    # 分岐1: 対象者が不明 -> 先に対象者確定
    if state["action"] == "ask":
        st.session_state.pending_question = combined_question
        logger.info("Action=ask pending_question='%s'", st.session_state.pending_question)
        st.session_state.history.append(("assistant", state["followup"]))
        st.rerun()

    # 分岐2: 意図が不明 -> 意図確定のための1問
    if state["action"] == "ask_intent":
        st.session_state.pending_question = combined_question
        logger.info("Action=ask_intent pending_question='%s'", st.session_state.pending_question)
        st.session_state.history.append(("assistant", state.get("followup") or "もう少し詳しく教えてください。"))
        st.rerun()

    # ここに来るのは search_intent（意図確度高い） or intent確定後の通常検索
    st.session_state.pending_question = ""
    intent_sentence = state.get("intent_sentence") or combined_question
    target_labels = state.get("target_labels", [])
    service_labels = state.get("service_labels", [])
    confidence = state.get("intent_confidence", 0.0)
    logger.info("SEARCH intent_sentence='%s' confidence=%.2f", intent_sentence, confidence)
    logger.info("検索を実行: 対象者ラベル=%s サービスラベル=%s", target_labels, service_labels)

    st.session_state.last_labels = (target_labels, service_labels)
    st.session_state.last_query = intent_sentence  # 検索に使った文として保存

    # 3) カタログをラベルでフィルタ
    filtered_df = searcher.filter_by_labels(target_labels, service_labels)
    logger.info("フィルター後のサービス件数: %s件", len(filtered_df))

    # 4) 埋め込み + 類似度上位
    query_vec = embed_text(intent_sentence)
    ranked_df = searcher.rank(filtered_df, query_vec, top_n=50)

    # 5) 推薦/表示（会話形式の返答を生成）
    try:
        if ranked_df is None or len(ranked_df) == 0:
            assistant_reply = f"{combined_question}\n\nすみません、該当する自治体サービスが見つかりませんでした。別の表現でお試しください。"
        else:
            # 候補を安全に構築（詳細情報を含む）
            candidates = []
            for _, row in ranked_df.head(20).iterrows():  # 上位20件を候補として使用
                t, u = row_to_title_url(row)
                if t:
                    service_data = {"title": t, "url": u}
                    # 行から他の情報も取得（概要、対象者など）
                    overview = series_get(row, "概要")
                    if overview is not None and not (isinstance(overview, float) and pd.isna(overview)):
                        if isinstance(overview, (list, tuple)) and len(overview) > 0:
                            service_data["概要"] = str(overview[0])
                        elif isinstance(overview, str):
                            service_data["概要"] = overview
                    
                    row_target_labels = series_get(row, "対象者ラベル")
                    if row_target_labels is not None and not (isinstance(row_target_labels, float) and pd.isna(row_target_labels)):
                        if isinstance(row_target_labels, (list, tuple)) and len(row_target_labels) > 0:
                            service_data["対象者"] = ", ".join(str(l) for l in row_target_labels)
                    
                    row_service_labels = series_get(row, "サービスラベル")
                    if row_service_labels is not None and not (isinstance(row_service_labels, float) and pd.isna(row_service_labels)):
                        if isinstance(row_service_labels, (list, tuple)) and len(row_service_labels) > 0:
                            service_data["サービス種別"] = ", ".join(str(l) for l in row_service_labels)
                    candidates.append(service_data)

            # 会話形式の返答を生成
            try:
                assistant_reply = selector.generate_conversational_response(
                    user_query=combined_question,
                    services=candidates[:10],  # 上位10件を使用
                    target_labels=target_labels,
                    service_labels=service_labels,
                    conversation_history=st.session_state.history,  # 会話履歴を追加
                    user_profile=st.session_state.user_profile  # ユーザープロフィールを追加
                )
                logger.info("Generated conversational response successfully")
            except Exception:
                logger.exception("Failed to generate conversational response; using fallback")
                # フォールバック: シンプルな形式で返す
                top_rows = ranked_df.head(5)
                lines = []
                for _, row in top_rows.iterrows():
                    t, u = row_to_title_url(row)
                    if t:
                        lines.append(f"- **{t}** ({u})" if u else f"- **{t}**")
                assistant_reply = f"以下のサービスが見つかりました:\n\n" + "\n".join(lines) if lines else "サービスが見つかりませんでした。"

        st.session_state.history.append(("assistant", assistant_reply))
        logger.info("Rendered response (length: %d chars)", len(assistant_reply))
        
        # データベースに保存
        if db_enabled:
            try:
                save_conversation(st.session_state.session_id, "assistant", assistant_reply)
                # 検索クエリも保存
                save_search_query(
                    st.session_state.session_id,
                    query=combined_question,
                    intent_sentence=intent_sentence,
                    intent_confidence=confidence,
                    target_labels=target_labels,
                    service_labels=service_labels,
                    results_count=len(ranked_df) if ranked_df is not None else 0
                )
            except Exception as e:
                logger.warning("Failed to save response to database: %s", e)
    except Exception:
        logger.exception("Rendering services failed")
        st.session_state.history.append(
            ("assistant", f"{combined_question}\n\n候補の表示でエラーが発生しました。入力条件を少し変えて再度お試しください。")
        )

    # 検索結果に対するフィードバックを受け付ける
    st.session_state.awaiting_feedback = True
    # rerunせず、このフレームでUIを描画

# -----------------------------------------------------------------------------
# 検索結果へのフィードバック処理
# -----------------------------------------------------------------------------
if st.session_state.get("awaiting_feedback", False):
    st.divider()
    st.info("この結果は役立ちましたか？")
    col1, col2 = st.columns(2)
    with col1:
        fb_yes = st.button("はい、終了する", key="fb_yes")
    with col2:
        fb_no = st.button("いいえ、条件を絞り込む", key="fb_no")

    if fb_yes:
        # 終了
        st.session_state.history.append(("assistant", "ご利用ありがとうございました。別の質問もどうぞ。"))
        st.session_state.awaiting_feedback = False
        st.session_state.refine_loops = 0
        # データベースに保存
        if db_enabled:
            try:
                save_feedback(st.session_state.session_id, "yes")
            except Exception as e:
                logger.warning("Failed to save feedback: %s", e)
        st.rerun()

    if fb_no:
        # ループ上限チェック
        st.session_state.refine_loops += 1
        if st.session_state.refine_loops >= 3:
            st.session_state.history.append(
                ("assistant", "うまく見つからないようです。担当窓口や有人チャットをご案内できます。続けますか？「続ける」または「終了」と入力してください。")
            )
            st.session_state.awaiting_feedback = False
            st.rerun()

        # フィードバックに基づく再絞り込み質問
        try:
            fb_state = feedback_workflow.invoke(
                {
                    "question": st.session_state.last_query,
                    "target_labels": st.session_state.last_labels[0],
                    "service_labels": st.session_state.last_labels[1],
                    "feedback": "bad",
                    "refine_hint": None,
                }
            )
            followup = fb_state.get("followup") or (
                "より具体的に条件を教えてください（対象者／サービス種別／オンライン手続き可否／費用・助成／時期・締切／地域・施設）。"
            )
        except Exception:
            logger.exception("feedback_workflow failed")
            followup = "より具体的に条件を教えてください（対象者／サービス種別／オンライン手続き可否／費用・助成／時期・締切／地域・施設）。"

        st.session_state.pending_question = st.session_state.last_query  # 直前の意図文を保持
        logger.info("ASK(by_feedback): pending='%s'", st.session_state.pending_question)
        st.session_state.history.append(("assistant", followup))
        st.session_state.awaiting_feedback = False
        st.rerun()

