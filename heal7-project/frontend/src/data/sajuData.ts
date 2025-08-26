// MZ세대 맞춤 사주 데이터

export interface SajuElement {
  element: '목' | '화' | '토' | '금' | '수'
  polarity: '양' | '음'
  animal: string
  description: string
  personality: string[]
  strengths: string[]
  weaknesses: string[]
  modernInterpretation: string
  mbtiConnection: string[]
  careerFit: string[]
  loveStyle: string
  moneyLuck: string
  healthTip: string
}

export interface SajuCompatibility {
  element1: string
  element2: string
  compatibility: number // 1-5
  description: string
  advice: string
}

export interface ModernSajuResult {
  birthInfo: {
    year: number
    month: number
    day: number
    hour: number
    gender: 'M' | 'F'
  }
  fourPillars: {
    year: { stem: string; branch: string; element: string }
    month: { stem: string; branch: string; element: string }
    day: { stem: string; branch: string; element: string }
    hour: { stem: string; branch: string; element: string }
  }
  dominantElement: string
  personality: {
    type: string
    description: string
    keywords: string[]
    mbtiLikely: string[]
    strengthsModern: string[]
    improvementAreas: string[]
  }
  lifeAspects: {
    love: {
      style: string
      compatibility: string[]
      advice: string
      idealType: string
    }
    career: {
      suitableJobs: string[]
      workStyle: string
      leadershipStyle: string
      advice: string
    }
    money: {
      style: string
      luckyPeriod: string
      investmentTip: string
      cautionPeriod: string
    }
    health: {
      careAreas: string[]
      recommendedExercise: string
      stressManagement: string
      supplementTip: string
    }
  }
  yearlyFortune: {
    [year: number]: {
      overall: number // 1-5
      love: number
      career: number
      money: number
      health: number
      keywords: string[]
      monthlyHighlights: { month: number; description: string }[]
    }
  }
  mzSummary: {
    oneLineDescription: string
    emoji: string
    hashTags: string[]
    shareableQuote: string
    trendKeyword: string
  }
}

// 오행별 현대적 해석
export const sajuElements: Record<string, SajuElement> = {
  '목': {
    element: '목',
    polarity: '양',
    animal: '🌳',
    description: '성장하는 나무처럼 끊임없이 발전하는 성격',
    personality: ['창의적', '진취적', '성장지향', '유연함', '리더십'],
    strengths: ['새로운 아이디어 생성', '적응력', '성장 잠재력', '창의성', '리더십'],
    weaknesses: ['급한 성격', '인내심 부족', '완벽주의', '스트레스에 민감'],
    modernInterpretation: '스타트업 창업이나 크리에이티브 분야에서 빛을 발하는 타입! SNS 인플루언서나 콘텐츠 크리에이터로도 성공 가능성 높음.',
    mbtiConnection: ['ENFP', 'ENTP', 'ENFJ'],
    careerFit: ['콘텐츠 크리에이터', '마케터', '디자이너', '스타트업 CEO', '컨설턴트', 'UX/UI 디자이너'],
    loveStyle: '썸 타는 걸 즐기는 스타일. 새로운 사람과의 만남을 좋아하고 로맨틱한 분위기 조성에 능함.',
    moneyLuck: '투자보다는 창업이나 사업으로 돈 벌 확률 높음. 부동산보다는 주식이나 코인 투자가 맞을 수도.',
    healthTip: '스트레스성 질환 주의. 요가나 명상으로 마음의 안정 찾기 추천.'
  },
  '화': {
    element: '화',
    polarity: '양',
    animal: '🔥',
    description: '불꽃처럼 열정적이고 에너지가 넘치는 성격',
    personality: ['열정적', '활동적', '사교적', '표현력 풍부', '감정적'],
    strengths: ['추진력', '카리스마', '소통능력', '열정', '에너지'],
    weaknesses: ['성급함', '감정기복', '충동적', '인내심 부족'],
    modernInterpretation: '인플루언서나 연예계 쪽에서 두각을 나타낼 수 있는 타입! 라이브 방송이나 이벤트 기획 같은 일에도 잘 어울림.',
    mbtiConnection: ['ESFP', 'ESTP', 'ENFP'],
    careerFit: ['유튜버/스트리머', '이벤트 기획자', '영업/마케팅', '방송인', '연예계', 'PR 전문가'],
    loveStyle: '직진하는 스타일. 좋아하면 바로 표현하고 열정적으로 사랑함. 드라마틱한 연애 선호.',
    moneyLuck: '돈을 빨리 벌지만 빨리 쓰는 스타일. 투자할 때도 대박 노리는 성향. 단기 투자 추천.',
    healthTip: '심장과 혈압 관리 필요. 격렬한 운동보다는 적당한 유산소 운동 추천.'
  },
  '토': {
    element: '토',
    polarity: '음',
    animal: '🏔️',
    description: '대지처럼 든든하고 안정적인 성격',
    personality: ['신뢰성', '책임감', '현실적', '끈기', '보수적'],
    strengths: ['안정성', '신뢰성', '지속성', '책임감', '현실감각'],
    weaknesses: ['변화 적응 어려움', '고집', '보수성', '융통성 부족'],
    modernInterpretation: '대기업이나 공기업에서 안정적으로 성공하는 타입. 부동산 투자나 장기 투자에 능함. 믿고 맡길 수 있는 신뢰감.',
    mbtiConnection: ['ISFJ', 'ISTJ', 'ESFJ'],
    careerFit: ['공무원', '은행원', '회계사', '부동산 전문가', '프로젝트 매니저', '품질관리'],
    loveStyle: '진중하고 안정적인 연애 추구. 결혼 전제로 만나는 스타일. 상대방에게 안정감을 주는 타입.',
    moneyLuck: '착실하게 모으는 스타일. 부동산이나 적금 같은 안전한 투자 선호. 노후 준비 잘함.',
    healthTip: '소화기 건강 관리 중요. 규칙적인 식사와 스트레스 관리 필요.'
  },
  '금': {
    element: '금',
    polarity: '음',
    animal: '⚔️',
    description: '금속처럼 날카롭고 정확한 성격',
    personality: ['논리적', '분석적', '완벽주의', '독립적', '비판적'],
    strengths: ['분석력', '정확성', '논리성', '독립성', '전문성'],
    weaknesses: ['융통성 부족', '비판적', '완벽주의', '감정표현 서툼'],
    modernInterpretation: 'IT나 공학 분야에서 실력을 발휘하는 타입. 데이터 분석이나 연구직에 적합. 전문가로 인정받을 가능성 높음.',
    mbtiConnection: ['INTJ', 'INTP', 'ISTJ'],
    careerFit: ['개발자', '데이터 사이언티스트', '연구원', '변호사', '의사', '엔지니어'],
    loveStyle: '감정표현이 서툴지만 진실한 마음. 오랜 친구에서 연인으로 발전하는 케이스 많음.',
    moneyLuck: '분석을 통한 투자로 수익 창출. 가상화폐나 주식 분석에 능함. 전문 지식 활용한 투자 추천.',
    healthTip: '호흡기 건강 주의. 미세먼지 차단과 금연 필수. 정기 건강검진 중요.'
  },
  '수': {
    element: '수',
    polarity: '음',
    animal: '🌊',
    description: '물처럼 유연하고 적응력이 뛰어난 성격',
    personality: ['유연성', '적응력', '직관력', '지혜', '포용력'],
    strengths: ['적응력', '직감', '포용력', '지혜', '유연성'],
    weaknesses: ['우유부단', '의존성', '소극적', '결정장애'],
    modernInterpretation: '다양한 분야에 적응 가능한 올라운더. 심리상담이나 서비스업에서 두각. 사람들과의 소통에 능함.',
    mbtiConnection: ['INFP', 'ISFP', 'INFJ'],
    careerFit: ['상담사', '서비스업', '교육자', '사회복지사', '간호사', '심리학자'],
    loveStyle: '상대방에게 잘 맞춰주는 스타일. 감정 공감 능력 뛰어나고 배려심 많음.',
    moneyLuck: '큰 욕심보다는 꾸준한 적립이 좋음. 펀드나 연금 상품 추천. 투자 타이밍 잘 잡음.',
    healthTip: '신장과 방광 건강 관리. 충분한 수분 섭취와 따뜻하게 하기. 스트레스성 방광염 주의.'
  }
}

// 현대적 직업 해석
export const modernCareers: Record<string, string[]> = {
  '창의형': ['콘텐츠 크리에이터', '유튜버', '웹툰작가', '게임 기획자', 'UX디자이너'],
  '분석형': ['데이터 사이언티스트', '개발자', '퀀트', '투자 분석가', 'AI 엔지니어'],
  '소통형': ['마케터', 'PR 전문가', 'SNS 매니저', '브랜드 매니저', '커뮤니티 매니저'],
  '안정형': ['공무원', 'HR', '회계사', '은행원', '품질관리자'],
  '모험형': ['스타트업 창업', '투자자', '트레이더', '해외 진출', '신사업 개발']
}

// MZ세대 연애 스타일
export const loveStyles: Record<string, any> = {
  '직진형': {
    description: '좋아하면 바로 어프로치하는 스타일',
    pros: ['솔직함', '적극적', '시간 단축'],
    cons: ['부담스러울 수 있음', '신중함 부족'],
    tip: '상대방 성향 파악 후 속도 조절하기'
  },
  '썸끌이형': {
    description: '오랫동안 썸을 즐기는 스타일',
    pros: ['로맨틱함', '설렘 지속', '안전함'],
    cons: ['기회 놓치기 쉬움', '상대방 지칠 수 있음'],
    tip: '적절한 타이밍에 관계 발전시키기'
  },
  '친구형': {
    description: '친구에서 연인으로 천천히 발전',
    pros: ['안정적', '서로 잘 알고 시작', '오래감'],
    cons: ['친구에서 벗어나기 어려움', '설렘 부족'],
    tip: '친구 관계와 연인 관계 경계 명확히 하기'
  }
}

// 샘플 사주 결과 데이터
export const sampleSajuResults: ModernSajuResult[] = [
  {
    birthInfo: { year: 1998, month: 5, day: 15, hour: 14, gender: 'F' },
    fourPillars: {
      year: { stem: '무', branch: '인', element: '토' },
      month: { stem: '정', branch: '사', element: '화' },
      day: { stem: '갑', branch: '자', element: '목' },
      hour: { stem: '신', branch: '미', element: '금' }
    },
    dominantElement: '목',
    personality: {
      type: '크리에이티브 리더형',
      description: '창의적이고 진취적인 성격으로 새로운 것을 만들어내는 것을 좋아합니다.',
      keywords: ['창의적', '리더십', '진취적', '트렌디', '소통능력'],
      mbtiLikely: ['ENFP', 'ENTP', 'ENFJ'],
      strengthsModern: [
        '콘텐츠 기획력 뛰어남',
        '트렌드 파악 능력',
        '소셜미디어 활용 능력',
        '팀워크 조율 능력',
        '새로운 아이디어 창출'
      ],
      improvementAreas: [
        '장기 계획 수립',
        '인내심 기르기',
        '디테일 놓치지 않기',
        '감정 관리'
      ]
    },
    lifeAspects: {
      love: {
        style: '썸끌이형',
        compatibility: ['화', '토'],
        advice: '너무 이상형만 고집하지 말고 현실적으로 접근해보세요',
        idealType: '유머러스하고 안정적인 사람'
      },
      career: {
        suitableJobs: ['콘텐츠 크리에이터', '마케터', '이벤트 기획자', '스타트업 창업'],
        workStyle: '자유로운 분위기에서 창의성을 발휘하는 타입',
        leadershipStyle: '팀원들과 소통하며 이끌어가는 민주적 리더십',
        advice: '2025년 하반기에 새로운 기회가 올 수 있어요'
      },
      money: {
        style: '투자보다는 사업으로 돈을 버는 타입',
        luckyPeriod: '2025년 8-10월',
        investmentTip: '부동산보다는 성장주에 투자하는 것이 유리',
        cautionPeriod: '2026년 상반기 무리한 투자 금물'
      },
      health: {
        careAreas: ['간 건강', '스트레스성 위장 장애'],
        recommendedExercise: '요가, 필라테스',
        stressManagement: '명상이나 독서로 마음의 안정 찾기',
        supplementTip: '비타민 B와 오메가3 섭취 권장'
      }
    },
    yearlyFortune: {
      2025: {
        overall: 4,
        love: 3,
        career: 5,
        money: 4,
        health: 3,
        keywords: ['성장', '기회', '변화', '발전'],
        monthlyHighlights: [
          { month: 3, description: '새로운 프로젝트 시작' },
          { month: 8, description: '재정적 성과' },
          { month: 11, description: '인간관계 확장' }
        ]
      }
    },
    mzSummary: {
      oneLineDescription: '크리에이티브한 아이디어로 세상을 바꾸는 트렌드세터',
      emoji: '🌟',
      hashTags: ['#크리에이터', '#아이디어뱅크', '#트렌드세터', '#소통왕', '#미래리더'],
      shareableQuote: '나만의 색깔로 세상을 더 재미있게 만드는 사람 ✨',
      trendKeyword: '크리에이터'
    }
  }
]

// 궁합 데이터
export const compatibilityData: SajuCompatibility[] = [
  {
    element1: '목',
    element2: '화',
    compatibility: 5,
    description: '목이 화를 키우는 관계로 최상의 궁합',
    advice: '서로를 성장시키는 완벽한 파트너십'
  },
  {
    element1: '화',
    element2: '토',
    compatibility: 4,
    description: '화가 토를 만드는 관계로 좋은 궁합',
    advice: '안정적이고 따뜻한 관계'
  },
  {
    element1: '토',
    element2: '금',
    compatibility: 4,
    description: '토가 금을 낳는 관계로 서로 도움',
    advice: '현실적이고 든든한 관계'
  },
  {
    element1: '금',
    element2: '수',
    compatibility: 4,
    description: '금이 수를 만드는 관계로 조화로움',
    advice: '지혜롭고 유연한 관계'
  },
  {
    element1: '수',
    element2: '목',
    compatibility: 5,
    description: '수가 목을 기르는 관계로 완벽한 궁합',
    advice: '서로를 성장시키는 이상적 관계'
  }
]

export default {
  sajuElements,
  modernCareers,
  loveStyles,
  sampleSajuResults,
  compatibilityData
}