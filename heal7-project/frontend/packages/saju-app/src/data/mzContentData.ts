// MZ세대 맞춤 콘텐츠 데이터

export interface DailyFortune {
  id: string
  date: string
  category: 'love' | 'career' | 'money' | 'health' | 'relationship' | 'study'
  emoji: string
  title: string
  subtitle: string
  content: string
  keywords: string[]
  mood: 'positive' | 'neutral' | 'caution' | 'lucky'
  score: number // 1-5
  mzSlang?: string
  shareText: string
}

export interface TrendingTopic {
  id: string
  title: string
  description: string
  emoji: string
  category: string
  popularity: number
  tags: string[]
  createdAt: string
}

export interface MBTIFortune {
  mbti: string
  todayMessage: string
  compatibleMBTI: string[]
  luckyColor: string
  luckyNumber: number
  advice: string
  mood: string
}

export interface AchievementBadge {
  id: string
  name: string
  description: string
  emoji: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
  unlockCondition: string
  isUnlocked: boolean
}

// 오늘의 운세 데이터 (MZ세대 맞춤)
export const dailyFortuneData: DailyFortune[] = [
  {
    id: 'df_001',
    date: '2025-08-25',
    category: 'love',
    emoji: '💕',
    title: '오늘 연애운 레전드 각',
    subtitle: '썸 타던 그 사람한테서 연락올듯',
    content: '오늘은 연애운이 상승세예요! 평소 관심있던 사람과의 관계에 진전이 있을 수 있어요. 너무 밀어붙이지 말고 자연스럽게 흘러가는 대로 두세요. DM 확인도 잊지 마세요! 💌',
    keywords: ['연락', '진전', 'DM체크', '자연스럽게'],
    mood: 'positive',
    score: 4,
    mzSlang: '이거 완전 개꿀이네 ㅋㅋ',
    shareText: '오늘 연애운 진짜 좋다는데... 믿어도 되는 거겠지? 😏💕'
  },
  {
    id: 'df_002',
    date: '2025-08-25',
    category: 'career',
    emoji: '🚀',
    title: '취업운 상승 중! 지원하면 된다',
    subtitle: '이력서 넣을 타이밍이 바로 지금',
    content: '취업 준비생들 주목! 오늘부터 일주일간 취업운이 상당히 좋아요. 미뤄왔던 지원서 작성하고 네트워킹도 적극적으로 해보세요. LinkedIn 활동도 늘려보는 걸 추천! 🎯',
    keywords: ['지원서', '네트워킹', '링크드인', '적극적'],
    mood: 'positive',
    score: 4,
    mzSlang: '이거 진짜 기회 놓치면 안 될듯',
    shareText: '취업운 떴다는데 진짜인가?? 이력서 넣어야겠다 🚀'
  },
  {
    id: 'df_003',
    date: '2025-08-25',
    category: 'money',
    emoji: '💰',
    title: '용돈 벌이 기회가 온다',
    subtitle: '부수입 찬스, 놓치지 마세요',
    content: '오늘은 경제운이 나쁘지 않아요! 사이드 잡이나 알바 기회가 생길 수 있어요. 투자보다는 안정적인 수익에 집중하는 게 좋겠어요. 가상화폐는 조심하시고요! 📈',
    keywords: ['사이드잡', '알바기회', '안정수익', '투자주의'],
    mood: 'positive',
    score: 3,
    mzSlang: '돈이 굴러들어온다는 뜻?',
    shareText: '용돈벌이 기회 온다니까? 진짜 와야 되는데... 💰'
  },
  {
    id: 'df_004',
    date: '2025-08-25',
    category: 'study',
    emoji: '📚',
    title: '집중력 MAX! 공부하기 딱 좋은 날',
    subtitle: '오늘 안 하면 언제 해?',
    content: '학습능력이 평소보다 높아지는 날이에요! 미뤄뒀던 자격증 공부나 새로운 스킬 학습을 시작해보세요. 유튜브 강의보다는 책이나 온라인 강의가 더 효과적일 거예요. 📖',
    keywords: ['자격증', '스킬업', '온라인강의', '집중'],
    mood: 'positive',
    score: 4,
    mzSlang: '공부 안 하면 바보 되는 날',
    shareText: '오늘 공부운 좋다는데 진짜 해야겠다... 📚✨'
  },
  {
    id: 'df_005',
    date: '2025-08-25',
    category: 'relationship',
    emoji: '👥',
    title: '인간관계에서 좋은 소식',
    subtitle: '새로운 인연 or 화해의 기회',
    content: '오늘은 사람들과의 관계에서 긍정적인 변화가 있을 수 있어요. 새로운 친구를 만나거나, 소원했던 사람과 다시 가까워질 기회가 올 수도! 먼저 연락해보는 용기를 내보세요. 💌',
    keywords: ['새친구', '화해', '먼저연락', '용기'],
    mood: 'positive',
    score: 3,
    mzSlang: '인맥 쌓을 기회 왔다',
    shareText: '인간관계운 좋다니까 누구한테 연락해볼까? 👥💕'
  }
]

// 트렌딩 토픽
export const trendingTopics: TrendingTopic[] = [
  {
    id: 'tt_001',
    title: 'MBTI와 사주의 만남',
    description: 'MBTI 성향과 사주팔자를 함께 분석해보는 새로운 트렌드',
    emoji: '🧠',
    category: 'personality',
    popularity: 95,
    tags: ['MBTI', '사주', '성격분석', '자기탐구'],
    createdAt: '2025-08-25'
  },
  {
    id: 'tt_002',
    title: '2025 띠별 운세 대공개',
    description: '올해 가장 운이 좋은 띠는? 띠별 맞춤 조언까지',
    emoji: '🐉',
    category: 'zodiac',
    popularity: 88,
    tags: ['띠운세', '2025년', '신년운세', '맞춤조언'],
    createdAt: '2025-08-24'
  },
  {
    id: 'tt_003',
    title: '타로로 보는 내 연애 스타일',
    description: '3장 뽑기로 알아보는 나만의 연애 패턴',
    emoji: '💕',
    category: 'love',
    popularity: 92,
    tags: ['타로', '연애스타일', '3장뽑기', '연애패턴'],
    createdAt: '2025-08-25'
  },
  {
    id: 'tt_004',
    title: '취준생을 위한 취업운 UP 루틴',
    description: '매일 5분으로 취업운을 올리는 방법',
    emoji: '🚀',
    category: 'career',
    popularity: 76,
    tags: ['취업운', '취준생', '매일루틴', '5분'],
    createdAt: '2025-08-24'
  },
  {
    id: 'tt_005',
    title: 'Z세대가 가장 많이 본 운세는?',
    description: '데이터로 보는 Z세대 운세 트렌드 분석',
    emoji: '📊',
    category: 'trend',
    popularity: 84,
    tags: ['Z세대', '운세트렌드', '데이터분석', '통계'],
    createdAt: '2025-08-23'
  }
]

// MBTI별 오늘의 운세
export const mbtiFortuneData: Record<string, MBTIFortune> = {
  'ENFP': {
    mbti: 'ENFP',
    todayMessage: '새로운 아이디어가 샘솟는 날! 창의력을 마음껏 발휘해보세요 ✨',
    compatibleMBTI: ['INTJ', 'INFJ'],
    luckyColor: '오렌지',
    luckyNumber: 7,
    advice: '너무 많은 일을 한번에 시작하지 말고, 하나씩 차근차근 진행해보세요',
    mood: '에너지 넘치는 하루 🔥'
  },
  'INTJ': {
    mbti: 'INTJ',
    todayMessage: '계획했던 일들이 술술 풀리는 날입니다. 전략적 사고가 빛을 발해요 🎯',
    compatibleMBTI: ['ENFP', 'ENTP'],
    luckyColor: '네이비',
    luckyNumber: 3,
    advice: '완벽을 추구하되 작은 실수에 너무 얽매이지 마세요',
    mood: '집중력 MAX 상태 💪'
  },
  // ... 다른 MBTI 타입들도 추가 가능
}

// 업적 배지 시스템
export const achievementBadges: AchievementBadge[] = [
  {
    id: 'badge_001',
    name: '첫 운세 체크',
    description: '처음으로 운세를 확인했어요!',
    emoji: '🔮',
    rarity: 'common',
    unlockCondition: '첫 운세 확인',
    isUnlocked: true
  },
  {
    id: 'badge_002',
    name: '연속 7일 접속',
    description: '7일 연속으로 접속했어요!',
    emoji: '📅',
    rarity: 'rare',
    unlockCondition: '7일 연속 접속',
    isUnlocked: false
  },
  {
    id: 'badge_003',
    name: '타로 마스터',
    description: '타로카드를 100번 뽑았어요!',
    emoji: '🃏',
    rarity: 'epic',
    unlockCondition: '타로카드 100회 뽑기',
    isUnlocked: false
  },
  {
    id: 'badge_004',
    name: '운세 인플루언서',
    description: '운세를 50번 공유했어요!',
    emoji: '📱',
    rarity: 'legendary',
    unlockCondition: '운세 50회 공유',
    isUnlocked: false
  }
]

// MZ세대 관심사별 운세 카테고리
export const mzCategories = [
  {
    id: 'love',
    name: '연애운',
    emoji: '💕',
    description: '썸, 연애, 이별까지 연애의 모든 것',
    color: 'pink',
    subcategories: ['썸타는중', '연애중', '짝사랑', '이별후', '솔로탈출']
  },
  {
    id: 'career',
    name: '취업/진로운',
    emoji: '🚀',
    description: '취준, 이직, 승진까지 커리어의 모든 것',
    color: 'blue',
    subcategories: ['취업준비', '이직', '승진', '창업', '프리랜서']
  },
  {
    id: 'money',
    name: '재물운',
    emoji: '💰',
    description: '용돈, 투자, 부수입까지 돈의 모든 것',
    color: 'green',
    subcategories: ['용돈벌이', '투자', '부수입', '절약', '대출']
  },
  {
    id: 'study',
    name: '학업/성장운',
    emoji: '📚',
    description: '공부, 자격증, 스킬업까지 성장의 모든 것',
    color: 'purple',
    subcategories: ['시험', '자격증', '어학', '스킬업', '취미']
  },
  {
    id: 'health',
    name: '건강운',
    emoji: '💪',
    description: '몸과 마음의 건강까지',
    color: 'red',
    subcategories: ['다이어트', '운동', '멘탈케어', '수면', '식단']
  },
  {
    id: 'relationship',
    name: '인간관계운',
    emoji: '👥',
    description: '친구, 가족, 직장 관계까지',
    color: 'yellow',
    subcategories: ['친구관계', '가족', '직장동료', '새로운인연', '갈등해결']
  }
]

// 공유 가능한 운세 템플릿
export const shareTemplates = [
  '오늘 {category} 운세가 {score}/5점이래! {emoji}',
  '{title} - {subtitle} {shareText}',
  '치유마녀에서 본 내 운세: {content}',
  '#{category}운 #{mood} #운세 #치유마녀'
]

// 인기 검색어 (실시간)
export const trendingKeywords = [
  '연애운', '취업운', '오늘운세', '타로', '사주',
  'MBTI운세', '띠별운세', '별자리', '꿈해몽', '이름궁합'
]

export default {
  dailyFortuneData,
  trendingTopics,
  mbtiFortuneData,
  achievementBadges,
  mzCategories,
  shareTemplates,
  trendingKeywords
}