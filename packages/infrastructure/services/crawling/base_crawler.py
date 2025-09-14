"""기본 크롤링 서비스를 위한 베이스 클래스."""

import time
import random
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from packages.infrastructure.config.config import get_settings

logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """크롤링을 위한 베이스 클래스."""
    
    def __init__(self):
        self.settings = get_settings()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.settings.crawling_user_agent
        })
    
    def _get_delay(self) -> float:
        """크롤링 간 지연 시간을 랜덤하게 반환."""
        return random.uniform(self.settings.crawling_delay_min, self.settings.crawling_delay_max)
    
    def _delay(self):
        """크롤링 간 지연."""
        delay = self._get_delay()
        logger.debug(f"크롤링 지연: {delay:.2f}초")
        time.sleep(delay)
    
# Selenium 메서드들 제거됨 - RSS 크롤러는 requests만 사용
    
    def _safe_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """안전한 HTTP 요청."""
        try:
            response = self.session.request(
                method, 
                url, 
                timeout=self.settings.crawling_timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"HTTP 요청 실패 ({url}): {e}")
            return None
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        """HTML 파싱."""
        return BeautifulSoup(html, 'html.parser')
    
    def _extract_text(self, element) -> str:
        """요소에서 텍스트 추출."""
        if element:
            return element.get_text(strip=True)
        return ""
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """페이지에서 링크 추출."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            if self._is_valid_url(full_url):
                links.append(full_url)
        return list(set(links))  # 중복 제거
    
    def _is_valid_url(self, url: str) -> bool:
        """유효한 URL인지 확인."""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.scheme in ['http', 'https']
        except:
            return False
    
    @abstractmethod
    def crawl(self) -> List[Dict[str, Any]]:
        """트렌드 정보 크롤링 (하위 클래스에서 구현)."""
        pass
    
    def __enter__(self):
        """컨텍스트 매니저 진입."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료."""
        self.session.close()
