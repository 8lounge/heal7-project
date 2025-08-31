import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Terminal, 
  Scroll, 
  Filter, 
  Download, 
  Trash2, 
  Pause, 
  Play,
  AlertCircle,
  Info,
  AlertTriangle,
  Bug,
  Search,
  X
} from 'lucide-react';

interface RealTimeLog {
  id: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  timestamp: string;
  source: string;
  details?: any;
}

interface RealTimeLogsProps {
  logs: RealTimeLog[];
  isConnected: boolean;
  onClearLogs: () => void;
  className?: string;
}

const RealTimeLogs: React.FC<RealTimeLogsProps> = ({
  logs,
  isConnected,
  onClearLogs,
  className = ''
}) => {
  const [isPaused, setIsPaused] = useState(false);
  const [selectedLevel, setSelectedLevel] = useState<'all' | 'info' | 'warn' | 'error' | 'debug'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const maxVisible = 100;
  
  const logContainerRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);

  const filteredLogs = logs.filter(log => {
    const matchesLevel = selectedLevel === 'all' || log.level === selectedLevel;
    const matchesSearch = searchTerm === '' || 
      log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.source.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesLevel && matchesSearch;
  }).slice(0, maxVisible);

  // 자동 스크롤
  useEffect(() => {
    if (autoScroll && !isPaused && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, autoScroll, isPaused]);

  // 스크롤 위치 감지
  const handleScroll = () => {
    if (logContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = logContainerRef.current;
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10;
      setAutoScroll(isAtBottom);
    }
  };

  const getLevelIcon = (level: string) => {
    switch (level) {
      case 'error': return <AlertCircle className="w-4 h-4" />;
      case 'warn': return <AlertTriangle className="w-4 h-4" />;
      case 'debug': return <Bug className="w-4 h-4" />;
      default: return <Info className="w-4 h-4" />;
    }
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error': return 'text-red-400 bg-red-400/10';
      case 'warn': return 'text-yellow-400 bg-yellow-400/10';
      case 'debug': return 'text-purple-400 bg-purple-400/10';
      default: return 'text-blue-400 bg-blue-400/10';
    }
  };

  const levelCounts = logs.reduce((acc, log) => {
    acc[log.level] = (acc[log.level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('ko-KR', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className={`bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl border border-slate-600/50 ${className}`}>
      {/* 헤더 */}
      <div className="p-4 border-b border-slate-700/50">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Terminal className="w-5 h-5 text-green-400" />
            <h3 className="text-lg font-semibold text-white">실시간 로그</h3>
            <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs ${
              isConnected ? 'bg-green-400/20 text-green-300' : 'bg-red-400/20 text-red-300'
            }`}>
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
              <span>{isConnected ? '연결됨' : '연결 끊김'}</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsPaused(!isPaused)}
              className={`p-1.5 rounded transition-colors ${
                isPaused 
                  ? 'text-yellow-400 bg-yellow-400/20 hover:bg-yellow-400/30' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
              title={isPaused ? '재개' : '일시정지'}
            >
              {isPaused ? <Play className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
            </button>
            
            <button
              onClick={onClearLogs}
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded transition-colors"
              title="로그 지우기"
            >
              <Trash2 className="w-4 h-4" />
            </button>
            
            <button
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded transition-colors"
              title="로그 다운로드"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* 필터 및 검색 */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value as any)}
              className="px-2 py-1 bg-slate-700 border border-slate-600 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="all">전체 ({logs.length})</option>
              <option value="error">오류 ({levelCounts.error || 0})</option>
              <option value="warn">경고 ({levelCounts.warn || 0})</option>
              <option value="info">정보 ({levelCounts.info || 0})</option>
              <option value="debug">디버그 ({levelCounts.debug || 0})</option>
            </select>
          </div>

          <div className="flex-1 max-w-xs relative">
            <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 w-3 h-3 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="로그 검색..."
              className="w-full pl-8 pr-8 py-1 bg-slate-700 border border-slate-600 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>

          <div className="text-xs text-slate-400">
            {filteredLogs.length} / {logs.length} 표시
          </div>
        </div>
      </div>

      {/* 로그 목록 */}
      <div 
        ref={logContainerRef}
        className="h-64 overflow-y-auto font-mono text-sm"
        onScroll={handleScroll}
      >
        <AnimatePresence initial={false}>
          {filteredLogs.map((log) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: isPaused ? 0.5 : 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className={`flex items-start space-x-2 p-2 border-b border-slate-700/20 hover:bg-slate-700/20 transition-colors ${getLevelColor(log.level)}`}
            >
              <div className="flex items-center space-x-2 flex-shrink-0 min-w-0">
                <span className="text-xs text-slate-500">{formatTime(log.timestamp)}</span>
                {getLevelIcon(log.level)}
                <span className="text-xs text-slate-400 truncate max-w-20">{log.source}</span>
              </div>
              <div className="flex-1 min-w-0">
                <span className="text-slate-200 break-words">{log.message}</span>
                {log.details && (
                  <div className="mt-1 text-xs text-slate-500">
                    {JSON.stringify(log.details, null, 2)}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {logs.length === 0 && (
          <div className="flex items-center justify-center h-full text-slate-400">
            <div className="text-center">
              <Scroll className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>로그 없음</p>
              <p className="text-xs">크롤링 작업이 시작되면 로그가 표시됩니다</p>
            </div>
          </div>
        )}

        {/* 자동 스크롤 표시 */}
        {!autoScroll && logs.length > 0 && (
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="fixed bottom-4 right-4 px-3 py-2 bg-blue-500/20 text-blue-300 rounded-lg border border-blue-500/30 hover:bg-blue-500/30 transition-colors text-xs"
            onClick={() => {
              setAutoScroll(true);
              if (logContainerRef.current) {
                logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
              }
            }}
          >
            최신 로그로 이동 ↓
          </motion.button>
        )}
      </div>

      {/* 푸터 */}
      <div className="p-2 border-t border-slate-700/50 bg-slate-900/20">
        <div className="flex items-center justify-between text-xs text-slate-500">
          <div className="flex items-center space-x-4">
            <span>마지막 업데이트: {logs.length > 0 ? formatTime(logs[0]?.timestamp) : '-'}</span>
            <span>버퍼: {logs.length}/1000</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className={autoScroll ? 'text-green-400' : 'text-slate-500'}>
              자동스크롤: {autoScroll ? 'ON' : 'OFF'}
            </span>
            {isPaused && (
              <span className="text-yellow-400 animate-pulse">일시정지</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeLogs;