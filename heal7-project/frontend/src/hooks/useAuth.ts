import { useState, useEffect } from 'react';

export interface User {
  id: string;
  username: string;
  email: string;
  full_name: string | null;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  isLoading: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    token: null,
    isLoading: true
  });

  // 토큰 유효성 검증
  const verifyToken = async (token: string): Promise<boolean> => {
    try {
      const response = await fetch('/api/auth/test-protected', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.ok;
    } catch (error) {
      console.error('Token verification failed:', error);
      return false;
    }
  };

  // 로그인 함수
  const login = (token: string, userInfo: User) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_info', JSON.stringify(userInfo));
    
    setAuthState({
      isAuthenticated: true,
      user: userInfo,
      token: token,
      isLoading: false
    });
  };

  // 로그아웃 함수
  const logout = async () => {
    const token = localStorage.getItem('access_token');
    
    if (token) {
      try {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_info');
    
    setAuthState({
      isAuthenticated: false,
      user: null,
      token: null,
      isLoading: false
    });
  };

  // 토큰 갱신 함수
  const refreshToken = async (): Promise<boolean> => {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      return false;
    }

    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        
        setAuthState(prev => ({
          ...prev,
          token: data.access_token
        }));
        
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }

    return false;
  };

  // 프로필 조회 함수
  const fetchProfile = async (token: string): Promise<User | null> => {
    try {
      const response = await fetch('/api/auth/profile', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Profile fetch failed:', error);
    }

    return null;
  };

  // 초기 인증 상태 확인
  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('access_token');
      const userInfo = localStorage.getItem('user_info');

      if (!token) {
        setAuthState(prev => ({ ...prev, isLoading: false }));
        return;
      }

      // 토큰 유효성 검증
      const isValid = await verifyToken(token);
      
      if (isValid && userInfo) {
        try {
          const user = JSON.parse(userInfo);
          setAuthState({
            isAuthenticated: true,
            user: user,
            token: token,
            isLoading: false
          });
        } catch (error) {
          console.error('Failed to parse user info:', error);
          logout();
        }
      } else {
        // 토큰이 유효하지 않은 경우 갱신 시도
        const refreshSuccess = await refreshToken();
        
        if (refreshSuccess && userInfo) {
          try {
            const user = JSON.parse(userInfo);
            const newToken = localStorage.getItem('access_token');
            
            setAuthState({
              isAuthenticated: true,
              user: user,
              token: newToken,
              isLoading: false
            });
          } catch (error) {
            console.error('Failed to parse user info after refresh:', error);
            logout();
          }
        } else {
          logout();
        }
      }
    };

    initializeAuth();
  }, []);

  return {
    ...authState,
    login,
    logout,
    refreshToken,
    fetchProfile
  };
};