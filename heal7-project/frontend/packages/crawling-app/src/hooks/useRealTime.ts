import { useState, useEffect, useRef, useCallback } from 'react';

interface SystemAlert {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: string;
  dismissed: boolean;
}

interface RealTimeLog {
  id: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  timestamp: string;
  source: string;
  details?: any;
}

interface SystemMetrics {
  cpu: number;
  memory: number;
  network: number;
  activeCrawlers: number;
  queueSize: number;
  errorRate: number;
}

interface ConnectionStatus {
  isConnected: boolean;
  lastHeartbeat: string;
  reconnectAttempts: number;
  latency: number;
}

interface UseRealTimeOptions {
  enableLogs?: boolean;
  enableAlerts?: boolean;
  enableMetrics?: boolean;
  logBufferSize?: number;
  updateInterval?: number;
}

export const useRealTime = (options: UseRealTimeOptions = {}) => {
  const {
    enableLogs = true,
    enableAlerts = true,
    enableMetrics = true,
    logBufferSize = 1000,
    updateInterval = 2000
  } = options;

  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    isConnected: false,
    lastHeartbeat: new Date().toISOString(),
    reconnectAttempts: 0,
    latency: 0
  });

  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics>({
    cpu: 0,
    memory: 0,
    network: 0,
    activeCrawlers: 0,
    queueSize: 0,
    errorRate: 0
  });

  const [logs, setLogs] = useState<RealTimeLog[]>([]);
  const [alerts, setAlerts] = useState<SystemAlert[]>([]);

  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const logIdCounter = useRef(0);
  const alertIdCounter = useRef(0);

  // WebSocket 연결 시뮬레이션
  const connect = useCallback(() => {
    console.log('🔌 WebSocket 연결 시뮬레이션 시작');
    
    setConnectionStatus(prev => ({
      ...prev,
      isConnected: true,
      reconnectAttempts: 0,
      lastHeartbeat: new Date().toISOString()
    }));

    // 연결 성공 알림
    if (enableAlerts) {
      addAlert('success', '실시간 연결', 'WebSocket 연결이 성공적으로 설정되었습니다.');
    }
  }, [enableAlerts]);

  const disconnect = useCallback(() => {
    console.log('🔌 WebSocket 연결 해제');
    
    setConnectionStatus(prev => ({
      ...prev,
      isConnected: false,
      lastHeartbeat: new Date().toISOString()
    }));

    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  // 로그 추가
  const addLog = useCallback((level: RealTimeLog['level'], message: string, source: string, details?: any) => {
    if (!enableLogs) return;

    const newLog: RealTimeLog = {
      id: `log_${++logIdCounter.current}`,
      level,
      message,
      source,
      timestamp: new Date().toISOString(),
      details
    };

    setLogs(prevLogs => {
      const newLogs = [newLog, ...prevLogs];
      return newLogs.slice(0, logBufferSize);
    });

    // 에러 로그인 경우 자동으로 알림 생성
    if (level === 'error' && enableAlerts) {
      addAlert('error', `${source} 오류`, message);
    }
  }, [enableLogs, enableAlerts, logBufferSize]);

  // 알림 추가
  const addAlert = useCallback((
    type: SystemAlert['type'],
    title: string,
    message: string
  ) => {
    if (!enableAlerts) return;

    const newAlert: SystemAlert = {
      id: `alert_${++alertIdCounter.current}`,
      type,
      title,
      message,
      timestamp: new Date().toISOString(),
      dismissed: false
    };

    setAlerts(prevAlerts => [newAlert, ...prevAlerts].slice(0, 50)); // 최대 50개 알림 유지
  }, [enableAlerts]);

  // 알림 해제
  const dismissAlert = useCallback((alertId: string) => {
    setAlerts(prevAlerts => 
      prevAlerts.map(alert => 
        alert.id === alertId ? { ...alert, dismissed: true } : alert
      )
    );
  }, []);

  // 모든 알림 해제
  const dismissAllAlerts = useCallback(() => {
    setAlerts(prevAlerts => 
      prevAlerts.map(alert => ({ ...alert, dismissed: true }))
    );
  }, []);

  // 시스템 메트릭 업데이트 시뮬레이션
  const updateMetrics = useCallback(() => {
    if (!enableMetrics) return;

    setSystemMetrics(prevMetrics => {
      const cpu = Math.max(0, Math.min(100, prevMetrics.cpu + (Math.random() - 0.5) * 20));
      const memory = Math.max(0, Math.min(100, prevMetrics.memory + (Math.random() - 0.5) * 10));
      const network = Math.random() * 100;
      const activeCrawlers = Math.max(0, prevMetrics.activeCrawlers + Math.floor((Math.random() - 0.5) * 3));
      const queueSize = Math.max(0, prevMetrics.queueSize + Math.floor((Math.random() - 0.5) * 10));
      const errorRate = Math.max(0, Math.min(10, prevMetrics.errorRate + (Math.random() - 0.5) * 2));

      const newMetrics = {
        cpu,
        memory,
        network,
        activeCrawlers,
        queueSize,
        errorRate
      };

      // 임계값 알림
      if (cpu > 90 && prevMetrics.cpu <= 90) {
        addAlert('error', '높은 CPU 사용률', `CPU 사용률이 ${cpu.toFixed(1)}%에 도달했습니다.`);
      }
      if (memory > 85 && prevMetrics.memory <= 85) {
        addAlert('warning', '메모리 부족', `메모리 사용률이 ${memory.toFixed(1)}%입니다.`);
      }
      if (errorRate > 5 && prevMetrics.errorRate <= 5) {
        addAlert('warning', '높은 오류율', `오류율이 ${errorRate.toFixed(1)}%로 증가했습니다.`);
      }

      return newMetrics;
    });

    // 하트비트 업데이트
    setConnectionStatus(prev => ({
      ...prev,
      lastHeartbeat: new Date().toISOString(),
      latency: Math.random() * 100 + 10
    }));
  }, [enableMetrics, addAlert]);

  // 랜덤 로그 생성 시뮬레이션
  const generateRandomLogs = useCallback(() => {
    const sources = ['httpx-crawler', 'playwright-engine', 'selenium-driver', 'ai-processor', 'data-manager'];
    const messages = [
      'HTTP 요청 성공적으로 처리됨',
      '새로운 데이터 항목 발견',
      '페이지 로딩 완료',
      'AI 분석 작업 시작',
      '데이터베이스 저장 완료',
      '크롤링 세션 시작',
      'JavaScript 실행 완료',
      '이미지 다운로드 완료',
      '테이블 데이터 추출',
      'OCR 처리 완료'
    ];

    if (Math.random() > 0.7) { // 30% 확률로 로그 생성
      const level = Math.random() > 0.9 ? 'error' : Math.random() > 0.7 ? 'warn' : 'info';
      const source = sources[Math.floor(Math.random() * sources.length)];
      const message = messages[Math.floor(Math.random() * messages.length)];
      
      addLog(level, message, source);
    }
  }, [addLog]);

  // 실시간 업데이트 시작
  useEffect(() => {
    if (connectionStatus.isConnected) {
      intervalRef.current = setInterval(() => {
        updateMetrics();
        generateRandomLogs();
      }, updateInterval);

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [connectionStatus.isConnected, updateMetrics, generateRandomLogs, updateInterval]);

  // 컴포넌트 마운트 시 자동 연결
  useEffect(() => {
    const timer = setTimeout(() => {
      connect();
    }, 1000);

    return () => {
      clearTimeout(timer);
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    // 연결 상태
    connectionStatus,
    connect,
    disconnect,

    // 시스템 메트릭
    systemMetrics,

    // 로그 관리
    logs,
    addLog,
    clearLogs: () => setLogs([]),

    // 알림 관리
    alerts: alerts.filter(alert => !alert.dismissed),
    allAlerts: alerts,
    addAlert,
    dismissAlert,
    dismissAllAlerts,

    // 유틸리티
    isHealthy: systemMetrics.cpu < 80 && systemMetrics.memory < 80 && systemMetrics.errorRate < 5,
    activeAlertsCount: alerts.filter(alert => !alert.dismissed).length
  };
};