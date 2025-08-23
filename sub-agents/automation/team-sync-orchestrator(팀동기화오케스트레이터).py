#!/usr/bin/env python3
"""
🤝 HEAL7 팀 동기화 오케스트레이터
AI 에이전트 팀 간 작업 조율 및 동기화 시스템

Author: AI Agent Team
Created: 2025-08-20
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TeamSyncOrchestrator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sync_results = {
            'timestamp': self.timestamp,
            'sync_status': 'pending',
            'agent_statuses': {},
            'task_assignments': {},
            'coordination_actions': [],
            'recommendations': []
        }
        
        # 에이전트 역할 정의
        self.agent_roles = {
            'orchestrator': {
                'name': '오케스트레이터 마스터',
                'responsibilities': ['품질 관리', '의사결정', '팀 조율'],
                'priority_level': 1,
                'tools': ['daily-health-check.py', 'code-quality-scanner.py']
            },
            'engineer': {
                'name': '엔지니어 마스터', 
                'responsibilities': ['코드 구현', '기술 문제 해결', '성능 최적화'],
                'priority_level': 2,
                'tools': ['code-quality-scanner.py', 'deployment-validator.py']
            },
            'designer': {
                'name': '디자이너 마스터',
                'responsibilities': ['UI/UX 디자인', '사용자 경험', '브랜드 일관성'],
                'priority_level': 3,
                'tools': ['team-sync-orchestrator.py']
            },
            'devops': {
                'name': '데브옵스 마스터',
                'responsibilities': ['인프라 관리', '배포 자동화', '시스템 보안'],
                'priority_level': 2,
                'tools': ['daily-health-check.py', 'deployment-validator.py', 'entropy-detector.py']
            },
            'owner': {
                'name': '오너 마스터',
                'responsibilities': ['전략 수립', '의사결정', '이해관계자 관리'],
                'priority_level': 1,
                'tools': ['team-sync-orchestrator.py']
            },
            'architect': {
                'name': '아키텍트 마스터',
                'responsibilities': ['시스템 설계', '기술 전략', '복잡성 관리'],
                'priority_level': 2,
                'tools': ['code-quality-scanner.py']
            }
        }
        
        # 작업 유형별 우선순위
        self.task_priorities = {
            'critical': {'weight': 10, 'max_duration_hours': 1},
            'high': {'weight': 7, 'max_duration_hours': 4},
            'medium': {'weight': 5, 'max_duration_hours': 8},
            'low': {'weight': 3, 'max_duration_hours': 24}
        }
        
        # 협업 규칙
        self.collaboration_rules = {
            'code_review': ['engineer', 'architect'],
            'ui_design': ['designer', 'engineer'],
            'deployment': ['devops', 'engineer'],
            'architecture_decision': ['architect', 'engineer', 'owner'],
            'emergency_response': ['orchestrator', 'devops', 'owner']
        }
    
    def analyze_current_workload(self) -> Dict[str, Any]:
        """현재 작업 부하 분석"""
        try:
            workload_analysis = {
                'active_tasks': self._scan_active_tasks(),
                'system_health': self._get_system_health_summary(),
                'recent_activities': self._analyze_recent_activities(),
                'resource_utilization': self._check_resource_utilization()
            }
            
            return workload_analysis
            
        except Exception as e:
            logging.error(f"작업 부하 분석 실패: {e}")
            return {'error': str(e)}
    
    def assign_tasks_intelligently(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """지능적 작업 할당"""
        try:
            task_assignments = {}
            
            # 작업을 우선순위별로 정렬
            sorted_tasks = sorted(tasks, key=lambda x: self.task_priorities.get(x.get('priority', 'medium'), {}).get('weight', 5), reverse=True)
            
            for task in sorted_tasks:
                # 작업 유형에 따른 적합한 에이전트 선택
                suitable_agents = self._find_suitable_agents(task)
                
                # 에이전트 가용성 및 부하 상태 확인
                best_agent = self._select_best_agent(suitable_agents, task)
                
                if best_agent:
                    if best_agent not in task_assignments:
                        task_assignments[best_agent] = []
                    
                    task_assignments[best_agent].append({
                        'task_id': task.get('id', f"task_{len(task_assignments) + 1}"),
                        'description': task.get('description', ''),
                        'priority': task.get('priority', 'medium'),
                        'estimated_duration': task.get('estimated_duration', '2h'),
                        'dependencies': task.get('dependencies', []),
                        'assigned_at': self.timestamp
                    })
            
            return task_assignments
            
        except Exception as e:
            logging.error(f"작업 할당 실패: {e}")
            return {'error': str(e)}
    
    def coordinate_team_activities(self) -> Dict[str, Any]:
        """팀 활동 조율"""
        try:
            coordination_actions = []
            
            # 1. 일일 스탠드업 체크
            standups = self._check_daily_standups()
            if standups['needed']:
                coordination_actions.append({
                    'type': 'daily_standup',
                    'action': '일일 스탠드업 미팅 필요',
                    'participants': list(self.agent_roles.keys()),
                    'priority': 'high',
                    'estimated_duration': '15분'
                })
            
            # 2. 코드 리뷰 조율
            code_reviews = self._check_pending_code_reviews()
            for review in code_reviews['pending']:
                coordination_actions.append({
                    'type': 'code_review',
                    'action': f"코드 리뷰 필요: {review['file']}",
                    'participants': ['engineer', 'architect'],
                    'priority': 'medium',
                    'details': review
                })
            
            # 3. 시스템 이슈 조율
            system_issues = self._check_system_issues()
            for issue in system_issues['critical']:
                coordination_actions.append({
                    'type': 'emergency_response',
                    'action': f"긴급 대응 필요: {issue['description']}",
                    'participants': ['orchestrator', 'devops', 'owner'],
                    'priority': 'critical',
                    'details': issue
                })
            
            # 4. 배포 조율
            deployment_status = self._check_deployment_readiness()
            if deployment_status['ready']:
                coordination_actions.append({
                    'type': 'deployment',
                    'action': '배포 준비 완료 - 승인 대기',
                    'participants': ['devops', 'owner'],
                    'priority': 'high',
                    'details': deployment_status
                })
            
            return {
                'coordination_actions': coordination_actions,
                'total_actions': len(coordination_actions),
                'urgent_actions': len([a for a in coordination_actions if a['priority'] == 'critical'])
            }
            
        except Exception as e:
            logging.error(f"팀 활동 조율 실패: {e}")
            return {'error': str(e)}
    
    def generate_team_recommendations(self, workload: Dict[str, Any], assignments: Dict[str, Any]) -> List[str]:
        """팀 추천사항 생성"""
        recommendations = []
        
        # 작업 부하 기반 추천
        if 'system_health' in workload:
            health = workload['system_health']
            if health.get('overall_status') in ['warning', 'critical']:
                recommendations.append("🚨 시스템 상태가 불안정합니다. DevOps와 Engineer의 긴급 대응이 필요합니다")
        
        # 작업 할당 기반 추천
        overloaded_agents = []
        underutilized_agents = []
        
        for agent, tasks in assignments.items():
            task_count = len(tasks)
            if task_count > 3:
                overloaded_agents.append(agent)
            elif task_count == 0:
                underutilized_agents.append(agent)
        
        if overloaded_agents:
            recommendations.append(f"⚖️ 과부하 상태: {', '.join(overloaded_agents)}. 작업 재분배를 고려하세요")
        
        if underutilized_agents:
            recommendations.append(f"💡 여유 리소스: {', '.join(underutilized_agents)}. 추가 작업 할당 가능")
        
        # 협업 패턴 기반 추천
        if 'recent_activities' in workload:
            activities = workload['recent_activities']
            if activities.get('code_changes_without_review', 0) > 5:
                recommendations.append("📝 코드 리뷰가 누락된 변경사항이 많습니다. Engineer-Architect 협업 강화 필요")
        
        # 기본 추천사항
        if not recommendations:
            recommendations.append("✅ 팀 협업이 원활합니다. 현재 패턴을 유지하세요")
        
        return recommendations
    
    def _scan_active_tasks(self) -> Dict[str, Any]:
        """활성 작업 스캔"""
        try:
            # TODO 주석 스캔
            todo_tasks = []
            project_dirs = [
                '/home/ubuntu/heal7-system',
                '/home/ubuntu/REFERENCE_LIBRARY',
                '/home/ubuntu/scripts'
            ]
            
            for project_dir in project_dirs:
                if Path(project_dir).exists():
                    result = subprocess.run(
                        ['grep', '-r', '-n', '-i', 'TODO\\|FIXME\\|HACK', project_dir],
                        capture_output=True, text=True
                    )
                    
                    if result.stdout:
                        lines = result.stdout.strip().split('\n')
                        for line in lines[:10]:  # 최대 10개까지
                            if ':' in line:
                                file_path, content = line.split(':', 2)[:2]
                                todo_tasks.append({
                                    'file': file_path,
                                    'content': content.strip(),
                                    'type': 'todo_comment'
                                })
            
            # Git 브랜치 확인
            git_branches = []
            for repo in ['/home/ubuntu/heal7-system']:
                if Path(repo).exists():
                    os.chdir(repo)
                    result = subprocess.run(['git', 'branch', '-v'], capture_output=True, text=True)
                    if result.stdout:
                        branches = result.stdout.strip().split('\n')
                        for branch in branches:
                            if not branch.strip().startswith('*'):  # 현재 브랜치 제외
                                git_branches.append({
                                    'branch': branch.strip(),
                                    'type': 'feature_branch'
                                })
            
            return {
                'todo_tasks': todo_tasks,
                'git_branches': git_branches,
                'total_active_tasks': len(todo_tasks) + len(git_branches)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_system_health_summary(self) -> Dict[str, Any]:
        """시스템 헬스 요약"""
        try:
            # 최근 헬스 체크 결과 읽기
            health_report_dir = Path('/home/ubuntu/logs/health-reports')
            if health_report_dir.exists():
                latest_report = health_report_dir / 'latest.json'
                if latest_report.exists():
                    with open(latest_report, 'r', encoding='utf-8') as f:
                        health_data = json.load(f)
                    
                    return {
                        'overall_status': health_data.get('overall_status', 'unknown'),
                        'last_check': health_data.get('timestamp', 'unknown'),
                        'critical_issues': len([r for r in health_data.get('recommendations', []) if '🚨' in r]),
                        'cube_health': health_data.get('cube_health', {})
                    }
            
            return {'status': 'no_recent_health_check'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_recent_activities(self) -> Dict[str, Any]:
        """최근 활동 분석"""
        try:
            activities = {
                'git_commits': 0,
                'code_changes_without_review': 0,
                'deployment_attempts': 0,
                'system_alerts': 0
            }
            
            # Git 커밋 분석
            repos = ['/home/ubuntu/heal7-system', '/home/ubuntu/REFERENCE_LIBRARY']
            for repo in repos:
                if Path(repo).exists():
                    os.chdir(repo)
                    
                    # 최근 24시간 커밋
                    result = subprocess.run([
                        'git', 'log', '--since=24 hours ago', '--oneline'
                    ], capture_output=True, text=True)
                    
                    if result.stdout:
                        activities['git_commits'] += len(result.stdout.strip().split('\n'))
            
            # 로그 파일에서 시스템 알림 분석
            log_files = [
                '/home/ubuntu/logs/daily-health-check.log',
                '/home/ubuntu/logs/entropy-reports/',
                '/home/ubuntu/logs/deployment-validation/'
            ]
            
            for log_path in log_files:
                if Path(log_path).exists():
                    if Path(log_path).is_file():
                        # 파일인 경우
                        try:
                            with open(log_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                activities['system_alerts'] += content.count('ERROR') + content.count('WARNING')
                        except:
                            pass
                    else:
                        # 디렉토리인 경우 최근 파일들 확인
                        for file in Path(log_path).glob('*.json'):
                            if (datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)).days < 1:
                                activities['deployment_attempts'] += 1
            
            return activities
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_resource_utilization(self) -> Dict[str, Any]:
        """리소스 활용도 확인"""
        try:
            import psutil
            
            utilization = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'active_processes': len(psutil.pids()),
                'network_connections': len(psutil.net_connections())
            }
            
            # 리소스 상태 평가
            utilization['resource_status'] = 'normal'
            if (utilization['cpu_percent'] > 80 or 
                utilization['memory_percent'] > 85 or 
                utilization['disk_percent'] > 90):
                utilization['resource_status'] = 'high'
            
            return utilization
            
        except Exception as e:
            return {'error': str(e)}
    
    def _find_suitable_agents(self, task: Dict[str, Any]) -> List[str]:
        """작업에 적합한 에이전트 찾기"""
        task_type = task.get('type', 'general')
        task_keywords = task.get('description', '').lower()
        
        suitable_agents = []
        
        # 키워드 기반 매칭
        keyword_mapping = {
            'code': ['engineer', 'architect'],
            'ui': ['designer', 'engineer'],
            'ux': ['designer'],
            'deploy': ['devops', 'engineer'],
            'infrastructure': ['devops'],
            'security': ['devops', 'engineer'],
            'database': ['engineer', 'devops'],
            'performance': ['engineer', 'architect'],
            'design': ['designer'],
            'architecture': ['architect'],
            'strategy': ['owner', 'architect'],
            'decision': ['owner', 'orchestrator'],
            'review': ['orchestrator', 'engineer', 'architect']
        }
        
        for keyword, agents in keyword_mapping.items():
            if keyword in task_keywords:
                suitable_agents.extend(agents)
        
        # 작업 유형별 매핑
        if task_type in self.collaboration_rules:
            suitable_agents.extend(self.collaboration_rules[task_type])
        
        # 중복 제거 및 우선순위 정렬
        suitable_agents = list(set(suitable_agents))
        suitable_agents.sort(key=lambda x: self.agent_roles.get(x, {}).get('priority_level', 5))
        
        return suitable_agents[:3]  # 최대 3개 에이전트
    
    def _select_best_agent(self, suitable_agents: List[str], task: Dict[str, Any]) -> Optional[str]:
        """최적 에이전트 선택"""
        if not suitable_agents:
            return 'orchestrator'  # 기본값
        
        # 현재 작업 부하 고려 (간단한 휴리스틱)
        agent_scores = {}
        
        for agent in suitable_agents:
            score = 100  # 기본 점수
            
            # 우선순위 레벨 보너스
            priority_level = self.agent_roles.get(agent, {}).get('priority_level', 5)
            score += (6 - priority_level) * 10
            
            # 작업 우선순위와 에이전트 매칭
            task_priority = task.get('priority', 'medium')
            if task_priority == 'critical' and priority_level <= 2:
                score += 20
            
            agent_scores[agent] = score
        
        # 가장 높은 점수의 에이전트 선택
        return max(agent_scores.items(), key=lambda x: x[1])[0]
    
    def _check_daily_standups(self) -> Dict[str, Any]:
        """일일 스탠드업 체크"""
        try:
            # 마지막 스탠드업 시간 확인 (간단한 파일 기반)
            standup_file = Path('/home/ubuntu/logs/last_standup.txt')
            
            if standup_file.exists():
                last_standup = datetime.fromtimestamp(standup_file.stat().st_mtime)
                hours_since = (datetime.now() - last_standup).total_seconds() / 3600
                
                return {
                    'needed': hours_since > 24,
                    'last_standup': last_standup.strftime('%Y-%m-%d %H:%M:%S'),
                    'hours_since': round(hours_since, 1)
                }
            else:
                return {
                    'needed': True,
                    'last_standup': 'never',
                    'hours_since': float('inf')
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def _check_pending_code_reviews(self) -> Dict[str, Any]:
        """대기 중인 코드 리뷰 확인"""
        try:
            pending_reviews = []
            
            # Git에서 최근 변경된 파일들 확인
            repos = ['/home/ubuntu/heal7-system']
            for repo in repos:
                if Path(repo).exists():
                    os.chdir(repo)
                    
                    # 최근 커밋된 파일들
                    result = subprocess.run([
                        'git', 'diff', '--name-only', 'HEAD~3..HEAD'
                    ], capture_output=True, text=True)
                    
                    if result.stdout:
                        files = result.stdout.strip().split('\n')
                        for file in files[:5]:  # 최대 5개
                            if file.endswith(('.py', '.js', '.ts', '.tsx')):
                                pending_reviews.append({
                                    'file': file,
                                    'repo': repo,
                                    'type': 'recent_change'
                                })
            
            return {
                'pending': pending_reviews,
                'count': len(pending_reviews)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_system_issues(self) -> Dict[str, Any]:
        """시스템 이슈 확인"""
        try:
            critical_issues = []
            warning_issues = []
            
            # 최근 헬스 체크 결과에서 이슈 추출
            health_report_dir = Path('/home/ubuntu/logs/health-reports')
            if health_report_dir.exists():
                latest_report = health_report_dir / 'latest.json'
                if latest_report.exists():
                    with open(latest_report, 'r', encoding='utf-8') as f:
                        health_data = json.load(f)
                    
                    overall_status = health_data.get('overall_status', 'unknown')
                    if overall_status == 'CRITICAL':
                        critical_issues.append({
                            'type': 'system_critical',
                            'description': '시스템 크리티컬 상태',
                            'source': 'health_check'
                        })
                    elif overall_status in ['WARNING', 'HEALTHY_WITH_WARNINGS']:
                        warning_issues.append({
                            'type': 'system_warning',
                            'description': '시스템 경고 상태',
                            'source': 'health_check'
                        })
            
            # 엔트로피 레벨 확인
            entropy_report_dir = Path('/home/ubuntu/logs/entropy-reports')
            if entropy_report_dir.exists():
                latest_entropy = entropy_report_dir / 'latest.json'
                if latest_entropy.exists():
                    with open(latest_entropy, 'r', encoding='utf-8') as f:
                        entropy_data = json.load(f)
                    
                    entropy_level = entropy_data.get('entropy_level', 'low')
                    if entropy_level == 'critical':
                        critical_issues.append({
                            'type': 'entropy_critical',
                            'description': '시스템 엔트로피 크리티컬',
                            'source': 'entropy_check'
                        })
                    elif entropy_level in ['high', 'medium']:
                        warning_issues.append({
                            'type': 'entropy_warning',
                            'description': f'시스템 엔트로피 {entropy_level}',
                            'source': 'entropy_check'
                        })
            
            return {
                'critical': critical_issues,
                'warning': warning_issues,
                'total_issues': len(critical_issues) + len(warning_issues)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_deployment_readiness(self) -> Dict[str, Any]:
        """배포 준비 상태 확인"""
        try:
            # 최근 배포 검증 결과 확인
            validation_dir = Path('/home/ubuntu/logs/deployment-validation')
            if validation_dir.exists():
                latest_validation = validation_dir / 'latest.json'
                if latest_validation.exists():
                    with open(latest_validation, 'r', encoding='utf-8') as f:
                        validation_data = json.load(f)
                    
                    overall_status = validation_data.get('overall_status', 'unknown')
                    return {
                        'ready': overall_status == 'ready',
                        'status': overall_status,
                        'last_validation': validation_data.get('timestamp', 'unknown')
                    }
            
            return {
                'ready': False,
                'status': 'no_validation',
                'last_validation': 'never'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def create_daily_sync_report(self) -> Dict[str, Any]:
        """일일 동기화 리포트 생성"""
        try:
            # 1. 현재 작업 부하 분석
            workload = self.analyze_current_workload()
            
            # 2. 활성 작업 기반 작업 할당
            active_tasks = workload.get('active_tasks', {})
            tasks_for_assignment = []
            
            # TODO 작업들을 할당 가능한 작업으로 변환
            for todo in active_tasks.get('todo_tasks', [])[:5]:
                tasks_for_assignment.append({
                    'id': f"todo_{len(tasks_for_assignment) + 1}",
                    'description': todo['content'],
                    'type': 'code_improvement',
                    'priority': 'medium',
                    'estimated_duration': '1h'
                })
            
            # 시스템 이슈 기반 긴급 작업
            system_issues = self._check_system_issues()
            for issue in system_issues.get('critical', []):
                tasks_for_assignment.append({
                    'id': f"critical_{len(tasks_for_assignment) + 1}",
                    'description': issue['description'],
                    'type': 'emergency_response',
                    'priority': 'critical',
                    'estimated_duration': '30m'
                })
            
            # 3. 작업 할당
            task_assignments = self.assign_tasks_intelligently(tasks_for_assignment)
            
            # 4. 팀 활동 조율
            coordination = self.coordinate_team_activities()
            
            # 5. 추천사항 생성
            recommendations = self.generate_team_recommendations(workload, task_assignments)
            
            # 6. 최종 리포트 구성
            sync_report = {
                'timestamp': self.timestamp,
                'sync_status': 'completed',
                'workload_analysis': workload,
                'task_assignments': task_assignments,
                'coordination_actions': coordination.get('coordination_actions', []),
                'recommendations': recommendations,
                'summary': {
                    'total_tasks_assigned': sum(len(tasks) for tasks in task_assignments.values()),
                    'agents_with_tasks': len(task_assignments),
                    'coordination_actions_needed': coordination.get('total_actions', 0),
                    'urgent_coordination': coordination.get('urgent_actions', 0)
                }
            }
            
            return sync_report
            
        except Exception as e:
            logging.error(f"일일 동기화 리포트 생성 실패: {e}")
            return {'error': str(e)}
    
    def execute_coordination_actions(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """조율 액션 실행"""
        try:
            executed_actions = []
            failed_actions = []
            
            for action in actions:
                try:
                    action_type = action.get('type')
                    
                    if action_type == 'daily_standup':
                        # 스탠드업 파일 업데이트
                        standup_file = Path('/home/ubuntu/logs/last_standup.txt')
                        standup_file.touch()
                        executed_actions.append(action)
                    
                    elif action_type == 'emergency_response':
                        # 긴급 대응 로그 기록
                        emergency_log = Path('/home/ubuntu/logs/emergency_actions.log')
                        with open(emergency_log, 'a', encoding='utf-8') as f:
                            f.write(f"{self.timestamp}: {action['action']}\n")
                        executed_actions.append(action)
                    
                    elif action_type in ['code_review', 'deployment']:
                        # 알림 로그 기록
                        notification_log = Path('/home/ubuntu/logs/team_notifications.log')
                        with open(notification_log, 'a', encoding='utf-8') as f:
                            f.write(f"{self.timestamp}: {action['action']} (참여자: {', '.join(action.get('participants', []))})\n")
                        executed_actions.append(action)
                    
                except Exception as e:
                    failed_actions.append({
                        'action': action,
                        'error': str(e)
                    })
            
            return {
                'executed': executed_actions,
                'failed': failed_actions,
                'execution_rate': len(executed_actions) / len(actions) if actions else 1.0
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def save_sync_report(self, report: Dict[str, Any]):
        """동기화 리포트 저장"""
        try:
            report_dir = Path('/home/ubuntu/logs/team-sync-reports')
            report_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = report_dir / f"team_sync_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logging.info(f"팀 동기화 리포트 저장됨: {report_file}")
            
            # 최신 리포트 링크 생성
            latest_link = report_dir / "latest.json"
            if latest_link.exists():
                latest_link.unlink()
            latest_link.symlink_to(report_file.name)
            
        except Exception as e:
            logging.error(f"리포트 저장 실패: {e}")
    
    def print_sync_summary(self, report: Dict[str, Any]):
        """동기화 요약 출력"""
        print(f"\n{'='*60}")
        print(f"🤝 HEAL7 팀 동기화 리포트")
        print(f"{'='*60}")
        print(f"📅 동기화 시간: {report['timestamp']}")
        print(f"📊 동기화 상태: ✅ {report.get('sync_status', 'unknown').upper()}")
        print(f"{'='*60}")
        
        # 요약 정보
        summary = report.get('summary', {})
        print(f"📋 할당된 작업: {summary.get('total_tasks_assigned', 0)}개")
        print(f"👥 작업 할당된 에이전트: {summary.get('agents_with_tasks', 0)}명")
        print(f"🔄 조율 액션: {summary.get('coordination_actions_needed', 0)}개")
        
        if summary.get('urgent_coordination', 0) > 0:
            print(f"🚨 긴급 조율: {summary['urgent_coordination']}개")
        
        # 작업 할당 상세
        task_assignments = report.get('task_assignments', {})
        if task_assignments:
            print(f"\n📝 에이전트별 작업 할당:")
            for agent, tasks in task_assignments.items():
                agent_name = self.agent_roles.get(agent, {}).get('name', agent)
                print(f"   🤖 {agent_name}: {len(tasks)}개 작업")
        
        # 조율 액션
        coordination_actions = report.get('coordination_actions', [])
        if coordination_actions:
            print(f"\n🔄 필요한 조율 액션:")
            for i, action in enumerate(coordination_actions[:3], 1):
                priority_emoji = {'critical': '🚨', 'high': '⚠️', 'medium': '📝', 'low': '💡'}.get(action.get('priority', 'medium'), '📝')
                print(f"   {i}. {priority_emoji} {action['action']}")
        
        # 추천사항
        recommendations = report.get('recommendations', [])
        if recommendations:
            print(f"\n📋 추천사항:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        print(f"{'='*60}\n")

def main():
    """메인 실행 함수"""
    try:
        orchestrator = TeamSyncOrchestrator()
        
        # 일일 동기화 리포트 생성
        sync_report = orchestrator.create_daily_sync_report()
        
        # 조율 액션 실행 (있는 경우)
        coordination_actions = sync_report.get('coordination_actions', [])
        if coordination_actions:
            execution_result = orchestrator.execute_coordination_actions(coordination_actions)
            sync_report['execution_result'] = execution_result
        
        # 리포트 저장 및 출력
        orchestrator.save_sync_report(sync_report)
        orchestrator.print_sync_summary(sync_report)
        
        return 0
        
    except Exception as e:
        logging.error(f"팀 동기화 실행 중 오류: {e}")
        return 1

if __name__ == "__main__":
    exit(main())