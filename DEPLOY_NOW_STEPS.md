# 🚀 Streamlit Cloud デプロイ実行手順

## ✅ 今すぐデプロイする手順

**Streamlit Cloudは手動でデプロイする必要があります。** 
以下の手順を**今すぐ**実行してください：

---

## 📋 実行手順（ブラウザで）

### ステップ1: Streamlit Cloud を開く ⏰ 1分

1. **https://share.streamlit.io/** にアクセス
2. **「Sign in with GitHub」** をクリック
3. あなたのGitHubアカウント（mutsu-6）でログイン

### ステップ2: アプリを作成 ⏰ 2分

1. **「New app」** ボタンをクリック
2. 以下を入力：

**基本設定:**
- Repository: **mutsu-6/municipal-ai-search** （ドロップダウンから選択）
- Branch: **main**
- Main file path: **SearchWebAPP/app/main.py**

**⚠️ 重要**: Main file path を入力してください！

### ステップ3: 環境変数を設定 ⏰ 2分

1. 右側の **「Advanced settings」** をクリック
2. **「Secrets」** タブを開く
3. 以下の形式で入力：

```toml
[secrets]
OPENAI_API_KEY = "あなたのOpenAIのAPIキー"
LLM_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
```

**例:**
```toml
[secrets]
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxxx"
LLM_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
```

⚠️ **OPENAI_API_KEY は実際のAPIキーを設定してください！**

### ステップ4: デプロイ実行 ⏰ 1分

1. **「Deploy!」** ボタンをクリック
2. 数分待機（5-10分かかる場合があります）

### ステップ5: 完了確認 ⏰ 1分

1. ログを確認
2. 「Your app is live!」と表示されたら成功
3. **公開URLをコピー**

---

## 🎉 デプロイ成功！

以下のようなURLが表示されます：

```
https://municipal-ai-search.streamlit.app
```

このURLを **世界中の誰とでも共有できます！**

---

## ⚠️ エラーが出た場合

### エラー1: ModuleNotFoundError

**症状**: `No module named 'conversation_graph'`

**解決方法**:
- Main file path を確認
- 正しくは: **`SearchWebAPP/app/main.py`**

### エラー2: API Key エラー

**症状**: `OPENAI_API_KEY が見つかりません`

**解決方法**:
- Advanced settings → Secrets を確認
- APIキーが正しく入力されているか確認

### エラー3: Database エラー

**症状**: MySQL接続エラー

**解決方法**:
- Streamlit CloudではMySQLが使えません
- 自動的にDBなしモードで動作します
- 問題ありません

### エラー4: ファイルが見つからない

**症状**: `FileNotFoundError`

**解決方法**:
- GitHubに全ファイルがプッシュされているか確認
- https://github.com/mutsu-6/municipal-ai-search で確認

---

## 📊 チェックリスト

デプロイ前に確認：

- [ ] GitHubにログイン済み
- [ ] リポジトリが選択されている: mutsu-6/municipal-ai-search
- [ ] Branch: main
- [ ] Main file path: SearchWebAPP/app/main.py
- [ ] OpenAI APIキーを設定した
- [ ] 「Deploy!」をクリックした

---

## 🔗 参考リンク

- Streamlit Cloud: https://share.streamlit.io/
- あなたのリポジトリ: https://github.com/mutsu-6/municipal-ai-search
- OpenAI APIキー取得: https://platform.openai.com/api-keys

---

## ⏱️ 所要時間

**約10分**で完了します！

1. ログイン: 1分
2. 設定: 3分
3. デプロイ: 5-10分
4. **合計: 約10分**

---

**🎯 今すぐ https://share.streamlit.io/ でデプロイを開始してください！**

