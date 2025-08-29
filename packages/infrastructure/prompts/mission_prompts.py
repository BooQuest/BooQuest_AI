"""미션 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class MissionPrompts:
    """미션 생성을 위한 프롬프트 템플릿 클래스."""
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 사이드잡을 분석하여 구체적이고 실현 가능한 미션을 제안하는 AI입니다.

각 미션은 title, orderNo, notes, guide 필드를 반드시 포함해야 합니다.
notes 는 title 을 하기 위한 세부설명으로 100자로 작성해주고,
guide 필드에 notes 에 작성한 것을 하기위해서 유용한 팁 같은 것을 500자로 작성해주세요.
"""

        user_prompt = """사이드잡 정보:
- 제목: {side_job_title}
- 설명: {side_job_description}

위 사이드잡을 성공적으로 완성하기 위한 구체적이고 실현 가능한 미션 5개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
