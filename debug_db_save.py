#!/usr/bin/env python3
"""DB 저장 과정 디버깅"""

import os

# 환경변수 설정
os.environ['CLOVA_X_PROVIDER'] = 'naver'
os.environ['CLOVA_X_MODEL'] = 'HCX-007'
os.environ['CLOVA_X_API_KEY'] = 'test'

def debug_db_save():
    """DB 저장 과정 디버깅"""
    try:
        print("🔍 DB 저장 과정 디버깅...")
        
        from packages.infrastructure.services.crawling.rss_crawler import RSSCrawler
        from packages.infrastructure.services.trend_storage_service import TrendStorageService
        
        # RSS 크롤링
        crawler = RSSCrawler()
        trends = crawler.crawl()
        
        print(f"📊 수집된 트렌드: {len(trends)}개")
        
        # 첫 번째 트렌드의 상세 정보 확인
        if trends:
            trend = trends[0]
            print(f"\n--- 첫 번째 트렌드 상세 정보 ---")
            for key, value in trend.items():
                print(f"{key}: {type(value)} = {repr(value)}")
                
                # JSON 직렬화 가능한지 확인
                if key in ['tags', 'engagement_metrics']:
                    try:
                        import json
                        json.dumps(value)
                        print(f"  ✅ JSON 직렬화 OK")
                    except Exception as e:
                        print(f"  ❌ JSON 직렬화 오류: {e}")
        
        # DB 저장 시도
        print(f"\n--- DB 저장 시도 ---")
        storage_service = TrendStorageService()
        saved_trends = storage_service.save_trends(trends)
        print(f"✅ 저장 완료: {len(saved_trends)}개")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_db_save()
