import { useState, useEffect, Suspense, lazy, useMemo, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'

// 테마 컨텍스트
import { ThemeProvider, useTheme } from './contexts/ThemeContext'

// 라우팅 관련 imports
import { getPageIdFromPath } from './config/routeConfig'

// 기본 컴포넌트들만 import (3D 관련 제외)
import Header from './components/layout/Header'
import Navigation from './components/layout/Navigation'
import RouteAwareNavigation from './components/routing/RouteAwareNavigation'
import EnhancedDashboard from './components/dashboard/EnhancedDashboard'
import SajuCalculator from './components/fortune/SajuCalculator'
import InteractiveTarotReader from './components/fortune/InteractiveTarotReader'

// Lazy loading으로 분할된 컴포넌트들
const Magazine = lazy(() => import('./components/magazine/Magazine'))
const Consultation = lazy(() => import('./components/consultation/Consultation'))
const Store = lazy(() => import('./components/store/Store'))
const Notices = lazy(() => import('./components/notices/Notices'))

// 운세 콘텐츠 컴포넌트들
import FortuneCategories from './components/fortune/FortuneCategories'
import ZodiacAnalysis from './components/fortune/ZodiacAnalysis'
import PersonalityProfile from './components/fortune/PersonalityProfile'
import LoveFortuneAnalysis from './components/fortune/LoveFortuneAnalysis'
import CompatibilityAnalysis from './components/fortune/CompatibilityAnalysis'
import DreamInterpretation from './components/fortune/DreamInterpretation'
import FortuneCalendar from './components/fortune/FortuneCalendar'

// 관리자 컴포넌트 (Lazy loading)
const SajuAdminDashboard = lazy(() => import('./components/saju-admin/ModularSajuAdminDashboard'))
const AdminLogin = lazy(() => import('./components/saju-admin/AdminLogin'))

import { getThemeClasses, themeTransitions } from './utils/themeStyles'

// 타입 정의
interface ApiHealth {
  status: string
  service: string
  version: string
}

type ViewMode = 'basic' // cyber_fantasy 모드 제거 (3D 관련)
type CurrentPage = 'dashboard' | 'saju' | 'tarot' | 'magazine' | 'consultation' | 'store' | 'notices' | 'profile' | 
                  'fortune' | 'zodiac' | 'personality' | 'love' | 'compatibility' | 'admin' | 'dream' | 'calendar' | 'subscription'

// 테마별 배경 이미지
const getBackgroundForTheme = (theme: 'light' | 'dark') => {
  if (theme === 'light') {
    return [
      'url("/images/backgrounds/light-theme.webp") center/cover, linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 30%, #FED7AA 70%, #FDBA74 100%)',
      'url("/images/backgrounds/light-mystic.webp") center/cover, linear-gradient(135deg, #FEF7F0 0%, #FED7D7 50%, #FECACA 100%)'
    ]
  } else {
    return [
      'url("/images/backgrounds/dark-theme.webp") center/cover, linear-gradient(135deg, #1A0D2E 0%, #2D1B4E 30%, #4C1D95 70%, #1E0A37 100%)',
      'url("/images/backgrounds/dark-mystic.webp") center/cover, linear-gradient(135deg, #0D0221 0%, #1B1464 50%, #2E1A47 100%)'
    ]
  }
}

function AppContent() {
  const { theme } = useTheme()
  const [viewMode, setViewMode] = useState<ViewMode>('basic')
  const [currentPage, setCurrentPage] = useState<CurrentPage>('dashboard')
  const [currentBgImage, setCurrentBgImage] = useState(0)
  const [adminAuthenticated, setAdminAuthenticated] = useState(false)
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)
  
  const [useHybridNavigation] = useState(true)
  
  // 페이지와 URL 동기화
  const handlePageChange = useCallback((newPage: CurrentPage) => {
    setCurrentPage(newPage)
    
    const pageRoutes = {
      dashboard: '/',
      saju: '/saju',
      tarot: '/tarot',
      magazine: '/magazine',
      consultation: '/consultation', 
      store: '/store',
      notices: '/notices',
      profile: '/profile',
      fortune: '/fortune',
      zodiac: '/zodiac',
      personality: '/personality',
      love: '/love',
      compatibility: '/compatibility',
      admin: '/admin',
      dream: '/dream',
      calendar: '/calendar',
      subscription: '/subscription'
    }
    
    const targetUrl = pageRoutes[newPage] || '/'
    window.history.pushState(null, '', targetUrl)
  }, [])
  
  // URL 기반 라우팅 초기화
  useEffect(() => {
    const path = window.location.pathname
    
    try {
      const pageId = getPageIdFromPath(path)
      if (pageId) {
        setCurrentPage(pageId)
        return
      }
    } catch (error) {
      console.warn('Route config loading failed, using fallback:', error)
    }
    
    // 기존 방식 폴백
    if (path === '/admin') {
      setCurrentPage('admin')
    } else if (path === '/saju' || path.startsWith('/saju/')) {
      setCurrentPage('saju')
    } else if (path === '/tarot' || path.startsWith('/tarot/')) {
      setCurrentPage('tarot')
    } else if (path === '/magazine' || path.startsWith('/magazine/')) {
      setCurrentPage('magazine')
    } else if (path === '/consultation' || path.startsWith('/consultation/')) {
      setCurrentPage('consultation')
    } else if (path === '/store' || path.startsWith('/store/')) {
      setCurrentPage('store')
    } else if (path === '/notices' || path.startsWith('/notices/')) {
      setCurrentPage('notices')
    } else if (path === '/fortune' || path.startsWith('/fortune/')) {
      setCurrentPage('fortune')
    } else if (path === '/dream' || path.startsWith('/dream/')) {
      setCurrentPage('dream')
    } else if (path === '/calendar' || path.startsWith('/calendar/')) {
      setCurrentPage('calendar')
    }
  }, [])
  
  // 하이브리드 모드용 URL 변경 핸들러
  const handleUrlChange = useCallback((path: string) => {
    if (useHybridNavigation) {
      window.history.pushState(null, '', path)
    }
  }, [useHybridNavigation])
  
  // 브라우저 뒤로가기/앞으로가기 지원
  useEffect(() => {
    if (!useHybridNavigation) return
    
    const handlePopState = () => {
      const path = window.location.pathname
      const pageId = getPageIdFromPath(path)
      
      if (pageId && pageId !== currentPage) {
        setCurrentPage(pageId)
      }
    }
    
    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [currentPage, useHybridNavigation])

  // 관리자 인증 상태 복구
  useEffect(() => {
    const checkAdminAuth = () => {
      const isAuthenticated = localStorage.getItem('heal7_admin_authenticated')
      const loginTime = localStorage.getItem('heal7_admin_login_time')
      const sessionId = localStorage.getItem('heal7_admin_session_id')
      
      if (isAuthenticated === 'true' && loginTime && sessionId) {
        const now = Date.now()
        const authTime = parseInt(loginTime)
        const hoursDiff = (now - authTime) / (1000 * 60 * 60)
        
        if (hoursDiff < 168) {
          setAdminAuthenticated(true)
          console.log('Admin session restored from localStorage')
        } else {
          localStorage.removeItem('heal7_admin_authenticated')
          localStorage.removeItem('heal7_admin_login_time')
          localStorage.removeItem('heal7_admin_session_id')
          console.log('Admin session expired, cleared localStorage')
        }
      }
    }
    
    checkAdminAuth()
  }, [])

  // 배경 이미지 자동 페이드 전환
  useEffect(() => {
    const bgTimer = setInterval(() => {
      setCurrentBgImage((prev) => (prev + 1) % getBackgroundForTheme(theme).length)
    }, 30000)
    return () => clearInterval(bgTimer)
  }, [theme])

  // API 헬스체크
  const { data: apiHealth } = useQuery<ApiHealth>({
    queryKey: ['api-health'],
    queryFn: async () => {
      try {
        const response = await fetch('/api/health')
        if (!response.ok) {
          return { status: 'unknown', service: 'heal7-api', version: '2.0.0' }
        }
        return response.json()
      } catch (error) {
        return { status: 'unknown', service: 'heal7-api', version: '2.0.0' }
      }
    },
    staleTime: 1000 * 60 * 30,
    refetchInterval: false,
    retry: 0,
    enabled: false,
    initialData: { status: 'healthy', service: 'heal7-api', version: '2.0.0' }
  })

  return (
    <div className={`min-h-screen relative overflow-hidden theme-transition theme-${theme}`}>
      {/* 배경 이미지들 (페이드 전환) */}
      {getBackgroundForTheme(theme).map((image, index) => (
        <div
          key={index}
          className={`absolute inset-0 bg-cover bg-center bg-no-repeat transition-opacity duration-3000 ease-in-out ${
            index === currentBgImage ? 'opacity-100' : 'opacity-0'
          }`}
          style={{
            background: image,
            backgroundAttachment: 'fixed'
          }}
        />
      ))}
      
      {/* 테마에 따른 전체 오버레이 */}
      <div className="absolute inset-0 theme-transition" 
           style={{
             background: 'linear-gradient(135deg, var(--theme-bg-overlay) 0%, var(--theme-bg-card) 100%)'
           }} />
      
      {/* 배경 이미지 인디케이터 */}
      {!isAuthModalOpen && (
        <div className="fixed top-20 right-4 flex space-x-2 z-40 theme-bg-card backdrop-blur-sm rounded-full p-2 theme-border border">
          {getBackgroundForTheme(theme).map((_, index) => (
            <motion.div
              key={index}
              className={`w-3 h-3 rounded-full cursor-pointer transition-all duration-300 ${
                index === currentBgImage 
                  ? 'theme-accent shadow-lg' 
                  : theme === 'light' 
                    ? 'bg-purple-400/60 hover:bg-purple-500' 
                    : 'bg-white/50 hover:bg-white/70'
              }`}
              style={{
                backgroundColor: index === currentBgImage 
                  ? 'var(--theme-accent)' 
                  : undefined
              }}
              onClick={() => setCurrentBgImage(index)}
              whileHover={{ scale: 1.2 }}
              whileTap={{ scale: 0.8 }}
            />
          ))}
        </div>
      )}

      {/* 메인 콘텐츠 */}
      <div className="relative z-10">
        <Header 
          viewMode={viewMode}
          onViewModeChange={setViewMode}
          apiStatus={apiHealth?.status || 'unknown'}
          currentPage={currentPage}
          onPageChange={handlePageChange}
          onAuthModalStateChange={setIsAuthModalOpen}
        />

        {useHybridNavigation ? (
          <RouteAwareNavigation
            currentPage={currentPage}
            onPageChange={handlePageChange}
            viewMode={viewMode}
            routingMode="router_hybrid"
            onUrlChange={handleUrlChange}
          />
        ) : (
          <Navigation 
            currentPage={currentPage}
            onPageChange={handlePageChange}
            viewMode={viewMode}
          />
        )}

        <main className={currentPage === 'admin' ? '' : 'container mx-auto px-4 py-8'}>
          <AnimatePresence mode="wait">
            <motion.div
              key={currentPage}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {currentPage === 'dashboard' && (
                <EnhancedDashboard viewMode={viewMode} />
              )}
              {currentPage === 'saju' && (
                <SajuCalculator viewMode={viewMode} />
              )}
              {currentPage === 'tarot' && (
                <InteractiveTarotReader viewMode={viewMode} />
              )}
              {currentPage === 'magazine' && (
                <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="text-white">매거진 로딩 중...</div></div>}>
                  <Magazine viewMode={viewMode} />
                </Suspense>
              )}
              {currentPage === 'consultation' && (
                <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="text-white">상담 페이지 로딩 중...</div></div>}>
                  <Consultation viewMode={viewMode} />
                </Suspense>
              )}
              {currentPage === 'store' && (
                <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="text-white">스토어 로딩 중...</div></div>}>
                  <Store viewMode={viewMode} />
                </Suspense>
              )}
              {currentPage === 'notices' && (
                <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="text-white">공지사항 로딩 중...</div></div>}>
                  <Notices viewMode={viewMode} />
                </Suspense>
              )}
              {currentPage === 'subscription' && (
                <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="text-white">구독 페이지 로딩 중...</div></div>}>
                  <Notices viewMode={viewMode} initialView="subscription" />
                </Suspense>
              )}
              {currentPage === 'profile' && (
                <div className="text-center py-20">
                  <h2 className="text-3xl font-bold text-white mb-4">
                    🎮 사용자 프로필
                  </h2>
                  <p className="text-gray-300">
                    게이미피케이션 시스템 - 구현 예정 (공지사항에서 프로필 확인 가능)
                  </p>
                  <motion.button
                    className="mt-4 px-6 py-3 rounded-lg font-medium btn-cosmic"
                    onClick={() => setCurrentPage('notices')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    📢 공지사항에서 프로필 보기
                  </motion.button>
                </div>
              )}
              {currentPage === 'fortune' && (
                <FortuneCategories 
                  viewMode={viewMode} 
                  onCategorySelect={(category) => setCurrentPage(category as CurrentPage)}
                />
              )}
              {currentPage === 'zodiac' && (
                <ZodiacAnalysis viewMode={viewMode} />
              )}
              {currentPage === 'personality' && (
                <PersonalityProfile />
              )}
              {currentPage === 'love' && (
                <LoveFortuneAnalysis />
              )}
              {currentPage === 'compatibility' && (
                <CompatibilityAnalysis viewMode={viewMode} />
              )}
              {currentPage === 'dream' && (
                <DreamInterpretation viewMode={viewMode} />
              )}
              {currentPage === 'calendar' && (
                <FortuneCalendar viewMode={viewMode} />
              )}
              {currentPage === 'admin' && (
                <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><div className="text-white">관리자 페이지 로딩 중...</div></div>}>
                  {adminAuthenticated ? (
                    <SajuAdminDashboard 
                      onLogout={() => {
                        localStorage.removeItem('heal7_admin_authenticated');
                        localStorage.removeItem('heal7_admin_login_time');
                        localStorage.removeItem('heal7_admin_session_id');
                        setAdminAuthenticated(false);
                        console.log('Admin logged out - all session data cleared');
                      }} 
                    />
                  ) : (
                    <AdminLogin onAuthenticated={() => {
                      console.log('Admin authentication successful');
                      setAdminAuthenticated(true);
                    }} />
                  )}
                </Suspense>
              )}
            </motion.div>
          </AnimatePresence>
        </main>

        <footer className="text-center py-8 text-gray-300 text-sm border-t border-gray-700/50 bg-black/30 backdrop-blur-sm">
          <div className="max-w-4xl mx-auto px-4">
            <div className="mb-6">
              <h3 className="text-lg font-bold text-white mb-2">🧙‍♀️ 치유 마녀 (HEAL-WITCH)</h3>
              <p className="text-gray-400">전통 명리학과 현대 기술의 만남</p>
            </div>

            <div className="mb-6">
              <h4 className="font-semibold text-white mb-3">빠른 메뉴</h4>
              <div className="flex flex-wrap items-center justify-center gap-3">
                <button 
                  onClick={() => setCurrentPage('saju')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  🔮 사주명리
                </button>
                <button 
                  onClick={() => setCurrentPage('tarot')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  🃏 타로카드
                </button>
                <button 
                  onClick={() => setCurrentPage('dream')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  🌙 꿈풀이
                </button>
                <button 
                  onClick={() => setCurrentPage('calendar')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  📅 운세달력
                </button>
                <button 
                  onClick={() => setCurrentPage('fortune')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  ⭐ 운세
                </button>
                <button 
                  onClick={() => setCurrentPage('consultation')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  💬 상담
                </button>
                <button 
                  onClick={() => setCurrentPage('store')}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white/90 hover:text-white"
                >
                  🛍️ 스토어
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h4 className="font-semibold text-white mb-2">연락처</h4>
                <p>📞 050-7722-7328</p>
                <p>✉️ arne40@heal7.com</p>
                <p>📍 인천광역시 미추홀구 석정로 229, 5층 505호-06호</p>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-2">사업자 정보</h4>
                <p>© 2025 (주)노마드컴퍼니. All rights reserved.</p>
                <p>대표자: 김희정</p>
                <p>사업자등록번호: 832-87-03176</p>
                <p>통신판매업신고: 제 2024-인천미추홀-1104호</p>
                <p>직업정보제공사업신고: J1500020250005</p>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App