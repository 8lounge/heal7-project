#!/usr/bin/env python3
"""
⚙️ 크롤링 시스템 환경 설정
하드코딩 제거 및 환경변수 기반 설정 관리

Author: HEAL7 Development Team  
Version: 1.0.0
Date: 2025-08-31
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class ServerConfig:
    """서버 설정"""
    host: str = "0.0.0.0"  # 수정: 0.0.0 → 0.0.0.0
    port: int = 8003
    reload: bool = False
    log_level: str = "info"
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("CRAWLING_HOST", "0.0.0.0"),
            port=int(os.getenv("CRAWLING_PORT", "8003")),
            reload=os.getenv("CRAWLING_RELOAD", "false").lower() == "true",
            log_level=os.getenv("CRAWLING_LOG_LEVEL", "info")
        )


@dataclass
class DatabaseConfig:
    """데이터베이스 설정"""
    host: str = "localhost"
    port: int = 5432
    database: str = "heal7"
    user: str = "crawling_user"
    password: Optional[str] = None
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "heal7"),
            user=os.getenv("DB_USER", "crawling_user"),
            password=os.getenv("DB_PASSWORD")
        )
    
    def get_url(self) -> str:
        """PostgreSQL 연결 URL 생성"""
        password_part = f":{self.password}" if self.password else ""
        return f"postgresql://{self.user}{password_part}@{self.host}:{self.port}/{self.database}"


@dataclass
class CORSConfig:
    """CORS 설정"""
    allowed_origins: list = None
    
    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = [
                "http://localhost:3000",
                "http://localhost:4173", 
                "https://crawling.heal7.com",
                "https://heal7.com"
            ]
    
    @classmethod
    def from_env(cls):
        origins_str = os.getenv("CORS_ORIGINS", "")
        if origins_str:
            origins = [origin.strip() for origin in origins_str.split(",")]
        else:
            origins = None
        return cls(allowed_origins=origins)


@dataclass
class AppConfig:
    """전체 애플리케이션 설정"""
    server: ServerConfig
    database: DatabaseConfig
    cors: CORSConfig
    environment: str = "production"
    
    @classmethod
    def from_env(cls):
        return cls(
            server=ServerConfig.from_env(),
            database=DatabaseConfig.from_env(), 
            cors=CORSConfig.from_env(),
            environment=os.getenv("ENVIRONMENT", "production")
        )


# 전역 설정 인스턴스
config = AppConfig.from_env()


def get_config() -> AppConfig:
    """설정 객체 반환"""
    return config


if __name__ == "__main__":
    # 설정 테스트
    cfg = get_config()
    print("🔧 크롤링 시스템 설정:")
    print(f"  서버: {cfg.server.host}:{cfg.server.port}")
    print(f"  데이터베이스: {cfg.database.get_url()}")
    print(f"  환경: {cfg.environment}")
    print(f"  CORS: {cfg.cors.allowed_origins}")