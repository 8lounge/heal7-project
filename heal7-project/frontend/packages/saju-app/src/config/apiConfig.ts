/**
 * API 설정 중앙 관리
 * 하드코딩된 API 엔드포인트를 환경변수 기반으로 변경
 */

// 환경변수에서 API 베이스 URL 가져오기
const getApiBaseUrl = (): string => {
  // 개발/프로덕션 환경 구분
  const isDevelopment = process.env.NODE_ENV === 'development'

  // 환경변수 우선, 없으면 기본값
  const baseUrl = process.env.REACT_APP_API_BASE_URL ||
                 (isDevelopment ? 'http://localhost:8002' : 'https://api.heal7.com')

  return baseUrl
}

// API 설정
export const API_CONFIG = {
  BASE_URL: getApiBaseUrl(),
  TIMEOUT: 10000, // 10초

  // API 엔드포인트들
  ENDPOINTS: {
    // 관리자 인증
    ADMIN: {
      LOGIN: '/api/admin/login',
      LOGOUT: '/api/admin/logout',
      SETTINGS: '/api/admin/settings',
    },

    // 분석 및 통계
    ANALYTICS: {
      DASHBOARD: '/api/admin/analytics/dashboard',
      AI_STATS: '/api/admin/ai/stats',
      USER_STATS: '/api/admin/users/stats',
      SYSTEM_HEALTH: '/api/admin/system/health'
    },

    // 1:1 문의 관리
    INQUIRIES: {
      OVERVIEW: '/api/admin/saju/inquiries/overview',
      LIST: '/api/admin/saju/inquiries',
      REPLY: (id: number) => `/api/admin/saju/inquiries/${id}/reply`,
      DETAIL: (id: number) => `/api/admin/saju/inquiries/${id}`,
      STATUS: (id: number) => `/api/admin/saju/inquiries/${id}/status`
    },

    // 포인트 시스템
    POINTS: {
      BALANCE: '/api/points/balance',
      CHARGE: '/api/points/charge',
      HISTORY: '/api/points/history'
    },

    // 사주 시스템
    SAJU: {
      CALCULATE: '/api/saju/calculate',
      HISTORY: '/api/saju/history'
    }
  },

  // HTTP 헤더 설정
  HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },

  // 인증 헤더 생성
  getAuthHeaders: (token?: string): Record<string, string> => {
    const headers = { ...API_CONFIG.HEADERS }

    // localStorage에서 토큰 가져오기
    const authToken = token || localStorage.getItem('admin_token')

    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`
    }

    return headers
  }
}

// 환경별 설정
export const ENV_CONFIG = {
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',

  // 디버그 모드
  DEBUG_API: process.env.REACT_APP_DEBUG_API === 'true',

  // 재시도 설정
  RETRY_ATTEMPTS: parseInt(process.env.REACT_APP_RETRY_ATTEMPTS || '3'),
  RETRY_DELAY: parseInt(process.env.REACT_APP_RETRY_DELAY || '1000'),

  // 캐시 설정
  CACHE_TTL: parseInt(process.env.REACT_APP_CACHE_TTL || '300'), // 5분

  // 로그 레벨
  LOG_LEVEL: process.env.REACT_APP_LOG_LEVEL || 'info'
}

// 디버그 로깅
if (ENV_CONFIG.DEBUG_API) {
  console.log('🔧 API Configuration:', {
    baseUrl: API_CONFIG.BASE_URL,
    environment: process.env.NODE_ENV,
    debugMode: ENV_CONFIG.DEBUG_API
  })
}