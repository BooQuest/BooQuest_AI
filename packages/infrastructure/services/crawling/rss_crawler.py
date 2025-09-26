"""SNS 트렌드에 특화된 RSS 피드 크롤러."""

import logging
import feedparser
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dateutil import parser as date_parser
from packages.infrastructure.services.crawling.base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class RSSCrawler(BaseCrawler):
    """SNS 트렌드에 특화된 RSS 피드 크롤러."""
    
    def __init__(self):
        super().__init__()
        self.platform = "rss"
        # SNS 트렌드 관련 RSS 피드들 (작동하는 것들만)
        self.rss_feeds = {
            "social_media_trends": [
                "https://blog.hootsuite.com/feed/",
                "https://sproutsocial.com/insights/feed/",
                "https://blog.hubspot.com/marketing/rss.xml"
            ],
            "marketing_trends": [
                "https://marketingland.com/feed",
                "https://neilpatel.com/feed/"
            ],
            "tech_trends": [
                "https://techcrunch.com/feed/",
                "https://www.theverge.com/rss/index.xml",
                "https://mashable.com/feeds/rss/all",
                "https://www.wired.com/feed/rss"
            ],
            "startup_trends": [
                "https://www.entrepreneur.com/latest.rss",
                "https://www.forbes.com/innovation/feed2/",
                "https://www.businessinsider.com/rss"
            ]
        }
        
        # SNS 트렌드 관련 키워드
        self.sns_keywords = [
            'instagram', 'tiktok', 'youtube', 'facebook', 'twitter', 'linkedin',
            'social media', 'influencer', 'viral', 'trending', 'hashtag',
            'content creator', 'digital marketing', 'social commerce',
            'short video', 'reels', 'stories', 'live streaming',
            'user generated content', 'ugc', 'social selling',
            '부업', '사이드잡', '인플루언서', '크리에이터', '콘텐츠',
            '소셜미디어', '마케팅', '트렌드', '바이럴'
        ]

    def crawl(self) -> List[Dict[str, Any]]:
        """SNS 트렌드에 특화된 RSS 크롤링."""
        all_trends = []
        
        for trend_type, urls in self.rss_feeds.items():
            for url in urls:
                self._delay()
                try:
                    feed = feedparser.parse(url)
                    if feed.bozo:
                        logger.warning(f"RSS 피드 파싱 오류: {url} - {getattr(feed, 'bozo_exception', 'Unknown error')}")
                        continue
                    
                    for entry in feed.entries:
                        # 최근 7일 이내의 게시물만 필터링
                        published_date = self._parse_date(entry.published)
                        if published_date:
                            # timezone 정보가 있는 경우와 없는 경우 모두 처리
                            now = datetime.utcnow()
                            if published_date.tzinfo is None:
                                # timezone 정보가 없는 경우 UTC로 가정
                                published_date = published_date.replace(tzinfo=None)
                            else:
                                # timezone 정보가 있는 경우 UTC로 변환
                                published_date = published_date.astimezone().replace(tzinfo=None)
                            
                            if published_date > now - timedelta(days=7):
                                # SNS 트렌드 관련성 체크
                                if self._is_sns_related(entry):
                                    trend = self._create_trend_data(entry, trend_type, published_date)
                                    if trend:
                                        all_trends.append(trend)
                                    
                except Exception as e:
                    logger.error(f"RSS 피드 크롤링 실패 ({url}): {e}")
                    continue
        
        logger.info(f"SNS 트렌드 RSS 크롤링 완료: {len(all_trends)}개")
        return all_trends

    def _is_sns_related(self, entry) -> bool:
        """SNS 트렌드 관련성 체크."""
        try:
            # 제목과 내용을 합쳐서 키워드 검사
            title = entry.get('title', '')
            if isinstance(title, bytes):
                title = title.decode('utf-8', errors='ignore')
            title = title.lower()
            
            content = self._extract_content(entry).lower()
            combined_text = f"{title} {content}"
            
            # SNS 키워드가 포함되어 있는지 확인
            for keyword in self.sns_keywords:
                if keyword.lower() in combined_text:
                    return True
            
            # 해시태그나 소셜미디어 관련 패턴 검사
            social_patterns = [
                r'#\w+',  # 해시태그
                r'@\w+',  # 멘션
                r'social\s+media',
                r'digital\s+marketing',
                r'content\s+creator',
                r'influencer',
                r'viral',
                r'trending'
            ]
            
            for pattern in social_patterns:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"SNS 관련성 체크 실패: {e}")
            return False

    def _create_trend_data(self, entry, trend_type: str, published_date: datetime) -> Dict[str, Any]:
        """트렌드 데이터 생성."""
        try:
            content = self._extract_content(entry)
            tags = self._extract_tags(entry)
            
            # SNS 트렌드 타입 결정
            sns_trend_type = self._determine_sns_trend_type(entry, trend_type)
            
            return {
                "platform": self.platform,
                "trend_type": sns_trend_type,
                "title": entry.get('title', ''),
                "content": content,
                "url": entry.get('link', ''),
                "tags": tags,
                "engagement_metrics": self._extract_engagement_metrics(entry),
                "legal_implications": self._extract_legal_implications(entry),
                "created_at": published_date
            }
            
        except Exception as e:
            logger.error(f"트렌드 데이터 생성 실패: {e}")
            return None

    def _determine_sns_trend_type(self, entry, original_type: str) -> str:
        """SNS 트렌드 타입 결정."""
        try:
            title = entry.get('title', '').lower()
            content = self._extract_content(entry).lower()
            combined_text = f"{title} {content}"
            
            # 플랫폼별 트렌드 타입
            if any(platform in combined_text for platform in ['instagram', 'insta']):
                return 'instagram_trend'
            elif any(platform in combined_text for platform in ['tiktok', '틱톡']):
                return 'tiktok_trend'
            elif any(platform in combined_text for platform in ['youtube', '유튜브']):
                return 'youtube_trend'
            elif any(platform in combined_text for platform in ['facebook', '페이스북']):
                return 'facebook_trend'
            elif any(platform in combined_text for platform in ['twitter', '트위터']):
                return 'twitter_trend'
            elif any(platform in combined_text for platform in ['linkedin', '링크드인']):
                return 'linkedin_trend'
            elif any(keyword in combined_text for keyword in ['influencer', '인플루언서']):
                return 'influencer_trend'
            elif any(keyword in combined_text for keyword in ['marketing', '마케팅']):
                return 'marketing_trend'
            elif any(keyword in combined_text for keyword in ['startup', '스타트업', '부업', '사이드잡']):
                return 'startup_trend'
            else:
                return 'general_sns_trend'
                
        except Exception as e:
            logger.error(f"SNS 트렌드 타입 결정 실패: {e}")
            return 'general_sns_trend'

    def _extract_content(self, entry) -> str:
        """RSS 항목에서 내용 추출."""
        try:
            # summary 또는 description에서 내용 추출
            content = entry.get('summary', '') or entry.get('description', '')
            
            # UTF-8 인코딩 문제 해결
            if isinstance(content, bytes):
                try:
                    content = content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        content = content.decode('latin-1')
                    except UnicodeDecodeError:
                        content = content.decode('utf-8', errors='ignore')
            
            # HTML 태그 제거
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text(strip=True)
            
            # 특수 문자 정리
            if text_content:
                text_content = text_content.encode('utf-8', errors='ignore').decode('utf-8')
                return text_content[:1000]
            else:
                title = entry.get('title', '')
                if isinstance(title, bytes):
                    title = title.decode('utf-8', errors='ignore')
                return title
            
        except Exception as e:
            logger.error(f"내용 추출 실패: {e}")
            title = entry.get('title', '')
            if isinstance(title, bytes):
                title = title.decode('utf-8', errors='ignore')
            return title

    def _extract_tags(self, entry) -> List[str]:
        """RSS 항목에서 태그 추출."""
        try:
            tags = []
            
            # RSS 태그에서 추출
            if hasattr(entry, 'tags'):
                for tag in entry.tags:
                    tags.append(f"#{tag.term}")
            
            # 카테고리에서 추출
            if hasattr(entry, 'categories'):
                for category in entry.categories:
                    tags.append(f"#{category}")
            
            # SNS 관련 태그 추가
            title = entry.get('title', '').lower()
            content = self._extract_content(entry).lower()
            combined_text = f"{title} {content}"
            
            for keyword in self.sns_keywords:
                if keyword.lower() in combined_text:
                    tags.append(f"#{keyword}")
            
            return list(set(tags))[:10]  # 중복 제거 후 최대 10개
            
        except Exception as e:
            logger.error(f"태그 추출 실패: {e}")
            return []

    def _extract_engagement_metrics(self, entry) -> Dict[str, Any]:
        """참여도 지표 추출 (RSS에서는 제한적)."""
        try:
            # RSS에서는 직접적인 참여도 지표가 제한적
            # 대신 제목 길이나 내용 길이로 간접 추정
            title_length = len(entry.get('title', ''))
            content_length = len(self._extract_content(entry))
            
            return {
                "title_length": title_length,
                "content_length": content_length,
                "has_media": self._has_media_content(entry)
            }
            
        except Exception as e:
            logger.error(f"참여도 지표 추출 실패: {e}")
            return {}

    def _has_media_content(self, entry) -> bool:
        """미디어 콘텐츠 포함 여부 확인."""
        try:
            content = self._extract_content(entry)
            media_patterns = [
                r'<img', r'<video', r'<audio', r'youtube\.com', r'youtu\.be',
                r'instagram\.com', r'tiktok\.com', r'vimeo\.com'
            ]
            
            for pattern in media_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"미디어 콘텐츠 확인 실패: {e}")
            return False

    def _extract_legal_implications(self, entry) -> str:
        """법적 시사점 추출."""
        try:
            content = self._extract_content(entry)
            
            # 법적 키워드가 포함된 경우
            legal_keywords = [
                'privacy', 'gdpr', 'data protection', 'regulation', 'compliance',
                'privacy law', '개인정보', '규제', '정책', '법률', '규정'
            ]
            
            for keyword in legal_keywords:
                if keyword.lower() in content.lower():
                    return f"법적 시사점: {content[:200]}..."
            
            return None
            
        except Exception as e:
            logger.error(f"법적 시사점 추출 실패: {e}")
            return None

    def _parse_date(self, date_string: str) -> datetime:
        """날짜 문자열을 datetime 객체로 파싱."""
        try:
            return date_parser.parse(date_string)
        except (ValueError, TypeError):
            return datetime.utcnow()