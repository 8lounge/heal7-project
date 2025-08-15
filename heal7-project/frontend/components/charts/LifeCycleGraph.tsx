'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, Area, AreaChart } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface DaeunData {
  시작년도: number;
  종료년도: number;
  천간: string;
  지지: string;
}

interface LifeCycleGraphProps {
  daeun: DaeunData[];
  currentAge?: number;
  className?: string;
  type?: 'line' | 'area';
}

// 대운의 길흉을 임의로 계산하는 함수 (실제로는 복잡한 명리학 계산 필요)
function calculateFortuneScore(cheongan: string, jiji: string, age: number): number {
  // 간단한 점수 계산 로직 (실제 구현 시 명리학 로직 적용)
  const cheongangScore = cheongan.charCodeAt(0) % 10;
  const jijiScore = jiji.charCodeAt(0) % 10;
  const ageBonus = Math.sin((age - 20) * Math.PI / 60) * 3; // 나이에 따른 변화
  
  return Math.max(0, Math.min(10, cheongangScore + jijiScore + ageBonus));
}

function getFortuneColor(score: number): string {
  if (score >= 8) return '#22c55e'; // 매우 좋음 - 초록
  if (score >= 6) return '#3b82f6'; // 좋음 - 파랑  
  if (score >= 4) return '#eab308'; // 보통 - 노랑
  if (score >= 2) return '#f59e0b'; // 나쁨 - 주황
  return '#ef4444'; // 매우 나쁨 - 빨강
}

function getFortuneLabel(score: number): string {
  if (score >= 8) return '대길';
  if (score >= 6) return '길';
  if (score >= 4) return '평';
  if (score >= 2) return '흉';
  return '대흉';
}

export function LifeCycleGraph({ daeun, currentAge, className, type = 'area' }: LifeCycleGraphProps) {
  // 차트 데이터 생성
  const chartData = daeun.map((period) => {
    const midAge = (period.시작년도 + period.종료년도) / 2;
    const fortuneScore = calculateFortuneScore(period.천간, period.지지, midAge);
    
    return {
      age: Math.round(midAge),
      startAge: period.시작년도,
      endAge: period.종료년도,
      fortune: fortuneScore,
      cheongan: period.천간,
      jiji: period.지지,
      period: `${period.천간}${period.지지}`,
      fortuneLabel: getFortuneLabel(fortuneScore),
      color: getFortuneColor(fortuneScore),
    };
  });

  // 커스텀 툴팁
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-800 border border-slate-600 rounded-lg p-3 shadow-lg">
          <p className="text-slate-200 font-medium">
            {data.startAge}세 ~ {data.endAge}세
          </p>
          <p className="text-slate-300 hanja text-lg">
            {data.period} 大運
          </p>
          <div className="flex items-center gap-2 mt-2">
            <Badge 
              style={{ backgroundColor: data.color }}
              className="text-white"
            >
              {data.fortuneLabel}
            </Badge>
            <span className="text-xs text-slate-400">
              운세: {data.fortune.toFixed(1)}/10
            </span>
          </div>
        </div>
      );
    }
    return null;
  };

  // 현재 대운 찾기
  const currentDaeun = currentAge ? 
    daeun.find(period => currentAge >= period.시작년도 && currentAge <= period.종료년도) :
    null;

  if (type === 'area') {
    return (
      <Card className={className}>
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200 flex items-center gap-2">
            대운 흐름 (생애주기)
          </CardTitle>
          {currentAge && currentDaeun && (
            <div className="text-sm text-slate-400">
              현재 {currentAge}세: <span className="text-slate-200 hanja">
                {currentDaeun.천간}{currentDaeun.지지} 大運
              </span>
              <span className="ml-2 text-xs">
                ({currentDaeun.시작년도}~{currentDaeun.종료년도}세)
              </span>
            </div>
          )}
        </CardHeader>
        <CardContent>
          <div className="h-64 w-full mb-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="age"
                  stroke="#9ca3af"
                  fontSize={12}
                  tickFormatter={(value) => `${value}세`}
                />
                <YAxis 
                  stroke="#9ca3af"
                  fontSize={12}
                  domain={[0, 10]}
                  tickFormatter={(value) => value.toFixed(0)}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="fortune"
                  stroke="#8b5cf6"
                  fill="url(#fortuneGradient)"
                  strokeWidth={2}
                />
                <defs>
                  <linearGradient id="fortuneGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* 대운별 상세 정보 */}
          <div className="space-y-2">
            <h4 className="text-slate-300 font-medium text-sm mb-3">대운별 상세</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {chartData.map((data, index) => {
                const isCurrent = currentAge && 
                  currentAge >= data.startAge && 
                  currentAge <= data.endAge;

                return (
                  <div 
                    key={index}
                    className={`p-2 rounded border transition-all ${
                      isCurrent 
                        ? 'border-purple-500/50 bg-purple-500/10' 
                        : 'border-slate-700/50 bg-slate-800/30'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-slate-300 hanja font-medium">
                        {data.period}
                      </span>
                      {isCurrent && (
                        <span className="text-xs text-purple-400">현재</span>
                      )}
                    </div>
                    <div className="text-xs text-slate-400 mb-2">
                      {data.startAge}세 ~ {data.endAge}세
                    </div>
                    <Badge 
                      style={{ backgroundColor: data.color }}
                      className="text-white text-xs"
                    >
                      {data.fortuneLabel} ({data.fortune.toFixed(1)})
                    </Badge>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 범례 */}
          <div className="mt-4 p-3 bg-slate-800/30 rounded-lg">
            <h4 className="text-slate-300 font-medium text-sm mb-2">운세 범례</h4>
            <div className="flex flex-wrap gap-2 text-xs">
              <Badge style={{ backgroundColor: '#22c55e' }} className="text-white">대길 (8-10)</Badge>
              <Badge style={{ backgroundColor: '#3b82f6' }} className="text-white">길 (6-8)</Badge>
              <Badge style={{ backgroundColor: '#eab308' }} className="text-white">평 (4-6)</Badge>
              <Badge style={{ backgroundColor: '#f59e0b' }} className="text-white">흉 (2-4)</Badge>
              <Badge style={{ backgroundColor: '#ef4444' }} className="text-white">대흉 (0-2)</Badge>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              * 운세 점수는 대운의 천간, 지지와 나이를 고려한 예측값입니다
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Line Chart
  return (
    <Card className={className}>
      <CardHeader className="pb-4">
        <CardTitle className="text-slate-200">대운 타임라인</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="age"
                stroke="#9ca3af"
                fontSize={12}
                tickFormatter={(value) => `${value}세`}
              />
              <YAxis 
                stroke="#9ca3af"
                fontSize={12}
                domain={[0, 10]}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="fortune"
                stroke="#8b5cf6"
                strokeWidth={3}
                dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#8b5cf6', strokeWidth: 2, fill: '#fff' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}