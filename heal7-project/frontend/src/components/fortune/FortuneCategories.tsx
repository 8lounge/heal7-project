import React, { useState } from 'react';
import { 
  Heart, 
  Brain, 
  TrendingUp,
  Sparkles
} from 'lucide-react';

interface FortuneCategory {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  features: string[];
  isPremium?: boolean;
}

interface FortuneService {
  id: string;
  name: string;
  description: string;
  price?: string;
  isPremium?: boolean;
}

interface FortuneCategoriesProps {
  viewMode: 'basic' | 'cyber_fantasy';
  onCategorySelect: (category: string) => void;
}

export const FortuneCategories: React.FC<FortuneCategoriesProps> = ({ viewMode: _viewMode, onCategorySelect }) => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const handleServiceClick = (serviceId: string) => {
    // 서비스 ID를 라우트 이름으로 매핑
    const routeMap: { [key: string]: string } = {
      'personality': 'personality',
      'mbti': 'personality', 
      'zodiac': 'zodiac',
      'love': 'love',
      'partner': 'compatibility',
      'marriage': 'love', // 결혼운도 연애운 페이지로
      'family': 'compatibility',
      'workplace': 'compatibility',
    };
    
    const route = routeMap[serviceId] || serviceId;
    onCategorySelect(route);
  };

  const categories: FortuneCategory[] = [
    {
      id: 'self-analysis',
      title: '나의 기본 성향 분석',
      description: '자신을 깊이 있게 이해하는 첫 번째 단계',
      icon: <Brain className="w-6 h-6" />,
      color: 'from-blue-500 to-purple-600',
      features: ['십이지신 분석', 'MBTI 통합 프로파일', '사상체질 진단']
    },
    {
      id: 'life-fortune',
      title: '인생과 운의 흐름 예측',
      description: '시간의 흐름에 따른 나의 운세 변화',
      icon: <TrendingUp className="w-6 h-6" />,
      color: 'from-green-500 to-blue-600',
      features: ['프리미엄 만세력', '오늘의 운세', '바이오리듬'],
      isPremium: true
    },
    {
      id: 'relationships',
      title: '관계 심층 분석 (궁합)',
      description: '모든 인간관계의 비밀을 풀어드립니다',
      icon: <Heart className="w-6 h-6" />,
      color: 'from-pink-500 to-red-600',
      features: ['연애&결혼운', '가족궁합', '동료궁합'],
      isPremium: true
    }
  ];

  const services: Record<string, FortuneService[]> = {
    'self-analysis': [
      {
        id: 'zodiac',
        name: '🐉 십이지신 분석',
        description: '나의 띠를 통해 알아보는 기본 성향과 숨겨진 잠재력'
      },
      {
        id: 'personality',
        name: '🧠 통합 성격 프로파일',
        description: 'MBTI + 사주 오행을 결합한 입체적 성격 분석'
      },
      {
        id: 'constitution',
        name: '🌿 사상체질 건강 진단',
        description: '나에게 맞는 음식, 운동, 생활습관 가이드'
      }
    ],
    'life-fortune': [
      {
        id: 'manseoryeok',
        name: '📊 프리미엄 만세력',
        description: '평생 운세 흐름을 한눈에 보는 인생 내비게이션',
        price: '₩5,000',
        isPremium: true
      },
      {
        id: 'daily',
        name: '📅 오늘의 운세 & 바이오리듬',
        description: '매일 업데이트되는 개인 맞춤형 운세 브리핑'
      },
      {
        id: 'wealth',
        name: '💰 심층 재물운 분석',
        description: '평생의 재물 흐름과 투자 방향성',
        price: '₩10,000',
        isPremium: true
      },
      {
        id: 'career',
        name: '🚀 직업/창업운 분석',
        description: '나에게 맞는 직업과 성공 시기 분석',
        price: '₩8,000',
        isPremium: true
      }
    ],
    'relationships': [
      {
        id: 'love',
        name: '💕 연애운 분석',
        description: '올해 연애 기운과 이상형, 만날 시기 예측'
      },
      {
        id: 'marriage',
        name: '💒 결혼운 분석',
        description: '최적 결혼 시기와 배우자상, 행복한 결혼 가이드'
      },
      {
        id: 'partner',
        name: '👫 파트너 심층 궁합',
        description: '두 사람의 상성과 갈등 해결 방안 제시',
        price: '₩15,000',
        isPremium: true
      },
      {
        id: 'family',
        name: '👨‍👩‍👧‍👦 가족 종합 궁합',
        description: '시부모, 가족 구성원과의 관계 개선 솔루션',
        price: '₩12,000',
        isPremium: true
      },
      {
        id: 'workplace',
        name: '🏢 직장 동료 궁합',
        description: '상사, 동료와의 협업 방법과 갈등 관리'
      }
    ]
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        
        {/* 헤더 섹션 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            🔮 HEAL7 운세 서비스
          </h1>
          <p className="text-xl text-white/90 mb-2">
            전통 명리학과 현대 기술의 만남
          </p>
          <p className="text-white/80">
            정확한 사주 분석 • 맞춤형 운세 • 실시간 상담
          </p>
        </div>

        {/* 카테고리 그리드 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {categories.map((category) => (
            <div 
              key={category.id}
              className={`relative overflow-hidden cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-xl rounded-xl backdrop-blur-md border border-white/20 ${
                selectedCategory === category.id 
                  ? 'bg-white/20 ring-2 ring-purple-400 shadow-lg' 
                  : 'bg-white/10 hover:bg-white/20'
              }`}
              onClick={() => setSelectedCategory(selectedCategory === category.id ? null : category.id)}
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${category.color} opacity-20`} />
              
              <div className="relative p-6">
                <div className="flex items-center gap-3 mb-3">
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${category.color} text-white shadow-lg`}>
                    {category.icon}
                  </div>
                  {category.isPremium && (
                    <div className="px-2 py-1 bg-amber-500/20 border border-amber-400/50 rounded-full">
                      <span className="text-amber-200 text-xs font-semibold flex items-center gap-1">
                        <Sparkles className="w-3 h-3" />
                        PREMIUM
                      </span>
                    </div>
                  )}
                </div>
                <h3 className="text-xl font-bold text-white mb-2">
                  {category.title}
                </h3>
                <p className="text-white/80 text-sm mb-4">
                  {category.description}
                </p>
                <div className="flex flex-wrap gap-2">
                  {category.features.map((feature, index) => (
                    <div key={index} className="px-2 py-1 bg-purple-500/30 text-purple-200 text-xs rounded-full">
                      {feature}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* 선택된 카테고리의 서비스 목록 */}
        {selectedCategory && (
          <div className="animate-fade-in">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">
              📋 {categories.find(c => c.id === selectedCategory)?.title} 서비스
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services[selectedCategory]?.map((service) => (
                <div key={service.id} className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:bg-white/20 transition-all duration-300 hover:shadow-lg">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-lg text-white">
                      {service.name}
                    </h3>
                    {service.isPremium && (
                      <div className="px-2 py-1 bg-amber-500/20 border border-amber-400/50 rounded-full">
                        <span className="text-amber-200 text-xs font-semibold">PRO</span>
                      </div>
                    )}
                  </div>
                  
                  <p className="text-white/80 text-sm mb-4 leading-relaxed">
                    {service.description}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-lg font-bold text-purple-300">
                      {service.price || 'FREE'}
                    </span>
                    <button 
                      className={`px-4 py-2 rounded-lg text-white font-medium transition-all duration-300 hover:scale-105 ${
                        service.isPremium 
                          ? 'bg-gradient-to-r from-amber-500/80 to-orange-500/80 hover:from-amber-500 hover:to-orange-500' 
                          : 'bg-gradient-to-r from-purple-500/80 to-pink-500/80 hover:from-purple-500 hover:to-pink-500'
                      }`}
                      onClick={() => handleServiceClick(service.id)}
                    >
                      {service.isPremium ? '프리미엄 시작' : '무료 체험'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 특별 혜택 섹션 */}
        <div className="mt-16">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-8 text-center">
            <h2 className="text-2xl font-bold text-white mb-4">
              🎁 런칭 기념 특별 혜택
            </h2>
            <p className="text-white/80 mb-6">
              지금 가입하면 모든 프리미엄 서비스 <strong className="text-amber-300">30일 무료</strong> + 
              개인 맞춤 운세 리포트 <strong className="text-amber-300">무료 제공</strong>!
            </p>
            <button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-3 rounded-lg font-medium transition-all duration-300 hover:scale-105">
              🚀 지금 시작하기
            </button>
          </div>
        </div>

        {/* 하단 안내 */}
        <div className="mt-12 text-center text-white/60 text-sm">
          <p>
            🔒 개인정보 보호 • ⚡ 실시간 업데이트 • 🎯 AI 개인화
          </p>
          <p className="mt-2">
            문의: help@heal7.com | 전화: 1588-7777
          </p>
        </div>

      </div>
    </div>
  );
};

export default FortuneCategories;