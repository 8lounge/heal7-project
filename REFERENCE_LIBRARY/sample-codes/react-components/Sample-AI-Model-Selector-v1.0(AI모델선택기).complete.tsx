/**
 * AI 모델 선택기 완전 구현 컴포넌트
 * 목적: 사용자가 문서 처리에 사용할 AI 모델을 선택할 수 있는 UI 제공
 * 사용법: <AIModelSelector onModelSelect={handleModelSelect} defaultModel="gemini" />
 */

import React, { useState, useEffect } from 'react';

// 타입 정의
export type AIModel = 'gemini' | 'gpt4' | 'claude' | 'perplexity' | 'clova';

export interface AIModelInfo {
  id: AIModel;
  name: string;
  provider: string;
  description: string;
  specialties: string[];
  color: string;
  lightColor: string;
  icon: string;
  pricing: 'free' | 'paid' | 'freemium';
  responseTime: string;
  accuracy: number; // 1-5 점수
}

export interface AIModelSelectorProps {
  onModelSelect: (model: AIModel) => void;
  defaultModel?: AIModel;
  className?: string;
  disabled?: boolean;
  showRecommendation?: boolean;
}

// AI 모델 정보 데이터
const AI_MODELS: Record<AIModel, AIModelInfo> = {
  gemini: {
    id: 'gemini',
    name: 'Google Gemini',
    provider: 'Google',
    description: '일반적인 문서 처리에 최적화된 모델입니다.',
    specialties: ['빠른 처리', '높은 정확도', '다국어 지원'],
    color: '#4285f4',
    lightColor: '#e8f0fe',
    icon: 'G',
    pricing: 'freemium',
    responseTime: '빠름',
    accuracy: 4
  },
  gpt4: {
    id: 'gpt4',
    name: 'OpenAI GPT-4',
    provider: 'OpenAI',
    description: '창의적 편집과 스타일 변경에 특화된 모델입니다.',
    specialties: ['창의적 편집', '복잡한 구조', '높은 품질'],
    color: '#10a37f',
    lightColor: '#e6f7f3',
    icon: 'AI',
    pricing: 'paid',
    responseTime: '보통',
    accuracy: 5
  },
  claude: {
    id: 'claude',
    name: 'Anthropic Claude',
    provider: 'Anthropic',
    description: '정확한 분석과 요약에 탁월한 성능을 보입니다.',
    specialties: ['정확한 분석', '긴 문서', '안전한 처리'],
    color: '#d97706',
    lightColor: '#fef3e2',
    icon: 'C',
    pricing: 'paid',
    responseTime: '보통',
    accuracy: 5
  },
  perplexity: {
    id: 'perplexity',
    name: 'Perplexity AI',
    provider: 'Perplexity',
    description: '실시간 정보 기반 문서 보강에 특화되어 있습니다.',
    specialties: ['실시간 정보', '팩트체크', '최신 데이터'],
    color: '#8b5cf6',
    lightColor: '#f3f0ff',
    icon: 'P',
    pricing: 'freemium',
    responseTime: '빠름',
    accuracy: 4
  },
  clova: {
    id: 'clova',
    name: '네이버 ClovaX',
    provider: 'Naver',
    description: '한국어 특화 처리와 문화적 맥락 이해에 특화되어 있습니다.',
    specialties: ['한국어 특화', '로컬 컨텍스트', '문화적 이해'],
    color: '#03c75a',
    lightColor: '#e6f9ee',
    icon: 'N',
    pricing: 'freemium',
    responseTime: '빠름',
    accuracy: 4
  }
};

// 추천 로직
const getRecommendedModel = (documentType?: string, userTier?: string): AIModel => {
  // 사용자 등급과 문서 타입에 따른 추천 로직
  if (userTier === 'free') {
    return 'gemini'; // 무료 사용자에게는 Gemini 추천
  }
  
  if (documentType === 'korean') {
    return 'clova'; // 한국어 문서는 ClovaX 추천
  }
  
  return 'gpt4'; // 기본적으로 GPT-4 추천
};

// 컴포넌트 스타일 (Tailwind CSS 클래스)
const styles = {
  container: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-1",
  modelCard: "relative cursor-pointer transition-all duration-200 ease-in-out",
  cardInner: "bg-white/10 border border-white/20 rounded-xl p-4 hover:bg-white/20 transition-all",
  cardSelected: "border-blue-400 bg-blue-500/20 ring-2 ring-blue-400/30",
  cardDisabled: "opacity-50 cursor-not-allowed",
  header: "flex items-center space-x-3 mb-3",
  icon: "w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-sm",
  modelInfo: "flex-1",
  modelName: "font-semibold text-white text-sm",
  modelProvider: "text-xs text-white/60",
  description: "text-sm text-white/70 mb-3 leading-relaxed",
  specialties: "flex flex-wrap gap-1 mb-3",
  specialty: "px-2 py-1 bg-white/10 rounded-full text-xs text-white/80",
  footer: "flex items-center justify-between",
  pricing: "text-xs text-white/60",
  accuracy: "flex items-center space-x-1",
  star: "w-3 h-3",
  recommendation: "absolute -top-2 -right-2 bg-yellow-500 text-white text-xs px-2 py-1 rounded-full font-medium shadow-lg",
  loadingShimmer: "animate-pulse bg-white/10 rounded"
};

export const AIModelSelector: React.FC<AIModelSelectorProps> = ({
  onModelSelect,
  defaultModel = 'gemini',
  className = '',
  disabled = false,
  showRecommendation = true
}) => {
  const [selectedModel, setSelectedModel] = useState<AIModel>(defaultModel);
  const [isLoading, setIsLoading] = useState(false);
  const [recommendedModel, setRecommendedModel] = useState<AIModel | null>(null);

  // 추천 모델 계산
  useEffect(() => {
    if (showRecommendation) {
      const recommended = getRecommendedModel();
      setRecommendedModel(recommended);
    }
  }, [showRecommendation]);

  // 모델 선택 핸들러
  const handleModelSelect = async (model: AIModel) => {
    if (disabled || isLoading) return;

    setIsLoading(true);
    
    try {
      // 실제 구현에서는 모델 가용성 체크 API 호출
      await new Promise(resolve => setTimeout(resolve, 300)); // 시뮬레이션
      
      setSelectedModel(model);
      onModelSelect(model);
    } catch (error) {
      console.error('모델 선택 오류:', error);
      // 에러 처리 (토스트 알림 등)
    } finally {
      setIsLoading(false);
    }
  };

  // 정확도 별표 렌더링
  const renderAccuracyStars = (accuracy: number) => {
    return (
      <div className={styles.accuracy}>
        {[1, 2, 3, 4, 5].map((star) => (
          <svg
            key={star}
            className={`${styles.star} ${star <= accuracy ? 'text-yellow-400' : 'text-gray-400'}`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        ))}
        <span className="text-xs text-white/60 ml-1">{accuracy}/5</span>
      </div>
    );
  };

  // 가격 표시 렌더링
  const renderPricing = (pricing: string) => {
    const pricingLabels = {
      free: '무료',
      paid: '유료',
      freemium: '부분 무료'
    };
    
    const pricingColors = {
      free: 'text-green-400',
      paid: 'text-orange-400',
      freemium: 'text-blue-400'
    };

    return (
      <span className={`${styles.pricing} ${pricingColors[pricing as keyof typeof pricingColors]}`}>
        {pricingLabels[pricing as keyof typeof pricingLabels]}
      </span>
    );
  };

  if (isLoading) {
    // 로딩 상태 스켈레톤 UI
    return (
      <div className={`${styles.container} ${className}`}>
        {Array.from({ length: 5 }).map((_, index) => (
          <div key={index} className={styles.modelCard}>
            <div className={styles.cardInner}>
              <div className={styles.header}>
                <div className={`${styles.loadingShimmer} w-10 h-10 rounded-lg`}></div>
                <div className="flex-1">
                  <div className={`${styles.loadingShimmer} h-4 w-24 mb-1`}></div>
                  <div className={`${styles.loadingShimmer} h-3 w-16`}></div>
                </div>
              </div>
              <div className={`${styles.loadingShimmer} h-12 w-full mb-3`}></div>
              <div className="flex space-x-1 mb-3">
                {Array.from({ length: 3 }).map((_, i) => (
                  <div key={i} className={`${styles.loadingShimmer} h-6 w-16 rounded-full`}></div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className={`${styles.container} ${className}`}>
      {Object.values(AI_MODELS).map((model) => {
        const isSelected = selectedModel === model.id;
        const isRecommended = recommendedModel === model.id;
        
        return (
          <div
            key={model.id}
            className={`
              ${styles.modelCard}
              ${disabled ? styles.cardDisabled : ''}
            `}
            onClick={() => handleModelSelect(model.id)}
          >
            {/* 추천 배지 */}
            {isRecommended && showRecommendation && (
              <div className={styles.recommendation}>
                추천
              </div>
            )}
            
            <div
              className={`
                ${styles.cardInner}
                ${isSelected ? styles.cardSelected : ''}
              `}
            >
              {/* 헤더: 아이콘 + 모델 정보 */}
              <div className={styles.header}>
                <div
                  className={styles.icon}
                  style={{ backgroundColor: model.color }}
                >
                  {model.icon}
                </div>
                <div className={styles.modelInfo}>
                  <div className={styles.modelName}>{model.name}</div>
                  <div className={styles.modelProvider}>{model.provider}</div>
                </div>
              </div>

              {/* 설명 */}
              <p className={styles.description}>
                {model.description}
              </p>

              {/* 특화 분야 태그 */}
              <div className={styles.specialties}>
                {model.specialties.map((specialty, index) => (
                  <span key={index} className={styles.specialty}>
                    {specialty}
                  </span>
                ))}
              </div>

              {/* 푸터: 가격 + 정확도 */}
              <div className={styles.footer}>
                {renderPricing(model.pricing)}
                {renderAccuracyStars(model.accuracy)}
              </div>

              {/* 선택 표시 */}
              {isSelected && (
                <div className="absolute top-2 right-2">
                  <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

// 사용법 예시 컴포넌트
export const AIModelSelectorExample: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState<AIModel>('gemini');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleModelSelect = (model: AIModel) => {
    setSelectedModel(model);
    console.log('선택된 모델:', model);
    
    // 실제 구현에서는 여기서 상태 관리 라이브러리나 컨텍스트 업데이트
  };

  const handleStartProcessing = async () => {
    setIsProcessing(true);
    
    // 실제 AI 처리 시뮬레이션
    try {
      console.log(`${selectedModel}으로 문서 처리 시작...`);
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('처리 완료!');
    } catch (error) {
      console.error('처리 오류:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">AI 모델 선택</h2>
        <p className="text-white/70">
          문서 처리에 사용할 AI 모델을 선택하세요. 각 모델은 고유한 특성과 장점을 가지고 있습니다.
        </p>
      </div>

      <AIModelSelector
        onModelSelect={handleModelSelect}
        defaultModel="gemini"
        disabled={isProcessing}
        showRecommendation={true}
        className="mb-8"
      />

      <div className="flex items-center justify-between bg-white/10 rounded-xl p-6">
        <div>
          <div className="text-white font-medium">
            선택된 모델: {AI_MODELS[selectedModel].name}
          </div>
          <div className="text-white/60 text-sm">
            {AI_MODELS[selectedModel].description}
          </div>
        </div>
        
        <button
          onClick={handleStartProcessing}
          disabled={isProcessing}
          className={`
            px-6 py-3 rounded-lg font-medium transition-all
            ${isProcessing 
              ? 'bg-gray-500 cursor-not-allowed' 
              : 'bg-blue-500 hover:bg-blue-600'
            }
            text-white
          `}
        >
          {isProcessing ? (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>처리 중...</span>
            </div>
          ) : (
            '문서 처리 시작'
          )}
        </button>
      </div>
    </div>
  );
};

// 타입 export
export type { AIModelInfo, AIModelSelectorProps };

// 상수 export
export { AI_MODELS };

export default AIModelSelector;