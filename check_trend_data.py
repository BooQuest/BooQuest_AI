"""데이터베이스의 트렌드 데이터 확인 스크립트."""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 환경 변수 설정
os.environ.setdefault('CLOVA_X_PROVIDER', 'naver')
os.environ.setdefault('CLOVA_X_MODEL', 'HCX-007')
os.environ.setdefault('CLOVA_X_API_KEY', 'dummy_key')
os.environ.setdefault('CLOVA_X_BASE_URL', 'https://clovastudio.naver.com')
os.environ.setdefault('DB_USER', 'postgres')
os.environ.setdefault('DB_PWD', 'Rlarldnd1!')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '5432')
os.environ.setdefault('DB_NAME', 'booquest')

from packages.core.db.database import create_database_engine_from_config
from sqlalchemy import text

def check_trend_data():
    """데이터베이스의 트렌드 데이터를 확인합니다."""
    try:
        print("🔍 데이터베이스 트렌드 데이터 확인 중...")
        
        engine = create_database_engine_from_config()
        
        with engine.connect() as conn:
            # sns_trends 테이블 데이터 확인
            print("\n📊 sns_trends 테이블 데이터:")
            result = conn.execute(text("SELECT COUNT(*) FROM sns_trends;"))
            count = result.scalar()
            print(f"총 트렌드 개수: {count}")
            
            if count > 0:
                # 최근 트렌드 5개 조회
                result = conn.execute(text("""
                    SELECT uuid, platform, title, created_at 
                    FROM sns_trends 
                    ORDER BY created_at DESC 
                    LIMIT 5;
                """))
                
                trends = result.fetchall()
                print("\n📋 최근 트렌드 5개:")
                for i, trend in enumerate(trends, 1):
                    print(f"  {i}. [{trend[1]}] {trend[2][:50]}... ({trend[3]})")
            
            # trend_embeddings 테이블 데이터 확인
            print("\n📊 trend_embeddings 테이블 데이터:")
            result = conn.execute(text("SELECT COUNT(*) FROM trend_embeddings;"))
            embedding_count = result.scalar()
            print(f"총 임베딩 개수: {embedding_count}")
            
            if embedding_count > 0:
                # 임베딩 샘플 확인
                result = conn.execute(text("""
                    SELECT embedding 
                    FROM trend_embeddings 
                    LIMIT 1;
                """))
                embedding_sample = result.scalar()
                if embedding_sample:
                    # 벡터를 파싱해서 차원 확인
                    import json
                    try:
                        vector_data = json.loads(embedding_sample)
                        dimension = len(vector_data)
                        print(f"임베딩 차원: {dimension}")
                    except:
                        print("임베딩 차원 확인 실패")
            
            return count > 0
            
    except Exception as e:
        print(f"❌ 데이터 확인 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_trend_retrieval():
    """트렌드 검색 기능을 테스트합니다."""
    try:
        print("\n🔍 트렌드 검색 기능 테스트...")
        
        from packages.infrastructure.services.trend_retriever_service import TrendRetrieverService
        
        retriever = TrendRetrieverService()
        
        # 테스트 쿼리로 검색
        test_query = "인스타그램 트렌드"
        trends = retriever.search_trends_by_query(query=test_query, limit=3)
        
        print(f"검색 쿼리: '{test_query}'")
        print(f"검색 결과: {len(trends)}개")
        
        for i, trend in enumerate(trends, 1):
            print(f"  {i}. [{trend.get('platform', 'N/A')}] {trend.get('title', 'N/A')}")
        
        return len(trends) > 0
        
    except Exception as e:
        print(f"❌ 트렌드 검색 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("트렌드 데이터 확인 및 테스트")
    print("=" * 50)
    
    # 1. 데이터베이스 데이터 확인
    has_data = check_trend_data()
    
    if has_data:
        # 2. 트렌드 검색 테스트
        retrieval_works = test_trend_retrieval()
        
        if retrieval_works:
            print("\n✅ 모든 테스트 통과!")
            print("트렌드 데이터가 정상적으로 저장되고 검색됩니다.")
        else:
            print("\n❌ 트렌드 검색에 문제가 있습니다.")
    else:
        print("\n❌ 데이터베이스에 트렌드 데이터가 없습니다.")
        print("먼저 트렌드 크롤링을 실행해주세요.")
