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
  lunarYear: number;
  lunarMonth: number;
  lunarDay: number;
  isLeapMonth: boolean;
  isToday: boolean;
  isWeekend: boolean;
  isHoliday: boolean;
  운세점수: number;
  특이사항: string[];
  isGoodDay: boolean;
  isBadDay: boolean;
  yearPillar: string;
  monthPillar?: string;
  // 호환성을 위한 영어 속성들 (deprecated)
  fortuneScore?: number;
  specialNotes?: string[];
  // 추가 한글 속성들
  zodiac: string;
  gilil?: boolean;
  흉일?: boolean;
  sonEobNeunNal?: boolean;
  절기?: string;
}

// 월별 운세 데이터 타입 정의
export interface MonthlyFortune {
  averageScore: number;
  goodDays: number;
  badDays: number;
  totalDays: number;
  bestDay: CalendarDate | null;
  worstDay: CalendarDate | null;
  monthlyMessage: string;
  bestDates: CalendarDate[];
  importantDates: CalendarDate[];
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

// 월주 계산은 백엔드에서 처리 (프론트엔드에서는 사용하지 않음)
// 백엔드 API: /api/perpetual-calendar/saju/{year}/{month}/{day}

// 년주 계산 함수 (입춘 기준) - 폴백용만 유지
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

// 🔥 메인 캘린더 생성 함수 (DB 연동 버전) ⚡ 2025-09-12 교체
export const generateCalendarMonth = async (year: number, month: number): Promise<CalendarDate[]> => {
  console.log(`📅 ${year}년 ${month}월 캘린더 생성 시작 (DB 연동)`);
  
  try {
    // 🚀 새로운 만세력 DB API 호출 (기존 KASI API 30회 → DB 쿼리 1회)
    const response = await fetch(`/api/perpetual-calendar/month/${year}/${month}`);
    
    if (!response.ok) {
      throw new Error(`DB API 호출 실패: ${response.status}`);
    }
    
    const dbData = await response.json();
    console.log(`✅ DB에서 ${dbData.days_count}일 데이터 조회 완료`);
    
    // DB 데이터를 CalendarDate 형식으로 변환
    const calendarDates: CalendarDate[] = [];
    const today = new Date();
    
    for (const dbDay of dbData.calendar_days) {
      // Date 객체를 UTC 0시로 생성하여 시간대 문제 방지
      const date = new Date(Date.UTC(year, month - 1, dbDay.solar_day, 0, 0, 0));
      // 로컬 날짜로 변환 (화면 표시용)
      date.setHours(0, 0, 0, 0);
      
      // 갑자 분해 (DB에서 가져온 정확한 데이터 사용)
      const gapja = dbDay.day_gapja;
      const cheongan = gapja?.[0] || '갑';
      const jiji = gapja?.[1] || '자';
      
      // 띠 동물 및 오행 계산 (상수 활용)
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
      
      // 년주는 DB에서 가져온 정확한 데이터 사용
      const yearPillar = dbDay.year_gapja;
      
      // 월주는 백엔드에서 계산된 값 사용 (백엔드가 Single Source of Truth)
      const monthPillar = dbDay.month_gapja || '-';  // 백엔드에서 이미 계산됨
      
      // 음력 정보도 DB에서 가져온 정확한 데이터 사용
      const lunarYear = dbDay.lunar_year;
      const lunarMonth = dbDay.lunar_month;
      const lunarDay = dbDay.lunar_day;
      const isLeapMonth = dbDay.is_leap_month;
      const lunarDate = `음력 ${lunarYear}년 ${lunarMonth}월 ${lunarDay}일${isLeapMonth ? ' (윤달)' : ''}`;
      
      // 길흉 및 운세 점수 계산 (기존 로직 유지)
      const 길흉결과 = get길흉(gapja, date) || { 길일: false, 흉일: false };
      const 운세점수 = get운세점수(gapja, date) || 3;
      const 특이사항 = get특이사항(date, gapja, !!dbDay.solar_term_name) || [];
      
      // 24절기 정보 추가
      if (dbDay.solar_term_name) {
        특이사항.unshift(`${dbDay.solar_term_name} 절기`);
      }
      
      // zodiac 매핑
      const zodiacMap: { [key: string]: string } = {
        '자': '쥐', '축': '소', '인': '호랑이', '묘': '토끼', '진': '용', '사': '뱀',
        '오': '말', '미': '양', '신': '원숭이', '유': '닭', '술': '개', '해': '돼지'
      };
      const zodiac = zodiacMap[jiji] || '알수없음';
      
      // 캘린더 데이터 객체 생성 (DB 데이터 기반)
      const calendarDate: CalendarDate = {
        date,
        day: dbDay.solar_day,
        gapja,
        cheongan,
        jiji,
        animal,
        element,
        lunarDate,
        lunarYear,
        lunarMonth,
        lunarDay,
        isLeapMonth,
        isToday: date.toDateString() === today.toDateString(),
        isWeekend: date.getDay() === 0 || date.getDay() === 6,
        isHoliday: false, // TODO: 공휴일 계산 추가
        운세점수,
        특이사항,
        isGoodDay: 길흉결과.길일,
        isBadDay: 길흉결과.흉일,
        yearPillar,
        monthPillar,
        zodiac,
        gilil: 길흉결과.길일,
        흉일: 길흉결과.흉일,
        sonEobNeunNal: is손없는날(date),
        절기: dbDay.solar_term_name,
        // 호환성을 위한 영어 속성들
        fortuneScore: 운세점수,
        specialNotes: 특이사항
      };
      
      calendarDates.push(calendarDate);
    }
    
    console.log(`✅ ${year}년 ${month}월 DB 연동 캘린더 생성 완료 (${calendarDates.length}일)`);
    console.log(`🚀 성능 향상: KASI API 30회 호출 → DB 쿼리 1회 (97% 단축)`);
    
    return calendarDates;
    
  } catch (error) {
    console.error(`❌ DB 연동 캘린더 생성 실패: ${error}`);
    console.log(`🔄 기존 KASI API 방식으로 폴백 처리`);
    
    // 폴백: 기존 KASI API 방식 (임시)
    return generateCalendarMonthFallback(year, month);
  }
};

// 🔄 기존 KASI API 방식 (폴백용) - 향후 제거 예정
const generateCalendarMonthFallback = async (year: number, month: number): Promise<CalendarDate[]> => {
  console.warn(`⚠️ 폴백 모드: 기존 KASI API 방식 사용 (${year}년 ${month}월)`);
  
  const daysInMonth = new Date(year, month, 0).getDate();
  const calendarDates: CalendarDate[] = [];
  
  // 간단한 폴백 로직 (정확성 낮음)
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month - 1, day);
    const today = new Date();
    
    const gapja = get60갑자Sync(date);
    const cheongan = gapja?.[0] || '갑';
    const jiji = gapja?.[1] || '자';
    
    const calendarDate: CalendarDate = {
      date,
      day,
      gapja,
      cheongan,
      jiji,
      animal: '미지',
      element: '미지', 
      lunarDate: `음력 ${month}월 ${day}일 (근사)`,
      lunarYear: year,
      lunarMonth: month,
      lunarDay: day,
      isLeapMonth: false,
      isToday: date.toDateString() === today.toDateString(),
      isWeekend: date.getDay() === 0 || date.getDay() === 6,
      isHoliday: false,
      운세점수: 3,
      특이사항: ['폴백 모드'],
      isGoodDay: false,
      isBadDay: false,
      yearPillar: get년주(date),
      zodiac: '알수없음',
      gilil: false,
      흉일: false,
      sonEobNeunNal: false,
      fortuneScore: 3,
      specialNotes: ['폴백 모드']
    };
    
    calendarDates.push(calendarDate);
  }
  
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
export const getMonthlyFortune = async (year: number, month: number): Promise<MonthlyFortune> => {
  const monthData = await generateCalendarMonth(year, month);
  
  const scores = monthData.map(d => d.운세점수);
  const averageScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
  
  const goodDays = monthData.filter(d => d.isGoodDay).length;
  const badDays = monthData.filter(d => d.isBadDay).length;
  
  const bestDay = monthData.reduce((best, current) => 
    current.운세점수 > (best?.운세점수 || 0) ? current : best, null as CalendarDate | null);
  
  const worstDay = monthData.reduce((worst, current) => 
    current.운세점수 < (worst?.운세점수 || 6) ? current : worst, null as CalendarDate | null);
  
  // 좋은 날들 (운세점수 4 이상)
  const bestDates = monthData.filter(d => d.운세점수 >= 4).slice(0, 5);
  
  // 중요한 날들 (절기, 특이사항 있는 날들)
  const importantDates = monthData.filter(d => 
    d.특이사항.length > 0 || is절기날(d.date)
  ).slice(0, 5);
  
  // 월간 메시지 생성
  const monthNames = ['', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
  let monthlyMessage = `${year}년 ${monthNames[month]}은 `;
  
  if (averageScore >= 4) {
    monthlyMessage += '매우 좋은 운세의 달입니다. 새로운 도전을 시작하기 좋은 시기입니다.';
  } else if (averageScore >= 3) {
    monthlyMessage += '평온한 운세의 달입니다. 꾸준함과 인내가 좋은 결과를 가져올 것입니다.';
  } else {
    monthlyMessage += '신중함이 필요한 달입니다. 중요한 결정은 미루시고 기초를 다지는 시간으로 활용하세요.';
  }
  
  return {
    averageScore: Math.round(averageScore * 100) / 100,
    goodDays,
    badDays,
    totalDays: monthData.length,
    bestDay,
    worstDay,
    monthlyMessage,
    bestDates,
    importantDates
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

// 타입 export 추가
export type { CalendarDate, MonthlyFortune };