import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';

interface RegisterProps {
  onRegisterSuccess?: (token: string, userInfo: any) => void;
  onSwitchToLogin?: () => void;
}

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  birth_date?: string;
  birth_time?: string;
  gender?: 'male' | 'female' | 'other';
}

interface RegisterResponse {
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

export const Register: React.FC<RegisterProps> = ({ onRegisterSuccess, onSwitchToLogin }) => {
  const [formData, setFormData] = useState<RegisterRequest>({
    username: '',
    email: '',
    password: '',
    full_name: '',
    birth_date: '',
    birth_time: '',
    gender: undefined
  });
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const showToast = (message: string, type: 'success' | 'error' = 'success') => {
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

  const handleSelectChange = (value: string) => {
    setFormData(prev => ({
      ...prev,
      gender: value as 'male' | 'female' | 'other'
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // 빈 필드 제거
      const cleanedData = Object.fromEntries(
        Object.entries(formData).filter(([_, value]) => value !== '' && value !== undefined)
      );

      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(cleanedData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '회원가입에 실패했습니다');
      }

      const data: RegisterResponse = await response.json();
      
      // useAuth를 통해 로그인 상태 업데이트 (localStorage 저장도 포함됨)
      login(data.access_token, data.user_info);

      showToast(`환영합니다, ${data.user_info.username}님!`, 'success');

      // 부모 컴포넌트에 성공 알림
      if (onRegisterSuccess) {
        onRegisterSuccess(data.access_token, data.user_info);
      }

    } catch (error) {
      showToast(error instanceof Error ? error.message : '회원가입 중 오류가 발생했습니다', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">✨ 회원가입</h2>
        <p className="text-white/80">
          HEAL7 사주명리학 서비스에 가입하세요
        </p>
      </div>
      <div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="username" className="text-white font-medium block text-sm">사용자명 *</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="사용자명 (3자 이상)"
              value={formData.username}
              onChange={handleInputChange}
              required
              minLength={3}
              disabled={isLoading}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-white/50 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="email" className="text-white font-medium block text-sm">이메일 *</label>
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
            <label htmlFor="password" className="text-white font-medium block text-sm">비밀번호 *</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="비밀번호 (6자 이상)"
              value={formData.password}
              onChange={handleInputChange}
              required
              minLength={6}
              disabled={isLoading}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-white/50 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="full_name" className="text-white/80 font-medium block text-sm">실명 (선택)</label>
            <input
              id="full_name"
              name="full_name"
              type="text"
              placeholder="실명"
              value={formData.full_name}
              onChange={handleInputChange}
              disabled={isLoading}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-white/50 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label htmlFor="birth_date" className="text-white/80 font-medium block text-sm">생년월일 (선택)</label>
              <input
                id="birth_date"
                name="birth_date"
                type="date"
                value={formData.birth_date}
                onChange={handleInputChange}
                disabled={isLoading}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="birth_time" className="text-white/80 font-medium block text-sm">출생시간 (선택)</label>
              <input
                id="birth_time"
                name="birth_time"
                type="time"
                value={formData.birth_time}
                onChange={handleInputChange}
                disabled={isLoading}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="gender" className="text-white/80 font-medium block text-sm">성별 (선택)</label>
            <select 
              onChange={(e) => setFormData(prev => ({ ...prev, gender: e.target.value as 'male' | 'female' | 'other' }))} 
              disabled={isLoading}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            >
              <option value="" className="bg-gray-800 text-white">성별을 선택하세요</option>
              <option value="male" className="bg-gray-800 text-white">남성</option>
              <option value="female" className="bg-gray-800 text-white">여성</option>
              <option value="other" className="bg-gray-800 text-white">기타</option>
            </select>
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
            {isLoading ? '가입 중...' : '회원가입'}
          </motion.button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-white/70">
            이미 계정이 있으신가요?{' '}
            <button
              type="button"
              onClick={onSwitchToLogin}
              className="text-purple-300 hover:text-purple-200 underline font-medium transition-colors"
            >
              로그인
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};