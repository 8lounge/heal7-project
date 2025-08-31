/**
 * 🔌 실제 크롤링 백엔드 API 클라이언트
 * - 포트 8003 백엔드와 실제 연동
 * - WebSocket 실시간 모니터링
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

interface APIStats {
  total_collected: number;
  avg_success_rate: number;
  avg_response_time: number;
  avg_quality: number;
  active_services: number;
  timestamp: string;
}

interface WebSocketMessage {
  type: 'service_update' | 'system_stats' | 'health_check';
  data: any;
  timestamp: string;
}

export class CrawlingAPIClient {
  private baseURL: string;
  private wsURL: string;
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000;

  constructor(baseURL?: string) {
    // 동적 백엔드 URL 결정
    if (baseURL) {
      this.baseURL = baseURL;
    } else if (typeof window !== 'undefined') {
      const currentHost = window.location.hostname;
      const currentProtocol = window.location.protocol;
      
      if (currentHost === 'crawling.heal7.com') {
        // 프로덕션: 같은 도메인의 API 사용 (NGINX 프록시)
        this.baseURL = `${currentProtocol}//crawling.heal7.com`;
      } else if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
        // 로컬 개발환경
        this.baseURL = 'http://localhost:8003';
      } else {
        // 기타 환경
        this.baseURL = `${currentProtocol}//${currentHost}:8003`;
      }
    } else {
      // SSR 환경 또는 기본값
      this.baseURL = 'http://localhost:8003';
    }
    
    // WebSocket URL 설정
    if (typeof window !== 'undefined' && window.location.hostname === 'crawling.heal7.com') {
      // 프로덕션: NGINX 프록시를 통한 WebSocket 연결
      this.wsURL = `wss://crawling.heal7.com/ws/monitor`;
    } else {
      // 로컬 개발환경
      this.wsURL = this.baseURL.replace('http://', 'ws://').replace('https://', 'wss://') + '/ws/monitor';
    }
  }

  /**
   * 🩺 헬스체크 - 백엔드 연결 상태 확인
   */
  async checkHealth(): Promise<{ status: string; service: string; port: number }> {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('❌ 헬스체크 실패:', error);
      throw new Error('백엔드 연결 실패');
    }
  }

  /**
   * 📊 크롤링 서비스 목록 조회
   */
  async getServices(): Promise<CrawlingService[]> {
    try {
      const response = await fetch(`${this.baseURL}/api/services`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      return data.services;
    } catch (error) {
      console.error('❌ 서비스 목록 조회 실패:', error);
      return [];
    }
  }

  /**
   * 📈 전체 통계 조회
   */
  async getStats(): Promise<APIStats | null> {
    try {
      const response = await fetch(`${this.baseURL}/api/stats`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('❌ 통계 조회 실패:', error);
      return null;
    }
  }

  /**
   * 🔌 WebSocket 실시간 연결
   */
  connectWebSocket(
    onMessage: (data: WebSocketMessage) => void,
    onConnected: () => void,
    onDisconnected: () => void,
    onError: (error: Event) => void
  ): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return; // 이미 연결됨
    }

    try {
      this.ws = new WebSocket(this.wsURL);
      
      this.ws.onopen = () => {
        console.log('🔌 WebSocket 연결 성공:', this.wsURL);
        this.reconnectAttempts = 0;
        onConnected();
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          onMessage(message);
        } catch (error) {
          console.error('❌ WebSocket 메시지 파싱 오류:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('🔌 WebSocket 연결 해제:', event.code, event.reason);
        this.ws = null;
        onDisconnected();
        
        // 자동 재연결
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          const delay = this.reconnectTimeout * Math.pow(2, this.reconnectAttempts - 1);
          console.log(`🔄 ${delay}ms 후 재연결 시도 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          
          setTimeout(() => {
            this.connectWebSocket(onMessage, onConnected, onDisconnected, onError);
          }, delay);
        }
      };

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket 오류:', error);
        onError(error);
      };

    } catch (error) {
      console.error('❌ WebSocket 연결 실패:', error);
      onError(error as Event);
    }
  }

  /**
   * 🔌 WebSocket 연결 해제
   */
  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.reconnectAttempts = 0;
    }
  }

  /**
   * 📡 연결 상태 확인
   */
  isWebSocketConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  /**
   * 🧪 연결 테스트 - 헬스체크 + 서비스 목록 조회
   */
  async testConnection(): Promise<{
    healthy: boolean;
    services: number;
    error?: string;
  }> {
    try {
      const health = await this.checkHealth();
      const services = await this.getServices();
      
      return {
        healthy: health.status === 'healthy',
        services: services.length
      };
    } catch (error) {
      return {
        healthy: false,
        services: 0,
        error: error instanceof Error ? error.message : '알 수 없는 오류'
      };
    }
  }

  /**
   * 🔧 크롤링 작업 목록 조회
   */
  async getJobs(): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseURL}/api/jobs`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      return data.jobs;
    } catch (error) {
      console.error('❌ 작업 목록 조회 실패:', error);
      return [];
    }
  }

  /**
   * 🤖 AI 분석 통계 조회
   */
  async getAIStats(): Promise<any> {
    try {
      const response = await fetch(`${this.baseURL}/api/ai-stats`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('❌ AI 통계 조회 실패:', error);
      return null;
    }
  }

  /**
   * 📊 데이터 관리 - 수집된 데이터 목록
   */
  async getDataItems(): Promise<any> {
    try {
      const response = await fetch(`${this.baseURL}/api/data`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('❌ 데이터 목록 조회 실패:', error);
      return null;
    }
  }

  /**
   * ⚙️ 시스템 설정 조회
   */
  async getSettings(): Promise<any> {
    try {
      const response = await fetch(`${this.baseURL}/api/settings`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('❌ 설정 조회 실패:', error);
      return null;
    }
  }

  /**
   * ⚙️ 시스템 설정 업데이트
   */
  async updateSettings(settings: any): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/api/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('❌ 설정 업데이트 실패:', error);
      return false;
    }
  }
}

// 싱글톤 인스턴스
export const crawlingAPI = new CrawlingAPIClient();