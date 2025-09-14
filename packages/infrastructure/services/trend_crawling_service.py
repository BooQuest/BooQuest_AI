"""SNS 트렌드 RSS 크롤링 서비스."""

import logging
from typing import List, Dict, Any
from packages.infrastructure.services.crawling.rss_crawler import RSSCrawler
from packages.infrastructure.services.trend_storage_service import TrendStorageService

logger = logging.getLogger(__name__)


class TrendCrawlingService:
    """SNS 트렌드 RSS 크롤링 서비스."""
    
    def __init__(self):
        self.storage_service = TrendStorageService()
        self.rss_crawler = RSSCrawler()
    
    def crawl_all_trends(self) -> Dict[str, int]:
        """SNS 트렌드 RSS 크롤링 및 저장."""
        try:
            logger.info("SNS 트렌드 RSS 크롤링 시작")
            trends = self.rss_crawler.crawl()
            
            if trends:
                saved_trends = self.storage_service.save_trends(trends)
                count = len(saved_trends)
                logger.info(f"SNS 트렌드 RSS 크롤링 완료: {count}개")
                return {"rss": count}
            else:
                logger.warning("SNS 트렌드 RSS 크롤링 결과 없음")
                return {"rss": 0}
                
        except Exception as e:
            logger.error(f"SNS 트렌드 RSS 크롤링 실패: {e}")
            return {"rss": 0}
    
    def crawl_platform_trends(self, platform: str) -> int:
        """RSS 트렌드 크롤링 (platform 파라미터는 호환성을 위해 유지)."""
        if platform != "rss":
            logger.warning(f"지원하지 않는 플랫폼: {platform}. RSS만 지원됩니다.")
            return 0
        
        try:
            logger.info("SNS 트렌드 RSS 크롤링 시작")
            trends = self.rss_crawler.crawl()
            
            if trends:
                saved_trends = self.storage_service.save_trends(trends)
                count = len(saved_trends)
                logger.info(f"SNS 트렌드 RSS 크롤링 완료: {count}개")
                return count
            else:
                logger.warning("SNS 트렌드 RSS 크롤링 결과 없음")
                return 0
                
        except Exception as e:
            logger.error(f"SNS 트렌드 RSS 크롤링 실패: {e}")
            return 0
    
    def search_trends(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """트렌드 검색."""
        try:
            return self.storage_service.search_similar_trends(query, limit)
        except Exception as e:
            logger.error(f"트렌드 검색 실패: {e}")
            raise