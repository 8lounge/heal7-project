import { ThemeMode } from '../hooks/useWeatherTheme'

// 테마별 스타일 유틸리티 함수들

export const getThemeClasses = {
  // 헤더 관련 클래스
  header: (theme: ThemeMode) => 
    theme === 'dark' 
      ? 'bg-black/20 border-white/10' 
      : 'bg-pink-100/30 border-orange-200/20',
  
  // 로고 텍스트 클래스
  logoTitle: (theme: ThemeMode) =>
    theme === 'dark' ? 'theme-text-heading' : 'theme-text-heading',
  
  logoSubtitle: (theme: ThemeMode) =>
    theme === 'dark' ? 'theme-text-caption' : 'theme-text-caption',
  
  // 메뉴 버튼 클래스
  menuButton: {
    active: (theme: ThemeMode) =>
      theme === 'dark'
        ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border-2 border-white/50 ring-1 ring-purple-400/30'
        : 'bg-pink-500/20 text-pink-900 shadow-lg backdrop-blur-sm border-2 border-pink-400/60 ring-1 ring-pink-300/30',
    inactive: (theme: ThemeMode) =>
      theme === 'dark'
        ? 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/30 hover:border-white/50'
        : 'bg-orange-300/10 text-orange-800/80 hover:bg-pink-400/20 hover:text-pink-900 backdrop-blur-sm border border-orange-300/30 hover:border-pink-400/50'
  },
  
  // 테마 토글 라벨 클래스
  themeLabel: {
    light: (theme: ThemeMode) =>
      theme === 'light' ? 'text-orange-700' : 'text-gray-500',
    dark: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-white' : 'text-gray-500'
  },
  
  // 툴팁 관련 클래스
  tooltip: {
    container: (theme: ThemeMode) =>
      theme === 'dark' 
        ? 'bg-black/80 text-white' 
        : 'bg-pink-50/90 text-gray-900 border border-pink-200/40',
    title: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-300' : 'text-pink-600',
    content: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-gray-300' : 'text-gray-800',
    accent: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-purple-300' : 'text-orange-600',
    subtitle: (theme: ThemeMode) =>
      theme === 'dark' ? 'text-gray-400' : 'text-gray-600'
  },
  
  // 전체 페이지 오버레이 클래스
  pageOverlay: (theme: ThemeMode) =>
    theme === 'dark' 
      ? 'bg-gradient-to-br from-black/90 via-purple-900/85 to-purple-950/90' 
      : 'bg-gradient-to-br from-pink-50/85 via-orange-50/90 to-pink-100/80'
}

// 테마 전환 애니메이션 클래스
export const themeTransitions = {
  fast: 'transition-all duration-300 ease-in-out',
  normal: 'transition-all duration-500 ease-in-out',
  slow: 'transition-all duration-1000 ease-in-out',
  colors: 'transition-colors duration-500'
}

// 테마별 색상 팔레트
export const themeColors = {
  dark: {
    primary: 'purple-500',
    secondary: 'indigo-500',
    accent: 'purple-300',
    text: 'white',
    textSecondary: 'gray-300',
    textMuted: 'gray-400',
    background: 'black',
    surface: 'white/20',
    border: 'white/10'
  },
  light: {
    primary: 'pink-500',
    secondary: 'orange-500',
    accent: 'pink-600',
    text: 'gray-900',
    textSecondary: 'gray-700',
    textMuted: 'gray-600',
    background: 'pink-50',
    surface: 'pink-300/20',
    border: 'orange-200/20'
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
      : 'bg-pink-500/20 border border-pink-400/30 hover:bg-pink-500/30',
      
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