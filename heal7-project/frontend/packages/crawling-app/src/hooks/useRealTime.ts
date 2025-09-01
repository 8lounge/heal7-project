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

  // 실제 WebSocket 연결
  const connect = useCallback(() => {
    console.log('🔌 실제 WebSocket 연결 시작');
    
    try {
      const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`;
      const socket = new WebSocket(wsUrl);
      
      socket.onopen = () => {
        setConnectionStatus(prev => ({
          ...prev,
          isConnected: true,
          reconnectAttempts: 0,
          lastHeartbeat: new Date().toISOString()
        }));

        if (enableAlerts) {
          addAlert('success', '실시간 연결', 'WebSocket 연결이 성공적으로 설정되었습니다.');
        }
      };

      socket.onerror = (error) => {
        console.error('WebSocket 연결 오류:', error);
        setConnectionStatus(prev => ({
          ...prev,
          isConnected: false,
          reconnectAttempts: prev.reconnectAttempts + 1
        }));

        if (enableAlerts) {
          addAlert('error', '연결 오류', 'WebSocket 연결에 실패했습니다. 서버 상태를 확인하세요.');
        }
      };

      socket.onclose = () => {
        setConnectionStatus(prev => ({
          ...prev,
          isConnected: false
        }));
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleRealTimeMessage(data);
        } catch (error) {
          console.error('WebSocket 메시지 파싱 오류:', error);
        }
      };
      
    } catch (error) {
      console.error('WebSocket 연결 실패:', error);
      if (enableAlerts) {
        addAlert('error', '연결 실패', `WebSocket 연결 실패: ${error instanceof Error ? error.message : '알 수 없는 오류'}`);
      }
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

  // 실제 시스템 메트릭 업데이트 (API 호출)
  const updateMetrics = useCallback(async () => {
    if (!enableMetrics) return;

    try {
      const response = await fetch('/api/system/metrics');
      if (response.ok) {
        const metrics = await response.json();
        setSystemMetrics(metrics);

        // 임계값 알림 (실제 데이터 기반)
        if (metrics.cpu > 90) {
          addAlert('error', '높은 CPU 사용률', `CPU 사용률이 ${metrics.cpu.toFixed(1)}%에 도달했습니다.`);
        }
        if (metrics.memory > 85) {
          addAlert('warning', '메모리 부족', `메모리 사용률이 ${metrics.memory.toFixed(1)}%입니다.`);
        }
        if (metrics.errorRate > 5) {
          addAlert('warning', '높은 오류율', `오류율이 ${metrics.errorRate.toFixed(1)}%로 증가했습니다.`);
        }
      } else {
        throw new Error(`API 응답 오류: ${response.status}`);
      }
    } catch (error) {
      console.error('메트릭 업데이트 오류:', error);
      addAlert('error', '메트릭 오류', `시스템 메트릭 업데이트 실패: ${error instanceof Error ? error.message : '알 수 없는 오류'}`);
    }

    // 하트비트 업데이트
    setConnectionStatus(prev => ({
      ...prev,
      lastHeartbeat: new Date().toISOString()
    }));
  }, [enableMetrics, addAlert]);

  // 실제 WebSocket 메시지 처리
  const handleRealTimeMessage = useCallback((data: any) => {
    try {
      switch (data.type) {
        case 'log':
          addLog(data.level || 'info', data.message, data.source || 'system', data.details);
          break;
        case 'metrics':
          setSystemMetrics(data.metrics);
          break;
        case 'alert':
          addAlert(data.alertType || 'info', data.title || '시스템 알림', data.message);
          break;
        case 'heartbeat':
          setConnectionStatus(prev => ({
            ...prev,
            lastHeartbeat: new Date().toISOString(),
            latency: data.latency || 0
          }));
          break;
        default:
          console.log('알 수 없는 WebSocket 메시지:', data);
      }
    } catch (error) {
      console.error('실시간 메시지 처리 오류:', error);
    }
  }, [addLog, addAlert]);

  // 실시간 업데이트 시작 (폴백용 정기 업데이트)
  useEffect(() => {
    if (connectionStatus.isConnected) {
      // WebSocket이 연결된 상태에서도 정기적으로 메트릭 업데이트 (폴백)
      intervalRef.current = setInterval(() => {
        updateMetrics();
      }, updateInterval);

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    } else {
      // 연결이 끊어진 경우 재연결 시도
      const reconnectTimer = setTimeout(() => {
        if (connectionStatus.reconnectAttempts < 5) {
          console.log(`재연결 시도 ${connectionStatus.reconnectAttempts + 1}/5`);
          connect();
        } else {
          addAlert('error', '연결 실패', '최대 재연결 횟수를 초과했습니다. 페이지를 새로고침해주세요.');
        }
      }, Math.min(1000 * Math.pow(2, connectionStatus.reconnectAttempts), 30000)); // 지수 백오프

      return () => clearTimeout(reconnectTimer);
    }
  }, [connectionStatus.isConnected, connectionStatus.reconnectAttempts, updateMetrics, updateInterval, connect, addAlert]);

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