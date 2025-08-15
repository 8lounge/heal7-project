'use client';

import { ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface WuXingData {
  목: number;
  화: number;
  토: number;
  금: number;
  수: number;
}

interface WuXingChartProps {
  data: WuXingData;
  type?: 'pie' | 'radar';
  showLabels?: boolean;
  className?: string;
}

const WUXING_COLORS = {
  목: '#22c55e', // green-500
  화: '#ef4444', // red-500
  토: '#eab308', // yellow-500
  금: '#64748b', // slate-500
  수: '#3b82f6', // blue-500
};

const WUXING_LABELS = {
  목: '木',
  화: '火', 
  토: '土',
  금: '金',
  수: '水',
};

const WUXING_NAMES = {
  목: '목(木)',
  화: '화(火)',
  토: '토(土)', 
  금: '금(金)',
  수: '수(水)',
};

export function WuXingChart({ data, type = 'radar', showLabels = true, className }: WuXingChartProps) {
  const chartData = Object.entries(data).map(([key, value]) => ({
    name: key,
    label: WUXING_LABELS[key as keyof WuXingData],
    fullName: WUXING_NAMES[key as keyof WuXingData],
    value,
    color: WUXING_COLORS[key as keyof WuXingData],
  }));

  const total = Object.values(data).reduce((sum, val) => sum + val, 0);
  const maxValue = Math.max(...Object.values(data));

  if (type === 'pie') {
    return (
      <Card className={className}>
        <CardHeader className="pb-4">
          <CardTitle className="text-slate-200 flex items-center gap-2">
            오행 분포 (원형)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          {showLabels && (
            <div className="mt-4 space-y-2">
              {chartData.map((entry) => (
                <div key={entry.name} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: entry.color }}
                    />
                    <span className="text-slate-300">{entry.fullName}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-slate-400">{entry.value}</span>
                    <span className="text-xs text-slate-500">
                      ({total > 0 ? Math.round((entry.value / total) * 100) : 0}%)
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    );
  }

  // Radar Chart (5각형)
  return (
    <Card className={className}>
      <CardHeader className="pb-4">
        <CardTitle className="text-slate-200 flex items-center gap-2">
          오행 균형 (오각형)
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <PolarGrid stroke="#374151" />
              <PolarAngleAxis 
                dataKey="label" 
                tick={{ fill: '#d1d5db', fontSize: 14, fontWeight: 600 }}
                className="hanja"
              />
              <PolarRadiusAxis
                angle={90}
                domain={[0, maxValue || 10]}
                tick={{ fill: '#9ca3af', fontSize: 12 }}
                tickCount={4}
              />
              <Radar
                name="오행"
                dataKey="value"
                stroke="#8b5cf6"
                fill="#8b5cf6"
                fillOpacity={0.2}
                strokeWidth={2}
                dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {showLabels && (
          <div className="mt-4">
            <div className="flex flex-wrap gap-2 justify-center">
              {chartData.map((entry) => {
                const isStrong = entry.value === maxValue && maxValue > 0;
                return (
                  <Badge 
                    key={entry.name}
                    variant={entry.name as any}
                    className={isStrong ? 'ring-2 ring-purple-500/50' : ''}
                  >
                    {entry.fullName}: {entry.value}
                    {isStrong && ' ★'}
                  </Badge>
                );
              })}
            </div>
            
            {maxValue > 0 && (
              <div className="mt-2 text-center text-xs text-slate-500">
                가장 강한 오행: {chartData.find(item => item.value === maxValue)?.fullName}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}