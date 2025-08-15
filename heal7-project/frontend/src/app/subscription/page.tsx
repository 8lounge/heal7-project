'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Layout } from '@/components/layout/Layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Zap, 
  Crown,
  Star,
  Check,
  X,
  Users,
  Calendar,
  TrendingUp,
  Shield,
  Sparkles,
  ArrowRight,
  Gift,
  Clock,
  Target,
  Award,
  Heart
} from 'lucide-react'

const plans = [
  {
    id: 'basic',
    name: '베이직',
    subtitle: '개인 사용자를 위한 기본 플랜',
    price: 29000,
    originalPrice: null,
    period: '월',
    description: '힐링 여정을 시작하는 분들을 위한 기본 서비스',
    badge: null,
    color: 'from-gray-500 to-gray-600',
    features: [
      { name: '월 1회 3D 성향분석', included: true },
      { name: '기본 리포트 제공', included: true },
      { name: '커뮤니티 참여', included: true },
      { name: '월간 뉴스레터', included: true },
      { name: 'AI 심리분석', included: false },
      { name: '1:1 전문가 상담', included: false },
      { name: '프리미엄 콘텐츠', included: false },
      { name: '우선 고객지원', included: false }
    ],
    benefits: [
      '자기이해의 첫걸음',
      '기본적인 성향 파악',
      '커뮤니티 네트워킹'
    ]
  },
  {
    id: 'premium',
    name: '프리미엄',
    subtitle: '성장을 추구하는 분들을 위한 완벽한 플랜',
    price: 79000,
    originalPrice: 99000,
    period: '월',
    description: '모든 분석과 개인 맞춤 서비스를 제공하는 인기 플랜',
    badge: 'MOST POPULAR',
    color: 'from-healing-500 to-healing-600',
    features: [
      { name: '월 3회 3D 성향분석', included: true },
      { name: '월 2회 AI 심리분석', included: true },
      { name: '월 1회 명리학 분석', included: true },
      { name: '상세 리포트 + 3D 시각화', included: true },
      { name: '월 1회 전문가 상담 (30분)', included: true },
      { name: '프리미엄 콘텐츠 무제한', included: true },
      { name: '우선 고객지원', included: true },
      { name: '분석 히스토리 관리', included: true }
    ],
    benefits: [
      '종합적인 자기분석',
      '전문가 맞춤 가이드',
      '지속적인 성장 관리',
      '우선 지원 서비스'
    ]
  },
  {
    id: 'enterprise',
    name: '엔터프라이즈',
    subtitle: '기업 및 전문가를 위한 최고급 플랜',
    price: 149000,
    originalPrice: 199000,
    period: '월',
    description: '무제한 분석과 전문가 서비스를 제공하는 최상위 플랜',
    badge: 'ENTERPRISE',
    color: 'from-purple-500 to-purple-600',
    features: [
      { name: '모든 분석 무제한', included: true },
      { name: '전담 전문가 배정', included: true },
      { name: '월 4회 전문가 상담 (60분)', included: true },
      { name: 'API 접근 권한', included: true },
      { name: '맞춤형 리포트 제작', included: true },
      { name: '팀/기업 분석 서비스', included: true },
      { name: '24/7 전용 지원', included: true },
      { name: '데이터 내보내기', included: true }
    ],
    benefits: [
      '무제한 프리미엄 서비스',
      '전담 전문가 지원',
      '기업용 맞춤 솔루션',
      '최고 수준의 지원'
    ]
  }
]

const yearlyDiscounts = {
  basic: { monthly: 29000, yearly: 290000, discount: 20 },
  premium: { monthly: 79000, yearly: 790000, discount: 25 },
  enterprise: { monthly: 149000, yearly: 1490000, discount: 30 }
}

const faqs = [
  {
    question: '구독은 언제든지 취소할 수 있나요?',
    answer: '네, 언제든지 구독을 취소할 수 있습니다. 취소 시점까지 이용하신 서비스에 대한 비용만 청구되며, 남은 기간에 대해서는 환불 처리됩니다.'
  },
  {
    question: '플랜 변경은 어떻게 하나요?',
    answer: '마이페이지에서 언제든지 플랜을 업그레이드하거나 다운그레이드할 수 있습니다. 변경 즉시 새로운 플랜의 혜택이 적용됩니다.'
  },
  {
    question: '연간 결제 시 할인 혜택이 있나요?',
    answer: '네, 연간 결제 시 베이직 20%, 프리미엄 25%, 엔터프라이즈 30%의 할인 혜택을 받으실 수 있습니다.'
  },
  {
    question: '무료 체험 기간이 있나요?',
    answer: '모든 플랜에 대해 14일 무료 체험을 제공합니다. 체험 기간 중 언제든지 취소하실 수 있습니다.'
  }
]

const PricingCard: React.FC<{ 
  plan: typeof plans[0] 
  isYearly: boolean 
  isPopular?: boolean 
}> = ({ plan, isYearly, isPopular }) => {
  const yearlyPlan = yearlyDiscounts[plan.id as keyof typeof yearlyDiscounts]
  const currentPrice = isYearly ? Math.floor(yearlyPlan.yearly / 12) : plan.price
  const savings = isYearly ? plan.price - currentPrice : 0

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -10 }}
      transition={{ duration: 0.5 }}
      className={`relative ${isPopular ? 'scale-105 z-10' : ''}`}
    >
      <Card className={`relative overflow-hidden border-2 ${
        isPopular 
          ? 'border-healing-500 shadow-2xl shadow-healing-500/20' 
          : 'border-gray-200 hover:border-healing-300 shadow-lg'
      } transition-all duration-300 h-full`}>
        {/* Popular Badge */}
        {isPopular && (
          <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 z-20">
            <Badge className="bg-healing-500 text-white px-4 py-1 rounded-full">
              <Crown className="w-4 h-4 mr-1" />
              {plan.badge}
            </Badge>
          </div>
        )}

        {/* Background Gradient */}
        <div className={`absolute top-0 left-0 right-0 h-32 bg-gradient-to-r ${plan.color} opacity-10`} />

        <CardHeader className="relative text-center pt-8">
          <CardTitle className="text-2xl font-bold mb-2">{plan.name}</CardTitle>
          <CardDescription className="text-base mb-4">{plan.subtitle}</CardDescription>
          
          {/* Price */}
          <div className="space-y-2">
            <div className="flex items-baseline justify-center gap-2">
              <span className="text-4xl font-bold text-gray-900 dark:text-white">
                {currentPrice.toLocaleString()}원
              </span>
              <span className="text-muted-foreground">/{plan.period}</span>
            </div>
            
            {isYearly && savings > 0 && (
              <div className="text-sm text-healing-600 font-semibold">
                월 {savings.toLocaleString()}원 할인!
              </div>
            )}
            
            {plan.originalPrice && !isYearly && (
              <div className="text-sm text-muted-foreground line-through">
                원래 {plan.originalPrice.toLocaleString()}원
              </div>
            )}
          </div>
          
          <CardDescription className="mt-4">{plan.description}</CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Features */}
          <div className="space-y-3">
            {plan.features.map((feature, index) => (
              <div key={index} className="flex items-center gap-3">
                <div className={`flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center ${
                  feature.included 
                    ? 'bg-healing-100 dark:bg-healing-900' 
                    : 'bg-gray-100 dark:bg-gray-800'
                }`}>
                  {feature.included ? (
                    <Check className="w-3 h-3 text-healing-600" />
                  ) : (
                    <X className="w-3 h-3 text-gray-400" />
                  )}
                </div>
                <span className={`text-sm ${
                  feature.included 
                    ? 'text-gray-900 dark:text-gray-100' 
                    : 'text-gray-400'
                }`}>
                  {feature.name}
                </span>
              </div>
            ))}
          </div>

          {/* Benefits */}
          <div className="pt-4 border-t">
            <h4 className="font-semibold text-sm text-gray-900 dark:text-gray-100 mb-3">
              주요 혜택
            </h4>
            <ul className="space-y-2">
              {plan.benefits.map((benefit, index) => (
                <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                  <Star className="w-4 h-4 text-healing-500 mt-0.5 flex-shrink-0" />
                  <span>{benefit}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* CTA */}
          <div className="pt-6">
            <Button 
              className={`w-full text-lg py-6 ${
                isPopular 
                  ? 'bg-healing-600 hover:bg-healing-700 text-white' 
                  : 'bg-gray-900 hover:bg-gray-800 text-white'
              }`}
              size="lg"
            >
              {plan.id === 'enterprise' ? (
                <>
                  <Users className="w-5 h-5 mr-2" />
                  영업팀 문의하기
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 mr-2" />
                  14일 무료 체험
                </>
              )}
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            
            <p className="text-xs text-muted-foreground text-center mt-3">
              신용카드 없이 체험 가능 • 언제든지 취소 가능
            </p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default function SubscriptionPage() {
  const [isYearly, setIsYearly] = useState(false)

  return (
    <Layout>
      <div className="pt-20">
        {/* Header Section */}
        <section className="py-20 bg-gradient-to-br from-healing-50 via-purple-50 to-sky-50 dark:from-gray-900 dark:via-purple-900 dark:to-sky-900">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-4xl mx-auto space-y-8"
            >
              <Badge variant="healing" className="mb-4 text-base px-6 py-2">
                <Zap className="w-5 h-5 mr-2" />
                SUBSCRIPTION PLANS
              </Badge>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8">
                <span className="bg-gradient-to-r from-healing-600 via-purple-600 to-sky-600 bg-clip-text text-transparent">
                  성장하는 삶,
                </span>
                <br />
                <span className="text-gray-900 dark:text-white">
                  지속되는 힐링
                </span>
              </h1>
              
              <p className="text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                당신의 성장 속도에 맞는 완벽한 구독 플랜을 선택하고
                <br className="hidden sm:block" />
                <strong className="text-healing-600">지속적인 변화</strong>를 경험하세요
              </p>

              {/* Billing Toggle */}
              <div className="flex items-center justify-center gap-4 mt-12">
                <span className={`font-medium ${!isYearly ? 'text-gray-900 dark:text-white' : 'text-muted-foreground'}`}>
                  월간 결제
                </span>
                <button
                  onClick={() => setIsYearly(!isYearly)}
                  className={`relative w-16 h-8 rounded-full transition-all duration-300 ${
                    isYearly ? 'bg-healing-600' : 'bg-gray-300'
                  }`}
                >
                  <div className={`absolute w-6 h-6 bg-white rounded-full transition-all duration-300 top-1 ${
                    isYearly ? 'left-9' : 'left-1'
                  }`} />
                </button>
                <span className={`font-medium ${isYearly ? 'text-gray-900 dark:text-white' : 'text-muted-foreground'}`}>
                  연간 결제
                </span>
                {isYearly && (
                  <Badge variant="healing" className="ml-2">
                    <Gift className="w-4 h-4 mr-1" />
                    최대 30% 할인
                  </Badge>
                )}
              </div>
            </motion.div>
          </div>
        </section>

        {/* Pricing Plans */}
        <section className="py-20 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {plans.map((plan, index) => (
                <PricingCard 
                  key={plan.id} 
                  plan={plan} 
                  isYearly={isYearly}
                  isPopular={index === 1}
                />
              ))}
            </div>
          </div>
        </section>

        {/* Features Comparison */}
        <section className="py-20 bg-gray-50 dark:bg-gray-800">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl font-bold mb-6">
                플랜별 상세 비교
              </h2>
              <p className="text-xl text-muted-foreground">
                어떤 플랜이 나에게 맞는지 자세히 비교해보세요
              </p>
            </motion.div>

            {/* Comparison Table for larger screens */}
            <div className="hidden lg:block">
              <div className="bg-white dark:bg-gray-900 rounded-xl shadow-lg overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th className="text-left p-6 font-semibold">기능</th>
                      {plans.map((plan) => (
                        <th key={plan.id} className="text-center p-6 font-semibold">
                          {plan.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {plans[0].features.map((_, featureIndex) => (
                      <tr key={featureIndex} className="border-t border-gray-200 dark:border-gray-700">
                        <td className="p-6 font-medium">
                          {plans[0].features[featureIndex].name}
                        </td>
                        {plans.map((plan) => (
                          <td key={plan.id} className="p-6 text-center">
                            {plan.features[featureIndex].included ? (
                              <Check className="w-6 h-6 text-healing-600 mx-auto" />
                            ) : (
                              <X className="w-6 h-6 text-gray-300 mx-auto" />
                            )}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-20 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl font-bold mb-6">자주 묻는 질문</h2>
              <p className="text-xl text-muted-foreground">
                구독에 대해 궁금한 점들을 확인해보세요
              </p>
            </motion.div>

            <div className="max-w-3xl mx-auto space-y-6">
              {faqs.map((faq, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.1 * index }}
                >
                  <Card className="p-6">
                    <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                      {faq.question}
                    </h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {faq.answer}
                    </p>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-r from-healing-600 via-purple-600 to-sky-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="max-w-4xl mx-auto space-y-8"
            >
              <h2 className="text-4xl md:text-5xl font-bold">
                지금 시작하면 14일 무료!
              </h2>
              <p className="text-2xl text-white/90 leading-relaxed">
                신용카드 정보 없이도 모든 기능을 체험해보세요
              </p>
              <div className="flex flex-col sm:flex-row gap-6 justify-center pt-8">
                <Button size="xl" variant="secondary" className="text-lg px-12 py-4">
                  <Sparkles className="w-6 h-6 mr-3" />
                  무료 체험 시작하기
                </Button>
                <Button 
                  size="xl" 
                  variant="outline" 
                  className="border-2 border-white text-white hover:bg-white hover:text-healing-600 text-lg px-12 py-4"
                >
                  <Users className="w-6 h-6 mr-3" />
                  영업팀 문의하기
                </Button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </Layout>
  )
}