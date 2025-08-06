"""
AI HTTP 어댑터
HTTP 요청을 AI 포트로 변환합니다.
"""
from fastapi import APIRouter, HTTPException
from app.application.ports.input.ai_port import AIInputPort
from app.domain.entities.ai_model import AIModelConfig, LLMProvider, LLMModel
from app.infrastructure.dependency_injection import resolve_dependency
from app.infrastructure.logging import get_logger
from .dto.ai_dto import AIRequest, AIResponse

class AIHttpAdapter:
    """AI HTTP 어댑터"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/api", tags=["ai"])
        self.logger = get_logger("AIHttpAdapter")
        self._setup_routes()
    
    def _setup_routes(self):
        """라우트 설정"""
        self.router.post("/chat", response_model=AIResponse)(self.ask_ai)
    
    async def ask_ai(self, request: AIRequest):
        """AI에게 질문을 합니다."""
        try:
            self.logger.info(f"AI 질문 요청: {request.question[:50]}...")
            
            # AI 모델 설정
            model_config = AIModelConfig(
                provider=LLMProvider.CLOVA_X,
                model=LLMModel.CLOVA_X_HCX_005,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            # AI 입력 포트를 통해 질문
            ai_input_port = resolve_dependency(AIInputPort)
            response = await ai_input_port.ask_question(request.question, model_config)
            
            # 응답 내용 추출
            answer_content = response["choices"][0]["message"]["content"]
            
            # 응답 변환
            result = AIResponse(
                answer=answer_content,
                usage=response["usage"]
            )
            
            self.logger.info("AI 질문 응답 성공")
            return result
            
        except Exception as e:
            self.logger.error(f"AI 질문 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI 질문 실패: {str(e)}") 