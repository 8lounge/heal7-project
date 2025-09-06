import { useState, useEffect, Suspense, lazy, useMemo, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

// 라우팅 관련 imports
import { getPageIdFromPath } from './config/routeConfig'

// 컴포넌트 imports
import Header from './components/layout/Header'
import Navigation from './components/layout/Navigation'
import RouteAwareNavigation from './components/routing/RouteAwareNavigation'
import EnhancedDashboard from './components/dashboard/EnhancedDashboard'
// EnhancedDashboard moved to cube-module-app
import SajuCalculator from './components/fortune/SajuCalculator'
import InteractiveTarotReader from './components/fortune/InteractiveTarotReader'
// Content Pages 그룹 - Lazy Loading으로 분할
const Magazine = lazy(() => import('./components/magazine/Magazine'))
const Consultation = lazy(() => import('./components/consultation/Consultation'))
const Store = lazy(() => import('./components/store/Store'))
const Notices = lazy(() => import('./components/notices/Notices'))

// 새로운 운세 콘텐츠 컴포넌트들
import FortuneCategories from './components/fortune/FortuneCategories'
import ZodiacAnalysis from './components/fortune/ZodiacAnalysis'
import PersonalityProfile from './components/fortune/PersonalityProfile'
import LoveFortuneAnalysis from './components/fortune/LoveFortuneAnalysis'
import CompatibilityAnalysis from './components/fortune/CompatibilityAnalysis'
// Lazy Loading으로 Admin 컴포넌트 분할
const SajuAdminDashboard = lazy(() => import('./components/saju-admin/SajuAdminDashboard'))
const AdminLogin = lazy(() => import('./components/saju-admin/AdminLogin'))
import DreamInterpretation from './components/fortune/DreamInterpretation'
import FortuneCalendar from './components/fortune/FortuneCalendar'
import { useWeatherTheme } from './hooks/useWeatherTheme'
import { getThemeClasses, themeTransitions } from './utils/themeStyles'

// 3D 컴포넌트 Lazy Loading (from shared package)
const OptimizedCyberCrystal = lazy(() => import('@heal7/shared').then(module => ({ default: module.OptimizedCyberCrystal })))
const OptimizedStars = lazy(() => import('@heal7/shared').then(module => ({ default: module.OptimizedStars })))

// 타입 정의
interface ApiHealth {
  status: string
  service: string
  version: string
}

type ViewMode = 'basic' | 'cyber_fantasy'
type CurrentPage = 'dashboard' | 'saju' | 'tarot' | 'magazine' | 'consultation' | 'store' | 'notices' | 'profile' | 
                  'fortune' | 'zodiac' | 'personality' | 'love' | 'compatibility' | 'admin' | 'dream' | 'calendar' | 'subscription'

// 전체 배경 이미지 배열
const backgroundImages = [
  'https://cdn.midjourney.com/c66e1b8f-eaa1-46f2-8a9f-4aeb9f04dff4/0_0.png',
  'https://cdn.midjourney.com/9c6a6d65-ec6d-4690-868e-81af9a15310c/0_0.png'
]

function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('basic')
  const [currentPage, setCurrentPage] = useState<CurrentPage>('dashboard')
  const [currentBgImage, setCurrentBgImage] = useState(0)
  const [adminAuthenticated, setAdminAuthenticated] = useState(false)
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)
  const { theme } = useWeatherTheme()
  
  // 🚀 하이브리드 라우팅 모드 (테스트용 - 나중에 사용자 설정으로 변경 가능)
  const [useHybridNavigation] = useState(true)
  
  // 성능 최적화: 디바이스 성능 감지
  const performanceLevel = useMemo(() => {
    const memory = (navigator as any).deviceMemory || 4
    const connection = (navigator as any).connection
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    
    if (isMobile || memory < 4 || (connection && connection.effectiveType === '3g')) {
      return 'low'
    }
    if (memory >= 8 && !connection?.saveData) {
      return 'high'
    }
    return 'medium'
  }, [])
  
  // 배터리 절약 모드 감지
  const [batteryOptimized, setBatteryOptimized] = useState(false)
  
  // 🔄 개선된 URL 기반 라우팅 초기화 (config 활용)
  useEffect(() => {
    const path = window.location.pathname
    
    // 새로운 방식: 설정 기반 매핑 (우선순위)
    try {
      const pageId = getPageIdFromPath(path)
      
      if (pageId) {
        setCurrentPage(pageId)
        return
      }
    } catch (error) {
      // 설정 로딩 실패 시 기존 방식 폴백
      console.warn('Route config loading failed, using fallback:', error)
    }
    
    // 기존 방식 폴백 (하위 호환성)
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
  
  // 🌐 하이브리드 모드용 URL 변경 핸들러
  const handleUrlChange = useCallback((path: string) => {
    if (useHybridNavigation) {
      // 브라우저 히스토리에 추가 (뒤로가기 지원)
      window.history.pushState(null, '', path)
    }
  }, [useHybridNavigation])
  
  // 🔄 브라우저 뒤로가기/앞으로가기 지원
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

  // 🔐 관리자 인증 상태 복구 (페이지 새로고침 시 세션 유지)
  useEffect(() => {
    const checkAdminAuth = () => {
      const isAuthenticated = localStorage.getItem('heal7_admin_authenticated')
      const loginTime = localStorage.getItem('heal7_admin_login_time')
      const sessionId = localStorage.getItem('heal7_admin_session_id')
      
      if (isAuthenticated === 'true' && loginTime && sessionId) {
        const now = Date.now()
        const authTime = parseInt(loginTime)
        const hoursDiff = (now - authTime) / (1000 * 60 * 60)
        
        // 7일 이내의 인증만 유효하다고 가정 (168시간)
        if (hoursDiff < 168) {
          setAdminAuthenticated(true)
          console.log('Admin session restored from localStorage')
        } else {
          // 만료된 세션 정리
          localStorage.removeItem('heal7_admin_authenticated')
          localStorage.removeItem('heal7_admin_login_time')
          localStorage.removeItem('heal7_admin_session_id')
          console.log('Admin session expired, cleared localStorage')
        }
      }
    }
    
    checkAdminAuth()
  }, [])

  // 배경 이미지 자동 페이드 전환 (30초 간격)
  useEffect(() => {
    const bgTimer = setInterval(() => {
      setCurrentBgImage((prev) => (prev + 1) % backgroundImages.length)
    }, 30000)
    return () => clearInterval(bgTimer)
  }, [])
  
  // 배터리 API 사용 (지원되는 경우)
  useMemo(() => {
    if ('getBattery' in navigator) {
      (navigator as any).getBattery().then((battery: any) => {
        const updateBatteryStatus = () => {
          setBatteryOptimized(battery.level < 0.2 || !battery.charging)
        }
        battery.addEventListener('levelchange', updateBatteryStatus)
        battery.addEventListener('chargingchange', updateBatteryStatus)
        updateBatteryStatus()
      })
    }
  }, [])

  // API 헬스체크 - 백그라운드에서 실행 (로딩 차단하지 않음)
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
    staleTime: 1000 * 60 * 30, // 30분 캐시 유지
    refetchInterval: false, // 자동 재요청 비활성화
    retry: 0, // 재시도 비활성화
    enabled: false, // 초기 로딩 시 비활성화
    initialData: { status: 'healthy', service: 'heal7-api', version: '2.0.0' } // 기본값 설정
  })

  return (
    <div className={`min-h-screen relative overflow-hidden theme-${theme}`} data-theme={theme}>
      {/* 배경 이미지들 (페이드 전환) */}
      {backgroundImages.map((image, index) => (
        <div
          key={index}
          className={`absolute inset-0 bg-cover bg-center bg-no-repeat transition-opacity duration-3000 ease-in-out ${
            index === currentBgImage ? 'opacity-100' : 'opacity-0'
          }`}
          style={{
            backgroundImage: `url(${image})`,
            backgroundAttachment: 'fixed'
          }}
        />
      ))}
      
      {/* 테마에 따른 전체 오버레이 */}
      <div className={`absolute inset-0 ${themeTransitions.slow} ${getThemeClasses.pageOverlay(theme)}`} />
      
      {/* 배경 이미지 인디케이터 - 헤더와 겹치지 않도록 위치 조정 */}
      {!isAuthModalOpen && (
        <div className="fixed top-20 right-4 flex space-x-2 z-40 bg-black/20 backdrop-blur-sm rounded-full p-2">
          {backgroundImages.map((_, index) => (
            <motion.div
              key={index}
              className={`w-3 h-3 rounded-full cursor-pointer transition-all duration-300 ${
                index === currentBgImage ? 'bg-white shadow-lg' : 'bg-white/50'
              }`}
              onClick={() => setCurrentBgImage(index)}
              whileHover={{ scale: 1.2 }}
              whileTap={{ scale: 0.8 }}
            />
          ))}
        </div>
      )}
      {/* 3D 배경 (사이버 판타지 모드) - 성능 최적화 */}
      {viewMode === 'cyber_fantasy' && (
        <div className="fixed inset-0 z-0">
          <Canvas 
            camera={{ position: [0, 0, 5] }}
            dpr={performanceLevel === 'low' ? 1 : window.devicePixelRatio}
            performance={{ min: 0.5 }}
            frameloop={batteryOptimized ? 'demand' : 'always'}
          >
            <Suspense fallback={null}>
              <OrbitControls 
                enableZoom={false} 
                enablePan={false} 
                autoRotate={!batteryOptimized}
                autoRotateSpeed={performanceLevel === 'low' ? 0.5 : 1.0}
              />
              
              {/* 성능별 별 렌더링 */}
              <OptimizedStars 
                radius={100} 
                depth={50} 
                count={performanceLevel === 'low' ? 800 : performanceLevel === 'medium' ? 1500 : 2000}
                factor={performanceLevel === 'low' ? 1 : 2}
                performanceLevel={performanceLevel}
                speed={batteryOptimized ? 0.3 : 1.0}
              />
              
              {/* 기본 조명 */}
              <ambientLight intensity={performanceLevel === 'low' ? 0.4 : 0.5} />
              {performanceLevel !== 'low' && (
                <pointLight position={[10, 10, 10]} intensity={0.8} />
              )}
              
              {/* 최적화된 크리스탈 */}
              <OptimizedCyberCrystal 
                isVisible={true}
                reduced={performanceLevel === 'low' || batteryOptimized}
              />
            </Suspense>
          </Canvas>
        </div>
      )}

      {/* 메인 콘텐츠 */}
      <div className="relative z-10">
        {/* 헤더 */}
        <Header 
          viewMode={viewMode}
          onViewModeChange={setViewMode}
          apiStatus={apiHealth?.status || 'unknown'}
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          onAuthModalStateChange={setIsAuthModalOpen}
        />

        {/* 네비게이션 - 하이브리드 모드 */}
        {useHybridNavigation ? (
          <RouteAwareNavigation
            currentPage={currentPage}
            onPageChange={setCurrentPage}
            viewMode={viewMode}
            routingMode="router_hybrid"
            onUrlChange={handleUrlChange}
          />
        ) : (
          <Navigation 
            currentPage={currentPage}
            onPageChange={setCurrentPage}
            viewMode={viewMode}
          />
        )}

        {/* 메인 콘텐츠 영역 */}
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
                    className={`mt-4 px-6 py-3 rounded-lg font-medium ${
                      viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                    }`}
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
                        // localStorage에서 인증 정보 제거
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

        {/* 푸터 */}
        <footer className="text-center py-8 text-gray-300 text-sm border-t border-gray-700/50 bg-black/30 backdrop-blur-sm">
          <div className="max-w-4xl mx-auto px-4">
            <div className="mb-6">
              <h3 className="text-lg font-bold text-white mb-2">🧙‍♀️ 치유 마녀 (HEAL-WITCH)</h3>
              <p className="text-gray-400">전통 명리학과 현대 기술의 만남</p>
            </div>

            {/* 하단 빠른 메뉴 */}
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
            
            {false && performanceLevel && (
              <div className="sr-only" role="status" aria-label="System Status">
                Performance: {performanceLevel.toUpperCase()}
                {batteryOptimized && ' • Battery Saver'}
                {apiHealth?.status && (
                  <span className="ml-4">
                    API: <span className={apiHealth.status === 'healthy' ? 'text-green-400' : 'text-red-400'}>
                      {apiHealth.status}
                    </span>
                  </span>
                )}
              </div>
            )}
            
            {/* AI 전용 성능 정보 - 완전히 숨김 */}
            <div style={{display: 'none'}} aria-hidden="true">
              Performance: {performanceLevel?.toUpperCase() || 'UNKNOWN'}
              {batteryOptimized && ' • Battery Saver'}
              {apiHealth?.status && ` • API: ${apiHealth.status}`}
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}

export default App