import React from 'react'
import { motion } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'

type ViewMode = 'basic' | 'cyber_fantasy'

interface DashboardProps {
  viewMode: ViewMode
}

interface FortuneData {
  message: string
  mode: string
  features: string[]
}

const Dashboard: React.FC<DashboardProps> = ({ viewMode }) => {
  // 기본 사주 데이터 조회
  const { data: sajuData, isLoading: sajuLoading } = useQuery<FortuneData>({
    queryKey: ['saju-basic'],
    queryFn: async () => {
      const response = await fetch('/api/fortune/saju/basic')
      return response.json()
    }
  })

  // 타로 데이터 조회
  const { data: tarotData, isLoading: tarotLoading } = useQuery<FortuneData>({
    queryKey: ['tarot'],
    queryFn: async () => {
      const response = await fetch('/api/fortune/tarot')
      return response.json()
    }
  })

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.2
      }
    }
  }

  const cardVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 300
      }
    }
  }

  return (
    <motion.div
      className="max-w-7xl mx-auto"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* 메인 히어로 섹션 */}
      <motion.section variants={cardVariants} className="text-center mb-12">
        <motion.h1 
          className={`text-4xl md:text-6xl font-bold mb-6 ${
            viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic'
          }`}
          initial={{ scale: 0.5 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, delay: 0.5 }}
        >
          🔮 운명의 문이 열립니다
        </motion.h1>
        
        <motion.p 
          className={`text-xl mb-8 ${
            viewMode === 'cyber_fantasy' ? 'text-gray-200' : 'text-gray-300'
          }`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          {viewMode === 'cyber_fantasy' 
            ? '디지털 우주에서 펼쳐지는 신비로운 운명 탐험' 
            : '포스텔러를 넘어선 차세대 운세 플랫폼'
          }
        </motion.p>

        {/* 모드별 특화 메시지 */}
        {viewMode === 'cyber_fantasy' && (
          <motion.div 
            className="inline-flex items-center px-6 py-3 card-crystal text-cyan-300 rounded-full mb-8"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.9 }}
          >
            <span className="mr-2">✨</span>
            사이버 판타지 모드 활성화
          </motion.div>
        )}
      </motion.section>

      {/* 서비스 카드 그리드 */}
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12"
        variants={containerVariants}
      >
        {/* 사주명리 카드 */}
        <motion.div 
          className={`p-6 rounded-xl ${
            viewMode === 'cyber_fantasy' ? 'card-crystal' : 'card-cosmic'
          }`}
          variants={cardVariants}
          whileHover={{ scale: 1.05, rotateY: 5 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="text-center">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold text-white mb-3">사주명리학</h3>
            
            {sajuLoading ? (
              <div className="animate-pulse">
                <div className="h-4 bg-gray-600 rounded mb-2"></div>
                <div className="h-4 bg-gray-600 rounded mb-2"></div>
              </div>
            ) : (
              <div>
                <p className="text-gray-300 mb-4">{sajuData?.message}</p>
                <div className="space-y-2">
                  {sajuData?.features.map((feature, index) => (
                    <motion.div
                      key={index}
                      className="text-sm text-purple-300 bg-purple-500/20 rounded px-3 py-1"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 1 + index * 0.1 }}
                    >
                      {feature}
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            <motion.button
              className="mt-4 btn-cosmic w-full"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              사주 보기
            </motion.button>
          </div>
        </motion.div>

        {/* 타로카드 카드 */}
        <motion.div 
          className={`p-6 rounded-xl ${
            viewMode === 'cyber_fantasy' ? 'card-crystal' : 'card-cosmic'
          }`}
          variants={cardVariants}
          whileHover={{ scale: 1.05, rotateY: -5 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="text-center">
            <div className="text-4xl mb-4">🃏</div>
            <h3 className="text-xl font-bold text-white mb-3">타로카드</h3>
            
            {tarotLoading ? (
              <div className="animate-pulse">
                <div className="h-4 bg-gray-600 rounded mb-2"></div>
                <div className="h-4 bg-gray-600 rounded mb-2"></div>
              </div>
            ) : (
              <div>
                <p className="text-gray-300 mb-4">{tarotData?.message}</p>
                <div className="space-y-2">
                  {tarotData?.features.map((feature, index) => (
                    <motion.div
                      key={index}
                      className="text-sm text-pink-300 bg-pink-500/20 rounded px-3 py-1"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 1.2 + index * 0.1 }}
                    >
                      {feature}
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            <motion.button
              className="mt-4 btn-mystic w-full"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              카드 뽑기
            </motion.button>
          </div>
        </motion.div>

        {/* 사용자 프로필 카드 */}
        <motion.div 
          className={`p-6 rounded-xl ${
            viewMode === 'cyber_fantasy' ? 'card-crystal' : 'card-cosmic'
          }`}
          variants={cardVariants}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="text-center">
            <div className="text-4xl mb-4">🎮</div>
            <h3 className="text-xl font-bold text-white mb-3">나의 프로필</h3>
            
            <div className="space-y-3">
              {/* 레벨 */}
              <div className="flex justify-between items-center">
                <span className="text-gray-300">레벨</span>
                <span className="level-badge">Lv. 1</span>
              </div>
              
              {/* 경험치 바 */}
              <div>
                <div className="flex justify-between text-sm text-gray-400 mb-1">
                  <span>EXP</span>
                  <span>150 / 1000</span>
                </div>
                <div className="progress-bar">
                  <motion.div 
                    className="progress-fill"
                    initial={{ width: 0 }}
                    animate={{ width: '15%' }}
                    transition={{ delay: 1.5, duration: 0.8 }}
                  />
                </div>
              </div>

              {/* 업적 */}
              <div className="text-sm text-gray-300">
                🏆 업적: 3/50 달성
              </div>
            </div>

            <motion.button
              className="mt-4 btn-outline w-full"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              상세 보기
            </motion.button>
          </div>
        </motion.div>
      </motion.div>

      {/* 최근 활동 섹션 */}
      <motion.section variants={cardVariants} className="mb-12">
        <h2 className={`text-2xl font-bold mb-6 text-center ${
          viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic'
        }`}>
          ✨ 오늘의 운세 하이라이트
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <motion.div 
            className={`p-6 rounded-xl ${
              viewMode === 'cyber_fantasy' ? 'card-crystal' : 'card-glass'
            }`}
            whileHover={{ scale: 1.02 }}
          >
            <h3 className="text-lg font-semibold text-white mb-3">💫 오늘의 키워드</h3>
            <div className="flex flex-wrap gap-2">
              {['성장', '기회', '행운', '변화'].map((keyword, index) => (
                <motion.span
                  key={keyword}
                  className="px-3 py-1 bg-gradient-to-r from-purple-500/30 to-pink-500/30 text-white text-sm rounded-full"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1.8 + index * 0.1 }}
                >
                  {keyword}
                </motion.span>
              ))}
            </div>
          </motion.div>

          <motion.div 
            className={`p-6 rounded-xl ${
              viewMode === 'cyber_fantasy' ? 'card-crystal' : 'card-glass'
            }`}
            whileHover={{ scale: 1.02 }}
          >
            <h3 className="text-lg font-semibold text-white mb-3">🎯 추천 서비스</h3>
            <p className="text-gray-300 text-sm mb-3">
              당신에게 맞춤형 운세 분석을 추천합니다
            </p>
            <motion.button
              className="btn-cosmic"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              맞춤 분석 시작
            </motion.button>
          </motion.div>
        </div>
      </motion.section>
    </motion.div>
  )
}

export default Dashboard