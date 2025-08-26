#!/usr/bin/env python3
"""
최적 수집 프로세스 가이드
정부 포털 스크래핑을 위한 종합적인 베스트 프랙티스 가이드

Author: Paperwork AI Team
Version: 1.0.0
Date: 2025-08-24
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import random

# 다른 모듈들 import
from safe_collection_guide import SafeScrapingManager, SafeCollectionConfig
from ip_blacklist_prevention import IPBlacklistPrevention, BlacklistStatus
from safe_collection_intervals import SafeCollectionIntervals, TimeOfDay
from bizinfo_integrity_fixer import BizinfoIntegrityFixer

logger = logging.getLogger(__name__)

class ProcessPhase(Enum):
    """프로세스 단계"""
    PREPARATION = "preparation"         # 준비 단계
    VALIDATION = "validation"           # 검증 단계  
    EXECUTION = "execution"             # 실행 단계
    MONITORING = "monitoring"           # 모니터링 단계
    OPTIMIZATION = "optimization"       # 최적화 단계
    RECOVERY = "recovery"               # 복구 단계

class CollectionStatus(Enum):
    """수집 상태"""
    IDLE = "idle"                       # 대기
    PREPARING = "preparing"             # 준비 중
    ACTIVE = "active"                   # 진행 중
    PAUSED = "paused"                   # 일시정지
    STOPPED = "stopped"                 # 정지
    ERROR = "error"                     # 오류
    COMPLETED = "completed"             # 완료

@dataclass
class OptimalProcessConfig:
    """최적 프로세스 설정"""
    portal_id: str
    target_daily_count: int             # 일일 목표 수집량
    max_daily_count: int               # 일일 최대 수집량
    preferred_time_windows: List[str]   # 선호 시간대
    avoid_time_windows: List[str]       # 회피 시간대
    quality_threshold: float            # 품질 임계치
    safety_threshold: float             # 안전도 임계치
    auto_recovery_enabled: bool         # 자동 복구 사용
    notification_enabled: bool          # 알림 사용

class OptimalCollectionProcess:
    """최적 수집 프로세스 관리자"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or '/home/ubuntu/heal7-project/backend/services/government-portal-scraper/optimal_process_config.json'
        
        # 서브시스템 초기화
        self.scraping_manager = SafeScrapingManager()
        self.ip_prevention = IPBlacklistPrevention()
        self.interval_manager = SafeCollectionIntervals()
        self.integrity_fixer = BizinfoIntegrityFixer()
        
        # 프로세스 상태
        self.current_phase = ProcessPhase.PREPARATION
        self.collection_status = CollectionStatus.IDLE
        self.process_history = []
        self.performance_metrics = {}
        
        # 포털별 최적 설정
        self.portal_configs = self._initialize_portal_configs()
        
        # 프로세스 가이드라인
        self.process_guidelines = self._initialize_guidelines()

    def _initialize_portal_configs(self) -> Dict[str, OptimalProcessConfig]:
        """포털별 최적 설정 초기화"""
        return {
            'kstartup': OptimalProcessConfig(
                portal_id='kstartup',
                target_daily_count=120,
                max_daily_count=150,
                preferred_time_windows=['22:00-03:00', '03:00-07:00'],
                avoid_time_windows=['09:00-18:00'],
                quality_threshold=75.0,
                safety_threshold=80.0,
                auto_recovery_enabled=True,
                notification_enabled=True
            ),
            'bizinfo': OptimalProcessConfig(
                portal_id='bizinfo',
                target_daily_count=80,
                max_daily_count=100,
                preferred_time_windows=['01:00-06:00', '22:00-24:00'],
                avoid_time_windows=['09:00-18:00', '12:00-14:00'],
                quality_threshold=70.0,
                safety_threshold=85.0,
                auto_recovery_enabled=True,
                notification_enabled=True
            )
        }

    def _initialize_guidelines(self) -> Dict[str, Dict]:
        """프로세스 가이드라인 초기화"""
        return {
            'preparation': {
                'title': '수집 준비 단계',
                'checklist': [
                    '시스템 상태 확인',
                    'IP 상태 점검',
                    '이전 수집 결과 분석',
                    '최적 시간대 확인',
                    '수집 목표량 설정',
                    '안전 임계치 설정'
                ],
                'critical_points': [
                    '업무시간 중 수집 금지',
                    'IP 블랙리스트 상태 확인 필수',
                    '연속 실패 이력이 있는 경우 대기'
                ]
            },
            'validation': {
                'title': '수집 전 검증 단계',
                'checklist': [
                    '안전도 점수 확인 (80점 이상)',
                    '현재 시간대 위험도 평가',
                    '포털별 수집 간격 계산',
                    '중복 데이터 필터 설정',
                    '데이터 품질 검증 규칙 적용'
                ],
                'critical_points': [
                    '안전도 80점 미만 시 수집 금지',
                    'IP 차단 상태 시 즉시 중단',
                    'BIZINFO는 특별히 주의'
                ]
            },
            'execution': {
                'title': '수집 실행 단계',
                'checklist': [
                    '실시간 모니터링 시작',
                    '적응형 간격 조절 활성화',
                    '데이터 품질 실시간 검증',
                    '실패 시 자동 복구 로직 적용',
                    '진행률 및 성과 추적'
                ],
                'critical_points': [
                    '연속 실패 5회 시 즉시 중단',
                    '응답 시간 10초 초과 시 간격 조정',
                    '성공률 70% 미만 시 패턴 변경'
                ]
            },
            'monitoring': {
                'title': '실시간 모니터링 단계',
                'checklist': [
                    '성공률 실시간 추적',
                    '응답 시간 모니터링',
                    'IP 상태 지속 확인',
                    '데이터 품질 점수 추적',
                    '위험 징후 조기 감지'
                ],
                'critical_points': [
                    '위험 징후 감지 시 즉시 알림',
                    '품질 점수 60점 미만 시 수집 중단',
                    '서킷브레이커 활성화 시 복구 대기'
                ]
            },
            'optimization': {
                'title': '성능 최적화 단계',
                'checklist': [
                    '수집 패턴 분석',
                    '최적 시간대 재조정',
                    '간격 설정 미세 조정',
                    '성과 지표 평가',
                    '다음 수집을 위한 개선점 도출'
                ],
                'critical_points': [
                    '성공적인 패턴 보존',
                    '실패 패턴 회피 규칙 강화',
                    '장기 트렌드 분석 반영'
                ]
            },
            'recovery': {
                'title': '오류 복구 단계',
                'checklist': [
                    '오류 원인 분석',
                    '복구 전략 선택',
                    '시스템 상태 복원',
                    '안전 모드 재시작',
                    '복구 결과 검증'
                ],
                'critical_points': [
                    'IP 차단 시 최소 1시간 대기',
                    '복구 실패 시 수동 개입 요청',
                    '안전 모드 확인 후 정상 모드 전환'
                ]
            }
        }

    def create_optimal_collection_plan(self, portal_id: str, hours_ahead: int = 24) -> Dict[str, any]:
        """최적 수집 계획 생성"""
        
        if portal_id not in self.portal_configs:
            return {'error': f'지원하지 않는 포털: {portal_id}'}
        
        config = self.portal_configs[portal_id]
        
        # 1단계: 현재 상황 분석
        current_analysis = self._analyze_current_situation(portal_id)
        
        # 2단계: 최적 시간대 선별
        optimal_windows = self._find_optimal_time_windows(portal_id, hours_ahead)
        
        # 3단계: 수집 일정 생성
        collection_schedule = self._generate_collection_schedule(portal_id, optimal_windows, config)
        
        # 4단계: 위험 완화 전략
        risk_mitigation = self._create_risk_mitigation_strategy(portal_id, current_analysis)
        
        # 5단계: 품질 보장 계획
        quality_assurance = self._create_quality_assurance_plan(portal_id)
        
        return {
            'portal_id': portal_id,
            'plan_created_at': datetime.now().isoformat(),
            'plan_period': f"{datetime.now().strftime('%Y-%m-%d %H:%M')} ~ {(datetime.now() + timedelta(hours=hours_ahead)).strftime('%Y-%m-%d %H:%M')}",
            'current_analysis': current_analysis,
            'optimal_time_windows': optimal_windows,
            'collection_schedule': collection_schedule,
            'risk_mitigation': risk_mitigation,
            'quality_assurance': quality_assurance,
            'expected_results': {
                'total_collections': len(collection_schedule['schedule']),
                'estimated_success_rate': collection_schedule['estimated_success_rate'],
                'estimated_quality_score': quality_assurance['expected_quality_score'],
                'risk_level': current_analysis['overall_risk_level']
            }
        }

    def _analyze_current_situation(self, portal_id: str) -> Dict[str, any]:
        """현재 상황 분석"""
        
        # IP 상태 분석
        ip_status = self.ip_prevention.get_system_status()
        
        # 시간대 분석
        current_time = datetime.now()
        time_category = self.interval_manager.get_current_time_category()
        
        # 최근 성과 분석 (시뮬레이션)
        recent_performance = {
            'success_rate': 85.0 + random.uniform(-10, 10),
            'average_response_time': 2.5 + random.uniform(-1, 2),
            'quality_score': 78.0 + random.uniform(-8, 12),
            'last_failure_time': None
        }
        
        # 위험도 계산
        risk_factors = []
        risk_score = 100
        
        if ip_status['status_distribution']['blocked'] > 0:
            risk_factors.append('IP 차단 상태')
            risk_score -= 40
        
        if time_category == TimeOfDay.BUSINESS_HOURS:
            risk_factors.append('업무시간대')
            risk_score -= 20
        
        if recent_performance['success_rate'] < 70:
            risk_factors.append('낮은 성공률')
            risk_score -= 15
        
        if portal_id == 'bizinfo' and recent_performance['quality_score'] < 70:
            risk_factors.append('BIZINFO 품질 문제')
            risk_score -= 10
        
        overall_risk_level = 'safe' if risk_score >= 80 else 'warning' if risk_score >= 60 else 'danger'
        
        return {
            'timestamp': current_time.isoformat(),
            'current_time_category': time_category.value,
            'ip_status': ip_status,
            'recent_performance': recent_performance,
            'risk_factors': risk_factors,
            'risk_score': max(0, risk_score),
            'overall_risk_level': overall_risk_level,
            'recommendations': self._get_current_recommendations(risk_factors, risk_score)
        }

    def _get_current_recommendations(self, risk_factors: List[str], risk_score: int) -> List[str]:
        """현재 상황별 권장사항"""
        recommendations = []
        
        if 'IP 차단 상태' in risk_factors:
            recommendations.append('즉시 수집 중단 및 IP 복구 대기')
        
        if '업무시간대' in risk_factors:
            recommendations.append('업무시간 종료까지 수집 지연')
        
        if '낮은 성공률' in risk_factors:
            recommendations.append('수집 간격 2배 증가 및 패턴 변경')
        
        if 'BIZINFO 품질 문제' in risk_factors:
            recommendations.append('BIZINFO 데이터 무결성 검증 강화')
        
        if risk_score >= 80:
            recommendations.append('현재 수집하기 좋은 상태입니다')
        elif risk_score >= 60:
            recommendations.append('주의하며 수집 진행 가능')
        else:
            recommendations.append('수집을 중단하고 문제 해결 후 재시도')
        
        return recommendations

    def _find_optimal_time_windows(self, portal_id: str, hours_ahead: int) -> List[Dict]:
        """최적 시간대 찾기"""
        config = self.portal_configs[portal_id]
        optimal_windows = self.interval_manager.get_optimal_collection_window(portal_id)
        
        # 다음 24시간 중 최적 시간대 찾기
        current_time = datetime.now()
        windows = []
        
        for i in range(hours_ahead):
            check_time = current_time + timedelta(hours=i)
            hour = check_time.hour
            
            # 시간대별 분류
            if 3 <= hour < 7:
                time_cat = 'early_morning'
                safety_level = 'very_safe'
                recommended_interval = 180
            elif 7 <= hour < 9:
                time_cat = 'morning'
                safety_level = 'safe'
                recommended_interval = 240
            elif 9 <= hour < 18:
                time_cat = 'business_hours'
                safety_level = 'risky'
                recommended_interval = 600
            elif 18 <= hour < 22:
                time_cat = 'evening'
                safety_level = 'moderate'
                recommended_interval = 300
            else:
                time_cat = 'late_night'
                safety_level = 'safe'
                recommended_interval = 200
            
            # 포털별 조정
            if portal_id == 'bizinfo':
                recommended_interval = int(recommended_interval * 1.4)
            
            windows.append({
                'start_time': check_time.strftime('%Y-%m-%d %H:00:00'),
                'end_time': (check_time + timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00'),
                'time_category': time_cat,
                'safety_level': safety_level,
                'recommended_interval_seconds': recommended_interval,
                'estimated_collections': 3600 // recommended_interval,
                'priority': self._calculate_window_priority(time_cat, safety_level, portal_id)
            })
        
        # 우선순위별 정렬
        windows.sort(key=lambda x: x['priority'], reverse=True)
        
        return windows

    def _calculate_window_priority(self, time_cat: str, safety_level: str, portal_id: str) -> int:
        """시간대 우선순위 계산"""
        base_priority = {
            'very_safe': 100,
            'safe': 80,
            'moderate': 60,
            'risky': 20
        }.get(safety_level, 0)
        
        # 시간대별 보정
        time_bonus = {
            'early_morning': 20,
            'late_night': 15,
            'morning': 10,
            'evening': 5,
            'business_hours': -30
        }.get(time_cat, 0)
        
        # 포털별 보정
        if portal_id == 'bizinfo':
            if safety_level in ['very_safe', 'safe']:
                base_priority += 10
            else:
                base_priority -= 20
        
        return base_priority + time_bonus

    def _generate_collection_schedule(self, portal_id: str, optimal_windows: List[Dict], 
                                    config: OptimalProcessConfig) -> Dict[str, any]:
        """수집 일정 생성"""
        
        schedule = []
        total_target = config.target_daily_count
        collections_planned = 0
        
        # 상위 우선순위 시간대부터 일정 배정
        for window in optimal_windows:
            if collections_planned >= total_target:
                break
            
            if window['safety_level'] in ['risky']:
                continue  # 위험한 시간대는 건너뛰기
            
            window_capacity = window['estimated_collections']
            remaining_target = total_target - collections_planned
            
            # 이 시간대에 할당할 수집 수
            assigned_collections = min(window_capacity, remaining_target)
            
            if assigned_collections > 0:
                schedule.append({
                    'time_window': f"{window['start_time']} ~ {window['end_time']}",
                    'safety_level': window['safety_level'],
                    'planned_collections': assigned_collections,
                    'interval_seconds': window['recommended_interval_seconds'],
                    'estimated_duration_minutes': (assigned_collections * window['recommended_interval_seconds']) // 60,
                    'notes': self._get_schedule_notes(window, portal_id)
                })
                
                collections_planned += assigned_collections
        
        # 성공률 예측
        estimated_success_rate = self._estimate_success_rate(schedule, portal_id)
        
        return {
            'total_planned_collections': collections_planned,
            'target_achievement_rate': (collections_planned / total_target * 100) if total_target > 0 else 0,
            'estimated_success_rate': estimated_success_rate,
            'estimated_actual_collections': int(collections_planned * estimated_success_rate / 100),
            'total_estimated_duration_hours': sum(item['estimated_duration_minutes'] for item in schedule) / 60,
            'schedule': schedule
        }

    def _get_schedule_notes(self, window: Dict, portal_id: str) -> List[str]:
        """일정별 주의사항"""
        notes = []
        
        if window['time_category'] == 'business_hours':
            notes.append('업무시간 중이므로 특별히 주의')
        
        if window['safety_level'] == 'moderate':
            notes.append('보통 위험도 - 실시간 모니터링 필요')
        
        if portal_id == 'bizinfo':
            notes.append('BIZINFO는 데이터 품질 검증 필수')
            notes.append('IP 차단 위험 높음 - 보수적 접근')
        
        if window['recommended_interval_seconds'] > 300:
            notes.append('긴 간격 설정으로 안전성 우선')
        
        return notes

    def _estimate_success_rate(self, schedule: List[Dict], portal_id: str) -> float:
        """성공률 예측"""
        if not schedule:
            return 0.0
        
        base_success_rates = {
            'very_safe': 95.0,
            'safe': 88.0,
            'moderate': 75.0,
            'risky': 55.0
        }
        
        total_collections = sum(item['planned_collections'] for item in schedule)
        weighted_success_rate = 0.0
        
        for item in schedule:
            base_rate = base_success_rates.get(item['safety_level'], 70.0)
            
            # 포털별 조정
            if portal_id == 'bizinfo':
                base_rate *= 0.85  # BIZINFO는 15% 낮춤
            
            weight = item['planned_collections'] / total_collections
            weighted_success_rate += base_rate * weight
        
        return round(weighted_success_rate, 1)

    def _create_risk_mitigation_strategy(self, portal_id: str, analysis: Dict) -> Dict[str, any]:
        """위험 완화 전략"""
        
        strategies = []
        
        # IP 관리 전략
        if analysis['ip_status']['status_distribution']['blocked'] > 0:
            strategies.append({
                'category': 'IP 관리',
                'action': 'IP 복구 대기',
                'description': '차단된 IP 복구까지 최소 1시간 대기',
                'priority': 'critical'
            })
        
        # 시간대 관리 전략
        if analysis['current_time_category'] == 'business_hours':
            strategies.append({
                'category': '시간 관리',
                'action': '업무시간 회피',
                'description': '18시 이후 수집 재시작',
                'priority': 'high'
            })
        
        # 품질 관리 전략
        if portal_id == 'bizinfo':
            strategies.append({
                'category': '품질 관리',
                'action': 'BIZINFO 무결성 검증',
                'description': '수집된 데이터의 실시간 무결성 검증',
                'priority': 'medium'
            })
        
        # 성능 관리 전략
        strategies.append({
            'category': '성능 관리',
            'action': '적응형 간격 조절',
            'description': '실시간 성능에 따른 수집 간격 자동 조절',
            'priority': 'medium'
        })
        
        # 모니터링 전략
        strategies.append({
            'category': '모니터링',
            'action': '실시간 위험 감지',
            'description': '블랙리스트 징후 실시간 모니터링',
            'priority': 'high'
        })
        
        return {
            'total_strategies': len(strategies),
            'critical_strategies': len([s for s in strategies if s['priority'] == 'critical']),
            'strategies': strategies,
            'emergency_procedures': [
                '연속 실패 5회 시 즉시 중단',
                'IP 차단 감지 시 즉시 중단',
                '응답 시간 10초 초과 시 간격 조정',
                '성공률 50% 미만 시 수집 중단'
            ]
        }

    def _create_quality_assurance_plan(self, portal_id: str) -> Dict[str, any]:
        """품질 보장 계획"""
        
        config = self.portal_configs[portal_id]
        
        quality_checks = [
            {
                'check_type': '필수 필드 검증',
                'description': '제목, 기관, 지원형태 등 필수 필드 존재 확인',
                'threshold': '100% 통과',
                'action': '실패 시 재수집'
            },
            {
                'check_type': '데이터 길이 검증',
                'description': '제목 최소 10자, 내용 최소 100자',
                'threshold': '90% 이상 통과',
                'action': '기준 미달 데이터 플래그'
            },
            {
                'check_type': '중복 데이터 검사',
                'description': 'URL 및 제목 기반 중복 검사',
                'threshold': '중복률 5% 미만',
                'action': '중복 데이터 자동 제거'
            },
            {
                'check_type': '날짜 형식 검증',
                'description': '신청기간, 마감일 등 날짜 형식 검증',
                'threshold': '85% 이상 정상',
                'action': '형식 오류 자동 수정'
            }
        ]
        
        # 포털별 특별 검사
        if portal_id == 'bizinfo':
            quality_checks.append({
                'check_type': 'BIZINFO 특화 검증',
                'description': '기관명 정규화, 지원형태 표준화',
                'threshold': '품질 점수 70점 이상',
                'action': '무결성 수정기 자동 실행'
            })
        
        return {
            'quality_threshold': config.quality_threshold,
            'expected_quality_score': 85.0 if portal_id == 'kstartup' else 78.0,
            'quality_checks': quality_checks,
            'auto_fix_enabled': True,
            'manual_review_triggers': [
                '품질 점수 60점 미만',
                '필수 필드 누락률 10% 초과', 
                '연속 품질 실패 5건'
            ],
            'quality_reports': {
                'realtime_monitoring': True,
                'hourly_summary': True,
                'daily_report': True,
                'quality_trend_analysis': True
            }
        }

    def generate_process_checklist(self, portal_id: str) -> Dict[str, any]:
        """프로세스 체크리스트 생성"""
        
        checklist = {}
        
        for phase, guidelines in self.process_guidelines.items():
            checklist[phase] = {
                'title': guidelines['title'],
                'items': [
                    {
                        'task': item,
                        'completed': False,
                        'notes': '',
                        'timestamp': None
                    } for item in guidelines['checklist']
                ],
                'critical_points': guidelines['critical_points'],
                'phase_status': 'pending'
            }
        
        # 포털별 특별 항목 추가
        if portal_id == 'bizinfo':
            checklist['validation']['items'].append({
                'task': 'BIZINFO 특별 주의사항 확인',
                'completed': False,
                'notes': 'IP 차단 위험 높음, 보수적 접근 필요',
                'timestamp': None
            })
        
        return {
            'portal_id': portal_id,
            'checklist_created_at': datetime.now().isoformat(),
            'total_phases': len(checklist),
            'total_tasks': sum(len(phase['items']) for phase in checklist.values()),
            'checklist': checklist,
            'completion_guide': {
                'sequence': ['preparation', 'validation', 'execution', 'monitoring', 'optimization'],
                'parallel_allowed': ['monitoring', 'optimization'],
                'blocking_conditions': [
                    'preparation 미완료 시 validation 불가',
                    'validation 실패 시 execution 불가',
                    '안전도 80점 미만 시 execution 불가'
                ]
            }
        }

    def get_best_practices_summary(self) -> Dict[str, any]:
        """베스트 프랙티스 요약"""
        
        return {
            'title': '정부 포털 스크래핑 베스트 프랙티스',
            'version': '1.0.0',
            'last_updated': '2025-08-24',
            
            'core_principles': [
                '안전성 우선: 수집 속도보다 안전성을 우선시',
                '점진적 접근: 소량부터 시작하여 점진적 확대',
                '실시간 모니터링: 위험 징후 조기 감지',
                '자동 복구: 오류 발생 시 자동 복구 시스템 활용',
                '품질 보장: 데이터 품질 실시간 검증'
            ],
            
            'golden_rules': {
                'timing': [
                    '업무시간(09:00-18:00) 수집 금지',
                    '새벽 시간대(03:00-07:00) 최우선 활용',
                    '야간 시간대(22:00-03:00) 적극 활용',
                    '점심시간(12:00-14:00) 특별 주의'
                ],
                'intervals': [
                    'K-startup: 기본 5분, 최소 3분',
                    'BIZINFO: 기본 7분, 최소 4분',
                    '실패 시 지수적 백오프 적용',
                    '성공률 기반 간격 자동 조절'
                ],
                'safety': [
                    '안전도 점수 80점 이상 유지',
                    'IP 차단 즉시 복구 대기',
                    '연속 실패 5회 시 즉시 중단',
                    '서킷브레이커 활성화 시 쿨다운 준수'
                ],
                'quality': [
                    '품질 점수 70점 이상 유지',
                    '필수 필드 100% 검증',
                    '중복 데이터 실시간 필터링',
                    'BIZINFO 데이터 무결성 특별 관리'
                ]
            },
            
            'portal_specific_tips': {
                'kstartup': [
                    '비교적 관대한 정책, 안정적 수집 가능',
                    '일일 100-150개 목표로 설정',
                    '응답 시간 2초 이내 정상',
                    '새로운 공고 업데이트가 빠름'
                ],
                'bizinfo': [
                    '매우 엄격한 정책, 보수적 접근 필수',
                    '일일 80-120개 목표로 설정', 
                    '응답 시간 5초 이내 허용',
                    '데이터 무결성 오류 빈발',
                    'IP 차단 위험 매우 높음'
                ]
            },
            
            'emergency_procedures': [
                '🚨 IP 차단 시: 즉시 중단, 최소 1시간 대기',
                '⚠️ 연속 실패 시: 간격 2배 증가, 패턴 변경',
                '🔄 서킷브레이커 시: 쿨다운 완료까지 대기',
                '📉 품질 저하 시: 무결성 검증 강화',
                '🛑 비상 상황 시: 수동 개입 요청'
            ],
            
            'success_metrics': {
                'safety_kpis': [
                    '안전도 점수 평균 85점 이상',
                    'IP 차단 발생률 월 1회 미만',
                    '서킷브레이커 활성화 주 1회 미만'
                ],
                'performance_kpis': [
                    '전체 성공률 80% 이상',
                    '일일 목표 달성률 90% 이상',
                    '평균 응답시간 3초 이내'
                ],
                'quality_kpis': [
                    '데이터 품질 점수 평균 75점 이상',
                    '필수 필드 누락률 5% 미만',
                    '중복 데이터율 3% 미만'
                ]
            }
        }

# 사용 예시
def main():
    """메인 실행 함수"""
    process = OptimalCollectionProcess()
    
    print("=" * 80)
    print("🎯 최적 수집 프로세스 가이드")
    print("=" * 80)
    print()
    
    # 베스트 프랙티스 출력
    best_practices = process.get_best_practices_summary()
    print(f"📚 {best_practices['title']}")
    print(f"버전: {best_practices['version']} | 업데이트: {best_practices['last_updated']}")
    print()
    
    print("🎯 핵심 원칙:")
    for principle in best_practices['core_principles']:
        print(f"  • {principle}")
    print()
    
    # 포털별 최적 계획 생성
    for portal_id in ['kstartup', 'bizinfo']:
        print(f"📋 {portal_id.upper()} 최적 수집 계획")
        print("-" * 50)
        
        # 수집 계획 생성
        plan = process.create_optimal_collection_plan(portal_id, 24)
        
        if 'error' in plan:
            print(f"오류: {plan['error']}")
            continue
        
        print(f"계획 기간: {plan['plan_period']}")
        print(f"예상 수집량: {plan['expected_results']['total_collections']}개")
        print(f"예상 성공률: {plan['expected_results']['estimated_success_rate']}%")
        print(f"위험 수준: {plan['expected_results']['risk_level']}")
        print()
        
        # 현재 상황 권장사항
        print("💡 현재 권장사항:")
        for rec in plan['current_analysis']['recommendations']:
            print(f"  • {rec}")
        print()
        
        # 체크리스트 생성
        checklist = process.generate_process_checklist(portal_id)
        print(f"📝 프로세스 체크리스트: 총 {checklist['total_tasks']}개 작업")
        print()

if __name__ == "__main__":
    main()