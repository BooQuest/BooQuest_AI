"""사용자 챗봇 이용 시 질문 검증 노드."""

from typing import Dict, Any
from packages.infrastructure.logging import get_logger

class ChatClassifyNode:
    name = "chat_classify"
    def __init__(self, llm):
        self.llm = llm
        self.logger = get_logger(__name__)

    async def __call__(self, state):
        q = state.request_data.get("query","")
        system = (
            "당신은 라우터입니다. 질문이 '부업/사이드잡, 미션, 부퀘스트, 사진/광고 인증, 보상/경험치, 앱 사용법'에 관한지 판별하세요. "
            "관련이면 is_relevant=true, intent를 위 범주 중 하나로 지정. 확신도 0~1로 표시. JSON만."
        )
        schema = {
          "type":"object",
          "properties":{
            "is_relevant":{"type":"boolean"},
            "confidence":{"type":"number"},
            "intent":{"type":"string"},
            "reason":{"type":"string"}
          },
          "required":["is_relevant","confidence"]
        }
        # LLM 호출은 생략된 의사코드
        out = await self.llm.ainvoke(system=system, user=q, schema=schema)
        state.is_relevant = out["is_relevant"]
        state.confidence = out["confidence"]
        state.intent = out.get("intent")
        state.reason = out.get("reason")
        return state
