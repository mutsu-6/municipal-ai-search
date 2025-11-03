# 🚀 新しいGitHubリポジトリ作成ガイド

## 📋 現在の状況

✅ **ローカルコミット完了**
- コミットID: `aa4d4e2`
- 変更: AI対話型自治体サービス検索システム
- 2つのコミットがローカルに存在

⚠️ **既存リポジトリ**: `dx-junkyard/odb-search`（権限なし）

---

## 🎯 推奨手順: 新しいリポジトリを作成

### ステップ1: GitHubで新しいリポジトリ作成

1. **GitHubにアクセス**
   - https://github.com/ にログイン

2. **新しいリポジトリを作成**
   - 右上の「+」→「New repository」
   - リポジトリ名: `municipal-ai-search` またはお好みの名前
   - 説明: `AI-powered municipal service search with conversation features`
   - Public/Private を選択
   - ⚠️ **「Initialize with README」はチェックしない**（既にローカルにコードがあるため）

3. **「Create repository」をクリック**

---

### ステップ2: リモートURLを変更してプッシュ

ターミナルで以下を実行：

```bash
cd /Users/mutsuk/Desktop/odb-search

# 既存のリモートを削除
git remote remove origin

# 新しいリモートを追加（YOUR_USERNAMEを置き換える）
git remote add origin https://github.com/YOUR_USERNAME/municipal-ai-search.git

# プッシュ
git push -u origin main
```

---

### ステップ3: Streamlit Cloudでデプロイ

プッシュ完了後：

1. **Streamlit Cloud にアクセス**
   - https://share.streamlit.io/
   - GitHubアカウントでログイン

2. **デプロイ設定**
   - 「New app」
   - Repository: `YOUR_USERNAME/municipal-ai-search`
   - Branch: `main`
   - Main file: `SearchWebAPP/app/main.py`

3. **環境変数を設定**
   ```
   OPENAI_API_KEY=your-openai-api-key
   LLM_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
   ```

4. **デプロイ**
   - 「Deploy!」をクリック
   - 数分で完了
   - **公開URLが表示される**

---

## 🔗 共有リンク

デプロイ完了後、以下のようなURLが生成されます：

```
https://municipal-ai-search.streamlit.app
```

このURLを世界中の誰とでも共有できます！

---

## 📊 コミット内容

### 新規ファイル
- `.gitignore` - セキュリティ設定
- `INTERNET_SHARING_GUIDE.md` - デプロイガイド
- `QUICK_START.md` - クイックスタート
- `SHARING_INFO.md` - 共有情報
- `SearchWebAPP/app/db_utils.py` - データベースユーティリティ
- `SearchWebAPP/mysql/init/init.sql` - MySQLスキーマ
- `SearchWebAPP/.env.example` - 環境変数テンプレート

### 更新ファイル
- `README.md` - プロジェクト概要
- `SearchWebAPP/app/main.py` - AI対話機能
- `SearchWebAPP/app/conversation_graph.py` - 会話誘導
- `SearchWebAPP/app/llm_utils.py` - コンテキスト管理
- `SearchWebAPP/app/requirements.txt` - 依存関係
- `SearchWebAPP/docker-compose.yaml` - MySQL統合

---

## ✨ 完成後の機能

- ✅ AI対話型検索
- ✅ 継続的な会話
- ✅ ユーザープロフィール管理
- ✅ 会話履歴の永続化
- ✅ 155件の自治体サービス

---

**参考リンク:**
- GitHub公式ドキュメント: https://docs.github.com/ja/repositories/creating-and-managing-repositories/creating-a-new-repository
- Streamlit Cloud: https://share.streamlit.io/

