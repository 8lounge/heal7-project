import React, { useEffect } from 'react';
import { motion } from 'framer-motion';

const IntegratedAdminDashboard: React.FC = () => {
  const [isRedirecting, setIsRedirecting] = React.useState(false);

  const handleRedirect = () => {
    setIsRedirecting(true);
    // 관리자 전용 사이트로 리디렉트
    window.open('https://admin.heal7.com', '_blank');
    setTimeout(() => setIsRedirecting(false), 2000);
  };

  useEffect(() => {
    // 컴포넌트 마운트 시 자동으로 관리자 페이지 안내
    const timer = setTimeout(() => {
      handleRedirect();
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <motion.div
      className="min-h-screen flex items-center justify-center p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-2xl w-full text-center">
        <motion.div
          className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20"
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          {/* 관리자 아이콘 */}
          <motion.div
            className="text-8xl mb-6"
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            ⚙️
          </motion.div>

          <h1 className="text-4xl font-bold text-white mb-4">
            🔐 관리자 대시보드
          </h1>

          <p className="text-xl text-gray-300 mb-8">
            관리자 전용 시스템으로 이동합니다
          </p>

          <div className="space-y-4">
            {!isRedirecting ? (
              <motion.button
                onClick={handleRedirect}
                className="w-full px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-xl text-white font-semibold text-lg transition-all duration-300 transform hover:scale-105"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🚀 관리자 시스템으로 이동
              </motion.button>
            ) : (
              <motion.div
                className="w-full px-8 py-4 bg-gradient-to-r from-blue-500 to-green-500 rounded-xl text-white font-semibold text-lg"
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              >
                📡 연결 중...
              </motion.div>
            )}

            <div className="text-sm text-gray-400 space-y-2">
              <p>🔗 관리자 시스템: admin.heal7.com</p>
              <p>🔒 인증이 필요한 서비스입니다</p>
              <p>💡 새 탭에서 열립니다</p>
            </div>
          </div>

          {/* 기능 미리보기 */}
          <motion.div
            className="mt-8 grid grid-cols-2 gap-4 text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-2xl mb-2">👥</div>
              <div className="text-white/80">사용자 관리</div>
            </div>
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-2xl mb-2">📊</div>
              <div className="text-white/80">통계 분석</div>
            </div>
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-2xl mb-2">🔮</div>
              <div className="text-white/80">사주 시스템</div>
            </div>
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-2xl mb-2">💰</div>
              <div className="text-white/80">결제 관리</div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

export default IntegratedAdminDashboard;