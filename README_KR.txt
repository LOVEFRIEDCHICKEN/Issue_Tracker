================================================================
  Issue Tracker - Flask 기반 이슈 관리 웹 애플리케이션
================================================================


■ 개발 배경 / 동기
----------------------------------------------------------------
이슈 관리 도구를 직접 구현해보며 기초적인 웹 개발에 대해 알아보기 위해 제작했습니다.
현재 올라가는 이 버전은 아무런 테스트를 거치지 않은 버전으로 제대로 작동되지 않을 것입니다.
추가적인 수정과 개발이 필요합니다.


■ 프로젝트 개요
----------------------------------------------------------------
Flask와 Python을 기반으로 제작한 이슈 트래킹 웹 애플리케이션입니다.
사용자 인증(회원가입 / 로그인 / 로그아웃 / 탈퇴)과
이슈의 생성, 조회, 수정, 삭제(CRUD) 기능을 RESTful API 형태로 제공합니다.

※ 현재 개발 진행 중인 프로젝트로, 로컬 환경에서만 동작합니다.
   프로덕션 배포 전 추가적인 보안 설정 및 기능 구현이 필요합니다.


■ 폴더 구조
----------------------------------------------------------------
Flask_Project/
├── app.py                  # 앱 팩토리 및 서버 진입점
├── config.py               # 환경변수 및 앱 설정
├── controllers/            # URL 라우팅 및 HTTP 요청 처리
│   ├── auth_controller.py
│   └── issue_controller.py
├── services/               # 비즈니스 로직 레이어
│   ├── user_service.py
│   └── issue_service.py
├── models/                 # DB 연결 및 데이터 모델
│   ├── database.py
│   └── users.py
├── templates/              # Jinja2 HTML 템플릿
└── .env.example            # 환경변수 템플릿


■ 설치 방법
----------------------------------------------------------------
1. 저장소 클론
   git clone https://github.com/{username}/Flask_Project.git
   cd Flask_Project

2. 가상환경 생성 및 활성화
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux

3. 패키지 설치
   pip install -r requirements.txt

4. 환경변수 설정
   .env.example 파일을 복사하여 .env 파일을 생성한 후,
   본인의 MySQL 정보와 SECRET_KEY를 입력합니다.

   cp .env.example .env

   SECRET_KEY=랜덤키 (아래 명령어로 생성 가능)
   python -c "import os; print(repr(os.urandom(24)))"

5. MySQL 데이터베이스 생성
   MySQL에서 아래 명령어를 실행합니다.
   CREATE DATABASE flask_issue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


■ 실행 방법
----------------------------------------------------------------
   python app.py

   서버 실행 후 아래 URL로 접속합니다.
   - 홈        : http://127.0.0.1:5000/
   - 회원가입   : http://127.0.0.1:5000/auth/register
   - 로그인     : http://127.0.0.1:5000/auth/login


■ 주요 기능
----------------------------------------------------------------
- 회원가입/탈퇴, 로그인/아웃
- 이슈 생성, 전체 조회, 단건 조회
- 이슈 생성, 수정, 삭제, 검색
- 세션 기반 로그인 유지 (1시간)


■ 향후 개발 예정 기능
----------------------------------------------------------------
- 각 페이지 UI/UX 디자인 개선
- 이슈 담당자(Assignee) 지정 기능
- 이슈 데드라인 표기 기능
- 프로덕션 환경 배포 설정


■ 기술 스택
----------------------------------------------------------------
- Backend  : Python 3.10, Flask 3.1
- Database : MySQL
- Auth     : Flask-Login, Werkzeug (비밀번호 해싱)
- 기타     : Flask-CORS, python-dotenv
================================================================