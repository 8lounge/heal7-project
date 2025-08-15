'use client';

import { ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface SipsinData {
  비겁: number;
  식상: number;
  재성: number;
  관살: number;
  인성: number;
}

interface SipsinWheelProps {
  data: SipsinData;
  showLabels?: boolean;
  className?: string;
}

const SIPSIN_COLORS = {
  비겁: '#8b5cf6', // violet-500
  식상: '#06b6d4', // cyan-500
  재성: '#10b981', // emerald-500
  관살: '#f59e0b', // amber-500
  인성: '#ec4899', // pink-500
};

const SIPSIN_LABELS = {
  비겁: '比劫',
  식상: '食傷',
  재성: '財星',
  관살: '官殺',
  인성: '印星',
};

const SIPSIN_DESCRIPTIONS = {
  비겁: '자아, 경쟁, 형제',
  식상: '표현, 재능, 자식',
  재성: '재물, 배우자, 욕망',
  관살: '권위, 명예, 책임',
  인성: '학습, 모성, 지혜',
};

export function SipsinWheel({ data, showLabels = true, className }: SipsinWheelProps) {
  const chartData = Object.entries(data).map(([key, value]) => ({
    name: key,
    label: SIPSIN_LABELS[key as keyof SipsinData],
    description: SIPSIN_DESCRIPTIONS[key as keyof SipsinData],
    value,
    color: SIPSIN_COLORS[key as keyof SipsinData],
  }));

  const total = Object.values(data).reduce((sum, val) => sum + val, 0);
  const maxValue = Math.max(...Object.values(data));
  const dominantSipsin = chartData.find(item => item.value === maxValue);

  // 커스텀 라벨 렌더링 함수
  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, label }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.7;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    if (percent < 0.05) return null; // 5% 미만은 라벨 숨김

    return (
      <text 
        x={x} 
        y={y} 
        fill="#f1f5f9"
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize="12"
        fontWeight="600"
        className="hanja"
      >
        {label}
      </text>
    );
  };

  return (
    <Card className={className}>
      <CardHeader className="pb-4">
        <CardTitle className="text-slate-200 flex items-center gap-2">
          십신 분포 (원형)
        </CardTitle>
        {dominantSipsin && maxValue > 0 && (
          <div className="text-sm text-slate-400">
            주요 십신: <span className="text-slate-200">{dominantSipsin.label}</span>
            <span className="text-xs ml-2">({dominantSipsin.description})</span>
          </div>
        )}
      </CardHeader>
      <CardContent>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderCustomLabel}
                outerRadius={100}
                innerRadius={30}
                paddingAngle={1}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.color}
                    stroke={entry.value === maxValue ? '#f8fafc' : 'transparent'}
                    strokeWidth={entry.value === maxValue ? 2 : 0}
                  />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>

        {showLabels && (
          <div className="mt-4 space-y-3">
            {/* 십신별 상세 정보 */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {chartData.map((entry) => {
                const percentage = total > 0 ? Math.round((entry.value / total) * 100) : 0;
                const isStrong = entry.value === maxValue && maxValue > 0;
                
                return (
                  <div 
                    key={entry.name}
                    className={`p-3 rounded-lg border transition-all ${
                      isStrong 
                        ? 'border-purple-500/50 bg-purple-500/5' 
                        : 'border-slate-700/50 bg-slate-800/30'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: entry.color }}
                        />
                        <span className="text-slate-200 font-medium hanja">
                          {entry.label}
                        </span>
                        {isStrong && <span className="text-xs text-purple-400">★ 주요</span>}
                      </div>
                      <div className="text-right">
                        <div className="text-slate-300 font-medium">{entry.value}</div>
                        <div className="text-xs text-slate-500">{percentage}%</div>
                      </div>
                    </div>
                    <div className="text-xs text-slate-400">
                      {entry.description}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* 십신 요약 */}
            <div className="flex flex-wrap gap-1 justify-center pt-2 border-t border-slate-700/50">
              {chartData
                .filter(entry => entry.value > 0)
                .sort((a, b) => b.value - a.value)
                .map((entry) => (
                  <Badge 
                    key={entry.name}
                    variant={entry.name as any}
                    className={entry.value === maxValue ? 'ring-1 ring-purple-500/50' : ''}
                  >
                    {entry.label} {entry.value}
                  </Badge>
                ))}
            </div>

            {maxValue === 0 && (
              <div className="text-center text-slate-500 py-4">
                십신 데이터가 없습니다
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}