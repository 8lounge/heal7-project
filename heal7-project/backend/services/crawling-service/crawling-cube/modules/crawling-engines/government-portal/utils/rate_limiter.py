"""
Rate Limiter for Government Portal Scraping
정부 포털 스크래핑용 요청 속도 제한기

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """비동기 요청 속도 제한기"""
    
    def __init__(self, requests_per_minute: int = 30, burst_limit: int = None):
        """
        Args:
            requests_per_minute: 분당 최대 요청 수
            burst_limit: 순간 최대 요청 수 (None이면 requests_per_minute의 1/4)
        """
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit or max(1, requests_per_minute // 4)
        self.min_interval = 60.0 / requests_per_minute  # 요청간 최소 간격 (초)
        
        # 요청 이력 추적
        self.request_times = []
        self.last_request_time = 0
        
        # 동시성 제어
        self.semaphore = asyncio.Semaphore(self.burst_limit)
        self.lock = asyncio.Lock()
        
        # 통계
        self.stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'average_wait_time': 0,
            'start_time': datetime.now()
        }
        
        logger.info(f"🚦 Rate Limiter 초기화: {requests_per_minute}req/min, burst={self.burst_limit}")
    
    async def acquire(self, priority: str = 'normal') -> None:
        """요청 권한 획득 (필요시 대기)"""
        start_wait = time.time()
        
        async with self.semaphore:
            async with self.lock:
                await self._wait_if_needed()
                
                # 요청 기록
                current_time = time.time()
                self.request_times.append(current_time)
                self.last_request_time = current_time
                
                # 오래된 기록 정리 (1분 이상)
                cutoff_time = current_time - 60
                self.request_times = [t for t in self.request_times if t > cutoff_time]
                
                # 통계 업데이트
                wait_time = time.time() - start_wait
                self.stats['total_requests'] += 1
                if wait_time > 0.1:  # 0.1초 이상 대기시 블록으로 간주
                    self.stats['blocked_requests'] += 1
                
                # 평균 대기 시간 업데이트
                prev_avg = self.stats['average_wait_time']
                total_requests = self.stats['total_requests']
                self.stats['average_wait_time'] = ((prev_avg * (total_requests - 1)) + wait_time) / total_requests
    
    async def _wait_if_needed(self) -> None:
        """필요시 대기"""
        current_time = time.time()
        
        # 1. 최소 간격 체크
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            logger.debug(f"⏳ 최소 간격 대기: {wait_time:.2f}초")
            await asyncio.sleep(wait_time)
            current_time = time.time()
        
        # 2. 분당 요청수 체크
        recent_requests = len([t for t in self.request_times if t > current_time - 60])
        if recent_requests >= self.requests_per_minute:
            # 가장 오래된 요청이 1분이 경과할 때까지 대기
            oldest_request = min(self.request_times) if self.request_times else current_time
            wait_time = 60 - (current_time - oldest_request) + 0.1  # 약간의 버퍼
            if wait_time > 0:
                logger.debug(f"⏳ 분당 한도 대기: {wait_time:.2f}초")
                await asyncio.sleep(wait_time)
    
    def get_stats(self) -> Dict:
        """통계 정보 반환"""
        current_time = time.time()
        uptime = (datetime.now() - self.stats['start_time']).total_seconds()
        recent_requests = len([t for t in self.request_times if t > current_time - 60])
        
        return {
            'requests_per_minute_limit': self.requests_per_minute,
            'burst_limit': self.burst_limit,
            'current_requests_in_last_minute': recent_requests,
            'total_requests': self.stats['total_requests'],
            'blocked_requests': self.stats['blocked_requests'],
            'block_rate': (self.stats['blocked_requests'] / max(1, self.stats['total_requests'])) * 100,
            'average_wait_time': self.stats['average_wait_time'],
            'requests_per_second_actual': self.stats['total_requests'] / max(1, uptime),
            'uptime_seconds': uptime
        }
    
    def reset_stats(self) -> None:
        """통계 초기화"""
        self.stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'average_wait_time': 0,
            'start_time': datetime.now()
        }
        logger.info("📊 Rate Limiter 통계 초기화")

class AdaptiveRateLimiter(RateLimiter):
    """적응형 요청 속도 제한기 (서버 응답에 따라 자동 조정)"""
    
    def __init__(self, initial_requests_per_minute: int = 30, **kwargs):
        super().__init__(initial_requests_per_minute, **kwargs)
        
        self.initial_rpm = initial_requests_per_minute
        self.current_rpm = initial_requests_per_minute
        self.max_rpm = initial_requests_per_minute * 2  # 최대 2배까지
        self.min_rpm = max(5, initial_requests_per_minute // 4)  # 최소 1/4 또는 5
        
        # 적응형 조정 설정
        self.success_count = 0
        self.error_count = 0
        self.adjustment_threshold = 10  # 10회마다 조정
        self.last_adjustment = datetime.now()
        
        logger.info(f"🎯 적응형 Rate Limiter: {initial_requests_per_minute}rpm (범위: {self.min_rpm}-{self.max_rpm})")
    
    async def report_response(self, success: bool, response_time: float, status_code: Optional[int] = None):
        """응답 결과 보고 (속도 조정용)"""
        if success and status_code != 429:  # 429 = Too Many Requests
            self.success_count += 1
        else:
            self.error_count += 1
            if status_code == 429:
                # 즉시 속도 감소
                await self._decrease_rate("Too Many Requests")
        
        # 주기적 조정
        total_responses = self.success_count + self.error_count
        if total_responses >= self.adjustment_threshold:
            await self._adjust_rate()
            self._reset_counters()
    
    async def _adjust_rate(self):
        """응답 패턴에 따라 요청 속도 조정"""
        total_responses = self.success_count + self.error_count
        success_rate = self.success_count / total_responses
        
        if success_rate >= 0.95:  # 95% 이상 성공시 속도 증가
            await self._increase_rate("High success rate")
        elif success_rate <= 0.8:  # 80% 이하 성공시 속도 감소
            await self._decrease_rate("Low success rate")
        
        logger.info(f"📈 Rate 조정: {self.current_rpm}rpm (성공률: {success_rate:.1%})")
    
    async def _increase_rate(self, reason: str):
        """요청 속도 증가"""
        if self.current_rpm < self.max_rpm:
            old_rpm = self.current_rpm
            self.current_rpm = min(self.max_rpm, int(self.current_rpm * 1.2))
            self.requests_per_minute = self.current_rpm
            self.min_interval = 60.0 / self.current_rpm
            
            logger.info(f"⬆️ Rate 증가: {old_rpm} → {self.current_rpm}rpm ({reason})")
    
    async def _decrease_rate(self, reason: str):
        """요청 속도 감소"""
        if self.current_rpm > self.min_rpm:
            old_rpm = self.current_rpm
            self.current_rpm = max(self.min_rpm, int(self.current_rpm * 0.7))
            self.requests_per_minute = self.current_rpm
            self.min_interval = 60.0 / self.current_rpm
            
            logger.info(f"⬇️ Rate 감소: {old_rpm} → {self.current_rpm}rpm ({reason})")
    
    def _reset_counters(self):
        """카운터 초기화"""
        self.success_count = 0
        self.error_count = 0
        self.last_adjustment = datetime.now()

class MultiPortalRateLimiter:
    """다중 포털용 통합 속도 제한기"""
    
    def __init__(self, portal_configs: Dict[str, Dict]):
        """
        Args:
            portal_configs: {portal_id: {requests_per_minute: int, adaptive: bool}}
        """
        self.limiters = {}
        
        for portal_id, config in portal_configs.items():
            rpm = config.get('requests_per_minute', 30)
            if config.get('adaptive', False):
                limiter = AdaptiveRateLimiter(rpm)
            else:
                limiter = RateLimiter(rpm)
            
            self.limiters[portal_id] = limiter
            logger.info(f"🏢 {portal_id} Rate Limiter: {rpm}rpm")
    
    async def acquire(self, portal_id: str, priority: str = 'normal'):
        """특정 포털의 요청 권한 획득"""
        if portal_id not in self.limiters:
            raise ValueError(f"Unknown portal: {portal_id}")
        
        await self.limiters[portal_id].acquire(priority)
    
    async def report_response(self, portal_id: str, success: bool, response_time: float, status_code: Optional[int] = None):
        """응답 결과 보고 (적응형 리미터만)"""
        limiter = self.limiters.get(portal_id)
        if limiter and isinstance(limiter, AdaptiveRateLimiter):
            await limiter.report_response(success, response_time, status_code)
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """모든 포털의 통계 조회"""
        return {
            portal_id: limiter.get_stats() 
            for portal_id, limiter in self.limiters.items()
        }
    
    def get_portal_limiter(self, portal_id: str) -> Optional[RateLimiter]:
        """특정 포털의 리미터 반환"""
        return self.limiters.get(portal_id)