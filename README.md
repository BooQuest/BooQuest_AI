# AI 사이드 허슬 어시스턴트

사용자 프로필을 기반으로 사이드 허슬을 추천하고 관리하는 AI 서비스입니다.

## 🏗️ 아키텍처

### 헥사고날 아키텍처 (Hexagonal Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                     │
├─────────────────────────────────────────────────────────────┤
│  HTTP API  │  Storage  │  AI Services                    │
│  Adapters  │  Adapters │  Adapters                       │
├─────────────────────────────────────────────────────────────┤
│                 Application Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Use Cases  │  Input Ports  │  Output Ports              │
├─────────────────────────────────────────────────────────────┤
│                    Domain Layer                            │
├─────────────────────────────────────────────────────────────┤
│  Entities  │  Value Objects  │  Domain Services           │
└─────────────────────────────────────────────────────────────┘
```

### 서비스 구조

#### Python AI 서버 (현재)
- **역할**: AI 처리만 담당
- **통신**: HTTP API만 제공
- **기능**: 채팅 완성, 큰 임무 생성, 작은 임무 생성

#### Java 서버 (향후 구현 예정)
- **역할**: 사용자 관리, 실시간 통신
- **통신**: WebSocket + HTTP API
- **기능**: 실시간 채팅, 세션 관리, 사용자 인증

## 🚀 시작하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
CLOVA_X_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

### 3. 서버 실행

```bash
python -m app.main
```

서버가 `http://localhost:8000`에서 실행됩니다.

## 📡 API 엔드포인트

### HTTP API (Python AI 서버)

#### 사용자 프로필 기반 큰 임무 생성
```bash
POST /api/v1/big-tasks/generate
Content-Type: application/json

{
  "user_id": "user123",
  "age": 28,
  "gender": "male",
  "mbti": "INTJ",
  "personality": "분석적이고 체계적인 성격",
  "side_hustle_interests": ["프로그래밍", "교육", "마케팅"],
  "available_time_per_week": 20,
  "target_income_per_month": 500000,
  "current_skills": ["Python", "JavaScript"],
  "preferred_work_style": "remote",
  "risk_tolerance": "medium"
}
```

#### 채팅 완성 생성
```bash
POST /api/v1/chat/completions
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "안녕하세요! 사이드 허슬에 대해 조언해주세요."
    }
  ],
  "config": {
    "model": "clova-x",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

#### 대화 세션 생성
```bash
POST /api/v1/conversations
Content-Type: application/json

{
  "user_id": "user123",
  "big_task_id": "task_456",
  "title": "온라인 강의 제작 계획"
}
```

## 🧪 테스트

### HTTP API 테스트

```bash
# 큰 임무 생성 테스트
curl -X POST http://localhost:8000/api/v1/big-tasks/generate \
  -H "Content-Type: application/json" \
  -d @test_data/user_profile.json

# 채팅 완성 테스트
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "안녕하세요!"}],
    "config": {"model": "clova-x", "temperature": 0.7, "max_tokens": 1000}
  }'
```

## 📁 프로젝트 구조

```
app/
├── domain/                    # 도메인 계층
│   ├── entities/             # 엔티티
│   └── exceptions.py         # 도메인 예외
├── application/              # 애플리케이션 계층
│   ├── usecases/            # 유스케이스
│   └── ports/               # 포트 인터페이스
│       ├── input/           # 입력 포트
│       └── output/          # 출력 포트
├── adapters/                # 어댑터 계층
│   ├── input/               # 입력 어댑터
│   │   └── http/           # HTTP 어댑터
│   └── output/              # 출력 어댑터
│       ├── storage/         # 저장소 어댑터
│       └── ai/              # AI 서비스 어댑터
└── infrastructure/          # 인프라 계층
    ├── config.py           # 설정
    ├── logging.py          # 로깅
    └── dependency_injection.py # 의존성 주입
```

## 🔧 주요 기능

### 1. 사용자 프로필 기반 추천
- 개인 성향 분석 (MBTI, 성격)
- 보유 스킬 및 관심사 반영
- 목표 수익 및 시간 가용성 고려

### 2. AI 채팅 완성
- HTTP API 기반 채팅 완성
- 다양한 AI 모델 지원
- 응답 품질 최적화

### 3. 임무 관리
- 큰 임무 → 작은 임무 분해
- 진행 상황 추적
- 우선순위 설정

### 4. 확장 가능한 아키텍처
- 헥사고날 아키텍처로 유지보수성 향상
- 새로운 AI 모델 쉽게 교체 가능
- 다양한 저장소 지원

## 🛠️ 기술 스택

- **Backend**: FastAPI, Python 3.12
- **AI**: Clova X API
- **통신**: HTTP REST API
- **아키텍처**: 헥사고날 아키텍처
- **로깅**: Python logging
- **의존성 주입**: 자체 구현 DI 컨테이너

## 📈 성능 특징

### HTTP API
- **AI 처리**: 사용자 요청에 대한 AI 응답 생성
- **데이터 관리**: CRUD 작업, 상태 조회
- **결과 저장**: 대화 완료 후 데이터 저장

## 🔒 보안 고려사항

- API 키 환경 변수 관리
- 입력 데이터 검증
- 에러 처리 및 로깅

## 🚧 향후 계획

- [ ] Java 서버와 연동
- [ ] 사용자 인증 시스템
- [ ] 데이터베이스 연동
- [ ] 더 많은 AI 모델 지원
- [ ] 모바일 앱 연동
- [ ] 실시간 협업 기능
- [ ] 분석 대시보드

## 📞 지원

문제가 있거나 제안사항이 있으시면 이슈를 생성해주세요.