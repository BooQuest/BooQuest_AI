import json
from app.domain.entities.user_profile import UserProfile

class PromptTemplates:
    """공통 프롬프트 템플릿 클래스"""
    
    @staticmethod
    def generate_task_prompt(user_profile: UserProfile) -> str:
        """태스크 생성 프롬프트를 생성합니다."""
        # UserProfile을 딕셔너리로 변환 후 JSON 직렬화
        user_profile_dict = user_profile.to_dict()
        
        return f"""
사용자 정보를 바탕으로 부업 태스크를 생성해주세요:

사용자 정보:
{json.dumps(user_profile_dict, ensure_ascii=False, indent=2)}

태스크 5개 목록을 다음과 같이 JSON 형태로 반환해주세요:
{{
    result : {
        [{
      "title": "태스크 제목",
      "description": "상세 설명",
      "difficulty": "난이도",
      "priority": "우선순위"
      }]
    }
}}
"""