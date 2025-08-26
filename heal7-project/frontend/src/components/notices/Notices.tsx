import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { notices, subscriptionPlans, sampleUser } from '../../data/systemData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface NoticesProps {
  viewMode: ViewMode
}

const Notices: React.FC<NoticesProps> = ({ viewMode }) => {
  const [selectedNotice, setSelectedNotice] = useState<string | null>(null)
  const [selectedType, setSelectedType] = useState<string>('all')
  const [showSubscription, setShowSubscription] = useState(false)
  const [showProfile, setShowProfile] = useState(false)

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
  const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white'
  const accentClass = viewMode === 'cyber_fantasy' ? 'text-pink-300' : 'text-purple-300'

  const filteredNotices = selectedType === 'all' 
    ? notices 
    : notices.filter(notice => notice.type === selectedType)

  const noticeTypes = [
    { key: 'all', label: '🌟 전체', count: notices.length },
    { key: 'system', label: '⚙️ 시스템', count: notices.filter(n => n.type === 'system').length },
    { key: 'event', label: '🎉 이벤트', count: notices.filter(n => n.type === 'event').length },
    { key: 'update', label: '🔧 업데이트', count: notices.filter(n => n.type === 'update').length },
    { key: 'promotion', label: '💎 프로모션', count: notices.filter(n => n.type === 'promotion').length }
  ]

  if (showSubscription) {
    return (
      <motion.div
        className="max-w-6xl mx-auto"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.button
          onClick={() => setShowSubscription(false)}
          className={`mb-6 px-4 py-2 rounded-lg ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 공지사항으로 돌아가기
        </motion.button>

        <motion.div
          className="text-center mb-12"
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h1 className={`text-4xl font-bold mb-6 ${
            viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic'
          }`}>
            💎 구독 요금제
          </h1>
          <p className="text-gray-300 text-lg">
            더 깊이 있는 운세 경험을 위한 프리미엄 서비스
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {subscriptionPlans.map((plan, index) => (
            <motion.div
              key={plan.id}
              className={`${cardClass} p-8 relative ${plan.isPopular ? 'ring-2 ring-purple-500 scale-105' : ''}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + index * 0.1 }}
            >
              {plan.badge && (
                <div className={`absolute -top-3 left-1/2 transform -translate-x-1/2 bg-gradient-to-r ${plan.color} text-white text-sm px-4 py-1 rounded-full`}>
                  {plan.badge}
                </div>
              )}

              <div className="text-center mb-6">
                <div className="text-6xl mb-4">{plan.icon}</div>
                <h3 className={`text-2xl font-bold ${textClass} mb-2`}>
                  {plan.name}
                </h3>
                <p className={`${textClass} opacity-75 mb-4`}>
                  {plan.description}
                </p>
              </div>

              <div className="text-center mb-6">
                <div className={`text-4xl font-bold ${accentClass} mb-2`}>
                  {plan.price === 0 ? '무료' : `${plan.price.toLocaleString()}원`}
                </div>
                {plan.price > 0 && (
                  <>
                    <div className={`${textClass} opacity-75 text-sm line-through`}>
                      {plan.originalPrice.toLocaleString()}원
                    </div>
                    <div className="text-green-400 text-sm font-medium">
                      {plan.discount}% 할인!
                    </div>
                  </>
                )}
                <div className={`${textClass} opacity-75 text-sm mt-2`}>
                  {plan.duration === 'monthly' ? '월간' : '연간'} 결제
                </div>
              </div>

              <div className="mb-8">
                <h4 className={`font-bold ${textClass} mb-4`}>포함 혜택</h4>
                <ul className={`${textClass} space-y-2`}>
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start text-sm">
                      <span className="text-green-400 mr-2 mt-0.5">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <motion.button
                className={`w-full py-4 rounded-lg font-bold text-lg ${
                  plan.id === sampleUser.subscriptionType
                    ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                    : viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                }`}
                disabled={plan.id === sampleUser.subscriptionType}
                whileHover={plan.id !== sampleUser.subscriptionType ? { scale: 1.05 } : {}}
                whileTap={plan.id !== sampleUser.subscriptionType ? { scale: 0.95 } : {}}
              >
                {plan.id === sampleUser.subscriptionType ? '현재 플랜' : '선택하기'}
              </motion.button>
            </motion.div>
          ))}
        </div>
      </motion.div>
    )
  }

  if (showProfile) {
    return (
      <motion.div
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.button
          onClick={() => setShowProfile(false)}
          className={`mb-6 px-4 py-2 rounded-lg ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 공지사항으로 돌아가기
        </motion.button>

        <motion.div
          className={`${cardClass} p-8`}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="text-center mb-8">
            <div className="text-8xl mb-4">{sampleUser.avatar}</div>
            <h1 className={`text-3xl font-bold ${textClass} mb-2`}>
              {sampleUser.username}
            </h1>
            <p className={`${accentClass} mb-4`}>{sampleUser.email}</p>
            
            <div className="flex justify-center gap-4 mb-6">
              <div className="text-center">
                <div className={`text-2xl font-bold ${textClass}`}>Lv.{sampleUser.profile.level}</div>
                <div className={`text-sm ${textClass} opacity-75`}>레벨</div>
              </div>
              <div className="text-center">
                <div className={`text-2xl font-bold ${accentClass}`}>
                  {sampleUser.profile.consultationHistory}
                </div>
                <div className={`text-sm ${textClass} opacity-75`}>상담 횟수</div>
              </div>
              <div className="text-center">
                <div className={`text-2xl font-bold ${textClass}`}>
                  {sampleUser.profile.totalSpent.toLocaleString()}원
                </div>
                <div className={`text-sm ${textClass} opacity-75`}>총 구매</div>
              </div>
            </div>

            <div className={`inline-flex items-center px-4 py-2 rounded-full ${
              sampleUser.subscriptionType === 'premium' 
                ? 'bg-gradient-to-r from-purple-500 to-pink-500' 
                : 'bg-gray-600'
            } text-white text-sm`}>
              💎 {sampleUser.subscriptionType === 'premium' ? '프리미엄' : '무료'} 멤버
              {sampleUser.subscriptionExpiry && (
                <span className="ml-2 opacity-75">
                  (~{sampleUser.subscriptionExpiry})
                </span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className={`text-xl font-bold ${textClass} mb-4`}>📊 개인 정보</h3>
              <div className="space-y-3">
                <div className={`${textClass}`}>
                  <span className="opacity-75">가입일:</span> {sampleUser.joinDate}
                </div>
                <div className={`${textClass}`}>
                  <span className="opacity-75">마지막 접속:</span> {sampleUser.lastLogin}
                </div>
                <div className={`${textClass}`}>
                  <span className="opacity-75">생년월일:</span> {sampleUser.profile.birthDate}
                </div>
                <div className={`${textClass}`}>
                  <span className="opacity-75">성별:</span> {sampleUser.profile.gender === 'F' ? '여성' : '남성'}
                </div>
              </div>
            </div>

            <div>
              <h3 className={`text-xl font-bold ${textClass} mb-4`}>🏆 획득 배지</h3>
              <div className="flex flex-wrap gap-2">
                {sampleUser.profile.badges.map((badge, index) => (
                  <span key={index} className="px-3 py-1 rounded-full bg-yellow-500/20 text-yellow-300 text-sm">
                    🏆 {badge}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className={`text-xl font-bold ${textClass} mb-4`}>💫 관심 분야</h3>
              <div className="flex flex-wrap gap-2">
                {sampleUser.profile.interests.map((interest, index) => (
                  <span key={index} className="px-3 py-1 rounded-full bg-purple-500/30 text-purple-200 text-sm">
                    {interest}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className={`text-xl font-bold ${textClass} mb-4`}>⚙️ 설정</h3>
              <div className={`${textClass} space-y-2`}>
                <div className="flex justify-between">
                  <span>알림 수신</span>
                  <span>{sampleUser.preferences.notifications ? '✅' : '❌'}</span>
                </div>
                <div className="flex justify-between">
                  <span>이메일 업데이트</span>
                  <span>{sampleUser.preferences.emailUpdates ? '✅' : '❌'}</span>
                </div>
                <div className="flex justify-between">
                  <span>테마</span>
                  <span>{sampleUser.preferences.theme}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8 text-center space-y-4">
            <motion.button
              onClick={() => setShowSubscription(true)}
              className={`px-6 py-3 rounded-lg font-medium ${
                viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              💎 구독 플랜 변경
            </motion.button>
          </div>
        </motion.div>
      </motion.div>
    )
  }

  if (selectedNotice) {
    const notice = notices.find(n => n.id === selectedNotice)
    if (!notice) return null

    return (
      <motion.div
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.button
          onClick={() => setSelectedNotice(null)}
          className={`mb-6 px-4 py-2 rounded-lg ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 공지사항 목록
        </motion.button>

        <motion.article
          className={`${cardClass} p-8`}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-4">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                notice.type === 'system' ? 'bg-blue-500' :
                notice.type === 'event' ? 'bg-green-500' :
                notice.type === 'update' ? 'bg-purple-500' :
                notice.type === 'promotion' ? 'bg-orange-500' :
                'bg-gray-500'
              } text-white`}>
                {notice.type === 'system' ? '⚙️ 시스템' :
                 notice.type === 'event' ? '🎉 이벤트' :
                 notice.type === 'update' ? '🔧 업데이트' :
                 notice.type === 'promotion' ? '💎 프로모션' :
                 '📢 공지'}
              </span>
              {notice.isImportant && (
                <span className="px-3 py-1 rounded-full text-sm font-medium bg-red-500 text-white">
                  ⚠️ 중요
                </span>
              )}
            </div>
            
            <h1 className={`text-3xl md:text-4xl font-bold ${textClass} mb-4`}>
              {notice.title}
            </h1>
            
            <div className={`flex flex-wrap items-center gap-4 text-sm ${textClass} opacity-75 mb-6`}>
              <span>👨‍💻 {notice.author}</span>
              <span>📅 {notice.publishDate}</span>
              <span>👀 {notice.views.toLocaleString()}</span>
            </div>
          </div>

          <div className={`${textClass} leading-relaxed whitespace-pre-line mb-8`}>
            {notice.content}
          </div>

          {notice.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-6">
              {notice.tags.map((tag, index) => (
                <span key={index} className="px-3 py-1 rounded-full text-sm bg-white/10 text-gray-300">
                  {tag}
                </span>
              ))}
            </div>
          )}

          {notice.attachments && notice.attachments.length > 0 && (
            <div className="mb-6">
              <h3 className={`font-bold ${textClass} mb-3`}>📎 첨부파일</h3>
              <div className="space-y-2">
                {notice.attachments.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                    <span className={`${textClass}`}>{file.name}</span>
                    <div className="flex items-center gap-3">
                      <span className={`${textClass} opacity-75 text-sm`}>{file.size}</span>
                      <button className={`px-3 py-1 rounded ${
                        viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                      } text-sm`}>
                        다운로드
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {notice.relatedLinks && notice.relatedLinks.length > 0 && (
            <div className="mb-6">
              <h3 className={`font-bold ${textClass} mb-3`}>🔗 관련 링크</h3>
              <div className="space-y-2">
                {notice.relatedLinks.map((link, index) => (
                  <motion.a
                    key={index}
                    href={link.url}
                    className={`block p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors ${accentClass}`}
                    whileHover={{ scale: 1.02 }}
                  >
                    {link.title} →
                  </motion.a>
                ))}
              </div>
            </div>
          )}
        </motion.article>
      </motion.div>
    )
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
        className="text-center mb-12"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className={`text-4xl md:text-5xl font-bold mb-6 ${
          viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic'
        }`}>
          📢 {viewMode === 'cyber_fantasy' ? '사이버 공지소' : '공지사항'}
        </h1>
        <p className="text-gray-300 text-lg">
          {viewMode === 'cyber_fantasy' 
            ? 'HEAL7 플랫폼의 모든 소식과 업데이트'
            : 'HEAL7 서비스의 새로운 소식과 중요한 안내사항'
          }
        </p>
      </motion.div>

      {/* 퀵 액세스 버튼 */}
      <motion.div
        className="flex flex-wrap gap-4 justify-center mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <motion.button
          onClick={() => setShowProfile(true)}
          className={`px-6 py-3 rounded-lg font-medium ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          👤 내 프로필
        </motion.button>
        <motion.button
          onClick={() => setShowSubscription(true)}
          className={`px-6 py-3 rounded-lg font-medium ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          💎 구독 플랜
        </motion.button>
      </motion.div>

      {/* 공지 타입 필터 */}
      <motion.div
        className="flex flex-wrap gap-3 justify-center mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {noticeTypes.map((type) => (
          <motion.button
            key={type.key}
            onClick={() => setSelectedType(type.key)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedType === type.key
                ? viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                : 'bg-white/10 hover:bg-white/20 text-gray-300'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {type.label} ({type.count})
          </motion.button>
        ))}
      </motion.div>

      {/* 공지사항 목록 */}
      <motion.div
        className="space-y-4"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        {filteredNotices.map((notice, index) => (
          <motion.article
            key={notice.id}
            className={`${cardClass} p-6 cursor-pointer hover:scale-[1.01] transition-transform ${
              notice.isPinned ? 'ring-1 ring-yellow-500/50' : ''
            }`}
            onClick={() => setSelectedNotice(notice.id)}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 + index * 0.05 }}
            whileHover={{ x: 5 }}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    notice.type === 'system' ? 'bg-blue-500' :
                    notice.type === 'event' ? 'bg-green-500' :
                    notice.type === 'update' ? 'bg-purple-500' :
                    notice.type === 'promotion' ? 'bg-orange-500' :
                    'bg-gray-500'
                  } text-white`}>
                    {notice.type === 'system' ? '⚙️ 시스템' :
                     notice.type === 'event' ? '🎉 이벤트' :
                     notice.type === 'update' ? '🔧 업데이트' :
                     notice.type === 'promotion' ? '💎 프로모션' :
                     '📢 공지'}
                  </span>
                  
                  {notice.isImportant && (
                    <span className="px-2 py-1 rounded-full text-xs bg-red-500 text-white animate-pulse">
                      ⚠️ 중요
                    </span>
                  )}
                  
                  {notice.isPinned && (
                    <span className="px-2 py-1 rounded-full text-xs bg-yellow-500 text-black">
                      📌 고정
                    </span>
                  )}
                </div>

                <h2 className={`text-xl font-bold ${textClass} mb-2 line-clamp-1`}>
                  {notice.title}
                </h2>
                
                <p className={`${textClass} opacity-75 mb-3 line-clamp-2`}>
                  {notice.summary}
                </p>

                <div className={`flex items-center gap-4 text-sm ${textClass} opacity-75`}>
                  <span>👨‍💻 {notice.author}</span>
                  <span>📅 {notice.publishDate}</span>
                  <span>👀 {notice.views.toLocaleString()}</span>
                </div>
              </div>

              <div className="text-right">
                <div className="text-2xl mb-2">
                  {notice.type === 'system' ? '⚙️' :
                   notice.type === 'event' ? '🎉' :
                   notice.type === 'update' ? '🔧' :
                   notice.type === 'promotion' ? '💎' :
                   '📢'}
                </div>
                <div className={`text-sm ${accentClass}`}>
                  자세히 →
                </div>
              </div>
            </div>
          </motion.article>
        ))}
      </motion.div>

      {filteredNotices.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📢</div>
          <p className={`${textClass} opacity-75`}>
            선택한 타입의 공지사항이 없습니다.
          </p>
        </div>
      )}
    </motion.div>
  )
}

export default Notices