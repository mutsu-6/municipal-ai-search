# ☁️ Streamlit Cloud デプロイ手順

## 🎯 重要: まずデプロイが必要です！

現在 **https://municipal-ai-search.streamlit.app** が開けないのは、
**まだデプロイしていないため** です。

---

## 🚀 Streamlit Cloudデプロイ手順（詳細版）

### ステップ1: Streamlit Cloud にアクセス

1. **https://share.streamlit.io/** を開く
2. **「Sign in with GitHub」** をクリック
3. GitHubアカウントで認証

### ステップ2: 新しいアプリを作成

1. **「New app」** ボタンをクリック
2. **「From existing repo」** を選択

### ステップ3: リポジトリ情報を入力

- **Repository URL**: `mutsu-6/municipal-ai-search`
- **Branch**: `main`
- **Main file path**: `SearchWebAPP/app/main.py` ⚠️ **重要！**

### ステップ4: Advanced settings

「Advanced settings」を開いて以下を設定：

#### 環境変数追加
```
OPENAI_API_KEY=your-actual-openai-api-key-here
LLM_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
```

⚠️ **OPENAI_API_KEY は実際のAPIキーを設定してください！**

### ステップ5: デプロイ実行

1. **「Deploy!」** ボタンをクリック
2. 数分待機（初回は5-10分かかることがあります）
3. ログを確認

---

## 🔍 デプロイ後の確認

### 成功した場合
- 「Your app is live!」と表示
- **公開URLが表示される**: `https://municipal-ai-search.streamlit.app`
- このURLを共有できる！

### エラーが発生した場合

#### よくあるエラーと対処法

**1. ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'conversation_graph'
```
→ Main file path が間違っています
→ 正しいパス: `SearchWebAPP/app/main.py`

**2. Environment variable not found**
```
OPENAI_API_KEY が見つかりません
```
→ Advanced settings で環境変数を設定してください

**3. Database connection error**
```
MySQLに接続できない
```
→ Streamlit Cloudでは外部DBを使用する必要があります
→ 一時的にDB機能を無効化するか、外部MySQLを使用

**4. Import エラー**
```
from conversation_graph import ...
```
→ ファイルが不足している可能性
→ GitHubに全ファイルがプッシュされているか確認

---

## 📊 必要なファイル確認

Streamlit Cloudで動作するために必要なファイル：

✅ **必須**:
- `SearchWebAPP/app/main.py`
- `SearchWebAPP/app/catalog_utils.py`
- `SearchWebAPP/app/conversation_graph.py`
- `SearchWebAPP/app/embed_utils.py`
- `SearchWebAPP/app/llm_utils.py`
- `SearchWebAPP/app/db_utils.py`
- `SearchWebAPP/app/requirements.txt`
- `SearchWebAPP/static/catalog_json/service_catalog.json`
- `SearchWebAPP/static/catalog_json/overview_embeddings.json`
- `.streamlit/config.toml`

---

## 🔧 トラブルシューティング

### ログを確認

Streamlit Cloudのダッシュボードで：
1. アプリを選択
2. 「Manage app」→「Logs」
3. エラーメッセージを確認

### よくある問題

**Q: 「App not found」が表示される**
A: まだデプロイしていません。上記手順でデプロイしてください。

**Q: デプロイが失敗する**
A: ログを確認してエラーメッセージを見てください。

**Q: OpenAI APIエラー**
A: 環境変数に正しいAPIキーを設定してください。

**Q: import エラー**
A: Main file path が正しいか確認してください。

---

## 🎉 デプロイ成功後

デプロイが成功すると：

1. **公開URL が発行される**
   ```
   https://municipal-ai-search.streamlit.app
   ```

2. **このURLを共有できる**
   - 世界中の誰でもアクセス可能
   - HTTPS自動
   - 24時間稼働

3. **自動更新**
   - GitHubにプッシュすると自動デプロイ
   - 再起動不要

---

## 📝 チェックリスト

デプロイ前に確認：

- [ ] GitHubに全ファイルがプッシュされている
- [ ] Main file path が正しい: `SearchWebAPP/app/main.py`
- [ ] 環境変数が設定されている（OPENAI_API_KEY必須）
- [ ] requirements.txt が最新
- [ ] .streamlit/config.toml が存在する

---

## 🔗 参考リンク

- Streamlit Cloud: https://share.streamlit.io/
- ドキュメント: https://docs.streamlit.io/streamlit-community-cloud
- リポジトリ: https://github.com/mutsu-6/municipal-ai-search

---

**🎯 結論: https://share.streamlit.io/ でデプロイしてください！**

