import { LoginRequest, RegisterRequest, AuthResponse, User } from '../types/auth'
import { API_BASE_URL as BASE_URL } from './config'

const API_BASE_URL = `${BASE_URL}/api/auth`

class AuthApiService {
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    })

    if (!response.ok) {
      const error = await response.json()
      // 422 에러시 Pydantic 검증 오류 메시지 파싱
      if (error.detail && Array.isArray(error.detail)) {
        const message = error.detail.map((item: any) => item.msg).join(', ')
        throw new Error(message)
      }
      throw new Error(error.detail || '회원가입에 실패했습니다')
    }

    return response.json()
  }

  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '로그인에 실패했습니다')
    }

    return response.json()
  }

  async getCurrentUser(token: string): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error('사용자 정보를 가져올 수 없습니다')
    }

    return response.json()
  }

  async logout(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/logout`, {
      method: 'POST',
    })

    if (!response.ok) {
      throw new Error('로그아웃에 실패했습니다')
    }
  }

  async refreshToken(token: string): Promise<{ access_token: string; token_type: string }> {
    const response = await fetch(`${API_BASE_URL}/refresh`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error('토큰 갱신에 실패했습니다')
    }

    return response.json()
  }
}

export const authApi = new AuthApiService()