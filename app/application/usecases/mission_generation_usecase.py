
from app.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from app.adapters.input.dto.generate_mission_response import GenerateMissionReponse
from app.application.ports.input.generate_mission_input_port import GenerateMissionInputPort
from app.application.ports.output.generate_mission_output_port import GenerateMissionOutputPort
from app.infrastructure.services.utils.prompt_templates import PromptTemplates
from app.infrastructure.logging import get_logger

class AIGenerateMissionUseCase(GenerateMissionInputPort):
    def __init__(self, mission_generation_output_port: GenerateMissionOutputPort):
        self.mission_generation_output_port = mission_generation_output_port
        self.logger = get_logger("MissionGenerationUseCase")
    
    async def generate_missions(self, request: GenerateMissionRequest) -> GenerateMissionReponse:
        
        # 공통 프롬프트 템플릿 사용
        prompt = PromptTemplates.generate_recommendation_mission_prompt(request)

        messages = {"role": "user", "content": prompt}

        return await self.mission_generation_output_port.generate_missions(messages, request)
    
