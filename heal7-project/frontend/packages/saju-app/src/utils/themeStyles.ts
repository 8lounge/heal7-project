import { ThemeMode } from '../hooks/useWeatherTheme'

// 테마별 스타일 유틸리티 함수들

export const getThemeClasses = {
  // 헤더 관련 클래스
  header: (theme: ThemeMode) => 
    theme === 'dark' 
      ? 'bg-purple-900/20 border-purple-500/20' 
      : 'bg-purple-50/30 border-purple-200/20',
  
  // 로고 텍스트 클래스
  logoTitle: (theme: ThemeMode) =>
    theme === 'dark' ? 'theme-text-heading' : 'theme-text-heading',
  
  logoSubtitle: (theme: ThemeMode) =>
    theme === 'dark' ? 'theme-text-caption' : 'theme-text-caption',
  
  // 메뉴 버튼 클래스 - Mystic Design System 적용 (블러효과 제거)
  menuButton: {
    active: (theme: ThemeMode) =>
      theme === 'dark'
        ? 'bg-purple-500/30 text-white shadow-lg border-2 border-purple-400/60 ring-1 ring-purple-300/40'
        : 'bg-purple-500/20 text-purple-900 shadow-lg border-2 border-purple-400/60 ring-1 ring-purple-300/30',
    inactive: (theme: ThemeMode) =>
      theme === 'dark'
        ? 'bg-purple-500/10 text-purple-100/80 hover:bg-purple-500/20 hover:text-white border border-purple-400/30 hover:border-purple-300/50'
        : 'bg-purple-300/10 text-purple-700/80 hover:bg-purple-400/20 hover:text-purple-900 border border-purple-300/30 hover:border-purple-400/50'
  },
  
  // 테마 토글 라벨 클래스 - 보라색 컨셉 통일
  themeLabel: {
    light: (theme: ThemeMode) =>
      theme === 'light' ? 'text-purple-700' : 'text-purple-400',
    dark: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-100' : 'text-purple-400'
  },
  
  // 툴팁 관련 클래스 - Mystic Design System
  tooltip: {
    container: (theme: ThemeMode) =>
      theme === 'dark' 
        ? 'bg-purple-900/80 text-white border border-purple-500/30' 
        : 'bg-purple-50/90 text-purple-900 border border-purple-200/40',
    title: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-200' : 'text-purple-700',
    content: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-100' : 'text-purple-800',
    accent: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-300' : 'text-purple-600',
    subtitle: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-300' : 'text-purple-600'
  },
  
  // 전체 페이지 오버레이 클래스 - 이미지 컨셉 기반
  pageOverlay: (theme: ThemeMode) =>
    theme === 'dark' 
      ? 'bg-gradient-to-br from-purple-950/90 via-purple-900/85 to-indigo-950/90' 
      : 'bg-gradient-to-br from-purple-50/85 via-indigo-50/90 to-purple-100/80'
}

// 테마 전환 애니메이션 클래스
export const themeTransitions = {
  fast: 'transition-all duration-300 ease-in-out',
  normal: 'transition-all duration-500 ease-in-out',
  slow: 'transition-all duration-1000 ease-in-out',
  colors: 'transition-colors duration-500'
}

// 테마별 색상 팔레트 - Mystic Design System v2.0
export const themeColors = {
  dark: {
    primary: 'purple-500',    // Mystic 보라색
    secondary: 'indigo-500',  // Cosmic 인디고
    accent: 'purple-300',     // 부드러운 보라색
    text: 'white',
    textSecondary: 'slate-200',
    textMuted: 'purple-200',
    background: 'purple-900', // 블랙 대신 보라색 기조
    surface: 'purple-500/20',
    border: 'purple-400/30'
  },
  light: {
    primary: 'purple-500',    // 통일된 Mystic 보라색
    secondary: 'indigo-500',  // 통일된 Cosmic 인디고
    accent: 'purple-300',     // 부드러운 보라색 액센트
    text: 'indigo-900',       // 진한 인디고 텍스트
    textSecondary: 'purple-700',
    textMuted: 'purple-500',
    background: 'purple-50',  // 연한 보라색 배경
    surface: 'purple-100/20',
    border: 'purple-200/30'
  }
}

// 테마별 텍스트 색상 유틸리티 - 새 CSS 클래스 활용
export const getThemeTextClasses = {
  // 기본 텍스트 색상 (제목, 메인 텍스트) - WCAG AA 준수
  primary: (theme: ThemeMode) => 'theme-text-primary',
    
  // 보조 텍스트 색상 (부제목, 설명) - 고대비율
  secondary: (theme: ThemeMode) => 'theme-text-secondary',
    
  // 흐린 텍스트 색상 (메타데이터, 라벨) - 접근성 준수
  muted: (theme: ThemeMode) => 'theme-text-muted',
    
  // 미묘한 텍스트 색상 (구분선, 힌트)
  subtle: (theme: ThemeMode) => 'theme-text-caption',
    
  // 헤딩 텍스트 (제목, 중요한 텍스트)
  heading: (theme: ThemeMode) => 'theme-text-heading',
  
  // 본문 텍스트 (일반 텍스트, 설명)
  body: (theme: ThemeMode) => 'theme-text-body',
  
  // 아이콘 색상
  icon: (theme: ThemeMode) => 'theme-text-muted',
    
  // 플레이스홀더 색상 - Tailwind 클래스 유지 (CSS 변수 지원 한계)
  placeholder: (theme: ThemeMode) =>
    theme === 'dark' ? 'placeholder-white/60' : 'placeholder-gray-500',
    
  // 링크/버튼 텍스트 색상 - 인터랙티브 요소
  interactive: (theme: ThemeMode) => 'theme-text-interactive',
    
  // 해시태그 키워드 텍스트 색상
  hashtag: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-white/90' : 'text-gray-800',
    
  // 해시태그 키워드 배경 및 테두리
  hashtagContainer: (theme: ThemeMode) =>
    theme === 'dark' 
      ? 'bg-purple-500/20 border border-purple-400/30 hover:bg-purple-500/30' 
      : 'bg-purple-500/20 border border-purple-400/30 hover:bg-purple-500/30',
      
  // 조합 해석 텍스트 (특별한 정보)
  combination: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-amber-200' : 'text-amber-700',
    
  // 조합 해석 보조 텍스트  
  combinationSecondary: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-amber-200/80' : 'text-amber-600',
    
  // 행운의 숫자 텍스트
  luckyNumber: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-yellow-200' : 'text-yellow-800',
    
  // CSS 변수를 사용한 동적 색상 (테마 전환 시 자동 변경)
  dynamicPrimary: () => 'text-[var(--theme-text-primary)]',
  dynamicSecondary: () => 'text-[var(--theme-text-secondary)]'
}

// 헬퍼 함수: 조건부 클래스 결합
export const combineClasses = (...classes: (string | undefined | false)[]): string => {
  return classes.filter(Boolean).join(' ')
}

// 헬퍼 함수: 테마별 완전한 메뉴 버튼 클래스
export const getMenuButtonClass = (theme: ThemeMode, isActive: boolean, baseclasses = 'px-4 py-2 rounded-lg font-medium'): string => {
  return combineClasses(
    baseclasses,
    themeTransitions.normal,
    isActive 
      ? getThemeClasses.menuButton.active(theme)
      : getThemeClasses.menuButton.inactive(theme)
  )
}