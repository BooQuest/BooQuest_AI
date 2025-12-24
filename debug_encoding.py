#!/usr/bin/env python3
"""UTF-8 인코딩 문제 디버깅"""

import os

# 환경변수 설정
os.environ["GOOGLE_API_KEY"] = "test"

def debug_encoding():
    """인코딩 문제 디버깅"""
    try:
        print("🔍 RSS 크롤링 및 인코딩 디버깅...")
        
        from packages.infrastructure.services.crawling.rss_crawler import RSSCrawler
        crawler = RSSCrawler()
        trends = crawler.crawl()
        
        print(f"📊 수집된 트렌드: {len(trends)}개")
        
        # 각 트렌드의 데이터 타입과 인코딩 확인
        for i, trend in enumerate(trends[:3]):  # 처음 3개만 확인
            print(f"\n--- 트렌드 {i+1} ---")
            for key, value in trend.items():
                if isinstance(value, str):
                    print(f"{key}: {type(value)} - 길이: {len(value)}")
                    # 문제가 될 수 있는 문자 확인
                    try:
                        value.encode('utf-8')
                        print(f"  ✅ UTF-8 인코딩 OK")
                    except UnicodeEncodeError as e:
                        print(f"  ❌ UTF-8 인코딩 오류: {e}")
                        print(f"  문제 문자: {repr(value[e.start:e.end])}")
                elif isinstance(value, bytes):
                    print(f"{key}: {type(value)} - 길이: {len(value)}")
                    try:
                        decoded = value.decode('utf-8')
                        print(f"  ✅ UTF-8 디코딩 OK")
                    except UnicodeDecodeError as e:
                        print(f"  ❌ UTF-8 디코딩 오류: {e}")
                        print(f"  문제 바이트: {repr(value[e.start:e.end])}")
                else:
                    print(f"{key}: {type(value)}")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_encoding()
