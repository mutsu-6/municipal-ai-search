"""OpenAI埋め込みAPIによるテキスト埋め込み生成ユーティリティ"""
import os
import numpy as np
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your-"):
    logger.error("OPENAI_API_KEY が正しく設定されていません。.env ファイルを確認してください。")
    raise ValueError("OPENAI_API_KEY が設定されていません。.env ファイルに正しいAPIキーを設定してください。")

client = OpenAI(api_key=api_key)
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
logger.info("OpenAI Embeddings API クライアントを初期化しました（モデル: %s）", EMBEDDING_MODEL)

def embed_text(text: str) -> np.ndarray:
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    embedding = response.data[0].embedding
    return np.array(embedding, dtype=np.float32)
