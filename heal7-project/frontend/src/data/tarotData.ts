// 타로카드 데이터와 시스템 (동서양 퓨전 78카드 덱 통합)

export interface TarotCard {
  id: string
  name: string
  nameKr: string
  suit?: 'cups' | 'wands' | 'swords' | 'pentacles' | 'major'
  number?: number
  emoji: string
  image: string
  upright: {
    meaning: string
    description: string
    love: string
    career: string
    money: string
    advice: string
  }
  reversed: {
    meaning: string
    description: string
    love: string
    career: string
    money: string
    advice: string
  }
  keywords: string[]
  mzInterpretation: string
  // 동서양 퓨전 확장 속성
  koreanElement?: string // 한국/동아시아 문화 요소
  guardian?: string // 사방신 수호자 (주작/현무/청룡/백호)
  zodiacAnimal?: string // 십이지신
  isGuardianVariant?: boolean // Guardian Variant 여부
}

export interface TarotSpread {
  id: string
  name: string
  description: string
  emoji: string
  positions: {
    name: string
    description: string
    x: number
    y: number
  }[]
  interpretation: string
  category: 'love' | 'career' | 'general' | 'decision' | 'daily'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  duration: string
}

export interface TarotReading {
  id: string
  spreadId: string
  cards: {
    cardId: string
    position: number
    isReversed: boolean
  }[]
  interpretation: string
  timestamp: string
}

// 주요 아르카나 카드들 (MZ세대 맞춤 해석)
export const majorArcanaCards: TarotCard[] = [
  {
    id: 'major_00',
    name: 'The Fool',
    nameKr: '바보',
    suit: 'major',
    number: 0,
    emoji: '🃏',
    image: '/images/tarot/major_00_fool.jpg',
    upright: {
      meaning: '새로운 시작, 순수함, 모험',
      description: '완전히 새로운 여정이 시작되는 시점입니다.',
      love: '새로운 연애가 시작될 기미! 설렘 가득한 만남이 기다리고 있어요.',
      career: '새로운 직장이나 프로젝트에 도전할 타이밍이에요. 겁먹지 말고 시작해보세요!',
      money: '새로운 수입원이 생길 수 있어요. 하지만 무모한 투자는 금물!',
      advice: '걱정 말고 일단 시작해보세요. 완벽하지 않아도 괜찮아요.'
    },
    reversed: {
      meaning: '무모함, 경솔함, 준비 부족',
      description: '너무 성급하게 행동하고 있는 것은 아닌지 돌아보세요.',
      love: '썸을 너무 밀어붙이고 있지는 않나요? 조금 여유를 가져보세요.',
      career: '준비 없이 이직하거나 전직하려고 하면 위험할 수 있어요.',
      money: '충동구매나 무분별한 투자로 손해를 볼 수 있어요.',
      advice: '한 번 더 생각해보고 신중하게 계획을 세워보세요.'
    },
    keywords: ['새출발', '모험', '순수', '용기', '시작'],
    mzInterpretation: '완전 YOLO 모드! 지금이야말로 새로운 걸 시도해볼 때예요 🚀',
    koreanElement: '천진난만한 동자승, 구도의 길을 시작하는 마음',
    guardian: '모든 방향의 시작점',
    isGuardianVariant: false
  },
  {
    id: 'major_01',
    name: 'The Magician',
    nameKr: '마법사',
    suit: 'major',
    number: 1,
    emoji: '🎩',
    image: '/images/tarot/major_01_magician.jpg',
    upright: {
      meaning: '의지력, 창조력, 실현',
      description: '모든 것을 가능하게 만들 수 있는 강력한 에너지가 있습니다.',
      love: '원하는 사람에게 어필할 수 있는 최고의 타이밍! 매력이 폭발해요.',
      career: '새로운 스킬을 배우거나 창업에 도전하기 좋은 시기예요.',
      money: '투자나 부업으로 돈을 벌 수 있는 아이디어가 떠오를 거예요.',
      advice: '자신감을 가지고 적극적으로 행동하세요. 당신에게는 그 능력이 있어요!'
    },
    reversed: {
      meaning: '허황됨, 조작, 능력 부족',
      description: '실력은 부족한데 자신감만 넘치고 있는 상태일 수 있어요.',
      love: '과장된 모습으로 어필하려 하지 마세요. 진실한 모습이 더 매력적이에요.',
      career: '실력을 기르지 않고 겉멋만 들었다가는 큰코다칠 수 있어요.',
      money: '사기나 허위 정보에 속아 손실을 입을 수 있어요.',
      advice: '허세 부리지 말고 실력을 차근차근 쌓아가세요.'
    },
    keywords: ['의지', '창조', '실현', '능력', '집중'],
    mzInterpretation: '지금 당신 완전 주인공 모드! 뭐든 할 수 있을 것 같은 기분이죠? ✨',
    koreanElement: '도술을 부리는 선인, 천지의 기운을 자유자재로 다루는 도사',
    guardian: '주작의 창조력',
    isGuardianVariant: false
  },
  {
    id: 'major_02',
    name: 'The High Priestess',
    nameKr: '여사제',
    suit: 'major',
    number: 2,
    emoji: '🌙',
    image: '/images/tarot/major_02_priestess.jpg',
    upright: {
      meaning: '직감, 내면의 지혜, 신비',
      description: '직감을 믿고 내면의 목소리에 귀 기울여야 할 때입니다.',
      love: '상대의 진심을 직감으로 알 수 있어요. 첫 인상을 믿어보세요.',
      career: '데이터보다 직감이 더 정확할 수 있어요. 느낌을 믿어보세요.',
      money: '투자 타이밍을 직감으로 잡을 수 있어요. 하지만 무모하지는 마세요.',
      advice: '남의 말보다 내 마음의 소리를 들어보세요.'
    },
    reversed: {
      meaning: '직감 무시, 표면적 판단, 비밀',
      description: '너무 논리적으로만 생각하려고 하고 있어요.',
      love: '상대의 겉모습에만 현혹되어 본질을 보지 못하고 있어요.',
      career: '중요한 정보를 놓치고 있을 수 있어요. 더 세심하게 살펴보세요.',
      money: '숨겨진 비용이나 위험이 있을 수 있어요.',
      advice: '겉으로 드러난 것 말고 숨겨진 진실을 찾아보세요.'
    },
    keywords: ['직감', '내면', '신비', '지혜', '비밀'],
    mzInterpretation: '지금 당신의 직감이 레전드급! 느낌 오는 대로 가보세요 🔮',
    koreanElement: '달빛 아래 기도하는 무녀, 영험한 직감의 무당',
    guardian: '현무의 깊은 지혜',
    isGuardianVariant: false
  },
  {
    id: 'major_10',
    name: 'Wheel of Fortune',
    nameKr: '운명의 바퀴',
    suit: 'major',
    number: 10,
    emoji: '🎡',
    image: '/images/tarot/major_10_wheel.jpg',
    upright: {
      meaning: '행운, 변화, 순환, 기회',
      description: '인생의 전환점이 다가오고 있습니다. 긍정적인 변화가 기다려요!',
      love: '운명적인 만남이 기다리고 있어요! 소개팅이나 미팅에 적극 참여해보세요.',
      career: '승진이나 이직 기회가 갑자기 생길 수 있어요. 준비는 되어 있나요?',
      money: '예상치 못한 수입이나 상금, 당첨이 있을 수 있어요! 복권 사볼까요?',
      advice: '변화를 두려워하지 마세요. 지금이 기회를 잡을 때예요!'
    },
    reversed: {
      meaning: '불운, 정체, 나쁜 타이밍',
      description: '지금은 조용히 때를 기다리는 것이 좋겠어요.',
      love: '연애운이 살짝 저조한 시기. 무리해서 만남을 가지려 하지 마세요.',
      career: '중요한 결정은 미루는 게 좋겠어요. 지금은 기다림의 시간입니다.',
      money: '투자나 도박은 절대 금물! 손실이 클 수 있어요.',
      advice: '지금은 현상 유지가 답입니다. 급하게 변화를 시도하지 마세요.'
    },
    keywords: ['행운', '변화', '순환', '운명', '기회'],
    mzInterpretation: '인생 대박 찬스가 온다! 이때 아니면 언제? 🍀',
    koreanElement: '음양의 태극, 천지가 돌아가는 자연의 이치',
    guardian: '사방신이 함께 도는 운명의 바퀴',
    isGuardianVariant: false
  },
  {
    id: 'major_13',
    name: 'Death',
    nameKr: '죽음',
    suit: 'major',
    number: 13,
    emoji: '💀',
    image: '/images/tarot/major_13_death.jpg',
    upright: {
      meaning: '변화, 끝과 시작, 해방',
      description: '무언가 끝나지만, 그것은 새로운 시작을 의미해요.',
      love: '지금 연애가 끝나더라도 더 좋은 인연이 기다리고 있어요.',
      career: '지금 직장을 그만두거나 전직하는 것도 나쁘지 않을 수 있어요.',
      money: '기존 수입원이 끊어져도 새로운 기회가 생길 거예요.',
      advice: '끝을 두려워하지 마세요. 새로운 시작의 기회입니다!'
    },
    reversed: {
      meaning: '변화 거부, 정체, 집착',
      description: '변화를 받아들이지 못하고 과거에 머물고 있어요.',
      love: '이미 끝난 연애에 계속 매달리고 있지는 않나요?',
      career: '안 좋은 직장환경인 줄 알면서도 못 떠나고 있어요.',
      money: '손해 보는 투자를 계속 붙들고 있어요.',
      advice: '놓아야 할 것은 과감하게 놓아주세요. 그래야 새로운 게 들어와요.'
    },
    keywords: ['변화', '끝', '시작', '해방', '재생'],
    mzInterpretation: '지금 인생 리셋 타이밍! 과감하게 정리하고 새 출발하세요 🔄',
    koreanElement: '저승사자의 인도, 환생의 문턱을 넘나드는 전환점',
    guardian: '백호의 정화와 재생',
    isGuardianVariant: false
  },
  // 나머지 메이저 아르카나 (3-9, 11-12, 14-21)
  {
    id: 'major_03',
    name: 'The Empress',
    nameKr: '여제',
    suit: 'major',
    number: 3,
    emoji: '👸',
    image: '/images/tarot/major_03_empress.jpg',
    upright: {
      meaning: '풍요, 모성, 창조력',
      description: '풍부한 창조력과 모성애가 넘치는 시기입니다.',
      love: '따뜻한 사랑과 포용력으로 관계가 깊어져요.',
      career: '창의적인 아이디어로 성과를 낼 수 있어요.',
      money: '안정적인 수입과 풍요로운 생활이 기대돼요.',
      advice: '자연스럽고 따뜻한 마음으로 주변을 돌보세요.'
    },
    reversed: {
      meaning: '과보호, 의존성, 창조력 부족',
      description: '너무 간섭하거나 의존적이 되고 있어요.',
      love: '상대를 너무 구속하려 하지 마세요.',
      career: '창의력이 막히고 있어요. 휴식이 필요해요.',
      money: '과소비나 무계획적인 지출을 조심하세요.',
      advice: '독립성을 기르고 균형을 찾아보세요.'
    },
    keywords: ['풍요', '모성', '창조', '포용', '자연'],
    mzInterpretation: '엄마 미소 모드 온! 모든 걸 품어주고 싶은 마음 💕',
    koreanElement: '대지모신, 삼신할매의 자비로운 품',
    guardian: '현무의 포용력',
    isGuardianVariant: false
  },
  {
    id: 'major_04',
    name: 'The Emperor',
    nameKr: '황제',
    suit: 'major',
    number: 4,
    emoji: '👑',
    image: '/images/tarot/major_04_emperor.jpg',
    upright: {
      meaning: '권위, 질서, 안정',
      description: '강한 리더십과 확고한 의지가 필요한 때입니다.',
      love: '주도적으로 관계를 이끌어갈 때예요.',
      career: '책임감 있는 리더로서 인정받을 수 있어요.',
      money: '체계적인 재정 관리로 안정을 도모하세요.',
      advice: '확고한 신념을 가지고 결단력 있게 행동하세요.'
    },
    reversed: {
      meaning: '독재, 고집, 권위주의',
      description: '너무 권위적이거나 고집스럽게 굴고 있어요.',
      love: '상대방의 의견도 들어보세요.',
      career: '독단적인 결정보다 팀워크를 중시하세요.',
      money: '무리한 투자나 과시욕을 조심하세요.',
      advice: '유연성을 기르고 다른 사람의 목소리에 귀 기울이세요.'
    },
    keywords: ['권위', '질서', '안정', '리더십', '책임'],
    mzInterpretation: '보스 모드 활성화! 카리스마 대폭발 시간 👑',
    koreanElement: '임금님의 위엄, 나라를 다스리는 성군의 덕',
    guardian: '청룡의 위엄과 질서',
    isGuardianVariant: false
  }
]

// 마이너 아르카나: 주작의 지팡이 (Wands) - 불 원소, 창조력
export const wandsCards: TarotCard[] = [
  {
    id: 'wands_ace',
    name: 'Ace of Wands',
    nameKr: '주작의 지팡이 에이스',
    suit: 'wands',
    number: 1,
    emoji: '🔥',
    image: '/images/tarot/wands_ace.jpg',
    upright: {
      meaning: '새로운 시작, 창조적 에너지, 영감',
      description: '창의적인 프로젝트나 새로운 열정이 시작돼요.',
      love: '뜨거운 새로운 사랑이나 관계의 새로운 시작!',
      career: '창업이나 새 프로젝트 시작에 최적의 타이밍이에요.',
      money: '새로운 수입원이 생기거나 투자 기회가 와요.',
      advice: '직감을 믿고 과감하게 시작해보세요!'
    },
    reversed: {
      meaning: '에너지 부족, 창조력 막힘, 지연',
      description: '아이디어는 있지만 실행력이 부족해요.',
      love: '열정이 식어가고 있거나 타이밍이 안 맞아요.',
      career: '계획만 많고 실행이 안 되고 있어요.',
      money: '투자나 사업 계획이 지연되고 있어요.',
      advice: '에너지를 재충전하고 다시 도전해보세요.'
    },
    keywords: ['시작', '창조', '영감', '열정', '가능성'],
    mzInterpretation: '완전 아이디어 폭발! 지금 시작하면 대박날 것 같아요 🚀',
    koreanElement: '주작의 화염, 봄의 생명력이 솟구치는 에너지',
    guardian: '주작',
    isGuardianVariant: false
  }
]

// 마이너 아르카나: 현무의 성배 (Cups) - 물 원소, 감정
export const cupsCards: TarotCard[] = [
  {
    id: 'cups_ace',
    name: 'Ace of Cups',
    nameKr: '현무의 성배 에이스',
    suit: 'cups',
    number: 1,
    emoji: '💧',
    image: '/images/tarot/cups_ace.jpg',
    upright: {
      meaning: '새로운 감정, 사랑의 시작, 직감',
      description: '마음 깊은 곳에서 우러나는 순수한 감정이 시작돼요.',
      love: '순수하고 깊은 사랑의 시작! 운명적 만남 예감.',
      career: '팀워크와 인간관계가 중요한 시기예요.',
      money: '감정적 만족을 주는 투자나 소비를 고려해보세요.',
      advice: '마음의 소리에 귀 기울이고 감정을 솔직하게 표현하세요.'
    },
    reversed: {
      meaning: '감정의 혼란, 실망, 관계 문제',
      description: '감정이 복잡하게 얽혀있거나 상처받은 상태예요.',
      love: '오해나 감정적 상처로 관계가 어려워져요.',
      career: '동료들과의 갈등이나 감정적 스트레스가 있어요.',
      money: '감정적 소비로 후회할 수 있어요.',
      advice: '감정을 정리하고 마음의 평화를 찾아보세요.'
    },
    keywords: ['감정', '사랑', '직감', '순수', '관계'],
    mzInterpretation: '하트 눈깔 모드! 세상이 온통 핑크빛으로 보여요 💕',
    koreanElement: '현무의 감성, 깊은 바다처럼 잔잔한 마음의 평화',
    guardian: '현무',
    zodiacAnimal: '토끼',
    isGuardianVariant: false
  }
]

// 마이너 아르카나: 청룡의 검 (Swords) - 공기 원소, 지성
export const swordsCards: TarotCard[] = [
  {
    id: 'swords_ace',
    name: 'Ace of Swords',
    nameKr: '청룡의 검 에이스',
    suit: 'swords',
    number: 1,
    emoji: '⚔️',
    image: '/images/tarot/swords_ace.jpg',
    upright: {
      meaning: '명료한 사고, 진실, 새로운 아이디어',
      description: '머리가 맑아지고 올바른 판단력이 생겨요.',
      love: '솔직한 대화로 관계가 명확해져요.',
      career: '새로운 아이디어나 해결책이 떠올라요.',
      money: '정확한 분석으로 좋은 투자 기회를 찾을 수 있어요.',
      advice: '논리적으로 생각하고 진실을 추구하세요.'
    },
    reversed: {
      meaning: '혼란, 잘못된 판단, 소통 부족',
      description: '생각이 복잡하고 판단력이 흐려져 있어요.',
      love: '오해나 소통 문제로 갈등이 생겨요.',
      career: '잘못된 정보로 실수할 수 있어요.',
      money: '성급한 결정으로 손실을 볼 수 있어요.',
      advice: '차분히 생각하고 정확한 정보를 확인하세요.'
    },
    keywords: ['지성', '진실', '명료함', '분석', '소통'],
    mzInterpretation: '머리 회전 max! 지금 생각하는 모든 게 다 맞을 것 같아요 🧠',
    koreanElement: '청룡의 예지, 동방의 지혜로운 바람',
    guardian: '청룡',
    zodiacAnimal: '원숭이',
    isGuardianVariant: false
  }
]

// 마이너 아르카나: 백호의 주화 (Pentacles) - 흙 원소, 물질
export const pentaclesCards: TarotCard[] = [
  {
    id: 'pentacles_ace',
    name: 'Ace of Pentacles',
    nameKr: '백호의 주화 에이스',
    suit: 'pentacles',
    number: 1,
    emoji: '🪙',
    image: '/images/tarot/pentacles_ace.jpg',
    upright: {
      meaning: '물질적 풍요, 새로운 기회, 안정',
      description: '물질적으로 풍요로워지거나 안정을 찾을 기회가 와요.',
      love: '안정적이고 현실적인 관계가 시작돼요.',
      career: '승진이나 연봉 인상, 좋은 일자리 기회가 있어요.',
      money: '수입 증가나 좋은 투자 기회가 생겨요.',
      advice: '실용적이고 현실적인 접근을 하세요.'
    },
    reversed: {
      meaning: '기회 상실, 물질적 불안, 욕심',
      description: '좋은 기회를 놓치거나 물질적으로 불안정해요.',
      love: '현실적 문제로 관계에 어려움이 있어요.',
      career: '기대했던 기회가 없어지거나 지연돼요.',
      money: '투자 손실이나 수입 감소가 있을 수 있어요.',
      advice: '욕심을 줄이고 기초를 탄탄히 하세요.'
    },
    keywords: ['물질', '안정', '기회', '현실', '풍요'],
    mzInterpretation: '돈 복 대폭발! 지갑이 두둑해질 예감이에요 💰',
    koreanElement: '백호의 실용성, 서방의 견고한 대지',
    guardian: '백호',
    zodiacAnimal: '닭',
    isGuardianVariant: false
  }
]

// 통합 78장 카드 덱
export const fullTarotDeck: TarotCard[] = [
  ...majorArcanaCards,
  ...wandsCards,
  ...cupsCards,
  ...swordsCards,
  ...pentaclesCards
]

// 타로 스프레드 (카드 배치법)
export const tarotSpreads: TarotSpread[] = [
  {
    id: 'daily_one',
    name: '오늘의 한 장',
    description: '오늘 하루를 위한 간단한 메시지',
    emoji: '📅',
    positions: [
      { name: '오늘의 메시지', description: '오늘 당신에게 필요한 조언', x: 50, y: 50 }
    ],
    interpretation: '선택한 카드가 오늘 하루를 위한 특별한 메시지를 전해드려요.',
    category: 'daily',
    difficulty: 'beginner',
    duration: '1분'
  },
  {
    id: 'love_triangle',
    name: '연애 삼각 스프레드',
    description: '연애와 관련된 고민을 해결해드려요',
    emoji: '💕',
    positions: [
      { name: '현재 상황', description: '지금 연애 상황은?', x: 50, y: 20 },
      { name: '내 마음', description: '나는 어떻게 생각하고 있을까?', x: 25, y: 70 },
      { name: '상대 마음', description: '상대방은 어떻게 생각할까?', x: 75, y: 70 }
    ],
    interpretation: '연애에 대한 현재 상황과 서로의 마음을 알아보는 스프레드입니다.',
    category: 'love',
    difficulty: 'intermediate',
    duration: '5분'
  },
  {
    id: 'career_path',
    name: '진로/취업 가이드',
    description: '취업과 진로에 대한 조언을 받아보세요',
    emoji: '🚀',
    positions: [
      { name: '현재 능력', description: '지금 나의 강점은?', x: 20, y: 50 },
      { name: '기회', description: '앞으로 올 기회는?', x: 50, y: 30 },
      { name: '조언', description: '무엇을 준비해야 할까?', x: 80, y: 50 }
    ],
    interpretation: '취업과 진로에 대한 통찰과 조언을 제공합니다.',
    category: 'career',
    difficulty: 'intermediate',
    duration: '7분'
  },
  {
    id: 'yes_no',
    name: '예스/노 질문',
    description: '궁금한 것에 대한 간단한 답변',
    emoji: '❓',
    positions: [
      { name: '답변', description: '당신의 질문에 대한 우주의 답변', x: 50, y: 50 }
    ],
    interpretation: '간단한 질문에 대한 명확한 답변을 받아보세요.',
    category: 'general',
    difficulty: 'beginner',
    duration: '30초'
  },
  {
    id: 'weekly_outlook',
    name: '이번 주 전망',
    description: '일주일간의 운세를 미리 확인해보세요',
    emoji: '📊',
    positions: [
      { name: '월요일', description: '한 주의 시작', x: 10, y: 50 },
      { name: '화수목', description: '주중의 흐름', x: 30, y: 30 },
      { name: '목금', description: '주말 준비', x: 50, y: 50 },
      { name: '주말', description: '휴식과 충전', x: 70, y: 30 },
      { name: '조언', description: '이번 주 핵심 메시지', x: 90, y: 50 }
    ],
    interpretation: '일주일간의 전반적인 흐름과 각 시기별 조언을 제공합니다.',
    category: 'general',
    difficulty: 'advanced',
    duration: '10분'
  },
  // 동서양 퓨전 스프레드 추가
  {
    id: 'four_guardians',
    name: '사방신 수호 스프레드',
    description: '동서남북 사방신의 가호로 종합 운세를 확인해보세요',
    emoji: '🐉',
    positions: [
      { name: '동방 청룡', description: '지혜와 성장 (봄의 기운)', x: 80, y: 50 },
      { name: '남방 주작', description: '열정과 창조 (여름의 기운)', x: 50, y: 20 },
      { name: '서방 백호', description: '안정과 결실 (가을의 기운)', x: 20, y: 50 },
      { name: '북방 현무', description: '휴식과 성찰 (겨울의 기운)', x: 50, y: 80 },
      { name: '중앙 황룡', description: '통합된 조언과 핵심 메시지', x: 50, y: 50 }
    ],
    interpretation: '사방신이 전하는 균형잡힌 지혜와 조언을 받아보세요.',
    category: 'general',
    difficulty: 'advanced',
    duration: '15분'
  },
  {
    id: 'zodiac_year',
    name: '십이지신 연간 운세',
    description: '12달의 흐름을 십이지신으로 풀어보는 연간 운세',
    emoji: '🐭',
    positions: [
      { name: '쥐띠 (1월)', description: '새로운 시작', x: 50, y: 5 },
      { name: '소띠 (2월)', description: '착실한 진행', x: 75, y: 15 },
      { name: '호랑이띠 (3월)', description: '용기와 도전', x: 90, y: 40 },
      { name: '토끼띠 (4월)', description: '조화와 균형', x: 85, y: 65 },
      { name: '용띠 (5월)', description: '변화와 발전', x: 65, y: 85 },
      { name: '뱀띠 (6월)', description: '지혜와 통찰', x: 35, y: 85 },
      { name: '말띠 (7월)', description: '활력과 전진', x: 15, y: 65 },
      { name: '양띠 (8월)', description: '평화와 안정', x: 10, y: 40 },
      { name: '원숭이띠 (9월)', description: '창의와 기민함', x: 25, y: 15 },
      { name: '닭띠 (10월)', description: '성실과 결실', x: 50, y: 10 },
      { name: '개띠 (11월)', description: '충성과 보호', x: 75, y: 25 },
      { name: '돼지띠 (12월)', description: '풍요와 마무리', x: 50, y: 50 }
    ],
    interpretation: '한 해 동안의 흐름을 십이지신의 순환으로 이해해보세요.',
    category: 'general',
    difficulty: 'advanced',
    duration: '20분'
  }
]

// MZ세대 맞춤 타로 질문 템플릿
export const mzQuestionTemplates = [
  '썸타는 그 사람과 연애 가능성은?',
  '이번 달 취업 운세는 어떨까?',
  '부업으로 돈 벌 수 있을까?',
  '이직하면 후회하지 않을까?',
  '오늘 고백하면 성공할까?',
  '투자하려는 종목 어떨까?',
  '새로운 사람 만날 기회 있을까?',
  '지금 연애 계속해도 될까?',
  '창업 아이디어 괜찮을까?',
  '다이어트 성공할 수 있을까?'
]

// 타로 결과 해석 템플릿
export const interpretationTemplates = {
  positive: [
    '완전 긍정적인 결과네요! 👍',
    '이거 진짜 좋은 신호인데요? ✨',
    '대박! 완전 좋은 카드 나왔어요 🎉',
    '우주가 당신을 응원하고 있어요! 🌟'
  ],
  negative: [
    '조금 신중하게 접근하세요 🤔',
    '지금은 기다리는 게 좋을 것 같아요 ⏰',
    '한 번 더 생각해보는 시간이 필요해요 💭',
    '서두르지 말고 천천히 진행하세요 🐌'
  ],
  neutral: [
    '균형을 맞춰가는 것이 중요해요 ⚖️',
    '현재 상황을 잘 유지하세요 🔄',
    '조금 더 지켜보는 것이 좋겠어요 👀',
    '안정적으로 진행하면 될 것 같아요 📈'
  ]
}

// 동서양 퓨전 질문 템플릿 추가
export const koreanFusionQuestions = [
  '사방신의 가호를 받을 수 있을까?',
  '십이지신 중 내 수호신은?',
  '올해 띠별 운세는 어떨까?',
  '동방청룡의 지혜를 얻을 수 있을까?',
  '남방주작의 열정을 받을 수 있을까?',
  '서방백호의 안정을 찾을 수 있을까?',
  '북방현무의 평화를 얻을 수 있을까?',
  '한국형 타로 해석으로 보는 내 운명은?'
]

// 수호신별 카드 필터링 함수
export const getCardsByGuardian = (guardian: string) => {
  return fullTarotDeck.filter(card => card.guardian === guardian)
}

// 십이지신별 카드 필터링 함수  
export const getCardsByZodiac = (zodiacAnimal: string) => {
  return fullTarotDeck.filter(card => card.zodiacAnimal === zodiacAnimal)
}

// Guardian Variant 카드만 필터링
export const getGuardianVariants = () => {
  return fullTarotDeck.filter(card => card.isGuardianVariant === true)
}

export default {
  // 기존 exports
  majorArcanaCards,
  tarotSpreads,
  mzQuestionTemplates,
  interpretationTemplates,
  
  // 새로운 78장 덱 exports
  fullTarotDeck,
  wandsCards,
  cupsCards,
  swordsCards,
  pentaclesCards,
  
  // 동서양 퓨전 exports
  koreanFusionQuestions,
  getCardsByGuardian,
  getCardsByZodiac,
  getGuardianVariants
}