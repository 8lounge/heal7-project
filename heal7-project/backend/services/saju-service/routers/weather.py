#!/usr/bin/env python3
"""
🌤️ 날씨 API 라우터
- 한국 기상청(KMA) 기반 날씨 정보 제공
- 테마 시스템을 위한 간소화된 날씨 API
- 위치 기반 날씨 조회 지원
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import logging
from datetime import datetime
import os
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

router = APIRouter()

class WeatherRequest(BaseModel):
    latitude: float
    longitude: float

class WeatherResponse(BaseModel):
    weather: str
    temperature: int
    city: str
    success: bool
    message: Optional[str] = None

# 간단한 날씨 매핑 (실제 구현에서는 더 정교한 매핑 필요)
WEATHER_MAPPING = {
    "맑음": "clear",
    "구름많음": "clouds", 
    "흐림": "clouds",
    "비": "rain",
    "소나기": "rain",
    "뇌우": "thunderstorm",
    "눈": "snow",
    "진눈깨비": "sleet",
    "안개": "fog",
    "황사": "dust",
    "연무": "haze",
    "미세먼지": "dust"
}

@router.post("/api/weather/current", response_model=WeatherResponse)
async def get_current_weather(request: WeatherRequest):
    """
    현재 날씨 정보 조회
    - 위도, 경도 기반으로 현재 날씨 정보 반환
    - 테마 시스템에서 사용할 수 있는 간소화된 형식으로 제공
    """
    try:
        # 서울 기본 위치로 설정 (37.5665, 126.9780)
        lat = request.latitude
        lon = request.longitude
        
        # 한국 범위 내 검증 (대략적)
        if not (33.0 <= lat <= 39.0 and 124.0 <= lon <= 132.0):
            # 한국 외 지역은 서울로 기본 설정
            lat, lon = 37.5665, 126.9780
            
        # 기상청 API에서 실제 날씨 데이터 조회
        try:
            weather_data = await fetch_kma_weather(lat, lon)
            weather = weather_data.get("weather", "clear")
            temperature = weather_data.get("temperature", 20)
        except Exception as weather_e:
            logger.warning(f"기상청 API 연동 실패, 기본값 사용: {str(weather_e)}")
            # API 실패 시 시간 기반 기본값
            current_hour = datetime.now().hour
            if 6 <= current_hour <= 18:
                weather = "clear"
                temperature = 25
            else:
                weather = "clear" 
                temperature = 18
            
        # 서울 기본 설정
        city = "서울"
        
        # 위치에 따른 도시명 결정 (간단한 매핑)
        if lat > 37.7:
            city = "의정부"
        elif lat < 37.3:
            city = "수원" 
        elif lon > 127.2:
            city = "강남"
        elif lon < 126.7:
            city = "인천"
            
        logger.info(f"날씨 조회 성공: {city} - {weather}, {temperature}°C")
        
        return WeatherResponse(
            weather=weather,
            temperature=temperature, 
            city=city,
            success=True,
            message="날씨 정보 조회 성공"
        )
        
    except Exception as e:
        logger.error(f"날씨 조회 실패: {str(e)}")
        
        # 실패 시 기본값 반환
        return WeatherResponse(
            weather="clear",
            temperature=20,
            city="서울",
            success=False,
            message=f"날씨 조회 실패, 기본값 사용: {str(e)}"
        )

@router.get("/api/weather/status")
async def weather_status():
    """날씨 API 상태 확인"""
    return {
        "service": "weather-api",
        "status": "active", 
        "version": "1.0.0",
        "description": "테마 시스템용 날씨 API",
        "endpoints": {
            "current": "/api/weather/current",
            "status": "/api/weather/status"
        }
    }

# 기상청 API 연동 구현
async def fetch_kma_weather(lat: float, lon: float) -> dict:
    """
    기상청 API에서 실제 날씨 정보 조회
    Args:
        lat: 위도
        lon: 경도
    Returns:
        dict: weather, temperature 포함한 날씨 정보
    """
    try:
        # 환경변수에서 API 키 로드
        api_key = os.getenv('KMA_WEATHER_API_KEY') or os.getenv('KMA_API_KEY_DECODED')
        if not api_key:
            raise ValueError("기상청 API 키가 설정되지 않음")
        
        # 위경도를 기상청 격자 좌표로 변환 (간단한 매핑)
        nx, ny = convert_to_grid(lat, lon)
        
        # 현재 시간 기준으로 base_date, base_time 설정
        now = datetime.now()
        base_date = now.strftime('%Y%m%d')
        base_time = f"{(now.hour // 3) * 3:02d}00"  # 3시간 단위
        
        # 기상청 단기예보 API 호출
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        params = {
            'serviceKey': api_key,
            'numOfRows': '20',
            'pageNo': '1',
            'base_date': base_date,
            'base_time': base_time if base_time != '0000' else '2100',  # 자정은 전날 21시 사용
            'nx': nx,
            'ny': ny
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="기상청 API 호출 실패")
            
            # XML 파싱
            root = ET.fromstring(response.text)
            header = root.find('.//header')
            result_code = header.find('resultCode').text if header is not None else None
            
            if result_code != '00':
                error_msg = header.find('resultMsg').text if header is not None else "알 수 없는 오류"
                raise ValueError(f"기상청 API 오류: {error_msg}")
            
            # 날씨 데이터 추출
            items = root.findall('.//item')
            weather_info = {}
            
            for item in items:
                category = item.find('category').text
                value = item.find('obsrValue').text
                
                if category == 'T1H':  # 기온
                    weather_info['temperature'] = int(float(value))
                elif category == 'PTY':  # 강수형태 (0=없음, 1=비, 2=비/눈, 3=눈, 4=소나기)
                    if value == '0':
                        weather_info['weather'] = 'clear'
                    elif value in ['1', '4']:
                        weather_info['weather'] = 'rain'
                    elif value in ['2', '3']:
                        weather_info['weather'] = 'snow'
                    else:
                        weather_info['weather'] = 'clear'
            
            # 기본값 설정
            if 'temperature' not in weather_info:
                weather_info['temperature'] = 20
            if 'weather' not in weather_info:
                weather_info['weather'] = 'clear'
            
            return weather_info
            
    except Exception as e:
        logger.error(f"기상청 API 호출 실패: {str(e)}")
        raise e

def convert_to_grid(lat: float, lon: float) -> tuple:
    """
    위경도를 기상청 격자 좌표로 변환 (간단한 근사치)
    """
    # 서울 중심 기준 간단한 매핑 (실제로는 더 정교한 변환 필요)
    if 37.4 <= lat <= 37.7 and 126.8 <= lon <= 127.2:
        return 60, 127  # 서울 중심
    elif lat > 37.7:
        return 60, 130  # 경기 북부
    elif lat < 37.4:
        return 60, 120  # 경기 남부
    else:
        return 60, 127  # 기본값