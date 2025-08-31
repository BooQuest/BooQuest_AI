"""미션 생성을 위한 프롬프트 템플릿."""

from langchain_core.prompts import ChatPromptTemplate
from packages.infrastructure.utils.platform_data_loader import PlatformDataLoader


class MissionPrompts:
    """미션 생성을 위한 프롬프트 템플릿 클래스."""
    def __init__(self):
        self.platform_loader = PlatformDataLoader()
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """프롬프트 템플릿 생성."""
        system_prompt = """사용자의 사이드잡을 분석하여 구체적이고 실현 가능한 미션을 제안하는 AI입니다.

        다음과 같은 형식으로 각 단계를 만들어주세요.
        “채널 세팅 → 초기 콘텐츠 확보 → 유입 활동 → 채널 영향력 강화 → 수익화 시도”
        미션 생성 형식 : {expression_type_steps}
        위의 형식에서 사용자의 부업 플랫폼과 앎맞은 미션을 생성해주세요.


각 미션은 title, orderNo, notes, guide 필드를 반드시 포함해야 합니다.
notes 는 title 을 하기 위한 세부설명으로 100자로 작성해주고,
guide 필드에 notes 에 작성한 것을 하기위해서 유용한 팁 같은 것을 500자로 작성해주세요.
"""

        user_prompt = """사이드잡 정보:
- 제목: {side_job_title}
- 설명: {side_job_description}


아래 형식을 지켜서 만들어주세요.

title : 미션 제목 ([분위기] + [주제] + [형식] + [플랫폼] 형태)
orderNo : 순서
notes : 미션에 대한 상세설명 100 글자
guide : 상세 설명에 대한 가이드 5가지 (예시 

**1. 채널명을 정하고 계정을 생성한다**

- 기억하기 쉽고, 활동 주제가 연상되는 이름이면 좋아요.
- 검색 시 중복이 적은 이름을 추천합니다.

**2. 프로필 이미지와 소개글을 설정한다**

- 얼굴 사진이나 로고를 넣어 신뢰도를 높이세요.
- 소개글은 간결하게 ‘무엇을 다루는 채널인지’ 전달하세요.

**3. 활동할 플랫폼의 알고리즘을 간단히 조사한다**

- 예: 인스타그램은 해시태그, 유튜브는 클릭률이 중요해요.
- 핵심 노출 방식만 이해해도 콘텐츠 설계가 쉬워집니다.

**4. 타깃 시청자/팔로워를 정의한다**

- 내 콘텐츠를 볼 사람은 누구인지 상상해보세요.
- 연령, 관심사, 고민을 구체적으로 떠올리는 게 좋아요.

**5. 콘텐츠 주제와 톤앤매너를 설정한다**

- 정보, 일상, 공감 등 핵심 콘텐츠 방향을 정해보세요.
- 말투, 색감, 표현 방식도 일관성 있게 정해두면 좋습니다.
)


위 사이드잡을 성공적으로 완성하기 위한 구체적이고 실현 가능한 미션 5개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
