# 🚀 HEAL7 CORE 사용 가이드

> **핵심 원칙**: AI가 70-80% 수정 없이 95% 완성도로 모듈을 구현할 수 있는 환경 조성

## 🎯 **사용 시나리오별 가이드**

### **📚 새로운 기능 개발 시**

#### **1단계: 요구사항 정의**
```bash
# feature-specs/에서 유사한 기능 명세 확인
ls /home/ubuntu/CORE/feature-specs/user-features/
# 기존 명세를 템플릿으로 활용하여 새 기능 명세 작성
```

#### **2단계: 아키텍처 설계**
```bash
# architecture-diagrams/에서 시스템 구조 확인
cat /home/ubuntu/CORE/architecture-diagrams/system-architecture/heal7-overall-system.mermaid
# 새 기능이 전체 시스템에 미치는 영향 분석
```

#### **3단계: 코드 모듈 확인**
```bash
# 기존 완성 코드 확인
ls /home/ubuntu/CORE/sample-codes/react-components/*.complete.tsx
ls /home/ubuntu/CORE/core-logic/saju-calculation/*.atomic.py
# 재사용 가능한 모듈 식별
```

#### **4단계: 개발 진행**
- **AI 에이전트 선택**: sub-agents/에서 적절한 전문 에이전트 프로필 확인
- **단일 모듈 집중**: 한 번에 하나의 .complete 또는 .atomic 파일만 작업
- **즉시 저장**: 완성 즉시 적절한 CORE/ 카테고리에 보관

### **🎨 UI/UX 개발 시**

#### **1단계: 시각적 참조**
```bash
# 화면 이미지로 정확한 디자인 확인
ls /home/ubuntu/CORE/screen-images/desktop-views/
ls /home/ubuntu/CORE/screen-images/component-references/
```

#### **2단계: 디자인 시스템 확인**
```bash
# 기존 컴포넌트 코드 확인
ls /home/ubuntu/CORE/sample-codes/react-components/
# 디자인 토큰과 스타일 가이드 확인
```

#### **3단계: 컴포넌트 개발**
```bash
# UI 디자이너 에이전트 설정 활용
cat /home/ubuntu/CORE/sub-agents/agent-profiles/ui-designer-agent.md
# .complete.tsx 파일로 완성 후 저장
```

### **🧠 비즈니스 로직 개발 시**

#### **1단계: 핵심 로직 확인**
```bash
# 관련 원자 모듈 탐색
ls /home/ubuntu/CORE/core-logic/saju-calculation/
ls /home/ubuntu/CORE/core-logic/ai-interpretation/
```

#### **2단계: 테스트 케이스 확인**
```bash
# 기존 .atomic 파일에서 테스트 패턴 확인
# 검증된 알고리즘과 예외 처리 패턴 학습
```

#### **3단계: 원자 모듈 개발**
- **단일 책임**: 하나의 기능만 담당하는 .atomic 모듈 생성
- **5분 규칙**: 5분 내 완전히 이해 가능한 복잡도 유지
- **테스트 포함**: 단위 테스트 100% 커버리지

### **🤖 AI 에이전트 활용 시**

#### **전문 에이전트 선택**
```bash
# 작업 유형별 적절한 에이전트 확인
cat /home/ubuntu/CORE/sub-agents/agent-profiles/saju-specialist-agent.md    # 사주 관련
cat /home/ubuntu/CORE/sub-agents/agent-profiles/backend-architect-agent.md  # 백엔드
cat /home/ubuntu/CORE/sub-agents/agent-profiles/ui-designer-agent.md        # 프론트엔드
```

#### **CLAUDE CLI 설정 적용**
```bash
# 에이전트별 설정 파일 활용
ls /home/ubuntu/CORE/sub-agents/claude-cli-configs/
# 특화된 프롬프트와 도구 설정 적용
```

### **📊 데이터 분석 및 연구 시**

#### **시장 조사**
```bash
# 기존 연구 자료 확인
ls /home/ubuntu/CORE/research-docs/market-research/
ls /home/ubuntu/CORE/research-docs/user-research/
```

#### **기술 동향 파악**
```bash
# 최신 기술 연구 자료 확인
ls /home/ubuntu/CORE/research-docs/technology-research/
# 구현 방안과 ROI 분석 참고
```

## 🔧 **일반적인 작업 플로우**

### **💻 개발 세션 시작**
```bash
# 1. 관련 CORE 폴더 확인
ls /home/ubuntu/CORE/[관련-카테고리]/

# 2. 기존 자산 탐색
find /home/ubuntu/CORE/ -name "*[키워드]*" -type f

# 3. 참조 문서 확인
cat /home/ubuntu/CORE/reference-docs/technical-standards/heal7-coding-standards.md

# 4. 에이전트 프로필 로드 (필요 시)
cat /home/ubuntu/CORE/sub-agents/agent-profiles/[적절한-에이전트].md
```

### **🔄 개발 진행**
1. **컨텍스트 최소화**: 필요한 모듈과 참조만 로드
2. **단일 집중**: 한 번에 하나의 완성 단위만 작업
3. **즉시 검증**: 완성 즉시 테스트 케이스로 검증
4. **적절한 저장**: 완성된 모듈을 적절한 CORE/ 위치에 저장

### **✅ 품질 검증**
```bash
# 코드 품질 검증
# - .complete 파일: 복사-붙여넣기로 즉시 동작하는지 확인
# - .atomic 파일: 단일 책임, 5분 이해 가능 확인
# - 테스트 케이스: 모든 경우의 수 커버 확인

# 문서화 확인
# - 목적(WHY), 방법(HOW), 내용(WHAT) 명확 기술
# - 의존성과 사용법 명시
# - 변경 이력 업데이트
```

## 📁 **파일 명명 규칙**

### **코드 파일**
```
[기능명].complete.[확장자]    # 즉시 사용 가능한 완성 코드
[로직명].atomic.[확장자]      # 원자 단위 로직 모듈
[설정명].config.[확장자]      # 설정 파일
```

### **문서 파일**
```
[주제명].spec.md             # 명세서
[주제명].guide.md            # 가이드 문서
[주제명].research.md         # 연구 보고서
[다이어그램명].mermaid       # 다이어그램 파일
```

### **이미지 파일**
```
[화면명]-[디바이스].png      # 화면 스크린샷
[컴포넌트명]-[상태].png      # 컴포넌트 참조
[플로우명]-[단계].png        # 사용자 플로우
```

## 🎯 **효과적 활용 팁**

### **검색 활용**
```bash
# 키워드로 관련 자료 찾기
find /home/ubuntu/CORE/ -name "*사주*" -type f
find /home/ubuntu/CORE/ -name "*auth*" -type f
grep -r "JWT" /home/ubuntu/CORE/

# 파일 타입별 검색
find /home/ubuntu/CORE/ -name "*.complete.*"
find /home/ubuntu/CORE/ -name "*.atomic.*"
find /home/ubuntu/CORE/ -name "*.mermaid"
```

### **재사용 우선 원칙**
1. **기존 확인**: 새로 만들기 전에 CORE/에서 기존 자산 확인
2. **조합 활용**: 여러 .atomic 모듈을 조합하여 복합 기능 구현
3. **확장 개선**: 기존 .complete 파일을 베이스로 확장 개발

### **문서화 습관**
- **즉시 문서화**: 개발과 동시에 문서 업데이트
- **의도 기록**: 왜 이렇게 구현했는지 WHY 중심 기록
- **사용 예시**: 실제 사용 가능한 예시 코드 포함

## ⚠️ **주의사항**

### **❌ 하지 말아야 할 것들**
- CORE/ 폴더에 임시 파일이나 테스트 파일 저장
- 미완성 코드를 .complete 확장자로 저장
- 복잡한 로직을 하나의 .atomic 파일에 구현
- 문서화 없이 코드만 저장

### **✅ 권장사항**
- 완성도 95% 이상 달성 후 CORE/에 저장
- 정기적으로 CORE/ 내용 검토 및 업데이트
- 팀원들과 CORE/ 활용법 공유
- 버전 관리를 통한 변경 이력 추적

---

**🎯 최종 목표**: AI가 CORE/의 자산을 활용하여 높은 완성도의 코드를 일관되게 생성할 수 있는 환경 구축

*작성일: 2025-08-18 | 버전: v1.0*