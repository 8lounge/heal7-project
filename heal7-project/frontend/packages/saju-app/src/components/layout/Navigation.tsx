import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

type CurrentPage = 'dashboard' | 'saju' | 'tarot' | 'magazine' | 'consultation' | 'store' | 'notices' | 'profile' |
                  'fortune' | 'zodiac' | 'personality' | 'love' | 'compatibility' | 'admin' | 'dream' | 'calendar' | 'subscription'
type ViewMode = 'basic' | 'cyber_fantasy'

interface NavigationProps {
  currentPage: CurrentPage
  onPageChange: (page: CurrentPage) => void
  viewMode: ViewMode
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange, viewMode }) => {
  const [showMore, setShowMore] = useState(false)

  // 핵심 메뉴 (항상 표시) - 띠운세 추가
  const coreNavItems = [
    { id: 'saju', label: '사주', icon: '🔮' },
    { id: 'tarot', label: '타로', icon: '🃏' },
    { id: 'zodiac', label: '띠운세', icon: '🐭' },
    { id: 'dream', label: '꿈풀이', icon: '🌙' },
    { id: 'consultation', label: '상담', icon: '💬' }
  ]

  // 부가 메뉴 (더보기에 표시) - 운세 관련 통합
  const extraNavItems = [
    { id: 'fortune', label: '종합운세', icon: '⭐' },
    { id: 'personality', label: '성격분석', icon: '🧠' },
    { id: 'love', label: '애정운', icon: '💕' },
    { id: 'compatibility', label: '궁합', icon: '💑' },
    { id: 'calendar', label: '운세달력', icon: '📅' },
    { id: 'magazine', label: '매거진', icon: '📰' },
    { id: 'store', label: '스토어', icon: '🛍️' },
    { id: 'notices', label: '공지사항', icon: '📢' },
    { id: 'admin', label: '관리자', icon: '⚙️' }
  ]


  // 더보기 버튼이 필요한지 판단 (부가 메뉴가 있으면 더보기 버튼 표시)
  const needsMoreButton = extraNavItems.length > 0

  // 표시할 항목과 숨길 항목 분리 - 핵심 메뉴는 항상 표시, 부가 메뉴는 더보기에
  const visibleItems = coreNavItems
  const hiddenItems = extraNavItems

  // 컴팩트 버튼 컴포넌트
  const CompactNavButton = ({ item, isPrimary = true }: { item: any, isPrimary?: boolean }) => (
    <motion.button
      className={`
        relative px-3 py-2 rounded-lg font-medium transition-all duration-300 text-white whitespace-nowrap
        ${isPrimary ? 'min-w-[70px] sm:min-w-[80px]' : 'min-w-[60px] sm:min-w-[70px]'}
        mobile-touch
        ${currentPage === item.id
          ? viewMode === 'cyber_fantasy'
            ? 'bg-gradient-to-r from-purple-500/80 to-pink-500/80 shadow-lg'
            : 'bg-gradient-to-r from-indigo-500/80 to-purple-500/80 shadow-lg'
          : viewMode === 'cyber_fantasy'
            ? 'bg-white/10 hover:bg-white/20 backdrop-blur-sm'
            : 'bg-white/10 hover:bg-white/20'
        }
        ${!isPrimary ? 'text-sm' : ''}
      `}
      onClick={() => onPageChange(item.id as CurrentPage)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className="flex items-center justify-center space-x-1 sm:space-x-2">
        <span className={`${isPrimary ? "text-base sm:text-lg" : "text-sm sm:text-base"}`}>{item.icon}</span>
        <span className={`font-semibold ${isPrimary ? "text-xs sm:text-sm" : "text-xs"}`}>
          {item.label}
        </span>
      </div>

      {/* 활성 상태 표시 */}
      {currentPage === item.id && (
        <motion.div
          className={`absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-6 h-0.5 rounded-full ${
            viewMode === 'cyber_fantasy'
              ? 'bg-gradient-to-r from-purple-400 to-pink-400'
              : 'bg-gradient-to-r from-indigo-400 to-purple-400'
          }`}
          layoutId="activeCompactTab"
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        />
      )}
    </motion.button>
  )

  return (
    <nav className="container mx-auto px-4 py-3">
      {/* 주요 메뉴 - 모바일 반응형 처리 */}
      <div className="mb-3">
        {/* 데스크톱: 한 줄 배치 */}
        <div className="hidden sm:flex items-center justify-center gap-2">
          {visibleItems.map((item) => (
            <CompactNavButton key={item.id} item={item} isPrimary={true} />
          ))}

          {/* 더보기 버튼 (필요할 때만 표시) */}
          {needsMoreButton && (
            <motion.button
              className={`
                px-3 py-2 rounded-lg font-medium transition-all duration-300 text-white
                ${viewMode === 'cyber_fantasy'
                  ? 'bg-white/10 hover:bg-white/20 backdrop-blur-sm'
                  : 'bg-white/10 hover:bg-white/20'
                }
              `}
              onClick={() => setShowMore(!showMore)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="flex items-center space-x-1">
                <span className="text-base">⋯</span>
                <span className="text-xs font-semibold">더보기</span>
              </div>
            </motion.button>
          )}
        </div>

        {/* 모바일: 고정 버튼 배치 (드래그 기능 없음) */}
        <div className="sm:hidden">
          <div className="flex items-center justify-center gap-2 flex-wrap">
            {visibleItems.map((item) => (
              <CompactNavButton key={item.id} item={item} isPrimary={true} />
            ))}

            {/* 더보기 버튼 (필요할 때만 표시) */}
            {needsMoreButton && (
              <motion.button
                className={`
                  px-3 py-2 rounded-lg font-medium transition-all duration-300 text-white min-w-[70px]
                  ${viewMode === 'cyber_fantasy'
                    ? 'bg-white/10 hover:bg-white/20 backdrop-blur-sm'
                    : 'bg-white/10 hover:bg-white/20'
                  }
                `}
                onClick={() => setShowMore(!showMore)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <div className="flex items-center justify-center space-x-1">
                  <span className="text-base">⋯</span>
                  <span className="text-xs font-semibold">더보기</span>
                </div>
              </motion.button>
            )}
          </div>
        </div>
      </div>

      {/* 부가 메뉴 (펼쳐지는 형태) - 모바일에서도 드래그 가능 */}
      <AnimatePresence>
        {showMore && needsMoreButton && (
          <motion.div
            className="mb-2"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* 데스크톱: 센터 정렬 */}
            <div className="hidden sm:flex items-center justify-center gap-2">
              {hiddenItems.map((item) => (
                <CompactNavButton key={item.id} item={item} isPrimary={false} />
              ))}
            </div>

            {/* 모바일: 가로 스크롤 */}
            <div className="sm:hidden">
              <div className="relative">
                <div
                  className="flex items-center gap-2 pb-2 scrollbar-hide mobile-nav-scroll overflow-x-auto"
                  style={{
                    overflowX: 'auto',
                    overflowY: 'hidden',
                    WebkitOverflowScrolling: 'touch',
                    scrollbarWidth: 'none',
                    msOverflowStyle: 'none',
                    touchAction: 'pan-x',
                    scrollBehavior: 'smooth',
                    willChange: 'scroll-position'
                  }}
                >
                  {hiddenItems.map((item) => (
                    <div key={item.id} className="flex-shrink-0">
                      <CompactNavButton item={item} isPrimary={false} />
                    </div>
                  ))}
                </div>

                {/* 더보기 메뉴 그라데이션 힌트 */}
                <div className="absolute left-0 top-0 bottom-0 w-3 bg-gradient-to-r from-black/20 via-transparent to-transparent pointer-events-none" />
                <div className="absolute right-0 top-0 bottom-0 w-3 bg-gradient-to-l from-black/20 via-transparent to-transparent pointer-events-none" />
              </div>

              {/* 하단 메뉴 스크롤 힌트 텍스트 */}
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

export default Navigation