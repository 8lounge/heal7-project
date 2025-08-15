import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, Heart, Shield, Zap, Users } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Heal7 - 통합 웰니스 플랫폼',
  description: '사주명리학, 건강관리, 교육 서비스를 한 곳에서 만나보세요.',
}

const features = [
  {
    icon: Heart,
    title: '사주명리학',
    description: '전통 명리학을 현대적으로 해석한 정확한 사주 분석',
    href: '/saju',
    color: 'text-red-500'
  },
  {
    icon: Shield,
    title: '건강관리',
    description: '개인 맞춤형 건강 관리 솔루션과 전문가 상담',
    href: '/health',
    color: 'text-green-500'
  },
  {
    icon: Zap,
    title: '교육 아카데미',
    description: '웰니스 관련 전문 교육과 자격증 과정',
    href: '/academy',
    color: 'text-yellow-500'
  },
  {
    icon: Users,
    title: '커뮤니티',
    description: '같은 관심사를 가진 사람들과의 소통 공간',
    href: '/community',
    color: 'text-blue-500'
  }
]

const services = [
  {
    name: '사주 서비스',
    description: '정확한 사주 분석과 운세 상담',
    href: '/saju',
    image: '🔮'
  },
  {
    name: '건강 스토어',
    description: '검증된 건강 제품과 영양제',
    href: '/store',
    image: '🏪'
  },
  {
    name: '교육 아카데미',
    description: '전문가 양성 교육 프로그램',
    href: '/academy',
    image: '🎓'
  }
]

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-heal7 py-20 sm:py-32">
        <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
        <div className="container relative">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="animate-in text-4xl font-bold tracking-tight text-white sm:text-6xl">
              당신의 웰니스 여정을 
              <span className="block text-yellow-300">함께하겠습니다</span>
            </h1>
            <p className="slide-in mt-6 text-xl leading-8 text-blue-100">
              Heal7은 전통 사주명리학부터 현대적 건강관리까지, 
              당신의 몸과 마음을 치유하는 통합 플랫폼입니다.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link 
                href="/saju"
                className="btn-primary h-12 px-8 text-lg shadow-glow"
              >
                무료 사주 보기
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link 
                href="/about"
                className="btn bg-white/10 text-white hover:bg-white/20 h-12 px-8 text-lg"
              >
                서비스 둘러보기
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 sm:py-32">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              하나의 플랫폼, 무한한 가능성
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Heal7에서 제공하는 다양한 서비스를 만나보세요
            </p>
          </div>
          
          <div className="mx-auto mt-16 grid max-w-5xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => (
              <Link
                key={feature.title}
                href={feature.href}
                className="group relative overflow-hidden rounded-2xl bg-card p-6 hover:shadow-lg transition-all duration-300 border"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-center gap-4">
                  <feature.icon className={`h-8 w-8 ${feature.color}`} />
                  <div>
                    <h3 className="font-semibold group-hover:text-primary transition-colors">
                      {feature.title}
                    </h3>
                  </div>
                </div>
                <p className="mt-4 text-sm text-muted-foreground">
                  {feature.description}
                </p>
                <div className="absolute bottom-0 left-0 h-1 w-0 bg-primary transition-all duration-300 group-hover:w-full" />
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="bg-secondary/50 py-20 sm:py-32">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              주요 서비스
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              각 서비스별로 전문화된 솔루션을 제공합니다
            </p>
          </div>
          
          <div className="mx-auto mt-16 grid max-w-5xl grid-cols-1 gap-8 sm:grid-cols-3">
            {services.map((service, index) => (
              <Link
                key={service.name}
                href={service.href}
                className="group rounded-2xl bg-card p-8 text-center hover:shadow-xl transition-all duration-300"
                style={{ animationDelay: `${index * 0.15}s` }}
              >
                <div className="text-6xl mb-6 animate-bounce-subtle">
                  {service.image}
                </div>
                <h3 className="text-xl font-semibold mb-3 group-hover:text-primary transition-colors">
                  {service.name}
                </h3>
                <p className="text-muted-foreground">
                  {service.description}
                </p>
                <div className="mt-6 inline-flex items-center text-primary group-hover:gap-2 transition-all">
                  자세히 보기
                  <ArrowRight className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 sm:py-32">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              지금 시작해보세요
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Heal7과 함께 더 건강하고 행복한 삶을 만들어가세요
            </p>
            <div className="mt-10">
              <Link 
                href="/saju"
                className="btn-primary h-14 px-10 text-lg shadow-glow"
              >
                무료로 시작하기
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}