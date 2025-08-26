// 1:1 운세 상담 시스템 데이터

export interface Consultant {
  id: string
  name: string
  nickname: string
  avatar: string
  specialties: string[]
  experience: number // 년수
  rating: number
  reviewCount: number
  consultationCount: number
  pricePerMinute: number
  isOnline: boolean
  introduction: string
  credentials: string[]
  availableHours: {
    [key: string]: { start: string; end: string }[] // 요일별 가능 시간
  }
  consultationMethods: ('chat' | 'voice' | 'video')[]
  languages: string[]
  responseTime: string // 평균 응답 시간
  tags: string[]
}

export interface Review {
  id: string
  consultantId: string
  userId: string
  username: string
  userAvatar: string
  rating: number
  content: string
  date: string
  consultationType: 'chat' | 'voice' | 'video'
  isVerified: boolean
  likes: number
  category: string
  tags: string[]
}

export interface ConsultationPackage {
  id: string
  name: string
  description: string
  duration: number // 분
  price: number
  originalPrice: number
  discount: number
  features: string[]
  isPopular: boolean
  consultationType: 'chat' | 'voice' | 'video'
  category: string
}

// 상담사 목록
export const consultants: Consultant[] = [
  {
    id: 'consultant-001',
    name: '김운세',
    nickname: '사주마스터',
    avatar: '👨‍🎓',
    specialties: ['사주명리', '운세분석', '인생상담'],
    experience: 15,
    rating: 4.9,
    reviewCount: 2847,
    consultationCount: 8520,
    pricePerMinute: 300,
    isOnline: true,
    introduction: '15년간 3만명 이상을 상담한 사주명리 전문가입니다. MZ세대의 고민을 현실적으로 해결해드립니다.',
    credentials: ['한국사주명리학회 정회원', '동양철학 박사', 'KBS 출연'],
    availableHours: {
      '월': [{ start: '09:00', end: '18:00' }],
      '화': [{ start: '09:00', end: '18:00' }],
      '수': [{ start: '09:00', end: '18:00' }],
      '목': [{ start: '09:00', end: '18:00' }],
      '금': [{ start: '09:00', end: '18:00' }],
      '토': [{ start: '10:00', end: '16:00' }],
      '일': [{ start: '14:00', end: '18:00' }]
    },
    consultationMethods: ['chat', 'voice', 'video'],
    languages: ['한국어', '영어'],
    responseTime: '평균 2분',
    tags: ['#사주전문가', '#15년경력', '#MZ세대특화', '#현실조언']
  },
  {
    id: 'consultant-002', 
    name: '이타로',
    nickname: '타로여신',
    avatar: '👩‍🔮',
    specialties: ['타로카드', '연애운', '진로상담'],
    experience: 8,
    rating: 4.8,
    reviewCount: 1923,
    consultationCount: 5640,
    pricePerMinute: 250,
    isOnline: true,
    introduction: '연애와 진로 고민에 특화된 타로 전문가. 솔직하고 따뜻한 상담으로 유명합니다.',
    credentials: ['국제타로협회 인증', '심리상담사 2급', '유튜브 구독자 50만'],
    availableHours: {
      '월': [{ start: '14:00', end: '22:00' }],
      '화': [{ start: '14:00', end: '22:00' }],
      '수': [{ start: '14:00', end: '22:00' }],
      '목': [{ start: '14:00', end: '22:00' }],
      '금': [{ start: '14:00', end: '22:00' }],
      '토': [{ start: '10:00', end: '20:00' }],
      '일': [{ start: '10:00', end: '20:00' }]
    },
    consultationMethods: ['chat', 'video'],
    languages: ['한국어'],
    responseTime: '평균 1분',
    tags: ['#타로전문', '#연애특화', '#유튜버', '#솔직상담']
  },
  {
    id: 'consultant-003',
    name: '박운명',
    nickname: 'AI운세박사',
    avatar: '👨‍💻',
    specialties: ['AI 사주분석', '데이터 운세', '투자운'],
    experience: 5,
    rating: 4.7,
    reviewCount: 892,
    consultationCount: 3120,
    pricePerMinute: 400,
    isOnline: false,
    introduction: 'AI와 전통 사주를 결합한 차세대 운세 분석가. 투자와 재테크 상담이 특기입니다.',
    credentials: ['데이터사이언스 박사', 'AI 운세 개발자', '투자상담사'],
    availableHours: {
      '월': [{ start: '19:00', end: '23:00' }],
      '수': [{ start: '19:00', end: '23:00' }],
      '금': [{ start: '19:00', end: '23:00' }],
      '토': [{ start: '09:00', end: '17:00' }]
    },
    consultationMethods: ['chat', 'video'],
    languages: ['한국어', '영어'],
    responseTime: '평균 5분',
    tags: ['#AI분석', '#투자운', '#데이터기반', '#차세대']
  },
  {
    id: 'consultant-004',
    name: '정신점',
    nickname: '신점할매',
    avatar: '👵',
    specialties: ['신점', '굿', '부적'],
    experience: 30,
    rating: 4.6,
    reviewCount: 3456,
    consultationCount: 12000,
    pricePerMinute: 200,
    isOnline: true,
    introduction: '30년 전통의 신점 전문가. 어려운 문제도 신령님의 힘으로 해결해드립니다.',
    credentials: ['무속인 자격증', '30년 경력', '전국 신당 네트워크'],
    availableHours: {
      '월': [{ start: '06:00', end: '18:00' }],
      '화': [{ start: '06:00', end: '18:00' }],
      '수': [{ start: '06:00', end: '18:00' }],
      '목': [{ start: '06:00', end: '18:00' }],
      '금': [{ start: '06:00', end: '18:00' }],
      '토': [{ start: '06:00', end: '18:00' }]
    },
    consultationMethods: ['voice'],
    languages: ['한국어'],
    responseTime: '평균 10분',
    tags: ['#신점전통', '#30년경력', '#부적', '#굿상담']
  }
]

// 상담 후기
export const reviews: Review[] = [
  {
    id: 'review-001',
    consultantId: 'consultant-001',
    userId: 'user-001',
    username: '취준생김씨',
    userAvatar: '😊',
    rating: 5,
    content: '취업 준비하면서 너무 막막했는데, 정확한 분석과 현실적인 조언 덕분에 방향을 잡을 수 있었어요. 특히 이력서 쓸 때 강점 위주로 어필하라는 말씀이 정말 도움됐습니다! 실제로 면접 3곳 다 붙었어요 ㅠㅠ',
    date: '2025-08-15',
    consultationType: 'video',
    isVerified: true,
    likes: 127,
    category: '취업/진로',
    tags: ['#취업성공', '#현실조언', '#정확분석']
  },
  {
    id: 'review-002', 
    consultantId: 'consultant-002',
    userId: 'user-002',
    username: '연애고수wannabe',
    userAvatar: '💕',
    rating: 5,
    content: '3년 사귄 남친과의 미래가 고민됐는데, 타로 결과가 너무 정확해서 소름돋았어요ㅋㅋ 솔직한 조언도 좋았고, 제가 놓치고 있던 부분들을 정확히 집어주셔서 관계 개선에 큰 도움이 됐어요! 이제 결혼 얘기도 나오고 있어요😍',
    date: '2025-08-12',
    consultationType: 'chat',
    isVerified: true,
    likes: 89,
    category: '연애/결혼',
    tags: ['#연애성공', '#정확한타로', '#솔직상담']
  },
  {
    id: 'review-003',
    consultantId: 'consultant-003',
    userId: 'user-003',
    username: '코인부자되고싶다',
    userAvatar: '💰',
    rating: 4,
    content: 'AI 분석 정말 신기해요! 제 투자 성향이랑 운세를 데이터로 분석해주시니까 더 믿음이 가더라고요. 비트코인 타이밍도 잘 맞춰서 수익 좀 봤습니다👍 다만 가격이 좀 비싼 게 아쉬워요',
    date: '2025-08-10',
    consultationType: 'video',
    isVerified: true,
    likes: 156,
    category: '재테크/투자',
    tags: ['#AI분석', '#투자성공', '#데이터기반']
  },
  {
    id: 'review-004',
    consultantId: 'consultant-004',
    userId: 'user-004',
    username: '할매믿음',
    userAvatar: '🙏',
    rating: 5,
    content: '집안에 우울한 기운이 계속 돌았는데, 할매님이 굿 추천해주시고 부적도 받아서 정말 좋아졌어요. 가족들 건강도 다 회복되고, 뭔가 집 분위기도 밝아진 느낌? 전통의 힘을 느꼈습니다🙏',
    date: '2025-08-08',
    consultationType: 'voice',
    isVerified: true,
    likes: 203,
    category: '가족/건강',
    tags: ['#전통신점', '#굿효과', '#부적', '#가족운']
  }
]

// 상담 패키지
export const consultationPackages: ConsultationPackage[] = [
  {
    id: 'package-basic',
    name: '기본 상담',
    description: '간단한 고민 해결을 위한 기본 패키지',
    duration: 15,
    price: 4500,
    originalPrice: 6000,
    discount: 25,
    features: ['15분 상담', '기본 분석서 제공', '1회 후속 질문 가능'],
    isPopular: false,
    consultationType: 'chat',
    category: 'basic'
  },
  {
    id: 'package-standard',
    name: '표준 상담',
    description: 'MZ세대가 가장 많이 선택하는 패키지',
    duration: 30,
    price: 8100,
    originalPrice: 12000,
    discount: 33,
    features: ['30분 집중 상담', '상세 분석서 제공', '3회 후속 질문', '녹화본 제공'],
    isPopular: true,
    consultationType: 'video',
    category: 'standard'
  },
  {
    id: 'package-premium',
    name: '프리미엄 상담',
    description: '인생 전환점에 필요한 깊이 있는 상담',
    duration: 60,
    price: 15000,
    originalPrice: 24000,
    discount: 38,
    features: ['60분 심화 상담', '종합 운세 분석서', '1개월 후속 상담', '개인 맞춤 개운법', '24시간 질문 답변'],
    isPopular: false,
    consultationType: 'video',
    category: 'premium'
  },
  {
    id: 'package-couple',
    name: '커플 상담',
    description: '연인이나 부부를 위한 특별 패키지',
    duration: 45,
    price: 12000,
    originalPrice: 18000,
    discount: 33,
    features: ['커플 궁합 분석', '관계 개선 가이드', '2주 후속 상담', '개별 상담도 가능'],
    isPopular: false,
    consultationType: 'video',
    category: 'couple'
  }
]

// 상담 카테고리
export const consultationCategories = [
  { id: 'career', name: '취업/진로', icon: '💼', count: 1247 },
  { id: 'love', name: '연애/결혼', icon: '💕', count: 2156 },
  { id: 'money', name: '재물/투자', icon: '💰', count: 894 },
  { id: 'health', name: '건강/가족', icon: '🏥', count: 567 },
  { id: 'general', name: '종합운세', icon: '🔮', count: 1832 },
  { id: 'business', name: '사업/창업', icon: '🚀', count: 423 }
]

// 인기 시간대
export const popularTimeSlots = [
  { time: '09:00-12:00', label: '오전', popularity: 65 },
  { time: '14:00-17:00', label: '오후', popularity: 85 },
  { time: '19:00-22:00', label: '저녁', popularity: 95 },
  { time: '22:00-24:00', label: '야간', popularity: 70 }
]

export default {
  consultants,
  reviews,
  consultationPackages,
  consultationCategories,
  popularTimeSlots
}