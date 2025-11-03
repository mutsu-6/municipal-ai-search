# 🏛️ Municipal AI Search

AI-powered municipal service search system with conversational interface.

[![Streamlit Cloud](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

## ✨ Features

- 🤖 **AI Conversational Search** - Natural language interface using GPT-4o-mini
- 💬 **Continuous Conversation** - Remembers previous interactions
- 👤 **User Profile Management** - Learns user preferences
- 💾 **Persistent Storage** - MySQL database integration
- 🔍 **Smart Guidance** - LangGraph workflow for intelligent assistance
- 📊 **155 Municipal Services** - Comprehensive Kokubunji City service catalog

## 🚀 Quick Start

### Local Development

```bash
cd SearchWebAPP
docker compose up
```

Access at: http://localhost:8501

### Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Select your repository
4. Main file: `SearchWebAPP/app/main.py`
5. Set environment variables
6. Deploy!

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started quickly
- **[SHARING_INFO.md](SHARING_INFO.md)** - Sharing and deployment info
- **[INTERNET_SHARING_GUIDE.md](INTERNET_SHARING_GUIDE.md)** - Internet deployment guide
- **[NEW_REPOSITORY_GUIDE.md](NEW_REPOSITORY_GUIDE.md)** - Create new repo guide
- **[SearchWebAPP/README.md](SearchWebAPP/README.md)** - Technical specifications

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

## 🤝 Contributing

Contributions welcome! Please read the documentation first.

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini and embeddings
- Streamlit for the framework
- Kokubunji City for open data

---

**Made with ❤️ for better municipal service access**
