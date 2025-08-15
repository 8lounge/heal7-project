'use client';

import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { SajuResult } from '@/types/saju';
import { RotateCcw, Zap, Calendar, Clock } from 'lucide-react';

interface InteractiveSajuWheelProps {
  result: SajuResult;
  className?: string;
}

// 오행 색상 매핑
const WUXING_COLORS = {
  목: { primary: '#22c55e', secondary: '#16a34a', glow: 'rgba(34, 197, 94, 0.3)' },
  화: { primary: '#ef4444', secondary: '#dc2626', glow: 'rgba(239, 68, 68, 0.3)' },
  토: { primary: '#eab308', secondary: '#ca8a04', glow: 'rgba(234, 179, 8, 0.3)' },
  금: { primary: '#f3f4f6', secondary: '#d1d5db', glow: 'rgba(243, 244, 246, 0.3)' },
  수: { primary: '#3b82f6', secondary: '#2563eb', glow: 'rgba(59, 130, 246, 0.3)' },
};

// 십신 색상 매핑
const SIPSIN_COLORS = {
  비겁: { color: '#8b5cf6', label: '비견겁재' },
  식상: { color: '#06b6d4', label: '식신상관' },
  재성: { color: '#eab308', label: '편재정재' },
  관살: { color: '#ef4444', label: '편관정관' },
  인성: { color: '#22c55e', label: '편인정인' },
};

// 천간지지 매핑
const CHEONGAN_HANJA = {
  '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
  '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸'
};

const JIJI_HANJA = {
  '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳',
  '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
};

export function InteractiveSajuWheel({ result, className }: InteractiveSajuWheelProps) {
  const [selectedPillar, setSelectedPillar] = useState<string | null>(null);
  const [animationPhase, setAnimationPhase] = useState(0);
  const [isRotating, setIsRotating] = useState(false);
  const wheelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationPhase(prev => (prev + 1) % 4);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const pillars = [
    { key: '년주', data: result.사주.년주, position: { top: '10%', left: '50%', transform: 'translateX(-50%)' }, label: '年柱', desc: '조상·유년기' },
    { key: '월주', data: result.사주.월주, position: { top: '50%', left: '10%', transform: 'translateY(-50%)' }, label: '月柱', desc: '부모·청년기' },
    { key: '일주', data: result.사주.일주, position: { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }, label: '日柱', desc: '본인·배우자' },
    { key: '시주', data: result.사주.시주, position: { top: '50%', right: '10%', transform: 'translateY(-50%)' }, label: '時柱', desc: '자식·노년기' }
  ];

  const startRotation = () => {
    setIsRotating(true);
    setTimeout(() => setIsRotating(false), 2000);
  };

  return (
    <Card className={`${className} overflow-hidden`}>
      <CardHeader className="pb-4">
        <CardTitle className="text-slate-200 flex items-center gap-2">
          <Calendar className="w-5 h-5 text-purple-400" />
          인터랙티브 사주 원반
          <button
            onClick={startRotation}
            className="ml-auto p-2 hover:bg-slate-700 rounded-full transition-colors"
          >
            <RotateCcw className={`w-4 h-4 text-slate-400 ${isRotating ? 'animate-spin' : ''}`} />
          </button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* 메인 사주 원반 */}
        <div className="relative w-80 h-80 mx-auto mb-8">
          {/* 배경 원반 */}
          <div
            ref={wheelRef}
            className={`absolute inset-0 rounded-full border-4 border-purple-500/30 bg-gradient-to-br from-slate-800/50 to-slate-900/80 backdrop-blur-sm ${isRotating ? 'animate-spin' : ''}`}
            style={{
              background: `conic-gradient(
                from ${animationPhase * 90}deg,
                #8b5cf6 0deg,
                #06b6d4 90deg,
                #eab308 180deg,
                #ef4444 270deg,
                #8b5cf6 360deg
              )`,
              padding: '4px'
            }}
          >
            <div className="w-full h-full rounded-full bg-slate-900/90 backdrop-blur-sm relative overflow-hidden">
              {/* 중앙 태극 심볼 */}
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-20 h-20">
                <div className="w-full h-full rounded-full bg-gradient-to-br from-white via-slate-200 to-black relative">
                  <div className="absolute top-0 left-1/2 w-1/2 h-1/2 bg-white rounded-tl-full"></div>
                  <div className="absolute bottom-0 right-1/2 w-1/2 h-1/2 bg-black rounded-br-full"></div>
                  <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-black rounded-full"></div>
                  <div className="absolute bottom-1/4 right-1/2 transform translate-x-1/2 w-2 h-2 bg-white rounded-full"></div>
                </div>
              </div>
            </div>
          </div>

          {/* 사주 기둥들 */}
          {pillars.map((pillar, index) => (
            <div
              key={pillar.key}
              className={`absolute cursor-pointer transition-all duration-300 ${
                selectedPillar === pillar.key ? 'scale-110 z-10' : 'hover:scale-105'
              }`}
              style={pillar.position}
              onClick={() => setSelectedPillar(selectedPillar === pillar.key ? null : pillar.key)}
            >
              <div className={`pillar-container relative ${pillar.key === '일주' ? 'ring-2 ring-purple-400/50' : ''}`}>
                {/* 기둥 카드 */}
                <div className="bg-slate-800/90 backdrop-blur-sm border border-slate-600/50 rounded-lg p-3 min-w-[80px] shadow-xl">
                  {/* 한자 표기 */}
                  <div className="text-center mb-2">
                    <div className="text-xs text-slate-400 font-medium">{pillar.label}</div>
                    <div className="text-xs text-slate-500">{pillar.desc}</div>
                  </div>

                  {/* 천간 */}
                  <div className="text-center mb-1">
                    <div className="text-lg font-bold text-white">
                      {CHEONGAN_HANJA[pillar.data.천간 as keyof typeof CHEONGAN_HANJA] || pillar.data.천간}
                    </div>
                  </div>

                  {/* 지지 */}
                  <div className="text-center">
                    <div className="text-lg font-bold text-white">
                      {JIJI_HANJA[pillar.data.지지 as keyof typeof JIJI_HANJA] || pillar.data.지지}
                    </div>
                  </div>

                  {/* 선택된 기둥의 추가 정보 */}
                  {selectedPillar === pillar.key && (
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg p-3 shadow-xl min-w-[200px] z-20">
                      <div className="text-sm text-slate-300 font-medium mb-2">{pillar.key} 상세정보</div>
                      <div className="space-y-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-slate-400">천간:</span>
                          <span className="text-white">{pillar.data.천간} ({pillar.data.한자천간})</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">지지:</span>
                          <span className="text-white">{pillar.data.지지} ({pillar.data.한자지지})</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* 글로우 효과 */}
                {selectedPillar === pillar.key && (
                  <div className="absolute inset-0 rounded-lg bg-purple-400/20 blur-xl -z-10 animate-pulse"></div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* 오행 분석 바 */}
        <div className="mb-6">
          <h4 className="text-slate-200 font-medium mb-3 flex items-center gap-2">
            <Zap className="w-4 h-4 text-yellow-400" />
            오행 균형도
          </h4>
          <div className="space-y-2">
            {Object.entries(result.오행분석).map(([wuxing, value]) => (
              <div key={wuxing} className="flex items-center gap-3">
                <div className="w-8 text-sm text-slate-300 font-medium">{wuxing}</div>
                <div className="flex-1 relative">
                  <div className="h-6 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full transition-all duration-1000 ease-out"
                      style={{
                        width: `${Math.min(value * 10, 100)}%`,
                        background: `linear-gradient(90deg, ${WUXING_COLORS[wuxing as keyof typeof WUXING_COLORS].primary}, ${WUXING_COLORS[wuxing as keyof typeof WUXING_COLORS].secondary})`,
                        boxShadow: `0 0 10px ${WUXING_COLORS[wuxing as keyof typeof WUXING_COLORS].glow}`
                      }}
                    />
                  </div>
                  <div className="absolute right-2 top-0 h-6 flex items-center">
                    <span className="text-xs text-white font-medium">{value}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 십신 분석 링 */}
        <div className="mb-6">
          <h4 className="text-slate-200 font-medium mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4 text-blue-400" />
            십신 분포
          </h4>
          <div className="grid grid-cols-5 gap-2">
            {Object.entries(result.십신분석).map(([sipsin, value]) => (
              <div key={sipsin} className="text-center">
                <div
                  className="w-12 h-12 rounded-full mx-auto mb-2 flex items-center justify-center text-white font-bold text-sm relative"
                  style={{
                    backgroundColor: SIPSIN_COLORS[sipsin as keyof typeof SIPSIN_COLORS].color,
                    boxShadow: `0 0 15px ${SIPSIN_COLORS[sipsin as keyof typeof SIPSIN_COLORS].color}40`
                  }}
                >
                  {value}
                  <div className="absolute inset-0 rounded-full animate-pulse" style={{
                    backgroundColor: `${SIPSIN_COLORS[sipsin as keyof typeof SIPSIN_COLORS].color}20`
                  }}></div>
                </div>
                <div className="text-xs text-slate-400">{sipsin}</div>
                <div className="text-xs text-slate-500">{SIPSIN_COLORS[sipsin as keyof typeof SIPSIN_COLORS].label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* 격국 표시 */}
        <div className="text-center">
          <Badge variant="outline" className="text-lg px-4 py-2 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-purple-500/30 text-purple-200">
            격국: {result.격국}
          </Badge>
        </div>

        {/* 상호작용 가이드 */}
        <div className="mt-6 p-4 bg-slate-800/30 rounded-lg">
          <h4 className="text-slate-200 font-medium mb-2 text-sm">🎯 상호작용 가이드</h4>
          <div className="space-y-1 text-xs text-slate-400">
            <div>• 기둥을 클릭하면 상세 정보를 확인할 수 있습니다</div>
            <div>• 회전 버튼으로 원반을 돌려보세요</div>
            <div>• 중앙의 일주가 가장 중요한 본인의 기둥입니다</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}