"""SNS 트렌드 크롤링을 수동으로 실행하는 스크립트."""

import sys
import os
import asyncio

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 환경 변수 설정 (필요한 경우)
os.environ.setdefault("GOOGLE_API_KEY", "dummy_key")
os.environ.setdefault("GEMINI_MODEL", "gemini-3.0-flash")
os.environ.setdefault('DB_USER', 'postgres')
os.environ.setdefault('DB_PWD', 'Rlarldnd1!')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '5432')
os.environ.setdefault('DB_NAME', 'booquest')

from packages.infrastructure.services.trend_crawling_service import TrendCrawlingService
from packages.infrastructure.services.trend_storage_service import TrendStorageService


async def run_trend_crawling():
    """트렌드 크롤링을 실행합니다."""
    try:
        print("🚀 SNS 트렌드 크롤링 시작...")
        
        # 크롤링 서비스 초기화
        crawling_service = TrendCrawlingService()
        
        # 모든 트렌드 크롤링
        print("📡 RSS 피드에서 트렌드 데이터 수집 중...")
        result = crawling_service.crawl_all_trends()
        
        print(f"✅ 크롤링 완료: {result}")
        
        # 결과 확인
        if isinstance(result, dict) and result.get("rss", 0) > 0:
            print(f"🎉 크롤링 및 저장 완료: {result['rss']}개 트렌드가 데이터베이스에 저장되었습니다!")
            return result
        else:
            print("⚠️ 크롤링된 트렌드가 없거나 저장에 실패했습니다.")
            return result
        
    except Exception as e:
        print(f"❌ 트렌드 크롤링 실패: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """메인 함수."""
    print("=" * 50)
    print("SNS 트렌드 크롤링 수동 실행")
    print("=" * 50)
    
    # 비동기 함수 실행
    result = asyncio.run(run_trend_crawling())
    
    if result:
        print("\n✅ 모든 작업이 성공적으로 완료되었습니다!")
        print(f"총 {len(result)}개의 트렌드가 데이터베이스에 저장되었습니다.")
    else:
        print("\n❌ 작업이 실패했습니다.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
