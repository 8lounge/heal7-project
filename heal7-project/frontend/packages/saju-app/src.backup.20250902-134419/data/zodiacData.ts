// 12지신 띠운세 데이터 시스템

export interface ZodiacSign {
  id: string;
  name: string;
  chineseName: string;
  emoji: string;
  image: string;
  element: string;
  years: number[];
  characteristics: string[];
  personalityTraits: string[];
  suitableJobs: string[];
  luckyNumbers: number[];
  luckyColors: string[];
  compatibility: {
    best: string[];
    good: string[];
    challenging: string[];
  };
  fortune2025: {
    overall: string;
    career: string;
    love: string;
  };
  currentFortune: {
    overall: string;
    career: string;
    love: string;
    health: string;
    wealth: string;
  };
}

export interface YearFortune {
  year: number;
  zodiac: string;
  overview: string;
  luckyMonths: number[];
  caution: string;
}

// 출생년도로 띠 계산하는 함수
export const calculateZodiac = (year: number): string => {
  const zodiacCycle = [
    'rat', 'ox', 'tiger', 'rabbit', 'dragon', 'snake',
    'horse', 'sheep', 'monkey', 'rooster', 'dog', 'pig'
  ];
  
  // 1900년이 쥐띠 시작년도
  const baseYear = 1900;
  const cyclePosition = (year - baseYear) % 12;
  return zodiacCycle[cyclePosition];
};

// 현재 년도 기준으로 각 띠에 해당하는 연도 생성
const generateYears = (startIndex: number): number[] => {
  const years = [];
  const currentYear = new Date().getFullYear();
  
  // 현재 년도부터 과거로 가면서 해당 띠의 년도들을 찾기
  for (let year = 1900; year <= currentYear + 20; year++) {
    if ((year - 1900) % 12 === startIndex) {
      years.push(year);
    }
  }
  return years.sort((a, b) => b - a); // 내림차순 정렬 (최신년도 우선)
};

// 현재 년도에서 가장 가까운 해당 띠의 년도 구하기
export const getMostRecentZodiacYear = (zodiacId: string): number => {
  const currentYear = new Date().getFullYear();
  const zodiac = zodiacSigns.find(sign => sign.id === zodiacId);
  
  if (!zodiac) return currentYear;
  
  // 현재 년도부터 과거로 가면서 해당 띠 찾기
  for (let year = currentYear; year >= 1900; year--) {
    if (calculateZodiac(year) === zodiacId) {
      return year;
    }
  }
  
  return zodiac.years[0] || currentYear;
};

// 생년월일을 기준으로 띠 계산 (음력 고려)
export const calculateZodiacFromBirth = (year: number, month: number, day: number): string => {
  // 2월 4일 입춘 이전은 전년도 띠로 계산
  // 음력 새해는 보통 1월 말~2월 중순 사이이지만, 
  // 간단히 2월 4일(입춘) 기준으로 구분
  let adjustedYear = year;
  if (month === 1 || (month === 2 && day < 4)) {
    adjustedYear = year - 1;
  }
  
  return calculateZodiac(adjustedYear);
};

// 현재 사용자의 나이로부터 띠 추정
export const getZodiacFromAge = (age: number): string => {
  const currentYear = new Date().getFullYear();
  const birthYear = currentYear - age;
  return calculateZodiac(birthYear);
};

// 12지신 데이터
export const zodiacSigns: ZodiacSign[] = [
  {
    id: 'rat',
    name: '쥐띠',
    chineseName: '자(子)',
    emoji: '🐭',
    image: '/zodiac-images/rat.png',
    element: '물',
    years: generateYears(0),
    characteristics: [
      '재치 있고 상황 파악 및 변화에 빠릅니다',
      '혁신적인 아이디어 제공자, 상상력 풍부',
      '프로의식을 갖고 살며, 고개 숙이는 것을 좋아하지 않습니다',
      '온순하지만 불의를 보면 참지 못합니다'
    ],
    personalityTraits: [
      '자신의 행동을 인정하고 받아들이는 성향',
      '도움받기를 꺼려하며, 스스로 노력해 돈을 모으는 것을 좋아함',
      '겉은 강해 보이나 속은 민감',
      '천재적일 정도로 머리가 좋으며, 과학에 관심이 많음',
      '예술적 재능을 지님'
    ],
    suitableJobs: [
      '마케팅', '사업 경영', '컨설팅', '금융 및 투자',
      'IT 및 기술 개발', '교육 및 강연', '연구직'
    ],
    luckyNumbers: [1, 6, 8],
    luckyColors: ['파란색', '검은색', '흰색'],
    compatibility: {
      best: ['dragon', 'monkey'],
      good: ['ox', 'rabbit'],
      challenging: ['horse', 'rooster']
    },
    fortune2025: {
      overall: '2025년은 쥐띠에게 변화와 성장의 해입니다. 새로운 기회를 적극적으로 활용하세요.',
      career: '직장에서의 승진 기회가 있으며, 새로운 프로젝트를 통해 실력을 인정받을 것입니다.',
      love: '새로운 만남이나 기존 관계의 발전이 기대되는 한 해입니다.'
    },
    currentFortune: {
      overall: '새로운 기회가 많이 찾아오는 해입니다. 적극적인 도전 정신으로 성공을 거둘 수 있습니다.',
      career: '직장에서의 승진이나 새로운 프로젝트 기회가 있을 것입니다.',
      love: '새로운 만남이나 기존 관계의 발전이 기대됩니다.',
      health: '전반적으로 건강하지만 스트레스 관리가 중요합니다.',
      wealth: '투자나 부업을 통한 재물 증가가 예상됩니다.'
    }
  },
  {
    id: 'ox',
    name: '소띠',
    chineseName: '축(丑)',
    emoji: '🐂',
    image: '/zodiac-images/ox.png',
    element: '흙',
    years: generateYears(1),
    characteristics: [
      '우직하고 책임감 있으며 끈기와 인내심이 강합니다',
      '뜻이 웅대하여 권력자나 혁명가적 기질을 지녔습니다',
      '신뢰할 수 있는 실행자로, 자수성가 타입입니다',
      '신념과 원칙을 고수하며 성격이 강합니다'
    ],
    personalityTraits: [
      '정직하고 책임감 있으며 마음이 두텁고 현실을 중시',
      '현실적 사고방식으로 큰 뜻을 품고 권력자로 성장할 운',
      '팀의 귀감이 되며, 디테일에 강한 관리자형',
      '손재주가 좋고 자유로운 일에 적성이 맞음',
      '부동산에 관심이 많고 재물복이 있어 자신감이 큼'
    ],
    suitableJobs: [
      '회계', '재무 전문가', '엔지니어', '교육자',
      '행정 관리직', '연구원', '농업 분야'
    ],
    luckyNumbers: [2, 5, 9],
    luckyColors: ['노란색', '갈색', '주황색'],
    compatibility: {
      best: ['rat', 'snake', 'rooster'],
      good: ['rabbit', 'tiger'],
      challenging: ['sheep', 'horse', 'dog']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '꾸준한 노력이 결실을 맺는 해입니다. 인내심을 갖고 차근차근 진행하세요.',
      career: '성실함이 인정받아 안정적인 성과를 거둘 것입니다.',
      love: '진실한 마음으로 다가가면 좋은 결과가 있을 것입니다.',
      health: '규칙적인 생활과 운동으로 건강을 유지하세요.',
      wealth: '저축과 안정적인 투자로 재산을 늘려가세요.'
    }
  },
  {
    id: 'tiger',
    name: '호랑이띠',
    chineseName: '인(寅)',
    emoji: '🐅',
    image: '/zodiac-images/tiger.png',
    element: '나무',
    years: generateYears(2),
    characteristics: [
      '장남·장녀 운을 타고났습니다',
      '고고한 인품과 권세를 지녔으며, 늘 높은 이상을 꿈꿉니다',
      '형이상학적인 추리 능력과 동시에 과학적 지혜를 갖춘 사람입니다',
      '강력한 카리스마형으로, 용맹하고 타고난 지도자입니다'
    ],
    personalityTraits: [
      '자존심이 강하고 대담하며, 현실적 사고와 모험적 성향',
      '자기 위주의 사고방식, 창조적 직업에 어울리고 머리가 좋음',
      '법 없이도 살 수 있는 성격이지만 뒷마무리가 약함',
      '남의 도움 없이 스스로 새롭게 시작하는 자수성가형'
    ],
    suitableJobs: [
      '기업 경영', '지도력 역할', '창업 및 사업', '정치',
      '법률', '군인', '예술', '엔터테인먼트', '스포츠 분야'
    ],
    luckyNumbers: [1, 3, 7],
    luckyColors: ['초록색', '파란색', '검은색'],
    compatibility: {
      best: ['horse', 'dog'],
      good: ['dragon', 'pig'],
      challenging: ['monkey', 'snake']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '도전적인 기회들이 많이 생기는 해입니다. 용기를 갖고 추진하세요.',
      career: '리더십을 발휘할 수 있는 중요한 역할이 주어질 것입니다.',
      love: '적극적인 어프로치로 좋은 결과를 얻을 수 있습니다.',
      health: '활발한 활동으로 건강이 좋아질 것입니다.',
      wealth: '모험적 투자보다는 신중한 재정 관리가 필요합니다.'
    }
  },
  {
    id: 'rabbit',
    name: '토끼띠',
    chineseName: '묘(卯)',
    emoji: '🐰',
    image: '/zodiac-images/rabbit.png',
    element: '나무',
    years: generateYears(3),
    characteristics: [
      '친절하고 온순한 성격을 지녔습니다',
      '섬세하고 예민하지만 두뇌가 비상해 창의력이 뛰어납니다',
      '일처리에서 재치가 있어 남에게 이쁨 받고 인정받습니다',
      '마음이 착하고 여리지만 감정 기복이 심합니다'
    ],
    personalityTraits: [
      '신중하고 계획적으로 행동하며, 현실적인 목표를 중요시',
      '세심하고 꼼꼼하여 작은 부분까지 신경 쓰며 정확하게 일 처리',
      '창의적이고 예술적인 감각이 뛰어남',
      '중요한 결정 시 충분히 고민하고 신중한 접근'
    ],
    suitableJobs: [
      '예술 및 디자인 분야', '작가', '일러스트레이터',
      '금융', '재무', '회계', '세무', '심리학자',
      '서비스 매니저', '문학 및 광고 카피라이터'
    ],
    luckyNumbers: [3, 4, 9],
    luckyColors: ['초록색', '파란색', '검은색'],
    compatibility: {
      best: ['sheep', 'pig'],
      good: ['dog', 'ox'],
      challenging: ['rooster', 'dragon']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '평온하고 안정적인 한 해가 될 것입니다. 꾸준함이 힘이 됩니다.',
      career: '차근차근한 노력으로 인정받는 성과를 거둘 것입니다.',
      love: '따뜻한 마음과 배려로 관계가 깊어질 것입니다.',
      health: '스트레스 관리와 충분한 휴식이 중요합니다.',
      wealth: '안정적인 수입과 절약으로 재정이 안정될 것입니다.'
    }
  },
  {
    id: 'dragon',
    name: '용띠',
    chineseName: '진(辰)',
    emoji: '🐲',
    image: '/zodiac-images/dragon.png',
    element: '흙',
    years: generateYears(4),
    characteristics: [
      '강력한 카리스마와 자신감을 지녔습니다',
      '사람들의 주목을 받는 것을 즐기며 어려운 상황에서도 앞장섭니다',
      '자존심이 강해 자기 능력과 도전을 과시하는 경향',
      '창의적이고 상상력이 풍부하며 예술적 감각이 뛰어납니다'
    ],
    personalityTraits: [
      '새로운 아이디어와 혁신을 추구하고, 높은 목표를 설정',
      '도덕적이고 정직한 성격으로 거짓말을 싫어함',
      '열정적이고 활력이 넘치며 목표를 향해 끊임없이 노력',
      '큰 그릇의 운명을 지녔으며, 영리하고 높은 자리에 앉는 기질'
    ],
    suitableJobs: [
      '관리직', '경영자', '조직의 리더 역할', '예술 분야',
      '글쓰기', '광고 등 창의적인 분야', '연구직', '정보통신',
      '법조계', '아티스트', '교수', '강사', '스포츠 코치'
    ],
    luckyNumbers: [1, 6, 7],
    luckyColors: ['금색', '은색', '흰색'],
    compatibility: {
      best: ['rat', 'monkey', 'rooster'],
      good: ['tiger', 'snake'],
      challenging: ['dog', 'rabbit']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '큰 성과를 이룰 수 있는 해입니다. 자신감을 갖고 도전하세요.',
      career: '리더십과 창의성이 빛을 발하는 시기입니다.',
      love: '화려하고 로맨틱한 만남이 기대됩니다.',
      health: '에너지가 넘치지만 과로에 주의하세요.',
      wealth: '큰 수익 기회가 있지만 신중한 판단이 필요합니다.'
    }
  },
  {
    id: 'snake',
    name: '뱀띠',
    chineseName: '사(巳)',
    emoji: '🐍',
    image: '/zodiac-images/snake.png',
    element: '불',
    years: generateYears(5),
    characteristics: [
      '총명하고 통찰력이 있어 문제 해결 능력이 우수합니다',
      '신비롭고 매력적인 성격으로 주변의 관심을 받습니다',
      '감정 표현이 서툴러 자신의 감정을 잘 드러내지 않습니다',
      '강한 독립심을 지녔습니다'
    ],
    personalityTraits: [
      '호기심이 많고 새로운 것에 대한 탐구심이 강함',
      '끈기와 인내심이 돋보여 시작한 일을 끝까지 마무리',
      '조용하고 내성적인 성격으로 사색적',
      '현실적이고 분석적인 성향으로 뛰어난 판단력'
    ],
    suitableJobs: [
      '학자 (과학/철학)', '심리학자', '의사 및 한의사',
      '법조인', '예술가', '디자인 분야', '금융 분석가',
      '작가 / 저널리스트', 'IT 전문가 / 프로그래머',
      '비즈니스 전략가 / 컨설턴트'
    ],
    luckyNumbers: [2, 8, 9],
    luckyColors: ['빨간색', '노란색', '검은색'],
    compatibility: {
      best: ['ox', 'rooster'],
      good: ['dragon', 'dog'],
      challenging: ['tiger', 'pig']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '지혜와 통찰력이 빛나는 해입니다. 신중한 판단으로 성공하세요.',
      career: '전문성이 인정받아 중요한 역할을 맡게 될 것입니다.',
      love: '깊이 있는 관계를 추구하게 될 것입니다.',
      health: '정신적 스트레스 관리가 중요합니다.',
      wealth: '분석적 사고로 현명한 투자 결정을 내릴 것입니다.'
    }
  },
  {
    id: 'horse',
    name: '말띠',
    chineseName: '오(午)',
    emoji: '🐎',
    image: '/zodiac-images/horse.png',
    element: '불',
    years: generateYears(6),
    characteristics: [
      '활동적이고 활발한 성격으로 다양한 활동을 즐깁니다',
      '긍정적이고 밝은 성격으로 주변 사람들을 즐겁게 합니다',
      '사교적이고 친화력이 뛰어나 여러 사람들과 어울리기를 좋아합니다',
      '독립심이 강해 남의 도움보다는 스스로 문제를 해결하려 합니다'
    ],
    personalityTraits: [
      '솔직하고 직설적이어서 자신의 의견을 분명히 표현',
      '긍정적인 사고방식으로 어려운 상황에서도 희망을 잃지 않음',
      '적극적이고 새로운 경험을 추구하며 도전적인 정신',
      '자유롭고 개성이 강하며, 자신만의 생각과 방식을 중시'
    ],
    suitableJobs: [
      '영업 / 마케팅', '여행사', '공연 예술가',
      '스포츠 트레이너', '이벤트 기획자', '창업 / 사업가',
      '교육자 / 강사', '광고 전문가'
    ],
    luckyNumbers: [2, 3, 7],
    luckyColors: ['빨간색', '초록색', '보라색'],
    compatibility: {
      best: ['tiger', 'sheep', 'dog'],
      good: ['rabbit', 'dragon'],
      challenging: ['rat', 'ox']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '활발한 활동과 새로운 경험이 가득한 해가 될 것입니다.',
      career: '적극성과 추진력으로 좋은 성과를 거둘 것입니다.',
      love: '자유로운 연애나 새로운 만남이 기대됩니다.',
      health: '활동적인 라이프스타일로 건강이 좋아질 것입니다.',
      wealth: '다양한 수입원을 통해 재정이 늘어날 것입니다.'
    }
  },
  {
    id: 'sheep',
    name: '양띠',
    chineseName: '미(未)',
    emoji: '🐑',
    image: '/zodiac-images/sheep.png',
    element: '흙',
    years: generateYears(7),
    characteristics: [
      '따뜻하고 다정다감한 성격으로 주변 사람들을 편안하게 해줍니다',
      '사교적이고 친화적이어서 다양한 사람들과 어울리기를 좋아합니다',
      '감수성이 풍부해 예술과 음악에 대한 감각이 좋습니다',
      '순진하고 어리숙한 면이 있어 때로는 속을 잘 드러냅니다'
    ],
    personalityTraits: [
      '안정적이고 평화로운 환경을 선호하며 불안정한 상황을 싫어함',
      '다른 사람의 말을 잘 듣고 이해하려는 노력으로 좋은 상담자',
      '인내심이 강해 어려운 상황에서도 포기하지 않고 꾸준히 노력',
      '공감 능력이 뛰어나 다른 사람들을 잘 배려'
    ],
    suitableJobs: [
      '예술가/디자이너', '상담사/심리학자', '사회복지사',
      '간호사/의료분야', '작가/편집자', '인사(HR) 관리자',
      '비영리 단체 활동가'
    ],
    luckyNumbers: [2, 7, 8],
    luckyColors: ['초록색', '빨간색', '보라색'],
    compatibility: {
      best: ['rabbit', 'horse', 'pig'],
      good: ['monkey', 'rooster'],
      challenging: ['ox', 'dog']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '온화하고 평화로운 한 해가 될 것입니다. 협력이 중요합니다.',
      career: '팀워크를 통해 좋은 성과를 거둘 것입니다.',
      love: '따뜻하고 안정적인 관계가 발전할 것입니다.',
      health: '마음의 평화를 찾으면 건강도 좋아질 것입니다.',
      wealth: '꾸준한 저축과 안정적인 투자로 재산을 모으세요.'
    }
  },
  {
    id: 'monkey',
    name: '원숭이띠',
    chineseName: '신(申)',
    emoji: '🐵',
    image: '/zodiac-images/monkey.png',
    element: '금',
    years: generateYears(8),
    characteristics: [
      '영리하고 재치 있는 성격으로 주변 사람들에게 웃음을 선사합니다',
      '낙천적이고 긍정적인 태도로 삶을 즐깁니다',
      '사교적이고 친화력이 뛰어나 다양한 사람들과 어울리기를 좋아합니다',
      '호기심이 많고 변화를 추구하는 성향입니다'
    ],
    personalityTraits: [
      '새로운 지식 습득에 열정적',
      '다양한 분야에 관심을 가지고 탐구',
      '변화에 유연하게 대처하는 능력',
      '독립적이고 자율적인 성향이 강해 스스로 문제를 해결'
    ],
    suitableJobs: [
      '창의적 기획자 / 아이디어 발굴가', '연구원 / 개발자',
      '마케팅 / 광고 전문가', '방송 / 엔터테인먼트 분야',
      '여행 / 문화 기획자', '교육자 / 강사', '창업가 / 컨설턴트'
    ],
    luckyNumbers: [1, 7, 8],
    luckyColors: ['금색', '흰색', '파란색'],
    compatibility: {
      best: ['rat', 'dragon'],
      good: ['sheep', 'dog'],
      challenging: ['tiger', 'pig']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '영리함과 재치로 많은 기회를 만들어내는 해입니다.',
      career: '창의적 아이디어로 주목받는 성과를 거둘 것입니다.',
      love: '유머와 매력으로 좋은 인연을 만날 것입니다.',
      health: '활발한 활동으로 건강이 좋아질 것입니다.',
      wealth: '다양한 방법으로 수입을 늘릴 기회가 있습니다.'
    }
  },
  {
    id: 'rooster',
    name: '닭띠',
    chineseName: '유(酉)',
    emoji: '🐓',
    image: '/zodiac-images/rooster.png',
    element: '금',
    years: generateYears(9),
    characteristics: [
      '명랑한 성격으로 주변 사람들과 잘 어울립니다',
      '지적 능력이 뛰어나 문제 해결에 탁월합니다',
      '목표 달성을 위해 노력하는 성향이 강합니다',
      '책임감이 있어 맡은 일을 철저히 수행합니다'
    ],
    personalityTraits: [
      '독립적으로 일을 처리하려는 경향',
      '자신의 의견이나 신념에 대해 확고한 태도',
      '근면하고 신중한 성격으로 계획적이고 조직적인 일 처리',
      '협력과 팀 워크를 중요시하며, 다양한 사람들과의 교류를 즐김'
    ],
    suitableJobs: [
      '회계사/재무 분석가', '법률 분야', '교사/교육자',
      '연구원/과학자', '경영자/관리자', '기술 전문가',
      '디자이너/예술가', '언론인/기자', '행정직/공무원'
    ],
    luckyNumbers: [5, 7, 8],
    luckyColors: ['금색', '노란색', '갈색'],
    compatibility: {
      best: ['ox', 'snake', 'dragon'],
      good: ['tiger', 'horse'],
      challenging: ['rabbit', 'dog']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '계획적인 접근으로 확실한 성과를 거두는 해입니다.',
      career: '전문성과 책임감으로 인정받는 위치에 오를 것입니다.',
      love: '진실된 마음으로 안정적인 관계를 만들어갈 것입니다.',
      health: '규칙적인 생활 패턴이 건강에 도움이 될 것입니다.',
      wealth: '체계적인 재정 관리로 안정적인 자산을 형성할 것입니다.'
    }
  },
  {
    id: 'dog',
    name: '개띠',
    chineseName: '술(戌)',
    emoji: '🐕',
    image: '/zodiac-images/dog.png',
    element: '흙',
    years: generateYears(10),
    characteristics: [
      '의리 있는 성격으로 주변 사람들을 위해 헌신합니다',
      '솔직하고 정직해 거짓말을 하지 않습니다',
      '열정적이고 적극적인 목표 달성을 위해 노력합니다',
      '책임감이 강해 맡은 일을 철저히 수행합니다'
    ],
    personalityTraits: [
      '충성심이 깊고 성실한 성향',
      '신중하게 결정을 내리고 일을 철저히 추진하여 성과를 냄',
      '차분하고 안정적인 성향으로 감정적으로 균형을 유지',
      '어떠한 상황에서도 평정을 잃지 않고 문제를 해결하는 능력'
    ],
    suitableJobs: [
      '사회복지사/상담사', '경찰/소방관', '변호사/법률 전문가',
      '의사/간호사', '교육자', '인사(HR) 관리자',
      '동물 관련 직업', '비영리 단체 활동가'
    ],
    luckyNumbers: [3, 4, 9],
    luckyColors: ['빨간색', '초록색', '보라색'],
    compatibility: {
      best: ['tiger', 'rabbit', 'horse'],
      good: ['snake', 'monkey'],
      challenging: ['dragon', 'sheep', 'rooster']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '성실함과 의리가 인정받는 의미 있는 해가 될 것입니다.',
      career: '신뢰를 바탕으로 중요한 역할을 맡게 될 것입니다.',
      love: '진실한 마음으로 깊은 관계를 만들어갈 것입니다.',
      health: '꾸준한 건강 관리로 좋은 컨디션을 유지할 것입니다.',
      wealth: '성실한 노력으로 안정적인 수입을 얻을 것입니다.'
    }
  },
  {
    id: 'pig',
    name: '돼지띠',
    chineseName: '해(亥)',
    emoji: '🐷',
    image: '/zodiac-images/pig.png',
    element: '물',
    years: generateYears(11),
    characteristics: [
      '온순하고 친절한 성격으로 주변 사람들을 배려하고 도와줍니다',
      '낙천적이고 유머러스해 주변을 즐겁게 합니다',
      '관대한 태도로 사람들을 아끼고 사랑합니다',
      '현실적이고 실용적인 성격으로 현실에 충실합니다'
    ],
    personalityTraits: [
      '긍정적인 사고방식으로 어려운 상황에서도 낙관적으로 대처',
      '솔직하고 정직해 대인 관계에서 신뢰를 얻기 쉬움',
      '목표 달성을 위해 끈기 있게 노력하는 성향',
      '물질적 풍요와 즐거움을 추구하는 경향'
    ],
    suitableJobs: [
      '의사/간호사', '교육자', '사회복지사/상담사',
      '요리사/바리스타', '인사(HR) 관리자', '금융/회계',
      '예술가/디자이너', '비영리 단체 활동가', '부동산/자산 관리'
    ],
    luckyNumbers: [2, 5, 8],
    luckyColors: ['노란색', '회색', '갈색', '금색'],
    compatibility: {
      best: ['rabbit', 'sheep', 'tiger'],
      good: ['rat', 'ox'],
      challenging: ['snake', 'monkey']
    },
    fortune2025: {
      overall: "2025년 운세 내용",
      career: "2025년 직업운 내용", 
      love: "2025년 연애운 내용"
    },
    currentFortune: {
      overall: '풍요롭고 즐거운 한 해가 될 것입니다. 관계에 집중하세요.',
      career: '협력과 화합으로 큰 성과를 거둘 것입니다.',
      love: '따뜻한 마음으로 행복한 관계를 만들어갈 것입니다.',
      health: '즐거운 마음으로 건강을 유지할 것입니다.',
      wealth: '여유로운 생활과 함께 재정도 안정될 것입니다.'
    }
  }
];

// 띠별 월별 운세
export const monthlyFortunes: { [key: string]: { [key: number]: string } } = {
  rat: {
    1: '새해 새로운 시작에 좋은 기운이 감돕니다.',
    2: '인간관계에서 좋은 만남이 있을 것입니다.',
    3: '직장에서의 변화나 승진 기회가 있습니다.',
    // ... 나머지 월들
  },
  // ... 다른 띠들의 월별 운세
};

// 띠 호환성 체크 함수
export const checkCompatibility = (zodiac1: string, zodiac2: string): string => {
  const sign1 = zodiacSigns.find(sign => sign.id === zodiac1);
  const sign2 = zodiacSigns.find(sign => sign.id === zodiac2);
  
  if (!sign1 || !sign2) return '알 수 없음';
  
  if (sign1.compatibility.best.includes(zodiac2)) return '매우 좋음';
  if (sign1.compatibility.good.includes(zodiac2)) return '좋음';
  if (sign1.compatibility.challenging.includes(zodiac2)) return '주의 필요';
  
  return '보통';
};

// 현재 연도 기준 운세 가져오기
export const getCurrentYearFortune = (zodiacId: string) => {
  const zodiac = zodiacSigns.find(sign => sign.id === zodiacId);
  return zodiac ? zodiac.currentFortune : null;
};

export default {
  zodiacSigns,
  calculateZodiac,
  checkCompatibility,
  getCurrentYearFortune,
  monthlyFortunes
};