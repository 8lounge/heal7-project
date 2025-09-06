import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { consultants, reviews, consultationPackages, consultationCategories } from '../../data/consultationData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface ConsultationProps {
  viewMode: ViewMode
}

const Consultation: React.FC<ConsultationProps> = ({ viewMode }) => {
  const [selectedConsultant, setSelectedConsultant] = useState<string | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [activeTab, setActiveTab] = useState<'consultants' | 'packages' | 'reviews'>('consultants')

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
  const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white'
  const accentClass = viewMode === 'cyber_fantasy' ? 'text-pink-300' : 'text-white'

  const filteredConsultants = selectedCategory === 'all' 
    ? consultants 
    : consultants.filter(consultant => 
        consultant.specialties.some(specialty => 
          specialty.includes(consultationCategories.find(cat => cat.id === selectedCategory)?.name.split('/')[0] || '')
        )
      )

  if (selectedConsultant) {
    const consultant = consultants.find(c => c.id === selectedConsultant)
    if (!consultant) return null

    const consultantReviews = reviews.filter(r => r.consultantId === selectedConsultant)

    return (
      <motion.div
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* 뒤로가기 */}
        <motion.button
          onClick={() => setSelectedConsultant(null)}
          className={`mb-6 px-4 py-2 rounded-lg ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 전문가 목록
        </motion.button>

        <motion.div
          className={`${cardClass} p-8`}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {/* 전문가 프로필 */}
          <div className="flex flex-col md:flex-row items-start gap-8 mb-8">
            <div className="text-center">
              <div className="text-8xl mb-4">{consultant.avatar}</div>
              <div className={`flex items-center justify-center gap-2 ${consultant.isOnline ? 'text-green-400' : 'text-gray-400'}`}>
                <div className={`w-3 h-3 rounded-full ${consultant.isOnline ? 'bg-green-400' : 'bg-gray-400'}`} />
                {consultant.isOnline ? '온라인' : '오프라인'}
              </div>
            </div>
            
            <div className="flex-1">
              <h1 className={`text-3xl font-bold ${textClass} mb-2`}>
                {consultant.name} <span className={`text-lg ${accentClass}`}>({consultant.nickname})</span>
              </h1>
              
              <div className="flex items-center gap-4 mb-4">
                <span className="text-yellow-400">⭐ {consultant.rating}</span>
                <span className={`${textClass} opacity-75`}>
                  후기 {consultant.reviewCount.toLocaleString()}개
                </span>
                <span className={`${textClass} opacity-75`}>
                  상담 {consultant.consultationCount.toLocaleString()}회
                </span>
              </div>

              <p className={`${textClass} mb-4`}>{consultant.introduction}</p>

              <div className="mb-4">
                <h3 className={`font-bold ${textClass} mb-2`}>전문 분야</h3>
                <div className="flex flex-wrap gap-2">
                  {consultant.specialties.map((specialty, index) => (
                    <span key={index} className="px-3 py-1 rounded-full bg-purple-500/30 text-white text-sm">
                      {specialty}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <h3 className={`font-bold ${textClass} mb-2`}>자격증/경력</h3>
                <ul className={`${textClass} opacity-75`}>
                  {consultant.credentials.map((cred, index) => (
                    <li key={index}>• {cred}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* 상담 정보 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-white/10 p-4 rounded-lg backdrop-blur-md border border-white/20">
              <h3 className={`font-bold ${textClass} mb-3`}>💰 상담 요금</h3>
              <div className={`text-2xl font-bold ${accentClass} mb-2`}>
                {consultant.pricePerMinute.toLocaleString()}원/분
              </div>
              <p className={`${textClass} opacity-75 text-sm`}>
                평균 응답시간: {consultant.responseTime}
              </p>
            </div>
            
            <div className="bg-white/10 p-4 rounded-lg backdrop-blur-md border border-white/20">
              <h3 className={`font-bold ${textClass} mb-3`}>📞 상담 방식</h3>
              <div className="flex flex-wrap gap-2">
                {consultant.consultationMethods.map((method, index) => (
                  <span key={index} className="px-3 py-1 rounded-full bg-green-500/30 text-green-200 text-sm">
                    {method === 'chat' ? '💬 채팅' : method === 'voice' ? '📞 음성' : '📹 영상'}
                  </span>
                ))}
              </div>
              <div className="mt-2">
                <span className={`${textClass} opacity-75 text-sm`}>
                  언어: {consultant.languages.join(', ')}
                </span>
              </div>
            </div>
          </div>

          {/* 상담 예약 버튼 */}
          <div className="text-center mb-8">
            <motion.button
              className={`px-8 py-4 rounded-lg text-lg font-bold ${
                viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={!consultant.isOnline}
            >
              {consultant.isOnline ? '🔮 상담 예약하기' : '현재 오프라인'}
            </motion.button>
            <p className={`${textClass} opacity-75 text-sm mt-2`}>
              {consultant.experience}년 경력 • {consultant.tags.join(' ')}
            </p>
          </div>

          {/* 후기 섹션 */}
          <div>
            <h3 className={`text-xl font-bold ${textClass} mb-4`}>
              💬 상담 후기 ({consultantReviews.length}개)
            </h3>
            <div className="space-y-4">
              {consultantReviews.slice(0, 3).map((review) => (
                <motion.div
                  key={review.id}
                  className="bg-white/10 p-4 rounded-lg backdrop-blur-md border border-white/20"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{review.userAvatar}</span>
                      <div>
                        <div className={`font-medium ${textClass}`}>{review.username}</div>
                        <div className="text-yellow-400">{'⭐'.repeat(review.rating)}</div>
                      </div>
                    </div>
                    <span className={`${textClass} opacity-75 text-sm`}>{review.date}</span>
                  </div>
                  <p className={`${textClass} mb-2`}>{review.content}</p>
                  <div className="flex items-center gap-2">
                    {review.tags.map((tag, index) => (
                      <span key={index} className="px-2 py-1 rounded text-xs bg-white/10 text-gray-400">
                        {tag}
                      </span>
                    ))}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </motion.div>
    )
  }

  return (
    <motion.div
      className="max-w-7xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* 헤더 */}
      <motion.div
        className="text-center mb-12"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className="text-4xl font-bold mb-6 text-white">
          💬 {viewMode === 'cyber_fantasy' ? '사이버 상담소' : '1:1 전문가 상담'}
        </h1>
        <p className="text-gray-300 text-lg">
          {viewMode === 'cyber_fantasy' 
            ? 'AI와 인간 전문가가 함께하는 미래형 상담'
            : '검증된 전문가와의 개인 맞춤 상담으로 고민 해결'
          }
        </p>
      </motion.div>

      {/* 탭 메뉴 */}
      <motion.div
        className="flex flex-wrap gap-4 justify-center mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        {[
          { key: 'consultants', label: '👨‍🎓 전문가', desc: '상담사 프로필' },
          { key: 'packages', label: '📦 패키지', desc: '상담 요금제' },
          { key: 'reviews', label: '⭐ 후기', desc: '생생한 후기' }
        ].map((tab) => (
          <motion.button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              activeTab === tab.key
                ? viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                : 'bg-white/10 hover:bg-white/20 text-gray-300'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <div className="text-center">
              <div>{tab.label}</div>
              <div className="text-xs opacity-75">{tab.desc}</div>
            </div>
          </motion.button>
        ))}
      </motion.div>

      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'consultants' && (
            <div>
              {/* 카테고리 필터 */}
              <div className="mb-8">
                <div className="flex flex-wrap gap-3 justify-center">
                  <motion.button
                    onClick={() => setSelectedCategory('all')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      selectedCategory === 'all'
                        ? viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                        : 'bg-white/10 hover:bg-white/20 text-gray-300'
                    }`}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    🌟 전체 ({consultants.length})
                  </motion.button>
                  {consultationCategories.map((category) => (
                    <motion.button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        selectedCategory === category.id
                          ? viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                          : 'bg-white/10 hover:bg-white/20 text-gray-300'
                      }`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {category.icon} {category.name} ({category.count})
                    </motion.button>
                  ))}
                </div>
              </div>

              {/* 전문가 목록 */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredConsultants.map((consultant, index) => (
                  <motion.div
                    key={consultant.id}
                    className={`${cardClass} p-6 cursor-pointer hover:scale-[1.02] transition-transform`}
                    onClick={() => setSelectedConsultant(consultant.id)}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * index }}
                    whileHover={{ y: -5 }}
                  >
                    <div className="text-center mb-4">
                      <div className="text-6xl mb-2">{consultant.avatar}</div>
                      <div className={`flex items-center justify-center gap-2 ${consultant.isOnline ? 'text-green-400' : 'text-gray-400'}`}>
                        <div className={`w-2 h-2 rounded-full ${consultant.isOnline ? 'bg-green-400' : 'bg-gray-400'}`} />
                        <span className="text-sm">{consultant.isOnline ? '온라인' : '오프라인'}</span>
                      </div>
                    </div>

                    <div className="text-center">
                      <h3 className={`text-lg font-bold ${textClass} mb-1`}>
                        {consultant.name}
                      </h3>
                      <p className={`${accentClass} text-sm mb-2`}>
                        {consultant.nickname}
                      </p>
                      
                      <div className="flex items-center justify-center gap-2 mb-3">
                        <span className="text-yellow-400">⭐ {consultant.rating}</span>
                        <span className={`${textClass} opacity-75 text-sm`}>
                          ({consultant.reviewCount})
                        </span>
                      </div>

                      <div className="flex flex-wrap gap-1 justify-center mb-3">
                        {consultant.specialties.slice(0, 2).map((specialty, index) => (
                          <span key={index} className="px-2 py-1 rounded-full bg-purple-500/30 text-white text-xs">
                            {specialty}
                          </span>
                        ))}
                      </div>

                      <div className={`text-lg font-bold ${accentClass} mb-2`}>
                        {consultant.pricePerMinute.toLocaleString()}원/분
                      </div>

                      <p className={`${textClass} text-sm opacity-75 line-clamp-2`}>
                        {consultant.introduction}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'packages' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {consultationPackages.map((pkg, index) => (
                <motion.div
                  key={pkg.id}
                  className={`${cardClass} p-6 relative ${pkg.isPopular ? 'ring-2 ring-purple-500' : ''}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * index }}
                  whileHover={{ y: -5 }}
                >
                  {pkg.isPopular && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm px-3 py-1 rounded-full">
                      인기
                    </div>
                  )}

                  <div className="text-center">
                    <h3 className={`text-xl font-bold ${textClass} mb-2`}>
                      {pkg.name}
                    </h3>
                    <p className={`${textClass} opacity-75 text-sm mb-4`}>
                      {pkg.description}
                    </p>
                    
                    <div className={`text-3xl font-bold ${accentClass} mb-2`}>
                      {pkg.price.toLocaleString()}원
                    </div>
                    {pkg.discount > 0 && (
                      <div className={`${textClass} opacity-75 text-sm line-through mb-4`}>
                        {pkg.originalPrice.toLocaleString()}원
                      </div>
                    )}

                    <div className={`${textClass} text-sm mb-4`}>
                      {pkg.duration}분 상담
                    </div>

                    <ul className={`${textClass} text-sm space-y-1 mb-6 text-left`}>
                      {pkg.features.map((feature, index) => (
                        <li key={index}>✓ {feature}</li>
                      ))}
                    </ul>

                    <motion.button
                      className={`w-full py-3 rounded-lg font-bold ${
                        viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                      }`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      선택하기
                    </motion.button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}

          {activeTab === 'reviews' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {reviews.slice(0, 6).map((review, index) => (
                <motion.div
                  key={review.id}
                  className={`${cardClass} p-6`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * index }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{review.userAvatar}</span>
                      <div>
                        <div className={`font-medium ${textClass}`}>{review.username}</div>
                        <div className="text-yellow-400">{'⭐'.repeat(review.rating)}</div>
                      </div>
                    </div>
                    <span className={`${textClass} opacity-75 text-sm`}>{review.date}</span>
                  </div>

                  <div className="mb-4">
                    <span className="px-3 py-1 rounded-full bg-purple-500/30 text-white text-sm">
                      {review.category}
                    </span>
                    <span className="ml-2 px-3 py-1 rounded-full bg-blue-500/30 text-blue-200 text-sm">
                      {review.consultationType === 'chat' ? '💬 채팅' : 
                       review.consultationType === 'voice' ? '📞 음성' : '📹 영상'}
                    </span>
                  </div>

                  <p className={`${textClass} mb-4`}>{review.content}</p>

                  <div className="flex items-center justify-between">
                    <div className="flex flex-wrap gap-1">
                      {review.tags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 rounded text-xs bg-white/10 text-gray-400">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <div className={`${textClass} opacity-75 text-sm flex items-center gap-1`}>
                      👍 {review.likes}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </motion.div>
  )
}

export default Consultation