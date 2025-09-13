/**
 * 월주 계산 및 표기 유틸리티
 * ================================
 *
 * 양력 달력에서 절기 전환점을 고려한 정확한 월주 표기
 * - 한 달 안에 절기 전환이 있으면 2개 월주 표기
 * - 절기 전환 날짜 정보 포함
 */

// 절기별 월지 매핑
const SOLAR_TERM_TO_JIJI_INDEX = {
  "입춘": 2,   // 인월 (정월)
  "경칩": 3,   // 묘월 (2월)
  "청명": 4,   // 진월 (3월)
  "입하": 5,   // 사월 (4월)
  "망종": 6,   // 오월 (5월)
  "소서": 7,   // 미월 (6월)
  "입추": 8,   // 신월 (7월)
  "백로": 9,   // 유월 (8월)
  "한로": 10,  // 술월 (9월)
  "입동": 11,  // 해월 (10월)
  "대설": 0,   // 자월 (11월)
  "소한": 1    // 축월 (12월)
} as const;

// 천간, 지지
const CHEONAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"] as const;
const JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"] as const;

// 년간별 월간 기준 (갑기년, 을경년, 병신년, 정임년, 무계년)
const YEAR_TO_MONTH_BASE = {
  "갑": 2, "기": 2,   // 병인월부터 시작
  "을": 4, "경": 4,   // 무인월부터 시작
  "병": 6, "신": 6,   // 경인월부터 시작
  "정": 8, "임": 8,   // 임인월부터 시작
  "무": 0, "계": 0    // 갑인월부터 시작
} as const;

interface MonthPillarInfo {
  /** 전체 월주 (절기 전환이 없으면 1개, 있으면 2개) */
  monthPillars: string[];
  /** 절기 전환 정보 */
  solarTermTransition?: {
    date: number;           // 전환 일자
    termName: string;       // 절기명
    beforePillar: string;   // 전환 전 월주
    afterPillar: string;    // 전환 후 월주
  };
  /** 표기용 문자열 */
  displayText: string;
}

/**
 * 년간과 월지 인덱스로 월간 계산
 */
function getMonthGapja(yearCheonan: string, jijiIndex: number): string {
  const baseIndex = YEAR_TO_MONTH_BASE[yearCheonan as keyof typeof YEAR_TO_MONTH_BASE] || 0;
  const monthOffset = (jijiIndex - 2 + 12) % 12; // 인월(2)을 기준으로 조정
  const cheonganIndex = (baseIndex + monthOffset) % 10;

  return `${CHEONAN[cheonganIndex]}${JIJI[jijiIndex]}`;
}

/**
 * 년주에서 년간 추출
 */
function getYearCheonan(yearPillar: string): string {
  return yearPillar[0];
}

/**
 * 양력 월의 절기 전환 정보 조회
 */
async function getSolarTermsInMonth(year: number, month: number): Promise<Array<{
  date: number;
  termName: string;
  jijiIndex: number;
}>> {
  try {
    // 백엔드 API 호출로 해당 월의 절기 정보 조회
    const response = await fetch(`/api/perpetual-calendar/solar-terms/${year}/${month}`);
    if (!response.ok) {
      throw new Error(`절기 조회 실패: ${response.status}`);
    }

    const solarTerms = await response.json();

    return solarTerms
      .filter((term: any) => term.solar_term_korean in SOLAR_TERM_TO_JIJI_INDEX)
      .map((term: any) => ({
        date: parseInt(term.solar_day),
        termName: term.solar_term_korean,
        jijiIndex: SOLAR_TERM_TO_JIJI_INDEX[term.solar_term_korean as keyof typeof SOLAR_TERM_TO_JIJI_INDEX]
      }))
      .sort((a, b) => a.date - b.date);

  } catch (error) {
    console.error('절기 정보 조회 실패:', error);
    return [];
  }
}

/**
 * 특정 날짜의 정확한 월주 계산 (절기 기준)
 */
export async function getDateMonthPillar(
  year: number,
  month: number,
  day: number,
  yearPillar: string
): Promise<string> {
  const yearCheonan = getYearCheonan(yearPillar);

  // 해당 월과 이전/다음 월의 절기 정보 조회
  const [prevMonthTerms, currentMonthTerms, nextMonthTerms] = await Promise.all([
    getSolarTermsInMonth(year, month - 1),
    getSolarTermsInMonth(year, month),
    getSolarTermsInMonth(year, month + 1)
  ]);

  // 현재 날짜가 속하는 절기 구간 찾기
  const allTerms = [
    ...prevMonthTerms.map(t => ({ ...t, month: month - 1 })),
    ...currentMonthTerms.map(t => ({ ...t, month: month })),
    ...nextMonthTerms.map(t => ({ ...t, month: month + 1 }))
  ].sort((a, b) => {
    const dateA = new Date(year, a.month - 1, a.date).getTime();
    const dateB = new Date(year, b.month - 1, b.date).getTime();
    return dateA - dateB;
  });

  const currentDate = new Date(year, month - 1, day);

  let currentJijiIndex = 2; // 기본값: 인월

  for (const term of allTerms) {
    const termDate = new Date(year, term.month - 1, term.date);
    if (currentDate >= termDate) {
      currentJijiIndex = term.jijiIndex;
    } else {
      break;
    }
  }

  return getMonthGapja(yearCheonan, currentJijiIndex);
}

/**
 * 양력 월의 월주 정보 계산 (절기 전환 고려)
 */
export async function getMonthPillarInfo(
  year: number,
  month: number,
  yearPillar: string
): Promise<MonthPillarInfo> {
  const yearCheonan = getYearCheonan(yearPillar);

  // 해당 월의 절기 정보 조회
  const solarTerms = await getSolarTermsInMonth(year, month);

  if (solarTerms.length === 0) {
    // 절기 전환이 없는 경우 - 이전 절기 기준으로 계산
    const monthStart = await getDateMonthPillar(year, month, 1, yearPillar);

    return {
      monthPillars: [monthStart],
      displayText: monthStart
    };
  }

  if (solarTerms.length === 1) {
    // 절기 전환이 1번 있는 경우
    const term = solarTerms[0];

    // 전환 전 월주 (1일 기준)
    const beforePillar = await getDateMonthPillar(year, month, 1, yearPillar);

    // 전환 후 월주
    const afterPillar = getMonthGapja(yearCheonan, term.jijiIndex);

    if (beforePillar === afterPillar) {
      // 월주가 같으면 1개만 표기
      return {
        monthPillars: [beforePillar],
        displayText: beforePillar
      };
    }

    return {
      monthPillars: [beforePillar, afterPillar],
      solarTermTransition: {
        date: term.date,
        termName: term.termName,
        beforePillar,
        afterPillar
      },
      displayText: `${beforePillar} → ${afterPillar} (${term.date}일 ${term.termName})`
    };
  }

  // 절기 전환이 2번 이상인 경우 (드문 경우)
  const firstTerm = solarTerms[0];
  const lastTerm = solarTerms[solarTerms.length - 1];

  const startPillar = await getDateMonthPillar(year, month, 1, yearPillar);
  const endPillar = getMonthGapja(yearCheonan, lastTerm.jijiIndex);

  if (startPillar === endPillar) {
    return {
      monthPillars: [startPillar],
      displayText: startPillar
    };
  }

  return {
    monthPillars: [startPillar, endPillar],
    solarTermTransition: {
      date: firstTerm.date,
      termName: firstTerm.termName,
      beforePillar: startPillar,
      afterPillar: endPillar
    },
    displayText: `${startPillar} → ${endPillar} (${firstTerm.date}일부터)`
  };
}

/**
 * 간단한 월주 문자열 가져오기 (기존 호환성용)
 */
export async function getSimpleMonthPillar(
  year: number,
  month: number,
  day: number,
  yearPillar: string
): Promise<string> {
  return await getDateMonthPillar(year, month, day, yearPillar);
}

/**
 * 양력 월 전체의 월주 표기 문자열 (캘린더 헤더용)
 */
export async function getMonthDisplayText(
  year: number,
  month: number,
  yearPillar: string
): Promise<string> {
  const info = await getMonthPillarInfo(year, month, yearPillar);
  return info.displayText;
}

export type { MonthPillarInfo };