"""챗봇 대화 제목 생성을 위한 LangGraph 노드."""

from typing import Dict, Union
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.prompts.chat_title_prompts import ChatTitlePrompts
from packages.infrastructure.nodes.states.langgraph_state import TitleState
from langchain_naver import ChatClovaX


class ChatTitleGenerationNode(BaseGenerationNode[TitleState]):
    """챗봇 대화 제목 생성을 위한 LangGraph 노드."""

    def __init__(self):
        super().__init__("chat_title_generate")
        self.settings = get_settings()

        self.llm = ChatClovaX(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.3,
            max_tokens=50,
            thinking={"effort": "none"},
        )

        self.prompt_templates = ChatTitlePrompts()

    def __call__(self, state: TitleState) -> TitleState:
        try:
            prompt_data = self._prepare_prompt_data(state)
            prompt = self.prompt_templates.create_prompt_template()

            chain = prompt | self.llm
            result = chain.invoke(prompt_data)

            # result에서 텍스트 추출
            text = getattr(result, "content", None) or str(result)
            # 제목 정리 (불필요한 문장부호 제거)
            title = text.strip().replace('"', '').replace("'", '')

            payload = {"title": title}
            updated_state = self._update_generation_state(state, payload)
            return updated_state
        except Exception as e:
            self.logger.error(f"챗봇 제목 생성 오류: {str(e)}")
            raise

    def _prepare_prompt_data(self, state: TitleState) -> Dict[str, Union[str]]:
        request_data = self._safe_get(state, "request_data", {})
        return {
            "message": request_data.get("message", "")
        }
