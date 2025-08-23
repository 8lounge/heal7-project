# 🎨 HEAL7 UI 컴포넌트 라이브러리 아키텍처 v1.0

> **프로젝트**: HEAL7 옴니버스 플랫폼 UI/UX 컴포넌트 시스템  
> **버전**: v1.0.0  
> **작성일**: 2025-08-18  
> **목적**: 사주명리학 특화 + 범용 UI 컴포넌트 통합 라이브러리  
> **범위**: React 19 + TypeScript + Storybook + 접근성 + 반응형

---

## 🎯 **컴포넌트 라이브러리 설계 철학**

### **🧩 레고블럭 컴포넌트 시스템**
```yaml
component_philosophy:
  atomic_design: "아토믹 디자인 방법론 기반 계층적 구조"
  composition_over_inheritance: "상속보다 조합을 통한 유연성"
  accessibility_first: "접근성 우선 설계"
  responsive_by_default: "기본 반응형 지원"
  themeable_architecture: "테마 변경 가능한 구조"
  
design_principles:
  mystic_aurora_integration: "Mystic Aurora 테마와 완전 통합"
  five_elements_harmony: "오행 조화 기반 컬러 시스템"
  eastern_aesthetics: "동양적 미학과 현대적 인터페이스 융합"
  intuitive_interaction: "직관적이고 자연스러운 상호작용"
  spiritual_trust: "영성 분야 특유의 신뢰감 표현"
```

### **📱 플랫폼 지원 전략**
```yaml
platform_support:
  primary_platforms:
    web: "React 19 + Vite + TypeScript"
    mobile_web: "PWA + 터치 최적화"
    
  responsive_strategy:
    mobile_first: "320px부터 시작"
    breakpoints: ["mobile: 320px", "tablet: 768px", "desktop: 1024px", "wide: 1440px"]
    fluid_design: "유동적 레이아웃"
    
  accessibility_compliance:
    wcag_version: "WCAG 2.1 AA"
    screen_readers: "NVDA, JAWS, VoiceOver 지원"
    keyboard_navigation: "완전한 키보드 조작 지원"
    color_contrast: "4.5:1 이상 대비율"
```

---

## 🎨 **디자인 토큰 시스템**

### **🌈 Mystic Aurora 컬러 시스템**

#### **1. 기본 컬러 팔레트**
```css
/* 기본 브랜드 컬러 */
:root {
  /* Primary Colors - 인디고 계열 (지혜) */
  --color-primary-50: #eef2ff;
  --color-primary-100: #e0e7ff;
  --color-primary-200: #c7d2fe;
  --color-primary-300: #a5b4fc;
  --color-primary-400: #818cf8;
  --color-primary-500: #6366f1;
  --color-primary-600: #4f46e5;
  --color-primary-700: #4338ca;
  --color-primary-800: #3730a3;
  --color-primary-900: #312e81;
  --color-primary-950: #1e1b4b;

  /* Mystic Colors - 핑크 계열 (운명) */
  --color-mystic-50: #fdf2f8;
  --color-mystic-100: #fce7f3;
  --color-mystic-200: #fbcfe8;
  --color-mystic-300: #f9a8d4;
  --color-mystic-400: #f472b6;
  --color-mystic-500: #ec4899;
  --color-mystic-600: #db2777;
  --color-mystic-700: #be185d;
  --color-mystic-800: #9d174d;
  --color-mystic-900: #831843;
  --color-mystic-950: #500724;

  /* Cosmic Colors - 사이안 계열 (에너지) */
  --color-cosmic-50: #ecfeff;
  --color-cosmic-100: #cffafe;
  --color-cosmic-200: #a5f3fc;
  --color-cosmic-300: #67e8f9;
  --color-cosmic-400: #22d3ee;
  --color-cosmic-500: #06b6d4;
  --color-cosmic-600: #0891b2;
  --color-cosmic-700: #0e7490;
  --color-cosmic-800: #155e75;
  --color-cosmic-900: #164e63;
  --color-cosmic-950: #083344;
}
```

#### **2. 오행 기반 의미 컬러**
```css
/* 오행(五行) 컬러 시스템 */
:root {
  /* 목(木) - 성장, 발전 */
  --color-wood-50: #f0fdf4;
  --color-wood-100: #dcfce7;
  --color-wood-200: #bbf7d0;
  --color-wood-300: #86efac;
  --color-wood-400: #4ade80;
  --color-wood-500: #22c55e;
  --color-wood-600: #16a34a;
  --color-wood-700: #15803d;
  --color-wood-800: #166534;
  --color-wood-900: #14532d;

  /* 화(火) - 열정, 에너지 */
  --color-fire-50: #fef2f2;
  --color-fire-100: #fee2e2;
  --color-fire-200: #fecaca;
  --color-fire-300: #fca5a5;
  --color-fire-400: #f87171;
  --color-fire-500: #ef4444;
  --color-fire-600: #dc2626;
  --color-fire-700: #b91c1c;
  --color-fire-800: #991b1b;
  --color-fire-900: #7f1d1d;

  /* 토(土) - 안정, 신뢰 */
  --color-earth-50: #fefce8;
  --color-earth-100: #fef9c3;
  --color-earth-200: #fef08a;
  --color-earth-300: #fde047;
  --color-earth-400: #facc15;
  --color-earth-500: #eab308;
  --color-earth-600: #ca8a04;
  --color-earth-700: #a16207;
  --color-earth-800: #854d0e;
  --color-earth-900: #713f12;

  /* 금(金) - 정밀, 완성 */
  --color-metal-50: #f8fafc;
  --color-metal-100: #f1f5f9;
  --color-metal-200: #e2e8f0;
  --color-metal-300: #cbd5e1;
  --color-metal-400: #94a3b8;
  --color-metal-500: #64748b;
  --color-metal-600: #475569;
  --color-metal-700: #334155;
  --color-metal-800: #1e293b;
  --color-metal-900: #0f172a;

  /* 수(水) - 지혜, 유연성 */
  --color-water-50: #eff6ff;
  --color-water-100: #dbeafe;
  --color-water-200: #bfdbfe;
  --color-water-300: #93c5fd;
  --color-water-400: #60a5fa;
  --color-water-500: #3b82f6;
  --color-water-600: #2563eb;
  --color-water-700: #1d4ed8;
  --color-water-800: #1e40af;
  --color-water-900: #1e3a8a;
}
```

#### **3. 상태 및 피드백 컬러**
```css
/* 상태 컬러 */
:root {
  /* Success - 성공, 긍정적 결과 */
  --color-success-50: #ecfdf5;
  --color-success-500: #10b981;
  --color-success-600: #059669;
  --color-success-700: #047857;

  /* Warning - 주의, 경고 */
  --color-warning-50: #fffbeb;
  --color-warning-500: #f59e0b;
  --color-warning-600: #d97706;
  --color-warning-700: #b45309;

  /* Error - 오류, 위험 */
  --color-error-50: #fef2f2;
  --color-error-500: #ef4444;
  --color-error-600: #dc2626;
  --color-error-700: #b91c1c;

  /* Info - 정보, 중립적 */
  --color-info-50: #eff6ff;
  --color-info-500: #3b82f6;
  --color-info-600: #2563eb;
  --color-info-700: #1d4ed8;
}
```

### **📐 타이포그래피 시스템**

#### **1. 폰트 패밀리 정의**
```css
:root {
  /* 한글 최적화 폰트 스택 */
  --font-family-sans: 
    "Pretendard Variable", "Pretendard", 
    -apple-system, BlinkMacSystemFont, system-ui, 
    "Segoe UI", "Malgun Gothic", "Apple SD Gothic Neo", 
    "Noto Sans KR", sans-serif;
    
  /* 영문 폰트 (브랜딩용) */
  --font-family-serif: 
    "Playfair Display", "Times New Roman", serif;
    
  /* 코드/데이터 표시용 */
  --font-family-mono: 
    "JetBrains Mono", "Fira Code", "Monaco", 
    "Cascadia Code", monospace;
    
  /* 장식적 텍스트 (로고, 특별한 제목) */
  --font-family-display: 
    "Gmarket Sans", "Pretendard Variable", sans-serif;
}
```

#### **2. 타이포그래피 스케일**
```css
:root {
  /* 글자 크기 - 모듈러 스케일 (1.25 비율) */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  --text-6xl: 3.75rem;    /* 60px */

  /* 행간 */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* 글자 간격 */
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.025em;

  /* 폰트 굵기 */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
}
```

### **📏 스페이싱 및 레이아웃**

#### **1. 스페이싱 시스템**
```css
:root {
  /* 기본 스페이싱 단위 (4px 기반) */
  --space-0: 0;
  --space-px: 1px;
  --space-0_5: 0.125rem;  /* 2px */
  --space-1: 0.25rem;     /* 4px */
  --space-1_5: 0.375rem;  /* 6px */
  --space-2: 0.5rem;      /* 8px */
  --space-2_5: 0.625rem;  /* 10px */
  --space-3: 0.75rem;     /* 12px */
  --space-3_5: 0.875rem;  /* 14px */
  --space-4: 1rem;        /* 16px */
  --space-5: 1.25rem;     /* 20px */
  --space-6: 1.5rem;      /* 24px */
  --space-7: 1.75rem;     /* 28px */
  --space-8: 2rem;        /* 32px */
  --space-10: 2.5rem;     /* 40px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  --space-24: 6rem;       /* 96px */
  --space-32: 8rem;       /* 128px */

  /* 컨테이너 너비 */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
}
```

#### **2. 그리드 시스템**
```css
/* 12-컬럼 그리드 시스템 */
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-4);
}

.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-8 { grid-column: span 8; }
.col-12 { grid-column: span 12; }

/* 반응형 그리드 */
@media (max-width: 768px) {
  .col-md-6 { grid-column: span 6; }
  .col-md-12 { grid-column: span 12; }
}
```

---

## 🧩 **기본 컴포넌트 아키텍처**

### **🔘 Button 컴포넌트**

#### **1. Button 타입 정의**
```typescript
// components/Button/Button.types.ts
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** 버튼 변형 스타일 */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'mystic' | 'cosmic';
  
  /** 버튼 크기 */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  
  /** 로딩 상태 */
  loading?: boolean;
  
  /** 로딩 텍스트 */
  loadingText?: string;
  
  /** 아이콘 (앞) */
  leftIcon?: React.ReactElement;
  
  /** 아이콘 (뒤) */
  rightIcon?: React.ReactElement;
  
  /** 전체 너비 사용 */
  fullWidth?: boolean;
  
  /** 오행 컬러 */
  elementColor?: 'wood' | 'fire' | 'earth' | 'metal' | 'water';
  
  /** 접근성 라벨 */
  'aria-label'?: string;
}

export interface ButtonStyleProps {
  variant: ButtonProps['variant'];
  size: ButtonProps['size'];
  elementColor?: ButtonProps['elementColor'];
  fullWidth?: boolean;
  disabled?: boolean;
  loading?: boolean;
}
```

#### **2. Button 스타일링**
```css
/* components/Button/Button.styles.css */
.heal7-button {
  /* 기본 스타일 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-family-sans);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  border: 1px solid transparent;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  outline: none;
  
  /* 포커스 스타일 */
  &:focus-visible {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }
  
  /* 비활성화 스타일 */
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }
  
  /* 로딩 스타일 */
  &[data-loading="true"] {
    cursor: wait;
    
    .button-content {
      opacity: 0.6;
    }
  }
}

/* 크기 변형 */
.heal7-button--size-xs {
  padding: var(--space-1) var(--space-2);
  font-size: var(--text-xs);
  gap: var(--space-1);
}

.heal7-button--size-sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  gap: var(--space-1_5);
}

.heal7-button--size-md {
  padding: var(--space-2_5) var(--space-4);
  font-size: var(--text-base);
  gap: var(--space-2);
}

.heal7-button--size-lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-lg);
  gap: var(--space-2);
}

.heal7-button--size-xl {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-xl);
  gap: var(--space-3);
}

/* 변형 스타일 */
.heal7-button--variant-primary {
  background-color: var(--color-primary-600);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-primary-700);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }
  
  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(99, 102, 241, 0.4);
  }
}

.heal7-button--variant-mystic {
  background: linear-gradient(135deg, var(--color-mystic-500), var(--color-mystic-600));
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
  }
  
  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(236, 72, 153, 0.5);
    
    &::before {
      left: 100%;
    }
  }
}

.heal7-button--variant-cosmic {
  background: linear-gradient(135deg, var(--color-cosmic-500), var(--color-cosmic-600));
  color: white;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, var(--color-cosmic-600), var(--color-cosmic-700));
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5);
  }
}

/* 오행 컬러 변형 */
.heal7-button--element-wood {
  background-color: var(--color-wood-500);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-wood-600);
  }
}

.heal7-button--element-fire {
  background-color: var(--color-fire-500);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-fire-600);
  }
}

.heal7-button--element-earth {
  background-color: var(--color-earth-500);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-earth-600);
  }
}

.heal7-button--element-metal {
  background-color: var(--color-metal-500);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-metal-600);
  }
}

.heal7-button--element-water {
  background-color: var(--color-water-500);
  color: white;
  
  &:hover:not(:disabled) {
    background-color: var(--color-water-600);
  }
}

/* 전체 너비 */
.heal7-button--full-width {
  width: 100%;
}

/* 로딩 스피너 */
.heal7-button__spinner {
  width: 1em;
  height: 1em;
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

#### **3. Button 컴포넌트 구현**
```tsx
// components/Button/Button.tsx
import React from 'react';
import { cn } from '../../utils/classNames';
import { ButtonProps } from './Button.types';
import './Button.styles.css';

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      loading = false,
      loadingText,
      leftIcon,
      rightIcon,
      fullWidth = false,
      elementColor,
      className,
      disabled,
      'aria-label': ariaLabel,
      ...props
    },
    ref
  ) => {
    const buttonClasses = cn(
      'heal7-button',
      `heal7-button--variant-${variant}`,
      `heal7-button--size-${size}`,
      elementColor && `heal7-button--element-${elementColor}`,
      fullWidth && 'heal7-button--full-width',
      className
    );

    const isDisabled = disabled || loading;
    const buttonContent = loading && loadingText ? loadingText : children;

    return (
      <button
        ref={ref}
        className={buttonClasses}
        disabled={isDisabled}
        data-loading={loading}
        aria-label={ariaLabel}
        {...props}
      >
        {loading && (
          <span className="heal7-button__spinner" aria-hidden="true" />
        )}
        
        {!loading && leftIcon && (
          <span className="heal7-button__icon-left" aria-hidden="true">
            {leftIcon}
          </span>
        )}
        
        <span className="button-content">{buttonContent}</span>
        
        {!loading && rightIcon && (
          <span className="heal7-button__icon-right" aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
```

### **💳 Card 컴포넌트**

#### **1. Card 타입 정의**
```typescript
// components/Card/Card.types.ts
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** 카드 변형 스타일 */
  variant?: 'default' | 'outline' | 'elevated' | 'mystic' | 'cosmic';
  
  /** 카드 크기 */
  size?: 'sm' | 'md' | 'lg';
  
  /** 호버 효과 */
  hoverable?: boolean;
  
  /** 클릭 가능 여부 */
  clickable?: boolean;
  
  /** 오행 컬러 테마 */
  elementTheme?: 'wood' | 'fire' | 'earth' | 'metal' | 'water';
  
  /** 카드 헤더 */
  header?: React.ReactNode;
  
  /** 카드 푸터 */
  footer?: React.ReactNode;
  
  /** 카드 이미지 */
  image?: {
    src: string;
    alt: string;
    aspectRatio?: 'square' | 'video' | 'wide';
  };
}
```

#### **2. Card 구현**
```tsx
// components/Card/Card.tsx
import React from 'react';
import { cn } from '../../utils/classNames';
import { CardProps } from './Card.types';
import './Card.styles.css';

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  size = 'md',
  hoverable = false,
  clickable = false,
  elementTheme,
  header,
  footer,
  image,
  className,
  ...props
}) => {
  const cardClasses = cn(
    'heal7-card',
    `heal7-card--variant-${variant}`,
    `heal7-card--size-${size}`,
    hoverable && 'heal7-card--hoverable',
    clickable && 'heal7-card--clickable',
    elementTheme && `heal7-card--element-${elementTheme}`,
    className
  );

  return (
    <div className={cardClasses} {...props}>
      {image && (
        <div className={cn('heal7-card__image', `aspect-${image.aspectRatio || 'video'}`)}>
          <img src={image.src} alt={image.alt} />
        </div>
      )}
      
      {header && (
        <div className="heal7-card__header">
          {header}
        </div>
      )}
      
      <div className="heal7-card__content">
        {children}
      </div>
      
      {footer && (
        <div className="heal7-card__footer">
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;
```

---

## 🔮 **사주명리학 특화 컴포넌트**

### **📊 사주 4개 기둥 표시 컴포넌트**

#### **1. SajuPillars 타입 정의**
```typescript
// components/SajuPillars/SajuPillars.types.ts
export interface SajuPillar {
  heavenlyStem: string;  // 천간 (갑, 을, 병, 정...)
  earthlyBranch: string; // 지지 (자, 축, 인, 묘...)
  element: 'wood' | 'fire' | 'earth' | 'metal' | 'water';
  polarity: 'yang' | 'yin';
}

export interface SajuData {
  year: SajuPillar;
  month: SajuPillar;
  day: SajuPillar;
  hour: SajuPillar;
  birthInfo: {
    date: string;
    time: string;
    location: string;
  };
}

export interface SajuPillarsProps {
  /** 사주 데이터 */
  data: SajuData;
  
  /** 표시 방향 */
  orientation?: 'horizontal' | 'vertical';
  
  /** 크기 */
  size?: 'sm' | 'md' | 'lg';
  
  /** 상세 정보 표시 */
  showDetails?: boolean;
  
  /** 애니메이션 효과 */
  animated?: boolean;
  
  /** 클릭 이벤트 */
  onPillarClick?: (pillar: 'year' | 'month' | 'day' | 'hour', data: SajuPillar) => void;
}
```

#### **2. SajuPillars 구현**
```tsx
// components/SajuPillars/SajuPillars.tsx
import React from 'react';
import { cn } from '../../utils/classNames';
import { SajuPillarsProps, SajuPillar } from './SajuPillars.types';
import { Card } from '../Card/Card';
import './SajuPillars.styles.css';

const PillarCard: React.FC<{
  pillar: SajuPillar;
  label: string;
  size: 'sm' | 'md' | 'lg';
  animated: boolean;
  onClick?: () => void;
}> = ({ pillar, label, size, animated, onClick }) => {
  const cardClasses = cn(
    'saju-pillar-card',
    `saju-pillar-card--size-${size}`,
    animated && 'saju-pillar-card--animated'
  );

  return (
    <Card
      className={cardClasses}
      elementTheme={pillar.element}
      clickable={!!onClick}
      hoverable={!!onClick}
      onClick={onClick}
    >
      <div className="saju-pillar-card__header">
        <span className="saju-pillar-card__label">{label}</span>
        <span className={cn('saju-pillar-card__polarity', `polarity-${pillar.polarity}`)}>
          {pillar.polarity === 'yang' ? '☯' : '☰'}
        </span>
      </div>
      
      <div className="saju-pillar-card__characters">
        <div className="saju-pillar-card__heavenly-stem">
          <span className="character">{pillar.heavenlyStem}</span>
          <span className="reading">천간</span>
        </div>
        <div className="saju-pillar-card__earthly-branch">
          <span className="character">{pillar.earthlyBranch}</span>
          <span className="reading">지지</span>
        </div>
      </div>
      
      <div className={cn('saju-pillar-card__element', `element-${pillar.element}`)}>
        <span className="element-name">{getElementName(pillar.element)}</span>
        <span className="element-symbol">{getElementSymbol(pillar.element)}</span>
      </div>
    </Card>
  );
};

export const SajuPillars: React.FC<SajuPillarsProps> = ({
  data,
  orientation = 'horizontal',
  size = 'md',
  showDetails = true,
  animated = true,
  onPillarClick
}) => {
  const containerClasses = cn(
    'saju-pillars',
    `saju-pillars--orientation-${orientation}`,
    `saju-pillars--size-${size}`
  );

  const pillars = [
    { key: 'year' as const, data: data.year, label: '년주 (年柱)' },
    { key: 'month' as const, data: data.month, label: '월주 (月柱)' },
    { key: 'day' as const, data: data.day, label: '일주 (日柱)' },
    { key: 'hour' as const, data: data.hour, label: '시주 (時柱)' }
  ];

  return (
    <div className={containerClasses}>
      {showDetails && (
        <div className="saju-pillars__birth-info">
          <Card variant="outline" size="sm">
            <div className="birth-info__content">
              <div className="birth-info__item">
                <span className="label">생년월일:</span>
                <span className="value">{data.birthInfo.date}</span>
              </div>
              <div className="birth-info__item">
                <span className="label">출생시간:</span>
                <span className="value">{data.birthInfo.time}</span>
              </div>
              <div className="birth-info__item">
                <span className="label">출생지:</span>
                <span className="value">{data.birthInfo.location}</span>
              </div>
            </div>
          </Card>
        </div>
      )}
      
      <div className="saju-pillars__grid">
        {pillars.map(({ key, data: pillarData, label }, index) => (
          <div
            key={key}
            className="saju-pillars__item"
            style={{ animationDelay: animated ? `${index * 0.1}s` : '0s' }}
          >
            <PillarCard
              pillar={pillarData}
              label={label}
              size={size}
              animated={animated}
              onClick={onPillarClick ? () => onPillarClick(key, pillarData) : undefined}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

// 헬퍼 함수들
function getElementName(element: string): string {
  const names = {
    wood: '목(木)',
    fire: '화(火)',
    earth: '토(土)',
    metal: '금(金)',
    water: '수(水)'
  };
  return names[element as keyof typeof names] || element;
}

function getElementSymbol(element: string): string {
  const symbols = {
    wood: '🌲',
    fire: '🔥',
    earth: '🏔️',
    metal: '⚡',
    water: '💧'
  };
  return symbols[element as keyof typeof symbols] || '';
}

export default SajuPillars;
```

### **📈 오행 균형 시각화 컴포넌트**

#### **1. FiveElementsBalance 구현**
```tsx
// components/FiveElementsBalance/FiveElementsBalance.tsx
import React, { useRef, useEffect } from 'react';
import { cn } from '../../utils/classNames';
import { Card } from '../Card/Card';
import './FiveElementsBalance.styles.css';

export interface ElementBalance {
  wood: number;
  fire: number;
  earth: number;
  metal: number;
  water: number;
}

export interface FiveElementsBalanceProps {
  balance: ElementBalance;
  size?: 'sm' | 'md' | 'lg';
  showLabels?: boolean;
  showValues?: boolean;
  animated?: boolean;
  chartType?: 'radar' | 'bar' | 'donut';
}

export const FiveElementsBalance: React.FC<FiveElementsBalanceProps> = ({
  balance,
  size = 'md',
  showLabels = true,
  showValues = true,
  animated = true,
  chartType = 'radar'
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  const elements = [
    { key: 'wood', name: '목(木)', value: balance.wood, color: 'var(--color-wood-500)', symbol: '🌲' },
    { key: 'fire', name: '화(火)', value: balance.fire, color: 'var(--color-fire-500)', symbol: '🔥' },
    { key: 'earth', name: '토(土)', value: balance.earth, color: 'var(--color-earth-500)', symbol: '🏔️' },
    { key: 'metal', name: '금(金)', value: balance.metal, color: 'var(--color-metal-500)', symbol: '⚡' },
    { key: 'water', name: '수(水)', value: balance.water, color: 'var(--color-water-500)', symbol: '💧' }
  ];

  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const size = canvas.width;
    const center = size / 2;
    const radius = size * 0.35;

    // 캔버스 초기화
    ctx.clearRect(0, 0, size, size);

    if (chartType === 'radar') {
      drawRadarChart(ctx, center, radius, elements, animated);
    } else if (chartType === 'donut') {
      drawDonutChart(ctx, center, radius, elements, animated);
    }
  }, [balance, chartType, animated]);

  const containerClasses = cn(
    'five-elements-balance',
    `five-elements-balance--size-${size}`,
    `five-elements-balance--chart-${chartType}`
  );

  return (
    <Card className={containerClasses} variant="elevated">
      <div className="five-elements-balance__header">
        <h3 className="five-elements-balance__title">오행 균형 분석</h3>
        <p className="five-elements-balance__subtitle">
          당신의 사주에 나타난 오행의 균형을 시각화했습니다
        </p>
      </div>
      
      <div className="five-elements-balance__chart">
        <canvas
          ref={canvasRef}
          width={300}
          height={300}
          className="five-elements-balance__canvas"
        />
      </div>
      
      {showLabels && (
        <div className="five-elements-balance__legend">
          {elements.map((element) => (
            <div key={element.key} className="legend-item">
              <span className="legend-item__symbol">{element.symbol}</span>
              <span className="legend-item__name">{element.name}</span>
              {showValues && (
                <span className="legend-item__value">{element.value}%</span>
              )}
              <div 
                className="legend-item__bar"
                style={{
                  width: `${element.value}%`,
                  backgroundColor: element.color
                }}
              />
            </div>
          ))}
        </div>
      )}
      
      <div className="five-elements-balance__interpretation">
        <Card variant="outline" size="sm">
          <h4>균형 해석</h4>
          <p>{getBalanceInterpretation(balance)}</p>
        </Card>
      </div>
    </Card>
  );
};

// 레이더 차트 그리기
function drawRadarChart(
  ctx: CanvasRenderingContext2D,
  centerX: number,
  centerY: number,
  radius: number,
  elements: any[],
  animated: boolean
) {
  const angleStep = (2 * Math.PI) / elements.length;
  
  // 배경 그리드 그리기
  ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
  ctx.lineWidth = 1;
  
  for (let i = 1; i <= 5; i++) {
    const gridRadius = (radius * i) / 5;
    ctx.beginPath();
    ctx.arc(centerX, centerY, gridRadius, 0, 2 * Math.PI);
    ctx.stroke();
  }
  
  // 축 그리기
  elements.forEach((_, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const x = centerX + Math.cos(angle) * radius;
    const y = centerY + Math.sin(angle) * radius;
    
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(x, y);
    ctx.stroke();
  });
  
  // 데이터 영역 그리기
  ctx.fillStyle = 'rgba(99, 102, 241, 0.2)';
  ctx.strokeStyle = 'rgba(99, 102, 241, 0.8)';
  ctx.lineWidth = 2;
  
  ctx.beginPath();
  elements.forEach((element, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const value = element.value / 100; // 0-1로 정규화
    const x = centerX + Math.cos(angle) * radius * value;
    const y = centerY + Math.sin(angle) * radius * value;
    
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  
  // 포인트 그리기
  elements.forEach((element, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const value = element.value / 100;
    const x = centerX + Math.cos(angle) * radius * value;
    const y = centerY + Math.sin(angle) * radius * value;
    
    ctx.fillStyle = element.color;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fill();
  });
}

// 도넛 차트 그리기
function drawDonutChart(
  ctx: CanvasRenderingContext2D,
  centerX: number,
  centerY: number,
  radius: number,
  elements: any[],
  animated: boolean
) {
  const total = elements.reduce((sum, el) => sum + el.value, 0);
  let currentAngle = -Math.PI / 2;
  
  elements.forEach((element) => {
    const sliceAngle = (element.value / total) * 2 * Math.PI;
    
    // 외부 호
    ctx.fillStyle = element.color;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
    ctx.arc(centerX, centerY, radius * 0.6, currentAngle + sliceAngle, currentAngle, true);
    ctx.closePath();
    ctx.fill();
    
    currentAngle += sliceAngle;
  });
}

// 균형 해석 함수
function getBalanceInterpretation(balance: ElementBalance): string {
  const max = Math.max(...Object.values(balance));
  const min = Math.min(...Object.values(balance));
  const difference = max - min;
  
  if (difference <= 20) {
    return "오행이 매우 균형잡혀 있습니다. 안정적이고 조화로운 성격을 가지고 있을 것입니다.";
  } else if (difference <= 40) {
    return "오행의 균형이 적당합니다. 특정 분야에서 강점을 보이면서도 전체적으로 조화를 이룹니다.";
  } else {
    return "오행의 편차가 큽니다. 뚜렷한 개성과 특장점을 가지고 있지만, 균형을 맞추는 노력이 필요합니다.";
  }
}

export default FiveElementsBalance;
```

### **🎴 타로카드 레이아웃 컴포넌트**

#### **1. TarotSpread 구현**
```tsx
// components/TarotSpread/TarotSpread.tsx
import React, { useState } from 'react';
import { cn } from '../../utils/classNames';
import { Card } from '../Card/Card';
import './TarotSpread.styles.css';

export interface TarotCard {
  id: string;
  name: string;
  image: string;
  meaning: string;
  reversed: boolean;
  position?: string;
}

export interface TarotSpreadProps {
  cards: TarotCard[];
  spreadType: 'three-card' | 'celtic-cross' | 'single-card';
  interactive?: boolean;
  showMeanings?: boolean;
  onCardClick?: (card: TarotCard) => void;
}

export const TarotSpread: React.FC<TarotSpreadProps> = ({
  cards,
  spreadType,
  interactive = true,
  showMeanings = false,
  onCardClick
}) => {
  const [flippedCards, setFlippedCards] = useState<Set<string>>(new Set());
  
  const handleCardClick = (card: TarotCard) => {
    if (interactive) {
      setFlippedCards(prev => {
        const newSet = new Set(prev);
        if (newSet.has(card.id)) {
          newSet.delete(card.id);
        } else {
          newSet.add(card.id);
        }
        return newSet;
      });
    }
    onCardClick?.(card);
  };

  const containerClasses = cn(
    'tarot-spread',
    `tarot-spread--type-${spreadType}`,
    interactive && 'tarot-spread--interactive'
  );

  return (
    <div className={containerClasses}>
      <div className="tarot-spread__layout">
        {cards.map((card, index) => (
          <TarotCardComponent
            key={card.id}
            card={card}
            index={index}
            isFlipped={flippedCards.has(card.id)}
            showMeaning={showMeanings}
            onClick={() => handleCardClick(card)}
            spreadType={spreadType}
          />
        ))}
      </div>
      
      {showMeanings && (
        <div className="tarot-spread__meanings">
          {cards.map(card => (
            <Card key={`meaning-${card.id}`} className="tarot-meaning-card">
              <h4>{card.position || card.name}</h4>
              <p>{card.meaning}</p>
              {card.reversed && (
                <span className="reversed-indicator">🔄 역방향</span>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

const TarotCardComponent: React.FC<{
  card: TarotCard;
  index: number;
  isFlipped: boolean;
  showMeaning: boolean;
  onClick: () => void;
  spreadType: string;
}> = ({ card, index, isFlipped, showMeaning, onClick, spreadType }) => {
  const cardClasses = cn(
    'tarot-card',
    `tarot-card--position-${index}`,
    `tarot-card--spread-${spreadType}`,
    isFlipped && 'tarot-card--flipped',
    card.reversed && 'tarot-card--reversed'
  );

  return (
    <div className={cardClasses} onClick={onClick}>
      <div className="tarot-card__inner">
        <div className="tarot-card__front">
          <div className="tarot-card__back-pattern" />
        </div>
        <div className="tarot-card__back">
          <img src={card.image} alt={card.name} />
          <div className="tarot-card__title">{card.name}</div>
          {card.position && (
            <div className="tarot-card__position">{card.position}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TarotSpread;
```

---

## 📱 **반응형 및 접근성**

### **🔧 반응형 디자인 시스템**

#### **1. 브레이크포인트 정의**
```css
/* 반응형 브레이크포인트 */
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* 미디어 쿼리 믹신 */
@custom-media --screen-sm (min-width: 640px);
@custom-media --screen-md (min-width: 768px);
@custom-media --screen-lg (min-width: 1024px);
@custom-media --screen-xl (min-width: 1280px);
@custom-media --screen-2xl (min-width: 1536px);

/* 모바일 우선 반응형 유틸리티 */
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

@media (--screen-sm) {
  .container { max-width: 640px; }
}

@media (--screen-md) {
  .container { max-width: 768px; }
}

@media (--screen-lg) {
  .container { 
    max-width: 1024px;
    padding: 0 var(--space-6);
  }
}

@media (--screen-xl) {
  .container { max-width: 1280px; }
}
```

#### **2. 반응형 컴포넌트 예제**
```tsx
// hooks/useResponsive.ts
import { useState, useEffect } from 'react';

export interface BreakpointValues {
  sm: boolean;
  md: boolean;
  lg: boolean;
  xl: boolean;
  '2xl': boolean;
}

export const useResponsive = (): BreakpointValues => {
  const [breakpoints, setBreakpoints] = useState<BreakpointValues>({
    sm: false,
    md: false,
    lg: false,
    xl: false,
    '2xl': false
  });

  useEffect(() => {
    const mediaQueries = {
      sm: '(min-width: 640px)',
      md: '(min-width: 768px)',
      lg: '(min-width: 1024px)',
      xl: '(min-width: 1280px)',
      '2xl': '(min-width: 1536px)'
    };

    const mediaQueryLists = Object.entries(mediaQueries).map(([key, query]) => ({
      key: key as keyof BreakpointValues,
      mql: window.matchMedia(query)
    }));

    const updateBreakpoints = () => {
      setBreakpoints(
        mediaQueryLists.reduce((acc, { key, mql }) => {
          acc[key] = mql.matches;
          return acc;
        }, {} as BreakpointValues)
      );
    };

    // 초기 설정
    updateBreakpoints();

    // 리스너 등록
    mediaQueryLists.forEach(({ mql }) => {
      mql.addListener(updateBreakpoints);
    });

    // 정리
    return () => {
      mediaQueryLists.forEach(({ mql }) => {
        mql.removeListener(updateBreakpoints);
      });
    };
  }, []);

  return breakpoints;
};

// 반응형 컴포넌트 예제
export const ResponsiveSajuPillars: React.FC<SajuPillarsProps> = (props) => {
  const breakpoints = useResponsive();
  
  const orientation = breakpoints.md ? 'horizontal' : 'vertical';
  const size = breakpoints.lg ? 'lg' : breakpoints.md ? 'md' : 'sm';
  
  return (
    <SajuPillars
      {...props}
      orientation={orientation}
      size={size}
    />
  );
};
```

### **♿ 접근성 (Accessibility) 구현**

#### **1. 접근성 유틸리티**
```tsx
// utils/accessibility.ts
export const announceToScreenReader = (message: string) => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', 'polite');
  announcement.setAttribute('aria-atomic', 'true');
  announcement.style.position = 'absolute';
  announcement.style.left = '-10000px';
  announcement.style.width = '1px';
  announcement.style.height = '1px';
  announcement.style.overflow = 'hidden';
  
  document.body.appendChild(announcement);
  announcement.textContent = message;
  
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

export const trapFocus = (element: HTMLElement) => {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstFocusable = focusableElements[0] as HTMLElement;
  const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement;
  
  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return;
    
    if (e.shiftKey) {
      if (document.activeElement === firstFocusable) {
        lastFocusable.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastFocusable) {
        firstFocusable.focus();
        e.preventDefault();
      }
    }
  };
  
  element.addEventListener('keydown', handleTabKey);
  firstFocusable?.focus();
  
  return () => {
    element.removeEventListener('keydown', handleTabKey);
  };
};
```

#### **2. 접근성 강화 컴포넌트**
```tsx
// components/AccessibleModal/AccessibleModal.tsx
import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { trapFocus, announceToScreenReader } from '../../utils/accessibility';

export interface AccessibleModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  closeOnEscape?: boolean;
  closeOnOverlayClick?: boolean;
}

export const AccessibleModal: React.FC<AccessibleModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  closeOnEscape = true,
  closeOnOverlayClick = true
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement;
      announceToScreenReader(`모달 열림: ${title}`);
      
      if (modalRef.current) {
        const cleanup = trapFocus(modalRef.current);
        return cleanup;
      }
    } else {
      previousActiveElement.current?.focus();
    }
  }, [isOpen, title]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && closeOnEscape) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, closeOnEscape, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div 
      className="modal-overlay"
      onClick={closeOnOverlayClick ? onClose : undefined}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        ref={modalRef}
        className="modal-content"
        onClick={e => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="모달 닫기"
          >
            ✕
          </button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
};
```

---

## 📚 **Storybook 문서화 시스템**

### **📖 Storybook 설정**

#### **1. Storybook 메인 구성**
```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx|mdx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    '@storybook/addon-viewport',
    '@storybook/addon-backgrounds',
    '@storybook/addon-measure',
    '@storybook/addon-outline'
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {}
  },
  typescript: {
    check: false,
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: (prop) => (prop.parent ? !/node_modules/.test(prop.parent.fileName) : true),
    },
  },
  docs: {
    autodocs: 'tag',
  },
};

export default config;
```

#### **2. Storybook 테마 설정**
```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import { withThemeByClassName } from '@storybook/addon-styling';
import '../src/styles/global.css';

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
        { name: 'mystic', value: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
      ],
    },
    viewport: {
      viewports: {
        mobile: {
          name: 'Mobile',
          styles: { width: '375px', height: '667px' },
        },
        tablet: {
          name: 'Tablet',
          styles: { width: '768px', height: '1024px' },
        },
        desktop: {
          name: 'Desktop',
          styles: { width: '1440px', height: '900px' },
        },
      },
    },
  },
  decorators: [
    withThemeByClassName({
      themes: {
        light: 'theme-light',
        dark: 'theme-dark',
      },
      defaultTheme: 'light',
    }),
  ],
};

export default preview;
```

#### **3. 컴포넌트 스토리 예제**
```typescript
// components/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
import { HeartIcon, PlusIcon } from '@heroicons/react/24/outline';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'HEAL7 옴니버스 플랫폼의 기본 버튼 컴포넌트입니다. Mystic Aurora 디자인 시스템을 따르며, 접근성과 사용성을 고려하여 설계되었습니다.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'outline', 'ghost', 'link', 'mystic', 'cosmic'],
      description: '버튼의 시각적 스타일 변형',
    },
    size: {
      control: { type: 'select' },
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
      description: '버튼의 크기',
    },
    elementColor: {
      control: { type: 'select' },
      options: ['wood', 'fire', 'earth', 'metal', 'water'],
      description: '오행 기반 컬러 테마',
    },
    loading: {
      control: { type: 'boolean' },
      description: '로딩 상태 표시',
    },
    disabled: {
      control: { type: 'boolean' },
      description: '비활성화 상태',
    },
    fullWidth: {
      control: { type: 'boolean' },
      description: '전체 너비 사용',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// 기본 스토리
export const Default: Story = {
  args: {
    children: '기본 버튼',
    variant: 'primary',
    size: 'md',
  },
};

// 변형 스토리들
export const Variants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
      <Button variant="mystic">Mystic</Button>
      <Button variant="cosmic">Cosmic</Button>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: '다양한 버튼 변형 스타일을 보여줍니다.',
      },
    },
  },
};

// 크기 스토리
export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
      <Button size="xs">XS</Button>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
      <Button size="xl">XL</Button>
    </div>
  ),
};

// 오행 컬러 스토리
export const ElementColors: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <Button elementColor="wood">목(木) - 성장</Button>
      <Button elementColor="fire">화(火) - 열정</Button>
      <Button elementColor="earth">토(土) - 안정</Button>
      <Button elementColor="metal">금(金) - 정밀</Button>
      <Button elementColor="water">수(水) - 지혜</Button>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: '오행 기반 컬러 시스템을 적용한 버튼들입니다.',
      },
    },
  },
};

// 아이콘 포함 스토리
export const WithIcons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexDirection: 'column', alignItems: 'flex-start' }}>
      <Button leftIcon={<PlusIcon width={16} height={16} />}>
        추가하기
      </Button>
      <Button rightIcon={<HeartIcon width={16} height={16} />}>
        좋아요
      </Button>
      <Button 
        leftIcon={<PlusIcon width={16} height={16} />}
        rightIcon={<HeartIcon width={16} height={16} />}
      >
        양쪽 아이콘
      </Button>
    </div>
  ),
};

// 로딩 상태 스토리
export const Loading: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexDirection: 'column', alignItems: 'flex-start' }}>
      <Button loading>로딩 중...</Button>
      <Button loading loadingText="저장 중...">저장하기</Button>
      <Button loading variant="mystic">신비로운 계산 중...</Button>
    </div>
  ),
};

// 접근성 테스트 스토리
export const Accessibility: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexDirection: 'column', alignItems: 'flex-start' }}>
      <Button aria-label="새 항목 추가">+</Button>
      <Button disabled>비활성화된 버튼</Button>
      <Button variant="outline" aria-describedby="button-description">
        도움말이 있는 버튼
      </Button>
      <div id="button-description" style={{ fontSize: '12px', color: '#666' }}>
        이 버튼은 특별한 기능을 수행합니다.
      </div>
    </div>
  ),
  parameters: {
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
          {
            id: 'button-name',
            enabled: true,
          },
        ],
      },
    },
  },
};

// 사주 특화 사용 사례
export const SajuUseCases: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '8px', flexDirection: 'column', alignItems: 'flex-start' }}>
      <Button variant="mystic" size="lg">
        🔮 사주 보기
      </Button>
      <Button variant="cosmic" elementColor="water">
        💧 수(水) 운세 확인
      </Button>
      <Button variant="outline" elementColor="fire">
        🔥 화(火) 기운 강화
      </Button>
      <Button variant="primary" loading loadingText="사주 계산 중...">
        운명 분석하기
      </Button>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: '사주명리학 서비스에서 실제 사용되는 버튼 예시들입니다.',
      },
    },
  },
};
```

---

## 🚀 **빌드 및 배포 설정**

### **📦 패키지 빌드 설정**

#### **1. Vite 라이브러리 빌드 구성**
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import dts from 'vite-plugin-dts';

export default defineConfig({
  plugins: [
    react(),
    dts({
      insertTypesEntry: true,
      include: ['src/components/**/*', 'src/utils/**/*', 'src/hooks/**/*'],
      exclude: ['src/**/*.stories.*', 'src/**/*.test.*'],
    }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'Heal7UI',
      formats: ['es', 'umd'],
      fileName: (format) => `heal7-ui.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    sourcemap: true,
    minify: 'esbuild',
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
});
```

#### **2. 패키지 설정**
```json
{
  "name": "@heal7/ui",
  "version": "1.0.0",
  "description": "HEAL7 옴니버스 플랫폼 UI 컴포넌트 라이브러리",
  "type": "module",
  "main": "./dist/heal7-ui.umd.js",
  "module": "./dist/heal7-ui.es.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/heal7-ui.es.js",
      "require": "./dist/heal7-ui.umd.js",
      "types": "./dist/index.d.ts"
    },
    "./styles": "./dist/style.css"
  },
  "files": [
    "dist",
    "README.md"
  ],
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "build:storybook": "storybook build",
    "preview": "vite preview",
    "storybook": "storybook dev -p 6006",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "type-check": "tsc --noEmit",
    "chromatic": "chromatic --project-token=PROJECT_TOKEN"
  },
  "keywords": [
    "react",
    "ui",
    "components",
    "design-system",
    "fortune-telling",
    "saju",
    "tarot",
    "mystic"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/heal7/ui-components.git"
  },
  "peerDependencies": {
    "react": "^18.0.0 || ^19.0.0",
    "react-dom": "^18.0.0 || ^19.0.0"
  },
  "devDependencies": {
    "@storybook/addon-a11y": "^7.6.0",
    "@storybook/addon-essentials": "^7.6.0",
    "@storybook/addon-interactions": "^7.6.0",
    "@storybook/addon-links": "^7.6.0",
    "@storybook/addon-viewport": "^7.6.0",
    "@storybook/blocks": "^7.6.0",
    "@storybook/react": "^7.6.0",
    "@storybook/react-vite": "^7.6.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "chromatic": "^10.0.0",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "eslint-plugin-storybook": "^0.6.15",
    "storybook": "^7.6.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vite-plugin-dts": "^3.7.0",
    "vitest": "^1.1.0"
  }
}
```

---

## 🏆 **결론**

### **✨ UI 컴포넌트 라이브러리 핵심 가치**

이 UI 컴포넌트 라이브러리는 **사주명리학 특화 설계**와 **현대적 개발 경험**을 완벽히 융합하여 다음을 달성합니다:

#### **🎨 핵심 UI/UX 성과**
1. **🔮 사주명리학 특화**: 4개 기둥, 오행 균형, 타로카드 등 전문 컴포넌트 완비
2. **🌈 Mystic Aurora 테마**: 오행 기반 컬러 시스템과 동양적 미학 구현
3. **♿ 접근성 우선**: WCAG 2.1 AA 준수, 스크린 리더 완벽 지원
4. **📱 완전 반응형**: 모바일 우선 설계, 모든 디바이스 최적화
5. **⚡ 개발자 경험**: TypeScript 완전 지원, Storybook 문서화, 트리 셰이킹

#### **🎯 즉시 사용 가능**
```bash
# 🎨 UI 컴포넌트 라이브러리 확인
cat CORE/reference-docs/technical-standards/UI-Component-Library-Architecture-v1.0*.md

# 📦 패키지 설치 및 사용
npm install @heal7/ui

# 🚀 컴포넌트 개발 시작
import { Button, SajuPillars, FiveElementsBalance } from '@heal7/ui';
import '@heal7/ui/styles';
```

**이제 사주명리학의 깊이와 현대적 UI/UX가 완벽히 조화된 컴포넌트 라이브러리가 완성되었습니다!** 🎨✨

---

*📅 UI 컴포넌트 라이브러리 완성일: 2025-08-18 19:45 KST*  
*🎨 컴포넌트: 사주명리학 특화 + 범용 UI 통합*  
*🎯 다음 단계: 접근성 및 국제화 전략*