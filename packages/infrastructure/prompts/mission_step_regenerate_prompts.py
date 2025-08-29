"""미션 스텝 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class MissionStepRegeneratePrompts:
    """미션 스텝 생성을 위한 프롬프트 템플릿 클래스."""
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 미션을 분석하여 구체적이고 실행 가능한 단계별 미션 스텝을 제안하는 AI입니다.

각 미션 스텝은 title, seq, detail 필드를 반드시 포함해야 합니다."""

        user_prompt = """미션 정보:
    - 제목: {mission_title}
    - 설명: {mission_description}
    피드백 정보:
    - 피드백 이유: {feedback_reasons}
    - 기타 피드백: {etc_feedback}

피드백을 반영하여 미션 스텝을 개선해주세요.
위 미션을 성공적으로 완성하기 위한 구체적이고 실행 가능한 미션 스텝 5개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
