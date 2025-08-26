#!/usr/bin/env python3
"""
IP 블랙리스트 방지 시스템
정부 포털 수집 시 IP 차단 방지 및 자동 복구

Author: Paperwork AI Team
Version: 1.0.0
Date: 2025-08-24
"""

import random
import logging
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import time
import os

logger = logging.getLogger(__name__)

class BlacklistStatus(Enum):
    """블랙리스트 상태"""
    SAFE = "safe"           # 안전
    WARNING = "warning"     # 경고
    BLOCKED = "blocked"     # 차단됨
    RECOVERING = "recovering"  # 복구 중

@dataclass
class IPStatus:
    """IP 상태 정보"""
    ip_address: str
    status: BlacklistStatus
    last_success: Optional[datetime]
    last_failure: Optional[datetime]
    failure_count: int
    success_count: int
    blocked_since: Optional[datetime]
    recovery_attempts: int
    current_cooldown: int  # 현재 쿨다운 시간(초)
    notes: List[str]

@dataclass
class ProxyConfig:
    """프록시 설정"""
    proxy_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: bool = True
    success_rate: float = 0.0
    last_used: Optional[datetime] = None

class IPBlacklistPrevention:
    """IP 블랙리스트 방지 시스템"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or '/home/ubuntu/heal7-project/backend/services/government-portal-scraper/ip_prevention_config.json'
        self.ip_status_history = {}  # IP별 상태 이력
        self.proxy_pool = []  # 프록시 풀
        self.current_ip = None
        self.blacklist_indicators = self._init_blacklist_indicators()
        self.recovery_strategies = self._init_recovery_strategies()
        
        # 설정 로드
        self.load_config()
        
        # 상태 모니터링
        self.monitoring_enabled = True
        self.last_health_check = None
        
    def _init_blacklist_indicators(self) -> Dict[str, Dict]:
        """블랙리스트 징후 패턴"""
        return {
            'http_codes': {
                403: {'severity': 'high', 'description': 'Forbidden - 접근 거부'},
                429: {'severity': 'high', 'description': 'Too Many Requests - 요청 과다'},
                503: {'severity': 'medium', 'description': 'Service Unavailable - 서비스 불가'},
                502: {'severity': 'medium', 'description': 'Bad Gateway - 게이트웨이 오류'},
                418: {'severity': 'high', 'description': "I'm a teapot - 봇 감지"},
                444: {'severity': 'high', 'description': 'Connection closed - 연결 차단'}
            },
            'response_patterns': {
                'captcha_keywords': ['captcha', '보안문자', '자동입력방지', 'verify', 'robot'],
                'block_keywords': ['blocked', '차단', '접근거부', 'access denied', 'banned'],
                'rate_limit_keywords': ['rate limit', '요청한도', 'too many', '과다요청']
            },
            'timing_patterns': {
                'consecutive_failures': 5,      # 연속 실패 임계치
                'success_rate_threshold': 0.3,  # 성공률 임계치
                'response_time_spike': 10.0     # 응답시간 급증 임계치(초)
            }
        }
    
    def _init_recovery_strategies(self) -> Dict[str, Dict]:
        """복구 전략"""
        return {
            'immediate': {
                'actions': ['change_user_agent', 'add_random_delay', 'change_headers'],
                'cooldown': 300,  # 5분
                'max_attempts': 3
            },
            'moderate': {
                'actions': ['switch_proxy', 'extend_intervals', 'reduce_concurrency'],
                'cooldown': 1800,  # 30분
                'max_attempts': 5
            },
            'aggressive': {
                'actions': ['full_ip_rotation', 'long_cooldown', 'pattern_randomization'],
                'cooldown': 3600,  # 1시간
                'max_attempts': 2
            },
            'emergency': {
                'actions': ['stop_collection', 'manual_intervention'],
                'cooldown': 7200,  # 2시간
                'max_attempts': 1
            }
        }

    def load_config(self):
        """설정 파일 로드"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # IP 상태 이력 로드
                if 'ip_history' in config:
                    for ip, status_data in config['ip_history'].items():
                        # 날짜 필드 파싱
                        for date_field in ['last_success', 'last_failure', 'blocked_since']:
                            if status_data.get(date_field):
                                status_data[date_field] = datetime.fromisoformat(status_data[date_field])
                        
                        self.ip_status_history[ip] = IPStatus(**status_data)
                
                # 프록시 풀 로드
                if 'proxy_pool' in config:
                    for proxy_data in config['proxy_pool']:
                        if proxy_data.get('last_used'):
                            proxy_data['last_used'] = datetime.fromisoformat(proxy_data['last_used'])
                        self.proxy_pool.append(ProxyConfig(**proxy_data))
                
                logger.info(f"설정 로드 완료: IP {len(self.ip_status_history)}개, 프록시 {len(self.proxy_pool)}개")
            
        except Exception as e:
            logger.error(f"설정 로드 실패: {e}")
            self._create_default_config()

    def save_config(self):
        """설정 파일 저장"""
        try:
            config = {
                'ip_history': {},
                'proxy_pool': [],
                'last_updated': datetime.now().isoformat()
            }
            
            # IP 상태 이력 저장
            for ip, status in self.ip_status_history.items():
                status_dict = asdict(status)
                # 날짜 필드 직렬화
                for date_field in ['last_success', 'last_failure', 'blocked_since']:
                    if status_dict.get(date_field):
                        status_dict[date_field] = status_dict[date_field].isoformat()
                status_dict['status'] = status_dict['status'].value
                config['ip_history'][ip] = status_dict
            
            # 프록시 풀 저장
            for proxy in self.proxy_pool:
                proxy_dict = asdict(proxy)
                if proxy_dict.get('last_used'):
                    proxy_dict['last_used'] = proxy_dict['last_used'].isoformat()
                config['proxy_pool'].append(proxy_dict)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            logger.debug("설정 저장 완료")
            
        except Exception as e:
            logger.error(f"설정 저장 실패: {e}")

    def _create_default_config(self):
        """기본 설정 생성"""
        # 현재 IP 확인
        try:
            import requests
            response = requests.get('https://api.ipify.org', timeout=5)
            current_ip = response.text.strip()
            
            self.ip_status_history[current_ip] = IPStatus(
                ip_address=current_ip,
                status=BlacklistStatus.SAFE,
                last_success=datetime.now(),
                last_failure=None,
                failure_count=0,
                success_count=1,
                blocked_since=None,
                recovery_attempts=0,
                current_cooldown=0,
                notes=["초기 IP"]
            )
            
            logger.info(f"기본 설정 생성 완료 - 현재 IP: {current_ip}")
            
        except Exception as e:
            logger.error(f"현재 IP 확인 실패: {e}")

    def detect_blacklist_signs(self, response_code: int, response_content: str = "", 
                             response_time: float = 0.0, url: str = "") -> Tuple[bool, str, str]:
        """블랙리스트 징후 감지"""
        detected_signs = []
        severity = "low"
        
        # HTTP 응답 코드 확인
        if response_code in self.blacklist_indicators['http_codes']:
            sign_info = self.blacklist_indicators['http_codes'][response_code]
            detected_signs.append(f"HTTP {response_code}: {sign_info['description']}")
            severity = max(severity, sign_info['severity'])
        
        # 응답 내용 패턴 확인
        if response_content:
            content_lower = response_content.lower()
            
            for pattern_type, keywords in self.blacklist_indicators['response_patterns'].items():
                for keyword in keywords:
                    if keyword in content_lower:
                        detected_signs.append(f"의심 패턴 감지: {keyword} ({pattern_type})")
                        severity = "high"
                        break
        
        # 응답 시간 확인
        if response_time > self.blacklist_indicators['timing_patterns']['response_time_spike']:
            detected_signs.append(f"응답 시간 급증: {response_time:.1f}초")
            severity = max(severity, "medium")
        
        is_suspicious = len(detected_signs) > 0
        summary = "; ".join(detected_signs) if detected_signs else "정상"
        
        return is_suspicious, severity, summary

    def update_ip_status(self, ip_address: str, success: bool, response_code: int = 200,
                        response_content: str = "", response_time: float = 0.0, url: str = ""):
        """IP 상태 업데이트"""
        now = datetime.now()
        
        # IP 상태 초기화 (없으면)
        if ip_address not in self.ip_status_history:
            self.ip_status_history[ip_address] = IPStatus(
                ip_address=ip_address,
                status=BlacklistStatus.SAFE,
                last_success=None,
                last_failure=None,
                failure_count=0,
                success_count=0,
                blocked_since=None,
                recovery_attempts=0,
                current_cooldown=0,
                notes=[]
            )
        
        ip_status = self.ip_status_history[ip_address]
        
        if success:
            # 성공 처리
            ip_status.last_success = now
            ip_status.success_count += 1
            ip_status.failure_count = 0  # 연속 실패 카운트 리셋
            
            # 복구 상태에서 성공하면 안전 상태로 전환
            if ip_status.status == BlacklistStatus.RECOVERING:
                ip_status.status = BlacklistStatus.SAFE
                ip_status.blocked_since = None
                ip_status.recovery_attempts = 0
                ip_status.current_cooldown = 0
                ip_status.notes.append(f"{now.strftime('%H:%M')} 복구 성공")
                logger.info(f"IP {ip_address} 복구 완료")
        
        else:
            # 실패 처리
            ip_status.last_failure = now
            ip_status.failure_count += 1
            
            # 블랙리스트 징후 확인
            is_suspicious, severity, summary = self.detect_blacklist_signs(
                response_code, response_content, response_time, url
            )
            
            if is_suspicious:
                ip_status.notes.append(f"{now.strftime('%H:%M')} {summary}")
                
                # 상태 전환 로직
                if severity == "high" or ip_status.failure_count >= 5:
                    if ip_status.status != BlacklistStatus.BLOCKED:
                        ip_status.status = BlacklistStatus.BLOCKED
                        ip_status.blocked_since = now
                        ip_status.current_cooldown = self.recovery_strategies['moderate']['cooldown']
                        logger.warning(f"IP {ip_address} 블랙리스트로 판단: {summary}")
                
                elif severity == "medium" or ip_status.failure_count >= 3:
                    if ip_status.status == BlacklistStatus.SAFE:
                        ip_status.status = BlacklistStatus.WARNING
                        ip_status.current_cooldown = self.recovery_strategies['immediate']['cooldown']
                        logger.warning(f"IP {ip_address} 경고 상태: {summary}")
        
        # 성공률 계산 및 상태 재평가
        total_requests = ip_status.success_count + ip_status.failure_count
        if total_requests > 10:  # 충분한 샘플이 있을 때만
            success_rate = ip_status.success_count / total_requests
            if success_rate < self.blacklist_indicators['timing_patterns']['success_rate_threshold']:
                if ip_status.status == BlacklistStatus.SAFE:
                    ip_status.status = BlacklistStatus.WARNING
                    logger.warning(f"IP {ip_address} 성공률 낮음: {success_rate:.1%}")

    def get_recovery_strategy(self, ip_address: str) -> Dict:
        """IP별 복구 전략 선택"""
        if ip_address not in self.ip_status_history:
            return self.recovery_strategies['immediate']
        
        ip_status = self.ip_status_history[ip_address]
        
        if ip_status.recovery_attempts == 0:
            return self.recovery_strategies['immediate']
        elif ip_status.recovery_attempts <= 3:
            return self.recovery_strategies['moderate'] 
        elif ip_status.recovery_attempts <= 5:
            return self.recovery_strategies['aggressive']
        else:
            return self.recovery_strategies['emergency']

    def apply_recovery_actions(self, ip_address: str, strategy: Dict) -> Dict[str, any]:
        """복구 작업 실행"""
        actions_applied = []
        recommendations = []
        
        for action in strategy['actions']:
            if action == 'change_user_agent':
                new_agent = self._get_random_user_agent()
                actions_applied.append(f"User-Agent 변경: {new_agent[:50]}...")
                
            elif action == 'add_random_delay':
                delay = random.randint(10, 30)
                actions_applied.append(f"랜덤 지연 추가: {delay}초")
                
            elif action == 'change_headers':
                actions_applied.append("HTTP 헤더 랜덤화 적용")
                
            elif action == 'switch_proxy':
                if self.proxy_pool:
                    proxy = self._select_best_proxy()
                    if proxy:
                        actions_applied.append(f"프록시 전환: {proxy.proxy_url}")
                    else:
                        recommendations.append("사용 가능한 프록시가 없습니다")
                else:
                    recommendations.append("프록시 풀이 비어있습니다")
                
            elif action == 'extend_intervals':
                actions_applied.append("수집 간격 확대 (2배)")
                
            elif action == 'reduce_concurrency':
                actions_applied.append("동시 요청 수 감소")
                
            elif action == 'full_ip_rotation':
                actions_applied.append("완전한 IP 순환 시작")
                
            elif action == 'long_cooldown':
                cooldown_hours = strategy['cooldown'] // 3600
                actions_applied.append(f"장기 휴지: {cooldown_hours}시간")
                
            elif action == 'pattern_randomization':
                actions_applied.append("요청 패턴 완전 랜덤화")
                
            elif action == 'stop_collection':
                actions_applied.append("⚠️ 수집 중지")
                recommendations.append("수동 개입이 필요합니다")
                
            elif action == 'manual_intervention':
                recommendations.append("🚨 수동 개입 필수 - 관리자 연락 필요")
        
        # 복구 시도 횟수 증가
        if ip_address in self.ip_status_history:
            self.ip_status_history[ip_address].recovery_attempts += 1
            self.ip_status_history[ip_address].status = BlacklistStatus.RECOVERING
        
        return {
            'actions_applied': actions_applied,
            'recommendations': recommendations,
            'cooldown_seconds': strategy['cooldown'],
            'max_attempts_reached': self.ip_status_history[ip_address].recovery_attempts >= strategy['max_attempts']
        }

    def _get_random_user_agent(self) -> str:
        """랜덤 User-Agent 생성"""
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        return random.choice(agents)

    def _select_best_proxy(self) -> Optional[ProxyConfig]:
        """최적 프록시 선택"""
        if not self.proxy_pool:
            return None
        
        # 활성 프록시만 필터링
        active_proxies = [p for p in self.proxy_pool if p.is_active]
        if not active_proxies:
            return None
        
        # 성공률과 마지막 사용 시간 고려하여 선택
        best_proxy = max(active_proxies, key=lambda p: (
            p.success_rate,
            -(time.time() - p.last_used.timestamp()) if p.last_used else 0
        ))
        
        return best_proxy

    def get_system_status(self) -> Dict[str, any]:
        """시스템 전체 상태 조회"""
        now = datetime.now()
        total_ips = len(self.ip_status_history)
        
        # 상태별 IP 개수
        status_counts = {status: 0 for status in BlacklistStatus}
        for ip_status in self.ip_status_history.values():
            status_counts[ip_status.status] += 1
        
        # 전체 성공률 계산
        total_success = sum(ip.success_count for ip in self.ip_status_history.values())
        total_failure = sum(ip.failure_count for ip in self.ip_status_history.values())
        total_requests = total_success + total_failure
        overall_success_rate = (total_success / total_requests * 100) if total_requests > 0 else 0
        
        # 위험도 계산
        blocked_count = status_counts[BlacklistStatus.BLOCKED]
        warning_count = status_counts[BlacklistStatus.WARNING]
        
        if blocked_count > total_ips * 0.5:
            risk_level = "위험"
            risk_color = "red"
        elif blocked_count > 0 or warning_count > total_ips * 0.3:
            risk_level = "경고" 
            risk_color = "orange"
        else:
            risk_level = "안전"
            risk_color = "green"
        
        # 권장사항
        recommendations = []
        if blocked_count > 0:
            recommendations.append("차단된 IP가 있습니다. 복구 작업이 필요합니다.")
        if warning_count > 2:
            recommendations.append("경고 상태 IP가 많습니다. 수집 속도를 줄이세요.")
        if overall_success_rate < 70:
            recommendations.append("전체 성공률이 낮습니다. 수집 전략을 재검토하세요.")
        
        return {
            'timestamp': now.isoformat(),
            'total_ips': total_ips,
            'status_distribution': {
                'safe': status_counts[BlacklistStatus.SAFE],
                'warning': status_counts[BlacklistStatus.WARNING], 
                'blocked': status_counts[BlacklistStatus.BLOCKED],
                'recovering': status_counts[BlacklistStatus.RECOVERING]
            },
            'overall_success_rate': round(overall_success_rate, 1),
            'risk_assessment': {
                'level': risk_level,
                'color': risk_color,
                'score': max(0, 100 - (blocked_count * 30 + warning_count * 10))
            },
            'active_proxies': len([p for p in self.proxy_pool if p.is_active]),
            'recommendations': recommendations,
            'last_incident': self._get_last_incident(),
            'recovery_in_progress': sum(1 for ip in self.ip_status_history.values() 
                                      if ip.status == BlacklistStatus.RECOVERING)
        }

    def _get_last_incident(self) -> Optional[Dict]:
        """최근 사건 조회"""
        last_blocked = None
        last_blocked_time = None
        
        for ip, status in self.ip_status_history.items():
            if status.blocked_since and (not last_blocked_time or status.blocked_since > last_blocked_time):
                last_blocked = ip
                last_blocked_time = status.blocked_since
        
        if last_blocked:
            return {
                'ip': last_blocked,
                'blocked_time': last_blocked_time.isoformat(),
                'time_ago': str(datetime.now() - last_blocked_time).split('.')[0]
            }
        
        return None

    def start_monitoring(self, check_interval: int = 300):
        """모니터링 시작 (5분 간격)"""
        async def monitor_loop():
            while self.monitoring_enabled:
                try:
                    await self.health_check()
                    await asyncio.sleep(check_interval)
                except Exception as e:
                    logger.error(f"모니터링 오류: {e}")
                    await asyncio.sleep(60)  # 오류 시 1분 대기
        
        logger.info("IP 블랙리스트 방지 모니터링 시작")
        return asyncio.create_task(monitor_loop())

    async def health_check(self):
        """상태 점검"""
        now = datetime.now()
        self.last_health_check = now
        
        # 자동 복구 확인
        for ip, status in self.ip_status_history.items():
            if status.status == BlacklistStatus.RECOVERING:
                if status.blocked_since:
                    cooldown_end = status.blocked_since + timedelta(seconds=status.current_cooldown)
                    if now > cooldown_end:
                        # 복구 시도
                        logger.info(f"IP {ip} 자동 복구 시도 중...")
                        strategy = self.get_recovery_strategy(ip)
                        recovery_result = self.apply_recovery_actions(ip, strategy)
                        
                        if recovery_result['max_attempts_reached']:
                            logger.error(f"IP {ip} 복구 시도 한도 초과")
        
        # 설정 자동 저장
        self.save_config()

# 사용 예시
async def main():
    """메인 실행 함수"""
    prevention = IPBlacklistPrevention()
    
    print("=" * 60)
    print("🛡️ IP 블랙리스트 방지 시스템 테스트")
    print("=" * 60)
    print()
    
    # 현재 상태 확인
    status = prevention.get_system_status()
    print("📊 시스템 상태:")
    print(f"  총 IP: {status['total_ips']}")
    print(f"  위험도: {status['risk_assessment']['level']} ({status['risk_assessment']['score']}점)")
    print(f"  전체 성공률: {status['overall_success_rate']}%")
    print()
    
    # 테스트 시나리오: 실패 상황 시뮬레이션
    test_ip = "192.168.1.100"
    
    print("🧪 블랙리스트 감지 테스트:")
    
    # 정상 요청
    prevention.update_ip_status(test_ip, success=True, response_code=200)
    print("  ✅ 정상 요청: 성공")
    
    # 실패 요청들
    prevention.update_ip_status(test_ip, success=False, response_code=403, 
                              response_content="Access Denied")
    print("  ❌ 403 Forbidden 감지")
    
    prevention.update_ip_status(test_ip, success=False, response_code=429, 
                              response_content="Too many requests")
    print("  ❌ 429 Too Many Requests 감지")
    
    # 복구 전략 테스트
    strategy = prevention.get_recovery_strategy(test_ip)
    recovery_result = prevention.apply_recovery_actions(test_ip, strategy)
    
    print()
    print("🔧 복구 작업 결과:")
    for action in recovery_result['actions_applied']:
        print(f"  - {action}")
    
    if recovery_result['recommendations']:
        print("\n💡 권장사항:")
        for rec in recovery_result['recommendations']:
            print(f"  - {rec}")

if __name__ == "__main__":
    asyncio.run(main())