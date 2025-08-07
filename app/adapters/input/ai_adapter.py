from typing import Dict, Any
from app.application.ports.input.ai_port import AIInputPort
from app.infrastructure.logging import get_logger

class AIAdapter:
    def __init__(self, ai_input_port: AIInputPort):
        self.ai_input_port = ai_input_port
        self.logger = get_logger("AIAdapter")
    
    async def generate_big_tasks(self, user_profile_request) -> Dict[str, Any]:
        try:
            result = await self.ai_input_port.generate_big_tasks(user_profile_request)
            return result
            
        except Exception as e:
            self.logger.error(f"부업 임무 생성 실패: {str(e)}")
            raise 