# 🧠 Core Logic - 원자 단위 비즈니스 로직

## 🎯 목적
- **단일 책임 원칙**을 따르는 원자 단위 로직
- **5분 내 이해** 가능한 복잡도
- **재사용성** 극대화
- **외부 의존성** 최소화

## 📂 구조

### **saju-calculation/** - 사주 계산 로직
```
gapja-calculator.atomic.py      # 60갑자 계산
lunar-solar-converter.atomic.py # 음력-양력 변환
five-elements-analyzer.atomic.py # 오행 분석
gyeokguk-determiner.atomic.py   # 격국 판정
```

### **ai-interpretation/** - AI 해석 로직
```
personality-analyzer.atomic.py   # 성격 분석
fortune-predictor.atomic.py     # 운세 예측
compatibility-matcher.atomic.py # 궁합 매칭
```

### **data-validation/** - 데이터 검증 로직
```
birth-data-validator.atomic.py  # 생년월일 검증
saju-result-validator.atomic.py # 사주 결과 검증
user-input-sanitizer.atomic.py  # 사용자 입력 정화
```

### **business-logic/** - 비즈니스 로직
```
user-registration.atomic.py     # 사용자 등록
payment-processor.atomic.py     # 결제 처리
subscription-manager.atomic.py  # 구독 관리
```

### **algorithms/** - 알고리즘
```
recommendation-engine.atomic.py # 추천 엔진
content-filter.atomic.py        # 콘텐츠 필터
analytics-tracker.atomic.py     # 분석 추적
```

## 🎯 파일 규칙

### **.atomic.*** 확장자
- 하나의 기능만 담당
- 외부 의존성 최소화
- 입력-출력 명확히 정의
- 단위 테스트 100% 커버리지

### 파일 구조 템플릿
```python
"""
원자 모듈: [정확한 기능명]
입력: [INPUT - 받는 매개변수]
출력: [OUTPUT - 반환하는 값]
로직: [LOGIC - 핵심 처리 과정]
"""

def atomic_function(input_param):
    """
    단일 책임을 가진 원자 함수
    
    Args:
        input_param: 입력 매개변수 설명
        
    Returns:
        expected_output: 출력 값 설명
        
    Raises:
        SpecificException: 예외 상황 설명
    """
    # 입력 검증
    if not input_param:
        raise ValueError("Invalid input")
    
    # 핵심 로직 (단순하고 명확하게)
    result = process_core_logic(input_param)
    
    # 출력 검증
    validate_output(result)
    
    return result

def test_atomic_function():
    """단위 테스트"""
    # 정상 케이스
    assert atomic_function("valid_input") == "expected_output"
    
    # 예외 케이스  
    with pytest.raises(ValueError):
        atomic_function(None)
```

## 🚀 사용 방법
1. 기능별 폴더에서 .atomic 파일 탐색
2. 필요한 원자 함수 확인
3. 다른 모듈에서 import하여 조합
4. 복잡한 기능을 원자 함수들의 조합으로 구현

## ✅ 품질 기준
- [ ] 단일 책임만 수행
- [ ] 5분 내 완전 이해 가능
- [ ] 외부 의존성 최소화
- [ ] 입출력 명확히 정의
- [ ] 단위 테스트 포함
- [ ] 예외 처리 완비