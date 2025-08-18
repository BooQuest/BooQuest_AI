from app.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from app.adapters.input.dto.generate_mission_step_response import GenerateMissionStepResponse
from app.application.ports.input.mission_step_generation_input_port import MissionStepGenerationInputPort
from app.application.ports.output.mission_step_generation_output_port import MissionStepGenerationOutputPort
from app.infrastructure.logging import get_logger
from app.infrastructure.services.utils.prompt_templates import PromptTemplates

class AIMissionStepGenerationUseCase(MissionStepGenerationInputPort):
    def __init__(self, mission_step_generation_output_port: MissionStepGenerationOutputPort):
        self.mission_step_generation_output_port = mission_step_generation_output_port
        self.logger = get_logger("AIStepGenerationUseCase")
    
    async def generate_mission_steps(self, request: GenerateMissionStepRequest) -> GenerateMissionStepResponse:
        """미션 스텝 생성을 위한 유스케이스"""
        
        self.logger.info(f"사용자 {request.user_id}의 미션 스텝 생성 시작")
        
        # 공통 프롬프트 템플릿 사용
        prompt = PromptTemplates.generate_mission_step_prompt(request)
        
        messages = {"role": "user", "content": prompt}
        
        # AI를 통해 미션 스텝 생성
        return await self.mission_step_generation_output_port.generate_mission_steps(messages, request)
