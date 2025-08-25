"""미션 저장 노드."""

from typing import Dict, Any
from sqlalchemy import insert, update
from packages.domain.entities.mission import Mission
from packages.domain.entities.side_job import SideJob
from packages.infrastructure.logging import get_logger


class SaveMissionNode:
    """미션 저장 노드."""
    
    def __init__(self, uow_factory):
        """노드 초기화."""
        self.uow_factory = uow_factory
        self.logger = get_logger(__name__)
    
    def save_missions(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """미션을 저장합니다."""
        try:
            # 상태에서 필요한 데이터 추출
            user_id = state.get("user_id")
            sidejob_id = state.get("sidejob_id")
            ai_result = state.get("ai_result", {})
            missions = ai_result.get("missions", [])
            
            if not missions:
                self.logger.warning("저장할 미션이 없습니다.")
                return {**state, "saved_missions": []}
            
            # 데이터베이스에 저장
            with self.uow_factory() as uow:
                saved_missions = []
                
                # 첫 번째 mission의 ID 유무로 전체 판단
                has_ids = missions[0].get("id") is not None if missions else False
                
                if has_ids:
                    # 전부 UPDATE
                    self.logger.info("모든 미션을 UPDATE로 처리합니다.")
                    
                    for mission in missions:
                        stmt = (
                            update(Mission)
                            .where(Mission.c.id == mission["id"])
                            .values(
                                user_id=user_id,
                                sidejob_id=sidejob_id,
                                title=mission.get("title", ""),
                                order_no=mission.get("orderNo", 1),
                                design_notes=mission.get("notes", ""),
                                status="PLANNED"
                            )
                        )
                        result = uow.session.execute(stmt)
                        self.logger.info(f"UPDATE 완료: ID {mission['id']}")

                        saved_missions.append(mission)
                else:
                    # 전부 INSERT - Bulk INSERT
                    self.logger.info("모든 미션을 Bulk INSERT로 처리합니다.")
                    
                    # Bulk INSERT를 위한 데이터 준비
                    insert_data = []
                    for mission in missions:
                        insert_data.append({
                            "user_id": user_id,
                            "sidejob_id": sidejob_id,
                            "title": mission.get("title", ""),
                            "order_no": mission.get("orderNo", 1),
                            "design_notes": mission.get("notes", ""),
                            "status": "PLANNED"
                        })
                    
                    # Bulk INSERT 실행 - RETURNING 절로 ID 가져오기
                    stmt = insert(Mission).values(insert_data).returning(Mission.c.id)
                    result = uow.session.execute(stmt)
                    
                    # RETURNING으로 반환된 ID들 가져오기
                    inserted_ids = result.fetchall()
                    for i, mission in enumerate(missions):
                        mission_id = inserted_ids[i][0] if i < len(inserted_ids) else None
                        # mission 객체에 ID 추가
                        mission_with_id = {**mission, "id": mission_id}
                        saved_missions.append(mission_with_id)
                        self.logger.info(f"Bulk INSERT 완료: ID {mission_id}")
                
                # 미션 저장 완료 후, 해당 사이드잡의 is_selected를 true로 업데이트
                if sidejob_id:
                    self.logger.info(f"사이드잡 ID {sidejob_id}의 is_selected를 true로 업데이트합니다.")
                    
                    # 사이드잡 업데이트
                    update_stmt = (
                        update(SideJob)
                        .where(SideJob.c.id == sidejob_id)
                        .values(is_selected=True)
                    )
                    
                    result = uow.session.execute(update_stmt)
                    self.logger.info(f"사이드잡 {sidejob_id} 업데이트 완료")
            
            self.logger.info(f"미션 {len(saved_missions)}개 저장 완료")
            
            # 상태에 저장된 미션 정보 추가
            return {**state, "saved_missions": saved_missions}
            
        except Exception as e:
            self.logger.error(f"미션 저장 실패: {e}")
            raise
