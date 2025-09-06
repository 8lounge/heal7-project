import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { useWeatherTheme } from '../../hooks/useWeatherTheme'
import { 
  dailyFortuneData, 
  trendingTopics, 
  mzCategories,
  trendingKeywords 
} from '../../data/mzContentData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface EnhancedDashboardProps {
  viewMode: ViewMode
}


const EnhancedDashboard: React.FC<EnhancedDashboardProps> = ({ viewMode }) => {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const { theme } = useWeatherTheme()
  const [showShareModal, setShowShareModal] = useState(false)
  const [shareContent, setShareContent] = useState('')
  const [animatedNumber, setAnimatedNumber] = useState(0)
  const [targetNumber] = useState(Math.floor(Math.random() * 300 + 1200)) // 1200-1500 범위

  // API 헬스체크 - 서버 로드 최적화 (중복 호출 제거)
  const { data: apiHealth } = useQuery({
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
    enabled: false, // 대시보드에서는 별도 헬스체크 비활성화
    initialData: { status: 'healthy', service: 'heal7-api', version: '2.0.0' }
  })

  // 오늘의 운세 자동 슬라이드
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % dailyFortuneData.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [])

  // 숫자 애니메이션 효과
  useEffect(() => {
    const duration = 2000 // 2초 동안 애니메이션
    const steps = 60
    const stepValue = targetNumber / steps
    let current = 0

    const timer = setInterval(() => {
      current += stepValue
      if (current >= targetNumber) {
        setAnimatedNumber(targetNumber)
        clearInterval(timer)
      } else {
        setAnimatedNumber(Math.floor(current))
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [targetNumber])


  // 현재 시간 기반 인사말
  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 6) return { text: '새벽에도 운세가 궁금하신가요? 🌙', emoji: '🌙' }
    if (hour < 12) return { text: '좋은 아침이에요! 오늘 운세 확인해볼까요? ☀️', emoji: '☀️' }
    if (hour < 18) return { text: '오후에도 운세 체크는 필수죠! 🌤️', emoji: '🌤️' }
    if (hour < 22) return { text: '저녁 운세로 하루 마무리해요 🌆', emoji: '🌆' }
    return { text: '늦은 밤까지 운세에 관심이 많으시네요! 🌃', emoji: '🌃' }
  }

  const greeting = getGreeting()

  // 공유하기 함수
  const handleShare = (content: string) => {
    setShareContent(content)
    setShowShareModal(true)
  }

  // 카테고리별 필터링 (현재는 모든 운세 표시)
  // const filteredFortunes = selectedCategory === 'all' 
  //   ? dailyFortuneData 
  //   : dailyFortuneData.filter(f => f.category === selectedCategory)

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
  const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white'

  return (
    <motion.div
      className="max-w-7xl mx-auto space-y-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* 개인화된 웰컴 섹션 */}
      <motion.section 
        className={`${cardClass} p-8 text-center relative overflow-hidden`}
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        {viewMode === 'cyber_fantasy' && (
          <div className="absolute inset-0 gradient-theme-primary-30 opacity-30" />
        )}
        
        <motion.div 
          className="relative z-10"
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.4, type: 'spring' }}
        >
          <div className="text-6xl mb-4">{greeting.emoji}</div>
          <h1 className={`text-3xl md:text-4xl font-bold mb-4 ${textClass}`}>
            🧙‍♀️ 치유 마녀 플랫폼
          </h1>
          <p className={`text-xl mb-4 ${textClass.replace('text-', 'text-opacity-90 text-')}`}>
            삶의 방향을 찾는 당신의 나침반
          </p>
          <p className={`text-lg mb-6 ${textClass.replace('text-', 'text-opacity-80 text-')}`}>
            마음의 평안 • 현명한 선택 • 따뜻한 조언
          </p>
          
          {/* 실시간 상태 표시 */}
          <div className="flex flex-col md:flex-row items-center justify-center space-y-2 md:space-y-0 md:space-x-6 text-sm">
            <div className="flex items-center">
              <div className={`w-2 h-2 rounded-full ${apiHealth?.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400'} mr-2`} />
              <span className="text-gray-300">
                {apiHealth?.status === 'healthy' ? '✨ 치유 시스템 운영 중' : '🔧 시스템 점검 중'}
              </span>
            </div>
            <span className="text-gray-400 hidden md:block">•</span>
            <div className="flex items-center">
              <span className="text-gray-300">📊 오늘&nbsp;</span>
              <motion.span 
                className="text-4xl font-bold text-white mx-2"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ 
                  delay: 0.8,
                  type: 'spring',
                  stiffness: 200,
                  damping: 10 
                }}
              >
                {animatedNumber.toLocaleString()}
              </motion.span>
              <span className="text-gray-300">명이 치유를 받았어요</span>
            </div>
          </div>
        </motion.div>
      </motion.section>

      {/* 트렌딩 키워드 */}
      <motion.section
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <h2 className={`text-xl font-bold mb-4 ${textClass} flex items-center`}>
          🔥 지금 HOT한 키워드
        </h2>
        <div className="flex flex-wrap gap-3">
          {trendingKeywords.map((keyword, index) => (
            <motion.span
              key={keyword}
              className={`px-4 py-2 rounded-full text-sm font-medium cursor-pointer transition-all
                ${viewMode === 'cyber_fantasy' 
                  ? 'gradient-theme-primary-30 text-theme-primary hover:opacity-80' 
                  : 'gradient-theme-primary-30 text-theme-primary hover:opacity-80'
                }`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.8 + index * 0.1 }}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
            >
              #{keyword}
            </motion.span>
          ))}
        </div>
      </motion.section>

      {/* 오늘의 운세 스토리 */}
      <motion.section
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 1.0 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className={`text-2xl font-bold ${textClass} flex items-center`}>
            📱 오늘의 운세 스토리
          </h2>
          <div className="flex space-x-2">
            {dailyFortuneData.map((_, index) => (
              <button
                key={index}
                className={`w-2 h-2 rounded-full transition-all ${
                  index === currentSlide ? 'bg-theme-primary' : 'bg-gray-600'
                }`}
                onClick={() => setCurrentSlide(index)}
              />
            ))}
          </div>
        </div>

        <div className="relative h-96 overflow-hidden">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              className={`${cardClass} p-8 h-full flex flex-col justify-between`}
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -100 }}
              transition={{ duration: 0.5 }}
            >
              <div>
                <div className="text-4xl mb-4">{dailyFortuneData[currentSlide].emoji}</div>
                <h3 className={`text-2xl font-bold mb-2 ${textClass}`}>
                  {dailyFortuneData[currentSlide].title}
                </h3>
                <p className="text-gray-300 text-lg mb-4">
                  {dailyFortuneData[currentSlide].subtitle}
                </p>
                <p className="text-gray-200 leading-relaxed mb-6">
                  {dailyFortuneData[currentSlide].content}
                </p>
                
                {/* 키워드 태그 */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {dailyFortuneData[currentSlide].keywords.map((keyword, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-black/30 text-gray-300 text-sm rounded-full"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
                
                {/* MZ슬랭 */}
                {dailyFortuneData[currentSlide].mzSlang && (
                  <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 p-3 rounded-lg">
                    <p className="text-yellow-200 text-sm font-medium">
                      💬 {dailyFortuneData[currentSlide].mzSlang}
                    </p>
                  </div>
                )}
              </div>

              {/* 하단 액션 */}
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-2">
                  {Array.from({length: 5}).map((_, i) => (
                    <span 
                      key={i}
                      className={`text-xl ${
                        i < dailyFortuneData[currentSlide].score ? '⭐' : '☆'
                      }`}
                    >
                      {i < dailyFortuneData[currentSlide].score ? '⭐' : '☆'}
                    </span>
                  ))}
                  <span className="text-gray-300 text-sm ml-2">
                    {dailyFortuneData[currentSlide].score}/5
                  </span>
                </div>
                
                <motion.button
                  className="flex items-center space-x-2 px-4 py-2 gradient-theme-primary text-theme-primary rounded-full text-sm font-medium"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleShare(dailyFortuneData[currentSlide].shareText)}
                >
                  <span>📤</span>
                  <span>공유하기</span>
                </motion.button>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </motion.section>

      {/* 카테고리별 운세 */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
      >
        <h2 className={`text-2xl font-bold mb-6 ${textClass}`}>
          🎯 관심사별 맞춤 운세
        </h2>

        {/* 카테고리 탭 */}
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedCategory === 'all'
                ? 'bg-theme-primary text-theme-primary'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
            onClick={() => setSelectedCategory('all')}
          >
            전체
          </button>
          {mzCategories.map((category) => (
            <button
              key={category.id}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                selectedCategory === category.id
                  ? 'bg-theme-primary text-theme-primary'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
              onClick={() => setSelectedCategory(category.id)}
            >
              {category.emoji} {category.name}
            </button>
          ))}
        </div>

        {/* 카테고리별 그리드 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mzCategories.map((category) => (
            <motion.div
              key={category.id}
              className={`${cardClass} p-6 cursor-pointer group`}
              whileHover={{ scale: 1.03, y: -5 }}
              whileTap={{ scale: 0.97 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.4 }}
            >
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">
                {category.emoji}
              </div>
              <h3 className={`text-xl font-bold mb-2 ${textClass}`}>
                {category.name}
              </h3>
              <p className="text-gray-300 text-sm mb-4">
                {category.description}
              </p>
              
              <div className="flex flex-wrap gap-1 mb-4">
                {category.subcategories.slice(0, 3).map((sub, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-black/20 text-xs text-gray-400 rounded"
                  >
                    {sub}
                  </span>
                ))}
                {category.subcategories.length > 3 && (
                  <span className="px-2 py-1 text-xs text-gray-500">
                    +{category.subcategories.length - 3}
                  </span>
                )}
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">
                  오늘 운세 확인하기
                </span>
                <span className="text-white">→</span>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* 트렌딩 토픽 */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6 }}
      >
        <h2 className={`text-2xl font-bold mb-6 ${textClass}`}>
          📈 지금 뜨는 운세 토픽
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {trendingTopics.slice(0, 4).map((topic, index) => (
            <motion.div
              key={topic.id}
              className={`${cardClass} p-6 cursor-pointer`}
              whileHover={{ scale: 1.02 }}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.8 + index * 0.1 }}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="text-3xl">{topic.emoji}</div>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-400">인기도</span>
                  <div className="w-16 h-2 bg-gray-700 rounded-full">
                    <div 
                      className="h-full gradient-theme-primary rounded-full"
                      style={{ width: `${topic.popularity}%` }}
                    />
                  </div>
                  <span className="text-sm text-white">{topic.popularity}%</span>
                </div>
              </div>

              <h3 className={`text-lg font-bold mb-2 ${textClass}`}>
                {topic.title}
              </h3>
              <p className="text-gray-300 text-sm mb-4">
                {topic.description}
              </p>

              <div className="flex flex-wrap gap-2">
                {topic.tags.map((tag, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-theme-primary-20 text-theme-primary text-xs rounded"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* 공유 모달 */}
      <AnimatePresence>
        {showShareModal && (
          <motion.div
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowShareModal(false)}
          >
            <motion.div
              className={`${cardClass} p-8 max-w-md w-full`}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className={`text-xl font-bold mb-4 ${textClass}`}>
                📤 운세 공유하기
              </h3>
              
              <textarea
                className="w-full h-24 p-4 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 resize-none"
                value={shareContent}
                onChange={(e) => setShareContent(e.target.value)}
                placeholder="운세를 공유해보세요..."
              />

              <div className="flex space-x-4 mt-6">
                <button
                  className="flex-1 py-3 gradient-theme-primary text-theme-primary rounded-lg font-medium"
                  onClick={() => {
                    navigator.share && navigator.share({
                      title: '치유마녀 운세',
                      text: shareContent,
                      url: window.location.href
                    })
                    setShowShareModal(false)
                  }}
                >
                  📱 모바일 공유
                </button>
                <button
                  className="flex-1 py-3 bg-gray-600 hover:bg-gray-500 text-white rounded-lg font-medium"
                  onClick={() => {
                    navigator.clipboard.writeText(shareContent)
                    setShowShareModal(false)
                  }}
                >
                  📋 복사하기
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export default EnhancedDashboard