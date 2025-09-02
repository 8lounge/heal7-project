import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Sparkles, 
  Moon, 
  Star, 
  BookOpen, 
  Globe,
  Users,
  Brain,
  Heart,
  Zap,
  Eye,
  RotateCcw,
  ChevronRight,
  ArrowLeftRight,
  Scale
} from 'lucide-react';

// 다각도 해석 타입 정의
interface Perspective {
  id: string;
  name: string;
  description: string;
  emoji: string;
  color: string;
  bgColor: string;
  icon: React.ComponentType<any>;
}

interface MultiPerspectiveInterpretation {
  dream_id: string;
  keyword: string;
  emoji: string;
  perspectives: {
    [key: string]: {
      perspective_id: string;
      perspective_name: string;
      interpretation: string;
      cultural_context: string;
      confidence_score: number;
      source_quality: 'verified' | 'community' | 'ai_generated';
      tags: string[];
    }
  };
  comparison_analysis: {
    common_themes: string[];
    conflicting_views: string[];
    cultural_differences: string[];
    recommended_interpretation: string;
  };
}

interface MultiPerspectiveDreamComparisonProps {
  onClose?: () => void;
}

const perspectives: Perspective[] = [
  {
    id: 'korean_traditional',
    name: '한국 전통',
    description: '전통 민속 해몽서 기반',
    emoji: '🏯',
    color: 'text-red-300',
    bgColor: 'bg-red-500/10 border-red-500/30',
    icon: BookOpen
  },
  {
    id: 'chinese_traditional', 
    name: '중국 전통',
    description: '주공해몽, 역경 기반',
    emoji: '🏮',
    color: 'text-yellow-300',
    bgColor: 'bg-yellow-500/10 border-yellow-500/30', 
    icon: Star
  },
  {
    id: 'western_psychology',
    name: '서구 심리학',
    description: '프로이드, 융 이론 기반',
    emoji: '🧠',
    color: 'text-blue-300',
    bgColor: 'bg-blue-500/10 border-blue-500/30',
    icon: Brain
  },
  {
    id: 'islamic',
    name: '이슬람 해몽',
    description: '이븐 시린 해몽서 기반',
    emoji: '🕌',
    color: 'text-green-300', 
    bgColor: 'bg-green-500/10 border-green-500/30',
    icon: Moon
  },
  {
    id: 'buddhist',
    name: '불교적 해석',
    description: '불교 경전 및 법문 기반',
    emoji: '☸️',
    color: 'text-white',
    bgColor: 'bg-purple-500/10 border-purple-500/30',
    icon: Heart
  },
  {
    id: 'scientific',
    name: '과학적 분석',
    description: '신경과학, 수면연구 기반',
    emoji: '🔬',
    color: 'text-cyan-300',
    bgColor: 'bg-cyan-500/10 border-cyan-500/30',
    icon: Zap
  }
];

export const MultiPerspectiveDreamComparison: React.FC<MultiPerspectiveDreamComparisonProps> = ({ onClose: _onClose }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDream, setSelectedDream] = useState<MultiPerspectiveInterpretation | null>(null);
  const [selectedPerspectives, setSelectedPerspectives] = useState<string[]>(['korean_traditional', 'western_psychology']);
  const [viewMode, setViewMode] = useState<'side-by-side' | 'stacked' | 'comparison'>('side-by-side');
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<any[]>([]);

  // API 호출 함수
  const searchMultiPerspectiveDreams = async (query: string) => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(`/api/dream-interpretation/multi-perspective/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      setSearchResults(data.results || []);
    } catch (error) {
      console.error('꿈 검색 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadDreamPerspectives = async (dreamId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`/api/dream-interpretation/multi-perspective/${dreamId}?perspectives=${selectedPerspectives.join(',')}`);
      const data = await response.json();
      setSelectedDream(data);
    } catch (error) {
      console.error('다각도 해석 로드 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      if (searchQuery.trim()) {
        searchMultiPerspectiveDreams(searchQuery);
      } else {
        setSearchResults([]);
      }
    }, 500);

    return () => clearTimeout(debounceTimer);
  }, [searchQuery]);

  const togglePerspective = (perspectiveId: string) => {
    setSelectedPerspectives(prev => {
      if (prev.includes(perspectiveId)) {
        return prev.filter(id => id !== perspectiveId);
      } else {
        return [...prev, perspectiveId];
      }
    });
  };

  const getPerspectiveById = (id: string) => perspectives.find(p => p.id === id);

  const renderPerspectiveCard = (perspectiveId: string, data: any) => {
    const perspective = getPerspectiveById(perspectiveId);
    if (!perspective || !data) return null;

    const IconComponent = perspective.icon;

    return (
      <div key={perspectiveId} className={`${perspective.bgColor} backdrop-blur-md border rounded-xl p-6`}>
        <div className="flex items-center gap-3 mb-4">
          <div className="text-2xl">{perspective.emoji}</div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <IconComponent className={`w-4 h-4 ${perspective.color}`} />
              <h3 className={`font-bold ${perspective.color}`}>{perspective.name}</h3>
              <div className={`px-2 py-1 rounded-full text-xs ${perspective.bgColor} ${perspective.color}`}>
                {data.confidence_score}% 신뢰도
              </div>
            </div>
            <p className="text-white/60 text-sm">{perspective.description}</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <h4 className="text-white font-medium mb-2">해석 내용</h4>
            <p className="text-white/80 text-sm leading-relaxed">{data.interpretation}</p>
          </div>

          {data.cultural_context && (
            <div>
              <h4 className="text-white font-medium mb-2">문화적 맥락</h4>
              <p className="text-white/70 text-sm">{data.cultural_context}</p>
            </div>
          )}

          {data.tags && data.tags.length > 0 && (
            <div>
              <h4 className="text-white font-medium mb-2">관련 태그</h4>
              <div className="flex flex-wrap gap-1">
                {data.tags.map((tag: string) => (
                  <span key={tag} className={`px-2 py-1 rounded text-xs ${perspective.bgColor} ${perspective.color}`}>
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center gap-2 text-xs">
            <div className={`w-2 h-2 rounded-full ${
              data.source_quality === 'verified' ? 'bg-green-400' :
              data.source_quality === 'community' ? 'bg-yellow-400' : 'bg-blue-400'
            }`} />
            <span className="text-white/60">
              {data.source_quality === 'verified' ? '검증된 자료' :
               data.source_quality === 'community' ? '커뮤니티 기여' : 'AI 생성'}
            </span>
          </div>
        </div>
      </div>
    );
  };

  const renderComparisonAnalysis = () => {
    if (!selectedDream?.comparison_analysis) return null;

    const analysis = selectedDream.comparison_analysis;

    return (
      <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <Scale className="w-6 h-6 text-amber-300" />
          <h3 className="text-xl font-bold text-white">종합 비교 분석</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* 공통 주제 */}
          {analysis.common_themes.length > 0 && (
            <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
              <h4 className="text-green-300 font-medium mb-3 flex items-center gap-2">
                <Users className="w-4 h-4" />
                공통된 해석
              </h4>
              <ul className="space-y-1">
                {analysis.common_themes.map((theme, index) => (
                  <li key={index} className="text-green-200/80 text-sm flex items-center gap-2">
                    <div className="w-1 h-1 bg-green-400 rounded-full flex-shrink-0" />
                    {theme}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 상충되는 견해 */}
          {analysis.conflicting_views.length > 0 && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <h4 className="text-red-300 font-medium mb-3 flex items-center gap-2">
                <ArrowLeftRight className="w-4 h-4" />
                상충되는 견해
              </h4>
              <ul className="space-y-1">
                {analysis.conflicting_views.map((view, index) => (
                  <li key={index} className="text-red-200/80 text-sm flex items-center gap-2">
                    <div className="w-1 h-1 bg-red-400 rounded-full flex-shrink-0" />
                    {view}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 문화적 차이 */}
          {analysis.cultural_differences.length > 0 && (
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
              <h4 className="text-blue-300 font-medium mb-3 flex items-center gap-2">
                <Globe className="w-4 h-4" />
                문화적 차이점
              </h4>
              <ul className="space-y-1">
                {analysis.cultural_differences.map((diff, index) => (
                  <li key={index} className="text-blue-200/80 text-sm flex items-center gap-2">
                    <div className="w-1 h-1 bg-blue-400 rounded-full flex-shrink-0" />
                    {diff}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 추천 해석 */}
          <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
            <h4 className="text-amber-300 font-medium mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              종합 추천 해석
            </h4>
            <p className="text-amber-200/80 text-sm leading-relaxed">
              {analysis.recommended_interpretation}
            </p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Eye className="w-8 h-8 text-white" />
            <h1 className="text-4xl font-bold text-white">🔮 다각도 꿈해몽 비교</h1>
            <Globe className="w-8 h-8 text-blue-300" />
          </div>
          <p className="text-white/80 text-lg">
            같은 꿈, 다른 문화권의 다양한 해석을 비교해보세요
          </p>
        </div>

        {/* 검색 및 관점 선택 */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 mb-8">
          {/* 검색 입력 */}
          <div className="relative mb-6">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white/60 w-5 h-5" />
            <input
              type="text"
              placeholder="꿈 키워드를 입력해서 다양한 관점의 해석을 비교해보세요"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white/20 border border-white/30 rounded-lg pl-12 pr-4 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>

          {/* 관점 선택 */}
          <div className="mb-6">
            <h3 className="text-white font-medium mb-3">비교할 관점 선택 (최소 2개)</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              {perspectives.map((perspective) => {
                const isSelected = selectedPerspectives.includes(perspective.id);
                const IconComponent = perspective.icon;
                
                return (
                  <button
                    key={perspective.id}
                    onClick={() => togglePerspective(perspective.id)}
                    className={`p-3 rounded-lg border transition-all ${
                      isSelected 
                        ? `${perspective.bgColor} border-current ${perspective.color}` 
                        : 'bg-white/10 border-white/20 text-white/70 hover:bg-white/20'
                    }`}
                  >
                    <div className="text-center">
                      <div className="text-2xl mb-1">{perspective.emoji}</div>
                      <IconComponent className="w-4 h-4 mx-auto mb-1" />
                      <div className="text-xs font-medium">{perspective.name}</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 보기 모드 선택 */}
          <div className="flex items-center gap-4">
            <span className="text-white font-medium">보기 모드:</span>
            <div className="flex gap-2">
              {[
                { key: 'side-by-side', label: '나란히', icon: ArrowLeftRight },
                { key: 'stacked', label: '세로형', icon: RotateCcw },
                { key: 'comparison', label: '비교표', icon: Scale }
              ].map(({ key, label, icon: Icon }) => (
                <button
                  key={key}
                  onClick={() => setViewMode(key as any)}
                  className={`flex items-center gap-2 px-3 py-1 rounded-lg text-sm transition-all ${
                    viewMode === key 
                      ? 'bg-purple-500/30 text-white border border-purple-500/50' 
                      : 'bg-white/10 text-white/70 hover:bg-white/20'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 검색 결과 */}
        {isLoading && (
          <div className="text-center py-12">
            <RotateCcw className="w-8 h-8 text-white mx-auto mb-4 animate-spin" />
            <p className="text-white/80">다각도 해석을 검색하고 있습니다...</p>
          </div>
        )}

        {searchResults.length > 0 && !selectedDream && (
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 mb-8">
            <h2 className="text-white text-xl font-bold mb-4">
              검색 결과 ({searchResults.length}개)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.map((result) => (
                <div
                  key={result.id}
                  className="bg-white/10 border border-white/20 rounded-lg p-4 cursor-pointer hover:bg-white/15 transition-all"
                  onClick={() => loadDreamPerspectives(result.id)}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="text-3xl">{result.emoji}</div>
                    <div className="flex-1">
                      <h3 className="text-white font-bold">{result.keyword}</h3>
                      <p className="text-white/60 text-sm">
                        {result.perspective_count}개 관점 해석 가능
                      </p>
                    </div>
                    <ChevronRight className="w-5 h-5 text-white/40" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 다각도 해석 결과 */}
        {selectedDream && (
          <div className="space-y-8">
            {/* 꿈 정보 헤더 */}
            <div className="text-center bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="text-6xl mb-3">{selectedDream.emoji}</div>
              <h2 className="text-3xl font-bold text-white mb-2">{selectedDream.keyword}</h2>
              <p className="text-white/60">
                {selectedPerspectives.length}개 문화권의 해석을 비교하고 있습니다
              </p>
            </div>

            {/* 관점별 해석 */}
            <div className={`${
              viewMode === 'side-by-side' 
                ? `grid grid-cols-1 ${selectedPerspectives.length === 2 ? 'lg:grid-cols-2' : selectedPerspectives.length === 3 ? 'lg:grid-cols-3' : 'lg:grid-cols-2'} gap-6`
                : 'space-y-6'
            }`}>
              {selectedPerspectives.map((perspectiveId) => {
                const data = selectedDream.perspectives[perspectiveId];
                return renderPerspectiveCard(perspectiveId, data);
              })}
            </div>

            {/* 종합 비교 분석 */}
            {renderComparisonAnalysis()}

            {/* 다시 검색 버튼 */}
            <div className="text-center">
              <button
                onClick={() => {
                  setSelectedDream(null);
                  setSearchQuery('');
                }}
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-6 py-3 rounded-lg font-medium transition-all"
              >
                다른 꿈 검색하기
              </button>
            </div>
          </div>
        )}

        {/* 초기 상태 안내 */}
        {!searchQuery && !selectedDream && (
          <div className="text-center py-20">
            <Moon className="w-16 h-16 text-white mx-auto mb-6" />
            <h3 className="text-white text-xl font-bold mb-4">다각도 꿈해몽 비교</h3>
            <div className="max-w-2xl mx-auto text-white/70 space-y-2">
              <p>같은 꿈도 문화권에 따라 다르게 해석됩니다.</p>
              <p>검색하여 한국, 중국, 서구, 이슬람, 불교, 과학적 관점을 비교해보세요.</p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-w-3xl mx-auto mt-8">
              {['뱀', '물', '비행', '동물', '돈', '꽃'].map((keyword) => (
                <button
                  key={keyword}
                  onClick={() => setSearchQuery(keyword)}
                  className="bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg p-4 text-white transition-all"
                >
                  {keyword} 꿈 비교하기
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MultiPerspectiveDreamComparison;