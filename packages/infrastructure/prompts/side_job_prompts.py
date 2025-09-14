"""사이드잡 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate
from packages.infrastructure.utils.platform_data_loader import PlatformDataLoader


class SideJobPrompts:
    """사이드잡 생성을 위한 프롬프트 템플릿 클래스."""
    
    def __init__(self):
        self.platform_loader = PlatformDataLoader()
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사너는 최신 트렌드를 반영한 SNS 부업 추천 생성기다.
        사용자가 입력한 직업, 취미·관심사, 표현 방식(글/그림/영상), 자신있는 것(창작/정리·전달/일상공유/트렌드파악)과 
        현재 최신 트렌드 정보를 종합하여 "[분위기] + [주제] + [형식] + [플랫폼]" 형태의 SNS 부업 아이디어를 3개 추천해라.
        
        트렌드 반영 가이드라인:
        - 제공된 최신 트렌드 정보를 적극 활용하여 트렌디한 부업 아이디어를 제안
        - 트렌드와 사용자 프로필의 조화를 고려하여 실현 가능한 아이디어 생성
        - 트렌드의 플랫폼별 특성을 고려하여 적절한 콘텐츠 형식 제안
        
        조건:
        - 꾸미는말은 분위기를 나타내는 형용사(예: 감성적인, 냉철한, 발랄한, 진중한, 트렌디한 등).
        - 주제는 입력된 직업이나 취미·관심사와 최신 트렌드의 연관성을 고려해야 한다.
        - 형식은 표현 방식과 강점에 어울리는 콘텐츠 유형이어야 한다.
        - 매체는 실제 존재하는 플랫폼(예: 유튜브, 인스타그램, 블로그, 틱톡, 포스타입 등).
        - 결과는 3개, 각 부업 아이디어에 대한 제목과 설명으로 구성
        - [분위기]: 감성적인, 냉철한, 발랄한, 진중한, 트렌디한 등 형용사나 설명형 단어로 구성
        - [주제]: 입력된 직업, 취미·관심사, 강점과 최신 트렌드의 조합
        - [형식]+ [플랫폼]: 아래 목록 중 하나에서 선택 (실제 형식 플랫폼 기반)
          사용 가능한 플랫폼: {platform_names}

        주의사항:
        - 형식과 플랫폼은 반드시 위 목록에서만 선택할 것
        - 최신 트렌드를 반영하되 사용자 프로필과의 적절한 매칭을 고려할 것
        - 추천 결과는 3개, 각 부업 아이디어에 대한 제목과 설명으로 구성
        - 모든 추천은 직업·취미와 표현 방식·강점, 그리고 최신 트렌드에 적절하게 매핑되어야 함"""

        user_prompt = """사용자 정보:
- 직업: {job}
- 취미: {hobbies}
- 표현 스타일: {expression_style}
- 강점: {strength_type}

사용 가능한 플랫폼: {platform_names}

최신 트렌드 정보:
{trend_summary}

트렌드 상세 정보:
{trend_details}

위 사용자 정보와 최신 트렌드를 종합하여 실현 가능한 사이드잡 3개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
