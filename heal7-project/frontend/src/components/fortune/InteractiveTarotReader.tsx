import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  majorArcanaCards, 
  tarotSpreads, 
  mzQuestionTemplates,
  interpretationTemplates,
  TarotCard,
  TarotSpread 
} from '../../data/tarotData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface InteractiveTarotReaderProps {
  viewMode: ViewMode
}

interface DrawnCard {
  card: TarotCard
  isReversed: boolean
  position: number
}

const InteractiveTarotReader: React.FC<InteractiveTarotReaderProps> = ({ viewMode }) => {
  const [currentStep, setCurrentStep] = useState<'select' | 'question' | 'drawing' | 'result'>('select')
  const [selectedSpread, setSelectedSpread] = useState<TarotSpread | null>(null)
  const [selectedQuestion, setSelectedQuestion] = useState<string>('')
  const [customQuestion, setCustomQuestion] = useState<string>('')
  const [drawnCards, setDrawnCards] = useState<DrawnCard[]>([])
  const [isDrawing, setIsDrawing] = useState(false)
  const [showCards, setShowCards] = useState(false)

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
  const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white'
  const accentClass = viewMode === 'cyber_fantasy' ? 'text-pink-300' : 'text-white'

  // 카드 뽑기 함수
  const drawCards = async () => {
    if (!selectedSpread) return

    setIsDrawing(true)
    setCurrentStep('drawing')
    
    const cards: DrawnCard[] = []
    
    for (let i = 0; i < selectedSpread.positions.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1000)) // 1초씩 지연
      
      const randomCard = majorArcanaCards[Math.floor(Math.random() * majorArcanaCards.length)]
      const isReversed = Math.random() > 0.7 // 30% 확률로 역방향
      
      cards.push({
        card: randomCard,
        isReversed,
        position: i
      })
      
      setDrawnCards([...cards])
    }
    
    setIsDrawing(false)
    setShowCards(true)
    setCurrentStep('result')
  }

  // 질문 선택 핸들러
  const handleQuestionSelect = (question: string) => {
    setSelectedQuestion(question)
    setCustomQuestion('')
  }

  // 다시하기
  const resetReading = () => {
    setCurrentStep('select')
    setSelectedSpread(null)
    setSelectedQuestion('')
    setCustomQuestion('')
    setDrawnCards([])
    setShowCards(false)
    setIsDrawing(false)
  }

  // 결과 해석
  const getInterpretation = (card: TarotCard, isReversed: boolean) => {
    const interpretation = isReversed ? card.reversed : card.upright
    const randomTemplate = interpretationTemplates.positive[
      Math.floor(Math.random() * interpretationTemplates.positive.length)
    ]
    return { interpretation, template: randomTemplate }
  }

  return (
    <motion.div
      className="max-w-6xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* 헤더 */}
      <motion.div 
        className="text-center mb-8"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className={`text-3xl md:text-4xl font-bold mb-4 ${textClass}`}>
          🃏 {viewMode === 'cyber_fantasy' ? '사이버 타로 리딩' : '타로카드 운세'}
        </h1>
        <p className="text-gray-300">
          {viewMode === 'cyber_fantasy' 
            ? '홀로그래픽 타로로 미래를 엿보세요'
            : '카드가 전하는 우주의 메시지를 받아보세요'
          }
        </p>
      </motion.div>

      {/* Step 1: 스프레드 선택 */}
      {currentStep === 'select' && (
        <AnimatePresence>
          <motion.section
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
          >
            <h2 className={`text-2xl font-bold mb-6 text-center ${textClass}`}>
              어떤 방식으로 운세를 보시겠어요?
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {tarotSpreads.map((spread, index) => (
                <motion.div
                  key={spread.id}
                  className={`${cardClass} p-6 cursor-pointer group`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, rotateY: 5 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setSelectedSpread(spread)
                    setCurrentStep('question')
                  }}
                >
                  <div className="text-center">
                    <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">
                      {spread.emoji}
                    </div>
                    <h3 className={`text-xl font-bold mb-2 ${textClass}`}>
                      {spread.name}
                    </h3>
                    <p className="text-gray-300 text-sm mb-4">
                      {spread.description}
                    </p>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs text-gray-400">
                        <span>카테고리: {spread.category}</span>
                        <span>소요시간: {spread.duration}</span>
                      </div>
                      <div className="flex justify-between text-xs text-gray-400">
                        <span>난이도: {spread.difficulty}</span>
                        <span>카드 {spread.positions.length}장</span>
                      </div>
                    </div>

                    <div className="mt-4 flex justify-center">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        spread.category === 'love' ? 'bg-pink-500/20 text-pink-300' :
                        spread.category === 'career' ? 'bg-blue-500/20 text-blue-300' :
                        spread.category === 'daily' ? 'bg-green-500/20 text-green-300' :
                        'bg-purple-500/20 text-white'
                      }`}>
                        {spread.category.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.section>
        </AnimatePresence>
      )}

      {/* Step 2: 질문 입력 */}
      {currentStep === 'question' && selectedSpread && (
        <AnimatePresence>
          <motion.section
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            className={`${cardClass} p-8`}
          >
            <button
              onClick={() => setCurrentStep('select')}
              className="mb-6 flex items-center text-gray-400 hover:text-white transition-colors"
            >
              ← 다른 스프레드 선택하기
            </button>

            <div className="text-center mb-8">
              <div className="text-6xl mb-4">{selectedSpread.emoji}</div>
              <h2 className={`text-2xl font-bold mb-2 ${textClass}`}>
                {selectedSpread.name}
              </h2>
              <p className="text-gray-300">
                {selectedSpread.description}
              </p>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className={`text-lg font-semibold mb-4 ${textClass}`}>
                  💭 무엇이 궁금하신가요?
                </h3>
                
                {/* 미리 준비된 질문들 */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
                  {mzQuestionTemplates.slice(0, 6).map((question, index) => (
                    <motion.button
                      key={index}
                      className={`p-4 text-left rounded-lg transition-all ${
                        selectedQuestion === question
                          ? 'bg-purple-500/30 border border-purple-400'
                          : 'bg-black/20 border border-white/20 hover:bg-black/30'
                      }`}
                      onClick={() => handleQuestionSelect(question)}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <span className="text-white">{question}</span>
                    </motion.button>
                  ))}
                </div>

                {/* 직접 질문 입력 */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>
                    또는 직접 질문해보세요
                  </label>
                  <textarea
                    className="w-full p-4 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 resize-none"
                    rows={3}
                    placeholder="예: 이번 달 연애운은 어떨까요?"
                    value={customQuestion}
                    onChange={(e) => {
                      setCustomQuestion(e.target.value)
                      setSelectedQuestion('')
                    }}
                  />
                </div>
              </div>

              <motion.button
                className={`w-full py-4 rounded-lg font-bold text-lg ${
                  viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
                disabled={!selectedQuestion && !customQuestion.trim() || isDrawing}
                onClick={drawCards}
                whileHover={{ scale: selectedQuestion || customQuestion.trim() ? 1.02 : 1 }}
                whileTap={{ scale: selectedQuestion || customQuestion.trim() ? 0.98 : 1 }}
              >
                {isDrawing 
                  ? '🌀 카드 뽑는 중...' 
                  : viewMode === 'cyber_fantasy' 
                    ? '🌌 사이버 카드 소환' 
                    : '🃏 카드 뽑기 시작'
                }
              </motion.button>
            </div>
          </motion.section>
        </AnimatePresence>
      )}

      {/* Step 3: 카드 뽑는 중 */}
      {currentStep === 'drawing' && (
        <AnimatePresence>
          <motion.section
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className={`${cardClass} p-12 text-center`}
          >
            <motion.div
              animate={{ 
                rotate: [0, 360],
                scale: [1, 1.1, 1]
              }}
              transition={{ 
                rotate: { duration: 2, repeat: Infinity, ease: "linear" },
                scale: { duration: 2, repeat: Infinity }
              }}
              className="text-8xl mb-8"
            >
              🔮
            </motion.div>
            
            <h2 className={`text-2xl font-bold mb-4 ${textClass}`}>
              카드가 당신을 선택하고 있어요...
            </h2>
            <p className="text-gray-300 mb-8">
              우주의 메시지가 전달되는 중입니다
            </p>

            {/* 뽑힌 카드들 미리보기 */}
            {drawnCards.length > 0 && (
              <div className="flex justify-center space-x-4">
                {drawnCards.map((drawnCard, index) => (
                  <motion.div
                    key={index}
                    className="w-16 h-24 bg-gradient-to-b from-purple-600 to-pink-600 rounded-lg shadow-lg flex items-center justify-center"
                    initial={{ opacity: 0, y: 50, rotateY: 180 }}
                    animate={{ opacity: 1, y: 0, rotateY: 0 }}
                    transition={{ delay: index * 0.5, duration: 0.8 }}
                  >
                    <span className="text-2xl">{drawnCard.card.emoji}</span>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.section>
        </AnimatePresence>
      )}

      {/* Step 4: 결과 */}
      {currentStep === 'result' && showCards && (
        <AnimatePresence>
          <motion.section
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* 질문 표시 */}
            <div className={`${cardClass} p-6 text-center`}>
              <h2 className={`text-xl font-bold mb-2 ${textClass}`}>
                📝 당신의 질문
              </h2>
              <p className={`${accentClass} text-lg`}>
                "{selectedQuestion || customQuestion}"
              </p>
            </div>

            {/* 카드 배치 시각화 */}
            {selectedSpread && (
              <div className={`${cardClass} p-8`}>
                <h3 className={`text-xl font-bold mb-6 text-center ${textClass}`}>
                  🃏 {selectedSpread.name} 결과
                </h3>
                
                <div className="relative w-full h-96 mb-8">
                  {selectedSpread.positions.map((position, index) => (
                    <motion.div
                      key={index}
                      className="absolute transform -translate-x-1/2 -translate-y-1/2"
                      style={{
                        left: `${position.x}%`,
                        top: `${position.y}%`
                      }}
                      initial={{ opacity: 0, scale: 0, rotate: 180 }}
                      animate={{ opacity: 1, scale: 1, rotate: drawnCards[index]?.isReversed ? 180 : 0 }}
                      transition={{ delay: index * 0.3, duration: 0.8 }}
                    >
                      {drawnCards[index] && (
                        <div className="text-center">
                          <div className="w-20 h-32 bg-gradient-to-b from-indigo-600 to-purple-600 rounded-lg shadow-xl flex items-center justify-center mb-2 relative overflow-hidden">
                            <div className="absolute inset-0 bg-black/20" />
                            <span className="text-3xl relative z-10">
                              {drawnCards[index].card.emoji}
                            </span>
                          </div>
                          <p className="text-xs text-gray-400 max-w-20">
                            {position.name}
                          </p>
                          {drawnCards[index].isReversed && (
                            <span className="text-xs text-yellow-400">역방향</span>
                          )}
                        </div>
                      )}
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* 상세 해석 */}
            <div className="space-y-6">
              {drawnCards.map((drawnCard, index) => {
                const { interpretation, template } = getInterpretation(drawnCard.card, drawnCard.isReversed)
                
                return (
                  <motion.div
                    key={index}
                    className={`${cardClass} p-6`}
                    initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 1.5 + index * 0.3 }}
                  >
                    <div className="flex items-start space-x-6">
                      {/* 카드 이미지 */}
                      <div className="flex-shrink-0">
                        <div className="w-24 h-36 bg-gradient-to-b from-indigo-600 to-purple-600 rounded-lg shadow-xl flex items-center justify-center relative overflow-hidden">
                          <div className="absolute inset-0 bg-black/20" />
                          <span className="text-4xl relative z-10" style={{
                            transform: drawnCard.isReversed ? 'rotate(180deg)' : 'none'
                          }}>
                            {drawnCard.card.emoji}
                          </span>
                        </div>
                        {drawnCard.isReversed && (
                          <p className="text-center text-xs text-yellow-400 mt-2">역방향</p>
                        )}
                      </div>

                      {/* 해석 내용 */}
                      <div className="flex-1">
                        <h3 className={`text-xl font-bold mb-2 ${textClass}`}>
                          {selectedSpread?.positions[index]?.name}: {drawnCard.card.nameKr}
                        </h3>
                        
                        <div className="space-y-4">
                          <div className={`p-4 rounded-lg ${
                            drawnCard.isReversed 
                              ? 'bg-orange-500/20 border border-orange-400/50' 
                              : 'bg-green-500/20 border border-green-400/50'
                          }`}>
                            <p className="font-semibold text-white mb-2">{template}</p>
                            <p className="text-gray-200">{interpretation.meaning}</p>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div className="bg-pink-500/20 p-3 rounded-lg">
                              <h4 className="font-semibold text-pink-300 mb-1">💕 연애</h4>
                              <p className="text-gray-300">{interpretation.love}</p>
                            </div>
                            <div className="bg-blue-500/20 p-3 rounded-lg">
                              <h4 className="font-semibold text-blue-300 mb-1">🚀 진로</h4>
                              <p className="text-gray-300">{interpretation.career}</p>
                            </div>
                            <div className="bg-green-500/20 p-3 rounded-lg">
                              <h4 className="font-semibold text-green-300 mb-1">💰 재물</h4>
                              <p className="text-gray-300">{interpretation.money}</p>
                            </div>
                          </div>

                          <div className="bg-purple-500/20 p-3 rounded-lg">
                            <h4 className="font-semibold text-white mb-1">💡 조언</h4>
                            <p className="text-gray-300">{interpretation.advice}</p>
                          </div>

                          {/* MZ 해석 */}
                          <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 p-3 rounded-lg">
                            <h4 className="font-semibold text-yellow-300 mb-1">💬 한마디로</h4>
                            <p className="text-gray-200 font-medium">{drawnCard.card.mzInterpretation}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </div>

            {/* 액션 버튼들 */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                className="px-8 py-4 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-lg font-medium"
                onClick={() => {
                  const resultText = `${selectedQuestion || customQuestion}\n\n${drawnCards.map(dc => `${dc.card.nameKr}: ${dc.card.mzInterpretation}`).join('\n\n')}\n\n#타로 #운세 #HEAL7`
                  navigator.share && navigator.share({
                    title: 'HEAL7 타로 운세',
                    text: resultText,
                    url: window.location.href
                  })
                }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                📱 결과 공유하기
              </motion.button>
              
              <motion.button
                className="px-8 py-4 bg-gray-600 hover:bg-gray-500 text-white rounded-lg font-medium"
                onClick={resetReading}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🔄 다시 운세보기
              </motion.button>
            </div>
          </motion.section>
        </AnimatePresence>
      )}
    </motion.div>
  )
}

export default InteractiveTarotReader