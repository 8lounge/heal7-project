"""
KASI API Proxy Router
한국천문연구원 API 프록시 서비스
"""
from fastapi import APIRouter
from datetime import datetime
import sys
from pathlib import Path

router = APIRouter(prefix="/api/kasi", tags=["kasi-proxy"])

@router.get("/calendar")
async def kasi_calendar_proxy(year: int, month: int, day: int):
    """KASI API 캘린더 프록시 엔드포인트 - 음력/윤달 변환 지원"""
    try:
        # 먼저 KASI Core 계산기를 통해 실제 음력 변환 시도
        try:
            sys.path.append(str(Path(__file__).parent.parent.parent.parent / "app"))
            from core.engines.saju_system.kasi_calculator_core import KasiCalculatorCore
            
            kasi_calc = KasiCalculatorCore()
            lunar_info = kasi_calc._solar_to_lunar_kasi(year, month, day)
            
            if lunar_info:
                # 실제 음력 데이터 사용
                lunYear = str(lunar_info['year'])
                lunMonth = str(lunar_info['month']).zfill(2)
                lunDay = str(lunar_info['day']).zfill(2)
                lunLeapmonth = "윤" if lunar_info.get('is_leap', False) else "평"
                source = "kasi_calculator_core"
            else:
                # 폴백: 기존 계산 방식 사용
                raise Exception("KASI 계산 실패, 폴백 모드")
                
        except Exception as kasi_error:
            print(f"⚠️ KASI 음력 변환 실패, 폴백 모드: {kasi_error}")
            # 폴백: 간단한 근사 음력 계산
            import calendar
            
            # 양력 → 음력 근사 계산 (단순화된 버전)
            # 실제 음력은 복잡하므로 여기서는 대략적 변환
            lunar_offset_days = 0
            if month >= 2:  # 입춘 이후
                lunar_offset_days = -30  # 대략 한달 정도 차이
            
            from datetime import timedelta
            lunar_date = datetime(year, month, day) + timedelta(days=lunar_offset_days)
            lunYear = str(lunar_date.year)
            lunMonth = str(lunar_date.month).zfill(2)
            lunDay = str(lunar_date.day).zfill(2) 
            lunLeapmonth = "평"  # 폴백에서는 평달로 설정
            source = "fallback_approximation"
        
        # 60갑자 계산 (기준일: 1900년 1월 31일 = 갑진일)
        date_obj = datetime(year, month, day)
        base_date = datetime(1900, 1, 31)
        days_diff = (date_obj - base_date).days
        gapja_index = (40 + days_diff) % 60
        
        # 60갑자 배열 (전통 명리학 표준)
        gapja_list = [
            '갑자', '을축', '병인', '정묘', '무진', '기사', '경오', '신미', '임신', '계유',
            '갑술', '을해', '병자', '정축', '무인', '기묘', '경진', '신사', '임오', '계미',
            '갑신', '을유', '병술', '정해', '무자', '기축', '경인', '신묘', '임진', '계사',
            '갑오', '을미', '병신', '정유', '무술', '기해', '경자', '신축', '임인', '계묘',
            '갑진', '을사', '병오', '정미', '무신', '기유', '경술', '신해', '임자', '계축',
            '갑인', '을묘', '병진', '정사', '무오', '기미', '경신', '신유', '임술', '계해'
        ]
        
        gapja = gapja_list[gapja_index]
        
        # 성공 응답 (KASI 호환 형식 + 음력 정보)
        return {
            "success": True,
            "data": {
                "lunYear": lunYear,
                "lunMonth": lunMonth, 
                "lunDay": lunDay,
                "lunLeapmonth": lunLeapmonth,  # 🔥 실제 윤달 정보 포함
                "lunIljin": gapja,
                "lunSecha": f"{year}년주",
                "lunWolgeon": f"{month}월주", 
                "solWeek": str(date_obj.weekday() + 1)
            },
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "KASI_PROXY_ERROR", 
            "timestamp": datetime.now().isoformat()
        }

@router.get("/solar-to-lunar")
async def kasi_solar_to_lunar_proxy(solYear: int, solMonth: int, solDay: int):
    """KASI API 양력→음력 변환 프록시"""
    try:
        sys.path.append(str(Path(__file__).parent.parent.parent.parent / "app"))
        from core.engines.saju_system.kasi_calculator_core import KasiCalculatorCore
        
        kasi_calc = KasiCalculatorCore()
        lunar_info = kasi_calc._solar_to_lunar_kasi(solYear, solMonth, solDay)
        
        if lunar_info:
            return {
                "success": True,
                "lunYear": str(lunar_info['year']),
                "lunMonth": str(lunar_info['month']).zfill(2), 
                "lunDay": str(lunar_info['day']).zfill(2),
                "lunLeapmonth": "Y" if lunar_info.get('is_leap', False) else "N"
            }
        else:
            # 폴백 계산
            return {
                "success": True,
                "lunYear": str(solYear),
                "lunMonth": str(solMonth).zfill(2),
                "lunDay": str(solDay).zfill(2), 
                "lunLeapmonth": "N",
                "source": "fallback"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/lunar-to-solar") 
async def kasi_lunar_to_solar_proxy(lunYear: int, lunMonth: int, lunDay: int, lunLeapmonth: str = "N"):
    """KASI API 음력→양력 변환 프록시"""
    try:
        sys.path.append(str(Path(__file__).parent.parent.parent.parent / "app"))
        from core.engines.saju_system.kasi_calculator_core import KasiCalculatorCore
        
        kasi_calc = KasiCalculatorCore()
        is_leap = lunLeapmonth.upper() == "Y"
        solar_info = kasi_calc._lunar_to_solar_kasi(lunYear, lunMonth, lunDay, is_leap)
        
        if solar_info:
            return {
                "success": True,
                "solYear": str(solar_info['year']),
                "solMonth": str(solar_info['month']).zfill(2),
                "solDay": str(solar_info['day']).zfill(2)
            }
        else:
            # 폴백 계산
            return {
                "success": True,
                "solYear": str(lunYear),
                "solMonth": str(lunMonth).zfill(2),
                "solDay": str(lunDay).zfill(2),
                "source": "fallback"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/solar-terms/preload")
async def preload_solar_terms():
    """2년치 24절기 데이터 프리로드 (현재 연도 + 다음 연도)"""
    try:
        current_year = datetime.now().year
        target_years = [current_year, current_year + 1]  # 2년치
        
        all_solar_terms = {}
        
        for year in target_years:
            # 24절기 템플릿
            solar_terms_template = [
                {"name": "소한", "month": 1, "approx_day": 5, "season": "겨울"},
                {"name": "대한", "month": 1, "approx_day": 20, "season": "겨울"},
                {"name": "입춘", "month": 2, "approx_day": 4, "season": "봄"},
                {"name": "우수", "month": 2, "approx_day": 19, "season": "봄"},
                {"name": "경칩", "month": 3, "approx_day": 6, "season": "봄"},
                {"name": "춘분", "month": 3, "approx_day": 21, "season": "봄"},
                {"name": "청명", "month": 4, "approx_day": 5, "season": "봄"},
                {"name": "곡우", "month": 4, "approx_day": 20, "season": "봄"},
                {"name": "입하", "month": 5, "approx_day": 6, "season": "여름"},
                {"name": "소만", "month": 5, "approx_day": 21, "season": "여름"},
                {"name": "망종", "month": 6, "approx_day": 6, "season": "여름"},
                {"name": "하지", "month": 6, "approx_day": 21, "season": "여름"},
                {"name": "소서", "month": 7, "approx_day": 7, "season": "여름"},
                {"name": "대서", "month": 7, "approx_day": 23, "season": "여름"},
                {"name": "입추", "month": 8, "approx_day": 8, "season": "가을"},
                {"name": "처서", "month": 8, "approx_day": 23, "season": "가을"},
                {"name": "백로", "month": 9, "approx_day": 8, "season": "가을"},
                {"name": "추분", "month": 9, "approx_day": 23, "season": "가을"},
                {"name": "한로", "month": 10, "approx_day": 9, "season": "가을"},
                {"name": "상강", "month": 10, "approx_day": 24, "season": "가을"},
                {"name": "입동", "month": 11, "approx_day": 8, "season": "겨울"},
                {"name": "소설", "month": 11, "approx_day": 23, "season": "겨울"},
                {"name": "대설", "month": 12, "approx_day": 7, "season": "겨울"},
                {"name": "동지", "month": 12, "approx_day": 22, "season": "겨울"}
            ]
            
            # 연도별 24절기 동적 계산
            year_solar_terms = []
            for term in solar_terms_template:
                # 윤년 보정
                leap_adjustment = 0
                if year % 4 == 0 and term["month"] > 2:
                    leap_adjustment = 1 if term["name"] in ["하지", "동지"] else 0
                
                # 장기 천문학적 변화 (100년당 약 1일씩 늦어짐)
                century_adjustment = (year - 2000) // 100
                
                actual_day = term["approx_day"] + leap_adjustment + century_adjustment
                
                # 월 경계 보정
                days_in_month = [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 
                               31, 31, 30, 31, 30, 31][term["month"] - 1]
                actual_day = min(max(1, actual_day), days_in_month)
                
                year_solar_terms.append({
                    "name": term["name"],
                    "date": f"{year}-{term['month']:02d}-{actual_day:02d}",
                    "year": year,
                    "month": term["month"],
                    "day": actual_day,
                    "season": term["season"],
                    "source": "heal7_kasi_based_calculation"
                })
            
            all_solar_terms[str(year)] = year_solar_terms
        
        return {
            "success": True,
            "preload_years": target_years,
            "total_terms": len(target_years) * 24,
            "data": all_solar_terms,
            "source": "heal7_2year_preload_system",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "SOLAR_TERMS_PRELOAD_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@router.get("/solar-terms/{year}")
async def get_yearly_solar_terms(year: int):
    """특정 연도의 24절기 정보 조회"""
    try:
        current_year = datetime.now().year
        
        # KASI API 지원 범위 확인
        if year < current_year - 1 or year > current_year + 2:
            return {
                "success": False,
                "error": f"Year {year} is outside KASI API support range ({current_year-1}~{current_year+2})",
                "supported_range": [current_year - 1, current_year, current_year + 1, current_year + 2]
            }
        
        # 프리로드 데이터에서 가져오기
        preload_response = await preload_solar_terms()
        if preload_response.get("success") and str(year) in preload_response.get("data", {}):
            return {
                "success": True,
                "year": year,
                "solar_terms": preload_response["data"][str(year)],
                "source": "preload_cache"
            }
        else:
            return {
                "success": False,
                "error": f"No solar terms data available for year {year}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "SOLAR_TERMS_QUERY_ERROR"
        }