from app.domain.entities.onboarding_profile import OnboardingProfile
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
    
    
    def adjust_config_for_user_type(self, config: AIModelConfig) -> AIModelConfig:
        # 고도화 필요 들어온 정보로 약간의 튜닝, 밖에서 콜백을 받아야할 듯

        # if user_type == "creative":
        #     config.temperature = 0.9
        #     config.frequency_penalty = 0.5
        #     config.max_tokens = 2500
        # elif user_type == "analytical":
        #     config.temperature = 0.3
        #     config.presence_penalty = 0.2
        #     config.max_tokens = 1500
        # elif user_type == "practical":
        #     config.temperature = 0.5
        #     config.max_tokens = 1800
        
        return config
    
    def create_ai_config(self, provider: str, model: str) -> AIModelConfig:
        # 기본 설정 생성
        base_config = self.create_base_config(provider, model)
        
        return self.adjust_config_for_user_type(base_config)
