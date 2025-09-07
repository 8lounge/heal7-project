"""
Saju Service Pydantic Schemas
사주 서비스용 데이터 모델 정의
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SajuRequest(BaseModel):
    birth_year: int
    birth_month: int 
    birth_day: int
    birth_hour: int
    birth_minute: int = 0
    gender: str  # "male" or "female"
    name: Optional[str] = None
    is_lunar: bool = False

class SajuResult(BaseModel):
    name: Optional[str]
    birth_info: Dict[str, Any]
    four_pillars: Dict[str, str]
    day_master: str
    element_balance: Dict[str, int]
    sipsin_analysis: Dict[str, Any]
    sinsal: List[str]
    analysis: str
    personality: str  # 프론트엔드에서 기대하는 성격 특성 필드
    timestamp: datetime
    calculation_method: str

class FortuneResult(BaseModel):
    today: dict
    weekly: dict
    monthly: dict
    yearly: dict