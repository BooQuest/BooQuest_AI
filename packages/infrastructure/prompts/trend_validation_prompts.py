"""트렌드 검증을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate


class TrendValidationPrompts:
    """트렌드 검증을 위한 프롬프트 템플릿 클래스."""
    
    def create_validation_prompt_template(self) -> ChatPromptTemplate:
        """트렌드 검증 프롬프트 템플릿 생성."""
        system_prompt = """당신은 SNS 부업 추천 시스템의 트렌드 검증자입니다.
주어진 트렌드 정보가 부업 정보로 활용될 수 있는지 판단해야 합니다.

중요: 검증 결과는 반드시 "Y" 또는 "N" 중 하나로만 응답해야 합니다.
- "Y": 부업 정보로 사용 가능
- "N": 부업 정보로 사용 불가능

검증 기준:
- 트렌드가 SNS 플랫폼(인스타그램, 유튜브, 틱톡, 블로그 등)과 관련이 있어야 함
- 트렌드가 개인이 활용할 수 있는 콘텐츠 아이디어나 수익화 가능성이 있어야 함
- 트렌드가 구체적이고 실행 가능한 정보를 포함해야 함
- 트렌드가 부적절하거나 불법적인 내용이 아니어야 함

부업 정보로 활용 가능한 예시 (Y 응답):
- SNS 콘텐츠 제작 방법, 팁, 트렌드
- 플랫폼별 수익화 전략
- 개인 브랜딩, 인플루언서 관련 트렌드
- 크리에이터 도구, 편집 기법
- 새로운 콘텐츠 형식이나 소셜미디어 기능

부업 정보로 활용 불가능한 예시 (N 응답):
- 일반 뉴스나 정치적 이슈
- 기술적인 내부 시스템 정보
- 개인적인 소식이나 유머
- 특정 브랜드나 제품의 단순 홍보
- 부적절하거나 불법적인 내용"""

        user_prompt = """트렌드 정보:
플랫폼: {platform}
제목: {title}
내용: {content}

위 트렌드 정보가 SNS 부업 정보로 활용될 수 있는지 판단하고, validation_result를 반드시 "Y" 또는 "N" 중 하나로만 응답해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])

