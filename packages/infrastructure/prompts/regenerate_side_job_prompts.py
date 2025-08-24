"""사이드잡 재생성을 위한 고도화된 프롬프트."""

from langchain_core.prompts import ChatPromptTemplate
from packages.infrastructure.utils.platform_data_loader import platform_loader


class RegenerateSideJobPrompts:
    """사이드잡 재생성을 위한 고도화된 프롬프트 클래스."""
    
    def __init__(self):
        """프롬프트 초기화."""
        # platform_loader는 이미 싱글톤으로 구현되어 있음
        pass
    
    def create_prompt_template(self, job: str, hobbies: list, expression_style: str, strength_type: str, 
                             feedback_reasons: list, etc_feedback: str = None) -> ChatPromptTemplate:
        """사이드잡 재생성 프롬프트 템플릿을 생성합니다."""
        
        # platform_loader를 통해 플랫폼 정보 가져오기
        platform_names = platform_loader.all_platform_names
        
        # SNS 정보 가져오기
        sns_platforms = []
        media_types = platform_loader.get_media_types()
        for media_type, platforms in media_types.items():
            for platform in platforms:
                sns_platforms.append({"platform": platform, "type": media_type})
        
        # 플랫폼 정보를 문자열로 변환
        platform_names_str = ", ".join([item["name"] for item in platform_names])
        sns_platforms_str = ", ".join([f"{p['platform']} ({p['type']})" for p in sns_platforms])
        
        system_prompt = """당신은 사용자의 피드백을 바탕으로 사이드잡을 재생성하는 AI 어시스턴트입니다.

기존 제안의 문제점을 파악하고 개선된 새로운 제안을 해야 합니다.
각 사이드잡은 "[분위기] + [주제] + [형식] + [플랫폼]" 형태로 구성되어야 합니다.

반드시 정확한 JSON 형식으로 응답해야 하며, side_jobs 배열에 3개의 사이드잡을 포함해야 합니다."""

        feedback_text = f"피드백 사유: {', '.join(feedback_reasons)}"
        if etc_feedback:
            feedback_text += f"\n추가 피드백: {etc_feedback}"
        
        user_prompt = f"""사용자 정보:
- 직업: {job}
- 취미: {', '.join(hobbies)}
- 표현 스타일: {expression_style}
- 강점: {strength_type}

{feedback_text}

사용 가능한 플랫폼:
{platform_names_str}

사용 가능한 SNS 플랫폼:
{sns_platforms_str}

위 피드백을 바탕으로 개선된 사이드잡 3개를 제안해주세요.

응답 형식:
{{{{  
  "side_jobs": [
    {{{{  
      "title": "[분위기] + [주제] + [형식] + [플랫폼] 형태의 제목",
      "description": "구체적인 설명과 실현 방법"
    }}}},
    {{{{  
      "title": "[분위기] + [주제] + [형식] + [플랫폼] 형태의 제목",
      "description": "구체적인 설명과 실현 방법"
    }}}},
    {{{{  
      "title": "[분위기] + [주제] + [형식] + [플랫폼] 형태의 제목",
      "description": "구체적인 설명과 실현 방법"
    }}}}
  ]
}}}}

피드백을 반영하여 더 적합하고 실현 가능한 제안을 해주세요."""

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
