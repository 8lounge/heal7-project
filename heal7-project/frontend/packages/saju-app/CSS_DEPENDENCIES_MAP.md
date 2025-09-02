# 🎨 CSS 클래스 의존성 매핑

## 핵심 CSS 클래스 시스템

### 🌟 테마 기반 클래스
- **`btn-cosmic`**: 인디고-퍼플 그라데이션 버튼 (basic 모드용)
- **`btn-mystic`**: 퍼플-핑크 그라데이션 버튼 (cyber_fantasy 모드용)
- **`btn-outline`**: 테두리 버튼 (호버 시 채움 효과)

### 🪟 카드 시스템
- **`card-glass`**: 반투명 블러 카드 (범용)
- **`card-cosmic`**: 코스믹 그라데이션 카드 (basic 모드)
- **`card-crystal`**: 크리스탈 효과 카드 (cyber_fantasy 모드)

### 🎯 텍스트 스타일
- **`text-cosmic`**: 화이트 텍스트 (basic 모드)
- **`text-mystic`**: 화이트 텍스트 (cyber_fantasy 모드)
- **`text-shadow-glow`**: 글로우 효과 텍스트

### ✨ 특수 효과
- **`glow-effect`**: 펄스 글로우 애니메이션
- **`holographic-effect`**: 홀로그래픽 스캔 효과
- **`level-badge`**: 게이미피케이션 레벨 배지

### 🌈 오행 컬러 시스템
- **`wood-gradient`**: 목(木) - 초록계열
- **`fire-gradient`**: 화(火) - 빨강계열  
- **`earth-gradient`**: 토(土) - 노랑계열
- **`metal-gradient`**: 금(金) - 회색계열
- **`water-gradient`**: 수(水) - 파랑계열

### 📱 모바일 최적화
- **`mobile-touch`**: 터치 최적화 (44px 최소 크기)
- **`scrollbar-hide`**: 스크롤바 숨김
- **`mobile-nav-scroll`**: 모바일 네비게이션 스크롤
- **`touch-scroll`**: 터치 스크롤 최적화

### 🎨 관리자 페이지 전용
- **`admin-select`**: 관리자 셀렉트 박스
- **`admin-input`**: 관리자 인풋 필드
- **`admin-textarea`**: 관리자 텍스트 영역

## ViewMode 분기 패턴

```typescript
// 컴포넌트에서 사용하는 일반적인 패턴
const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
const buttonClass = viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white'
```

## 라우터 전환 시 보존 필수 요소

1. **CSS 변수 시스템**: `:root` 내 모든 커스텀 프로퍼티
2. **ViewMode 분기 로직**: 모든 컴포넌트의 테마 전환 로직  
3. **애니메이션 클래스**: Framer Motion과 연동된 모든 클래스
4. **반응형 클래스**: `hidden md:flex` 등 모바일/데스크톱 분기

## 위험 요소

- **동적 클래스명**: 템플릿 리터럴로 생성되는 클래스들
- **조건부 클래스**: 삼항연산자로 분기되는 클래스들
- **애니메이션 연동**: `layoutId`, `key` prop과 연결된 클래스들