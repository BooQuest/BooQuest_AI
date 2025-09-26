# Windows에서 PostgreSQL pgvector 확장 설치

## 방법 1: PostgreSQL용 pgvector 바이너리 설치 (권장)

### 1. pgvector 릴리스 페이지에서 다운로드
- https://github.com/pgvector/pgvector/releases
- Windows용 최신 릴리스를 다운로드 (예: `pgvector-v0.7.0-windows-x64.zip`)

### 2. PostgreSQL 설치 디렉토리에 복사
```bash
# PostgreSQL 17 기준 (일반적인 설치 경로)
C:\Program Files\PostgreSQL\17\lib\vector.dll
C:\Program Files\PostgreSQL\17\share\extension\vector.control
C:\Program Files\PostgreSQL\17\share\extension\vector--0.7.0.sql
```

### 3. PostgreSQL 서비스 재시작
```bash
# Windows 서비스에서 PostgreSQL 재시작
net stop postgresql-x64-17
net start postgresql-x64-17
```

### 4. 확장 설치 확인
```sql
psql -h localhost -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## 방법 2: Docker를 사용한 PostgreSQL with pgvector

### 1. docker-compose.yml에 PostgreSQL 추가
```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: postgres_with_pgvector
    environment:
      POSTGRES_DB: ai_project
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 2. Docker 컨테이너 실행
```bash
docker-compose up -d postgres
```

### 3. 확장 설치 확인
```bash
docker exec -it postgres_with_pgvector psql -U postgres -d ai_project -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## 방법 3: 소스에서 컴파일 (고급 사용자)

### 1. Visual Studio Build Tools 설치
- Visual Studio 2022 Build Tools 다운로드
- C++ 빌드 도구 포함하여 설치

### 2. pgvector 소스 다운로드 및 컴파일
```bash
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install
```

## 설치 확인

### 1. 확장 설치 확인
```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### 2. 벡터 타입 확인
```sql
SELECT typname FROM pg_type WHERE typname = 'vector';
```

### 3. 벡터 연산 테스트
```sql
SELECT '[1,2,3]'::vector;
SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector;
```

## 문제 해결

### 1. 권한 문제
- PostgreSQL 설치 디렉토리에 관리자 권한으로 접근
- 파일 복사 시 관리자 권한 필요

### 2. 버전 호환성
- PostgreSQL 버전과 pgvector 버전 호환성 확인
- 32비트/64비트 아키텍처 일치 확인

### 3. 경로 문제
- PostgreSQL 설치 경로 확인
- 환경변수 PATH 설정 확인

## 참고 링크
- pgvector GitHub: https://github.com/pgvector/pgvector
- PostgreSQL 확장 설치 가이드: https://www.postgresql.org/docs/current/extend-extensions.html
