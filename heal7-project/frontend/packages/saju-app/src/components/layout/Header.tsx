import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { AuthModal } from '../auth/AuthModal'
import { useAuth } from '../../hooks/useAuth'
import { useTheme } from '../../contexts/ThemeContext'
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
  const { theme, weatherData, isLoading: isWeatherLoading, toggleTheme, isManualOverride, resetToAuto } = useTheme();

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

            {/* 개선된 테마 토글 시스템 - 모바일에서 숨김 */}
            <div className="hidden md:flex items-center space-x-3 group relative">
              {/* 라이트 모드 라벨 */}
              <span className={`text-sm ${themeTransitions.colors} ${
                theme === 'light' ? 'theme-accent' : 'theme-text-muted'
              }`}>
                ☀️
              </span>

              {/* 테마 토글 스위치 */}
              <motion.button
                className={`relative w-16 h-8 rounded-full theme-transition ${
                  theme === 'dark' 
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg theme-shadow' 
                    : 'bg-gradient-to-r from-orange-400 to-amber-500 shadow-lg'
                } ${isManualOverride ? 'ring-2 ring-white/30' : ''}`}
                onClick={toggleTheme}
                whileTap={{ scale: 0.95 }}
                whileHover={{ scale: 1.02 }}
                disabled={isWeatherLoading}
              >
                <motion.div
                  className="absolute top-1 w-6 h-6 bg-white rounded-full shadow-lg flex items-center justify-center text-sm font-bold"
                  animate={{
                    x: theme === 'dark' ? 36 : 4
                  }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  {theme === 'dark' ? '🌙' : '☀️'}
                </motion.div>
              </motion.button>

              {/* 다크 모드 라벨 */}
              <span className={`text-sm ${themeTransitions.colors} ${
                theme === 'dark' ? 'theme-accent' : 'theme-text-muted'
              }`}>
                🌙
              </span>

              {/* 자동 모드 복원 버튼 (수동 모드일 때만 표시) */}
              {isManualOverride && (
                <motion.button
                  className="text-xs px-2 py-1 theme-bg-surface theme-border rounded-lg theme-text-secondary hover:theme-text-primary theme-transition"
                  onClick={resetToAuto}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  title="자동 테마로 복원"
                >
                  🤖 자동
                </motion.button>
              )}

              {/* 기상청 날씨 정보 툴팁 */}
              <div className={`absolute top-10 right-0 text-xs px-4 py-3 rounded-lg opacity-0 group-hover:opacity-100 ${themeTransitions.normal} whitespace-nowrap z-50 theme-bg-card theme-border backdrop-blur-sm`}>
                <div className="space-y-2">
                  <div className="font-semibold theme-accent">
                    🌤️ 실시간 기상정보
                  </div>
                  
                  {weatherData && (
                    <>
                      <div className="theme-text-primary">
                        🇰🇷 {weatherData.city} {weatherData.temperature}°C
                      </div>
                      <div className="theme-text-secondary">
                        {weatherData.weather === 'clear' && '☀️ 맑음'}
                        {weatherData.weather === 'clouds' && '☁️ 구름많음/흐림'}
                        {weatherData.weather === 'rain' && '🌧️ 비'}
                        {weatherData.weather === 'snow' && '❄️ 눈'}
                      </div>
                    </>
                  )}

                  <div className="theme-text-muted border-t theme-border pt-2">
                    <div>현재: <span className="theme-accent">{theme === 'dark' ? '다크 모드' : '라이트 모드'}</span></div>
                    <div className="text-xs mt-1">
                      기상청 API 연동 • 30분마다 갱신
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 사용자 프로필 */}
            <div className="flex items-center space-x-2">
              {isAuthenticated ? (
                <div className="flex items-center space-x-3">
                  <motion.div 
                    className={`w-10 h-10 rounded-full flex items-center justify-center cursor-pointer ${theme === 'dark' ? 'bg-gradient-to-r from-purple-500 to-indigo-500' : 'bg-gradient-to-r from-orange-500 to-amber-500'}`}
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
                    className="btn-ghost !py-1 !px-3 text-sm"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleLogout}
                  >
                    로그아웃
                  </motion.button>
                </div>
              ) : (
                <motion.button
                  className="btn-primary"
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
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'dashboard' ? 'active' : ''}`}
              >
                🏠 메인
              </button>
              <button 
                onClick={() => onPageChange?.('saju')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'saju' ? 'active' : ''}`}
              >
                🔮 사주명리
              </button>
              <button 
                onClick={() => onPageChange?.('tarot')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'tarot' ? 'active' : ''}`}
              >
                🃏 타로카드
              </button>
              <button 
                onClick={() => onPageChange?.('magazine')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'magazine' ? 'active' : ''}`}
              >
                📰 매거진
              </button>
              <button 
                onClick={() => onPageChange?.('compatibility')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'compatibility' ? 'active' : ''}`}
              >
                💑 궁합
              </button>
              <button 
                onClick={() => onPageChange?.('consultation')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'consultation' ? 'active' : ''}`}
              >
                💬 상담
              </button>
              <button 
                onClick={() => onPageChange?.('store')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'store' ? 'active' : ''}`}
              >
                🛍️ 스토어
              </button>
              <button 
                onClick={() => onPageChange?.('notices')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'notices' ? 'active' : ''}`}
              >
                📢 공지사항
              </button>
              <button 
                onClick={() => onPageChange?.('profile')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'profile' ? 'active' : ''}`}
              >
                👤 프로필
              </button>
              <button 
                onClick={() => onPageChange?.('admin')}
                className={`card-nav text-xs whitespace-nowrap flex-shrink-0 ${currentPage === 'admin' ? 'active' : ''}`}
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
            
            {/* 모바일 기상정보 표시만 (토글 숨김) */}
            <div className="mt-6 pt-4 border-t border-white/20">
              <div className="text-center text-xs text-white/60">
                🌤️ 기상청 연동 자동 테마 • 현재: {theme === 'dark' ? '다크' : '라이트'} 모드
              </div>
              {weatherData && (
                <div className="text-center mt-1 text-xs text-white/70">
                  🇰🇷 {weatherData.city} {weatherData.temperature}°C • {weatherData.weather === 'clear' ? '☀️ 맑음' : weatherData.weather === 'clouds' ? '☁️ 흐림' : weatherData.weather === 'rain' ? '🌧️ 비' : '❄️ 눈'}
                </div>
              )}
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