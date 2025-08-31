import React from 'react'
import { motion } from 'framer-motion'

type CurrentPage = 'dashboard' | 'saju' | 'tarot' | 'magazine' | 'consultation' | 'store' | 'notices' | 'profile' | 
                  'fortune' | 'zodiac' | 'personality' | 'love' | 'compatibility' | 'admin'

interface HeaderProps {
  viewMode: 'basic' | 'cyber_fantasy'
  onViewModeChange: (mode: 'basic' | 'cyber_fantasy') => void
  apiStatus: string
  currentPage?: CurrentPage
  onPageChange?: (page: CurrentPage) => void
}

const Header: React.FC<HeaderProps> = ({ viewMode, onViewModeChange, currentPage, onPageChange }) => {
  return (
    <motion.header 
      className="sticky top-0 z-50 bg-black/20 backdrop-blur-md border-b border-white/10"
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
              <h1 className="text-2xl font-bold text-cosmic">치유 마녀</h1>
              <p className="text-sm text-gray-300">HEAL-WITCH</p>
            </div>
          </motion.button>

          {/* 중앙 네비게이션 */}
          <nav className="hidden md:flex items-center space-x-4">
            <button 
              onClick={() => onPageChange?.('dashboard')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                currentPage === 'dashboard' 
                  ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                  : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
              }`}
            >
              메인
            </button>
            <button 
              onClick={() => onPageChange?.('saju')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                currentPage === 'saju' 
                  ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                  : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
              }`}
            >
              사주명리
            </button>
            <button 
              onClick={() => onPageChange?.('tarot')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                currentPage === 'tarot' 
                  ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                  : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
              }`}
            >
              타로카드
            </button>
            <button 
              onClick={() => onPageChange?.('profile')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                currentPage === 'profile' 
                  ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                  : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
              }`}
            >
              프로필
            </button>
          </nav>

          {/* 모드 전환 & 상태 */}
          <div className="flex items-center space-x-4">

            {/* 테마 모드 전환 */}
            <div className="flex items-center space-x-2 group relative">
              <span className={`text-sm ${viewMode === 'basic' ? 'text-white' : 'text-gray-500'}`}>
                🌙 클래식
              </span>
              <motion.button
                className={`relative w-14 h-7 rounded-full ${
                  viewMode === 'cyber_fantasy' 
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500' 
                    : 'bg-gray-600'
                }`}
                onClick={() => onViewModeChange(viewMode === 'basic' ? 'cyber_fantasy' : 'basic')}
                whileTap={{ scale: 0.95 }}
              >
                <motion.div
                  className="absolute top-1 w-5 h-5 bg-white rounded-full shadow-lg flex items-center justify-center text-xs"
                  animate={{
                    x: viewMode === 'cyber_fantasy' ? 28 : 4
                  }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  {viewMode === 'cyber_fantasy' ? '✨' : '🌙'}
                </motion.div>
              </motion.button>
              <span className={`text-sm ${viewMode === 'cyber_fantasy' ? 'text-white' : 'text-gray-500'}`}>
                ✨ 판타지
              </span>
              {/* 모드 설명 툴팁 */}
              <div className="absolute top-8 right-0 bg-black/80 text-white text-xs px-3 py-2 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
                {viewMode === 'basic' 
                  ? '클릭하면 3D 판타지 모드로 전환됩니다' 
                  : '클릭하면 클래식 모드로 전환됩니다'
                }
              </div>
            </div>

            {/* 사용자 프로필 */}
            <motion.div 
              className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center cursor-pointer"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="text-white font-bold">U</span>
            </motion.div>
          </div>
        </div>

        {/* 모바일 메뉴 */}
        <div className="md:hidden mt-4">
          {/* 드래그 안내 텍스트 */}
          <div className="text-center mb-2">
            <p className="text-white/70 text-xs">👈 좌우로 드래그 하세요 👉</p>
          </div>
          
          {/* 드래그 가능한 메뉴 */}
          <div className="relative">
            <nav className="flex gap-3 px-4 overflow-x-auto scrollbar-hide pb-2 scroll-smooth touch-scroll">
              <button 
                onClick={() => onPageChange?.('dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'dashboard' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🏠 메인
              </button>
              <button 
                onClick={() => onPageChange?.('saju')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'saju' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🔮 사주명리
              </button>
              <button 
                onClick={() => onPageChange?.('tarot')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'tarot' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🃏 타로카드
              </button>
              <button 
                onClick={() => onPageChange?.('magazine')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'magazine' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                📰 매거진
              </button>
              <button 
                onClick={() => onPageChange?.('consultation')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'consultation' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                💬 상담
              </button>
              <button 
                onClick={() => onPageChange?.('store')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'store' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                🛍️ 스토어
              </button>
              <button 
                onClick={() => onPageChange?.('notices')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'notices' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                📢 공지사항
              </button>
              <button 
                onClick={() => onPageChange?.('profile')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 text-xs whitespace-nowrap flex-shrink-0 ${
                  currentPage === 'profile' 
                    ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30' 
                    : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white backdrop-blur-sm border border-white/20'
                }`}
              >
                👤 프로필
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
    </motion.header>
  )
}

export default Header