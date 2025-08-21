import json
import re
from typing import TypeVar
from pydantic import BaseModel

from packages.infrastructure.logging import get_logger


T = TypeVar('T', bound=BaseModel)

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
        
        return content


    def parse_json_safely(self, text: str, logger) -> dict:
        cleaned = (text or "").strip()
        # 코드펜스 제거
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        # BOM/따옴표 정리
        cleaned = cleaned.replace("\ufeff", "").replace("“", "\"").replace("”", "\"").replace("’", "'")
        # 1차 시도
        try:
            return json.loads(cleaned)
        except Exception as e:
            logger.debug(f"[parse_json_safely] loads fail: {e}")

        # 바깥 { ... }만 추출
        s, e = cleaned.find("{"), cleaned.rfind("}")
        if s != -1 and e != -1 and e > s:
            core = cleaned[s:e+1]
            try:
                return json.loads(core)
            except Exception as e2:
                logger.debug(f"[parse_json_safely] outer fail: {e2}")

        # 단일 따옴표 → 쌍따옴표로 보수적 대체
        try_single = re.sub(r"(?<!\\)'", '"', cleaned)
        if try_single != cleaned:
            try:
                return json.loads(try_single)
            except Exception as e3:
                logger.debug(f"[parse_json_safely] single-quote fix fail: {e3}")

        logger.error("[parse_json_safely] cannot parse JSON. head=%s", cleaned[:200])
        raise ValueError("Invalid JSON")

    def is_brace_balanced(self, s: str) -> bool:
        c, in_str, esc = 0, False, False
        for ch in s:
            if ch == '"' and not esc:
                in_str = not in_str
            esc = (ch == '\\' and not esc) if in_str else False
            if not in_str:
                if ch == '{': c += 1
                elif ch == '}': c -= 1
                if c < 0: return False
        return c == 0