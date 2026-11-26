# 🌍 インターネット公開ガイド

## 現在の状態

**現在はローカルネットワーク内でのみ共有可能**（`http://192.168.11.9:8501`）

インターネットからアクセスするには、以下の方法があります：

---

## 🚀 方法1: ngrok（最も簡単・迅速）

### インストール
```bash
# macOS
brew install ngrok

# または直接ダウンロード
# https://ngrok.com/download
```

### 使用方法
```bash
# ポート8501を公開
ngrok http 8501
```

### 出力例
```
Forwarding    https://xxxx-xx-xxx-xxx-xxx.jp.ngrok-free.app -> http://localhost:8501
```

**このURLを世界中の誰とでも共有できます！**

---

## ☁️ 方法2: Streamlit Community Cloud（無料）

### 手順
1. GitHubにコードをプッシュ
2. [https://share.streamlit.io/](https://share.streamlit.io/) でアカウント作成
3. リポジトリを選択してデプロイ
4. 環境変数を設定（OPENAI_API_KEY）

### メリット
- ✅ **完全無料**
- ✅ **HTTPS自動**
- ✅ **永続的**
- ✅ **再起動不要**

### デメリット
- ❌ 認証機能なし（誰でもアクセス可能）
- ❌ リソース制限あり

---

## ☁️ 方法3: Google Cloud Run

### 手順
```bash
# Dockerfile確認
cat SearchWebAPP/Dockerfile

# Cloud Runにデプロイ
gcloud run deploy searchwebapp \
  --source SearchWebAPP \
  --port 8501 \
  --allow-unauthenticated

# 環境変数設定
gcloud run services update searchwebapp \
  --set-env-vars="OPENAI_API_KEY=your-key"
```

### メリット
- ✅ スケーラブル
- ✅ HTTPS自動
- ✅ 使用量課金

---

## ☁️ 方法4: AWS EC2 / Lightsail

### 手順
1. EC2インスタンス作成
2. Dockerインストール
3. コードをアップロード
4. `docker compose up` 実行
5. セキュリティグループで8501ポート開放

### メリット
- ✅ 完全制御
- ✅ カスタマイズ可能

---

## ☁️ 方法5: Heroku

### 手順
```bash
cd SearchWebAPP

# Heroku CLIログイン
heroku login

# アプリ作成
heroku create your-app-name

# MySQLアドオン追加
heroku addons:create heroku-postgresql:hobby-dev

# デプロイ
git push heroku main

# 環境変数設定
heroku config:set OPENAI_API_KEY=your-key
```

---

## 🔒 セキュリティ推奨事項

### インターネット公開時
1. **HTTPSの使用**（Streamlit Cloud/ngrok/Cloud Runは自動）
2. **認証の追加**
3. **APIキーの保護**（.env使用）
4. **レート制限**
5. **ログ監視**

### 認証の追加方法
```python
# app/main.py に追加
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    {'usernames': {'user1': {'password': 'hashed_password'}}},
    'cookie_name',
    'signature_key'
)

name, authentication_status, username = authenticator.login('Login', 'main')
if not authentication_status:
    st.error('Please login')
    st.stop()
```

---

## 📊 各方法の比較

| 方法 | 難易度 | コスト | 認証 | 永続性 |
|------|--------|--------|------|--------|
| **ngrok** | ⭐ | 無料（制限あり） | ❌ | ⏱️ 一時的 |
| **Streamlit Cloud** | ⭐⭐ | 無料 | ❌ | ✅ 永続 |
| **Cloud Run** | ⭐⭐⭐ | 使用量課金 | 可 | ✅ 永続 |
| **AWS EC2** | ⭐⭐⭐⭐ | 月額$20〜 | 可 | ✅ 永続 |
| **Heroku** | ⭐⭐⭐ | 月額$7〜 | 可 | ✅ 永続 |

---

## 🎯 推奨

### 開発・デモ用途
→ **ngrok** または **Streamlit Cloud**

### 本番運用
→ **Cloud Run** または **AWS EC2**

### 予算重視
→ **Streamlit Cloud**（無料）

---

## 📝 次のステップ

最も簡単な方法から始める：

1. **ngrok をインストール**
2. **実行**: `ngrok http 8501`
3. **生成されたURLを共有**

または

1. **GitHubにプッシュ**
2. **Streamlit Cloud でデプロイ**
3. **環境変数を設定**

---

**最終更新**: 2025年11月3日

