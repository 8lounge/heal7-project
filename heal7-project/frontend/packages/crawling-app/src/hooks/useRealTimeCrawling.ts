/**
 * 🔌 실제 크롤링 백엔드 연동 Real-Time 훅
 * - 가짜 시뮬레이션 제거
 * - 실제 API 및 WebSocket 연결
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { crawlingAPI } from '../api/CrawlingAPIClient';

interface CrawlingService {
  service_id: string;
  service_name: string;
  target_urls: string[];
  status: 'running' | 'paused' | 'stopped' | 'error';
  collected_count: number;
  success_rate: number;
  avg_response_time: number;
  last_update: string;
  errors_count: number;
  data_quality_score: number;
  collection_speed: number;
  last_collected_item?: string;
}

interface SystemStats {
  total_collected: number;
  avg_success_rate: number;
  avg_response_time: number;
  avg_quality: number;
  active_services: number;
  timestamp: string;
}

interface SystemAlert {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: string;
  dismissed: boolean;
}

interface ConnectionStatus {
  isConnected: boolean;
  isHealthy: boolean;
  lastHeartbeat: string;
  reconnectAttempts: number;
  latency: number;
  error?: string;
}

interface UseRealTimeCrawlingOptions {
  autoConnect?: boolean;
  pollInterval?: number;
}

export const useRealTimeCrawling = (options: UseRealTimeCrawlingOptions = {}) => {
  const { autoConnect = true, pollInterval = 5000 } = options;
  
  const [services, setServices] = useState<CrawlingService[]>([]);
  const [systemStats, setSystemStats] = useState<SystemStats | null>(null);
  const [alerts, setAlerts] = useState<SystemAlert[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    isConnected: false,
    isHealthy: false,
    lastHeartbeat: '',
    reconnectAttempts: 0,
    latency: 0
  });

  const pollIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const alertIdCounter = useRef(0);
  const isInitialized = useRef(false);

  // 알림 추가 함수
  const addAlert = useCallback((
    type: SystemAlert['type'],
    title: string,
    message: string
  ) => {
    const newAlert: SystemAlert = {
      id: `alert_${++alertIdCounter.current}`,
      type,
      title,
      message,
      timestamp: new Date().toISOString(),
      dismissed: false
    };

    setAlerts(prevAlerts => [newAlert, ...prevAlerts].slice(0, 20)); // 최대 20개 알림 유지
  }, []);

  // 백엔드 데이터 폴링
  const pollBackendData = useCallback(async () => {
    const startTime = Date.now();
    
    try {
      // 동시에 여러 API 호출
      const [health, servicesData, statsData] = await Promise.all([
        crawlingAPI.checkHealth().catch(() => null),
        crawlingAPI.getServices().catch(() => []),
        crawlingAPI.getStats().catch(() => null)
      ]);

      const latency = Date.now() - startTime;
      const isHealthy = health?.status === 'healthy';
      
      setConnectionStatus(prev => ({
        ...prev,
        isHealthy,
        lastHeartbeat: new Date().toISOString(),
        latency,
        error: isHealthy ? undefined : '백엔드 연결 불안정'
      }));

      // 서비스 데이터 업데이트
      if (servicesData.length > 0) {
        setServices(prevServices => {
          // 새로운 서비스가 추가되었거나 상태가 변경된 경우 알림
          servicesData.forEach(newService => {
            const oldService = prevServices.find(s => s.service_id === newService.service_id);
            
            if (!oldService) {
              addAlert('info', '새 서비스', `${newService.service_name} 서비스가 시작되었습니다.`);
            } else if (oldService.status !== newService.status) {
              const statusMap = {
                running: '실행 중',
                paused: '일시정지',
                stopped: '중지됨',
                error: '오류'
              };
              addAlert(
                newService.status === 'error' ? 'error' : 'info',
                '상태 변경',
                `${newService.service_name}: ${statusMap[oldService.status]} → ${statusMap[newService.status]}`
              );
            }
          });
          
          return servicesData;
        });
      }

      // 통계 데이터 업데이트
      if (statsData) {
        setSystemStats(statsData);
        
        // 이상 상태 모니터링
        if (statsData.avg_success_rate < 80) {
          addAlert('warning', '낮은 성공률', `평균 성공률이 ${statsData.avg_success_rate.toFixed(1)}%로 낮습니다.`);
        }
        if (statsData.avg_response_time > 5) {
          addAlert('warning', '높은 응답시간', `평균 응답시간이 ${statsData.avg_response_time.toFixed(1)}초입니다.`);
        }
      }

    } catch (error) {
      console.error('❌ 백엔드 폴링 오류:', error);
      setConnectionStatus(prev => ({
        ...prev,
        isHealthy: false,
        error: error instanceof Error ? error.message : '폴링 오류'
      }));
      
      if (!isInitialized.current) {
        addAlert('error', '연결 실패', '크롤링 백엔드에 연결할 수 없습니다.');
      }
    }
    
    isInitialized.current = true;
  }, [addAlert]);

  // WebSocket 연결 설정
  const connectWebSocket = useCallback(() => {
    crawlingAPI.connectWebSocket(
      // onMessage
      (message) => {
        console.log('📡 WebSocket 메시지:', message);
        
        switch (message.type) {
          case 'service_update':
            setServices(prevServices => {
              return prevServices.map(service => 
                service.service_id === message.data.service_id 
                  ? { ...service, ...message.data }
                  : service
              );
            });
            break;
          case 'system_stats':
            setSystemStats(message.data);
            break;
          case 'health_check':
            setConnectionStatus(prev => ({
              ...prev,
              lastHeartbeat: message.timestamp
            }));
            break;
        }
      },
      // onConnected
      () => {
        setConnectionStatus(prev => ({ ...prev, isConnected: true }));
        addAlert('success', 'WebSocket 연결', '실시간 모니터링이 활성화되었습니다.');
      },
      // onDisconnected
      () => {
        setConnectionStatus(prev => ({ ...prev, isConnected: false }));
      },
      // onError
      (error) => {
        console.error('❌ WebSocket 오류:', error);
        addAlert('error', 'WebSocket 오류', '실시간 연결에 문제가 발생했습니다.');
      }
    );
  }, [addAlert]);

  // 연결 해제
  const disconnect = useCallback(() => {
    crawlingAPI.disconnectWebSocket();
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  // 수동 새로고침
  const refresh = useCallback(async () => {
    addAlert('info', '새로고침', '데이터를 새로고침합니다.');
    await pollBackendData();
  }, [pollBackendData, addAlert]);

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

  // 초기화 및 자동 연결
  useEffect(() => {
    if (autoConnect) {
      // 즉시 데이터 로드
      pollBackendData();
      
      // WebSocket 연결 시도 (1초 후)
      const wsTimer = setTimeout(connectWebSocket, 1000);
      
      // 주기적 폴링 시작
      pollIntervalRef.current = setInterval(pollBackendData, pollInterval);
      
      return () => {
        clearTimeout(wsTimer);
        disconnect();
      };
    }
  }, [autoConnect, pollBackendData, connectWebSocket, disconnect, pollInterval]);

  return {
    // 데이터
    services,
    systemStats,
    connectionStatus,
    
    // 알림
    alerts: alerts.filter(alert => !alert.dismissed),
    allAlerts: alerts,
    dismissAlert,
    dismissAllAlerts,
    
    // 연결 제어
    refresh,
    disconnect,
    connectWebSocket,
    
    // 상태 확인
    isConnected: connectionStatus.isConnected || connectionStatus.isHealthy,
    isHealthy: connectionStatus.isHealthy,
    activeAlertsCount: alerts.filter(alert => !alert.dismissed).length,
    
    // 유틸리티
    getTotalCollected: () => services.reduce((sum, s) => sum + s.collected_count, 0),
    getActiveServices: () => services.filter(s => s.status === 'running').length,
    getAverageSuccessRate: () => {
      if (services.length === 0) return 0;
      return services.reduce((sum, s) => sum + s.success_rate, 0) / services.length;
    }
  };
};