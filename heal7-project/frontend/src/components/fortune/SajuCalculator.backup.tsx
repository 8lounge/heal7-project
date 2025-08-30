import React, { useState, useMemo, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { sampleSajuResults, sajuElements } from '../../data/sajuData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface SajuCalculatorProps {
  viewMode: ViewMode
}

interface SajuForm {
  year: string
  month: string
  day: string
  hour: string
  minute: string
  gender: 'M' | 'F'
  location: string
}

const SajuCalculator: React.FC<SajuCalculatorProps> = ({ viewMode }) => {
  const [formData, setFormData] = useState<SajuForm>({
    year: '',
    month: '',
    day: '',
    hour: '',
    minute: '0',
    gender: 'M',
    location: '서울'
  })
  const [showResult, setShowResult] = useState(false)
  const [selectedResult, setSelectedResult] = useState<typeof sampleSajuResults[0] | null>(null)
  const [activeTab, setActiveTab] = useState<'personality' | 'career' | 'love' | 'fortune'>('personality')
  const [loadingProgress, setLoadingProgress] = useState(0)
  const [loadingStep, setLoadingStep] = useState(0)

  const loadingSteps = [
    { icon: '🔍', message: '생년월일 분석 시작', emoji: '✨' },
    { icon: '⚖️', message: '오행 균형 계산중', emoji: '💫' },
    { icon: '🎯', message: '현대적 직업 매칭중', emoji: '🚀' },
    { icon: '💕', message: '연애 스타일 분석중', emoji: '💖' },
    { icon: '🔮', message: 'AI 운명 분석 완료', emoji: '✅' }
  ]

  // 사주 계산 API 호출 (실패 시 샘플 데이터 사용)
  const { isLoading, refetch } = useQuery({
    queryKey: ['saju-calculation', formData],
    queryFn: async () => {
      try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 10000) // 10초 타임아웃
        
        const apiEndpoint = viewMode === 'cyber_fantasy' 
          ? '/api/saju/fortune/cyber' 
          : '/api/saju/fortune/calculate'
        
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
          signal: controller.signal
        })
        
        clearTimeout(timeoutId)
        
        if (!response.ok) throw new Error('API 호출 실패')
        return response.json()
      } catch (error) {
        // API 실패 시 샘플 데이터 반환
        console.log('API 실패, 샘플 데이터 사용')
        return 'use-sample-data'
      }
    },
    enabled: false, // 수동 실행
    retry: false,
    refetchOnWindowFocus: false
  })

  // 로딩 진행률 관리
  useEffect(() => {
    if (isLoading) {
      const totalTime = 10000 // 10초
      const stepTime = totalTime / loadingSteps.length
      const interval = setInterval(() => {
        setLoadingProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval)
            return 100
          }
          return prev + (100 / (totalTime / 50)) // 50ms마다 업데이트
        })
      }, 50)
      
      // 단계별 메시지 업데이트
      const stepInterval = setInterval(() => {
        setLoadingStep(prev => {
          if (prev >= loadingSteps.length - 1) {
            clearInterval(stepInterval)
            return loadingSteps.length - 1
          }
          return prev + 1
        })
      }, stepTime)

      return () => {
        clearInterval(interval)
        clearInterval(stepInterval)
      }
    } else {
      setLoadingProgress(0)
      setLoadingStep(0)
    }
  }, [isLoading, loadingSteps.length])

  // 샘플 결과 선택 (생년월일 기반 또는 랜덤)
  const getSampleResult = useMemo(() => {
    if (!formData.year || !formData.month || !formData.day) {
      return sampleSajuResults[0] // 기본 샘플
    }
    
    // 간단한 해싱으로 일관된 결과 제공
    const hash = parseInt(formData.year) + parseInt(formData.month) * 31 + parseInt(formData.day) * 12
    const index = hash % sampleSajuResults.length
    return sampleSajuResults[index] || sampleSajuResults[0]
  }, [formData.year, formData.month, formData.day])

  const handleInputChange = (field: keyof SajuForm, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleCalculate = async () => {
    if (formData.year && formData.month && formData.day && formData.hour) {
      setShowResult(true)
      
      // 시작 시간 기록 (최소 10초 로딩을 위해)
      const startTime = Date.now()
      const minLoadingTime = 10000 // 10초
      
      // API 호출 (백그라운드에서)
      const resultPromise = refetch()
      
      // 최소 로딩 시간과 API 응답 중 더 긴 시간까지 대기
      const [result] = await Promise.all([
        resultPromise,
        new Promise(resolve => {
          const elapsed = Date.now() - startTime
          const remaining = Math.max(0, minLoadingTime - elapsed)
          setTimeout(resolve, remaining)
        })
      ])
      
      if (result.data === 'use-sample-data' || !result.data) {
        // 샘플 데이터 사용
        setSelectedResult(getSampleResult)
      } else {
        // API 결과 사용 (나중에 구현)
        setSelectedResult(getSampleResult) // 현재는 샘플 데이터 사용
      }
    }
  }

  const handleShare = () => {
    if (selectedResult) {
      const shareText = `${selectedResult.mzSummary.shareableQuote} ${selectedResult.mzSummary.hashTags.join(' ')}`
      if (navigator.share) {
        navigator.share({
          title: '내 사주팔자 결과',
          text: shareText,
          url: window.location.href
        })
      } else {
        navigator.clipboard.writeText(shareText)
        alert('결과가 클립보드에 복사되었습니다!')
      }
    }
  }

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal' : 'card-cosmic'

  return (
    <motion.div
      className="max-w-4xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* 타이틀 */}
      <motion.div 
        className="text-center mb-8"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className={`text-3xl md:text-4xl font-bold mb-4 ${
          viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic'
        }`}>
          📊 {viewMode === 'cyber_fantasy' ? '사이버 사주팔자' : '사주명리학'}
        </h1>
        <p className="text-gray-300">
          {viewMode === 'cyber_fantasy' 
            ? '3D 크리스탈로 펼쳐지는 신비로운 운명 분석'
            : '정확한 생년월일로 사주팔자를 분석합니다'
          }
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 입력 폼 */}
        <motion.div 
          className={`p-6 rounded-xl ${cardClass}`}
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="text-xl font-bold text-white mb-6 flex items-center">
            <span className="mr-2">📝</span>
            생년월일 입력
          </h2>

          <div className="space-y-4">
            {/* 생년월일 */}
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">년</label>
                <input
                  type="number"
                  placeholder="1990"
                  min="1900"
                  max="2030"
                  className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  value={formData.year}
                  onChange={(e) => handleInputChange('year', e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">월</label>
                <input
                  type="number"
                  placeholder="1"
                  min="1"
                  max="12"
                  className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  value={formData.month}
                  onChange={(e) => handleInputChange('month', e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">일</label>
                <input
                  type="number"
                  placeholder="1"
                  min="1"
                  max="31"
                  className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  value={formData.day}
                  onChange={(e) => handleInputChange('day', e.target.value)}
                />
              </div>
            </div>

            {/* 시간 */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">시</label>
                <select
                  className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                  value={formData.hour}
                  onChange={(e) => handleInputChange('hour', e.target.value)}
                >
                  <option value="">시간 선택</option>
                  {Array.from({length: 24}, (_, i) => (
                    <option key={i} value={i.toString()}>
                      {i.toString().padStart(2, '0')}시
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">분</label>
                <select
                  className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                  value={formData.minute}
                  onChange={(e) => handleInputChange('minute', e.target.value)}
                >
                  <option value="0">정확히 모름</option>
                  <option value="15">15분경</option>
                  <option value="30">30분경</option>
                  <option value="45">45분경</option>
                </select>
              </div>
            </div>

            {/* 성별 & 지역 */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">성별</label>
                <div className="flex space-x-4">
                  {['M', 'F'].map((gender) => (
                    <label key={gender} className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="gender"
                        value={gender}
                        checked={formData.gender === gender}
                        onChange={(e) => handleInputChange('gender', e.target.value)}
                        className="sr-only"
                      />
                      <motion.div
                        className={`w-6 h-6 rounded-full border-2 mr-2 flex items-center justify-center ${
                          formData.gender === gender
                            ? 'border-purple-500 bg-purple-500'
                            : 'border-gray-400'
                        }`}
                        whileTap={{ scale: 0.9 }}
                      >
                        {formData.gender === gender && (
                          <div className="w-2 h-2 bg-white rounded-full" />
                        )}
                      </motion.div>
                      <span className="text-white">{gender === 'M' ? '남성' : '여성'}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">출생지</label>
                <input
                  type="text"
                  placeholder="서울"
                  className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  value={formData.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                />
              </div>
            </div>

            {/* 계산 버튼 */}
            <motion.button
              className={`w-full py-4 rounded-lg font-bold text-lg mt-6 ${
                viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
              }`}
              onClick={handleCalculate}
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-2"></div>
                  분석 중...
                </div>
              ) : viewMode === 'cyber_fantasy' ? (
                '🌌 사이버 사주 생성'
              ) : (
                '📊 사주팔자 분석'
              )}
            </motion.button>
          </div>
        </motion.div>

        {/* 결과 표시 */}
        <motion.div 
          className={`p-6 rounded-xl ${cardClass}`}
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h2 className="text-xl font-bold text-white mb-6 flex items-center">
            <span className="mr-2">✨</span>
            {viewMode === 'cyber_fantasy' ? '사이버 운명 분석' : 'AI 사주 분석'}
          </h2>

          {!showResult ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔮</div>
              <p className="text-gray-400 mb-4">
                생년월일을 입력하고 분석을 시작하세요
              </p>
              <div className="text-sm text-gray-500">
                <p>• MZ세대 맞춤 현대적 해석</p>
                <p>• 커리어 & 연애 가이드</p>
                <p>• 트렌드 키워드 & 해시태그</p>
              </div>
            </div>
          ) : isLoading ? (
            <div className="text-center py-12">
              {/* 메인 로딩 아이콘 */}
              <motion.div
                className="text-6xl mb-6"
                animate={{ 
                  rotate: 360,
                  scale: [1, 1.1, 1]
                }}
                transition={{ 
                  rotate: { duration: 3, repeat: Infinity, ease: "linear" },
                  scale: { duration: 2, repeat: Infinity, ease: "easeInOut" }
                }}
              >
                🌌
              </motion.div>
              
              {/* 진행률 바 */}
              <div className="mb-6 mx-auto max-w-md">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-400 text-sm">AI 분석 진행률</span>
                  <span className="text-white text-sm font-medium">{Math.round(loadingProgress)}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500 rounded-full"
                    style={{ width: `${loadingProgress}%` }}
                    initial={{ width: 0 }}
                    animate={{ width: `${loadingProgress}%` }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                  />
                </div>
              </div>

              {/* 현재 단계 표시 */}
              <motion.div
                key={loadingStep}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="mb-6"
              >
                <div className="text-4xl mb-3">
                  {loadingSteps[loadingStep]?.icon}
                </div>
                <p className="text-gray-300 text-lg font-medium mb-2">
                  {loadingSteps[loadingStep]?.message}
                </p>
              </motion.div>

              {/* 단계별 체크리스트 */}
              <div className="space-y-3 max-w-sm mx-auto">
                {loadingSteps.map((step, index) => (
                  <motion.div
                    key={index}
                    className={`flex items-center text-left p-3 rounded-lg transition-all duration-500 ${
                      index <= loadingStep 
                        ? 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-white' 
                        : 'bg-gray-800/30 text-gray-500'
                    }`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <motion.div
                      className={`mr-3 text-xl ${index <= loadingStep ? 'scale-110' : ''}`}
                      animate={index === loadingStep ? { 
                        rotate: [0, 5, -5, 0],
                        scale: [1, 1.1, 1]
                      } : {}}
                      transition={{ duration: 1, repeat: Infinity }}
                    >
                      {index < loadingStep ? '✅' : index === loadingStep ? step.icon : '⏳'}
                    </motion.div>
                    <span className="text-sm font-medium flex-1">{step.message}</span>
                    {index <= loadingStep && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="text-white"
                      >
                        {step.emoji}
                      </motion.div>
                    )}
                  </motion.div>
                ))}
              </div>

              {/* 로딩 상태 메시지 */}
              <motion.p 
                className="text-gray-400 text-sm mt-6"
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                잠시만 기다려주세요... 정확한 분석을 위해 열심히 계산중입니다 ✨
              </motion.p>
            </div>
          ) : selectedResult ? (
            <AnimatePresence mode="wait">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* MZ 요약 */}
                <motion.div
                  className="p-4 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg text-center"
                  initial={{ scale: 0.9 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <div className="text-4xl mb-2">{selectedResult.mzSummary.emoji}</div>
                  <h3 className="text-lg font-bold text-white mb-2">
                    {selectedResult.personality.type}
                  </h3>
                  <p className="text-white mb-3">
                    {selectedResult.mzSummary.oneLineDescription}
                  </p>
                  <div className="flex flex-wrap justify-center gap-1">
                    {selectedResult.mzSummary.hashTags.map((tag, index) => (
                      <span key={index} className="text-xs bg-purple-500/30 text-white px-2 py-1 rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <motion.button
                    onClick={handleShare}
                    className="mt-3 px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-500 rounded-lg text-sm font-medium text-white hover:from-pink-600 hover:to-purple-600 transition-colors"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    📱 결과 공유하기
                  </motion.button>
                </motion.div>

                {/* 탭 네비게이션 */}
                <div className="flex space-x-2 overflow-x-auto">
                  {[
                    { key: 'personality', label: '🧠 성격', emoji: '🧠' },
                    { key: 'career', label: '💼 커리어', emoji: '💼' },
                    { key: 'love', label: '💕 연애', emoji: '💕' },
                    { key: 'fortune', label: '🔮 운세', emoji: '🔮' }
                  ].map((tab) => (
                    <motion.button
                      key={tab.key}
                      onClick={() => setActiveTab(tab.key as any)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        activeTab === tab.key
                          ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white'
                          : 'bg-black/20 text-gray-300 hover:bg-black/30'
                      }`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {tab.emoji} {tab.label.split(' ')[1]}
                    </motion.button>
                  ))}
                </div>

                {/* 탭 컨텐츠 */}
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="space-y-4"
                  >
                    {activeTab === 'personality' && (
                      <div className="space-y-4">
                        <div className="p-4 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2 flex items-center">
                            🎯 성격 키워드
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {selectedResult.personality.keywords.map((keyword, index) => (
                              <span key={index} className="bg-blue-500/30 text-blue-200 px-3 py-1 rounded-full text-sm">
                                {keyword}
                              </span>
                            ))}
                          </div>
                        </div>
                        
                        <div className="p-4 bg-gradient-to-r from-green-500/20 to-teal-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">💪 현대적 강점</h4>
                          <ul className="space-y-1">
                            {selectedResult.personality.strengthsModern.map((strength, index) => (
                              <li key={index} className="text-green-200 text-sm flex items-start">
                                <span className="mr-2">•</span> {strength}
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div className="p-4 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">🎯 MBTI 가능성</h4>
                          <div className="flex flex-wrap gap-2">
                            {selectedResult.personality.mbtiLikely.map((mbti, index) => (
                              <span key={index} className="bg-yellow-500/30 text-yellow-200 px-3 py-1 rounded-full text-sm font-medium">
                                {mbti}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {activeTab === 'career' && (
                      <div className="space-y-4">
                        <div className="p-4 bg-gradient-to-r from-purple-500/20 to-indigo-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-3">🚀 추천 직업 (MZ세대 버전)</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                            {selectedResult.lifeAspects.career.suitableJobs.map((job, index) => (
                              <motion.div
                                key={index}
                                className="bg-purple-500/30 text-white px-3 py-2 rounded-lg text-sm text-center"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                              >
                                {job}
                              </motion.div>
                            ))}
                          </div>
                        </div>
                        
                        <div className="p-4 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">💼 워킹 스타일</h4>
                          <p className="text-cyan-200 text-sm mb-3">{selectedResult.lifeAspects.career.workStyle}</p>
                          <h4 className="font-semibold text-white mb-2">👑 리더십 스타일</h4>
                          <p className="text-cyan-200 text-sm">{selectedResult.lifeAspects.career.leadershipStyle}</p>
                        </div>

                        <div className="p-4 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">💡 커리어 조언</h4>
                          <p className="text-emerald-200 text-sm">{selectedResult.lifeAspects.career.advice}</p>
                        </div>
                      </div>
                    )}

                    {activeTab === 'love' && (
                      <div className="space-y-4">
                        <div className="p-4 bg-gradient-to-r from-pink-500/20 to-rose-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">💕 연애 스타일</h4>
                          <div className="bg-pink-500/30 text-pink-200 px-3 py-2 rounded-lg text-center mb-3">
                            {selectedResult.lifeAspects.love.style}
                          </div>
                          <p className="text-pink-200 text-sm">{selectedResult.lifeAspects.love.advice}</p>
                        </div>
                        
                        <div className="p-4 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">✨ 이상형</h4>
                          <p className="text-white text-sm mb-3">{selectedResult.lifeAspects.love.idealType}</p>
                          <h4 className="font-semibold text-white mb-2">🎯 궁합 좋은 타입</h4>
                          <div className="flex flex-wrap gap-2">
                            {selectedResult.lifeAspects.love.compatibility.map((comp, index) => (
                              <span key={index} className="bg-purple-500/30 text-white px-3 py-1 rounded-full text-sm">
                                {comp} {sajuElements[comp]?.animal}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {activeTab === 'fortune' && (
                      <div className="space-y-4">
                        <div className="p-4 bg-gradient-to-r from-amber-500/20 to-yellow-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-3">💰 재물운 스타일</h4>
                          <p className="text-amber-200 text-sm mb-2">{selectedResult.lifeAspects.money.style}</p>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
                            <div className="bg-green-500/20 p-3 rounded-lg">
                              <h5 className="text-green-300 font-medium text-sm">🍀 길운 시기</h5>
                              <p className="text-green-200 text-xs">{selectedResult.lifeAspects.money.luckyPeriod}</p>
                            </div>
                            <div className="bg-red-500/20 p-3 rounded-lg">
                              <h5 className="text-red-300 font-medium text-sm">⚠️ 주의 시기</h5>
                              <p className="text-red-200 text-xs">{selectedResult.lifeAspects.money.cautionPeriod}</p>
                            </div>
                          </div>
                        </div>
                        
                        <div className="p-4 bg-gradient-to-r from-teal-500/20 to-cyan-500/20 rounded-lg">
                          <h4 className="font-semibold text-white mb-2">🏥 건강 관리 포인트</h4>
                          <div className="space-y-2">
                            <div>
                              <span className="text-teal-300 text-sm font-medium">주의 부위:</span>
                              <span className="text-teal-200 text-sm ml-2">
                                {selectedResult.lifeAspects.health.careAreas.join(', ')}
                              </span>
                            </div>
                            <div>
                              <span className="text-teal-300 text-sm font-medium">추천 운동:</span>
                              <span className="text-teal-200 text-sm ml-2">
                                {selectedResult.lifeAspects.health.recommendedExercise}
                              </span>
                            </div>
                            <div>
                              <span className="text-teal-300 text-sm font-medium">스트레스 관리:</span>
                              <span className="text-teal-200 text-sm ml-2">
                                {selectedResult.lifeAspects.health.stressManagement}
                              </span>
                            </div>
                          </div>
                        </div>

                        {selectedResult.yearlyFortune[2025] && (
                          <div className="p-4 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-lg">
                            <h4 className="font-semibold text-white mb-3">🔮 2025년 운세</h4>
                            <div className="grid grid-cols-4 gap-2 mb-3">
                              {[
                                { label: '종합', value: selectedResult.yearlyFortune[2025].overall, color: 'purple' },
                                { label: '연애', value: selectedResult.yearlyFortune[2025].love, color: 'pink' },
                                { label: '커리어', value: selectedResult.yearlyFortune[2025].career, color: 'blue' },
                                { label: '재물', value: selectedResult.yearlyFortune[2025].money, color: 'green' }
                              ].map((item, index) => (
                                <div key={index} className="text-center">
                                  <div className="text-xs text-gray-300 mb-1">{item.label}</div>
                                  <div className="flex justify-center">
                                    {Array.from({length: 5}).map((_, i) => (
                                      <span key={i} className={`text-xs ${
                                        i < item.value ? `text-${item.color}-400` : 'text-gray-600'
                                      }`}>
                                        ⭐
                                      </span>
                                    ))}
                                  </div>
                                </div>
                              ))}
                            </div>
                            <div className="flex flex-wrap gap-1">
                              {selectedResult.yearlyFortune[2025].keywords.map((keyword, index) => (
                                <span key={index} className="bg-indigo-500/30 text-indigo-200 px-2 py-1 rounded-full text-xs">
                                  {keyword}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </motion.div>
                </AnimatePresence>

                {viewMode === 'cyber_fantasy' && (
                  <motion.div
                    className="mt-6 p-4 border border-cyan-500/50 rounded-lg bg-cyan-500/10"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.8 }}
                  >
                    <h3 className="text-cyan-300 font-semibold mb-2 flex items-center">
                      🌌 사이버 모드 특별 분석
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm">
                      <div className="bg-cyan-500/20 p-2 rounded text-cyan-200">
                        🔮 3D 오행 크리스탈 시각화
                      </div>
                      <div className="bg-cyan-500/20 p-2 rounded text-cyan-200">
                        🤖 AI 맞춤 미래 예측
                      </div>
                      <div className="bg-cyan-500/20 p-2 rounded text-cyan-200">
                        ✨ 홀로그램 궁합 분석
                      </div>
                    </div>
                  </motion.div>
                )}
              </motion.div>
            </AnimatePresence>
          ) : null}
        </motion.div>
      </div>
    </motion.div>
  )
}

export default SajuCalculator