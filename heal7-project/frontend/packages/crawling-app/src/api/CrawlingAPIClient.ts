/**
 * 🌐 크롤링 시스템 API 클라이언트
 * - FastAPI 백엔드 연결
 * - WebSocket 실시간 통신
 * - REST API 인터페이스
 */

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

interface CrawlingStats {
  total_collected: number;
  avg_success_rate: number;
  avg_response_time: number;
  avg_quality: number;
  active_services: number;
  timestamp: string;
}

interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  version: string;
  uptime: string;
  database_status: 'connected' | 'disconnected';
  websocket_status: 'connected' | 'disconnected';
  last_check: string;
}

interface SystemSettings {
  autoRefresh: boolean;
  refreshInterval: number;
  notifications: boolean;
  soundAlerts: boolean;
  realTimeUpdates: boolean;
  darkMode: boolean;
  maxRetries: number;
  timeout: number;
  concurrentConnections: number;
  logLevel: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
}

interface CrawlerSettings {
  httpx: {
    enabled: boolean;
    timeout: number;
    maxRetries: number;
    userAgent: string;
  };
  playwright: {
    enabled: boolean;
    headless: boolean;
    timeout: number;
    viewport: { width: number; height: number };
  };
  selenium: {
    enabled: boolean;
    headless: boolean;
    timeout: number;
    driver: 'chrome' | 'firefox' | 'edge';
  };
}

interface APIKeys {
  openai: string;
  anthropic: string;
  google: string;
}

interface Settings {
  system: SystemSettings;
  crawler: CrawlerSettings;
  apiKeys?: APIKeys;
}

class CrawlingAPIClient {
  private baseURL: string;
  private wsURL: string;
  private socket: WebSocket | null = null;
  private messageHandlers: Set<(message: any) => void> = new Set();

  constructor() {
    // 프로덕션에서는 같은 도메인의 API를 사용
    this.baseURL = window.location.origin;
    this.wsURL = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}`;
  }

  /**
   * 🏥 헬스체크 API
   */
  async checkHealth(): Promise<HealthStatus | null> {
    try {
      const response = await fetch(`${this.baseURL}/api/health`);
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      console.error('Health check failed:', error);
      return null;
    }
  }

  /**
   * 📋 서비스 목록 조회
   */
  async getServices(): Promise<CrawlingService[]> {
    try {
      const response = await fetch(`${this.baseURL}/api/services`);
      if (response.ok) {
        return await response.json();
      }
      return [];
    } catch (error) {
      console.error('Failed to fetch services:', error);
      return [];
    }
  }

  /**
   * 📊 통계 정보 조회
   */
  async getStats(): Promise<CrawlingStats | null> {
    try {
      const response = await fetch(`${this.baseURL}/api/stats`);
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      console.error('Failed to fetch stats:', error);
      return null;
    }
  }

  /**
   * ⚙️ 설정 정보 조회
   */
  async getSettings(): Promise<Settings | null> {
    try {
      const response = await fetch(`${this.baseURL}/api/settings`);
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      return null;
    }
  }

  /**
   * 💾 설정 정보 업데이트
   */
  async updateSettings(settings: Settings): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/api/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });
      return response.ok;
    } catch (error) {
      console.error('Failed to update settings:', error);
      return false;
    }
  }

  /**
   * 🔌 WebSocket 연결
   */
  connectWebSocket(onMessage?: (message: any) => void, onConnected?: () => void, onDisconnected?: () => void, onError?: (error: any) => void): void {
    if (this.socket?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    try {
      this.socket = new WebSocket(`${this.wsURL}/ws`);
      
      this.socket.onopen = () => {
        console.log('🔌 WebSocket connected');
        if (onConnected) onConnected();
      };

      this.socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.messageHandlers.forEach(handler => handler(message));
          if (onMessage) onMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.socket.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        if (onError) onError(error);
      };

      this.socket.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        this.socket = null;
        if (onDisconnected) onDisconnected();
      };
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      if (onError) onError(error);
    }
  }

  /**
   * 🔌 WebSocket 연결 해제
   */
  disconnectWebSocket(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.messageHandlers.clear();
    }
  }

  /**
   * 📨 WebSocket 메시지 핸들러 추가
   */
  addMessageHandler(handler: (message: any) => void): void {
    this.messageHandlers.add(handler);
  }

  /**
   * 📨 WebSocket 메시지 핸들러 제거
   */
  removeMessageHandler(handler: (message: any) => void): void {
    this.messageHandlers.delete(handler);
  }

  /**
   * 🚀 크롤링 서비스 시작
   */
  async startService(serviceId: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/api/services/${serviceId}/start`, {
        method: 'POST',
      });
      return response.ok;
    } catch (error) {
      console.error('Failed to start service:', error);
      return false;
    }
  }

  /**
   * ⏸️ 크롤링 서비스 일시정지
   */
  async pauseService(serviceId: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/api/services/${serviceId}/pause`, {
        method: 'POST',
      });
      return response.ok;
    } catch (error) {
      console.error('Failed to pause service:', error);
      return false;
    }
  }

  /**
   * ⏹️ 크롤링 서비스 정지
   */
  async stopService(serviceId: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/api/services/${serviceId}/stop`, {
        method: 'POST',
      });
      return response.ok;
    } catch (error) {
      console.error('Failed to stop service:', error);
      return false;
    }
  }
}

// 싱글톤 인스턴스 생성
export const crawlingAPI = new CrawlingAPIClient();
export default CrawlingAPIClient;