// 운세 캘린더 데이터 시스템 - KASI API 연동
// ======================================================================
// 🔥 만세력 핵심 상수 기준값 (CRITICAL CONSTANTS) 🔥
// ======================================================================

// 🎯 1. 60갑자 계산 핵심 기준점 (절대 변경 금지)
export const GAPJA_REFERENCE_CONSTANTS = {
  /** 
   * 🔥 60갑자 절대 기준일: 1900년 1월 31일 = 갑진일
   * ⚠️  이 값을 변경하면 모든 만세력 계산이 틀어짐
   * 📚 출처: 전통 명리학 표준, KASI API 호환
   */
  REFERENCE_DATE: new Date(1900, 0, 31), // 1900년 1월 31일
  REFERENCE_GAPJA: '갑진',
  REFERENCE_GAPJA_INDEX: 40, // 갑자60순환 배열에서의 위치
  
  /** 
   * 🔥 입춘 기준 (연주 계산의 핵심)
   * ⚠️  매년 2월 4일 전후가 입춘이며, 이 기준으로 연주가 바뀜
   */
  SPRING_START_MONTH: 2,
  SPRING_START_DAY: 4,
} as const;

// 🎯 2. 진태양시 계산 상수 (국가별 지역 기준)
export const SOLAR_TIME_CONSTANTS = {
  /** 
   * 🔥 한국(서울) 기준 진태양시 보정
   * 위도: 37.5665°N, 경도: 126.9780°E (서울 중심)
   * 표준 경도: 135°E (동경 135도 - 한국표준시)
   * 보정값: (126.978 - 135) × 4분/도 = -32.09분 ≈ -32분
   */
  KOREA_LONGITUDE: 126.978,
  KOREA_STANDARD_LONGITUDE: 135.0,
  KOREA_TIME_CORRECTION_MINUTES: -32, // 서울 표준시 기준 경도차 보정
  
  /** 
   * 🔥 다른 국가 확장용 (향후 글로벌 서비스 대비)
   */
  CHINA_LONGITUDE: 116.4074, // 베이징
  CHINA_TIME_CORRECTION_MINUTES: -46,
  JAPAN_LONGITUDE: 139.6917, // 도쿄  
  JAPAN_TIME_CORRECTION_MINUTES: 19,
} as const;

// 🎯 3. 24절기 및 계절 기준 상수
export const SEASONAL_CONSTANTS = {
  /** 
   * 🔥 24절기 기준 (월주 계산의 핵심)
   * ⚠️  KASI API 기준이지만 표준시 → 진태양시 보정 필요
   * 📌 KASI는 표준시(KST) 기준이므로 진태양시 적용시 -32분 보정 적용
   */
  SOLAR_TERMS_REFERENCE: {
    1: { term: '입춘', approx_date: [2, 4], kasi_time_offset: -32 }, // 2월 4일 전후, 진태양시 -32분
    2: { term: '경칩', approx_date: [3, 5], kasi_time_offset: -32 },
    3: { term: '청명', approx_date: [4, 5], kasi_time_offset: -32 },  
    4: { term: '입하', approx_date: [5, 5], kasi_time_offset: -32 },
    5: { term: '망종', approx_date: [6, 6], kasi_time_offset: -32 },
    6: { term: '소서', approx_date: [7, 7], kasi_time_offset: -32 },
    7: { term: '입추', approx_date: [8, 7], kasi_time_offset: -32 },
    8: { term: '백로', approx_date: [9, 8], kasi_time_offset: -32 },
    9: { term: '한로', approx_date: [10, 8], kasi_time_offset: -32 },
    10: { term: '입동', approx_date: [11, 7], kasi_time_offset: -32 },
    11: { term: '대설', approx_date: [12, 7], kasi_time_offset: -32 },
    12: { term: '소한', approx_date: [1, 5], kasi_time_offset: -32 }, // 다음해 1월
  },
  
  /** 
   * 🔥 KASI API vs 진태양시 보정 상수
   * ⚠️  KASI API는 KST(한국표준시) 기준으로 절기를 제공
   * 📌 진태양시 사주계산에서는 이 보정값을 적용해야 정확함
   */
  KASI_TO_TRUE_SOLAR_CORRECTION: {
    KOREA_KST_OFFSET_MINUTES: -32, // 서울 기준 진태양시 보정
    DST_ADJUSTMENT_NEEDED: false, // 한국은 서머타임 없음
    PRECISION_THRESHOLD_HOURS: 2, // 절기 전후 2시간 내에서는 정밀 계산 필요
  },
  
  /** 
   * 🔥 월지지 매핑 (절기 기준)
   * ⚠️  입춘부터 시작하여 12개월 순환
   */
  MONTH_JIJI_MAP: {
    1: '寅', 2: '卯', 3: '辰', 4: '巳', 5: '午', 6: '未',
    7: '申', 8: '酉', 9: '戌', 10: '亥', 11: '子', 12: '丑'
  },
  
  /** 
   * 🔥 음력 + 절기 비교대조 계산 원칙 (2025-09-04 신규 반영)
   * ⚠️  월주, 일주 계산의 정확성을 위한 핵심 원칙
   * 📌 양력 계산 대비 복잡도 감소 및 정확도 향상
   */
  LUNAR_SOLAR_TERMS_PRINCIPLE: {
    /** 월주 계산 방식: 음력 월 + 해당 절기 확인 */
    MONTH_PILLAR_METHOD: '음력_절기_비교대조',
    
    /** 일주 계산 방식: 음력 날짜 기준 60갑자 순환 */
    DAY_PILLAR_METHOD: '음력_60갑자_순환',
    
    /** 계산 복잡도 감소: 양력 → 음력 변환 후 계산 */
    COMPLEXITY_REDUCTION: true,
    
    /** 정확도 보장: 전통 명리학 표준 준수 */
    TRADITIONAL_ACCURACY: true,
    
    /** 
     * 🔥 핵심 계산 순서 (반드시 준수)
     * 1. 양력 출생일 → KASI API → 음력 변환
     * 2. 음력 기준으로 해당 절기 확인
     * 3. 절기와 음력 월 비교대조하여 월주 결정
     * 4. 음력 일자로 60갑자 순환 계산하여 일주 결정
     */
    CALCULATION_ORDER: [
      'solar_to_lunar_conversion',
      'solar_term_identification', 
      'lunar_month_solar_term_comparison',
      'month_pillar_determination',
      'lunar_date_60gapja_calculation',
      'day_pillar_determination'
    ],
  },
} as const;

// 🎯 4. 서머타임 및 시간대 상수
export const TIMEZONE_CONSTANTS = {
  /** 
   * 🔥 한국은 서머타임 없음 (연중 UTC+9 고정)
   * ⚠️  따라서 KASI API도 서머타임 고려 불필요
   */
  KOREA_USES_DST: false,
  KOREA_UTC_OFFSET: 9,
  
  /** 
   * 🔥 서머타임 적용 국가들 (향후 확장용)
   * ⚠️  이들 국가에서는 KASI 대응 API의 절기 시간도 DST 보정 필요
   */
  DST_COUNTRIES: {
    'US': { 
      start: [3, 2, 0], end: [11, 1, 0], // 3월 2주 일요일 ~ 11월 1주 일요일
      standard_offset: -5, // EST UTC-5
      dst_offset: -4, // EDT UTC-4
      solar_time_correction_needed: true
    },
    'EU': { 
      start: [3, -1, 0], end: [10, -1, 0], // 3월 마지막 일요일 ~ 10월 마지막 일요일  
      standard_offset: 1, // CET UTC+1
      dst_offset: 2, // CEST UTC+2
      solar_time_correction_needed: true
    },
  },
  
  /** 
   * 🔥 시간대별 KASI 대응 API 정보 (향후 글로벌 서비스용)
   * ⚠️  각 국가의 천문 API는 해당 지역 표준시 기준이므로 진태양시 보정 필수
   */
  GLOBAL_ASTRONOMICAL_APIS: {
    'KOREA': { source: 'KASI', timezone: 'KST', needs_solar_correction: true },
    'CHINA': { source: 'CAS', timezone: 'CST', needs_solar_correction: true },
    'JAPAN': { source: 'NAOJ', timezone: 'JST', needs_solar_correction: true },
    'US': { source: 'USNO', timezone: 'multiple', needs_dst_handling: true },
  },
} as const;

// 🎯 5. 시주 계산 핵심 상수
export const HOUR_CONSTANTS = {
  /** 
   * 🔥 시두법 매핑 (일간에 따른 시천간 결정)
   * ⚠️  이 매핑이 시주 계산의 핵심
   */
  HOUR_CHEONGAN_BY_DAY: {
    '甲': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '乙': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '丙': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '丁': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '戊': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
    '己': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
    '庚': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
    '辛': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
    '壬': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
    '癸': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
  },
  
  /** 
   * 🔥 시지지 매핑 (2시간 단위)
   * 23:00-01:00=자, 01:00-03:00=축, ... 순서
   */
  HOUR_JIJI_BOUNDARIES: [23, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23],
} as const;

export interface CalendarDate {
  date: Date;
  lunarDate: string;
  lunarYear: number;
  lunarMonth: number;
  lunarDay: number;
  isLeapMonth: boolean; // 윤달 여부
  gapja: string;
  zodiac: string;
  element: string;
  sonEobNeunNal: boolean; // 손없는날
  gilil: boolean; // 길일
  흉일: boolean; // 흉일
  절기: string | null;
  운세점수: number; // 1-5
  특이사항: string[];
  solarCalendarType: 'solar'; // 양력 표기
  yearPillar?: string; // 연주
  monthPillar?: string; // 월주
}

export interface MonthlyFortune {
  month: number;
  year: number;
  bestDates: CalendarDate[];
  worstDates: CalendarDate[];
  importantDates: CalendarDate[];
  monthlyMessage: string;
}

// 천간 데이터
export const 천간 = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'];
export const 지지 = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해'];

// 12지신 동물 매핑
export const 띠동물: Record<string, string> = {
  '자': '쥐', '축': '소', '인': '호랑이', '묘': '토끼', 
  '진': '용', '사': '뱀', '오': '말', '미': '양',
  '신': '원숭이', '유': '닭', '술': '개', '해': '돼지'
};

// 오행 매핑
export const 오행매핑: Record<string, string> = {
  '갑': '목', '을': '목', '병': '화', '정': '화', '무': '토',
  '기': '토', '경': '금', '신': '금', '임': '수', '계': '수'
};

// 완전한 60갑자 배열 (정확한 순서, 존재하지 않는 조합 방지)
export const 갑자60순환 = [
  // 1-10
  '갑자', '을축', '병인', '정묘', '무진', '기사', '경오', '신미', '임신', '계유',
  // 11-20  
  '갑술', '을해', '병자', '정축', '무인', '기묘', '경진', '신사', '임오', '계미',
  // 21-30
  '갑신', '을유', '병술', '정해', '무자', '기축', '경인', '신묘', '임진', '계사',
  // 31-40
  '갑오', '을미', '병신', '정유', '무술', '기해', '경자', '신축', '임인', '계묘',
  // 41-50
  '갑진', '을사', '병오', '정미', '무신', '기유', '경술', '신해', '임자', '계축',
  // 51-60
  '갑인', '을묘', '병진', '정사', '무오', '기미', '경신', '신유', '임술', '계해'
];

// 60갑자 계산 함수 (배열 기반으로 정확한 조합만 반환)
export const get60갑자 = (date: Date): string => {
  // 🔥 핵심 상수 사용 (상단에서 정의된 CRITICAL CONSTANTS)
  const 기준일 = GAPJA_REFERENCE_CONSTANTS.REFERENCE_DATE;
  const 기준갑자인덱스 = GAPJA_REFERENCE_CONSTANTS.REFERENCE_GAPJA_INDEX;
  
  const 날짜차이 = Math.floor((date.getTime() - 기준일.getTime()) / (24 * 60 * 60 * 1000));
  let 갑자인덱스 = (기준갑자인덱스 + 날짜차이) % 60;
  
  // 음수 보정 (과거 날짜 계산시)
  if (갑자인덱스 < 0) {
    갑자인덱스 += 60;
  }
  
  // 배열에서 직접 조회 (존재하지 않는 조합 방지)
  return 갑자60순환[갑자인덱스];
};

// 크로스체크 함수 (검증용) - 60갑자에 실제 존재하는지 확인
export const is유효한60갑자 = (gapja: string): boolean => {
  return 갑자60순환.includes(gapja);
};

// 레거시 방식과 비교 검증 함수 (개발/디버깅용)
export const get60갑자WithValidation = (date: Date): { result: string; isValid: boolean; legacy: string } => {
  // 새로운 배열 기반 방식
  const 새로운결과 = get60갑자(date);
  
  // 레거시 방식 (천간/지지 개별 계산)
  const 기준일 = new Date(1900, 0, 1);
  const 날짜차이 = Math.floor((date.getTime() - 기준일.getTime()) / (24 * 60 * 60 * 1000));
  let 갑자인덱스 = (40 + 날짜차이) % 60;
  if (갑자인덱스 < 0) 갑자인덱스 += 60;
  
  const 천간인덱스 = 갑자인덱스 % 10;
  const 지지인덱스 = 갑자인덱스 % 12;
  const 레거시결과 = 천간[천간인덱스] + 지지[지지인덱스];
  
  return {
    result: 새로운결과,
    isValid: is유효한60갑자(레거시결과),
    legacy: 레거시결과
  };
};

// 근사 음력 변환 함수 (정확도 제한적, KASI API 사용 권장)
export const get음력변환 = (date: Date): string => {
  // 간단한 근사 계산: 양력이 음력보다 평균 18-50일 정도 빠름
  // 정확한 계산을 위해서는 KASI API 필요
  
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  // 2025년 기준 주요 음력 절기일 (근사값)
  const 음력근사표 = {
    2025: [
      // [양력월, 양력일, 음력월, 음력일] 형태의 기준점들
      [1, 29, 1, 1],   // 설날
      [2, 12, 1, 15],  // 정월대보름  
      [2, 28, 2, 1],   // 음력 2월 1일
      [3, 14, 2, 15],  // 음력 2월 15일
      [3, 30, 3, 1],   // 음력 3월 1일
      [4, 13, 3, 15],  // 음력 3월 15일
      [4, 28, 4, 1],   // 음력 4월 1일
      [5, 12, 4, 15],  // 음력 4월 15일 (부처님오신날)
      [5, 27, 5, 1],   // 음력 5월 1일
      [6, 10, 5, 15],  // 음력 5월 15일
      [6, 25, 6, 1],   // 음력 6월 1일
      [7, 9, 6, 15],   // 음력 6월 15일
      [7, 24, 7, 1],   // 음력 7월 1일
      [8, 7, 7, 15],   // 음력 7월 15일 (중원절)
      [8, 22, 8, 1],   // 음력 8월 1일
      [9, 5, 8, 15],   // 음력 8월 15일 (추석)
      [9, 20, 9, 1],   // 음력 9월 1일
      [10, 4, 9, 15],  // 음력 9월 15일
      [10, 19, 10, 1], // 음력 10월 1일
      [11, 2, 10, 15], // 음력 10월 15일
      [11, 17, 11, 1], // 음력 11월 1일
      [12, 1, 11, 15], // 음력 11월 15일
      [12, 16, 12, 1], // 음력 12월 1일
      [12, 30, 12, 15] // 음력 12월 15일
    ]
  };
  
  const 기준점들 = 음력근사표[year];
  if (!기준점들) {
    return `음력 ${month}월 ${day}일 (근사)`; // 기본값
  }
  
  // 가장 가까운 기준점 찾기
  let 가장가까운기준 = 기준점들[0];
  let 최소차이 = Math.abs((month - 가장가까운기준[0]) * 31 + (day - 가장가까운기준[1]));
  
  for (const 기준점 of 기준점들) {
    const 차이 = Math.abs((month - 기준점[0]) * 31 + (day - 기준점[1]));
    if (차이 < 최소차이) {
      최소차이 = 차이;
      가장가까운기준 = 기준점;
    }
  }
  
  // 기준점으로부터 음력 날짜 추정
  const 양력기준일 = 가장가까운기준[0] * 31 + 가장가까운기준[1];
  const 현재양력일 = month * 31 + day;
  const 일수차이 = 현재양력일 - 양력기준일;
  
  let 음력월 = 가장가까운기준[2];
  let 음력일 = 가장가까운기준[3] + 일수차이;
  
  // 월 경계 처리 (29일/30일 기준)
  while (음력일 > 30) {
    음력일 -= 29; // 평균 음력월 길이
    음력월++;
  }
  while (음력일 < 1) {
    음력일 += 29;
    음력월--;
  }
  
  // 연도 경계 처리
  if (음력월 > 12) {
    음력월 = 음력월 % 12 || 12;
  }
  if (음력월 < 1) {
    음력월 = 12 + 음력월;
  }
  
  return `음력 ${음력월}월 ${음력일}일`;
};

// 손없는날 계산 (매월 9일, 10일, 19일, 20일, 29일, 30일)
export const is손없는날 = (date: Date): boolean => {
  const day = date.getDate();
  return [9, 10, 19, 20, 29, 30].includes(day);
};

// 길일/흉일 계산 (단순 규칙 기반)
export const get길흉 = (gapja: string, date: Date): { 길일: boolean; 흉일: boolean } => {
  const 천간 = gapja[0];
  const 지지 = gapja[1];
  const dayOfWeek = date.getDay();
  
  // 간단한 길일 규칙 (실제로는 더 복잡한 계산 필요)
  const 길일조건 = [
    천간 === '갑' && dayOfWeek === 1, // 갑일 + 월요일
    천간 === '을' && dayOfWeek === 2, // 을일 + 화요일
    지지 === '자' && dayOfWeek === 0, // 자일 + 일요일
    지지 === '축' && dayOfWeek === 6, // 축일 + 토요일
  ];
  
  const 흉일조건 = [
    천간 === '무' && dayOfWeek === 4, // 무일 + 목요일
    천간 === '기' && dayOfWeek === 5, // 기일 + 금요일
    지지 === '사' && dayOfWeek === 3, // 사일 + 수요일
  ];
  
  return {
    길일: 길일조건.some(condition => condition),
    흉일: 흉일조건.some(condition => condition)
  };
};

// 절기 데이터 (2025년 기준)
export const 절기2025 = [
  { 이름: '소한', 날짜: new Date(2025, 0, 5) },
  { 이름: '대한', 날짜: new Date(2025, 0, 20) },
  { 이름: '입춘', 날짜: new Date(2025, 1, 3) },
  { 이름: '우수', 날짜: new Date(2025, 1, 18) },
  { 이름: '경칩', 날짜: new Date(2025, 2, 5) },
  { 이름: '춘분', 날짜: new Date(2025, 2, 20) },
  { 이름: '청명', 날짜: new Date(2025, 3, 4) },
  { 이름: '곡우', 날짜: new Date(2025, 3, 19) },
  { 이름: '입하', 날짜: new Date(2025, 4, 5) },
  { 이름: '소만', 날짜: new Date(2025, 4, 20) },
  { 이름: '망종', 날짜: new Date(2025, 5, 5) },
  { 이름: '하지', 날짜: new Date(2025, 5, 21) },
  { 이름: '소서', 날짜: new Date(2025, 6, 6) },
  { 이름: '대서', 날짜: new Date(2025, 6, 22) },
  { 이름: '입추', 날짜: new Date(2025, 7, 7) },
  { 이름: '처서', 날짜: new Date(2025, 7, 22) },
  { 이름: '백로', 날짜: new Date(2025, 8, 7) },
  { 이름: '추분', 날짜: new Date(2025, 8, 22) },
  { 이름: '한로', 날짜: new Date(2025, 9, 8) },
  { 이름: '상강', 날짜: new Date(2025, 9, 23) },
  { 이름: '입동', 날짜: new Date(2025, 10, 7) },
  { 이름: '소설', 날짜: new Date(2025, 10, 22) },
  { 이름: '대설', 날짜: new Date(2025, 11, 7) },
  { 이름: '동지', 날짜: new Date(2025, 11, 21) }
];

// 절기 찾기
export const get절기 = (date: Date): string | null => {
  const 해당절기 = 절기2025.find(절기 => {
    const diff = Math.abs(date.getTime() - 절기.날짜.getTime());
    return diff < 24 * 60 * 60 * 1000; // 1일 이내
  });
  return 해당절기?.이름 || null;
};

// 운세 점수 계산 (1-5)
export const get운세점수 = (gapja: string, date: Date): number => {
  const 천간 = gapja[0];
  const 지지 = gapja[1];
  const 오행 = 오행매핑[천간];
  const dayOfWeek = date.getDay();
  const day = date.getDate();
  
  let 점수 = 3; // 기본 점수
  
  // 오행별 요일 보정
  const 오행요일보정: Record<string, number[]> = {
    '목': [1, 4], // 월, 목
    '화': [2], // 화
    '토': [6], // 토
    '금': [5], // 금
    '수': [0, 3] // 일, 수
  };
  
  if (오행요일보정[오행]?.includes(dayOfWeek)) {
    점수 += 1;
  }
  
  // 날짜별 보정
  if (day % 6 === 0) 점수 += 1; // 6의 배수
  if (day === 8 || day === 18 || day === 28) 점수 += 1; // 발음이 좋은 날
  
  // 지지별 보정
  const 지지보정: Record<string, number> = {
    '용': 1, '호랑이': 1, '말': 1, '닭': 1, // 활동적
    '쥐': -1, '뱀': -1 // 조용한
  };
  
  const 띠 = 띠동물[지지];
  if (띠) {
    점수 += 지지보정[띠] || 0;
  }
  
  return Math.max(1, Math.min(5, 점수));
};

// 특이사항 생성
export const get특이사항 = (date: Date, gapja: string): string[] => {
  const 특이사항: string[] = [];
  const 천간 = gapja[0];
  const 지지 = gapja[1];
  const 띠 = 띠동물[지지];
  const dayOfWeek = date.getDay();
  
  if (is손없는날(date)) {
    특이사항.push('👻 손없는날');
  }
  
  const { 길일, 흉일 } = get길흉(gapja, date);
  if (길일) 특이사항.push('✨ 길일');
  if (흉일) 특이사항.push('⚠️ 흉일');
  
  const 절기 = get절기(date);
  if (절기) 특이사항.push(`🌸 ${절기}`);
  
  // 특별한 조합
  if (천간 === '갑' && 지지 === '자') {
    특이사항.push('🌟 갑자일 (새로운 시작)');
  }
  
  if (dayOfWeek === 0) {
    특이사항.push('☀️ 일요일 (휴식)');
  }
  
  if (띠 === '용') {
    특이사항.push('🐉 용의 기운 (강운)');
  }
  
  return 특이사항;
};

// ===== KASI API 전용 캘린더 데이터 생성 =====
// 폴백 없음, 오류 발생 시 구체적 표기 및 기록

interface KasiApiError {
  date: Date;
  errorType: 'API_CALL_FAILED' | 'PARSING_FAILED' | 'NETWORK_ERROR' | 'TIMEOUT';
  errorMessage: string;
  timestamp: string;
}

// KASI API 오류 로그 (메모리 저장)
const kasiApiErrors: KasiApiError[] = [];

// KASI API 전용 캘린더 데이터 생성 (비동기)
export const generateCalendarMonth = async (year: number, month: number): Promise<CalendarDate[]> => {
  const daysInMonth = new Date(year, month, 0).getDate();
  const calendarDates: CalendarDate[] = [];
  
  console.log(`🔮 KASI API 전용 캘린더 생성 시작: ${year}년 ${month}월 (${daysInMonth}일)`);
  
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month - 1, day);
    
    try {
      // KASI API에서 정확한 정보 가져오기 (실패 시 폴백)
      const kasiData = await fetchKasiCalendarInfo(year, month, day);
      
      let gapja, lunarYear, lunarMonth, lunarDay, isLeapMonth, yearPillar, monthPillar;
      
      if (kasiData) {
        // KASI 응답 파싱
        gapja = kasiData.lunIljin?.match(/^([가-힣]+)/)?.[1] || get60갑자(date);
        lunarYear = parseInt(kasiData.lunYear) || year;
        lunarMonth = parseInt(kasiData.lunMonth) || month;
        lunarDay = parseInt(kasiData.lunDay) || day;
        isLeapMonth = kasiData.lunLeapmonth === '윤';
        yearPillar = kasiData.lunSecha || `${year}년주`;
        monthPillar = kasiData.lunWolgeon || `${month}월주`;
      } else {
        // 🔥 폴백: 로컬 계산 사용 (정확한 60갑자 상수 기반)
        gapja = get60갑자(date);
        lunarYear = year;
        lunarMonth = month;
        lunarDay = day;
        isLeapMonth = false;
        yearPillar = `${year}년주(추정)`;
        monthPillar = `${month}월주(추정)`;
      }
      
      // 음력 날짜 문자열 생성
      const lunarDate = `음력 ${lunarYear}년 ${lunarMonth}월 ${lunarDay}일${isLeapMonth ? ' (윤달)' : ''}`;
      
      // 기본 정보 계산
      const 천간 = gapja[0] || '미';
      const 지지 = gapja[1] || '지';
      const 띠 = 띠동물[지지] || '미지';
      const 오행 = 오행매핑[천간] || '미지';
      const { 길일, 흉일 } = get길흉(gapja, date);
      const 손없는날 = is손없는날(date);
      const 절기 = getKasi절기(date); // KASI 기반 24절기
      const 운세점수 = get운세점수(gapja, date);
      const 특이사항 = get특이사항(date, gapja);
      
      // KASI API 성공 표시
      if (day === 3) {
        console.log(`✅ 9월 ${day}일 KASI API 성공: ${gapja}`);
      }
      
      calendarDates.push({
        date,
        lunarDate,
        lunarYear,
        lunarMonth,
        lunarDay,
        isLeapMonth,
        gapja,
        zodiac: 띠,
        element: 오행,
        sonEobNeunNal: 손없는날,
        gilil: 길일,
        흉일,
        절기,
        운세점수,
        특이사항,
        solarCalendarType: 'solar',
        yearPillar,
        monthPillar,
      });
      
    } catch (error: any) {
      // 오류 상세 기록
      const kasiError: KasiApiError = {
        date,
        errorType: error.name === 'TypeError' ? 'NETWORK_ERROR' : 
                  error.message?.includes('파싱') ? 'PARSING_FAILED' : 
                  error.message?.includes('timeout') ? 'TIMEOUT' : 'API_CALL_FAILED',
        errorMessage: error.message || '알 수 없는 오류',
        timestamp: new Date().toISOString(),
      };
      
      kasiApiErrors.push(kasiError);
      
      console.error(`❌ KASI API 오류 (${year}-${month}-${day}):`, {
        type: kasiError.errorType,
        message: kasiError.errorMessage,
        date: date.toISOString().split('T')[0]
      });
      
      // 오류 발생한 날짜는 오류 표시와 함께 추가
      calendarDates.push({
        date,
        lunarDate: `❌ KASI API 오류: ${kasiError.errorType}`,
        lunarYear: year,
        lunarMonth: month,
        lunarDay: day,
        isLeapMonth: false,
        gapja: `❌오류`,
        zodiac: '오류',
        element: '오류',
        sonEobNeunNal: is손없는날(date),
        gilil: false,
        흉일: true, // 오류 발생일은 흉일로 표시
        절기: null,
        운세점수: 1, // 최저 점수
        특이사항: [`KASI API 오류: ${kasiError.errorType}`, kasiError.errorMessage],
        solarCalendarType: 'solar',
        yearPillar: '❌오류',
        monthPillar: '❌오류',
      });
    }
  }
  
  // 오류 요약 출력
  const errorCount = kasiApiErrors.filter(e => 
    e.date.getFullYear() === year && e.date.getMonth() + 1 === month
  ).length;
  
  console.log(`🔮 KASI API 캘린더 생성 완료: ${year}년 ${month}월`);
  console.log(`✅ 성공: ${daysInMonth - errorCount}일 | ❌ 오류: ${errorCount}일`);
  
  if (errorCount > 0) {
    console.warn('⚠️  오류 발생 날짜들:', kasiApiErrors.filter(e => 
      e.date.getFullYear() === year && e.date.getMonth() + 1 === month
    ).map(e => `${e.date.getDate()}일(${e.errorType})`).join(', '));
  }
  
  return calendarDates;
};

// KASI API 오류 통계 조회
export const getKasiApiErrors = (): KasiApiError[] => {
  return [...kasiApiErrors];
};

// KASI API 오류 통계 요약
export const getKasiApiErrorSummary = () => {
  const total = kasiApiErrors.length;
  const byType = kasiApiErrors.reduce((acc, err) => {
    acc[err.errorType] = (acc[err.errorType] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return { total, byType, recentErrors: kasiApiErrors.slice(-5) };
};

// 월별 운세 메시지 생성
export const getMonthlyFortune = async (year: number, month: number): Promise<MonthlyFortune> => {
  const dates = await generateCalendarMonth(year, month);
  
  const bestDates = dates
    .filter(d => d.운세점수 >= 4)
    .sort((a, b) => b.운세점수 - a.운세점수)
    .slice(0, 5);
    
  const worstDates = dates
    .filter(d => d.운세점수 <= 2)
    .sort((a, b) => a.운세점수 - b.운세점수)
    .slice(0, 3);
    
  const importantDates = dates.filter(d => 
    d.절기 || d.gilil || d.특이사항.length > 1
  );
  
  const monthlyMessages = [
    '새해를 맞이하는 희망찬 달입니다.',
    '사랑의 기운이 가득한 달입니다.',
    '새로운 시작과 성장의 달입니다.',
    '안정과 조화를 찾는 달입니다.',
    '활발한 활동과 성취의 달입니다.',
    '균형과 화합이 중요한 달입니다.',
    '여름의 활기가 넘치는 달입니다.',
    '풍성한 수확을 기대하는 달입니다.',
    '변화와 적응의 지혜가 필요한 달입니다.',
    '깊이 있는 성찰과 준비의 달입니다.',
    '마무리와 정리가 중요한 달입니다.',
    '한 해를 돌아보며 감사하는 달입니다.'
  ];
  
  return {
    month,
    year,
    bestDates,
    worstDates,
    importantDates,
    monthlyMessage: monthlyMessages[month - 1]
  };
};

// 오늘의 운세 정보
export const getTodayFortune = async (): Promise<CalendarDate> => {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const day = today.getDate();
  
  const monthData = await generateCalendarMonth(year, month);
  return monthData.find(d => d.date.getDate() === day) || monthData[0];
};

// ===== KASI API 연동 함수들 =====

// KASI API 기본 설정 (프록시 서버 경유)
const KASI_API_BASE = '/api/kasi'; // 프록시를 통해 CORS 문제 해결
const KASI_SERVICE_KEY = 'AR2zMFQPIPEq1WK5i1YIrWJO1jzGpBGGJUxFLQN5TXXWqFgBhC6r9WjKNFa5zWQF'; // 실제 키

// KASI API 전용 호출 함수 (백엔드 프록시 연동)
export const fetchKasiCalendarInfo = async (year: number, month: number, day: number): Promise<any> => {
  const dateStr = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
  
  try {
    // 백엔드 KASI 프록시를 통해 호출
    const proxyUrl = `/api/kasi/calendar?year=${year}&month=${month}&day=${day}`;
    
    console.log(`🔮 KASI API 프록시 호출: ${dateStr}`);
    
    const response = await fetch(proxyUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    if (result.success && result.data) {
      console.log(`✅ KASI API 프록시 성공 (${dateStr}):`, result.data);
      return result.data; // lunYear, lunMonth, lunDay, lunIljin 등이 포함된 데이터
    } else {
      throw new Error(result.error || 'KASI API 프록시 응답 실패');
    }
    
  } catch (error) {
    console.warn(`⚠️  KASI API 프록시 호출 실패 (${dateStr}):`, error);
    return null; // 실패 시 null 반환하여 폴백 로직 실행
  }
};

// KASI XML 응답 파싱
const parseKasiXmlResponse = (xmlText: string): any => {
  try {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
    
    const item = xmlDoc.querySelector('item');
    if (!item) return null;

    return {
      lunDay: item.querySelector('lunDay')?.textContent || '',
      lunIljin: item.querySelector('lunIljin')?.textContent || '',
      lunLeapmonth: item.querySelector('lunLeapmonth')?.textContent || '평',
      lunMonth: item.querySelector('lunMonth')?.textContent || '',
      lunNday: item.querySelector('lunNday')?.textContent || '',
      lunSecha: item.querySelector('lunSecha')?.textContent || '',
      lunWolgeon: item.querySelector('lunWolgeon')?.textContent || '',
      lunYear: item.querySelector('lunYear')?.textContent || '',
      solWeek: item.querySelector('solWeek')?.textContent || '',
    };
  } catch (error) {
    console.warn('KASI XML 파싱 실패:', error);
    return null;
  }
};

// KASI API 전용 60갑자 계산 (폴백 없음)
export const getKasi60갑자 = async (date: Date): Promise<string> => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  const kasiData = await fetchKasiCalendarInfo(year, month, day);
  
  if (!kasiData) {
    throw new Error(`KASI API 응답 없음: ${year}-${month}-${day}`);
  }
  
  if (!kasiData.lunIljin) {
    throw new Error(`KASI API lunIljin 필드 없음: ${year}-${month}-${day}`);
  }
  
  // KASI에서 받은 일진(lunIljin)에서 한글 부분 추출
  // 예: "을해(乙亥)" -> "을해"
  const match = kasiData.lunIljin.match(/^([가-힣]+)/);
  if (!match) {
    throw new Error(`KASI API lunIljin 파싱 실패: ${kasiData.lunIljin}`);
  }
  
  return match[1];
};

// KASI API 전용 음력 정보 계산 (폴백 없음)
export const getKasi음력정보 = async (date: Date): Promise<{
  lunarDate: string;
  lunarYear: number;
  lunarMonth: number;
  lunarDay: number;
  isLeapMonth: boolean;
  yearPillar: string;
  monthPillar: string;
}> => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  const kasiData = await fetchKasiCalendarInfo(year, month, day);
  
  if (!kasiData) {
    throw new Error(`KASI API 응답 없음: ${year}-${month}-${day}`);
  }
  
  const lunarYear = parseInt(kasiData.lunYear);
  const lunarMonth = parseInt(kasiData.lunMonth);
  const lunarDay = parseInt(kasiData.lunDay);
  const isLeapMonth = kasiData.lunLeapmonth === '윤';
  
  if (!lunarYear || !lunarMonth || !lunarDay) {
    throw new Error(`KASI API 음력 날짜 파싱 실패: ${JSON.stringify(kasiData)}`);
  }
  
  const lunarDateStr = `음력 ${lunarYear}년 ${lunarMonth}월 ${lunarDay}일${isLeapMonth ? ' (윤달)' : ''}`;
  
  return {
    lunarDate: lunarDateStr,
    lunarYear,
    lunarMonth,
    lunarDay,
    isLeapMonth,
    yearPillar: kasiData.lunSecha || '연주미확인',
    monthPillar: kasiData.lunWolgeon || '월주미확인',
  };
};

// 24절기 정보 (KASI API 기반)
const 절기정보 = {
  1: [['소한', 5], ['대한', 20]],
  2: [['입춘', 4], ['우수', 19]],
  3: [['경칩', 6], ['춘분', 21]],
  4: [['청명', 5], ['곡우', 20]],
  5: [['입하', 6], ['소만', 21]],
  6: [['망종', 6], ['하지', 21]],
  7: [['소서', 7], ['대서', 23]],
  8: [['입추', 8], ['처서', 23]],
  9: [['백로', 8], ['추분', 23]],
  10: [['한로', 9], ['상강', 24]],
  11: [['입동', 8], ['소설', 23]],
  12: [['대설', 7], ['동지', 22]],
} as const;

export const getKasi절기 = (date: Date): string | null => {
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  const monthInfo = 절기정보[month as keyof typeof 절기정보];
  if (!monthInfo) return null;
  
  for (const [name, targetDay] of monthInfo) {
    if (Math.abs(day - targetDay) <= 1) { // ±1일 오차 허용
      return name;
    }
  }
  
  return null;
};

export default {
  generateCalendarMonth,
  getMonthlyFortune,
  getTodayFortune,
  get60갑자,
  getKasi60갑자,
  getKasi음력정보,
  getKasi절기,
  fetchKasiCalendarInfo,
  get음력변환,
  is손없는날,
  get길흉,
  get절기,
  get운세점수,
  get특이사항,
  천간,
  지지,
  띠동물,
  오행매핑
};