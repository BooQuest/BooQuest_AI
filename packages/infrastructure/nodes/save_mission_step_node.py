"""미션 단계 저장 노드."""

from typing import Dict, Any
from sqlalchemy import insert, update
from packages.domain.entities.mission_step import MissionStep
from packages.infrastructure.logging import get_logger


class SaveMissionStepNode:
    """미션 단계 저장 노드."""
    
    def __init__(self, uow_factory):
        """노드 초기화."""
        self.uow_factory = uow_factory
        self.logger = get_logger(__name__)
    
    def save_mission_steps(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """미션 단계를 저장합니다."""
        try:
            # 상태에서 필요한 데이터 추출
            mission_id = state.get("mission_id")
            ai_result = state.get("ai_result", {})
            mission_steps = ai_result.get("mission_steps", [])
            
            if not mission_steps:
                self.logger.warning("저장할 미션 단계가 없습니다.")
                return {**state, "saved_mission_steps": []}
            
            # 데이터베이스에 저장
            with self.uow_factory() as uow:
                saved_steps = []
                
                # 첫 번째 step의 ID 유무로 전체 판단
                has_ids = mission_steps[0].get("id") is not None if mission_steps else False
                
                if has_ids:
                    # 전부 UPDATE
                    self.logger.info("모든 미션 단계를 UPDATE로 처리합니다.")
                    
                    for step in mission_steps:
                        stmt = (
                            update(MissionStep)
                            .where(MissionStep.c.id == step["id"])
                            .values(
                                mission_id=mission_id,
                                seq=step.get("seq", 1),
                                title=step.get("title", ""),
                                detail=step.get("detail", ""),
                                status="PLANNED"
                            )
                        )
                        result = uow.session.execute(stmt)
                        self.logger.info(f"UPDATE 완료: ID {step['id']}")

                        saved_steps.append(step)
                else:
                    # 전부 INSERT - Bulk INSERT
                    self.logger.info("모든 미션 단계를 Bulk INSERT로 처리합니다.")
                    
                    # Bulk INSERT를 위한 데이터 준비
                    insert_data = []
                    for step in mission_steps:
                        insert_data.append({
                            "mission_id": mission_id,
                            "seq": step.get("seq", 1),
                            "title": step.get("title", ""),
                            "detail": step.get("detail", ""),
                            "status": "PLANNED"
                        })
                    
                    # Bulk INSERT 실행 - RETURNING 절로 ID 가져오기
                    stmt = insert(MissionStep).values(insert_data).returning(MissionStep.c.id)
                    result = uow.session.execute(stmt)
                    
                    # RETURNING으로 반환된 ID들 가져오기
                    inserted_ids = result.fetchall()
                    for i, step in enumerate(mission_steps):
                        step_id = inserted_ids[i][0] if i < len(inserted_ids) else None
                        # step 객체에 ID 추가
                        step_with_id = {**step, "id": step_id, "status": "PLANNED"}
                        saved_steps.append(step_with_id)
                        self.logger.info(f"Bulk INSERT 완료: ID {step_id}")
            
            self.logger.info(f"미션 단계 {len(saved_steps)}개 저장 완료")
            
            # 상태에 저장된 미션 단계 정보 추가
            return {**state, "saved_mission_steps": saved_steps}
            
        except Exception as e:
            self.logger.error(f"미션 단계 저장 실패: {e}")
            raise
