"""챗봇 대화 제목 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class ChatTitlePrompts:
    """챗봇 대화 제목 생성을 위한 프롬프트 템플릿 클래스."""

    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = (
            "당신은 사용자의 첫 질문을 분석하여 대화의 핵심을 담은 짧은 제목을 만드는 AI입니다.\n"
            "- 제목은 10-20자 내외로 간결하게 작성하세요.\n"
            "- 부업, 사이드잡, 직업 관련 키워드를 포함하세요.\n"
            "- 구체적이고 명확한 제목을 만들어주세요.\n"
            "- 예시: '유튜브 부업 시작하기', '온라인 쇼핑몰 창업 문의', '부업 추천 요청'\n"
        )

        user_prompt = (
            "사용자의 첫 질문: {message}\n\n"
            "위 질문을 바탕으로 대화의 제목을 만들어주세요. "
            "제목만 답변하고 다른 설명은 하지 마세요."
        )

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt),
        ])
