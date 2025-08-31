import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { 
  Database,
  Search,
  Filter,
  Download,
  Upload,
  Trash2,
  Edit,
  Eye,
  RefreshCw,
  BarChart3,
  FileText,
  Table as TableIcon,
  Image,
  CheckCircle,
  AlertTriangle,
  XCircle,
  ArrowUp,
  ArrowDown
} from 'lucide-react';

interface DataItem {
  id: string;
  title: string;
  content: string;
  sourceUrl: string;
  crawlerTier: 'httpx' | 'playwright' | 'selenium';
  dataType: 'text' | 'table' | 'image' | 'document';
  quality: 'high' | 'medium' | 'low';
  collectedAt: string;
  size: number; // bytes
  processingStatus: 'processed' | 'pending' | 'failed';
  aiAnalyzed: boolean;
  tags: string[];
  metadata: {
    wordCount?: number;
    imageCount?: number;
    tableRows?: number;
    confidence?: number;
  };
}

interface DataStats {
  totalItems: number;
  totalSize: number;
  byTier: Record<string, number>;
  byType: Record<string, number>;
  byQuality: Record<string, number>;
  processingRate: number;
}

const DataManagement: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTier, setSelectedTier] = useState<'all' | 'httpx' | 'playwright' | 'selenium'>('all');
  const [selectedType, setSelectedType] = useState<'all' | 'text' | 'table' | 'image' | 'document'>('all');
  const [selectedQuality, setSelectedQuality] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'size' | 'quality' | 'title'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [selectedItems, setSelectedItems] = useState<string[]>([]);
  const [showDetails, setShowDetails] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  const [dataItems] = useState<DataItem[]>([
    {
      id: '1',
      title: '정부포털 일반공고 - 공공기관 채용정보',
      content: '2025년 상반기 공공기관 채용계획 발표... 총 1,250명 신규 채용 예정...',
      sourceUrl: 'https://www.gov.kr/portal/ntnadmNews/1234',
      crawlerTier: 'httpx',
      dataType: 'text',
      quality: 'high',
      collectedAt: '2025-08-30 15:30:25',
      size: 15420,
      processingStatus: 'processed',
      aiAnalyzed: true,
      tags: ['정부', '채용', '공고'],
      metadata: {
        wordCount: 2340,
        confidence: 0.96
      }
    },
    {
      id: '2',
      title: '예산 현황 테이블',
      content: '2025년도 국가예산 배정 현황표',
      sourceUrl: 'https://budget.gov.kr/table/2025/allocation',
      crawlerTier: 'playwright',
      dataType: 'table',
      quality: 'high',
      collectedAt: '2025-08-30 14:45:12',
      size: 8920,
      processingStatus: 'processed',
      aiAnalyzed: true,
      tags: ['예산', '테이블', '정부'],
      metadata: {
        tableRows: 156,
        confidence: 0.94
      }
    },
    {
      id: '3',
      title: '꿈풀이 사전 - 물고기 꿈',
      content: '물고기가 나오는 꿈의 의미와 해석... 물고기는 일반적으로 재물과 행운을...',
      sourceUrl: 'https://dream.co.kr/search/fish',
      crawlerTier: 'playwright',
      dataType: 'text',
      quality: 'medium',
      collectedAt: '2025-08-30 13:20:45',
      size: 6750,
      processingStatus: 'processed',
      aiAnalyzed: false,
      tags: ['꿈풀이', '물고기', '해석'],
      metadata: {
        wordCount: 1250,
        confidence: 0.88
      }
    },
    {
      id: '4',
      title: '사주 차트 이미지',
      content: '생년월일시 기반 사주 차트 다이어그램',
      sourceUrl: 'https://saju.example.com/chart/19900315.png',
      crawlerTier: 'selenium',
      dataType: 'image',
      quality: 'medium',
      collectedAt: '2025-08-30 12:15:30',
      size: 124800,
      processingStatus: 'failed',
      aiAnalyzed: false,
      tags: ['사주', '차트', '이미지'],
      metadata: {
        imageCount: 1
      }
    },
    {
      id: '5',
      title: '운세 종합 분석 보고서',
      content: '2025년 하반기 12간지별 종합 운세 분석 및 전망 자료...',
      sourceUrl: 'https://fortune.kr/report/2025h2',
      crawlerTier: 'httpx',
      dataType: 'document',
      quality: 'high',
      collectedAt: '2025-08-30 11:30:15',
      size: 45600,
      processingStatus: 'pending',
      aiAnalyzed: false,
      tags: ['운세', '분석', '보고서'],
      metadata: {
        wordCount: 5420,
        imageCount: 12
      }
    }
  ]);

  const dataStats: DataStats = useMemo(() => {
    const stats: DataStats = {
      totalItems: dataItems.length,
      totalSize: dataItems.reduce((sum, item) => sum + item.size, 0),
      byTier: {},
      byType: {},
      byQuality: {},
      processingRate: 0
    };

    dataItems.forEach(item => {
      stats.byTier[item.crawlerTier] = (stats.byTier[item.crawlerTier] || 0) + 1;
      stats.byType[item.dataType] = (stats.byType[item.dataType] || 0) + 1;
      stats.byQuality[item.quality] = (stats.byQuality[item.quality] || 0) + 1;
    });

    stats.processingRate = (dataItems.filter(item => item.processingStatus === 'processed').length / dataItems.length) * 100;

    return stats;
  }, [dataItems]);

  const filteredAndSortedItems = useMemo(() => {
    let filtered = dataItems.filter(item => {
      const matchesSearch = searchTerm === '' || 
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesTier = selectedTier === 'all' || item.crawlerTier === selectedTier;
      const matchesType = selectedType === 'all' || item.dataType === selectedType;
      const matchesQuality = selectedQuality === 'all' || item.quality === selectedQuality;
      
      return matchesSearch && matchesTier && matchesType && matchesQuality;
    });

    filtered.sort((a, b) => {
      let aValue: any, bValue: any;
      
      switch (sortBy) {
        case 'date':
          aValue = new Date(a.collectedAt).getTime();
          bValue = new Date(b.collectedAt).getTime();
          break;
        case 'size':
          aValue = a.size;
          bValue = b.size;
          break;
        case 'quality':
          const qualityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
          aValue = qualityOrder[a.quality];
          bValue = qualityOrder[b.quality];
          break;
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        default:
          return 0;
      }
      
      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    return filtered;
  }, [dataItems, searchTerm, selectedTier, selectedType, selectedQuality, sortBy, sortOrder]);

  const paginatedItems = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredAndSortedItems.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredAndSortedItems, currentPage]);

  const totalPages = Math.ceil(filteredAndSortedItems.length / itemsPerPage);

  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'high': return 'text-green-400 bg-green-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/20';
      case 'low': return 'text-red-400 bg-red-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'processed': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'pending': return <RefreshCw className="w-4 h-4 text-yellow-400 animate-spin" />;
      case 'failed': return <XCircle className="w-4 h-4 text-red-400" />;
      default: return <AlertTriangle className="w-4 h-4 text-gray-400" />;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'text': return <FileText className="w-4 h-4" />;
      case 'table': return <TableIcon className="w-4 h-4" />;
      case 'image': return <Image className="w-4 h-4" />;
      case 'document': return <Database className="w-4 h-4" />;
      default: return <Database className="w-4 h-4" />;
    }
  };

  const handleSort = (field: typeof sortBy) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  const handleExport = (format: 'csv' | 'json' | 'excel') => {
    console.log(`Exporting ${selectedItems.length || filteredAndSortedItems.length} items as ${format}`);
    // Export logic would go here
  };

  const handleBulkAction = (action: 'delete' | 'reprocess' | 'analyze') => {
    console.log(`Bulk action: ${action} on ${selectedItems.length} items`);
    // Bulk action logic would go here
  };

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            데이터 관리
          </h1>
          <p className="text-slate-400 mt-2">수집된 데이터 검색, 분석 및 내보내기</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1">
            <button
              onClick={() => handleExport('csv')}
              className="p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-slate-300 transition-colors"
              title="CSV 내보내기"
            >
              <Download className="w-4 h-4" />
            </button>
            <button className="p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-slate-300 transition-colors">
              <Upload className="w-4 h-4" />
            </button>
          </div>
          <button className="p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-slate-300 transition-colors">
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 통계 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">총 데이터</p>
              <p className="text-2xl font-bold text-blue-300">{dataStats.totalItems.toLocaleString()}</p>
              <p className="text-xs text-slate-500 mt-1">{formatSize(dataStats.totalSize)}</p>
            </div>
            <Database className="w-8 h-8 text-blue-400" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">처리율</p>
              <p className="text-2xl font-bold text-green-300">{dataStats.processingRate.toFixed(1)}%</p>
              <p className="text-xs text-slate-500 mt-1">자동 처리</p>
            </div>
            <BarChart3 className="w-8 h-8 text-green-400" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">고품질 데이터</p>
              <p className="text-2xl font-bold text-yellow-300">{dataStats.byQuality.high || 0}</p>
              <p className="text-xs text-slate-500 mt-1">신뢰도 90% 이상</p>
            </div>
            <CheckCircle className="w-8 h-8 text-yellow-400" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">AI 분석 완료</p>
              <p className="text-2xl font-bold text-purple-300">{dataItems.filter(item => item.aiAnalyzed).length}</p>
              <p className="text-xs text-slate-500 mt-1">멀티모달 AI</p>
            </div>
            <Eye className="w-8 h-8 text-purple-400" />
          </div>
        </div>
      </div>

      {/* 필터 및 검색 */}
      <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex-1 max-w-md relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="데이터 검색 (제목, 내용, 태그)..."
              className="w-full pl-10 pr-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={selectedTier}
              onChange={(e) => setSelectedTier(e.target.value as any)}
              className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="all">모든 Tier</option>
              <option value="httpx">Tier 1 (httpx)</option>
              <option value="playwright">Tier 2 (Playwright)</option>
              <option value="selenium">Tier 3 (Selenium)</option>
            </select>
          </div>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value as any)}
            className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
          >
            <option value="all">모든 타입</option>
            <option value="text">텍스트</option>
            <option value="table">테이블</option>
            <option value="image">이미지</option>
            <option value="document">문서</option>
          </select>

          <select
            value={selectedQuality}
            onChange={(e) => setSelectedQuality(e.target.value as any)}
            className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
          >
            <option value="all">모든 품질</option>
            <option value="high">높음</option>
            <option value="medium">보통</option>
            <option value="low">낮음</option>
          </select>
        </div>

        {/* 선택된 항목 액션 */}
        {selectedItems.length > 0 && (
          <div className="mt-4 flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
            <span className="text-sm text-slate-300">{selectedItems.length}개 항목 선택됨</span>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleBulkAction('analyze')}
                className="px-3 py-1 bg-blue-500/20 text-blue-300 rounded transition-colors hover:bg-blue-500/30 text-sm"
              >
                AI 분석
              </button>
              <button
                onClick={() => handleBulkAction('reprocess')}
                className="px-3 py-1 bg-yellow-500/20 text-yellow-300 rounded transition-colors hover:bg-yellow-500/30 text-sm"
              >
                재처리
              </button>
              <button
                onClick={() => handleBulkAction('delete')}
                className="px-3 py-1 bg-red-500/20 text-red-300 rounded transition-colors hover:bg-red-500/30 text-sm"
              >
                삭제
              </button>
            </div>
          </div>
        )}
      </div>

      {/* 데이터 테이블 */}
      <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl border border-slate-600/50 overflow-hidden">
        <div className="p-6 pb-0">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center">
              <Database className="w-5 h-5 mr-2 text-blue-400" />
              데이터 목록
            </h2>
            <div className="text-sm text-slate-400">
              {filteredAndSortedItems.length}개 중 {paginatedItems.length}개 표시
            </div>
          </div>
        </div>

        {/* 테이블 헤더 */}
        <div className="px-6 py-3 bg-slate-900/20 border-b border-slate-700/50 grid grid-cols-12 gap-4 text-sm font-medium text-slate-400">
          <div className="col-span-1">
            <input
              type="checkbox"
              checked={selectedItems.length === paginatedItems.length && paginatedItems.length > 0}
              onChange={(e) => {
                if (e.target.checked) {
                  setSelectedItems(paginatedItems.map(item => item.id));
                } else {
                  setSelectedItems([]);
                }
              }}
              className="rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500"
            />
          </div>
          <div className="col-span-4">
            <button
              onClick={() => handleSort('title')}
              className="flex items-center space-x-1 hover:text-slate-200 transition-colors"
            >
              <span>제목</span>
              {sortBy === 'title' && (
                sortOrder === 'asc' ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />
              )}
            </button>
          </div>
          <div className="col-span-1">타입</div>
          <div className="col-span-1">품질</div>
          <div className="col-span-1">
            <button
              onClick={() => handleSort('size')}
              className="flex items-center space-x-1 hover:text-slate-200 transition-colors"
            >
              <span>크기</span>
              {sortBy === 'size' && (
                sortOrder === 'asc' ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />
              )}
            </button>
          </div>
          <div className="col-span-1">상태</div>
          <div className="col-span-2">
            <button
              onClick={() => handleSort('date')}
              className="flex items-center space-x-1 hover:text-slate-200 transition-colors"
            >
              <span>수집일시</span>
              {sortBy === 'date' && (
                sortOrder === 'asc' ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />
              )}
            </button>
          </div>
          <div className="col-span-1">액션</div>
        </div>

        {/* 테이블 본문 */}
        <div className="max-h-96 overflow-y-auto">
          {paginatedItems.map((item) => (
            <motion.div
              key={item.id}
              className="px-6 py-3 border-b border-slate-700/30 hover:bg-slate-700/20 transition-colors grid grid-cols-12 gap-4 text-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="col-span-1 flex items-center">
                <input
                  type="checkbox"
                  checked={selectedItems.includes(item.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedItems([...selectedItems, item.id]);
                    } else {
                      setSelectedItems(selectedItems.filter(id => id !== item.id));
                    }
                  }}
                  className="rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500"
                />
              </div>
              <div className="col-span-4 flex items-center">
                <div>
                  <div className="font-medium text-white truncate">{item.title}</div>
                  <div className="text-xs text-slate-400 truncate">{item.sourceUrl}</div>
                  <div className="flex items-center space-x-1 mt-1">
                    {item.tags.map((tag) => (
                      <span key={tag} className="px-1.5 py-0.5 bg-slate-600/30 text-slate-300 rounded text-xs">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              <div className="col-span-1 flex items-center">
                <div className="flex items-center space-x-1">
                  {getTypeIcon(item.dataType)}
                  <span className="text-slate-300 capitalize">{item.dataType}</span>
                </div>
              </div>
              <div className="col-span-1 flex items-center">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getQualityColor(item.quality)}`}>
                  {item.quality === 'high' ? '높음' : item.quality === 'medium' ? '보통' : '낮음'}
                </span>
              </div>
              <div className="col-span-1 flex items-center">
                <span className="text-slate-300">{formatSize(item.size)}</span>
              </div>
              <div className="col-span-1 flex items-center">
                <div className="flex items-center space-x-1">
                  {getStatusIcon(item.processingStatus)}
                  <span className="text-slate-300 text-xs">
                    {item.processingStatus === 'processed' ? '완료' : 
                     item.processingStatus === 'pending' ? '대기' : '실패'}
                  </span>
                </div>
              </div>
              <div className="col-span-2 flex items-center">
                <span className="text-slate-300 text-xs">{new Date(item.collectedAt).toLocaleString('ko-KR')}</span>
              </div>
              <div className="col-span-1 flex items-center space-x-1">
                <button
                  onClick={() => setShowDetails(showDetails === item.id ? null : item.id)}
                  className="p-1 text-slate-400 hover:text-white hover:bg-slate-700 rounded transition-colors"
                  title="자세히 보기"
                >
                  <Eye className="w-4 h-4" />
                </button>
                <button
                  className="p-1 text-slate-400 hover:text-white hover:bg-slate-700 rounded transition-colors"
                  title="편집"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  className="p-1 text-slate-400 hover:text-red-400 hover:bg-red-500/20 rounded transition-colors"
                  title="삭제"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* 페이지네이션 */}
        {totalPages > 1 && (
          <div className="px-6 py-4 bg-slate-900/20 border-t border-slate-700/50 flex items-center justify-between">
            <div className="text-sm text-slate-400">
              페이지 {currentPage} / {totalPages}
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-600 transition-colors"
              >
                이전
              </button>
              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-600 transition-colors"
              >
                다음
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataManagement;