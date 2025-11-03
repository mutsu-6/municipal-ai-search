"""Database utilities for SearchWebAPP."""
import os
import logging
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
import pymysql
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# データベース接続情報
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "searchapp"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


@contextmanager
def get_db_connection():
    """データベース接続のコンテキストマネージャー"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        logger.exception("Database error: %s", e)
        raise
    finally:
        if connection:
            connection.close()


def ensure_session(session_id: str) -> bool:
    """セッションが存在することを確認し、なければ作成"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # セッションが存在するか確認
                cursor.execute(
                    "SELECT session_id FROM sessions WHERE session_id = %s",
                    (session_id,)
                )
                if not cursor.fetchone():
                    # 新規セッションを作成
                    cursor.execute(
                        "INSERT INTO sessions (session_id) VALUES (%s)",
                        (session_id,)
                    )
                return True
    except Exception as e:
        logger.exception("Failed to ensure session: %s", e)
        return False


def save_conversation(session_id: str, role: str, message: str) -> bool:
    """会話履歴をデータベースに保存"""
    try:
        ensure_session(session_id)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO conversations (session_id, role, message) VALUES (%s, %s, %s)",
                    (session_id, role, message)
                )
                return True
    except Exception as e:
        logger.exception("Failed to save conversation: %s", e)
        return False


def get_conversation_history(session_id: str, limit: int = 100) -> List[Tuple[str, str]]:
    """会話履歴を取得"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT role, message FROM conversations WHERE session_id = %s ORDER BY created_at DESC LIMIT %s",
                    (session_id, limit)
                )
                results = cursor.fetchall()
                # タプル形式に変換（(role, message)）
                history = [(row["role"], row["message"]) for row in results]
                # 時系列順に戻す
                history.reverse()
                return history
    except Exception as e:
        logger.exception("Failed to get conversation history: %s", e)
        return []


def save_search_query(
    session_id: str,
    query: str,
    intent_sentence: str = None,
    intent_confidence: float = None,
    target_labels: List[str] = None,
    service_labels: List[str] = None,
    results_count: int = None
) -> Optional[int]:
    """検索クエリを保存し、IDを返す"""
    try:
        ensure_session(session_id)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # JSON形式でラベルを保存
                import json
                target_labels_json = json.dumps(target_labels) if target_labels else None
                service_labels_json = json.dumps(service_labels) if service_labels else None
                
                cursor.execute(
                    """INSERT INTO search_queries 
                    (session_id, query, intent_sentence, intent_confidence, target_labels, service_labels, results_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (session_id, query, intent_sentence, intent_confidence, 
                     target_labels_json, service_labels_json, results_count)
                )
                return cursor.lastrowid
    except Exception as e:
        logger.exception("Failed to save search query: %s", e)
        return None


def save_feedback(
    session_id: str,
    feedback_type: str,
    search_query_id: int = None,
    feedback_text: str = None
) -> bool:
    """フィードバックを保存"""
    try:
        ensure_session(session_id)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO feedbacks (session_id, search_query_id, feedback_type, feedback_text) VALUES (%s, %s, %s, %s)",
                    (session_id, search_query_id, feedback_type, feedback_text)
                )
                return True
    except Exception as e:
        logger.exception("Failed to save feedback: %s", e)
        return False


def save_service_click(
    session_id: str,
    service_title: str,
    service_url: str,
    search_query_id: int = None
) -> bool:
    """サービスクリックを記録"""
    try:
        ensure_session(session_id)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO service_clicks (session_id, search_query_id, service_title, service_url) VALUES (%s, %s, %s, %s)",
                    (session_id, search_query_id, service_title, service_url)
                )
                return True
    except Exception as e:
        logger.exception("Failed to save service click: %s", e)
        return False


def get_popular_services(limit: int = 10) -> List[Dict[str, Any]]:
    """人気のサービスを取得（クリック数が多い順）"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT service_title, service_url, COUNT(*) as click_count
                    FROM service_clicks
                    GROUP BY service_title, service_url
                    ORDER BY click_count DESC
                    LIMIT %s""",
                    (limit,)
                )
                return cursor.fetchall()
    except Exception as e:
        logger.exception("Failed to get popular services: %s", e)
        return []


def test_db_connection() -> bool:
    """データベース接続をテスト"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
    except Exception as e:
        logger.error("Database connection test failed: %s", e)
        return False

