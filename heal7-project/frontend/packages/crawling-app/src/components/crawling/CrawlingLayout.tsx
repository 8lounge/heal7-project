import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import CrawlingHeader from './CrawlingHeader';
import CrawlingSidebar from './CrawlingSidebar';
import RealTimeLogs from './RealTimeLogs';
import SystemAlerts from './SystemAlerts';
import { useRealTime } from '../../hooks/useRealTime';
import { Terminal, Bell } from 'lucide-react';

type CrawlingPage = 'dashboard' | 'crawling' | 'ai-analysis' | 'data-management' | 'settings';

interface SystemMetrics {
  crawlerStatus: 'active' | 'idle' | 'error';
  activeTasks: number;
  totalCollected: number;
  systemLoad: number;
  lastSync: string;
}

interface CrawlingLayoutProps {
  children: React.ReactNode;
  currentPage: CrawlingPage;
  onPageChange: (page: CrawlingPage) => void;
}

const CrawlingLayout: React.FC<CrawlingLayoutProps> = ({
  children,
  currentPage,
  onPageChange
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [showRealTimeLogs, setShowRealTimeLogs] = useState(false);
  const [showSystemAlerts, setShowSystemAlerts] = useState(false);
  
  // 실시간 기능 훅 사용
  const {
    connectionStatus,
    systemMetrics: realTimeMetrics,
    logs,
    alerts,
    clearLogs,
    dismissAlert,
    dismissAllAlerts,
    activeAlertsCount,
    isHealthy
  } = useRealTime({
    enableLogs: true,
    enableAlerts: true,
    enableMetrics: true,
    logBufferSize: 1000,
    updateInterval: 2000
  });

  // 기존 시스템 메트릭을 실시간 데이터로 업데이트
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics>({
    crawlerStatus: 'active',
    activeTasks: 8,
    totalCollected: 15420,
    systemLoad: 67,
    lastSync: new Date().toLocaleTimeString('ko-KR')
  });

  // 실시간 메트릭을 시스템 메트릭에 반영
  useEffect(() => {
    setSystemMetrics(prev => ({
      ...prev,
      activeTasks: realTimeMetrics.activeCrawlers,
      systemLoad: Math.round(realTimeMetrics.cpu),
      lastSync: new Date().toLocaleTimeString('ko-KR'),
      crawlerStatus: isHealthy ? 'active' : realTimeMetrics.errorRate > 5 ? 'error' : 'idle'
    }));
  }, [realTimeMetrics, isHealthy]);

  // 키보드 단축키
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case '1':
            e.preventDefault();
            onPageChange('dashboard');
            break;
          case '2':
            e.preventDefault();
            onPageChange('crawling');
            break;
          case '3':
            e.preventDefault();
            onPageChange('ai-analysis');
            break;
          case '4':
            e.preventDefault();
            onPageChange('data-management');
            break;
          case '5':
            e.preventDefault();
            onPageChange('settings');
            break;
          case 'b':
            e.preventDefault();
            setIsCollapsed(!isCollapsed);
            break;
          case 'l':
            e.preventDefault();
            setShowRealTimeLogs(!showRealTimeLogs);
            break;
          case 'n':
            e.preventDefault();
            setShowSystemAlerts(!showSystemAlerts);
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isCollapsed, onPageChange]);

  const handleSettingsClick = () => {
    onPageChange('settings');
  };

  const handleNotificationsClick = () => {
    setShowSystemAlerts(!showSystemAlerts);
  };

  const handleProfileClick = () => {
    // 프로필 메뉴 또는 모달 열기
    console.log('Profile clicked');
  };

  const handleToggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* 헤더 */}
      <CrawlingHeader
        systemMetrics={systemMetrics}
        onSettingsClick={handleSettingsClick}
        onNotificationsClick={handleNotificationsClick}
        onProfileClick={handleProfileClick}
      />

      <div className="flex h-screen pt-0">
        {/* 사이드바 */}
        <CrawlingSidebar
          currentPage={currentPage}
          onPageChange={onPageChange}
          isCollapsed={isCollapsed}
          onToggleCollapse={handleToggleCollapse}
        />

        {/* 메인 컨텐츠 영역 */}
        <main className="flex-1 overflow-auto">
          <motion.div
            className="p-6 h-full"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            key={currentPage}
          >
            {children}
          </motion.div>
        </main>
      </div>

      {/* 실시간 로그 패널 */}
      <AnimatePresence>
        {showRealTimeLogs && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowRealTimeLogs(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="w-full max-w-4xl max-h-[80vh] overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <RealTimeLogs
                logs={logs}
                isConnected={connectionStatus.isConnected}
                onClearLogs={clearLogs}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 시스템 알림 패널 */}
      <AnimatePresence>
        {showSystemAlerts && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed top-20 right-4 z-50 w-96 max-h-[calc(100vh-8rem)] overflow-hidden"
          >
            <SystemAlerts
              alerts={alerts}
              onDismiss={dismissAlert}
              onDismissAll={dismissAllAlerts}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* 플로팅 실시간 제어 버튼 */}
      <div className="fixed bottom-4 right-4 flex flex-col space-y-2 z-40">
        {/* 알림 버튼 */}
        <motion.button
          className={`p-3 rounded-full backdrop-blur-sm border transition-all duration-300 relative ${
            activeAlertsCount > 0
              ? 'bg-red-500/20 border-red-500/30 text-red-300 hover:bg-red-500/30'
              : 'bg-slate-800/80 border-slate-600/50 text-slate-400 hover:text-white hover:bg-slate-700/80'
          }`}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleNotificationsClick}
          title="시스템 알림"
        >
          <Bell className="w-5 h-5" />
          {activeAlertsCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-medium">
              {activeAlertsCount > 9 ? '9+' : activeAlertsCount}
            </span>
          )}
        </motion.button>

        {/* 로그 버튼 */}
        <motion.button
          className={`p-3 rounded-full backdrop-blur-sm border transition-all duration-300 ${
            connectionStatus.isConnected
              ? 'bg-green-500/20 border-green-500/30 text-green-300 hover:bg-green-500/30'
              : 'bg-red-500/20 border-red-500/30 text-red-300 hover:bg-red-500/30'
          }`}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowRealTimeLogs(!showRealTimeLogs)}
          title="실시간 로그"
        >
          <Terminal className="w-5 h-5" />
        </motion.button>
      </div>

      {/* 키보드 단축키 힌트 (개발 시에만 표시) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed bottom-4 left-4 bg-slate-800/90 backdrop-blur-sm p-3 rounded-lg text-xs text-slate-400 border border-slate-700/50 max-w-xs">
          <div className="font-semibold text-slate-200 mb-2">키보드 단축키</div>
          <div className="space-y-1">
            <div>Ctrl/Cmd + 1-5: 페이지 전환</div>
            <div>Ctrl/Cmd + B: 사이드바 축소/확장</div>
            <div>Ctrl/Cmd + L: 실시간 로그 열기</div>
            <div>Ctrl/Cmd + N: 알림 패널 열기</div>
          </div>
        </div>
      )}

      {/* 연결 상태 표시 */}
      <div className="fixed top-4 right-4 z-30">
        <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-full backdrop-blur-sm border text-xs font-medium ${
          connectionStatus.isConnected
            ? 'bg-green-500/20 border-green-500/30 text-green-300'
            : 'bg-red-500/20 border-red-500/30 text-red-300'
        }`}>
          <div className={`w-2 h-2 rounded-full animate-pulse ${
            connectionStatus.isConnected ? 'bg-green-400' : 'bg-red-400'
          }`} />
          <span>
            {connectionStatus.isConnected ? '실시간 연결됨' : '연결 끊김'}
          </span>
          {connectionStatus.isConnected && (
            <span className="text-slate-500">
              ({connectionStatus.latency.toFixed(0)}ms)
            </span>
          )}
        </div>
      </div>

      {/* 배경 그라데이션 오버레이 */}
      <div className="fixed inset-0 bg-gradient-to-br from-purple-900/5 via-transparent to-pink-900/5 pointer-events-none" />
    </div>
  );
};

export default CrawlingLayout;