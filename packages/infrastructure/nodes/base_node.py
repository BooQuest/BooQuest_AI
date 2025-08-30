"""공통 노드 베이스 클래스 - 중복 제거 및 API 응답 최적화."""

from abc import ABC, abstractmethod
from typing import Dict, List, TypeVar, Generic, Union, Optional
from sqlalchemy import insert, update, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session
from packages.infrastructure.logging import get_logger
from packages.infrastructure.nodes.states.langgraph_state import LangGraphState

# 타입 변수 정의
T = TypeVar('T', bound=LangGraphState)

class BaseNode(ABC, Generic[T]):
    """모든 노드의 공통 베이스 클래스."""
    
    def __init__(self, name: str):
        """노드 초기화."""
        self.logger = get_logger(self.__class__.__name__)
        self.name = name
    
    def _update_state(self, state: T, updates: Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]], Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]], None]]) -> T:
        """상태 업데이트 - 항상 새 객체 생성으로 통일."""
        new_state = dict(state)  # TypedDict를 dict로 변환
        new_state.update(updates)
        return new_state
    
    def _safe_get(self, state: T, key: str, default: Optional[Union[int, str, bool, List[Dict[str, Union[int, str, bool]]], Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]]]] = None) -> Optional[Union[int, str, bool, List[Dict[str, Union[int, str, bool]]], Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]]]]:
        """안전하게 상태에서 값을 가져오기."""
        return state.get(key, default)
    
    def _safe_get_nested(self, state: T, *keys: str, default: Optional[Union[int, str, bool, List[Dict[str, Union[int, str, bool]]], Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]]]] = None) -> Optional[Union[int, str, bool, List[Dict[str, Union[int, str, bool]]], Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]]]]:
        """중첩된 키로 안전하게 값을 가져오기."""
        current = state
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, default)
            else:
                return default
        return current
    
    def _extract_common_fields(self, state: T) -> Dict[str, Optional[int]]:
        """공통 필드들을 추출하여 반환."""
        return {
            "user_id": self._safe_get(state, "user_id")
        }


class BaseSaveNode(BaseNode[T]):
    """공통 저장 로직을 제공하는 베이스 클래스."""
    
    def __init__(self, name: str, uow_factory, table: Table):
        super().__init__(name)
        self.uow_factory = uow_factory
        self.table = table
    
    def save_entities(self, state: T, entity_key: str, post_save_hook=None) -> T:
        """엔티티들을 저장합니다."""
        try:
            entities = self._safe_get_nested(state, "ai_result", entity_key, default=[])
            if not entities:
                self.logger.warning(f"{entity_key}가 없습니다.")
                return self._update_state(state, {"saved_entities": []})
            
            with self.uow_factory() as uow:
                saved_entities = self._process_entities(uow, entities, state)
                
                # 저장 후 후처리 훅 실행 (같은 트랜잭션에서)
                if post_save_hook:
                    post_save_hook(uow, state, saved_entities)
                
                # SqlAlchemyUoW는 컨텍스트 매니저로 자동 커밋됨
            
            # 공통 필드들 유지하면서 saved_entities 업데이트
            common_fields = {
                "user_id": state.get("user_id"),
                "profile_data": state.get("profile_data"),
                "request_data": state.get("request_data"),
                "sidejob_id": state.get("sidejob_id"),
                "mission_id": state.get("mission_id")
            }
            
            # None이 아닌 값만 포함
            filtered_common_fields = {k: v for k, v in common_fields.items() if v is not None}
            
            updates = {
                "saved_entities": saved_entities,
                **filtered_common_fields
            }
            
            return self._update_state(state, updates)
            
        except Exception as e:
            self.logger.error(f"{entity_key} 저장 실패: {e}")
            raise
    
    def _process_entities(self, uow: Session, entities: List[Dict[str, Union[int, str, bool]]], state: T) -> List[Dict[str, Union[int, str, bool]]]:
        """엔티티 처리 (INSERT/UPDATE)."""
        if not entities:
            return []
        

        return self._insert_entities(uow, entities, state)
    
    def _insert_entities(self, uow: Session, entities: List[Dict[str, Union[int, str, bool]]], state: T) -> List[Dict[str, Union[int, str, bool]]]:
        """엔티티 삽입."""
        insert_data = [self._prepare_data(entity, state) for entity in entities]
        stmt = insert(self.table).values(insert_data).returning(self.table.c.id)
        result = uow.session.execute(stmt)
        
        inserted_ids = result.fetchall()
        
        # INSERT된 entities에 ID와 모든 필드 추가
        for i, entity in enumerate(entities):
            if i < len(inserted_ids):
                # 원본 엔티티 데이터 유지하면서 ID와 prepared_data 추가
                prepared_data = insert_data[i]
                entity.update(prepared_data)
                entity["id"] = inserted_ids[i][0]
        
        return entities

    
    
    @abstractmethod
    def _prepare_data(self, entity: Dict[str, Union[int, str, bool]], state: T) -> Dict[str, Union[int, str, bool]]:
        """데이터 준비 (INSERT/UPDATE 공통)."""
        pass


class BaseGenerationNode(BaseNode[T]):
    """AI 생성 노드를 위한 베이스 클래스."""
    
    def __init__(self, name: str):
        super().__init__(name)
    
    def _update_generation_state(self, state: T, result) -> T:
        """생성 결과로 상태 업데이트 - 공통 로직."""
        # 공통 필드들 유지 (user_id 등)
        common_fields = {
            "user_id": state.get("user_id"),
            "profile_data": state.get("profile_data"),
            "request_data": state.get("request_data"),
            "sidejob_id": state.get("sidejob_id"),
            "mission_id": state.get("mission_id")
        }
        
        # None이 아닌 값만 포함
        filtered_common_fields = {k: v for k, v in common_fields.items() if v is not None}
        
        updates = {
            "ai_result": result.model_dump() if hasattr(result, 'model_dump') else result,
            **filtered_common_fields
        }
        
        updated_state = self._update_state(state, updates)
        
        return updated_state
    
    @abstractmethod
    def _prepare_prompt_data(self, state: T) -> Dict[str, Union[str, List[str]]]:
        """프롬프트 데이터 준비 (하위 클래스에서 구현)."""
        pass