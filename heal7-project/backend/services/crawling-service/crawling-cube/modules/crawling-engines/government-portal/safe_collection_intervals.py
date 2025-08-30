#!/usr/bin/env python3
"""
안전한 수집 간격 가이드라인 및 자동 조절 시스템
정부 포털별 최적 수집 패턴 관리

Author: Paperwork AI Team
Version: 1.0.0
Date: 2025-08-24
"""

import random
import logging
from datetime import datetime, timedelta, time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
import math

logger = logging.getLogger(__name__)

class TimeOfDay(Enum):
    """시간대 분류"""
    EARLY_MORNING = "early_morning"    # 03:00-07:00
    MORNING = "morning"                # 07:00-09:00
    BUSINESS_HOURS = "business_hours"  # 09:00-18:00
    EVENING = "evening"                # 18:00-22:00
    LATE_NIGHT = "late_night"         # 22:00-03:00

class RiskLevel(Enum):
    """위험도 레벨"""
    VERY_LOW = "very_low"     # 매우 낮음
    LOW = "low"               # 낮음
    MODERATE = "moderate"     # 보통
    HIGH = "high"             # 높음
    CRITICAL = "critical"     # 위험

@dataclass
class IntervalConfig:
    """간격 설정"""
    min_seconds: int          # 최소 간격 (초)
    max_seconds: int          # 최대 간격 (초)
    recommended_seconds: int  # 권장 간격 (초)
    randomization: float      # 랜덤화 정도 (0.0-1.0)
    burst_protection: bool    # 연속 요청 방지
    adaptive: bool            # 적응형 간격 조절

@dataclass  
class PortalProfile:
    """포털별 프로파일"""
    portal_id: str
    portal_name: str
    base_url: str
    default_interval: IntervalConfig
    time_based_intervals: Dict[TimeOfDay, IntervalConfig]
    risk_factors: Dict[str, float]
    notes: List[str]

class SafeCollectionIntervals:
    """안전한 수집 간격 관리"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or '/home/ubuntu/heal7-project/backend/services/government-portal-scraper/interval_config.json'
        self.portal_profiles = {}
        self.collection_history = {}  # 포털별 수집 이력
        
        # 기본 포털 프로파일 초기화
        self._initialize_portal_profiles()
        
        # 시간대별 위험도
        self.time_risk_factors = {
            TimeOfDay.EARLY_MORNING: 0.3,    # 새벽 - 매우 안전
            TimeOfDay.MORNING: 0.5,          # 아침 - 안전
            TimeOfDay.BUSINESS_HOURS: 1.0,   # 업무시간 - 위험
            TimeOfDay.EVENING: 0.7,          # 저녁 - 보통
            TimeOfDay.LATE_NIGHT: 0.4        # 심야 - 안전
        }

    def _initialize_portal_profiles(self):
        """포털별 기본 프로파일 설정"""
        
        # K-startup 프로파일
        kstartup_profile = PortalProfile(
            portal_id="kstartup",
            portal_name="창업진흥원 K-startup",
            base_url="https://www.k-startup.go.kr",
            default_interval=IntervalConfig(
                min_seconds=180,      # 3분
                max_seconds=600,      # 10분
                recommended_seconds=300,  # 5분
                randomization=0.4,
                burst_protection=True,
                adaptive=True
            ),
            time_based_intervals={
                TimeOfDay.EARLY_MORNING: IntervalConfig(120, 300, 180, 0.3, True, True),
                TimeOfDay.MORNING: IntervalConfig(150, 400, 240, 0.3, True, True),
                TimeOfDay.BUSINESS_HOURS: IntervalConfig(300, 900, 600, 0.5, True, True),
                TimeOfDay.EVENING: IntervalConfig(180, 500, 300, 0.4, True, True),
                TimeOfDay.LATE_NIGHT: IntervalConfig(120, 350, 200, 0.3, True, True)
            },
            risk_factors={
                'server_load': 0.7,      # 서버 부하 민감도
                'rate_limiting': 0.8,    # 레이트 리밋 엄격도  
                'bot_detection': 0.6,    # 봇 감지 수준
                'traffic_analysis': 0.5  # 트래픽 분석 정도
            },
            notes=[
                "창업진흥원 공식 포털",
                "업무시간 중 수집 주의",
                "일일 100-150개 공고 수집 권장",
                "연속 요청 시 429 에러 발생 가능"
            ]
        )
        
        # BIZINFO 프로파일
        bizinfo_profile = PortalProfile(
            portal_id="bizinfo",
            portal_name="중소기업 비즈니스정보",
            base_url="https://www.bizinfo.go.kr",
            default_interval=IntervalConfig(
                min_seconds=240,      # 4분
                max_seconds=800,      # 13분
                recommended_seconds=420,  # 7분
                randomization=0.5,
                burst_protection=True,
                adaptive=True
            ),
            time_based_intervals={
                TimeOfDay.EARLY_MORNING: IntervalConfig(180, 400, 240, 0.4, True, True),
                TimeOfDay.MORNING: IntervalConfig(200, 500, 300, 0.4, True, True), 
                TimeOfDay.BUSINESS_HOURS: IntervalConfig(400, 1200, 800, 0.6, True, True),
                TimeOfDay.EVENING: IntervalConfig(240, 600, 400, 0.5, True, True),
                TimeOfDay.LATE_NIGHT: IntervalConfig(180, 450, 280, 0.4, True, True)
            },
            risk_factors={
                'server_load': 0.9,      # 높은 서버 부하 민감도
                'rate_limiting': 0.9,    # 매우 엄격한 레이트 리밋
                'bot_detection': 0.8,    # 높은 봇 감지 수준
                'traffic_analysis': 0.7  # 높은 트래픽 분석
            },
            notes=[
                "중소벤처기업부 통합정보시스템",
                "가장 보수적인 접근 필요",
                "일일 80-120개 공고 수집 권장",  
                "IP 차단 위험성 높음",
                "데이터 무결성 오류 빈발"
            ]
        )
        
        self.portal_profiles[kstartup_profile.portal_id] = kstartup_profile
        self.portal_profiles[bizinfo_profile.portal_id] = bizinfo_profile

    def get_current_time_category(self) -> TimeOfDay:
        """현재 시간대 분류"""
        current_hour = datetime.now().hour
        
        if 3 <= current_hour < 7:
            return TimeOfDay.EARLY_MORNING
        elif 7 <= current_hour < 9:
            return TimeOfDay.MORNING
        elif 9 <= current_hour < 18:
            return TimeOfDay.BUSINESS_HOURS
        elif 18 <= current_hour < 22:
            return TimeOfDay.EVENING
        else:  # 22-03
            return TimeOfDay.LATE_NIGHT

    def calculate_safe_interval(self, portal_id: str, recent_failures: int = 0, 
                              last_request_time: Optional[datetime] = None) -> Tuple[int, str]:
        """안전한 수집 간격 계산"""
        
        if portal_id not in self.portal_profiles:
            logger.warning(f"알 수 없는 포털 ID: {portal_id}")
            return 300, "기본 간격 (5분)"
        
        profile = self.portal_profiles[portal_id]
        time_category = self.get_current_time_category()
        
        # 시간대별 간격 설정 가져오기
        if time_category in profile.time_based_intervals:
            interval_config = profile.time_based_intervals[time_category]
        else:
            interval_config = profile.default_interval
        
        # 기본 간격
        base_interval = interval_config.recommended_seconds
        
        # 실패 횟수에 따른 조정
        failure_multiplier = 1.0
        if recent_failures > 0:
            failure_multiplier = min(1.0 + (recent_failures * 0.5), 3.0)  # 최대 3배
        
        # 시간대 위험도 반영
        time_risk = self.time_risk_factors[time_category]
        time_multiplier = 1.0 if time_risk <= 0.5 else (1.0 + (time_risk - 0.5))
        
        # 포털별 위험 요소 반영  
        portal_risk = sum(profile.risk_factors.values()) / len(profile.risk_factors)
        portal_multiplier = 1.0 + (portal_risk - 0.5) * 0.5
        
        # 최종 간격 계산
        adjusted_interval = base_interval * failure_multiplier * time_multiplier * portal_multiplier
        
        # 최소/최대 간격 제한
        final_interval = max(
            interval_config.min_seconds,
            min(interval_config.max_seconds, int(adjusted_interval))
        )
        
        # 랜덤화 적용
        if interval_config.randomization > 0:
            random_factor = 1.0 + (random.uniform(-1, 1) * interval_config.randomization)
            final_interval = int(final_interval * random_factor)
            final_interval = max(interval_config.min_seconds, 
                               min(interval_config.max_seconds, final_interval))
        
        # 설명 생성
        factors = []
        if recent_failures > 0:
            factors.append(f"실패 조정({recent_failures}회)")
        factors.append(f"시간대({time_category.value})")
        factors.append(f"포털위험도({portal_risk:.1f})")
        if interval_config.randomization > 0:
            factors.append("랜덤화")
        
        explanation = f"{final_interval}초 - " + ", ".join(factors)
        
        return final_interval, explanation

    def get_optimal_collection_window(self, portal_id: str) -> Dict[str, any]:
        """최적 수집 시간대 추천"""
        
        if portal_id not in self.portal_profiles:
            return {'error': f'알 수 없는 포털: {portal_id}'}
        
        profile = self.portal_profiles[portal_id]
        
        # 시간대별 점수 계산 (낮을수록 좋음)
        time_scores = {}
        
        for time_category in TimeOfDay:
            # 기본 위험도
            base_risk = self.time_risk_factors[time_category]
            
            # 간격 설정에서 권장 간격 (짧을수록 더 안전함을 의미)
            if time_category in profile.time_based_intervals:
                interval_config = profile.time_based_intervals[time_category]
                interval_score = interval_config.recommended_seconds / 600  # 10분을 1.0으로 정규화
            else:
                interval_score = profile.default_interval.recommended_seconds / 600
            
            # 종합 점수 (낮을수록 안전)
            total_score = base_risk + interval_score * 0.5
            time_scores[time_category] = total_score
        
        # 점수순으로 정렬
        sorted_times = sorted(time_scores.items(), key=lambda x: x[1])
        
        # 시간대별 정보
        time_windows = []
        for time_category, score in sorted_times:
            if time_category == TimeOfDay.EARLY_MORNING:
                hours = "03:00-07:00"
            elif time_category == TimeOfDay.MORNING:
                hours = "07:00-09:00"
            elif time_category == TimeOfDay.BUSINESS_HOURS:
                hours = "09:00-18:00"
            elif time_category == TimeOfDay.EVENING:
                hours = "18:00-22:00"
            else:  # LATE_NIGHT
                hours = "22:00-03:00"
            
            # 간격 설정
            if time_category in profile.time_based_intervals:
                interval = profile.time_based_intervals[time_category].recommended_seconds
            else:
                interval = profile.default_interval.recommended_seconds
            
            # 안전도 등급
            if score < 0.4:
                safety = "매우 안전"
                color = "green"
            elif score < 0.6:
                safety = "안전"
                color = "lightgreen"
            elif score < 0.8:
                safety = "보통"
                color = "yellow"
            elif score < 1.0:
                safety = "위험"
                color = "orange"
            else:
                safety = "매우 위험"
                color = "red"
            
            time_windows.append({
                'time_category': time_category.value,
                'hours': hours,
                'safety_level': safety,
                'safety_color': color,
                'recommended_interval_seconds': interval,
                'recommended_interval_display': f"{interval//60}분 {interval%60}초",
                'score': round(score, 2)
            })
        
        return {
            'portal_id': portal_id,
            'portal_name': profile.portal_name,
            'best_time_window': time_windows[0],
            'worst_time_window': time_windows[-1],
            'all_time_windows': time_windows,
            'general_recommendations': [
                f"최적 수집 시간: {time_windows[0]['hours']} ({time_windows[0]['safety_level']})",
                f"피해야 할 시간: {time_windows[-1]['hours']} ({time_windows[-1]['safety_level']})",
                f"일일 권장 수집량: {self._get_daily_recommendation(portal_id)}개",
                f"기본 수집 간격: {profile.default_interval.recommended_seconds//60}분"
            ]
        }

    def _get_daily_recommendation(self, portal_id: str) -> str:
        """일일 수집 권장량"""
        daily_limits = {
            'kstartup': "100-150",
            'bizinfo': "80-120"
        }
        return daily_limits.get(portal_id, "50-100")

    def validate_interval_safety(self, portal_id: str, proposed_interval: int) -> Dict[str, any]:
        """간격 안전성 검증"""
        
        if portal_id not in self.portal_profiles:
            return {'valid': False, 'error': f'알 수 없는 포털: {portal_id}'}
        
        profile = self.portal_profiles[portal_id]
        time_category = self.get_current_time_category()
        
        # 현재 시간대 간격 설정
        if time_category in profile.time_based_intervals:
            interval_config = profile.time_based_intervals[time_category]
        else:
            interval_config = profile.default_interval
        
        # 안전성 검증
        warnings = []
        errors = []
        
        if proposed_interval < interval_config.min_seconds:
            errors.append(f"간격이 너무 짧습니다. 최소 {interval_config.min_seconds}초 필요")
        
        if proposed_interval > interval_config.max_seconds:
            warnings.append(f"간격이 너무 깁니다. 최대 {interval_config.max_seconds}초 권장")
        
        # 시간대별 권장사항
        if time_category == TimeOfDay.BUSINESS_HOURS:
            if proposed_interval < interval_config.recommended_seconds * 1.5:
                warnings.append("업무시간 중이므로 더 긴 간격을 권장합니다")
        
        # 포털별 특별 권장사항
        if portal_id == 'bizinfo' and proposed_interval < 240:
            warnings.append("BIZINFO는 IP 차단 위험이 높으므로 4분 이상 권장")
        
        # 안전도 점수 계산 (0-100)
        safety_score = 100
        if proposed_interval < interval_config.min_seconds:
            safety_score = 0
        else:
            # 권장 간격과의 비교
            ratio = proposed_interval / interval_config.recommended_seconds
            if ratio < 0.8:
                safety_score = max(30, int(ratio * 100 / 0.8))
            elif ratio > 2.0:
                safety_score = max(70, 100 - int((ratio - 2.0) * 10))
        
        # 시간대 보정
        time_risk = self.time_risk_factors[time_category]
        if time_risk > 0.7:  # 업무시간
            safety_score = max(0, safety_score - 20)
        
        return {
            'valid': len(errors) == 0,
            'safety_score': safety_score,
            'safety_level': self._get_safety_level(safety_score),
            'errors': errors,
            'warnings': warnings,
            'recommendations': [
                f"현재 시간대 권장 간격: {interval_config.recommended_seconds}초",
                f"안전 범위: {interval_config.min_seconds}-{interval_config.max_seconds}초"
            ]
        }

    def _get_safety_level(self, score: int) -> str:
        """안전도 점수를 레벨로 변환"""
        if score >= 80:
            return "매우 안전"
        elif score >= 60:
            return "안전"
        elif score >= 40:
            return "보통"
        elif score >= 20:
            return "위험"
        else:
            return "매우 위험"

    def generate_collection_schedule(self, portal_id: str, hours_ahead: int = 24) -> Dict[str, any]:
        """수집 스케줄 생성"""
        
        if portal_id not in self.portal_profiles:
            return {'error': f'알 수 없는 포털: {portal_id}'}
        
        schedule = []
        current_time = datetime.now()
        end_time = current_time + timedelta(hours=hours_ahead)
        
        next_collection = current_time
        collection_count = 0
        
        while next_collection < end_time:
            # 현재 시간의 간격 계산
            hour = next_collection.hour
            if 3 <= hour < 7:
                time_cat = TimeOfDay.EARLY_MORNING
            elif 7 <= hour < 9:
                time_cat = TimeOfDay.MORNING
            elif 9 <= hour < 18:
                time_cat = TimeOfDay.BUSINESS_HOURS
            elif 18 <= hour < 22:
                time_cat = TimeOfDay.EVENING
            else:
                time_cat = TimeOfDay.LATE_NIGHT
            
            # 간격 설정 가져오기
            profile = self.portal_profiles[portal_id]
            if time_cat in profile.time_based_intervals:
                interval_config = profile.time_based_intervals[time_cat]
            else:
                interval_config = profile.default_interval
            
            # 랜덤 간격 적용
            interval = interval_config.recommended_seconds
            if interval_config.randomization > 0:
                random_factor = 1.0 + (random.uniform(-1, 1) * interval_config.randomization)
                interval = int(interval * random_factor)
                interval = max(interval_config.min_seconds, 
                             min(interval_config.max_seconds, interval))
            
            # 안전도 계산
            time_risk = self.time_risk_factors[time_cat]
            if time_risk <= 0.4:
                safety = "높음"
            elif time_risk <= 0.6:
                safety = "보통"
            else:
                safety = "낮음"
            
            schedule.append({
                'collection_time': next_collection.strftime('%Y-%m-%d %H:%M:%S'),
                'time_category': time_cat.value,
                'interval_seconds': interval,
                'safety_level': safety,
                'collection_number': collection_count + 1
            })
            
            next_collection += timedelta(seconds=interval)
            collection_count += 1
            
            # 일일 한도 체크
            daily_limit = int(self._get_daily_recommendation(portal_id).split('-')[1])
            if collection_count >= daily_limit:
                break
        
        return {
            'portal_id': portal_id,
            'schedule_period': f"{current_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}",
            'total_collections': len(schedule),
            'estimated_completion': schedule[-1]['collection_time'] if schedule else None,
            'average_interval_minutes': sum(s['interval_seconds'] for s in schedule) / len(schedule) / 60 if schedule else 0,
            'schedule': schedule
        }

    def get_emergency_intervals(self, portal_id: str) -> Dict[str, int]:
        """비상 상황별 간격"""
        base_intervals = {
            'normal': 300,      # 5분 - 정상
            'warning': 600,     # 10분 - 경고
            'error': 1800,      # 30분 - 오류
            'blocked': 3600,    # 1시간 - 차단
            'emergency': 7200   # 2시간 - 비상상황
        }
        
        # 포털별 조정
        if portal_id == 'bizinfo':
            # BIZINFO는 모든 간격을 1.5배 늘림
            for situation in base_intervals:
                base_intervals[situation] = int(base_intervals[situation] * 1.5)
        
        return base_intervals

# 사용 예시
def main():
    """메인 실행 함수"""
    intervals = SafeCollectionIntervals()
    
    print("=" * 80)
    print("⏱️ 안전한 수집 간격 가이드라인 시스템")
    print("=" * 80)
    print()
    
    for portal_id in ['kstartup', 'bizinfo']:
        print(f"📊 {portal_id.upper()} 포털 분석")
        print("-" * 40)
        
        # 현재 권장 간격
        interval, explanation = intervals.calculate_safe_interval(portal_id)
        print(f"현재 권장 간격: {explanation}")
        
        # 최적 수집 시간대
        optimal = intervals.get_optimal_collection_window(portal_id)
        print(f"최적 수집 시간: {optimal['best_time_window']['hours']} ({optimal['best_time_window']['safety_level']})")
        print(f"위험 시간대: {optimal['worst_time_window']['hours']} ({optimal['worst_time_window']['safety_level']})")
        
        # 간격 안전성 테스트
        test_intervals = [120, 300, 600, 1200]  # 2분, 5분, 10분, 20분
        print("간격 안전성 테스트:")
        for test_interval in test_intervals:
            validation = intervals.validate_interval_safety(portal_id, test_interval)
            print(f"  {test_interval}초({test_interval//60}분): {validation['safety_level']} ({validation['safety_score']}점)")
        
        # 비상 간격
        emergency = intervals.get_emergency_intervals(portal_id)
        print(f"비상 간격: 차단 시 {emergency['blocked']//60}분, 비상 시 {emergency['emergency']//60}분")
        
        print()

if __name__ == "__main__":
    main()