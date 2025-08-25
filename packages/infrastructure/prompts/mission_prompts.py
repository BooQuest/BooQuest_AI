"""미션 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class MissionPrompts:
    """미션 생성을 위한 프롬프트 템플릿 클래스."""
    
    def create_prompt_template(self, **kwargs) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 사이드잡을 분석하여 구체적이고 실현 가능한 미션을 제안하는 AI입니다.

각 미션은 title, orderNo, notes 필드를 반드시 포함해야 합니다."""

        user_prompt = """사이드잡 정보:
- 제목: {side_job_title}
- 설명: {side_job_description}

위 사이드잡을 성공적으로 완성하기 위한 구체적이고 실현 가능한 미션 5개를 제안해주세요.

응답 형식 예시:
{{
  "missions": [
    {{"title": "미션 제목", "orderNo": 1, "notes": "미션 노트 및 구체적인 실행 방안"}},
    {{"title": "미션 제목", "orderNo": 2, "notes": "미션 노트 및 구체적인 실행 방안"}},
    {{"title": "미션 제목", "orderNo": 3, "notes": "미션 노트 및 구체적인 실행 방안"}},
    {{"title": "미션 제목", "orderNo": 4, "notes": "미션 노트 및 구체적인 실행 방안"}},
    {{"title": "미션 제목", "orderNo": 5, "notes": "미션 노트 및 구체적인 실행 방안"}}
  ]
}}

위 형식에 맞춰 **JSON만** 출력하세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
