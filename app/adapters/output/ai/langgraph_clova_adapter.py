"""
LangGraph Clova X 어댑터
LangGraph를 사용하여 Clova X AI 서비스를 호출합니다.
"""
from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from app.application.ports.output.ai_port import AIPort
from app.domain.entities.ai_model import ChatMessage, AIModelConfig
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings

class LangGraphClovaAdapter(AIPort):
    """LangGraph를 사용한 Clova X AI 서비스 어댑터"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger("LangGraphClovaAdapter")
        
        # LangChain OpenAI 클라이언트 초기화 (Clova X 호환)
        self.llm = ChatOpenAI(
            api_key=self.settings.clova_x_api_key,
            base_url="https://clovastudio.stream.ntruss.com/v1/openai",
            model="HCX-005",
            temperature=0.7,
            max_tokens=1000
        )
        
        # LangGraph 워크플로우 설정
        self._setup_workflow()
    
    def _setup_workflow(self):
        """LangGraph 워크플로우 설정"""
        # 상태 정의
        workflow = StateGraph(StateType=Dict[str, Any])
        
        # 노드 추가
        workflow.add_node("process_question", self._process_question)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("format_output", self._format_output)
        
        # 엣지 연결
        workflow.set_entry_point("process_question")
        workflow.add_edge("process_question", "generate_response")
        workflow.add_edge("generate_response", "format_output")
        workflow.add_edge("format_output", END)
        
        # 워크플로우 컴파일
        self.app = workflow.compile()
    
    def _process_question(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """질문 처리 노드"""
        question = state.get("question", "")
        self.logger.info(f"질문 처리: {question[:50]}...")
        
        # 질문을 LangChain 메시지로 변환
        messages = [HumanMessage(content=question)]
        
        return {
            **state,
            "messages": messages,
            "processed": True
        }
    
    def _generate_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """응답 생성 노드"""
        messages = state.get("messages", [])
        
        # LangChain을 사용하여 응답 생성
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "ai_response": response,
            "generated": True
        }
    
    def _format_output(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """출력 포맷팅 노드"""
        ai_response = state.get("ai_response")
        
        # OpenAI 호환 형식으로 변환
        formatted_response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": ai_response.content
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 0,  # 실제 토큰 수는 추후 구현
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
        
        return {
            **state,
            "formatted_response": formatted_response
        }
    
    async def chat_completion(self, messages: List[ChatMessage], model_config: AIModelConfig) -> Dict[str, Any]:
        """
        채팅 완성 생성 (LangGraph 사용)
        
        Args:
            messages: 채팅 메시지 목록
            model_config: AI 모델 설정
            
        Returns:
            AI 응답
        """
        try:
            self.logger.info(f"LangGraph 채팅 완성 요청 - 메시지 수: {len(messages)}")
            
            # 마지막 사용자 메시지 추출
            user_message = messages[-1].content if messages else ""
            
            # LangGraph 워크플로우 실행
            result = self.app.invoke({
                "question": user_message,
                "temperature": model_config.temperature,
                "max_tokens": model_config.max_tokens
            })
            
            # 결과에서 포맷된 응답 추출
            response = result.get("formatted_response", {})
            
            self.logger.info("LangGraph 채팅 완성 성공")
            return response
            
        except Exception as e:
            self.logger.error(f"LangGraph 채팅 완성 실패: {str(e)}")
            raise 