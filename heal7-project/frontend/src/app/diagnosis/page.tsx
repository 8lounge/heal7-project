'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Layout } from '@/components/layout/Layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Sparkles, 
  Brain, 
  Target,
  TrendingUp,
  Users,
  Clock,
  Star,
  ArrowRight,
  CheckCircle,
  Zap,
  Shield,
  Award,
  BarChart,
  Layers,
  PlayCircle
} from 'lucide-react'

const analysisTypes = [
  {
    id: '3d-personality',
    title: '3D 성향 분석',
    subtitle: 'AI 기반 입체적 성격 분석',
    description: '최신 AI 기술과 심리학 이론을 결합하여 당신의 성향을 3차원으로 분석합니다.',
    duration: '15-20분',
    accuracy: '97.3%',
    users: '29,890명',
    price: 49000,
    originalPrice: 79000,
    image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&h=400&fit=crop',
    badge: 'BEST',
    features: [
      '16가지 성향 유형 분석',
      '3D 시각화 리포트',
      '개인 맞춤 성장 가이드',
      '직업 적합성 분석',
      '인간관계 패턴 분석',
      '평생 무료 재분석'
    ],
    benefits: [
      { icon: Target, title: '정확한 자기이해', desc: '객관적 데이터 기반 성향 파악' },
      { icon: TrendingUp, title: '성장 방향 제시', desc: '개인 맞춤 발전 전략 수립' },
      { icon: Users, title: '관계 개선', desc: '타인과의 소통 방식 최적화' }
    ]
  },
  {
    id: 'ai-psychology',
    title: 'AI 심리 분석',
    subtitle: '딥러닝 기반 심층 심리 진단',
    description: '고도화된 AI 알고리즘으로 무의식 영역까지 포함한 심층적 심리 상태를 분석합니다.',
    duration: '25-30분',
    accuracy: '94.8%',
    users: '18,456명',
    price: 69000,
    originalPrice: 99000,
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
    badge: 'NEW',
    features: [
      '감정 패턴 분석',
      'AI 심리 상담사 매칭',
      '스트레스 수준 측정',
      '우울/불안 지수 체크',
      '개인 맞춤 치료 제안',
      '3개월 추적 관리'
    ],
    benefits: [
      { icon: Brain, title: '심층 진단', desc: '무의식 영역까지 포함한 종합 분석' },
      { icon: Shield, title: '정신건강 관리', desc: '조기 발견 및 예방 중심 접근' },
      { icon: Zap, title: '즉시 솔루션', desc: 'AI 기반 맞춤 치료법 제안' }
    ]
  },
  {
    id: 'myeongri-analysis',
    title: '명리학 v5.0',
    subtitle: '전통과 현대의 만남',
    description: '5000년 전통 명리학을 현대 과학으로 재해석한 차세대 운명 분석 시스템입니다.',
    duration: '10-15분',
    accuracy: '92.1%',
    users: '15,234명',
    price: 39000,
    originalPrice: 59000,
    image: 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=600&h=400&fit=crop',
    badge: 'HOT',
    features: [
      '정밀 사주 계산',
      '대운/세운 분석',
      '직업/재물운 예측',
      '건강/인연 운세',
      '월간 운세 업데이트',
      '전문가 해석 서비스'
    ],
    benefits: [
      { icon: BarChart, title: '인생 로드맵', desc: '생애 주기별 운세 변화 예측' },
      { icon: Award, title: '의사결정 지원', desc: '중요한 선택의 순간에 가이드' },
      { icon: Layers, title: '종합적 해석', desc: '전통 지혜와 현대 분석의 융합' }
    ]
  }
]

const testimonials = [
  {
    name: '김민수',
    age: '32세, 직장인',
    analysis: '3D 성향 분석',
    rating: 5,
    content: '정말 놀라웠습니다. 저도 몰랐던 제 성향까지 정확하게 짚어주더라고요. 특히 3D 시각화 리포트가 이해하기 쉬워서 좋았어요.',
    avatar: '👨‍💼'
  },
  {
    name: '박지영',
    age: '28세, 프리랜서',
    analysis: 'AI 심리 분석',
    rating: 5,
    content: '최근 스트레스가 많았는데, AI가 제 심리 상태를 정확히 파악하고 맞춤 솔루션을 제시해줘서 많은 도움이 되었습니다.',
    avatar: '👩‍💻'
  },
  {
    name: '이창호',
    age: '45세, 사업가',
    analysis: '명리학 v5.0',
    rating: 5,
    content: '전통 명리학을 현대적으로 해석한 점이 인상적이었어요. 사업 결정에 큰 도움이 되었습니다.',
    avatar: '👨‍💼'
  }
]

const AnalysisCard: React.FC<{ analysis: typeof analysisTypes[0] }> = ({ analysis }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -10 }}
      transition={{ duration: 0.5 }}
      className="group"
    >
      <Card className="relative overflow-hidden border-0 shadow-xl hover:shadow-2xl transition-all duration-300 h-full">
        {/* Header Image */}
        <div className="relative">
          <div
            className="aspect-[16/10] bg-cover bg-center group-hover:scale-105 transition-transform duration-500"
            style={{ backgroundImage: `url(${analysis.image})` }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          
          {/* Badge */}
          {analysis.badge && (
            <Badge 
              variant={analysis.badge === 'BEST' ? 'healing' : analysis.badge === 'HOT' ? 'destructive' : 'secondary'}
              className="absolute top-4 left-4 text-sm font-bold"
            >
              {analysis.badge}
            </Badge>
          )}

          {/* Price */}
          <div className="absolute top-4 right-4 text-right">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-2">
              <div className="text-2xl font-bold text-healing-600">
                {analysis.price.toLocaleString()}원
              </div>
              {analysis.originalPrice && (
                <div className="text-sm text-muted-foreground line-through">
                  {analysis.originalPrice.toLocaleString()}원
                </div>
              )}
            </div>
          </div>

          {/* Play Button */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <PlayCircle className="w-20 h-20 text-white drop-shadow-lg" />
          </div>
        </div>

        <CardHeader className="pb-4">
          <div className="space-y-2">
            <CardTitle className="text-2xl font-bold group-hover:text-healing-600 transition-colors">
              {analysis.title}
            </CardTitle>
            <CardDescription className="text-base font-medium text-healing-600">
              {analysis.subtitle}
            </CardDescription>
            <CardDescription className="leading-relaxed">
              {analysis.description}
            </CardDescription>
          </div>

          {/* Stats */}
          <div className="flex items-center gap-6 pt-4 text-sm">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4 text-muted-foreground" />
              <span>{analysis.duration}</span>
            </div>
            <div className="flex items-center gap-1">
              <Target className="w-4 h-4 text-muted-foreground" />
              <span>정확도 {analysis.accuracy}</span>
            </div>
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4 text-muted-foreground" />
              <span>{analysis.users} 완료</span>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Features */}
          <div>
            <h4 className="font-semibold mb-3 text-gray-900 dark:text-gray-100">포함 서비스</h4>
            <div className="grid grid-cols-1 gap-2">
              {analysis.features.map((feature, index) => (
                <div key={index} className="flex items-center gap-2 text-sm">
                  <CheckCircle className="w-4 h-4 text-healing-600 shrink-0" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Benefits */}
          <div>
            <h4 className="font-semibold mb-3 text-gray-900 dark:text-gray-100">기대 효과</h4>
            <div className="space-y-3">
              {analysis.benefits.map((benefit, index) => (
                <div key={index} className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-healing-100 dark:bg-healing-900 rounded-lg flex items-center justify-center">
                    <benefit.icon className="w-4 h-4 text-healing-600" />
                  </div>
                  <div>
                    <div className="font-medium text-sm">{benefit.title}</div>
                    <div className="text-xs text-muted-foreground">{benefit.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="pt-4 border-t">
            <Button 
              className="w-full bg-healing-600 hover:bg-healing-700 text-lg py-6"
              size="lg"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              지금 분석 시작하기
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default function DiagnosisPage() {
  return (
    <Layout>
      <div className="pt-20">
        {/* Header Section */}
        <section className="py-20 bg-gradient-to-br from-healing-50 via-sky-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-4xl mx-auto space-y-8"
            >
              <Badge variant="healing" className="mb-4 text-base px-6 py-2">
                <Sparkles className="w-5 h-5 mr-2" />
                AI POWERED ANALYSIS
              </Badge>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8">
                <span className="bg-gradient-to-r from-healing-600 via-sky-600 to-purple-600 bg-clip-text text-transparent">
                  나를 알면
                </span>
                <br />
                <span className="text-gray-900 dark:text-white">
                  미래가 보인다
                </span>
              </h1>
              
              <p className="text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                AI와 전통 지혜가 만나 탄생한 차세대 분석 시스템으로
                <br className="hidden sm:block" />
                <strong className="text-healing-600">진짜 나</strong>를 발견하고 <strong className="text-sky-600">미래</strong>를 설계하세요
              </p>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 pt-8 border-t border-gray-200 dark:border-gray-700">
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="text-center"
                >
                  <div className="text-4xl font-bold text-healing-600 mb-2">63,580</div>
                  <div className="text-sm text-muted-foreground">총 분석 완료</div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                  className="text-center"
                >
                  <div className="text-4xl font-bold text-sky-600 mb-2">94.8%</div>
                  <div className="text-sm text-muted-foreground">정확도</div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                  className="text-center"
                >
                  <div className="text-4xl font-bold text-purple-600 mb-2">4.9</div>
                  <div className="text-sm text-muted-foreground">만족도</div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.5 }}
                  className="text-center"
                >
                  <div className="text-4xl font-bold text-healing-600 mb-2">15분</div>
                  <div className="text-sm text-muted-foreground">평균 소요시간</div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Analysis Types */}
        <section className="py-20 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                <span className="bg-gradient-to-r from-healing-600 to-sky-600 bg-clip-text text-transparent">
                  3가지 분석 시스템
                </span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                각각의 전문성과 차별화된 접근 방식으로 당신의 진정한 모습을 찾아드립니다
              </p>
            </motion.div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {analysisTypes.map((analysis) => (
                <AnalysisCard key={analysis.id} analysis={analysis} />
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="py-20 bg-gray-50 dark:bg-gray-800">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl font-bold mb-6">실제 이용자 후기</h2>
              <p className="text-xl text-muted-foreground">
                이미 수만 명이 경험한 놀라운 변화를 확인해보세요
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
                  <Card className="p-6 h-full">
                    <CardContent className="p-0">
                      <div className="flex items-center mb-4">
                        {[...Array(testimonial.rating)].map((_, i) => (
                          <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                      <p className="text-muted-foreground mb-6 italic leading-relaxed">
                        "{testimonial.content}"
                      </p>
                      <div className="flex items-center space-x-3">
                        <div className="text-3xl">{testimonial.avatar}</div>
                        <div>
                          <div className="font-semibold">{testimonial.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {testimonial.age} • {testimonial.analysis}
                          </div>
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
        <section className="py-20 bg-gradient-to-r from-healing-600 via-sky-600 to-purple-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="max-w-4xl mx-auto space-y-8"
            >
              <h2 className="text-4xl md:text-5xl font-bold">
                오늘부터 새로운 나를 만나보세요
              </h2>
              <p className="text-2xl text-white/90 leading-relaxed">
                15분 투자로 평생의 가치를 발견하는 여정을 시작하세요
              </p>
              <div className="flex flex-col sm:flex-row gap-6 justify-center pt-8">
                <Button size="xl" variant="secondary" className="text-lg px-12 py-4">
                  <Sparkles className="w-6 h-6 mr-3" />
                  무료 체험하기
                </Button>
                <Button 
                  size="xl" 
                  variant="outline" 
                  className="border-2 border-white text-white hover:bg-white hover:text-healing-600 text-lg px-12 py-4"
                >
                  <PlayCircle className="w-6 h-6 mr-3" />
                  분석 과정 보기
                </Button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </Layout>
  )
}