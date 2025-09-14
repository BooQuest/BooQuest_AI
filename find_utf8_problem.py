#!/usr/bin/env python3
"""UTF-8 문제가 있는 데이터 찾기"""

import os

# 환경변수 설정
os.environ['CLOVA_X_PROVIDER'] = 'naver'
os.environ['CLOVA_X_MODEL'] = 'HCX-007'
os.environ['CLOVA_X_API_KEY'] = 'test'
os.environ['DB_NAME'] = 'ai_project'
os.environ['DB_PWD'] = 'postgres123'

def find_utf8_problem():
    """UTF-8 문제가 있는 데이터 찾기"""
    try:
        from packages.infrastructure.services.crawling.rss_crawler import RSSCrawler
        crawler = RSSCrawler()
        trends = crawler.crawl()
        
        print(f"📊 수집된 트렌드: {len(trends)}개")
        
        # 각 트렌드의 모든 필드를 체크
        for i, trend in enumerate(trends):
            print(f"\n--- 트렌드 {i+1} ---")
            problem_found = False
            
            for key, value in trend.items():
                if isinstance(value, str):
                    try:
                        # UTF-8 인코딩 테스트
                        value.encode('utf-8')
                    except UnicodeEncodeError as e:
                        print(f"❌ {key}에서 UTF-8 인코딩 오류: {e}")
                        print(f"   문제 위치: {e.start}-{e.end}")
                        print(f"   문제 문자: {repr(value[e.start:e.end])}")
                        print(f"   전체 값: {repr(value)}")
                        problem_found = True
                        
                        # position 65 근처 확인
                        if e.start <= 65 <= e.end:
                            print(f"   🎯 position 65 근처 문제 발견!")
                            print(f"   position 60-70: {repr(value[60:70])}")
                
                elif isinstance(value, (list, dict)):
                    # 리스트나 딕셔너리 내부도 체크
                    import json
                    try:
                        json.dumps(value)
                    except Exception as e:
                        print(f"❌ {key}에서 JSON 직렬화 오류: {e}")
                        print(f"   값: {repr(value)}")
                        problem_found = True
            
            if problem_found:
                print(f"   🚨 트렌드 {i+1}에서 문제 발견!")
                break
            else:
                print(f"   ✅ 트렌드 {i+1} 정상")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_utf8_problem()
