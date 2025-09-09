/**
 * 캘린더 핵심 로직 모듈 - 700줄 제한 준수
 * =========================================
 * 
 * 캘린더 생성 및 KASI API 연동 핵심 기능만 포함
 * - generateCalendarMonth (메인 함수)
 * - KASI API 연동 함수들
 * - 60갑자 계산 핵심 로직
 * - Atomic API 설정
 */

// 🔥 중복 제거: 상수는 sajuConstants.ts에서 import
import { 갑자60순환, 갑자한자매핑, get갑자표시 } from './sajuConstants';
import { get운세점수, get특이사항, get길흉, is손없는날, get절기상세정보, is절기날 } from './calendarUtils';

// 🚀 Atomic API 전환 설정 (점진적 마이그레이션)
export const ATOMIC_API_CONFIG = {
  /** 
   * 🔥 Atomic API 사용 여부 (기본값: false - 기존 시스템 유지)
   * ⚠️  true로 설정 시 모든 계산이 백엔드 atomic 모듈로 이동
   * 📈 성능: 프론트엔드 로직 제거, 서버 중앙화
   */
  USE_ATOMIC_API: false, // 개발 단계에서는 false로 시작
  
  /** 
   * 🎯 부분적 전환 설정 (특정 기능만 atomic 사용)
   */
  ATOMIC_FEATURES: {
    GAPJA_CALCULATION: true,   // 60갑자 계산을 atomic으로
    YEAR_PILLAR: true,         // 년주 계산을 atomic으로
    LUNAR_CONVERSION: false,   // 음력 변환은 아직 기존 시스템
    COMPLETE_SAJU: false,      // 완전한 사주는 아직 기존 시스템
  },
  
  /** 
   * 🔧 폴백 설정 (atomic API 실패 시 기존 로직 사용)
   */
  ENABLE_FALLBACK: true,
  
  /** 
   * 📊 성능 모니터링 (atomic vs 기존 로직 비교)
   */
  ENABLE_PERFORMANCE_MONITORING: true,
} as const;

// 📅 캘린더 데이터 타입 정의
export interface CalendarDate {
  date: Date;
  day: number;
  gapja: string;
  cheongan: string;
  jiji: string;
  animal: string;
  element: string;
  lunarDate: string;
  isToday: boolean;
  isWeekend: boolean;
  isHoliday: boolean;
  fortuneScore: number;
  specialNotes: string[];
  isGoodDay: boolean;
  isBadDay: boolean;
  yearPillar: string;
}

// KASI API 오류 추적
interface KasiApiError {
  date: string;
  endpoint: string;
  error: string;
  timestamp: number;
}

let kasiErrors: KasiApiError[] = [];

// 🔥 핵심 60갑자 계산 함수들
const get60갑자Local = (date: Date): string => {
  const 기준일 = new Date(1900, 0, 31); // 1900년 1월 31일 = 갑진일 
  const 기준갑자인덱스 = 40; // 갑진의 인덱스
  
  const 날짜차이 = Math.floor((date.getTime() - 기준일.getTime()) / (24 * 60 * 60 * 1000));
  let 갑자인덱스 = (기준갑자인덱스 + 날짜차이) % 60;
  
  if (갑자인덱스 < 0) {
    갑자인덱스 += 60;
  }
  
  return 갑자60순환[갑자인덱스];
};

export const get60갑자Sync = (date: Date): string => {
  return get60갑자Local(date);
};

export const get60갑자 = async (date: Date): Promise<string> => {
  // Atomic API 연동은 추후 구현
  return get60갑자Local(date);
};

// 년주 계산 함수 (입춘 기준)
export const get년주 = (date: Date): string => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1; // 1-12월
  const day = date.getDate();
  
  // 입춘 기준: 매년 2월 4일 전후
  let sajuYear = year;
  if (month < 2 || (month === 2 && day < 4)) {
    sajuYear = year - 1; // 입춘 이전은 전년도
  }
  
  // 1900년 = 경자년(36번째) 기준으로 60갑자 순환 계산
  const 기준년도 = 1900;
  const 기준년갑자인덱스 = 36; // 경자의 인덱스
  
  let 년갑자인덱스 = (기준년갑자인덱스 + (sajuYear - 기준년도)) % 60;
  if (년갑자인덱스 < 0) 년갑자인덱스 += 60;
  
  return 갑자60순환[년갑자인덱스];
};

// 🔥 KASI API 연동 함수들
export const fetchKasiCalendarInfo = async (year: number, month: number, day: number): Promise<any> => {
  try {
    const response = await fetch(`/api/kasi/calendar?year=${year}&month=${month}&day=${day}`);
    
    if (!response.ok) {
      throw new Error(`KASI API HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (!data.lunIljin || !data.lunSecha) {
      throw new Error('KASI API 응답 데이터 불완전');
    }
    
    return data;
  } catch (error) {
    console.warn(`KASI API 오류 (${year}-${month}-${day}):`, error);
    
    // 오류 기록
    kasiErrors.push({
      date: `${year}-${month}-${day}`,
      endpoint: `/api/kasi/calendar`,
      error: error instanceof Error ? error.message : String(error),
      timestamp: Date.now()
    });
    
    // 최대 100개 오류 기록 유지
    if (kasiErrors.length > 100) {
      kasiErrors = kasiErrors.slice(-100);
    }
    
    return null;
  }
};

export const getKasi60갑자 = async (date: Date): Promise<string> => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  try {
    const kasiData = await fetchKasiCalendarInfo(year, month, day);
    
    if (kasiData && kasiData.lunIljin) {
      return kasiData.lunIljin;
    }
  } catch (error) {
    console.warn('KASI 60갑자 조회 실패, 로컬 계산으로 폴백:', error);
  }
  
  return get60갑자Local(date);
};

export const getKasi음력정보 = async (date: Date): Promise<{
  lunYear: number;
  lunMonth: number;
  lunDay: number;
  lunLeapmonth: string;
  lunWolgeonString: string;
}> => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  try {
    const kasiData = await fetchKasiCalendarInfo(year, month, day);
    
    if (kasiData) {
      return {
        lunYear: kasiData.lunYear || year,
        lunMonth: kasiData.lunMonth || month,
        lunDay: kasiData.lunDay || day,
        lunLeapmonth: kasiData.lunLeapmonth || "평달",
        lunWolgeonString: kasiData.lunWolgeonString || `${month}월 ${day}일`
      };
    }
  } catch (error) {
    console.warn('KASI 음력 정보 조회 실패:', error);
  }
  
  // 폴백: 간단한 근사값
  return {
    lunYear: year,
    lunMonth: month,
    lunDay: day,
    lunLeapmonth: "평달",
    lunWolgeonString: `${month}월 ${day}일 (근사)`
  };
};

// KASI API 오류 추적 함수들
export const getKasiApiErrors = (): KasiApiError[] => {
  return [...kasiErrors];
};

export const getKasiApiErrorSummary = () => {
  const total = kasiErrors.length;
  const recent = kasiErrors.filter(e => Date.now() - e.timestamp < 3600000).length; // 1시간 이내
  
  return {
    totalErrors: total,
    recentErrors: recent,
    oldestError: total > 0 ? new Date(kasiErrors[0].timestamp).toISOString() : null,
    latestError: total > 0 ? new Date(kasiErrors[total - 1].timestamp).toISOString() : null
  };
};

// 🔥 메인 캘린더 생성 함수 (핵심 로직)
export const generateCalendarMonth = async (year: number, month: number): Promise<CalendarDate[]> => {
  const daysInMonth = new Date(year, month, 0).getDate();
  const calendarDates: CalendarDate[] = [];
  
  console.log(`📅 ${year}년 ${month}월 캘린더 생성 시작 (${daysInMonth}일)`);
  
  // KASI API에서 기준점 데이터 가져오기 (15일 기준)
  const referenceDay = 15;
  let kasiReferenceData: any = null;
  
  if (referenceDay <= daysInMonth) {
    try {
      kasiReferenceData = await fetchKasiCalendarInfo(year, month, referenceDay);
      if (kasiReferenceData) {
        console.log(`🎯 KASI 기준 데이터 (${month}월 ${referenceDay}일):`, {
          갑자: kasiReferenceData.lunIljin,
          음력: kasiReferenceData.lunWolgeonString
        });
      }
    } catch (error) {
      console.warn(`KASI 기준 데이터 조회 실패 (${month}월 ${referenceDay}일):`, error);
    }
  }
  
  // 패턴 기반 오프셋 계산 (성능 최적화)
  let gapjaOffset = 0;
  if (kasiReferenceData) {
    const referenceDate = new Date(year, month - 1, referenceDay);
    const localGapja = get60갑자Sync(referenceDate);
    const kasiGapja = kasiReferenceData.lunIljin;
    
    const localIndex = 갑자60순환.indexOf(localGapja);
    const kasiIndex = 갑자60순환.indexOf(kasiGapja);
    
    if (localIndex !== -1 && kasiIndex !== -1) {
      gapjaOffset = (kasiIndex - localIndex + 60) % 60;
      console.log(`🔧 갑자 오프셋 계산: ${localGapja}(${localIndex}) → ${kasiGapja}(${kasiIndex}) = +${gapjaOffset}`);
    }
  }
  
  // 각 날짜별 캘린더 데이터 생성
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month - 1, day);
    const today = new Date();
    
    // 갑자 계산 (오프셋 적용)
    let gapja = get60갑자Sync(date);
    if (gapjaOffset > 0) {
      const currentIndex = 갑자60순환.indexOf(gapja);
      if (currentIndex !== -1) {
        const newIndex = (currentIndex + gapjaOffset) % 60;
        gapja = 갑자60순환[newIndex];
      }
    }
    
    // 갑자 분해
    const cheongan = gapja[0];
    const jiji = gapja[1];
    
    // 띠 동물 및 오행 계산
    const animals: Record<string, string> = {
      '자': '쥐', '축': '소', '인': '호랑이', '묘': '토끼',
      '진': '용', '사': '뱀', '오': '말', '미': '양',
      '신': '원숭이', '유': '닭', '술': '개', '해': '돼지'
    };
    
    const elements: Record<string, string> = {
      '갑': '목', '을': '목', '병': '화', '정': '화', '무': '토',
      '기': '토', '경': '금', '신': '금', '임': '수', '계': '수'
    };
    
    const animal = animals[jiji] || '미지';
    const element = elements[cheongan] || '미지';
    
    // 년주 계산
    const yearPillar = get년주(date);
    
    // 음력 변환 (간단 근사)
    const lunarDate = `음력 ${month}월 ${day}일`;
    
    // 길흉 및 운세 점수 계산
    const 길흉결과 = get길흉(gapja, date);
    const fortuneScore = get운세점수(gapja, date);
    const specialNotes = get특이사항(date, gapja, false);
    
    // 캘린더 데이터 객체 생성
    const calendarDate: CalendarDate = {
      date,
      day,
      gapja,
      cheongan,
      jiji,
      animal,
      element,
      lunarDate,
      isToday: date.toDateString() === today.toDateString(),
      isWeekend: date.getDay() === 0 || date.getDay() === 6,
      isHoliday: false, // TODO: 공휴일 계산 추가
      fortuneScore,
      specialNotes,
      isGoodDay: 길흉결과.길일,
      isBadDay: 길흉결과.흉일,
      yearPillar
    };
    
    calendarDates.push(calendarDate);
  }
  
  console.log(`✅ ${year}년 ${month}월 캘린더 생성 완료 (${calendarDates.length}일)`);
  return calendarDates;
};

// 오늘의 운세 조회
export const getTodayFortune = async (): Promise<CalendarDate> => {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  
  const monthData = await generateCalendarMonth(year, month);
  const todayData = monthData.find(d => d.isToday);
  
  if (!todayData) {
    throw new Error('오늘 날짜 데이터를 찾을 수 없습니다');
  }
  
  return todayData;
};

// 월별 운세 요약
export const getMonthlyFortune = async (year: number, month: number): Promise<{
  averageScore: number;
  goodDays: number;
  badDays: number;
  totalDays: number;
  bestDay: CalendarDate | null;
  worstDay: CalendarDate | null;
}> => {
  const monthData = await generateCalendarMonth(year, month);
  
  const scores = monthData.map(d => d.fortuneScore);
  const averageScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
  
  const goodDays = monthData.filter(d => d.isGoodDay).length;
  const badDays = monthData.filter(d => d.isBadDay).length;
  
  const bestDay = monthData.reduce((best, current) => 
    current.fortuneScore > (best?.fortuneScore || 0) ? current : best, null as CalendarDate | null);
  
  const worstDay = monthData.reduce((worst, current) => 
    current.fortuneScore < (worst?.fortuneScore || 6) ? current : worst, null as CalendarDate | null);
  
  return {
    averageScore: Math.round(averageScore * 100) / 100,
    goodDays,
    badDays,
    totalDays: monthData.length,
    bestDay,
    worstDay
  };
};

// 내보내기
// Re-export utilities for backward compatibility
export { get절기상세정보, is절기날 };
export { get갑자표시 };

export default {
  ATOMIC_API_CONFIG,
  get60갑자,
  get60갑자Sync,
  get년주,
  generateCalendarMonth,
  getTodayFortune,
  getMonthlyFortune,
  fetchKasiCalendarInfo,
  getKasi60갑자,
  getKasi음력정보,
  getKasiApiErrors,
  getKasiApiErrorSummary,
  get절기상세정보,
  is절기날,
  get갑자표시
};