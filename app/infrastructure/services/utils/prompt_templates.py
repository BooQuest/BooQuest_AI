import json
from app.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from app.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from app.domain.entities.onboarding_profile import OnboardingProfile

class PromptTemplates:

    @staticmethod
    def generate_recommendation_sidejob_prompt(user_profile: OnboardingProfile) -> str:
        user_profile_dict = user_profile.to_dict()
        desired = user_profile_dict.get("desiredSideJob", "")
        desired = desired.strip()

        if desired:
            additional_guide = f"""
            또한 사용자가 선호하는 부업 아이디어로 "{desired}"를 입력했으니,
            해당 부업을 할 수 있는 SNS 기반 부업 아이디어를 추천해라.
            직업, 성격, 취미와 무관하거나 비현실적인 경우에는 무시하고 나머지 데이터를 기반으로 추천
            """
        else:
            additional_guide = ""

        prompt = f"""
        너는 SNS 부업 추천 생성기다.
        사용자가 입력한 직업, 취미·관심사, 표현 방식(글/그림/영상), 자신있는 것(창작/정리·전달/일상공유/트렌드파악)을 참고하여
        "꾸미는말 + 주제 + 형식 + 매체" 형태의 SNS 부업 아이디어를 3개 추천해라.

        조건:

        - 꾸미는말은 분위기를 나타내는 형용사(예: 감성적인, 냉철한, 발랄한, 진중한 등).
        - 주제는 입력된 직업이나 취미·관심사와 연관성이 있어야 한다.
        - 형식은 표현 방식과 강점에 어울리는 콘텐츠 유형이어야 한다.
        - 매체는 실제 존재하는 플랫폼(예: 유튜브, 인스타그램, 블로그, 틱톡, 포스타입 등).
        - 결과는 3개, 한 줄 문장만 출력.
        - 꾸미는 말, 주제, 형식은 서로 연관이 있는 주제들끼리 엮어서 만들어 
        예를들어 "감성 주식 일러스트 인스타그램" 이건 서로 안어울리는 거야

        예시
        1. 발랄한 여행 브이로그 유튜버
        2. 감성적인 카페 탐방 릴스 인스타그램
        3. 트렌디한 여행 숏폼 틱톡
        {additional_guide}

        사용자 정보:
        {json.dumps(user_profile_dict, ensure_ascii=False, indent=2)}

        반드시 아래와 같은 형식으로만 응답하세요:
        ```json
            {{
            "recommendations": [
                {{
                "title": "부업 아이디어 제목",
                "description": "추천 이유와 부업에 대한 설명"
                }},
                {{
                "title": "부업 아이디어 제목",
                "description": "추천 이유와 부업에 대한 설명"
                }},
                {{
                "title": "부업 아이디어 제목",
                "description": "추천 이유와 부업에 대한 설명"
                }}
            ]
            }}
        ```
        """
        return prompt.strip()



    @staticmethod
    def generate_recommendation_mission_prompt(requestDto: GenerateMissionRequest) -> str:
        """미션 생성을 위한 프롬프트 생성"""
        prompt = f"""
사용자의 입력(부업 유형, 매체, 주제 등)을 바탕으로, 실제 수익화까지 이어지는 5단계 메인퀘스트와 부퀘스트를 설계하라.

조건:

- 메인퀘스트는 정확히 5개로 나눈다.
- 각 메인퀘스트에는 부퀘스트 5개를 반드시 작성한다.
- 메인퀘스트는 장기 목표와 기간을 포함하며, 플랫폼별 평균 수익화 조건을 반영한다.
(예: 유튜브=누적 영상 50편+구독자 1000명, 블로그=글 30~50개+일 방문자 100명, 인스타그램=팔로워 5000명 이상 등)
- 메인퀘스트는 단계별로 누적 목표가 자연스럽게 이어지도록 작성한다.
- 부퀘스트는 목표가 아니라 실행 가능한 행동 단위여야 한다.
- 모든 부퀘스트는 난이도가 비슷하게 구성한다.

사이드잡 정보:
- 제목: {requestDto.side_job_title}
- 디자인 노트: {requestDto.side_job_design_notes}

다음 형식으로 JSON 응답을 제공해주세요:

```json
{{
    "result": [
        {{
            "title": "미션 제목",
            "orderNo": 1,
            "notes": "미션에 대한 상세 설명"
        }},
        {{
            "title": "미션 제목",
            "orderNo": 2,
            "notes": "미션에 대한 상세 설명"
        }}
    ]
}}
```

        미션은 5개 입니다 
        생성하고, 각 미션은 구체적이고 실행 가능한 단계여야 합니다.
        """
        return prompt.strip()

    @staticmethod
    def generate_mission_step_prompt(requestDto: GenerateMissionStepRequest) -> str:
        """미션 스텝 생성을 위한 프롬프트 생성"""
        prompt = f"""
미션을 위한 상세 스텝을 생성해주세요.

미션 정보:
- 제목: {requestDto.mission_title}
- 디자인 노트: {requestDto.mission_design_notes}

다음 형식으로 JSON 응답을 제공해주세요:

```json
{{
    "result": [
        {{
            "title": "스텝 제목",
            "seq": 1,
            "detail": "스텝에 대한 상세 설명"
        }},
        {{
            "title": "스텝 제목",
            "seq": 2,
            "detail": "스텝에 대한 상세 설명"
        }}
    ]
}}
```

미션 스텝은 5개 생성하고, 각 스텝은 구체적이고 실행 가능한 단계여야 합니다.
스텝은 순차적으로 진행되어야 하며, 이전 스텝을 완료해야 다음 스텝으로 진행할 수 있어야 합니다.
        """
        return prompt.strip()
