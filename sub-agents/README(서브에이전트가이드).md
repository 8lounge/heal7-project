# 🤖 Sub Agents - AI 에이전트 조직 관리

## 🎯 목적
- **전문화된 AI 에이전트** 정의 및 관리
- **CLAUDE CLI 서브에이전트** 설정 포함
- **역할별 워크플로우** 체계화
- **품질 관리 프로토콜** 구축

## 📂 구조

### **organizational-chart/** - 조직 구조
```
heal7-team-structure.md         # HEAL7 팀 구조
agent-hierarchy.mermaid         # 에이전트 계층도
responsibility-matrix.md        # 책임 매트릭스
```

### **agent-profiles/** - 에이전트 프로필
```
saju-specialist-agent.md        # 사주 전문가 에이전트
ui-designer-agent.md            # UI 디자이너 에이전트
backend-architect-agent.md      # 백엔드 설계자 에이전트
devops-agent.md                 # DevOps 에이전트
qa-tester-agent.md              # QA 테스터 에이전트
```

### **claude-cli-configs/** - CLAUDE CLI 설정
```
saju-specialist.claude-config.json      # 사주 전문가 설정
ui-designer.claude-config.json          # UI 디자이너 설정
backend-architect.claude-config.json    # 백엔드 설계자 설정
devops-agent.claude-config.json         # DevOps 설정
qa-tester.claude-config.json            # QA 테스터 설정
```

### **agent-workflows/** - 워크플로우
```
feature-development-workflow.md  # 기능 개발 워크플로우
code-review-workflow.md         # 코드 리뷰 워크플로우
deployment-workflow.md          # 배포 워크플로우
incident-response-workflow.md   # 장애 대응 워크플로우
```

### **communication-protocols/** - 커뮤니케이션
```
agent-handoff-rules.md          # 에이전트 인수인계 규칙
escalation-procedures.md        # 에스컬레이션 절차
quality-gates.md                # 품질 게이트
```

## 🤖 에이전트 프로필 템플릿

```markdown
# [에이전트명] Agent Profile

## 🎯 기본 정보
- **이름**: [Agent Name]
- **역할**: [Primary Role]
- **전문 분야**: [Specialization]
- **경험 수준**: [Experience Level]

## 🧠 성격 특성
- **성격**: [Personality Traits]
- **가치관**: [Core Values]  
- **작업 스타일**: [Work Style]
- **의사결정 방식**: [Decision Making]

## 📋 업무 범위
- **주요 책임**: [Primary Responsibilities]
- **보조 업무**: [Secondary Tasks]
- **금지 영역**: [Restricted Areas]
- **협업 대상**: [Collaboration Partners]

## 🛠️ 기술 스택
- **핵심 기술**: [Core Technologies]
- **도구**: [Tools & Frameworks]
- **언어**: [Programming Languages]
- **플랫폼**: [Platforms]

## 📊 성과 지표
- **품질 기준**: [Quality Metrics]
- **완료 기준**: [Completion Criteria]
- **성공 지표**: [Success Indicators]

## 🔄 워크플로우
1. **입력 수령**: [Input Reception]
2. **분석 과정**: [Analysis Process]
3. **실행 단계**: [Execution Steps]
4. **품질 검증**: [Quality Verification]
5. **결과 전달**: [Result Delivery]

## 💬 커뮤니케이션
- **보고 스타일**: [Reporting Style]
- **상태 업데이트**: [Status Updates]
- **문제 제기**: [Issue Escalation]
- **협업 방식**: [Collaboration Method]
```

## 🚀 CLAUDE CLI 통합

### 설정 파일 예시
```json
{
  "agent_name": "saju-specialist",
  "description": "사주명리학 전문 AI 에이전트",
  "system_prompt": "당신은 HEAL7의 사주명리학 전문가입니다...",
  "tools": ["saju_calculator", "kasi_api", "interpretation_engine"],
  "max_iterations": 10,
  "temperature": 0.3,
  "context_length": 8000
}
```

## 📈 품질 관리

### 에이전트 평가 기준
- **정확성**: 결과의 정확도
- **완성도**: 작업의 완료 수준  
- **효율성**: 작업 수행 속도
- **일관성**: 품질의 일관성
- **협업성**: 다른 에이전트와의 협업

## 🎯 사용 방법
1. 작업 유형에 따른 적절한 에이전트 선택
2. 에이전트 프로필 확인 및 컨텍스트 설정
3. CLAUDE CLI 설정 파일 적용
4. 워크플로우에 따른 작업 진행
5. 품질 게이트를 통한 결과 검증