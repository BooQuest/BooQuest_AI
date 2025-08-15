from fastapi import APIRouter
from app.adapters.input.dto.big_task_response import BigTaskResponse
from app.infrastructure.logging import get_logger
from app.infrastructure.dependency_injection import resolve
from app.application.ports.input.ai_input_port import AIInputPort
from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
from .dto.user_profile_dto import UserProfileRequest
from .dto.side_job_response import SideJobResponse
from .dto.onboarding_profile_dto import OnboardingProfileRequest
from app.adapters.input.dto.side_job_response import SideJobItem

router = APIRouter(prefix="/ai", tags=["AI"])
logger = get_logger("AIHttpAdapter")

@router.post("/generate-tasks", response_model=BigTaskResponse)
async def generate_big_tasks(request: UserProfileRequest):
    try:
        # 의존성 주입 컨테이너를 통해 AIInputPort 가져오기
        ai_input_port = resolve(AIInputPort)
        result = await ai_input_port.generate_big_tasks(request)
        
        # BigTaskResponse DTO를 사용하여 응답 반환
        return BigTaskResponse(
            success=True,
            big_tasks=result,
            message="태스크 생성이 완료되었습니다."
        )
        
    except Exception as e:
        logger.error(f"태스크 생성 실패: {str(e)}")
        # 에러 발생 시에도 BigTaskResponse DTO 사용
        return BigTaskResponse(
            success=False,
            big_tasks=[],
            message=f"태스크 생성 중 오류가 발생했습니다: {str(e)}"
        )
    
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
    