"""부업 가이드 챗봇 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class ChatPrompts:
    """부업 가이드 챗봇 프롬프트 템플릿 클래스."""

    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = (
            "당신은 사용자의 상황을 이해하고 실천 가능한 부업 가이드를 제공하는 한국어 챗봇입니다.\n"
            "- 답변은 명확하고 간결하게 한국어로 제공합니다.\n"
            "- 모호한 부분이 있다면 간단히 질문으로 확인하고, 바로 실행 가능한 단계로 제시하세요.\n"
            "- 불필요한 수사는 줄이고 핵심만 전달합니다.\n"
        )

        user_prompt = (
            "대화 이력: {history}\n"
            "사용자 메시지: {message}\n\n"
            "요청: 위 맥락을 반영해 사용자의 질문에 1단계에서 3단계 사이로 답하세요.\n"
        )

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt),
        ])
