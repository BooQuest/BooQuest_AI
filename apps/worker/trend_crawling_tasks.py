"""SNS 트렌드 RSS 크롤링을 위한 Celery 태스크."""

import logging
from celery import shared_task
from packages.infrastructure.services.trend_crawling_service import TrendCrawlingService

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='crawl_sns_trends')
def crawl_sns_trends_task(self):
    """SNS 트렌드 RSS 크롤링 태스크."""
    try:
        logger.info("SNS 트렌드 RSS 크롤링 시작")
        crawling_service = TrendCrawlingService()
        results = crawling_service.crawl_all_trends()
        
        logger.info(f"SNS 트렌드 RSS 크롤링 완료: {results}")
        return results
    except Exception as e:
        logger.error(f"SNS 트렌드 RSS 크롤링 실패: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)