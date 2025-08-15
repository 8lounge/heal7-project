import React, { createContext, useContext, useState, useEffect } from 'react'
import { User, LoginRequest, RegisterRequest, AuthContextType } from '../types/auth'
import { authApi } from '../services/authApi'

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: React.ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // 로컬 스토리지에서 토큰 복원
  useEffect(() => {
    const storedToken = localStorage.getItem('heal7_token')
    const storedUser = localStorage.getItem('heal7_user')

    if (storedToken && storedUser) {
      try {
        setToken(storedToken)
        setUser(JSON.parse(storedUser))
      } catch (error) {
        console.error('Failed to parse stored user data:', error)
        localStorage.removeItem('heal7_token')
        localStorage.removeItem('heal7_user')
      }
    }
    
    setIsLoading(false)
  }, [])

  const login = async (credentials: LoginRequest) => {
    try {
      setIsLoading(true)
      const response = await authApi.login(credentials)
      
      setUser(response.user)
      setToken(response.access_token)
      
      // 로컬 스토리지에 저장
      localStorage.setItem('heal7_token', response.access_token)
      localStorage.setItem('heal7_user', JSON.stringify(response.user))
    } catch (error) {
      console.error('Login error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData: RegisterRequest) => {
    try {
      setIsLoading(true)
      const response = await authApi.register(userData)
      
      setUser(response.user)
      setToken(response.access_token)
      
      // 로컬 스토리지에 저장
      localStorage.setItem('heal7_token', response.access_token)
      localStorage.setItem('heal7_user', JSON.stringify(response.user))
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('heal7_token')
    localStorage.removeItem('heal7_user')
    
    // 로그아웃 API 호출 (실패해도 로컬 상태는 정리됨)
    authApi.logout().catch(console.error)
  }

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isLoading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}