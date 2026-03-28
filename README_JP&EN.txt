================================================================
  Issue Tracker
  Flask ベースの課題管理 Web アプリケーション
  Flask-Based Issue Tracking Web Application
================================================================


■ 開発背景 / Development Background
----------------------------------------------------------------
[JP]
イシュー管理ツールを一から実装することで、基礎的なウェブ開発について学ぶために作成しました。
現在アップロードされているこのバージョンは一切のテストを経ておらず、正常に動作しません。
これから修正と追加的な開発が必要です。

[EN]
This project was created to understand basic web development by implementing an issue management tool from scratch.
The current version being uploaded has not done any testing and will not work properly.
Need to fix and develop after first commit.


■ プロジェクト概要 / Project Overview
----------------------------------------------------------------
[JP]
Flask と Python を使用して開発した課題（Issue）管理 Web アプリケーションです。
ユーザー認証（登録 / ログイン / ログアウト / 退会）と、
課題の作成・取得・更新・削除（CRUD）を 提供します。

※ 本プロジェクトは現在開発中であり、ローカル環境のみで動作します。
   本番環境へのデプロイには、今後となります。


[EN]
A web application for issue tracking, built with Flask and Python.
Provides user authentication (register / login / logout / delete account)
and full CRUD operations for issues.

※ This project is currently under development and runs in local environments only.
   Additional feature implementation are required before production deployment.


■ フォルダ構成 / Folder Structure
----------------------------------------------------------------
Flask_Project/
├── app.py                  # App factory & server entry point
├── config.py               # Environment variables & app config
├── controllers/            # URL routing & HTTP request handling
│   ├── auth_controller.py
│   └── issue_controller.py
├── services/               # Business logic layer
│   ├── user_service.py
│   └── issue_service.py
├── models/                 # DB connection & data models
│   ├── database.py
│   └── users.py
├── templates/              # Jinja2 HTML templates
└── .env.example            # Credential template


■ インストール方法 / Installation
----------------------------------------------------------------
[JP]
1. リポジトリをクローン
   git clone https://github.com/LOVEFRIEDCHICKEN/Issue_Tracker.git
   cd Flask_Project

2. 仮想環境の作成と有効化
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux

3. パッケージのインストール
   pip install -r requirements.txt

4. 環境変数の設定
   .env.example をコピーして .env ファイルを作成し、
   MySQL の接続情報と SECRET_KEY を入力してください。

   cp .env.example .env

   SECRET_KEY の生成方法：
   python -c "import os; print(repr(os.urandom(24)))"

   次に .env ファイルのバリューを自分の環境に合わせて修正
   SECRET_KEY=your-key

   MYSQL_HOST=localhost_or_hostname
   MYSQL_USER=root_or_username
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_db_name

5. MySQL データベースの作成
   CREATE DATABASE flask_issue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

   cmdから 下の コマンド実行
   1. cd (ダウンロードした経路)
      ※ ex) cd C:\Users\(username)\PycharmProjects\Issue_Tracker
   2. mysql -u (username) -p flask_issue_db < schema.sql

[EN]
1. Clone the repository
   git clone https://github.com/{username}/Flask_Project.git
   cd Flask_Project

2. Create and activate a virtual environment
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux

3. Install dependencies
   pip install -r requirements.txt

4. Configure environment variables
   Copy .env.example to .env and fill in your MySQL credentials and SECRET_KEY.

   cp .env.example .env

   To generate a SECRET_KEY:
   python -c "import os; print(repr(os.urandom(24)))"

   Then need to fix .env file's detail value on your environment
   SECRET_KEY=your-key

   MYSQL_HOST=localhost_or_hostname
   MYSQL_USER=root_or_username
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_db_name

5. Create the MySQL database
   CREATE DATABASE flask_issue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

   From cmd window
   1. cd (download folder address)
      ※ ex) cd C:\Users\(username)\PycharmProjects\Issue_Tracker
   2. mysql -u (username) -p flask_issue_db < schema.sql


■ 実行方法 / How to Run
----------------------------------------------------------------
[JP]
   python app.py

   起動後、以下の URL にアクセスしてください。
   - ホーム     : http://127.0.0.1:5000/
   - ユーザー登録: http://127.0.0.1:5000/auth/register
   - ログイン   : http://127.0.0.1:5000/auth/login

[EN]
   python app.py

   After starting the server, access the following URLs:
   - Home     : http://127.0.0.1:5000/
   - Register : http://127.0.0.1:5000/auth/register
   - Login    : http://127.0.0.1:5000/auth/login


■ 主な機能 / Key Features
----------------------------------------------------------------
[JP]
- ユーザー登録 / ログイン / ログアウト / アカウント削除
- 課題の作成・全件取得・個別取得
- 課題ステータスの更新・削除
- キーワードによる課題検索
- セッションベースのログイン維持（1時間）

[EN]
- User register / login / logout / account deletion
- Issue creation, list retrieval, single retrieval
- Issue status update and deletion
- Keyword-based issue search
- Session-based login persistence (1 hour)


■ 今後の実装予定 / Planned Features
----------------------------------------------------------------
[JP]
- 各ページの UI/UX デザイン改善
- 課題担当者（Assignee）指定機能
- 課題デッドライン表示機能

[EN]
- UI/UX design improvements for each page
- Issue assignee designation feature
- Issue deadline display feature


■ 技術スタック / Tech Stack
----------------------------------------------------------------
[JP]
- バックエンド : Python 3.10, Flask 3.1
- データベース : MySQL
- 認証         : Flask-Login, Werkzeug（パスワードハッシュ化）
- その他       : Flask-CORS, python-dotenv

[EN]
- Backend  : Python 3.10, Flask 3.1
- Database : MySQL
- Auth     : Flask-Login, Werkzeug (password hashing)
- Others   : Flask-CORS, python-dotenv

================================================================