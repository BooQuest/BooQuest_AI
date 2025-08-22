import json, os
from typing import Dict
from app.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from app.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from app.domain.entities.onboarding_profile import OnboardingProfile
from app.adapters.input.dto.regenerate_side_job_request import RegenerateSideJobRequest
from app.domain.entities.regenerate_side_job import RegenerateSideJobRequest


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

platform_path = os.path.join(BASE_DIR, "platform_side_jobs.json")
sns_path = os.path.join(BASE_DIR, "sns_side_jobs.json")
expression_path = os.path.join(BASE_DIR, "expression_side_jobs.json")

with open(expression_path, "r", encoding="utf-8") as f:
    EXPRESSION_SIDE_JOBS = json.load(f)



SIDE_JOB_SYSTEM_PROMPT = f"""
        너는 SNS 부업 추천 생성기다.
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
        - [형식]+ [플랫폼]: 아래 목록 중 하나에서 선택 (실제 형식 플랫폼 기반), 
        - 반드시 사용자 정보의 "expressionStyle"과 같은 key의 목록에서만 선택해야 한다.
        - 그 외의 key에서 선택하면 안 된다.
        - 선택한 [형식]+ [플랫폼]을 제목에다가 추가한다
            사용 가능한 형식 + 플랫폼 조합 목록:
            {json.dumps(EXPRESSION_SIDE_JOBS, ensure_ascii=False, indent=2)}

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
        3. 트렌디한 여행 숏폼 틱톡

        반드시 아래와 같은 형식으로만 응답하세요:
        괄호 안의 형식을 지켜서 만들어
        ```json
            {{
            "recommendations": [
                {{
                "title": "부업 아이디어 제목 ([분위기] + [주제] + [형식] + [플랫폼] 형태)",
                "description": "어떤 활동을 어떤 방식으로 하는 사람인지 요약"
                }},
                {{
                "title": "부업 아이디어 제목 ([분위기] + [주제] + [형식] + [플랫폼] 형태)",
                "description": "어떤 활동을 어떤 방식으로 하는 사람인지 요약"
                }},
                {{
                "title": "부업 아이디어 제목 ([분위기] + [주제] + [형식] + [플랫폼] 형태)",
                "description": "어떤 활동을 어떤 방식으로 하는 사람인지 요약"
                }}
            ]
            }}
        ```
    """.strip()

class PromptTemplates:

    def generate_recommendation_sidejob_user_prompt(user_profile: OnboardingProfile) -> str:
        user_profile_dict = user_profile.to_dict()
        return f"""
            사용자 정보:
            {json.dumps(user_profile_dict, ensure_ascii=False, indent=2)}

            사용 가능한 형식 + 플랫폼 조합 목록에서 사용자 정보의 expressionStyle과 일치하는 key의 value를 골라 응답을 만들어줘
            반드시 목록에 있는거중에서만 골라야해 없으면 차라리 추천했던거 그대로 추천해

            부업 추천을 3개 생성해주세요.
            """.strip()
    

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
        }},
        {{
            "title": "미션 제목",
            "orderNo": 3,
            "notes": "미션에 대한 상세 설명"
        }},
        {{
            "title": "미션 제목",
            "orderNo": 4,
            "notes": "미션에 대한 상세 설명"
        }},
        {{
            "title": "미션 제목",
            "orderNo": 5,
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
        }},
        {{
            "title": "스텝 제목",
            "seq": 3,
            "detail": "스텝에 대한 상세 설명"
        }},
        {{
            "title": "스텝 제목",
            "seq": 4,
            "detail": "스텝에 대한 상세 설명"
        }},
        {{
            "title": "스텝 제목",
            "seq": 5,
            "detail": "스텝에 대한 상세 설명"
        }}
    ]
}}
```

미션 스텝은 5개 생성하고, 각 스텝은 구체적이고 실행 가능한 단계여야 합니다.
스텝은 순차적으로 진행되어야 하며, 이전 스텝을 완료해야 다음 스텝으로 진행할 수 있어야 합니다.
        """
        return prompt.strip()

    @staticmethod
    def regenerate_sidejob_prompt_by_feedback(requestDto: RegenerateSideJobRequest) -> str:
        # 피드백 기반 제약 조건 만들기
        feedback = requestDto.feedbackData
        feedback_messages = []

        mapping = {
            "LOW_PROFITABILITY": "수익성이 낮은 아이디어는 제외해 주세요.",
            "NO_INTEREST": "흥미가 없는 주제는 피해주세요.",
            "NOT_MY_STYLE": "스타일이 안 맞는 콘텐츠 형식은 배제해주세요.",
            "TAKES_TOO_MUCH_TIME": "시간이 많이 걸리는 부업은 피해주세요.",
            "NOT_FEASIBLE": "실현 불가능하거나 실행이 어려운 아이디어는 제외해주세요.",
            "TOO_EXPENSIVE": "비용이 많이 드는 아이디어는 피해주세요.",
        }   

        for reason in feedback.reasons:
            if reason in mapping:
                feedback_messages.append(f"- {mapping[reason]}")

        if feedback.etcFeedback:
            feedback_messages.append(f"- 기타 사유: {feedback.etcFeedback}")

        feedback_constraints = "\n".join(feedback_messages)
        
        return f"""
            사용자 정보:
            {json.dumps(requestDto.model_dump(), ensure_ascii=False, indent=2)}

            사용자의 피드백을 반영하여 아래 조건들을 반드시 지켜야 한다:
            {feedback_constraints}

            사용 가능한 형식 + 플랫폼 조합 목록에서 사용자 정보의 expressionStyle과 일치하는 key의 value를 골라 응답을 만들어줘
            반드시 목록에 있는거중에서만 골라야해 없으면 차라리 추천했던거 그대로 추천해

            부업 추천을 3개 생성해주세요.
            """.strip()
        
