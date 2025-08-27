# 🤖 Automated Validation Scripts - 자동 검증 스크립트 시스템

> **목적**: REFERENCE_LIBRARY 품질을 자동으로 검증하고 관리하는 스크립트 시스템  
> **범위**: 파일명, 템플릿, 링크, 중복 콘텐츠 등 종합 검증  
> **업데이트**: 2025-08-26

## 🎯 **검증 스크립트 구조**

### **1. 마스터 검증 스크립트**
```bash
#!/bin/bash
# master-quality-validator.sh
# REFERENCE_LIBRARY 종합 품질 검증 스크립트

set -e

LIBRARY_PATH="/home/ubuntu/REFERENCE_LIBRARY"
REPORT_PATH="$LIBRARY_PATH/quality-management/reports"
DATE_STAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$REPORT_PATH/quality-report-$DATE_STAMP.md"

echo "🔍 REFERENCE_LIBRARY 품질 검증 시작 - $(date)"

# 보고서 디렉토리 생성
mkdir -p "$REPORT_PATH"

# 헤더 작성
cat > "$REPORT_FILE" << 'EOL'
# 📊 REFERENCE_LIBRARY 품질 검증 리포트

> **생성일시**: $(date)  
> **검증 범위**: 전체 라이브러리  
> **검증 항목**: 파일명, 템플릿, 링크, 중복 콘텐츠

## 🎯 **검증 결과 요약**
EOL

echo "## 📋 **상세 검증 결과**" >> "$REPORT_FILE"

# 1. 파일명 표준 검증
echo "🔤 1단계: 파일명 표준 검증..."
python3 "$LIBRARY_PATH/quality-management/scripts/validate_file_names.py" >> "$REPORT_FILE"

# 2. README 템플릿 검증  
echo "📚 2단계: README 템플릿 검증..."
python3 "$LIBRARY_PATH/quality-management/scripts/validate_readme_templates.py" >> "$REPORT_FILE"

# 3. .complete 파일 검증
echo "⚙️ 3단계: .complete 파일 검증..."
python3 "$LIBRARY_PATH/quality-management/scripts/validate_complete_files.py" >> "$REPORT_FILE"

# 4. 내부 링크 검증
echo "🔗 4단계: 내부 링크 검증..."
python3 "$LIBRARY_PATH/quality-management/scripts/validate_internal_links.py" >> "$REPORT_FILE"

# 5. 중복 콘텐츠 검사
echo "🔍 5단계: 중복 콘텐츠 검사..."
python3 "$LIBRARY_PATH/quality-management/scripts/detect_duplicate_content.py" >> "$REPORT_FILE"

# 6. 전체 통계 생성
echo "📊 6단계: 종합 통계 생성..."
python3 "$LIBRARY_PATH/quality-management/scripts/generate_statistics.py" >> "$REPORT_FILE"

# 완료 메시지
echo "## ✅ **검증 완료**" >> "$REPORT_FILE"
echo "- **생성 시간**: $(date)" >> "$REPORT_FILE"
echo "- **다음 검증**: 7일 후 권장" >> "$REPORT_FILE"

echo "✅ 품질 검증 완료!"
echo "📋 리포트 위치: $REPORT_FILE"

# Slack 알림 (선택적)
if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
    curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"📊 REFERENCE_LIBRARY 품질 검증 완료\\n리포트: $REPORT_FILE\"}" \
    "$SLACK_WEBHOOK_URL"
fi
```

### **2. 파일명 검증 스크립트**
```python
#!/usr/bin/env python3
"""
validate_file_names.py
파일명 표준 준수 여부를 검증하는 스크립트
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class FileNameValidator:
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)
        self.results = {'compliant': [], 'non_compliant': []}
        
        # 표준 패턴들
        self.patterns = {
            'standard': r'^[A-Z][a-zA-Z0-9-]*-v\d+\.\d+\([가-힣]+\)\.(md|py|tsx?|html|json)$',
            'readme': r'^README\([가-힣]+\)\.md$',
            'complete': r'^Sample-[A-Z][a-zA-Z0-9-]*-v\d+\.\d+\([가-힣]+\)\.complete\.(py|tsx?|html)$',
            'atomic': r'^Core-[A-Z][a-zA-Z0-9-]*-v\d+\.\d+\([가-힣]+\)\.atomic\.py$'
        }
    
    def validate_filename(self, file_path: Path) -> Tuple[bool, str]:
        """파일명 검증"""
        filename = file_path.name
        
        # README 파일 체크
        if filename.startswith('README'):
            return bool(re.match(self.patterns['readme'], filename)), 'readme'
        
        # .complete 파일 체크
        if '.complete.' in filename:
            return bool(re.match(self.patterns['complete'], filename)), 'complete'
        
        # .atomic 파일 체크
        if '.atomic.' in filename:
            return bool(re.match(self.patterns['atomic'], filename)), 'atomic'
        
        # 일반 표준 파일 체크
        return bool(re.match(self.patterns['standard'], filename)), 'standard'
    
    def scan_all_files(self):
        """모든 파일 스캔"""
        for file_path in self.library_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                is_compliant, file_type = self.validate_filename(file_path)
                
                result_entry = {
                    'path': str(file_path.relative_to(self.library_path)),
                    'filename': file_path.name,
                    'type': file_type
                }
                
                if is_compliant:
                    self.results['compliant'].append(result_entry)
                else:
                    self.results['non_compliant'].append(result_entry)
    
    def generate_report(self) -> str:
        """검증 결과 리포트 생성"""
        total_files = len(self.results['compliant']) + len(self.results['non_compliant'])
        compliant_count = len(self.results['compliant'])
        compliance_rate = (compliant_count / total_files * 100) if total_files > 0 else 0
        
        report = f"""
### 🔤 **파일명 표준 검증 결과**

- **전체 파일**: {total_files}개
- **표준 준수**: {compliant_count}개  
- **표준 미준수**: {len(self.results['non_compliant'])}개
- **준수율**: {compliance_rate:.1f}%

"""
        
        if self.results['non_compliant']:
            report += "#### ❌ **표준 미준수 파일들**\n"
            for item in self.results['non_compliant'][:10]:  # 상위 10개만 표시
                report += f"- `{item['path']}`\n"
            
            if len(self.results['non_compliant']) > 10:
                report += f"- ... 외 {len(self.results['non_compliant']) - 10}개\n"
        
        return report

if __name__ == "__main__":
    validator = FileNameValidator("/home/ubuntu/REFERENCE_LIBRARY")
    validator.scan_all_files()
    print(validator.generate_report())
```

### **3. 중복 콘텐츠 탐지 스크립트**
```python
#!/usr/bin/env python3
"""
detect_duplicate_content.py
중복 또는 유사한 콘텐츠를 탐지하는 스크립트
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Set
from difflib import SequenceMatcher

class DuplicateContentDetector:
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)
        self.similarity_threshold = 0.8  # 80% 이상 유사하면 중복으로 간주
        self.duplicates = []
        self.file_hashes = {}
        
    def get_file_hash(self, file_path: Path) -> str:
        """파일 해시 생성"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            # 공백과 줄바꿈 정규화
            normalized = ' '.join(content.split())
            return hashlib.md5(normalized.encode()).hexdigest()
        except Exception:
            return None
    
    def calculate_similarity(self, content1: str, content2: str) -> float:
        """두 텍스트의 유사도 계산"""
        return SequenceMatcher(None, content1, content2).ratio()
    
    def scan_for_duplicates(self):
        """중복 파일 스캔"""
        md_files = list(self.library_path.rglob('*.md'))
        
        # 1단계: 완전 동일한 파일 찾기
        hash_groups = {}
        for file_path in md_files:
            file_hash = self.get_file_hash(file_path)
            if file_hash:
                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []
                hash_groups[file_hash].append(file_path)
        
        # 동일한 해시를 가진 파일들이 2개 이상이면 중복
        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                self.duplicates.append({
                    'type': 'identical',
                    'similarity': 1.0,
                    'files': [str(f.relative_to(self.library_path)) for f in files]
                })
        
        # 2단계: 유사한 콘텐츠 찾기 (소규모 파일들만)
        small_files = [f for f in md_files if f.stat().st_size < 50000]  # 50KB 이하
        
        for i, file1 in enumerate(small_files):
            for file2 in small_files[i+1:]:
                try:
                    content1 = file1.read_text(encoding='utf-8', errors='ignore')
                    content2 = file2.read_text(encoding='utf-8', errors='ignore')
                    
                    similarity = self.calculate_similarity(content1, content2)
                    
                    if similarity >= self.similarity_threshold:
                        self.duplicates.append({
                            'type': 'similar',
                            'similarity': similarity,
                            'files': [
                                str(file1.relative_to(self.library_path)),
                                str(file2.relative_to(self.library_path))
                            ]
                        })
                except Exception:
                    continue
    
    def generate_report(self) -> str:
        """중복 콘텐츠 리포트 생성"""
        report = f"""
### 🔍 **중복 콘텐츠 검사 결과**

- **탐지된 중복 그룹**: {len(self.duplicates)}개

"""
        
        if self.duplicates:
            report += "#### 🔄 **발견된 중복/유사 콘텐츠**\n"
            
            for i, dup in enumerate(self.duplicates[:5], 1):  # 상위 5개만 표시
                dup_type = "완전 동일" if dup['type'] == 'identical' else f"유사 ({dup['similarity']:.1%})"
                report += f"\n**{i}. {dup_type}**\n"
                for file_path in dup['files']:
                    report += f"- `{file_path}`\n"
            
            if len(self.duplicates) > 5:
                report += f"\n*... 외 {len(self.duplicates) - 5}개 그룹*\n"
        else:
            report += "✅ 중복 콘텐츠가 발견되지 않았습니다.\n"
        
        return report

if __name__ == "__main__":
    detector = DuplicateContentDetector("/home/ubuntu/REFERENCE_LIBRARY")
    detector.scan_for_duplicates()
    print(detector.generate_report())
```

### **4. 통계 생성 스크립트**
```python
#!/usr/bin/env python3
"""
generate_statistics.py
REFERENCE_LIBRARY 전체 통계를 생성하는 스크립트
"""

from pathlib import Path
from collections import defaultdict
import json

class LibraryStatisticsGenerator:
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)
        self.stats = {
            'total_files': 0,
            'file_types': defaultdict(int),
            'categories': defaultdict(int),
            'completion_status': {
                'complete_files': 0,
                'atomic_files': 0,
                'spec_files': 0,
                'readme_files': 0
            }
        }
    
    def analyze_library(self):
        """라이브러리 분석"""
        for file_path in self.library_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                self.stats['total_files'] += 1
                
                # 파일 확장자별 분류
                extension = file_path.suffix.lower()
                self.stats['file_types'][extension] += 1
                
                # 카테고리별 분류 (1단계 폴더명 기준)
                try:
                    category = file_path.relative_to(self.library_path).parts[0]
                    self.stats['categories'][category] += 1
                except IndexError:
                    pass
                
                # 완성도별 분류
                filename = file_path.name
                if '.complete.' in filename:
                    self.stats['completion_status']['complete_files'] += 1
                elif '.atomic.' in filename:
                    self.stats['completion_status']['atomic_files'] += 1
                elif '.spec.' in filename:
                    self.stats['completion_status']['spec_files'] += 1
                elif filename.startswith('README'):
                    self.stats['completion_status']['readme_files'] += 1
    
    def generate_report(self) -> str:
        """통계 리포트 생성"""
        report = f"""
### 📊 **REFERENCE_LIBRARY 통계**

#### 📁 **전체 현황**
- **총 파일 수**: {self.stats['total_files']:,}개

#### 📄 **파일 유형별**
"""
        
        for ext, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True):
            if ext:
                report += f"- **{ext}**: {count}개\n"
        
        report += f"\n#### 📂 **카테고리별**\n"
        for category, count in sorted(self.stats['categories'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **{category}**: {count}개\n"
        
        report += f"""
#### 🎯 **완성도별**
- **완성 모듈 (.complete)**: {self.stats['completion_status']['complete_files']}개
- **원자 모듈 (.atomic)**: {self.stats['completion_status']['atomic_files']}개  
- **명세서 (.spec)**: {self.stats['completion_status']['spec_files']}개
- **가이드 (README)**: {self.stats['completion_status']['readme_files']}개

#### 🏆 **품질 지표**
- **AI 친화적 파일 비율**: {((self.stats['completion_status']['complete_files'] + self.stats['completion_status']['atomic_files']) / self.stats['total_files'] * 100) if self.stats['total_files'] > 0 else 0:.1f}%
- **문서화 비율**: {(self.stats['completion_status']['readme_files'] / len(self.stats['categories']) * 100) if len(self.stats['categories']) > 0 else 0:.1f}%
"""
        
        return report

if __name__ == "__main__":
    generator = LibraryStatisticsGenerator("/home/ubuntu/REFERENCE_LIBRARY")
    generator.analyze_library()
    print(generator.generate_report())
```

## 🔄 **자동화 설정**

### **Cron 설정 예시**
```bash
# 매주 화요일 오전 9시에 품질 검증 실행
0 9 * * 2 /home/ubuntu/REFERENCE_LIBRARY/quality-management/master-quality-validator.sh

# 매일 오후 6시에 간단한 상태 체크
0 18 * * * /home/ubuntu/REFERENCE_LIBRARY/quality-management/daily-health-check.sh
```

### **GitHub Actions 연동**
```yaml
name: Reference Library Quality Check

on:
  schedule:
    - cron: '0 9 * * 2'  # 매주 화요일 오전 9시
  push:
    paths:
      - 'REFERENCE_LIBRARY/**'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Quality Validation
      run: |
        chmod +x REFERENCE_LIBRARY/quality-management/master-quality-validator.sh
        ./REFERENCE_LIBRARY/quality-management/master-quality-validator.sh
    
    - name: Upload Report
      uses: actions/upload-artifact@v3
      with:
        name: quality-report
        path: REFERENCE_LIBRARY/quality-management/reports/
```

## 📈 **성능 최적화**

### **검증 속도 향상**
- 대용량 파일 (> 1MB) 제외
- 병렬 처리 적용
- 캐시 활용으로 중복 계산 방지
- 점진적 검증 (변경된 파일만)

### **리소스 사용 최적화**
- 메모리 사용량 모니터링
- 임시 파일 자동 정리
- 검증 결과 압축 저장

---

**🎯 최종 목표**: 완전 자동화된 품질 관리로 REFERENCE_LIBRARY의 지속적 품질 보장

*작성일: 2025-08-26 | 버전: v1.0*