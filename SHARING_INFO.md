# 自治体サービス検索システム - 共有情報

## 🌐 共有リンク

### ローカルアクセス
**ローカルマシンからアクセス:**
```
http://localhost:8501
```

### ネットワーク共有
**同じネットワーク内の他のデバイスからアクセス:**
```
http://192.168.11.9:8501
```

## 📱 使用方法

### ブラウザでアクセス
1. 上記のURLをブラウザで開く
2. 質問を入力して送信
3. AIが適切な自治体サービスを案内

### 機能
- ✅ AI対話型検索
- ✅ 会話を通じた情報収集
- ✅ ユーザープロフィール管理
- ✅ MySQL永続化
- ✅ 検索履歴・フィードバック保存

## 🔧 技術スタック

- **Frontend**: Streamlit
- **Backend**: Python 3.11
- **Database**: MySQL 8.0
- **AI**: OpenAI GPT-4o-mini (会話) + text-embedding-ada-002 (検索)
- **Container**: Docker Compose

## 🌍 外部共有方法

### 1. SSH トンネル（推奨）
```bash
ssh -L 8501:localhost:8501 user@192.168.11.9
```
その後、リモートマシンで `http://localhost:8501` にアクセス

### 2. クラウドデプロイ

#### Streamlit Cloud
1. GitHubにプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud) でデプロイ
3. 環境変数を設定（OPENAI_API_KEYなど）

#### Heroku
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### AWS/GCP/Azure
- EC2/Compute Engine/VMでのホスティング
- セキュリティグループでポート8501を開放

### 3. ngrok で一時公開
```bash
ngrok http 8501
```
生成されたURLを共有

## ⚠️ セキュリティ注意事項

1. **本番環境での使用:**
   - `.env`ファイルの管理
   - APIキーの保護
   - HTTPSの使用（推奨）
   - ファイアウォール設定

2. **データ保護:**
   - MySQL認証情報の変更
   - セッション管理の強化
   - ログファイルの定期的な削除

## 📊 現在のステータス

- **稼働状態**: ✅ 正常稼働中
- **データベース**: ✅ MySQL接続成功
- **AI機能**: ✅ OpenAI API接続成功
- **利用可能サービス**: 155件

## 📝 データソース

- **自治体**: 国分寺市 (https://www.city.kokubunji.tokyo.jp/)
- **サービス数**: 155件
- **データ形式**: JSON

## 📞 サポート

問題が発生した場合:
1. ログを確認: `docker compose logs app`
2. データベース状態確認: `docker compose logs mysql`
3. 再起動: `docker compose restart`

---

**最終更新**: 2025年11月3日
**バージョン**: 1.0.0

