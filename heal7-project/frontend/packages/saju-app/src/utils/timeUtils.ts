/**
 * 시간 관련 글로벌 상수 및 유틸리티 함수
 * 한국 표준시(KST) UTC+9 기준으로 통일
 */

// 🇰🇷 한국 표준시 상수
export const KOREA_TIMEZONE_OFFSET = 9; // UTC+9
export const KOREA_TIMEZONE_MS = KOREA_TIMEZONE_OFFSET * 60 * 60 * 1000;

/**
 * 현재 한국 시간을 반환하는 함수
 * @returns {Date} 한국 시간대로 변환된 Date 객체
 */
export const getKoreaTime = (): Date => {
  // 올바른 방법: 시간대를 명시적으로 지정하여 한국시간 획득
  return new Date(new Date().toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
};

/**
 * 한국 시간 기준 현재 시각(0-23)을 반환
 * @returns {number} 0-23 시간
 */
export const getKoreaHour = (): number => {
  return getKoreaTime().getHours();
};

/**
 * 한국 시간 기준으로 낮인지 밤인지 판단
 * @param hour 시간 (선택사항, 기본값은 현재 한국 시간)
 * @returns {boolean} true: 밤(19:00-05:59), false: 낮(06:00-18:59)
 */
export const isNightTimeInKorea = (hour?: number): boolean => {
  const currentHour = hour ?? getKoreaHour();
  // 더 정확한 한국의 일출/일몰 시간 반영: 밤 19시~새벽 5시59분
  return currentHour >= 19 || currentHour < 6;
};

/**
 * 한국 시간 기준 날짜 문자열 반환
 * @param format 포맷 타입
 * @returns {string} 포맷된 날짜 문자열
 */
export const getKoreaDateString = (format: 'YYYY-MM-DD' | 'YYYY-MM-DD HH:mm' | 'HH:mm' = 'YYYY-MM-DD'): string => {
  const koreaTime = getKoreaTime();
  
  switch (format) {
    case 'YYYY-MM-DD':
      return koreaTime.toISOString().split('T')[0];
    case 'HH:mm':
      return koreaTime.toTimeString().slice(0, 5);
    case 'YYYY-MM-DD HH:mm':
      const date = koreaTime.toISOString().split('T')[0];
      const time = koreaTime.toTimeString().slice(0, 5);
      return `${date} ${time}`;
    default:
      return koreaTime.toISOString();
  }
};

/**
 * 사주명리학에서 사용하는 한국 전통 시간대 변환
 * @param hour 24시간 형식 시간
 * @returns {string} 전통 시간 이름 (자시, 축시, 인시...)
 */
export const getTraditionalKoreaHour = (hour?: number): string => {
  const currentHour = hour ?? getKoreaHour();
  
  const traditionalHours = [
    '자시 (23-01시)', '축시 (01-03시)', '인시 (03-05시)', '묘시 (05-07시)',
    '진시 (07-09시)', '사시 (09-11시)', '오시 (11-13시)', '미시 (13-15시)',
    '신시 (15-17시)', '유시 (17-19시)', '술시 (19-21시)', '해시 (21-23시)'
  ];
  
  // 23시는 자시(0), 1시는 축시(1) 방식으로 매핑
  let index;
  if (currentHour >= 23) index = 0; // 23시 = 자시
  else if (currentHour === 0) index = 0; // 0시 = 자시  
  else index = Math.floor((currentHour + 1) / 2); // 1-22시는 2시간씩 묶어서 계산
  
  return traditionalHours[index] || '알 수 없음';
};