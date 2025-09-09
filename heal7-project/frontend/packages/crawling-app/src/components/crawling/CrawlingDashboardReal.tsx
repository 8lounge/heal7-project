/**
 * 🔍 실제 백엔드 연동 크롤링 대시보드
 * - 하드코딩 제거, 실제 API 연동
 * - 실시간 WebSocket 업데이트
 */

import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors, DragEndEvent } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useRealTimeCrawling } from '../../hooks/useRealTimeCrawling';
import CrawlingLayout from './CrawlingLayout';
import CrawlingManagement from './CrawlingManagement';
import AIAnalysis from './AIAnalysis';
import DataManagement from './DataManagement';
import SettingsPage from './SettingsPage';
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
  Eye,
  GripVertical,
  Settings,
  Maximize2,
  Minimize2,
  Bell,
  Wifi,
  RefreshCw,
  WifiOff
} from 'lucide-react';

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

// 연결 상태 표시기
const ConnectionStatus: React.FC<{ 
  isConnected: boolean; 
  isHealthy: boolean; 
  latency: number;
  onRefresh: () => void;
}> = ({ isConnected, isHealthy, latency, onRefresh }) => {
  const getStatusColor = () => {
    if (isHealthy && isConnected) return 'text-green-400';
    if (isHealthy && !isConnected) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getStatusIcon = () => {
    if (isHealthy && isConnected) return <Wifi className="w-4 h-4" />;
    return <WifiOff className="w-4 h-4" />;
  };

  return (
    <div className="flex items-center space-x-2 text-sm">
      <span className={getStatusColor()}>{getStatusIcon()}</span>
      <span className="text-slate-300">
        {isHealthy ? 
          (isConnected ? `연결됨 (${latency}ms)` : '연결됨 (HTTP)') : 
          '연결 안됨'
        }
      </span>
      <button 
        onClick={onRefresh}
        className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
        title="새로고침"
      >
        <RefreshCw className="w-3 h-3" />
      </button>
    </div>
  );
};

const CrawlingDashboardReal: React.FC = () => {
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
    { id: '3', type: 'monitoring', title: '시스템 모니터링', size: 'large', position: { x: 0, y: 1 }, minimized: false },
    { id: '4', type: 'settings', title: '시스템 설정', size: 'medium', position: { x: 1, y: 1 }, minimized: false }
  ]);

  const [settings] = useState<SystemSettings>({
    autoRefresh: true,
    notifications: true,
    soundAlerts: false,
    realTimeUpdates: true,
    darkMode: true,
    refreshInterval: 5000,
    maxRetries: 3,
    timeout: 30000
  });

  // 실제 백엔드 연동
  const {
    services,
    systemStats,
    connectionStatus,
    alerts,
    refresh,
    dismissAlert,
    dismissAllAlerts,
    isConnected,
    isHealthy,
    getTotalCollected,
    getActiveServices,
    getAverageSuccessRate,
    activeAlertsCount
  } = useRealTimeCrawling({
    autoConnect: true,
    pollInterval: settings.refreshInterval
  });
  
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
    }
  ];
  
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

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

  const renderDashboardContent = () => (
    <div className="space-y-6">
      {/* 헤더 with 연결 상태 */}
      <motion.div 
        className="flex justify-between items-start"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div>
          <h1 className={`text-3xl font-bold bg-gradient-to-r ${currentTheme.primary} bg-clip-text text-transparent`}>
            실시간 크롤링 시스템
          </h1>
          <p className="text-slate-400 mt-2">실제 백엔드 연동 • 3-Tier 크롤링 & 멀티모달 AI 분석</p>
          
          {/* 연결 상태 */}
          <div className="mt-3">
            <ConnectionStatus 
              isConnected={isConnected}
              isHealthy={isHealthy}
              latency={connectionStatus.latency}
              onRefresh={refresh}
            />
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          {/* 알림 표시기 */}
          {activeAlertsCount > 0 && (
            <GlassBox theme={currentTheme} className="p-2">
              <div className="flex items-center space-x-2 text-sm">
                <Bell className="w-4 h-4 text-yellow-400" />
                <span className="text-slate-300">{activeAlertsCount}개 알림</span>
                <button 
                  onClick={dismissAllAlerts}
                  className="text-xs text-slate-500 hover:text-slate-300"
                >
                  모두 해제
                </button>
              </div>
            </GlassBox>
          )}
          
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
        </div>
      </motion.div>

      {/* 알림 목록 */}
      {alerts.length > 0 && (
        <motion.div 
          className="space-y-2"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {alerts.slice(0, 3).map((alert) => (
            <div 
              key={alert.id}
              className={`p-3 rounded-lg border ${
                alert.type === 'error' ? 'border-red-400/50 bg-red-400/10' :
                alert.type === 'warning' ? 'border-yellow-400/50 bg-yellow-400/10' :
                alert.type === 'success' ? 'border-green-400/50 bg-green-400/10' :
                'border-blue-400/50 bg-blue-400/10'
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-slate-200">{alert.title}</h4>
                  <p className="text-sm text-slate-400">{alert.message}</p>
                </div>
                <button 
                  onClick={() => dismissAlert(alert.id)}
                  className="text-slate-400 hover:text-slate-200 transition-colors"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </motion.div>
      )}

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
            {/* KPI 카드 위젯 - 실제 데이터 */}
            <GlassBox 
              theme={currentTheme}
              isDraggable
              dragId={widgets[0]?.id}
              className={widgets[0]?.minimized ? 'h-16' : ''}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className={`text-lg font-semibold bg-gradient-to-r ${currentTheme.secondary} bg-clip-text text-transparent`}>
                    실시간 핵심 지표
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
                            <p className="text-2xl font-bold text-blue-300">{getTotalCollected().toLocaleString()}</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <Database className="w-3 h-3 inline mr-1" />
                              실시간 업데이트
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
                            <p className="text-slate-400 text-sm">활성 서비스</p>
                            <p className="text-2xl font-bold text-green-300">{getActiveServices()}</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <Server className="w-3 h-3 inline mr-1" />
                              총 {services.length}개 중
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
                            <p className="text-slate-400 text-sm">평균 성공률</p>
                            <p className="text-2xl font-bold text-yellow-300">{getAverageSuccessRate().toFixed(1)}%</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <TrendingUp className="w-3 h-3 inline mr-1" />
                              실시간 계산
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
                            <p className="text-slate-400 text-sm">전체 품질</p>
                            <p className="text-2xl font-bold text-purple-300">{systemStats?.avg_quality.toFixed(1) || 0}%</p>
                            <p className="text-xs text-slate-500 mt-1">
                              <Eye className="w-3 h-3 inline mr-1" />
                              데이터 품질점수
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

            {/* 실제 크롤러 상태 위젯 */}
            <GlassBox 
              theme={currentTheme}
              isDraggable
              dragId={widgets[1]?.id}
              className={widgets[1]?.minimized ? 'h-16' : ''}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className={`text-xl font-semibold flex items-center bg-gradient-to-r ${currentTheme.secondary} bg-clip-text text-transparent`}>
                    <Activity className="w-5 h-5 mr-2 text-green-400" />
                    실제 크롤러 현황
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
                      onClick={refresh}
                    >
                      <RefreshCw className="w-4 h-4 inline mr-1" />
                      새로고침
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
                      {services.length === 0 ? (
                        <div className="text-center py-8 text-slate-400">
                          <WifiOff className="w-12 h-12 mx-auto mb-4" />
                          <p>크롤링 서비스에 연결할 수 없습니다.</p>
                          <button 
                            onClick={refresh}
                            className="mt-2 text-blue-400 hover:text-blue-300 transition-colors"
                          >
                            다시 시도
                          </button>
                        </div>
                      ) : (
                        services.map((service) => (
                          <div key={service.service_id} className={`p-4 rounded-lg border ${getStatusColor(service.status)} hover:bg-slate-700/20 transition-colors`}>
                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center space-x-3">
                                {getStatusIcon(service.status)}
                                <span className="font-medium">{service.service_name}</span>
                                <span className="px-2 py-1 rounded-full text-xs font-mono bg-blue-500/20 text-blue-300 border border-blue-500/30">
                                  {service.target_urls.join(', ')}
                                </span>
                              </div>
                              <div className="text-right">
                                <div className="text-sm font-semibold text-slate-200">{service.collected_count.toLocaleString()}</div>
                                <div className="text-xs text-slate-500">{service.collection_speed}/min</div>
                              </div>
                            </div>
                            
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex-1 mr-4">
                                <div className="w-full bg-slate-700/50 rounded-full h-2">
                                  <motion.div 
                                    className={`bg-gradient-to-r ${currentTheme.accent} h-2 rounded-full transition-all duration-300`}
                                    initial={{ width: 0 }}
                                    animate={{ width: `${service.success_rate}%` }}
                                    transition={{ duration: 1.5, ease: "easeInOut" }}
                                  />
                                </div>
                              </div>
                              <div className="text-sm font-mono">
                                <span className="text-slate-300">{service.success_rate.toFixed(1)}%</span>
                              </div>
                            </div>
                            
                            <div className="flex items-center justify-between text-xs text-slate-500">
                              <div className="flex items-center">
                                <Clock className="w-3 h-3 mr-1" />
                                응답시간: {service.avg_response_time.toFixed(1)}s
                              </div>
                              <div className="flex items-center">
                                <span>품질: {service.data_quality_score.toFixed(1)}%</span>
                              </div>
                              <div className={`px-2 py-1 rounded-full ${
                                service.status === 'running' ? 'bg-green-400/20 text-green-300' : 
                                service.status === 'error' ? 'bg-red-400/20 text-red-300' : 
                                'bg-yellow-400/20 text-yellow-300'
                              }`}>
                                {service.status === 'running' ? '실행 중' : 
                                 service.status === 'error' ? '오류' : '일시정지'}
                              </div>
                            </div>
                            
                            {service.last_collected_item && (
                              <div className="mt-2 text-xs text-slate-400">
                                <span>최근 수집: </span>
                                <span className="text-slate-300">{service.last_collected_item}</span>
                              </div>
                            )}
                          </div>
                        ))
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </GlassBox>
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
      case 'settings':
        return <SettingsPage />;
      default:
        return renderDashboardContent();
    }
  };

  return (
    <CrawlingLayout currentPage={currentPage} onPageChange={(page: CrawlingPage) => setCurrentPage(page)}>
      {renderPageContent()}
    </CrawlingLayout>
  );
};

export default CrawlingDashboardReal;