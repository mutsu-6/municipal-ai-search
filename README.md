# 🏛️ Municipal AI Search

AI-powered municipal service search system with conversational interface.

[![Streamlit Cloud](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

## 🌐 アクセスリンク

### インターネット公開URL（Streamlit Cloud）
**デプロイ待ち**: https://municipal-ai-search.streamlit.app

### ローカル/ネットワーク
- **ローカル**: http://localhost:8501
- **ネットワーク**: http://192.168.11.9:8501

---

## ✨ Features

- 🤖 **AI Conversational Search** - Natural language interface using GPT-4o-mini
- 💬 **Continuous Conversation** - Remembers previous interactions
- 👤 **User Profile Management** - Learns user preferences
- 💾 **Persistent Storage** - MySQL database integration
- 🔍 **Smart Guidance** - LangGraph workflow for intelligent assistance
- 📊 **155 Municipal Services** - Comprehensive Kokubunji City service catalog

## 🚀 デプロイ手順（Streamlit Cloud）

### 1. Streamlit Cloudにアクセス
https://share.streamlit.io/ でログイン

### 2. アプリを作成
1. 「New app」をクリック
2. 以下を設定：
   - **Repository**: mutsu-6/municipal-ai-search
   - **Branch**: main
   - **Main file path**: `SearchWebAPP/app/main.py`

### 3. 環境変数を設定
Advanced settings → Secrets：
```toml
[secrets]
OPENAI_API_KEY = "あなたのAPIキー"
LLM_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
```

### 4. デプロイ実行
「Deploy!」をクリック → 完了！

詳細: [DEPLOY_NOW_STEPS.md](DEPLOY_NOW_STEPS.md)

---

## 🛠️ Local Development

### Docker
```bash
cd SearchWebAPP
docker compose up
```

Access: http://localhost:8501

### 直接実行
```bash
cd SearchWebAPP
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
streamlit run app/main.py
```

---

## 📚 Documentation

- **[DEPLOY_NOW_STEPS.md](DEPLOY_NOW_STEPS.md)** - Streamlit Cloudデプロイ手順
- **[STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)** - 詳細なデプロイガイド
- **[WHICH_LINK_TO_SHARE.md](WHICH_LINK_TO_SHARE.md)** - リンク共有ガイド
- **[QUICK_START.md](QUICK_START.md)** - クイックスタート
- **[SearchWebAPP/README.md](SearchWebAPP/README.md)** - 技術仕様

---

## 🏗️ Architecture

```
┌─────────────┐
│   Streamlit │
│  Frontend   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  LangGraph       │
│  Workflow        │
└──────┬───────────┘
       │
       ▼
┌─────────────────────┐
│  GPT-4o-mini        │
│  + Embeddings       │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐    ┌─────────┐
│  MySQL      │    │ Catalog │
│  Database   │    │ Search  │
└─────────────┘    └─────────┘
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.51.0
- **AI**: OpenAI GPT-4o-mini, text-embedding-ada-002
- **Database**: MySQL 8.0
- **Backend**: Python 3.11
- **Orchestration**: LangGraph
- **Container**: Docker Compose

## 🔒 Environment Variables

```env
OPENAI_API_KEY=your-key
LLM_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=searchapp
```

## 📊 Data Source

- **Municipality**: Kokubunji City
- **Services**: 155 indexed services
- **Data Format**: JSON
- **Source**: https://www.city.kokubunji.tokyo.jp/

## 📝 License

See [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for better municipal service access**
