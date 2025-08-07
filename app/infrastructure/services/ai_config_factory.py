from httpx import stream
from app.domain.entities.user_profile import UserProfile
from app.domain.entities.ai_model import AIModelConfig
from app.infrastructure.config import get_settings

class AIConfigFactory:
    def __init__(self):
        self.settings = get_settings()
    
    def create_base_config(self, provider: str, model: str) -> AIModelConfig:
        return AIModelConfig(
            provider=provider,
            model=model,
            temperature=self.settings.default_temperature,
            max_tokens=self.settings.default_max_tokens,
            top_p=self.settings.default_top_p,
            frequency_penalty=self.settings.default_frequency_penalty,
            presence_penalty=self.settings.default_presence_penalty,
            streaming=self.settings.default_streaming
        )
    
    def determine_user_type(self, user_profile: UserProfile) -> str:
        personality = user_profile.personality.lower()
        
        # MBTI 으로 분류하는게 더 좋아보인다.
        # personality 를 mbti 로 바꿀까..
        if any(word in personality for word in []):
            return "creative"
        elif any(word in personality for word in []):
            return "analytical"
        else:
            return "practical"
    
    def adjust_config_for_user_type(self, config: AIModelConfig, user_type: str) -> AIModelConfig:
        if user_type == "creative":
            # 창의적인 사용자
            config.temperature = 0.9
            config.frequency_penalty = 0.5
            config.max_tokens = 2500
        elif user_type == "analytical":
            # 분석적인 사용자
            config.temperature = 0.3
            config.presence_penalty = 0.2
            config.max_tokens = 1500
        elif user_type == "practical":
            # 실용적인 사용자
            config.temperature = 0.5
            config.max_tokens = 1800
        
        return config
    
    def create_ai_config(self, user_profile: UserProfile, provider: str, model: str) -> AIModelConfig:
        # 기본 설정 생성
        base_config = self.create_base_config(provider, model)
        
        # 사용자 성향에 따른 설정 튜닝
        user_type = self.determine_user_type(user_profile)
        return self.adjust_config_for_user_type(base_config, user_type)
