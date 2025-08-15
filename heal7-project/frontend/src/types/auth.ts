export interface User {
  id: number
  email: string
  full_name: string
  phone?: string
  is_active: boolean
  email_verified: boolean
  created_at: string
  last_login?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
  phone?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface AuthContextType {
  user: User | null
  token: string | null
  login: (credentials: LoginRequest) => Promise<void>
  register: (userData: RegisterRequest) => Promise<void>
  logout: () => void
  isLoading: boolean
}