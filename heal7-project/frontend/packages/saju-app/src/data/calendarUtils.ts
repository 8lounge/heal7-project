/**
 * 캘린더 유틸리티 함수 모듈 - 부가 기능들
 * ===========================================
 * 
 * 절기, 운세, 길흉, 손없는날 등 캘린더 보조 기능들
 * - 24절기 계산 및 아이콘
 * - 운세 점수 계산
 * - 길흉 판정
 * - 특이사항 계산
 */

// 🔥 중복 제거: 상수는 sajuConstants.ts에서 import
import { 갑자60순환, 손없는날기준, 절기매핑, 운세점수기준, 오행매핑 } from './sajuConstants';

// 절기 데이터 타입 정의
export interface SolarTermData {
  name: string;
  date: string;
  year: number;
  month: number;
  day: number;
  description: string;
}

// 절기 아이콘 매핑
export const 절기아이콘매핑: Record<string, { icon: string; color: string; description: string; season: string }> = {
  '입춘': { icon: '🌱', color: '#22c55e', description: '봄의 시작', season: '봄' },
  '우수': { icon: '💧', color: '#3b82f6', description: '눈과 비가 내림', season: '봄' },
  '경칩': { icon: '🐛', color: '#84cc16', description: '벌레들이 깨어남', season: '봄' },
  '춘분': { icon: '⚖️', color: '#10b981', description: '밤낮이 같아짐', season: '봄' },
  '청명': { icon: '🌸', color: '#f59e0b', description: '하늘이 맑고 밝음', season: '봄' },
  '곡우': { icon: '🌾', color: '#8b5cf6', description: '곡식에 단비', season: '봄' },
  '입하': { icon: '☀️', color: '#f97316', description: '여름의 시작', season: '여름' },
  '소만': { icon: '🌿', color: '#059669', description: '만물이 점차 자람', season: '여름' },
  '망종': { icon: '🌾', color: '#ca8a04', description: '씨 뿌리고 거두는 때', season: '여름' },
  '하지': { icon: '🌞', color: '#dc2626', description: '낮이 가장 긴 날', season: '여름' },
  '소서': { icon: '🔥', color: '#ea580c', description: '더위가 시작됨', season: '여름' },
  '대서': { icon: '🌡️', color: '#b91c1c', description: '가장 더운 때', season: '여름' },
  '입추': { icon: '🍂', color: '#d97706', description: '가을의 시작', season: '가을' },
  '처서': { icon: '🌬️', color: '#0891b2', description: '더위가 그침', season: '가을' },
  '백로': { icon: '☁️', color: '#64748b', description: '흰 이슬이 내림', season: '가을' },
  '추분': { icon: '🌕', color: '#7c3aed', description: '밤낮이 같아짐', season: '가을' },
  '한로': { icon: '❄️', color: '#0284c7', description: '찬 이슬이 내림', season: '가을' },
  '상강': { icon: '🧊', color: '#1e40af', description: '서리가 내림', season: '가을' },
  '입동': { icon: '🌨️', color: '#475569', description: '겨울의 시작', season: '겨울' },
  '소설': { icon: '❄️', color: '#334155', description: '눈이 내리기 시작', season: '겨울' },
  '대설': { icon: '☃️', color: '#1e293b', description: '큰 눈이 내림', season: '겨울' },
  '동지': { icon: '🌑', color: '#0f172a', description: '밤이 가장 긴 날', season: '겨울' },
  '소한': { icon: '🧊', color: '#1e40af', description: '추위가 시작됨', season: '겨울' },
  '대한': { icon: '🥶', color: '#1e3a8a', description: '가장 추운 때', season: '겨울' }
};

// 절기 관련 함수들
export const get절기 = (date: Date): string | null => {
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  // 현재 날짜와 가장 가까운 절기 찾기 (±2일 범위)
  let 가장가까운절기 = null;
  let 최소차이 = 3; // 2일 초과하면 null 반환
  
  Object.entries(절기매핑).forEach(([절기명, { month: 절기월, day: 절기일 }]) => {
    if (month === 절기월) {
      const 차이 = Math.abs(day - 절기일);
      if (차이 <= 최소차이) {
        최소차이 = 차이;
        가장가까운절기 = 절기명;
      }
    }
  });
  
  return 가장가까운절기;
};

export const get절기상세정보 = (date: Date): { 
  절기이름: string | null; 
  아이콘: string; 
  색상: string; 
  설명: string; 
  계절: string;
  절기여부: boolean;
} => {
  const 절기이름 = get절기(date);
  
  if (절기이름 && 절기아이콘매핑[절기이름]) {
    const 정보 = 절기아이콘매핑[절기이름];
    return {
      절기이름,
      아이콘: 정보.icon,
      색상: 정보.color,
      설명: 정보.description,
      계절: 정보.season,
      절기여부: true
    };
  }
  
  return {
    절기이름: null,
    아이콘: '',
    색상: '#6b7280',
    설명: '',
    계절: '',
    절기여부: false
  };
};

export const is절기날 = (date: Date): boolean => {
  return get절기(date) !== null;
};

export const get절기운세보정 = (절기이름: string | null): number => {
  if (!절기이름) return 0;
  
  // 절기별 운세 보정값
  const 절기보정값: Record<string, number> = {
    '입춘': 1.5, '입하': 1.2, '입추': 1.0, '입동': 0.8,
    '춘분': 1.3, '하지': 1.1, '추분': 0.9, '동지': 0.7,
    '경칩': 1.1, '소만': 1.0, '백로': 0.8, '소설': 0.6
  };
  
  return 절기보정값[절기이름] || 0.5;
};

// 손없는날 판정
export const is손없는날 = (date: Date): boolean => {
  const month = date.getMonth() + 1; // 1-12월
  const day = date.getDate();
  
  const 해당월손없는날 = 손없는날기준[month as keyof typeof 손없는날기준];
  return 해당월손없는날 ? 해당월손없는날.includes(day) : false;
};

// 길흉 판정 함수 (간단한 로직)
export const get길흉 = (gapja: string, date: Date): { 길일: boolean; 흉일: boolean } => {
  if (gapja.length !== 2) {
    return { 길일: false, 흉일: false };
  }
  
  const 천간 = gapja[0];
  const 지지 = gapja[1];
  const 요일 = date.getDay(); // 0=일요일, 1=월요일, ...
  
  // 기본 길흉 판정 (예시 - 실제로는 더 복잡한 계산 필요)
  const 길일여부 = (천간 === '갑' && 지지 === '자') || 
                 (천간 === '을' && 지지 === '축') ||
                 (요일 === 0 || 요일 === 6) || // 주말은 길일
                 is손없는날(date); // 손없는날은 길일
  
  const 흉일여부 = (천간 === '무' && 지지 === '신') ||
                 (천간 === '기' && 지지 === '유') ||
                 (요일 === 2 || 요일 === 4); // 화,목요일은 흉일
  
  return {
    길일: 길일여부 && !흉일여부, // 흉일이면 길일 무효
    흉일: 흉일여부
  };
};

// 운세 점수 계산
export const get운세점수 = (gapja: string, date: Date): number => {
  // 기본 점수
  let 점수 = 3; // 보통
  
  if (gapja.length !== 2) return 점수;
  
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
  const 절기이름 = get절기(date);
  if (절기이름) {
    점수 += get절기운세보정(절기이름);
  }
  
  // 길흉 판정 반영
  const { 길일, 흉일 } = get길흉(gapja, date);
  if (길일) 점수 += 1;
  if (흉일) 점수 -= 1;
  
  // 1-5 범위로 제한
  return Math.max(1, Math.min(5, Math.floor(점수)));
};

// 특이사항 판정
export const get특이사항 = (date: Date, gapja: string, isLeapMonth?: boolean): string[] => {
  try {
    const 특이사항들: string[] = [];
    
    // 매개변수 검증
    if (!date || !gapja) {
      return [];
    }
    
    // 손없는날
    try {
      if (is손없는날 && is손없는날(date)) {
        특이사항들.push('손없는날');
      }
    } catch (error) {
      console.warn('손없는날 계산 오류:', error);
    }
    
    // 길일/흉일
    try {
      const 길흉결과 = get길흉(gapja, date) || { 길일: false, 흉일: false };
      const { 길일, 흉일 } = 길흉결과;
      if (길일) 특이사항들.push('길일');
      if (흉일) 특이사항들.push('흉일');
    } catch (error) {
      console.warn('길흉 계산 오류:', error);
    }
    
    // 절기
    try {
      const 절기 = get절기(date);
      if (절기) {
        특이사항들.push(`${절기}`);
      }
    } catch (error) {
      console.warn('절기 계산 오류:', error);
    }
    
    // 윤달
    if (isLeapMonth) {
      특이사항들.push('윤달');
    }
    
    // 특별한 갑자 조합
    if (gapja === '갑자') {
      특이사항들.push('갑자일');
    } else if (gapja === '경신') {
      특이사항들.push('경신일');
    }
    
    // 요일별 특이사항 (방어적 코딩)
    try {
      const 요일명배열 = ['일', '월', '화', '수', '목', '금', '토'];
      const 요일인덱스 = date.getDay();
      const 요일명 = 요일명배열[요일인덱스];
      if (요일명 === '일') {
        특이사항들.push('일요일');
      }
    } catch (error) {
      console.warn('요일 계산 오류:', error);
    }
    
    return Array.isArray(특이사항들) ? 특이사항들 : [];
  } catch (error) {
    console.warn('get특이사항 전체 오류:', error);
    return [];
  }
};

// 띠 동물 조회 (sajuConstants.ts에서 이미 정의됨, 여기서는 유틸리티 함수만)
export const get띠동물설명 = (jiji: string): { 
  동물: string; 
  특성: string[]; 
  색상: string; 
  길일: number[];
} => {
  const 띠정보: Record<string, { 동물: string; 특성: string[]; 색상: string; 길일: number[] }> = {
    '자': { 동물: '쥐', 특성: ['민첩', '영리', '적응력'], 색상: '#6366f1', 길일: [1, 9, 17, 25] },
    '축': { 동물: '소', 특성: ['성실', '근면', '인내'], 색상: '#8b5cf6', 길일: [2, 10, 18, 26] },
    '인': { 동물: '호랑이', 특성: ['용맹', '정의', '리더십'], 색상: '#f59e0b', 길일: [3, 11, 19, 27] },
    '묘': { 동물: '토끼', 특성: ['온화', '친화력', '예술감각'], 색상: '#10b981', 길일: [4, 12, 20, 28] },
    '진': { 동물: '용', 특성: ['권위', '창조력', '변화'], 색상: '#dc2626', 길일: [5, 13, 21, 29] },
    '사': { 동물: '뱀', 특성: ['지혜', '직관', '신중'], 색상: '#059669', 길일: [6, 14, 22, 30] },
    '오': { 동물: '말', 특성: ['활동적', '자유', '열정'], 색상: '#ea580c', 길일: [7, 15, 23, 31] },
    '미': { 동물: '양', 특성: ['온순', '협력', '평화'], 색상: '#84cc16', 길일: [8, 16, 24] },
    '신': { 동물: '원숭이', 특성: ['재치', '유머', '다재다능'], 색상: '#f97316', 길일: [1, 9, 17, 25] },
    '유': { 동물: '닭', 특성: ['정확', '계획성', '책임감'], 색상: '#eab308', 길일: [2, 10, 18, 26] },
    '술': { 동물: '개', 특성: ['충성', '정직', '보호'], 색상: '#64748b', 길일: [3, 11, 19, 27] },
    '해': { 동물: '돼지', 특성: ['관용', '풍요', '행복'], 색상: '#ec4899', 길일: [4, 12, 20, 28] }
  };
  
  return 띠정보[jiji] || { 동물: '미지', 특성: [], 색상: '#6b7280', 길일: [] };
};

// 유틸리티 함수들
export const formatKoreanDate = (date: Date): string => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const 요일명 = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()];
  
  return `${year}년 ${month}월 ${day}일 (${요일명})`;
};

export const getSeasonByMonth = (month: number): string => {
  if (month >= 3 && month <= 5) return '봄';
  if (month >= 6 && month <= 8) return '여름'; 
  if (month >= 9 && month <= 11) return '가을';
  return '겨울';
};

export const getDayColor = (gapja: string, 점수: number): string => {
  // 갑자에 따른 기본 색상
  const 갑자색상: Record<string, string> = {
    '갑자': '#22c55e', '을축': '#3b82f6', '병인': '#f59e0b',
    '정묘': '#10b981', '무진': '#8b5cf6', '기사': '#f97316'
  };
  
  const 기본색상 = 갑자색상[gapja] || '#6b7280';
  
  // 점수에 따른 투명도 조절
  const 투명도 = Math.max(0.3, 점수 / 5);
  
  return `${기본색상}${Math.floor(투명도 * 255).toString(16).padStart(2, '0')}`;
};

export default {
  // 절기 관련
  get절기,
  get절기상세정보, 
  is절기날,
  get절기운세보정,
  절기아이콘매핑,
  
  // 운세 관련
  get운세점수,
  get특이사항,
  get길흉,
  
  // 유틸리티
  is손없는날,
  get띠동물설명,
  formatKoreanDate,
  getSeasonByMonth,
  getDayColor
};