/**
 * 통합 API 서비스
 * 모든 API 호출을 중앙에서 관리하는 서비스
 */

import { API_CONFIG, ENV_CONFIG } from '../config/apiConfig'

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiService {
  private baseUrl: string
  private timeout: number

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL
    this.timeout = API_CONFIG.TIMEOUT
  }

  /**
   * HTTP 요청 실행
   */
  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`

    // 기본 설정
    const config: RequestInit = {
      timeout: this.timeout,
      ...options,
      headers: {
        ...API_CONFIG.HEADERS,
        ...options.headers
      }
    }

    if (ENV_CONFIG.DEBUG_API) {
      console.log('🌐 API Request:', { url, config })
    }

    try {
      // AbortController로 타임아웃 구현
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), this.timeout)

      const response = await fetch(url, {
        ...config,
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      // 응답 처리
      const contentType = response.headers.get('content-type')
      let data: any

      if (contentType && contentType.includes('application/json')) {
        data = await response.json()
      } else {
        data = await response.text()
      }

      if (ENV_CONFIG.DEBUG_API) {
        console.log('📡 API Response:', { status: response.status, data })
      }

      // 에러 응답 처리
      if (!response.ok) {
        throw new ApiError(
          data?.detail || data?.message || `HTTP ${response.status}`,
          response.status,
          data
        )
      }

      // 성공 응답
      return {
        success: true,
        data,
        message: data?.message
      }

    } catch (error) {
      if (error.name === 'AbortError') {
        throw new ApiError('Request timeout', 408)
      }

      if (error instanceof ApiError) {
        throw error
      }

      // 네트워크 에러 등
      throw new ApiError(
        error.message || 'Network error occurred',
        0,
        error
      )
    }
  }

  /**
   * GET 요청
   */
  async get<T = any>(endpoint: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    let url = endpoint

    // 쿼리 파라미터 추가
    if (params) {
      const searchParams = new URLSearchParams()
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, value.toString())
        }
      })

      if (searchParams.toString()) {
        url += `?${searchParams.toString()}`
      }
    }

    return this.request<T>(url, {
      method: 'GET',
      headers: API_CONFIG.getAuthHeaders()
    })
  }

  /**
   * POST 요청
   */
  async post<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      headers: API_CONFIG.getAuthHeaders(),
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * PUT 요청
   */
  async put<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      headers: API_CONFIG.getAuthHeaders(),
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * DELETE 요청
   */
  async delete<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
      headers: API_CONFIG.getAuthHeaders()
    })
  }

  /**
   * 재시도 로직이 있는 요청
   */
  async requestWithRetry<T = any>(
    requestFn: () => Promise<ApiResponse<T>>,
    maxRetries: number = ENV_CONFIG.RETRY_ATTEMPTS
  ): Promise<ApiResponse<T>> {
    let lastError: Error

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await requestFn()
      } catch (error) {
        lastError = error

        if (attempt === maxRetries) {
          break
        }

        // 재시도할 수 있는 에러인지 확인
        if (error instanceof ApiError && error.status >= 400 && error.status < 500) {
          // 4xx 에러는 재시도하지 않음
          break
        }

        // 재시도 대기
        await new Promise(resolve =>
          setTimeout(resolve, ENV_CONFIG.RETRY_DELAY * attempt)
        )

        if (ENV_CONFIG.DEBUG_API) {
          console.log(`🔄 Retrying request (${attempt}/${maxRetries})`)
        }
      }
    }

    throw lastError
  }

  /**
   * 토큰 갱신
   */
  refreshToken(newToken: string) {
    localStorage.setItem('admin_token', newToken)
  }

  /**
   * 토큰 제거
   */
  clearToken() {
    localStorage.removeItem('admin_token')
  }
}

// 싱글톤 인스턴스
export const apiService = new ApiService()

// 편의 메서드들
export const api = {
  get: <T = any>(endpoint: string, params?: Record<string, any>) =>
    apiService.get<T>(endpoint, params),

  post: <T = any>(endpoint: string, data?: any) =>
    apiService.post<T>(endpoint, data),

  put: <T = any>(endpoint: string, data?: any) =>
    apiService.put<T>(endpoint, data),

  delete: <T = any>(endpoint: string) =>
    apiService.delete<T>(endpoint),

  // 특정 API 호출들
  admin: {
    login: (credentials: { username: string; password: string }) =>
      apiService.post(API_CONFIG.ENDPOINTS.ADMIN.LOGIN, credentials),

    logout: () =>
      apiService.post(API_CONFIG.ENDPOINTS.ADMIN.LOGOUT),

    getSettings: () =>
      apiService.get(API_CONFIG.ENDPOINTS.ADMIN.SETTINGS),

    updateSettings: (settings: any) =>
      apiService.put(API_CONFIG.ENDPOINTS.ADMIN.SETTINGS, settings)
  },

  analytics: {
    getDashboard: () =>
      apiService.get(API_CONFIG.ENDPOINTS.ANALYTICS.DASHBOARD),

    getAiStats: () =>
      apiService.get(API_CONFIG.ENDPOINTS.ANALYTICS.AI_STATS),

    getUserStats: () =>
      apiService.get(API_CONFIG.ENDPOINTS.ANALYTICS.USER_STATS),

    getSystemHealth: () =>
      apiService.get(API_CONFIG.ENDPOINTS.ANALYTICS.SYSTEM_HEALTH)
  },

  inquiries: {
    getOverview: () =>
      apiService.get(API_CONFIG.ENDPOINTS.INQUIRIES.OVERVIEW),

    getList: (params: any) =>
      apiService.get(API_CONFIG.ENDPOINTS.INQUIRIES.LIST, params),

    reply: (id: number, reply: string) =>
      apiService.post(API_CONFIG.ENDPOINTS.INQUIRIES.REPLY(id), { admin_reply: reply }),

    getDetail: (id: number) =>
      apiService.get(API_CONFIG.ENDPOINTS.INQUIRIES.DETAIL(id)),

    updateStatus: (id: number, status: string) =>
      apiService.put(API_CONFIG.ENDPOINTS.INQUIRIES.STATUS(id), { status })
  }
}