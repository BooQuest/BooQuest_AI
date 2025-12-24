"""사이드잡 생성 API 테스트 스크립트."""

import sys
import os
import asyncio
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 환경 변수 설정
os.environ.setdefault("GOOGLE_API_KEY", "dummy_key")
os.environ.setdefault("GEMINI_MODEL", "gemini-3.0-flash")
os.environ.setdefault('DB_USER', 'postgres')
os.environ.setdefault('DB_PWD', 'Rlarldnd1!')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '5432')
os.environ.setdefault('DB_NAME', 'booquest')

from packages.core.external.langgraph.workflow import LangGraphWorkflowService
from packages.infrastructure.di.container import Container
from packages.core.db.uow_sqlalchemy import SqlAlchemyUoW

async def test_side_job_generation():
    """사이드잡 생성 테스트."""
    try:
        print("🚀 사이드잡 생성 API 테스트 시작...")
        
        # LangGraph 워크플로우 서비스 초기화
        # 간단한 UoW 팩토리 클래스 생성
        class SimpleUoWFactory:
            def __call__(self):
                return SqlAlchemyUoW()
        
        uow_factory = SimpleUoWFactory()
        workflow_service = LangGraphWorkflowService(uow_factory)
        
        # 테스트 데이터
        test_data = {
            "user_id": 1,
            "profile_data": {
                "job": "개발자",
                "hobbies": ["프로그래밍", "게임", "영화감상"],
                "expression_style": "글",
                "strength_type": "창작"
            }
        }
        
        print("📋 테스트 데이터:")
        print(json.dumps(test_data, indent=2, ensure_ascii=False))
        
        # 사이드잡 생성 실행
        print("\n🔄 사이드잡 생성 중...")
        result = await workflow_service.generate_side_jobs(test_data)
        
        print(f"\n✅ 생성 완료: {len(result)}개 사이드잡")
        
        # 결과 출력
        for i, side_job in enumerate(result, 1):
            print(f"\n{i}. {side_job.get('title', 'N/A')}")
            print(f"   설명: {side_job.get('description', 'N/A')}")
            print(f"   플랫폼: {side_job.get('platform', 'N/A')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 사이드잡 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("사이드잡 생성 API 테스트")
    print("=" * 50)
    
    result = asyncio.run(test_side_job_generation())
    
    if result:
        print("\n🎉 테스트 성공!")
    else:
        print("\n❌ 테스트 실패!")
