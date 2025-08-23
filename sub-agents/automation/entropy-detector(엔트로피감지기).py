#!/usr/bin/env python3
"""
🌪️ HEAL7 엔트로피 감지 및 정리 시스템
시스템 복잡도 모니터링 및 자동 정리 스크립트

Author: AI Agent Team
Created: 2025-08-20
"""

import os
import shutil
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import logging
import hashlib

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EntropyDetector:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entropy_report = {
            'timestamp': self.timestamp,
            'entropy_level': 'low',
            'issues_found': [],
            'cleanup_actions': [],
            'recommendations': []
        }
        
        # 허용된 파일/폴더 (화이트리스트)
        self.whitelist_files = {
            '/home/ubuntu/CLAUDE.md',
            '/home/ubuntu/.env.ai',
            '/home/ubuntu/.bashrc',
            '/home/ubuntu/.bash_history',
            '/home/ubuntu/.gitconfig',
            '/home/ubuntu/.ssh/',
            '/home/ubuntu/.local/',
            '/home/ubuntu/.cache/',
            '/home/ubuntu/snap/'
        }
        
        self.whitelist_patterns = [
            r'.*\.pem$',           # SSH 키
            r'.*\.key$',           # 키 파일
            r'.*\.crt$',           # 인증서
            r'.*\.log$',           # 로그 파일 (logs/ 폴더 외부)
        ]
        
        # 정리 대상 디렉토리
        self.scan_directories = [
            '/home/ubuntu/',
            '/tmp/',
            '/var/tmp/'
        ]
        
        # 엔트로피 임계값
        self.thresholds = {
            'max_top_level_files': 3,       # 최상위 폴더 파일 수
            'max_top_level_folders': 1,     # 최상위 폴더 비허가 폴더 수
            'max_temp_file_age_days': 7,    # 임시 파일 최대 보관 일수
            'max_duplicate_files': 10,      # 중복 파일 수
            'max_orphaned_configs': 5       # 고아 설정 파일 수
        }
    
    def scan_top_level_entropy(self) -> Dict[str, Any]:
        """최상위 디렉토리 엔트로피 스캔"""
        home_dir = Path('/home/ubuntu')
        
        # 허가되지 않은 파일들
        unauthorized_files = []
        unauthorized_dirs = []
        
        for item in home_dir.iterdir():
            item_path = str(item)
            
            # 화이트리스트 체크
            if item_path in self.whitelist_files:
                continue
            
            # 패턴 체크
            if any(re.match(pattern, item_path) for pattern in self.whitelist_patterns):
                continue
            
            # 허가된 프로젝트 폴더들
            allowed_dirs = {
                'heal7-system', 'REFERENCE_LIBRARY', 'docs', 'scripts', 
                'logs', 'backups', 'database', 'archive', '.heal7-session'
            }
            
            if item.is_file():
                unauthorized_files.append({
                    'path': item_path,
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'file'
                })
            elif item.is_dir() and item.name not in allowed_dirs:
                unauthorized_dirs.append({
                    'path': item_path,
                    'item_count': len(list(item.rglob('*'))),
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'directory'
                })
        
        return {
            'unauthorized_files': unauthorized_files,
            'unauthorized_dirs': unauthorized_dirs,
            'file_count': len(unauthorized_files),
            'dir_count': len(unauthorized_dirs)
        }
    
    def scan_temp_files(self) -> Dict[str, Any]:
        """임시 파일 스캔"""
        temp_patterns = [
            '*.tmp', '*.temp', '*.bak', '*.backup', '*.old',
            '*.swp', '*.swo', '*~', '.DS_Store', 'Thumbs.db'
        ]
        
        temp_files = []
        cutoff_date = datetime.now() - timedelta(days=self.thresholds['max_temp_file_age_days'])
        
        for scan_dir in ['/home/ubuntu', '/tmp', '/var/tmp']:
            scan_path = Path(scan_dir)
            if not scan_path.exists():
                continue
                
            for pattern in temp_patterns:
                for temp_file in scan_path.rglob(pattern):
                    if temp_file.is_file():
                        modified_time = datetime.fromtimestamp(temp_file.stat().st_mtime)
                        if modified_time < cutoff_date:
                            temp_files.append({
                                'path': str(temp_file),
                                'size': temp_file.stat().st_size,
                                'age_days': (datetime.now() - modified_time).days,
                                'pattern': pattern
                            })
        
        return {
            'temp_files': temp_files,
            'total_count': len(temp_files),
            'total_size_mb': sum(f['size'] for f in temp_files) / (1024 * 1024)
        }
    
    def scan_duplicate_files(self) -> Dict[str, Any]:
        """중복 파일 스캔 (해시 기반)"""
        file_hashes = {}
        duplicates = []
        
        # 스캔할 디렉토리 (node_modules 제외)
        scan_dirs = [
            '/home/ubuntu/heal7-system',
            '/home/ubuntu/REFERENCE_LIBRARY',
            '/home/ubuntu/scripts'
        ]
        
        for scan_dir in scan_dirs:
            scan_path = Path(scan_dir)
            if not scan_path.exists():
                continue
            
            for file_path in scan_path.rglob('*'):
                if (file_path.is_file() and 
                    'node_modules' not in str(file_path) and 
                    '.git' not in str(file_path) and
                    file_path.stat().st_size > 1024):  # 1KB 이상 파일만
                    
                    try:
                        # 파일 해시 계산
                        hasher = hashlib.md5()
                        with open(file_path, 'rb') as f:
                            hasher.update(f.read())
                        file_hash = hasher.hexdigest()
                        
                        if file_hash in file_hashes:
                            # 중복 발견
                            duplicates.append({
                                'hash': file_hash,
                                'files': [file_hashes[file_hash], str(file_path)],
                                'size': file_path.stat().st_size
                            })
                        else:
                            file_hashes[file_hash] = str(file_path)
                            
                    except Exception as e:
                        logging.warning(f"파일 해시 계산 실패 {file_path}: {e}")
        
        return {
            'duplicates': duplicates,
            'duplicate_count': len(duplicates),
            'wasted_space_mb': sum(d['size'] for d in duplicates) / (1024 * 1024)
        }
    
    def scan_orphaned_configs(self) -> Dict[str, Any]:
        """고아 설정 파일 스캔"""
        config_patterns = [
            '*.conf', '*.config', '*.cfg', '*.ini',
            '.env.*', '*.yaml', '*.yml', '*.json'
        ]
        
        orphaned_configs = []
        
        # 프로젝트 루트가 아닌 위치의 설정 파일들
        scan_dirs = ['/home/ubuntu']
        
        for scan_dir in scan_dirs:
            scan_path = Path(scan_dir)
            
            for pattern in config_patterns:
                for config_file in scan_path.glob(pattern):  # 하위 디렉토리 제외, 최상위만
                    if config_file.is_file():
                        # 알려진 설정 파일 제외
                        known_configs = {'.env.ai', 'CLAUDE.md'}
                        if config_file.name not in known_configs:
                            orphaned_configs.append({
                                'path': str(config_file),
                                'size': config_file.stat().st_size,
                                'modified': datetime.fromtimestamp(config_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                            })
        
        return {
            'orphaned_configs': orphaned_configs,
            'count': len(orphaned_configs)
        }
    
    def scan_log_accumulation(self) -> Dict[str, Any]:
        """로그 파일 누적 스캔"""
        log_dirs = [
            '/home/ubuntu/logs',
            '/var/log',
            '/tmp'
        ]
        
        large_logs = []
        old_logs = []
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for log_dir in log_dirs:
            log_path = Path(log_dir)
            if not log_path.exists():
                continue
            
            for log_file in log_path.rglob('*.log'):
                if log_file.is_file():
                    file_size = log_file.stat().st_size
                    modified_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    
                    # 큰 로그 파일 (10MB 이상)
                    if file_size > 10 * 1024 * 1024:
                        large_logs.append({
                            'path': str(log_file),
                            'size_mb': file_size / (1024 * 1024),
                            'modified': modified_time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    
                    # 오래된 로그 파일
                    if modified_time < cutoff_date:
                        old_logs.append({
                            'path': str(log_file),
                            'age_days': (datetime.now() - modified_time).days,
                            'size_mb': file_size / (1024 * 1024)
                        })
        
        return {
            'large_logs': large_logs,
            'old_logs': old_logs,
            'large_count': len(large_logs),
            'old_count': len(old_logs)
        }
    
    def scan_broken_symlinks(self) -> Dict[str, Any]:
        """깨진 심볼릭 링크 스캔"""
        broken_links = []
        
        for scan_dir in ['/home/ubuntu']:
            scan_path = Path(scan_dir)
            
            for item in scan_path.rglob('*'):
                if item.is_symlink() and not item.exists():
                    broken_links.append({
                        'path': str(item),
                        'target': str(item.readlink()) if item.readlink() else 'unknown'
                    })
        
        return {
            'broken_links': broken_links,
            'count': len(broken_links)
        }
    
    def calculate_entropy_level(self, scan_results: Dict[str, Any]) -> str:
        """엔트로피 레벨 계산"""
        entropy_score = 0
        
        # 최상위 파일/폴더 수
        top_level = scan_results.get('top_level', {})
        if top_level.get('file_count', 0) > self.thresholds['max_top_level_files']:
            entropy_score += 3
        if top_level.get('dir_count', 0) > self.thresholds['max_top_level_folders']:
            entropy_score += 5
        
        # 임시 파일 수
        temp_files = scan_results.get('temp_files', {})
        if temp_files.get('total_count', 0) > 20:
            entropy_score += 2
        
        # 중복 파일
        duplicates = scan_results.get('duplicates', {})
        if duplicates.get('duplicate_count', 0) > self.thresholds['max_duplicate_files']:
            entropy_score += 2
        
        # 고아 설정 파일
        orphaned = scan_results.get('orphaned_configs', {})
        if orphaned.get('count', 0) > self.thresholds['max_orphaned_configs']:
            entropy_score += 2
        
        # 로그 누적
        logs = scan_results.get('log_accumulation', {})
        if logs.get('large_count', 0) > 5 or logs.get('old_count', 0) > 10:
            entropy_score += 1
        
        # 깨진 링크
        broken = scan_results.get('broken_symlinks', {})
        if broken.get('count', 0) > 0:
            entropy_score += 1
        
        # 엔트로피 레벨 결정
        if entropy_score >= 10:
            return 'critical'
        elif entropy_score >= 7:
            return 'high'
        elif entropy_score >= 4:
            return 'medium'
        else:
            return 'low'
    
    def generate_cleanup_plan(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """정리 계획 생성"""
        cleanup_actions = []
        
        # 임시 파일 정리
        temp_files = scan_results.get('temp_files', {})
        if temp_files.get('total_count', 0) > 0:
            cleanup_actions.append({
                'type': 'temp_files_cleanup',
                'description': f"{temp_files['total_count']}개의 오래된 임시 파일 삭제",
                'files': temp_files.get('temp_files', []),
                'priority': 'medium',
                'safe': True
            })
        
        # 중복 파일 정리 (수동 확인 필요)
        duplicates = scan_results.get('duplicates', {})
        if duplicates.get('duplicate_count', 0) > 0:
            cleanup_actions.append({
                'type': 'duplicate_files_review',
                'description': f"{duplicates['duplicate_count']}개의 중복 파일 검토 필요",
                'files': duplicates.get('duplicates', []),
                'priority': 'low',
                'safe': False  # 수동 검토 필요
            })
        
        # 고아 설정 파일 정리
        orphaned = scan_results.get('orphaned_configs', {})
        if orphaned.get('count', 0) > 0:
            cleanup_actions.append({
                'type': 'orphaned_configs_review',
                'description': f"{orphaned['count']}개의 고아 설정 파일 검토",
                'files': orphaned.get('orphaned_configs', []),
                'priority': 'medium',
                'safe': False  # 수동 검토 필요
            })
        
        # 큰 로그 파일 압축
        logs = scan_results.get('log_accumulation', {})
        if logs.get('large_count', 0) > 0:
            cleanup_actions.append({
                'type': 'log_compression',
                'description': f"{logs['large_count']}개의 큰 로그 파일 압축",
                'files': logs.get('large_logs', []),
                'priority': 'low',
                'safe': True
            })
        
        # 깨진 심볼릭 링크 정리
        broken = scan_results.get('broken_symlinks', {})
        if broken.get('count', 0) > 0:
            cleanup_actions.append({
                'type': 'broken_symlinks_cleanup',
                'description': f"{broken['count']}개의 깨진 심볼릭 링크 삭제",
                'files': broken.get('broken_links', []),
                'priority': 'low',
                'safe': True
            })
        
        return cleanup_actions
    
    def execute_safe_cleanup(self, cleanup_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """안전한 정리 작업 실행"""
        executed_actions = []
        skipped_actions = []
        
        for action in cleanup_actions:
            if not action.get('safe', False):
                skipped_actions.append({
                    'action': action,
                    'reason': 'Manual review required'
                })
                continue
            
            try:
                if action['type'] == 'temp_files_cleanup':
                    self._cleanup_temp_files(action['files'])
                elif action['type'] == 'log_compression':
                    self._compress_large_logs(action['files'])
                elif action['type'] == 'broken_symlinks_cleanup':
                    self._cleanup_broken_symlinks(action['files'])
                
                executed_actions.append(action)
                logging.info(f"정리 작업 완료: {action['description']}")
                
            except Exception as e:
                logging.error(f"정리 작업 실패 {action['type']}: {e}")
                skipped_actions.append({
                    'action': action,
                    'reason': f'Error: {str(e)}'
                })
        
        return {
            'executed': executed_actions,
            'skipped': skipped_actions,
            'executed_count': len(executed_actions),
            'skipped_count': len(skipped_actions)
        }
    
    def _cleanup_temp_files(self, temp_files: List[Dict[str, Any]]):
        """임시 파일 삭제"""
        for temp_file in temp_files:
            try:
                file_path = Path(temp_file['path'])
                if file_path.exists() and file_path.is_file():
                    file_path.unlink()
                    logging.debug(f"임시 파일 삭제: {file_path}")
            except Exception as e:
                logging.warning(f"임시 파일 삭제 실패 {temp_file['path']}: {e}")
    
    def _compress_large_logs(self, large_logs: List[Dict[str, Any]]):
        """큰 로그 파일 압축"""
        for log_info in large_logs:
            try:
                log_path = Path(log_info['path'])
                if log_path.exists() and log_path.suffix == '.log':
                    # gzip으로 압축
                    import gzip
                    compressed_path = log_path.with_suffix('.log.gz')
                    
                    with open(log_path, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # 원본 파일 삭제
                    log_path.unlink()
                    logging.info(f"로그 파일 압축: {log_path} -> {compressed_path}")
                    
            except Exception as e:
                logging.warning(f"로그 압축 실패 {log_info['path']}: {e}")
    
    def _cleanup_broken_symlinks(self, broken_links: List[Dict[str, Any]]):
        """깨진 심볼릭 링크 삭제"""
        for link_info in broken_links:
            try:
                link_path = Path(link_info['path'])
                if link_path.is_symlink() and not link_path.exists():
                    link_path.unlink()
                    logging.debug(f"깨진 심볼릭 링크 삭제: {link_path}")
            except Exception as e:
                logging.warning(f"심볼릭 링크 삭제 실패 {link_info['path']}: {e}")
    
    def generate_recommendations(self, scan_results: Dict[str, Any], entropy_level: str) -> List[str]:
        """추천사항 생성"""
        recommendations = []
        
        if entropy_level in ['critical', 'high']:
            recommendations.append("🚨 시스템 엔트로피가 높습니다. 즉시 정리 작업을 수행하세요")
            
        # 최상위 디렉토리 정리
        top_level = scan_results.get('top_level', {})
        if top_level.get('file_count', 0) > 0:
            recommendations.append(f"📁 최상위 디렉토리에 {top_level['file_count']}개의 미허가 파일이 있습니다")
        
        if top_level.get('dir_count', 0) > 0:
            recommendations.append(f"📂 최상위 디렉토리에 {top_level['dir_count']}개의 미허가 폴더가 있습니다")
        
        # 저장공간 절약
        duplicates = scan_results.get('duplicates', {})
        if duplicates.get('wasted_space_mb', 0) > 10:
            recommendations.append(f"💾 중복 파일로 {duplicates['wasted_space_mb']:.1f}MB 낭비되고 있습니다")
        
        # 정기 정리 제안
        if entropy_level == 'low':
            recommendations.append("✅ 시스템이 깔끔합니다. 주간 정리 스케줄을 유지하세요")
        
        return recommendations
    
    def run_full_scan(self) -> Dict[str, Any]:
        """전체 엔트로피 스캔 실행"""
        logging.info("엔트로피 스캔 시작...")
        
        scan_results = {
            'top_level': self.scan_top_level_entropy(),
            'temp_files': self.scan_temp_files(),
            'duplicates': self.scan_duplicate_files(),
            'orphaned_configs': self.scan_orphaned_configs(),
            'log_accumulation': self.scan_log_accumulation(),
            'broken_symlinks': self.scan_broken_symlinks()
        }
        
        # 엔트로피 레벨 계산
        entropy_level = self.calculate_entropy_level(scan_results)
        
        # 정리 계획 생성
        cleanup_plan = self.generate_cleanup_plan(scan_results)
        
        # 추천사항 생성
        recommendations = self.generate_recommendations(scan_results, entropy_level)
        
        # 결과 구성
        self.entropy_report.update({
            'entropy_level': entropy_level,
            'scan_results': scan_results,
            'cleanup_plan': cleanup_plan,
            'recommendations': recommendations
        })
        
        logging.info(f"엔트로피 스캔 완료. 레벨: {entropy_level}")
        
        return self.entropy_report
    
    def save_report(self, report: Dict[str, Any]):
        """엔트로피 리포트 저장"""
        report_dir = Path('/home/ubuntu/logs/entropy-reports')
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"entropy_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logging.info(f"엔트로피 리포트 저장됨: {report_file}")
        
        # 최신 리포트 링크 생성
        latest_link = report_dir / "latest.json"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(report_file.name)
    
    def print_summary(self, report: Dict[str, Any]):
        """엔트로피 리포트 요약 출력"""
        entropy_emoji = {
            'low': '🟢',
            'medium': '🟡', 
            'high': '🟠',
            'critical': '🔴'
        }
        
        print(f"\n{'='*60}")
        print(f"🌪️ HEAL7 엔트로피 감지 리포트")
        print(f"{'='*60}")
        print(f"📅 스캔 시간: {report['timestamp']}")
        print(f"📊 엔트로피 레벨: {entropy_emoji.get(report['entropy_level'], '❓')} {report['entropy_level'].upper()}")
        print(f"{'='*60}")
        
        # 주요 이슈 요약
        scan_results = report.get('scan_results', {})
        
        top_level = scan_results.get('top_level', {})
        print(f"📁 최상위 미허가 파일: {top_level.get('file_count', 0)}개")
        print(f"📂 최상위 미허가 폴더: {top_level.get('dir_count', 0)}개")
        
        temp_files = scan_results.get('temp_files', {})
        print(f"🗑️ 오래된 임시 파일: {temp_files.get('total_count', 0)}개 ({temp_files.get('total_size_mb', 0):.1f}MB)")
        
        duplicates = scan_results.get('duplicates', {})
        print(f"📋 중복 파일: {duplicates.get('duplicate_count', 0)}개 ({duplicates.get('wasted_space_mb', 0):.1f}MB 낭비)")
        
        # 정리 계획
        cleanup_plan = report.get('cleanup_plan', [])
        if cleanup_plan:
            print(f"\n🧹 정리 계획:")
            for i, action in enumerate(cleanup_plan, 1):
                safe_indicator = "✅" if action.get('safe') else "⚠️"
                print(f"   {i}. {safe_indicator} {action['description']}")
        
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
        detector = EntropyDetector()
        report = detector.run_full_scan()
        detector.save_report(report)
        detector.print_summary(report)
        
        # 자동 정리 옵션 (안전한 작업만)
        cleanup_plan = report.get('cleanup_plan', [])
        safe_actions = [action for action in cleanup_plan if action.get('safe', False)]
        
        if safe_actions:
            print(f"🤖 안전한 정리 작업 {len(safe_actions)}개를 자동 실행합니다...")
            cleanup_result = detector.execute_safe_cleanup(safe_actions)
            print(f"✅ {cleanup_result['executed_count']}개 작업 완료, {cleanup_result['skipped_count']}개 건너뜀")
        
        # 크리티컬 엔트로피면 exit code 1 반환
        if report['entropy_level'] == 'critical':
            return 1
        
        return 0
        
    except Exception as e:
        logging.error(f"엔트로피 스캔 실행 중 오류: {e}")
        return 1

if __name__ == "__main__":
    exit(main())