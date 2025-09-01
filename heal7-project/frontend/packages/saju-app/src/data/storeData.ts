// 운세 스토어 데이터

export interface Product {
  id: string
  name: string
  description: string
  category: 'digital' | 'physical' | 'service' | 'bundle'
  subcategory: string
  price: number
  originalPrice: number
  discount: number
  rating: number
  reviewCount: number
  salesCount: number
  images: string[]
  tags: string[]
  features: string[]
  isPopular: boolean
  isBestseller: boolean
  isNew: boolean
  deliveryInfo: string
  digitalDelivery?: boolean
  estimatedDelivery?: string
  stock?: number
  variants?: { name: string; price: number; stock: number }[]
}

export interface StoreCategory {
  id: string
  name: string
  description: string
  icon: string
  color: string
  productCount: number
  subcategories: string[]
}

// 스토어 카테고리
export const storeCategories: StoreCategory[] = [
  {
    id: 'digital',
    name: '디지털 콘텐츠',
    description: '즉시 다운로드 가능한 디지털 상품',
    icon: '📱',
    color: 'from-blue-500 to-indigo-500',
    productCount: 45,
    subcategories: ['사주분석서', 'AI 운세리포트', '타로카드 해석', '개운법 가이드', '명상 콘텐츠']
  },
  {
    id: 'physical',
    name: '실물 상품',
    description: '배송으로 받는 운세 관련 실물 상품',
    icon: '📦',
    color: 'from-green-500 to-teal-500',
    productCount: 28,
    subcategories: ['타로카드', '수정/원석', '부적/액세서리', '풍수용품', '도서']
  },
  {
    id: 'service',
    name: '서비스',
    description: '전문가 상담 및 맞춤 서비스',
    icon: '🎯',
    color: 'from-purple-500 to-pink-500',
    productCount: 12,
    subcategories: ['개인상담', '그룹상담', '맞춤제작', 'VIP 서비스']
  },
  {
    id: 'bundle',
    name: '패키지',
    description: '여러 상품을 묶은 할인 패키지',
    icon: '🎁',
    color: 'from-amber-500 to-orange-500',
    productCount: 15,
    subcategories: ['스타터 패키지', '프리미엄 패키지', '시즌 한정']
  }
]

// 상품 목록
export const products: Product[] = [
  {
    id: 'digital-001',
    name: 'AI 맞춤 사주분석서 (2025년 특별판)',
    description: 'ChatGPT와 전통 사주학을 결합한 개인 맞춤형 분석서. MZ세대를 위한 현실적이고 실용적인 조언 포함.',
    category: 'digital',
    subcategory: '사주분석서',
    price: 19900,
    originalPrice: 35000,
    discount: 43,
    rating: 4.8,
    reviewCount: 892,
    salesCount: 5640,
    images: ['🤖', '📊', '✨'],
    tags: ['#AI분석', '#MZ세대', '#2025년', '#현실조언', '#즉시다운로드'],
    features: [
      '30페이지 전문 분석서',
      '개인별 맞춤 개운법 10가지',
      '월별 운세 캘린더 포함',
      '취업/연애/재물운 상세 분석',
      '평생 무료 업데이트',
      'PDF + 모바일 최적화'
    ],
    isPopular: true,
    isBestseller: true,
    isNew: false,
    deliveryInfo: '결제 후 즉시 이메일 발송',
    digitalDelivery: true
  },
  {
    id: 'physical-002',
    name: '한정판 골드 타로카드 (MZ에디션)',
    description: 'MZ세대를 위해 새롭게 디자인된 한정판 타로카드. 모던하고 직관적인 해석 가이드북 포함.',
    category: 'physical',
    subcategory: '타로카드',
    price: 45000,
    originalPrice: 65000,
    discount: 31,
    rating: 4.9,
    reviewCount: 324,
    salesCount: 1280,
    images: ['🃏', '✨', '📚'],
    tags: ['#한정판', '#MZ디자인', '#프리미엄', '#가이드북포함'],
    features: [
      '78장 풀 타로카드',
      'MZ세대 맞춤 해석서',
      '고급 벨벳 파우치 포함',
      '카드별 QR코드 해석',
      '작가 사인 인증서',
      '한정 1000세트만 제작'
    ],
    isPopular: false,
    isBestseller: false,
    isNew: true,
    deliveryInfo: '무료배송 (2-3일 소요)',
    digitalDelivery: false,
    estimatedDelivery: '2-3일',
    stock: 127
  },
  {
    id: 'digital-003',
    name: '연애운 상승 21일 챌린지',
    description: '21일 동안 매일 실천하는 연애운 상승 프로그램. 실제 성공 사례 95% 이상의 검증된 방법.',
    category: 'digital',
    subcategory: '개운법 가이드',
    price: 12900,
    originalPrice: 25000,
    discount: 48,
    rating: 4.7,
    reviewCount: 1567,
    salesCount: 8920,
    images: ['💕', '📅', '🎯'],
    tags: ['#연애운', '#21일챌린지', '#성공률95%', '#검증된방법'],
    features: [
      '21일 일별 실천 가이드',
      '매일 개운법 알림 메시지',
      '진도 체크 앱 연동',
      '성공 스토리 사례집',
      '개인 맞춤 피드백',
      '실패 시 100% 환불 보장'
    ],
    isPopular: true,
    isBestseller: false,
    isNew: false,
    deliveryInfo: '결제 후 즉시 이용 가능',
    digitalDelivery: true
  },
  {
    id: 'physical-004',
    name: '금전운 상승 수정 팔찌 (천연 시트린)',
    description: '브라질산 천연 시트린으로 제작한 금전운 팔찌. 개인별 사주에 맞는 크기와 색상으로 맞춤 제작.',
    category: 'physical',
    subcategory: '수정/원석',
    price: 89000,
    originalPrice: 120000,
    discount: 26,
    rating: 4.6,
    reviewCount: 234,
    salesCount: 567,
    images: ['💎', '✋', '💰'],
    tags: ['#천연시트린', '#맞춤제작', '#금전운', '#브라질산'],
    features: [
      '브라질산 AAA급 시트린',
      '개인 손목 사이즈 맞춤',
      '사주별 맞춤 디자인',
      '정품 인증서 포함',
      '평생 A/S 보장',
      '고급 보석 케이스 포함'
    ],
    isPopular: false,
    isBestseller: true,
    isNew: false,
    deliveryInfo: '맞춤 제작으로 7-10일 소요',
    digitalDelivery: false,
    estimatedDelivery: '7-10일',
    stock: 45,
    variants: [
      { name: '14mm', price: 89000, stock: 15 },
      { name: '16mm', price: 95000, stock: 20 },
      { name: '18mm', price: 105000, stock: 10 }
    ]
  },
  {
    id: 'service-005',
    name: 'VIP 전용 운세 상담 (1시간)',
    description: '국내 최고 전문가와의 1:1 프리미엄 상담. 인생의 중요한 결정을 앞둔 분들을 위한 특별 서비스.',
    category: 'service',
    subcategory: 'VIP 서비스',
    price: 150000,
    originalPrice: 200000,
    discount: 25,
    rating: 5.0,
    reviewCount: 89,
    salesCount: 245,
    images: ['👑', '🎯', '📞'],
    tags: ['#VIP전용', '#최고전문가', '#1시간상담', '#프리미엄'],
    features: [
      '국내 최고 전문가 배정',
      '60분 집중 상담',
      '상담 내용 녹음 파일 제공',
      '상세 분석서 별도 제공',
      '1개월 후속 상담 무료',
      '24시간 우선 예약 가능'
    ],
    isPopular: false,
    isBestseller: false,
    isNew: false,
    deliveryInfo: '예약 후 24시간 내 상담 가능',
    digitalDelivery: false
  },
  {
    id: 'bundle-006',
    name: '신입생 운세 스타터 패키지',
    description: '대학생이나 신입사원을 위한 운세 입문 패키지. 기본기부터 실전까지 한 번에!',
    category: 'bundle',
    subcategory: '스타터 패키지',
    price: 39900,
    originalPrice: 75000,
    discount: 47,
    rating: 4.8,
    reviewCount: 456,
    salesCount: 2130,
    images: ['🎓', '📦', '🌟'],
    tags: ['#신입생특가', '#스타터패키지', '#기본부터실전', '#올인원'],
    features: [
      'AI 사주분석서',
      '미니 타로카드 세트',
      '개운법 실천 가이드',
      '1개월 전문가 상담권',
      '운세 앱 프리미엄 이용권',
      '학습용 동영상 강의 10편'
    ],
    isPopular: true,
    isBestseller: false,
    isNew: true,
    deliveryInfo: '디지털+실물 혼합배송',
    digitalDelivery: false,
    estimatedDelivery: '3-5일'
  },
  {
    id: 'digital-007',
    name: '취업운 극대화 30일 프로그램',
    description: '면접 성공률 85% 향상! 취업 준비생을 위한 체계적인 운세 관리 프로그램.',
    category: 'digital',
    subcategory: 'AI 운세리포트',
    price: 24900,
    originalPrice: 40000,
    discount: 38,
    rating: 4.9,
    reviewCount: 723,
    salesCount: 3450,
    images: ['💼', '📈', '🎯'],
    tags: ['#취업운', '#면접성공', '#30일프로그램', '#성공률85%'],
    features: [
      '개인별 취업운 분석',
      '면접 최적 날짜 추천',
      '복장/색상 가이드',
      '자기소개서 첨삭 포인트',
      '모의면접 운세 코칭',
      '성공 후기 사례집'
    ],
    isPopular: true,
    isBestseller: true,
    isNew: false,
    deliveryInfo: '결제 후 즉시 시작',
    digitalDelivery: true
  },
  {
    id: 'physical-008',
    name: '책상 위 미니 풍수 인테리어 세트',
    description: '좁은 공간에서도 풍수 효과를 볼 수 있는 미니 인테리어 세트. 재택근무족 필수템!',
    category: 'physical',
    subcategory: '풍수용품',
    price: 35000,
    originalPrice: 55000,
    discount: 36,
    rating: 4.5,
    reviewCount: 167,
    salesCount: 890,
    images: ['🖥️', '🌱', '✨'],
    tags: ['#미니풍수', '#책상인테리어', '#재택근무', '#소형공간'],
    features: [
      '미니 금전수 화분',
      '수정 원석 3종 세트',
      '풍수 나침반',
      '배치 가이드북',
      '개운 스티커 10장',
      '관리 방법 동영상'
    ],
    isPopular: false,
    isBestseller: false,
    isNew: true,
    deliveryInfo: '무료배송 (식물 특별포장)',
    digitalDelivery: false,
    estimatedDelivery: '2-4일',
    stock: 78
  }
]

// 베스트셀러 상품 ID
export const bestsellers = [
  'digital-001',
  'digital-007', 
  'physical-004',
  'bundle-006'
]

// 신상품 ID
export const newProducts = [
  'physical-002',
  'bundle-006',
  'physical-008'
]

// 할인 이벤트
export const saleEvents = [
  {
    id: 'event-001',
    name: '신학기 대박 세일',
    description: '대학생/신입사원 대상 최대 50% 할인',
    discount: 50,
    endDate: '2025-09-30',
    targetProducts: ['bundle-006', 'digital-007'],
    bannerColor: 'from-green-500 to-blue-500'
  },
  {
    id: 'event-002', 
    name: '연애운 상승 위크',
    description: '연애 관련 상품 특가 + 무료 상담권 증정',
    discount: 30,
    endDate: '2025-08-31',
    targetProducts: ['digital-003'],
    bannerColor: 'from-pink-500 to-red-500'
  }
]

// 고객 리뷰 샘플
export const productReviews = [
  {
    id: 'review-p001',
    productId: 'digital-001',
    username: '취준생파이팅',
    rating: 5,
    content: 'AI 분석 정말 정확해요! 면접 날짜 추천받은 대로 했더니 정말 합격했어요 ㅠㅠ 믿고 사세요',
    date: '2025-08-20',
    verified: true,
    helpful: 45
  },
  {
    id: 'review-p002',
    productId: 'physical-002',
    username: '타로초보',
    rating: 5,
    content: '카드 퀄리티가 정말 좋아요! 디자인도 예쁘고 해석서도 이해하기 쉬워서 초보한테 딱이에요',
    date: '2025-08-18',
    verified: true,
    helpful: 32
  },
  {
    id: 'review-p003',
    productId: 'digital-003',
    username: '솔로탈출성공',
    rating: 4,
    content: '21일 챌린지 하니까 정말 변화가 있더라고요! 자신감도 생기고 실제로 소개팅에서 좋은 결과 있었어요👍',
    date: '2025-08-15',
    verified: true,
    helpful: 67
  }
]

// 추천 상품 조합
export const recommendedCombos = [
  {
    mainProductId: 'digital-001',
    comboProducts: ['digital-007', 'service-005'],
    discount: 15,
    title: '취업 완전 정복 패키지'
  },
  {
    mainProductId: 'physical-002',
    comboProducts: ['digital-003', 'physical-004'],
    discount: 20,
    title: '연애운 올인원 세트'
  }
]

export default {
  storeCategories,
  products,
  bestsellers,
  newProducts,
  saleEvents,
  productReviews,
  recommendedCombos
}