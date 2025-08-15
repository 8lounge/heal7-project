// API 설정 - 마이크로서비스 구조
export const API_ENDPOINTS = {
  MAIN: 'https://heal7.com',            // heal7.com - 메인 서비스
  ADMIN: 'https://admin.heal7.com',     // admin.heal7.com - 관리자
  MARKETING: 'https://marketing.heal7.com', // marketing.heal7.com - 마케팅
  TEST: 'http://localhost:8014',        // test.heal7.com - 테스트 백엔드
  BACKUP: 'https://backup.heal7.com'    // backup.heal7.com - 백업
}

// 기본 API URL (테스트 환경에서는 로컬 백엔드 사용)
export const API_BASE_URL = API_ENDPOINTS.TEST

// 관리자 API URL
export const ADMIN_API_BASE_URL = API_ENDPOINTS.ADMIN

// 기타 설정
export const APP_NAME = 'HEALINGSPACE'
export const APP_VERSION = '2.0.0'