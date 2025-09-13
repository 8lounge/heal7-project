import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../../contexts/ThemeContext';

interface AdminLoginProps {
  onAuthenticated: () => void;
}

const AdminLogin: React.FC<AdminLoginProps> = ({ onAuthenticated }) => {
  const { isDarkMode } = useTheme();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // 통합 API 서비스 사용
      const { api } = await import('../../services/apiService');

      const response = await api.admin.login({
        username: username,
        password: password
      });

      if (response.success && response.data?.token) {
        const loginResult = response.data;

        // localStorage에 인증 상태 저장 (7일간 세션 유지)
        localStorage.setItem('heal7_admin_authenticated', 'true');
        localStorage.setItem('heal7_admin_login_time', Date.now().toString());
        localStorage.setItem('heal7_admin_session_id', 'admin_' + Date.now());
        localStorage.setItem('admin_token', loginResult.token); // API 토큰 저장
        localStorage.setItem('admin_user', JSON.stringify(loginResult.user)); // 사용자 정보 저장

        console.log('Admin login successful - session will persist for 7 days');
        console.log('User info:', loginResult.user);
        onAuthenticated();
      } else {
        setError('로그인 응답이 올바르지 않습니다.');
      }
    } catch (err: any) {
      console.error('Login error:', err);

      if (err.status === 401) {
        setError('아이디 또는 비밀번호가 잘못되었습니다.');
      } else if (err.status === 429) {
        setError('너무 많은 로그인 시도입니다. 잠시 후 다시 시도해주세요.');
      } else if (err.status === 0) {
        setError('서버에 연결할 수 없습니다. 네트워크를 확인해주세요.');
      } else {
        setError(err.message || '네트워크 오류가 발생했습니다.');
      }
    }

    setIsLoading(false);
  };

  return (
    <div className={`min-h-[60vh] flex items-center justify-center ${
      isDarkMode
        ? 'bg-gradient-to-br from-purple-900/20 via-violet-900/10 to-fuchsia-900/20'
        : 'bg-gradient-to-br from-pink-100/50 via-white/30 to-pink-50/40'
    }`}>
      <motion.div
        className={`${
          isDarkMode
            ? 'bg-purple-500/10 border-purple-400/30 shadow-purple-500/20'
            : 'bg-white/80 border-pink-200/50 shadow-pink-200/30'
        } backdrop-blur-lg rounded-3xl border p-8 w-full max-w-md mx-4 shadow-2xl relative overflow-hidden`}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Neon glow background effects */}
        <div className={`absolute -inset-1 ${
          isDarkMode
            ? 'bg-gradient-to-r from-purple-600 to-violet-600'
            : 'bg-gradient-to-r from-pink-400 to-pink-500'
        } rounded-3xl blur opacity-25 group-hover:opacity-40 transition duration-1000`}></div>
        <div className={`absolute inset-0 ${
          isDarkMode
            ? 'bg-gradient-to-br from-purple-800/20 via-violet-700/10 to-fuchsia-800/20'
            : 'bg-gradient-to-br from-pink-50/30 via-white/20 to-pink-100/30'
        } rounded-3xl`}></div>
        <div className="relative z-10">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4 filter drop-shadow-lg">🔐</div>
          <h1 className={`text-3xl font-bold mb-2 drop-shadow-lg ${
            isDarkMode
              ? 'bg-gradient-to-r from-purple-300 to-violet-200 bg-clip-text text-transparent'
              : 'bg-gradient-to-r from-pink-600 to-pink-700 bg-clip-text text-transparent'
          }`}>
            관리자 로그인
          </h1>
          <p className={`text-sm font-medium ${
            isDarkMode ? 'text-purple-200/80' : 'text-pink-600/70'
          }`}>
            HEAL7 사주 시스템 관리자 전용 페이지
          </p>
        </div>

        {/* 로그인 폼 */}
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="username" className={`block text-sm font-medium mb-2 ${
              isDarkMode ? 'text-purple-200' : 'text-pink-700'
            }`}>
              사용자명
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className={`w-full px-4 py-3 backdrop-blur-sm border rounded-xl focus:outline-none focus:ring-2 transition-all duration-300 shadow-inner ${
                isDarkMode
                  ? 'bg-purple-500/10 border-purple-400/30 text-white placeholder-purple-300/60 focus:ring-purple-400 focus:border-purple-300/50 focus:bg-purple-400/10'
                  : 'bg-white/70 border-pink-200/50 text-pink-900 placeholder-pink-400/60 focus:ring-pink-400 focus:border-pink-400/70 focus:bg-white/80'
              }`}
              placeholder="사용자명을 입력하세요"
              required
              autoFocus
            />
          </div>

          <div>
            <label htmlFor="password" className={`block text-sm font-medium mb-2 ${
              isDarkMode ? 'text-purple-200' : 'text-pink-700'
            }`}>
              관리자 비밀번호
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={`w-full px-4 py-3 backdrop-blur-sm border rounded-xl focus:outline-none focus:ring-2 transition-all duration-300 shadow-inner ${
                isDarkMode
                  ? 'bg-purple-500/10 border-purple-400/30 text-white placeholder-purple-300/60 focus:ring-purple-400 focus:border-purple-300/50 focus:bg-purple-400/10'
                  : 'bg-white/70 border-pink-200/50 text-pink-900 placeholder-pink-400/60 focus:ring-pink-400 focus:border-pink-400/70 focus:bg-white/80'
              }`}
              placeholder="비밀번호를 입력하세요"
              required
            />
          </div>

          {error && (
            <motion.div
              className={`backdrop-blur-sm border rounded-xl p-3 text-sm shadow-lg ${
                isDarkMode
                  ? 'bg-red-500/20 border-red-400/40 text-red-200'
                  : 'bg-red-100/80 border-red-300/60 text-red-700'
              }`}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              ⚠️ {error}
            </motion.div>
          )}

          <motion.button
            type="submit"
            disabled={isLoading || !password}
            className={`w-full py-4 px-6 rounded-xl font-bold transition-all duration-300 backdrop-blur-sm ${
              isLoading || !password
                ? 'bg-gray-600/50 cursor-not-allowed border border-gray-500/30 text-gray-400'
                : isDarkMode
                  ? 'bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-500 hover:to-violet-500 shadow-xl shadow-purple-500/25 hover:shadow-2xl hover:shadow-purple-500/40 border border-purple-400/50 hover:border-purple-300/70 text-white'
                  : 'bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-500 hover:to-pink-600 shadow-xl shadow-pink-500/25 hover:shadow-2xl hover:shadow-pink-500/40 border border-pink-400/50 hover:border-pink-300/70 text-white'
            }`}
            whileHover={!isLoading && password ? {
              scale: 1.02,
              boxShadow: isDarkMode
                ? "0 25px 50px -12px rgba(139, 92, 246, 0.5)"
                : "0 25px 50px -12px rgba(236, 72, 153, 0.5)"
            } : {}}
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
        <div className={`mt-6 p-4 backdrop-blur-sm border rounded-xl shadow-lg ${
          isDarkMode
            ? 'bg-amber-500/10 border-amber-400/30'
            : 'bg-amber-100/80 border-amber-300/50'
        }`}>
          <div className={`flex items-center text-sm ${
            isDarkMode ? 'text-amber-200' : 'text-amber-700'
          }`}>
            <span className="mr-2 text-lg">🔒</span>
            <span>보안상 3회 실패 시 5분간 접근이 제한됩니다.</span>
          </div>
        </div>

        {/* 임시 로그인 정보 표시 */}
        <div className={`mt-6 p-4 backdrop-blur-sm border rounded-xl shadow-lg ${
          isDarkMode
            ? 'bg-blue-500/10 border-blue-400/30'
            : 'bg-pink-100/80 border-pink-300/50'
        }`}>
          <div className="text-center">
            <div className={`text-sm font-bold mb-2 flex items-center justify-center ${
              isDarkMode ? 'text-blue-200' : 'text-pink-700'
            }`}>
              <span className="mr-2">🔑</span>
              임시 접속 정보
            </div>
            <div className={`text-xs ${
              isDarkMode ? 'text-blue-100' : 'text-pink-600'
            }`}>
              비밀번호: <span className={`font-mono backdrop-blur-sm px-3 py-1 rounded-lg border ${
                isDarkMode
                  ? 'bg-blue-600/30 border-blue-400/40 text-blue-100'
                  : 'bg-pink-200/80 border-pink-300/60 text-pink-800'
              }`}>admin123</span>
            </div>
            <div className={`text-xs mt-2 ${
              isDarkMode ? 'text-blue-300/80' : 'text-pink-500/80'
            }`}>
              (개발 편의를 위한 임시 표시)
            </div>
          </div>
        </div>

        {/* 시스템 정보 */}
        <div className={`mt-4 text-center text-xs font-medium ${
          isDarkMode ? 'text-purple-300/60' : 'text-pink-500/60'
        }`}>
          HEAL7 Admin Dashboard v2.0.0 | saju.heal7.com
        </div>
        </div>
      </motion.div>
    </div>
  );
};

export default AdminLogin;