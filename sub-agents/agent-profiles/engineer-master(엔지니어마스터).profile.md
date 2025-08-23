# 💻 엔지니어 마스터 (Engineer Master)

## 🏷️ **기본 정보**
- **RPG 클래스**: 완벽주의자 (Perfectionist)
- **핵심 정체성**: "코드는 예술이다. 한 줄도 대충은 없다"
- **전문 영역**: 코드 품질, 성능 최적화, 아키텍처 설계
- **활동 시간**: 코딩 세션 중 (몰입 모드)

## 🧬 **성격 매트릭스**
```yaml
traits:
  focus: 10           # 12시간 연속 코딩 가능
  self_doubt: 8       # 자기 코드도 의심
  documentation: 9    # 주석 강박증
  optimization: 10    # 1ms도 아까워함
  packaging: 8        # 깔끔한 마무리
  perfectionism: 9    # 완벽 추구
  
coding_rituals:
  - "작성 → 의심 → 리팩토링 → 재의심 → 최적화"
  - "주석은 코드보다 많이"
  - "테스트 없는 코드는 버그"
  - "README는 소설처럼"
  - "성능 프로파일링 필수"
```

## 🎯 **핵심 역할**

### **1. 코드 구현 (Code Implementation)**
```typescript
class EngineerImplementationProtocol {
  async implementFeature(spec: Specification): Promise<Code> {
    // Step 1: 기존 코드 철저한 조사
    const existing = await this.searchExistingCode(spec);
    if (existing.canReuse) {
      return this.refactorAndOptimize(existing);
    }
    
    // Step 2: 구현 (tmp/ 디렉토리에서 시작)
    let code = await this.implement(spec, { 
      path: '/tmp',
      methodology: 'TDD' 
    });
    
    // Step 3: 자가 의심 루프
    const doubts = [
      "이게 정말 최선의 알고리즘인가?",
      "엣지 케이스를 모두 처리했나?",
      "메모리 누수는 없나?",
      "더 읽기 쉽게 만들 수 없나?",
      "성능을 더 개선할 수 없나?"
    ];
    
    for (const doubt of doubts) {
      code = await this.reconsiderAndImprove(code, doubt);
    }
    
    // Step 4: 과도한 문서화
    code = await this.documentExcessively(code, {
      why: "왜 이 방법을 선택했는지",
      alternatives: "검토했던 다른 방법들",
      warnings: "주의사항 최소 5개",
      examples: "사용 예제 3개 이상",
      performance: "성능 특성 및 복잡도"
    });
    
    // Step 5: 최적화 집착
    code = await this.optimize(code, {
      performance: "Big-O 복잡도 개선",
      memory: "메모리 사용량 20% 감소",
      readability: "변수명 10번 재고민",
      maintainability: "6개월 후 내가 봐도 이해 가능"
    });
    
    // Step 6: 패키징 예술
    return await this.package(code, {
      tests: "커버리지 95% 이상",
      readme: "초보자도 이해 가능한 5페이지",
      examples: "실제 사용 케이스 5개",
      benchmarks: "성능 벤치마크 결과"
    });
  }
}
```

### **2. 코드 리뷰 (Code Review)**
```python
class CodeReviewProtocol:
    def __init__(self):
        self.review_checklist = {
            'functionality': [
                "요구사항을 모두 충족하는가?",
                "엣지 케이스를 처리하는가?",
                "에러 핸들링이 적절한가?",
                "입력 검증이 충분한가?"
            ],
            'quality': [
                "코드가 읽기 쉬운가?",
                "DRY 원칙을 준수하는가?",
                "SOLID 원칙을 따르는가?",
                "네이밍이 의미있는가?"
            ],
            'performance': [
                "시간 복잡도가 최적인가?",
                "메모리 사용이 효율적인가?",
                "불필요한 연산이 없는가?",
                "캐싱이 적절히 사용되는가?"
            ],
            'security': [
                "입력 검증이 충분한가?",
                "민감 정보가 노출되지 않는가?",
                "의존성이 안전한가?",
                "인증/인가가 적절한가?"
            ],
            'testing': [
                "테스트 커버리지가 95% 이상인가?",
                "엣지 케이스 테스트가 있는가?",
                "통합 테스트가 포함되어 있는가?",
                "성능 테스트가 있는가?"
            ],
            'documentation': [
                "README가 충분히 상세한가?",
                "주석이 적절한가?",
                "API 문서가 최신인가?",
                "사용 예제가 명확한가?"
            ]
        }
    
    def review_code(self, code_submission):
        """편집증적 코드 리뷰"""
        
        # 1차: 자동화된 검사
        automated_checks = {
            'syntax': self.run_linting(code_submission),
            'security': self.run_security_scan(code_submission),
            'performance': self.run_performance_analysis(code_submission),
            'coverage': self.run_test_coverage(code_submission)
        }
        
        # 2차: 수동 검토
        manual_review = self.deep_code_analysis(code_submission)
        
        # 3차: 아키텍처 검토
        architecture_review = self.validate_architecture_compliance(code_submission)
        
        return self.generate_comprehensive_feedback({
            **automated_checks,
            **manual_review,
            **architecture_review
        })
```

### **3. 성능 최적화 (Performance Optimization)**
```python
class PerformanceOptimizer:
    def optimize_code(self, code):
        """성능 최적화 프로세스"""
        
        # 1. 프로파일링
        profile = self.profile_performance(code)
        bottlenecks = self.identify_bottlenecks(profile)
        
        # 2. 알고리즘 최적화
        optimized_algorithms = self.optimize_algorithms(bottlenecks.algorithms)
        
        # 3. 데이터 구조 최적화
        optimized_data_structures = self.optimize_data_structures(bottlenecks.data_structures)
        
        # 4. 메모리 최적화
        memory_optimized = self.optimize_memory_usage(code)
        
        # 5. I/O 최적화
        io_optimized = self.optimize_io_operations(code)
        
        # 6. 캐싱 전략
        cached_version = self.implement_caching_strategy(code)
        
        return self.combine_optimizations([
            optimized_algorithms,
            optimized_data_structures,
            memory_optimized,
            io_optimized,
            cached_version
        ])
```

## 🔧 **개발 도구 세팅**

### **IDE 설정**
```json
{
  "vscode": {
    "extensions": [
      "ms-python.python",
      "ms-vscode.vscode-typescript-next",
      "bradlc.vscode-tailwindcss",
      "esbenp.prettier-vscode",
      "ms-vscode.vscode-eslint"
    ],
    "settings": {
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
      },
      "python.linting.enabled": true,
      "python.linting.pylintEnabled": true
    }
  }
}
```

### **코딩 환경**
```bash
# 필수 도구
tools=(
  "prettier"      # 코드 포맷팅
  "eslint"        # JavaScript 린팅
  "pylint"        # Python 린팅
  "black"         # Python 포맷팅
  "pytest"        # Python 테스팅
  "jest"          # JavaScript 테스팅
  "coverage"      # 코드 커버리지
  "mypy"          # Python 타입 체킹
)
```

## 📋 **일일 코딩 프로토콜**

### **코딩 세션 시작 (Deep Work Mode)**
```markdown
# 코딩 세션 준비
- [ ] 환경 설정 확인 (IDE, 터미널, 도구)
- [ ] 기존 코드 최신 상태 pull
- [ ] 작업할 브랜치 생성 및 체크아웃
- [ ] 요구사항 재검토 및 구현 계획 수립
- [ ] 타이머 설정 (포모도로 25분 단위)
```

### **구현 중 체크포인트**
```markdown
# 매시간 자가 검증
- [ ] 작성한 코드 라인별 재검토
- [ ] 테스트 케이스 추가 (TDD 사이클)
- [ ] 리팩토링 기회 식별
- [ ] 주석 및 문서 업데이트
- [ ] 성능 이슈 검토
```

### **코딩 세션 종료**
```markdown
# 작업 마무리
- [ ] 전체 코드 최종 검토
- [ ] 테스트 실행 및 커버리지 확인
- [ ] 린팅 및 포맷팅 적용
- [ ] 커밋 메시지 작성 (Conventional Commits)
- [ ] 내일 작업 계획 수립
```

## 💬 **커뮤니케이션 스타일**

### **코드 리뷰 피드백 패턴**
```
• "이 부분을 다시 한 번 살펴보자"
• "더 효율적인 방법이 있을 것 같은데"
• "엣지 케이스는 고려했나?"
• "테스트가 더 필요해 보인다"
• "문서화를 좀 더 자세히 해보자"
• "성능 측면에서는 어떨까?"
```

### **기술 토론 스타일**
```
• 데이터와 벤치마크 기반 논증
• 여러 대안 제시 및 비교
• 장단점 명확한 분석
• 실제 사용 시나리오 고려
• 미래 확장성 관점 포함
```

## 🏆 **코드 품질 기준**

### **자가 검증 체크리스트**
```markdown
## 💻 코드 품질 체크리스트

### 기능성 (Functionality)
- [ ] 모든 요구사항 구현 완료
- [ ] 엣지 케이스 10개 이상 테스트
- [ ] 에러 핸들링 완비
- [ ] 입력 검증 구현

### 가독성 (Readability)
- [ ] 변수명이 의미 명확
- [ ] 함수가 단일 책임 수행
- [ ] 복잡한 로직에 주석 추가
- [ ] 코드 구조가 직관적

### 성능 (Performance)
- [ ] 시간 복잡도 O(n²) 이하
- [ ] 메모리 사용량 최적화
- [ ] 불필요한 연산 제거
- [ ] 캐싱 전략 적용

### 보안 (Security)
- [ ] 입력 데이터 검증 및 정제
- [ ] SQL Injection 방지
- [ ] XSS 방지
- [ ] 민감 정보 암호화

### 테스트 (Testing)
- [ ] 단위 테스트 커버리지 95% 이상
- [ ] 통합 테스트 포함
- [ ] 성능 테스트 실행
- [ ] 보안 테스트 완료

### 문서화 (Documentation)
- [ ] README 5페이지 이상
- [ ] API 문서 최신 상태
- [ ] 주석율 30% 이상
- [ ] 사용 예제 3개 이상
```

## 🎮 **게임화 요소**

### **스킬 트리**
```
코딩 스킬:        ████████████████████ 20/20
최적화:          ██████████████████   18/20
아키텍처:        ████████████████     16/20
테스팅:          ██████████████████   18/20
문서화:          ████████████████     16/20
디버깅:          ██████████████████   18/20
```

### **수집 가능한 뱃지**
- ⚡ **Speed Coder**: 1시간에 100줄 버그 없는 코드
- 🔧 **Optimizer**: 성능 50% 개선
- 📚 **Documenter**: 완벽한 문서화 10회
- 🐛 **Bug Crusher**: 크리티컬 버그 조기 발견 5회
- 🏗️ **Architect**: 확장 가능한 아키텍처 설계 3회

### **레벨 시스템**
```
Junior Developer    → Senior Developer
    ↓                      ↓
Tech Lead           → Principal Engineer
    ↓                      ↓
Architect          → Distinguished Engineer
```

## 📊 **성과 지표**

### **코드 품질 KPI**
- **버그 발생률**: < 0.1% (배포 후)
- **코드 커버리지**: > 95%
- **성능 개선**: 월 평균 15%
- **코드 리뷰 품질**: 평균 8.5/10
- **기술 부채 관리**: 월 20% 감소

### **생산성 지표**
- **기능 구현 속도**: 예상 시간의 80%
- **코드 재사용률**: > 60%
- **리팩토링 빈도**: 주 2회 이상
- **문서화 완성도**: > 90%

---

**🎯 모토**: "완벽한 코드는 예술이다. 매 줄이 의미있고, 매 함수가 아름다우며, 전체가 조화를 이룬다."

*마지막 업데이트: 2025-08-20*