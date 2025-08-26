#!/usr/bin/env python3
"""
안전한 정부포털 스크래핑 가이드라인
IP 블랙리스트 방지 및 데이터 무결성 보장

Author: Paperwork AI Team
Version: 1.0.0
Date: 2025-08-24
"""

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass
import asyncio
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class SafeCollectionConfig:
    """안전한 수집 설정"""
    # 기본 수집 제한
    max_requests_per_hour: int = 30          # 시간당 최대 요청수
    max_requests_per_day: int = 200          # 일일 최대 요청수
    min_interval_seconds: int = 120          # 최소 요청 간격 (2분)
    max_interval_seconds: int = 600          # 최대 요청 간격 (10분)
    
    # 랜덤화 설정
    randomize_intervals: bool = True         # 간격 랜덤화 사용
    randomize_user_agents: bool = True       # User-Agent 랜덤화
    randomize_headers: bool = True           # HTTP 헤더 랜덤화
    
    # 안전 장치
    enable_circuit_breaker: bool = True      # 서킷 브레이커 사용
    max_consecutive_failures: int = 5        # 최대 연속 실패 허용
    cooldown_period_minutes: int = 60        # 쿨다운 기간 (분)
    
    # 데이터 무결성
    enable_integrity_check: bool = True      # 무결성 검사 활성화
    min_content_length: int = 100            # 최소 컨텐츠 길이
    required_fields: List[str] = None        # 필수 필드 목록

class SafeScrapingManager:
    """안전한 스크래핑 관리자"""
    
    def __init__(self, config: SafeCollectionConfig = None):
        self.config = config or SafeCollectionConfig()
        self.request_history = []  # 요청 이력
        self.failure_count = 0     # 연속 실패 카운트
        self.circuit_open = False  # 서킷 브레이커 상태
        self.last_failure_time = None
        
        # User-Agent 풀
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        
        # 헤더 템플릿
        self.header_templates = [
            {"Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"},
            {"Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"},
            {"Accept-Encoding": "gzip, deflate, br"},
            {"DNT": "1"},
            {"Connection": "keep-alive"},
            {"Upgrade-Insecure-Requests": "1"}
        ]

    def get_safe_interval(self) -> int:
        """안전한 요청 간격 계산"""
        if self.config.randomize_intervals:
            # 랜덤 간격 (최소 2분 ~ 최대 10분)
            base_interval = random.randint(
                self.config.min_interval_seconds, 
                self.config.max_interval_seconds
            )
            
            # 최근 실패가 있었다면 간격 증가
            if self.failure_count > 0:
                multiplier = min(2.0 * self.failure_count, 5.0)  # 최대 5배
                base_interval = int(base_interval * multiplier)
            
            return base_interval
        else:
            return self.config.min_interval_seconds

    def get_random_headers(self) -> Dict[str, str]:
        """랜덤 HTTP 헤더 생성"""
        headers = {
            "User-Agent": random.choice(self.user_agents)
        }
        
        if self.config.randomize_headers:
            # 랜덤 헤더 추가
            num_headers = random.randint(2, 4)
            selected_headers = random.sample(self.header_templates, num_headers)
            
            for header_dict in selected_headers:
                headers.update(header_dict)
        
        return headers

    def check_rate_limit(self) -> bool:
        """요청 비율 제한 확인"""
        now = datetime.now()
        
        # 1시간 이내 요청 수 확인
        hour_ago = now - timedelta(hours=1)
        recent_requests = [
            req for req in self.request_history 
            if req['timestamp'] > hour_ago
        ]
        
        if len(recent_requests) >= self.config.max_requests_per_hour:
            logger.warning(f"시간당 요청 한도 초과: {len(recent_requests)}/{self.config.max_requests_per_hour}")
            return False
        
        # 24시간 이내 요청 수 확인
        day_ago = now - timedelta(days=1)
        daily_requests = [
            req for req in self.request_history 
            if req['timestamp'] > day_ago
        ]
        
        if len(daily_requests) >= self.config.max_requests_per_day:
            logger.warning(f"일일 요청 한도 초과: {len(daily_requests)}/{self.config.max_requests_per_day}")
            return False
        
        return True

    def check_circuit_breaker(self) -> bool:
        """서킷 브레이커 상태 확인"""
        if not self.config.enable_circuit_breaker:
            return True
        
        # 서킷이 열려있는 경우
        if self.circuit_open:
            if self.last_failure_time:
                cooldown_end = self.last_failure_time + timedelta(
                    minutes=self.config.cooldown_period_minutes
                )
                
                if datetime.now() > cooldown_end:
                    logger.info("서킷 브레이커 쿨다운 완료, 재시도 허용")
                    self.circuit_open = False
                    self.failure_count = 0
                    return True
                else:
                    remaining = (cooldown_end - datetime.now()).total_seconds()
                    logger.warning(f"서킷 브레이커 활성화, {remaining:.0f}초 후 재시도 가능")
                    return False
        
        return True

    def record_request(self, success: bool, response_data: Dict = None):
        """요청 결과 기록"""
        now = datetime.now()
        
        # 요청 이력 추가
        self.request_history.append({
            'timestamp': now,
            'success': success,
            'response_data': response_data
        })
        
        # 이력 크기 제한 (최근 1000개만 유지)
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
        
        if success:
            # 성공 시 실패 카운트 리셋
            self.failure_count = 0
            if self.circuit_open:
                logger.info("요청 성공, 서킷 브레이커 닫힘")
                self.circuit_open = False
        else:
            # 실패 시 카운트 증가
            self.failure_count += 1
            self.last_failure_time = now
            
            if (self.config.enable_circuit_breaker and 
                self.failure_count >= self.config.max_consecutive_failures):
                logger.error(f"연속 실패 {self.failure_count}회, 서킷 브레이커 활성화")
                self.circuit_open = True

    def validate_data_integrity(self, data: Dict) -> Tuple[bool, List[str]]:
        """데이터 무결성 검증"""
        if not self.config.enable_integrity_check:
            return True, []
        
        errors = []
        
        # 필수 필드 확인
        if self.config.required_fields:
            for field in self.config.required_fields:
                if field not in data or not data[field]:
                    errors.append(f"필수 필드 누락: {field}")
        
        # 컨텐츠 길이 확인
        content = str(data.get('content', ''))
        if len(content) < self.config.min_content_length:
            errors.append(f"컨텐츠 길이 부족: {len(content)} < {self.config.min_content_length}")
        
        # 제목 유효성 확인
        title = data.get('title', '')
        if not title or len(title.strip()) < 5:
            errors.append("제목이 너무 짧거나 비어있음")
        
        # 날짜 유효성 확인
        date_fields = ['created_at', 'updated_at', 'deadline']
        for field in date_fields:
            if field in data and data[field]:
                try:
                    datetime.fromisoformat(str(data[field]))
                except:
                    errors.append(f"날짜 형식 오류: {field}")
        
        # URL 유효성 확인
        url = data.get('url', '')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            errors.append("잘못된 URL 형식")
        
        return len(errors) == 0, errors

    def get_collection_recommendations(self) -> Dict[str, str]:
        """수집 최적화 권장사항"""
        recommendations = {}
        
        # 최근 성공률 계산
        recent_requests = self.request_history[-50:] if self.request_history else []
        if recent_requests:
            success_rate = sum(1 for req in recent_requests if req['success']) / len(recent_requests)
            
            if success_rate < 0.8:
                recommendations['interval'] = "요청 간격을 늘려주세요 (현재 성공률 낮음)"
            elif success_rate > 0.95:
                recommendations['interval'] = "요청 간격을 약간 줄일 수 있습니다"
        
        # 시간대 권장사항
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 18:
            recommendations['timing'] = "업무시간대입니다. 간격을 더 길게 설정하세요"
        elif 22 <= current_hour or current_hour <= 6:
            recommendations['timing'] = "야간시간대입니다. 비교적 안전한 시간입니다"
        
        # 요청량 권장사항
        today_requests = len([
            req for req in self.request_history 
            if req['timestamp'].date() == datetime.now().date()
        ])
        
        if today_requests > self.config.max_requests_per_day * 0.8:
            recommendations['volume'] = "금일 요청량이 많습니다. 내일까지 대기를 권장합니다"
        
        return recommendations

    def get_safety_score(self) -> Tuple[float, str]:
        """현재 수집 안전도 점수 (0-100)"""
        score = 100.0
        factors = []
        
        # 최근 실패율 반영
        recent_requests = self.request_history[-20:] if self.request_history else []
        if recent_requests:
            failure_rate = sum(1 for req in recent_requests if not req['success']) / len(recent_requests)
            score -= failure_rate * 30
            if failure_rate > 0.2:
                factors.append("높은 실패율")
        
        # 요청 빈도 반영
        hour_ago = datetime.now() - timedelta(hours=1)
        recent_count = len([
            req for req in self.request_history 
            if req['timestamp'] > hour_ago
        ])
        
        if recent_count > self.config.max_requests_per_hour * 0.8:
            score -= 20
            factors.append("높은 요청 빈도")
        
        # 서킷 브레이커 상태 반영
        if self.circuit_open:
            score -= 40
            factors.append("서킷 브레이커 활성화")
        
        # 시간대 반영
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 18:
            score -= 10
            factors.append("업무시간대")
        
        score = max(0, min(100, score))
        
        if score >= 80:
            status = "안전"
        elif score >= 60:
            status = "주의"
        elif score >= 40:
            status = "경고"
        else:
            status = "위험"
        
        return score, status

# BIZINFO 특화 데이터 무결성 검사
class BizinfoIntegrityChecker:
    """BIZINFO 데이터 무결성 검사기"""
    
    def __init__(self):
        self.required_fields = [
            'title',           # 사업명
            'agency',          # 주관기관
            'support_type',    # 지원형태
            'application_period', # 신청기간
            'target',          # 지원대상
        ]
        
        self.optional_fields = [
            'budget',          # 예산규모
            'contact',         # 담당자 연락처
            'homepage',        # 홈페이지
            'detail_url'       # 상세URL
        ]

    def check_bizinfo_data(self, data: Dict) -> Tuple[bool, List[str], Dict]:
        """BIZINFO 데이터 무결성 상세 검사"""
        errors = []
        warnings = []
        quality_score = 100.0
        
        # 필수 필드 검사
        for field in self.required_fields:
            if field not in data or not str(data[field]).strip():
                errors.append(f"BIZINFO 필수 필드 누락: {field}")
                quality_score -= 15
        
        # 제목 품질 검사
        title = data.get('title', '')
        if title:
            if len(title) < 10:
                warnings.append("제목이 너무 짧습니다")
                quality_score -= 5
            elif len(title) > 200:
                warnings.append("제목이 너무 깁니다")
                quality_score -= 3
            
            # 특정 패턴 검사 (공고, 모집 등)
            important_keywords = ['공고', '모집', '지원', '사업']
            if not any(keyword in title for keyword in important_keywords):
                warnings.append("제목에 중요 키워드가 없습니다")
                quality_score -= 5
        
        # 기관명 유효성 검사
        agency = data.get('agency', '')
        if agency:
            if len(agency) < 3:
                errors.append("기관명이 너무 짧습니다")
                quality_score -= 10
            
            # 알려진 기관명 패턴 확인
            valid_agency_patterns = [
                '부', '청', '원', '공단', '재단', '협회', '센터', 
                '기업진흥원', '창업진흥원', '중소벤처기업부'
            ]
            
            if not any(pattern in agency for pattern in valid_agency_patterns):
                warnings.append("기관명 패턴이 일반적이지 않습니다")
                quality_score -= 3
        
        # 신청기간 형식 검사
        application_period = data.get('application_period', '')
        if application_period:
            # 일반적인 기간 표현 패턴 확인
            date_patterns = ['~', '-', '부터', '까지', '월', '일']
            if not any(pattern in application_period for pattern in date_patterns):
                warnings.append("신청기간 형식이 비정상적입니다")
                quality_score -= 5
        
        # URL 유효성 검사
        detail_url = data.get('detail_url', '')
        if detail_url:
            if not detail_url.startswith('http'):
                errors.append("상세URL 형식이 잘못되었습니다")
                quality_score -= 8
            elif 'bizinfo.go.kr' not in detail_url:
                warnings.append("BIZINFO 도메인이 아닙니다")
                quality_score -= 3
        
        # 지원대상 검사
        target = data.get('target', '')
        if target:
            target_keywords = [
                '중소기업', '소상공인', '벤처기업', '스타트업', 
                '청년', '여성', '창업', '기업'
            ]
            
            if not any(keyword in target for keyword in target_keywords):
                warnings.append("지원대상이 명확하지 않습니다")
                quality_score -= 5
        
        quality_score = max(0, min(100, quality_score))
        
        result = {
            'quality_score': round(quality_score, 1),
            'errors': errors,
            'warnings': warnings,
            'recommendations': []
        }
        
        # 개선 권장사항
        if quality_score < 70:
            result['recommendations'].append("데이터 품질이 낮습니다. 다시 수집하시기 바랍니다.")
        
        if len(warnings) > 3:
            result['recommendations'].append("경고사항이 많습니다. 데이터 검증을 강화하세요.")
        
        is_valid = len(errors) == 0 and quality_score >= 60
        
        return is_valid, errors + warnings, result

# 사용 예시 및 권장사항 출력
def print_collection_guidelines():
    """수집 가이드라인 출력"""
    print("=" * 60)
    print("🛡️ 안전한 정부포털 스크래핑 가이드라인")
    print("=" * 60)
    print()
    
    print("📋 기본 원칙:")
    print("  1. 요청 간격: 최소 2분, 권장 5-10분")
    print("  2. 일일 요청량: 최대 200회 (시간당 30회)")
    print("  3. 실패 시 지수적 백오프 적용")
    print("  4. User-Agent 및 헤더 랜덤화")
    print("  5. 업무시간(09-18시) 수집 자제")
    print()
    
    print("⚠️ 위험 요소:")
    print("  - 너무 빠른 연속 요청 (블랙리스트 위험)")
    print("  - 동일한 헤더 반복 사용")
    print("  - 대량 데이터 일괄 수집")
    print("  - 에러 발생 시 계속 시도")
    print()
    
    print("✅ 권장 설정:")
    print("  - 랜덤 간격: 2-10분")
    print("  - 야간 수집: 22시-06시")
    print("  - 배치 크기: 50-100개")
    print("  - 실패 임계치: 5회")
    print("  - 쿨다운: 1시간")
    print()
    
    print("🔍 데이터 무결성:")
    print("  - 필수 필드 검증")
    print("  - 컨텐츠 길이 확인")
    print("  - 중복 데이터 필터링")
    print("  - 품질 점수 60점 이상")
    print()

if __name__ == "__main__":
    print_collection_guidelines()