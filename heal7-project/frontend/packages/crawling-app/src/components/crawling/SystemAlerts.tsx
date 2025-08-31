import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bell, 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  Info,
  X,
  Trash2,
  Settings
} from 'lucide-react';

interface SystemAlert {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: string;
  dismissed: boolean;
}

interface SystemAlertsProps {
  alerts: SystemAlert[];
  onDismiss: (alertId: string) => void;
  onDismissAll: () => void;
  className?: string;
}

const SystemAlerts: React.FC<SystemAlertsProps> = ({
  alerts,
  onDismiss,
  onDismissAll,
  className = ''
}) => {
  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'success': return <CheckCircle className="w-5 h-5" />;
      case 'warning': return <AlertTriangle className="w-5 h-5" />;
      case 'error': return <XCircle className="w-5 h-5" />;
      default: return <Info className="w-5 h-5" />;
    }
  };

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'success': 
        return 'border-green-500/30 bg-green-500/10 text-green-300';
      case 'warning': 
        return 'border-yellow-500/30 bg-yellow-500/10 text-yellow-300';
      case 'error': 
        return 'border-red-500/30 bg-red-500/10 text-red-300';
      default: 
        return 'border-blue-500/30 bg-blue-500/10 text-blue-300';
    }
  };

  const formatTime = (timestamp: string) => {
    const now = new Date();
    const alertTime = new Date(timestamp);
    const diffMs = now.getTime() - alertTime.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return '방금 전';
    if (diffMins < 60) return `${diffMins}분 전`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}시간 전`;
    return alertTime.toLocaleDateString('ko-KR');
  };

  const activeAlerts = alerts.filter(alert => !alert.dismissed);

  return (
    <div className={`bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl border border-slate-600/50 ${className}`}>
      {/* 헤더 */}
      <div className="p-4 border-b border-slate-700/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bell className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold text-white">시스템 알림</h3>
            {activeAlerts.length > 0 && (
              <span className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded-full text-xs font-medium">
                {activeAlerts.length}
              </span>
            )}
          </div>

          <div className="flex items-center space-x-2">
            {activeAlerts.length > 0 && (
              <button
                onClick={onDismissAll}
                className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded transition-colors"
                title="모든 알림 해제"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
            <button
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded transition-colors"
              title="알림 설정"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* 알림 목록 */}
      <div className="max-h-80 overflow-y-auto">
        <AnimatePresence>
          {activeAlerts.map((alert) => (
            <motion.div
              key={alert.id}
              initial={{ opacity: 0, x: 300 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 300 }}
              className={`p-4 border-b border-slate-700/30 last:border-b-0 ${getAlertColor(alert.type)} border-l-4 hover:bg-opacity-20 transition-colors`}
            >
              <div className="flex items-start justify-between space-x-3">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-0.5">
                    {getAlertIcon(alert.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-semibold text-white mb-1">{alert.title}</h4>
                    <p className="text-sm text-slate-200 mb-2">{alert.message}</p>
                    <div className="flex items-center space-x-2 text-xs text-slate-400">
                      <span>{formatTime(alert.timestamp)}</span>
                      <span>•</span>
                      <span className="capitalize">{alert.type}</span>
                    </div>
                  </div>
                </div>
                
                <button
                  onClick={() => onDismiss(alert.id)}
                  className="flex-shrink-0 p-1 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded transition-colors"
                  title="알림 해제"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {activeAlerts.length === 0 && (
          <div className="flex items-center justify-center h-32 text-slate-400">
            <div className="text-center">
              <Bell className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>새 알림 없음</p>
              <p className="text-xs">시스템이 정상적으로 작동 중입니다</p>
            </div>
          </div>
        )}
      </div>

      {/* 푸터 통계 */}
      {alerts.length > 0 && (
        <div className="p-3 bg-slate-900/20 border-t border-slate-700/50">
          <div className="flex items-center justify-between text-xs text-slate-500">
            <div className="flex items-center space-x-4">
              <span>총 {alerts.length}개 알림</span>
              <span>활성 {activeAlerts.length}개</span>
            </div>
            <div className="flex items-center space-x-3">
              <span className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>{alerts.filter(a => a.type === 'success').length}</span>
              </span>
              <span className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                <span>{alerts.filter(a => a.type === 'warning').length}</span>
              </span>
              <span className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                <span>{alerts.filter(a => a.type === 'error').length}</span>
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SystemAlerts;