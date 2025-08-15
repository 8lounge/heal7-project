/**
 * HEAL7 사주명리학 시스템 - 핵심 타입 정의
 * 
 * 이 파일은 사주명리학의 모든 핵심 타입을 정의합니다.
 * Python 백엔드와 호환성을 유지하면서 TypeScript의 강력한 타입 시스템을 활용합니다.
 */

// ============================================================================
// 기본 타입 정의
// ============================================================================

/** 천간 (Heavenly Stems) */
export type CheonGan = '甲' | '乙' | '丙' | '丁' | '戊' | '己' | '庚' | '辛' | '壬' | '癸'

/** 지지 (Earthly Branches) */
export type JiJi = '子' | '丑' | '寅' | '卯' | '辰' | '巳' | '午' | '未' | '申' | '酉' | '戌' | '亥'

/** 오행 (Five Elements) */
export type WuXing = 'wood' | 'fire' | 'earth' | 'metal' | 'water'

/** 음양 */
export type YinYang = 'yin' | 'yang'

/** 십신 (Ten Gods) */
export type SipSin = 
  | 'bi_gyeon'      // 비견
  | 'geop_jae'      // 겁재
  | 'sik_sin'       // 식신
  | 'sang_gwan'     // 상관
  | 'pyeon_jae'     // 편재
  | 'jeong_jae'     // 정재
  | 'pyeon_gwan'    // 편관
  | 'jeong_gwan'    // 정관
  | 'pyeon_in'      // 편인
  | 'jeong_in'      // 정인

/** 성별 */
export type Gender = 'male' | 'female'

// ============================================================================
// 갑자 60 관련 타입
// ============================================================================

/** 갑자 정보 */
export interface GapJa {
  readonly index: number           // 0-59
  readonly gapja: string          // "갑자", "을축" 등
  readonly cheongan: CheonGan     // 천간
  readonly jiji: JiJi             // 지지
  readonly cheongan_index: number // 천간 인덱스 (0-9)
  readonly jiji_index: number     // 지지 인덱스 (0-11)
}

/** 사주 사주 (년, 월, 일, 시) */
export interface SajuPillar {
  readonly cheongan: CheonGan
  readonly jiji: JiJi
  readonly gapja_index: number
  readonly wuxing: WuXing
  readonly yin_yang: YinYang
}

/** 완전한 사주 정보 */
export interface SajuInfo {
  readonly year: SajuPillar
  readonly month: SajuPillar
  readonly day: SajuPillar
  readonly hour: SajuPillar
  readonly day_master: CheonGan    // 일간 (본인의 핵심)
}

// ============================================================================
// 입력 및 계산 관련 타입
// ============================================================================

/** 생년월일시 입력 정보 */
export interface BirthInfo {
  readonly year: number
  readonly month: number
  readonly day: number
  readonly hour: number
  readonly minute: number
  readonly gender: Gender
  readonly is_lunar: boolean
  readonly is_leap_month: boolean
  readonly timezone: string
  readonly location?: {
    readonly latitude: number
    readonly longitude: number
    readonly name: string
  }
}

/** 시간 보정 정보 */
export interface TimeCorrection {
  readonly true_solar_time_minutes: number    // 진태양시 보정 (분)
  readonly timezone_offset_minutes: number    // 시간대 보정 (분)
  readonly daylight_saving: boolean           // 서머타임 적용 여부
}

/** 계산 옵션 */
export interface CalculationOptions {
  readonly use_kasi_api: boolean               // KASI API 사용 여부
  readonly apply_true_solar_time: boolean      // 진태양시 보정 적용
  readonly calculation_method: 'kasi' | 'mathematical' | 'hybrid'
  readonly precision_level: 'high' | 'medium' | 'low'
}

// ============================================================================
// 분석 결과 타입
// ============================================================================

/** 오행 분석 결과 */
export interface WuXingAnalysis {
  readonly elements: Record<WuXing, {
    readonly count: number
    readonly strength: number      // 0-100
    readonly sources: string[]     // 어디서 나왔는지
  }>
  readonly balance_score: number   // 0-100 (균형도)
  readonly dominant_element: WuXing
  readonly weakest_element: WuXing
  readonly recommendations: string[]
}

/** 십신 분석 결과 */
export interface SipSinAnalysis {
  readonly day_master: CheonGan
  readonly relations: Record<SipSin, {
    readonly count: number
    readonly positions: ('year' | 'month' | 'day' | 'hour')[]
    readonly strength: number
  }>
  readonly personality_traits: string[]
  readonly career_suggestions: string[]
  readonly relationship_patterns: string[]
}

/** 지장간 분석 */
export interface JiJangGan {
  readonly main: CheonGan         // 주기
  readonly middle?: CheonGan      // 중기
  readonly residual?: CheonGan    // 여기
  readonly percentages: number[]  // 각 기의 비율
}

/** 대운 정보 */
export interface DaeUn {
  readonly cycle_number: number   // 몇 번째 대운 (1-8)
  readonly start_age: number
  readonly end_age: number
  readonly cheongan: CheonGan
  readonly jiji: JiJi
  readonly wuxing: WuXing
  readonly fortune_level: 'excellent' | 'good' | 'normal' | 'challenging' | 'difficult'
  readonly key_themes: string[]
  readonly detailed_analysis: {
    readonly general: string
    readonly career: string
    readonly relationship: string
    readonly health: string
    readonly wealth: string
  }
}

/** 세운 (연운) 정보 */
export interface SaeUn {
  readonly year: number
  readonly age: number
  readonly cheongan: CheonGan
  readonly jiji: JiJi
  readonly scores: {
    readonly overall: number      // 0-100
    readonly career: number
    readonly relationship: number
    readonly health: number
    readonly wealth: number
  }
  readonly major_events: string[]
  readonly monthly_fortunes: Record<number, number> // 1-12월 운세 점수
}

// ============================================================================
// 궁합 관련 타입
// ============================================================================

/** 궁합 타입 */
export type CompatibilityType = 'romantic' | 'friendship' | 'business' | 'family'

/** 궁합 분석 결과 */
export interface CompatibilityResult {
  readonly type: CompatibilityType
  readonly overall_score: number          // 0-100
  readonly detailed_scores: {
    readonly day_master: number          // 일간 궁합
    readonly year_branch: number         // 연지 궁합
    readonly wuxing_balance: number      // 오행 밸런스
    readonly sipsin_harmony: number      // 십신 조화
  }
  readonly strengths: string[]
  readonly weaknesses: string[]
  readonly recommendations: string[]
  readonly compatibility_analysis: string
}

// ============================================================================
// KASI API 관련 타입
// ============================================================================

/** KASI API 응답 타입 */
export interface KasiResponse {
  readonly isSuccessful: boolean
  readonly resultCode: string
  readonly resultMsg: string
  readonly data?: {
    readonly solYear: number
    readonly solMonth: number
    readonly solDay: number
    readonly lunYear: number
    readonly lunMonth: number
    readonly lunDay: number
    readonly lunLeapmonth: number
    readonly dayGan: string
    readonly dayJi: string
    readonly timeGan: string
    readonly timeJi: string
  }
}

/** 24절기 정보 */
export interface SolarTerm {
  readonly name: string
  readonly order: number          // 1-24
  readonly type: '절' | '기'
  readonly datetime: Date
  readonly lunar_date?: Date
}

// ============================================================================
// 에러 및 검증 타입
// ============================================================================

/** 계산 오류 타입 */
export type SajuErrorType = 
  | 'invalid_date'
  | 'kasi_api_error'
  | 'calculation_error'
  | 'network_error'
  | 'validation_error'

/** 사주 계산 오류 */
export interface SajuError {
  readonly type: SajuErrorType
  readonly message: string
  readonly details?: Record<string, unknown>
  readonly timestamp: Date
}

/** 계산 결과 (성공/실패 포함) */
export type SajuResult<T> = 
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: SajuError }

// ============================================================================
// 캐시 및 성능 관련 타입
// ============================================================================

/** 캐시 키 */
export interface CacheKey {
  readonly type: 'saju' | 'analysis' | 'compatibility' | 'kasi'
  readonly hash: string
  readonly ttl?: number          // TTL in seconds
}

/** 계산 성능 메트릭 */
export interface PerformanceMetrics {
  readonly calculation_time_ms: number
  readonly api_call_time_ms?: number
  readonly cache_hit: boolean
  readonly complexity_score: number     // 계산 복잡도 (1-10)
}

// ============================================================================
// UI 상태 관련 타입
// ============================================================================

/** 계산 진행 상태 */
export type CalculationStatus = 
  | 'idle'
  | 'validating'
  | 'calculating'
  | 'analyzing'
  | 'completed'
  | 'error'

/** 계산 단계 */
export interface CalculationStep {
  readonly id: string
  readonly name: string
  readonly description: string
  readonly status: 'pending' | 'in_progress' | 'completed' | 'error'
  readonly progress: number     // 0-100
}

/** 사주 계산 상태 */
export interface SajuCalculationState {
  readonly status: CalculationStatus
  readonly steps: CalculationStep[]
  readonly current_step?: string
  readonly progress: number
  readonly result?: SajuInfo
  readonly error?: SajuError
  readonly metrics?: PerformanceMetrics
}

// ============================================================================
// 데이터베이스 관련 타입 (API 연동용)
// ============================================================================

/** 사용자 사주 프로필 */
export interface SajuProfile {
  readonly id: string
  readonly user_id: string
  readonly name: string
  readonly birth_info: BirthInfo
  readonly saju_info: SajuInfo
  readonly analyses: {
    readonly wuxing: WuXingAnalysis
    readonly sipsin: SipSinAnalysis
  }
  readonly is_favorite: boolean
  readonly created_at: Date
  readonly updated_at: Date
}

/** API 응답 래퍼 */
export interface ApiResponse<T> {
  readonly success: boolean
  readonly data?: T
  readonly error?: {
    readonly code: string
    readonly message: string
  }
  readonly timestamp: Date
}

// ============================================================================
// 유틸리티 타입
// ============================================================================

/** 깊은 읽기 전용 타입 */
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P]
}

/** 부분적 업데이트 타입 */
export type PartialUpdate<T> = {
  readonly [P in keyof T]?: T[P] extends object ? PartialUpdate<T[P]> : T[P]
}

/** 타입 가드 헬퍼 */
export const isCheonGan = (value: string): value is CheonGan => {
  return ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'].includes(value)
}

export const isJiJi = (value: string): value is JiJi => {
  return ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'].includes(value)
}

export const isWuXing = (value: string): value is WuXing => {
  return ['wood', 'fire', 'earth', 'metal', 'water'].includes(value)
}