"""임베딩 서비스를 위한 베이스 클래스."""

import logging
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from packages.infrastructure.config.config import get_settings

logger = logging.getLogger(__name__)


class BaseEmbeddingService(ABC):
    """임베딩 서비스를 위한 베이스 클래스."""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self.model_name = self.settings.embedding_model
        self.dimension = self.settings.embedding_dimension
    
    @abstractmethod
    def load_model(self):
        """임베딩 모델 로드 (하위 클래스에서 구현)."""
        pass
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """텍스트를 벡터로 변환 (하위 클래스에서 구현)."""
        pass
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """여러 텍스트를 벡터로 변환."""
        if not self.model:
            self.load_model()
        
        try:
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"텍스트 임베딩 실패: {e}")
            raise
    
    def create_embedding_data(self, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """트렌드 데이터로부터 임베딩 데이터 생성."""
        try:
            # 임베딩할 텍스트 조합
            text_to_embed = self._prepare_text_for_embedding(trend_data)
            
            # 임베딩 생성
            embedding_vector = self.embed_text(text_to_embed)
            
            # 임베딩 데이터 구성
            embedding_data = {
                "trend_id": trend_data.get("id"),
                "embedding_model": self.model_name,
                "embedding_vector": json.dumps(embedding_vector),
                "embedding_dimension": len(embedding_vector),
                "created_at": trend_data.get("created_at")
            }
            
            return embedding_data
            
        except Exception as e:
            logger.error(f"임베딩 데이터 생성 실패: {e}")
            raise
    
    def _prepare_text_for_embedding(self, trend_data: Dict[str, Any]) -> str:
        """임베딩을 위한 텍스트 준비."""
        # 제목, 내용, 태그를 조합하여 임베딩용 텍스트 생성
        title = trend_data.get("title", "")
        content = trend_data.get("content", "")
        tags = trend_data.get("tags", [])
        
        # 태그를 문자열로 변환
        tags_text = " ".join(tags) if tags else ""
        
        # 모든 텍스트를 조합
        combined_text = f"{title} {content} {tags_text}".strip()
        
        return combined_text
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """두 임베딩 벡터 간의 유사도 계산 (코사인 유사도)."""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # 코사인 유사도 계산
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"유사도 계산 실패: {e}")
            return 0.0
    
    def is_similar(self, embedding1: List[float], embedding2: List[float]) -> bool:
        """두 임베딩이 유사한지 확인."""
        similarity = self.calculate_similarity(embedding1, embedding2)
        return similarity >= self.settings.vector_similarity_threshold
