import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, 
  Shield, 
  Users, 
  Cpu, 
  Globe, 
  Code, 
  Settings, 
  Target,
  ChevronDown,
  ChevronRight,
  Play,
  Pause,
  RotateCcw,
  Info,
  CheckCircle,
  AlertCircle,
  ArrowRight
} from 'lucide-react';
import { safeAPICall, APIError } from '../../utils/ErrorHandler';

interface CrawlerTool {
  tool_type: string;
  display_name: string;
  description: string;
  strengths: string[];
  weaknesses: string[];
  performance_score: number;
  reliability_score: number;
  ease_of_use_score: number;
  resource_usage: string;
  javascript_support: boolean;
  async_support: boolean;
  installation_complexity: string;
  recommended_fallbacks: string[];
  radial_data: {
    performance: number;
    reliability: number;
    ease_of_use: number;
    resource_efficiency: number;
  };
}

interface ToolRecommendation {
  primary_tool: string;
  confidence_score: number;
  reasoning: string;
  fallback_tools: string[];
  setup_steps: string[];
  estimated_performance: {
    estimated_speed_rpm: number;
    estimated_reliability: string;
    resource_usage: string;
    maintenance_level: string;
  };
}

interface CrawlingRequirements {
  target_urls: string[];
  expected_data_types: string[];
  javascript_required: boolean;
  form_interaction_required: boolean;
  expected_volume: 'small' | 'medium' | 'large';
  priority: 'speed' | 'reliability' | 'balanced';
  budget_constraint: 'low' | 'medium' | 'high';
}

const CrawlerToolSelector: React.FC = () => {
  const [availableTools, setAvailableTools] = useState<CrawlerTool[]>([]);
  const [selectedTool, setSelectedTool] = useState<CrawlerTool | null>(null);
  const [recommendations, setRecommendations] = useState<ToolRecommendation[]>([]);
  const [requirements, setRequirements] = useState<CrawlingRequirements>({
    target_urls: [''],
    expected_data_types: ['text'],
    javascript_required: false,
    form_interaction_required: false,
    expected_volume: 'medium',
    priority: 'balanced',
    budget_constraint: 'medium'
  });
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState<APIError | null>(null);
  const [activeTab, setActiveTab] = useState<'browse' | 'recommend' | 'compare'>('browse');
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  useEffect(() => {
    loadAvailableTools();
  }, []);

  const loadAvailableTools = async () => {
    setLoading(true);
    setApiError(null);
    console.log('[DEV] 크롤링 도구 목록 API 호출 시작...');

    const { data, error } = await safeAPICall<{ tools: CrawlerTool[] }>(
      '/api/crawler-tools/available-tools',
      { method: 'GET' },
      { component: 'CrawlerToolSelector', action: 'loadAvailableTools' }
    );

    if (error) {
      console.error(`[DEV] 크롤링 도구 목록 API 오류 - ${error.code}: ${error.message}`);
      setApiError(error);
      setAvailableTools([]);
    } else if (data && data.tools) {
      console.log(`[DEV] 크롤링 도구 목록 로드 완료 - ${data.tools.length}개 도구`);
      setAvailableTools(data.tools);
      setApiError(null);
    }

    setLoading(false);
  };

  const getToolRecommendations = async () => {
    console.log('[DEV] 도구 추천 API 호출 시작...', requirements);

    const { data, error } = await safeAPICall<{ recommendations: ToolRecommendation[] }>(
      '/api/crawler-tools/recommend',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requirements)
      },
      { component: 'CrawlerToolSelector', action: 'getToolRecommendations' }
    );

    if (error) {
      console.error(`[DEV] 도구 추천 API 오류 - ${error.code}: ${error.message}`);
      setApiError(error);
    } else if (data && data.recommendations) {
      console.log(`[DEV] 도구 추천 완료 - ${data.recommendations.length}개 추천`);
      setRecommendations(data.recommendations);
      setActiveTab('recommend');
    }
  };

  const getResourceUsageColor = (usage: string) => {
    switch (usage) {
      case 'low': return 'text-green-400 bg-green-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/20';
      case 'high': return 'text-red-400 bg-red-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getComplexityIcon = (complexity: string) => {
    switch (complexity) {
      case 'easy': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'medium': return <AlertCircle className="w-4 h-4 text-yellow-400" />;
      case 'hard': return <Settings className="w-4 h-4 text-red-400" />;
      default: return <Info className="w-4 h-4 text-gray-400" />;
    }
  };

  // 방사형 차트 생성 함수
  const RadialChart: React.FC<{ data: CrawlerTool['radial_data']; size?: number }> = ({ data, size = 120 }) => {
    const center = size / 2;
    const radius = size / 2 - 20;
    const categories = ['performance', 'reliability', 'ease_of_use', 'resource_efficiency'];
    const labels = ['성능', '안정성', '사용성', '효율성'];
    
    const points = categories.map((category, index) => {
      const angle = (index * Math.PI * 2) / 4 - Math.PI / 2; // Start from top
      const value = data[category as keyof typeof data] / 10; // Normalize to 0-1
      const x = center + Math.cos(angle) * radius * value;
      const y = center + Math.sin(angle) * radius * value;
      return { x, y, value: data[category as keyof typeof data], label: labels[index] };
    });

    const pathData = `M ${points[0].x} ${points[0].y} ` + 
      points.slice(1).map(p => `L ${p.x} ${p.y}`).join(' ') + ' Z';

    return (
      <div className="relative">
        <svg width={size} height={size} className="transform">
          {/* Grid lines */}
          {[0.2, 0.4, 0.6, 0.8, 1.0].map((scale, idx) => (
            <polygon
              key={idx}
              points={categories.map((_, index) => {
                const angle = (index * Math.PI * 2) / 4 - Math.PI / 2;
                const x = center + Math.cos(angle) * radius * scale;
                const y = center + Math.sin(angle) * radius * scale;
                return `${x},${y}`;
              }).join(' ')}
              fill="none"
              stroke="rgb(71, 85, 105)"
              strokeWidth="0.5"
              opacity={0.3}
            />
          ))}
          
          {/* Axis lines */}
          {categories.map((_, index) => {
            const angle = (index * Math.PI * 2) / 4 - Math.PI / 2;
            const x = center + Math.cos(angle) * radius;
            const y = center + Math.sin(angle) * radius;
            return (
              <line
                key={index}
                x1={center}
                y1={center}
                x2={x}
                y2={y}
                stroke="rgb(71, 85, 105)"
                strokeWidth="0.5"
                opacity={0.5}
              />
            );
          })}
          
          {/* Data area */}
          <path
            d={pathData}
            fill="rgb(59, 130, 246)"
            fillOpacity={0.3}
            stroke="rgb(59, 130, 246)"
            strokeWidth={2}
          />
          
          {/* Data points */}
          {points.map((point, index) => (
            <circle
              key={index}
              cx={point.x}
              cy={point.y}
              r={3}
              fill="rgb(59, 130, 246)"
            />
          ))}
        </svg>
        
        {/* Labels */}
        <div className="absolute inset-0 pointer-events-none">
          {points.map((point, index) => {
            const angle = (index * Math.PI * 2) / 4 - Math.PI / 2;
            const labelRadius = radius + 15;
            const labelX = center + Math.cos(angle) * labelRadius;
            const labelY = center + Math.sin(angle) * labelRadius;
            
            return (
              <div
                key={index}
                className="absolute text-xs text-slate-400 transform -translate-x-1/2 -translate-y-1/2"
                style={{
                  left: labelX,
                  top: labelY,
                }}
              >
                {point.label}
                <br/>
                <span className="text-blue-400 font-medium">{point.value}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const ToolCard: React.FC<{ tool: CrawlerTool }> = ({ tool }) => {
    const isExpanded = expandedCard === tool.tool_type;
    
    return (
      <motion.div
        className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl border border-slate-600/50 overflow-hidden"
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-white mb-2">{tool.display_name}</h3>
              <p className="text-slate-400 text-sm mb-3">{tool.description}</p>
              
              <div className="flex items-center space-x-2 mb-3">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getResourceUsageColor(tool.resource_usage)}`}>
                  {tool.resource_usage} 리소스
                </span>
                {tool.javascript_support && (
                  <span className="px-2 py-1 bg-purple-500/20 text-purple-400 rounded-full text-xs font-medium">
                    JS 지원
                  </span>
                )}
                {tool.async_support && (
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded-full text-xs font-medium">
                    비동기
                  </span>
                )}
              </div>
            </div>
            
            <div className="ml-4">
              <RadialChart data={tool.radial_data} size={100} />
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {getComplexityIcon(tool.installation_complexity)}
              <span className="text-sm text-slate-400">
                설치 {tool.installation_complexity === 'easy' ? '쉬움' : 
                     tool.installation_complexity === 'medium' ? '보통' : '어려움'}
              </span>
            </div>
            
            <button
              onClick={() => setExpandedCard(isExpanded ? null : tool.tool_type)}
              className="flex items-center space-x-1 text-blue-400 hover:text-blue-300 transition-colors"
            >
              <span className="text-sm">자세히</span>
              {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </button>
          </div>

          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="mt-4 pt-4 border-t border-slate-600/30"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-sm font-medium text-green-400 mb-2">💪 장점</h4>
                    <ul className="space-y-1">
                      {tool.strengths.map((strength, idx) => (
                        <li key={idx} className="text-sm text-slate-300 flex items-start">
                          <span className="mr-2">•</span>
                          <span>{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium text-red-400 mb-2">⚠️ 단점</h4>
                    <ul className="space-y-1">
                      {tool.weaknesses.map((weakness, idx) => (
                        <li key={idx} className="text-sm text-slate-300 flex items-start">
                          <span className="mr-2">•</span>
                          <span>{weakness}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                {tool.recommended_fallbacks.length > 0 && (
                  <div className="mt-4">
                    <h4 className="text-sm font-medium text-yellow-400 mb-2">🔄 추천 폴백</h4>
                    <div className="flex flex-wrap gap-2">
                      {tool.recommended_fallbacks.map((fallback, idx) => (
                        <span key={idx} className="px-2 py-1 bg-yellow-500/20 text-yellow-300 rounded text-xs">
                          {fallback}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                <div className="mt-4 flex justify-end">
                  <button
                    onClick={() => setSelectedTool(tool)}
                    className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center space-x-2"
                  >
                    <Target className="w-4 h-4" />
                    <span>이 도구 선택</span>
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            크롤링 도구 선택기
          </h1>
          <p className="text-slate-400 mt-2">목적에 맞는 최적의 크롤링 도구를 선택하세요</p>
        </div>
        
        <button
          onClick={loadAvailableTools}
          className="p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-slate-300 transition-colors"
          title="새로고침"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* API 에러 표시 */}
      {apiError && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-red-500/10 to-pink-500/10 border border-red-500/30 rounded-xl p-4"
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
              <div>
                <h3 className="text-red-300 font-medium">크롤링 도구 API 오류</h3>
                <p className="text-red-200/80 text-sm mt-1">{apiError.message}</p>
                <div className="text-xs text-red-300/60 mt-2">
                  <span className="font-mono bg-red-500/20 px-2 py-1 rounded">
                    {apiError.code} | {apiError.timestamp}
                  </span>
                </div>
              </div>
            </div>
            <button
              onClick={() => {
                setApiError(null);
                loadAvailableTools();
              }}
              className="text-red-300 hover:text-red-100 transition-colors p-1 hover:bg-red-500/20 rounded"
              title="다시 시도"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </motion.div>
      )}

      {/* 탭 네비게이션 */}
      <div className="flex space-x-1 bg-slate-800/50 rounded-lg p-1">
        {[
          { id: 'browse', label: '도구 둘러보기', icon: Globe },
          { id: 'recommend', label: '맞춤 추천', icon: Target },
          { id: 'compare', label: '비교 분석', icon: Settings }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors flex-1 justify-center ${
              activeTab === tab.id 
                ? 'bg-blue-500 text-white' 
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* 탭 콘텐츠 */}
      <AnimatePresence mode="wait">
        {activeTab === 'browse' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-2 border-blue-500 border-t-transparent"></div>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {availableTools.map((tool) => (
                  <ToolCard key={tool.tool_type} tool={tool} />
                ))}
              </div>
            )}
          </motion.div>
        )}

        {activeTab === 'recommend' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {/* 요구사항 입력 폼 */}
            <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Target className="w-5 h-5 mr-2 text-blue-400" />
                크롤링 요구사항
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    대상 URL
                  </label>
                  <input
                    type="url"
                    value={requirements.target_urls[0]}
                    onChange={(e) => setRequirements(prev => ({
                      ...prev,
                      target_urls: [e.target.value]
                    }))}
                    placeholder="https://example.com"
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    예상 데이터량
                  </label>
                  <select
                    value={requirements.expected_volume}
                    onChange={(e) => setRequirements(prev => ({
                      ...prev,
                      expected_volume: e.target.value as any
                    }))}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="small">소량 (1-100 페이지)</option>
                    <option value="medium">중간 (100-1000 페이지)</option>
                    <option value="large">대량 (1000+ 페이지)</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    우선순위
                  </label>
                  <select
                    value={requirements.priority}
                    onChange={(e) => setRequirements(prev => ({
                      ...prev,
                      priority: e.target.value as any
                    }))}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="speed">속도 중시</option>
                    <option value="reliability">안정성 중시</option>
                    <option value="balanced">균형</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    예산 제약
                  </label>
                  <select
                    value={requirements.budget_constraint}
                    onChange={(e) => setRequirements(prev => ({
                      ...prev,
                      budget_constraint: e.target.value as any
                    }))}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="low">저예산 (리소스 절약)</option>
                    <option value="medium">중간 예산</option>
                    <option value="high">고예산 (성능 우선)</option>
                  </select>
                </div>
              </div>
              
              <div className="mt-4 space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={requirements.javascript_required}
                    onChange={(e) => setRequirements(prev => ({
                      ...prev,
                      javascript_required: e.target.checked
                    }))}
                    className="rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-slate-300">JavaScript 실행 필요</span>
                </label>
                
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={requirements.form_interaction_required}
                    onChange={(e) => setRequirements(prev => ({
                      ...prev,
                      form_interaction_required: e.target.checked
                    }))}
                    className="rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-slate-300">폼 상호작용 필요</span>
                </label>
              </div>
              
              <div className="mt-6 flex justify-end">
                <button
                  onClick={getToolRecommendations}
                  className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center space-x-2"
                >
                  <Target className="w-4 h-4" />
                  <span>추천 받기</span>
                </button>
              </div>
            </div>
            
            {/* 추천 결과 */}
            {recommendations.length > 0 && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-white flex items-center">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  추천 결과
                </h2>
                
                {recommendations.map((rec, index) => {
                  const tool = availableTools.find(t => t.tool_type === rec.primary_tool);
                  if (!tool) return null;
                  
                  return (
                    <motion.div
                      key={rec.primary_tool}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-gradient-to-br from-green-900/20 to-blue-900/20 backdrop-blur-sm rounded-xl p-6 border border-green-500/30"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="text-xl font-semibold text-white">{tool.display_name}</h3>
                            <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm font-medium">
                              {rec.confidence_score.toFixed(1)}% 적합
                            </span>
                            {index === 0 && (
                              <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded-full text-xs font-medium">
                                최고 추천
                              </span>
                            )}
                          </div>
                          <p className="text-slate-300 mb-3">{rec.reasoning}</p>
                        </div>
                        <RadialChart data={tool.radial_data} size={80} />
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="text-sm font-medium text-blue-400 mb-2">📊 예상 성능</h4>
                          <ul className="space-y-1 text-sm text-slate-300">
                            <li>• 처리 속도: {rec.estimated_performance.estimated_speed_rpm} rpm</li>
                            <li>• 예상 안정성: {rec.estimated_performance.estimated_reliability}</li>
                            <li>• 리소스 사용: {rec.estimated_performance.resource_usage}</li>
                            <li>• 유지보수: {rec.estimated_performance.maintenance_level}</li>
                          </ul>
                        </div>
                        
                        {rec.fallback_tools.length > 0 && (
                          <div>
                            <h4 className="text-sm font-medium text-yellow-400 mb-2">🔄 폴백 도구</h4>
                            <div className="flex flex-wrap gap-2">
                              {rec.fallback_tools.map((fallback, idx) => (
                                <span key={idx} className="px-2 py-1 bg-yellow-500/20 text-yellow-300 rounded text-xs">
                                  {fallback}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                      
                      <div className="mt-4 flex justify-end">
                        <button
                          onClick={() => setSelectedTool(tool)}
                          className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors flex items-center space-x-2"
                        >
                          <Play className="w-4 h-4" />
                          <span>이 도구로 시작</span>
                        </button>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* 선택된 도구 확인 모달 */}
      {selectedTool && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedTool(null)}
        >
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-slate-800 rounded-xl p-6 max-w-md w-full border border-slate-600"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
              도구 선택 확인
            </h3>
            
            <p className="text-slate-300 mb-6">
              <strong>{selectedTool.display_name}</strong>을(를) 크롤링 도구로 선택하시겠습니까?
            </p>
            
            <div className="flex space-x-3">
              <button
                onClick={() => setSelectedTool(null)}
                className="flex-1 px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg transition-colors"
              >
                취소
              </button>
              <button
                onClick={() => {
                  console.log(`[DEV] 도구 선택됨: ${selectedTool.display_name}`);
                  setSelectedTool(null);
                  // 실제 크롤링 작업 시작 로직
                }}
                className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center justify-center space-x-2"
              >
                <ArrowRight className="w-4 h-4" />
                <span>선택</span>
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default CrawlerToolSelector;