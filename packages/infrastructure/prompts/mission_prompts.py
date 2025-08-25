"""미션 생성을 위한 고도화된 프롬프트."""

from langchain_core.prompts import ChatPromptTemplate


class MissionPrompts:
    """미션 생성을 위한 고도화된 프롬프트 클래스."""
    
    def create_prompt_template(self, user_request: str, context: str) -> ChatPromptTemplate:
        """미션 생성 프롬프트 템플릿을 생성합니다."""
        
        system_prompt = """당신은 사용자의 요청과 컨텍스트를 분석하여 구체적이고 실현 가능한 미션을 생성하는 AI 어시스턴트입니다.

사용자의 목표를 달성할 수 있는 단계별 미션을 제안해야 합니다.
각 미션은 명확하고 구체적인 목표를 가져야 합니다.

반드시 정확한 JSON 형식으로 응답해야 하며, missions 배열에 3개의 미션을 포함해야 합니다."""

        user_prompt = f"""사용자 요청: {user_request}
컨텍스트: {context}

위 정보를 바탕으로 사용자가 목표를 달성할 수 있는 미션 5개를 생성해주세요.
**중요: 반드시 각 미션에 title, orderNo, notes 필드를 모두 포함해야 합니다.**

응답 형식:
{{{{  
  "missions": [
    {{{{  
      "title": "미션 제목",
      "orderNo": 1,
      "notes": "미션 설계 노트 및 구체적인 실행 방안"
    }}}},
    {{{{  
      "title": "미션 제목",
      "orderNo": 2,
      "notes": "미션 설계 노트 및 구체적인 실행 방안"
    }}}},
    {{{{  
      "title": "미션 제목",
      "orderNo": 3,
      "notes": "미션 설계 노트 및 구체적인 실행 방안"
    }}}},
    {{{{  
      "title": "미션 제목",
      "orderNo": 4,
      "notes": "미션 설계 노트 및 구체적인 실행 방안"
    }}}},
    {{{{  
      "title": "미션 제목",
      "orderNo": 5,
      "notes": "미션 설계 노트 및 구체적인 실행 방안"
    }}}}
  ]
}}}}

**주의사항:**
1. title, orderNo, notes 필드는 반드시 모든 미션에 포함되어야 합니다
2. orderNo는 1부터 시작하여 순차적으로 증가해야 합니다
3. notes 필드가 비어있거나 누락되면 안 됩니다
4. JSON 형식이 정확해야 합니다

구체적이고 실현 가능한 미션을 제안해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
