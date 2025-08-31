#!/usr/bin/env python3
"""
🕷️ 크롤러 기본 구조
추상 베이스 클래스 및 데이터 구조 정의

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class CrawlerType(Enum):
    """크롤러 타입 정의"""
    HTTPX = "httpx"
    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"


class CrawlStatus(Enum):
    """크롤링 상태"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class CrawlResult:
    """크롤링 결과 데이터 구조"""
    success: bool
    status: CrawlStatus = CrawlStatus.FAILED
    
    # 크롤링 데이터
    html: Optional[str] = None
    status_code: Optional[int] = None
    screenshot: Optional[bytes] = None
    
    # 에러 정보
    error: Optional[str] = None
    error_type: Optional[str] = None
    
    # 메타데이터
    metadata: Dict[str, Any] = field(default_factory=dict)
    crawler_used: Optional[CrawlerType] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None
    
    # 성능 정보
    response_time: Optional[float] = None
    attempts: int = 1
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        
        if self.success:
            self.status = CrawlStatus.SUCCESS
        elif self.html and len(self.html) > 100:
            self.status = CrawlStatus.PARTIAL_SUCCESS
        else:
            self.status = CrawlStatus.FAILED


@dataclass 
class CrawlConfig:
    """크롤링 설정"""
    url: str
    timeout: int = 30
    retries: int = 2
    headers: Dict[str, str] = field(default_factory=dict)
    
    # 스크린샷 설정
    screenshot: bool = False
    screenshot_full_page: bool = True
    
    # JavaScript 설정
    wait_for_load: bool = True
    wait_for_selector: Optional[str] = None
    
    # Stealth 설정
    stealth_mode: bool = False
    user_agent: Optional[str] = None
    
    def __post_init__(self):
        if not self.headers:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }


class BaseCrawler(ABC):
    """크롤러 추상 베이스 클래스"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
        self.is_initialized = False
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0
        }
    
    @abstractmethod
    async def initialize(self):
        """크롤러 초기화"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """리소스 정리"""
        pass
    
    @abstractmethod
    async def crawl(self, config: CrawlConfig) -> CrawlResult:
        """메인 크롤링 함수"""
        pass
    
    @abstractmethod
    async def can_handle(self, url: str) -> bool:
        """해당 URL 처리 가능 여부"""
        pass
    
    async def health_check(self) -> bool:
        """크롤러 상태 확인"""
        try:
            # 간단한 테스트 요청으로 상태 확인
            test_config = CrawlConfig(
                url="https://httpbin.org/status/200",
                timeout=10
            )
            result = await self.crawl(test_config)
            return result.success
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def update_stats(self, result: CrawlResult):
        """통계 업데이트"""
        self.stats['total_requests'] += 1
        
        if result.success:
            self.stats['successful_requests'] += 1
        else:
            self.stats['failed_requests'] += 1
        
        if result.response_time:
            # 평균 응답 시간 계산 (이동 평균)
            current_avg = self.stats['average_response_time']
            total_requests = self.stats['total_requests']
            
            self.stats['average_response_time'] = (
                (current_avg * (total_requests - 1) + result.response_time) / total_requests
            )
    
    def get_success_rate(self) -> float:
        """성공률 반환"""
        if self.stats['total_requests'] == 0:
            return 0.0
        return self.stats['successful_requests'] / self.stats['total_requests']
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 정보 반환"""
        return {
            **self.stats,
            'success_rate': self.get_success_rate(),
            'crawler_type': self.name
        }


class CrawlerError(Exception):
    """크롤러 에러 베이스 클래스"""
    pass


class InitializationError(CrawlerError):
    """초기화 에러"""
    pass


class CrawlingError(CrawlerError):
    """크롤링 에러"""
    pass


class TimeoutError(CrawlerError):
    """타임아웃 에러"""
    pass


class AntiBotDetectionError(CrawlerError):
    """안티봇 감지 에러"""
    pass


# 유틸리티 함수들

def create_default_headers(user_agent: str = None) -> Dict[str, str]:
    """기본 HTTP 헤더 생성"""
    if user_agent is None:
        user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
    
    return {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def is_valid_url(url: str) -> bool:
    """URL 유효성 검사"""
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def estimate_content_type(url: str, html: str = None) -> str:
    """URL과 내용으로 콘텐츠 타입 추정"""
    url_lower = url.lower()
    
    # API 엔드포인트
    if any(keyword in url_lower for keyword in ['api', '.json', '/rest/', '/graphql']):
        return 'api'
    
    # 문서 파일
    if any(ext in url_lower for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
        return 'document'
    
    # 이미지
    if any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
        return 'image'
    
    # HTML 내용 분석
    if html:
        html_lower = html.lower()
        
        # JavaScript 렌더링 필요한 사이트
        if any(keyword in html_lower for keyword in ['<script', 'javascript:', 'ajax']):
            return 'dynamic'
        
        # 정적 HTML
        return 'static'
    
    return 'unknown'


def format_error_message(error: Exception, url: str, crawler_type: str) -> str:
    """에러 메시지 포맷팅"""
    return f"[{crawler_type.upper()}] {url} - {type(error).__name__}: {str(error)}"