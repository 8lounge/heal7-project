import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
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
    onAuthSuccess?.(token, userInfo);
    onClose();
  };

  const handleSwitchMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          className="fixed inset-0 z-[60] flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* 배경 오버레이 */}
          <motion.div 
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          
          {/* 모달 콘텐츠 */}
          <motion.div 
            className="relative z-10 w-full max-w-md"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ 
              type: "spring", 
              stiffness: 300, 
              damping: 30,
              duration: 0.5 
            }}
          >
            <div className="bg-black/30 backdrop-blur-lg rounded-2xl border border-white/20 shadow-2xl overflow-hidden">
              {/* 닫기 버튼 */}
              <div className="absolute top-4 right-4 z-20">
                <motion.button
                  onClick={onClose}
                  className="w-8 h-8 flex items-center justify-center bg-white/10 hover:bg-white/20 rounded-full text-white/60 hover:text-white text-xl transition-all duration-300"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  ×
                </motion.button>
              </div>

              {/* 모드별 컴포넌트 렌더링 */}
              <AnimatePresence mode="wait">
                {mode === 'login' ? (
                  <motion.div
                    key="login"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Login 
                      onLoginSuccess={handleAuthSuccess}
                      onSwitchToRegister={handleSwitchMode}
                    />
                  </motion.div>
                ) : (
                  <motion.div
                    key="register"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Register 
                      onRegisterSuccess={handleAuthSuccess}
                      onSwitchToLogin={handleSwitchMode}
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};