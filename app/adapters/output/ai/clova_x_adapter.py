"""
Clova X 어댑터
Clova X AI 서비스를 애플리케이션의 AI 포트로 변환합니다.
"""
from typing import List, Dict, Any
from openai import OpenAI
from app.application.ports.output.ai_port import AIPort
from app.domain.entities.ai_model import ChatMessage, AIModelConfig
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings

class ClovaXAdapter(AIPort):
    """Clova X AI 서비스 어댑터"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger("ClovaXAdapter")
        
        # OpenAI 클라이언트 초기화
        self.client = OpenAI(
            api_key=self.settings.clova_x_api_key,
            base_url="https://clovastudio.stream.ntruss.com/v1/openai"
        )
        
    async def chat_completion(self, messages: List[ChatMessage], model_config: AIModelConfig) -> Dict[str, Any]:
        """
        채팅 완성 생성
        
        Args:
            messages: 채팅 메시지 목록
            model_config: AI 모델 설정
            
        Returns:
            AI 응답
        """
        try:
            self.logger.info(f"Clova X 채팅 완성 요청 - 메시지 수: {len(messages)}")
            
            # OpenAI 클라이언트를 사용한 API 호출
            response = self.client.chat.completions.create(
                model="HCX-005",  # Clova X 모델명
                messages=[
                    {
                        "role": msg.role,
                        "content": msg.content
                    } for msg in messages
                ],
                temperature=model_config.temperature,
                max_tokens=model_config.max_tokens
            )
            
            # 응답 내용 추출
            content = response.choices[0].message.content
            self.logger.info(f"Clova X 응답 내용: {content[:100]}...")
            
            # OpenAI 응답 형식으로 변환
            result = {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": content
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
            self.logger.info("Clova X 채팅 완성 성공")
            return result
            
        except Exception as e:
            self.logger.error(f"Clova X 채팅 완성 실패: {str(e)}")
            raise
    
