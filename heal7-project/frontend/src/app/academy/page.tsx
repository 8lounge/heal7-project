'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Layout } from '@/components/layout/Layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  BookOpen, 
  Star, 
  Users,
  Clock,
  PlayCircle,
  TrendingUp,
  Award,
  Calendar,
  User,
  Target,
  Sparkles,
  ArrowRight,
  CheckCircle
} from 'lucide-react'

const categories = [
  { id: 'all', name: '전체 강의', count: 15 },
  { id: 'personality', name: '성향 분석', count: 6 },
  { id: 'psychology', name: '심리학', count: 4 },
  { id: 'meditation', name: '명상/힐링', count: 3 },
  { id: 'career', name: '진로 개발', count: 2 }
]

const courses = [
  {
    id: 1,
    title: '3D 성향분석 마스터 클래스',
    description: '나를 완전히 이해하는 3차원 성향분석의 모든 것을 배우고 활용하는 완벽한 가이드',
    instructor: '김희정 대표',
    duration: '8주 과정',
    lessons: 32,
    students: 1247,
    rating: 4.9,
    price: 298000,
    originalPrice: 398000,
    image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&h=400&fit=crop',
    category: 'personality',
    level: '초급-중급',
    badge: 'BEST',
    status: 'ongoing',
    progress: 68,
    features: ['1:1 멘토링', '실습 프로젝트', '수료증 발급', '평생 복습'],
    nextStart: '2025-08-25'
  },
  {
    id: 2,
    title: 'AI 심리분석 전문가 양성과정',
    description: 'AI 기술과 심리학을 융합한 차세대 심리분석 전문가로 성장하는 체계적 교육',
    instructor: '박민수 교수',
    duration: '12주 과정',
    lessons: 48,
    students: 892,
    rating: 4.8,
    price: 498000,
    originalPrice: 698000,
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
    category: 'psychology',
    level: '중급-고급',
    badge: 'NEW',
    status: 'upcoming',
    progress: 0,
    features: ['AI 도구 활용', '케이스 스터디', '자격증 준비', '취업 연계'],
    nextStart: '2025-09-01'
  },
  {
    id: 3,
    title: '명상과 마음챙김 실천 워크숍',
    description: '일상에서 실천할 수 있는 명상과 마음챙김 기법을 배우는 실용적 과정',
    instructor: '이정은 명상치료사',
    duration: '4주 과정',
    lessons: 16,
    students: 654,
    rating: 4.7,
    price: 158000,
    originalPrice: null,
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop',
    category: 'meditation',
    level: '입문',
    badge: 'HOT',
    status: 'ongoing',
    progress: 25,
    features: ['실시간 세션', '개인 상담', '명상 가이드', '커뮤니티'],
    nextStart: '2025-08-30'
  },
  {
    id: 4,
    title: '현대 명리학과 진로 컨설팅',
    description: '전통 명리학을 현대적으로 해석하여 진로와 인생 설계에 활용하는 방법',
    instructor: '최서윤 명리학박사',
    duration: '6주 과정',
    lessons: 24,
    students: 423,
    rating: 4.6,
    price: 248000,
    originalPrice: 318000,
    image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&h=400&fit=crop',
    category: 'career',
    level: '중급',
    badge: null,
    status: 'upcoming',
    progress: 0,
    features: ['개인 사주 해석', '진로 로드맵', '1:1 컨설팅', '평생 지원'],
    nextStart: '2025-09-15'
  },
  {
    id: 5,
    title: '감정 조절과 스트레스 관리',
    description: '과학적 접근을 통한 감정 조절 능력 향상과 효과적인 스트레스 관리 기법',
    instructor: '정혜민 심리치료사',
    duration: '5주 과정',
    lessons: 20,
    students: 789,
    rating: 4.8,
    price: 198000,
    originalPrice: null,
    image: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&h=400&fit=crop',
    category: 'psychology',
    level: '초급-중급',
    badge: null,
    status: 'ongoing',
    progress: 45,
    features: ['심리 테스트', '실습 워크북', '그룹 상담', '애프터케어'],
    nextStart: '2025-09-08'
  },
  {
    id: 6,
    title: '힐링 라이프스타일 디자인',
    description: '건강하고 균형 잡힌 라이프스타일을 설계하고 실천하는 통합적 접근법',
    instructor: '김나영 라이프코치',
    duration: '8주 과정',
    lessons: 32,
    students: 567,
    rating: 4.5,
    price: 268000,
    originalPrice: 348000,
    image: 'https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=600&h=400&fit=crop',
    category: 'meditation',
    level: '입문-초급',
    badge: null,
    status: 'upcoming',
    progress: 0,
    features: ['라이프 플래닝', '습관 형성', '건강 관리', '지속 코칭'],
    nextStart: '2025-09-22'
  }
]

const CourseCard: React.FC<{ course: typeof courses[0] }> = ({ course }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -5 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="group cursor-pointer border-0 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden">
        <div className="relative">
          <div
            className="aspect-[16/10] bg-cover bg-center group-hover:scale-105 transition-transform duration-300"
            style={{ backgroundImage: `url(${course.image})` }}
          />
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300" />
          
          {/* Badge */}
          {course.badge && (
            <Badge 
              variant={course.badge === 'BEST' ? 'healing' : course.badge === 'HOT' ? 'destructive' : 'secondary'}
              className="absolute top-4 left-4"
            >
              {course.badge}
            </Badge>
          )}

          {/* Status */}
          <div className="absolute top-4 right-4">
            <Badge 
              variant={course.status === 'ongoing' ? 'default' : 'outline'}
              className="bg-white/90 text-gray-900"
            >
              {course.status === 'ongoing' ? '진행중' : '모집중'}
            </Badge>
          </div>

          {/* Play Button */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <PlayCircle className="w-16 h-16 text-white drop-shadow-lg" />
          </div>
        </div>
        
        <CardHeader className="pb-4">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1">
              <CardTitle className="text-xl font-bold line-clamp-2 group-hover:text-healing-600 transition-colors mb-2">
                {course.title}
              </CardTitle>
              <CardDescription className="line-clamp-2 mb-3">
                {course.description}
              </CardDescription>
            </div>
          </div>

          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <User className="w-4 h-4" />
              <span>{course.instructor}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>{course.duration}</span>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-0 space-y-4">
          {/* Stats */}
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1 text-yellow-500">
                <Star className="w-4 h-4 fill-current" />
                <span className="font-medium">{course.rating}</span>
              </div>
              <div className="flex items-center gap-1 text-muted-foreground">
                <Users className="w-4 h-4" />
                <span>{course.students.toLocaleString()}명</span>
              </div>
              <div className="flex items-center gap-1 text-muted-foreground">
                <BookOpen className="w-4 h-4" />
                <span>{course.lessons}강의</span>
              </div>
            </div>
            <Badge variant="outline" className="text-xs">
              {course.level}
            </Badge>
          </div>

          {/* Progress (if ongoing) */}
          {course.status === 'ongoing' && course.progress > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">진행률</span>
                <span className="font-medium">{course.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-healing-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${course.progress}%` }}
                />
              </div>
            </div>
          )}

          {/* Features */}
          <div className="flex flex-wrap gap-2">
            {course.features.slice(0, 3).map((feature) => (
              <Badge key={feature} variant="secondary" className="text-xs">
                {feature}
              </Badge>
            ))}
            {course.features.length > 3 && (
              <Badge variant="secondary" className="text-xs">
                +{course.features.length - 3}
              </Badge>
            )}
          </div>

          {/* Price & CTA */}
          <div className="flex items-center justify-between pt-4 border-t">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-2xl font-bold text-healing-600">
                  {course.price.toLocaleString()}원
                </span>
                {course.originalPrice && (
                  <span className="text-sm text-muted-foreground line-through">
                    {course.originalPrice.toLocaleString()}원
                  </span>
                )}
              </div>
              <div className="text-sm text-muted-foreground">
                <Calendar className="w-4 h-4 inline mr-1" />
                개강: {course.nextStart}
              </div>
            </div>
            <Button className="bg-healing-600 hover:bg-healing-700">
              {course.status === 'ongoing' ? '계속 학습' : '수강 신청'}
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default function AcademyPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')

  const filteredCourses = courses.filter(course => 
    selectedCategory === 'all' || course.category === selectedCategory
  )

  return (
    <Layout>
      <div className="pt-20">
        {/* Header Section */}
        <section className="py-16 bg-gradient-to-br from-sky-50 via-healing-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-4xl mx-auto space-y-6"
            >
              <Badge variant="healing" className="mb-4">
                <BookOpen className="w-4 h-4 mr-2" />
                HEALING ACADEMY
              </Badge>
              
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
                <span className="bg-gradient-to-r from-sky-600 to-healing-600 bg-clip-text text-transparent">
                  체험 아카데미
                </span>
              </h1>
              
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                전문가와 함께하는 체계적인 성장 여정을 시작하세요.
                <br className="hidden sm:block" />
                크라우드펀딩 방식으로 더 많은 분들과 함께 배우고 성장할 수 있습니다.
              </p>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="text-center"
                >
                  <div className="text-3xl font-bold text-healing-600 mb-2">15+</div>
                  <div className="text-sm text-muted-foreground">전문 강의</div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                  className="text-center"
                >
                  <div className="text-3xl font-bold text-sky-600 mb-2">5,000+</div>
                  <div className="text-sm text-muted-foreground">수강생</div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                  className="text-center"
                >
                  <div className="text-3xl font-bold text-healing-600 mb-2">98%</div>
                  <div className="text-sm text-muted-foreground">만족도</div>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.5 }}
                  className="text-center"
                >
                  <div className="text-3xl font-bold text-sky-600 mb-2">4.8</div>
                  <div className="text-sm text-muted-foreground">평균 평점</div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Categories & Courses */}
        <section className="py-16 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            {/* Category Filter */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-wrap justify-center gap-4 mb-12"
            >
              {categories.map((category) => (
                <Button
                  key={category.id}
                  variant={selectedCategory === category.id ? "healing" : "outline"}
                  size="lg"
                  onClick={() => setSelectedCategory(category.id)}
                  className="rounded-full"
                >
                  {category.name}
                  <Badge variant="secondary" className="ml-2 text-xs">
                    {category.count}
                  </Badge>
                </Button>
              ))}
            </motion.div>

            {/* Courses Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {filteredCourses.map((course) => (
                <CourseCard key={course.id} course={course} />
              ))}
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-16 bg-gray-50 dark:bg-gray-800">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                아카데미만의 특별한 혜택
              </h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                단순한 강의가 아닌, 평생 함께하는 성장 파트너가 되겠습니다
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {[
                {
                  icon: Award,
                  title: '전문가 인증',
                  description: '각 분야 최고 전문가들의 검증된 커리큘럼과 1:1 멘토링'
                },
                {
                  icon: Users,
                  title: '커뮤니티 학습',
                  description: '함께 배우는 동료들과의 네트워킹과 지속적인 동기부여'
                },
                {
                  icon: Target,
                  title: '실무 적용',
                  description: '이론뿐만 아니라 실제 상황에 바로 적용할 수 있는 실용적 교육'
                },
                {
                  icon: CheckCircle,
                  title: '평생 지원',
                  description: '수료 후에도 지속되는 애프터케어와 업데이트된 콘텐츠 제공'
                },
                {
                  icon: TrendingUp,
                  title: '개인 맞춤',
                  description: '개인별 성향과 목표에 따른 맞춤형 학습 경로 제공'
                },
                {
                  icon: Sparkles,
                  title: '최신 기술',
                  description: 'AI와 최신 기술을 활용한 혁신적인 학습 경험'
                }
              ].map((benefit, index) => (
                <motion.div
                  key={benefit.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: 0.1 * index }}
                >
                  <Card className="text-center p-6 h-full">
                    <benefit.icon className="w-12 h-12 text-healing-600 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold mb-3">{benefit.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {benefit.description}
                    </p>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-sky-600 to-healing-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="max-w-3xl mx-auto space-y-8"
            >
              <h2 className="text-3xl md:text-4xl font-bold">
                지금 시작하면 특별 할인 혜택!
              </h2>
              <p className="text-xl text-sky-100">
                얼리버드 등록 시 최대 30% 할인된 가격으로 수강하실 수 있습니다
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="xl" variant="secondary">
                  <BookOpen className="w-5 h-5 mr-2" />
                  무료 체험강의 듣기
                </Button>
                <Button size="xl" variant="outline" className="border-white text-white hover:bg-white hover:text-sky-600">
                  <Users className="w-5 h-5 mr-2" />
                  수강생 후기 보기
                </Button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </Layout>
  )
}