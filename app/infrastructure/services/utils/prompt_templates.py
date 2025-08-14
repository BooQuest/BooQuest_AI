import json
from app.domain.entities.user_profile import UserProfile
from app.domain.entities.onboarding_profile import OnboardingProfile

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

    @staticmethod
    def generate_recommendation_sidejob_prompt(user_profile: OnboardingProfile) -> str:
        user_profile_dict = user_profile.to_dict()

        return f"""
            부업 3개 목록을 다음과 같이 JSON 형태로 반환해주세요: 설명이나 서론 없이 아래 형식 그대로 JSON 객체만 반환하세요. 

            아래 사용자 정보를 기반으로 적합한 SNS 부업 아이디어를 3가지 추천해 주세요.
            - 인스타그램, 블로그, 유튜브, 틱톡처럼 SNS 기반의 수익형 아이디어만 허용합니다.
            - 부업 주제는 사용자의 직업, 성격, 취미와 연관되어야 합니다.
            - 반드시 JSON 형식으로만 응답하세요.

            사용자 정보:
            {json.dumps(user_profile_dict, ensure_ascii=False, indent=2)}

            반드시 아래와 같은 형식으로만 응답하세요:

            {{
            "recommendations": [
                {{
                "title": "부업 아이디어 제목",
                "description": "추천 이유와 부업에 대한 설명",
                }},
                {{
                "title": "부업 아이디어 제목",
                "description": "추천 이유와 부업에 대한 설명",
                }},
                {{
                "title": "부업 아이디어 제목",
                "description": "추천 이유와 부업에 대한 설명",
                }}
            ]
            }}
    """