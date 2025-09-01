import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';
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
  const { toast } = useToast();
  const { login } = useAuth();

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

      toast({
        title: "로그인 성공",
        description: `안녕하세요, ${data.user_info.username || data.user_info.full_name || data.user_info.email || '사용자'}님!`,
      });

      // 부모 컴포넌트에 성공 알림
      if (onLoginSuccess) {
        onLoginSuccess(data.access_token, data.user_info);
      }

    } catch (error) {
      toast({
        variant: "destructive",
        title: "로그인 실패",
        description: error instanceof Error ? error.message : '로그인 중 오류가 발생했습니다',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto card-cosmic p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">🔮 로그인</h2>
        <p className="text-white/80">
          HEAL7 사주명리학 서비스에 로그인하세요
        </p>
      </div>
      <div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-white font-medium">이메일</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={handleInputChange}
              required
              disabled={isLoading}
              className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-purple-400 focus:ring-purple-400"
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="password" className="text-white font-medium">비밀번호</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="비밀번호를 입력하세요"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={isLoading}
              className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-purple-400 focus:ring-purple-400"
            />
          </div>

          <Button 
            type="submit" 
            className="w-full btn-mystic"
            disabled={isLoading}
          >
            {isLoading ? '로그인 중...' : '로그인'}
          </Button>
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