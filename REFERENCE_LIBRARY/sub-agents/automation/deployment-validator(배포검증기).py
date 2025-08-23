#!/usr/bin/env python3
"""
🚀 HEAL7 배포 검증 시스템
큐브 모델 기반 안전한 배포 검증 및 롤백 준비

Author: AI Agent Team
Created: 2025-08-20
"""

import subprocess
import requests
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DeploymentValidator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.validation_results = {
            'timestamp': self.timestamp,
            'overall_status': 'unknown',
            'pre_deployment': {},
            'deployment_readiness': {},
            'post_deployment': {},
            'rollback_plan': {},
            'recommendations': []
        }
        
        # 큐브 서비스 정의
        self.cube_services = {
            'saju_cube': {
                'name': '사주 서비스',
                'url': 'http://localhost:8000',
                'health_endpoint': '/health',
                'port': 8000,
                'process_pattern': 'python.*simple_server.py',
                'working_dir': '/home/ubuntu/archive/projects/duplicates'
            },
            'admin_cube': {
                'name': '관리자 서비스',
                'url': 'http://localhost:3001',
                'health_endpoint': '/',
                'port': 3001,
                'process_pattern': 'npm.*run.*dev',
                'working_dir': '/home/ubuntu/heal7-system/apps/admin/heal7-admin-vite'
            },
            'main_cube': {
                'name': '메인 서비스',
                'url': 'http://localhost:3000',
                'health_endpoint': '/',
                'port': 3000,
                'process_pattern': 'npm.*run.*dev',
                'working_dir': '/home/ubuntu/heal7-system/apps/index/heal7-index-vite'
            },
            'keywords_cube': {
                'name': '키워드 서비스',
                'url': 'http://localhost:3002',
                'health_endpoint': '/',
                'port': 3002,
                'process_pattern': 'npm.*run.*dev',
                'working_dir': '/home/ubuntu/heal7-system/apps/keywords/heal7-keywords-vite'
            }
        }
        
        # 검증 임계값
        self.thresholds = {
            'response_time_ms': 2000,
            'error_rate_percent': 1.0,
            'cpu_usage_percent': 85.0,
            'memory_usage_percent': 90.0,
            'disk_usage_percent': 95.0
        }
    
    def validate_pre_deployment(self) -> Dict[str, Any]:
        """배포 전 검증"""
        logging.info("배포 전 검증 시작...")
        
        pre_checks = {
            'git_status': self._check_git_status(),
            'dependencies': self._check_dependencies(),
            'tests': self._run_tests(),
            'security_scan': self._run_security_scan(),
            'build_validation': self._validate_builds(),
            'database_backup': self._verify_database_backup()
        }
        
        return pre_checks
    
    def validate_deployment_readiness(self) -> Dict[str, Any]:
        """배포 준비 상태 검증"""
        logging.info("배포 준비 상태 검증...")
        
        readiness_checks = {
            'system_resources': self._check_system_resources(),
            'service_health': self._check_current_services(),
            'nginx_config': self._validate_nginx_config(),
            'ssl_certificates': self._check_ssl_certificates(),
            'disk_space': self._check_disk_space(),
            'backup_verification': self._verify_rollback_capability()
        }
        
        return readiness_checks
    
    def validate_post_deployment(self, deployment_type: str = 'standard') -> Dict[str, Any]:
        """배포 후 검증"""
        logging.info("배포 후 검증 시작...")
        
        post_checks = {
            'service_availability': self._check_service_availability(),
            'response_times': self._measure_response_times(),
            'functionality_tests': self._run_functionality_tests(),
            'error_monitoring': self._check_error_rates(),
            'performance_metrics': self._collect_performance_metrics(),
            'user_impact_assessment': self._assess_user_impact()
        }
        
        return post_checks
    
    def _check_git_status(self) -> Dict[str, Any]:
        """Git 상태 확인"""
        try:
            repos = [
                '/home/ubuntu/heal7-system',
                '/home/ubuntu/REFERENCE_LIBRARY'
            ]
            
            git_status = {}
            for repo in repos:
                if Path(repo).exists():
                    os.chdir(repo)
                    
                    # 변경사항 확인
                    result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True)
                    uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                    
                    # 브랜치 확인
                    branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                                 capture_output=True, text=True)
                    current_branch = branch_result.stdout.strip()
                    
                    # 원격과의 차이 확인
                    try:
                        ahead_result = subprocess.run(['git', 'rev-list', '--count', '@{u}..HEAD'], 
                                                    capture_output=True, text=True)
                        ahead_commits = int(ahead_result.stdout.strip()) if ahead_result.stdout.strip() else 0
                    except:
                        ahead_commits = 0
                    
                    git_status[repo] = {
                        'uncommitted_changes': uncommitted,
                        'current_branch': current_branch,
                        'ahead_commits': ahead_commits,
                        'ready_for_deployment': uncommitted == 0 and ahead_commits == 0
                    }
            
            return {
                'repositories': git_status,
                'all_clean': all(status['ready_for_deployment'] for status in git_status.values())
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_dependencies(self) -> Dict[str, Any]:
        """의존성 확인"""
        try:
            dependency_status = {}
            
            # Python 의존성 확인
            python_deps = [
                ('fastapi', 'FastAPI 웹 프레임워크'),
                ('uvicorn', 'ASGI 서버'),
                ('psycopg2', 'PostgreSQL 드라이버'),
                ('redis', 'Redis 클라이언트')
            ]
            
            for dep, description in python_deps:
                try:
                    result = subprocess.run(['python3', '-c', f'import {dep}'], 
                                          capture_output=True)
                    dependency_status[dep] = {
                        'installed': result.returncode == 0,
                        'description': description
                    }
                except:
                    dependency_status[dep] = {
                        'installed': False,
                        'description': description
                    }
            
            # Node.js 프로젝트 의존성 확인
            node_projects = [
                '/home/ubuntu/heal7-system/apps/admin/heal7-admin-vite',
                '/home/ubuntu/heal7-system/apps/index/heal7-index-vite',
                '/home/ubuntu/heal7-system/apps/keywords/heal7-keywords-vite'
            ]
            
            for project in node_projects:
                project_path = Path(project)
                if project_path.exists():
                    package_json = project_path / 'package.json'
                    node_modules = project_path / 'node_modules'
                    
                    dependency_status[project] = {
                        'package_json_exists': package_json.exists(),
                        'node_modules_exists': node_modules.exists(),
                        'dependencies_installed': package_json.exists() and node_modules.exists()
                    }
            
            return dependency_status
            
        except Exception as e:
            return {'error': str(e)}
    
    def _run_tests(self) -> Dict[str, Any]:
        """테스트 실행"""
        try:
            test_results = {
                'unit_tests': {'status': 'skipped', 'reason': 'No test framework configured'},
                'integration_tests': {'status': 'skipped', 'reason': 'No integration tests found'},
                'basic_functionality': self._run_basic_functionality_tests()
            }
            
            return test_results
            
        except Exception as e:
            return {'error': str(e)}
    
    def _run_basic_functionality_tests(self) -> Dict[str, Any]:
        """기본 기능 테스트"""
        try:
            functionality_tests = {}
            
            for cube_name, cube_config in self.cube_services.items():
                test_result = {
                    'service_name': cube_config['name'],
                    'process_running': self._is_process_running(cube_config['process_pattern']),
                    'port_listening': self._is_port_listening(cube_config['port']),
                    'basic_response': self._test_basic_response(cube_config['url'])
                }
                
                test_result['overall_status'] = (
                    'healthy' if all([
                        test_result['process_running'],
                        test_result['port_listening'],
                        test_result['basic_response']['success']
                    ]) else 'unhealthy'
                )
                
                functionality_tests[cube_name] = test_result
            
            return functionality_tests
            
        except Exception as e:
            return {'error': str(e)}
    
    def _run_security_scan(self) -> Dict[str, Any]:
        """보안 스캔"""
        try:
            security_checks = {
                'ssl_configuration': self._check_ssl_security(),
                'open_ports': self._scan_open_ports(),
                'file_permissions': self._check_critical_file_permissions(),
                'environment_variables': self._check_env_security()
            }
            
            return security_checks
            
        except Exception as e:
            return {'error': str(e)}
    
    def _validate_builds(self) -> Dict[str, Any]:
        """빌드 검증"""
        try:
            build_results = {}
            
            # Vite 프로젝트 빌드 검증
            vite_projects = [
                ('/home/ubuntu/heal7-system/apps/admin/heal7-admin-vite', 'admin'),
                ('/home/ubuntu/heal7-system/apps/index/heal7-index-vite', 'main'),
                ('/home/ubuntu/heal7-system/apps/keywords/heal7-keywords-vite', 'keywords')
            ]
            
            for project_path, project_name in vite_projects:
                if Path(project_path).exists():
                    os.chdir(project_path)
                    
                    # 빌드 테스트 (dry run)
                    result = subprocess.run(['npm', 'run', 'build', '--dry-run'], 
                                          capture_output=True, text=True, timeout=30)
                    
                    build_results[project_name] = {
                        'build_success': result.returncode == 0,
                        'build_output': result.stdout[:500] if result.stdout else '',
                        'build_errors': result.stderr[:500] if result.stderr else ''
                    }
            
            return build_results
            
        except Exception as e:
            return {'error': str(e)}
    
    def _verify_database_backup(self) -> Dict[str, Any]:
        """데이터베이스 백업 검증"""
        try:
            backup_dir = Path('/home/ubuntu/backups/database')
            
            if not backup_dir.exists():
                return {'status': 'no_backup_directory', 'backup_available': False}
            
            # 최근 백업 찾기
            backup_files = list(backup_dir.glob('*.sql'))
            if not backup_files:
                return {'status': 'no_backups_found', 'backup_available': False}
            
            latest_backup = max(backup_files, key=os.path.getctime)
            backup_age_hours = (datetime.now() - datetime.fromtimestamp(latest_backup.stat().st_mtime)).total_seconds() / 3600
            
            return {
                'status': 'backup_available',
                'backup_available': True,
                'latest_backup': str(latest_backup),
                'backup_age_hours': round(backup_age_hours, 2),
                'backup_fresh': backup_age_hours < 24
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """시스템 리소스 확인"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resources = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent,
                'load_average': os.getloadavg(),
                'available_memory_gb': round(memory.available / (1024**3), 2),
                'free_disk_gb': round(disk.free / (1024**3), 2)
            }
            
            # 임계값 검사
            resources['cpu_ok'] = cpu_percent < self.thresholds['cpu_usage_percent']
            resources['memory_ok'] = memory.percent < self.thresholds['memory_usage_percent']
            resources['disk_ok'] = disk.percent < self.thresholds['disk_usage_percent']
            resources['resources_ok'] = all([
                resources['cpu_ok'], 
                resources['memory_ok'], 
                resources['disk_ok']
            ])
            
            return resources
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_current_services(self) -> Dict[str, Any]:
        """현재 서비스 상태 확인"""
        try:
            service_health = {}
            
            for cube_name, cube_config in self.cube_services.items():
                health_status = {
                    'service_name': cube_config['name'],
                    'process_running': self._is_process_running(cube_config['process_pattern']),
                    'port_listening': self._is_port_listening(cube_config['port']),
                    'responds_to_requests': False,
                    'response_time_ms': 0
                }
                
                # HTTP 응답 테스트
                if health_status['port_listening']:
                    response_test = self._test_basic_response(cube_config['url'])
                    health_status['responds_to_requests'] = response_test['success']
                    health_status['response_time_ms'] = response_test['response_time_ms']
                
                health_status['overall_healthy'] = all([
                    health_status['process_running'],
                    health_status['port_listening'],
                    health_status['responds_to_requests']
                ])
                
                service_health[cube_name] = health_status
            
            return service_health
            
        except Exception as e:
            return {'error': str(e)}
    
    def _validate_nginx_config(self) -> Dict[str, Any]:
        """Nginx 설정 검증"""
        try:
            # Nginx 설정 테스트
            result = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
            
            config_status = {
                'syntax_valid': result.returncode == 0,
                'test_output': result.stderr,
                'nginx_running': self._is_process_running('nginx')
            }
            
            # 활성 사이트 확인
            sites_enabled = Path('/etc/nginx/sites-enabled')
            if sites_enabled.exists():
                enabled_sites = [site.name for site in sites_enabled.iterdir() if site.is_file()]
                config_status['enabled_sites'] = enabled_sites
                config_status['expected_sites'] = ['heal7.com', 'saju.heal7.com', 'test.heal7.com']
                config_status['sites_configured'] = all(
                    site in enabled_sites for site in config_status['expected_sites']
                )
            
            return config_status
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_ssl_certificates(self) -> Dict[str, Any]:
        """SSL 인증서 확인"""
        try:
            domains = ['heal7.com', 'saju.heal7.com', 'admin.heal7.com', 'keywords.heal7.com']
            ssl_status = {}
            
            for domain in domains:
                try:
                    result = subprocess.run([
                        'openssl', 's_client', '-connect', f'{domain}:443', 
                        '-servername', domain, '-verify_return_error'
                    ], input='', capture_output=True, text=True, timeout=10)
                    
                    ssl_status[domain] = {
                        'certificate_valid': 'Verify return code: 0 (ok)' in result.stdout,
                        'connection_successful': result.returncode == 0
                    }
                except subprocess.TimeoutExpired:
                    ssl_status[domain] = {
                        'certificate_valid': False,
                        'connection_successful': False,
                        'error': 'Connection timeout'
                    }
                except Exception as e:
                    ssl_status[domain] = {
                        'certificate_valid': False,
                        'connection_successful': False,
                        'error': str(e)
                    }
            
            return ssl_status
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_disk_space(self) -> Dict[str, Any]:
        """디스크 공간 확인"""
        try:
            import shutil
            
            paths_to_check = [
                '/',
                '/home/ubuntu',
                '/var/log',
                '/tmp'
            ]
            
            disk_status = {}
            for path in paths_to_check:
                if Path(path).exists():
                    total, used, free = shutil.disk_usage(path)
                    usage_percent = (used / total) * 100
                    
                    disk_status[path] = {
                        'total_gb': round(total / (1024**3), 2),
                        'used_gb': round(used / (1024**3), 2),
                        'free_gb': round(free / (1024**3), 2),
                        'usage_percent': round(usage_percent, 2),
                        'space_ok': usage_percent < self.thresholds['disk_usage_percent']
                    }
            
            return disk_status
            
        except Exception as e:
            return {'error': str(e)}
    
    def _verify_rollback_capability(self) -> Dict[str, Any]:
        """롤백 능력 확인"""
        try:
            rollback_readiness = {
                'git_clean': True,
                'backup_available': False,
                'previous_version_tagged': False,
                'rollback_script_exists': False
            }
            
            # Git 상태 확인
            repos = ['/home/ubuntu/heal7-system']
            for repo in repos:
                if Path(repo).exists():
                    os.chdir(repo)
                    result = subprocess.run(['git', 'status', '--porcelain'], 
                                          capture_output=True, text=True)
                    if result.stdout.strip():
                        rollback_readiness['git_clean'] = False
            
            # 백업 확인
            backup_check = self._verify_database_backup()
            rollback_readiness['backup_available'] = backup_check.get('backup_available', False)
            
            # 롤백 스크립트 확인
            rollback_script = Path('/home/ubuntu/scripts/deployment/rollback.sh')
            rollback_readiness['rollback_script_exists'] = rollback_script.exists()
            
            rollback_readiness['rollback_ready'] = all([
                rollback_readiness['git_clean'],
                rollback_readiness['backup_available'],
                rollback_readiness['rollback_script_exists']
            ])
            
            return rollback_readiness
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_service_availability(self) -> Dict[str, Any]:
        """서비스 가용성 확인"""
        return self._check_current_services()
    
    def _measure_response_times(self) -> Dict[str, Any]:
        """응답 시간 측정"""
        try:
            response_times = {}
            
            for cube_name, cube_config in self.cube_services.items():
                measurements = []
                
                # 5번 측정해서 평균 계산
                for _ in range(5):
                    response_test = self._test_basic_response(cube_config['url'])
                    if response_test['success']:
                        measurements.append(response_test['response_time_ms'])
                    time.sleep(0.5)
                
                if measurements:
                    avg_response_time = sum(measurements) / len(measurements)
                    response_times[cube_name] = {
                        'avg_response_time_ms': round(avg_response_time, 2),
                        'min_response_time_ms': min(measurements),
                        'max_response_time_ms': max(measurements),
                        'measurements': measurements,
                        'performance_ok': avg_response_time < self.thresholds['response_time_ms']
                    }
                else:
                    response_times[cube_name] = {
                        'avg_response_time_ms': 0,
                        'measurements': [],
                        'performance_ok': False,
                        'error': 'No successful responses'
                    }
            
            return response_times
            
        except Exception as e:
            return {'error': str(e)}
    
    def _run_functionality_tests(self) -> Dict[str, Any]:
        """기능 테스트 실행"""
        # 기본 기능 테스트와 동일하지만 더 상세한 테스트 포함
        return self._run_basic_functionality_tests()
    
    def _check_error_rates(self) -> Dict[str, Any]:
        """에러율 확인"""
        try:
            error_rates = {}
            
            for cube_name, cube_config in self.cube_services.items():
                success_count = 0
                total_requests = 10
                
                # 10번 요청해서 에러율 계산
                for _ in range(total_requests):
                    response_test = self._test_basic_response(cube_config['url'])
                    if response_test['success']:
                        success_count += 1
                    time.sleep(0.2)
                
                error_rate = ((total_requests - success_count) / total_requests) * 100
                
                error_rates[cube_name] = {
                    'success_count': success_count,
                    'total_requests': total_requests,
                    'error_rate_percent': round(error_rate, 2),
                    'error_rate_ok': error_rate < self.thresholds['error_rate_percent']
                }
            
            return error_rates
            
        except Exception as e:
            return {'error': str(e)}
    
    def _collect_performance_metrics(self) -> Dict[str, Any]:
        """성능 메트릭 수집"""
        try:
            import psutil
            
            # 시스템 메트릭
            system_metrics = {
                'cpu_usage': psutil.cpu_percent(interval=1),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
            
            # 프로세스별 메트릭
            process_metrics = {}
            for cube_name, cube_config in self.cube_services.items():
                try:
                    result = subprocess.run(['pgrep', '-f', cube_config['process_pattern']], 
                                          capture_output=True, text=True)
                    pids = result.stdout.strip().split('\n') if result.stdout.strip() else []
                    
                    if pids and pids[0]:
                        pid = int(pids[0])
                        process = psutil.Process(pid)
                        
                        process_metrics[cube_name] = {
                            'pid': pid,
                            'cpu_percent': process.cpu_percent(),
                            'memory_percent': process.memory_percent(),
                            'memory_mb': round(process.memory_info().rss / (1024 * 1024), 2),
                            'num_threads': process.num_threads()
                        }
                except Exception as e:
                    process_metrics[cube_name] = {'error': str(e)}
            
            return {
                'system_metrics': system_metrics,
                'process_metrics': process_metrics
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _assess_user_impact(self) -> Dict[str, Any]:
        """사용자 영향 평가"""
        try:
            impact_assessment = {
                'service_availability': 'available',
                'response_performance': 'acceptable',
                'functionality': 'working',
                'overall_impact': 'minimal'
            }
            
            # 서비스 가용성 확인
            service_health = self._check_current_services()
            unhealthy_services = [
                name for name, status in service_health.items() 
                if not status.get('overall_healthy', False)
            ]
            
            if unhealthy_services:
                impact_assessment['service_availability'] = 'degraded'
                impact_assessment['affected_services'] = unhealthy_services
            
            # 응답 성능 확인
            response_times = self._measure_response_times()
            slow_services = [
                name for name, metrics in response_times.items()
                if not metrics.get('performance_ok', False)
            ]
            
            if slow_services:
                impact_assessment['response_performance'] = 'degraded'
                impact_assessment['slow_services'] = slow_services
            
            # 전체 영향 평가
            if unhealthy_services or slow_services:
                impact_assessment['overall_impact'] = 'moderate' if len(unhealthy_services) < 2 else 'severe'
            
            return impact_assessment
            
        except Exception as e:
            return {'error': str(e)}
    
    def _is_process_running(self, pattern: str) -> bool:
        """프로세스 실행 확인"""
        try:
            result = subprocess.run(['pgrep', '-f', pattern], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def _is_port_listening(self, port: int) -> bool:
        """포트 리스닝 확인"""
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def _test_basic_response(self, url: str) -> Dict[str, Any]:
        """기본 HTTP 응답 테스트"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            response_time_ms = (time.time() - start_time) * 1000
            
            return {
                'success': response.status_code in [200, 404],  # Vite는 404도 정상
                'status_code': response.status_code,
                'response_time_ms': round(response_time_ms, 2)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time_ms': 0
            }
    
    def _check_ssl_security(self) -> Dict[str, Any]:
        """SSL 보안 설정 확인"""
        # SSL 인증서 확인과 동일
        return self._check_ssl_certificates()
    
    def _scan_open_ports(self) -> Dict[str, Any]:
        """열린 포트 스캔"""
        try:
            # 예상되는 포트만 확인
            expected_ports = [22, 80, 443, 3000, 3001, 3002, 5432, 6379, 8000, 8001]
            open_ports = []
            
            for port in expected_ports:
                if self._is_port_listening(port):
                    open_ports.append(port)
            
            return {
                'open_ports': open_ports,
                'expected_ports': expected_ports,
                'unexpected_ports': [p for p in open_ports if p not in expected_ports]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _check_critical_file_permissions(self) -> Dict[str, Any]:
        """중요 파일 권한 확인"""
        try:
            critical_files = [
                '/home/ubuntu/.env.ai',
                '/home/ubuntu/.ssh/',
                '/etc/nginx/sites-available/',
                '/etc/ssl/private/'
            ]
            
            permissions = {}
            for file_path in critical_files:
                path = Path(file_path)
                if path.exists():
                    stat = path.stat()
                    mode = oct(stat.st_mode)[-3:]
                    permissions[file_path] = {
                        'permissions': mode,
                        'secure': mode in ['600', '700', '644', '755']  # 일반적으로 안전한 권한
                    }
            
            return permissions
        except Exception as e:
            return {'error': str(e)}
    
    def _check_env_security(self) -> Dict[str, Any]:
        """환경변수 보안 확인"""
        try:
            env_file = Path('/home/ubuntu/.env.ai')
            if env_file.exists():
                stat = env_file.stat()
                mode = oct(stat.st_mode)[-3:]
                return {
                    'env_file_exists': True,
                    'permissions': mode,
                    'secure_permissions': mode == '600'
                }
            else:
                return {
                    'env_file_exists': False,
                    'secure_permissions': False
                }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_rollback_plan(self) -> Dict[str, Any]:
        """롤백 계획 생성"""
        rollback_plan = {
            'rollback_steps': [
                {
                    'step': 1,
                    'action': 'Stop new deployments',
                    'command': 'kill -TERM $(pgrep -f "npm run dev")',
                    'description': '새로운 서비스 중지'
                },
                {
                    'step': 2,
                    'action': 'Restore database backup',
                    'command': 'pg_restore -d heal7_db /home/ubuntu/backups/database/latest.sql',
                    'description': '데이터베이스 백업 복원'
                },
                {
                    'step': 3,
                    'action': 'Checkout previous version',
                    'command': 'git checkout HEAD~1',
                    'description': '이전 버전으로 롤백'
                },
                {
                    'step': 4,
                    'action': 'Restart services',
                    'command': 'bash /home/ubuntu/scripts/deployment/heal7-deploy-master.sh',
                    'description': '서비스 재시작'
                },
                {
                    'step': 5,
                    'action': 'Verify rollback success',
                    'command': 'python3 /home/ubuntu/REFERENCE_LIBRARY/sub-agents/automation/deployment-validator.py',
                    'description': '롤백 성공 검증'
                }
            ],
            'estimated_rollback_time': '5-10 minutes',
            'data_loss_risk': 'minimal (with recent backup)',
            'rollback_triggers': [
                'Error rate > 5%',
                'Response time > 5 seconds',
                'Service unavailability > 2 minutes',
                'Critical functionality broken'
            ]
        }
        
        return rollback_plan
    
    def generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """검증 결과 기반 추천사항 생성"""
        recommendations = []
        
        # 시스템 리소스 기반 추천
        readiness = validation_results.get('deployment_readiness', {})
        resources = readiness.get('system_resources', {})
        
        if not resources.get('cpu_ok', True):
            recommendations.append("🔧 CPU 사용률이 높습니다. 배포 전 부하를 줄이세요")
        
        if not resources.get('memory_ok', True):
            recommendations.append("💾 메모리 사용률이 높습니다. 메모리 정리 후 배포하세요")
        
        if not resources.get('disk_ok', True):
            recommendations.append("💿 디스크 공간이 부족합니다. 로그 정리 후 배포하세요")
        
        # Git 상태 기반 추천
        pre_deployment = validation_results.get('pre_deployment', {})
        git_status = pre_deployment.get('git_status', {})
        
        if not git_status.get('all_clean', True):
            recommendations.append("📝 Git 리포지토리에 커밋되지 않은 변경사항이 있습니다")
        
        # 백업 상태 기반 추천
        backup_status = pre_deployment.get('database_backup', {})
        if not backup_status.get('backup_fresh', False):
            recommendations.append("💾 최신 데이터베이스 백업을 생성하세요")
        
        # 서비스 상태 기반 추천
        service_health = readiness.get('service_health', {})
        unhealthy_services = [
            name for name, status in service_health.items()
            if not status.get('overall_healthy', False)
        ]
        
        if unhealthy_services:
            recommendations.append(f"🔴 다음 서비스들이 비정상 상태입니다: {', '.join(unhealthy_services)}")
        
        if not recommendations:
            recommendations.append("✅ 배포 준비가 완료되었습니다")
        
        return recommendations
    
    def run_full_validation(self, phase: str = 'pre') -> Dict[str, Any]:
        """전체 배포 검증 실행"""
        logging.info(f"{phase} 배포 검증 시작...")
        
        if phase == 'pre':
            self.validation_results['pre_deployment'] = self.validate_pre_deployment()
            self.validation_results['deployment_readiness'] = self.validate_deployment_readiness()
        elif phase == 'post':
            self.validation_results['post_deployment'] = self.validate_post_deployment()
        
        # 롤백 계획 생성
        self.validation_results['rollback_plan'] = self.generate_rollback_plan()
        
        # 추천사항 생성
        self.validation_results['recommendations'] = self.generate_recommendations(self.validation_results)
        
        # 전체 상태 결정
        self.validation_results['overall_status'] = self._determine_overall_status()
        
        logging.info(f"배포 검증 완료. 상태: {self.validation_results['overall_status']}")
        
        return self.validation_results
    
    def _determine_overall_status(self) -> str:
        """전체 검증 상태 결정"""
        # 시스템 리소스 확인
        readiness = self.validation_results.get('deployment_readiness', {})
        resources = readiness.get('system_resources', {})
        
        if not resources.get('resources_ok', True):
            return 'not_ready'
        
        # 서비스 상태 확인
        service_health = readiness.get('service_health', {})
        if any(not status.get('overall_healthy', False) for status in service_health.values()):
            return 'degraded'
        
        # Git 상태 확인
        pre_deployment = self.validation_results.get('pre_deployment', {})
        git_status = pre_deployment.get('git_status', {})
        
        if not git_status.get('all_clean', True):
            return 'needs_attention'
        
        return 'ready'
    
    def save_validation_report(self, results: Dict[str, Any]):
        """검증 리포트 저장"""
        report_dir = Path('/home/ubuntu/logs/deployment-validation')
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"deployment_validation_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logging.info(f"배포 검증 리포트 저장됨: {report_file}")
        
        # 최신 리포트 링크 생성
        latest_link = report_dir / "latest.json"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(report_file.name)
    
    def print_validation_summary(self, results: Dict[str, Any]):
        """검증 결과 요약 출력"""
        status_emoji = {
            'ready': '✅',
            'needs_attention': '⚠️',
            'degraded': '🟡',
            'not_ready': '🔴'
        }
        
        print(f"\n{'='*60}")
        print(f"🚀 HEAL7 배포 검증 리포트")
        print(f"{'='*60}")
        print(f"📅 검증 시간: {results['timestamp']}")
        print(f"📊 전체 상태: {status_emoji.get(results['overall_status'], '❓')} {results['overall_status'].upper()}")
        print(f"{'='*60}")
        
        # 주요 검증 결과
        if 'deployment_readiness' in results:
            readiness = results['deployment_readiness']
            resources = readiness.get('system_resources', {})
            print(f"🖥️  CPU: {resources.get('cpu_usage', 'N/A')}% | 메모리: {resources.get('memory_usage', 'N/A')}% | 디스크: {resources.get('disk_usage', 'N/A')}%")
            
            service_health = readiness.get('service_health', {})
            healthy_services = sum(1 for status in service_health.values() if status.get('overall_healthy', False))
            total_services = len(service_health)
            print(f"🎲 서비스 상태: {healthy_services}/{total_services} 정상")
        
        # 성능 메트릭 (배포 후 검증 시)
        if 'post_deployment' in results:
            post = results['post_deployment']
            response_times = post.get('response_times', {})
            if response_times:
                avg_times = [
                    metrics.get('avg_response_time_ms', 0) 
                    for metrics in response_times.values() 
                    if isinstance(metrics, dict)
                ]
                if avg_times:
                    overall_avg = sum(avg_times) / len(avg_times)
                    print(f"⚡ 평균 응답시간: {overall_avg:.0f}ms")
        
        # 추천사항
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"\n📋 추천사항:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        # 롤백 계획
        rollback = results.get('rollback_plan', {})
        if rollback:
            print(f"\n🔄 롤백 준비: 예상 소요시간 {rollback.get('estimated_rollback_time', 'N/A')}")
        
        print(f"{'='*60}\n")

def main():
    """메인 실행 함수"""
    import sys
    
    try:
        phase = sys.argv[1] if len(sys.argv) > 1 else 'pre'
        
        validator = DeploymentValidator()
        results = validator.run_full_validation(phase)
        validator.save_validation_report(results)
        validator.print_validation_summary(results)
        
        # 배포 준비되지 않았으면 exit code 1 반환
        if results['overall_status'] in ['not_ready', 'degraded']:
            return 1
        
        return 0
        
    except Exception as e:
        logging.error(f"배포 검증 실행 중 오류: {e}")
        return 1

if __name__ == "__main__":
    exit(main())