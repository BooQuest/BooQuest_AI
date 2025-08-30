"""플랫폼별 사이드잡 데이터 로더 모듈.

기존에 사용하던 플랫폼별 사이드잡 데이터를 로드하고 활용합니다.
"""

import json
import os
from typing import List, Dict, Any
from packages.infrastructure.logging import get_logger

logger = get_logger("PlatformDataLoader")


class PlatformDataLoader:
    """플랫폼별 사이드잡 데이터를 로드하고 관리하는 클래스."""
    
    def __init__(self):
        self.logger = logger
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.platform_path = os.path.join(self.base_dir, "platform_side_jobs.json")
        self.sns_path = os.path.join(self.base_dir, "sns_side_jobs.json")
        self.expression_path = os.path.join(self.base_dir, "expression_side_jobs.json")

        # 데이터 로드
        self.platform_data = self._load_json_file(self.platform_path)
        self.sns_data = self._load_json_file(self.sns_path)
        self.expression_data = self._load_json_file(self.expression_path)
        
        # 플랫폼 이름 목록 생성
        self.all_platform_names = self._generate_platform_names()
    
    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        """JSON 파일을 로드합니다."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.logger.info(f"데이터 로드 완료: {file_path}")
                return data
        except Exception as e:
            self.logger.error(f"데이터 로드 실패: {file_path}, 오류: {str(e)}")
            return {}
    
    def _generate_platform_names(self) -> List[Dict[str, str]]:
        """모든 플랫폼 이름을 카테고리별로 생성합니다."""
        platform_names = []
        
        if "platforms" in self.platform_data:
            for category, names in self.platform_data["platforms"].items():
                for name in names:
                    platform_names.append({
                        "category": category,
                        "name": name
                    })
        
        return platform_names
    
    def get_platform_names(self, category: str = None) -> List[str]:
        """특정 카테고리의 플랫폼 이름을 반환합니다."""
        if category:
            return self.platform_data.get("platforms", {}).get(category, [])
        return [item["name"] for item in self.all_platform_names]
    
    def get_platform_categories(self) -> List[str]:
        """사용 가능한 플랫폼 카테고리를 반환합니다."""
        return list(self.platform_data.get("platforms", {}).keys())
    
    def get_media_types(self) -> Dict[str, List[str]]:
        """미디어 타입별 플랫폼을 반환합니다."""
        return self.sns_data.get("media_type", {})
    
    def get_topics(self) -> Dict[str, List[str]]:
        """주제별 카테고리를 반환합니다."""
        return self.sns_data.get("topic", {})
    
    def get_content_categories(self) -> Dict[str, List[str]]:
        """콘텐츠 카테고리를 반환합니다."""
        return self.sns_data.get("category", {})
    
    def get_content_formats(self) -> Dict[str, List[str]]:
        """콘텐츠 형식을 반환합니다."""
        return self.sns_data.get("format", {})
    
    def get_monetization_methods(self) -> Dict[str, List[str]]:
        """수익화 방법을 반환합니다."""
        return self.sns_data.get("monetization", {})
    
    def get_blog_platform_traits(self) -> Dict[str, str]:
        """블로그 플랫폼별 특성을 반환합니다."""
        return self.platform_data.get("blog_platform_traits", {})
    
    def get_random_platform_suggestion(self, category: str = None) -> str:
        """랜덤한 플랫폼 제안을 반환합니다."""
        import random
        
        if category:
            platforms = self.get_platform_names(category)
        else:
            platforms = self.get_platform_names()
        
        if platforms:
            return random.choice(platforms)
        return "유튜브"  # 기본값
    
    def get_platform_suggestions_by_media_type(self, media_type: str) -> List[str]:
        """미디어 타입에 따른 플랫폼 제안을 반환합니다."""
        media_platforms = self.get_media_types()
        return media_platforms.get(media_type, [])
    
    def get_topic_suggestions(self, category: str = None) -> List[str]:
        """주제 제안을 반환합니다."""
        topics = self.get_topics()
        if category:
            return topics.get(category, [])
        return [topic for topics_list in topics.values() for topic in topics_list]
    
    def get_content_format_suggestions(self, format_type: str = None) -> List[str]:
        """콘텐츠 형식 제안을 반환합니다."""
        formats = self.get_content_formats()
        if format_type:
            return formats.get(format_type, [])
        return [fmt for fmt_list in formats.values() for fmt in fmt_list]
    
    def get_expression_side_jobs(self, expression_type: str = None) -> Dict[str, List[str]]:
        """표현 방식(TEXT, IMAGE, VIDEO)에 따른 부업 리스트를 반환합니다."""
        if not self.expression_data:
            self.logger.warning("expression_side_jobs.json 데이터가 비어 있습니다.")
            return {}

        if expression_type:
            result = self.expression_data.get(expression_type.upper(), [])
            if not result:
                self.logger.warning(f"해당 표현 방식에 대한 데이터가 없습니다: {expression_type}")
            return {expression_type.upper(): result}

        return self.expression_data


# 싱글톤 인스턴스
platform_loader = PlatformDataLoader()
