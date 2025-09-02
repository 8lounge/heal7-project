// 시스템 관련 데이터 (공지사항, 인증, 구독)

export interface Notice {
  id: string
  type: 'system' | 'event' | 'update' | 'maintenance' | 'promotion'
  title: string
  content: string
  summary: string
  publishDate: string
  isImportant: boolean
  isPinned: boolean
  views: number
  author: string
  tags: string[]
  attachments?: { name: string; url: string; size: string }[]
  relatedLinks?: { title: string; url: string }[]
}

export interface User {
  id: string
  email: string
  username: string
  avatar: string
  joinDate: string
  lastLogin: string
  subscriptionType: 'free' | 'premium' | 'vip'
  subscriptionExpiry?: string
  profile: {
    birthDate?: string
    gender?: 'M' | 'F'
    interests: string[]
    favoriteConsultants: string[]
    consultationHistory: number
    totalSpent: number
    level: number
    badges: string[]
  }
  preferences: {
    notifications: boolean
    emailUpdates: boolean
    smsAlerts: boolean
    theme: 'light' | 'dark' | 'auto'
    language: 'ko' | 'en'
  }
}

export interface SubscriptionPlan {
  id: string
  name: string
  description: string
  price: number
  originalPrice: number
  discount: number
  duration: 'monthly' | 'yearly'
  features: string[]
  limitations: string[]
  isPopular: boolean
  color: string
  icon: string
  badge?: string
  benefits: {
    consultations: number | 'unlimited'
    magazines: boolean
    premiumContent: boolean
    aiReports: number | 'unlimited'
    prioritySupport: boolean
    customAnalysis: boolean
    exclusiveEvents: boolean
  }
}

// 공지사항 목록
export const notices: Notice[] = [
  {
    id: 'notice-001',
    type: 'system',
    title: '🎉 치유마녀 플랫폼 2.0 업데이트 완료!',
    content: `
# 치유마녀 플랫폼 2.0 주요 업데이트 사항 ✨

안녕하세요! 치유마녀 운영팀입니다.

MZ세대 맞춤형 운세 플랫폼으로 대대적인 리뉴얼을 완료했습니다!

## 🆕 새로운 기능들

### 1. AI 맞춤 사주 분석 시스템
- ChatGPT 기반 개인별 맞춤 분석
- MZ세대 트렌드 반영한 현실적 조언
- 취업/연애/재테크 특화 해석

### 2. 인터랙티브 타로 시스템  
- 3D 카드 뽑기 애니메이션
- 실시간 카드 해석
- 소셜 공유 기능 추가

### 3. 매거진 서비스 런칭
- 매주 업데이트되는 운세 트렌드 기사
- 유명 크리에이터 인터뷰
- MZ세대 맞춤 콘텐츠

### 4. 1:1 전문가 상담 시스템
- 실시간 채팅/영상 상담
- 전문가 프로필 및 후기 시스템
- 다양한 상담 패키지

## 🎁 론칭 기념 이벤트

1. **신규 가입 시 프리미엄 1개월 무료**
2. **첫 상담 50% 할인**
3. **AI 사주분석서 무료 체험**

감사합니다! 💜
    `,
    summary: '치유마녀 플랫폼 2.0 업데이트 완료! AI 사주분석, 타로, 매거진, 1:1 상담 등 새로운 기능 추가',
    publishDate: '2025-08-25',
    isImportant: true,
    isPinned: true,
    views: 15420,
    author: '치유마녀 운영팀',
    tags: ['#업데이트', '#신기능', '#이벤트'],
    relatedLinks: [
      { title: 'AI 사주분석 체험하기', url: '/saju' },
      { title: '매거진 둘러보기', url: '/magazine' }
    ]
  },
  {
    id: 'notice-002',
    type: 'event',
    title: '📚 신학기 대박 운세 이벤트 (8/25~9/30)',
    content: `
# 📚 신학기 대박 운세 이벤트

새 학기를 맞아 특별한 이벤트를 준비했습니다!

## 🎯 이벤트 혜택

### 대학생/신입사원 특가
- **취업운 프로그램**: 40% 할인
- **신입생 스타터 패키지**: 50% 할인
- **전문가 상담**: 첫 회 무료

### 추가 혜택
- 친구 추천 시 양쪽 모두 포인트 적립
- 후기 작성 시 다음 상담 20% 할인
- SNS 공유 시 추가 할인 쿠폰

## 📅 이벤트 기간
2025년 8월 25일 ~ 9월 30일

## 🎁 참여 방법
1. 회원 가입 후 학생 인증
2. 원하는 상품/서비스 선택  
3. 결제 시 쿠폰 적용

많은 참여 부탁드립니다! ✨
    `,
    summary: '신학기 맞이 특가 이벤트! 대학생/신입사원 대상 최대 50% 할인 + 다양한 혜택',
    publishDate: '2025-08-25',
    isImportant: true,
    isPinned: true,
    views: 8930,
    author: '이벤트팀',
    tags: ['#신학기', '#할인', '#이벤트', '#학생특가'],
    attachments: [
      { name: '신학기_이벤트_상세안내.pdf', url: '/files/event-detail.pdf', size: '2.3MB' }
    ]
  },
  {
    id: 'notice-003',
    type: 'update',
    title: '🔧 시스템 점검 안내 (8/27 새벽 2~4시)',
    content: `
# 정기 시스템 점검 안내 🔧

안정적인 서비스 제공을 위한 정기 점검을 실시합니다.

## 📅 점검 일시
- **일시**: 2025년 8월 27일(화) 새벽 2:00 ~ 4:00
- **소요시간**: 약 2시간 예상

## 🚫 점검 중 이용 불가 서비스
- 전체 웹사이트 접속
- 모바일 앱 이용
- 1:1 상담 서비스
- 결제 시스템

## ✅ 점검 후 개선사항
- 사이트 속도 30% 향상
- 새로운 AI 모델 적용
- 보안 강화
- 모바일 최적화

이용에 불편을 드려 죄송합니다.
더 나은 서비스로 보답하겠습니다! 🙏
    `,
    summary: '8/27(화) 새벽 2~4시 정기 시스템 점검으로 서비스 일시 중단. 점검 후 성능 개선 예정',
    publishDate: '2025-08-24',
    isImportant: true,
    isPinned: false,
    views: 3240,
    author: '기술팀',
    tags: ['#시스템점검', '#서비스중단', '#업데이트']
  },
  {
    id: 'notice-004',
    type: 'promotion',
    title: '💎 프리미엄 멤버십 런칭! 첫 달 무료 체험',
    content: `
# 💎 치유마녀 프리미엄 멤버십 런칭!

더 깊이 있는 운세 서비스를 원하시는 분들을 위해 프리미엄 멤버십을 출시합니다!

## 🌟 프리미엄 혜택

### 무제한 서비스
- AI 사주분석 무제한 이용
- 전문가 상담 월 3회 무료
- 프리미엄 매거진 콘텐츠 이용

### 특별 혜택  
- 신규 기능 우선 체험
- VIP 고객 전용 이벤트 참여
- 24시간 우선 고객지원

### 개인 맞춤 서비스
- 월 1회 개인별 종합 운세 리포트
- 중요 일정 운세 알림 서비스
- 개운법 맞춤 추천

## 💰 요금 안내
- **월간 요금**: 19,900원/월
- **연간 요금**: 199,000원/년 (2개월 무료!)

## 🎁 런칭 기념 혜택
**첫 달 완전 무료 체험!**
지금 가입하시면 30일 동안 무료로 이용 가능합니다.

지금 바로 프리미엄의 차이를 경험해보세요! ✨
    `,
    summary: '프리미엄 멤버십 런칭! 무제한 AI 분석, 전문가 상담, 특별 혜택 제공. 첫 달 무료 체험 가능',
    publishDate: '2025-08-22',
    isImportant: false,
    isPinned: false,
    views: 12750,
    author: '마케팅팀',
    tags: ['#프리미엄', '#멤버십', '#무료체험', '#런칭']
  },
  {
    id: 'notice-005',
    type: 'system',
    title: '📱 치유마녀 모바일 앱 출시 예정!',
    content: `
# 📱 치유마녀 모바일 앱 곧 출시!

언제 어디서나 편리하게! 치유마녀 모바일 앱이 곧 출시됩니다.

## 🚀 앱 특별 기능

### 푸시 알림
- 개인별 맞춤 운세 알림
- 중요한 날짜 미리 알림
- 상담 예약 알림

### 오프라인 기능
- 다운로드한 콘텐츠 오프라인 이용
- 즐겨찾기 기능
- 히스토리 관리

### 모바일 최적화  
- 터치 친화적 UI/UX
- 빠른 로딩 속도
- 배터리 최적화

## 📅 출시 일정
- **안드로이드**: 9월 중 출시 예정
- **iOS**: 10월 중 출시 예정

## 🎁 앱 출시 기념 이벤트
- 사전 예약자 대상 특별 혜택
- 첫 주 다운로드 시 포인트 적립
- 앱 전용 할인 쿠폰 제공

많은 기대 부탁드립니다! 📲
    `,
    summary: '치유마녀 모바일 앱 9월 안드로이드, 10월 iOS 출시 예정. 푸시 알림, 오프라인 기능 등 추가',
    publishDate: '2025-08-20',
    isImportant: false,
    isPinned: false,
    views: 6820,
    author: '개발팀',
    tags: ['#모바일앱', '#출시예정', '#안드로이드', '#iOS']
  }
]

// 구독 요금제
export const subscriptionPlans: SubscriptionPlan[] = [
  {
    id: 'free',
    name: '무료 회원',
    description: '기본적인 운세 서비스를 무료로 이용하세요',
    price: 0,
    originalPrice: 0,
    discount: 0,
    duration: 'monthly',
    features: [
      '일일 운세 확인',
      '기본 사주 분석 (월 1회)',
      '타로카드 뽑기 (일 3회)',
      '매거진 무료 기사 열람',
      '커뮤니티 참여 가능'
    ],
    limitations: [
      'AI 상세 분석 제한',
      '전문가 상담 불가',
      '프리미엄 콘텐츠 제한',
      '광고 포함'
    ],
    isPopular: false,
    color: 'from-gray-400 to-gray-500',
    icon: '🆓',
    benefits: {
      consultations: 0,
      magazines: false,
      premiumContent: false,
      aiReports: 1,
      prioritySupport: false,
      customAnalysis: false,
      exclusiveEvents: false
    }
  },
  {
    id: 'premium',
    name: '프리미엄',
    description: 'MZ세대가 가장 많이 선택하는 플랜',
    price: 19900,
    originalPrice: 35000,
    discount: 43,
    duration: 'monthly',
    features: [
      '무제한 AI 사주 분석',
      '전문가 상담 월 3회',
      '프리미엄 매거진 이용',
      '개인 맞춤 운세 리포트',
      '상세 궁합 분석',
      '운세 캘린더 알림',
      '광고 제거'
    ],
    limitations: [
      'VIP 상담사 이용 제한',
      '일부 프리미엄 기능 제한'
    ],
    isPopular: true,
    color: 'from-purple-500 to-pink-500',
    icon: '💎',
    badge: '인기',
    benefits: {
      consultations: 3,
      magazines: true,
      premiumContent: true,
      aiReports: 'unlimited',
      prioritySupport: true,
      customAnalysis: true,
      exclusiveEvents: false
    }
  },
  {
    id: 'vip',
    name: 'VIP',
    description: '최고급 운세 서비스의 모든 것',
    price: 49900,
    originalPrice: 80000,
    discount: 38,
    duration: 'monthly',
    features: [
      '모든 프리미엄 혜택 포함',
      '무제한 전문가 상담',
      'VIP 전용 상담사 배정',
      '개인별 종합 운세서 (월 1회)',
      '중요 일정 맞춤 컨설팅',
      'VIP 전용 이벤트 참여',
      '24시간 우선 고객지원',
      '맞춤 개운법 추천'
    ],
    limitations: [],
    isPopular: false,
    color: 'from-amber-400 to-yellow-500',
    icon: '👑',
    badge: '최고급',
    benefits: {
      consultations: 'unlimited',
      magazines: true,
      premiumContent: true,
      aiReports: 'unlimited',
      prioritySupport: true,
      customAnalysis: true,
      exclusiveEvents: true
    }
  }
]

// 샘플 사용자 데이터
export const sampleUser: User = {
  id: 'user-sample',
  email: 'mz@example.com',
  username: 'MZ세대운세러',
  avatar: '😊',
  joinDate: '2025-07-15',
  lastLogin: '2025-08-25',
  subscriptionType: 'premium',
  subscriptionExpiry: '2025-09-15',
  profile: {
    birthDate: '1998-05-20',
    gender: 'F',
    interests: ['사주', '타로', '연애운', '취업운'],
    favoriteConsultants: ['consultant-001', 'consultant-002'],
    consultationHistory: 12,
    totalSpent: 280000,
    level: 3,
    badges: ['첫 상담 완료', '프리미엄 가입', '매거진 애독자', '후기 작성왕']
  },
  preferences: {
    notifications: true,
    emailUpdates: true,
    smsAlerts: false,
    theme: 'auto',
    language: 'ko'
  }
}

// 소셜 로그인 옵션
export const socialLoginOptions = [
  {
    id: 'kakao',
    name: '카카오 로그인',
    icon: '💬',
    color: 'bg-yellow-400 hover:bg-yellow-500',
    textColor: 'text-gray-900'
  },
  {
    id: 'naver',
    name: '네이버 로그인', 
    icon: 'N',
    color: 'bg-green-500 hover:bg-green-600',
    textColor: 'text-white'
  },
  {
    id: 'google',
    name: '구글 로그인',
    icon: 'G',
    color: 'bg-white hover:bg-gray-100 border border-gray-300',
    textColor: 'text-gray-700'
  },
  {
    id: 'apple',
    name: 'Apple 로그인',
    icon: '🍎',
    color: 'bg-black hover:bg-gray-800',
    textColor: 'text-white'
  }
]

export default {
  notices,
  subscriptionPlans,
  sampleUser,
  socialLoginOptions
}