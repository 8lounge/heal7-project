import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors, DragEndEvent } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import CrawlingLayout from './CrawlingLayout';
import CrawlingManagement from './CrawlingManagement';
import AIAnalysis from './AIAnalysis';
import DataManagement from './DataManagement';
import CrawlerToolSelector from './CrawlerToolSelector';
import { safeAPICall, useErrorHandler, ErrorContext } from '../../utils/ErrorHandler';
import { 
  Activity, 
  Clock, 
  Database, 
  Zap, 
  AlertCircle, 
  CheckCircle,
  Pause,
  Play,
  Square,
  TrendingUp,
  Server,
  Brain,
  Eye,
  Download,
  GripVertical,
  Settings,
  Maximize2,
  Minimize2,
  BarChart3,
  Volume2,
  Bell,
  Wifi,
  RefreshCw
} from 'lucide-react';

interface CrawlerStatus {
  id: string;
  name: string;
  type: 'httpx' | 'httpx_bs' | 'playwright';
  status: 'idle' | 'running' | 'paused' | 'error';
  progress: number;
  itemsCollected: number;
  speed: number;
  lastUpdate: string;
}

interface AIStats {
  totalProcessed: number;
  geminiFlash: number;
  gpt4o: number;
  claudeSonnet: number;
  successRate: number;
}

interface MonitoringData {
  timestamp: string;
  cpu: number;
  memory: number;
  network: number;
  requests: number;
  errors: number;
}

interface SystemSettings {
  autoRefresh: boolean;
  notifications: boolean;
  soundAlerts: boolean;
  realTimeUpdates: boolean;
  darkMode: boolean;
  refreshInterval: number;
  maxRetries: number;
  timeout: number;
}

type CrawlingPage = 'dashboard' | 'crawling' | 'ai-analysis' | 'data-management' | 'tool-selector' | 'settings';

interface DashboardWidget {
  id: string;
  type: 'kpi' | 'crawler-status' | 'ai-stats' | 'monitoring' | 'settings';
  title: string;
  size: 'small' | 'medium' | 'large';
  position: { x: number; y: number };
  minimized: boolean;
  data?: any;
}

interface DynamicTheme {
  name: string;
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  glass: string;
  border: string;
}

// 유리반투명 컴포넌트
const GlassBox: React.FC<{
  children: React.ReactNode;
  className?: string;
  theme?: DynamicTheme;
  isDraggable?: boolean;
  dragId?: string;
}> = ({ children, className = '', theme, isDraggable = false, dragId }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: dragId || 'default' });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.8 : 1,
  };

  const themeColors = theme || {
    background: 'from-slate-900/30 via-slate-800/20 to-slate-900/30',
    border: 'border-slate-600/30',
    glass: 'backdrop-blur-xl'
  };

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      {...(isDraggable ? attributes : {})}
      className={`
        relative bg-gradient-to-br ${themeColors.background}
        ${themeColors.glass} ${themeColors.border} border
        rounded-2xl overflow-hidden
        shadow-2xl shadow-black/20
        hover:shadow-3xl hover:shadow-black/30
        transition-all duration-300
        before:absolute before:inset-0 before:bg-gradient-to-br 
        before:from-white/5 before:via-transparent before:to-transparent
        before:rounded-2xl before:pointer-events-none
        after:absolute after:inset-px after:bg-gradient-to-br
        after:from-transparent after:via-white/5 after:to-transparent
        after:rounded-2xl after:pointer-events-none
        ${className}
      `}
      whileHover={{ 
        scale: 1.01,
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.4)'
      }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      {isDraggable && (
        <div 
          {...listeners}
          className="absolute top-2 right-2 p-1 opacity-0 hover:opacity-100 transition-opacity cursor-grab active:cursor-grabbing z-10"
        >
          <GripVertical className="w-4 h-4 text-slate-400" />
        </div>
      )}
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
};

// 실시간 모니터링 차트 컴포넌트
const MonitoringChart: React.FC<{ data: MonitoringData[], type: 'cpu' | 'memory' | 'network' | 'requests' }> = ({ 
  data, type
}) => {
  const getColor = () => {
    switch (type) {
      case 'cpu': return 'rgb(34, 197, 94)';
      case 'memory': return 'rgb(59, 130, 246)';
      case 'network': return 'rgb(168, 85, 247)';
      case 'requests': return 'rgb(249, 115, 22)';
      default: return 'rgb(156, 163, 175)';
    }
  };

  const maxValue = Math.max(...data.map(d => {
    switch (type) {
      case 'cpu': return d.cpu;
      case 'memory': return d.memory;
      case 'network': return d.network;
      case 'requests': return d.requests;
      default: return 0;
    }
  }));

  return (
    <div className="h-32 w-full relative">
      <svg viewBox="0 0 300 100" className="w-full h-full">
        <defs>
          <linearGradient id={`gradient-${type}`} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={getColor()} stopOpacity={0.3} />
            <stop offset="100%" stopColor={getColor()} stopOpacity={0} />
          </linearGradient>
        </defs>
        
        {/* 그리드 선 */}
        {[0, 25, 50, 75, 100].map(y => (
          <line 
            key={y}
            x1="0" 
            y1={y} 
            x2="300" 
            y2={y} 
            stroke="rgb(71, 85, 105)" 
            strokeOpacity={0.2}
            strokeWidth="1"
          />
        ))}
        
        {/* 데이터 라인 */}
        <motion.path
          d={`M ${data.map((d, i) => {
            const x = (i / (data.length - 1)) * 300;
            const value = type === 'cpu' ? d.cpu : type === 'memory' ? d.memory : type === 'network' ? d.network : d.requests;
            const y = 100 - (value / maxValue) * 100;
            return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
          }).join(' ')}`}
          fill="none"
          stroke={getColor()}
          strokeWidth="2"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, ease: "easeInOut" }}
        />
        
        {/* 영역 채우기 */}
        <motion.path
          d={`M ${data.map((d, i) => {
            const x = (i / (data.length - 1)) * 300;
            const value = type === 'cpu' ? d.cpu : type === 'memory' ? d.memory : type === 'network' ? d.network : d.requests;
            const y = 100 - (value / maxValue) * 100;
            return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
          }).join(' ')} L 300 100 L 0 100 Z`}
          fill={`url(#gradient-${type})`}
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, ease: "easeInOut" }}
        />
      </svg>
    </div>
  );
};

// 설정 토글 컴포넌트
const SettingsToggle: React.FC<{
  label: string;
  enabled: boolean;
  onChange: (enabled: boolean) => void;
  icon?: React.ReactNode;
}> = ({ label, enabled, onChange, icon }) => {
  return (
    <div className="flex items-center justify-between p-3 rounded-lg bg-slate-800/30 hover:bg-slate-700/30 transition-colors">
      <div className="flex items-center space-x-3">
        {icon}
        <span className="text-sm text-slate-300">{label}</span>
      </div>
      <motion.button
        onClick={() => onChange(!enabled)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          enabled ? 'bg-blue-500' : 'bg-slate-600'
        }`}
        whileTap={{ scale: 0.95 }}
      >
        <motion.span
          className="inline-block h-4 w-4 transform rounded-full bg-white shadow-lg transition-transform"
          animate={{ x: enabled ? 6 : 2 }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
        />
      </motion.button>
    </div>
  );
};

const CrawlingDashboard: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<CrawlingPage>('dashboard');
  const [currentTheme, setCurrentTheme] = useState<DynamicTheme>({
    name: 'aurora',
    primary: 'from-purple-400 via-pink-400 to-red-400',
    secondary: 'from-blue-400 via-purple-400 to-pink-400', 
    accent: 'from-cyan-400 via-blue-400 to-purple-400',
    background: 'from-slate-900/40 via-slate-800/30 to-slate-900/40',
    glass: 'backdrop-blur-xl',
    border: 'border-slate-600/30'
  });
  
  const [widgets, setWidgets] = useState<DashboardWidget[]>([
    { id: '1', type: 'kpi', title: 'KPI 카드들', size: 'large', position: { x: 0, y: 0 }, minimized: false },
    { id: '2', type: 'crawler-status', title: '크롤러 현황', size: 'large', position: { x: 1, y: 0 }, minimized: false },
    { id: '3', type: 'ai-stats', title: 'AI 분석', size: 'medium', position: { x: 2, y: 0 }, minimized: false },
    { id: '4', type: 'monitoring', title: '시스템 모니터링', size: 'large', position: { x: 0, y: 1 }, minimized: false },
    { id: '5', type: 'settings', title: '시스템 설정', size: 'medium', position: { x: 1, y: 1 }, minimized: false }
  ]);

  const [settings, setSettings] = useState<SystemSettings>({
    autoRefresh: true,
    notifications: true,
    soundAlerts: false,
    realTimeUpdates: true,
    darkMode: true,
    refreshInterval: 3000,
    maxRetries: 3,
    timeout: 30000
  });

  const [monitoringData, setMonitoringData] = useState<MonitoringData[]>([]);
  
  const themes: DynamicTheme[] = [
    {
      name: 'aurora',
      primary: 'from-purple-400 via-pink-400 to-red-400',
      secondary: 'from-blue-400 via-purple-400 to-pink-400',
      accent: 'from-cyan-400 via-blue-400 to-purple-400',
      background: 'from-slate-900/40 via-slate-800/30 to-slate-900/40',
      glass: 'backdrop-blur-xl',
      border: 'border-slate-600/30'
    },
    {
      name: 'ocean',
      primary: 'from-blue-400 via-cyan-400 to-teal-400',
      secondary: 'from-indigo-400 via-blue-400 to-cyan-400',
      accent: 'from-teal-400 via-cyan-400 to-blue-400',
      background: 'from-slate-900/40 via-blue-900/20 to-slate-900/40',
      glass: 'backdrop-blur-xl',
      border: 'border-blue-600/30'
    },
    {
      name: 'forest',
      primary: 'from-green-400 via-emerald-400 to-teal-400',
      secondary: 'from-lime-400 via-green-400 to-emerald-400',
      accent: 'from-emerald-400 via-teal-400 to-cyan-400',
      background: 'from-slate-900/40 via-green-900/20 to-slate-900/40',
      glass: 'backdrop-blur-xl',
      border: 'border-green-600/30'
    },
    {
      name: 'sunset',
      primary: 'from-orange-400 via-red-400 to-pink-400',
      secondary: 'from-yellow-400 via-orange-400 to-red-400',
      accent: 'from-red-400 via-pink-400 to-purple-400',
      background: 'from-slate-900/40 via-orange-900/20 to-slate-900/40',
      glass: 'backdrop-blur-xl',
      border: 'border-orange-600/30'
    }
  ];
  
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );
  
  const [crawlers, setCrawlers] = useState<CrawlerStatus[]>([]);

  const [aiStats, setAiStats] = useState<AIStats>({
    totalProcessed: 0,
    geminiFlash: 0,
    gpt4o: 0,
    claudeSonnet: 0,
    successRate: 0
  });

  const { handleError, safeAPICall: safeFetch } = useErrorHandler();

  // API 기반 데이터 로딩 (에러 처리 포함)
  useEffect(() => {
    const loadInitialData = async () => {
      const context: ErrorContext = {
        component: 'CrawlingDashboard',
        action: 'loadInitialData'
      };

      // 크롤러 상태 로드
      const { data: crawlersData, error: crawlersError } = await safeFetch(
        '/api/crawlers/status', 
        {}, 
        { ...context, action: 'loadCrawlers' }
      );
      
      if (crawlersData) {
        setCrawlers(Array.isArray(crawlersData) ? crawlersData : []);
      } else if (crawlersError) {
        console.error('크롤러 상태 로드 실패:', crawlersError.message);
      }

      // AI 통계 로드
      const { data: aiStatsData, error: aiStatsError } = await safeFetch(
        '/api/ai/stats', 
        {}, 
        { ...context, action: 'loadAIStats' }
      );
      
      if (aiStatsData && typeof aiStatsData === 'object') {
        setAiStats({
          totalProcessed: aiStatsData.totalProcessed || 0,
          geminiFlash: aiStatsData.geminiFlash || 0,
          gpt4o: aiStatsData.gpt4o || 0,
          claudeSonnet: aiStatsData.claudeSonnet || 0,
          successRate: aiStatsData.successRate || 0
        });
      } else if (aiStatsError) {
        console.error('AI 통계 로드 실패:', aiStatsError.message);
      }

      // 모니터링 데이터 로드
      const { data: monitoringData, error: monitoringError } = await safeFetch(
        '/api/system/monitoring?limit=12', 
        {}, 
        { ...context, action: 'loadMonitoring' }
      );
      
      if (monitoringData) {
        setMonitoringData(Array.isArray(monitoringData) ? monitoringData : []);
      } else if (monitoringError) {
        console.error('모니터링 데이터 로드 실패:', monitoringError.message);
      }
    };

    loadInitialData();

    // 정기적인 데이터 업데이트 (WebSocket 폴백)
    if (settings.realTimeUpdates) {
      const interval = setInterval(() => {
        loadInitialData();
      }, settings.refreshInterval * 2);

      return () => clearInterval(interval);
    }
  }, [settings.realTimeUpdates, settings.refreshInterval, safeFetch]);

  const handleDragEnd = useCallback((event: DragEndEvent) => {
    const { active, over } = event;
    
    if (over && active.id !== over.id) {
      setWidgets((widgets) => {
        const oldIndex = widgets.findIndex(widget => widget.id === active.id);
        const newIndex = widgets.findIndex(widget => widget.id === over.id);
        
        return arrayMove(widgets, oldIndex, newIndex);
      });
    }
  }, []);
  
  const toggleWidget = useCallback((widgetId: string) => {
    setWidgets(prev => prev.map(widget => 
      widget.id === widgetId 
        ? { ...widget, minimized: !widget.minimized }
        : widget
    ));
  }, []);

  const updateSetting = useCallback((key: keyof SystemSettings, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Play className="w-4 h-4 text-green-400" />;
      case 'paused':
        return <Pause className="w-4 h-4 text-yellow-400" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Square className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'border-green-400/50 bg-green-400/10';
      case 'paused':
        return 'border-yellow-400/50 bg-yellow-400/10';
      case 'error':
        return 'border-red-400/50 bg-red-400/10';
      default:
        return 'border-gray-400/50 bg-gray-400/10';
    }
  };

  const getTierBadgeColor = (type: string) => {
    switch (type) {
      case 'httpx':
        return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      case 'playwright':
        return 'bg-purple-500/20 text-purple-300 border border-purple-500/30';
      case 'httpx_bs':
        return 'bg-orange-500/20 text-orange-300 border border-orange-500/30';
      default:
        return 'bg-gray-500/20 text-gray-300 border border-gray-500/30';
    }
  };

  const getTierDisplayName = (type: string) => {
    switch (type) {
      case 'httpx':
        return 'HTTPX';
      case 'playwright':
        return 'PLAYWRIGHT';
      case 'httpx_bs':
        return 'HTTPX+BS';
      default:
        return type.toUpperCase();
    }
  };

  const renderDashboardContent = () => (
    <div className="space-y-6">
      {/* 헤더 with 테마 선택기 */}
      <motion.div 
        className="flex justify-between items-start"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div>
          <h1 className={`text-3xl font-bold bg-gradient-to-r ${currentTheme.primary} bg-clip-text text-transparent`}>
            시스템 개요
          </h1>
          <p className="text-slate-400 mt-2">3-Tier 크롤링 시스템 & 멀티모달 AI 분석 현황</p>
        </div>
        
        <GlassBox theme={currentTheme} className="p-3">
          <div className="flex items-center space-x-2">
            <Settings className="w-4 h-4 text-slate-400" />
            <select 
              value={currentTheme.name}
              onChange={(e) => setCurrentTheme(themes.find(t => t.name === e.target.value) || themes[0])}
              className="bg-transparent text-slate-300 text-sm focus:outline-none cursor-pointer"
            >
              {themes.map(theme => (
                <option key={theme.name} value={theme.name} className="bg-slate-800">
                  {theme.name.charAt(0).toUpperCase() + theme.name.slice(1)}
                </option>
              ))}
            </select>
          </div>
        </GlassBox>
      </motion.div>

      {/* 드래그 가능한 위젯들 */}
      <DndContext 
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext 
          items={widgets.map(w => w.id)}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-6">
            {/* KPI 카드 위젯 */}
            <GlassBox 
              theme={currentTheme}
              isDraggable
              dragId={widgets[0]?.id}
              className={widgets[0]?.minimized ? 'h-16' : ''}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className={`text-lg font-semibold bg-gradient-to-r ${currentTheme.secondary} bg-clip-text text-transparent`}>
                    핵심 지표
                  </h2>
                  <motion.button
                    onClick={() => toggleWidget(widgets[0]?.id)}
                    className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    {widgets[0]?.minimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                  </motion.button>
                </div>
                
                <AnimatePresence>
                  {!widgets[0]?.minimized && (
                    <motion.div 
                      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <motion.div 
                        className={`bg-gradient-to-br ${currentTheme.background} ${currentTheme.glass} rounded-xl p-6 border ${currentTheme.border}`}
                        whileHover={{ scale: 1.02, rotate: 1 }}
                        transition={{ type: "spring", stiffness: 300 }}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-slate-400 text-sm">총 수집 데이터</p>
                            <p className="text-2xl font-bold text-blue-300">{crawlers.reduce((sum, c) => sum + c.itemsCollected, 0).toLocaleString()}</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <TrendingUp className="w-3 h-3 inline mr-1" />
                              +12.3% 전일 대비
                            </p>
                          </div>
                          <Database className="w-8 h-8 text-blue-400" />
                        </div>
                      </motion.div>

                      <motion.div 
                        className={`bg-gradient-to-br ${currentTheme.background} ${currentTheme.glass} rounded-xl p-6 border ${currentTheme.border}`}
                        whileHover={{ scale: 1.02, rotate: -1 }}
                        transition={{ type: "spring", stiffness: 300 }}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-slate-400 text-sm">활성 크롤러</p>
                            <p className="text-2xl font-bold text-green-300">{crawlers.filter(c => c.status === 'running').length}</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <Server className="w-3 h-3 inline mr-1" />
                              총 {crawlers.length}개 중
                            </p>
                          </div>
                          <Activity className="w-8 h-8 text-green-400" />
                        </div>
                      </motion.div>

                      <motion.div 
                        className={`bg-gradient-to-br ${currentTheme.background} ${currentTheme.glass} rounded-xl p-6 border ${currentTheme.border}`}
                        whileHover={{ scale: 1.02, rotate: 0.5 }}
                        transition={{ type: "spring", stiffness: 300 }}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-slate-400 text-sm">AI 처리율</p>
                            <p className="text-2xl font-bold text-yellow-300">{aiStats.successRate.toFixed(1)}%</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <Brain className="w-3 h-3 inline mr-1" />
                              실시간 모니터링
                            </p>
                          </div>
                          <Zap className="w-8 h-8 text-yellow-400" />
                        </div>
                      </motion.div>

                      <motion.div 
                        className={`bg-gradient-to-br ${currentTheme.background} ${currentTheme.glass} rounded-xl p-6 border ${currentTheme.border}`}
                        whileHover={{ scale: 1.02, rotate: -0.5 }}
                        transition={{ type: "spring", stiffness: 300 }}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-slate-400 text-sm">AI 총 처리</p>
                            <p className="text-2xl font-bold text-purple-300">{aiStats.totalProcessed.toLocaleString()}</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <Eye className="w-3 h-3 inline mr-1" />
                              멀티모달 분석
                            </p>
                          </div>
                          <CheckCircle className="w-8 h-8 text-purple-400" />
                        </div>
                      </motion.div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </GlassBox>

            {/* 시스템 모니터링 위젯 */}
            <GlassBox 
              theme={currentTheme}
              isDraggable
              dragId={widgets[3]?.id}
              className={widgets[3]?.minimized ? 'h-16' : ''}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className={`text-xl font-semibold flex items-center bg-gradient-to-r ${currentTheme.accent} bg-clip-text text-transparent`}>
                    <BarChart3 className="w-5 h-5 mr-2 text-blue-400" />
                    실시간 시스템 모니터링
                  </h2>
                  <div className="flex items-center space-x-2">
                    <motion.button
                      onClick={() => toggleWidget(widgets[3]?.id)}
                      className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      {widgets[3]?.minimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                    </motion.button>
                    <motion.button
                      className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
                      whileHover={{ scale: 1.1, rotate: 180 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => {
                        setMonitoringData(prev => [...prev.slice(1), {
                          timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
                          cpu: Math.floor(Math.random() * 40) + 40,
                          memory: Math.floor(Math.random() * 30) + 60,
                          network: Math.floor(Math.random() * 40) + 20,
                          requests: Math.floor(Math.random() * 50) + 100,
                          errors: Math.floor(Math.random() * 5)
                        }]);
                      }}
                    >
                      <RefreshCw className="w-4 h-4" />
                    </motion.button>
                  </div>
                </div>
                
                <AnimatePresence>
                  {!widgets[3]?.minimized && (
                    <motion.div 
                      className="grid grid-cols-1 md:grid-cols-2 gap-6"
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <div className="space-y-4">
                        <div className={`p-4 rounded-xl bg-gradient-to-br ${currentTheme.background} border ${currentTheme.border}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-slate-300">CPU 사용률</span>
                            <span className="text-lg font-bold text-green-400">{monitoringData[monitoringData.length - 1]?.cpu}%</span>
                          </div>
                          <MonitoringChart data={monitoringData} type="cpu" />
                        </div>
                        
                        <div className={`p-4 rounded-xl bg-gradient-to-br ${currentTheme.background} border ${currentTheme.border}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-slate-300">메모리 사용률</span>
                            <span className="text-lg font-bold text-blue-400">{monitoringData[monitoringData.length - 1]?.memory}%</span>
                          </div>
                          <MonitoringChart data={monitoringData} type="memory" />
                        </div>
                      </div>
                      
                      <div className="space-y-4">
                        <div className={`p-4 rounded-xl bg-gradient-to-br ${currentTheme.background} border ${currentTheme.border}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-slate-300">네트워크 I/O</span>
                            <span className="text-lg font-bold text-purple-400">{monitoringData[monitoringData.length - 1]?.network} MB/s</span>
                          </div>
                          <MonitoringChart data={monitoringData} type="network" />
                        </div>
                        
                        <div className={`p-4 rounded-xl bg-gradient-to-br ${currentTheme.background} border ${currentTheme.border}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-slate-300">요청/분</span>
                            <span className="text-lg font-bold text-orange-400">{monitoringData[monitoringData.length - 1]?.requests}</span>
                          </div>
                          <MonitoringChart data={monitoringData} type="requests" />
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </GlassBox>

            {/* 시스템 설정 위젯 */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              <GlassBox 
                theme={currentTheme}
                isDraggable
                dragId={widgets[4]?.id}
                className={`xl:col-span-1 ${widgets[4]?.minimized ? 'h-16' : ''}`}
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className={`text-xl font-semibold flex items-center bg-gradient-to-r ${currentTheme.primary} bg-clip-text text-transparent`}>
                      <Settings className="w-5 h-5 mr-2 text-slate-400" />
                      시스템 설정
                    </h2>
                    <motion.button
                      onClick={() => toggleWidget(widgets[4]?.id)}
                      className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      {widgets[4]?.minimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                    </motion.button>
                  </div>
                  
                  <AnimatePresence>
                    {!widgets[4]?.minimized && (
                      <motion.div 
                        className="space-y-3"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        <SettingsToggle
                          label="자동 새로고침"
                          enabled={settings.autoRefresh}
                          onChange={(enabled) => updateSetting('autoRefresh', enabled)}
                          icon={<RefreshCw className="w-4 h-4 text-slate-400" />}
                        />
                        
                        <SettingsToggle
                          label="실시간 업데이트"
                          enabled={settings.realTimeUpdates}
                          onChange={(enabled) => updateSetting('realTimeUpdates', enabled)}
                          icon={<Wifi className="w-4 h-4 text-slate-400" />}
                        />
                        
                        <SettingsToggle
                          label="알림"
                          enabled={settings.notifications}
                          onChange={(enabled) => updateSetting('notifications', enabled)}
                          icon={<Bell className="w-4 h-4 text-slate-400" />}
                        />
                        
                        <SettingsToggle
                          label="소리 알림"
                          enabled={settings.soundAlerts}
                          onChange={(enabled) => updateSetting('soundAlerts', enabled)}
                          icon={<Volume2 className="w-4 h-4 text-slate-400" />}
                        />

                        <div className="pt-4 border-t border-slate-700/50">
                          <div className="space-y-3">
                            <div>
                              <label className="block text-sm text-slate-400 mb-2">새로고침 간격</label>
                              <select 
                                value={settings.refreshInterval}
                                onChange={(e) => updateSetting('refreshInterval', parseInt(e.target.value))}
                                className="w-full bg-slate-800/50 border border-slate-600/50 rounded-lg px-3 py-2 text-slate-300 text-sm focus:outline-none focus:border-blue-500/50"
                              >
                                <option value={1000}>1초</option>
                                <option value={3000}>3초</option>
                                <option value={5000}>5초</option>
                                <option value={10000}>10초</option>
                              </select>
                            </div>
                            
                            <div>
                              <label className="block text-sm text-slate-400 mb-2">최대 재시도</label>
                              <select 
                                value={settings.maxRetries}
                                onChange={(e) => updateSetting('maxRetries', parseInt(e.target.value))}
                                className="w-full bg-slate-800/50 border border-slate-600/50 rounded-lg px-3 py-2 text-slate-300 text-sm focus:outline-none focus:border-blue-500/50"
                              >
                                <option value={1}>1회</option>
                                <option value={3}>3회</option>
                                <option value={5}>5회</option>
                                <option value={10}>10회</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </GlassBox>

              {/* 3-Tier 크롤러 상태 위젯 */}
              <GlassBox 
                theme={currentTheme}
                isDraggable
                dragId={widgets[1]?.id}
                className={`xl:col-span-2 ${widgets[1]?.minimized ? 'h-16' : ''}`}
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className={`text-xl font-semibold flex items-center bg-gradient-to-r ${currentTheme.secondary} bg-clip-text text-transparent`}>
                      <Activity className="w-5 h-5 mr-2 text-green-400" />
                      3-Tier 상태
                    </h2>
                    <div className="flex items-center space-x-2">
                      <motion.button
                        onClick={() => toggleWidget(widgets[1]?.id)}
                        className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        {widgets[1]?.minimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                      </motion.button>
                      <motion.button
                        className={`px-3 py-1 bg-gradient-to-r ${currentTheme.background} hover:bg-slate-600/50 rounded-lg text-sm text-slate-300 transition-colors border ${currentTheme.border}`}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setCurrentPage('crawling')}
                      >
                        <Download className="w-4 h-4 inline mr-1" />
                        자세히 보기
                      </motion.button>
                    </div>
                  </div>
                  
                  <AnimatePresence>
                    {!widgets[1]?.minimized && (
                      <motion.div 
                        className="space-y-4"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        {crawlers.map((crawler) => (
                          <div key={crawler.id} className={`p-4 rounded-lg border ${getStatusColor(crawler.status)} hover:bg-slate-700/20 transition-colors`}>
                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center space-x-3">
                                {getStatusIcon(crawler.status)}
                                <span className="font-medium">{crawler.name}</span>
                                <span className={`px-2 py-1 rounded-full text-xs font-mono ${getTierBadgeColor(crawler.type)}`}>
                                  {getTierDisplayName(crawler.type)}
                                </span>
                              </div>
                              <div className="text-right">
                                <div className="text-sm font-semibold text-slate-200">{crawler.itemsCollected.toLocaleString()}</div>
                                <div className="text-xs text-slate-500">{crawler.speed}/min</div>
                              </div>
                            </div>
                            
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex-1 mr-4">
                                <div className="w-full bg-slate-700/50 rounded-full h-2">
                                  <motion.div 
                                    className={`bg-gradient-to-r ${currentTheme.accent} h-2 rounded-full transition-all duration-300`}
                                    initial={{ width: 0 }}
                                    animate={{ width: `${crawler.progress}%` }}
                                    transition={{ duration: 1.5, ease: "easeInOut" }}
                                  />
                                </div>
                              </div>
                              <div className="text-sm font-mono">
                                <span className="text-slate-300">{crawler.progress.toFixed(1)}%</span>
                              </div>
                            </div>
                            
                            <div className="flex items-center justify-between text-xs text-slate-500">
                              <div className="flex items-center">
                                <Clock className="w-3 h-3 mr-1" />
                                마지막 업데이트: {crawler.lastUpdate}
                              </div>
                              <div className={`px-2 py-1 rounded-full ${
                                crawler.status === 'running' ? 'bg-green-400/20 text-green-300' : 
                                crawler.status === 'error' ? 'bg-red-400/20 text-red-300' : 
                                'bg-yellow-400/20 text-yellow-300'
                              }`}>
                                {crawler.status === 'running' ? '실행 중' : 
                                 crawler.status === 'error' ? '오류' : '일시정지'}
                              </div>
                            </div>
                          </div>
                        ))}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </GlassBox>
            </div>
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );

  const renderPageContent = () => {
    switch (currentPage) {
      case 'dashboard':
        return renderDashboardContent();
      case 'crawling':
        return <CrawlingManagement />;
      case 'ai-analysis':
        return <AIAnalysis />;
      case 'data-management':
        return <DataManagement />;
      case 'tool-selector':
        return <CrawlerToolSelector />;
      case 'settings':
        return <div className="text-center py-20 text-slate-400">설정 페이지 (개발 중)</div>;
      default:
        return renderDashboardContent();
    }
  };

  return (
    <CrawlingLayout currentPage={currentPage} onPageChange={setCurrentPage}>
      {renderPageContent()}
    </CrawlingLayout>
  );
};

export default CrawlingDashboard;