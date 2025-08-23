import { 
  Compass, 
  Eye,
  ArrowRight,
  Heart,
  Mountain,
  Sun,
  Star,
  Sparkles,
  Moon,
  Leaf,
  ShoppingCart,
  NewspaperIcon,
  BookMarked,
  Gem,
  Crown
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import Navigation from './Navigation'
import Footer from './Footer'

// 신비스럽고 철학적인 브랜드 정체성
const brandPhilosophy = {
  mainSlogan: "운명을 읽고, 삶을 쓰다",
  subSlogans: [
    "천년의 지혜, 당신만의 여정",
    "별이 말하고, 마음이 듣다",
    "타고난 것을 알고, 만들어갈 것을 선택하다",
    "우주의 언어를 해독하는 곳",
    "신비로운 지혜가 현실이 되는 공간"
  ]
}

// 핵심 사주 서비스 (기존 + 강화)
const sajuServices = [
  {
    icon: Eye,
    title: '자아 발견',
    subtitle: '내면의 나를 만나다',
    description: '타고난 본성과 잠재력을 발견하여 진정한 자아를 찾아가는 첫걸음',
    philosophy: '사주는 당신이 누구인지 알려주는 거울입니다',
    features: ['본성과 기질 탐구', '숨겨진 재능 발견', '성격의 빛과 그림자', '자아실현의 방향'],
    price: '무료',
    href: '/saju/basic',
    color: 'primary',
    gradient: 'from-blue-600 to-purple-600'
  },
  {
    icon: Heart,
    title: '관계의 조화',
    subtitle: '사랑 속에서 성장하다',
    description: '진정한 사랑은 서로를 이해하는 것에서 시작됩니다',
    philosophy: '둘이 하나가 되는 것이 아니라, 하나하나가 온전해지는 것',
    features: ['마음의 언어 이해', '갈등의 근원 파악', '성장하는 사랑', '조화로운 관계'],
    price: '₩5,000',
    href: '/saju/compatibility',
    color: 'accent',
    gradient: 'from-pink-500 to-rose-500'
  },
  {
    icon: Mountain,
    title: '성공의 길',
    subtitle: '천직을 찾아 걷다',
    description: '당신만의 성공 패턴을 찾아 지속 가능한 성취를 이루어가세요',
    philosophy: '성공은 목적지가 아니라 여정입니다',
    features: ['타고난 사업 감각', '성공의 타이밍', '협력의 지혜', '지속 가능한 성장'],
    price: '₩10,000',
    href: '/saju/business',
    color: 'secondary',
    gradient: 'from-amber-500 to-orange-500'
  },
  {
    icon: Sun,
    title: '시간의 흐름',
    subtitle: '계절처럼 변화하다',
    description: '인생의 리듬을 이해하고 각 시기에 맞는 지혜로운 선택을 하세요',
    philosophy: '모든 것에는 때가 있고, 모든 목적에는 시절이 있다',
    features: ['계절별 에너지', '성장의 시기', '휴식의 지혜', '변화의 준비'],
    price: '₩15,000',
    href: '/saju/yearly',
    color: 'primary',
    gradient: 'from-yellow-400 to-orange-400'
  }
]

// 새로운 신비학 서비스들
const mysticalServices = [
  {
    icon: Star,
    title: '타로 리딩',
    subtitle: '카드가 전하는 메시지',
    description: '78장의 타로카드를 통해 현재 상황과 미래의 가능성을 탐구합니다',
    philosophy: '카드는 우연이 아닌 필연의 언어입니다',
    features: ['현재 상황 분석', '미래 가능성 탐구', '숨겨진 메시지 해독', '행동 지침 제공'],
    price: '₩8,000',
    href: '/tarot',
    color: 'primary',
    gradient: 'from-indigo-500 to-purple-600',
    isNew: true
  },
  {
    icon: Leaf,
    title: '사상체질 진단',
    subtitle: '나만의 체질 찾기',
    description: '태양인, 태음인, 소양인, 소음인 - 당신의 타고난 체질을 발견하세요',
    philosophy: '몸과 마음은 하나, 체질을 알면 건강한 삶의 길이 보입니다',
    features: ['체질별 특성 분석', '건강 관리법 제공', '음식 궁합 가이드', '라이프스타일 조언'],
    price: '₩7,000',
    href: '/sasang',
    color: 'accent',
    gradient: 'from-green-500 to-emerald-600',
    isNew: true
  },
  {
    icon: Moon,
    title: '서양 별자리',
    subtitle: '별들이 속삭이는 이야기',
    description: '12개 별자리와 행성의 움직임을 통해 당신의 성격과 운명을 알아보세요',
    philosophy: '우리는 모두 별의 자녀, 하늘에 새겨진 이야기를 읽어봅니다',
    features: ['별자리별 성격 분석', '행성의 영향력', '월간 운세 제공', '궁합 분석'],
    price: '₩6,000',
    href: '/astrology',
    color: 'secondary',
    gradient: 'from-blue-400 to-cyan-500',
    isNew: true
  },
  {
    icon: Compass,
    title: '풍수지리',
    subtitle: '공간의 에너지 읽기',
    description: '집과 사무실의 기운을 개선하여 운을 높이는 풍수지리 컨설팅',
    philosophy: '공간은 운명을 바꾸는 힘이 있습니다',
    features: ['공간 에너지 진단', '가구 배치 조언', '색채 치료법', '개운법 제시'],
    price: '₩12,000',
    href: '/fengshui',
    color: 'primary',
    gradient: 'from-teal-500 to-green-600',
    isNew: true
  }
]

// 스토어 상품들
const storeProducts = [
  {
    icon: Gem,
    title: '천연 크리스탈',
    description: '에너지 정화와 개운을 위한 천연 수정들',
    price: '₩15,000~',
    image: '💎',
    badge: 'HOT'
  },
  {
    icon: BookMarked,
    title: '사주 해석서',
    description: '전문가가 직접 쓴 개인 맞춤 사주 해석서',
    price: '₩25,000',
    image: '📜',
    badge: 'BEST'
  },
  {
    icon: Crown,
    title: '개운 팔찌',
    description: '개인 사주에 맞춘 맞춤형 개운 팔찌',
    price: '₩35,000',
    image: '📿',
    badge: 'NEW'
  },
  {
    icon: Star,
    title: '타로카드 세트',
    description: '초보자를 위한 타로카드와 해석 가이드북',
    price: '₩18,000',
    image: '🔮',
    badge: ''
  }
]

// 매거진 콘텐츠
const magazineArticles = [
  {
    category: '사주 이야기',
    title: '2024년 갑진년, 청룡의 해에 주목할 운세 포인트',
    excerpt: '올해는 특히 변화와 도전의 해입니다. 각 띠별로 어떤 에너지를 활용해야 할까요?',
    readTime: '5분 읽기',
    date: '2024.03.15',
    author: '김명리',
    image: '🐉'
  },
  {
    category: '타로 가이드',
    title: '초보자를 위한 타로카드 기초 - 메이저 아르카나 22장 완벽 정리',
    excerpt: '바보부터 세계까지, 인생의 여정을 담은 메이저 아르카나의 깊은 의미를 탐구해봅니다.',
    readTime: '8분 읽기',
    date: '2024.03.12',
    author: '이타로',
    image: '🎭'
  },
  {
    category: '건강 관리',
    title: '사상체질별 봄철 건강관리법 - 체질에 맞는 음식과 운동',
    excerpt: '봄이 되면서 각 체질별로 어떤 점에 주의하고 어떤 음식을 섭취해야 할지 알아봅시다.',
    readTime: '6분 읽기',
    date: '2024.03.10',
    author: '박체질',
    image: '🌸'
  },
  {
    category: '별자리 운세',
    title: '3월 별자리별 사랑운 - 금성의 움직임이 가져오는 변화',
    excerpt: '이달 금성의 특별한 움직임이 12개 별자리에게 어떤 사랑의 메시지를 전할까요?',
    readTime: '4분 읽기',
    date: '2024.03.08',
    author: '최별자리',
    image: '💕'
  }
]


const ViteSajuMain = () => {
  const navigate = useNavigate()
  
  const handleNavigation = (href: string) => {
    navigate(href)
  }

  return (
    <div className="min-h-screen bg-heal7-surface">
      <Navigation />
      
      {/* 동적 배경 효과 */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-heal7-primary/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '0s'}}></div>
        <div className="absolute top-3/4 right-1/4 w-48 h-48 bg-heal7-secondary/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/2 left-1/3 w-32 h-32 bg-heal7-accent/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
        <div className="absolute bottom-1/4 right-1/3 w-56 h-56 bg-purple-500/5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '6s'}}></div>
      </div>
      {/* Hero Section - 신비스럽고 장엄한 인트로 */}
      <section className="section-heal7-hero relative overflow-hidden min-h-screen flex items-center">
        {/* 마법같은 배경 그라데이션 */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/20 via-purple-900/20 to-pink-900/20" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(var(--heal7-secondary),0.15),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_80%,rgba(var(--heal7-accent),0.15),transparent_50%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_0deg_at_50%_50%,transparent_0deg,rgba(var(--heal7-primary),0.1)_60deg,transparent_120deg)]" />
        
        {/* 신비로운 파티클 효과 */}
        <div className="absolute inset-0">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white/20 rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${3 + Math.random() * 4}s`
              }}
            />
          ))}
        </div>
        
        <div className="container relative z-10">
          <div className="mx-auto max-w-6xl text-center">
            {/* 신비로운 브랜드 아이콘 */}
            <div className="mb-12 flex justify-center animate-heal7-scale-in">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full blur-2xl opacity-40 scale-150 animate-pulse"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 rounded-full blur-xl opacity-30 scale-125 animate-pulse" style={{animationDelay: '1s'}}></div>
                <div className="relative bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-full p-8 shadow-2xl border border-white/20">
                  <Compass className="h-20 w-20 text-white drop-shadow-lg" />
                </div>
              </div>
            </div>
            
            {/* 장엄한 메인 슬로건 */}
            <div className="mb-8 animate-heal7-fade-in">
              <h1 className="text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold tracking-tight mb-6">
                <span className="bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
                  {brandPhilosophy.mainSlogan}
                </span>
              </h1>
              <div className="text-2xl md:text-3xl lg:text-4xl text-heal7-muted font-medium opacity-90">
                {brandPhilosophy.subSlogans[0]}
              </div>
            </div>
            
            {/* 신비로운 설명 */}
            <div className="mb-16 max-w-4xl mx-auto animate-heal7-fade-in" style={{animationDelay: '0.2s'}}>
              <p className="text-xl md:text-2xl text-heal7-muted leading-relaxed mb-8">
                사주는 당신의 <strong className="bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent font-bold">운명을 읽어주는 나침반</strong>입니다.<br />
                하지만 실제 <strong className="bg-gradient-to-r from-orange-500 to-pink-500 bg-clip-text text-transparent font-bold">삶은 당신이 써내려가는 이야기</strong>입니다.
              </p>
              <p className="text-lg md:text-xl text-heal7-muted opacity-80">
                🌟 천년의 지혜와 현대적 성찰이 만나는 곳에서 당신만의 여정을 시작하세요 🌟
              </p>
            </div>
            
            {/* 마법같은 CTA 버튼들 */}
            <div className="flex flex-col sm:flex-row justify-center gap-6 mb-12 animate-heal7-fade-in" style={{animationDelay: '0.4s'}}>
              <button 
                onClick={() => handleNavigation('/saju/basic')}
                className="relative group px-10 py-5 text-xl font-semibold text-white rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-100 group-hover:opacity-90"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="relative flex items-center gap-3">
                  <Sparkles className="h-6 w-6" />
                  자아 발견의 여정 시작하기
                  <ArrowRight className="h-6 w-6 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>
              <button 
                onClick={() => handleNavigation('/store')}
                className="relative group px-10 py-5 text-xl font-semibold text-white rounded-2xl border-2 border-white/30 backdrop-blur-sm transition-all duration-300 hover:scale-105 hover:bg-white/10"
              >
                <div className="flex items-center gap-3">
                  <ShoppingCart className="h-6 w-6" />
                  신비용품 둘러보기
                </div>
              </button>
            </div>
            
            {/* 마법같은 부가 슬로건들 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto animate-heal7-fade-in" style={{animationDelay: '0.6s'}}>
              {brandPhilosophy.subSlogans.slice(1).map((slogan, index) => (
                <div key={index} className="glass-heal7 rounded-xl p-4 text-heal7-muted opacity-80 hover:opacity-100 transition-opacity">
                  ✨ {slogan}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* 핵심 사주 서비스 - 신비로운 디자인 */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-white via-blue-50/30 to-purple-50/30"></div>
        <div className="container relative z-10">
          <div className="mx-auto max-w-4xl text-center mb-20">
            <div className="mb-8 animate-heal7-fade-in">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
                자아실현을 위한 <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">신비로운 여정</span>
              </h2>
              <p className="text-xl md:text-2xl text-heal7-muted leading-relaxed">
                🌟 각각의 여정은 당신만의 고유한 성장 이야기입니다 🌟
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {sajuServices.map((service, index) => (
              <div
                key={service.title}
                className="relative group animate-heal7-fade-in overflow-hidden"
                style={{ animationDelay: `${index * 0.15}s` }}
              >
                {/* 카드 배경 */}
                <div className="absolute inset-0 bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl group-hover:shadow-3xl transition-all duration-500"></div>
                <div className={`absolute inset-0 bg-gradient-to-br ${service.gradient} opacity-0 group-hover:opacity-10 transition-all duration-500 rounded-3xl`}></div>
                
                {/* 카드 내용 */}
                <div className="relative p-8">
                  {/* 서비스 헤더 */}
                  <div className="flex items-start justify-between mb-8">
                    <div className="flex items-center space-x-4">
                      <div className="relative">
                        <div className={`absolute inset-0 bg-gradient-to-br ${service.gradient} rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity scale-110`}></div>
                        <div className={`relative bg-gradient-to-br ${service.gradient} rounded-2xl p-4 shadow-lg`}>
                          <service.icon className="h-8 w-8 text-white drop-shadow-sm" />
                        </div>
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900 group-hover:text-purple-700 transition-colors">
                          {service.title}
                        </h3>
                        <p className="text-heal7-muted font-medium text-lg">
                          {service.subtitle}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                        {service.price}
                      </div>
                    </div>
                  </div>
                  
                  {/* 철학적 설명 */}
                  <div className="mb-8">
                    <p className="text-heal7-muted leading-relaxed mb-4 text-lg">
                      {service.description}
                    </p>
                    <div className={`bg-gradient-to-r ${service.gradient} bg-opacity-10 rounded-xl p-5 border-l-4 border-opacity-60`} style={{borderColor: service.gradient.split(' ')[1]}}>
                      <p className="text-heal7-muted italic font-medium">
                        💫 "{service.philosophy}"
                      </p>
                    </div>
                  </div>
                  
                  {/* 특징 목록 */}
                  <div className="mb-10">
                    <div className="grid grid-cols-2 gap-4">
                      {service.features.map((feature, i) => (
                        <div key={i} className="flex items-center space-x-3">
                          <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${service.gradient}`}></div>
                          <span className="text-heal7-muted font-medium">
                            {feature}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* CTA 버튼 */}
                  <button
                    onClick={() => handleNavigation(service.href)}
                    className={`w-full relative group/btn py-4 px-8 text-lg font-semibold text-white rounded-2xl overflow-hidden transition-all duration-300 hover:scale-[1.02] shadow-lg hover:shadow-xl`}
                  >
                    <div className={`absolute inset-0 bg-gradient-to-r ${service.gradient}`}></div>
                    <div className="relative flex items-center justify-center gap-2">
                      ✨ 여정 시작하기
                      <ArrowRight className="h-5 w-5 group-hover/btn:translate-x-1 transition-transform" />
                    </div>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* 신비학 서비스 섹션 */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-purple-900/5 via-indigo-900/5 to-blue-900/5"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-1/4 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '0s'}}></div>
          <div className="absolute bottom-0 right-1/4 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '3s'}}></div>
        </div>
        
        <div className="container relative z-10">
          <div className="mx-auto max-w-4xl text-center mb-20">
            <div className="mb-8 animate-heal7-fade-in">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
                <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  신비학의 다양한 세계
                </span>
              </h2>
              <p className="text-xl md:text-2xl text-heal7-muted leading-relaxed">
                🔮 타로, 별자리, 체질, 풍수 - 고대의 지혜가 현대와 만나다 🔮
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {mysticalServices.map((service, index) => (
              <div
                key={service.title}
                className="relative group animate-heal7-fade-in overflow-hidden"
                style={{ animationDelay: `${index * 0.15}s` }}
              >
                {service.isNew && (
                  <div className="absolute top-4 right-4 z-20 bg-gradient-to-r from-pink-500 to-rose-500 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg">
                    NEW ✨
                  </div>
                )}
                
                {/* 카드 배경 */}
                <div className="absolute inset-0 bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl group-hover:shadow-3xl transition-all duration-500"></div>
                <div className={`absolute inset-0 bg-gradient-to-br ${service.gradient} opacity-0 group-hover:opacity-15 transition-all duration-500 rounded-3xl`}></div>
                
                {/* 카드 내용 */}
                <div className="relative p-8">
                  {/* 서비스 헤더 */}
                  <div className="flex items-start justify-between mb-8">
                    <div className="flex items-center space-x-4">
                      <div className="relative">
                        <div className={`absolute inset-0 bg-gradient-to-br ${service.gradient} rounded-2xl blur-lg opacity-40 group-hover:opacity-60 transition-opacity scale-110`}></div>
                        <div className={`relative bg-gradient-to-br ${service.gradient} rounded-2xl p-4 shadow-lg`}>
                          <service.icon className="h-8 w-8 text-white drop-shadow-sm" />
                        </div>
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900 group-hover:text-indigo-700 transition-colors">
                          {service.title}
                        </h3>
                        <p className="text-heal7-muted font-medium text-lg">
                          {service.subtitle}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                        {service.price}
                      </div>
                    </div>
                  </div>
                  
                  {/* 철학적 설명 */}
                  <div className="mb-8">
                    <p className="text-heal7-muted leading-relaxed mb-4 text-lg">
                      {service.description}
                    </p>
                    <div className={`bg-gradient-to-r ${service.gradient} bg-opacity-10 rounded-xl p-5 border-l-4`} style={{borderColor: service.gradient.split(' ')[1]}}>
                      <p className="text-heal7-muted italic font-medium">
                        🌟 "{service.philosophy}"
                      </p>
                    </div>
                  </div>
                  
                  {/* 특징 목록 */}
                  <div className="mb-10">
                    <div className="grid grid-cols-2 gap-4">
                      {service.features.map((feature, i) => (
                        <div key={i} className="flex items-center space-x-3">
                          <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${service.gradient}`}></div>
                          <span className="text-heal7-muted font-medium">
                            {feature}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* CTA 버튼 */}
                  <button
                    onClick={() => handleNavigation(service.href)}
                    className={`w-full relative group/btn py-4 px-8 text-lg font-semibold text-white rounded-2xl overflow-hidden transition-all duration-300 hover:scale-[1.02] shadow-lg hover:shadow-xl`}
                  >
                    <div className={`absolute inset-0 bg-gradient-to-r ${service.gradient}`}></div>
                    <div className="relative flex items-center justify-center gap-2">
                      🔮 체험해보기
                      <ArrowRight className="h-5 w-5 group-hover/btn:translate-x-1 transition-transform" />
                    </div>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* 스토어 섹션 */}
      <section className="py-24 relative overflow-hidden bg-gradient-to-b from-gray-50 to-white">
        <div className="container relative z-10">
          <div className="mx-auto max-w-4xl text-center mb-20">
            <div className="mb-8 animate-heal7-fade-in">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
                <span className="bg-gradient-to-r from-green-600 via-teal-600 to-blue-600 bg-clip-text text-transparent">
                  신비로운 아이템 스토어
                </span>
              </h2>
              <p className="text-xl md:text-2xl text-heal7-muted leading-relaxed">
                💎 영적 성장과 개운을 위한 특별한 아이템들 💎
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto mb-12">
            {storeProducts.map((product, index) => (
              <div
                key={product.title}
                className="relative group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden animate-heal7-fade-in hover:scale-[1.02]"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {product.badge && (
                  <div className="absolute top-3 right-3 z-10 bg-gradient-to-r from-red-500 to-pink-500 text-white px-2 py-1 rounded-full text-xs font-bold">
                    {product.badge}
                  </div>
                )}
                
                {/* 상품 이미지 영역 */}
                <div className="h-32 bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center text-6xl">
                  {product.image}
                </div>
                
                <div className="p-6">
                  <div className="flex items-center gap-3 mb-3">
                    <product.icon className="h-6 w-6 text-purple-600" />
                    <h3 className="text-lg font-bold text-gray-900">
                      {product.title}
                    </h3>
                  </div>
                  <p className="text-heal7-muted mb-4 leading-relaxed">
                    {product.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent">
                      {product.price}
                    </span>
                    <button className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:scale-105 transition-transform">
                      구매하기
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <button 
              onClick={() => handleNavigation('/store')}
              className="relative group px-10 py-4 text-lg font-semibold text-white rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-teal-600"></div>
              <div className="relative flex items-center gap-3">
                <ShoppingCart className="h-6 w-6" />
                스토어 전체보기
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </div>
            </button>
          </div>
        </div>
      </section>
      
      {/* 매거진 섹션 */}
      <section className="py-24 relative overflow-hidden bg-gradient-to-b from-indigo-50/50 to-purple-50/50">
        <div className="container relative z-10">
          <div className="mx-auto max-w-4xl text-center mb-20">
            <div className="mb-8 animate-heal7-fade-in">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
                <span className="bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 bg-clip-text text-transparent">
                  HEAL7 매거진
                </span>
              </h2>
              <p className="text-xl md:text-2xl text-heal7-muted leading-relaxed">
                📚 신비학과 영성에 관한 깊이 있는 인사이트 📚
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto mb-12">
            {magazineArticles.map((article, index) => (
              <div
                key={article.title}
                className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden animate-heal7-fade-in hover:scale-[1.02]"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="h-40 bg-gradient-to-br from-orange-100 to-pink-100 flex items-center justify-center text-8xl">
                  {article.image}
                </div>
                
                <div className="p-8">
                  <div className="flex items-center justify-between mb-4">
                    <span className="bg-gradient-to-r from-orange-500 to-pink-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                      {article.category}
                    </span>
                    <span className="text-heal7-muted text-sm">
                      {article.readTime}
                    </span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-orange-600 transition-colors leading-tight">
                    {article.title}
                  </h3>
                  
                  <p className="text-heal7-muted leading-relaxed mb-6">
                    {article.excerpt}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-heal7-muted">
                      <span className="font-semibold">{article.author}</span>
                      <span className="mx-2">•</span>
                      <span>{article.date}</span>
                    </div>
                    <button className="text-orange-600 hover:text-orange-700 font-semibold text-sm flex items-center gap-1 group-hover:gap-2 transition-all">
                      읽어보기
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <button 
              onClick={() => handleNavigation('/magazine')}
              className="relative group px-10 py-4 text-lg font-semibold text-white rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-orange-600 to-pink-600"></div>
              <div className="relative flex items-center gap-3">
                <NewspaperIcon className="h-6 w-6" />
                매거진 전체보기
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </div>
            </button>
          </div>
        </div>
      </section>

      {/* 마법같은 CTA Section */}
      <section className="section-heal7-hero relative overflow-hidden">
        {/* 환상적인 배경 */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_30%,rgba(255,255,255,0.1),transparent_60%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_70%,rgba(255,255,255,0.1),transparent_60%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_0deg_at_50%_50%,transparent_0deg,rgba(255,255,255,0.05)_60deg,transparent_120deg)]" />
        
        {/* 떠다니는 마법 파티클 */}
        <div className="absolute inset-0">
          {[...Array(15)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-white/30 rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${2 + Math.random() * 3}s`
              }}
            />
          ))}
        </div>
        
        <div className="container relative z-10">
          <div className="mx-auto max-w-5xl text-center text-white">
            {/* 신비로운 중앙 아이콘 */}
            <div className="mb-12 flex justify-center animate-heal7-scale-in">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 rounded-full blur-2xl opacity-40 scale-150 animate-pulse"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 rounded-full blur-xl opacity-20 scale-125 animate-pulse" style={{animationDelay: '1s'}}></div>
                <div className="relative bg-white/10 backdrop-blur-lg rounded-full p-8 border border-white/20 shadow-2xl">
                  <Compass className="h-16 w-16 text-white drop-shadow-lg" />
                </div>
              </div>
            </div>
            
            {/* 마법같은 메인 메시지 */}
            <div className="mb-12 animate-heal7-fade-in">
              <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight mb-8">
                🌟 당신만의 <span className="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">신비로운 여정</span>을 <br className="hidden sm:block" />
                <span className="bg-gradient-to-r from-cyan-300 to-blue-300 bg-clip-text text-transparent">시작해보세요</span> ✨
              </h2>
              <p className="text-xl md:text-2xl text-white/90 leading-relaxed max-w-3xl mx-auto">
                무료 기본 사주 분석으로 자아 발견의 첫걸음을 내디뎌보세요.<br />
                🔮 당신이 누구인지, 어디로 가야 하는지 그 답을 함께 찾아갑니다 🔮
              </p>
            </div>
            
            {/* 화려한 CTA 버튼들 */}
            <div className="flex flex-col sm:flex-row justify-center gap-6 mb-16 animate-heal7-fade-in" style={{animationDelay: '0.2s'}}>
              <button 
                onClick={() => handleNavigation('/saju/basic')}
                className="relative group px-12 py-5 text-xl font-bold text-indigo-900 rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105 shadow-2xl"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white via-yellow-100 to-white"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-200 via-orange-200 to-pink-200 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="relative flex items-center gap-3">
                  <Eye className="h-6 w-6" />
                  ✨ 무료로 자아 발견하기 ✨
                </div>
              </button>
              <button 
                onClick={() => handleNavigation('/store')}
                className="relative group px-12 py-5 text-xl font-bold text-white rounded-2xl border-2 border-white/30 backdrop-blur-lg transition-all duration-300 hover:scale-105 hover:bg-white/10"
              >
                <div className="flex items-center gap-3">
                  <ShoppingCart className="h-6 w-6" />
                  🛍️ 신비용품 구경하기
                </div>
              </button>
            </div>
            
            {/* 마법같은 특징들 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto animate-heal7-fade-in" style={{animationDelay: '0.4s'}}>
              {[
                { icon: Heart, text: "💕 진정한 관계의 조화", gradient: "from-pink-400 to-rose-400" },
                { icon: Mountain, text: "⛰️ 지속 가능한 성공", gradient: "from-green-400 to-emerald-400" },
                { icon: Sun, text: "☀️ 인생의 자연스러운 흐름", gradient: "from-yellow-400 to-orange-400" },
                { icon: Star, text: "⭐ 우주의 신비로운 메시지", gradient: "from-blue-400 to-purple-400" }
              ].map((item, index) => (
                <div key={index} className="group glass-heal7 rounded-2xl p-6 hover:bg-white/10 transition-all duration-300">
                  <div className="flex flex-col items-center text-center space-y-3">
                    <div className={`bg-gradient-to-r ${item.gradient} rounded-full p-3 group-hover:scale-110 transition-transform`}>
                      <item.icon className="h-6 w-6 text-white drop-shadow-sm" />
                    </div>
                    <span className="text-white/90 font-medium group-hover:text-white transition-colors">
                      {item.text}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}

export default ViteSajuMain