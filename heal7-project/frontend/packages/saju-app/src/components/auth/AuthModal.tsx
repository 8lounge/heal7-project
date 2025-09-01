import React, { useState } from 'react';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Login } from './Login';
import { Register } from './Register';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAuthSuccess?: (token: string, userInfo: any) => void;
  defaultMode?: 'login' | 'register';
}

export const AuthModal: React.FC<AuthModalProps> = ({ 
  isOpen, 
  onClose, 
  onAuthSuccess,
  defaultMode = 'login' 
}) => {
  const [mode, setMode] = useState<'login' | 'register'>(defaultMode);

  const handleAuthSuccess = (token: string, userInfo: any) => {
    if (onAuthSuccess) {
      onAuthSuccess(token, userInfo);
    }
    onClose();
  };

  const switchToRegister = () => setMode('register');
  const switchToLogin = () => setMode('login');

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px] bg-transparent border-none p-0 shadow-none">
        <DialogTitle className="sr-only">
          {mode === 'login' ? '로그인' : '회원가입'}
        </DialogTitle>
        <DialogDescription className="sr-only">
          {mode === 'login' ? '로그인 폼' : '회원가입 폼'}
        </DialogDescription>
        <div className="relative">
          {mode === 'login' ? (
            <Login 
              onLoginSuccess={handleAuthSuccess}
              onSwitchToRegister={switchToRegister}
            />
          ) : (
            <Register 
              onRegisterSuccess={handleAuthSuccess}
              onSwitchToLogin={switchToLogin}
            />
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};