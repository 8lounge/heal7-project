import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { crawlingAPI } from '../../api/CrawlingAPIClient';
import { 
  Brain,
  Eye,
  FileText,
  Table,
  Image,
  Zap,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Clock,
  CheckCircle,
  XCircle,
  RefreshCw,
  Filter,
  Download,
  Search
} from 'lucide-react';

interface AIModel {
  id: 'gemini' | 'gpt4o' | 'claude';
  name: string;
  displayName: string;
  color: string;
  icon: React.ReactNode;
  stats: {
    totalProcessed: number;
    successRate: number;
    avgProcessingTime: number;
    costPerItem: number;
    totalCost: number;
  };
}

interface ProcessingJob {
  id: string;
  model: 'gemini' | 'gpt4o' | 'claude';
  type: 'document' | 'table' | 'image' | 'ocr';
  status: 'processing' | 'completed' | 'failed' | 'queued';
  title: string;
  sourceUrl: string;
  processingTime: number;
  accuracy: number;
  createdAt: string;
  result?: {
    extractedText?: string;
    tableData?: any[];
    confidence?: number;
  };
}

const AIAnalysis: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState<'all' | 'gemini' | 'gpt4o' | 'claude'>('all');
  const [selectedType, setSelectedType] = useState<'all' | 'document' | 'table' | 'image' | 'ocr'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showDetails, setShowDetails] = useState<string | null>(null);
  const [aiModels, setAIModels] = useState<AIModel[]>([]);
  const [processingJobs, setProcessingJobs] = useState<ProcessingJob[]>([]);
  const [loading, setLoading] = useState(true);

  // 실제 API에서 AI 통계 로드
  useEffect(() => {
    loadAIStats();
  }, []);

  const loadAIStats = async () => {
    setLoading(true);
    try {
      const data = await crawlingAPI.getAIStats();
      if (data) {
        // AI 모델 데이터 변환 (아이콘 추가)
        const modelsWithIcons = data.models.map((model: any) => ({
          ...model,
          icon: model.color === 'blue' ? <Zap className="w-5 h-5" /> :
                model.color === 'green' ? <Eye className="w-5 h-5" /> :
                <Brain className="w-5 h-5" />
        }));
        setAIModels(modelsWithIcons);
        setProcessingJobs(data.processing_jobs);
      }
    } catch (error) {
      console.error('AI 통계 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };


  // 실시간 업데이트 시뮬레이션
  useEffect(() => {
    const interval = setInterval(() => {
      setProcessingJobs(prev => prev.map(job => {
        if (job.status === 'processing') {
          // 50% 확률로 완료 처리
          if (Math.random() > 0.5) {
            return {
              ...job,
              status: 'completed',
              processingTime: Math.random() * 5 + 1,
              accuracy: Math.random() * 10 + 90,
              result: {
                extractedText: '처리 완료된 결과...',
                confidence: Math.random() * 0.1 + 0.9
              }
            };
          }
        }
        return job;
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getModelColor = (modelId: string, opacity = '400') => {
    const model = aiModels.find(m => m.id === modelId);
    switch (model?.color) {
      case 'blue':
        return `text-blue-${opacity} border-blue-${opacity}`;
      case 'green':
        return `text-green-${opacity} border-green-${opacity}`;
      case 'purple':
        return `text-purple-${opacity} border-purple-${opacity}`;
      default:
        return `text-gray-${opacity} border-gray-${opacity}`;
    }
  };

  const getStatusColor = (status: ProcessingJob['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/20 text-green-300 border border-green-500/30';
      case 'processing':
        return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      case 'failed':
        return 'bg-red-500/20 text-red-300 border border-red-500/30';
      case 'queued':
        return 'bg-gray-500/20 text-gray-300 border border-gray-500/30';
    }
  };

  const getStatusIcon = (status: ProcessingJob['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'processing':
        return <RefreshCw className="w-4 h-4 animate-spin" />;
      case 'failed':
        return <XCircle className="w-4 h-4" />;
      case 'queued':
        return <Clock className="w-4 h-4" />;
    }
  };

  const getTypeIcon = (type: ProcessingJob['type']) => {
    switch (type) {
      case 'document':
        return <FileText className="w-4 h-4" />;
      case 'table':
        return <Table className="w-4 h-4" />;
      case 'image':
        return <Image className="w-4 h-4" />;
      case 'ocr':
        return <Eye className="w-4 h-4" />;
    }
  };

  const filteredJobs = processingJobs.filter(job => {
    const matchesModel = selectedModel === 'all' || job.model === selectedModel;
    const matchesType = selectedType === 'all' || job.type === selectedType;
    const matchesSearch = searchTerm === '' || job.title.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesModel && matchesType && matchesSearch;
  });

  const totalStats = aiModels.reduce((acc, model) => ({
    totalProcessed: acc.totalProcessed + model.stats.totalProcessed,
    totalCost: acc.totalCost + model.stats.totalCost,
    avgSuccessRate: (acc.avgSuccessRate + model.stats.successRate) / aiModels.length
  }), { totalProcessed: 0, totalCost: 0, avgSuccessRate: 0 });

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            AI 분석 시각화
          </h1>
          <p className="text-slate-400 mt-2">멀티모달 AI 모델 성능 및 처리 결과 분석</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <button className="p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-slate-300 transition-colors">
            <Download className="w-4 h-4" />
          </button>
          <button className="p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-slate-300 transition-colors">
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 전체 통계 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">총 처리량</p>
              <p className="text-2xl font-bold text-blue-300">{totalStats.totalProcessed.toLocaleString()}</p>
              <p className="text-xs text-slate-500 mt-1">
                <TrendingUp className="w-3 h-3 inline mr-1" />
                +15.3% 전일 대비
              </p>
            </div>
            <Brain className="w-8 h-8 text-blue-400" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">평균 성공률</p>
              <p className="text-2xl font-bold text-green-300">{totalStats.avgSuccessRate.toFixed(1)}%</p>
              <p className="text-xs text-slate-500 mt-1">
                <TrendingUp className="w-3 h-3 inline mr-1" />
                품질 향상
              </p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-400" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">총 비용</p>
              <p className="text-2xl font-bold text-yellow-300">${totalStats.totalCost.toFixed(2)}</p>
              <p className="text-xs text-slate-500 mt-1">
                <TrendingDown className="w-3 h-3 inline mr-1" />
                -8.5% 최적화
              </p>
            </div>
            <DollarSign className="w-8 h-8 text-yellow-400" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">처리 중</p>
              <p className="text-2xl font-bold text-purple-300">{processingJobs.filter(j => j.status === 'processing').length}</p>
              <p className="text-xs text-slate-500 mt-1">
                <RefreshCw className="w-3 h-3 inline mr-1" />
                실시간 처리
              </p>
            </div>
            <Clock className="w-8 h-8 text-purple-400" />
          </div>
        </div>
      </div>

      {/* AI 모델별 성능 비교 */}
      <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
        <h2 className="text-xl font-semibold mb-6 flex items-center">
          <Brain className="w-5 h-5 mr-2 text-blue-400" />
          AI 모델 성능 비교
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {aiModels.map((model) => (
            <motion.div
              key={model.id}
              className="p-4 bg-slate-900/30 rounded-lg border border-slate-700/50 hover:bg-slate-900/50 transition-colors"
              whileHover={{ scale: 1.02 }}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg bg-${model.color}-500/20`}>
                    {model.icon}
                  </div>
                  <div>
                    <h3 className="font-semibold text-white">{model.displayName}</h3>
                    <p className="text-xs text-slate-400">{model.name}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-slate-200">{model.stats.totalProcessed.toLocaleString()}</div>
                  <div className="text-xs text-slate-500">처리 완료</div>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-400">성공률</span>
                    <span className="text-slate-200">{model.stats.successRate}%</span>
                  </div>
                  <div className="w-full bg-slate-700/50 rounded-full h-2">
                    <div 
                      className={`bg-${model.color}-500 h-2 rounded-full transition-all duration-300`}
                      style={{ width: `${model.stats.successRate}%` }}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-slate-400">평균 처리시간</span>
                    <div className="text-white font-semibold">{model.stats.avgProcessingTime}s</div>
                  </div>
                  <div>
                    <span className="text-slate-400">총 비용</span>
                    <div className="text-white font-semibold">${model.stats.totalCost}</div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* 필터 및 검색 */}
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value as any)}
            className="px-3 py-1.5 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
          >
            <option value="all">모든 모델</option>
            <option value="gemini">Gemini Flash</option>
            <option value="gpt4o">GPT-4o</option>
            <option value="claude">Claude Sonnet</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value as any)}
            className="px-3 py-1.5 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
          >
            <option value="all">모든 타입</option>
            <option value="document">문서</option>
            <option value="table">테이블</option>
            <option value="image">이미지</option>
            <option value="ocr">OCR</option>
          </select>
        </div>

        <div className="flex-1 max-w-md relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="작업 검색..."
            className="w-full pl-10 pr-4 py-1.5 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
          />
        </div>
      </div>

      {/* 처리 작업 목록 */}
      <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold flex items-center">
            <Eye className="w-5 h-5 mr-2 text-purple-400" />
            AI 처리 작업
          </h2>
          <div className="text-sm text-slate-400">
            {filteredJobs.length}개 작업 (총 {processingJobs.length}개 중)
          </div>
        </div>

        <div className="space-y-4">
          {filteredJobs.map((job) => (
            <motion.div
              key={job.id}
              className="p-4 bg-slate-900/30 rounded-lg border border-slate-700/50 hover:bg-slate-900/50 transition-colors cursor-pointer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              whileHover={{ scale: 1.01 }}
              onClick={() => setShowDetails(showDetails === job.id ? null : job.id)}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  {getTypeIcon(job.type)}
                  <div>
                    <h3 className="font-semibold text-white">{job.title}</h3>
                    <p className="text-xs text-slate-400 truncate max-w-md">{job.sourceUrl}</p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-mono ${getModelColor(job.model).split(' ')[0]} border ${getModelColor(job.model).split(' ')[1]}`}>
                    {aiModels.find(m => m.id === job.model)?.displayName}
                  </span>
                </div>

                <div className="flex items-center space-x-3">
                  <div className={`px-3 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(job.status)}`}>
                    {getStatusIcon(job.status)}
                    <span>
                      {job.status === 'processing' ? '처리 중' : 
                       job.status === 'completed' ? '완료' :
                       job.status === 'failed' ? '실패' : '대기 중'}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500">{job.createdAt}</div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-slate-400">처리 시간:</span>
                  <div className="text-white font-semibold">
                    {job.processingTime > 0 ? `${job.processingTime.toFixed(1)}s` : '-'}
                  </div>
                </div>
                <div>
                  <span className="text-slate-400">정확도:</span>
                  <div className="text-white font-semibold">
                    {job.accuracy > 0 ? `${job.accuracy.toFixed(1)}%` : '-'}
                  </div>
                </div>
                <div>
                  <span className="text-slate-400">타입:</span>
                  <div className="text-white font-semibold capitalize">
                    {job.type === 'document' ? '문서' :
                     job.type === 'table' ? '테이블' :
                     job.type === 'image' ? '이미지' : 'OCR'}
                  </div>
                </div>
              </div>

              {/* 상세 정보 확장 */}
              <AnimatePresence>
                {showDetails === job.id && job.result && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mt-4 pt-4 border-t border-slate-700/50"
                  >
                    <h4 className="text-sm font-semibold text-slate-300 mb-2">처리 결과</h4>
                    <div className="p-3 bg-slate-800/50 rounded-lg">
                      <div className="text-xs text-slate-400 mb-2">
                        신뢰도: {((job.result.confidence || 0) * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-slate-300 font-mono">
                        {job.result.extractedText && (
                          <p>{job.result.extractedText.substring(0, 200)}...</p>
                        )}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AIAnalysis;