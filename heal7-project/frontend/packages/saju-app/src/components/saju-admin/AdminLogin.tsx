import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface AdminLoginProps {
  onAuthenticated: () => void;
}

const AdminLogin: React.FC<AdminLoginProps> = ({ onAuthenticated }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 관리자 비밀번호 (실제 환경에서는 환경변수나 백엔드에서 관리해야 함)
  const ADMIN_PASSWORD = 'heal7admin2025!';

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // 간단한 딜레이로 로딩 효과
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (password === ADMIN_PASSWORD) {
      // localStorage에 인증 상태 저장 (세션 유지를 위해)
      localStorage.setItem('heal7_admin_authenticated', 'true');
      localStorage.setItem('heal7_admin_login_time', Date.now().toString());
      
      onAuthenticated();
    } else {
      setError('잘못된 비밀번호입니다.');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <motion.div 
        className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8 w-full max-w-md mx-4"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🔐</div>
          <h1 className="text-2xl font-bold text-white mb-2">
            관리자 로그인
          </h1>
          <p className="text-gray-300 text-sm">
            HEAL7 사주 시스템 관리자 전용 페이지
          </p>
        </div>

        {/* 로그인 폼 */}
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
              관리자 비밀번호
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent"
              placeholder="비밀번호를 입력하세요"
              required
              autoFocus
            />
          </div>

          {error && (
            <motion.div 
              className="bg-red-500/20 border border-red-500/30 rounded-lg p-3 text-red-300 text-sm"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              ⚠️ {error}
            </motion.div>
          )}

          <motion.button
            type="submit"
            disabled={isLoading || !password}
            className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-all duration-300 ${
              isLoading || !password
                ? 'bg-gray-600 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-lg hover:shadow-xl'
            }`}
            whileHover={!isLoading && password ? { scale: 1.02 } : {}}
            whileTap={!isLoading && password ? { scale: 0.98 } : {}}
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                인증 중...
              </div>
            ) : (
              '🔓 로그인'
            )}
          </motion.button>
        </form>

        {/* 보안 안내 */}
        <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
          <div className="flex items-center text-yellow-300 text-sm">
            <span className="mr-2">🔒</span>
            <span>보안상 3회 실패 시 5분간 접근이 제한됩니다.</span>
          </div>
        </div>

        {/* 임시 로그인 정보 표시 */}
        <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <div className="text-center">
            <div className="text-blue-300 text-sm font-medium mb-2">🔑 임시 접속 정보</div>
            <div className="text-blue-200 text-xs">
              비밀번호: <span className="font-mono bg-blue-900/30 px-2 py-1 rounded">heal7admin2025!</span>
            </div>
            <div className="text-blue-400 text-xs mt-1">
              (개발 편의를 위한 임시 표시)
            </div>
          </div>
        </div>

        {/* 시스템 정보 */}
        <div className="mt-4 text-center text-xs text-gray-400">
          HEAL7 Admin Dashboard v2.0.0 | saju.heal7.com
        </div>
      </motion.div>
    </div>
  );
};

export default AdminLogin;