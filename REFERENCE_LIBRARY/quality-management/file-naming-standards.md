# 📝 REFERENCE_LIBRARY 파일명 표준화 가이드

> **목적**: REFERENCE_LIBRARY 내 모든 파일의 명명 규칙 통일  
> **적용 범위**: 신규 파일 및 기존 파일 리네이밍  
> **업데이트**: 2025-08-26

## 🎯 **표준 명명 규칙**

### **기본 구조**
```
[Category]-[Function]-v[Version]([Korean-Description]).[Extension]
```

### **세부 규칙**

#### **1. Category (카테고리)**
- **Sample**: 완성 코드 샘플
- **Core**: 핵심 로직 모듈  
- **Arch**: 아키텍처 다이어그램
- **Spec**: 기능 명세서
- **Agent**: AI 에이전트 관련
- **Ref**: 참조 문서
- **Research**: 연구 자료
- **Guide**: 가이드 문서

#### **2. Function (기능명)**
- **PascalCase** 사용 (예: UserAuth, SajuCalculator)
- **하이픈(-)으로 구분** (예: User-Authentication)
- **약어 지양**, 명확한 전체명 사용

#### **3. Version (버전)**
- **-v[Major].[Minor]** 형식
- **Major**: 큰 변경사항 (1, 2, 3...)
- **Minor**: 소규모 수정 (.0, .1, .2...)
- 예: `-v1.0`, `-v2.1`, `-v3.0`

#### **4. Korean Description (한글 설명)**
- **괄호 안에 한글로 명시**
- **간결하고 명확한 설명**
- **띄어쓰기 없이 연결**

#### **5. Extension (확장자)**
- **.complete.[ext]**: 즉시 사용 가능한 완성 코드
- **.atomic.[ext]**: 원자 단위 로직
- **.spec.md**: 명세서
- **.guide.md**: 가이드
- **.mermaid**: 다이어그램

## 📋 **표준화 대상 파일 목록**

### **_guides/ 폴더**
```
현재: HEAL7_MZ_PLATFORM_MASTER_INDEX-v4.0(HEAL7_MZ플랫폼마스터색인).md
권장: Guide-MZ-Platform-Master-Index-v4.0(MZ플랫폼마스터색인).md

현재: SAJU_SITE_RENOVATION_MASTER_INDEX-v1.0(사주사이트개편마스터색인).md  
권장: Guide-Saju-Site-Renovation-Master-Index-v1.0(사주사이트개편마스터색인).md

현재: 사주사이트완전구현가이드-v2.0(HEAL7_MZ운세플랫폼_개발명세서).md
권장: Guide-Saju-Site-Complete-Implementation-v2.0(사주사이트완전구현가이드).md
```

### **architecture-diagrams/ 폴더**
```
현재: AI-Document-Composition-Engine-v2.0(AI문서조합엔진).complete.md
권장: Arch-AI-Document-Composition-Engine-v2.0(AI문서조합엔진).complete.md

현재: Government-Portal-Intelligence-System-v2.0(정부포털지능화시스템).complete.md
권장: Arch-Government-Portal-Intelligence-System-v2.0(정부포털지능화시스템).complete.md
```

### **feature-specs/ 폴더**
```
현재: Institution-Requirements-Database-v2.0(기관별요구사항데이터베이스).complete.md
권장: Spec-Institution-Requirements-Database-v2.0(기관별요구사항데이터베이스).complete.md

현재: language-pipeline-spec(언어파이프라인명세).complete.md
권장: Spec-Language-Pipeline-v1.0(언어파이프라인명세).complete.md
```

### **sample-codes/ 폴더**
```
현재: KeywordMatrix3D(3D키워드매트릭스).complete.html
권장: Sample-KeywordMatrix3D-v1.0(3D키워드매트릭스).complete.html

현재: ai-model-selector(AI모델선택기).complete.tsx
권장: Sample-AI-Model-Selector-v1.0(AI모델선택기).complete.tsx
```

## 🔧 **리네이밍 스크립트**

### **자동 리네이밍 명령어**
```bash
#!/bin/bash
# REFERENCE_LIBRARY 파일명 표준화 스크립트

# _guides 폴더
cd /home/ubuntu/REFERENCE_LIBRARY/_guides/
mv "HEAL7_MZ_PLATFORM_MASTER_INDEX-v4.0(HEAL7_MZ플랫폼마스터색인).md" "Guide-MZ-Platform-Master-Index-v4.0(MZ플랫폼마스터색인).md"
mv "SAJU_SITE_RENOVATION_MASTER_INDEX-v1.0(사주사이트개편마스터색인).md" "Guide-Saju-Site-Renovation-Master-Index-v1.0(사주사이트개편마스터색인).md"

# sample-codes 폴더
cd /home/ubuntu/REFERENCE_LIBRARY/sample-codes/react-components/
mv "KeywordMatrix3D(3D키워드매트릭스).complete.html" "Sample-KeywordMatrix3D-v1.0(3D키워드매트릭스).complete.html"
mv "ai-model-selector(AI모델선택기).complete.tsx" "Sample-AI-Model-Selector-v1.0(AI모델선택기).complete.tsx"
mv "SajuCrystal3D(사주크리스탈3D).complete.tsx" "Sample-SajuCrystal3D-v1.0(사주크리스탈3D).complete.tsx"

# architecture-diagrams 폴더 - 핵심 파일들만
cd /home/ubuntu/REFERENCE_LIBRARY/architecture-diagrams/frameworks/
mv "AI-Document-Composition-Engine-v2.0(AI문서조합엔진).complete.md" "Arch-AI-Document-Composition-Engine-v2.0(AI문서조합엔진).complete.md"
```

## ✅ **검증 체크리스트**

### **파일명 품질 기준**
- [ ] Category-Function-Version(Korean).Extension 형식 준수
- [ ] 버전 표기 통일 (-v1.0, -v2.1 형식)
- [ ] 한글 설명 간결하고 명확
- [ ] 확장자가 파일 성격과 일치 (.complete, .atomic, .spec 등)
- [ ] 폴더 구조와 파일명이 논리적으로 일치

### **우선순위**
1. **고우선순위**: _guides/, sample-codes/ 폴더
2. **중우선순위**: architecture-diagrams/, feature-specs/ 폴더  
3. **저우선순위**: reference-docs/, research-docs/ 폴더

## 📅 **단계별 실행 계획**

### **1단계 (즉시 적용)**: 핵심 파일 리네이밍
- _guides/ 폴더의 마스터 가이드 파일들
- sample-codes/ 폴더의 .complete 파일들
- 자주 참조되는 아키텍처 문서들

### **2단계 (1주 내)**: 전체 구조 표준화
- 모든 폴더의 파일명 표준화
- 깨진 링크 수정
- 문서 내 참조 경로 업데이트

### **3단계 (지속)**: 신규 파일 품질 관리
- 신규 파일 생성 시 표준 적용
- 정기적 품질 검증
- 자동화 도구 활용

---

**🎯 목표**: 모든 파일이 일관된 명명 규칙을 따라 AI와 개발자가 쉽게 탐색하고 활용할 수 있는 구조 완성

*작성일: 2025-08-26 | 버전: v1.0*