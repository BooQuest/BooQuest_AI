from fastapi import APIRouter
from app.infrastructure.logging import get_logger
from app.infrastructure.dependency_injection import resolve
from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
from .dto.side_job_response import SideJobResponse
from .dto.onboarding_profile_dto import OnboardingProfileRequest

router = APIRouter(prefix="/ai", tags=["AI"])
logger = get_logger("AIHttpAdapter")
    
@router.post("/generate-side-job", response_model=SideJobResponse)
async def generate_side_job(request: OnboardingProfileRequest):
    try:
        ai_input_port = resolve(AISideJobInputPort)
        return await ai_input_port.generate_side_jobs(request)  
    
    except Exception as e:
        logger.error(f"부업 생성 실패: {str(e)}")
        return SideJobResponse(
            success=False,
            message=f"부업 생성 실패: {str(e)}",
            tasks=[],
            prompt=""
        )
    