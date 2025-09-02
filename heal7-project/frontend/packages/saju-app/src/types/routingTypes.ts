/**
 * 🚀 라우팅 시스템 타입 정의
 * 기존 CurrentPage 타입을 확장하여 Router 호환성 제공
 */

// 기존 CurrentPage 타입 (하위 호환성 보장)
export type CurrentPage = 
  | 'dashboard' 
  | 'saju' 
  | 'tarot' 
  | 'magazine' 
  | 'consultation' 
  | 'store' 
  | 'notices' 
  | 'profile'
  | 'fortune' 
  | 'zodiac' 
  | 'personality' 
  | 'love' 
  | 'compatibility' 
  | 'admin' 
  | 'dream' 
  | 'calendar' 
  | 'subscription'

// 새로운 Route 정보 인터페이스
export interface RouteInfo {
  /** 기존 페이지 ID (하위 호환성) */
  pageId: CurrentPage
  /** URL 경로 */
  path: string
  /** 페이지 제목 (SEO용) */
  title: string
  /** 페이지 설명 (SEO용) */
  description: string
  /** 이모지 아이콘 */
  icon: string
  /** 네비게이션에 표시할 라벨 */
  label: string
  /** 상위 카테고리 (중첩 라우팅용) */
  category?: string
  /** 메타 키워드 (SEO용) */
  keywords?: string[]
  /** Open Graph 이미지 URL */
  ogImage?: string
}

// URL 패턴과 페이지 ID 매핑 타입
export type RouteMapping = {
  [K in CurrentPage]: RouteInfo
}

// 라우터 전환 모드
export type RoutingMode = 'state_based' | 'router_hybrid' | 'router_only'

// 네비게이션 Props (기존 호환성 + 라우터 기능)
export interface NavigationProps {
  /** 현재 페이지 (기존 state 기반) */
  currentPage: CurrentPage
  /** 페이지 변경 핸들러 (기존 방식 - 하위 호환성) */
  onPageChange: (page: CurrentPage) => void
  /** 테마 모드 */
  viewMode: 'basic' | 'cyber_fantasy'
  /** 라우팅 모드 (점진적 전환용) */
  routingMode?: RoutingMode
}

// 헤더 Props (기존 호환성 유지)
export interface HeaderProps {
  viewMode: 'basic' | 'cyber_fantasy'
  onViewModeChange: (mode: 'basic' | 'cyber_fantasy') => void
  apiStatus: string
  currentPage?: CurrentPage
  onPageChange?: (page: CurrentPage) => void
  routingMode?: RoutingMode
}

// 라우트별 메타데이터 생성 함수 타입
export type MetaDataGenerator = (routeInfo: RouteInfo) => {
  title: string
  description: string
  keywords: string
  ogTitle: string
  ogDescription: string
  ogImage: string
}

// 페이지 컴포넌트 Props (공통)
export interface PageComponentProps {
  viewMode: 'basic' | 'cyber_fantasy'
  routeInfo?: RouteInfo
}

// 하이브리드 모드용 페이지 래퍼 Props
export interface PageWrapperProps {
  children: React.ReactNode
  routeInfo: RouteInfo
  viewMode: 'basic' | 'cyber_fantasy'
  /** 기존 애니메이션 키 (Framer Motion 호환) */
  animationKey?: string
}