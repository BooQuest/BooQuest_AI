"""사이드잡 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate
from packages.infrastructure.utils.platform_data_loader import PlatformDataLoader


class SideJobPrompts:
    """사이드잡 생성을 위한 프롬프트 템플릿 클래스."""
    
    def __init__(self):
        self.platform_loader = PlatformDataLoader()
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사너는 SNS 부업 추천 생성기다.
        사용자가 입력한 직업, 취미·관심사, 표현 방식(글/그림/영상), 자신있는 것(창작/정리·전달/일상공유/트렌드파악)을 참고하여
        "[분위기] + [주제] + [형식] + [플랫폼]" 형태의 SNS 부업 아이디어를 3개 추천해라.
        - 예시)
        감성적인 + 카페 탐방 + 릴스 + 인스타그램
        → 분위기 있는 카페를 소개하며 감각적인 릴스를 업로드하는 크리에이터
        조건:
        - 꾸미는말은 분위기를 나타내는 형용사(예: 감성적인, 냉철한, 발랄한, 진중한 등).
        - 주제는 입력된 직업이나 취미·관심사와 연관성이 있어야 한다.
        - 형식은 표현 방식과 강점에 어울리는 콘텐츠 유형이어야 한다.
        - 매체는 실제 존재하는 플랫폼(예: 유튜브, 인스타그램, 블로그, 틱톡, 포스타입 등).
        - 결과는 3개, 한 줄 문장만 출력.
        - [분위기]: 감성적인, 냉철한, 발랄한, 진중한 등 형용사나 설명형 단어로 구성
        - [주제]: 입력된 직업, 취미·관심사, 강점과 연관되어야 함
        - [형식]+ [플랫폼]: 아래 목록 중 하나에서 선택 (실제 형식 플랫폼 기반)
          사용 가능한 플랫폼: {platform_names}

        주의사항:
        - 형식과 플랫폼은 반드시 위 목록에서만 선택할 것
        - 어울리지 않는 조합은 피할 것 (예: 감성 주식 일러스트 인스타그램 X)
        - 추천 결과는 3개, 각 부업 아이디어에 대한 제목과 설명으로 구성
        - 모든 추천은 직업·취미와 표현 방식·강점에 적절하게 매핑되어야 함
        부업 추천 실행 예시
        입력:
        - 직업: 프리랜서
        - 취미·관심사: 여행, 카페 탐방
        - 표현 방식: 영상
        - 자신있는 것: 일상 공유하기
        출력:
        1. 발랄한 여행 브이로그 유튜버
        2. 감성적인 카페 탐방 릴스 인스타그램
        3. 트렌디한 여행 숏폼 틱톡"""

        user_prompt = """사용자 정보:
- 직업: {job}
- 취미: {hobbies}
- 표현 스타일: {expression_style}
- 강점: {strength_type}

사용 가능한 플랫폼: {platform_names}

위 정보를 바탕으로 실현 가능한 사이드잡 3개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
