# 🖼️ Screen Images - 시각적 참조 자료

## 🎯 목적
- **정확한 UI 재현**을 위한 시각적 기준 제공
- **디자인 일관성** 유지를 위한 참조 이미지
- **사용자 플로우** 시각화
- **컴포넌트 라이브러리** 시각적 가이드

## 📂 구조

### **desktop-views/** - 데스크탑 화면
```
heal7-main-desktop.png          # 메인 페이지 데스크탑 뷰
saju-calculator-desktop.png     # 사주 계산기 데스크탑 뷰  
admin-dashboard-desktop.png     # 관리자 대시보드
user-profile-desktop.png        # 사용자 프로필 페이지
```

### **mobile-views/** - 모바일 화면
```
heal7-main-mobile.png           # 메인 페이지 모바일 뷰
saju-calculator-mobile.png      # 사주 계산기 모바일 뷰
navigation-mobile.png           # 모바일 내비게이션
```

### **component-references/** - 컴포넌트 참조
```
buttons-collection.png          # 버튼 컬렉션
cards-variations.png            # 카드 변형들
forms-layouts.png               # 폼 레이아웃들
loading-animations.gif          # 로딩 애니메이션들
```

### **user-flows/** - 사용자 플로우
```
registration-flow.png           # 회원가입 플로우
saju-consultation-flow.png      # 사주 상담 플로우
payment-flow.png               # 결제 플로우
```

### **design-inspiration/** - 디자인 영감
```
color-schemes.png               # 색상 조합
typography-examples.png         # 타이포그래피 예시
competitor-references/          # 경쟁사 참조 이미지들
```

## 🎨 이미지 기준

### **스크린샷 규격**
- **데스크탑**: 1920x1080 (또는 실제 해상도)
- **모바일**: 375x667 (iPhone SE 기준)
- **컴포넌트**: 최소 300x200, 배경 투명 또는 흰색
- **플로우**: 전체 과정이 한 눈에 보이는 크기

### **파일 명명 규칙**
```
[화면명]-[디바이스].png
[컴포넌트명]-[상태].png  
[플로우명]-[단계번호].png
[영감명]-[카테고리].png
```

### **품질 기준**
- **해상도**: 최소 72dpi, 권장 300dpi
- **포맷**: PNG (투명도 필요 시), JPG (일반 화면)
- **파일 크기**: 최대 5MB
- **명확성**: 텍스트와 요소들이 선명하게 보여야 함

## 📱 캡처 가이드

### **화면 캡처 시 주의사항**
1. **일관된 브라우저** 사용 (Chrome 권장)
2. **확장 프로그램** 비활성화
3. **개발자 도구** 닫기
4. **실제 데이터** 사용 (Lorem ipsum 지양)
5. **사용자 개인정보** 마스킹

### **컴포넌트 캡처**
1. **배경 제거** 또는 일관된 배경 사용
2. **다양한 상태** 캡처 (기본, hover, active, disabled)
3. **크기 변형** 포함 (small, medium, large)
4. **테마 변형** 포함 (light, dark)

## 🎯 활용 방법

### **UI 개발 시**
1. 해당 화면의 참조 이미지 확인
2. 픽셀 퍼펙트 매칭 목표
3. 반응형 대응을 위한 다중 해상도 확인

### **컴포넌트 개발 시**
1. component-references/ 에서 정확한 스타일 확인
2. 상태별 변화 구현
3. 일관성 있는 디자인 패턴 적용

### **사용자 경험 개선**
1. user-flows/ 를 통한 전체 여정 이해
2. 단계별 최적화 포인트 파악
3. 사용자 행동 패턴 분석

## ✅ 체크리스트
- [ ] 명확하고 선명한 이미지
- [ ] 일관된 캡처 환경
- [ ] 적절한 파일 명명
- [ ] 다양한 상태/크기 포함
- [ ] 개인정보 보호 확인
- [ ] 파일 크기 최적화