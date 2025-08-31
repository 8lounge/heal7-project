import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';

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
  const { toast } = useToast();

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
      
      // 토큰을 localStorage에 저장
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user_info', JSON.stringify(data.user_info));

      toast({
        title: "회원가입 성공",
        description: `환영합니다, ${data.user_info.username}님!`,
      });

      // 부모 컴포넌트에 성공 알림
      if (onRegisterSuccess) {
        onRegisterSuccess(data.access_token, data.user_info);
      }

    } catch (error) {
      toast({
        variant: "destructive",
        title: "회원가입 실패",
        description: error instanceof Error ? error.message : '회원가입 중 오류가 발생했습니다',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto card-cosmic p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">✨ 회원가입</h2>
        <p className="text-white/80">
          HEAL7 사주명리학 서비스에 가입하세요
        </p>
      </div>
      <div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username" className="text-white font-medium">사용자명 *</Label>
            <Input
              id="username"
              name="username"
              type="text"
              placeholder="사용자명 (3자 이상)"
              value={formData.username}
              onChange={handleInputChange}
              required
              minLength={3}
              disabled={isLoading}
              className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-purple-400 focus:ring-purple-400"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="email" className="text-white font-medium">이메일 *</Label>
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
            <Label htmlFor="password" className="text-white font-medium">비밀번호 *</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="비밀번호 (6자 이상)"
              value={formData.password}
              onChange={handleInputChange}
              required
              minLength={6}
              disabled={isLoading}
              className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-purple-400 focus:ring-purple-400"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="full_name" className="text-white/80 font-medium">실명 (선택)</Label>
            <Input
              id="full_name"
              name="full_name"
              type="text"
              placeholder="실명"
              value={formData.full_name}
              onChange={handleInputChange}
              disabled={isLoading}
              className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-purple-400 focus:ring-purple-400"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="birth_date" className="text-white/80 font-medium">생년월일 (선택)</Label>
              <Input
                id="birth_date"
                name="birth_date"
                type="date"
                value={formData.birth_date}
                onChange={handleInputChange}
                disabled={isLoading}
                className="bg-white/10 border-white/20 text-white focus:border-purple-400 focus:ring-purple-400"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="birth_time" className="text-white/80 font-medium">출생시간 (선택)</Label>
              <Input
                id="birth_time"
                name="birth_time"
                type="time"
                value={formData.birth_time}
                onChange={handleInputChange}
                disabled={isLoading}
                className="bg-white/10 border-white/20 text-white focus:border-purple-400 focus:ring-purple-400"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="gender" className="text-white/80 font-medium">성별 (선택)</Label>
            <Select onValueChange={handleSelectChange} disabled={isLoading}>
              <SelectTrigger className="bg-white/10 border-white/20 text-white focus:border-purple-400 focus:ring-purple-400">
                <SelectValue placeholder="성별을 선택하세요" className="text-white/50" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-white/20">
                <SelectItem value="male" className="text-white hover:bg-white/10">남성</SelectItem>
                <SelectItem value="female" className="text-white hover:bg-white/10">여성</SelectItem>
                <SelectItem value="other" className="text-white hover:bg-white/10">기타</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button 
            type="submit" 
            className="w-full btn-mystic"
            disabled={isLoading}
          >
            {isLoading ? '가입 중...' : '회원가입'}
          </Button>
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