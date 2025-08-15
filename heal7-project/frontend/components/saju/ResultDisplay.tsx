'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { SajuResult } from '@/types/saju';
import { WuXingChart } from '@/components/charts/WuXingChart';
import { SipsinWheel } from '@/components/charts/SipsinWheel';
import { SajuBoard } from '@/components/charts/SajuBoard';
import { LifeCycleGraph } from '@/components/charts/LifeCycleGraph';
import { Eye, EyeOff, Download, Share2, Clock, Zap } from 'lucide-react';

interface ResultDisplayProps {
  result: SajuResult;
  className?: string;
}

export function ResultDisplay({ result, className }: ResultDisplayProps) {
  const [showDetailedAnalysis, setShowDetailedAnalysis] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'charts' | 'interpretation'>('overview');

  const tabs = [
    { id: 'overview', label: '개요', icon: Eye },
    { id: 'charts', label: '차트', icon: Zap },  
    { id: 'interpretation', label: '해석', icon: Clock },
  ];

  return (
    <div className={className}>
      {/* 헤더 */}
      <Card className="mb-6">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-slate-200 flex items-center gap-2">
                사주 계산 결과
              </CardTitle>
              <div className="flex items-center gap-4 mt-2 text-sm text-slate-400">
                <span>엔진: {result.계산정보.엔진}</span>
                <span>계산시간: {result.계산정보.계산시간}</span>
                <span>정확도: {result.계산정보.정확도}%</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setShowDetailedAnalysis(!showDetailedAnalysis)}
              >
                {showDetailedAnalysis ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                {showDetailedAnalysis ? '간단히' : '상세히'}
              </Button>
              <Button variant="outline" size="sm">
                <Share2 className="w-4 h-4 mr-2" />
                공유
              </Button>
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                저장
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* 탭 네비게이션 */}
      <div className="flex space-x-1 mb-6 bg-slate-800/50 p-1 rounded-lg">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-purple-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-300 hover:bg-slate-700/50'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* 탭 내용 */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* 사주팔자 */}
          <SajuBoard pillars={result.사주} />

          {/* 기본 정보 */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* 격국 */}
            <Card>
              <CardHeader className="pb-4">
                <CardTitle className="text-slate-200">격국 (格局)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-200 mb-2 hanja">
                    {result.격국}
                  </div>
                  <Badge variant="default" className="text-lg px-4 py-2">
                    {result.격국} 격
                  </Badge>
                </div>
                {showDetailedAnalysis && (
                  <div className="mt-4 p-3 bg-slate-800/30 rounded-lg">
                    <p className="text-sm text-slate-400">
                      격국은 사주의 기본 구조를 나타내며, 개인의 성향과 인생의 방향을 결정하는 중요한 요소입니다.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* 간단한 오행/십신 요약 */}
            <Card>
              <CardHeader className="pb-4">
                <CardTitle className="text-slate-200">오행/십신 요약</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* 오행 */}
                <div>
                  <h4 className="text-slate-300 font-medium mb-2 text-sm">오행 분포</h4>
                  <div className="flex flex-wrap gap-1">
                    {Object.entries(result.오행분석).map(([key, value]) => (
                      <Badge key={key} variant={key as any}>
                        {key}: {value}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* 십신 */}
                <div>
                  <h4 className="text-slate-300 font-medium mb-2 text-sm">십신 분포</h4>
                  <div className="flex flex-wrap gap-1">
                    {Object.entries(result.십신분석).map(([key, value]) => (
                      <Badge key={key} variant={key as any}>
                        {key}: {value}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* 기본 해석 */}
          {showDetailedAnalysis && (
            <Card>
              <CardHeader>
                <CardTitle className="text-slate-200">기본 해석</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-6">
                  {Object.entries(result.해석).map(([category, interpretation]) => (
                    <div key={category} className="space-y-2">
                      <h4 className="text-slate-300 font-medium">
                        {category === '성격' && '성격'}
                        {category === '재물' && '재물운'}
                        {category === '건강' && '건강'}
                        {category === '관계' && '인간관계'}
                      </h4>
                      <p className="text-sm text-slate-400 leading-relaxed">
                        {interpretation}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {activeTab === 'charts' && (
        <div className="space-y-6">
          {/* 차트 그리드 */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* 오행 차트 */}
            <WuXingChart 
              data={result.오행분석}
              type="radar"
            />

            {/* 십신 휠 */}
            <SipsinWheel 
              data={result.십신분석}
            />
          </div>

          {/* 대운 그래프 */}
          {result.대운 && result.대운.length > 0 && (
            <LifeCycleGraph 
              daeun={result.대운}
              currentAge={30} // TODO: 실제 나이 계산
            />
          )}

          {/* 오행 원형 차트 (추가 옵션) */}
          {showDetailedAnalysis && (
            <WuXingChart 
              data={result.오행분석}
              type="pie"
            />
          )}
        </div>
      )}

      {activeTab === 'interpretation' && (
        <div className="space-y-6">
          {/* 상세 해석 */}
          <div className="grid gap-6">
            {Object.entries(result.해석).map(([category, interpretation]) => (
              <Card key={category}>
                <CardHeader>
                  <CardTitle className="text-slate-200">
                    {category === '성격' && '🧠 성격 분석'}
                    {category === '재물' && '💰 재물운'}
                    {category === '건강' && '💊 건강'}
                    {category === '관계' && '👥 인간관계'}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-slate-300 leading-relaxed">
                    {interpretation}
                  </p>
                  {showDetailedAnalysis && (
                    <div className="mt-4 p-3 bg-slate-800/30 rounded-lg">
                      <p className="text-sm text-slate-400">
                        이 분석은 {result.계산정보.엔진} 엔진을 통해 생성되었으며, 
                        정확도는 {result.계산정보.정확도}%입니다.
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>

          {/* 대운 상세 */}
          {result.대운 && result.대운.length > 0 && showDetailedAnalysis && (
            <Card>
              <CardHeader>
                <CardTitle className="text-slate-200">🔮 대운 분석</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {result.대운.slice(0, 3).map((daeun, index) => (
                    <div key={index} className="p-4 bg-slate-800/30 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-200 font-medium hanja">
                          {daeun.천간}{daeun.지지} 大運
                        </span>
                        <span className="text-slate-400 text-sm">
                          {daeun.시작년도}세 ~ {daeun.종료년도}세
                        </span>
                      </div>
                      <p className="text-sm text-slate-400">
                        이 시기에는 {daeun.천간}{daeun.지지}의 기운이 강하게 작용하여...
                        (실제 해석은 복잡한 명리학 분석이 필요합니다)
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}