'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Calculator, Sparkles, Zap, Brain } from 'lucide-react';
import { useSajuStore } from '@/stores/saju-store';
import { ParticleBackground, FloatingElement, WaveBackground } from '@/components/ui/interactive-elements';

export default function CalculatorPage() {
  const {
    currentInput,
    currentResult,
    isCalculating,
    selectedEngine,
    availableEngines,
    setCurrentInput,
    setSelectedEngine,
    setIsCalculating,
  } = useSajuStore();

  const [formData, setFormData] = useState({
    name: '',
    year: new Date().getFullYear() - 30,
    month: 1,
    day: 1,
    hour: 12,
    minute: 0,
    gender: 'male' as 'male' | 'female',
  });

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleCalculate = async () => {
    if (!formData.name) {
      alert('이름을 입력해주세요.');
      return;
    }

    setIsCalculating(true);
    
    const inputData = {
      name: formData.name,
      birth: {
        year: formData.year,
        month: formData.month,
        day: formData.day,
        hour: formData.hour,
        minute: formData.minute,
      },
      gender: formData.gender,
    };

    setCurrentInput(inputData);

    try {
      const response = await fetch('/api/saju/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputData)
      });

      if (response.ok) {
        const result = await response.json();
        // 결과 페이지로 이동
        const params = new URLSearchParams({
          name: formData.name,
          date: `${formData.year}-${formData.month}-${formData.day}`,
          time: `${formData.hour}:${formData.minute}`
        });
        window.location.href = `/result?${params.toString()}`;
      } else {
        // API 실패시에도 결과 페이지로 이동 (샘플 데이터 사용)
        const params = new URLSearchParams({
          name: formData.name,
          date: `${formData.year}-${formData.month}-${formData.day}`,
          time: `${formData.hour}:${formData.minute}`
        });
        window.location.href = `/result?${params.toString()}`;
      }
    } catch (error) {
      console.error('계산 오류:', error);
      // 오류 발생시에도 결과 페이지로 이동
      const params = new URLSearchParams({
        name: formData.name,
        date: `${formData.year}-${formData.month}-${formData.day}`,
        time: `${formData.hour}:${formData.minute}`
      });
      window.location.href = `/result?${params.toString()}`;
    } finally {
      setIsCalculating(false);
    }
  };

  const getEngineIcon = (engineName: string) => {
    switch (engineName) {
      case 'hybrid': return <Sparkles className="w-5 h-5" />;
      case 'kasi-precision': return <Zap className="w-5 h-5" />;
      case 'traditional': return <Brain className="w-5 h-5" />;
      default: return <Calculator className="w-5 h-5" />;
    }
  };

  const getEngineColor = (engineName: string) => {
    switch (engineName) {
      case 'hybrid': return 'from-purple-500 to-pink-500';
      case 'kasi-precision': return 'from-blue-500 to-cyan-500';
      case 'traditional': return 'from-green-500 to-emerald-500';
      default: return 'from-slate-500 to-slate-600';
    }
  };

  return (
    <div className="min-h-screen px-4 py-8 relative overflow-hidden">
      <ParticleBackground color="#8b5cf6" />
      <WaveBackground color="#3b82f6" opacity={0.03} />
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-slate-300 mb-4">
            <ArrowLeft className="w-4 h-4" />
            홈으로 돌아가기
          </Link>
          <h1 className="text-3xl sm:text-4xl font-bold gradient-text mb-4">
            사주 계산기
          </h1>
          <p className="text-lg text-slate-400">
            정확한 출생정보를 입력하시면 정밀한 사주 분석 결과를 제공해드립니다.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* 입력 폼 */}
          <Card className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border-slate-700/50">
            <CardHeader>
              <CardTitle className="text-slate-200 flex items-center gap-2">
                <Calculator className="w-5 h-5" />
                출생정보 입력
              </CardTitle>
              <CardDescription className="text-slate-400">
                정확한 정보를 입력할수록 더 정밀한 결과를 얻을 수 있습니다.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* 이름 */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  이름 *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="w-full px-4 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="이름을 입력하세요"
                />
              </div>

              {/* 성별 */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  성별
                </label>
                <div className="flex gap-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="gender"
                      value="male"
                      checked={formData.gender === 'male'}
                      onChange={(e) => handleInputChange('gender', e.target.value)}
                      className="text-purple-500 focus:ring-purple-500"
                    />
                    <span className="ml-2 text-slate-300">남성</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="gender"
                      value="female"
                      checked={formData.gender === 'female'}
                      onChange={(e) => handleInputChange('gender', e.target.value)}
                      className="text-purple-500 focus:ring-purple-500"
                    />
                    <span className="ml-2 text-slate-300">여성</span>
                  </label>
                </div>
              </div>

              {/* 출생년월일 */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  출생년월일 *
                </label>
                <div className="grid grid-cols-3 gap-3">
                  <select
                    value={formData.year}
                    onChange={(e) => handleInputChange('year', parseInt(e.target.value))}
                    className="px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500"
                  >
                    {Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i).map(year => (
                      <option key={year} value={year}>{year}년</option>
                    ))}
                  </select>
                  <select
                    value={formData.month}
                    onChange={(e) => handleInputChange('month', parseInt(e.target.value))}
                    className="px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500"
                  >
                    {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                      <option key={month} value={month}>{month}월</option>
                    ))}
                  </select>
                  <select
                    value={formData.day}
                    onChange={(e) => handleInputChange('day', parseInt(e.target.value))}
                    className="px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500"
                  >
                    {Array.from({ length: 31 }, (_, i) => i + 1).map(day => (
                      <option key={day} value={day}>{day}일</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* 출생시간 */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  출생시간
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <select
                    value={formData.hour}
                    onChange={(e) => handleInputChange('hour', parseInt(e.target.value))}
                    className="px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500"
                  >
                    {Array.from({ length: 24 }, (_, i) => i).map(hour => (
                      <option key={hour} value={hour}>{hour}시</option>
                    ))}
                  </select>
                  <select
                    value={formData.minute}
                    onChange={(e) => handleInputChange('minute', parseInt(e.target.value))}
                    className="px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500"
                  >
                    {Array.from({ length: 60 }, (_, i) => i).map(minute => (
                      <option key={minute} value={minute}>{minute}분</option>
                    ))}
                  </select>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  모르시는 경우 대략적인 시간을 입력하시면 됩니다.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* 엔진 선택 */}
          <div className="space-y-6">
            <Card className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border-slate-700/50">
              <CardHeader>
                <CardTitle className="text-slate-200">계산 엔진 선택</CardTitle>
                <CardDescription className="text-slate-400">
                  원하는 계산 방식을 선택하세요.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {availableEngines.map((engine) => (
                  <div
                    key={engine.name}
                    className={`p-4 rounded-lg border cursor-pointer transition-all ${
                      selectedEngine === engine.name
                        ? 'border-purple-500 bg-purple-500/10'
                        : 'border-slate-600 hover:border-slate-500'
                    }`}
                    onClick={() => setSelectedEngine(engine.name)}
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-2 bg-gradient-to-br ${getEngineColor(engine.name)} rounded-lg flex-shrink-0`}>
                        <div className="text-white">
                          {getEngineIcon(engine.name)}
                        </div>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-slate-200 font-medium mb-1">
                          {engine.description}
                        </h3>
                        <div className="flex items-center gap-4 text-sm text-slate-400 mb-2">
                          <span>정확도: {engine.accuracy}%</span>
                          <span>속도: {engine.speed === 'fast' ? '빠름' : engine.speed === 'normal' ? '보통' : '느림'}</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {engine.features.map((feature) => (
                            <span
                              key={feature}
                              className="px-2 py-1 bg-slate-700/50 rounded text-xs text-slate-300"
                            >
                              {feature}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* 계산 버튼 */}
            <Button
              onClick={handleCalculate}
              disabled={isCalculating || !formData.name}
              size="lg"
              variant="saju"
              className="w-full text-lg py-6 glow"
            >
              {isCalculating ? (
                <>
                  <div className="loading-dots mr-3">
                    <div></div>
                    <div></div>
                    <div></div>
                  </div>
                  계산 중...
                </>
              ) : (
                <>
                  <Calculator className="w-5 h-5 mr-2" />
                  사주 계산하기
                </>
              )}
            </Button>

            {isCalculating && (
              <Card className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border-slate-700/50">
                <CardContent className="pt-6">
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mx-auto mb-4 flex items-center justify-center pulse-slow">
                      <Sparkles className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-slate-200 font-medium mb-2">계산 진행 중</h3>
                    <p className="text-slate-400 text-sm">
                      {selectedEngine === 'hybrid' && 'AI와 전통 명리학을 융합하여 계산하고 있습니다...'}
                      {selectedEngine === 'kasi-precision' && 'KASI 천문학 데이터로 정밀 계산하고 있습니다...'}
                      {selectedEngine === 'traditional' && '전통 명리학 방식으로 계산하고 있습니다...'}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}