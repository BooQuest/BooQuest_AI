"""사용자 정의 부업 검증을 위한 LangGraph 노드."""

from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.nodes.states.langgraph_state import ValidateCustomSideJobState
from packages.core.external.google_genai.client import create_gemini_llm


class ValidateCustomSideJobNode(BaseGenerationNode[ValidateCustomSideJobState]):
    """사용자 입력 부업이 sns 부업인지 검증을 위한 LangGraph 노드."""

    def __init__(self):
        super().__init__("validate_custom_side_job")
        self.settings = get_settings()

        # Gemini 3 Flash 설정
        self.llm = create_gemini_llm(
            temperature=0.3,
            max_output_tokens=512,
        )

    def __call__(self, state: ValidateCustomSideJobState) -> ValidateCustomSideJobState:
        """부업 검증 실행."""
        try:
            self.logger.info("사용자 정의 부업 검증 시작")
            prompt_data = self._prepare_prompt_data(state)
            side_job = prompt_data.get("side_job", "")

            if not side_job:
                self.logger.warning("검증할 side_job이 없습니다.")
                return {**state, "ai_result": False}

            # 프롬프트 생성
            prompt = (
                f"'{side_job}'이라는 부업이 SNS(소셜 미디어)를 활용한 부업인지 여부를 판단해줘. "
                f"오직 'True' 또는 'False'로만 답변해."
            )
            self.logger.info(f"프롬프트생성")
            # LLM 호출
            result = self.llm.invoke(prompt)
            answer = str(result).strip().lower()

            # 결과 판별
            is_valid = "true" in answer

            self.logger.info(f"부업 검증 완료: '{side_job}' → {is_valid}")
            return {**state, "ai_result": is_valid}

        except Exception as e:
            self.logger.error(f"부업 검증 중 오류: {str(e)}")
            return {**state, "ai_result": False}
        

    def _prepare_prompt_data(self, state: ValidateCustomSideJobState) -> dict:
        """BaseGenerationNode에서 요구하는 추상 메서드 구현"""
        # state에서 필요한 데이터를 뽑아 프롬프트용 dict 반환
        return {"side_job": state.get("request_data", "").strip()}
