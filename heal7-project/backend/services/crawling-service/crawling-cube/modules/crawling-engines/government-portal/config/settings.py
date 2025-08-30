"""
Government Portal Intelligence System Configuration
정부 포털 지능화 시스템 설정

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import os
from typing import Dict, List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """시스템 설정"""
    
    # 기본 설정
    PROJECT_NAME: str = "Government Portal Intelligence System"
    VERSION: str = "2.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # 서버 설정
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8005, env="PORT")
    WORKERS: int = Field(default=1, env="WORKERS")
    
    # 데이터베이스
    DATABASE_URL: str = Field(
        default="postgresql://postgres:heal7postgres@localhost:5432/paperworkdb",
        env="DATABASE_URL"
    )
    
    # Redis (캐싱)
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Paperwork AI 연동
    PAPERWORK_API_URL: str = Field(
        default="https://paperwork.heal7.com",
        env="PAPERWORK_API_URL"
    )
    PAPERWORK_API_KEY: str = Field(default="", env="PAPERWORK_API_KEY")
    PAPERWORK_SECRET_KEY: str = Field(default="", env="PAPERWORK_SECRET_KEY")
    
    # AI 모델 설정
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    GOOGLE_AI_API_KEY: str = Field(default="", env="GOOGLE_AI_API_KEY")
    
    # 스크래핑 설정
    USER_AGENT: str = "PaperworkAI-GovernmentPortal/2.0 (+https://paperwork.heal7.com/bot)"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RATE_LIMIT_PER_MINUTE: int = 30
    
    # 포털별 설정
    PORTAL_CONFIGS: Dict = {
        "bizinfo": {
            "base_url": "https://www.bizinfo.go.kr",
            "rate_limit": 20,
            "timeout": 30,
            "enabled": True
        },
        "kstartup": {
            "base_url": "https://www.k-startup.go.kr", 
            "rate_limit": 15,
            "timeout": 45,
            "enabled": True,
            "use_browser": True
        },
        "government24": {
            "base_url": "https://www.gov.kr",
            "rate_limit": 25,
            "timeout": 30,
            "enabled": False  # 향후 구현
        }
    }
    
    # 스케줄링 설정
    ENABLE_SCHEDULER: bool = Field(default=True, env="ENABLE_SCHEDULER")
    SCHEDULE_TIMEZONE: str = "Asia/Seoul"
    
    # 기본 스케줄
    DEFAULT_SCHEDULES: Dict = {
        "bizinfo_daily": {
            "hour": 6,
            "minute": 0,
            "enabled": True
        },
        "kstartup_daily": {
            "hour": 7,
            "minute": 0,
            "enabled": True
        },
        "full_analysis": {
            "hour": 13,
            "minute": 0,
            "enabled": True
        }
    }
    
    # 로그 설정
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/government_portal.log", env="LOG_FILE")
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # 보안 설정
    SECRET_KEY: str = Field(default="your-secret-key-change-this", env="SECRET_KEY")
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1", "paperwork.heal7.com"],
        env="ALLOWED_HOSTS"
    )
    
    # 성능 설정
    MAX_CONCURRENT_SCRAPERS: int = 5
    MAX_QUEUE_SIZE: int = 1000
    BATCH_SIZE: int = 50
    
    # Playwright 설정 (K-Startup용)
    PLAYWRIGHT_HEADLESS: bool = Field(default=True, env="PLAYWRIGHT_HEADLESS")
    PLAYWRIGHT_TIMEOUT: int = 45000
    PLAYWRIGHT_VIEWPORT_WIDTH: int = 1920
    PLAYWRIGHT_VIEWPORT_HEIGHT: int = 1080
    
    # 품질 관리
    MIN_QUALITY_SCORE: float = 7.0
    AUTO_APPROVAL_SCORE: float = 8.5
    
    # 알림 설정
    ENABLE_NOTIFICATIONS: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")
    NOTIFICATION_WEBHOOK: Optional[str] = Field(default=None, env="NOTIFICATION_WEBHOOK")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

class DevelopmentSettings(Settings):
    """개발 환경 설정"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    PLAYWRIGHT_HEADLESS: bool = False  # 개발시 브라우저 보기
    ENABLE_SCHEDULER: bool = False  # 개발시 스케줄러 비활성화

class ProductionSettings(Settings):
    """프로덕션 환경 설정"""
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    PLAYWRIGHT_HEADLESS: bool = True
    WORKERS: int = 2
    MAX_CONCURRENT_SCRAPERS: int = 3  # 서버 리소스 고려

class TestSettings(Settings):
    """테스트 환경 설정"""
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres@localhost:5432/paperworkdb"
    ENABLE_SCHEDULER: bool = False
    RATE_LIMIT_PER_MINUTE: int = 100  # 테스트시 높은 제한

def get_settings() -> Settings:
    """환경에 따른 설정 반환"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()

# 전역 설정 인스턴스
settings = get_settings()

# 로깅 설정
import logging
import logging.handlers
import os

def setup_logging():
    """로깅 설정"""
    # 로그 디렉토리 생성
    log_dir = os.path.dirname(settings.LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)
    
    # 포매터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 파일 핸들러 (로테이션)
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 써드파티 로거 레벨 조정
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('playwright').setLevel(logging.WARNING)

# 자동 로깅 설정
setup_logging()