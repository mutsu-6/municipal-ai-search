# odb-search
OpenData Bridgeで整形したデータ等を検索する機能

## 🌐 アクセス方法

### ローカルネットワーク
```
http://localhost:8501          # ローカルPCから
http://192.168.11.9:8501       # 同じネットワーク内のデバイスから
```

### インターネット公開方法
詳細は [INTERNET_SHARING_GUIDE.md](INTERNET_SHARING_GUIDE.md) を参照

**簡単な方法：**
```bash
# ngrokを使用（一時公開）
brew install ngrok
ngrok http 8501

# または Streamlit Cloud（永続的・無料）
# https://share.streamlit.io/
```

## 📚 ドキュメント

- **QUICK_START.md** - クイックスタートガイド
- **SHARING_INFO.md** - 共有方法と詳細情報
- **INTERNET_SHARING_GUIDE.md** - インターネット公開ガイド
- **SearchWebAPP/README.md** - 技術仕様とセットアップ

## 🚀 すぐに使う

```bash
cd SearchWebAPP
docker compose up
```

ブラウザで http://localhost:8501 を開く

## 📋 プロジェクト構成

```
odb-search/
├── SearchWebAPP/          # メインアプリケーション
├── QUICK_START.md         # クイックスタート
├── SHARING_INFO.md        # 共有情報
└── INTERNET_SHARING_GUIDE.md  # インターネット公開ガイド
```

## ✨ 機能

- AI対話型自治体サービス検索
- 会話履歴の永続化（MySQL）
- ユーザープロフィール管理
- 155件の国分寺市サービスデータ

## 📞 サポート

問題がある場合は `docker compose logs` でログを確認してください。
