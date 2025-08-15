/**
 * HEAL7 사주명리학 시스템 - 메인 페이지
 */

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Calculator, Sparkles, Users, TrendingUp, Shield, Zap } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-background/50">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="mx-auto max-w-4xl space-y-8">
          <Badge variant="secondary" className="mb-4">
            <Sparkles className="mr-2 h-4 w-4" />
            프론트엔드 중심 아키텍처
          </Badge>
          
          <h1 className="text-4xl font-bold tracking-tight text-gradient sm:text-6xl">
            HEAL7 사주명리학
          </h1>
          
          <p className="text-xl text-muted-foreground">
            정확하고 과학적인 사주명리학 서비스
            <br />
            <span className="text-primary font-semibold">KASI 데이터 기반</span> • 
            <span className="text-primary font-semibold"> 실시간 계산</span> • 
            <span className="text-primary font-semibold"> 오프라인 지원</span>
          </p>
          
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Button asChild size="lg" className="hover-lift">
              <Link href="/saju/calculate">
                <Calculator className="mr-2 h-5 w-5" />
                사주 계산하기
              </Link>
            </Button>
            
            <Button variant="outline" size="lg" asChild className="hover-lift">
              <Link href="/about">
                <Shield className="mr-2 h-5 w-5" />
                서비스 소개
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">핵심 특징</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            최신 기술과 전통 명리학의 만남으로 정확하고 신뢰할 수 있는 사주 서비스를 제공합니다
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="saju-card hover-glow">
            <CardHeader>
              <div className="mb-4">
                <Zap className="h-12 w-12 text-saju-fire" />
              </div>
              <CardTitle>실시간 계산</CardTitle>
              <CardDescription>
                프론트엔드에서 직접 계산하여 서버 지연 없는 즉시 결과 제공
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-fire rounded-full"></span>
                  0.3초 초고속 계산
                </li>
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-fire rounded-full"></span>
                  네트워크 지연 없음
                </li>
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-fire rounded-full"></span>
                  오프라인 지원
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card className="saju-card hover-glow">
            <CardHeader>
              <div className="mb-4">
                <Shield className="h-12 w-12 text-saju-water" />
              </div>
              <CardTitle>KASI 데이터 기반</CardTitle>
              <CardDescription>
                한국천문연구원 공식 데이터로 보장하는 100% 정확한 만세력
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-water rounded-full"></span>
                  공식 천문 데이터
                </li>
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-water rounded-full"></span>
                  진태양시 보정
                </li>
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-water rounded-full"></span>
                  24절기 정확 계산
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card className="saju-card hover-glow">
            <CardHeader>
              <div className="mb-4">
                <TrendingUp className="h-12 w-12 text-saju-wood" />
              </div>
              <CardTitle>종합 분석</CardTitle>
              <CardDescription>
                오행, 십신, 격국 등 전통 명리학의 모든 요소를 체계적으로 분석
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-wood rounded-full"></span>
                  오행 균형 분석
                </li>
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-wood rounded-full"></span>
                  십신 관계 해석
                </li>
                <li className="flex items-center">
                  <span className="mr-2 h-2 w-2 bg-saju-wood rounded-full"></span>
                  개인 맞춤 조언
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-muted/30 py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary">99.9%</div>
              <div className="text-sm text-muted-foreground">계산 정확도</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">0.3초</div>
              <div className="text-sm text-muted-foreground">평균 계산 시간</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">24/7</div>
              <div className="text-sm text-muted-foreground">오프라인 지원</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">100%</div>
              <div className="text-sm text-muted-foreground">KASI 호환성</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="mx-auto max-w-2xl space-y-8">
          <h2 className="text-3xl font-bold">지금 바로 시작해보세요</h2>
          <p className="text-muted-foreground">
            정확한 생년월일시만 있으면 몇 초 안에 완벽한 사주 분석 결과를 확인할 수 있습니다
          </p>
          
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Button asChild size="lg" className="hover-lift animate-saju-glow">
              <Link href="/saju/calculate">
                <Calculator className="mr-2 h-5 w-5" />
                무료 사주 계산
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}