"""
AI 어댑터 공통 기능을 제공하는 베이스 클래스.

여러 AI 어댑터에서 중복되는 설정 로딩, AI 호출, 응답 파싱 로직을
한 곳에 모았습니다. 서브클래스는 특정 비즈니스 로직에 맞는 키나
후처리를 정의하기만 하면 됩니다.
"""

from typing import Dict, Any, Tuple, List, Optional
from packages.infrastructure.config import get_settings
from packages.infrastructure.services.utils.ai_config_factory import AIConfigFactory
from packages.infrastructure.services.utils.ai_response_reader import AIResponseReader
from packages.infrastructure.logging import get_logger


class BaseAIAdapter:
    """AI 호출 및 공통 파싱 로직을 담당하는 베이스 클래스."""

    def __init__(self, logger_name: str) -> None:
        self.settings = get_settings()
        self.ai_config_factory = AIConfigFactory()
        self.response_reader = AIResponseReader()
        self.logger = get_logger(logger_name)

    async def _call_openai(self, messages: Dict[str, str]) -> Tuple[str, Any]:
        """
        OpenAI(ChatGPT) API를 호출하여 응답 콘텐츠를 반환합니다.

        Args:
            messages: Chat API에 전달할 메시지 딕셔너리

        Returns:
            response_content: 모델의 응답 문자열 (JSON 포맷 포함 가능)
            model_config: 사용한 모델 설정 객체
        """
        try:
            import openai  # 지연 임포트
        except ImportError as ie:
            raise RuntimeError("openai 패키지가 필요합니다. 패키지를 설치해주세요.") from ie

        client = openai.OpenAI(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
        )
        model_config = self.ai_config_factory.create_ai_config(
            self.settings.clova_x_provider,
            self.settings.clova_x_model,
        )
        api_params = {
            "model": model_config.model,
            "messages": [messages],
            "temperature": model_config.temperature,
            "top_p": model_config.top_p,
            "stream": model_config.streaming,
        }
        if model_config.max_tokens is not None:
            api_params["max_tokens"] = model_config.max_tokens

        # API 호출
        response = client.chat.completions.create(**api_params)
        # 응답 추출
        response_content = self.response_reader.read_ai_response(
            response,
            is_streaming=model_config.streaming,
        )
        # 스트리밍 모드에서는 중괄호 균형 검증
        if model_config.streaming and not self.response_reader.is_brace_balanced(response_content):
            self.logger.warning("JSON brace not balanced; trying repair once.")
        return response_content, model_config

    def _parse_json(self, response_content: str) -> Dict[str, Any]:
        """
        JSON 문자열을 안전하게 파싱하여 딕셔너리로 반환합니다.

        파싱 실패 시 빈 딕셔너리를 반환하며 로그를 남깁니다.
        """
        try:
            parsed = self.response_reader.parse_json_safely(response_content, self.logger)
            return parsed if isinstance(parsed, dict) else {}
        except Exception as e:
            self.logger.warning(f"Parse fail; err={e}")
            return {}

    async def call_ai_and_extract(self, messages: Dict[str, str], key: str) -> List[Any]:
        """
        AI 모델을 호출하고 지정된 키로부터 리스트를 추출합니다.

        Args:
            messages: AI 모델에 전달할 메시지
            key: 응답 JSON에서 추출할 리스트의 키 (예: "result", "recommendations")

        Returns:
            추출된 리스트. 실패 시 빈 리스트 반환
        """
        try:
            response_content, _ = await self._call_openai(messages)
            parsed = self._parse_json(response_content)
            items = parsed.get(key, []) if isinstance(parsed, dict) else []
            # 결과가 리스트가 아닐 경우 빈 리스트 반환
            return items if isinstance(items, list) else []
        except Exception as e:
            self.logger.error(f"AI 호출 또는 파싱 중 오류: {str(e)}")
            return []