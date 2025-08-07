from fastapi import APIRouter, HTTPException
from app.infrastructure.logging import get_logger
from app.infrastructure.dependency_injection import resolve
from app.application.ports.input.ai_port import AIInputPort
from .dto.user_profile_dto import UserProfileRequest, BigTaskResponse

router = APIRouter(prefix="/ai", tags=["AI"])
logger = get_logger("AIHttpAdapter")

@router.post("/generate-tasks", response_model=BigTaskResponse)
async def generate_big_tasks(request: UserProfileRequest):
    try:
        # 의존성 주입 컨테이너를 통해 AIInputPort 가져오기
        ai_input_port = resolve(AIInputPort)
        result = await ai_input_port.generate_big_tasks(request)
        
        return BigTaskResponse(
            success=True,
            big_tasks=result.get("big_tasks", []),
            message="태스크 생성이 완료되었습니다."
        )
        
    except Exception as e:
        logger.error(f"태스크 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"태스크 생성 중 오류가 발생했습니다: {str(e)}")