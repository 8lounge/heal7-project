# 🎨 HEAL7 사주사이트 디자인 시스템 아키텍처 v1.0

> **프로젝트**: HEAL7 사주사이트 통합 디자인 시스템  
> **버전**: v1.0.0  
> **설계일**: 2025-08-18  
> **최종 수정**: 2025-08-18 14:30 KST  
> **설계자**: HEAL7 Design & Architecture Team  
> **컨셉**: 신비로운 우주적 아름다움과 현대적 UX의 조화

## 🌌 **디자인 철학**

### **핵심 가치**
- **🔮 Mystical**: 신비롭고 영적인 경험 제공
- **✨ Intuitive**: 직관적이고 쉬운 사용성
- **🌟 Harmonious**: 조화로운 시각적 균형
- **🚀 Modern**: 현대적인 기술과 트렌드 반영

### **디자인 원칙**
1. **우주적 일관성**: 모든 요소가 하나의 우주처럼 조화
2. **직관적 내비게이션**: 사용자가 길을 잃지 않는 명확한 구조
3. **감정적 연결**: 사용자의 감정과 공명하는 디자인
4. **접근성 우선**: 모든 사용자가 편리하게 이용 가능

## 🎨 **컬러 시스템 아키텍처**

### **📊 메인 컬러 팔레트**
```scss
// 🌌 Cosmic Color Palette v1.0
$color-palette: (
  // 🔮 Primary Colors (신비로운 보라 계열)
  primary: (
    50:  #faf5ff,   // 가장 연한 라벤더
    100: #f3e8ff,   // 연한 라벤더
    200: #e9d5ff,   // 중간 라벤더
    300: #d8b4fe,   // 연한 보라
    400: #c084fc,   // 중간 보라
    500: #a855f7,   // 메인 보라 (브랜드 컬러)
    600: #9333ea,   // 진한 보라
    700: #7c3aed,   // 더 진한 보라
    800: #6b21a8,   // 매우 진한 보라
    900: #581c87,   // 가장 진한 보라
  ),
  
  // ⭐ Secondary Colors (신비로운 골드 계열)
  secondary: (
    50:  #fefbeb,   // 아이보리 골드
    100: #fef3c7,   // 연한 골드
    200: #fde68a,   // 중간 골드
    300: #fcd34d,   // 밝은 골드
    400: #fbbf24,   // 황금색
    500: #f59e0b,   // 메인 골드
    600: #d97706,   // 진한 황금
    700: #b45309,   // 더 진한 황금
    800: #92400e,   // 구리색 골드
    900: #78350f,   // 브론즈 골드
  ),
  
  // 🌟 Accent Colors (에너지 계열)
  accent: (
    cosmic-pink: #ec4899,   // 우주적 핑크
    mystic-cyan: #06b6d4,   // 신비로운 사이안
    stellar-blue: #3b82f6,  // 별빛 파란색
    aurora-green: #10b981,  // 오로라 초록
  ),
  
  // 🔥 Element Colors (오행 기반)
  elements: (
    fire:   #ef4444,  // 화(火) - 빨강
    earth:  #f59e0b,  // 토(土) - 노랑
    metal:  #6b7280,  // 금(金) - 회색
    water:  #3b82f6,  // 수(水) - 파랑
    wood:   #10b981,  // 목(木) - 초록
  ),
  
  // 🌑 Neutral Colors (배경 및 텍스트)
  neutral: (
    50:  #fafafa,   // 순백
    100: #f5f5f5,   // 연한 회색
    200: #e5e5e5,   // 밝은 회색
    300: #d4d4d4,   // 중간 회색
    400: #a3a3a3,   // 진한 회색
    500: #737373,   // 중간 진한 회색
    600: #525252,   // 어두운 회색
    700: #404040,   // 매우 어두운 회색
    800: #262626,   // 거의 검정
    900: #171717,   // 검정
  )
);

// 🎨 테마별 컬러 맵핑
$theme-colors: (
  // ☀️ 라이트 테마
  light: (
    background: var(--color-neutral-50),
    surface: var(--color-neutral-100),
    text-primary: var(--color-neutral-900),
    text-secondary: var(--color-neutral-600),
    border: var(--color-neutral-200),
  ),
  
  // 🌙 다크 테마  
  dark: (
    background: var(--color-neutral-900),
    surface: var(--color-neutral-800),
    text-primary: var(--color-neutral-50),
    text-secondary: var(--color-neutral-300),
    border: var(--color-neutral-700),
  ),
  
  // 🔮 미스틱 테마
  mystic: (
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%),
    surface: rgba(139, 92, 246, 0.1),
    text-primary: var(--color-neutral-50),
    text-secondary: var(--color-primary-300),
    border: var(--color-primary-500),
  )
);
```

### **🎯 컬러 사용 가이드라인**
```typescript
// 🎨 컬러 사용 규칙
const ColorUsageGuide = {
  // 🔮 사주 관련 컬러
  saju: {
    primary: 'primary-500',     // 메인 사주 컬러
    background: 'primary-50',   // 사주 배경
    accent: 'secondary-400',    // 사주 강조 컬러
  },
  
  // 🃏 타로 관련 컬러
  tarot: {
    primary: 'accent-cosmic-pink',  // 타로 메인
    background: 'neutral-900',      // 어두운 배경 (신비감)
    accent: 'accent-mystic-cyan',   // 타로 강조
  },
  
  // 🐲 12지신 관련 컬러
  zodiac: {
    primary: 'secondary-500',       // 황금 컬러
    background: 'neutral-50',       // 밝은 배경
    accent: 'accent-stellar-blue',  // 별자리 컬러
  },
  
  // 💰 결제/상거래 컬러
  commerce: {
    success: 'accent-aurora-green', // 성공/확인
    warning: 'secondary-400',       // 경고
    error: 'elements-fire',         // 오류
    info: 'accent-stellar-blue',    // 정보
  }
};
```

## 📝 **타이포그래피 시스템**

### **📚 폰트 계층 구조**
```scss
// 🔤 Font Family Stack
$font-families: (
  // 🏷️ 한글 폰트
  korean: (
    primary: 'Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif',
    display: 'Gmarket Sans, Pretendard Variable, sans-serif',
    accent: 'Noto Sans KR, Pretendard Variable, sans-serif',
  ),
  
  // 🔤 영문 폰트
  english: (
    primary: 'Inter Variable, Inter, system-ui, sans-serif',
    display: 'Playfair Display, Georgia, serif',
    mono: 'Fira Code, Monaco, Cascadia Code, monospace',
  ),
  
  // ✨ 특수 폰트 (로고, 제목)
  special: (
    mystic: 'Cinzel, Playfair Display, serif',  // 신비로운 느낌
    cosmic: 'Orbitron, system-ui, sans-serif',  // 우주적 느낌
  )
);

// 📏 Font Scale (1.25 비율 기반)
$font-scale: (
  xs:   0.75rem,  // 12px - 작은 라벨
  sm:   0.875rem, // 14px - 보조 텍스트
  base: 1rem,     // 16px - 기본 텍스트
  lg:   1.125rem, // 18px - 중간 제목
  xl:   1.25rem,  // 20px - 큰 제목
  2xl:  1.5rem,   // 24px - 섹션 제목
  3xl:  1.875rem, // 30px - 페이지 제목
  4xl:  2.25rem,  // 36px - 메인 제목
  5xl:  3rem,     // 48px - 히어로 제목
  6xl:  3.75rem,  // 60px - 대형 디스플레이
);

// 📐 Line Height 
$line-heights: (
  none: 1,
  tight: 1.25,
  snug: 1.375,
  normal: 1.5,
  relaxed: 1.625,
  loose: 2,
);

// ⚖️ Font Weight
$font-weights: (
  thin: 100,
  light: 300,
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
  extrabold: 800,
  black: 900,
);
```

### **🎨 타이포그래피 컴포넌트**
```scss
// 📝 Typography Components
.typography {
  // 🏆 Display Headings (메인 제목)
  &-display {
    font-family: var(--font-display);
    font-weight: var(--font-bold);
    line-height: var(--line-height-tight);
    letter-spacing: -0.025em;
    
    &-1 { font-size: var(--font-6xl); }  // 60px
    &-2 { font-size: var(--font-5xl); }  // 48px
    &-3 { font-size: var(--font-4xl); }  // 36px
  }
  
  // 📋 Headings (일반 제목)
  &-heading {
    font-family: var(--font-primary);
    font-weight: var(--font-semibold);
    line-height: var(--line-height-snug);
    
    &-1 { font-size: var(--font-3xl); }  // 30px
    &-2 { font-size: var(--font-2xl); }  // 24px
    &-3 { font-size: var(--font-xl); }   // 20px
    &-4 { font-size: var(--font-lg); }   // 18px
  }
  
  // 📄 Body Text (본문)
  &-body {
    font-family: var(--font-primary);
    line-height: var(--line-height-relaxed);
    
    &-large {
      font-size: var(--font-lg);    // 18px
      font-weight: var(--font-normal);
    }
    
    &-base {
      font-size: var(--font-base);  // 16px
      font-weight: var(--font-normal);
    }
    
    &-small {
      font-size: var(--font-sm);    // 14px
      font-weight: var(--font-normal);
    }
  }
  
  // 🏷️ Labels & Captions
  &-label {
    font-family: var(--font-primary);
    font-weight: var(--font-medium);
    font-size: var(--font-sm);     // 14px
    line-height: var(--line-height-normal);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  &-caption {
    font-family: var(--font-primary);
    font-weight: var(--font-normal);
    font-size: var(--font-xs);     // 12px
    line-height: var(--line-height-normal);
    color: var(--color-text-secondary);
  }
}
```

## 🧩 **컴포넌트 라이브러리 아키텍처**

### **📦 컴포넌트 계층 구조**
```typescript
// 🏗️ Component Hierarchy
interface ComponentLibrary {
  // 🧱 Atoms (원자 컴포넌트)
  atoms: {
    Button: React.ComponentType<ButtonProps>;
    Input: React.ComponentType<InputProps>;
    Icon: React.ComponentType<IconProps>;
    Badge: React.ComponentType<BadgeProps>;
    Avatar: React.ComponentType<AvatarProps>;
    Spinner: React.ComponentType<SpinnerProps>;
  };
  
  // 🔗 Molecules (분자 컴포넌트)
  molecules: {
    SearchBox: React.ComponentType<SearchBoxProps>;
    FormField: React.ComponentType<FormFieldProps>;
    Card: React.ComponentType<CardProps>;
    Dropdown: React.ComponentType<DropdownProps>;
    Pagination: React.ComponentType<PaginationProps>;
    Toast: React.ComponentType<ToastProps>;
  };
  
  // 🏢 Organisms (유기체 컴포넌트)
  organisms: {
    Header: React.ComponentType<HeaderProps>;
    Sidebar: React.ComponentType<SidebarProps>;
    Footer: React.ComponentType<FooterProps>;
    Modal: React.ComponentType<ModalProps>;
    DataTable: React.ComponentType<DataTableProps>;
    Navigation: React.ComponentType<NavigationProps>;
  };
  
  // 📄 Templates (템플릿)
  templates: {
    DashboardLayout: React.ComponentType<DashboardLayoutProps>;
    ServiceLayout: React.ComponentType<ServiceLayoutProps>;
    AuthLayout: React.ComponentType<AuthLayoutProps>;
    LandingLayout: React.ComponentType<LandingLayoutProps>;
  };
}
```

### **🎨 컴포넌트 스타일 시스템**
```typescript
// 🎭 Component Style System
const ComponentStyles = {
  // 🔘 Button Variants
  button: {
    variants: {
      primary: {
        backgroundColor: 'var(--color-primary-500)',
        color: 'white',
        '&:hover': {
          backgroundColor: 'var(--color-primary-600)',
        }
      },
      secondary: {
        backgroundColor: 'var(--color-secondary-500)',
        color: 'white',
        '&:hover': {
          backgroundColor: 'var(--color-secondary-600)',
        }
      },
      outline: {
        backgroundColor: 'transparent',
        border: '2px solid var(--color-primary-500)',
        color: 'var(--color-primary-500)',
        '&:hover': {
          backgroundColor: 'var(--color-primary-500)',
          color: 'white',
        }
      },
      ghost: {
        backgroundColor: 'transparent',
        color: 'var(--color-primary-500)',
        '&:hover': {
          backgroundColor: 'var(--color-primary-50)',
        }
      }
    },
    sizes: {
      sm: {
        padding: '0.5rem 1rem',
        fontSize: 'var(--font-sm)',
        height: '2rem'
      },
      md: {
        padding: '0.75rem 1.5rem',
        fontSize: 'var(--font-base)',
        height: '2.5rem'
      },
      lg: {
        padding: '1rem 2rem',
        fontSize: 'var(--font-lg)',
        height: '3rem'
      }
    }
  },
  
  // 📦 Card Variants
  card: {
    variants: {
      default: {
        backgroundColor: 'var(--color-surface)',
        border: '1px solid var(--color-border)',
        borderRadius: '0.75rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      },
      elevated: {
        backgroundColor: 'var(--color-surface)',
        borderRadius: '0.75rem',
        boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
      },
      mystic: {
        background: 'linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-accent-cosmic-pink) 100%)',
        color: 'white',
        borderRadius: '1rem',
        boxShadow: '0 20px 40px rgba(139, 92, 246, 0.3)',
      }
    }
  }
};
```

## 🎭 **애니메이션 시스템**

### **✨ 모션 원칙**
```scss
// 🎬 Animation Principles
$motion: (
  // ⏱️ Duration
  duration: (
    fast: 150ms,
    normal: 300ms,
    slow: 500ms,
    slower: 700ms,
  ),
  
  // 📈 Easing Functions
  easing: (
    linear: cubic-bezier(0, 0, 1, 1),
    ease: cubic-bezier(0.25, 0.1, 0.25, 1),
    ease-in: cubic-bezier(0.42, 0, 1, 1),
    ease-out: cubic-bezier(0, 0, 0.58, 1),
    ease-in-out: cubic-bezier(0.42, 0, 0.58, 1),
    spring: cubic-bezier(0.68, -0.55, 0.265, 1.55),
  ),
  
  // 🌟 Special Effects
  effects: (
    glow: '0 0 20px var(--color-primary-500)',
    mystic-glow: '0 0 30px var(--color-accent-cosmic-pink)',
    cosmic-glow: '0 0 40px var(--color-accent-mystic-cyan)',
  )
);

// ✨ 애니메이션 유틸리티
@mixin animate($name, $duration: normal, $easing: ease, $delay: 0ms) {
  animation: #{$name} map-get($motion, duration, $duration) map-get($motion, easing, $easing) #{$delay};
}

@mixin transition($properties: all, $duration: normal, $easing: ease) {
  transition: #{$properties} map-get($motion, duration, $duration) map-get($motion, easing, $easing);
}
```

### **🌟 키프레임 애니메이션**
```scss
// 🎭 Keyframe Animations

// ✨ 반짝임 효과 (별, 포인트)
@keyframes twinkle {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1);
  }
  50% { 
    opacity: 0.3; 
    transform: scale(0.8);
  }
}

// 🔮 신비로운 글로우 효과
@keyframes mystic-glow {
  0%, 100% { 
    box-shadow: 0 0 20px var(--color-primary-500);
    filter: brightness(1);
  }
  50% { 
    box-shadow: 0 0 40px var(--color-accent-cosmic-pink);
    filter: brightness(1.2);
  }
}

// 🌀 회전 효과 (로딩, 로고)
@keyframes cosmic-spin {
  from { 
    transform: rotate(0deg); 
  }
  to { 
    transform: rotate(360deg); 
  }
}

// 🌊 파도 효과 (백그라운드)
@keyframes wave {
  0%, 100% { 
    transform: translateY(0px); 
  }
  50% { 
    transform: translateY(-10px); 
  }
}

// 💫 떠오르는 효과 (카드, 모달)
@keyframes float-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 🎆 폭죽 효과 (성공, 완료)
@keyframes celebration {
  0% {
    transform: scale(0) rotate(0deg);
    opacity: 1;
  }
  50% {
    transform: scale(1.2) rotate(180deg);
    opacity: 0.8;
  }
  100% {
    transform: scale(1) rotate(360deg);
    opacity: 0;
  }
}
```

### **🎮 인터랙션 애니메이션**
```typescript
// 🖱️ Interactive Animations
const InteractionAnimations = {
  // 🔘 버튼 애니메이션
  button: {
    hover: {
      scale: 1.05,
      transition: { duration: 0.2 }
    },
    tap: {
      scale: 0.95,
      transition: { duration: 0.1 }
    }
  },
  
  // 🃏 카드 애니메이션
  card: {
    hover: {
      y: -8,
      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15)',
      transition: { duration: 0.3 }
    },
    tap: {
      scale: 0.98,
      transition: { duration: 0.1 }
    }
  },
  
  // 📄 페이지 전환
  pageTransition: {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -20 },
    transition: { duration: 0.3 }
  },
  
  // 🔮 모달 애니메이션
  modal: {
    overlay: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
      exit: { opacity: 0 }
    },
    content: {
      initial: { scale: 0.9, opacity: 0 },
      animate: { scale: 1, opacity: 1 },
      exit: { scale: 0.9, opacity: 0 }
    }
  }
};
```

## 📱 **반응형 그리드 시스템**

### **📐 브레이크포인트 정의**
```scss
// 📱 Responsive Breakpoints
$breakpoints: (
  xs: 320px,   // 작은 모바일
  sm: 640px,   // 큰 모바일
  md: 768px,   // 태블릿
  lg: 1024px,  // 작은 데스크톱
  xl: 1280px,  // 큰 데스크톱
  2xl: 1536px, // 초대형 데스크톱
);

// 📊 Container Sizes
$containers: (
  xs: 100%,
  sm: 640px,
  md: 768px,
  lg: 1024px,
  xl: 1280px,
  2xl: 1536px,
);

// 🎯 Media Query Mixins
@mixin respond-above($breakpoint) {
  @media (min-width: map-get($breakpoints, $breakpoint)) {
    @content;
  }
}

@mixin respond-below($breakpoint) {
  @media (max-width: #{map-get($breakpoints, $breakpoint) - 1px}) {
    @content;
  }
}

@mixin respond-between($min, $max) {
  @media (min-width: map-get($breakpoints, $min)) and (max-width: #{map-get($breakpoints, $max) - 1px}) {
    @content;
  }
}
```

### **🏗️ 그리드 시스템**
```scss
// 🔲 Flexbox Grid System
.grid {
  display: grid;
  gap: var(--grid-gap, 1rem);
  
  // 📱 반응형 컬럼
  &-cols {
    &-1 { grid-template-columns: repeat(1, 1fr); }
    &-2 { grid-template-columns: repeat(2, 1fr); }
    &-3 { grid-template-columns: repeat(3, 1fr); }
    &-4 { grid-template-columns: repeat(4, 1fr); }
    &-5 { grid-template-columns: repeat(5, 1fr); }
    &-6 { grid-template-columns: repeat(6, 1fr); }
    &-12 { grid-template-columns: repeat(12, 1fr); }
  }
  
  // 📐 반응형 변형
  @include respond-above(sm) {
    &-sm-cols {
      &-1 { grid-template-columns: repeat(1, 1fr); }
      &-2 { grid-template-columns: repeat(2, 1fr); }
      &-3 { grid-template-columns: repeat(3, 1fr); }
      &-4 { grid-template-columns: repeat(4, 1fr); }
    }
  }
  
  @include respond-above(md) {
    &-md-cols {
      &-1 { grid-template-columns: repeat(1, 1fr); }
      &-2 { grid-template-columns: repeat(2, 1fr); }
      &-3 { grid-template-columns: repeat(3, 1fr); }
      &-4 { grid-template-columns: repeat(4, 1fr); }
      &-6 { grid-template-columns: repeat(6, 1fr); }
    }
  }
  
  @include respond-above(lg) {
    &-lg-cols {
      &-1 { grid-template-columns: repeat(1, 1fr); }
      &-2 { grid-template-columns: repeat(2, 1fr); }
      &-3 { grid-template-columns: repeat(3, 1fr); }
      &-4 { grid-template-columns: repeat(4, 1fr); }
      &-6 { grid-template-columns: repeat(6, 1fr); }
      &-12 { grid-template-columns: repeat(12, 1fr); }
    }
  }
}

// 📦 Flex Utilities
.flex {
  display: flex;
  
  &-col { flex-direction: column; }
  &-row { flex-direction: row; }
  &-wrap { flex-wrap: wrap; }
  &-nowrap { flex-wrap: nowrap; }
  
  // 🎯 Justify Content
  &-justify {
    &-start { justify-content: flex-start; }
    &-center { justify-content: center; }
    &-end { justify-content: flex-end; }
    &-between { justify-content: space-between; }
    &-around { justify-content: space-around; }
    &-evenly { justify-content: space-evenly; }
  }
  
  // 📐 Align Items
  &-items {
    &-start { align-items: flex-start; }
    &-center { align-items: center; }
    &-end { align-items: flex-end; }
    &-stretch { align-items: stretch; }
    &-baseline { align-items: baseline; }
  }
}
```

## 🔣 **아이콘 시스템**

### **📚 아이콘 라이브러리 구조**
```typescript
// 🎨 Icon System Architecture
interface IconLibrary {
  // 🔮 운세 관련 아이콘
  fortune: {
    saju: 'saju-chart',
    tarot: 'tarot-cards', 
    zodiac: 'zodiac-wheel',
    astrology: 'star-constellation',
    fengshui: 'compass-directions',
    constitution: 'body-energy'
  };
  
  // 🎯 UI 기본 아이콘
  ui: {
    // 내비게이션
    home: 'home-outline',
    menu: 'menu-hamburger',
    close: 'close-x',
    back: 'arrow-left',
    forward: 'arrow-right',
    
    // 액션
    search: 'search-magnifier',
    filter: 'filter-funnel',
    sort: 'sort-arrows',
    refresh: 'refresh-circular',
    
    // 상태
    loading: 'spinner-dots',
    success: 'check-circle',
    warning: 'warning-triangle',
    error: 'error-circle',
    info: 'info-circle'
  };
  
  // 👤 사용자 관련
  user: {
    profile: 'user-avatar',
    settings: 'settings-gear',
    logout: 'logout-door',
    heart: 'heart-filled',
    bookmark: 'bookmark-ribbon'
  };
  
  // 💰 상거래 관련  
  commerce: {
    cart: 'shopping-cart',
    payment: 'credit-card',
    coin: 'coin-stack',
    gift: 'gift-box',
    subscription: 'membership-card'
  };
}

// 🎨 아이콘 컴포넌트
interface IconProps {
  name: keyof IconLibrary[keyof IconLibrary];
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  color?: string;
  variant?: 'outline' | 'filled' | 'duotone';
  className?: string;
}

const Icon: React.FC<IconProps> = ({ 
  name, 
  size = 'md', 
  color, 
  variant = 'outline',
  className 
}) => {
  const iconSizes = {
    xs: 'w-3 h-3',      // 12px
    sm: 'w-4 h-4',      // 16px  
    md: 'w-5 h-5',      // 20px
    lg: 'w-6 h-6',      // 24px
    xl: 'w-8 h-8',      // 32px
    '2xl': 'w-12 h-12'  // 48px
  };

  return (
    <svg 
      className={`icon icon-${name} ${iconSizes[size]} ${className}`}
      style={{ color }}
      fill={variant === 'filled' ? 'currentColor' : 'none'}
      stroke={variant !== 'filled' ? 'currentColor' : 'none'}
      strokeWidth={variant === 'outline' ? 2 : 0}
    >
      <use href={`#icon-${name}`} />
    </svg>
  );
};
```

## 🌓 **테마 시스템**

### **🎭 테마 구조**
```typescript
// 🌈 Theme System Architecture
interface ThemeSystem {
  themes: {
    light: LightTheme;
    dark: DarkTheme;
    mystic: MysticTheme;
    cosmic: CosmicTheme;
  };
  
  // 🎯 컨텍스트별 테마
  contextual: {
    saju: SajuTheme;
    tarot: TarotTheme;
    zodiac: ZodiacTheme;
    community: CommunityTheme;
    commerce: CommerceTheme;
  };
}

// 🌟 테마 인터페이스
interface Theme {
  name: string;
  colors: ColorPalette;
  typography: TypographyConfig;
  spacing: SpacingConfig;
  components: ComponentThemes;
  effects: EffectConfig;
}

// 🔮 미스틱 테마 예시
const MysticTheme: Theme = {
  name: 'mystic',
  colors: {
    background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)',
    surface: 'rgba(139, 92, 246, 0.1)',
    primary: '#a855f7',
    secondary: '#ec4899',
    accent: '#06b6d4',
    text: {
      primary: '#ffffff',
      secondary: '#d8b4fe',
      muted: '#a3a3a3'
    }
  },
  effects: {
    glow: '0 0 30px var(--color-primary)',
    shadow: '0 20px 40px rgba(139, 92, 246, 0.3)',
    blur: 'backdrop-filter: blur(20px)'
  }
};
```

### **🔧 테마 전환 시스템**
```typescript
// 🎛️ Theme Management
class ThemeManager {
  private currentTheme: string = 'light';
  private themes = new Map<string, Theme>();
  
  // 🔄 테마 등록
  registerTheme(name: string, theme: Theme): void {
    this.themes.set(name, theme);
  }
  
  // 🎨 테마 적용
  applyTheme(themeName: string): void {
    const theme = this.themes.get(themeName);
    if (!theme) return;
    
    // 1️⃣ CSS 변수 업데이트
    this.updateCSSVariables(theme);
    
    // 2️⃣ 로컬 스토리지 저장
    localStorage.setItem('preferred-theme', themeName);
    
    // 3️⃣ 현재 테마 업데이트
    this.currentTheme = themeName;
    
    // 4️⃣ 테마 변경 이벤트 발생
    document.dispatchEvent(new CustomEvent('theme-changed', {
      detail: { theme: themeName }
    }));
  }
  
  // 🔧 CSS 변수 업데이트
  private updateCSSVariables(theme: Theme): void {
    const root = document.documentElement;
    
    // 컬러 변수 설정
    Object.entries(theme.colors).forEach(([key, value]) => {
      if (typeof value === 'string') {
        root.style.setProperty(`--color-${key}`, value);
      } else if (typeof value === 'object') {
        Object.entries(value).forEach(([subKey, subValue]) => {
          root.style.setProperty(`--color-${key}-${subKey}`, subValue);
        });
      }
    });
    
    // 이펙트 변수 설정
    Object.entries(theme.effects).forEach(([key, value]) => {
      root.style.setProperty(`--effect-${key}`, value);
    });
  }
  
  // 🌗 다크모드 자동 감지
  enableAutoTheme(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      const preferredTheme = e.matches ? 'dark' : 'light';
      this.applyTheme(preferredTheme);
    };
    
    mediaQuery.addEventListener('change', handleChange);
    handleChange(mediaQuery); // 초기 적용
  }
}

// 🌐 전역 테마 매니저
export const themeManager = new ThemeManager();
```

---

## 📋 **구현 체크리스트**

### **1단계: 기본 시스템 구축** ✅
- [x] 컬러 팔레트 정의
- [x] 타이포그래피 스케일 설정
- [x] 기본 컴포넌트 스타일링
- [ ] 아이콘 라이브러리 구축
- [ ] 테마 시스템 구현

### **2단계: 고급 기능** 🔄
- [ ] 애니메이션 시스템 완성
- [ ] 반응형 그리드 최적화
- [ ] 다크모드 구현
- [ ] 접근성 개선

### **3단계: 특화 테마** 📋
- [ ] 사주 테마 구현
- [ ] 타로 테마 구현
- [ ] 12지신 테마 구현
- [ ] 커뮤니티 테마 구현

---

*📅 설계 완료일: 2025-08-18*  
*🎨 설계자: HEAL7 Design System Team*  
*📝 문서 위치: `/home/ubuntu/CORE/reference-docs/technical-standards/`*  
*🔄 다음 버전: v1.1 (2025-08-25 예정)*