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
      // localStorage에 인증 상태 저장 (7일간 세션 유지)
      localStorage.setItem('heal7_admin_authenticated', 'true');
      localStorage.setItem('heal7_admin_login_time', Date.now().toString());
      localStorage.setItem('heal7_admin_session_id', 'admin_' + Date.now()); // 세션 ID 추가
      
      console.log('Admin login successful - session will persist for 7 days');
      onAuthenticated();
    } else {
      setError('잘못된 비밀번호입니다.');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="min-h-[60vh] flex items-center justify-center bg-gradient-to-br from-purple-900/20 via-violet-900/10 to-fuchsia-900/20">
      <motion.div 
        className="bg-purple-500/10 backdrop-blur-lg rounded-3xl border border-purple-400/30 p-8 w-full max-w-md mx-4 shadow-2xl shadow-purple-500/20 relative overflow-hidden"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Neon glow background effects */}
        <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-violet-600 rounded-3xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-purple-800/20 via-violet-700/10 to-fuchsia-800/20 rounded-3xl"></div>
        <div className="relative z-10">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4 filter drop-shadow-lg">🔐</div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-violet-200 bg-clip-text text-transparent mb-2 drop-shadow-lg">
            관리자 로그인
          </h1>
          <p className="text-purple-200/80 text-sm font-medium">
            HEAL7 사주 시스템 관리자 전용 페이지
          </p>
        </div>

        {/* 로그인 폼 */}
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-purple-200 mb-2">
              관리자 비밀번호
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-purple-500/10 backdrop-blur-sm border border-purple-400/30 rounded-xl text-white placeholder-purple-300/60 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-300/50 focus:bg-purple-400/10 transition-all duration-300 shadow-inner"
              placeholder="비밀번호를 입력하세요"
              required
              autoFocus
            />
          </div>

          {error && (
            <motion.div 
              className="bg-red-500/20 backdrop-blur-sm border border-red-400/40 rounded-xl p-3 text-red-200 text-sm shadow-lg"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              ⚠️ {error}
            </motion.div>
          )}

          <motion.button
            type="submit"
            disabled={isLoading || !password}
            className={`w-full py-4 px-6 rounded-xl font-bold text-white transition-all duration-300 backdrop-blur-sm ${
              isLoading || !password
                ? 'bg-gray-600/50 cursor-not-allowed border border-gray-500/30'
                : 'bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-500 hover:to-violet-500 shadow-xl shadow-purple-500/25 hover:shadow-2xl hover:shadow-purple-500/40 border border-purple-400/50 hover:border-purple-300/70'
            }`}
            whileHover={!isLoading && password ? { scale: 1.02, boxShadow: "0 25px 50px -12px rgba(139, 92, 246, 0.5)" } : {}}
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
        <div className="mt-6 p-4 bg-amber-500/10 backdrop-blur-sm border border-amber-400/30 rounded-xl shadow-lg">
          <div className="flex items-center text-amber-200 text-sm">
            <span className="mr-2 text-lg">🔒</span>
            <span>보안상 3회 실패 시 5분간 접근이 제한됩니다.</span>
          </div>
        </div>

        {/* 임시 로그인 정보 표시 */}
        <div className="mt-6 p-4 bg-blue-500/10 backdrop-blur-sm border border-blue-400/30 rounded-xl shadow-lg">
          <div className="text-center">
            <div className="text-blue-200 text-sm font-bold mb-2 flex items-center justify-center">
              <span className="mr-2">🔑</span>
              임시 접속 정보
            </div>
            <div className="text-blue-100 text-xs">
              비밀번호: <span className="font-mono bg-blue-600/30 backdrop-blur-sm px-3 py-1 rounded-lg border border-blue-400/40">heal7admin2025!</span>
            </div>
            <div className="text-blue-300/80 text-xs mt-2">
              (개발 편의를 위한 임시 표시)
            </div>
          </div>
        </div>

        {/* 시스템 정보 */}
        <div className="mt-4 text-center text-xs text-purple-300/60 font-medium">
          HEAL7 Admin Dashboard v2.0.0 | saju.heal7.com
        </div>
        </div>
      </motion.div>
    </div>
  );
};

export default AdminLogin;