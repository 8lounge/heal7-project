// 운세 캘린더 데이터 시스템

export interface CalendarDate {
  date: Date;
  lunarDate: string;
  gapja: string;
  zodiac: string;
  element: string;
  sonEobNeunNal: boolean; // 손없는날
  gilil: boolean; // 길일
  흉일: boolean; // 흉일
  절기: string | null;
  운세점수: number; // 1-5
  특이사항: string[];
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

// 60갑자 계산 함수
export const get60갑자 = (date: Date): string => {
  // 기준일: 2024년 1월 1일 = 갑진일
  const 기준일 = new Date(2024, 0, 1);
  const 기준갑자인덱스 = 40; // 갑진의 인덱스 (갑이 0일 때)
  
  const 날짜차이 = Math.floor((date.getTime() - 기준일.getTime()) / (24 * 60 * 60 * 1000));
  const 갑자인덱스 = (기준갑자인덱스 + 날짜차이) % 60;
  
  const 천간인덱스 = 갑자인덱스 % 10;
  const 지지인덱스 = 갑자인덱스 % 12;
  
  return 천간[천간인덱스] + 지지[지지인덱스];
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

// 캘린더 데이터 생성
export const generateCalendarMonth = (year: number, month: number): CalendarDate[] => {
  const daysInMonth = new Date(year, month, 0).getDate();
  const calendarDates: CalendarDate[] = [];
  
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month - 1, day);
    const gapja = get60갑자(date);
    const 천간 = gapja[0];
    const 지지 = gapja[1];
    const 띠 = 띠동물[지지];
    const 오행 = 오행매핑[천간];
    const { 길일, 흉일 } = get길흉(gapja, date);
    const 손없는날 = is손없는날(date);
    const 절기 = get절기(date);
    const 운세점수 = get운세점수(gapja, date);
    const 특이사항 = get특이사항(date, gapja);
    
    calendarDates.push({
      date,
      lunarDate: `음력 ${month}월 ${day}일`, // 실제로는 음력 계산 필요
      gapja,
      zodiac: 띠,
      element: 오행,
      sonEobNeunNal: 손없는날,
      gilil: 길일,
      흉일,
      절기,
      운세점수,
      특이사항
    });
  }
  
  return calendarDates;
};

// 월별 운세 메시지 생성
export const getMonthlyFortune = (year: number, month: number): MonthlyFortune => {
  const dates = generateCalendarMonth(year, month);
  
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
export const getTodayFortune = (): CalendarDate => {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const day = today.getDate();
  
  const monthData = generateCalendarMonth(year, month);
  return monthData.find(d => d.date.getDate() === day) || monthData[0];
};

export default {
  generateCalendarMonth,
  getMonthlyFortune,
  getTodayFortune,
  get60갑자,
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