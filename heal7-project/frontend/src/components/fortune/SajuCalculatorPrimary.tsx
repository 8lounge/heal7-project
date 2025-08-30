import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { sampleSajuResults } from '../../data/sajuData';
import { SajuForm, SajuCalculatorProps, LoadingStep } from '../../types/sajuCalculatorTypes';

interface SajuCalculatorPrimaryProps extends SajuCalculatorProps {
  onDetailedAnalysis: (result: any) => void;
}

const SajuCalculatorPrimary: React.FC<SajuCalculatorPrimaryProps> = ({ 
  viewMode, 
  onDetailedAnalysis 
}) => {
  const [formData, setFormData] = useState<SajuForm>({
    year: '',
    month: '',
    day: '',
    hour: '',
    minute: '0',
    gender: 'M',
    location: '서울'
  });
  
  const [showResult, setShowResult] = useState(false);
  const [selectedResult, setSelectedResult] = useState<typeof sampleSajuResults[0] | null>(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingStep, setLoadingStep] = useState(0);
  const [apiError, setApiError] = useState<string | null>(null);

  const loadingSteps: LoadingStep[] = [
    { icon: '🔍', message: '생년월일 분석 시작', emoji: '✨' },
    { icon: '⚖️', message: '오행 균형 계산중', emoji: '💫' },
    { icon: '🎯', message: '현대적 직업 매칭중', emoji: '🚀' },
    { icon: '💕', message: '연애 스타일 분석중', emoji: '💖' },
    { icon: '🔮', message: 'AI 운명 분석 완료', emoji: '✅' }
  ];

  // 사주 계산 API 호출 (실패 시 샘플 데이터 사용)
  const { isLoading, refetch } = useQuery({
    queryKey: ['saju-calculation', formData],
    queryFn: async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        const apiEndpoint = '/api/saju/analyze';

        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
          signal: controller.signal
        });

        clearTimeout(timeoutId);
        
        if (response.ok) {
          return await response.json();
        }
        throw new Error(`API Error: ${response.status}`);
      } catch (error) {
        console.warn('API 호출 실패, 샘플 데이터 사용:', error);
        setApiError('서버 연결에 실패했습니다. 샘플 데이터로 결과를 보여드립니다.');
        return sampleSajuResults[Math.floor(Math.random() * sampleSajuResults.length)];
      }
    },
    enabled: false,
    retry: 1
  });

  // 로딩 진행률 관리
  useEffect(() => {
    if (isLoading) {
      const interval = setInterval(() => {
        setLoadingProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          
          const increment = Math.random() * 15 + 5;
          const newProgress = Math.min(prev + increment, 100);
          
          const newStep = Math.floor((newProgress / 100) * loadingSteps.length);
          setLoadingStep(Math.min(newStep, loadingSteps.length - 1));
          
          return newProgress;
        });
      }, 300);

      return () => clearInterval(interval);
    }
  }, [isLoading, loadingSteps.length]);

  const handleInputChange = (field: keyof SajuForm, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // 에러 상태 초기화
    setApiError(null);
    
    if (!formData.year || !formData.month || !formData.day) {
      alert('생년월일을 모두 입력해주세요.');
      return;
    }

    setLoadingProgress(0);
    setLoadingStep(0);
    setShowResult(false);
    setSelectedResult(null);

    const result = await refetch();
    if (result.data) {
      setSelectedResult(result.data);
      setShowResult(true);
    }
  };

  const cardClass = viewMode === 'cyber_fantasy' 
    ? 'bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-md border border-cyan-500/30' 
    : 'bg-white/10 backdrop-blur-md border border-white/20';

  const buttonClass = viewMode === 'cyber_fantasy'
    ? 'bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-bold py-3 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-lg'
    : 'bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-8 rounded-xl transition-all duration-300';

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* 헤더 */}
        <motion.div 
          className="text-center mb-12"
          initial={{ y: -30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-4xl font-bold text-white mb-4">
            {viewMode === 'cyber_fantasy' ? '🔮 3D 크리스탈 사주' : '📊 사주명리학'}
          </h1>
          <p className="text-gray-300">
            {viewMode === 'cyber_fantasy' 
              ? '3D 크리스탈로 펼쳐지는 신비로운 운명 분석'
              : '정확한 생년월일로 사주팔자를 분석합니다'
            }
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 입력 폼 */}
          <motion.div 
            className={`p-6 rounded-xl ${cardClass}`}
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <span className="mr-2">📝</span>
              생년월일 입력
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* 생년월일 */}
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">년</label>
                  <input
                    type="number"
                    placeholder="1990"
                    min="1900"
                    max="2030"
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                    value={formData.year}
                    onChange={(e) => handleInputChange('year', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">월</label>
                  <input
                    type="number"
                    placeholder="1"
                    min="1"
                    max="12"
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                    value={formData.month}
                    onChange={(e) => handleInputChange('month', e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">일</label>
                  <input
                    type="number"
                    placeholder="15"
                    min="1"
                    max="31"
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                    value={formData.day}
                    onChange={(e) => handleInputChange('day', e.target.value)}
                  />
                </div>
              </div>

              {/* 시간 */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">시</label>
                  <select
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                    value={formData.hour}
                    onChange={(e) => handleInputChange('hour', e.target.value)}
                  >
                    <option value="">모름</option>
                    {Array.from({ length: 24 }, (_, i) => (
                      <option key={i} value={i.toString()}>{i}시</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">분</label>
                  <select
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                    value={formData.minute}
                    onChange={(e) => handleInputChange('minute', e.target.value)}
                  >
                    <option value="0">0분</option>
                    <option value="15">15분</option>
                    <option value="30">30분</option>
                    <option value="45">45분</option>
                  </select>
                </div>
              </div>

              {/* 성별 및 지역 */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">성별</label>
                  <select
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                    value={formData.gender}
                    onChange={(e) => handleInputChange('gender', e.target.value as 'M' | 'F')}
                  >
                    <option value="M">남성</option>
                    <option value="F">여성</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">출생지</label>
                  <select
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                    value={formData.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                  >
                    <option value="서울">서울</option>
                    <option value="부산">부산</option>
                    <option value="대구">대구</option>
                    <option value="인천">인천</option>
                    <option value="대전">대전</option>
                    <option value="광주">광주</option>
                    <option value="기타">기타</option>
                  </select>
                </div>
              </div>

              {/* API 에러 알림 */}
              {apiError && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mb-4 p-3 bg-orange-500/20 border border-orange-500/30 rounded-lg"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-orange-400">⚠️</span>
                    <p className="text-orange-300 text-sm">{apiError}</p>
                  </div>
                </motion.div>
              )}

              <button
                type="submit"
                disabled={isLoading}
                className={`w-full ${buttonClass} ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {isLoading ? '분석 중...' : (viewMode === 'cyber_fantasy' ? '🔮 크리스탈 분석 시작' : '📊 사주 분석하기')}
              </button>
            </form>
          </motion.div>

          {/* 로딩 또는 결과 */}
          <div className={`p-6 rounded-xl ${cardClass}`}>
            <AnimatePresence mode="wait">
              {isLoading ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-center"
                >
                  <div className="mb-6">
                    <div className={`w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center text-3xl
                      ${viewMode === 'cyber_fantasy' ? 'bg-gradient-to-br from-cyan-500 to-purple-600' : 'bg-purple-600'}`}>
                      {loadingSteps[loadingStep]?.icon}
                    </div>
                    <p className="text-white font-medium">{loadingSteps[loadingStep]?.message}</p>
                    <p className="text-2xl mt-2">{loadingSteps[loadingStep]?.emoji}</p>
                  </div>

                  <div className="w-full bg-gray-700 rounded-full h-3 mb-4">
                    <motion.div
                      className={`h-3 rounded-full ${
                        viewMode === 'cyber_fantasy' 
                          ? 'bg-gradient-to-r from-cyan-500 to-purple-600' 
                          : 'bg-purple-600'
                      }`}
                      initial={{ width: 0 }}
                      animate={{ width: `${loadingProgress}%` }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>
                  <p className="text-gray-300 text-sm">{Math.round(loadingProgress)}% 완료</p>
                </motion.div>
              ) : showResult && selectedResult ? (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-4"
                >
                  <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                    <span className="mr-2">✨</span>
                    사주 분석 결과
                  </h3>

                  {/* 기본 정보 */}
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="font-semibold text-white mb-2">기본 정보</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="text-gray-300">출생일:</div>
                      <div className="text-white">{formData.year}-{formData.month.padStart(2, '0')}-{formData.day.padStart(2, '0')}</div>
                      <div className="text-gray-300">성별:</div>
                      <div className="text-white">{formData.gender === 'M' ? '남성' : '여성'}</div>
                      <div className="text-gray-300">출생지:</div>
                      <div className="text-white">{formData.location}</div>
                    </div>
                  </div>

                  {/* 간단한 성격 분석 */}
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="font-semibold text-white mb-2">성격 특성</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">
                      {(() => {
                        const personality = selectedResult?.personality as any;
                        if (typeof personality === 'string') {
                          return personality.slice(0, 150) + "...";
                        } else if (personality && typeof personality.description === 'string') {
                          return personality.description.slice(0, 150) + "...";
                        }
                        return "성격 특성 분석 중...";
                      })()}
                    </p>
                  </div>

                  {/* 상세 분석 버튼 */}
                  <button
                    onClick={() => onDetailedAnalysis(selectedResult)}
                    className={`w-full ${buttonClass} mt-4`}
                  >
                    🔍 상세 분석 보기
                  </button>
                </motion.div>
              ) : (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-16"
                >
                  <div className="text-6xl mb-4">
                    {viewMode === 'cyber_fantasy' ? '🔮' : '📊'}
                  </div>
                  <p className="text-gray-400">
                    생년월일을 입력하고 분석을 시작하세요
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SajuCalculatorPrimary;