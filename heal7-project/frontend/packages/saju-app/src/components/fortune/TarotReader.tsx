import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'

type ViewMode = 'basic' | 'cyber_fantasy'

interface TarotReaderProps {
  viewMode: ViewMode
}

interface TarotCard {
  id: number
  name: string
  meaning: string
  reversed: boolean
  image: string
}

const TarotReader: React.FC<TarotReaderProps> = ({ viewMode }) => {
  const [selectedSpread, setSelectedSpread] = useState<'single' | 'three' | 'celtic'>('single')
  const [isReading, setIsReading] = useState(false)
  const [drawnCards, setDrawnCards] = useState<TarotCard[]>([])
  const [showResult, setShowResult] = useState(false)

  // 타로 리딩 API 호출
  const { data: tarotData, refetch } = useQuery({
    queryKey: ['tarot-reading', selectedSpread],
    queryFn: async () => {
      const response = await fetch('/api/fortune/tarot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ spread: selectedSpread, mode: viewMode })
      })
      return response.json()
    },
    enabled: false
  })

  // 카드 뽑기 애니메이션
  const drawCards = async () => {
    setIsReading(true)
    setShowResult(false)
    
    // 애니메이션 딜레이 후 API 호출
    setTimeout(() => {
      refetch().then(() => {
        // 임시 카드 데이터 (실제론 API에서 받아옴)
        const cardCount = selectedSpread === 'single' ? 1 : selectedSpread === 'three' ? 3 : 10
        const mockCards: TarotCard[] = Array.from({length: cardCount}, (_, i) => ({
          id: i,
          name: `카드 ${i + 1}`,
          meaning: `의미 ${i + 1}`,
          reversed: Math.random() > 0.5,
          image: `🃏`
        }))
        
        setDrawnCards(mockCards)
        setShowResult(true)
        setIsReading(false)
      })
    }, 2000)
  }

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-featured' : 'card-base'

  // 스프레드 옵션
  const spreadOptions = [
    { id: 'single', name: '원 카드', description: '오늘의 메시지', cards: 1 },
    { id: 'three', name: '쓰리 카드', description: '과거/현재/미래', cards: 3 },
    { id: 'celtic', name: '켈틱 크로스', description: '종합 운세', cards: 10 }
  ]

  return (
    <motion.div
      className="max-w-6xl mx-auto"
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
          'text-white'
        }`}>
          🃏 {viewMode === 'cyber_fantasy' ? '홀로그래픽 타로' : '타로카드 리딩'}
        </h1>
        <p className="text-gray-300">
          {viewMode === 'cyber_fantasy' 
            ? '디지털 우주에서 펼쳐지는 신비로운 카드의 메시지'
            : '마음을 열고 카드가 전하는 메시지를 들어보세요'
          }
        </p>
      </motion.div>

      {/* 스프레드 선택 */}
      <motion.div 
        className={`p-6 rounded-xl ${cardClass} mb-8`}
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <h2 className="text-xl font-bold text-white mb-4 flex items-center">
          <span className="mr-2">🔮</span>
          스프레드 선택
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {spreadOptions.map((option) => (
            <motion.button
              key={option.id}
              className={`p-4 rounded-lg border-2 transition-all ${
                selectedSpread === option.id
                  ? 'border-purple-500 bg-purple-500/20'
                  : 'border-gray-600 hover:border-gray-500'
              }`}
              onClick={() => setSelectedSpread(option.id as any)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="text-white">
                <h3 className="font-semibold text-lg">{option.name}</h3>
                <p className="text-sm text-gray-400 mt-1">{option.description}</p>
                <p className="text-xs text-white mt-2">{option.cards}장의 카드</p>
              </div>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* 카드 뽑기 버튼 */}
      <motion.div 
        className="text-center mb-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        <motion.button
          className={`px-8 py-4 text-lg font-bold rounded-xl ${
            viewMode === 'cyber_fantasy' ? 'btn-primary' : 'btn-secondary'
          }`}
          onClick={drawCards}
          disabled={isReading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isReading ? (
            <div className="flex items-center">
              <motion.div
                className="w-6 h-6 border-2 border-white border-t-transparent rounded-full mr-3"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              />
              카드를 뽑는 중...
            </div>
          ) : viewMode === 'cyber_fantasy' ? (
            '🌌 홀로그램 카드 소환'
          ) : (
            '🃏 카드 뽑기'
          )}
        </motion.button>
      </motion.div>

      {/* 카드 표시 영역 */}
      <AnimatePresence mode="wait">
        {isReading && (
          <motion.div
            className="text-center py-16"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="text-8xl mb-8"
              animate={{ 
                rotateY: [0, 180, 360],
                scale: [1, 1.2, 1]
              }}
              transition={{ 
                duration: 2, 
                repeat: Infinity, 
                ease: "easeInOut" 
              }}
            >
              🃏
            </motion.div>
            
            <motion.p 
              className="text-xl text-gray-300"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              {viewMode === 'cyber_fantasy' 
                ? '디지털 우주에서 카드를 소환하고 있습니다...'
                : '운명의 카드를 선별하고 있습니다...'
              }
            </motion.p>
          </motion.div>
        )}

        {showResult && drawnCards.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            {/* 카드 배치 */}
            <div className={`mb-8 ${
              selectedSpread === 'single' ? 'flex justify-center' :
              selectedSpread === 'three' ? 'flex justify-center space-x-8' :
              'grid grid-cols-2 md:grid-cols-5 gap-4 max-w-4xl mx-auto'
            }`}>
              {drawnCards.map((card, index) => (
                <motion.div
                  key={card.id}
                  className={`${cardClass} p-6 text-center ${
                    selectedSpread === 'single' ? 'w-64' : 
                    selectedSpread === 'three' ? 'w-48' : 'w-32'
                  }`}
                  initial={{ opacity: 0, rotateY: 180, scale: 0.5 }}
                  animate={{ opacity: 1, rotateY: 0, scale: 1 }}
                  transition={{ delay: index * 0.3, duration: 0.8 }}
                  whileHover={{ scale: 1.05, rotateY: 5 }}
                >
                  <motion.div
                    className={`text-6xl mb-4 ${card.reversed ? 'rotate-180' : ''}`}
                    animate={viewMode === 'cyber_fantasy' ? {
                      textShadow: [
                        '0 0 10px #00F5FF',
                        '0 0 20px #FF00FF',
                        '0 0 10px #00F5FF'
                      ]
                    } : {}}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    🃏
                  </motion.div>
                  
                  <h3 className="text-white font-bold text-lg mb-2">
                    {card.name}
                    {card.reversed && <span className="text-red-400 ml-2">(역방향)</span>}
                  </h3>
                  
                  {selectedSpread !== 'celtic' && (
                    <p className="text-gray-300 text-sm">
                      {card.meaning}
                    </p>
                  )}
                </motion.div>
              ))}
            </div>

            {/* 해석 결과 */}
            <motion.div
              className={`${cardClass} p-6`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1 }}
            >
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="mr-2">✨</span>
                {viewMode === 'cyber_fantasy' ? '디지털 오라클의 메시지' : '타로 해석'}
              </h2>

              {tarotData ? (
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg">
                    <p className="text-white">{tarotData.message}</p>
                  </div>

                  {tarotData.features && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {tarotData.features.map((feature: string, index: number) => (
                        <motion.div
                          key={index}
                          className="p-4 bg-black/30 rounded-lg"
                          initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 1.2 + index * 0.2 }}
                        >
                          <p className="text-gray-300">• {feature}</p>
                        </motion.div>
                      ))}
                    </div>
                  )}

                  {viewMode === 'cyber_fantasy' && (
                    <motion.div
                      className="mt-6 p-4 border border-cyan-500/50 rounded-lg bg-cyan-500/10"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 1.5 }}
                    >
                      <h3 className="text-cyan-300 font-semibold mb-2">🌌 사이버 모드 특별 해석</h3>
                      <p className="text-cyan-200 text-sm">
                        홀로그래픽 패턴 분석을 통해 더욱 정교한 해석이 적용되었습니다.
                      </p>
                    </motion.div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="animate-pulse">
                    <div className="h-4 bg-gray-600 rounded mb-4"></div>
                    <div className="h-4 bg-gray-600 rounded mb-4"></div>
                    <div className="h-4 bg-gray-600 rounded w-2/3 mx-auto"></div>
                  </div>
                  <p className="text-gray-400 mt-4">해석을 불러오는 중...</p>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 다시 뽑기 버튼 */}
      {showResult && !isReading && (
        <motion.div 
          className="text-center mt-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2 }}
        >
          <motion.button
            className="btn-secondary"
            onClick={() => {
              setShowResult(false)
              setDrawnCards([])
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            🔄 다시 뽑기
          </motion.button>
        </motion.div>
      )}
    </motion.div>
  )
}

export default TarotReader