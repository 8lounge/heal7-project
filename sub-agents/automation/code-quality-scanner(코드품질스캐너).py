#!/usr/bin/env python3
"""
🔍 HEAL7 코드 품질 스캐너
큐브 모델 기반 코드 품질 분석 및 개선 제안

Author: AI Agent Team
Created: 2025-08-20
"""

import os
import subprocess
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CodeQualityScanner:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.scan_results = {
            'timestamp': self.timestamp,
            'overall_score': 0,
            'cube_analysis': {},
            'security_issues': [],
            'performance_issues': [],
            'maintainability_issues': [],
            'best_practices_violations': [],
            'recommendations': []
        }
        
        # 스캔 대상 큐브 디렉토리
        self.cube_directories = {
            'admin_cube': '/home/ubuntu/heal7-system/apps/admin/heal7-admin-vite',
            'main_cube': '/home/ubuntu/heal7-system/apps/index/heal7-index-vite',
            'keywords_cube': '/home/ubuntu/heal7-system/apps/keywords/heal7-keywords-vite',
            'saju_backend': '/home/ubuntu/archive/projects/duplicates',
            'reference_library': '/home/ubuntu/REFERENCE_LIBRARY'
        }
        
        # 코드 품질 기준
        self.quality_standards = {
            'max_function_length': 50,
            'max_file_length': 500,
            'max_cyclomatic_complexity': 10,
            'min_test_coverage': 80,
            'max_todo_comments': 5
        }
    
    def scan_python_files(self, directory: Path) -> Dict[str, Any]:
        """Python 파일 품질 분석"""
        python_files = list(directory.rglob("*.py"))
        if not python_files:
            return {'message': 'No Python files found'}
        
        results = {
            'file_count': len(python_files),
            'total_lines': 0,
            'issues': [],
            'metrics': {}
        }
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    results['total_lines'] += len(lines)
                
                # AST 파싱으로 구조 분석
                try:
                    tree = ast.parse(content)
                    file_analysis = self._analyze_python_ast(tree, file_path, lines)
                    results['issues'].extend(file_analysis['issues'])
                except SyntaxError as e:
                    results['issues'].append({
                        'type': 'syntax_error',
                        'file': str(file_path),
                        'line': e.lineno,
                        'message': str(e),
                        'severity': 'high'
                    })
                
                # 기본 코드 스타일 체크
                style_issues = self._check_python_style(content, file_path, lines)
                results['issues'].extend(style_issues)
                
            except Exception as e:
                logging.error(f"Python 파일 분석 실패 {file_path}: {e}")
        
        return results
    
    def scan_typescript_files(self, directory: Path) -> Dict[str, Any]:
        """TypeScript/JavaScript 파일 품질 분석"""
        ts_files = list(directory.rglob("*.ts")) + list(directory.rglob("*.tsx")) + \
                   list(directory.rglob("*.js")) + list(directory.rglob("*.jsx"))
        
        # node_modules 제외
        ts_files = [f for f in ts_files if 'node_modules' not in str(f)]
        
        if not ts_files:
            return {'message': 'No TypeScript/JavaScript files found'}
        
        results = {
            'file_count': len(ts_files),
            'total_lines': 0,
            'issues': [],
            'metrics': {}
        }
        
        for file_path in ts_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    results['total_lines'] += len(lines)
                
                # TypeScript/JavaScript 스타일 체크
                style_issues = self._check_typescript_style(content, file_path, lines)
                results['issues'].extend(style_issues)
                
                # React 컴포넌트 분석
                if file_path.suffix in ['.tsx', '.jsx']:
                    react_issues = self._check_react_patterns(content, file_path, lines)
                    results['issues'].extend(react_issues)
                
            except Exception as e:
                logging.error(f"TypeScript 파일 분석 실패 {file_path}: {e}")
        
        return results
    
    def scan_css_files(self, directory: Path) -> Dict[str, Any]:
        """CSS 파일 품질 분석"""
        css_files = list(directory.rglob("*.css")) + list(directory.rglob("*.scss"))
        css_files = [f for f in css_files if 'node_modules' not in str(f)]
        
        if not css_files:
            return {'message': 'No CSS files found'}
        
        results = {
            'file_count': len(css_files),
            'total_lines': 0,
            'issues': [],
            'metrics': {}
        }
        
        for file_path in css_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    results['total_lines'] += len(lines)
                
                # CSS 스타일 체크
                style_issues = self._check_css_style(content, file_path, lines)
                results['issues'].extend(style_issues)
                
            except Exception as e:
                logging.error(f"CSS 파일 분석 실패 {file_path}: {e}")
        
        return results
    
    def _analyze_python_ast(self, tree: ast.AST, file_path: Path, lines: List[str]) -> Dict[str, Any]:
        """Python AST 분석"""
        issues = []
        
        for node in ast.walk(tree):
            # 함수 길이 체크
            if isinstance(node, ast.FunctionDef):
                func_length = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if func_length > self.quality_standards['max_function_length']:
                    issues.append({
                        'type': 'long_function',
                        'file': str(file_path),
                        'line': node.lineno,
                        'message': f"함수 '{node.name}'이 너무 깁니다 ({func_length}줄 > {self.quality_standards['max_function_length']}줄)",
                        'severity': 'medium'
                    })
                
                # 복잡한 함수 체크 (네스팅 깊이)
                nesting_depth = self._calculate_nesting_depth(node)
                if nesting_depth > 4:
                    issues.append({
                        'type': 'high_complexity',
                        'file': str(file_path),
                        'line': node.lineno,
                        'message': f"함수 '{node.name}'의 중첩 깊이가 너무 깊습니다 ({nesting_depth})",
                        'severity': 'medium'
                    })
            
            # 클래스 길이 체크
            if isinstance(node, ast.ClassDef):
                class_length = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if class_length > 200:
                    issues.append({
                        'type': 'long_class',
                        'file': str(file_path),
                        'line': node.lineno,
                        'message': f"클래스 '{node.name}'이 너무 깁니다 ({class_length}줄)",
                        'severity': 'medium'
                    })
        
        return {'issues': issues}
    
    def _calculate_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        """AST 노드의 중첩 깊이 계산"""
        max_depth = depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                child_depth = self._calculate_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _check_python_style(self, content: str, file_path: Path, lines: List[str]) -> List[Dict[str, Any]]:
        """Python 스타일 체크"""
        issues = []
        
        # 파일 길이 체크
        if len(lines) > self.quality_standards['max_file_length']:
            issues.append({
                'type': 'long_file',
                'file': str(file_path),
                'line': 1,
                'message': f"파일이 너무 깁니다 ({len(lines)}줄 > {self.quality_standards['max_file_length']}줄)",
                'severity': 'low'
            })
        
        # TODO 주석 체크
        todo_count = len([line for line in lines if 'TODO' in line.upper() or 'FIXME' in line.upper()])
        if todo_count > self.quality_standards['max_todo_comments']:
            issues.append({
                'type': 'too_many_todos',
                'file': str(file_path),
                'line': 1,
                'message': f"TODO/FIXME 주석이 너무 많습니다 ({todo_count}개)",
                'severity': 'low'
            })
        
        # 하드코딩된 문자열 체크
        hardcoded_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']'
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in hardcoded_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'hardcoded_secret',
                        'file': str(file_path),
                        'line': i,
                        'message': "하드코딩된 시크릿이 감지되었습니다",
                        'severity': 'high'
                    })
        
        return issues
    
    def _check_typescript_style(self, content: str, file_path: Path, lines: List[str]) -> List[Dict[str, Any]]:
        """TypeScript/JavaScript 스타일 체크"""
        issues = []
        
        # console.log 체크
        console_logs = [i for i, line in enumerate(lines, 1) if 'console.log' in line]
        if console_logs:
            for line_num in console_logs:
                issues.append({
                    'type': 'debug_code',
                    'file': str(file_path),
                    'line': line_num,
                    'message': "프로덕션 코드에 console.log가 남아있습니다",
                    'severity': 'low'
                })
        
        # any 타입 체크
        any_types = [i for i, line in enumerate(lines, 1) if ': any' in line or 'any[]' in line]
        if any_types:
            for line_num in any_types:
                issues.append({
                    'type': 'any_type_usage',
                    'file': str(file_path),
                    'line': line_num,
                    'message': "any 타입 사용을 피하고 구체적인 타입을 정의하세요",
                    'severity': 'medium'
                })
        
        # 긴 함수 체크 (단순한 라인 수 기반)
        function_pattern = r'(function\s+\w+|const\s+\w+\s*=\s*\([^)]*\)\s*=>|\w+\s*\([^)]*\)\s*{)'
        in_function = False
        function_start = 0
        brace_count = 0
        
        for i, line in enumerate(lines, 1):
            if re.search(function_pattern, line):
                in_function = True
                function_start = i
                brace_count = line.count('{') - line.count('}')
            elif in_function:
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0:
                    function_length = i - function_start
                    if function_length > 30:
                        issues.append({
                            'type': 'long_function',
                            'file': str(file_path),
                            'line': function_start,
                            'message': f"함수가 너무 깁니다 ({function_length}줄)",
                            'severity': 'medium'
                        })
                    in_function = False
        
        return issues
    
    def _check_react_patterns(self, content: str, file_path: Path, lines: List[str]) -> List[Dict[str, Any]]:
        """React 컴포넌트 패턴 체크"""
        issues = []
        
        # 인라인 스타일 체크
        inline_styles = [i for i, line in enumerate(lines, 1) if 'style={{' in line]
        if len(inline_styles) > 3:
            issues.append({
                'type': 'too_many_inline_styles',
                'file': str(file_path),
                'line': 1,
                'message': f"인라인 스타일이 너무 많습니다 ({len(inline_styles)}개). CSS 클래스 사용을 권장합니다",
                'severity': 'low'
            })
        
        # useEffect 의존성 배열 체크
        useeffect_pattern = r'useEffect\s*\(\s*\(\s*\)\s*=>\s*{[^}]*},\s*\[\s*\]\s*\)'
        empty_deps = len(re.findall(useeffect_pattern, content, re.DOTALL))
        if empty_deps > 2:
            issues.append({
                'type': 'empty_useeffect_deps',
                'file': str(file_path),
                'line': 1,
                'message': "빈 의존성 배열을 가진 useEffect가 너무 많습니다",
                'severity': 'medium'
            })
        
        return issues
    
    def _check_css_style(self, content: str, file_path: Path, lines: List[str]) -> List[Dict[str, Any]]:
        """CSS 스타일 체크"""
        issues = []
        
        # !important 체크
        important_uses = [i for i, line in enumerate(lines, 1) if '!important' in line]
        if len(important_uses) > 5:
            issues.append({
                'type': 'too_many_important',
                'file': str(file_path),
                'line': 1,
                'message': f"!important 사용이 너무 많습니다 ({len(important_uses)}개)",
                'severity': 'medium'
            })
        
        # 중복 속성 체크
        properties = []
        for line in lines:
            if ':' in line and '{' not in line and '}' not in line:
                prop = line.split(':')[0].strip()
                properties.append(prop)
        
        duplicate_props = [prop for prop in set(properties) if properties.count(prop) > 3]
        if duplicate_props:
            issues.append({
                'type': 'duplicate_css_properties',
                'file': str(file_path),
                'line': 1,
                'message': f"중복된 CSS 속성: {', '.join(duplicate_props[:3])}...",
                'severity': 'low'
            })
        
        return issues
    
    def check_security_vulnerabilities(self, directory: Path) -> List[Dict[str, Any]]:
        """보안 취약점 체크"""
        vulnerabilities = []
        
        # Python 파일에서 보안 이슈 체크
        for py_file in directory.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # SQL 인젝션 위험 패턴
                if re.search(r'execute\s*\(\s*f?["\'][^"\']*\{[^}]+\}[^"\']*["\']', content):
                    vulnerabilities.append({
                        'type': 'sql_injection_risk',
                        'file': str(py_file),
                        'message': "SQL 인젝션 위험: f-string이나 포맷팅된 쿼리 감지",
                        'severity': 'high'
                    })
                
                # 하드코딩된 시크릿
                secret_patterns = [
                    r'password\s*=\s*["\'][^"\']{8,}["\']',
                    r'secret\s*=\s*["\'][^"\']{16,}["\']',
                    r'token\s*=\s*["\'][^"\']{20,}["\']'
                ]
                
                for pattern in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        vulnerabilities.append({
                            'type': 'hardcoded_secret',
                            'file': str(py_file),
                            'message': "하드코딩된 시크릿 감지",
                            'severity': 'high'
                        })
                
            except Exception as e:
                logging.error(f"보안 스캔 실패 {py_file}: {e}")
        
        # JavaScript/TypeScript 파일에서 보안 이슈 체크
        for js_file in directory.rglob("*.js"):
            if 'node_modules' in str(js_file):
                continue
                
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # eval 사용 체크
                if 'eval(' in content:
                    vulnerabilities.append({
                        'type': 'eval_usage',
                        'file': str(js_file),
                        'message': "eval() 사용은 보안 위험을 초래할 수 있습니다",
                        'severity': 'high'
                    })
                
                # innerHTML 사용 체크
                if '.innerHTML' in content:
                    vulnerabilities.append({
                        'type': 'innerHTML_usage',
                        'file': str(js_file),
                        'message': "innerHTML 사용 시 XSS 위험이 있습니다",
                        'severity': 'medium'
                    })
                
            except Exception as e:
                logging.error(f"JavaScript 보안 스캔 실패 {js_file}: {e}")
        
        return vulnerabilities
    
    def check_performance_issues(self, directory: Path) -> List[Dict[str, Any]]:
        """성능 이슈 체크"""
        performance_issues = []
        
        # 큰 파일 체크
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.js', '.ts', '.tsx', '.jsx', '.py', '.css']:
                if 'node_modules' in str(file_path):
                    continue
                    
                file_size = file_path.stat().st_size
                if file_size > 100 * 1024:  # 100KB 이상
                    performance_issues.append({
                        'type': 'large_file',
                        'file': str(file_path),
                        'message': f"큰 파일 크기: {file_size // 1024}KB",
                        'severity': 'medium'
                    })
        
        # React 컴포넌트 성능 이슈
        for tsx_file in directory.rglob("*.tsx"):
            if 'node_modules' in str(tsx_file):
                continue
                
            try:
                with open(tsx_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 인라인 함수 정의
                inline_functions = len(re.findall(r'onClick=\{[^}]*=>[^}]*\}', content))
                if inline_functions > 3:
                    performance_issues.append({
                        'type': 'inline_functions',
                        'file': str(tsx_file),
                        'message': f"인라인 함수가 너무 많습니다 ({inline_functions}개)",
                        'severity': 'low'
                    })
                
            except Exception as e:
                logging.error(f"React 성능 스캔 실패 {tsx_file}: {e}")
        
        return performance_issues
    
    def generate_cube_score(self, cube_analysis: Dict[str, Any]) -> int:
        """큐브별 점수 계산 (0-100)"""
        base_score = 100
        
        # 이슈 심각도별 점수 차감
        for lang_analysis in cube_analysis.values():
            if isinstance(lang_analysis, dict) and 'issues' in lang_analysis:
                for issue in lang_analysis['issues']:
                    if issue['severity'] == 'high':
                        base_score -= 10
                    elif issue['severity'] == 'medium':
                        base_score -= 5
                    elif issue['severity'] == 'low':
                        base_score -= 2
        
        return max(0, base_score)
    
    def scan_cube(self, cube_name: str, cube_path: str) -> Dict[str, Any]:
        """개별 큐브 스캔"""
        cube_dir = Path(cube_path)
        if not cube_dir.exists():
            return {'error': f'Cube directory not found: {cube_path}'}
        
        logging.info(f"큐브 스캔 시작: {cube_name}")
        
        cube_analysis = {
            'python': self.scan_python_files(cube_dir),
            'typescript': self.scan_typescript_files(cube_dir),
            'css': self.scan_css_files(cube_dir),
            'security': self.check_security_vulnerabilities(cube_dir),
            'performance': self.check_performance_issues(cube_dir)
        }
        
        cube_analysis['score'] = self.generate_cube_score(cube_analysis)
        
        return cube_analysis
    
    def generate_recommendations(self) -> List[str]:
        """개선 추천사항 생성"""
        recommendations = []
        
        # 보안 이슈 기반 추천
        security_issues = self.scan_results.get('security_issues', [])
        if security_issues:
            high_security = len([i for i in security_issues if i.get('severity') == 'high'])
            if high_security > 0:
                recommendations.append(f"🔒 {high_security}개의 심각한 보안 이슈를 즉시 해결하세요")
        
        # 성능 이슈 기반 추천
        performance_issues = self.scan_results.get('performance_issues', [])
        if performance_issues:
            large_files = len([i for i in performance_issues if i.get('type') == 'large_file'])
            if large_files > 3:
                recommendations.append(f"📊 {large_files}개의 큰 파일을 최적화하세요")
        
        # 큐브별 점수 기반 추천
        low_score_cubes = [
            name for name, analysis in self.scan_results.get('cube_analysis', {}).items()
            if isinstance(analysis, dict) and analysis.get('score', 100) < 70
        ]
        if low_score_cubes:
            recommendations.append(f"🎯 다음 큐브들의 코드 품질 개선이 필요합니다: {', '.join(low_score_cubes)}")
        
        # 일반적인 권장사항
        if not recommendations:
            recommendations.append("✅ 전반적인 코드 품질이 양호합니다. 지속적인 리팩토링을 권장합니다")
        
        return recommendations
    
    def calculate_overall_score(self) -> int:
        """전체 시스템 점수 계산"""
        cube_scores = [
            analysis.get('score', 0) 
            for analysis in self.scan_results.get('cube_analysis', {}).values()
            if isinstance(analysis, dict) and 'score' in analysis
        ]
        
        if not cube_scores:
            return 0
        
        return sum(cube_scores) // len(cube_scores)
    
    def run_full_scan(self) -> Dict[str, Any]:
        """전체 코드 품질 스캔 실행"""
        logging.info("전체 코드 품질 스캔 시작...")
        
        # 각 큐브 스캔
        for cube_name, cube_path in self.cube_directories.items():
            self.scan_results['cube_analysis'][cube_name] = self.scan_cube(cube_name, cube_path)
        
        # 보안 및 성능 이슈 수집
        all_security_issues = []
        all_performance_issues = []
        
        for cube_analysis in self.scan_results['cube_analysis'].values():
            if isinstance(cube_analysis, dict):
                all_security_issues.extend(cube_analysis.get('security', []))
                all_performance_issues.extend(cube_analysis.get('performance', []))
        
        self.scan_results['security_issues'] = all_security_issues
        self.scan_results['performance_issues'] = all_performance_issues
        
        # 추천사항 생성
        self.scan_results['recommendations'] = self.generate_recommendations()
        
        # 전체 점수 계산
        self.scan_results['overall_score'] = self.calculate_overall_score()
        
        logging.info(f"코드 품질 스캔 완료. 전체 점수: {self.scan_results['overall_score']}")
        
        return self.scan_results
    
    def save_report(self, results: Dict[str, Any]):
        """스캔 결과를 파일로 저장"""
        report_dir = Path('/home/ubuntu/logs/code-quality-reports')
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"code_quality_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logging.info(f"코드 품질 리포트 저장됨: {report_file}")
        
        # 최신 리포트 링크 생성
        latest_link = report_dir / "latest.json"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(report_file.name)
    
    def print_summary(self, results: Dict[str, Any]):
        """스캔 결과 요약 출력"""
        print(f"\n{'='*60}")
        print(f"🔍 HEAL7 코드 품질 스캔 리포트")
        print(f"{'='*60}")
        print(f"📅 스캔 시간: {results['timestamp']}")
        print(f"📊 전체 점수: {results['overall_score']}/100")
        print(f"{'='*60}")
        
        # 큐브별 점수
        print(f"📦 큐브별 점수:")
        for cube_name, analysis in results.get('cube_analysis', {}).items():
            if isinstance(analysis, dict) and 'score' in analysis:
                score = analysis['score']
                emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                print(f"   {emoji} {cube_name}: {score}/100")
        
        # 이슈 요약
        security_high = len([i for i in results.get('security_issues', []) if i.get('severity') == 'high'])
        performance_issues = len(results.get('performance_issues', []))
        
        if security_high > 0:
            print(f"🚨 심각한 보안 이슈: {security_high}개")
        
        if performance_issues > 0:
            print(f"📈 성능 이슈: {performance_issues}개")
        
        # 추천사항
        if results.get('recommendations'):
            print(f"\n📋 추천사항:")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print(f"{'='*60}\n")

def main():
    """메인 실행 함수"""
    try:
        scanner = CodeQualityScanner()
        results = scanner.run_full_scan()
        scanner.save_report(results)
        scanner.print_summary(results)
        
    except Exception as e:
        logging.error(f"코드 품질 스캔 실행 중 오류: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())