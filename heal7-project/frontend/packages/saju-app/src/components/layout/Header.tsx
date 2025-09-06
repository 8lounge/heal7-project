import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { AuthModal } from '../auth/AuthModal'
import { useAuth } from '../../hooks/useAuth'
import { useWeatherTheme } from '../../hooks/useWeatherTheme'
import { getThemeClasses, getMenuButtonClass, themeTransitions } from '../../utils/themeStyles'

type CurrentPage = 'dashboard' | 'saju' | 'tarot' | 'magazine' | 'consultation' | 'store' | 'notices' | 'profile' | 
                  'fortune' | 'zodiac' | 'personality' | 'love' | 'compatibility' | 'admin' | 'dream' | 'calendar' | 'subscription'

interface HeaderProps {
  viewMode: 'basic' | 'cyber_fantasy'
  onViewModeChange: (mode: 'basic' | 'cyber_fantasy') => void
  apiStatus: string
  currentPage?: CurrentPage
  onPageChange?: (page: CurrentPage) => void
  onAuthModalStateChange?: (isOpen: boolean) => void
}

const Header: React.FC<HeaderProps> = ({ viewMode, onViewModeChange, currentPage, onPageChange, onAuthModalStateChange }) => {
  const { isAuthenticated, user, logout } = useAuth();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const { theme, weatherData, isLoading: isWeatherLoading, toggleTheme } = useWeatherTheme();

  const handleAuthModalOpen = (isOpen: boolean) => {
    setIsAuthModalOpen(isOpen);
    onAuthModalStateChange?.(isOpen);
  };

  const handleAuthSuccess = () => {
    handleAuthModalOpen(false);
  };

  const handleLogout = () => {
    logout();
  };

  const handleProfileClick = () => {
    if (isAuthenticated) {
      // 로그인된 경우 프로필 페이지로 이동 또는 메뉴 표시
      onPageChange?.('profile');
    } else {
      // 로그인되지 않은 경우 인증 모달 열기
      handleAuthModalOpen(true);
    }
  };

  return (
    <motion.header 
      className={`sticky top-0 z-50 backdrop-blur-md border-b ${themeTransitions.normal} ${getThemeClasses.header(theme)}`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* 로고 - 클릭으로 메인페이지 이동 */}
          <motion.button 
            className="flex items-center space-x-3 cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onPageChange?.('dashboard')}
          >
            <div className="text-3xl">🧙‍♀️</div>
            <div>
              <h1 className={`text-2xl font-bold ${themeTransitions.colors} ${getThemeClasses.logoTitle(theme)}`}>
                치유마녀
              </h1>
              <p className={`text-sm ${themeTransitions.colors} ${getThemeClasses.logoSubtitle(theme)}`}>
                HEAL-WITCH
              </p>
            </div>
          </motion.button>

          {/* 중앙 네비게이션 - 주요 메뉴 */}
          <nav className="hidden md:flex items-center space-x-4">
            <button 
              onClick={() => onPageChange?.('saju')}
              className={getMenuButtonClass(theme, currentPage === 'saju')}
            >
              🔮 사주명리
            </button>
            <button 
              onClick={() => onPageChange?.('tarot')}
              className={getMenuButtonClass(theme, currentPage === 'tarot')}
            >
              🃏 타로카드
            </button>
            <button 
              onClick={() => onPageChange?.('zodiac')}
              className={getMenuButtonClass(theme, currentPage === 'zodiac')}
            >
              🐭 띠운세
            </button>
            <button 
              onClick={() => onPageChange?.('fortune')}
              className={getMenuButtonClass(theme, currentPage === 'fortune')}
            >
              ⭐ 운세
            </button>
          </nav>

          {/* 모드 전환 & 상태 */}
          <div className="flex items-center space-x-4">

            {/* 날씨 기반 테마 전환 - 모바일에서 숨김 */}
            <div className="hidden md:flex items-center space-x-2 group relative">
              <span className={`text-sm ${themeTransitions.colors} ${getThemeClasses.themeLabel.light(theme)}`}>
                ☀️ 낮
              </span>
              <motion.button
                className={`relative w-14 h-7 rounded-full ${
                  theme === 'dark' 
                    ? 'bg-gradient-to-r from-purple-500 to-indigo-500' 
                    : 'bg-gradient-to-r from-pink-400 to-orange-500'
                }`}
                onClick={toggleTheme}
                whileTap={{ scale: 0.95 }}
                disabled={isWeatherLoading}
              >
                <motion.div
                  className="absolute top-1 w-5 h-5 bg-white rounded-full shadow-lg flex items-center justify-center text-xs"
                  animate={{
                    x: theme === 'dark' ? 28 : 4
                  }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  {theme === 'dark' ? '🌙' : '☀️'}
                </motion.div>
              </motion.button>
              <span className={`text-sm ${themeTransitions.colors} ${getThemeClasses.themeLabel.dark(theme)}`}>
                🌙 밤
              </span>
              {/* 한국 기상청 날씨 정보 툴팁 */}
              <div className={`absolute top-8 right-0 text-xs px-3 py-2 rounded-lg opacity-0 group-hover:opacity-100 ${themeTransitions.normal} whitespace-nowrap z-50 ${getThemeClasses.tooltip.container(theme)}`}>
                {isWeatherLoading ? (
                  '🌦️ 기상청 날씨 정보 로딩 중...'
                ) : weatherData ? (
                  <>
                    <div className={`font-semibold ${getThemeClasses.tooltip.title(theme)}`}>🇰🇷 기상청 날씨</div>
                    <div>{weatherData.city} {weatherData.temperature}°C</div>
                    <div className={getThemeClasses.tooltip.content(theme)}>
                      {weatherData.weather === 'clear' && '☀️ 맑음'}
                      {weatherData.weather === 'clouds' && '☁️ 구름많음/흐림'}
                      {weatherData.weather === 'rain' && '🌧️ 비'}
                      {weatherData.weather === 'snow' && '❄️ 눈'}
                      {' - '}
                      <span className={getThemeClasses.tooltip.accent(theme)}>
                        {theme === 'dark' ? '어두운 테마' : '밝은 테마'}
                      </span>
                      {' 활성화'}
                    </div>
                    <div className={`text-xs mt-1 ${getThemeClasses.tooltip.subtitle(theme)}`}>클릭으로 수동 전환 가능</div>
                  </>
                ) : (
                  <>
                    <div>🌦️ 기상청 날씨 기반 자동 테마</div>
                    <div className="text-xs text-gray-400">오후 6시 이후/흐린날 = 어두운 테마</div>
                    <div className="text-xs text-gray-400">그 외 시간 = 밝은 테마</div>
                  </>
                )}
              </div>
            </div>

            {/* 사용자 프로필 */}
            <div className="flex items-center space-x-2">
              {isAuthenticated ? (
                <div className="flex items-center space-x-3">
                  <motion.div 
                    className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center cursor-pointer"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleProfileClick}
                    title={`${user?.username || user?.full_name || user?.email || '사용자'}님`}
                  >
                    <span className="text-white font-bold">
                      {
                        user?.username?.charAt(0).toUpperCase() || 
                        user?.full_name?.charAt(0).toUpperCase() ||
                        user?.email?.charAt(0).toUpperCase() || 
                        '사'
                      }
                    </span>
                  </motion.div>
                  <motion.button
                    className="px-3 py-1 text-sm bg-white/10 hover:bg-white/20 rounded-lg text-white transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleLogout}
                  >
                    로그아웃
                  </motion.button>
                </div>
              ) : (
                <motion.button
                  className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg text-white font-medium transition-all duration-300"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleAuthModalOpen(true)}
                >
                  로그인
                </motion.button>
              )}
            </div>
          </div>
        </div>

        {/* 모바일 메뉴 - 주요 메뉴 */}
        <div className="md:hidden mt-4">
          
          {/* 드래그 가능한 메뉴 */}
          <div className="relative">
            <nav className="flex gap-3 px-4 overflow-x-auto scrollbar-hide pb-2 scroll-smooth mobile-nav-scroll">
              <button 
                onClick={() => onPageChange?.('dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'dashboard' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🏠 메인
              </button>
              <button 
                onClick={() => onPageChange?.('saju')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'saju' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🔮 사주명리
              </button>
              <button 
                onClick={() => onPageChange?.('tarot')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'tarot' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🃏 타로카드
              </button>
              <button 
                onClick={() => onPageChange?.('magazine')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'magazine' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                📰 매거진
              </button>
              <button 
                onClick={() => onPageChange?.('consultation')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'consultation' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                💬 상담
              </button>
              <button 
                onClick={() => onPageChange?.('store')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'store' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🛍️ 스토어
              </button>
              <button 
                onClick={() => onPageChange?.('notices')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'notices' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                📢 공지사항
              </button>
              <button 
                onClick={() => onPageChange?.('profile')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'profile' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                👤 프로필
              </button>
              <button 
                onClick={() => onPageChange?.('admin')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'admin' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/20 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                ⚙️ 관리자
              </button>
            </nav>
            
            {/* 스크롤 인디케이터 */}
            <div className="absolute -bottom-1 left-0 right-0 flex justify-center">
              <div className="w-16 h-1 bg-white/20 rounded-full">
                <div className="w-8 h-1 bg-white/50 rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 인증 모달 */}
      <AuthModal 
        isOpen={isAuthModalOpen}
        onClose={() => handleAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </motion.header>
  )
}

export default Header