"""
HEAL7 사주명리학 시스템 - 설정 관리

환경변수와 설정을 중앙에서 관리하는 모듈입니다.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    """애플리케이션 설정"""
    
    # 기본 설정
    app_name: str = "HEAL7 사주명리학 시스템"
    debug: bool = False
    environment: str = "production"
    
    # KASI API 설정
    kasi_api_key: Optional[str] = None
    kasi_base_url: str = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService"
    request_timeout: float = 30.0
    max_retries: int = 3
    
    # 데이터베이스 설정
    database_url: Optional[str] = None
    sqlite_path: str = "database/saju.db"
    
    # Redis 설정 (향후 사용)
    redis_url: str = "redis://localhost:6379"
    
    # 로깅 설정
    log_level: str = "INFO"
    log_file: str = "logs/saju.log"
    
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    """설정 인스턴스 반환"""
    return Settings(
        # 환경변수에서 로드
        kasi_api_key=os.getenv("KASI_API_KEY"),
        database_url=os.getenv("DATABASE_URL"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        environment=os.getenv("ENVIRONMENT", "production")
    )