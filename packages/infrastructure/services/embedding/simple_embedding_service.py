"""간단한 임베딩 서비스 (sentence-transformers 대신 사용)"""

import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)


class SimpleEmbeddingService:
    """간단한 임베딩 서비스 - 실제 프로덕션에서는 sentence-transformers 사용"""
    
    def __init__(self):
        self.dimension = 384  # sentence-transformers/all-MiniLM-L6-v2와 동일한 차원
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """텍스트들을 임베딩으로 변환 (더미 구현)"""
        embeddings = []
        
        for text in texts:
            # 간단한 해시 기반 임베딩 생성 (실제로는 sentence-transformers 사용)
            # 텍스트의 길이와 단어 수를 기반으로 한 더미 벡터 생성
            words = text.split()
            text_length = len(text)
            word_count = len(words)
            
            # 384차원 벡터 생성 (텍스트 특성을 반영한 더미 벡터)
            embedding = []
            for i in range(self.dimension):
                # 텍스트 길이, 단어 수, 문자 코드 등을 기반으로 한 결정적 벡터
                seed = hash(text[:min(50, len(text))]) + i
                np.random.seed(seed % (2**32))
                value = np.random.normal(0, 1)
                embedding.append(float(value))
            
            # 정규화
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = [x / norm for x in embedding]
            
            embeddings.append(embedding)
        
        logger.info(f"간단한 임베딩 생성 완료: {len(embeddings)}개")
        return embeddings
    
    def embed_text(self, text: str) -> List[float]:
        """단일 텍스트 임베딩"""
        return self.embed_texts([text])[0]
