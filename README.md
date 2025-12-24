# AI 사이드 허슬 어시스턴트

사용자 프로필을 기반으로 사이드 허슬을 추천하고 관리하는 AI 서비스입니다.

## 🚀 시작하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.0-flash
GOOGLE_API_VERSION=v1
LOG_LEVEL=INFO
```

### 3. 서버 실행

```bash
python -m app.main
```

서버가 `http://localhost:8000`에서 실행됩니다.

## 📡 API 엔드포인트

### AI 채팅

```bash
POST /api/chat
Content-Type: application/json

{
  "question": "안녕하세요! 사이드 허슬에 대해 조언해주세요.",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

## 🛠️ 기술 스택

- **Backend**: FastAPI, Python 3.12
- **AI**: Google Gemini (via `langchain_google_genai`)
- **아키텍처**: 헥사고날 아키텍처

## 🔧 주요 기능

- AI와의 대화를 통한 사이드 허슬 추천
- 사용자 프로필 기반 맞춤형 조언
- 확장 가능한 아키텍처

## 📞 지원

문제가 있거나 제안사항이 있으시면 이슈를 생성해주세요.
