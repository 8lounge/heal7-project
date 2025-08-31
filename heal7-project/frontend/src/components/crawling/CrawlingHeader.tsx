import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Database, Cpu, Wifi, Settings, Bell, User } from 'lucide-react';

interface SystemMetrics {
  crawlerStatus: 'active' | 'idle' | 'error';
  activeTasks: number;
  totalCollected: number;
  systemLoad: number;
  lastSync: string;
}

interface CrawlingHeaderProps {
  systemMetrics: SystemMetrics;
  onSettingsClick: () => void;
  onNotificationsClick: () => void;
  onProfileClick: () => void;
}

const CrawlingHeader: React.FC<CrawlingHeaderProps> = ({
  systemMetrics,
  onSettingsClick,
  onNotificationsClick,
  onProfileClick
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-400 bg-green-400/20';
      case 'idle':
        return 'text-blue-400 bg-blue-400/20';
      case 'error':
        return 'text-red-400 bg-red-400/20';
      default:
        return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active':
        return '활성';
      case 'idle':
        return '대기';
      case 'error':
        return '오류';
      default:
        return '알수없음';
    }
  };

  return (
    <motion.header 
      className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-700/50"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* 로고 및 타이틀 */}
          <motion.div 
            className="flex items-center space-x-4"
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">크롤링 대시보드</h1>
                <p className="text-sm text-slate-400">HEAL7 Crawling Control Center</p>
              </div>
            </div>
          </motion.div>

          {/* 시스템 상태 지표 */}
          <div className="flex items-center space-x-6">
            {/* 크롤러 상태 */}
            <div className="flex items-center space-x-2">
              <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-full ${getStatusColor(systemMetrics.crawlerStatus)}`}>
                <div className={`w-2 h-2 rounded-full ${systemMetrics.crawlerStatus === 'active' ? 'bg-green-400' : systemMetrics.crawlerStatus === 'error' ? 'bg-red-400' : 'bg-blue-400'} animate-pulse`} />
                <span className="text-sm font-medium">{getStatusLabel(systemMetrics.crawlerStatus)}</span>
              </div>
            </div>

            {/* 활성 작업 */}
            <div className="flex items-center space-x-2 text-slate-300">
              <Cpu className="w-4 h-4" />
              <span className="text-sm font-medium">{systemMetrics.activeTasks}개 작업</span>
            </div>

            {/* 수집 데이터 */}
            <div className="flex items-center space-x-2 text-slate-300">
              <Database className="w-4 h-4" />
              <span className="text-sm font-medium">{systemMetrics.totalCollected.toLocaleString()}건</span>
            </div>

            {/* 시스템 부하 */}
            <div className="flex items-center space-x-2 text-slate-300">
              <Wifi className="w-4 h-4" />
              <div className="flex items-center space-x-1">
                <span className="text-sm font-medium">{systemMetrics.systemLoad}%</span>
                <div className="w-16 h-2 bg-slate-700 rounded-full">
                  <div 
                    className={`h-full rounded-full transition-all duration-300 ${
                      systemMetrics.systemLoad > 80 ? 'bg-red-400' : 
                      systemMetrics.systemLoad > 60 ? 'bg-yellow-400' : 'bg-green-400'
                    }`}
                    style={{ width: `${systemMetrics.systemLoad}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* 컨트롤 버튼 */}
          <div className="flex items-center space-x-3">
            {/* 알림 */}
            <motion.button
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onNotificationsClick}
            >
              <Bell className="w-5 h-5" />
            </motion.button>

            {/* 설정 */}
            <motion.button
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onSettingsClick}
            >
              <Settings className="w-5 h-5" />
            </motion.button>

            {/* 프로필 */}
            <motion.button
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onProfileClick}
            >
              <User className="w-5 h-5" />
            </motion.button>
          </div>
        </div>

        {/* 마지막 동기화 시간 */}
        <div className="mt-2 text-xs text-slate-500 text-right">
          마지막 업데이트: {systemMetrics.lastSync}
        </div>
      </div>
    </motion.header>
  );
};

export default CrawlingHeader;