/**
 * 🧭 Route-Aware 네비게이션 컴포넌트
 * 기존 Navigation 컴포넌트를 확장하여 Router 기능 추가
 * 기존 onClick 방식과 새로운 Link 방식을 병행 지원
 */

import React, { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { NavigationProps, CurrentPage, RoutingMode } from '../../types/routingTypes'
import { CORE_NAVIGATION, EXTRA_NAVIGATION, ROUTE_CONFIG } from '../../config/routeConfig'
import { useTheme } from '../../contexts/ThemeContext'

// 하이브리드 네비게이션 Props (기존 + 라우터 기능)
interface RouteAwareNavigationProps extends NavigationProps {
  routingMode?: RoutingMode
  onUrlChange?: (path: string) => void
}

export const RouteAwareNavigation: React.FC<RouteAwareNavigationProps> = ({
  currentPage,
  onPageChange,
  viewMode,
  routingMode = 'state_based',
  onUrlChange
}) => {
  const [showMore, setShowMore] = useState(false)
  const { theme } = useTheme()

  // 🔄 하이브리드 페이지 변경 핸들러
  const handlePageChange = useCallback((pageId: CurrentPage) => {
    // 1. 기존 state 기반 변경 (하위 호환성)
    onPageChange(pageId)
    
    // 2. URL 변경 (점진적 라우터 도입)
    if (routingMode !== 'state_based' && onUrlChange) {
      const routeInfo = ROUTE_CONFIG[pageId]
      if (routeInfo) {
        onUrlChange(routeInfo.path)
        // 브라우저 히스토리에 추가 (뒤로가기 지원)
        window.history.pushState({ pageId }, routeInfo.title, routeInfo.path)
      }
    }
  }, [onPageChange, onUrlChange, routingMode])

  // 핵심 메뉴 렌더링
  const renderCoreNavigation = () => (
    CORE_NAVIGATION.map((routeInfo) => (
      <CompactNavButton 
        key={routeInfo.pageId}
        routeInfo={routeInfo}
        isActive={currentPage === routeInfo.pageId}
        viewMode={viewMode}
        theme={theme}
        onClick={() => handlePageChange(routeInfo.pageId)}
        isPrimary={true}
      />
    ))
  )

  // 확장 메뉴 렌더링
  const renderExtraNavigation = () => (
    EXTRA_NAVIGATION.map((routeInfo) => (
      <CompactNavButton 
        key={routeInfo.pageId}
        routeInfo={routeInfo}
        isActive={currentPage === routeInfo.pageId}
        viewMode={viewMode}
        theme={theme}
        onClick={() => handlePageChange(routeInfo.pageId)}
        isPrimary={false}
      />
    ))
  )

  return (
    <nav className="container mx-auto px-4 py-3">
      {/* 데스크톱 네비게이션 */}
      <div className="hidden sm:flex items-center justify-center gap-2 mb-3">
        {renderCoreNavigation()}
        
        {/* 더보기 버튼 */}
        <motion.button
          className={`px-3 py-2 rounded-lg font-medium transition-all duration-300 backdrop-blur-md border ${
            theme === 'light'
              ? 'bg-gradient-to-r from-pink-200/60 to-orange-200/60 hover:from-pink-300/70 hover:to-orange-300/70 border-orange-300/40 text-pink-800'
              : 'bg-white/10 hover:bg-white/20 border-white/20 text-white'
          }`}
          onClick={() => setShowMore(!showMore)}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <div className="flex items-center space-x-1">
            <span className="text-base">⋯</span>
            <span className="text-xs font-semibold">더보기</span>
          </div>
        </motion.button>
      </div>

      {/* 모바일 네비게이션 */}
      <div className="sm:hidden mb-3">
        <div className="flex items-center justify-center gap-2 flex-wrap">
          {renderCoreNavigation()}
          
          <motion.button
            className={`px-3 py-2 rounded-lg font-medium transition-all duration-300 min-w-[70px] backdrop-blur-md border ${
              theme === 'light'
                ? 'bg-gradient-to-r from-pink-200/60 to-orange-200/60 hover:from-pink-300/70 hover:to-orange-300/70 border-orange-300/40 text-pink-800'
                : 'bg-white/10 hover:bg-white/20 border-white/20 text-white'
            }`}
            onClick={() => setShowMore(!showMore)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="flex items-center justify-center space-x-1">
              <span className="text-base">⋯</span>
              <span className="text-xs font-semibold">더보기</span>
            </div>
          </motion.button>
        </div>
      </div>

      {/* 확장 메뉴 (더보기) */}
      <AnimatePresence>
        {showMore && (
          <motion.div
            className="mb-2"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* 데스크톱: 센터 정렬 */}
            <div className="hidden sm:flex items-center justify-center gap-2">
              {renderExtraNavigation()}
            </div>

            {/* 모바일: 가로 스크롤 */}
            <div className="sm:hidden">
              <div className="relative">
                <div className="flex items-center gap-2 pb-2 scrollbar-hide mobile-nav-scroll overflow-x-auto">
                  {renderExtraNavigation()}
                </div>
                
                {/* 그라데이션 힌트 */}
                <div className="absolute left-0 top-0 bottom-0 w-3 bg-gradient-to-r from-black/20 via-transparent to-transparent pointer-events-none" />
                <div className="absolute right-0 top-0 bottom-0 w-3 bg-gradient-to-l from-black/20 via-transparent to-transparent pointer-events-none" />
              </div>
              
              {/* 스크롤 힌트 텍스트 */}
              <div className="flex justify-center mt-1">
                <span className="text-xs text-white/60">← 손가락으로 밀어서 스크롤하세요 →</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}

// 🎯 컴팩트 네비게이션 버튼 컴포넌트
interface CompactNavButtonProps {
  routeInfo: typeof ROUTE_CONFIG[keyof typeof ROUTE_CONFIG]
  isActive: boolean
  viewMode: 'basic' | 'cyber_fantasy'
  theme: 'light' | 'dark'
  onClick: () => void
  isPrimary: boolean
}

const CompactNavButton: React.FC<CompactNavButtonProps> = ({
  routeInfo,
  isActive,
  viewMode,
  theme,
  onClick,
  isPrimary
}) => (
  <motion.button
    className={`
      relative px-3 py-2 rounded-lg font-medium transition-all duration-300 whitespace-nowrap
      ${isPrimary ? 'min-w-[70px] sm:min-w-[80px]' : 'min-w-[60px] sm:min-w-[70px]'}
      mobile-touch backdrop-blur-md
      ${theme === 'light'
        ? isActive
          ? 'bg-gradient-to-r from-pink-500 to-orange-500 text-white shadow-lg shadow-pink-500/25'
          : 'bg-gradient-to-r from-pink-200/60 to-orange-200/60 hover:from-pink-300/70 hover:to-orange-300/70 border border-orange-300/40 text-pink-800'
        : isActive
          ? viewMode === 'cyber_fantasy'
            ? 'bg-gradient-to-r from-[var(--theme-primary)]/80 to-[var(--theme-secondary)]/80 shadow-lg text-white'
            : 'bg-gradient-to-r from-[var(--theme-secondary)]/80 to-[var(--theme-primary)]/80 shadow-lg text-white'
          : 'bg-white/10 hover:bg-white/20 border border-white/20 text-white'
      }
      ${!isPrimary ? 'text-sm' : ''}
    `}
    onClick={onClick}
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    title={routeInfo.description}
  >
    <div className="flex items-center justify-center space-x-1 sm:space-x-2">
      <span className={`${isPrimary ? "text-base sm:text-lg" : "text-sm sm:text-base"}`}>
        {routeInfo.icon}
      </span>
      <span className={`font-semibold ${isPrimary ? "text-xs sm:text-sm" : "text-xs"}`}>
        {routeInfo.label}
      </span>
    </div>

    {/* 활성 상태 표시 */}
    {isActive && (
      <motion.div
        className={`absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-6 h-0.5 rounded-full ${
          viewMode === 'cyber_fantasy'
            ? 'bg-gradient-to-r from-[var(--theme-primary)] to-[var(--theme-secondary)]'
            : 'bg-gradient-to-r from-[var(--theme-secondary)] to-[var(--theme-primary)]'
        }`}
        layoutId="activeCompactTab"
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      />
    )}
  </motion.button>
)

export default RouteAwareNavigation