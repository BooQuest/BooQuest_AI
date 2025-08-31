"""미션 스텝 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class MissionStepPrompts:
    """미션 스텝 생성을 위한 프롬프트 템플릿 클래스."""
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 미션을 분석하여 구체적이고 실행 가능한 단계별 미션 스텝을 제안하는 AI입니다.

각 미션 스텝은 title, seq, detail 필드를 반드시 포함해야 합니다."""

        user_prompt = """미션 정보:
- 제목: {mission_title}
- 설명: {mission_description}

미션 스텝은 5개 생성하고, 각 스텝은 구체적이고 실행 가능한 단계여야 합니다.
스텝은 순차적으로 진행되어야 하며, 이전 스텝을 완료해야 다음 스텝으로 진행할 수 있어야 합니다.
"""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
