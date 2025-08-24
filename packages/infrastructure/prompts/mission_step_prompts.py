"""미션 단계 생성을 위한 고도화된 프롬프트."""

from langchain_core.prompts import ChatPromptTemplate


class MissionStepPrompts:
    """미션 단계 생성을 위한 고도화된 프롬프트 클래스."""
    
    def create_prompt_template(self, mission_info: str, user_context: str) -> ChatPromptTemplate:
        """미션 단계 생성 프롬프트 템플릿을 생성합니다."""
        
        system_prompt = """당신은 미션 정보와 사용자 컨텍스트를 분석하여 구체적이고 단계별로 실행 가능한 미션 단계를 생성하는 AI 어시스턴트입니다.

미션을 성공적으로 완료할 수 있는 상세한 단계를 제안해야 합니다.
각 단계는 명확하고 실행 가능하며, 사용자가 단계별로 진행할 수 있어야 합니다.

반드시 정확한 JSON 형식으로 응답해야 하며, mission_steps 배열에 5-8개의 단계를 포함해야 합니다."""

        user_prompt = f"""미션 정보: {mission_info}
사용자 컨텍스트: {user_context}

위 정보를 바탕으로 미션을 완료하기 위한 구체적인 단계 5개를 생성해주세요.
**중요: 반드시 각 단계에 title, seq, detail 필드를 모두 포함해야 합니다.**

응답 형식:
{{{{  
  "mission_steps": [
    {{{{  
      "title": "단계 제목",
      "seq": 1,
      "detail": "단계별 상세 내용 및 구체적인 실행 방법"
    }}}},
    {{{{  
      "title": "단계 제목",
      "seq": 2,
      "detail": "단계별 상세 내용 및 구체적인 실행 방법"
    }}}},
    {{{{  
      "title": "단계 제목",
      "seq": 3,
      "detail": "단계별 상세 내용 및 구체적인 실행 방법"
    }}}},
    {{{{  
      "title": "단계 제목",
      "seq": 4,
      "detail": "단계별 상세 내용 및 구체적인 실행 방법"
    }}}},
    {{{{  
      "title": "단계 제목",
      "seq": 5,
      "detail": "단계별 상세 내용 및 구체적인 실행 방법"
    }}}}
  ]
}}}}

**주의사항:**
1. title, seq, detail 필드는 반드시 모든 단계에 포함되어야 합니다
2. seq는 1부터 시작하여 순차적으로 증가해야 합니다
3. detail 필드가 비어있거나 누락되면 안 됩니다
4. JSON 형식이 정확해야 합니다

구체적이고 실현 가능한 단계를 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
