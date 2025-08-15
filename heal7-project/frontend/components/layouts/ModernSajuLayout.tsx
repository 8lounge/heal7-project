'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/radix-tabs';
import { SajuResult } from '@/types/saju';
import { SajuBoard } from '@/components/charts/SajuBoard';
import { InteractiveSajuWheel } from '@/components/charts/InteractiveSajuWheel';
import { SajuInfographic } from '@/components/charts/SajuInfographic';
import { 
  ParticleBackground, 
  GlowCard, 
  TypewriterText, 
  CountUp,
  WaveBackground,
  FloatingElement
} from '@/components/ui/interactive-elements';
import { 
  Calendar,
  Sparkles,
  Target,
  TrendingUp,
  Heart,
  Brain,
  Zap,
  Download,
  Share2,
  Maximize2,
  RefreshCw
} from 'lucide-react';

interface ModernSajuLayoutProps {
  result: SajuResult;
  birthInfo: {
    date: string;
    time: string;
    isLunar?: boolean;
    timezone?: string;
  };
}

export function ModernSajuLayout({ result, birthInfo }: ModernSajuLayoutProps) {
  const [activeTab, setActiveTab] = useState('overview');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [animationPhase, setAnimationPhase] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationPhase(prev => (prev + 1) % 3);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  // 전체 운세 점수 계산
  const calculateOverallScore = () => {
    const wuxingBalance = Object.values(result.오행분석);
    const maxWuxing = Math.max(...wuxingBalance);
    const minWuxing = Math.min(...wuxingBalance);
    const balance = 100 - ((maxWuxing - minWuxing) * 8);
    return Math.min(Math.max(balance, 30), 95);
  };

  const overallScore = calculateOverallScore();

  // 주요 특성 추출
  const getMainCharacteristics = () => {
    const strongestSipsin = Object.entries(result.십신분석)
      .sort(([,a], [,b]) => b - a)[0];
    const dominantWuxing = Object.entries(result.오행분석)
      .sort(([,a], [,b]) => b - a)[0];
    
    return {
      sipsin: strongestSipsin[0],
      wuxing: dominantWuxing[0],
      격국: result.격국
    };
  };

  const characteristics = getMainCharacteristics();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 
                    text-white overflow-hidden relative">
      {/* 배경 효과들 */}
      <ParticleBackground color="#8b5cf6" />
      <WaveBackground color="#3b82f6" opacity={0.05} />
      
      {/* 메인 컨테이너 */}
      <div className={`relative z-10 ${isFullscreen ? 'fixed inset-0 bg-slate-900/95 backdrop-blur-sm' : ''}`}>
        {/* 헤더 */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="sticky top-0 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50 z-20"
        >
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <FloatingElement intensity={0.5}>
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 
                                 flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                </FloatingElement>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 
                                bg-clip-text text-transparent">
                    AI 사주명리학 분석
                  </h1>
                  <p className="text-slate-400 text-sm">
                    {birthInfo.date} {birthInfo.time} • {birthInfo.isLunar ? '음력' : '양력'}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 
                       border-green-500/30 text-green-200 px-3 py-1">
                  <CountUp end={overallScore} className="font-bold" />점
                </Badge>
                <Button variant="ghost" size="sm" onClick={() => window.location.reload()}>
                  <RefreshCw className="w-4 h-4" />
                </Button>
                <Button variant="ghost" size="sm">
                  <Share2 className="w-4 h-4" />
                </Button>
                <Button variant="ghost" size="sm">
                  <Download className="w-4 h-4" />
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setIsFullscreen(!isFullscreen)}
                >
                  <Maximize2 className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* 메인 컨텐츠 */}
        <div className="container mx-auto px-4 py-8">
          {/* 요약 카드 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-8"
          >
            <GlowCard glowColor="#8b5cf6">
              <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700/50">
                <CardContent className="p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* 전체 운세 */}
                    <div className="text-center">
                      <div className="mb-4">
                        <div className="text-3xl font-bold text-white mb-2">
                          <CountUp end={overallScore} />점
                        </div>
                        <div className="text-slate-400">종합 운세</div>
                      </div>
                      <div className="relative w-20 h-20 mx-auto">
                        <svg className="w-20 h-20 transform -rotate-90">
                          <circle
                            cx="40"
                            cy="40"
                            r="36"
                            stroke="#374151"
                            strokeWidth="8"
                            fill="transparent"
                          />
                          <circle
                            cx="40"
                            cy="40"
                            r="36"
                            stroke="url(#gradient)"
                            strokeWidth="8"
                            fill="transparent"
                            strokeDasharray={`${2 * Math.PI * 36}`}
                            strokeDashoffset={`${2 * Math.PI * 36 * (1 - overallScore / 100)}`}
                            strokeLinecap="round"
                            className="transition-all duration-2000 ease-out"
                          />
                          <defs>
                            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                              <stop offset="0%" stopColor="#8b5cf6" />
                              <stop offset="100%" stopColor="#06b6d4" />
                            </linearGradient>
                          </defs>
                        </svg>
                      </div>
                    </div>

                    {/* 격국 정보 */}
                    <div className="text-center">
                      <div className="mb-4">
                        <Badge variant="outline" className="text-lg px-4 py-2 bg-gradient-to-r 
                               from-yellow-500/20 to-orange-500/20 border-yellow-500/30 text-yellow-200">
                          {result.격국}
                        </Badge>
                      </div>
                      <TypewriterText 
                        text="당신의 사주 격국은 안정적이고 균형잡힌 발전 가능성을 보여줍니다."
                        speed={30}
                        className="text-sm text-slate-400"
                      />
                    </div>

                    {/* 주요 특성 */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-slate-400 text-sm">주요 십신</span>
                        <Badge variant="secondary" className="bg-purple-500/20 text-purple-200">
                          {characteristics.sipsin}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-400 text-sm">주요 오행</span>
                        <Badge variant="secondary" className="bg-blue-500/20 text-blue-200">
                          {characteristics.wuxing}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-400 text-sm">운세 트렌드</span>
                        <div className="flex items-center gap-1">
                          <TrendingUp className="w-4 h-4 text-green-400" />
                          <span className="text-green-400 text-sm">상승</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </GlowCard>
          </motion.div>

          {/* 탭 네비게이션 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="grid w-full grid-cols-4 bg-slate-800/50 backdrop-blur-sm">
                <TabsTrigger 
                  value="overview" 
                  className="flex items-center gap-2 data-[state=active]:bg-purple-500/20"
                >
                  <Target className="w-4 h-4" />
                  종합분석
                </TabsTrigger>
                <TabsTrigger 
                  value="interactive" 
                  className="flex items-center gap-2 data-[state=active]:bg-purple-500/20"
                >
                  <Zap className="w-4 h-4" />
                  인터랙티브
                </TabsTrigger>
                <TabsTrigger 
                  value="detailed" 
                  className="flex items-center gap-2 data-[state=active]:bg-purple-500/20"
                >
                  <Brain className="w-4 h-4" />
                  상세분석
                </TabsTrigger>
                <TabsTrigger 
                  value="traditional" 
                  className="flex items-center gap-2 data-[state=active]:bg-purple-500/20"
                >
                  <Calendar className="w-4 h-4" />
                  전통사주
                </TabsTrigger>
              </TabsList>

              <AnimatePresence mode="wait">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <TabsContent value="overview" className="space-y-6">
                    <SajuInfographic result={result} />
                  </TabsContent>

                  <TabsContent value="interactive" className="space-y-6">
                    <InteractiveSajuWheel result={result} />
                  </TabsContent>

                  <TabsContent value="detailed" className="space-y-6">
                    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                      <SajuInfographic result={result} />
                      <InteractiveSajuWheel result={result} />
                    </div>
                  </TabsContent>

                  <TabsContent value="traditional" className="space-y-6">
                    <SajuBoard pillars={result.사주} />
                  </TabsContent>
                </motion.div>
              </AnimatePresence>
            </Tabs>
          </motion.div>

          {/* 추가 인사이트 섹션 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="mt-12"
          >
            <GlowCard glowColor="#06b6d4">
              <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-200">
                    <Heart className="w-5 h-5 text-pink-400" />
                    개인화된 조언
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <h4 className="font-medium text-slate-200">💎 당신의 강점</h4>
                      <div className="space-y-2 text-sm text-slate-400">
                        <p>• {characteristics.sipsin} 특성으로 인한 뛰어난 적응력</p>
                        <p>• {characteristics.wuxing} 기운이 강해 안정적인 성장 가능</p>
                        <p>• {result.격국} 격국으로 꾸준한 발전 운세</p>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <h4 className="font-medium text-slate-200">🎯 발전 방향</h4>
                      <div className="space-y-2 text-sm text-slate-400">
                        <p>• 오행의 균형을 맞춰 전체적인 조화 추구</p>
                        <p>• 타고난 특성을 살려 전문성 개발</p>
                        <p>• 인간관계에서 신뢰를 바탕으로 한 성장</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </GlowCard>
          </motion.div>
        </div>
      </div>
    </div>
  );
}