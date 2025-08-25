"""미션 스텝 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class MissionStepPrompts:
    """미션 스텝 생성을 위한 프롬프트 템플릿 클래스."""
    
    def create_prompt_template(self, **kwargs) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 미션을 분석하여 구체적이고 실행 가능한 단계별 미션 스텝을 제안하는 AI입니다.

각 미션 스텝은 title, seq, detail 필드를 반드시 포함해야 합니다."""

        user_prompt = """미션 정보:
- 제목: {mission_title}
- 설명: {mission_description}

위 미션을 성공적으로 완성하기 위한 구체적이고 실행 가능한 미션 스텝 5개를 제안해주세요.

응답 형식 예시:
{{
  "mission_steps": [
    {{"title": "단계 제목", "seq": 1, "detail": "단계별 상세 내용 및 구체적인 실행 방법"}},
    {{"title": "단계 제목", "seq": 2, "detail": "단계별 상세 내용 및 구체적인 실행 방법"}},
    {{"title": "단계 제목", "seq": 3, "detail": "단계별 상세 내용 및 구체적인 실행 방법"}},
    {{"title": "단계 제목", "seq": 4, "detail": "단계별 상세 내용 및 구체적인 실행 방법"}},
    {{"title": "단계 제목", "seq": 5, "detail": "단계별 상세 내용 및 구체적인 실행 방법"}}
  ]
}}

위 형식에 맞춰 **JSON만** 출력하세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
