# SNS 트렌드 RSS 크롤링 시스템

SNS 트렌드에 특화된 RSS 피드 크롤링 시스템입니다. 다양한 뉴스 소스에서 SNS, 마케팅, 기술 트렌드 관련 정보를 수집하여 벡터 데이터베이스에 저장합니다.

## 🎯 주요 기능

- **SNS 트렌드 특화**: Instagram, TikTok, YouTube, Facebook, Twitter 등 SNS 관련 뉴스만 필터링
- **다양한 소스**: Social Media Today, Marketing Land, TechCrunch, Entrepreneur 등 20개 RSS 피드
- **지능형 필터링**: 키워드 기반 SNS 관련성 자동 판별
- **벡터 검색**: PostgreSQL pgvector를 활용한 유사도 검색
- **주간 자동화**: 매주 월요일 오전 2시 자동 크롤링

## 🏗️ 시스템 구조

```
RSS 피드들 → RSSCrawler → SNS 관련성 필터링 → 임베딩 생성 → PostgreSQL pgvector 저장
```

### 핵심 컴포넌트

- **RSSCrawler**: SNS 트렌드에 특화된 RSS 크롤러
- **TrendStorageService**: 벡터 데이터베이스 저장 및 검색
- **Celery 태스크**: 주간 자동 크롤링 스케줄링

## 📊 RSS 피드 소스

### Social Media Trends
- Social Media Today
- Hootsuite Blog
- Sprout Social Insights
- Buffer Resources
- Twitter Blog

### Marketing Trends
- Marketing Land
- MarketingProfs
- Content Marketing Institute
- Neil Patel
- HubSpot Marketing Blog

### Tech Trends
- TechCrunch
- VentureBeat
- The Verge
- Mashable
- Wired

### Startup Trends
- Entrepreneur
- Inc.com
- Fast Company
- Forbes Innovation
- Business Insider

## 🔍 SNS 트렌드 필터링

### 키워드 기반 필터링
- **플랫폼**: instagram, tiktok, youtube, facebook, twitter, linkedin
- **콘텐츠**: influencer, viral, trending, hashtag, content creator
- **마케팅**: digital marketing, social commerce, social selling
- **한국어**: 부업, 사이드잡, 인플루언서, 크리에이터, 소셜미디어

### 트렌드 타입 자동 분류
- `instagram_trend`: Instagram 관련
- `tiktok_trend`: TikTok 관련
- `youtube_trend`: YouTube 관련
- `influencer_trend`: 인플루언서 관련
- `marketing_trend`: 마케팅 관련
- `startup_trend`: 스타트업/부업 관련
- `general_sns_trend`: 일반 SNS 관련

## 🚀 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
# config/.env 파일에 다음 설정 추가
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
VECTOR_SIMILARITY_THRESHOLD=0.7
```

### 3. 데이터베이스 초기화

```bash
# PostgreSQL에 pgvector 확장 설치
docker exec -it your_postgres_container psql -U your_user -d your_db
CREATE EXTENSION IF NOT EXISTS vector;
```

## 🎮 사용 방법

### 1. Docker Compose로 전체 서비스 실행 (권장)

```bash
# 전체 서비스 실행 (API, Worker, Celery Beat, Valkey)
docker-compose up -d

# 서비스 상태 확인
docker-compose ps
```

### 2. 개별 서비스 실행 (개발용)

```bash
# Celery Beat 실행 (스케줄러)
celery -A packages.presentation.worker.celery_app.celery_app beat --loglevel=info

# Celery Worker 실행 (작업자)
celery -A packages.presentation.worker.celery_app.celery_app worker --loglevel=info -Q ai,trends

# API 서버 실행 (포트 8081)
uvicorn apps.api.main:app --host 0.0.0.0 --port 8081
```

### 3. Python에서 직접 태스크 실행

```python
from apps.worker.trend_crawling_tasks import crawl_sns_trends_task

# SNS 트렌드 RSS 크롤링 태스크 실행
task = crawl_sns_trends_task.delay()
print(f"태스크 ID: {task.id}")

# 태스크 결과 확인
result = task.get()
print(f"결과: {result}")
```

## 📅 스케줄 설정

현재 설정된 스케줄:

- **SNS 트렌드 RSS 크롤링**: 매주 월요일 오전 2시
- **크롤링 주기**: 주간 1회
- **데이터 보관**: 최근 7일 이내 게시물만 수집

## 🔍 API 사용

### 트렌드 검색

```bash
curl -X POST "http://localhost:8081/trends/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "인스타그램 마케팅 트렌드",
       "limit": 10,
       "platform": "rss",
       "trend_type": "instagram_trend"
     }'
```

### 지원 플랫폼 조회

```bash
curl -X GET "http://localhost:8081/trends/platforms"
```

### 지원 트렌드 타입 조회

```bash
curl -X GET "http://localhost:8081/trends/trend-types"
```

## 📈 모니터링

### 로그 확인

```bash
# Celery Worker 로그
docker logs ai_worker

# Celery Beat 로그
docker logs ai_celery_beat

# API 서버 로그
docker logs ai_api
```

### 태스크 상태 확인

```python
from celery.result import AsyncResult
from packages.presentation.worker.celery_app import celery_app

# 태스크 상태 확인
result = AsyncResult('task_id', app=celery_app)
print(f"상태: {result.status}")
print(f"결과: {result.result}")
```

## 🛠️ 개발 및 디버깅

### RSS 피드 테스트

```python
from packages.infrastructure.services.crawling.rss_crawler import RSSCrawler

# RSS 크롤러 테스트
crawler = RSSCrawler()
trends = crawler.crawl()
print(f"수집된 트렌드: {len(trends)}개")
```

### 벡터 검색 테스트

```python
from packages.infrastructure.services.trend_storage_service import TrendStorageService

# 벡터 검색 테스트
storage_service = TrendStorageService()
results = storage_service.search_similar_trends("인스타그램 마케팅", limit=5)
print(f"검색 결과: {len(results)}개")
```

## 🔧 설정 커스터마이징

### RSS 피드 추가

`packages/infrastructure/services/crawling/rss_crawler.py`에서 `rss_feeds` 딕셔너리에 새로운 피드 추가:

```python
self.rss_feeds = {
    "custom_trends": [
        "https://your-custom-feed.com/rss",
        # 추가 피드들...
    ]
}
```

### 키워드 추가

`packages/infrastructure/services/crawling/rss_crawler.py`에서 `sns_keywords` 리스트에 새로운 키워드 추가:

```python
self.sns_keywords = [
    # 기존 키워드들...
    'your_custom_keyword',
    '새로운_키워드'
]
```

### 스케줄 변경

`packages/presentation/worker/celery_app.py`에서 `beat_schedule` 수정:

```python
celery_app.conf.beat_schedule = {
    'weekly-sns-trends': {
        'task': 'crawl_sns_trends',
        'schedule': crontab(hour=14, minute=30, day_of_week=3),  # 매주 수요일 오후 2시 30분
    },
}
```

## 📝 주의사항

1. **RSS 피드 가용성**: 일부 RSS 피드는 접근 제한이 있을 수 있습니다.
2. **크롤링 정책**: 각 사이트의 robots.txt와 이용약관을 준수해야 합니다.
3. **데이터 품질**: RSS 피드의 품질에 따라 수집되는 데이터의 품질이 달라질 수 있습니다.
4. **저장 공간**: 벡터 데이터는 상당한 저장 공간을 사용할 수 있습니다.

## 🚀 성능 최적화

- **배치 처리**: 여러 RSS 피드를 병렬로 처리
- **중복 제거**: URL 기반 중복 게시물 제거
- **인덱싱**: PostgreSQL 벡터 인덱스 최적화
- **캐싱**: 자주 검색되는 쿼리 결과 캐싱

## 📞 지원

문제가 발생하거나 개선 사항이 있으면 이슈를 등록해 주세요.