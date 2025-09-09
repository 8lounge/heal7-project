/**
 * 사주명리학 계산 함수 모듈
 * ==========================
 * 
 * 모든 사주 계산 로직 통합
 * - 60갑자 계산
 * - 년주/월주/일주/시주 계산
 * - 길흉 판정
 * - 운세 점수 계산
 */

import { 
  갑자60순환, 
  천간, 
  지지, 
  오행매핑, 
  띠동물, 
  GAPJA_REFERENCE_CONSTANTS,
  손없는날기준,
  길흉판정기준,
  절기매핑,
  운세점수기준
} from './sajuConstants';

import { get60갑자Hybrid, get년주Hybrid } from './atomicIntegration';

// 🔥 로컬 60갑자 계산 함수 (기존 로직 유지)
const get60갑자Local = (date: Date): string => {
  const 기준일 = GAPJA_REFERENCE_CONSTANTS.REFERENCE_DATE;
  const 기준갑자인덱스 = GAPJA_REFERENCE_CONSTANTS.REFERENCE_GAPJA_INDEX;
  
  const 날짜차이 = Math.floor((date.getTime() - 기준일.getTime()) / (24 * 60 * 60 * 1000));
  let 갑자인덱스 = (기준갑자인덱스 + 날짜차이) % 60;
  
  if (갑자인덱스 < 0) {
    갑자인덱스 += 60;
  }
  
  return 갑자60순환[갑자인덱스];
};

// 🚀 하이브리드 60갑자 계산 함수 (Atomic API + 로컬 계산)
export const get60갑자 = async (date: Date): Promise<string> => {
  return await get60갑자Hybrid(date, get60갑자Local);
};

// 🔄 동기 버전 (기존 코드 호환성)
export const get60갑자Sync = (date: Date): string => {
  return get60갑자Local(date);
};

// 🔥 로컬 년주 계산 함수 (입춘 기준)
const get년주Local = (date: Date): string => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1; // 1-12월
  const day = date.getDate();
  
  // 🔥 입춘 기준: 매년 2월 4일 전후 (KASI 기준)
  // 입춘 이전은 전년도 년주, 입춘 이후는 당년도 년주
  let sajuYear = year;
  if (month < 2 || (month === 2 && day < 4)) {
    sajuYear = year - 1; // 입춘 이전은 전년도
  }
  
  // 🎯 1900년 = 경자년(36번째) 기준으로 60갑자 순환 계산
  const 기준년도 = 1900;
  const 기준년갑자인덱스 = 36; // 경자의 인덱스
  
  let 년갑자인덱스 = (기준년갑자인덱스 + (sajuYear - 기준년도)) % 60;
  if (년갑자인덱스 < 0) 년갑자인덱스 += 60;
  
  const 년주 = 갑자60순환[년갑자인덱스];
  
  // 🔍 2025년 검증 로그
  if (year === 2025) {
    console.log(`🔥 년주 계산 (${year}-${month}-${day}):`, {
      입력날짜: `${year}년 ${month}월 ${day}일`,
      사주기준년도: sajuYear,
      입춘기준적용: month < 2 || (month === 2 && day < 4) ? '전년도' : '당년도',
      계산된인덱스: 년갑자인덱스,
      최종년주: 년주
    });
  }
  
  return 년주;
};

// 🚀 하이브리드 년주 계산 함수
export const get년주 = async (date: Date): Promise<string> => {
  return await get년주Hybrid(date, get년주Local);
};

// 🔄 동기 버전 년주 계산
export const get년주Sync = (date: Date): string => {
  return get년주Local(date);
};

// 크로스체크 함수 (검증용) - 60갑자에 실제 존재하는지 확인
export const is유효한60갑자 = (gapja: string): boolean => {
  return 갑자60순환.includes(gapja);
};

// 60갑자 유효성 검사와 함께 결과 반환
export const get60갑자WithValidation = (date: Date): { result: string; isValid: boolean; legacy: string } => {
  // 새로운 배열 기반 방식
  const 새로운결과 = get60갑자Sync(date);
  
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

// 길흉 판정 함수
export const get길흉 = (gapja: string, date: Date): { 길일: boolean; 흉일: boolean } => {
  // 간단한 길흉 판정 로직 (실제로는 더 복잡한 계산 필요)
  const 천간 = gapja[0];
  const 지지 = gapja[1];
  const 요일 = date.getDay(); // 0=일요일, 1=월요일, ...
  
  // 기본 길흉 판정 (예시)
  const 길일여부 = (천간 === '갑' && 지지 === '자') || 
                 (천간 === '을' && 지지 === '축') ||
                 (요일 === 0 || 요일 === 6); // 주말은 길일
  
  const 흉일여부 = (천간 === '무' && 지지 === '신') ||
                 (천간 === '기' && 지지 === '유') ||
                 (요일 === 2 ||요일 === 4); // 화,목요일은 흉일
  
  return {
    길일: 길일여부,
    흉일: 흉일여부
  };
};

// 손없는날 판정
export const is손없는날 = (date: Date): boolean => {
  const month = date.getMonth() + 1; // 1-12월
  const day = date.getDate();
  
  const 해당월손없는날 = 손없는날기준[month as keyof typeof 손없는날기준];
  return 해당월손없는날 ? 해당월손없는날.includes(day) : false;
};

// 24절기 판정
export const get절기 = (date: Date): string => {
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  // 현재 날짜와 가장 가까운 절기 찾기
  let 가장가까운절기 = '';
  let 최소차이 = Infinity;
  
  Object.entries(절기매핑).forEach(([절기명, { month: 절기월, day: 절기일 }]) => {
    // 날짜 차이 계산 (대략적)
    const 현재일수 = month * 30 + day;
    const 절기일수 = 절기월 * 30 + 절기일;
    const 차이 = Math.abs(현재일수 - 절기일수);
    
    if (차이 < 최소차이 && 차이 <= 3) { // 3일 이내
      최소차이 = 차이;
      가장가까운절기 = 절기명;
    }
  });
  
  return 가장가까운절기 || '';
};

// 운세 점수 계산
export const get운세점수 = (gapja: string, date: Date): number => {
  // 기본 점수
  let 점수 = 3; // 보통
  
  // 갑자에 따른 점수 조정
  const 천간 = gapja[0];
  const 지지 = gapja[1];
  
  // 오행 조화 확인
  const 천간오행 = 오행매핑[천간];
  const 지지오행 = 오행매핑[지지];
  
  if (천간오행 === 지지오행) {
    점수 += 1; // 오행이 같으면 +1
  }
  
  // 요일에 따른 조정
  const 요일 = date.getDay();
  if (요일 === 0 || 요일 === 6) {
    점수 += 1; // 주말 +1
  }
  
  // 손없는날 보너스
  if (is손없는날(date)) {
    점수 += 1;
  }
  
  // 절기 보너스
  if (get절기(date)) {
    점수 += 0.5;
  }
  
  // 1-5 범위로 제한
  return Math.max(1, Math.min(5, Math.floor(점수)));
};

// 특이사항 판정
export const get특이사항 = (date: Date, gapja: string, isLeapMonth: boolean = false): string[] => {
  const 특이사항들: string[] = [];
  
  // 손없는날
  if (is손없는날(date)) {
    특이사항들.push('손없는날');
  }
  
  // 길일/흉일
  const { 길일, 흉일 } = get길흉(gapja, date);
  if (길일) 특이사항들.push('길일');
  if (흉일) 특이사항들.push('흉일');
  
  // 절기
  const 절기 = get절기(date);
  if (절기) 특이사항들.push(`${절기}절기`);
  
  // 윤달
  if (isLeapMonth) {
    특이사항들.push('윤달');
  }
  
  // 특별한 갑자 조합
  if (gapja === '갑자') {
    특이사항들.push('갑자일');
  }
  
  // 요일별 특이사항
  const 요일명 = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()];
  if (요일명 === '일') {
    특이사항들.push('일요일');
  }
  
  return 특이사항들;
};

// 띠 동물 조회
export const get띠동물 = (jiji: string): string => {
  return 띠동물[jiji] || '미지';
};

// 오행 조회
export const get오행 = (cheongan: string): string => {
  return 오행매핑[cheongan] || '미지';
};

// 갑자 분해
export const split갑자 = (gapja: string): { 천간: string; 지지: string } => {
  if (gapja.length !== 2) {
    return { 천간: '미지', 지지: '미지' };
  }
  
  return {
    천간: gapja[0],
    지지: gapja[1]
  };
};

// 배치 계산 (월 전체)
export const calculateMonthGapja = async (year: number, month: number): Promise<Map<number, string>> => {
  const { getBatchGapjaHybrid } = await import('./atomicIntegration');
  return await getBatchGapjaHybrid(year, month, get60갑자Local);
};

// 유틸리티 함수들
export const getGapjaIndex = (gapja: string): number => {
  return 갑자60순환.indexOf(gapja);
};

export const getGapjaByIndex = (index: number): string => {
  const normalizedIndex = ((index % 60) + 60) % 60; // 음수 처리
  return 갑자60순환[normalizedIndex];
};

export const calculateDateOffset = (date1: Date, date2: Date): number => {
  return Math.floor((date2.getTime() - date1.getTime()) / (24 * 60 * 60 * 1000));
};

// 검증 함수들
export const validateDate = (year: number, month: number, day: number): boolean => {
  const date = new Date(year, month - 1, day);
  return date.getFullYear() === year && 
         date.getMonth() === month - 1 && 
         date.getDate() === day;
};

export const validateGapja = (gapja: string): boolean => {
  return gapja.length === 2 && 
         천간.includes(gapja[0]) && 
         지지.includes(gapja[1]) && 
         갑자60순환.includes(gapja);
};

// 테스트 함수
export const testCalculations = (): void => {
  console.log('🧪 사주 계산 함수 테스트 시작');
  
  const testDate = new Date(2025, 8, 9); // 2025년 9월 9일
  
  console.log('📅 테스트 날짜:', testDate);
  console.log('60갑자:', get60갑자Sync(testDate));
  console.log('년주:', get년주Sync(testDate));
  console.log('손없는날:', is손없는날(testDate));
  console.log('절기:', get절기(testDate));
  console.log('운세점수:', get운세점수(get60갑자Sync(testDate), testDate));
  console.log('특이사항:', get특이사항(testDate, get60갑자Sync(testDate)));
  
  console.log('✅ 사주 계산 함수 테스트 완료');
};

export default {
  get60갑자,
  get60갑자Sync,
  get년주,
  get년주Sync,
  get길흉,
  is손없는날,
  get절기,
  get운세점수,
  get특이사항,
  get띠동물,
  get오행,
  split갑자,
  calculateMonthGapja,
  testCalculations
};