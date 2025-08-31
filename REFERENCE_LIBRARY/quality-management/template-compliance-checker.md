# 🔍 Template Compliance Checker - 템플릿 준수 검증 시스템

> **목적**: REFERENCE_LIBRARY 내 모든 문서가 정의된 템플릿을 준수하는지 자동 검증  
> **범위**: README, .spec, .guide, .complete, .atomic 파일들의 구조 분석  
> **업데이트**: 2025-08-26

## 🎯 **검증 대상 템플릿**

### **1. README 파일 템플릿**
```markdown
# [Title] - [Description]

## 🎯 목적
[Purpose description]

## 📂 구조
[Directory/File structure]

## [Additional sections...]

## ✅ 품질 기준
[Quality criteria checklist]
```

### **2. .spec 파일 템플릿** 
```markdown
# [기능명] 기능 명세서

## 📋 기본 정보
- **기능명**: [Feature Name]
- **우선순위**: [Priority]
- **예상 개발 기간**: [Duration]

## 🎯 개요
[Overview sections]

## 📋 상세 요구사항
[Requirements sections]

## ✅ 검수 기준
[Acceptance criteria]
```

### **3. .complete 파일 템플릿**
```python/typescript/html
"""
모듈명: [정확한 기능명]
목적: [WHY - 왜 만들었는지]
사용법: [HOW - 어떻게 사용하는지]
의존성: [DEPENDENCIES - 필요한 패키지들]
"""

# 모든 imports
# 상수 정의
# 메인 클래스/함수
# 테스트 케이스
# 사용 예시
```

### **4. .atomic 파일 템플릿**
```python
"""
원자 모듈: [단일 기능명]
복잡도: 5분 이해 가능
책임: 단일 책임 원칙 준수
테스트: 100% 커버리지
"""

# 단일 기능 구현
# 완전한 테스트
# 사용 예시
```

## 🔧 **자동 검증 스크립트**

### **README 템플릿 검증기**
```python
#!/usr/bin/env python3
"""
README 파일들의 템플릿 준수 여부를 검증하는 스크립트
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class ReadmeTemplateChecker:
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)
        self.required_sections = [
            r"## 🎯 목적",
            r"## 📂 구조", 
            r"## ✅ 품질 기준"
        ]
        self.results = []
    
    def check_file(self, file_path: Path) -> Dict:
        """단일 README 파일 검증"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            result = {
                'file': str(file_path),
                'compliant': True,
                'missing_sections': [],
                'issues': []
            }
            
            # 필수 섹션 체크
            for section in self.required_sections:
                if not re.search(section, content, re.MULTILINE):
                    result['missing_sections'].append(section)
                    result['compliant'] = False
            
            # 제목 형식 체크
            title_pattern = r"^# .+ - .+"
            if not re.search(title_pattern, content, re.MULTILINE):
                result['issues'].append("제목이 '# [Title] - [Description]' 형식이 아님")
                result['compliant'] = False
            
            # 이모지 사용 체크 (일관성)
            emoji_sections = re.findall(r"## [🎯📂🔧🚀✅].+", content)
            if len(emoji_sections) < 3:
                result['issues'].append("섹션에 일관된 이모지 사용 권장")
            
            return result
            
        except Exception as e:
            return {
                'file': str(file_path),
                'compliant': False,
                'error': str(e)
            }
    
    def scan_all_readme_files(self) -> List[Dict]:
        """모든 README 파일 검증"""
        readme_files = list(self.library_path.rglob("README*.md"))
        
        for readme_file in readme_files:
            result = self.check_file(readme_file)
            self.results.append(result)
        
        return self.results
    
    def generate_report(self) -> str:
        """검증 결과 리포트 생성"""
        total_files = len(self.results)
        compliant_files = sum(1 for r in self.results if r['compliant'])
        
        report = f"""
# README 템플릿 준수 검증 리포트

## 📊 요약
- **전체 파일 수**: {total_files}
- **준수 파일 수**: {compliant_files}
- **준수율**: {compliant_files/total_files*100:.1f}%

## 📋 상세 결과

"""
        
        for result in self.results:
            status = "✅ PASS" if result['compliant'] else "❌ FAIL"
            report += f"\n### {status} {result['file']}\n"
            
            if not result['compliant']:
                if 'missing_sections' in result:
                    report += "**누락된 섹션:**\n"
                    for section in result['missing_sections']:
                        report += f"- {section}\n"
                
                if 'issues' in result:
                    report += "**기타 이슈:**\n"
                    for issue in result['issues']:
                        report += f"- {issue}\n"
        
        return report

# 사용 예시
if __name__ == "__main__":
    checker = ReadmeTemplateChecker("/home/ubuntu/REFERENCE_LIBRARY")
    results = checker.scan_all_readme_files()
    report = checker.generate_report()
    
    # 리포트 저장
    with open("/home/ubuntu/REFERENCE_LIBRARY/quality-management/readme-compliance-report.md", "w") as f:
        f.write(report)
    
    print(f"검증 완료: {len(results)}개 파일 처리")
    print("리포트 저장: readme-compliance-report.md")
```

### **.complete 파일 검증기**
```python
#!/usr/bin/env python3
"""
.complete 파일들의 완성도를 검증하는 스크립트
"""

import ast
import os
from pathlib import Path
from typing import List, Dict

class CompleteFileChecker:
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)
        self.results = []
    
    def check_python_complete_file(self, file_path: Path) -> Dict:
        """Python .complete 파일 검증"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            result = {
                'file': str(file_path),
                'language': 'python',
                'compliant': True,
                'issues': []
            }
            
            # 문서 문자열 체크
            if '"""' not in content or 'WHY' not in content or 'HOW' not in content:
                result['issues'].append("모듈 설명 문서가 불완전")
                result['compliant'] = False
            
            # import 문 체크
            if 'import ' not in content:
                result['issues'].append("import 문이 없음 (의존성 불명확)")
            
            # 테스트 케이스 체크
            if 'test_' not in content and 'def test' not in content:
                result['issues'].append("테스트 케이스가 없음")
                result['compliant'] = False
            
            # 사용 예시 체크
            if '__name__ == "__main__"' not in content:
                result['issues'].append("사용 예시가 없음")
                result['compliant'] = False
            
            # 구문 분석 (문법 오류 체크)
            try:
                ast.parse(content)
            except SyntaxError as e:
                result['issues'].append(f"문법 오류: {e}")
                result['compliant'] = False
            
            return result
            
        except Exception as e:
            return {
                'file': str(file_path),
                'compliant': False,
                'error': str(e)
            }
    
    def check_typescript_complete_file(self, file_path: Path) -> Dict:
        """TypeScript/TSX .complete 파일 검증"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            result = {
                'file': str(file_path),
                'language': 'typescript',
                'compliant': True,
                'issues': []
            }
            
            # import 문 체크
            if 'import ' not in content and 'require(' not in content:
                result['issues'].append("import/require 문이 없음")
            
            # 타입 정의 체크 (.tsx 파일)
            if file_path.suffix == '.tsx':
                if 'interface ' not in content and 'type ' not in content:
                    result['issues'].append("TypeScript 타입 정의 권장")
                
                if 'React.FC' not in content and ': React.FC' not in content:
                    result['issues'].append("React.FC 타입 사용 권장")
            
            # export 체크
            if 'export ' not in content:
                result['issues'].append("export 문이 없음")
                result['compliant'] = False
            
            return result
            
        except Exception as e:
            return {
                'file': str(file_path),
                'compliant': False,
                'error': str(e)
            }
    
    def scan_all_complete_files(self) -> List[Dict]:
        """모든 .complete 파일 검증"""
        complete_files = list(self.library_path.rglob("*.complete.*"))
        
        for complete_file in complete_files:
            if complete_file.suffix == '.py':
                result = self.check_python_complete_file(complete_file)
            elif complete_file.suffix in ['.ts', '.tsx']:
                result = self.check_typescript_complete_file(complete_file)
            else:
                result = {
                    'file': str(complete_file),
                    'compliant': True,
                    'issues': ['언어별 상세 검증 미지원']
                }
            
            self.results.append(result)
        
        return self.results

# 실행 예시
if __name__ == "__main__":
    checker = CompleteFileChecker("/home/ubuntu/REFERENCE_LIBRARY")
    results = checker.scan_all_complete_files()
    
    print(f"✅ 검증 완료: {len(results)}개 .complete 파일 처리")
    
    for result in results:
        status = "✅" if result['compliant'] else "❌"
        print(f"{status} {result['file']}")
        if not result['compliant'] and 'issues' in result:
            for issue in result['issues']:
                print(f"   - {issue}")
```

## 📊 **검증 결과 분석**

### **품질 지표 계산**
```python
def calculate_quality_metrics(results: List[Dict]) -> Dict:
    """품질 메트릭 계산"""
    total_files = len(results)
    if total_files == 0:
        return {}
    
    compliant_files = sum(1 for r in results if r.get('compliant', False))
    compliance_rate = compliant_files / total_files * 100
    
    # 이슈 유형별 분석
    issue_types = {}
    for result in results:
        if 'issues' in result:
            for issue in result['issues']:
                issue_types[issue] = issue_types.get(issue, 0) + 1
    
    return {
        'total_files': total_files,
        'compliant_files': compliant_files,
        'compliance_rate': compliance_rate,
        'common_issues': sorted(issue_types.items(), key=lambda x: x[1], reverse=True)
    }
```

### **자동 수정 제안**
```python
def generate_fix_suggestions(results: List[Dict]) -> List[str]:
    """자동 수정 제안 생성"""
    suggestions = []
    
    # 공통 이슈 패턴 분석
    common_issues = {}
    for result in results:
        if not result.get('compliant', True) and 'issues' in result:
            for issue in result['issues']:
                common_issues[issue] = common_issues.get(issue, 0) + 1
    
    # 수정 제안 생성
    if "테스트 케이스가 없음" in common_issues:
        suggestions.append("""
### 🔧 테스트 케이스 추가 권장
.complete 파일에는 반드시 테스트 케이스가 포함되어야 합니다.

```python
def test_functionality():
    # 기본 테스트
    result = your_function(test_input)
    assert result == expected_output
    
    # 예외 케이스 테스트
    try:
        your_function(invalid_input)
        assert False, "예외가 발생해야 함"
    except ValueError:
        pass  # 예상된 예외
```
""")
    
    if "모듈 설명 문서가 불완전" in common_issues:
        suggestions.append("""
### 📝 문서화 개선 권장
.complete 파일 상단에 완전한 문서 문자열을 추가하세요.

```python
\"\"\"
모듈명: [정확한 기능명]
목적: [WHY - 왜 만들었는지]
사용법: [HOW - 어떻게 사용하는지]  
의존성: [DEPENDENCIES - 필요한 패키지들]
\"\"\"
```
""")
    
    return suggestions
```

## 🚀 **실행 가이드**

### **전체 검증 실행**
```bash
#!/bin/bash
# 전체 템플릿 준수 검증 실행

echo "🔍 REFERENCE_LIBRARY 템플릿 준수 검증 시작..."

# 1. README 파일 검증
echo "📋 README 파일들 검증 중..."
python3 /home/ubuntu/REFERENCE_LIBRARY/quality-management/readme-template-checker.py

# 2. .complete 파일 검증  
echo "⚙️ .complete 파일들 검증 중..."
python3 /home/ubuntu/REFERENCE_LIBRARY/quality-management/complete-file-checker.py

# 3. .spec 파일 검증
echo "📄 .spec 파일들 검증 중..."
python3 /home/ubuntu/REFERENCE_LIBRARY/quality-management/spec-file-checker.py

# 4. 통합 리포트 생성
echo "📊 통합 품질 리포트 생성 중..."
python3 /home/ubuntu/REFERENCE_LIBRARY/quality-management/generate-quality-report.py

echo "✅ 템플릿 준수 검증 완료!"
echo "📋 결과 확인: /home/ubuntu/REFERENCE_LIBRARY/quality-management/compliance-report-$(date +%Y%m%d).md"
```

### **개별 파일 검증**
```bash
# 특정 파일만 검증
python3 template-checker.py --file /path/to/specific/file.md

# 특정 카테고리만 검증
python3 template-checker.py --category sample-codes

# 수정 제안만 생성
python3 template-checker.py --suggest-fixes
```

## 🎯 **목표 달성 기준**

### **템플릿 준수 목표**
- **README 파일**: 95% 이상 템플릿 준수
- **.complete 파일**: 90% 이상 완성도 달성
- **.spec 파일**: 100% 구조 일관성
- **.atomic 파일**: 100% 단일 책임 원칙 준수

### **품질 개선 프로세스**
1. **주간 검증**: 매주 화요일 전체 검증 실행
2. **즉시 피드백**: 새 파일 추가 시 자동 검증
3. **월간 리포트**: 품질 트렌드 분석 및 개선방향 수립
4. **자동 수정**: 패턴 기반 자동 수정 제안 시스템

---

**🎯 최종 목표**: 모든 REFERENCE_LIBRARY 파일이 일관된 템플릿을 준수하여 AI와 개발자 모두에게 최적화된 구조 달성

*작성일: 2025-08-26 | 버전: v1.0*