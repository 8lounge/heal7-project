"""
HEAL7 사주명리학 시스템 - KASI API 서비스

한국천문연구원(KASI) API와 통합하여 24절기 데이터를 관리하는 서비스입니다.
1900-2026년 24절기 완전 데이터베이스 구축을 목표로 합니다.

Features:
- KASI API 호출 및 데이터 수집
- 진태양시 보정 (한국 시간대 역사 고려)
- 24절기 데이터 캐싱 및 검증
- 비동기 처리 및 에러 핸들링
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

import httpx
# Redis는 임시 제외 - 향후 통합 예정
# import aioredis
from loguru import logger
from pydantic import BaseModel, Field, validator

try:
    from ..config.settings import get_settings
except ImportError:
    from config.settings import get_settings


class SolarTermType(str, Enum):
    """24절기 타입"""
    # 정기(正氣) - 입춘, 경칩, 청명, 입하, 망종, 소서, 입추, 백로, 한로, 입동, 대설, 소한
    MAJOR = "major"
    # 중기(中氣) - 우수, 춘분, 곡우, 소만, 하지, 대서, 처서, 추분, 상강, 소설, 동지, 대한  
    MINOR = "minor"


@dataclass
class KoreanTimezone:
    """한국 시간대 역사 정보"""
    start_date: datetime
    end_date: Optional[datetime]
    offset_minutes: int
    description: str
    
    def applies_to_date(self, date: datetime) -> bool:
        """특정 날짜에 이 시간대가 적용되는지 확인"""
        if date < self.start_date:
            return False
        if self.end_date and date > self.end_date:
            return False
        return True


class SolarTermData(BaseModel):
    """24절기 데이터 모델"""
    
    year: int = Field(..., ge=1900, le=2050, description="연도")
    month: int = Field(..., ge=1, le=12, description="월")
    day: int = Field(..., ge=1, le=31, description="일")
    solar_term_code: int = Field(..., description="절기 코드")
    solar_term_name: str = Field(..., description="절기명")
    solar_term_type: SolarTermType = Field(..., description="절기 타입")
    
    # 시간 정보
    kst_datetime: datetime = Field(..., description="한국표준시")
    solar_time_datetime: datetime = Field(..., description="진태양시")
    timezone_offset_minutes: int = Field(..., description="시간대 보정값(분)")
    
    # 메타데이터
    data_source: str = Field(default="KASI", description="데이터 출처")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = Field(default=False, description="검증 완료 여부")
    
    @validator('kst_datetime', 'solar_time_datetime')
    def validate_datetime_range(cls, v):
        """날짜/시간 유효성 검증"""
        if v.year < 1900 or v.year > 2050:
            raise ValueError("연도는 1900-2050 범위여야 합니다")
        return v

    @property
    def lunar_month_number(self) -> int:
        """절기에 해당하는 음력 월 번호"""
        # 24절기와 음력 월의 매핑
        return (self.solar_term_code - 1) // 2 + 1


class KASIAPIResponse(BaseModel):
    """KASI API 응답 모델"""
    
    response: Dict[str, Any] = Field(..., description="API 응답")
    
    @property
    def items(self) -> List[Dict[str, Any]]:
        """응답에서 아이템 목록 추출"""
        try:
            return self.get("body", {}).get("items", [])
        except (KeyError, AttributeError):
            return []
    
    @property
    def total_count(self) -> int:
        """총 아이템 수"""
        try:
            return self.get("body", {}).get("totalCount", 0)
        except (KeyError, AttributeError):
            return 0


class KASIService:
    """KASI API 서비스 클래스"""
    
    # 24절기 정보 (코드 : (이름, 타입))
    SOLAR_TERMS = {
        1: ("입춘", SolarTermType.MAJOR), 2: ("우수", SolarTermType.MINOR),
        3: ("경칩", SolarTermType.MAJOR), 4: ("춘분", SolarTermType.MINOR),
        5: ("청명", SolarTermType.MAJOR), 6: ("곡우", SolarTermType.MINOR),
        7: ("입하", SolarTermType.MAJOR), 8: ("소만", SolarTermType.MINOR),
        9: ("망종", SolarTermType.MAJOR), 10: ("하지", SolarTermType.MINOR),
        11: ("소서", SolarTermType.MAJOR), 12: ("대서", SolarTermType.MINOR),
        13: ("입추", SolarTermType.MAJOR), 14: ("처서", SolarTermType.MINOR),
        15: ("백로", SolarTermType.MAJOR), 16: ("추분", SolarTermType.MINOR),
        17: ("한로", SolarTermType.MAJOR), 18: ("상강", SolarTermType.MINOR),
        19: ("입동", SolarTermType.MAJOR), 20: ("소설", SolarTermType.MINOR),
        21: ("대설", SolarTermType.MAJOR), 22: ("동지", SolarTermType.MINOR),
        23: ("소한", SolarTermType.MAJOR), 24: ("대한", SolarTermType.MINOR),
    }
    
    # 한국 시간대 역사 (CLAUDE.md 기준)
    KOREAN_TIMEZONE_HISTORY = [
        KoreanTimezone(
            start_date=datetime(1961, 8, 10),
            end_date=None,
            offset_minutes=-32,
            description="현대 한국 (표준시 - 32분)"
        ),
        KoreanTimezone(
            start_date=datetime(1954, 3, 21),
            end_date=datetime(1961, 8, 9),
            offset_minutes=0,
            description="한국표준시 복구 (보정 없음)"
        ),
        KoreanTimezone(
            start_date=datetime(1912, 1, 1),
            end_date=datetime(1954, 3, 20),
            offset_minutes=-30,
            description="일제강점기 (표준시 - 30분)"
        ),
        KoreanTimezone(
            start_date=datetime(1908, 4, 1),
            end_date=datetime(1911, 12, 31),
            offset_minutes=0,
            description="대한제국 (보정 없음)"
        ),
    ]
    
    def __init__(self):
        """서비스 초기화"""
        self.settings = get_settings()
        self.http_client: Optional[httpx.AsyncClient] = None
        # Redis는 현재 비활성화 - 향후 통합 예정
        # self.redis_client: Optional[aioredis.Redis] = None
        self.redis_client = None
        self._cache_prefix = "kasi:solar_terms"
        self._is_initialized = False
        
        logger.info("KASI 서비스 초기화 시작")
    
    async def initialize(self) -> None:
        """서비스 초기화"""
        if self._is_initialized:
            return
            
        try:
            # HTTP 클라이언트 초기화
            timeout = httpx.Timeout(self.request_timeout)
            self.http_client = httpx.AsyncClient(
                timeout=timeout,
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=100)
            )
            
            # Redis 클라이언트는 현재 비활성화 - 향후 통합 예정
            # self.redis_client = await aioredis.from_url(
            #     self.redis_url,
            #     decode_responses=True,
            #     max_connections=10
            # )
            logger.info("Redis 캐시 현재 비활성화 상태")
            
            self._is_initialized = True
            logger.info("KASI 서비스 초기화 완료")
            
        except Exception as e:
            logger.error(f"KASI 서비스 초기화 실패: {e}")
            raise
    
    async def cleanup(self) -> None:
        """리소스 정리"""
        if self.http_client:
            await self.aclose()
            self.http_client = None
            
        if self.redis_client:
            await self.close()
            self.redis_client = None
            
        self._is_initialized = False
        logger.info("KASI 서비스 정리 완료")
    
    async def health_check(self) -> Dict[str, Any]:
        """헬스체크"""
        if not self._is_initialized:
            return {"status": "unhealthy", "reason": "not_initialized"}
        
        try:
            # KASI API 연결 테스트
            response = await self._call_kasi_api(2024, 1)  # 테스트 호출
            
            # Redis 연결 테스트
            await self.ping()
            
            return {
                "status": "healthy",
                "kasi_api": "connected",
                "redis": "connected",
                "solar_terms_available": len(self.SOLAR_TERMS)
            }
            
        except Exception as e:
            logger.error(f"KASI 서비스 헬스체크 실패: {e}")
            return {
                "status": "unhealthy", 
                "reason": str(e),
                "kasi_api": "disconnected",
                "redis": "disconnected"
            }
    
    def _get_timezone_offset(self, date: datetime) -> int:
        """특정 날짜의 진태양시 보정값을 반환 (분 단위)"""
        for tz in self.KOREAN_TIMEZONE_HISTORY:
            if tz.applies_to_date(date):
                return tz.offset_minutes
        
        # 기본값: 1900년 이전은 보정 없음
        return 0
    
    def _apply_solar_time_correction(self, kst_datetime: datetime) -> Tuple[datetime, int]:
        """진태양시 보정 적용"""
        offset_minutes = self._get_timezone_offset(kst_datetime)
        solar_time = kst_datetime + timedelta(minutes=offset_minutes)
        
        return solar_time, offset_minutes
    
    async def _call_kasi_api(
        self, 
        year: int, 
        month: int,
        num_rows: int = 100
    ) -> KASIAPIResponse:
        """KASI API 호출"""
        if not self.http_client:
            raise RuntimeError("HTTP 클라이언트가 초기화되지 않음")
        
        url = f"{self.kasi_base_url}/getRestDeInfo"
        params = {
            "serviceKey": self.kasi_api_key,
            "solYear": year,
            "solMonth": month,
            "numOfRows": num_rows,
            "_type": "json"
        }
        
        try:
            logger.debug(f"KASI API 호출: {year}년 {month}월")
            
            response = await self.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return KASIAPIResponse(response=data)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"KASI API HTTP 오류 ({e.status_code}): {e.text}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"KASI API JSON 파싱 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"KASI API 호출 오류: {e}")
            raise
    
    async def _get_cache_key(self, year: int, month: Optional[int] = None) -> str:
        """캐시 키 생성"""
        if month:
            return f"{self._cache_prefix}:{year}:{month:02d}"
        return f"{self._cache_prefix}:{year}"
    
    async def _cache_solar_terms(
        self, 
        year: int,
        month: int, 
        terms: List[SolarTermData],
        ttl: int = 3600
    ) -> None:
        """24절기 데이터 캐시"""
        if not self.redis_client:
            return
            
        cache_key = await self._get_cache_key(year, month)
        data = [term.dict() for term in terms]
        
        try:
            await self.setex(
                cache_key,
                ttl,
                json.dumps(data, default=str, ensure_ascii=False)
            )
            logger.debug(f"캐시 저장: {cache_key} ({len(terms)}개 절기)")
            
        except Exception as e:
            logger.warning(f"캐시 저장 실패 ({cache_key}): {e}")
    
    async def _get_cached_solar_terms(
        self, 
        year: int, 
        month: int
    ) -> Optional[List[SolarTermData]]:
        """캐시된 24절기 데이터 조회"""
        if not self.redis_client:
            return None
            
        cache_key = await self._get_cache_key(year, month)
        
        try:
            cached_data = await self.get(cache_key)
            if not cached_data:
                return None
                
            data = json.loads(cached_data)
            terms = []
            
            for item in data:
                # 날짜 문자열을 datetime 객체로 변환
                item['kst_datetime'] = datetime.fromisoformat(item['kst_datetime'])
                item['solar_time_datetime'] = datetime.fromisoformat(item['solar_time_datetime'])
                item['created_at'] = datetime.fromisoformat(item['created_at'])
                
                terms.append(SolarTermData(**item))
            
            logger.debug(f"캐시 조회 성공: {cache_key} ({len(terms)}개 절기)")
            return terms
            
        except Exception as e:
            logger.warning(f"캐시 조회 실패 ({cache_key}): {e}")
            return None
    
    async def get_solar_terms_by_month(
        self, 
        year: int, 
        month: int,
        use_cache: bool = True
    ) -> List[SolarTermData]:
        """월별 24절기 데이터 조회"""
        if not self._is_initialized:
            await self.initialize()
        
        # 캐시 확인
        if use_cache:
            cached_terms = await self._get_cached_solar_terms(year, month)
            if cached_terms:
                return cached_terms
        
        try:
            # KASI API 호출
            api_response = await self._call_kasi_api(year, month)
            terms = []
            
            for item in api_response.items:
                try:
                    # KASI API 응답 파싱
                    date_name = item.get("dateName", "")
                    locdate = str(item.get("locdate", ""))
                    
                    if not date_name or not locdate or len(locdate) != 8:
                        continue
                    
                    # 절기 코드 찾기
                    solar_term_code = None
                    solar_term_type = None
                    
                    for code, (name, term_type) in self.items():
                        if name in date_name:
                            solar_term_code = code
                            solar_term_type = term_type
                            break
                    
                    if not solar_term_code:
                        continue
                    
                    # 날짜 파싱
                    year_part = int(locdate[:4])
                    month_part = int(locdate[4:6])
                    day_part = int(locdate[6:8])
                    
                    # 기본 시간 설정 (정오)
                    kst_datetime = datetime(year_part, month_part, day_part, 12, 0, 0)
                    
                    # 진태양시 보정
                    solar_time, offset_minutes = self._apply_solar_time_correction(kst_datetime)
                    
                    # SolarTermData 객체 생성
                    solar_term = SolarTermData(
                        year=year_part,
                        month=month_part,
                        day=day_part,
                        solar_term_code=solar_term_code,
                        solar_term_name=date_name,
                        solar_term_type=solar_term_type,
                        kst_datetime=kst_datetime,
                        solar_time_datetime=solar_time,
                        timezone_offset_minutes=offset_minutes,
                        data_source="KASI",
                        is_verified=True
                    )
                    
                    terms.append(solar_term)
                    
                except (ValueError, KeyError, AttributeError) as e:
                    logger.warning(f"절기 데이터 파싱 실패: {item}, 오류: {e}")
                    continue
            
            # 절기 코드 순으로 정렬
            terms.sort(key=lambda x: x.solar_term_code)
            
            # 캐시 저장
            if terms and use_cache:
                await self._cache_solar_terms(year, month, terms, self.cache_ttl)
            
            logger.info(f"{year}년 {month}월 24절기 조회 완료: {len(terms)}개")
            return terms
            
        except Exception as e:
            logger.error(f"{year}년 {month}월 24절기 조회 실패: {e}")
            raise
    
    async def get_solar_terms_by_year(
        self, 
        year: int,
        use_cache: bool = True
    ) -> List[SolarTermData]:
        """연도별 24절기 데이터 조회"""
        if not (1900 <= year <= 2050):
            raise ValueError("연도는 1900-2050 범위여야 합니다")
        
        all_terms = []
        tasks = []
        
        # 각 월별로 병렬 처리
        for month in range(1, 13):
            task = self.get_solar_terms_by_month(year, month, use_cache)
            tasks.append(task)
        
        try:
            month_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for month, result in enumerate(month_results, 1):
                if isinstance(result, Exception):
                    logger.error(f"{year}년 {month}월 절기 조회 실패: {result}")
                    continue
                    
                all_terms.extend(result)
            
            # 절기 코드와 날짜순 정렬
            all_terms.sort(key=lambda x: (x.kst_datetime, x.solar_term_code))
            
            logger.info(f"{year}년 24절기 조회 완료: {len(all_terms)}개")
            return all_terms
            
        except Exception as e:
            logger.error(f"{year}년 24절기 조회 실패: {e}")
            raise
    
    async def get_solar_terms_range(
        self, 
        start_year: int, 
        end_year: int,
        use_cache: bool = True
    ) -> List[SolarTermData]:
        """연도 범위별 24절기 데이터 조회"""
        if not (1900 <= start_year <= end_year <= 2050):
            raise ValueError("연도 범위가 유효하지 않습니다 (1900-2050)")
        
        all_terms = []
        tasks = []
        
        # 각 연도별로 병렬 처리 (단, 너무 많은 동시 요청을 방지하기 위해 제한)
        semaphore = asyncio.Semaphore(5)  # 최대 5개 연도 동시 처리
        
        async def get_year_with_semaphore(year: int):
            async with semaphore:
                return await self.get_solar_terms_by_year(year, use_cache)
        
        for year in range(start_year, end_year + 1):
            task = get_year_with_semaphore(year)
            tasks.append(task)
        
        try:
            year_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for year_idx, result in enumerate(year_results):
                year = start_year + year_idx
                
                if isinstance(result, Exception):
                    logger.error(f"{year}년 절기 조회 실패: {result}")
                    continue
                    
                all_terms.extend(result)
            
            # 날짜순 정렬
            all_terms.sort(key=lambda x: x.kst_datetime)
            
            logger.info(f"{start_year}-{end_year}년 24절기 조회 완료: {len(all_terms)}개")
            return all_terms
            
        except Exception as e:
            logger.error(f"{start_year}-{end_year}년 24절기 조회 실패: {e}")
            raise
    
    async def find_solar_term_by_date(
        self, 
        date: datetime
    ) -> Optional[SolarTermData]:
        """특정 날짜의 24절기 조회"""
        try:
            # 해당 월의 절기들 조회
            terms = await self.get_solar_terms_by_month(date.year, date.month)
            
            # 정확한 날짜 매칭
            for term in terms:
                if (term.year == date.year and 
                    term.month == date.month and 
                    term.day == date.day):
                    return term
            
            return None
            
        except Exception as e:
            logger.error(f"날짜별 절기 조회 실패 ({date}): {e}")
            return None
    
    async def get_next_solar_term(
        self, 
        from_date: datetime
    ) -> Optional[SolarTermData]:
        """다음 24절기 조회"""
        try:
            # 현재 월부터 시작해서 다음 3개월까지 조회
            current_date = from_date
            
            for _ in range(4):  # 최대 4개월 조회
                terms = await self.get_solar_terms_by_month(current_date.year, current_date.month)
                
                for term in terms:
                    if term.kst_datetime > from_date:
                        return term
                
                # 다음 월로 이동
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
            
            return None
            
        except Exception as e:
            logger.error(f"다음 절기 조회 실패 ({from_date}): {e}")
            return None
    
    async def verify_data_integrity(
        self, 
        year: int
    ) -> Dict[str, Any]:
        """데이터 무결성 검증"""
        try:
            terms = await self.get_solar_terms_by_year(year)
            
            # 검증 결과
            result = {
                "year": year,
                "total_terms": len(terms),
                "expected_terms": 24,
                "is_complete": len(terms) == 24,
                "missing_terms": [],
                "duplicate_terms": [],
                "date_errors": [],
                "timezone_corrections": {}
            }
            
            # 24절기 완성도 체크
            found_codes = {term.solar_term_code for term in terms}
            expected_codes = set(range(1, 25))
            result["missing_terms"] = list(expected_codes - found_codes)
            
            # 중복 체크
            code_counts = {}
            for term in terms:
                code_counts[term.solar_term_code] = code_counts.get(term.solar_term_code, 0) + 1
            
            result["duplicate_terms"] = [
                code for code, count in code_counts.items() if count > 1
            ]
            
            # 날짜 순서 체크
            for i in range(1, len(terms)):
                if terms[i].kst_datetime <= terms[i-1].kst_datetime:
                    result["date_errors"].append({
                        "term": terms[i].solar_term_name,
                        "date": terms[i].kst_datetime,
                        "issue": "날짜 순서 오류"
                    })
            
            # 시간대 보정 통계
            for term in terms:
                offset = term.timezone_offset_minutes
                if offset not in result["timezone_corrections"]:
                    result["timezone_corrections"][offset] = 0
                result["timezone_corrections"][offset] += 1
            
            logger.info(f"{year}년 데이터 무결성 검증 완료: {result['total_terms']}/24")
            return result
            
        except Exception as e:
            logger.error(f"{year}년 데이터 무결성 검증 실패: {e}")
            return {
                "year": year,
                "error": str(e),
                "is_complete": False
            }
    
    def __repr__(self) -> str:
        status = "initialized" if self._is_initialized else "not_initialized"
        return f"KASIService(status={status}, terms={len(self.SOLAR_TERMS)})"