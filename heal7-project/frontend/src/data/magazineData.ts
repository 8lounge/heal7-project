// MZ세대 운세 매거진 데이터

export interface MagazineArticle {
  id: string
  title: string
  subtitle: string
  category: 'trend' | 'career' | 'love' | 'lifestyle' | 'interview' | 'guide'
  author: string
  authorImage: string
  publishDate: string
  readTime: string
  coverImage: string
  excerpt: string
  content: string
  tags: string[]
  likes: number
  views: number
  comments: number
  isFeatured: boolean
  isPremium: boolean
}

export interface MagazineCategory {
  id: string
  name: string
  description: string
  icon: string
  color: string
  articleCount: number
}

// 매거진 카테고리
export const magazineCategories: MagazineCategory[] = [
  {
    id: 'trend',
    name: '트렌드',
    description: 'MZ세대 운세 트렌드와 최신 이슈',
    icon: '🔥',
    color: 'from-red-500 to-pink-500',
    articleCount: 24
  },
  {
    id: 'career',
    name: '커리어',
    description: '직장생활과 취업 운세 가이드',
    icon: '💼',
    color: 'from-blue-500 to-indigo-500',
    articleCount: 18
  },
  {
    id: 'love',
    name: '연애',
    description: '사랑과 인간관계 운세 분석',
    icon: '💕',
    color: 'from-pink-500 to-rose-500',
    articleCount: 32
  },
  {
    id: 'lifestyle',
    name: '라이프스타일',
    description: '일상 속 운세와 개운 팁',
    icon: '✨',
    color: 'from-purple-500 to-indigo-500',
    articleCount: 15
  },
  {
    id: 'interview',
    name: '인터뷰',
    description: '운세 전문가와 셀럽 인터뷰',
    icon: '🎤',
    color: 'from-green-500 to-teal-500',
    articleCount: 8
  },
  {
    id: 'guide',
    name: '가이드',
    description: '초보자를 위한 운세 기초 가이드',
    icon: '📖',
    color: 'from-amber-500 to-orange-500',
    articleCount: 12
  }
]

// 샘플 매거진 기사들
export const magazineArticles: MagazineArticle[] = [
  {
    id: 'trend-001',
    title: '2025년 MZ세대가 가장 많이 본 운세 키워드 TOP 10',
    subtitle: '사주에서 타로까지, 올해 핫했던 운세 트렌드 총정리',
    category: 'trend',
    author: '운세킹 에디터',
    authorImage: '👨‍💻',
    publishDate: '2025-08-20',
    readTime: '5분',
    coverImage: '🔥',
    excerpt: '2025년 상반기, MZ세대들이 가장 관심을 가진 운세 키워드들을 분석해봤습니다. 취업운부터 연애운까지...',
    content: `
# 2025년 MZ세대 운세 트렌드 분석 🔥

## 1위: "취업운" - 현실적 고민이 1순위
- 검색량: 전년 대비 340% 증가
- 주요 연령: 23-28세
- 핫 키워드: "이직", "연봉", "스타트업"

## 2위: "연애운" - 솔로탈출 열망 여전
- 검색량: 전년 대비 280% 증가  
- 주요 키워드: "썸", "MBTI 궁합", "이상형"

## 3위: "부동산운" - 영끌의 시대
- 검색량: 전년 대비 150% 증가
- 주요 키워드: "집값", "전세", "투자 타이밍"

...더 자세한 분석은 프리미엄 구독으로 확인하세요! 💎
    `,
    tags: ['#MZ세대', '#운세트렌드', '#2025년', '#취업운', '#연애운'],
    likes: 1248,
    views: 15730,
    comments: 89,
    isFeatured: true,
    isPremium: false
  },
  {
    id: 'career-002',
    title: '이직하기 좋은 달은 언제? AI가 분석한 사주별 최적 타이밍',
    subtitle: 'ChatGPT도 놀란 사주 기반 커리어 전략',
    category: 'career',
    author: '커리어운세연구소',
    authorImage: '👩‍💼',
    publishDate: '2025-08-18',
    readTime: '8분',
    coverImage: '📊',
    excerpt: 'AI 분석을 통해 각 사주별로 이직하기 가장 좋은 시기를 찾아드립니다. 당신의 커리어 업그레이드를 위한...',
    content: `
# AI × 사주로 찾는 최적 이직 타이밍 🤖

## 목(木) 사주 - 3월, 8월이 기회
- **3월**: 새싹이 돋는 계절, 새로운 시작에 최적
- **8월**: 성장 에너지 최고조, 면접 합격률 30% 상승
- **피해야 할 시기**: 11월-1월 (휴면기)

## 화(火) 사주 - 5월, 9월 추천  
- **5월**: 열정 에너지 활성화, 적극적 어필 가능
- **9월**: 실행력 최대, 빠른 결정에 유리
- **주의사항**: 겨울철 이직은 신중하게

## 토(土) 사주 - 6월, 9월이 안정적
...더 보기 (프리미엄 콘텐츠) 🔒
    `,
    tags: ['#이직', '#AI분석', '#사주', '#커리어', '#타이밍'],
    likes: 892,
    views: 12450,
    comments: 156,
    isFeatured: false,
    isPremium: true
  },
  {
    id: 'love-003',
    title: '소개팅 전 필수 체크! MBTI별 첫인상 운세 가이드',
    subtitle: '첫 만남에서 호감도 200% 올리는 비법',
    category: 'love',
    author: '연애의신',
    authorImage: '💕',
    publishDate: '2025-08-15',
    readTime: '6분',
    coverImage: '💘',
    excerpt: 'MBTI와 사주를 결합한 첫인상 전략! 소개팅에서 호감도를 극대화하는 노하우를 공개합니다...',
    content: `
# MBTI × 사주로 완성하는 소개팅 필승법 💘

## ENFP + 목(木) 사주 조합
- **패션**: 밝은 색상, 자연스러운 스타일 추천
- **대화법**: 흥미진진한 경험담으로 어필
- **주의사항**: 너무 많은 얘기보다 경청도 중요

## INTJ + 금(金) 사주 조합
- **패션**: 모던하고 깔끔한 룩 추천  
- **대화법**: 깊이 있는 주제로 지적 매력 어필
- **팁**: 계획적인 데이트 코스 제안하기

## 소개팅 운세별 최적 장소 🗺️
- **연애운 상승기**: 카페, 갤러리, 공원 산책
- **연애운 하강기**: 맛집, 영화관 (안전한 선택)
- **운세 중립기**: 액티비티 (볼링, 방탈출 등)

...각 MBTI별 세부 전략은 프리미엄에서! 💎
    `,
    tags: ['#소개팅', '#MBTI', '#첫인상', '#연애운', '#호감도'],
    likes: 2156,
    views: 28940,
    comments: 267,
    isFeatured: true,
    isPremium: false
  },
  {
    id: 'lifestyle-004', 
    title: '집안 인테리어로 금전운 올리기! 풍수 인테리어 완전정복',
    subtitle: '작은 변화로 만드는 럭키 하우스',
    category: 'lifestyle',
    author: '풍수인테리어마스터',
    authorImage: '🏠',
    publishDate: '2025-08-12',
    readTime: '7분',
    coverImage: '✨',
    excerpt: '월세방에서도 할 수 있는 간단한 풍수 인테리어로 금전운을 업그레이드해보세요...',
    content: `
# 금전운 상승하는 인테리어 꿀팁 ✨

## 현관 - 돈이 들어오는 입구
- **거울 배치**: 현관 옆면에 설치 (정면은 금기!)
- **조명**: 따뜻한 색온도 LED 추천
- **식물**: 금전수, 개운죽으로 생기 충전

## 침실 - 재물이 쌓이는 공간  
- **침대 방향**: 문에서 대각선 방향이 최적
- **색상**: 베이지, 연한 핑크로 안정감 UP
- **수납**: 침대 아래 정리정돈 필수

## 작업 공간 - 수입 창구
- **책상 위치**: 벽을 등지고 문이 보이는 자리
- **아이템**: 수정, 황금 소품으로 금전운 강화
- **정리**: 좌측에 성장하는 식물 배치

## 원룸러를 위한 특별 팁 🏠
...더 자세한 가이드는 프리미엄에서! 
    `,
    tags: ['#풍수', '#인테리어', '#금전운', '#원룸', '#정리정돈'],
    likes: 743,
    views: 9820,
    comments: 92,
    isFeatured: false,
    isPremium: true
  },
  {
    id: 'interview-005',
    title: '[독점 인터뷰] 유명 유튜버가 말하는 "운세와 콘텐츠 창작"',
    subtitle: '구독자 100만 크리에이터의 운세 활용법',
    category: 'interview',
    author: '치유마녀 에디터팀',
    authorImage: '🎤',
    publishDate: '2025-08-10',
    readTime: '12분',
    coverImage: '🌟',
    excerpt: '유명 크리에이터가 직접 말하는 운세와 창작의 관계. 영감이 막힐 때 사용하는 비법까지...',
    content: `
# 크리에이터가 말하는 운세의 힘 🌟

## 인터뷰이: 김크리에이터 (유튜브 구독자 120만)

**Q: 콘텐츠 창작에 운세를 어떻게 활용하시나요?**

**A:** 저는 매주 월요일마다 주간 운세를 확인해요. 특히 창작운이 좋은 날에는 중요한 기획을 잡고, 소통운이 좋을 때는 라이브를 진행하죠. 실제로 조회수 차이가 30% 이상 나더라고요! 

**Q: 가장 신기했던 경험이 있다면?**

**A:** 사주를 보고 "8월에 큰 기회가 온다"는 말을 들었는데, 정말 그 달에 대기업 협업 제안이 들어왔어요. 우연의 일치일 수도 있지만, 마음 준비가 되어 있어서 더 좋은 결과를 낼 수 있었던 것 같아요.

**Q: MZ세대에게 운세를 추천하는 이유는?**

**A:** 빠르게 변하는 시대에 나만의 기준점이 필요하잖아요. 운세가 그런 역할을 해준다고 생각해요. 맹신하지 말고, 하나의 가이드라인으로 활용하면 도움이 많이 돼요.

...전체 인터뷰는 프리미엄에서! 💎
    `,
    tags: ['#인터뷰', '#유튜버', '#크리에이터', '#콘텐츠', '#운세활용'],
    likes: 1567,
    views: 21340,
    comments: 198,
    isFeatured: true,
    isPremium: false
  }
]

// 에디터 추천 기사
export const editorsPick = [
  'trend-001',
  'love-003', 
  'interview-005'
]

// 인기 태그
export const popularTags = [
  '#MZ세대', '#취업운', '#연애운', '#사주', '#타로', 
  '#MBTI', '#이직', '#소개팅', '#인테리어', '#크리에이터',
  '#AI분석', '#트렌드', '#가이드', '#팁', '#후기'
]

export default {
  magazineCategories,
  magazineArticles,
  editorsPick,
  popularTags
}