"""
HEAL7 사주명리학 시스템 - 설정 관리

환경변수 기반 설정 관리와 Pydantic 모델을 사용한 타입 안전성 보장
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 애플리케이션 정보
    app_name: str = "HEAL7 사주명리학 시스템"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="디버그 모드")
    
    # 서버 설정
    host: str = Field(default="0.0.0.0", description="서버 호스트")
    port: int = Field(default=8002, description="서버 포트")
    workers: int = Field(default=1, description="워커 프로세스 수")
    
    # 데이터베이스 설정
    database_url: str = Field(
        default="sqlite:///./database/heal7_saju.db",
        description="데이터베이스 URL"
    )
    
    # Redis 설정 (캐싱 및 세션)
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis URL"
    )
    
    # KASI API 설정
    kasi_api_key: str = Field(
        default="AR2zMFQPIPBFak+MdXzznzVmtsICp7dwd3eo9XCUP62kXpr4GrX3eqi28erzZhXfIemuo6C5AK58eLMKBw8VGQ==",
        description="KASI API 키"
    )
    kasi_base_url: str = Field(
        default="http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService",
        description="KASI API 베이스 URL"
    )
    
    # AI 서비스 설정
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API 키")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API 키") 
    google_api_key: Optional[str] = Field(default=None, description="Google API 키")
    
    # 보안 설정
    secret_key: str = Field(
        default="heal7-saju-secret-key-change-in-production",
        description="JWT 서명용 비밀키"
    )
    algorithm: str = Field(default="HS256", description="JWT 알고리즘")
    access_token_expire_minutes: int = Field(default=30, description="액세스 토큰 만료 시간(분)")
    
    # CORS 설정
    allowed_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8080", 
            "https://saju.heal7.com",
            "https://test.heal7.com",
        ],
        description="CORS 허용 오리진"
    )
    
    allowed_hosts: List[str] = Field(
        default=["localhost", "127.0.0.1", "saju.heal7.com", "test.heal7.com"],
        description="허용된 호스트"
    )
    
    # 로깅 설정
    log_level: str = Field(default="INFO", description="로그 레벨")
    log_file: Optional[str] = Field(default=None, description="로그 파일 경로")
    
    # 모니터링 설정
    enable_metrics: bool = Field(default=True, description="Prometheus 메트릭 활성화")
    
    # 경로 설정
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path("./data"))
    logs_dir: Path = Field(default_factory=lambda: Path("./logs"))
    
    # 성능 설정
    max_workers: int = Field(default=4, description="최대 워커 스레드 수")
    request_timeout: int = Field(default=300, description="요청 타임아웃(초)")
    rate_limit_per_minute: int = Field(default=60, description="분당 요청 제한")
    
    # 캐시 설정
    cache_ttl: int = Field(default=3600, description="캐시 TTL(초)")
    cache_max_size: int = Field(default=1000, description="메모리 캐시 최대 크기")
    
    @validator("port")
    def validate_port(cls, v):
        if not (1 <= v <= 65535):
            raise ValueError("포트는 1-65535 사이여야 합니다")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"로그 레벨은 {valid_levels} 중 하나여야 합니다")
        return v.upper()
    
    @validator("data_dir", "logs_dir", pre=True)
    def create_directories(cls, v):
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def environment(self) -> str:
        """현재 환경 반환"""
        return "development" if self.debug else "production"
    
    @property
    def database_path(self) -> Path:
        """데이터베이스 파일 경로"""
        if self.database_url.startswith("sqlite"):
            return Path(self.database_url.replace("sqlite:///", ""))
        return None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# 싱글톤 인스턴스
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """설정 인스턴스 반환 (싱글톤)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def reload_settings() -> Settings:
    """설정 재로드"""
    global _settings
    _settings = Settings()
    return _settings