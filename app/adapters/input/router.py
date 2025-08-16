from multiprocessing import get_logger
from fastapi import APIRouter
from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
from app.application.ports.input.generate_mission_input_port import GenerateMissionInputPort
from app.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from app.adapters.input.dto.generate_mission_response import GenerateMissionReponse
from app.adapters.input.dto.onboarding_profile_dto import OnboardingProfileRequest
from app.adapters.input.dto.side_job_response import SideJobResponse
from app.infrastructure.dependency_injection import resolve
from app.infrastructure.logging import get_logger

router = APIRouter(prefix="/ai", tags=["AI"])
logger = get_logger("AIHttpAdapter")
    
@router.post("/generate-side-job", response_model=SideJobResponse)
async def generate_side_job(request: OnboardingProfileRequest):
    try:
        ai_input_port = resolve(AISideJobInputPort)
        return await ai_input_port.generate_side_jobs(request)  
    
    except Exception as e:
        return SideJobResponse(
            success=False,
            message=f"부업 생성 실패: {str(e)}",
            tasks=[],
            prompt=""
        )

@router.post("/generate-mission", response_model=GenerateMissionReponse)
async def generate_missions(request: GenerateMissionRequest):
    try:
        use_case = resolve(GenerateMissionInputPort)
        return await use_case.generate_missions(request)
    except Exception as e:
        return GenerateMissionReponse(
            success=False,
            message=f"미션 생성 실패: {str(e)}",
            tasks=[]
        )
    