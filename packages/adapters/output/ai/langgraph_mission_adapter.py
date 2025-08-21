"""
미션 생성을 위한 LangGraph 어댑터.

기존 구현에서는 LangGraph의 StateGraph를 사용했지만, 실제로는 하나의
노드에서 AI 모델을 호출하여 결과를 얻는 단순한 흐름이므로, 공통 베이스
클래스를 활용하여 중복을 제거하고 로직을 간소화했습니다.
"""

from typing import Dict, List

from packages.adapters.output.ai.base_ai_adapter import BaseAIAdapter
from packages.application.ports.output.generate_mission_output_port import (
    GenerateMissionOutputPort,
)
from packages.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from packages.adapters.input.dto.generate_mission_response import GenerateMissionReponse
from packages.domain.entities.mission_draft import MissionDraft


class LangGraphMissionAdapter(BaseAIAdapter, GenerateMissionOutputPort):
    """AI를 통해 미션을 생성하는 어댑터."""

    def __init__(self) -> None:
        super().__init__("LangGraphMissionAdapter")

    async def generate_missions(
        self,
        messages: Dict[str, str],
        request: GenerateMissionRequest,
    ) -> GenerateMissionReponse:
        """AI를 호출하여 미션을 생성하고 응답 객체를 반환합니다."""
        items: List[Dict[str, str]] = await self.call_ai_and_extract(messages, "result")
        if not items:
            raise ValueError("AI 응답에서 미션 리스트가 비어 있습니다.")
        return GenerateMissionReponse(
            success=True,
            message="미션 생성 완료",
            tasks=[MissionDraft.model_validate(item) for item in items],
        )