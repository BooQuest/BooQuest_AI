"""부업 가이드 챗봇 응답 생성을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.prompts.chat_prompts import ChatPrompts
from packages.infrastructure.nodes.states.langgraph_state import ChatState
from langchain_naver import ChatClovaX


class ChatGenerationNode(BaseGenerationNode[ChatState]):
    """챗봇 응답 생성을 위한 LangGraph 노드."""

    def __init__(self):
        super().__init__("chat_generate")
        self.settings = get_settings()

        self.llm = ChatClovaX(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.5,
            max_tokens=1024,
            thinking={"effort": "none"},
        )

        self.prompt_templates = ChatPrompts()

    def __call__(self, state: ChatState) -> ChatState:
        try:
            prompt_data = self._prepare_prompt_data(state)
            prompt = self.prompt_templates.create_prompt_template()

            chain = prompt | self.llm
            result = chain.invoke(prompt_data)

            # result는 일반 텍스트일 것으로 가정
            payload = {"message": str(result)}
            updated_state = self._update_generation_state(state, payload)
            return updated_state
        except Exception as e:
            self.logger.error(f"챗봇 응답 생성 오류: {str(e)}")
            raise

    def _prepare_prompt_data(self, state: ChatState) -> Dict[str, Union[str, List[str]]]:
        request_data = self._safe_get(state, "request_data", {})
        history = request_data.get("history", [])
        if isinstance(history, list):
            # 간단한 텍스트 결합
            history_text = "\n".join([f"{turn.get('role','user')}: {turn.get('content','')}" for turn in history])
        else:
            history_text = str(history)

        prompt_data = {
#             "history": history_text,
            "message": request_data.get("message", "")
        }
        return prompt_data
