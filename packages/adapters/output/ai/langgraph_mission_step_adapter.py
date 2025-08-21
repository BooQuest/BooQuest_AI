"""
미션 스텝 생성을 위한 LangGraph 어댑터.

중복을 줄이기 위해 BaseAIAdapter를 활용하여 AI 호출 및 파싱을 공통화하고,
미션 스텝 전용 로직만 정의합니다.
"""

from typing import Dict, List

from packages.adapters.output.ai.base_ai_adapter import BaseAIAdapter
from packages.application.ports.output.mission_step_generation_output_port import (
    MissionStepGenerationOutputPort,
)
from packages.adapters.input.dto.generate_mission_step_request import (
    GenerateMissionStepRequest,
)
from packages.adapters.input.dto.generate_mission_step_response import (
    GenerateMissionStepResponse,
)
from packages.domain.entities.mission_step import MissionStep


class LangGraphMissionStepAdapter(BaseAIAdapter, MissionStepGenerationOutputPort):
    """AI를 통해 미션 스텝을 생성하는 어댑터."""

    def __init__(self) -> None:
        super().__init__("LangGraphMissionStepAdapter")

    async def generate_mission_steps(
        self,
        messages: Dict[str, str],
        request: GenerateMissionStepRequest,
    ) -> GenerateMissionStepResponse:
        """AI를 호출하여 미션 스텝 목록을 생성하고 응답 객체를 반환합니다."""
        items: List[Dict[str, str]] = await self.call_ai_and_extract(messages, "result")
        if not items:
            raise ValueError("AI 응답에서 미션 스텝 리스트가 비어 있습니다.")
        return GenerateMissionStepResponse(
            success=True,
            message="미션 생성 완료",
            steps=[MissionStep(**item) for item in items],
        )