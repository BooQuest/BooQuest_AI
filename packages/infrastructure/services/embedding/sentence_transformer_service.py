"""Sentence Transformers를 사용한 임베딩 서비스."""

import logging
from typing import List
from sentence_transformers import SentenceTransformer
from packages.infrastructure.services.embedding.base_embedding_service import BaseEmbeddingService

logger = logging.getLogger(__name__)


class SentenceTransformerEmbeddingService(BaseEmbeddingService):
    """Sentence Transformers를 사용한 임베딩 서비스."""
    
    def __init__(self):
        super().__init__()
        self.model = None
    
    def load_model(self):
        """Sentence Transformers 모델 로드."""
        try:
            logger.info(f"임베딩 모델 로딩 시작: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("임베딩 모델 로딩 완료")
            
        except Exception as e:
            logger.error(f"임베딩 모델 로딩 실패: {e}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """텍스트를 벡터로 변환."""
        if not self.model:
            self.load_model()
        
        try:
            # 텍스트 임베딩
            embedding = self.model.encode([text])
            return embedding[0].tolist()
            
        except Exception as e:
            logger.error(f"텍스트 임베딩 실패: {e}")
            raise
    
    def embed_texts_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """배치로 여러 텍스트를 임베딩."""
        if not self.model:
            self.load_model()
        
        try:
            # 배치 단위로 임베딩
            embeddings = []
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.model.encode(batch_texts)
                embeddings.extend(batch_embeddings.tolist())
            
            return embeddings
            
        except Exception as e:
            logger.error(f"배치 임베딩 실패: {e}")
            raise
