# app/llm_utils.py
import os
import json
from typing import List, Dict, Any, Tuple

from openai import OpenAI
import logging

# モデルは .env の LLM_MODEL で上書き可能（既定: gpt-4o-mini）
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

logger = logging.getLogger(__name__)

# APIキーの確認とログ出力
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your-"):
    logger.error("OPENAI_API_KEY が正しく設定されていません。.env ファイルを確認してください。")
    raise ValueError("OPENAI_API_KEY が設定されていません。.env ファイルに正しいAPIキーを設定してください。")

logger.info("OpenAI API クライアントを初期化します（モデル: %s）", DEFAULT_MODEL)
client = OpenAI(api_key=api_key)


# --------------------------------------------------------------------
# ラベル付け：ユーザー質問から 対象者ラベル / サービスラベル を推定
# 返り値: {"target_labels": [...], "service_labels": [...]}
# --------------------------------------------------------------------
def label_question(
    question: str, 
    conversation_history: List[Tuple[str, str]] = None,
    user_profile: Dict[str, Any] = None
) -> Dict[str, List[str]]:
    system_prompt = (
        "あなたは自治体サービス検索のラベリング係です。"
        "入力文から『対象者ラベル』と『サービスラベル』を推定し、必ずJSONで返してください。"
        "キーは target_labels と service_labels の2つです。"
        "候補は以下のリストのみから選んでください。"
        "\n\n"
        "【対象者ラベル】\n"
        "  乳幼児（0～2歳）, 未就学児（3歳〜小学校入学前）, 小学生, 中学生, 高校生, 大学生, "
        "  保護者, 社会人, 高齢者, 障がい者, 事業者, 男性, 女性, どなたでも利用・参加可能, その他（該当が不明な場合）\n\n"
        "【サービスラベル】\n"
        "  補助金・助成金, 住まい・住宅支援, ペット・動物愛護, 水道・上下水道, 公園・緑地・レクリエーション, "
        "  意見・要望・苦情受付, 健康・医療, 福祉・介護, 子育て・教育, 雇用・就労支援, 市民生活・手続き, 防災・災害対応, "
        "  環境・ごみ・リサイクル, まちづくり・都市整備, 産業・事業者支援, 文化・スポーツ, 交通・移動支援, 移住・定住促進, "
        "  男女共同参画・人権・相談, 行政運営・計画・評価, 選挙・政治参加, デジタル・IT関連, 消費生活・トラブル対応, その他\n"
        "\n必ずJSONのみを出力してください。"
    )
    
    # 会話履歴をフォーマット
    history_context = ""
    if conversation_history and len(conversation_history) > 0:
        recent_history = conversation_history[-10:]
        history_parts = []
        for role, msg in recent_history:
            if role == "user":
                history_parts.append(f"ユーザー: {msg}")
            elif role == "assistant":
                history_parts.append(f"アシスタント: {msg}")
        if history_parts:
            history_context = "\n\n【前の会話】\n" + "\n".join(history_parts) + "\n"
    
    # ユーザープロフィールをフォーマット
    profile_context = ""
    if user_profile:
        profile_parts = []
        if user_profile.get("年齢層"):
            profile_parts.append(f"年齢層: {user_profile['年齢層']}")
        if user_profile.get("家族構成"):
            profile_parts.append(f"家族構成: {user_profile['家族構成']}")
        if user_profile.get("関心事"):
            profile_parts.append(f"関心事: {', '.join(user_profile['関心事'])}")
        if profile_parts:
            profile_context = "\n\n【ユーザー情報】\n" + "\n".join(profile_parts) + "\n"
    
    user_prompt = f"入力文: {question}{history_context}{profile_context}"

    # 会話履歴がある場合はmessages配列として渡す
    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history and len(conversation_history) > 0:
        recent_history = conversation_history[-10:]
        for role, msg in recent_history:
            if role == "user":
                messages.append({"role": "user", "content": msg})
            elif role == "assistant":
                messages.append({"role": "assistant", "content": msg})
    messages.append({"role": "user", "content": f"入力文: {question}{profile_context}"})

    resp = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"},  # JSON を強制
    )
    content = (resp.choices[0].message.content or "").strip()
    try:
        data = json.loads(content)
        return {
            "target_labels": data.get("target_labels", []) or [],
            "service_labels": data.get("service_labels", []) or [],
        }
    except Exception as e:
        logger.warning("label_question JSON parse failed: %s | raw=%s", e, content[:300].replace("\n", " "))
        return {"target_labels": [], "service_labels": []}


# --------------------------------------------------------------------
# 候補サービスから最大3件を選ぶセレクタ
# candidates: [{"title": str, "url": str}, ...]
# --------------------------------------------------------------------
class ServiceSelector:
    def __init__(self, model: str = DEFAULT_MODEL, top_k: int = 3):
        self.model = model
        self.top_k = top_k

    def recommend(self, query: str, candidates: List[Dict[str, str]]) -> List[Dict[str, str]]:
        prompt = (
            "あなたは自治体サービスの案内係です。ユーザー質問に最も関連する候補を最大3件、"
            "JSON で返してください。出力形式:\n"
            '{"recommendations":[{"title":"...","url":"..."}, ...]}\n\n'
            f"ユーザー質問: {query}\n\n候補:\n{json.dumps(candidates, ensure_ascii=False, indent=2)}"
        )
        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"},  # JSON を強制
        )
        content = (resp.choices[0].message.content or "").strip()
        try:
            parsed = json.loads(content)
            recs = parsed.get("recommendations", []) or []
            normed = []
            for r in recs:
                t = str(r.get("title", "")).strip()
                u = r.get("url", "")
                if t:
                    normed.append({"title": t, "url": u if isinstance(u, str) else u})
            return normed[: self.top_k]
        except Exception as e:
            logger.warning("ServiceSelector JSON parse failed: %s | raw=%s", e, content[:300].replace("\n", " "))
            return []

    def generate_conversational_response(
        self, 
        user_query: str, 
        services: List[Dict[str, Any]], 
        target_labels: List[str] = None,
        service_labels: List[str] = None,
        conversation_history: List[Tuple[str, str]] = None,
        user_profile: Dict[str, Any] = None
    ) -> str:
        """
        検索結果を基に、会話形式の詳細な説明を生成します。
        
        Args:
            user_query: ユーザーの質問
            services: 検索結果のサービスリスト [{"title": str, "url": str, "概要": str, ...}, ...]
            target_labels: 対象者ラベル
            service_labels: サービスラベル
        
        Returns:
            会話形式のマークダウン形式の説明文
        """
        services_json = json.dumps(services, ensure_ascii=False, indent=2)
        labels_info = ""
        if target_labels or service_labels:
            labels_info = f"\n対象者: {', '.join(target_labels or [])}\nサービス種別: {', '.join(service_labels or [])}"
        
        # ユーザープロフィール情報をフォーマット
        profile_context = ""
        if user_profile:
            profile_parts = []
            if user_profile.get("年齢層"):
                profile_parts.append(f"年齢層: {user_profile['年齢層']}")
            if user_profile.get("家族構成"):
                profile_parts.append(f"家族構成: {user_profile['家族構成']}")
            if user_profile.get("関心事"):
                profile_parts.append(f"関心事: {', '.join(user_profile['関心事'])}")
            if user_profile.get("急ぎの要件"):
                profile_parts.append(f"急ぎの要件: {user_profile['急ぎの要件']}")
            if profile_parts:
                profile_context = "\n\n【ユーザー情報】\n" + "\n".join(profile_parts) + "\n"
        
        # 会話履歴をフォーマット（メッセージ配列として構築）
        messages = []
        if conversation_history and len(conversation_history) > 0:
            # 直近の会話履歴を含める（最大8往復分＝16メッセージ）
            recent_history = conversation_history[-16:] if len(conversation_history) > 16 else conversation_history
            for role, msg in recent_history:
                if role == "user":
                    messages.append({"role": "user", "content": msg})
                elif role == "assistant":
                    messages.append({"role": "assistant", "content": msg})
        
        system_prompt = (
            "あなたは親切で知識豊富な自治体サービスの案内係です。ChatGPTと同レベルの"
            "人間らしい自然な会話を提供しながら、ユーザーの質問に対して検索結果を基に"
            "詳細な説明を提供してください。\n\n"
            "【重要な役割】\n"
            "- 会話を通じてユーザーの状況を理解し、必要な情報を自然に収集する\n"
            "- ユーザーが具体的な質問ができない場合でも、優しく誘導して必要な情報を引き出す\n"
            "- 年齢、家族構成、収入状況、急ぎの要件など、サービス選定に重要な情報を忘れずに把握する\n\n"
            "【返答の形式】\n"
            "1. 冒頭で、ユーザーの状況を深く理解していることを示す、共感的で親しみやすい挨拶\n"
            "2. 絵文字（✅、🔍、🎯、💡、📝など）を使った視覚的な構造化\n"
            "3. 主な支援制度の詳細な説明（各制度の説明、対象条件、申請期限、特筆事項など）\n"
            "4. 実務的な留意点・確認すべきこと（よくある質問や注意点を含む）\n"
            "5. 次のステップ（具体的で実行可能なアクション）\n\n"
            "【重要な注意事項】\n"
            "- 人間らしい自然な会話トーンを心がける（機械的にならないよう注意）\n"
            "- ユーザーの状況に深く共感し、適切な助言を提供する\n"
            "- ユーザー情報が不足している場合は、会話の流れの中で自然に質問を追加する\n"
            "- 各サービスには必ずURLを明記し、クリックできるようフォーマットする\n"
            "- 実務的な情報（申請期限、対象条件、必要書類など）を正確に記載する\n"
            "- マークダウン形式で返答する（見出し、リスト、強調、引用など）\n"
            "- 必要に応じて、関連する他のサービスにも言及する\n"
            "- ユーモアや励ましを適度に交えつつ、専門性と正確性を重視する\n"
        )
        
        # 現在の質問にユーザープロフィールとラベル情報を追加
        current_query_with_context = f"ユーザーの質問: {user_query}{profile_context}{labels_info}\n\n"
        current_query_with_context += f"検索結果のサービス:\n{services_json}\n\n"
        current_query_with_context += "上記の検索結果を基に、会話形式で詳細な説明を生成してください。"
        current_query_with_context += "各サービスについて、どのような制度なのか、対象条件、申請方法、期限などを含めて説明してください。"
        current_query_with_context += "ユーザー情報が不足している場合は、自然な形で追加の質問を促してください。"
        
        # メッセージ配列を構築
        full_messages = [
            {"role": "system", "content": system_prompt},
            *messages,  # 会話履歴を挿入
            {"role": "user", "content": current_query_with_context},
        ]
        
        try:
            resp = client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=0.8,  # より人間らしい自然な会話のため温度を上げる
                top_p=0.9,  # nucleus samplingで多様性を確保
                presence_penalty=0.3,  # 繰り返しを減らす
                frequency_penalty=0.3,  # 繰り返しを減らす
            )
            content = (resp.choices[0].message.content or "").strip()
            logger.info("Generated conversational response (length: %d)", len(content))
            return content
        except Exception as e:
            logger.exception("Failed to generate conversational response")
            # フォールバック: シンプルな形式で返す
            fallback_lines = []
            for svc in services[:5]:
                title = svc.get("title", "")
                url = svc.get("url", "")
                if title:
                    if url:
                        fallback_lines.append(f"- **{title}** ({url})")
                    else:
                        fallback_lines.append(f"- **{title}**")
            return f"以下のサービスが見つかりました:\n\n" + "\n".join(fallback_lines)


# --------------------------------------------------------------------
# 検索用「正規化1文」ビルダー
# 返り値:
#   {
#     "intent_sentence": str,
#     "target_labels": [str, ...],
#     "service_labels": [str, ...],
#     "confidence": float(0-1),
#     "followup": str or None
#   }
#   ※ UI には出さず、LLMが生成したメッセージはログにINFOで出力する
# --------------------------------------------------------------------
class IntentBuilder:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def build(self, user_query: str) -> Dict[str, Any]:
        system_prompt = (
            "あなたは自治体サービス検索の案内係です。"
            "ユーザー質問から、検索で使う代表的な1文（短く具体的）を作成し、"
            "対象者ラベル・サービスラベルを付与し、確信度(0-1)を数値で返し、"
            "不明瞭なら追質問を1つだけ生成してください。"
            "必ずJSONのみを出力し、キーは intent_sentence, target_labels, service_labels, confidence, followup にしてください。"
            "意図が明確なら followup は null にしてください。"
            "\n\n"
            "【対象者ラベル候補】\n"
            "  乳幼児（0～2歳）, 未就学児（3歳〜小学校入学前）, 小学生, 中学生, 高校生, 大学生, "
            "  保護者, 社会人, 高齢者, 障がい者, 事業者, 男性, 女性, どなたでも利用・参加可能, その他（該当が不明な場合）\n\n"
            "【サービスラベル候補】\n"
            "  補助金・助成金, 住まい・住宅支援, ペット・動物愛護, 水道・上下水道, 公園・緑地・レクリエーション, "
            "  意見・要望・苦情受付, 健康・医療, 福祉・介護, 子育て・教育, 雇用・就労支援, 市民生活・手続き, 防災・災害対応, "
            "  環境・ごみ・リサイクル, まちづくり・都市整備, 産業・事業者支援, 文化・スポーツ, 交通・移動支援, 移住・定住促進, "
            "  男女共同参画・人権・相談, 行政運営・計画・評価, 選挙・政治参加, デジタル・IT関連, 消費生活・トラブル対応, その他\n"
        )
        user_prompt = (
            f"ユーザー質問: {user_query}\n"
            "注意: intent_sentence は実際に検索にかける代表文です。可能なら手続名や補助金名を具体化してください。"
        )

        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},  # JSON を強制
        )
        content = (resp.choices[0].message.content or "").strip()

        # 解析とログ出力
        try:
            data = json.loads(content)
        except Exception as e:
            logger.warning("IntentBuilder JSON parse failed: %s | raw=%s", e, content[:300].replace("\n", " "))
            # フォールバック（followup をログに出すため定型文を入れる）
            data = {
                "intent_sentence": user_query,
                "target_labels": [],
                "service_labels": [],
                "confidence": 0.0,
                "followup": "どのような種類のサービス（例：補助金、手続き、相談、求人等）をお探しですか？",
            }

        # 既定値補強
        intent_sentence = data.get("intent_sentence") or user_query
        target_labels = data.get("target_labels", []) or []
        service_labels = data.get("service_labels", []) or []
        confidence = data.get("confidence", 0.0)
        followup = data.get("followup", None)

        # 型整形
        if isinstance(confidence, str):
            try:
                confidence = float(confidence)
            except Exception:
                confidence = 0.0

        # ★ ここで「UIには出さずに」ログ出力する
        # followup があればそのまま、なければ「検索用にこう解釈しました：intent_sentence」
        if followup:
            logger.info("[IntentBuilder msg] %s", str(followup))
        else:
            logger.info('[IntentBuilder msg] 検索用にこう解釈しました：「%s」', intent_sentence)

        # 参考ログ（デバッグ用に要約も出す）
        logger.info(
            "IntentBuilder summary: sentence='%s' conf=%.2f targets=%s services=%s",
            intent_sentence, confidence, target_labels, service_labels
        )

        # 呼び出し側が使えるように返却（UI 表示はしない）
        return {
            "intent_sentence": intent_sentence,
            "target_labels": target_labels,
            "service_labels": service_labels,
            "confidence": confidence,
            "followup": followup,
        }

