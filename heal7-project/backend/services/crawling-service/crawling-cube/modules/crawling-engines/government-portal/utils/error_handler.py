"""
스크래핑 오류 처리 및 복구 전략
정부 포털 변경 사항 대응을 위한 복구 시스템

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
from bs4 import BeautifulSoup
import backoff

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """오류 유형 분류"""
    NETWORK_ERROR = "network_error"          # 네트워크 연결 오류
    HTTP_ERROR = "http_error"                # HTTP 상태 코드 오류
    PARSING_ERROR = "parsing_error"          # HTML 파싱 오류
    STRUCTURE_CHANGED = "structure_changed"   # 사이트 구조 변경
    RATE_LIMITED = "rate_limited"            # 요청 제한
    TIMEOUT_ERROR = "timeout_error"          # 타임아웃 오류
    VALIDATION_ERROR = "validation_error"    # 데이터 검증 오류
    UNKNOWN_ERROR = "unknown_error"          # 기타 오류

@dataclass
class ErrorContext:
    """오류 컨텍스트 정보"""
    error_type: ErrorType
    url: str
    status_code: Optional[int] = None
    error_message: str = ""
    retry_count: int = 0
    timestamp: float = field(default_factory=time.time)
    additional_info: Dict = field(default_factory=dict)

class CircuitBreaker:
    """회로 차단기 패턴 구현"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 300, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        
    async def __call__(self, func: Callable, *args, **kwargs) -> Any:
        """함수 호출 시 회로 차단기 로직 적용"""
        
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time < self.recovery_timeout:
                raise CircuitBreakerOpenException(f"Circuit breaker is OPEN. Recovery in {self.recovery_timeout - (time.time() - self.last_failure_time):.1f}s")
            else:
                self.state = 'HALF_OPEN'
        
        try:
            result = await func(*args, **kwargs)
            
            # 성공 시 회로 리셋
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
                logger.info(f"🔄 Circuit breaker RESET for {func.__name__}")
            
            return result
            
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
                logger.error(f"⚡ Circuit breaker OPENED for {func.__name__} (failures: {self.failure_count})")
            
            raise

class CircuitBreakerOpenException(Exception):
    """회로 차단기가 열린 상태일 때 발생하는 예외"""
    pass

class AdaptiveRateLimit:
    """적응형 속도 제한"""
    
    def __init__(self, initial_delay: float = 1.0, min_delay: float = 0.5, max_delay: float = 60.0):
        self.current_delay = initial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.success_count = 0
        self.failure_count = 0
        
    async def wait(self):
        """현재 지연 시간만큼 대기"""
        await asyncio.sleep(self.current_delay)
        
    def on_success(self):
        """성공 시 지연 시간 조정"""
        self.success_count += 1
        self.failure_count = 0
        
        # 연속 성공 시 지연 시간 감소
        if self.success_count >= 5:
            self.current_delay = max(self.min_delay, self.current_delay * 0.9)
            self.success_count = 0
            
    def on_failure(self, status_code: Optional[int] = None):
        """실패 시 지연 시간 조정"""
        self.failure_count += 1
        self.success_count = 0
        
        # 429 (Too Many Requests) 또는 연속 실패 시 지연 시간 증가
        if status_code == 429 or self.failure_count >= 3:
            self.current_delay = min(self.max_delay, self.current_delay * 2)
            logger.warning(f"⏱️ Rate limit increased to {self.current_delay}s")

class StructureChangeDetector:
    """사이트 구조 변경 감지"""
    
    def __init__(self):
        self.expected_structures = {
            'bizinfo': {
                'table_selector': 'table',
                'row_selector': 'tbody tr',
                'min_columns': 6,
                'required_elements': ['td'],
                'fallback_selectors': ['tr', '.list-item', '.business-item']
            },
            'kstartup': {
                'list_selector': '.list-item, .announcement-item, ul li',
                'min_items': 5,
                'required_elements': ['a', 'span', 'div'],
                'fallback_selectors': ['.content li', '.main li', 'li']
            }
        }
    
    def detect_structure_change(self, site_type: str, soup: BeautifulSoup) -> bool:
        """구조 변경 감지"""
        if site_type not in self.expected_structures:
            return False
        
        expected = self.expected_structures[site_type]
        
        if site_type == 'bizinfo':
            return self._detect_bizinfo_change(soup, expected)
        elif site_type == 'kstartup':
            return self._detect_kstartup_change(soup, expected)
        
        return False
    
    def _detect_bizinfo_change(self, soup: BeautifulSoup, expected: Dict) -> bool:
        """기업마당 구조 변경 감지"""
        # 테이블 존재 확인
        table = soup.select_one(expected['table_selector'])
        if not table:
            logger.warning("⚠️ 기업마당 테이블 구조가 변경됨")
            return True
        
        # 행 개수 확인
        rows = table.select(expected['row_selector'])
        if len(rows) < 3:  # 최소한의 데이터가 있어야 함
            logger.warning(f"⚠️ 기업마당 테이블 행이 부족함: {len(rows)}개")
            return True
        
        # 컬럼 개수 확인
        first_row = rows[0]
        columns = first_row.select('td')
        if len(columns) < expected['min_columns']:
            logger.warning(f"⚠️ 기업마당 테이블 컬럼이 부족함: {len(columns)}개")
            return True
        
        return False
    
    def _detect_kstartup_change(self, soup: BeautifulSoup, expected: Dict) -> bool:
        """K-Startup 구조 변경 감지"""
        # 리스트 아이템 확인
        selectors = expected['list_selector'].split(', ')
        items = []
        
        for selector in selectors:
            items = soup.select(selector.strip())
            if len(items) >= expected['min_items']:
                break
        
        if len(items) < expected['min_items']:
            logger.warning(f"⚠️ K-Startup 리스트 아이템이 부족함: {len(items)}개")
            return True
        
        return False
    
    def get_fallback_selectors(self, site_type: str) -> List[str]:
        """대안 셀렉터 제공"""
        if site_type in self.expected_structures:
            return self.expected_structures[site_type].get('fallback_selectors', [])
        return []

class ErrorHandler:
    """통합 오류 처리기"""
    
    def __init__(self):
        self.circuit_breakers = {}
        self.rate_limiters = {}
        self.structure_detector = StructureChangeDetector()
        self.error_stats = {
            'total_errors': 0,
            'error_by_type': {},
            'recovery_attempts': 0,
            'successful_recoveries': 0
        }
        
    def get_circuit_breaker(self, site_type: str) -> CircuitBreaker:
        """사이트별 회로 차단기 반환"""
        if site_type not in self.circuit_breakers:
            self.circuit_breakers[site_type] = CircuitBreaker(
                failure_threshold=5,
                recovery_timeout=300,
                expected_exception=Exception
            )
        return self.circuit_breakers[site_type]
    
    def get_rate_limiter(self, site_type: str) -> AdaptiveRateLimit:
        """사이트별 속도 제한기 반환"""
        if site_type not in self.rate_limiters:
            initial_delays = {
                'bizinfo': 1.0,
                'kstartup': 2.0,
                'default': 1.5
            }
            
            self.rate_limiters[site_type] = AdaptiveRateLimit(
                initial_delay=initial_delays.get(site_type, initial_delays['default'])
            )
        return self.rate_limiters[site_type]
    
    async def handle_error(self, error_context: ErrorContext) -> Dict[str, Any]:
        """오류 처리 메인 로직"""
        self._update_error_stats(error_context)
        
        recovery_strategy = self._determine_recovery_strategy(error_context)
        
        logger.error(
            f"❌ 오류 발생: {error_context.error_type.value} | "
            f"URL: {error_context.url} | "
            f"메시지: {error_context.error_message}"
        )
        
        return await self._execute_recovery_strategy(recovery_strategy, error_context)
    
    def _update_error_stats(self, error_context: ErrorContext):
        """오류 통계 업데이트"""
        self.error_stats['total_errors'] += 1
        
        error_type = error_context.error_type.value
        if error_type not in self.error_stats['error_by_type']:
            self.error_stats['error_by_type'][error_type] = 0
        self.error_stats['error_by_type'][error_type] += 1
    
    def _determine_recovery_strategy(self, error_context: ErrorContext) -> str:
        """복구 전략 결정"""
        error_type = error_context.error_type
        
        strategy_map = {
            ErrorType.NETWORK_ERROR: 'retry_with_backoff',
            ErrorType.HTTP_ERROR: 'adaptive_retry',
            ErrorType.PARSING_ERROR: 'fallback_selectors',
            ErrorType.STRUCTURE_CHANGED: 'structure_recovery',
            ErrorType.RATE_LIMITED: 'rate_limit_backoff',
            ErrorType.TIMEOUT_ERROR: 'timeout_recovery',
            ErrorType.VALIDATION_ERROR: 'validation_recovery',
            ErrorType.UNKNOWN_ERROR: 'general_recovery'
        }
        
        return strategy_map.get(error_type, 'general_recovery')
    
    async def _execute_recovery_strategy(self, strategy: str, error_context: ErrorContext) -> Dict[str, Any]:
        """복구 전략 실행"""
        self.error_stats['recovery_attempts'] += 1
        
        try:
            if strategy == 'retry_with_backoff':
                return await self._retry_with_backoff(error_context)
            elif strategy == 'adaptive_retry':
                return await self._adaptive_retry(error_context)
            elif strategy == 'fallback_selectors':
                return await self._fallback_selectors(error_context)
            elif strategy == 'structure_recovery':
                return await self._structure_recovery(error_context)
            elif strategy == 'rate_limit_backoff':
                return await self._rate_limit_backoff(error_context)
            elif strategy == 'timeout_recovery':
                return await self._timeout_recovery(error_context)
            elif strategy == 'validation_recovery':
                return await self._validation_recovery(error_context)
            else:
                return await self._general_recovery(error_context)
                
        except Exception as e:
            logger.error(f"❌ 복구 전략 실행 실패: {strategy} | {str(e)}")
            return {'success': False, 'strategy': strategy, 'error': str(e)}
    
    async def _retry_with_backoff(self, error_context: ErrorContext) -> Dict[str, Any]:
        """지수적 백오프로 재시도"""
        if error_context.retry_count >= 3:
            return {'success': False, 'reason': 'max_retries_exceeded'}
        
        wait_time = 2 ** error_context.retry_count
        logger.info(f"🔄 {wait_time}초 후 재시도 ({error_context.retry_count + 1}/3)")
        
        await asyncio.sleep(wait_time)
        return {'success': True, 'action': 'retry', 'wait_time': wait_time}
    
    async def _adaptive_retry(self, error_context: ErrorContext) -> Dict[str, Any]:
        """적응형 재시도"""
        site_type = error_context.additional_info.get('site_type', 'default')
        rate_limiter = self.get_rate_limiter(site_type)
        
        rate_limiter.on_failure(error_context.status_code)
        await rate_limiter.wait()
        
        return {'success': True, 'action': 'adaptive_retry', 'delay': rate_limiter.current_delay}
    
    async def _fallback_selectors(self, error_context: ErrorContext) -> Dict[str, Any]:
        """대안 셀렉터 사용"""
        site_type = error_context.additional_info.get('site_type', 'default')
        fallback_selectors = self.structure_detector.get_fallback_selectors(site_type)
        
        logger.info(f"🔄 대안 셀렉터 사용: {fallback_selectors}")
        
        return {
            'success': True, 
            'action': 'fallback_selectors',
            'selectors': fallback_selectors
        }
    
    async def _structure_recovery(self, error_context: ErrorContext) -> Dict[str, Any]:
        """사이트 구조 변경 복구"""
        logger.warning("🔧 사이트 구조 변경 감지, 관리자에게 알림 필요")
        
        return {
            'success': True,
            'action': 'structure_recovery',
            'requires_manual_intervention': True
        }
    
    async def _rate_limit_backoff(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Rate Limit 백오프"""
        wait_time = 60  # 1분 대기
        logger.warning(f"⏱️ Rate limit 감지, {wait_time}초 대기")
        
        await asyncio.sleep(wait_time)
        return {'success': True, 'action': 'rate_limit_backoff', 'wait_time': wait_time}
    
    async def _timeout_recovery(self, error_context: ErrorContext) -> Dict[str, Any]:
        """타임아웃 복구"""
        if error_context.retry_count < 2:
            wait_time = 5
            await asyncio.sleep(wait_time)
            return {'success': True, 'action': 'timeout_retry', 'wait_time': wait_time}
        
        return {'success': False, 'reason': 'repeated_timeouts'}
    
    async def _validation_recovery(self, error_context: ErrorContext) -> Dict[str, Any]:
        """데이터 검증 오류 복구"""
        return {'success': True, 'action': 'skip_invalid_data'}
    
    async def _general_recovery(self, error_context: ErrorContext) -> Dict[str, Any]:
        """일반 복구 전략"""
        if error_context.retry_count < 1:
            await asyncio.sleep(3)
            return {'success': True, 'action': 'general_retry'}
        
        return {'success': False, 'reason': 'general_failure'}
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """오류 통계 반환"""
        return self.error_stats.copy()
    
    def reset_statistics(self):
        """통계 초기화"""
        self.error_stats = {
            'total_errors': 0,
            'error_by_type': {},
            'recovery_attempts': 0,
            'successful_recoveries': 0
        }

# 데코레이터 함수들
def with_error_handling(error_handler: ErrorHandler, site_type: str):
    """오류 처리 데코레이터"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            circuit_breaker = error_handler.get_circuit_breaker(site_type)
            rate_limiter = error_handler.get_rate_limiter(site_type)
            
            try:
                await rate_limiter.wait()
                result = await circuit_breaker(func, *args, **kwargs)
                rate_limiter.on_success()
                return result
                
            except Exception as e:
                error_context = ErrorContext(
                    error_type=classify_error(e),
                    url=kwargs.get('url', 'unknown'),
                    error_message=str(e),
                    additional_info={'site_type': site_type}
                )
                
                await error_handler.handle_error(error_context)
                raise
                
        return wrapper
    return decorator

def classify_error(exception: Exception) -> ErrorType:
    """예외를 오류 유형으로 분류"""
    if isinstance(exception, aiohttp.ClientError):
        return ErrorType.NETWORK_ERROR
    elif isinstance(exception, asyncio.TimeoutError):
        return ErrorType.TIMEOUT_ERROR
    elif isinstance(exception, aiohttp.ClientResponseError):
        if exception.status == 429:
            return ErrorType.RATE_LIMITED
        else:
            return ErrorType.HTTP_ERROR
    elif "parsing" in str(exception).lower():
        return ErrorType.PARSING_ERROR
    else:
        return ErrorType.UNKNOWN_ERROR