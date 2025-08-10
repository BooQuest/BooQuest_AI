import threading
import time
import logging
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Clova X 설정
    clova_x_provider: str
    clova_x_model: str 
    clova_x_api_key: str
    clova_x_base_url: str
    
    # AI 모델 기본 설정값들 (어댑터에서 사용할 수 있도록)
    default_temperature: float
    default_max_tokens: int
    default_top_p: float
    default_frequency_penalty: float
    default_presence_penalty: float
    default_streaming: bool
    
    # 로깅 설정
    log_level: str
    
    # 서버 설정
    host: str
    port: int
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class HotReloadSettings:
    def __init__(self):
        self._settings: Optional[Settings] = None
        self._lock = threading.RLock()  # 재진입 가능한 락
        self._last_modified = 0
        self._env_file_path = Path(".env")
        self._logger = logging.getLogger("HotReloadSettings")
        self._watcher_thread = None
        self._stop_watcher = threading.Event()
        
        # 초기 설정 로드
        self._load_settings()
        
        # 파일 감시 시작
        self._start_file_watcher()
    
    def _load_settings(self) -> None:
        try:
            with self._lock:
                self._settings = Settings()
                self._last_modified = self._get_env_file_mtime()
        except Exception as e:
            self._logger.error(f"설정 로드 실패: {str(e)}")
            # 기본값으로 설정 생성
            self._settings = Settings()
    
    def _get_env_file_mtime(self) -> float:
        try:
            return self._env_file_path.stat().st_mtime if self._env_file_path.exists() else 0
        except Exception:
            return 0
    
    def _start_file_watcher(self) -> None:
        def watch_file():
            while not self._stop_watcher.is_set():
                try:
                    current_mtime = self._get_env_file_mtime()
                    if current_mtime > self._last_modified:
                        self._load_settings()
                        self._last_modified = current_mtime
                    
                    # 1초마다 체크
                    time.sleep(1)
                except Exception as e:
                    self._logger.error(f"파일 감시 중 오류: {str(e)}")
                    time.sleep(5)  # 오류 시 5초 대기
        
        self._watcher_thread = threading.Thread(target=watch_file, daemon=True)
        self._watcher_thread.start()
    
    def stop_watcher(self) -> None:
        self._stop_watcher.set()
        if self._watcher_thread:
            self._watcher_thread.join(timeout=5)
    
    def get_settings(self) -> Settings:
        with self._lock:
            return self._settings
    
    def reload_settings(self) -> Settings:
        self._load_settings()
        return self._settings

# 전역 설정 관리자 인스턴스
_settings_manager: Optional[HotReloadSettings] = None
_settings_manager_lock = threading.Lock()

def get_settings() -> Settings:
    global _settings_manager
    if _settings_manager is None:
        with _settings_manager_lock:
            if _settings_manager is None:
                _settings_manager = HotReloadSettings()
    return _settings_manager.get_settings()

def reload_settings() -> Settings:
    global _settings_manager
    if _settings_manager is None:
        with _settings_manager_lock:
            if _settings_manager is None:
                _settings_manager = HotReloadSettings()
    return _settings_manager.reload_settings()

def stop_settings_watcher() -> None:
    global _settings_manager
    if _settings_manager:
        _settings_manager.stop_watcher() 