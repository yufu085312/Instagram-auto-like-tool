# Instagram 自動化ツール

このツールは、Selenium を使用して Instagram のハッシュタグ検索や投稿操作（いいね、保存、シェア）を自動化するために設計されています。

## 必要な環境

### 動作環境
- OS: Windows, macOS, Linux
- Python: 3.9以上
- ブラウザ: Google Chrome 最新版

### 必要なライブラリ
以下のライブラリをインストールしてください。

```bash
pip install selenium webdriver-manager
```


---

## プロジェクト構造

```
project/
├── main.py                   # メインエントリーポイント
├── config/
│   ├── accounts.json         # アカウント情報（ユーザー名・パスワードなど）
│   ├── schedule.txt          # 実行時間の設定ファイル
│   └── cookies/              # クッキー情報の保存ディレクトリ
├── logs/
│   └── execution.log         # 実行ログ
├── utils/
│   ├── login.py              # ログイン関連のコード
│   ├── hashtag_search.py     # ハッシュタグ検索関連のコード
│   ├── post_interaction.py   # 投稿のいいね・保存・シェアのコード
|   ├── driver_setup.py       # 
│   └── schedule_manager.py   # 実行スケジュール関連のコード
├── requirements.txt          # 必要なライブラリ一覧
└── README.md                 # プロジェクトの説明
```

---

## セットアップ手順

### 1. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. アカウント情報の設定

`config/accounts.json` に以下の形式でアカウント情報を記述してください。

```json
[
    {
        "username": "account1",
        "password": "password1"
    },
    {
        "username": "account2",
        "password": "password2"
    }
]
```

### 3. 実行時間の設定

`config/schedule.txt` に実行したい時間を記述してください。フォーマットは 24時間制です。

例:
```
12:00
```

### 4. クッキーの準備

- 一度手動でログインし、ブラウザのクッキーを取得して `config/cookies/` ディレクトリに保存してください。
- 保存ファイル名は `<username>_cookies.json` にしてください。

---

## 実行方法

以下のコマンドを実行してツールを起動します。

```bash
python main.py
```

---

## 実装されている機能

1. **ログイン処理**
   - 事前に保存したクッキーを使用して自動ログインします。

2. **ハッシュタグ検索**
   - 指定したハッシュタグで検索し、投稿をスクロールして収集します。

3. **投稿の抽出**
   - 最新の投稿のみ（3時間以内の投稿）をフィルタリングします。

4. **いいね、保存、シェア操作**
   - 抽出した投稿に対して、順番にいいね、保存、シェアを行います。

5. **ログ記録**
   - 実行状況を `logs/execution.log` に記録します。

---

## 注意事項

1. **Instagramの利用規約を遵守**
   - 過度な自動化はアカウント停止のリスクがあります。適切なスリープタイムを設定してください。

2. **CAPTCHAやセキュリティ対応**
   - ログイン時に CAPTCHA が表示される場合は、手動で対応してください。

3. **IPアドレスの管理**
   - 同一IPアドレスからの過剰な操作はアカウントロックの原因となる可能性があります。

4. **ブラウザの最新版を使用**
   - Selenium とブラウザのバージョンが一致していることを確認してください。
