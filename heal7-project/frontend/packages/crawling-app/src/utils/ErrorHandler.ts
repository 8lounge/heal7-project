/**
 * 🚨 크롤링 시스템 에러 핸들링
 * - 실제 API 에러 처리
 * - 사용자 친화적 에러 메시지
 * - 에러 로깅 및 리포팅
 */

export interface APIError {
  code: string;
  message: string;
  details?: any;
  timestamp: string;
  source: 'api' | 'websocket' | 'network' | 'validation' | 'system';
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface ErrorContext {
  component: string;
  action: string;
  userId?: string;
  sessionId?: string;
  additionalData?: any;
}

class ErrorHandler {
  private errorQueue: APIError[] = [];
  private maxQueueSize = 100;
  private reportingEndpoint = '/api/errors/report';

  /**
   * API 응답 오류 처리
   */
  handleAPIError(response: Response, context: ErrorContext): APIError {
    const error: APIError = {
      code: `HTTP_${response.status}`,
      message: this.getHTTPErrorMessage(response.status),
      details: {
        url: response.url,
        method: response.type || 'GET',
        status: response.status,
        statusText: response.statusText,
        context
      },
      timestamp: new Date().toISOString(),
      source: 'api',
      severity: this.getErrorSeverity(response.status)
    };

    this.logError(error);
    return error;
  }

  /**
   * WebSocket 연결 오류 처리
   */
  handleWebSocketError(event: Event, context: ErrorContext): APIError {
    const error: APIError = {
      code: 'WEBSOCKET_ERROR',
      message: 'WebSocket 연결에 실패했습니다. 실시간 업데이트가 제한될 수 있습니다.',
      details: {
        event: event.type,
        context
      },
      timestamp: new Date().toISOString(),
      source: 'websocket',
      severity: 'medium'
    };

    this.logError(error);
    return error;
  }

  /**
   * 네트워크 오류 처리
   */
  handleNetworkError(error: Error, context: ErrorContext): APIError {
    const apiError: APIError = {
      code: 'NETWORK_ERROR',
      message: '네트워크 연결을 확인해주세요. 서버에 접근할 수 없습니다.',
      details: {
        originalError: error.message,
        stack: error.stack,
        context
      },
      timestamp: new Date().toISOString(),
      source: 'network',
      severity: 'high'
    };

    this.logError(apiError);
    return apiError;
  }

  /**
   * 검증 오류 처리
   */
  handleValidationError(field: string, value: any, rules: string[], context: ErrorContext): APIError {
    const error: APIError = {
      code: 'VALIDATION_ERROR',
      message: `입력값이 올바르지 않습니다: ${field}`,
      details: {
        field,
        value,
        rules,
        context
      },
      timestamp: new Date().toISOString(),
      source: 'validation',
      severity: 'low'
    };

    this.logError(error);
    return error;
  }

  /**
   * 시스템 오류 처리
   */
  handleSystemError(error: Error, context: ErrorContext): APIError {
    const apiError: APIError = {
      code: 'SYSTEM_ERROR',
      message: '시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
      details: {
        originalError: error.message,
        stack: error.stack,
        context
      },
      timestamp: new Date().toISOString(),
      source: 'system',
      severity: 'critical'
    };

    this.logError(apiError);
    return apiError;
  }

  /**
   * 에러 로깅
   */
  private logError(error: APIError): void {
    // 콘솔에 에러 출력
    console.error(`[${error.severity.toUpperCase()}] ${error.code}: ${error.message}`, error.details);

    // 에러 큐에 추가
    this.errorQueue.push(error);
    if (this.errorQueue.length > this.maxQueueSize) {
      this.errorQueue.shift(); // 오래된 에러 제거
    }

    // 중요한 에러는 즉시 서버에 리포트
    if (error.severity === 'high' || error.severity === 'critical') {
      this.reportErrorToServer(error);
    }
  }

  /**
   * 서버에 에러 리포트
   */
  private async reportErrorToServer(error: APIError): Promise<void> {
    try {
      await fetch(this.reportingEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(error),
      });
    } catch (reportingError) {
      console.error('에러 리포팅 실패:', reportingError);
    }
  }

  /**
   * HTTP 상태 코드별 에러 메시지
   */
  private getHTTPErrorMessage(status: number): string {
    const errorMessages: { [key: number]: string } = {
      400: '잘못된 요청입니다. 입력값을 확인해주세요.',
      401: '인증이 필요합니다. 다시 로그인해주세요.',
      403: '접근 권한이 없습니다.',
      404: '요청한 리소스를 찾을 수 없습니다.',
      408: '요청 시간이 초과되었습니다.',
      429: '너무 많은 요청을 보냈습니다. 잠시 후 다시 시도해주세요.',
      500: '서버 내부 오류가 발생했습니다.',
      502: '서버 게이트웨이 오류입니다.',
      503: '서비스를 사용할 수 없습니다. 잠시 후 다시 시도해주세요.',
      504: '서버 응답 시간이 초과되었습니다.',
    };

    return errorMessages[status] || `알 수 없는 오류가 발생했습니다 (${status})`;
  }

  /**
   * HTTP 상태 코드별 심각도 결정
   */
  private getErrorSeverity(status: number): APIError['severity'] {
    if (status >= 500) return 'critical';
    if (status >= 400) return 'medium';
    return 'low';
  }

  /**
   * 에러 큐 조회
   */
  getRecentErrors(limit: number = 10): APIError[] {
    return this.errorQueue.slice(-limit);
  }

  /**
   * 에러 큐 초기화
   */
  clearErrors(): void {
    this.errorQueue = [];
  }

  /**
   * 특정 심각도 이상의 에러 개수 조회
   */
  getErrorCount(minSeverity: APIError['severity'] = 'low'): number {
    const severityLevels = ['low', 'medium', 'high', 'critical'];
    const minIndex = severityLevels.indexOf(minSeverity);
    
    return this.errorQueue.filter(error => 
      severityLevels.indexOf(error.severity) >= minIndex
    ).length;
  }
}

// 싱글톤 인스턴스
export const errorHandler = new ErrorHandler();

/**
 * API 호출 래퍼 함수 - 자동 에러 처리
 */
export async function safeAPICall<T>(
  url: string, 
  options: RequestInit = {}, 
  context: ErrorContext
): Promise<{ data: T | null; error: APIError | null }> {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const error = errorHandler.handleAPIError(response, context);
      return { data: null, error };
    }

    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      const error = errorHandler.handleNetworkError(err, context);
      return { data: null, error };
    } else {
      const error = errorHandler.handleSystemError(err as Error, context);
      return { data: null, error };
    }
  }
}

/**
 * React Hook: 에러 상태 관리
 */
export function useErrorHandler() {
  return {
    handleError: (error: Error | Response, context: ErrorContext) => {
      if (error instanceof Response) {
        return errorHandler.handleAPIError(error, context);
      } else {
        return errorHandler.handleSystemError(error, context);
      }
    },
    getRecentErrors: errorHandler.getRecentErrors.bind(errorHandler),
    clearErrors: errorHandler.clearErrors.bind(errorHandler),
    getErrorCount: errorHandler.getErrorCount.bind(errorHandler),
    safeAPICall: (url: string, options: RequestInit = {}, context: ErrorContext) =>
      safeAPICall(url, options, context)
  };
}

export default errorHandler;