import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';

interface LoginProps {
  onLoginSuccess?: (token: string, userInfo: any) => void;
  onSwitchToRegister?: () => void;
}

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user_info: {
    id: string;
    username: string;
    email: string;
    full_name: string | null;
  };
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [formData, setFormData] = useState<LoginRequest>({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const showToast = (message: string, type: 'success' | 'error' = 'success') => {
    // 간단한 토스트 알림 (나중에 실제 toast 라이브러리로 교체 가능)
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-[70] px-6 py-3 rounded-lg text-white font-medium ${
      type === 'success' ? 'bg-green-600' : 'bg-red-600'
    }`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => document.body.removeChild(toast), 3000);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '로그인에 실패했습니다');
      }

      const data: LoginResponse = await response.json();
      
      // useAuth를 통해 로그인 상태 업데이트 (localStorage 저장도 포함됨)
      login(data.access_token, data.user_info);

      showToast(`안녕하세요, ${data.user_info.username || data.user_info.full_name || data.user_info.email || '사용자'}님!`, 'success');

      // 부모 컴포넌트에 성공 알림
      if (onLoginSuccess) {
        onLoginSuccess(data.access_token, data.user_info);
      }

    } catch (error) {
      showToast(error instanceof Error ? error.message : '로그인 중 오류가 발생했습니다', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">🔮 로그인</h2>
        <p className="text-white/80">
          HEAL7 사주명리학 서비스에 로그인하세요
        </p>
      </div>
      <div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="email" className="text-white font-medium block text-sm">이메일</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={handleInputChange}
              required
              disabled={isLoading}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-white/50 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            />
          </div>
          
          <div className="space-y-2">
            <label htmlFor="password" className="text-white font-medium block text-sm">비밀번호</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="비밀번호를 입력하세요"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={isLoading}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-white/50 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            />
          </div>

          <motion.button 
            type="submit" 
            className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-300 ${
              isLoading 
                ? 'bg-gray-600 cursor-not-allowed' 
                : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 shadow-lg hover:shadow-xl'
            } text-white`}
            disabled={isLoading}
            whileHover={!isLoading ? { scale: 1.02 } : {}}
            whileTap={!isLoading ? { scale: 0.98 } : {}}
          >
            {isLoading ? '로그인 중...' : '로그인'}
          </motion.button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-white/70">
            계정이 없으신가요?{' '}
            <button
              type="button"
              onClick={onSwitchToRegister}
              className="text-purple-300 hover:text-purple-200 underline font-medium transition-colors"
            >
              회원가입
            </button>
          </p>
        </div>

        <div className="mt-4 p-3 bg-white/5 border border-white/10 rounded-lg">
          <h4 className="text-sm font-medium mb-2 text-white">✨ 테스트 계정</h4>
          <p className="text-xs text-white/60">
            이메일: admin@heal7.com<br />
            비밀번호: admin123
          </p>
        </div>
      </div>
    </div>
  );
};