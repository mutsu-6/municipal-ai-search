# 📤 GitHubプッシュ手順

## ✅ 現在の状況

**ローカルコミット完了** ✅
- コミットID: `37fe7f5`
- 変更内容: AI対話型自治体サービス検索システム

**プッシュエラー発生** ⚠️
- 原因: 403 Permission denied
- リポジトリ: dx-junkyard/odb-search

---

## 🔧 プッシュ手順

### 方法1: Personal Access Token（推奨）

1. **GitHubでトークン作成**
   - https://github.com/settings/tokens
   - "Generate new token (classic)"
   - スコープ: `repo` にチェック

2. **トークンを設定**
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/dx-junkyard/odb-search.git
   git push origin main
   ```

### 方法2: SSH認証

1. **SSH鍵を生成**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **公開鍵をGitHubに登録**
   - https://github.com/settings/keys
   - 公開鍵を追加

3. **リモートURLを変更**
   ```bash
   git remote set-url origin git@github.com:dx-junkyard/odb-search.git
   git push origin main
   ```

### 方法3: 管理者依頼

組織の管理者にプッシュ権限を依頼してください。

---

## 🚀 プッシュ後の次のステップ

### Streamlit Cloud デプロイ

1. **リポジトリ確認**
   - https://github.com/dx-junkyard/odb-search

2. **Streamlit Cloudでデプロイ**
   - https://share.streamlit.io/
   - リポジトリを選択
   - メインファイル: `SearchWebAPP/app/main.py`

3. **環境変数を設定**
   ```
   OPENAI_API_KEY=your-key
   LLM_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
   ```

4. **MySQLの設定**
   - Streamlit CloudではMySQLを使えないため、
   - 一時的にファイルベースの履歴管理に切り替えるか、
   - 外部MySQL（Cloud SQL等）を使用

---

## 📝 コミット内容

### 新規ファイル
- ✅ `.gitignore` - セキュリティ設定
- ✅ `INTERNET_SHARING_GUIDE.md` - デプロイガイド
- ✅ `QUICK_START.md` - クイックスタート
- ✅ `SHARING_INFO.md` - 共有情報
- ✅ `SearchWebAPP/app/db_utils.py` - データベースユーティリティ
- ✅ `SearchWebAPP/mysql/init/init.sql` - スキーマ定義
- ✅ `SearchWebAPP/.env.example` - 環境変数テンプレート

### 更新ファイル
- ✅ `README.md` - プロジェクト概要更新
- ✅ `SearchWebAPP/app/main.py` - 会話機能追加
- ✅ `SearchWebAPP/app/conversation_graph.py` - 誘導強化
- ✅ `SearchWebAPP/app/llm_utils.py` - コンテキスト追加
- ✅ `SearchWebAPP/app/requirements.txt` - 依存関係追加
- ✅ `SearchWebAPP/docker-compose.yaml` - MySQL追加
- ✅ `SearchWebAPP/static/catalog_json/*.json` - データ更新

---

## 🔒 セキュリティ確認

✅ `.env` ファイルは含まれていません
✅ `__pycache__/` は除外されています
✅ `mysql_data/` ボリュームは除外されています

---

**最終更新**: 2025年11月3日

