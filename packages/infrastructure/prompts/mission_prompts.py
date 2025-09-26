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
guide : 생성된 미션에 대한 (가이드 제목 + 세부설명) 5개  
예시) 
생성된 미션이 유튜브와 관련 있었을 때의 결과 : 유튜브 계정 만드는 법에 대한 가이드, 수익화 까지 필요한 구독자 및 시청 횟수 등등 ... 가이드


위 사이드잡을 성공적으로 완성하기 위한 구체적이고 실현 가능한 미션 5개를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
