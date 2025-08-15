'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Layout } from '@/components/layout/Layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, HealingCard } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Sparkles, 
  Brain, 
  BookOpen, 
  ShoppingBag, 
  Users, 
  Star,
  ArrowRight,
  Zap
} from 'lucide-react'


const services = [
  {
    icon: Sparkles,
    title: '분석 솔루션',
    description: '3D 성향 분석, AI 심리 분석, 명리학 v5.0으로 나를 완전히 이해하세요',
    href: '/diagnosis',
    badge: 'NEW',
    gradient: 'from-healing-500 to-healing-600',
    features: ['3D 시각화', 'AI 분석', '전문가 검증']
  },
  {
    icon: BookOpen,
    title: '체험아카데미',
    description: '크라우드펀딩과 전문 강의로 성장과 힐링의 기회를 만나보세요',
    href: '/academy',
    badge: 'HOT',
    gradient: 'from-sky-500 to-sky-600',
    features: ['크라우드펀딩', '전문 강의', '실습 프로그램']
  },
  {
    icon: ShoppingBag,
    title: '힐링스토어',
    description: '엄선된 힐링 상품과 도서로 일상에 평화를 더하세요',
    href: '/store',
    gradient: 'from-earth-500 to-earth-600',
    features: ['엄선된 상품', '빠른 배송', '전문가 추천']
  },
  {
    icon: Users,
    title: '커뮤니티',
    description: '공지사항, 전문가 상담, 사용자 후기를 한곳에서 확인하세요',
    href: '/community',
    gradient: 'from-lavender-500 to-lavender-600',
    features: ['소통 공간', '전문가 상담', '경험 공유']
  }
]

const stats = [
  {
    icon: Users,
    value: 29890,
    suffix: '명',
    label: '분석 완료',
    description: '누적 분석 참여자 수'
  },
  {
    icon: Brain,
    value: 442,
    suffix: '개',
    label: '분석 키워드',
    description: 'M-PIS 분석 키워드'
  },
  {
    icon: Star,
    value: 3090,
    suffix: '개',
    label: '연관 키워드',
    description: '상호 연결 분석'
  },
  {
    icon: Zap,
    value: 97,
    suffix: '.1%',
    label: 'AI 정확도',
    description: '교차검증 완료'
  }
]

const testimonials = [
  {
    name: '김민지',
    role: '직장인',
    content: '3D 성향 분석을 통해 제 자신을 새롭게 이해할 수 있었어요. 시각적으로 보여주는 결과가 정말 인상적이었습니다.',
    rating: 5,
    avatar: '👩‍💼'
  },
  {
    name: '박준호',
    role: '대학생',
    content: 'AI 심리 분석이 제가 몰랐던 부분까지 정확하게 짚어줘서 놀랐습니다. 진로 고민에 큰 도움이 되었어요.',
    rating: 5,
    avatar: '👨‍🎓'
  },
  {
    name: '이수연',
    role: '프리랜서',
    content: '명리학 v5.0은 기존의 명리학과는 차원이 달랐어요. 현대적이면서도 깊이 있는 해석이 인상적입니다.',
    rating: 5,
    avatar: '👩‍💻'
  }
]

// CountUp hook for dynamic counting animation
const useCountUp = (end: number, duration: number = 2000, start: boolean = false) => {
  const [count, setCount] = useState(0)

  useEffect(() => {
    if (!start) return

    let startTime: number
    let animationId: number

    const updateCount = (timestamp: number) => {
      if (!startTime) startTime = timestamp
      const progress = Math.min((timestamp - startTime) / duration, 1)
      
      // Easing function for smooth animation
      const easeOut = 1 - Math.pow(1 - progress, 3)
      setCount(Math.floor(end * easeOut))

      if (progress < 1) {
        animationId = requestAnimationFrame(updateCount)
      }
    }

    animationId = requestAnimationFrame(updateCount)
    return () => cancelAnimationFrame(animationId)
  }, [end, duration, start])

  return count
}

// StatCounter component for animated statistics
const StatCounter: React.FC<{
  stat: typeof stats[0]
  index: number
  start: boolean
}> = ({ stat, index, start }) => {
  const count = useCountUp(stat.value, 2000 + index * 200, start)
  const Icon = stat.icon

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.6, delay: 0.1 * index }}
      className="text-center group"
    >
      <div className="relative p-3 sm:p-4 rounded-xl sm:rounded-2xl bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/15 transition-all duration-300">
        <div className="flex items-center justify-center w-8 h-8 sm:w-12 sm:h-12 mx-auto mb-2 sm:mb-3 rounded-lg sm:rounded-xl bg-gradient-to-br from-sky-500 to-healing-500 shadow-lg">
          <Icon className="w-4 h-4 sm:w-6 sm:h-6 text-white" />
        </div>
        
        <div className="text-xl sm:text-2xl md:text-3xl font-bold mb-1 text-white bg-gradient-to-br from-white to-sky-200 bg-clip-text text-transparent">
          {count.toLocaleString()}<span className="text-sky-300">{stat.suffix}</span>
        </div>
        
        <div className="text-xs sm:text-sm font-semibold mb-1 text-sky-200">{stat.label}</div>
        <div className="text-xs text-slate-400 leading-tight">{stat.description}</div>
      </div>
    </motion.div>
  )
}

export default function HomePage() {
  const [statsInView, setStatsInView] = useState(false)
  
  return (
    <Layout>
      <div className="pt-20">
        {/* Hero Section */}
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
          {/* Background Image */}
          <div 
            className="absolute inset-0 bg-cover bg-center bg-no-repeat z-0"
            style={{ 
              backgroundImage: 'url(https://cdn.midjourney.com/c0cdbe48-3ac1-4b2d-b58f-8d7f5ae7d2c4/0_1.png)',
            }}
          />

          {/* Overlay */}
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm z-10" />

          <div className="container mx-auto px-4 text-center relative z-20">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="max-w-4xl mx-auto space-y-6 sm:space-y-8 py-20 sm:py-0 sm:-mt-32"
            >
              <Badge variant="outline" className="mb-4 bg-white/10 text-white border-white/30 backdrop-blur-sm text-sm sm:text-base px-3 py-2 sm:px-4 sm:py-2">
                <Sparkles className="w-4 h-4 mr-2 text-sky-300" />
                마음의 평화를 찾아가는 여정
              </Badge>
              
              <h1 className="heading-xl text-white space-y-2">
                <span className="text-white font-bold drop-shadow-lg text-2xl sm:text-4xl md:text-5xl xl:text-6xl leading-tight block">나의 성향을</span>
                <span className="bg-gradient-to-r from-sky-400 to-healing-500 bg-clip-text text-transparent text-2xl sm:text-4xl md:text-5xl xl:text-6xl font-black leading-tight block">
                  입체적으로 분석하자
                </span>
              </h1>
              
              <p className="text-lg sm:text-2xl text-slate-200 max-w-2xl mx-auto leading-relaxed font-medium px-4">
                <strong className="text-sky-300">명리학 + 심리학 + 뇌과학</strong><br className="hidden sm:block" />
                <span className="sm:hidden"> • </span>강한 경쟁력은 <strong className="text-sky-300">나</strong>를 아는것
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center px-4">
                <Button size="xl" className="bg-gradient-to-r from-sky-500 to-healing-500 text-white hover:from-sky-600 hover:to-healing-600 shadow-lg shadow-sky-500/25 text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4" asChild>
                  <Link href="/diagnosis">
                    <Sparkles className="w-5 h-5 sm:w-6 sm:h-6 mr-2 sm:mr-3" />
                    <span className="whitespace-nowrap">3D 성향분석 시작</span>
                    <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 ml-2 sm:ml-3" />
                  </Link>
                </Button>
                <Button size="xl" variant="outline" className="bg-white/10 text-white border-white/30 hover:bg-white/20 backdrop-blur-sm text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4" asChild>
                  <Link href="/about">
                    <Brain className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
                    <span className="whitespace-nowrap">분석 방법 보기</span>
                  </Link>
                </Button>
              </div>

              {/* Stats Section - 히어로 하단에 통합 */}
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
                onViewportEnter={() => setStatsInView(true)}
                className="mt-8 sm:mt-16 max-w-5xl mx-auto px-4"
              >
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6">
                  {stats.map((stat, index) => (
                    <StatCounter 
                      key={stat.label}
                      stat={stat}
                      index={index}
                      start={statsInView}
                    />
                  ))}
                </div>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* Services Section */}
        <section className="py-24 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <Badge variant="healing" className="mb-4">
                Services
              </Badge>
              <h2 className="heading-lg mb-4">
                완벽한 힐링 생태계
              </h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                분석부터 성장까지, 당신의 힐링 여정을 위한 모든 것을 한 곳에서 만나보세요
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
              {services.map((service, index) => {
                const Icon = service.icon
                return (
                  <motion.div
                    key={service.title}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: 0.1 * index }}
                  >
                    <HealingCard className="h-full group cursor-pointer">
                      <div className="relative">
                        <div className={`absolute inset-0 bg-gradient-to-r ${service.gradient} opacity-5 rounded-t-xl`} />
                        <CardHeader className="relative z-10">
                          <div className="flex items-center justify-between">
                            <div className={`flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-r ${service.gradient} shadow-lg`}>
                              <Icon className="w-6 h-6 text-white" />
                            </div>
                            {service.badge && (
                              <Badge variant="healing">
                                {service.badge}
                              </Badge>
                            )}
                          </div>
                          <CardTitle className="text-xl mt-4">{service.title}</CardTitle>
                          <CardDescription className="text-base">
                            {service.description}
                          </CardDescription>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-4">
                            <div className="flex flex-wrap gap-2">
                              {service.features.map((feature) => (
                                <Badge key={feature} variant="outline" className="text-xs">
                                  {feature}
                                </Badge>
                              ))}
                            </div>
                            <Button 
                              variant="ghost" 
                              className="w-full group-hover:bg-gray-50 dark:group-hover:bg-gray-800"
                              asChild
                            >
                              <Link href={service.href}>
                                자세히 보기
                                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                              </Link>
                            </Button>
                          </div>
                        </CardContent>
                      </div>
                    </HealingCard>
                  </motion.div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-24 bg-gray-50 dark:bg-gray-800">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <Badge variant="healing" className="mb-4">
                Testimonials
              </Badge>
              <h2 className="heading-lg mb-4">
                사용자들의 진심 어린 후기
              </h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                HEALINGSPACE와 함께한 분들의 솔직한 이야기를 들어보세요
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={testimonial.name}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: 0.1 * index }}
                >
                  <Card className="h-full">
                    <CardContent className="p-6">
                      <div className="flex items-center mb-4">
                        {[...Array(testimonial.rating)].map((_, i) => (
                          <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                      <p className="text-muted-foreground mb-6 italic">
                        &quot;{testimonial.content}&quot;
                      </p>
                      <div className="flex items-center space-x-3">
                        <div className="text-2xl">{testimonial.avatar}</div>
                        <div>
                          <div className="font-semibold">{testimonial.name}</div>
                          <div className="text-sm text-muted-foreground">{testimonial.role}</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="max-w-3xl mx-auto space-y-8"
            >
              <h2 className="heading-lg">
                진짜 나는 어떤 모습일까요?
              </h2>
              <p className="text-xl text-muted-foreground">
                3D 성향분석으로 숨겨진 나의 가능성을 발견하고<br />
                AI가 제시하는 최적의 진로를 확인해보세요.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="xl" variant="healing" asChild>
                  <Link href="/diagnosis">
                    <Sparkles className="w-5 h-5 mr-2" />
                    3D 성향분석 체험하기
                  </Link>
                </Button>
                <Button size="xl" variant="outline" asChild>
                  <Link href="/academy">
                    <BookOpen className="w-5 h-5 mr-2" />
                    아카데미 둘러보기
                  </Link>
                </Button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </Layout>
  )
}