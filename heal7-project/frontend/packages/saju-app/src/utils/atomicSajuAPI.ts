/**
 * Atomic Saju API 클라이언트
 * ========================
 * 백엔드 atomic 모듈과 통신하는 API 클라이언트
 * 프론트엔드의 계산 로직을 완전히 대체
 */

const ATOMIC_API_BASE = '/api/atomic/saju';

// === API Response Types ===

interface GapjaResponse {
  success: boolean;
  date: string;
  gapja: string;
  cheongan: string;
  jiji: string;
  index: number;
  source: string;
}

interface PillarInfo {
  gapja: string;
  cheongan: string;
  jiji: string;
  element: string;
  yin_yang: string;
}

interface PillarsResponse {
  success: boolean;
  birth_datetime: string;
  year_pillar: PillarInfo;
  month_pillar: PillarInfo;
  day_pillar: PillarInfo;
  time_pillar: PillarInfo;
  source: string;
}

interface SajuCalculateResponse {
  success: boolean;
  birth_datetime: string;
  calculation_method: string;
  pillars: {
    year: PillarInfo;
    month: PillarInfo;
    day: PillarInfo;
    time: PillarInfo;
  };
  summary: {
    saju_string: string;
    ilgan: string;
    ilji: string;
    primary_element: string;
  };
}

interface LunarConvertResponse {
  success: boolean;
  solar_date?: {
    year: number;
    month: number;
    day: number;
    date_string: string;
  };
  lunar_date?: {
    year: number;
    month: number;
    day: number;
    is_leap_month: boolean;
    date_string: string;
  };
  source: string;
  error_message?: string;
}

interface ConstantsResponse {
  gapja_60: string[];
  cheongan: string[];
  jiji: string[];
  reference_date: string;
  reference_gapja: string;
}

// === API 클라이언트 클래스 ===

class AtomicSajuAPI {
  private baseURL: string;

  constructor(baseURL: string = ATOMIC_API_BASE) {
    this.baseURL = baseURL;
  }

  /**
   * 60갑자 계산
   */
  async getGapja(year: number, month: number, day: number): Promise<GapjaResponse> {
    const response = await fetch(
      `${this.baseURL}/gapja?year=${year}&month=${month}&day=${day}`
    );
    
    if (!response.ok) {
      throw new Error(`갑자 계산 실패: ${response.status}`);
    }
    
    return response.json();
  }

  /**
   * 사주 기둥 계산 (년주/월주/일주/시주)
   */
  async getPillars(
    year: number, 
    month: number, 
    day: number, 
    hour: number = 12, 
    minute: number = 0,
    useTrueSolarTime: boolean = false
  ): Promise<PillarsResponse> {
    const params = new URLSearchParams({
      year: year.toString(),
      month: month.toString(),
      day: day.toString(),
      hour: hour.toString(),
      minute: minute.toString(),
      use_true_solar_time: useTrueSolarTime.toString()
    });

    const response = await fetch(`${this.baseURL}/pillars?${params}`);
    
    if (!response.ok) {
      throw new Error(`기둥 계산 실패: ${response.status}`);
    }
    
    return response.json();
  }

  /**
   * 완전한 사주 계산
   */
  async calculateCompleteSaju(
    year: number,
    month: number,
    day: number,
    hour: number = 12,
    minute: number = 0,
    useTrueSolarTime: boolean = false,
    longitude: number = 126.978
  ): Promise<SajuCalculateResponse> {
    const requestBody = {
      year,
      month,
      day,
      hour,
      minute,
      use_true_solar_time: useTrueSolarTime,
      longitude
    };

    const response = await fetch(`${this.baseURL}/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      throw new Error(`사주 계산 실패: ${response.status}`);
    }
    
    return response.json();
  }

  /**
   * 음력 변환 (양력 ↔ 음력)
   */
  async convertLunar(
    year: number,
    month: number,
    day: number,
    direction: 'solar_to_lunar' | 'lunar_to_solar' = 'solar_to_lunar',
    isLeap: boolean = false
  ): Promise<LunarConvertResponse> {
    const params = new URLSearchParams({
      year: year.toString(),
      month: month.toString(),
      day: day.toString(),
      direction,
      is_leap: isLeap.toString()
    });

    const response = await fetch(`${this.baseURL}/lunar-convert?${params}`);
    
    if (!response.ok) {
      throw new Error(`음력 변환 실패: ${response.status}`);
    }
    
    return response.json();
  }

  /**
   * 사주 상수 조회
   */
  async getConstants(): Promise<ConstantsResponse> {
    const response = await fetch(`${this.baseURL}/constants`);
    
    if (!response.ok) {
      throw new Error(`상수 조회 실패: ${response.status}`);
    }
    
    return response.json();
  }

  /**
   * 헬스 체크
   */
  async healthCheck(): Promise<any> {
    const response = await fetch(`${this.baseURL}/health`);
    
    if (!response.ok) {
      throw new Error(`헬스 체크 실패: ${response.status}`);
    }
    
    return response.json();
  }
}

// === 전역 API 인스턴스 ===
export const atomicSajuAPI = new AtomicSajuAPI();

// === 편의 함수들 (기존 코드와의 호환성) ===

/**
 * 60갑자 계산 (기존 get60갑자 함수 대체)
 */
export async function get60갑자Atomic(date: Date): Promise<string> {
  try {
    const response = await atomicSajuAPI.getGapja(
      date.getFullYear(),
      date.getMonth() + 1,
      date.getDate()
    );
    
    if (response.success) {
      return response.gapja;
    } else {
      console.error('갑자 계산 실패:', response);
      return '❌오류';
    }
  } catch (error) {
    console.error('갑자 API 호출 실패:', error);
    return '❌오류';
  }
}

/**
 * 년주 계산 (기존 get년주 함수 대체)
 */
export async function get년주Atomic(date: Date): Promise<string> {
  try {
    const response = await atomicSajuAPI.getPillars(
      date.getFullYear(),
      date.getMonth() + 1,
      date.getDate()
    );
    
    if (response.success) {
      return response.year_pillar.gapja;
    } else {
      console.error('년주 계산 실패:', response);
      return '❌오류';
    }
  } catch (error) {
    console.error('년주 API 호출 실패:', error);
    return '❌오류';
  }
}

/**
 * 배치 갑자 계산 (월 전체)
 */
export async function getBatchGapja(year: number, month: number): Promise<Map<number, string>> {
  const daysInMonth = new Date(year, month, 0).getDate();
  const results = new Map<number, string>();
  
  // 병렬 요청으로 성능 최적화
  const promises = [];
  for (let day = 1; day <= daysInMonth; day++) {
    promises.push(
      atomicSajuAPI.getGapja(year, month, day)
        .then(response => ({ day, gapja: response.success ? response.gapja : '❌오류' }))
        .catch(() => ({ day, gapja: '❌오류' }))
    );
  }
  
  const batchResults = await Promise.all(promises);
  batchResults.forEach(({ day, gapja }) => {
    results.set(day, gapja);
  });
  
  return results;
}

/**
 * 사주 상수 캐시
 */
let constantsCache: ConstantsResponse | null = null;

export async function getSajuConstants(): Promise<ConstantsResponse> {
  if (!constantsCache) {
    constantsCache = await atomicSajuAPI.getConstants();
  }
  return constantsCache;
}

/**
 * 캐시 클리어
 */
export function clearConstantsCache(): void {
  constantsCache = null;
}

// === 에러 핸들링 유틸리티 ===

export function isAtomicAPIError(error: any): boolean {
  return error instanceof Error && error.message.includes('API');
}

export function getErrorMessage(error: any): string {
  if (isAtomicAPIError(error)) {
    return `API 오류: ${error.message}`;
  }
  return `계산 오류: ${error.message || '알 수 없는 오류'}`;
}

// === 개발용 테스트 함수 ===

export async function testAtomicAPI(): Promise<void> {
  console.log('🧪 Atomic API 테스트 시작');
  
  try {
    // 헬스 체크
    const health = await atomicSajuAPI.healthCheck();
    console.log('✅ 헬스 체크:', health);
    
    // 갑자 계산 테스트
    const gapja = await atomicSajuAPI.getGapja(2025, 9, 9);
    console.log('✅ 갑자 계산:', gapja);
    
    // 기둥 계산 테스트
    const pillars = await atomicSajuAPI.getPillars(2025, 9, 9, 12, 0);
    console.log('✅ 기둥 계산:', pillars);
    
    // 상수 조회 테스트
    const constants = await getSajuConstants();
    console.log('✅ 상수 조회:', constants);
    
    console.log('🎉 모든 테스트 통과!');
  } catch (error) {
    console.error('❌ 테스트 실패:', getErrorMessage(error));
  }
}

export default atomicSajuAPI;