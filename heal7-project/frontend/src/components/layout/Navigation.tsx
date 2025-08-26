import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

type CurrentPage = 'dashboard' | 'saju' | 'tarot' | 'magazine' | 'consultation' | 'store' | 'notices' | 'profile' | 
                  'fortune' | 'zodiac' | 'personality' | 'love' | 'compatibility' | 'admin'
type ViewMode = 'basic' | 'cyber_fantasy'

interface NavigationProps {
  currentPage: CurrentPage
  onPageChange: (page: CurrentPage) => void
  viewMode: ViewMode
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange, viewMode }) => {
  const [showMore, setShowMore] = useState(false)
  
  // 주요 메뉴 항목 (항상 표시)
  const primaryNavItems = [
    { id: 'dashboard', label: '메인', icon: '🏠' },
    { id: 'saju', label: '사주명리', icon: '📊' },
    { id: 'tarot', label: '타로카드', icon: '🃏' },
    { id: 'magazine', label: '매거진', icon: '📰' },
    { id: 'consultation', label: '상담', icon: '💬' }
  ]
  
  // 부가 메뉴 항목 (더보기로 숨김) - 헤더와 겹치지 않는 항목들만
  const secondaryNavItems = [
    { id: 'store', label: '스토어', icon: '🛍️' },
    { id: 'notices', label: '공지사항', icon: '📢' },
    { id: 'admin', label: '관리자', icon: '⚙️' }
  ]

  // 컴팩트 버튼 컴포넌트
  const CompactNavButton = ({ item, isPrimary = true }: { item: any, isPrimary?: boolean }) => (
    <motion.button
      className={`
        relative px-3 py-2 rounded-lg font-medium transition-all duration-300 text-white whitespace-nowrap
        ${isPrimary ? 'min-w-[80px]' : 'min-w-[70px]'}
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
      <div className="flex items-center space-x-2">
        <span className={isPrimary ? "text-lg" : "text-base"}>{item.icon}</span>
        <span className={`font-semibold ${isPrimary ? "text-sm" : "text-xs"}`}>
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
      {/* 주요 메뉴 */}
      <div className="flex items-center justify-center gap-2 mb-3">
        {primaryNavItems.map((item) => (
          <CompactNavButton key={item.id} item={item} isPrimary={true} />
        ))}
        
        {/* 더보기 버튼 */}
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
      </div>

      {/* 부가 메뉴 (펼쳐지는 형태) */}
      <AnimatePresence>
        {showMore && (
          <motion.div
            className="flex items-center justify-center gap-2 mb-2"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {secondaryNavItems.map((item) => (
              <CompactNavButton key={item.id} item={item} isPrimary={false} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}

export default Navigation