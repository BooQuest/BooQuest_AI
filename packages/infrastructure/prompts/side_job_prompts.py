"""사이드잡 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate
from packages.infrastructure.utils.platform_data_loader import PlatformDataLoader


class SideJobPrompts:
    """사이드잡 생성을 위한 프롬프트 템플릿 클래스."""
    
    def __init__(self):
        self.platform_loader = PlatformDataLoader()
    
    def create_prompt_template(self, **kwargs) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 직업, 취미, 표현 스타일, 강점을 분석하여 맞춤형 사이드잡을 추천하는 AI입니다.

각 사이드잡은 "[분위기] + [주제] + [형식] + [플랫폼]" 형태로 구성하고, 
title과 description 필드를 반드시 포함해야 합니다."""

        user_prompt = """사용자 정보:
- 직업: {job}
- 취미: {hobbies}
- 표현 스타일: {expression_style}
- 강점: {strength_type}

사용 가능한 플랫폼: {platform_names}
사용 가능한 SNS: {sns_platforms}

위 정보를 바탕으로 실현 가능한 사이드잡 3개를 제안해주세요.

응답 형식 예시:
{{
  "side_jobs": [
    {{"title": "[분위기] + [주제] + [형식] + [플랫폼]", "description": "상세 설명 및 구체적인 실행 방안"}},
    {{"title": "[분위기] + [주제] + [형식] + [플랫폼]", "description": "상세 설명 및 구체적인 실행 방안"}},
    {{"title": "[분위기] + [주제] + [형식] + [플랫폼]", "description": "상세 설명 및 구체적인 실행 방안"}}
  ]
}}

위 형식에 맞춰 **JSON만** 출력하세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
