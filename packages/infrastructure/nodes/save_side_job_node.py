"""사이드잡 저장 노드."""

from typing import Dict, Any
from sqlalchemy import insert, update
from packages.domain.entities.side_job import SideJob
from packages.infrastructure.logging import get_logger


class SaveSideJobNode:
    """사이드잡 저장 노드."""
    
    def __init__(self, uow_factory):
        """노드 초기화."""
        self.uow_factory = uow_factory
        self.logger = get_logger(__name__)
    
    def save_side_jobs(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡을 저장합니다."""
        try:
            # 상태에서 필요한 데이터 추출
            user_id = state.get("user_id")
            ai_result = state.get("ai_result", {})
            side_jobs = ai_result.get("side_jobs", [])
            
            if not side_jobs:
                self.logger.warning("저장할 사이드잡이 없습니다.")
                return {**state, "saved_side_jobs": []}
            
            # 데이터베이스에 저장
            with self.uow_factory() as uow:
                saved_jobs = []
                
                # 첫 번째 job의 ID 유무로 전체 판단
                has_ids = side_jobs[0].get("id") is not None if side_jobs else False
                
                if has_ids:
                    # 전부 UPDATE
                    self.logger.info("모든 사이드잡을 UPDATE로 처리합니다.")
                    
                    for job in side_jobs:
                        stmt = (
                            update(SideJob)
                            .where(SideJob.c.id == job["id"])
                            .values(
                                user_id=user_id,
                                title=job.get("title", ""),
                                description=job.get("description", ""),
                                prompt_meta=ai_result.get("prompt_meta", ""),
                                is_selected=False
                            )
                        )
                        result = uow.session.execute(stmt)
                        self.logger.info(f"UPDATE 완료: ID {job['id']}")
                    
                        saved_jobs.append(job)
                else:
                    # 전부 INSERT - Bulk INSERT
                    self.logger.info("모든 사이드잡을 Bulk INSERT로 처리합니다.")
                    
                    # Bulk INSERT를 위한 데이터 준비
                    insert_data = []
                    for job in side_jobs:
                        insert_data.append({
                            "user_id": user_id,
                            "title": job.get("title", ""),
                            "description": job.get("description", "설명이 제공되지 않았습니다"),
                            "prompt_meta": ai_result.get("prompt_meta", ""),
                            "is_selected": False
                        })
                    
                    # Bulk INSERT 실행 - RETURNING 절로 ID 가져오기
                    stmt = insert(SideJob).values(insert_data).returning(SideJob.c.id)
                    result = uow.session.execute(stmt)
                    
                    # RETURNING으로 반환된 ID들 가져오기
                    inserted_ids = result.fetchall()
                    for i, job in enumerate(side_jobs):
                        job_id = inserted_ids[i][0] if i < len(inserted_ids) else None
                        # job 객체에 ID 추가
                        job_with_id = {**job, "id": job_id}
                        saved_jobs.append(job_with_id)
                        self.logger.info(f"Bulk INSERT 완료: ID {job_id}")
            
            self.logger.info(f"사이드잡 {len(saved_jobs)}개 저장 완료")
            
            # 상태에 저장된 사이드잡 정보 추가
            return {**state, "saved_side_jobs": saved_jobs}
            
        except Exception as e:
            self.logger.error(f"사이드잡 저장 실패: {e}")
            raise
