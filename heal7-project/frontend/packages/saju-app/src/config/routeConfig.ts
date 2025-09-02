/**
 * 🗺️ 라우트 설정 및 URL 매핑
 * 기존 페이지 구조를 유지하면서 URL 경로 매핑
 */

import { RouteMapping, RouteInfo } from '../types/routingTypes'

// 🎯 전체 라우트 매핑 (15개 페이지)
export const ROUTE_CONFIG: RouteMapping = {
  dashboard: {
    pageId: 'dashboard',
    path: '/',
    title: '치유마녀 - HEAL-WITCH | 전통 명리학과 AI가 만나는 운세 서비스',
    description: '전통 명리학과 현대 AI 기술이 만나는 새로운 차원의 운세 서비스. 사주명리, 타로카드, 꿈풀이까지 한번에.',
    icon: '🏠',
    label: '메인',
    keywords: ['운세', '사주명리', '타로카드', '꿈풀이', '치유마녀', 'HEAL-WITCH', '띠운세'],
    ogImage: '/og-images/dashboard.png'
  },
  
  saju: {
    pageId: 'saju',
    path: '/saju',
    title: '사주명리 | 치유마녀 - 전통 명리학 AI 해석',
    description: '정통 사주명리학을 기반으로 한 AI 운세 해석. 사주팔자, 대운, 세운 분석으로 인생의 방향을 제시합니다.',
    icon: '🔮',
    label: '사주명리',
    keywords: ['사주', '명리', '팔자', '대운', '세운', '천간', '지지', '오행'],
    ogImage: '/og-images/saju.png'
  },
  
  tarot: {
    pageId: 'tarot',
    path: '/tarot',
    title: '타로카드 | 치유마녀 - 인터랙티브 타로 리딩',
    description: '직관적인 타로카드 해석으로 현재 상황과 미래를 읽어보세요. 다양한 스프레드와 AI 해석 제공.',
    icon: '🃏',
    label: '타로카드',
    keywords: ['타로', '카드', '리딩', '점술', '미래예측', '타로해석'],
    ogImage: '/og-images/tarot.png'
  },
  
  zodiac: {
    pageId: 'zodiac',
    path: '/zodiac',
    title: '띠운세 | 치유마녀 - 12띠별 운세 분석',
    description: '12간지별 상세 운세 분석. 올해 띠운세, 월별 운세, 궁합까지 종합적인 띠별 운명 해석.',
    icon: '🐭',
    label: '띠운세',
    keywords: ['띠운세', '12띠', '간지', '쥐띠', '소띠', '호랑이띠', '토끼띠', '용띠', '뱀띠', '말띠', '양띠', '원숭이띠', '닭띠', '개띠', '돼지띠'],
    ogImage: '/og-images/zodiac.png'
  },
  
  dream: {
    pageId: 'dream',
    path: '/dream',
    title: '꿈풀이 | 치유마녀 - AI 기반 꿈 해석',
    description: '전통 꿈풀이와 현대 심리학이 결합된 AI 꿈 해석. 당신의 꿈이 전하는 메시지를 알아보세요.',
    icon: '🌙',
    label: '꿈풀이',
    keywords: ['꿈풀이', '꿈해석', '꿈의미', '심리분석', '무의식'],
    ogImage: '/og-images/dream.png'
  },
  
  consultation: {
    pageId: 'consultation',
    path: '/consultation',
    title: '상담 | 치유마녀 - 전문가 운세 상담',
    description: '전문 명리학자와의 1:1 개인 상담. 깊이 있는 운세 분석과 인생 상담을 받아보세요.',
    icon: '💬',
    label: '상담',
    keywords: ['상담', '개인상담', '운세상담', '명리상담', '인생상담'],
    ogImage: '/og-images/consultation.png'
  },
  
  fortune: {
    pageId: 'fortune',
    path: '/fortune',
    title: '종합운세 | 치유마녀 - 다각도 운세 분석',
    description: '사주, 타로, 꿈풀이를 통합한 종합적인 운세 분석. 전방위적인 운세 관점을 제공합니다.',
    icon: '⭐',
    label: '종합운세',
    category: 'fortune',
    keywords: ['종합운세', '전체운세', '통합분석', '다각도분석'],
    ogImage: '/og-images/fortune.png'
  },
  
  personality: {
    pageId: 'personality',
    path: '/fortune/personality',
    title: '성격분석 | 치유마녀 - AI 기반 성격 유형 분석',
    description: '사주를 바탕으로 한 정밀한 성격 분석. 당신의 숨겨진 성향과 잠재력을 발견해보세요.',
    icon: '🧠',
    label: '성격분석',
    category: 'fortune',
    keywords: ['성격분석', '성향', '기질', 'MBTI', '성격유형'],
    ogImage: '/og-images/personality.png'
  },
  
  love: {
    pageId: 'love',
    path: '/fortune/love',
    title: '애정운 | 치유마녀 - 사랑과 인연의 운세',
    description: '사랑과 인연에 관한 특별한 운세. 이상형, 만남의 시기, 연애운까지 애정 전반을 다룹니다.',
    icon: '💕',
    label: '애정운',
    category: 'fortune',
    keywords: ['애정운', '연애운', '사랑', '인연', '결혼운', '궁합'],
    ogImage: '/og-images/love.png'
  },
  
  compatibility: {
    pageId: 'compatibility',
    path: '/fortune/compatibility',
    title: '궁합 | 치유마녀 - 사주 기반 인연 분석',
    description: '사주팔자를 통한 정밀한 궁합 분석. 연인, 부부, 친구, 동료와의 인연을 깊이 있게 분석합니다.',
    icon: '💑',
    label: '궁합',
    category: 'fortune',
    keywords: ['궁합', '사주궁합', '인연분석', '상성', '만족도'],
    ogImage: '/og-images/compatibility.png'
  },
  
  calendar: {
    pageId: 'calendar',
    path: '/calendar',
    title: '운세달력 | 치유마녀 - 날짜별 운세 확인',
    description: '매일매일 달라지는 운세를 달력으로 한눈에. 길일, 흉일, 주의사항까지 상세 제공.',
    icon: '📅',
    label: '운세달력',
    keywords: ['운세달력', '일일운세', '길일', '흉일', '택일'],
    ogImage: '/og-images/calendar.png'
  },
  
  magazine: {
    pageId: 'magazine',
    path: '/magazine',
    title: '매거진 | 치유마녀 - 운세 트렌드와 이야기',
    description: '최신 운세 트렌드, 명리학 지식, 재미있는 운세 이야기를 매거진 스타일로 만나보세요.',
    icon: '📰',
    label: '매거진',
    keywords: ['매거진', '운세트렌드', '명리지식', '운세이야기'],
    ogImage: '/og-images/magazine.png'
  },
  
  store: {
    pageId: 'store',
    path: '/store',
    title: '스토어 | 치유마녀 - 운세 관련 상품',
    description: '운세와 관련된 다양한 상품들. 부적, 액세서리, 책자 등 특별한 아이템들을 만나보세요.',
    icon: '🛍️',
    label: '스토어',
    keywords: ['스토어', '상품', '부적', '액세서리', '운세용품'],
    ogImage: '/og-images/store.png'
  },
  
  notices: {
    pageId: 'notices',
    path: '/notices',
    title: '공지사항 | 치유마녀 - 서비스 소식',
    description: '치유마녀 서비스의 최신 소식, 업데이트, 이벤트 정보를 확인하세요.',
    icon: '📢',
    label: '공지사항',
    keywords: ['공지사항', '소식', '업데이트', '이벤트', '서비스'],
    ogImage: '/og-images/notices.png'
  },
  
  profile: {
    pageId: 'profile',
    path: '/profile',
    title: '프로필 | 치유마녀 - 마이페이지',
    description: '개인 운세 히스토리, 즐겨찾기, 게이미피케이션 레벨 등 나만의 운세 공간.',
    icon: '👤',
    label: '프로필',
    keywords: ['프로필', '마이페이지', '개인설정', '히스토리'],
    ogImage: '/og-images/profile.png'
  },
  
  subscription: {
    pageId: 'subscription',
    path: '/notices/subscription',
    title: '구독 서비스 | 치유마녀 - 프리미엄 운세',
    description: '프리미엄 운세 구독 서비스. 더 정확하고 깊이 있는 운세 분석을 정기적으로 받아보세요.',
    icon: '💎',
    label: '구독',
    category: 'notices',
    keywords: ['구독', '프리미엄', '정기운세', '멤버십'],
    ogImage: '/og-images/subscription.png'
  },
  
  admin: {
    pageId: 'admin',
    path: '/admin',
    title: '관리자 | 치유마녀 - Admin Dashboard',
    description: '치유마녀 서비스 관리자 대시보드',
    icon: '⚙️',
    label: '관리자',
    keywords: ['관리자', 'admin', 'dashboard'],
    ogImage: '/og-images/admin.png'
  }
}

// 🔄 URL에서 페이지 ID 찾기 (기존 App.tsx 로직 대체)
export function getPageIdFromPath(pathname: string): keyof RouteMapping | null {
  // 정확한 경로 매칭 우선
  for (const [pageId, config] of Object.entries(ROUTE_CONFIG)) {
    if (config.path === pathname) {
      return pageId as keyof RouteMapping
    }
  }
  
  // 부분 경로 매칭 (하위 경로 지원)
  for (const [pageId, config] of Object.entries(ROUTE_CONFIG)) {
    if (pathname.startsWith(config.path) && config.path !== '/') {
      return pageId as keyof RouteMapping
    }
  }
  
  return null
}

// 📊 페이지별 메타데이터 생성
export function generateMetadata(routeInfo: RouteInfo) {
  return {
    title: routeInfo.title,
    description: routeInfo.description,
    keywords: routeInfo.keywords?.join(', ') || '',
    ogTitle: routeInfo.title,
    ogDescription: routeInfo.description,
    ogImage: routeInfo.ogImage || '/og-images/default.png'
  }
}

// 🎯 네비게이션 그룹 분류 (기존 Navigation.tsx 로직 활용)
export const CORE_NAVIGATION = [
  ROUTE_CONFIG.saju,
  ROUTE_CONFIG.tarot,
  ROUTE_CONFIG.zodiac,
  ROUTE_CONFIG.dream,
  ROUTE_CONFIG.consultation
] as const

export const EXTRA_NAVIGATION = [
  ROUTE_CONFIG.fortune,
  ROUTE_CONFIG.personality,
  ROUTE_CONFIG.love,
  ROUTE_CONFIG.compatibility,
  ROUTE_CONFIG.calendar,
  ROUTE_CONFIG.magazine,
  ROUTE_CONFIG.store,
  ROUTE_CONFIG.notices,
  ROUTE_CONFIG.admin
] as const