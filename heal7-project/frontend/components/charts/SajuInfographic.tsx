'use client';

import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/radix-progress';
import { Badge } from '@/components/ui/badge';
import { SajuResult } from '@/types/saju';
import { 
  TrendingUp, 
  Heart, 
  DollarSign, 
  Crown, 
  Brain, 
  Zap,
  Star,
  Target,
  Activity
} from 'lucide-react';

interface SajuInfographicProps {
  result: SajuResult;
  className?: string;
}

// 운세별 아이콘 매핑
const FORTUNE_ICONS = {
  연애운: Heart,
  재물운: DollarSign,
  건강운: Activity,
  사업운: TrendingUp,
  학업운: Brain,
  인기운: Star,
  직업운: Crown,
  가족운: Target
};

// 십신별 특성 매핑
const SIPSIN_TRAITS = {
  비겁: { 
    name: '비견겁재', 
    traits: ['자립심', '경쟁력', '동료의식'],
    color: '#8b5cf6',
    description: '형제자매, 친구, 동업자를 나타내며 자립심과 경쟁의식이 강함'
  },
  식상: { 
    name: '식신상관', 
    traits: ['창조력', '표현력', '자유로움'],
    color: '#06b6d4',
    description: '재능과 아이디어를 표현하며 자유롭고 창조적인 성향'
  },
  재성: { 
    name: '편재정재', 
    traits: ['재물관리', '현실감각', '안정추구'],
    color: '#eab308',
    description: '재물과 물질적 풍요를 관리하는 능력과 현실적 사고'
  },
  관살: { 
    name: '편관정관', 
    traits: ['리더십', '책임감', '권위'],
    color: '#ef4444',
    description: '권위와 지위를 나타내며 리더십과 책임감이 강함'
  },
  인성: { 
    name: '편인정인', 
    traits: ['학습력', '보호본능', '지혜'],
    color: '#22c55e',
    description: '학습과 지혜를 상징하며 보호받고 보호하는 성향'
  }
};

// 오행별 성격 특성
const WUXING_PERSONALITY = {
  목: {
    name: '목(木)',
    traits: ['성장지향', '유연성', '창의성'],
    color: '#22c55e',
    personality: '봄의 에너지처럼 성장하고 발전하려는 의지가 강하며 유연한 사고를 가짐'
  },
  화: {
    name: '화(火)',
    traits: ['열정적', '활동적', '사교성'],
    color: '#ef4444',
    personality: '여름의 에너지처럼 열정적이고 활발하며 사람들과 어울리기를 좋아함'
  },
  토: {
    name: '토(土)',
    traits: ['안정감', '신뢰성', '포용력'],
    color: '#eab308',
    personality: '대지처럼 안정적이고 신뢰할 수 있으며 다른 사람을 포용하는 성향'
  },
  금: {
    name: '금(金)',
    traits: ['의리', '원칙성', '결단력'],
    color: '#f3f4f6',
    personality: '가을의 에너지처럼 원칙을 중시하고 의리를 지키며 결단력이 강함'
  },
  수: {
    name: '수(水)',
    traits: ['지혜', '적응력', '깊이'],
    color: '#3b82f6',
    personality: '겨울의 에너지처럼 깊은 사고를 하며 상황에 잘 적응하고 지혜로움'
  }
};

export function SajuInfographic({ result, className }: SajuInfographicProps) {
  const [visibleSection, setVisibleSection] = useState(0);
  const [animationTrigger, setAnimationTrigger] = useState(0);
  const observerRef = useRef<IntersectionObserver | null>(null);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationTrigger(prev => prev + 1);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // 주요 운세 계산
  const calculateFortunes = () => {
    const fortunes = [];
    const wuxingValues = Object.values(result.오행분석);
    const sipsunValues = Object.values(result.십신분석);
    
    // 오행 균형도를 바탕으로 한 운세
    const maxWuxing = Math.max(...wuxingValues);
    const minWuxing = Math.min(...wuxingValues);
    const balance = 100 - ((maxWuxing - minWuxing) * 10);
    
    fortunes.push({ name: '전체운', score: Math.min(balance, 100), icon: Zap });
    fortunes.push({ name: '연애운', score: result.오행분석.화 * 15 + 20, icon: Heart });
    fortunes.push({ name: '재물운', score: result.오행분석.토 * 12 + result.십신분석.재성 * 8 + 10, icon: DollarSign });
    fortunes.push({ name: '건강운', score: result.오행분석.목 * 10 + result.오행분석.수 * 8 + 25, icon: Activity });
    fortunes.push({ name: '사업운', score: result.십신분석.관살 * 12 + result.오행분석.금 * 8 + 15, icon: TrendingUp });
    
    return fortunes.map(f => ({ ...f, score: Math.min(Math.max(f.score, 10), 95) }));
  };

  const fortunes = calculateFortunes();

  // 강한 십신 찾기
  const strongestSipsin = Object.entries(result.십신분석)
    .sort(([,a], [,b]) => b - a)[0];

  // 균형 잡힌 오행 찾기
  const balancedWuxing = Object.entries(result.오행분석)
    .filter(([,value]) => value >= 2 && value <= 4);

  return (
    <div className={`space-y-6 ${className}`}>
      {/* 종합 운세 대시보드 */}
      <Card className="overflow-hidden">
        <CardHeader>
          <CardTitle className="text-slate-200 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-400" />
            종합 운세 분석
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {fortunes.map((fortune, index) => {
              const Icon = fortune.icon;
              const scoreLevel = fortune.score >= 80 ? 'excellent' : 
                               fortune.score >= 60 ? 'good' : 
                               fortune.score >= 40 ? 'average' : 'poor';
              
              const levelColors = {
                excellent: 'from-green-500 to-emerald-400',
                good: 'from-blue-500 to-cyan-400',
                average: 'from-yellow-500 to-orange-400',
                poor: 'from-red-500 to-pink-400'
              };

              return (
                <div key={fortune.name} 
                     className="bg-slate-800/50 rounded-lg p-4 relative overflow-hidden">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Icon className="w-5 h-5 text-slate-300" />
                      <span className="text-slate-200 font-medium">{fortune.name}</span>
                    </div>
                    <Badge variant="outline" 
                           className={`bg-gradient-to-r ${levelColors[scoreLevel]} border-none text-white`}>
                      {fortune.score}점
                    </Badge>
                  </div>
                  
                  <div className="relative">
                    <Progress 
                      value={fortune.score} 
                      className="h-3"
                    />
                    <div className={`absolute inset-0 bg-gradient-to-r ${levelColors[scoreLevel]} 
                                    opacity-20 rounded-full animate-pulse`}></div>
                  </div>
                  
                  {/* 글로우 효과 */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${levelColors[scoreLevel]} 
                                  opacity-5 animate-pulse`}></div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* 성격 특성 분석 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-slate-200 flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" />
            성격 특성 분석
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 십신 기반 성격 */}
            <div>
              <h4 className="text-slate-300 font-medium mb-4">주요 성향 (십신 기반)</h4>
              <div className="space-y-4">
                {strongestSipsin && SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS] && (
                  <div className="bg-slate-800/30 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-4 h-4 rounded-full" 
                           style={{ backgroundColor: SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS].color }}>
                      </div>
                      <span className="text-slate-200 font-medium">
                        {SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS].name}
                      </span>
                      <Badge variant="secondary" className="ml-auto">
                        {strongestSipsin[1]}개
                      </Badge>
                    </div>
                    <p className="text-slate-400 text-sm mb-3">
                      {SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS].description}
                    </p>
                    <div className="flex gap-2 flex-wrap">
                      {SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS].traits.map(trait => (
                        <Badge key={trait} variant="outline" className="text-xs">
                          {trait}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* 오행 기반 성격 */}
            <div>
              <h4 className="text-slate-300 font-medium mb-4">기질적 특성 (오행 기반)</h4>
              <div className="space-y-3">
                {balancedWuxing.slice(0, 2).map(([wuxing, value]) => {
                  const trait = WUXING_PERSONALITY[wuxing as keyof typeof WUXING_PERSONALITY];
                  return (
                    <div key={wuxing} className="bg-slate-800/30 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-4 h-4 rounded-full" style={{ backgroundColor: trait.color }}></div>
                        <span className="text-slate-200 font-medium">{trait.name}</span>
                        <div className="ml-auto flex gap-1">
                          {[...Array(Math.min(value, 5))].map((_, i) => (
                            <div key={i} className="w-2 h-2 rounded-full" 
                                 style={{ backgroundColor: trait.color }}></div>
                          ))}
                        </div>
                      </div>
                      <p className="text-slate-400 text-sm mb-2">{trait.personality}</p>
                      <div className="flex gap-2 flex-wrap">
                        {trait.traits.map(t => (
                          <Badge key={t} variant="outline" className="text-xs">
                            {t}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 생애 주기별 분석 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-slate-200 flex items-center gap-2">
            <Target className="w-5 h-5 text-green-400" />
            생애 주기별 특징
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { period: '유년기', pillar: result.사주.년주, age: '0-15세', focus: '가정환경' },
              { period: '청년기', pillar: result.사주.월주, age: '16-30세', focus: '학업·커리어' },
              { period: '장년기', pillar: result.사주.일주, age: '31-45세', focus: '결혼·사업' },
              { period: '노년기', pillar: result.사주.시주, age: '46세+', focus: '자녀·여가' }
            ].map((phase, index) => (
              <div key={phase.period} 
                   className="bg-slate-800/50 rounded-lg p-4 relative overflow-hidden">
                <div className="text-center mb-3">
                  <div className="text-lg font-bold text-white mb-1">{phase.period}</div>
                  <div className="text-xs text-slate-400 mb-1">{phase.age}</div>
                  <div className="text-xs text-slate-500">{phase.focus}</div>
                </div>
                
                <div className="text-center">
                  <div className="inline-flex items-center gap-2 bg-slate-700/50 rounded-full px-3 py-1">
                    <span className="text-sm text-slate-200">{phase.pillar.천간}</span>
                    <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                    <span className="text-sm text-slate-200">{phase.pillar.지지}</span>
                  </div>
                </div>

                {/* 생애 주기 표시선 */}
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r 
                               from-purple-500 via-blue-500 to-green-500"
                     style={{ opacity: 0.3 + (index * 0.2) }}></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 격국별 조언 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-slate-200 flex items-center gap-2">
            <Crown className="w-5 h-5 text-yellow-400" />
            맞춤형 인생 조언
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <Badge variant="outline" className="text-lg px-4 py-2 bg-gradient-to-r 
                     from-yellow-500/20 to-orange-500/20 border-yellow-500/30 text-yellow-200">
                {result.격국}
              </Badge>
              <div className="h-px flex-1 bg-gradient-to-r from-yellow-500/30 to-transparent"></div>
            </div>
            
            <div className="space-y-4 text-slate-300">
              <div>
                <h5 className="font-medium text-slate-200 mb-2">🎯 추천 발전 방향</h5>
                <p className="text-sm">
                  {result.격국}의 특성을 살려 안정적인 성장을 추구하되, 
                  오행의 균형을 맞춰 전체적인 조화를 이루는 것이 중요합니다.
                </p>
              </div>
              
              <div>
                <h5 className="font-medium text-slate-200 mb-2">💎 활용할 강점</h5>
                <p className="text-sm">
                  {strongestSipsin && SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS] ? 
                    `${SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS].name}의 특성인 
                     ${SIPSIN_TRAITS[strongestSipsin[0] as keyof typeof SIPSIN_TRAITS].traits.join(', ')}을 
                     적극 활용하여 자신만의 영역을 구축하세요.` :
                    '균형 잡힌 사주로 다방면에서 안정적인 발전이 가능합니다.'
                  }
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}