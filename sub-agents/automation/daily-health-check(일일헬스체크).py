#!/usr/bin/env python3
"""
🏥 HEAL7 일일 헬스 체크 자동화 스크립트
큐브 모델 기반 시스템 상태 점검 및 리포팅

Author: AI Agent Team
Created: 2025-08-20
"""

import subprocess
import json
import requests
import psutil
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/logs/daily-health-check.log'),
        logging.StreamHandler()
    ]
)

class HealthChecker:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report = {
            'timestamp': self.timestamp,
            'overall_status': 'UNKNOWN',
            'cube_health': {},
            'infrastructure': {},
            'security': {},
            'performance': {},
            'recommendations': []
        }
        
    def check_system_resources(self) -> Dict[str, Any]:
        """시스템 리소스 상태 점검"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resources = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent,
                'available_memory_gb': round(memory.available / (1024**3), 2),
                'free_disk_gb': round(disk.free / (1024**3), 2)
            }
            
            # 임계값 검사
            alerts = []
            if cpu_percent > 85:
                alerts.append(f"🚨 CPU 사용률 위험: {cpu_percent}%")
            elif cpu_percent > 70:
                alerts.append(f"⚠️ CPU 사용률 주의: {cpu_percent}%")
                
            if memory.percent > 90:
                alerts.append(f"🚨 메모리 사용률 위험: {memory.percent}%")
            elif memory.percent > 80:
                alerts.append(f"⚠️ 메모리 사용률 주의: {memory.percent}%")
                
            if disk.percent > 95:
                alerts.append(f"🚨 디스크 사용률 위험: {disk.percent}%")
            elif disk.percent > 85:
                alerts.append(f"⚠️ 디스크 사용률 주의: {disk.percent}%")
            
            resources['alerts'] = alerts
            return resources
            
        except Exception as e:
            logging.error(f"시스템 리소스 체크 실패: {e}")
            return {'error': str(e)}
    
    def check_services_status(self) -> Dict[str, Any]:
        """핵심 서비스 상태 점검"""
        services = {
            'nginx': self._check_systemd_service('nginx'),
            'postgresql': self._check_systemd_service('postgresql@14-main'),
            'redis': self._check_systemd_service('redis-server')
        }
        
        # 포트 점검
        ports = {
            '8000': self._check_port(8000),  # 사주 서비스
            '8001': self._check_port(8001),  # 테스트 서비스
            '3000': self._check_port(3000),  # 메인 Vite
            '3001': self._check_port(3001),  # 관리자 Vite
            '3002': self._check_port(3002),  # 키워드 Vite
            '5432': self._check_port(5432),  # PostgreSQL
            '6379': self._check_port(6379)   # Redis
        }
        
        return {
            'systemd_services': services,
            'port_status': ports,
            'active_python_processes': self._count_python_processes(),
            'active_node_processes': self._count_node_processes()
        }
    
    def check_cube_health(self) -> Dict[str, Any]:
        """큐브별 헬스 체크"""
        cubes = {
            'saju_cube': self._check_saju_cube(),
            'admin_cube': self._check_admin_cube(),
            'keywords_cube': self._check_keywords_cube(),
            'main_cube': self._check_main_cube()
        }
        
        return cubes
    
    def check_security_status(self) -> Dict[str, Any]:
        """보안 상태 점검"""
        security = {
            'ssl_certificates': self._check_ssl_certificates(),
            'failed_logins': self._check_failed_logins(),
            'firewall_status': self._check_firewall(),
            'ssh_keys': self._check_ssh_security()
        }
        
        return security
    
    def check_backup_status(self) -> Dict[str, Any]:
        """백업 상태 점검"""
        return {
            'database_backups': self._check_db_backups(),
            'code_repos': self._check_git_status(),
            'config_backups': self._check_config_backups()
        }
    
    def _check_systemd_service(self, service_name: str) -> Dict[str, Any]:
        """systemd 서비스 상태 확인"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True, text=True
            )
            active = result.stdout.strip() == 'active'
            
            # 메모리 사용량 확인
            if active:
                result = subprocess.run(
                    ['systemctl', 'show', service_name, '--property=MemoryCurrent'],
                    capture_output=True, text=True
                )
                memory_info = result.stdout.strip()
            else:
                memory_info = "N/A"
            
            return {
                'active': active,
                'memory_usage': memory_info,
                'status': 'healthy' if active else 'unhealthy'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}
    
    def _check_port(self, port: int) -> Dict[str, Any]:
        """포트 사용 상태 확인"""
        try:
            result = subprocess.run(
                ['lsof', '-i', f':{port}'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # 헤더 제외
                processes = []
                for line in lines:
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            processes.append({
                                'command': parts[0],
                                'pid': parts[1]
                            })
                
                return {
                    'listening': True,
                    'processes': processes,
                    'status': 'active'
                }
            else:
                return {
                    'listening': False,
                    'processes': [],
                    'status': 'inactive'
                }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}
    
    def _count_python_processes(self) -> int:
        """실행 중인 Python 프로세스 수"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'python'],
                capture_output=True, text=True
            )
            return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            return 0
    
    def _count_node_processes(self) -> int:
        """실행 중인 Node.js 프로세스 수"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'node'],
                capture_output=True, text=True
            )
            return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            return 0
    
    def _check_saju_cube(self) -> Dict[str, Any]:
        """사주 큐브 헬스 체크"""
        try:
            # 8000 포트 응답 확인
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'last_check': self.timestamp
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}",
                    'last_check': self.timestamp
                }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error': str(e),
                'last_check': self.timestamp
            }
    
    def _check_admin_cube(self) -> Dict[str, Any]:
        """관리자 큐브 헬스 체크"""
        try:
            # 3001 포트 응답 확인 (Vite 서버)
            response = requests.get('http://localhost:3001', timeout=5)
            if response.status_code in [200, 404]:  # Vite는 404도 정상
                return {
                    'status': 'healthy',
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'last_check': self.timestamp
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}",
                    'last_check': self.timestamp
                }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error': str(e),
                'last_check': self.timestamp
            }
    
    def _check_keywords_cube(self) -> Dict[str, Any]:
        """키워드 큐브 헬스 체크"""
        try:
            # 3002 포트 응답 확인
            response = requests.get('http://localhost:3002', timeout=5)
            if response.status_code in [200, 404]:
                return {
                    'status': 'healthy',
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'last_check': self.timestamp
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}",
                    'last_check': self.timestamp
                }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error': str(e),
                'last_check': self.timestamp
            }
    
    def _check_main_cube(self) -> Dict[str, Any]:
        """메인 큐브 헬스 체크"""
        try:
            # 3000 포트 응답 확인
            response = requests.get('http://localhost:3000', timeout=5)
            if response.status_code in [200, 404]:
                return {
                    'status': 'healthy',
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'last_check': self.timestamp
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}",
                    'last_check': self.timestamp
                }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'error': str(e),
                'last_check': self.timestamp
            }
    
    def _check_ssl_certificates(self) -> Dict[str, Any]:
        """SSL 인증서 상태 확인"""
        domains = [
            'heal7.com',
            'saju.heal7.com',
            'admin.heal7.com',
            'keywords.heal7.com'
        ]
        
        ssl_status = {}
        for domain in domains:
            try:
                result = subprocess.run(
                    ['openssl', 's_client', '-connect', f'{domain}:443', '-servername', domain],
                    input='',
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if 'Verify return code: 0 (ok)' in result.stdout:
                    ssl_status[domain] = 'valid'
                else:
                    ssl_status[domain] = 'invalid'
            except:
                ssl_status[domain] = 'unreachable'
        
        return ssl_status
    
    def _check_failed_logins(self) -> Dict[str, Any]:
        """실패한 로그인 시도 확인"""
        try:
            result = subprocess.run(
                ['grep', 'Failed password', '/var/log/auth.log'],
                capture_output=True, text=True
            )
            
            failed_attempts = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            return {
                'failed_attempts_today': failed_attempts,
                'status': 'suspicious' if failed_attempts > 10 else 'normal'
            }
        except:
            return {'error': 'Cannot access auth logs'}
    
    def _check_firewall(self) -> Dict[str, Any]:
        """방화벽 상태 확인"""
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            status = 'active' if 'Status: active' in result.stdout else 'inactive'
            
            return {
                'status': status,
                'rules_count': len([line for line in result.stdout.split('\n') if ' ALLOW ' in line])
            }
        except:
            return {'error': 'Cannot check firewall status'}
    
    def _check_ssh_security(self) -> Dict[str, Any]:
        """SSH 보안 설정 확인"""
        try:
            with open('/etc/ssh/sshd_config', 'r') as f:
                config = f.read()
            
            checks = {
                'password_auth_disabled': 'PasswordAuthentication no' in config,
                'root_login_disabled': 'PermitRootLogin no' in config,
                'key_auth_enabled': 'PubkeyAuthentication yes' in config
            }
            
            return checks
        except:
            return {'error': 'Cannot access SSH config'}
    
    def _check_db_backups(self) -> Dict[str, Any]:
        """데이터베이스 백업 상태 확인"""
        backup_dir = Path('/home/ubuntu/backups/database')
        if backup_dir.exists():
            backups = list(backup_dir.glob('*.sql'))
            latest_backup = max(backups, key=os.path.getctime) if backups else None
            
            if latest_backup:
                backup_age_hours = (datetime.now() - datetime.fromtimestamp(latest_backup.stat().st_mtime)).total_seconds() / 3600
                return {
                    'latest_backup': str(latest_backup),
                    'backup_age_hours': round(backup_age_hours, 2),
                    'status': 'fresh' if backup_age_hours < 24 else 'stale'
                }
            else:
                return {'status': 'no_backups_found'}
        else:
            return {'status': 'backup_directory_not_found'}
    
    def _check_git_status(self) -> Dict[str, Any]:
        """Git 저장소 상태 확인"""
        repos = [
            '/home/ubuntu/heal7-system',
            '/home/ubuntu/REFERENCE_LIBRARY'
        ]
        
        git_status = {}
        for repo in repos:
            if Path(repo).exists():
                try:
                    os.chdir(repo)
                    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        uncommitted_changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                        git_status[repo] = {
                            'uncommitted_changes': uncommitted_changes,
                            'status': 'clean' if uncommitted_changes == 0 else 'dirty'
                        }
                    else:
                        git_status[repo] = {'error': 'Not a git repository'}
                except Exception as e:
                    git_status[repo] = {'error': str(e)}
            else:
                git_status[repo] = {'error': 'Repository not found'}
        
        return git_status
    
    def _check_config_backups(self) -> Dict[str, Any]:
        """설정 파일 백업 상태 확인"""
        important_configs = [
            '/etc/nginx/sites-available/',
            '/etc/postgresql/14/main/postgresql.conf',
            '/home/ubuntu/.env.ai'
        ]
        
        config_status = {}
        for config in important_configs:
            config_path = Path(config)
            if config_path.exists():
                config_status[config] = {
                    'exists': True,
                    'last_modified': datetime.fromtimestamp(config_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                config_status[config] = {'exists': False}
        
        return config_status
    
    def generate_recommendations(self) -> List[str]:
        """상태 기반 추천사항 생성"""
        recommendations = []
        
        # 리소스 기반 추천
        if 'infrastructure' in self.report:
            if self.report['infrastructure'].get('cpu_usage', 0) > 80:
                recommendations.append("🔧 CPU 사용률이 높습니다. 프로세스 최적화를 검토하세요.")
            
            if self.report['infrastructure'].get('memory_usage', 0) > 85:
                recommendations.append("💾 메모리 사용률이 높습니다. 메모리 누수를 확인하세요.")
            
            if self.report['infrastructure'].get('disk_usage', 0) > 90:
                recommendations.append("💿 디스크 공간이 부족합니다. 로그 정리를 진행하세요.")
        
        # 큐브 상태 기반 추천
        if 'cube_health' in self.report:
            unhealthy_cubes = [
                cube for cube, status in self.report['cube_health'].items()
                if status.get('status') != 'healthy'
            ]
            if unhealthy_cubes:
                recommendations.append(f"🔴 다음 큐브들의 상태를 확인하세요: {', '.join(unhealthy_cubes)}")
        
        # 보안 기반 추천
        if 'security' in self.report:
            failed_logins = self.report['security'].get('failed_logins', {}).get('failed_attempts_today', 0)
            if failed_logins > 20:
                recommendations.append("🛡️ 비정상적인 로그인 시도가 감지되었습니다. 보안을 강화하세요.")
        
        return recommendations
    
    def determine_overall_status(self) -> str:
        """전체 시스템 상태 결정"""
        critical_issues = 0
        warning_issues = 0
        
        # 인프라 체크
        if 'infrastructure' in self.report:
            infra = self.report['infrastructure']
            if infra.get('cpu_usage', 0) > 90 or infra.get('memory_usage', 0) > 95:
                critical_issues += 1
            elif infra.get('cpu_usage', 0) > 80 or infra.get('memory_usage', 0) > 85:
                warning_issues += 1
        
        # 큐브 상태 체크
        if 'cube_health' in self.report:
            for cube, status in self.report['cube_health'].items():
                if status.get('status') == 'error':
                    critical_issues += 1
                elif status.get('status') == 'unhealthy':
                    warning_issues += 1
        
        if critical_issues > 0:
            return "CRITICAL"
        elif warning_issues > 2:
            return "WARNING"
        elif warning_issues > 0:
            return "HEALTHY_WITH_WARNINGS"
        else:
            return "HEALTHY"
    
    def generate_report(self) -> Dict[str, Any]:
        """전체 헬스 체크 실행 및 리포트 생성"""
        logging.info("시스템 헬스 체크 시작...")
        
        # 각 체크 실행
        self.report['infrastructure'] = self.check_system_resources()
        self.report['services'] = self.check_services_status()
        self.report['cube_health'] = self.check_cube_health()
        self.report['security'] = self.check_security_status()
        self.report['backups'] = self.check_backup_status()
        
        # 추천사항 생성
        self.report['recommendations'] = self.generate_recommendations()
        
        # 전체 상태 결정
        self.report['overall_status'] = self.determine_overall_status()
        
        logging.info(f"헬스 체크 완료. 전체 상태: {self.report['overall_status']}")
        
        return self.report
    
    def save_report(self, report: Dict[str, Any]):
        """리포트를 파일로 저장"""
        report_dir = Path('/home/ubuntu/logs/health-reports')
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"health_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logging.info(f"헬스 리포트 저장됨: {report_file}")
        
        # 최신 리포트 링크 생성
        latest_link = report_dir / "latest.json"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(report_file.name)
    
    def print_summary(self, report: Dict[str, Any]):
        """리포트 요약 출력"""
        status_emoji = {
            'HEALTHY': '✅',
            'HEALTHY_WITH_WARNINGS': '⚠️',
            'WARNING': '🟡',
            'CRITICAL': '🚨'
        }
        
        print(f"\n{'='*60}")
        print(f"🏥 HEAL7 시스템 헬스 체크 리포트")
        print(f"{'='*60}")
        print(f"📅 검사 시간: {report['timestamp']}")
        print(f"📊 전체 상태: {status_emoji.get(report['overall_status'], '❓')} {report['overall_status']}")
        print(f"{'='*60}")
        
        # 인프라 요약
        if 'infrastructure' in report:
            infra = report['infrastructure']
            print(f"🖥️  CPU: {infra.get('cpu_usage', 'N/A')}% | 메모리: {infra.get('memory_usage', 'N/A')}% | 디스크: {infra.get('disk_usage', 'N/A')}%")
        
        # 큐브 상태 요약
        if 'cube_health' in report:
            healthy_cubes = sum(1 for status in report['cube_health'].values() if status.get('status') == 'healthy')
            total_cubes = len(report['cube_health'])
            print(f"🎲 큐브 상태: {healthy_cubes}/{total_cubes} 정상")
        
        # 추천사항
        if report.get('recommendations'):
            print(f"\n📋 추천사항:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print(f"{'='*60}\n")

def main():
    """메인 실행 함수"""
    try:
        checker = HealthChecker()
        report = checker.generate_report()
        checker.save_report(report)
        checker.print_summary(report)
        
        # 크리티컬 상태면 exit code 1 반환
        if report['overall_status'] == 'CRITICAL':
            sys.exit(1)
        
    except Exception as e:
        logging.error(f"헬스 체크 실행 중 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()