"""
부업 아이디어 생성을 위한 LangGraph 어댑터.

이 어댑터는 BaseAIAdapter를 상속받아 AI 호출 및 응답 파싱 로직을 공통화하고,
부업 추천에 특화된 필드명을 지정하여 결과를 추출합니다.
"""

from typing import Dict, List, Union, Optional

from packages.adapters.output.ai.base_ai_adapter import BaseAIAdapter
from packages.application.ports.output.ai_sidejob_output_port import AISideJobOutputPort
from packages.domain.entities.onboarding_profile import OnboardingProfile
from packages.adapters.input.dto.side_job_response import SideJobResponse, SideJobItem
from packages.domain.entities.regenerate_side_job import RegenerateSideJobRequest


class LangGraphSideJobAdapter(BaseAIAdapter, AISideJobOutputPort):
    """AI를 통해 부업 아이디어를 생성하는 어댑터."""

    def __init__(self) -> None:
        super().__init__("LangGraphSideJobAdapter")

    from typing import Optional
    async def generate_tasks_for_sidejob(
        self,
        messages_or_request: Union[Dict[str, str], RegenerateSideJobRequest],
        onboarding_profile: Optional[OnboardingProfile] = None,
    ) -> SideJobResponse:
        """
        부업 생성을 위한 메서드.

        Args:
            messages_or_request: 유저 입력 메시지 또는 재생성 요청 객체
            onboarding_profile: 온보딩 프로필 (messages가 dict인 경우 필수)

        Returns:
            SideJobResponse: 성공 또는 실패 여부와 결과 데이터
        """
        try:
            # 재생성 요청이 아닌 경우: messages(dict)와 onboarding_profile 사용
            if isinstance(messages_or_request, dict):
                if onboarding_profile is None:
                    raise ValueError("OnboardingProfile은 필수입니다.")
                items: List[Dict[str, str]] = await self.call_ai_and_extract(
                    messages_or_request, "recommendations"
                )
                if not items:
                    raise ValueError("AI 응답에서 부업 리스트가 비어 있습니다.")
                return SideJobResponse(
                    success=True,
                    message="부업 생성 완료",
                    tasks=[SideJobItem(**item) for item in items],
                    prompt=messages_or_request.get("content", ""),
                )
            # 아래 분기는 regenerate_side_job 요청을 그대로 전달받는 경우를 위한 백업 플로우
            elif isinstance(messages_or_request, RegenerateSideJobRequest):
                # 현재 구현에서는 재생성 요청을 직접 처리하는 로직이 없으므로
                # 예외를 발생시켜 상위 계층에서 처리하도록 합니다.
                raise NotImplementedError(
                    "RegenerateSideJobRequest 타입은 직접 처리할 수 없습니다."
                )
            else:
                raise TypeError("지원하지 않는 타입입니다.")
        except Exception as e:
            self.logger.error(f"부업 생성 실패: {str(e)}")
            return SideJobResponse(
                success=False,
                message=f"부업 생성 실패: {str(e)}",
                tasks=[],
                prompt="",
            )