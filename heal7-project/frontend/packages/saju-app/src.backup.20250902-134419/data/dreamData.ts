// 꿈풀이/해몽 데이터 시스템

export interface DreamCategory {
  id: string;
  name: string;
  emoji: string;
  description: string;
  parentId?: string;
  subcategories?: string[];
}

export interface DreamInterpretation {
  id: string;
  keyword: string;
  category: string;
  subcategory?: string;
  emoji: string;
  traditionInterpretation: string; // 전통적 해석
  modernInterpretation: string;    // 현대적 해석
  psychologyInterpretation?: string; // 심리학적 해석
  keywords: string[];
  relatedDreams: string[];
  luckyNumbers?: number[];
  mood: 'positive' | 'neutral' | 'negative' | 'warning';
  frequency: number; // 검색 빈도
  tags: string[];
  variations: string[]; // 유사한 꿈들
  combinationEffects?: CombinationEffect[];
}

export interface CombinationEffect {
  with: string[]; // 함께 꾼 꿈들
  effect: string; // 조합 효과
  interpretation: string;
  strength: 'weak' | 'medium' | 'strong';
}

export interface DreamSearchResult {
  dreams: DreamInterpretation[];
  totalCount: number;
  suggestions: string[];
  popularKeywords: string[];
}

// 꿈 카테고리 분류 체계
export const dreamCategories: DreamCategory[] = [
  // 주요 카테고리
  {
    id: 'animals',
    name: '동물',
    emoji: '🐾',
    description: '동물이 나오는 꿈',
    subcategories: ['포유류', '조류', '어류', '곤충류', '파충류', '상상동물']
  },
  {
    id: 'nature',
    name: '자연',
    emoji: '🌿',
    description: '자연 현상과 환경',
    subcategories: ['날씨', '산/바다', '식물', '천체', '계절', '재해']
  },
  {
    id: 'people',
    name: '사람',
    emoji: '👥',
    description: '사람이 등장하는 꿈',
    subcategories: ['가족', '친구', '연인', '낯선사람', '유명인', '고인']
  },
  {
    id: 'objects',
    name: '사물',
    emoji: '🏺',
    description: '물건이나 도구',
    subcategories: ['생활용품', '교통수단', '건물', '음식', '의류', '보석']
  },
  {
    id: 'actions',
    name: '행동',
    emoji: '🏃‍♂️',
    description: '특정 행동을 하는 꿈',
    subcategories: ['이동', '일상생활', '운동', '작업', '학습', '놀이']
  },
  {
    id: 'emotions',
    name: '감정',
    emoji: '😊',
    description: '감정 상태나 느낌',
    subcategories: ['기쁨', '슬픔', '두려움', '분노', '사랑', '놀람']
  },
  {
    id: 'body',
    name: '신체',
    emoji: '👤',
    description: '몸과 관련된 꿈',
    subcategories: ['얼굴', '손발', '머리카락', '상처', '질병', '변화']
  },
  {
    id: 'spiritual',
    name: '영적/신비',
    emoji: '🔮',
    description: '초자연적 현상',
    subcategories: ['신/부처', '귀신', '천사', '예언', '환상', '죽음']
  }
];

// 인기 꿈풀이 키워드 (검색량 기준)
export const popularDreamKeywords = [
  // 동물
  '뱀', '거미', '물고기', '새', '고양이', '개', '쥐', '호랑이', '용', '돼지',
  // 자연
  '물', '불', '산', '바다', '꽃', '나무', '비', '눈', '번개', '지진',
  // 사람
  '죽은사람', '아기', '임신', '결혼', '이별', '싸움', '키스', '포옹',
  // 사물
  '돈', '금', '집', '차', '옷', '음식', '칼', '거울', '다리', '계단',
  // 행동
  '날아가기', '떨어지기', '쫓기기', '도망가기', '시험', '여행', '청소', '요리',
  // 감정/상황
  '울기', '웃기', '화내기', '무서워하기', '길잃기', '찾기', '숨기', '잃어버리기'
];

// 샘플 꿈풀이 데이터 (실제로는 수천 개가 필요)
export const dreamInterpretations: DreamInterpretation[] = [
  {
    id: 'dream_001',
    keyword: '뱀',
    category: 'animals',
    subcategory: '파충류',
    emoji: '🐍',
    traditionInterpretation: '뱀꿈은 전통적으로 길몽으로 여겨집니다. 재물운 상승, 지혜 획득, 치유의 의미가 있습니다.',
    modernInterpretation: '변화와 변신의 상징입니다. 새로운 시작이나 성장을 의미하며, 때로는 숨겨진 적이나 위험을 나타내기도 합니다.',
    psychologyInterpretation: '무의식의 힘, 원시적 에너지, 억압된 욕망의 상징입니다.',
    keywords: ['재물', '변화', '치유', '지혜', '위험', '변신'],
    relatedDreams: ['용', '도마뱀', '거북이'],
    luckyNumbers: [3, 7, 21],
    mood: 'positive',
    frequency: 9500,
    tags: ['길몽', '재물운', '변화', '동물'],
    variations: ['독사', '비단뱀', '뱀이 물다', '뱀을 잡다', '큰 뱀', '작은 뱀'],
    combinationEffects: [
      {
        with: ['물'],
        effect: '재물운 대폭 상승',
        interpretation: '뱀과 물이 함께 나오는 꿈은 큰 재물을 얻게 될 길몽입니다.',
        strength: 'strong'
      }
    ]
  },
  {
    id: 'dream_002',
    keyword: '물',
    category: 'nature',
    subcategory: '자연현상',
    emoji: '💧',
    traditionInterpretation: '맑은 물은 재물과 복을, 흐린 물은 걱정과 근심을 의미합니다.',
    modernInterpretation: '감정의 흐름, 무의식의 세계, 정화와 재생을 상징합니다.',
    psychologyInterpretation: '감정 상태와 정서적 균형을 반영합니다.',
    keywords: ['재물', '감정', '정화', '흐름', '무의식'],
    relatedDreams: ['비', '바다', '강', '호수'],
    luckyNumbers: [2, 6, 8],
    mood: 'neutral',
    frequency: 8700,
    tags: ['자연', '감정', '재물', '정화'],
    variations: ['맑은 물', '흐린 물', '물에 빠지다', '물을 마시다', '홍수', '물이 새다'],
    combinationEffects: [
      {
        with: ['뱀'],
        effect: '재물운 대폭 상승',
        interpretation: '물과 뱀이 함께 나오는 꿈은 큰 재물을 얻게 될 길몽입니다.',
        strength: 'strong'
      }
    ]
  },
  {
    id: 'dream_003',
    keyword: '죽은사람',
    category: 'people',
    subcategory: '고인',
    emoji: '👻',
    traditionInterpretation: '돌아가신 분이 꿈에 나타나는 것은 보살핌과 축복의 의미입니다.',
    modernInterpretation: '그리움과 미완성된 감정, 또는 새로운 시작을 알리는 메시지일 수 있습니다.',
    psychologyInterpretation: '상실감 처리와 내적 치유 과정을 나타냅니다.',
    keywords: ['그리움', '축복', '메시지', '치유', '보살핌'],
    relatedDreams: ['장례식', '무덤', '유품'],
    luckyNumbers: [4, 9, 49],
    mood: 'neutral',
    frequency: 7200,
    tags: ['사람', '영적', '치유', '메시지'],
    variations: ['죽은 가족', '죽은 친구', '대화하다', '음식주다', '화내다', '웃다'],
    combinationEffects: []
  },
  {
    id: 'dream_004',
    keyword: '돈',
    category: 'objects',
    subcategory: '가치있는것',
    emoji: '💰',
    traditionInterpretation: '돈을 주워도 길몽, 잃어도 길몽으로 해석됩니다. 재물운의 변화를 의미합니다.',
    modernInterpretation: '성공욕구, 안정감 추구, 또는 경제적 불안감을 나타냅니다.',
    psychologyInterpretation: '자존감과 가치 인정에 대한 욕구를 반영합니다.',
    keywords: ['재물', '성공', '안정', '욕구', '가치'],
    relatedDreams: ['금', '보석', '지갑', '은행'],
    luckyNumbers: [1, 8, 18, 28],
    mood: 'positive',
    frequency: 6800,
    tags: ['재물', '성공', '욕구', '사물'],
    variations: ['돈을 줍다', '돈을 잃다', '돈을 받다', '돈을 세다', '가짜돈', '외국돈'],
    combinationEffects: []
  },
  {
    id: 'dream_005',
    keyword: '날아가기',
    category: 'actions',
    subcategory: '이동',
    emoji: '🕊️',
    traditionInterpretation: '자유로움과 성공을 의미하는 길몽입니다.',
    modernInterpretation: '제약에서 벗어나고 싶은 욕구, 이상과 목표 달성 의지를 나타냅니다.',
    psychologyInterpretation: '억압에서 해방되고 싶은 무의식적 욕구를 나타냅니다.',
    keywords: ['자유', '성공', '해방', '이상', '목표'],
    relatedDreams: ['새가 되다', '하늘', '구름'],
    luckyNumbers: [5, 11, 15],
    mood: 'positive',
    frequency: 5900,
    tags: ['행동', '자유', '성공', '해방'],
    variations: ['높이 날다', '낮게 날다', '떨어지다', '날개가 생기다'],
    combinationEffects: []
  }
];

// 꿈풀이 검색 함수
export const searchDreams = (query: string): DreamSearchResult => {
  const normalizedQuery = query.toLowerCase().trim();
  
  if (!normalizedQuery) {
    return {
      dreams: [],
      totalCount: 0,
      suggestions: popularDreamKeywords.slice(0, 10),
      popularKeywords: popularDreamKeywords.slice(0, 20)
    };
  }

  // 키워드 매칭
  const exactMatches = dreamInterpretations.filter(dream => 
    dream.keyword.includes(normalizedQuery) ||
    dream.variations.some(v => v.includes(normalizedQuery)) ||
    dream.keywords.some(k => k.includes(normalizedQuery))
  );

  // 카테고리 매칭
  const categoryMatches = dreamInterpretations.filter(dream =>
    dream.category.includes(normalizedQuery) ||
    dream.subcategory?.includes(normalizedQuery)
  );

  // 태그 매칭
  const tagMatches = dreamInterpretations.filter(dream =>
    dream.tags.some(tag => tag.includes(normalizedQuery))
  );

  // 중복 제거 및 빈도순 정렬
  const allMatches = [...new Set([...exactMatches, ...categoryMatches, ...tagMatches])];
  const sortedMatches = allMatches.sort((a, b) => b.frequency - a.frequency);

  // 연관 검색어 생성
  const suggestions = popularDreamKeywords
    .filter(keyword => keyword.includes(normalizedQuery) && keyword !== normalizedQuery)
    .slice(0, 8);

  return {
    dreams: sortedMatches.slice(0, 50), // 최대 50개 결과
    totalCount: sortedMatches.length,
    suggestions,
    popularKeywords: popularDreamKeywords.slice(0, 15)
  };
};

// 꿈 조합 해석
export const getCombinationInterpretation = (dreamKeywords: string[]): string => {
  if (dreamKeywords.length < 2) return '';
  
  // 특별한 조합 패턴 확인
  const specialCombinations = [
    {
      keywords: ['뱀', '물'],
      interpretation: '뱀과 물이 함께 나오는 꿈은 재물운이 크게 상승할 길몽입니다. 특히 사업이나 투자에서 좋은 결과를 얻을 수 있습니다.'
    },
    {
      keywords: ['물고기', '물'],
      interpretation: '물고기와 물의 조합은 풍요와 번영을 의미합니다. 생활이 안정되고 재물이 늘어날 것을 암시합니다.'
    },
    {
      keywords: ['돈', '죽은사람'],
      interpretation: '고인이 돈을 주는 꿈은 뜻밖의 재물이나 도움을 받게 될 것을 의미합니다.'
    }
  ];

  for (const combo of specialCombinations) {
    if (combo.keywords.every(keyword => dreamKeywords.includes(keyword))) {
      return combo.interpretation;
    }
  }

  return '여러 요소가 복합적으로 나타난 꿈으로, 각 요소의 의미를 종합적으로 해석해야 합니다.';
};

// 월별 인기 꿈 키워드 (계절성 반영)
export const getSeasonalDreams = (month: number): string[] => {
  const seasonal = {
    spring: ['꽃', '나무', '새', '물', '여행'],
    summer: ['바다', '물고기', '비', '더위', '휴가'],
    autumn: ['단풍', '열매', '추수', '바람', '옷'],
    winter: ['눈', '불', '집', '따뜻함', '가족']
  };

  if (month >= 3 && month <= 5) return seasonal.spring;
  if (month >= 6 && month <= 8) return seasonal.summer;
  if (month >= 9 && month <= 11) return seasonal.autumn;
  return seasonal.winter;
};

export default {
  dreamCategories,
  popularDreamKeywords,
  dreamInterpretations,
  searchDreams,
  getCombinationInterpretation,
  getSeasonalDreams
};