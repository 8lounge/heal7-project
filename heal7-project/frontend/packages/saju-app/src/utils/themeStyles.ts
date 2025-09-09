import { ThemeMode } from '../hooks/useWeatherTheme'

// 테마별 스타일 유틸리티 함수들

export const getThemeClasses = {
  // 헤더 관련 클래스 - ForeTeller inspired with glassmorphism
  header: (theme: ThemeMode) => 
    theme === 'dark' 
      ? 'bg-purple-900/10 backdrop-blur-md border-pink-500/20' 
      : 'bg-white/80 backdrop-blur-xl border-pink-200/30 shadow-lg',
  
  // 로고 텍스트 클래스
  logoTitle: (theme: ThemeMode) =>
    theme === 'dark' ? 'theme-text-heading' : 'theme-text-heading',
  
  logoSubtitle: (theme: ThemeMode) =>
    theme === 'dark' ? 'theme-text-caption' : 'theme-text-caption',
  
  // 메뉴 버튼 클래스 - ForeTeller inspired glassmorphism (Pink theme only)
  menuButton: {
    active: (theme: ThemeMode) =>
      theme === 'dark'
        ? 'bg-pink-500/30 backdrop-blur-md text-white shadow-lg border-2 border-pink-400/60 ring-1 ring-pink-300/40'
        : 'bg-pink-500/15 backdrop-blur-md text-black shadow-lg border border-pink-400/40 ring-1 ring-pink-300/20',
    inactive: (theme: ThemeMode) =>
      theme === 'dark'
        ? 'bg-pink-500/10 backdrop-blur-sm text-white/80 hover:bg-pink-500/20 hover:text-white border border-pink-400/30 hover:border-pink-300/50'
        : 'bg-white/60 backdrop-blur-sm text-black hover:bg-pink-100/50 hover:text-black border border-pink-200/30 hover:border-pink-300/50'
  },
  
  // 테마 토글 라벨 클래스 - ForeTeller inspired
  themeLabel: {
    light: (theme: ThemeMode) =>
      theme === 'light' ? 'text-pink-700' : 'text-pink-400',
    dark: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-white' : 'text-pink-600'
  },
  
  // 툴팁 관련 클래스 - ForeTeller inspired glassmorphism
  tooltip: {
    container: (theme: ThemeMode) =>
      theme === 'dark' 
        ? 'bg-purple-900/80 backdrop-blur-lg text-white border border-pink-500/30' 
        : 'bg-white/85 backdrop-blur-xl text-black border border-pink-200/40 shadow-lg',
    title: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-white' : 'text-black',
    content: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-white' : 'text-black',
    accent: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-pink-300' : 'text-pink-600',
    subtitle: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-pink-300' : 'text-pink-600'
  },
  
  // 전체 페이지 오버레이 클래스 - ForeTeller inspired clean design
  pageOverlay: (theme: ThemeMode) =>
    theme === 'dark' 
      ? 'bg-gradient-to-br from-purple-950/90 via-purple-900/85 to-indigo-950/90 backdrop-blur-sm' 
      : 'bg-gradient-to-br from-white/80 via-white/70 to-white/60 backdrop-blur-sm'
}

// 테마 전환 애니메이션 클래스
export const themeTransitions = {
  fast: 'transition-all duration-300 ease-in-out',
  normal: 'transition-all duration-500 ease-in-out',
  slow: 'transition-all duration-1000 ease-in-out',
  colors: 'transition-colors duration-500'
}

// ForeTeller-inspired color palette - Dark Pink + Black & Dark Purple
export const themeColors = {
  dark: {
    primary: 'pink-500',      // Dark Pink for interactive elements
    secondary: 'purple-500',  // Dark Purple background support
    accent: 'pink-300',       // Pink accents
    text: 'white',            // All text unified to WHITE
    textSecondary: 'white',   // All text unified to WHITE
    textMuted: 'white/80',    // Slightly transparent white
    background: 'purple-900', // Dark purple background
    surface: 'white/10',      // Glassmorphism surface
    border: 'pink-400/30'     // Pink borders
  },
  light: {
    primary: 'pink-500',      // Dark Pink for interactive elements
    secondary: 'pink-600',    // Darker pink support
    accent: 'pink-400',       // Pink accents
    text: 'black',            // All text unified to BLACK
    textSecondary: 'black',   // All text unified to BLACK
    textMuted: 'black/80',    // Slightly transparent black
    background: 'white',      // Clean white background
    surface: 'white/80',      // Glassmorphism surface
    border: 'pink-200/30'     // Pink borders
  }
}

// ForeTeller-inspired text color system - BLACK for day, WHITE for night
export const getThemeTextClasses = {
  // 기본 텍스트 색상 - All text unified
  primary: (theme: ThemeMode) => theme === 'dark' ? 'text-white' : 'text-black',
    
  // 보조 텍스트 색상 - All text unified
  secondary: (theme: ThemeMode) => theme === 'dark' ? 'text-white' : 'text-black',
    
  // 흐린 텍스트 색상 - Slightly transparent
  muted: (theme: ThemeMode) => theme === 'dark' ? 'text-white/80' : 'text-black/80',
    
  // 미묘한 텍스트 색상
  subtle: (theme: ThemeMode) => theme === 'dark' ? 'text-white/60' : 'text-black/60',
    
  // 헤딩 텍스트 - All text unified
  heading: (theme: ThemeMode) => theme === 'dark' ? 'text-white' : 'text-black',
  
  // 본문 텍스트 - All text unified
  body: (theme: ThemeMode) => theme === 'dark' ? 'text-white' : 'text-black',
  
  // 아이콘 색상
  icon: (theme: ThemeMode) => theme === 'dark' ? 'text-white/80' : 'text-black/80',
    
  // 플레이스홀더 색상 - ForeTeller inspired
  placeholder: (theme: ThemeMode) =>
    theme === 'dark' ? 'placeholder-white/60' : 'placeholder-black/60',
    
  // 링크/버튼 텍스트 색상 - Pink for interactive elements
  interactive: (theme: ThemeMode) => theme === 'dark' ? 'text-pink-300' : 'text-pink-600',
    
  // 해시태그 키워드 텍스트 색상 - All text unified
  hashtag: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-white' : 'text-black',
    
  // 해시태그 키워드 배경 및 테두리 - Pink theme
  hashtagContainer: (theme: ThemeMode) =>
    theme === 'dark' 
      ? 'bg-pink-500/20 backdrop-blur-sm border border-pink-400/30 hover:bg-pink-500/30' 
      : 'bg-pink-100/70 backdrop-blur-sm border border-pink-300/40 hover:bg-pink-200/60',
      
  // 조합 해석 텍스트 - All text unified
  combination: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-white' : 'text-black',
    
  // 조합 해석 보조 텍스트 - All text unified
  combinationSecondary: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-white/80' : 'text-black/80',
    
  // 행운의 숫자 텍스트 - All text unified
  luckyNumber: (theme: ThemeMode) =>
    theme === 'dark' ? 'text-white' : 'text-black',
    
  // CSS 변수를 사용한 동적 색상 - ForeTeller inspired
  dynamicPrimary: (theme: ThemeMode) => theme === 'dark' ? 'text-white' : 'text-black',
  dynamicSecondary: (theme: ThemeMode) => theme === 'dark' ? 'text-white/80' : 'text-black/80'
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