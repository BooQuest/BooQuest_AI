"""사이드잡 재생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class RegenerateSideJobPrompts:
    """사이드잡 재생성을 위한 프롬프트 템플릿 클래스."""
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 피드백을 바탕으로 기존 사이드잡을 개선하여 새로운 사이드잡을 제안하는 AI입니다.

각 사이드잡은 "[분위기] + [주제] + [형식] + [플랫폼]" 형태로 구성하고, 
title과 description 필드를 반드시 포함해야 합니다."""

        user_prompt = """사용자 정보:
- 직업: {job}
- 취미: {hobbies}
- 표현 스타일: {expression_style}
- 강점: {strength_type}

피드백 정보:
- 피드백 이유: {feedback_reasons}
- 기타 피드백: {etc_feedback}

위 정보를 바탕으로 피드백을 반영한 개선된 사이드잡 1개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
