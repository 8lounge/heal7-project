// 타로카드 데이터와 시스템

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
    mzInterpretation: '완전 YOLO 모드! 지금이야말로 새로운 걸 시도해볼 때예요 🚀'
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
    mzInterpretation: '지금 당신 완전 주인공 모드! 뭐든 할 수 있을 것 같은 기분이죠? ✨'
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
    mzInterpretation: '지금 당신의 직감이 레전드급! 느낌 오는 대로 가보세요 🔮'
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
    mzInterpretation: '인생 대박 찬스가 온다! 이때 아니면 언제? 🍀'
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
    mzInterpretation: '지금 인생 리셋 타이밍! 과감하게 정리하고 새 출발하세요 🔄'
  }
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

export default {
  majorArcanaCards,
  tarotSpreads,
  mzQuestionTemplates,
  interpretationTemplates
}