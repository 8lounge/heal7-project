import { Metadata } from 'next'
import Link from 'next/link'
import { Calendar, Star, Heart, TrendingUp, Zap, Users } from 'lucide-react'

export const metadata: Metadata = {
  title: '사주명리학 | Heal7',
  description: '전통 명리학을 현대적으로 해석한 정확한 사주 분석 서비스',
}

const services = [
  {
    icon: Star,
    title: '기본 사주분석',
    description: '태어난 시간을 기반으로 한 기본 사주 분석',
    features: ['사주팔자 해석', '성격 분석', '기본 운세'],
    price: '무료',
    href: '/saju/basic'
  },
  {
    icon: Heart,
    title: '연애 궁합',
    description: '두 사람의 사주를 비교한 궁합 분석',
    features: ['궁합도 분석', '관계 조언', '결혼 적합성'],
    price: '₩5,000',
    href: '/saju/compatibility'
  },
  {
    icon: TrendingUp,
    title: '사업 운세',
    description: '사업과 투자에 관련된 운세 분석',
    features: ['사업 적성', '투자 타이밍', '파트너 궁합'],
    price: '₩10,000',
    href: '/saju/business'
  },
  {
    icon: Calendar,
    title: '연간 운세',
    description: '1년간의 상세한 운세 분석',
    features: ['월별 운세', '주요 사건', '주의사항'],
    price: '₩15,000',
    href: '/saju/yearly'
  }
]

const testimonials = [
  {
    name: '김○○',
    age: 28,
    content: '정말 정확한 분석에 놀랐어요. 특히 성격 분석 부분이 저를 너무 잘 아시는 것 같았습니다.',
    rating: 5
  },
  {
    name: '이○○',
    age: 35,
    content: '연애 궁합 분석을 통해 연인과의 관계를 더 잘 이해하게 되었습니다.',
    rating: 5
  },
  {
    name: '박○○',
    age: 42,
    content: '사업 운세 분석으로 중요한 결정을 내릴 수 있었습니다. 감사합니다.',
    rating: 4
  }
]

export default function SajuPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-lavender-50 to-sky-100">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        <div className="absolute inset-0 bg-gradient-to-r from-lavender-600 to-sky-600 opacity-10" />
        <div className="container relative">
          <div className="mx-auto max-w-4xl text-center">
            <div className="mb-8 flex justify-center">
              <div className="rounded-full bg-gradient-to-r from-lavender-600 to-sky-600 p-3">
                <Star className="h-12 w-12 text-white" />
              </div>
            </div>
            <h1 className="mb-6 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              전통 사주명리학으로
              <span className="block text-gradient">당신의 운명을 읽어드립니다</span>
            </h1>
            <p className="mb-10 text-xl leading-8 text-gray-600">
              수천 년의 전통을 이어온 사주명리학을 현대적으로 해석하여
              <br />정확하고 신뢰할 수 있는 분석을 제공합니다.
            </p>
            <div className="flex justify-center gap-4">
              <Link 
                href="/saju/basic"
                className="btn-primary h-14 px-8 text-lg shadow-glow"
              >
                무료 사주 보기
                <Star className="ml-2 h-5 w-5" />
              </Link>
              <Link 
                href="/saju/about"
                className="btn bg-white hover:bg-gray-50 h-14 px-8 text-lg border"
              >
                서비스 소개
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              다양한 사주 분석 서비스
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              목적에 맞는 맞춤형 사주 분석을 선택하세요
            </p>
          </div>
          
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {services.map((service, index) => (
              <div
                key={service.title}
                className="group rounded-2xl bg-white p-8 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 border saju-focus"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="mb-6 flex items-center justify-between">
                  <service.icon className="h-10 w-10 text-lavender-600" />
                  <span className="text-2xl font-bold text-lavender-600">
                    {service.price}
                  </span>
                </div>
                
                <h3 className="mb-3 text-xl font-semibold text-gray-900">
                  {service.title}
                </h3>
                <p className="mb-6 text-gray-600">
                  {service.description}
                </p>
                
                <ul className="mb-8 space-y-2">
                  {service.features.map((feature, i) => (
                    <li key={i} className="flex items-center text-sm text-gray-500">
                      <Zap className="mr-2 h-4 w-4 text-green-500" />
                      {feature}
                    </li>
                  ))}
                </ul>
                
                <Link
                  href={service.href}
                  className="btn-primary w-full justify-center group-hover:shadow-lg transition-all"
                >
                  분석 시작하기
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="bg-white py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              고객 후기
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              실제 이용하신 분들의 생생한 후기입니다
            </p>
          </div>
          
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
            {testimonials.map((testimonial, index) => (
              <div
                key={index}
                className="rounded-2xl bg-gray-50 p-8 text-center"
              >
                <div className="mb-4 flex justify-center">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-5 w-5 ${
                        i < testimonial.rating
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
                <p className="mb-6 text-gray-600 italic">
                  "{testimonial.content}"
                </p>
                <div className="font-semibold text-gray-900">
                  {testimonial.name}
                </div>
                <div className="text-sm text-gray-500">
                  {testimonial.age}세
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-lavender-600 to-sky-600 py-20 text-white">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              지금 바로 시작해보세요
            </h2>
            <p className="mt-6 text-xl">
              무료 기본 사주 분석으로 당신의 운명을 확인해보세요
            </p>
            <div className="mt-10">
              <Link 
                href="/saju/basic"
                className="btn bg-white text-lavender-600 hover:bg-gray-100 h-14 px-10 text-lg font-semibold shadow-xl"
              >
                무료 사주 분석 시작
                <Star className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}