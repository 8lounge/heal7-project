# 🎨 Paperwork AI B2B 하이브리드 디자인 시스템

> **프로젝트**: AI 기반 B2B 하이브리드 문서 편집 플랫폼 디자인 시스템  
> **버전**: v3.0.0 - B2B 하이브리드 확장  
> **작성일**: 2025-08-22  
> **대상**: 디자이너, 프론트엔드 개발자, UX 연구원, B2B 제품 매니저

---

## 🎯 **1. 디자인 철학 (Design Philosophy)**

### **1.1 핵심 가치**

#### **직관성 (Intuitive)**
- **원칙**: 사용자가 학습 없이도 즉시 사용 가능한 인터페이스
- **구현**: 친숙한 패턴, 명확한 아이콘, 예측 가능한 동작
- **측정**: 첫 사용 성공률 > 90%, 도움말 참조율 < 10%

#### **효율성 (Efficient)**
- **원칙**: 최소한의 클릭으로 목표 달성
- **구현**: 단축키, 자동 완성, 스마트 기본값
- **측정**: 작업 완료 시간 < 5분, 클릭 수 < 15회

#### **접근성 (Accessible)**
- **원칙**: 모든 사용자가 차별 없이 사용 가능
- **구현**: WCAG 2.1 AA 준수, 다양한 입력 방식 지원
- **측정**: 접근성 점수 > 95%, 다양한 디바이스 호환성

#### **신뢰성 (Trustworthy)**
- **원칙**: 안전하고 예측 가능한 사용자 경험
- **구현**: 명확한 상태 표시, 오류 방지, 데이터 보호 알림
- **측정**: 오류 발생률 < 1%, 사용자 만족도 > 4.5/5

### **1.2 브랜드 아이덴티티**

#### **브랜드 성격**
- **Professional**: 비즈니스 환경에 적합한 전문성
- **Modern**: 최신 기술과 트렌드 반영
- **Friendly**: 접근하기 쉽고 친근한 느낌
- **Intelligent**: AI 기술의 똑똑함과 효율성

#### **브랜드 톤 앤 보이스**
- **명확함**: 복잡한 기능을 간단명료하게 설명
- **도움됨**: 사용자의 문제 해결에 집중
- **신뢰감**: 정확하고 안정적인 정보 제공
- **혁신성**: 새로운 가능성과 기회 제시

---

## 🎨 **2. 비주얼 디자인 시스템**

### **2.1 컬러 시스템 (Color System)**

#### **Primary Colors - 신뢰와 전문성**
```css
:root {
  /* Primary Blue - 메인 브랜드 컬러 */
  --primary-50:  #f0f9ff;   /* 극히 연한 파랑 - 배경 */
  --primary-100: #e0f2fe;   /* 연한 파랑 - 호버 배경 */
  --primary-200: #bae6fd;   /* 밝은 파랑 - 비활성 상태 */
  --primary-300: #7dd3fc;   /* 중간 파랑 - 보조 요소 */
  --primary-400: #38bdf8;   /* 선명한 파랑 - 액센트 */
  --primary-500: #3b82f6;   /* 메인 파랑 - 주 액션 */
  --primary-600: #2563eb;   /* 진한 파랑 - 호버 상태 */
  --primary-700: #1d4ed8;   /* 어두운 파랑 - 액티브 상태 */
  --primary-800: #1e40af;   /* 매우 진한 파랑 - 강조 */
  --primary-900: #1e3a8a;   /* 네이비 - 텍스트 */
}
```

#### **AI Model Colors - 각 AI별 고유 색상**
```css
:root {
  /* Google Gemini - 구글 블루/그린 */
  --gemini-primary:   #4285f4;
  --gemini-secondary: #34a853;
  --gemini-light:     #e8f0fe;
  
  /* OpenAI GPT - 오픈AI 그린 */
  --openai-primary:   #10a37f;
  --openai-secondary: #0d8f73;
  --openai-light:     #e6f7f3;
  
  /* Anthropic Claude - 앤스로픽 오렌지 */
  --claude-primary:   #d97706;
  --claude-secondary: #b45309;
  --claude-light:     #fef3e2;
  
  /* Perplexity - 퍼플렉시티 퍼플 */
  --perplexity-primary:   #8b5cf6;
  --perplexity-secondary: #7c3aed;
  --perplexity-light:     #f3f0ff;
  
  /* Naver ClovaX - 네이버 그린 */
  --clova-primary:   #03c75a;
  --clova-secondary: #00b04f;
  --clova-light:     #e6f9ee;
}
```

#### **Semantic Colors - 의미별 색상**
```css
:root {
  /* Success - 성공, 완료 */
  --success-50:  #f0fdf4;
  --success-500: #10b981;
  --success-600: #059669;
  --success-700: #047857;
  
  /* Warning - 주의, 확인 필요 */
  --warning-50:  #fffbeb;
  --warning-500: #f59e0b;
  --warning-600: #d97706;
  --warning-700: #b45309;
  
  /* Error - 오류, 실패 */
  --error-50:  #fef2f2;
  --error-500: #ef4444;
  --error-600: #dc2626;
  --error-700: #b91c1c;
  
  /* Info - 정보, 도움말 */
  --info-50:  #f0f9ff;
  --info-500: #3b82f6;
  --info-600: #2563eb;
  --info-700: #1d4ed8;
}
```

#### **Neutral Colors - 텍스트 및 배경**
```css
:root {
  /* Neutral Gray Scale */
  --neutral-0:   #ffffff;   /* 순백 */
  --neutral-50:  #f9fafb;   /* 극히 연한 회색 */
  --neutral-100: #f3f4f6;   /* 연한 회색 */
  --neutral-200: #e5e7eb;   /* 밝은 회색 */
  --neutral-300: #d1d5db;   /* 중간 회색 */
  --neutral-400: #9ca3af;   /* 어두운 회색 */
  --neutral-500: #6b7280;   /* 진한 회색 */
  --neutral-600: #4b5563;   /* 매우 진한 회색 */
  --neutral-700: #374151;   /* 어두운 회색 */
  --neutral-800: #1f2937;   /* 매우 어두운 회색 */
  --neutral-900: #111827;   /* 거의 검은색 */
  --neutral-950: #030712;   /* 순검은색 */
}
```

### **2.2 타이포그래피 시스템 (Typography)**

#### **폰트 계층 구조**
```css
:root {
  /* Font Families */
  --font-primary: 'Inter', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'Fira Code', 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', monospace;
  
  /* Font Sizes - 1.25 Major Third Scale */
  --text-xs:   0.75rem;    /* 12px */
  --text-sm:   0.875rem;   /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg:   1.125rem;   /* 18px */
  --text-xl:   1.25rem;    /* 20px */
  --text-2xl:  1.5rem;     /* 24px */
  --text-3xl:  1.875rem;   /* 30px */
  --text-4xl:  2.25rem;    /* 36px */
  --text-5xl:  3rem;       /* 48px */
  --text-6xl:  3.75rem;    /* 60px */
  
  /* Font Weights */
  --font-thin:       100;
  --font-extralight: 200;
  --font-light:      300;
  --font-normal:     400;
  --font-medium:     500;
  --font-semibold:   600;
  --font-bold:       700;
  --font-extrabold:  800;
  --font-black:      900;
  
  /* Line Heights */
  --leading-none:    1;
  --leading-tight:   1.25;
  --leading-snug:    1.375;
  --leading-normal:  1.5;
  --leading-relaxed: 1.625;
  --leading-loose:   2;
  
  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight:   -0.025em;
  --tracking-normal:  0em;
  --tracking-wide:    0.025em;
  --tracking-wider:   0.05em;
  --tracking-widest:  0.1em;
}
```

#### **텍스트 스타일 클래스**
```css
/* Heading Styles */
.text-heading-1 {
  font-size: var(--text-5xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--neutral-900);
}

.text-heading-2 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--neutral-900);
}

.text-heading-3 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
  color: var(--neutral-800);
}

/* Body Text Styles */
.text-body-large {
  font-size: var(--text-lg);
  font-weight: var(--font-normal);
  line-height: var(--leading-relaxed);
  color: var(--neutral-700);
}

.text-body {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--neutral-700);
}

.text-body-small {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--neutral-600);
}

/* UI Text Styles */
.text-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  color: var(--neutral-700);
}

.text-caption {
  font-size: var(--text-xs);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--neutral-500);
}

/* Code Text */
.text-code {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--neutral-800);
  background: var(--neutral-100);
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}
```

### **2.3 공간 시스템 (Spacing System)**

#### **Spacing Scale - 8pt 그리드 시스템**
```css
:root {
  /* Spacing Scale (8px base) */
  --space-0:   0;           /* 0px */
  --space-px:  1px;         /* 1px */
  --space-0-5: 0.125rem;    /* 2px */
  --space-1:   0.25rem;     /* 4px */
  --space-1-5: 0.375rem;    /* 6px */
  --space-2:   0.5rem;      /* 8px */
  --space-2-5: 0.625rem;    /* 10px */
  --space-3:   0.75rem;     /* 12px */
  --space-3-5: 0.875rem;    /* 14px */
  --space-4:   1rem;        /* 16px */
  --space-5:   1.25rem;     /* 20px */
  --space-6:   1.5rem;      /* 24px */
  --space-7:   1.75rem;     /* 28px */
  --space-8:   2rem;        /* 32px */
  --space-9:   2.25rem;     /* 36px */
  --space-10:  2.5rem;      /* 40px */
  --space-11:  2.75rem;     /* 44px */
  --space-12:  3rem;        /* 48px */
  --space-14:  3.5rem;      /* 56px */
  --space-16:  4rem;        /* 64px */
  --space-20:  5rem;        /* 80px */
  --space-24:  6rem;        /* 96px */
  --space-28:  7rem;        /* 112px */
  --space-32:  8rem;        /* 128px */
  --space-36:  9rem;        /* 144px */
  --space-40:  10rem;       /* 160px */
  --space-44:  11rem;       /* 176px */
  --space-48:  12rem;       /* 192px */
  --space-52:  13rem;       /* 208px */
  --space-56:  14rem;       /* 224px */
  --space-60:  15rem;       /* 240px */
  --space-64:  16rem;       /* 256px */
  --space-72:  18rem;       /* 288px */
  --space-80:  20rem;       /* 320px */
  --space-96:  24rem;       /* 384px */
}
```

#### **Layout Spacing 가이드라인**
```css
/* Component Internal Spacing */
.spacing-component-xs {
  padding: var(--space-2);          /* 8px */
}

.spacing-component-sm {
  padding: var(--space-3);          /* 12px */
}

.spacing-component-md {
  padding: var(--space-4);          /* 16px */
}

.spacing-component-lg {
  padding: var(--space-6);          /* 24px */
}

.spacing-component-xl {
  padding: var(--space-8);          /* 32px */
}

/* Stack Spacing (Vertical) */
.spacing-stack-xs > * + * {
  margin-top: var(--space-2);       /* 8px */
}

.spacing-stack-sm > * + * {
  margin-top: var(--space-4);       /* 16px */
}

.spacing-stack-md > * + * {
  margin-top: var(--space-6);       /* 24px */
}

.spacing-stack-lg > * + * {
  margin-top: var(--space-8);       /* 32px */
}

.spacing-stack-xl > * + * {
  margin-top: var(--space-12);      /* 48px */
}
```

### **2.4 그림자 시스템 (Shadow System)**

#### **Elevation Shadows**
```css
:root {
  /* Shadow Tokens */
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
  --shadow-none: 0 0 #0000;
  
  /* Colored Shadows */
  --shadow-primary: 0 4px 6px -1px rgba(59, 130, 246, 0.1), 0 2px 4px -1px rgba(59, 130, 246, 0.06);
  --shadow-success: 0 4px 6px -1px rgba(16, 185, 129, 0.1), 0 2px 4px -1px rgba(16, 185, 129, 0.06);
  --shadow-warning: 0 4px 6px -1px rgba(245, 158, 11, 0.1), 0 2px 4px -1px rgba(245, 158, 11, 0.06);
  --shadow-error: 0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06);
}
```

#### **Component Shadow Usage**
```css
/* Cards */
.shadow-card {
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease-in-out;
}

.shadow-card:hover {
  box-shadow: var(--shadow-md);
}

/* Modals */
.shadow-modal {
  box-shadow: var(--shadow-2xl);
}

/* Buttons */
.shadow-button {
  box-shadow: var(--shadow-xs);
}

.shadow-button:hover {
  box-shadow: var(--shadow-sm);
}

.shadow-button:active {
  box-shadow: var(--shadow-inner);
}

/* Dropdowns */
.shadow-dropdown {
  box-shadow: var(--shadow-lg);
}
```

### **2.5 Border Radius 시스템**

#### **Radius Scale**
```css
:root {
  --radius-none: 0;
  --radius-sm: 0.125rem;    /* 2px */
  --radius-md: 0.375rem;    /* 6px */
  --radius-lg: 0.5rem;      /* 8px */
  --radius-xl: 0.75rem;     /* 12px */
  --radius-2xl: 1rem;       /* 16px */
  --radius-3xl: 1.5rem;     /* 24px */
  --radius-full: 9999px;    /* 완전한 원형 */
}
```

#### **Component Radius Usage**
```css
/* Buttons */
.radius-button {
  border-radius: var(--radius-lg);
}

/* Cards */
.radius-card {
  border-radius: var(--radius-xl);
}

/* Input Fields */
.radius-input {
  border-radius: var(--radius-md);
}

/* Modals */
.radius-modal {
  border-radius: var(--radius-2xl);
}

/* Pills/Tags */
.radius-pill {
  border-radius: var(--radius-full);
}
```

---

## 🧩 **3. 컴포넌트 시스템 (Component System)**

### **3.1 기본 컴포넌트 (Foundation Components)**

#### **Button Component**
```css
/* Button Base Styles */
.btn {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  
  /* Typography */
  font-family: var(--font-primary);
  font-weight: var(--font-medium);
  text-decoration: none;
  white-space: nowrap;
  
  /* Interaction */
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease-in-out;
  
  /* Accessibility */
  outline: none;
  border: none;
  
  /* Focus Ring */
  position: relative;
}

.btn:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Button Sizes */
.btn-xs {
  padding: var(--space-1) var(--space-2);
  font-size: var(--text-xs);
  border-radius: var(--radius-sm);
  min-height: 1.5rem;
}

.btn-sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
  min-height: 2rem;
}

.btn-md {
  padding: var(--space-2-5) var(--space-4);
  font-size: var(--text-sm);
  border-radius: var(--radius-lg);
  min-height: 2.5rem;
}

.btn-lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-base);
  border-radius: var(--radius-lg);
  min-height: 3rem;
}

.btn-xl {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-lg);
  border-radius: var(--radius-xl);
  min-height: 3.5rem;
}

/* Button Variants */
.btn-primary {
  background-color: var(--primary-500);
  color: white;
  box-shadow: var(--shadow-xs);
}

.btn-primary:hover {
  background-color: var(--primary-600);
  box-shadow: var(--shadow-sm);
}

.btn-primary:active {
  background-color: var(--primary-700);
  box-shadow: var(--shadow-inner);
}

.btn-secondary {
  background-color: var(--neutral-100);
  color: var(--neutral-700);
  border: 1px solid var(--neutral-300);
}

.btn-secondary:hover {
  background-color: var(--neutral-200);
  border-color: var(--neutral-400);
}

.btn-ghost {
  background-color: transparent;
  color: var(--neutral-700);
}

.btn-ghost:hover {
  background-color: var(--neutral-100);
}

.btn-outline {
  background-color: transparent;
  color: var(--primary-500);
  border: 1px solid var(--primary-500);
}

.btn-outline:hover {
  background-color: var(--primary-50);
  border-color: var(--primary-600);
}

/* Button States */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.btn-loading {
  color: transparent;
  pointer-events: none;
}

.btn-loading::after {
  content: "";
  position: absolute;
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

#### **Input Component**
```css
/* Input Base Styles */
.input {
  /* Layout */
  width: 100%;
  
  /* Typography */
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
  
  /* Appearance */
  background-color: white;
  border: 1px solid var(--neutral-300);
  border-radius: var(--radius-md);
  color: var(--neutral-900);
  
  /* Interaction */
  transition: all 0.2s ease-in-out;
  outline: none;
}

.input:focus {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input:disabled {
  background-color: var(--neutral-50);
  color: var(--neutral-500);
  cursor: not-allowed;
}

.input::placeholder {
  color: var(--neutral-400);
}

/* Input Sizes */
.input-sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
}

.input-md {
  padding: var(--space-2-5) var(--space-3-5);
  font-size: var(--text-sm);
}

.input-lg {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
}

/* Input States */
.input-error {
  border-color: var(--error-500);
}

.input-error:focus {
  border-color: var(--error-500);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-success {
  border-color: var(--success-500);
}
```

#### **Card Component**
```css
/* Card Base Styles */
.card {
  background-color: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--neutral-200);
  overflow: hidden;
  transition: all 0.2s ease-in-out;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

/* Card Variants */
.card-elevated {
  box-shadow: var(--shadow-lg);
}

.card-flat {
  box-shadow: none;
  border: 1px solid var(--neutral-200);
}

.card-outlined {
  box-shadow: none;
  border: 2px solid var(--neutral-300);
}

/* Card Sections */
.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--neutral-200);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--neutral-200);
  background-color: var(--neutral-50);
}

/* Card Sizes */
.card-compact .card-header,
.card-compact .card-body,
.card-compact .card-footer {
  padding: var(--space-4);
}

.card-spacious .card-header,
.card-spacious .card-body,
.card-spacious .card-footer {
  padding: var(--space-8);
}
```

### **3.2 복합 컴포넌트 (Composite Components)**

#### **Modal Component**
```css
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
  
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  
  animation: modal-overlay-enter 0.2s ease-out;
}

.modal-overlay.closing {
  animation: modal-overlay-exit 0.2s ease-in;
}

/* Modal Content */
.modal {
  background-color: white;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-2xl);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  
  animation: modal-enter 0.2s ease-out;
}

.modal.closing {
  animation: modal-exit 0.2s ease-in;
}

/* Modal Sizes */
.modal-sm {
  width: 100%;
  max-width: 20rem;
}

.modal-md {
  width: 100%;
  max-width: 28rem;
}

.modal-lg {
  width: 100%;
  max-width: 40rem;
}

.modal-xl {
  width: 100%;
  max-width: 56rem;
}

.modal-full {
  width: 100%;
  max-width: 80rem;
}

/* Modal Sections */
.modal-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--neutral-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--neutral-900);
}

.modal-close {
  appearance: none;
  background: none;
  border: none;
  color: var(--neutral-500);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-md);
  transition: all 0.2s ease-in-out;
}

.modal-close:hover {
  background-color: var(--neutral-100);
  color: var(--neutral-700);
}

.modal-body {
  padding: var(--space-6);
  overflow-y: auto;
}

.modal-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--neutral-200);
  background-color: var(--neutral-50);
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
}

/* Modal Animations */
@keyframes modal-overlay-enter {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes modal-overlay-exit {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

@keyframes modal-enter {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes modal-exit {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
}
```

#### **Toast Notification Component**
```css
/* Toast Container */
.toast-container {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  z-index: 1100;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  pointer-events: none;
}

/* Toast Base */
.toast {
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--neutral-200);
  padding: var(--space-4);
  min-width: 20rem;
  max-width: 24rem;
  pointer-events: auto;
  
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  
  animation: toast-enter 0.3s ease-out;
}

.toast.exiting {
  animation: toast-exit 0.2s ease-in;
}

/* Toast Variants */
.toast-success {
  border-left: 4px solid var(--success-500);
}

.toast-warning {
  border-left: 4px solid var(--warning-500);
}

.toast-error {
  border-left: 4px solid var(--error-500);
}

.toast-info {
  border-left: 4px solid var(--info-500);
}

/* Toast Icon */
.toast-icon {
  flex-shrink: 0;
  width: 1.25rem;
  height: 1.25rem;
  margin-top: 0.125rem;
}

.toast-success .toast-icon {
  color: var(--success-500);
}

.toast-warning .toast-icon {
  color: var(--warning-500);
}

.toast-error .toast-icon {
  color: var(--error-500);
}

.toast-info .toast-icon {
  color: var(--info-500);
}

/* Toast Content */
.toast-content {
  flex: 1;
}

.toast-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--neutral-900);
  margin-bottom: var(--space-1);
}

.toast-message {
  font-size: var(--text-sm);
  color: var(--neutral-600);
  line-height: var(--leading-normal);
}

/* Toast Close Button */
.toast-close {
  appearance: none;
  background: none;
  border: none;
  color: var(--neutral-400);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: color 0.2s ease-in-out;
  flex-shrink: 0;
}

.toast-close:hover {
  color: var(--neutral-600);
}

/* Toast Animations */
@keyframes toast-enter {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes toast-exit {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}
```

### **3.3 특수 컴포넌트 (Specialized Components)**

#### **File Upload Component**
```css
/* File Upload Container */
.file-upload {
  border: 2px dashed var(--neutral-300);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  text-align: center;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
  background-color: var(--neutral-50);
}

.file-upload:hover {
  border-color: var(--primary-400);
  background-color: var(--primary-50);
}

.file-upload.dragover {
  border-color: var(--primary-500);
  background-color: var(--primary-100);
  transform: scale(1.02);
}

.file-upload.uploading {
  pointer-events: none;
  opacity: 0.7;
}

/* File Upload Icon */
.file-upload-icon {
  width: 3rem;
  height: 3rem;
  color: var(--neutral-400);
  margin: 0 auto var(--space-4);
}

.file-upload:hover .file-upload-icon {
  color: var(--primary-500);
}

/* File Upload Text */
.file-upload-text {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  color: var(--neutral-700);
  margin-bottom: var(--space-2);
}

.file-upload-subtext {
  font-size: var(--text-sm);
  color: var(--neutral-500);
}

/* File Upload Progress */
.file-upload-progress {
  margin-top: var(--space-4);
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: var(--neutral-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--primary-500);
  border-radius: var(--radius-full);
  transition: width 0.3s ease-in-out;
}
```

#### **AI Model Selector Component**
```css
/* AI Model Selector */
.ai-model-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: var(--space-4);
}

/* Model Option */
.model-option {
  position: relative;
  cursor: pointer;
}

.model-option input[type="radio"] {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.model-option-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 2px solid var(--neutral-200);
  border-radius: var(--radius-lg);
  background-color: white;
  transition: all 0.2s ease-in-out;
}

.model-option:hover .model-option-card {
  border-color: var(--neutral-300);
  box-shadow: var(--shadow-sm);
}

.model-option input:checked + .model-option-card {
  border-color: var(--primary-500);
  background-color: var(--primary-50);
  box-shadow: var(--shadow-primary);
}

.model-option input:focus + .model-option-card {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Model Icon */
.model-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: var(--font-semibold);
  flex-shrink: 0;
}

.model-gemini .model-icon {
  background-color: var(--gemini-primary);
}

.model-openai .model-icon {
  background-color: var(--openai-primary);
}

.model-claude .model-icon {
  background-color: var(--claude-primary);
}

.model-perplexity .model-icon {
  background-color: var(--perplexity-primary);
}

.model-clova .model-icon {
  background-color: var(--clova-primary);
}

/* Model Info */
.model-info {
  flex: 1;
}

.model-name {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--neutral-900);
  margin-bottom: var(--space-1);
}

.model-description {
  font-size: var(--text-sm);
  color: var(--neutral-600);
  line-height: var(--leading-normal);
}

/* Model Badge */
.model-badge {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  background-color: var(--primary-500);
  color: white;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-full);
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.2s ease-in-out;
}

.model-option input:checked ~ .model-badge {
  opacity: 1;
  transform: scale(1);
}
```

---

## 🎯 **4. 사용자 경험 (UX) 설계**

### **4.1 사용자 여정 (User Journey)**

#### **신규 사용자 온보딩 플로우**
```
1. 랜딩 페이지 진입
   ├── 가치 제안 확인 (3초 이내)
   ├── 데모 영상 시청 (선택사항)
   └── "무료로 시작하기" 클릭

2. 계정 생성
   ├── 이메일 입력
   ├── 비밀번호 설정
   ├── 이용약관 동의
   └── 인증 이메일 확인

3. 첫 번째 문서 업로드
   ├── 온보딩 투어 시작 (스킵 가능)
   ├── 샘플 파일 제공
   ├── 드래그 앤 드롭 가이드
   └── 업로드 완료 축하

4. AI 모델 선택 가이드
   ├── 각 모델 특징 설명
   ├── 추천 모델 하이라이트
   ├── 테스트 실행
   └── 결과 비교 제공

5. 첫 번째 편집 완료
   ├── 단계별 가이드
   ├── 실시간 도움말
   ├── 결과 확인
   └── 다운로드/공유
```

#### **기존 사용자 워크플로우**
```
1. 로그인 후 대시보드
   ├── 최근 문서 목록
   ├── 진행 중인 작업
   ├── 사용량 현황
   └── 새 문서 시작

2. 빠른 업로드
   ├── 즐겨찾는 설정 적용
   ├── 배치 업로드 지원
   ├── 템플릿 선택
   └── 자동 처리 시작

3. 고급 편집
   ├── 커스텀 프롬프트
   ├── 여러 AI 모델 비교
   ├── 단계별 편집
   └── 히스토리 관리

4. 협업 및 공유
   ├── 팀원 초대
   ├── 댓글 및 피드백
   ├── 버전 관리
   └── 최종 승인
```

### **4.2 인터랙션 패턴 (Interaction Patterns)**

#### **파일 업로드 인터랙션**
```css
/* 드래그 앤 드롭 상태 피드백 */
.upload-zone {
  transition: all 0.2s ease-in-out;
}

.upload-zone.drag-enter {
  transform: scale(1.02);
  border-color: var(--primary-500);
  background-color: var(--primary-50);
}

.upload-zone.drag-over {
  border-style: solid;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.upload-zone.drag-leave {
  transform: scale(1);
  border-color: var(--neutral-300);
  background-color: var(--neutral-50);
}

/* 업로드 진행 애니메이션 */
.upload-progress {
  position: relative;
  overflow: hidden;
}

.upload-progress::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}
```

#### **단계 네비게이션 인터랙션**
```css
/* 단계 인디케이터 */
.step-navigator {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-lg);
  transition: all 0.2s ease-in-out;
}

.step:hover {
  background-color: var(--neutral-50);
}

.step.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.step.disabled:hover {
  background-color: transparent;
}

/* 단계 번호 */
.step-number {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  transition: all 0.2s ease-in-out;
}

.step.pending .step-number {
  background-color: var(--neutral-200);
  color: var(--neutral-500);
}

.step.current .step-number {
  background-color: var(--primary-500);
  color: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.step.completed .step-number {
  background-color: var(--success-500);
  color: white;
}

/* 단계 연결선 */
.step-connector {
  flex: 1;
  height: 2px;
  background-color: var(--neutral-200);
  position: relative;
  margin: 0 var(--space-2);
}

.step-connector.active::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: var(--success-500);
  transition: width 0.3s ease-in-out;
}

.step.completed + .step-connector.active::before {
  width: 100%;
}
```

#### **AI 처리 상태 인터랙션**
```css
/* AI 처리 상태 카드 */
.ai-processing-card {
  background: linear-gradient(45deg, var(--primary-50), var(--primary-100));
  border: 1px solid var(--primary-200);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
}

.ai-processing-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(59, 130, 246, 0.1),
    transparent
  );
  animation: ai-thinking 2s infinite;
}

@keyframes ai-thinking {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* AI 모델 표시기 */
.ai-model-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.ai-model-indicator.gemini {
  background-color: var(--gemini-light);
  color: var(--gemini-primary);
}

.ai-model-indicator.openai {
  background-color: var(--openai-light);
  color: var(--openai-primary);
}

/* 처리 단계 애니메이션 */
.processing-step {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  margin-bottom: var(--space-2);
  border-radius: var(--radius-lg);
  transition: all 0.3s ease-in-out;
}

.processing-step.active {
  background-color: var(--primary-50);
  border-left: 4px solid var(--primary-500);
}

.processing-step.completed {
  background-color: var(--success-50);
  border-left: 4px solid var(--success-500);
}

.processing-step-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.processing-step.active .processing-step-icon {
  background-color: var(--primary-500);
  color: white;
  animation: pulse 1.5s infinite;
}

.processing-step.completed .processing-step-icon {
  background-color: var(--success-500);
  color: white;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}
```

### **4.3 에러 상태 및 피드백**

#### **에러 상태 디자인**
```css
/* 에러 컨테이너 */
.error-state {
  text-align: center;
  padding: var(--space-12);
  border-radius: var(--radius-xl);
  background-color: var(--error-50);
  border: 1px solid var(--error-200);
}

/* 에러 아이콘 */
.error-icon {
  width: 4rem;
  height: 4rem;
  color: var(--error-500);
  margin: 0 auto var(--space-4);
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* 에러 메시지 */
.error-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--error-700);
  margin-bottom: var(--space-2);
}

.error-description {
  font-size: var(--text-base);
  color: var(--error-600);
  margin-bottom: var(--space-6);
  max-width: 32rem;
  margin-left: auto;
  margin-right: auto;
}

/* 에러 액션 버튼 */
.error-actions {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
  flex-wrap: wrap;
}
```

#### **로딩 상태 디자인**
```css
/* 스켈레톤 로딩 */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--neutral-200) 25%,
    var(--neutral-100) 50%,
    var(--neutral-200) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton-text {
  height: 1rem;
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-2);
}

.skeleton-text.short {
  width: 60%;
}

.skeleton-text.medium {
  width: 80%;
}

.skeleton-text.long {
  width: 100%;
}

/* 스피너 로딩 */
.spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid var(--neutral-200);
  border-top-color: var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-sm {
  width: 1rem;
  height: 1rem;
  border-width: 1px;
}

.spinner-lg {
  width: 3rem;
  height: 3rem;
  border-width: 3px;
}
```

---

## ♿ **5. 접근성 (Accessibility) 가이드라인**

### **5.1 WCAG 2.1 AA 준수 사항**

#### **색상 대비 (Color Contrast)**
```css
/* 최소 대비율 4.5:1 준수 */
:root {
  /* AAA 등급 대비율 (7:1 이상) */
  --text-aaa: #000000;           /* 21:1 대비 */
  --text-primary: #111827;       /* 16.9:1 대비 */
  
  /* AA 등급 대비율 (4.5:1 이상) */
  --text-secondary: #374151;     /* 11.4:1 대비 */
  --text-tertiary: #6b7280;      /* 6.7:1 대비 */
  
  /* 최소 대비율 */
  --text-minimum: #9ca3af;       /* 4.5:1 대비 */
}

/* 대비율 검증 클래스 */
.text-aa {
  color: var(--text-secondary);  /* 4.5:1 이상 */
}

.text-aaa {
  color: var(--text-primary);    /* 7:1 이상 */
}

/* 링크 색상 대비 */
.link {
  color: var(--primary-700);     /* 5.1:1 대비 */
  text-decoration: underline;
}

.link:hover {
  color: var(--primary-800);
  text-decoration: none;
}

/* 버튼 색상 대비 */
.btn-primary {
  background-color: var(--primary-600);  /* 충분한 대비 확보 */
  color: white;
}
```

#### **키보드 내비게이션 (Keyboard Navigation)**
```css
/* 포커스 링 스타일 */
.focus-ring {
  outline: none;
  position: relative;
}

.focus-ring:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
  border-radius: var(--radius-md);
}

/* 고대비 포커스 링 (고대비 모드용) */
@media (prefers-contrast: high) {
  .focus-ring:focus-visible {
    outline: 3px solid currentColor;
    outline-offset: 2px;
  }
}

/* 키보드 전용 요소 표시 */
.keyboard-only {
  position: absolute;
  left: -10000px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.keyboard-only:focus {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
}

/* 탭 순서 관리 */
.tab-trap {
  position: relative;
}

.tab-trap::before,
.tab-trap::after {
  content: "";
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}
```

#### **스크린 리더 지원 (Screen Reader Support)**
```css
/* 스크린 리더 전용 텍스트 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 스크린 리더에서 포커스 시 표시 */
.sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}

/* ARIA 레이블 스타일링 */
[aria-label]::after {
  content: " (" attr(aria-label) ")";
  font-size: 0;
  color: transparent;
}

@media screen and (max-width: 0) {
  [aria-label]::after {
    font-size: inherit;
    color: inherit;
  }
}
```

### **5.2 운동 장애 지원 (Motor Disabilities)**

#### **터치 타겟 크기 (Touch Target Size)**
```css
/* 최소 터치 타겟 크기 44x44px */
.touch-target {
  min-width: 2.75rem;   /* 44px */
  min-height: 2.75rem;  /* 44px */
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* 터치 영역 확장 */
.touch-target::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 2.75rem;
  min-height: 2.75rem;
  z-index: -1;
}

/* 드래그 가능한 요소 */
.draggable {
  cursor: grab;
  user-select: none;
  -webkit-user-drag: element;
}

.draggable:active {
  cursor: grabbing;
}

/* 호버 효과 확장 시간 */
.extended-hover {
  transition-delay: 0.1s;
  transition-duration: 0.3s;
}
```

#### **축소 모션 지원 (Reduced Motion)**
```css
/* 모션 감소 설정 존중 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  
  /* 필수 애니메이션만 유지 */
  .essential-animation {
    animation-duration: inherit;
    transition-duration: inherit;
  }
}

/* 모션 선호 설정 */
@media (prefers-reduced-motion: no-preference) {
  .smooth-scroll {
    scroll-behavior: smooth;
  }
  
  .fade-in {
    animation: fade-in 0.3s ease-out;
  }
  
  .slide-in {
    animation: slide-in 0.4s ease-out;
  }
}
```

### **5.3 인지 접근성 (Cognitive Accessibility)**

#### **명확한 레이블링 (Clear Labeling)**
```css
/* 폼 레이블 스타일 */
.form-label {
  font-weight: var(--font-medium);
  margin-bottom: var(--space-2);
  display: block;
}

.form-label.required::after {
  content: " *";
  color: var(--error-500);
}

/* 도움말 텍스트 */
.help-text {
  font-size: var(--text-sm);
  color: var(--neutral-600);
  margin-top: var(--space-1);
}

/* 에러 메시지 */
.error-message {
  font-size: var(--text-sm);
  color: var(--error-600);
  margin-top: var(--space-1);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.error-message::before {
  content: "⚠";
  font-size: var(--text-base);
}
```

#### **진행 상황 표시 (Progress Indication)**
```css
/* 진행률 표시기 */
.progress {
  width: 100%;
  height: 0.5rem;
  background-color: var(--neutral-200);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 100%;
  background-color: var(--primary-500);
  border-radius: var(--radius-full);
  transition: width 0.3s ease-in-out;
  position: relative;
}

.progress-bar::after {
  content: attr(data-progress) "%";
  position: absolute;
  top: -1.5rem;
  right: 0;
  font-size: var(--text-xs);
  color: var(--neutral-600);
  white-space: nowrap;
}

/* 단계 진행 표시 */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.step-indicator-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  flex: 1;
  position: relative;
}

.step-indicator-item:not(:last-child)::after {
  content: "";
  position: absolute;
  top: 0.75rem;
  left: 2rem;
  right: -2rem;
  height: 2px;
  background-color: var(--neutral-200);
  z-index: -1;
}

.step-indicator-item.completed::after {
  background-color: var(--success-500);
}
```

---

## 📱 **6. 반응형 디자인 (Responsive Design)**

### **6.1 브레이크포인트 시스템**

#### **브레이크포인트 정의**
```css
:root {
  /* Breakpoints */
  --breakpoint-xs: 0px;        /* Extra small devices */
  --breakpoint-sm: 640px;      /* Small devices (landscape phones) */
  --breakpoint-md: 768px;      /* Medium devices (tablets) */
  --breakpoint-lg: 1024px;     /* Large devices (laptops) */
  --breakpoint-xl: 1280px;     /* Extra large devices (desktops) */
  --breakpoint-2xl: 1536px;    /* 2X large devices (large desktops) */
}

/* Container sizes */
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
    padding-left: var(--space-6);
    padding-right: var(--space-6);
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
    padding-left: var(--space-8);
    padding-right: var(--space-8);
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}

@media (min-width: 1536px) {
  .container {
    max-width: 1536px;
  }
}
```

### **6.2 모바일 우선 접근법**

#### **모바일 레이아웃**
```css
/* 모바일 기본 레이아웃 */
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-header {
  background-color: white;
  border-bottom: 1px solid var(--neutral-200);
  padding: var(--space-4);
  position: sticky;
  top: 0;
  z-index: 100;
}

.main-nav {
  display: none; /* 모바일에서 숨김 */
}

.mobile-menu-toggle {
  display: block;
  background: none;
  border: none;
  font-size: var(--text-xl);
  color: var(--neutral-700);
}

.main-content {
  flex: 1;
  padding: var(--space-4);
}

.main-sidebar {
  display: none; /* 모바일에서 숨김 */
}

/* 태블릿 레이아웃 */
@media (min-width: 768px) {
  .main-layout {
    flex-direction: row;
  }
  
  .main-header {
    position: static;
    border-bottom: none;
    border-right: 1px solid var(--neutral-200);
    width: 240px;
    flex-shrink: 0;
  }
  
  .main-nav {
    display: block;
  }
  
  .mobile-menu-toggle {
    display: none;
  }
  
  .main-content {
    padding: var(--space-6);
  }
}

/* 데스크톱 레이아웃 */
@media (min-width: 1024px) {
  .main-layout {
    grid-template-columns: 240px 1fr 300px;
    grid-template-areas: "sidebar content aside";
    display: grid;
  }
  
  .main-sidebar {
    display: block;
    grid-area: aside;
    padding: var(--space-6);
    border-left: 1px solid var(--neutral-200);
  }
  
  .main-content {
    grid-area: content;
    padding: var(--space-8);
  }
}
```

#### **반응형 컴포넌트**
```css
/* 반응형 카드 그리드 */
.card-grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr; /* 모바일: 1열 */
}

@media (min-width: 640px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr); /* 태블릿: 2열 */
    gap: var(--space-6);
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr); /* 데스크톱: 3열 */
    gap: var(--space-8);
  }
}

/* 반응형 AI 모델 선택기 */
.ai-model-selector {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

@media (min-width: 768px) {
  .ai-model-selector {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .model-option {
    flex: 1;
    min-width: 200px;
  }
}

/* 반응형 스텝 네비게이터 */
.step-navigator {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

@media (min-width: 640px) {
  .step-navigator {
    flex-direction: row;
    gap: var(--space-4);
  }
  
  .step-connector {
    display: block;
  }
}

/* 반응형 모달 */
.modal {
  width: 100vw;
  height: 100vh;
  max-width: none;
  max-height: none;
  border-radius: 0;
}

@media (min-width: 640px) {
  .modal {
    width: auto;
    height: auto;
    max-width: 90vw;
    max-height: 90vh;
    border-radius: var(--radius-2xl);
  }
}
```

### **6.3 터치 친화적 인터페이스**

#### **터치 제스처 지원**
```css
/* 터치 스크롤 개선 */
.touch-scroll {
  -webkit-overflow-scrolling: touch;
  overflow-scrolling: touch;
}

/* 터치 선택 비활성화 */
.no-touch-select {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
}

/* 터치 액션 최적화 */
.touch-action-pan {
  touch-action: pan-x pan-y;
}

.touch-action-none {
  touch-action: none;
}

/* 스와이프 가능한 요소 */
.swipeable {
  touch-action: pan-y;
  user-select: none;
}

/* 터치 피드백 */
.touch-feedback {
  -webkit-tap-highlight-color: rgba(59, 130, 246, 0.1);
  transition: background-color 0.1s ease-in-out;
}

.touch-feedback:active {
  background-color: var(--neutral-100);
}
```

---

## 🎬 **7. 애니메이션 및 모션 (Animation & Motion)**

### **7.1 모션 원칙 (Motion Principles)**

#### **모션 토큰 (Motion Tokens)**
```css
:root {
  /* Duration */
  --duration-instant: 0ms;
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  --duration-slower: 700ms;
  
  /* Easing */
  --ease-linear: cubic-bezier(0, 0, 1, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-elastic: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

#### **진입/퇴장 애니메이션 (Enter/Exit Animations)**
```css
/* 페이드 인/아웃 */
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fade-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* 슬라이드 인/아웃 */
@keyframes slide-in-up {
  from {
    opacity: 0;
    transform: translateY(1rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-out-down {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(1rem);
  }
}

/* 스케일 인/아웃 */
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes scale-out {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* 애니메이션 클래스 */
.animate-fade-in {
  animation: fade-in var(--duration-normal) var(--ease-out);
}

.animate-slide-in-up {
  animation: slide-in-up var(--duration-normal) var(--ease-out);
}

.animate-scale-in {
  animation: scale-in var(--duration-fast) var(--ease-out);
}
```

### **7.2 마이크로 인터랙션 (Micro-interactions)**

#### **버튼 호버 효과**
```css
.btn-animated {
  position: relative;
  overflow: hidden;
  transition: all var(--duration-normal) var(--ease-out);
}

.btn-animated::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left var(--duration-slow) var(--ease-out);
}

.btn-animated:hover::before {
  left: 100%;
}

.btn-animated:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.btn-animated:active {
  transform: translateY(0);
  transition-duration: var(--duration-fast);
}
```

#### **카드 호버 효과**
```css
.card-interactive {
  transition: all var(--duration-normal) var(--ease-out);
  cursor: pointer;
}

.card-interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.card-interactive:hover .card-title {
  color: var(--primary-600);
}

.card-interactive .card-arrow {
  transition: transform var(--duration-normal) var(--ease-out);
}

.card-interactive:hover .card-arrow {
  transform: translateX(0.25rem);
}
```

#### **로딩 애니메이션**
```css
/* 도트 로딩 */
.loading-dots {
  display: inline-flex;
  gap: var(--space-1);
}

.loading-dot {
  width: 0.5rem;
  height: 0.5rem;
  background-color: var(--primary-500);
  border-radius: 50%;
  animation: loading-dot var(--duration-slow) infinite;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.1s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.2s;
}

@keyframes loading-dot {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 펄스 로딩 */
.loading-pulse {
  animation: pulse var(--duration-slow) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
```

---

## 📋 **8. 구현 체크리스트**

### **8.1 디자인 토큰 구현**
- [ ] CSS 커스텀 속성으로 모든 토큰 정의
- [ ] 컬러 시스템 완전 구현
- [ ] 타이포그래피 스케일 적용
- [ ] 간격 시스템 일관성 확보
- [ ] 그림자 및 테두리 스타일 표준화

### **8.2 컴포넌트 라이브러리**
- [ ] 기본 컴포넌트 (Button, Input, Card) 구현
- [ ] 복합 컴포넌트 (Modal, Toast) 구현
- [ ] 특수 컴포넌트 (FileUpload, AISelector) 구현
- [ ] 모든 컴포넌트 Storybook 문서화
- [ ] 컴포넌트 테스트 코드 작성

### **8.3 접근성 구현**
- [ ] WCAG 2.1 AA 기준 색상 대비 확보
- [ ] 키보드 내비게이션 완전 지원
- [ ] 스크린 리더 호환성 확보
- [ ] ARIA 레이블 및 속성 적용
- [ ] 터치 타겟 크기 기준 준수

### **8.4 반응형 디자인**
- [ ] 모든 브레이크포인트 테스트
- [ ] 터치 친화적 인터페이스 구현
- [ ] 모바일 우선 접근법 적용
- [ ] 다양한 디바이스 호환성 확인

### **8.5 성능 최적화**
- [ ] 애니메이션 성능 최적화
- [ ] CSS 번들 크기 최소화
- [ ] 중요 CSS 인라인화
- [ ] 이미지 최적화 및 지연 로딩

---

## 🎯 **9. 품질 보증 (Quality Assurance)**

### **9.1 디자인 QA 체크리스트**

#### **시각적 일관성**
- [ ] 모든 페이지에서 일관된 브랜딩
- [ ] 컬러 팔레트 정확한 적용
- [ ] 타이포그래피 계층 구조 준수
- [ ] 간격 시스템 일관성 확인

#### **사용성 테스트**
- [ ] 5초 테스트 (첫인상 평가)
- [ ] 작업 완료율 > 90%
- [ ] 평균 작업 시간 < 목표 시간
- [ ] 사용자 만족도 > 4.5/5

#### **접근성 테스트**
- [ ] 자동화된 접근성 테스트 (axe, WAVE)
- [ ] 수동 키보드 내비게이션 테스트
- [ ] 스크린 리더 테스트 (NVDA, JAWS)
- [ ] 색맹 시뮬레이션 테스트

#### **성능 테스트**
- [ ] First Contentful Paint < 1.5초
- [ ] Largest Contentful Paint < 2.5초
- [ ] Cumulative Layout Shift < 0.1
- [ ] First Input Delay < 100ms

### **9.2 브라우저 호환성**

#### **지원 브라우저**
- **Desktop**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: Chrome Mobile 90+, Safari iOS 14+, Samsung Internet 15+

#### **호환성 테스트 매트릭스**
| 기능 | Chrome | Firefox | Safari | Edge | 모바일 |
|------|--------|---------|---------|------|--------|
| CSS Grid | ✅ | ✅ | ✅ | ✅ | ✅ |
| CSS Flexbox | ✅ | ✅ | ✅ | ✅ | ✅ |
| CSS Custom Properties | ✅ | ✅ | ✅ | ✅ | ✅ |
| WebP Images | ✅ | ✅ | ✅ | ✅ | ✅ |
| Touch Events | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🚀 **10. 결론 및 다음 단계**

### **10.1 디자인 시스템의 핵심 가치**

1. **일관성**: 모든 인터페이스 요소의 통일된 경험
2. **확장성**: 새로운 기능과 컴포넌트의 쉬운 추가
3. **접근성**: 모든 사용자를 위한 포용적 디자인
4. **효율성**: 디자이너와 개발자의 협업 최적화

### **10.2 지속적 개선 계획**

#### **단기 계획 (1-3개월)**
- 사용자 피드백 수집 시스템 구축
- A/B 테스트를 통한 UX 최적화
- 접근성 개선 사항 지속 적용

#### **중기 계획 (3-6개월)**
- 다크 모드 지원
- 고대비 테마 옵션
- 다국어 지원 확장

#### **장기 계획 (6-12개월)**
- AI 기반 개인화 인터페이스
- 음성 인터페이스 지원
- AR/VR 인터페이스 연구

---

*📝 이 디자인 시스템은 Paperwork AI의 완전한 사용자 경험을 정의합니다. 모든 이해관계자의 관점을 통합하여 일관되고 접근 가능하며 효율적인 인터페이스를 제공합니다.*