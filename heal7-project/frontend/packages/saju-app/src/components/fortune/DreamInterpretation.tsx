import React, { useState, useEffect } from 'react';
import { Search, Sparkles, Moon, Star, Tags, TrendingUp, BookOpen, Lightbulb, Eye, Globe } from 'lucide-react';
import { 
  dreamCategories, 
  popularDreamKeywords, 
  searchDreams, 
  getCombinationInterpretation,
  getSeasonalDreams,
  type DreamInterpretation as DreamType 
} from '../../data/dreamData';
// import dreamInterpretations from '../../data/enhanced_dreamData'; // 하드코딩 제거
import MultiPerspectiveDreamComparison from './MultiPerspectiveDreamComparison';
import { useTheme } from '../../contexts/ThemeContext';
import { getThemeTextClasses, themeTransitions } from '../../utils/themeStyles';

type ViewMode = 'basic' | 'cyber_fantasy'

interface DreamInterpretationProps {
  onClose?: () => void;
  viewMode: ViewMode;
}

export const DreamInterpretation: React.FC<DreamInterpretationProps> = ({ onClose: _, viewMode }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<DreamType[]>([]);
  const [selectedDream, setSelectedDream] = useState<DreamType | null>(null);
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);
  const [, setIsSearching] = useState(false);
  const [currentMonth] = useState(new Date().getMonth() + 1);
  const [dreamViewMode, setDreamViewMode] = useState<'regular' | 'multi-perspective'>('regular');
  
  // 테마 훅 추가
  const { theme } = useTheme();

  useEffect(() => {
    if (searchQuery.trim()) {
      setIsSearching(true);
      
      // API 호출로 데이터베이스 검색
      const searchDreamAPI = async () => {
        try {
          const query = searchQuery.toLowerCase().trim();
          const response = await fetch('/api/dreams/search', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              keywords: [query],
              search_mode: "any",
              limit: 10
            })
          });

          if (response.ok) {
            const apiResults = await response.json();
            
            // API 응답 구조 확인: List[DreamInterpretationResponse]
            if (Array.isArray(apiResults)) {
              // API 응답을 프론트엔드 형식으로 변환
              const formattedResults = apiResults.map((dream: any, index: number) => ({
                id: (index + 1).toString(),
                keyword: dream.keyword || '알 수 없는 꿈',
                category: dream.category || '꿈풀이',
                emoji: '🌙', // 기본 이모지 (백엔드에서 emoji 필드 없음)
                traditionInterpretation: dream.traditional_meaning || '',
                modernInterpretation: dream.modern_meaning || dream.traditional_meaning || '',
                psychologyInterpretation: dream.psychological_meaning || '',
                mood: dream.fortune_aspect === '길몽' ? 'positive' : 
                      dream.fortune_aspect === '흉몽' ? 'negative' : 'neutral',
                frequency: Math.round(dream.confidence_score * 10) || Math.floor(Math.random() * 100) + 1,
                keywords: Array.isArray(dream.related_keywords) ? dream.related_keywords : [dream.keyword].filter(Boolean),
                variations: [dream.keyword].filter(Boolean),
                luckyNumbers: Array.isArray(dream.lucky_numbers) ? dream.lucky_numbers : [],
                tags: ['꿈풀이'],
                relatedDreams: Array.isArray(dream.related_keywords) ? dream.related_keywords : []
              }));
              
              console.log('Formatted Results:', formattedResults);
              setSearchResults(formattedResults);
            } else {
              console.warn('API 응답 형식 오류:', apiResults);
              // API 응답이 예상 형식이 아닐 경우 빈 결과 표시
              setSearchResults([]);
            }
          } else {
            // API 실패 시 빈 결과 표시
            console.warn('API 호출 실패:', response.status, response.statusText);
            setSearchResults([]);
          }
        } catch (error) {
          console.error('API 호출 오류:', error);
          // 오류 시 빈 결과 표시
          setSearchResults([]);
        } finally {
          setIsSearching(false);
        }
      };

      searchDreamAPI();
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const handleKeywordClick = (keyword: string) => {
    if (!selectedKeywords.includes(keyword)) {
      setSelectedKeywords(prev => [...prev, keyword]);
    }
  };

  const removeKeyword = (keyword: string) => {
    setSelectedKeywords(prev => prev.filter(k => k !== keyword));
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const getMoodColor = (mood: string) => {
    switch (mood) {
      case 'positive': return 'text-green-400';
      case 'negative': return 'text-red-400';
      case 'warning': return 'text-yellow-400';
      default: return 'text-blue-400';
    }
  };

  const getMoodBg = (mood: string) => {
    switch (mood) {
      case 'positive': return 'bg-green-500/10';
      case 'negative': return 'bg-red-500/10';
      case 'warning': return 'bg-yellow-500/10';
      default: return 'bg-blue-500/10';
    }
  };

  const seasonalDreams = getSeasonalDreams(currentMonth);
  const combinationInterpretation = selectedKeywords.length >= 2 
    ? getCombinationInterpretation(selectedKeywords) 
    : '';

  // 다각도 비교 모드일 때 해당 컴포넌트 렌더링
  if (dreamViewMode === 'multi-perspective') {
    return <MultiPerspectiveDreamComparison onClose={() => setDreamViewMode('regular')} />;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="max-w-6xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Moon className={`w-8 h-8 ${getThemeTextClasses.primary(theme)}`} />
            <h1 className={`text-4xl font-bold ${getThemeTextClasses.primary(theme)}`}>🔮 AI 꿈해몽 센터</h1>
            <Star className="w-8 h-8 text-yellow-300" />
          </div>
          <p className={`${getThemeTextClasses.secondary(theme)} text-lg mb-4`}>
            당신의 꿈이 전하는 메시지를 AI와 전통 명리학으로 해석해드립니다
          </p>
          
          {/* 다각도 비교 버튼 */}
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => setDreamViewMode('multi-perspective')}
              className={`flex items-center gap-2 bg-gradient-to-r from-[var(--theme-primary)]/30 to-[var(--theme-secondary)]/30 hover:from-[var(--theme-primary)]/50 hover:to-[var(--theme-secondary)]/50 border border-[var(--theme-primary)]/50 ${getThemeTextClasses.primary(theme)} px-4 py-2 rounded-lg font-medium transition-all`}
            >
              <Eye className="w-4 h-4" />
              <Globe className="w-4 h-4" />
              다각도 문화 비교
            </button>
            <span className={getThemeTextClasses.subtle(theme)}>|</span>
            <span className={`${getThemeTextClasses.muted(theme)} text-sm`}>
              같은 꿈도 문화권마다 다르게 해석됩니다
            </span>
          </div>
        </div>

        {/* 검색 영역 */}
        <div className={`p-6 mb-8 ${
          viewMode === 'cyber_fantasy' ? 'card-featured' : 'card-base'
        }`}>
          <div className="relative mb-6">
            <Search className={`absolute left-4 top-1/2 transform -translate-y-1/2 ${getThemeTextClasses.icon(theme)} w-5 h-5`} />
            <input
              type="text"
              placeholder="꿈에서 본 것을 검색해보세요 (예: 뱀, 물, 돈, 날아가기)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={`w-full glass-4 pl-12 pr-4 py-3 ${getThemeTextClasses.primary(theme)} ${getThemeTextClasses.placeholder(theme)} focus:outline-none focus:ring-2 focus:ring-purple-500`}
            />
          </div>

          {/* 선택된 키워드 */}
          {selectedKeywords.length > 0 && (
            <div className="mb-6">
              <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-3 flex items-center gap-2`}>
                <Tags className="w-4 h-4" />
                선택된 꿈 키워드
              </h3>
              <div className="flex flex-wrap gap-2">
                {selectedKeywords.map((keyword) => (
                  <span
                    key={keyword}
                    className={`bg-[var(--theme-primary)]/30 ${getThemeTextClasses.primary(theme)} px-3 py-1 rounded-full text-sm cursor-pointer hover:bg-[var(--theme-primary)]/40 transition-colors`}
                    onClick={() => removeKeyword(keyword)}
                  >
                    {keyword} ×
                  </span>
                ))}
              </div>
              
              {/* 조합 해석 */}
              {combinationInterpretation && (
                <div className="mt-4 bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
                  <h4 className={`${getThemeTextClasses.combination(theme)} font-medium mb-2 flex items-center gap-2`}>
                    <Sparkles className="w-4 h-4" />
                    조합 해석
                  </h4>
                  <p className={`${getThemeTextClasses.combinationSecondary(theme)} text-sm`}>{combinationInterpretation}</p>
                </div>
              )}
            </div>
          )}

          {/* 인기 키워드 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-3 flex items-center gap-2`}>
                <TrendingUp className="w-4 h-4" />
                인기 꿈 키워드
              </h3>
              <div className="flex flex-wrap gap-2">
                {popularDreamKeywords.slice(0, 15).map((keyword) => (
                  <button
                    key={keyword}
                    onClick={() => handleSearch(keyword)}
                    className={`card-nav px-3 py-1 rounded-full text-sm ${getThemeTextClasses.interactive(theme)}`}
                  >
                    {keyword}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-3 flex items-center gap-2`}>
                <Star className="w-4 h-4" />
                이달의 꿈 키워드
              </h3>
              <div className="flex flex-wrap gap-2">
                {seasonalDreams.map((keyword) => (
                  <button
                    key={keyword}
                    onClick={() => handleSearch(keyword)}
                    className={`bg-gradient-to-r from-[var(--theme-secondary)]/30 to-[var(--theme-primary)]/30 hover:from-[var(--theme-secondary)]/40 hover:to-[var(--theme-primary)]/40 ${getThemeTextClasses.primary(theme)} px-3 py-1 rounded-full text-sm transition-colors`}
                  >
                    {keyword}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 카테고리 & 검색 결과 */}
          <div className="lg:col-span-2">
            {searchResults.length > 0 ? (
              <div className="space-y-4">
                <h2 className={`${getThemeTextClasses.primary(theme)} text-xl font-bold mb-4`}>
                  검색 결과 ({searchResults.length}개)
                </h2>
                {searchResults.map((dream) => (
                  <div
                    key={dream.id}
                    className={`card-nav p-4 cursor-pointer ${selectedDream?.id === dream.id ? 'active ring-2 ring-[var(--theme-accent)]' : ''}`}
                    onClick={() => setSelectedDream(dream)}
                  >
                    <div className="flex items-start gap-4">
                      <div className="text-3xl">{dream.emoji}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className={`${getThemeTextClasses.primary(theme)} font-bold text-lg`}>{dream.keyword}</h3>
                          <span className={`text-xs px-2 py-1 rounded-full ${getMoodBg(dream.mood)} ${getMoodColor(dream.mood)}`}>
                            {dream.mood === 'positive' ? '길몽' : dream.mood === 'negative' ? '흉몽' : dream.mood === 'warning' ? '주의' : '중성'}
                          </span>
                          <span className={`${getThemeTextClasses.muted(theme)} text-sm`}>검색 {dream.frequency}회</span>
                        </div>
                        <p className={`${getThemeTextClasses.secondary(theme)} text-sm mb-2 line-clamp-2`}>
                          {dream.modernInterpretation}
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {dream.keywords.slice(0, 4).map((keyword) => (
                            <span
                              key={keyword}
                              className={`${getThemeTextClasses.hashtagContainer(theme)} ${getThemeTextClasses.hashtag(theme)} px-2 py-1 rounded text-xs cursor-pointer transition-colors`}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleKeywordClick(keyword);
                              }}
                            >
                              #{keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-6">
                <h2 className={`${getThemeTextClasses.primary(theme)} text-xl font-bold mb-4`}>꿈 카테고리</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {dreamCategories.map((category) => (
                    <div
                      key={category.id}
                      className="card-nav p-4 text-center cursor-pointer"
                      onClick={() => handleSearch(category.name)}
                    >
                      <div className="text-3xl mb-2">{category.emoji}</div>
                      <h3 className={`${getThemeTextClasses.primary(theme)} font-medium`}>{category.name}</h3>
                      <p className={`${getThemeTextClasses.muted(theme)} text-xs mt-1`}>{category.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* 상세 해석 */}
          <div className="lg:col-span-1">
            {selectedDream ? (
              <div className="glass-3 p-6 sticky top-6">
                <div className="text-center mb-6">
                  <div className="text-6xl mb-3">{selectedDream.emoji}</div>
                  <h2 className={`text-2xl font-bold ${getThemeTextClasses.primary(theme)} mb-2`}>{selectedDream.keyword}</h2>
                  <span className={`text-sm px-3 py-1 rounded-full ${getMoodBg(selectedDream.mood)} ${getMoodColor(selectedDream.mood)}`}>
                    {selectedDream.mood === 'positive' ? '길몽' : selectedDream.mood === 'negative' ? '흉몽' : selectedDream.mood === 'warning' ? '주의' : '중성'}
                  </span>
                </div>

                <div className="space-y-6">
                  {/* 전통 해석 */}
                  <div>
                    <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2 flex items-center gap-2`}>
                      <BookOpen className="w-4 h-4" />
                      전통적 해석
                    </h3>
                    <p className={`${getThemeTextClasses.secondary(theme)} text-sm`}>{selectedDream.traditionInterpretation}</p>
                  </div>

                  {/* 현대적 해석 */}
                  <div>
                    <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2 flex items-center gap-2`}>
                      <Lightbulb className="w-4 h-4" />
                      현대적 해석
                    </h3>
                    <p className={`${getThemeTextClasses.secondary(theme)} text-sm`}>{selectedDream.modernInterpretation}</p>
                  </div>

                  {/* 심리학적 해석 */}
                  {selectedDream.psychologyInterpretation && (
                    <div>
                      <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2 flex items-center gap-2`}>
                        <span className={getThemeTextClasses.primary(theme)}>🧠</span>
                        심리학적 해석
                      </h3>
                      <p className={`${getThemeTextClasses.secondary(theme)} text-sm`}>{selectedDream.psychologyInterpretation}</p>
                    </div>
                  )}

                  {/* 행운의 숫자 */}
                  {selectedDream.luckyNumbers && selectedDream.luckyNumbers.length > 0 && (
                    <div>
                      <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2`}>🎰 행운의 숫자</h3>
                      <div className="flex gap-2">
                        {selectedDream.luckyNumbers.map((num) => (
                          <span key={num} className={`bg-gradient-to-r from-yellow-500/30 to-orange-500/30 ${getThemeTextClasses.luckyNumber(theme)} w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold`}>
                            {num}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 키워드 */}
                  <div>
                    <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2`}>🏷️ 연관 키워드</h3>
                    <div className="flex flex-wrap gap-1">
                      {selectedDream.keywords.map((keyword) => (
                        <span
                          key={keyword}
                          className={`${getThemeTextClasses.hashtagContainer(theme)} ${getThemeTextClasses.hashtag(theme)} px-2 py-1 rounded text-xs cursor-pointer transition-colors`}
                          onClick={() => handleKeywordClick(keyword)}
                        >
                          #{keyword}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* 관련 꿈 */}
                  {selectedDream.relatedDreams.length > 0 && (
                    <div>
                      <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2`}>🔗 관련 꿈</h3>
                      <div className="flex flex-wrap gap-2">
                        {selectedDream.relatedDreams.map((related) => (
                          <button
                            key={related}
                            onClick={() => handleSearch(related)}
                            className={`card-compact !p-2 text-xs cursor-pointer ${getThemeTextClasses.interactive(theme)}`}
                          >
                            {related}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="glass-3 p-6 text-center">
                <Moon className={`w-16 h-16 ${getThemeTextClasses.primary(theme)} mx-auto mb-4`} />
                <h3 className={`${getThemeTextClasses.primary(theme)} font-medium mb-2`}>꿈을 선택해주세요</h3>
                <p className={`${getThemeTextClasses.muted(theme)} text-sm`}>
                  왼쪽에서 꿈을 검색하거나 카테고리를 선택하면
                  <br />
                  상세한 해석을 볼 수 있습니다
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DreamInterpretation;