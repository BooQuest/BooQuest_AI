import json
from typing import Any, Optional, Dict, List
from app.infrastructure.logging import get_logger

class AIResponseReader:
    def __init__(self):
        self.logger = get_logger("AIResponseReader")
    
    def read_streaming_response(self, response) -> str:
        content = ""
        try:
            for chunk in response:
                if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta.content:
                    content += chunk.choices[0].delta.content
            self.logger.info(f"스트리밍 응답 수집 완료. 길이: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"스트리밍 응답 처리 실패: {str(e)}")
            return ""
    
    def read_non_streaming_response(self, response) -> str:
        try:
            content = response.choices[0].message.content
            self.logger.info(f"Non-streaming 응답 수집 완료. 길이: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Non-streaming 응답 처리 실패: {str(e)}")
            return ""

    def read_ai_response(self, response, is_streaming: bool) -> str:
        # 스트리밍 여부에 따른 응답 처리
        if is_streaming:
            content = self.read_streaming_response(response)
        else:
            content = self.read_non_streaming_response(response)
        
        return self.extract_json_from_markdown(content)
    
    def extract_json_from_markdown(self, content: str) -> str:
        """마크다운 코드 블록에서 JSON을 추출합니다."""
        if not content or not content.strip():
            return content
        
        # ```json ... ``` 패턴 찾기
        import re
        json_pattern = r'```json\s*(\{.*?\})\s*```'
        match = re.search(json_pattern, content, re.DOTALL)
        
        if match:
            return match.group(1)
        
        if match:
            return match.group(1)
        
        return content
    
        
