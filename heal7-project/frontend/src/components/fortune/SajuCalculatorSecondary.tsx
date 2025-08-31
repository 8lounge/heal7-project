import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Star, Briefcase, Heart, TrendingUp } from 'lucide-react';
import { SajuCalculatorProps, SajuTabType } from '../../types/sajuCalculatorTypes';

interface SajuCalculatorSecondaryProps extends SajuCalculatorProps {
  result: any;
  onBackToCalculator: () => void;
}

const SajuCalculatorSecondary: React.FC<SajuCalculatorSecondaryProps> = ({ 
  viewMode, 
  result, 
  onBackToCalculator 
}) => {
  const [activeTab, setActiveTab] = useState<SajuTabType>('personality');

  const cardClass = viewMode === 'cyber_fantasy' 
    ? 'bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-md border border-cyan-500/30' 
    : 'bg-white/10 backdrop-blur-md border border-white/20';

  const tabButtonClass = (isActive: boolean) => {
    const baseClass = 'px-4 py-2 rounded-lg font-medium transition-all duration-300 flex items-center gap-2';
    if (viewMode === 'cyber_fantasy') {
      return `${baseClass} ${isActive 
        ? 'bg-gradient-to-r from-cyan-500/30 to-purple-600/30 text-cyan-300 border border-cyan-500/50' 
        : 'text-gray-400 hover:text-cyan-300 hover:bg-cyan-500/10'
      }`;
    } else {
      return `${baseClass} ${isActive 
        ? 'bg-purple-600 text-white' 
        : 'text-gray-400 hover:text-white hover:bg-purple-600/30'
      }`;
    }
  };

  const tabs = [
    { id: 'personality' as SajuTabType, label: '성격', icon: Star },
    { id: 'career' as SajuTabType, label: '직업', icon: Briefcase },
    { id: 'love' as SajuTabType, label: '연애', icon: Heart },
    { id: 'fortune' as SajuTabType, label: '운세', icon: TrendingUp }
  ];

  const renderTabContent = () => {
    const rawContent = result[activeTab];
    
    // 객체인 경우 적절한 속성을 추출하여 텍스트로 변환
    const getContentText = (content: any) => {
      if (!content) return '분석 데이터가 없습니다.';
      if (typeof content === 'string') return content;
      if (typeof content === 'object') {
        // 객체인 경우 description 속성을 사용하거나 JSON으로 변환
        return content.description || content.text || JSON.stringify(content, null, 2);
      }
      return String(content);
    };
    
    const content = getContentText(rawContent);
    
    switch (activeTab) {
      case 'personality':
        return (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <Star className="w-6 h-6" />
              성격 분석
            </h3>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed">{content}</p>
            </div>
            
            {/* 객체 데이터가 있을 경우 추가 정보 표시 */}
            {rawContent && typeof rawContent === 'object' && (
              <>
                {rawContent.type && (
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="text-lg font-semibold text-white mb-2">✨ {rawContent.type}</h4>
                    <p className="text-gray-300">{rawContent.description}</p>
                  </div>
                )}
                
                {rawContent.keywords && rawContent.keywords.length > 0 && (
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="text-lg font-semibold text-white mb-3">🏷️ 성격 키워드</h4>
                    <div className="flex flex-wrap gap-2">
                      {rawContent.keywords.map((keyword: string, index: number) => (
                        <span 
                          key={index}
                          className="px-3 py-1 bg-purple-600/30 text-purple-300 rounded-full text-sm"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {rawContent.mbtiLikely && rawContent.mbtiLikely.length > 0 && (
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="text-lg font-semibold text-white mb-3">🎯 MBTI 가능성</h4>
                    <div className="flex flex-wrap gap-2">
                      {rawContent.mbtiLikely.map((mbti: string, index: number) => (
                        <span 
                          key={index}
                          className="px-3 py-1 bg-yellow-600/30 text-yellow-300 rounded-full text-sm font-medium"
                        >
                          {mbti}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {rawContent.strengthsModern && rawContent.strengthsModern.length > 0 && (
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="text-lg font-semibold text-white mb-3">💪 현대적 강점</h4>
                    <ul className="text-gray-300 space-y-1">
                      {rawContent.strengthsModern.map((strength: string, index: number) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2 text-green-400">•</span>
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {rawContent.improvementAreas && rawContent.improvementAreas.length > 0 && (
                  <div className="bg-black/20 p-4 rounded-lg">
                    <h4 className="text-lg font-semibold text-white mb-3">🎯 개선 영역</h4>
                    <ul className="text-gray-300 space-y-1">
                      {rawContent.improvementAreas.map((area: string, index: number) => (
                        <li key={index} className="flex items-start">
                          <span className="mr-2 text-orange-400">•</span>
                          {area}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}
            
            {/* 성격 특성 차트 */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {['외향성', '개방성', '성실성', '친화성'].map((trait) => (
                <div key={trait} className="bg-black/20 p-3 rounded-lg text-center">
                  <div className="text-sm text-gray-400 mb-1">{trait}</div>
                  <div className="text-lg font-bold text-white">
                    {Math.floor(Math.random() * 40) + 60}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'career':
        return (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <Briefcase className="w-6 h-6" />
              직업 운세
            </h3>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed">{content}</p>
            </div>
            
            {/* 추천 직업군 */}
            <div className="bg-black/20 p-4 rounded-lg">
              <h4 className="text-lg font-semibold text-white mb-3">추천 직업군</h4>
              <div className="flex flex-wrap gap-2">
                {['창작직', '기술직', '교육직', '서비스직'].map((job) => (
                  <span 
                    key={job}
                    className="px-3 py-1 bg-purple-600/30 text-purple-300 rounded-full text-sm"
                  >
                    {job}
                  </span>
                ))}
              </div>
            </div>
          </div>
        );

      case 'love':
        return (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <Heart className="w-6 h-6" />
              연애 운세
            </h3>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed">{content}</p>
            </div>
            
            {/* 연애 스타일 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-black/20 p-4 rounded-lg">
                <h4 className="font-semibold text-white mb-2">연애 스타일</h4>
                <ul className="text-gray-300 text-sm space-y-1">
                  <li>• 감정 표현이 풍부함</li>
                  <li>• 안정적인 관계 선호</li>
                  <li>• 상대방에 대한 배려심 많음</li>
                </ul>
              </div>
              <div className="bg-black/20 p-4 rounded-lg">
                <h4 className="font-semibold text-white mb-2">이상형 특징</h4>
                <ul className="text-gray-300 text-sm space-y-1">
                  <li>• 유머감각이 있는 사람</li>
                  <li>• 진실된 마음을 가진 사람</li>
                  <li>• 공통 관심사가 많은 사람</li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'fortune':
        return (
          <div className="space-y-6">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-6 h-6" />
              종합 운세
            </h3>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed">{content}</p>
            </div>
            
            {/* 월별 운세 */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Array.from({ length: 12 }, (_, i) => (
                <div key={i + 1} className="bg-black/20 p-3 rounded-lg text-center">
                  <div className="text-sm text-gray-400 mb-1">{i + 1}월</div>
                  <div className="text-lg">
                    {['🌟', '⭐', '✨', '💫'][Math.floor(Math.random() * 4)]}
                  </div>
                </div>
              ))}
            </div>
            
            {/* 주요 운세 포인트 */}
            <div className="bg-yellow-900/20 border border-yellow-500/30 p-4 rounded-lg">
              <h4 className="text-yellow-300 font-semibold mb-2">💡 이번 달 주요 포인트</h4>
              <ul className="text-yellow-200 text-sm space-y-1">
                <li>• 새로운 기회가 찾아올 수 있는 시기</li>
                <li>• 인간관계에서 좋은 변화 예상</li>
                <li>• 건강 관리에 특별히 신경 쓸 것</li>
              </ul>
            </div>
          </div>
        );

      default:
        return <div className="text-gray-400">선택된 탭의 내용이 없습니다.</div>;
    }
  };

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* 헤더 */}
        <motion.div 
          className="flex items-center justify-between mb-8"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
        >
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToCalculator}
              className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              계산기로 돌아가기
            </button>
            <div>
              <h1 className="text-3xl font-bold text-white">
                {viewMode === 'cyber_fantasy' ? '🔮 크리스탈 상세 분석' : '📊 상세 사주 해석'}
              </h1>
              <p className="text-gray-400">전문적인 사주 분석 결과</p>
            </div>
          </div>
        </motion.div>

        {/* 탭 네비게이션 */}
        <motion.div 
          className="flex flex-wrap gap-2 mb-8 p-2 bg-black/20 rounded-xl"
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          {tabs.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={tabButtonClass(activeTab === id)}
            >
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </motion.div>

        {/* 탭 컨텐츠 */}
        <motion.div 
          className={`p-8 rounded-xl ${cardClass}`}
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {renderTabContent()}
        </motion.div>

        {/* 하단 정보 */}
        <motion.div 
          className="mt-8 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="bg-black/20 p-4 rounded-lg inline-block">
            <p className="text-gray-400 text-sm">
              ✨ 이 분석은 전통 사주명리학과 현대 AI 기술을 결합한 결과입니다
            </p>
            <p className="text-gray-500 text-xs mt-2">
              참고용으로만 활용하시고, 중요한 결정은 전문가와 상담하세요
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SajuCalculatorSecondary;