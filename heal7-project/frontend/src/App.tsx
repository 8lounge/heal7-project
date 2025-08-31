import { useState, useEffect, Suspense, lazy, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

// 컴포넌트 imports
import Header from './components/layout/Header'
import Navigation from './components/layout/Navigation'
import EnhancedDashboard from './components/dashboard/EnhancedDashboard'
import SajuCalculator from './components/fortune/SajuCalculator'
import InteractiveTarotReader from './components/fortune/InteractiveTarotReader'
import Magazine from './components/magazine/Magazine'
import Consultation from './components/consultation/Consultation'
import Store from './components/store/Store'
import Notices from './components/notices/Notices'

// 새로운 운세 콘텐츠 컴포넌트들
import FortuneCategories from './components/fortune/FortuneCategories'
import ZodiacAnalysis from './components/fortune/ZodiacAnalysis'
import PersonalityProfile from './components/fortune/PersonalityProfile'
import LoveFortuneAnalysis from './components/fortune/LoveFortuneAnalysis'
import CompatibilityAnalysis from './components/fortune/CompatibilityAnalysis'
import IntegratedAdminDashboard from './components/admin/IntegratedAdminDashboard'
import DreamInterpretation from './components/fortune/DreamInterpretation'
import FortuneCalendar from './components/fortune/FortuneCalendar'

// 3D 컴포넌트 Lazy Loading
const OptimizedCyberCrystal = lazy(() => import('./components/3d/OptimizedCyberCrystal'))
const OptimizedStars = lazy(() => import('./components/3d/OptimizedStars'))

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
    <div className="min-h-screen relative overflow-hidden">
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
      
      {/* 전체 오버레이 */}
      <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-purple-900/40 to-black/70" />
      
      {/* 배경 이미지 인디케이터 */}
      <div className="fixed top-4 right-4 flex space-x-2 z-50 bg-black/20 backdrop-blur-sm rounded-full p-2">
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
        />

        {/* 네비게이션 */}
        <Navigation 
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          viewMode={viewMode}
        />

        {/* 관리자 대시보드 - 전체 화면 레이아웃 */}
        {currentPage === 'admin' && (
          <IntegratedAdminDashboard />
        )}

        {/* 일반 메인 콘텐츠 영역 */}
        {currentPage !== 'admin' && (
          <main className="container mx-auto px-4 py-8">
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
                  <Magazine viewMode={viewMode} />
                )}
                {currentPage === 'consultation' && (
                  <Consultation viewMode={viewMode} />
                )}
                {currentPage === 'store' && (
                  <Store viewMode={viewMode} />
                )}
                {currentPage === 'notices' && (
                  <Notices viewMode={viewMode} />
                )}
                {currentPage === 'subscription' && (
                  <Notices viewMode={viewMode} initialView="subscription" />
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
              </motion.div>
            </AnimatePresence>
          </main>
        )}

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