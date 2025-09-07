import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { magazineCategories, magazineArticles, editorsPick, popularTags } from '../../data/magazineData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface MagazineProps {
  viewMode: ViewMode
}

const Magazine: React.FC<MagazineProps> = ({ viewMode }) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedArticle, setSelectedArticle] = useState<string | null>(null)

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-featured' : 'card-base'
  const textClass = 'theme-text-primary'
  const accentClass = 'theme-accent'

  const filteredArticles = selectedCategory === 'all' 
    ? magazineArticles 
    : magazineArticles.filter(article => article.category === selectedCategory)

  // const featuredArticles = magazineArticles.filter(article => article.isFeatured) // 예비용
  const editorsPickArticles = magazineArticles.filter(article => editorsPick.includes(article.id))

  if (selectedArticle) {
    const article = magazineArticles.find(a => a.id === selectedArticle)
    if (!article) return null

    return (
      <motion.div
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* 뒤로가기 버튼 */}
        <motion.button
          onClick={() => setSelectedArticle(null)}
          className="mb-6 btn-secondary"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 목록으로 돌아가기
        </motion.button>

        {/* 기사 상세 */}
        <motion.article
          className={`${cardClass} p-8`}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {/* 기사 헤더 */}
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-4">
              <span className={`px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r ${
                magazineCategories.find(cat => cat.id === article.category)?.color || 'from-gray-500 to-gray-600'
              } text-white`}>
                {magazineCategories.find(cat => cat.id === article.category)?.name}
              </span>
              {article.isPremium && (
                <span className="px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-amber-500 to-orange-500 text-white">
                  💎 프리미엄
                </span>
              )}
            </div>
            
            <h1 className="text-3xl md:text-4xl font-bold theme-text-heading mb-4">
              {article.title}
            </h1>
            
            <p className="text-xl theme-accent mb-6">
              {article.subtitle}
            </p>
            
            <div className="flex flex-wrap items-center gap-4 text-sm theme-text-caption">
              <span className="flex items-center gap-2">
                <span className="text-2xl">{article.authorImage}</span>
                {article.author}
              </span>
              <span>📅 {article.publishDate}</span>
              <span>⏱️ {article.readTime} 읽기</span>
              <span>👀 {article.views.toLocaleString()}</span>
              <span>❤️ {article.likes.toLocaleString()}</span>
              <span>💬 {article.comments}</span>
            </div>
          </div>

          {/* 기사 내용 */}
          <div className="theme-text-body leading-relaxed whitespace-pre-line mb-8">
            {article.content}
          </div>

          {/* 태그 */}
          <div className="flex flex-wrap gap-2 mb-6">
            {article.tags.map((tag, index) => (
              <span 
                key={index} 
                className="px-3 py-1 rounded-full text-sm bg-[var(--theme-bg-primary)] text-[var(--theme-text-primary)] border border-[var(--theme-border)]"
              >
                {tag}
              </span>
            ))}
          </div>

          {/* 소셜 공유 버튼 */}
          <div className="flex items-center gap-4">
            <motion.button
              className="btn-primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                if (navigator.share) {
                  navigator.share({
                    title: article.title,
                    text: article.excerpt,
                    url: window.location.href
                  })
                } else {
                  navigator.clipboard.writeText(window.location.href)
                  alert('링크가 클립보드에 복사되었습니다!')
                }
              }}
            >
              📱 공유하기
            </motion.button>
            
            <motion.button
              className="btn-outlined"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ❤️ 좋아요 {article.likes.toLocaleString()}
            </motion.button>
          </div>
        </motion.article>
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
        <h1 className="text-4xl font-bold mb-6 theme-text-heading">
          📰 {viewMode === 'cyber_fantasy' ? '사이버 매거진' : '치유마녀 매거진'}
        </h1>
        <p className="theme-text-secondary text-lg">
          {viewMode === 'cyber_fantasy' 
            ? '차세대 MZ 운세 트렌드의 모든 것'
            : 'MZ세대를 위한 운세 트렌드와 라이프스타일 매거진'
          }
        </p>
      </motion.div>

      {/* 인기 태그 */}
      <motion.div
        className="mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <h2 className={`text-xl font-bold ${textClass} mb-4`}>🔥 인기 태그</h2>
        <div className="flex flex-wrap gap-2">
          {popularTags.slice(0, 10).map((tag, index) => (
            <motion.span
              key={index}
              className="px-3 py-1 rounded-full text-sm bg-[var(--theme-bg-primary)] hover:bg-[var(--theme-bg-secondary)] cursor-pointer text-[var(--theme-text-primary)] border border-[var(--theme-border)] transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {tag}
            </motion.span>
          ))}
        </div>
      </motion.div>

      {/* 카테고리 필터 */}
      <motion.div
        className="mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex flex-wrap gap-3">
          <motion.button
            onClick={() => setSelectedCategory('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedCategory === 'all'
                ? 'btn-primary'
                : 'btn-ghost'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            🌟 전체
          </motion.button>
          {magazineCategories.map((category) => (
            <motion.button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedCategory === category.id
                  ? 'btn-primary'
                  : 'btn-ghost'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {category.icon} {category.name} ({category.articleCount})
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* 에디터 추천 */}
      {selectedCategory === 'all' && (
        <motion.section
          className="mb-12"
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className={`text-2xl font-bold ${textClass} mb-6 flex items-center`}>
            ⭐ 에디터 추천
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {editorsPickArticles.map((article, index) => (
              <motion.article
                key={article.id}
                className={`${cardClass} p-6 cursor-pointer hover:scale-[1.02] transition-transform`}
                onClick={() => setSelectedArticle(article.id)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className={`px-2 py-1 rounded text-xs font-medium bg-gradient-to-r ${
                    magazineCategories.find(cat => cat.id === article.category)?.color
                  } text-white`}>
                    {magazineCategories.find(cat => cat.id === article.category)?.name}
                  </span>
                  <span className="text-4xl">{article.coverImage}</span>
                </div>
                <h3 className={`text-lg font-bold ${textClass} mb-2 line-clamp-2`}>
                  {article.title}
                </h3>
                <p className={`${accentClass} text-sm mb-3 line-clamp-2`}>
                  {article.excerpt}
                </p>
                <div className={`flex items-center justify-between text-xs ${textClass} opacity-75`}>
                  <span>{article.author}</span>
                  <span>👀 {article.views.toLocaleString()}</span>
                </div>
              </motion.article>
            ))}
          </div>
        </motion.section>
      )}

      {/* 기사 목록 */}
      <motion.section
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.7 }}
      >
        <h2 className={`text-2xl font-bold ${textClass} mb-6`}>
          {selectedCategory === 'all' ? '📰 최신 기사' : `${magazineCategories.find(cat => cat.id === selectedCategory)?.icon} ${magazineCategories.find(cat => cat.id === selectedCategory)?.name} 기사`}
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredArticles.map((article, index) => (
            <motion.article
              key={article.id}
              className={`${cardClass} p-6 cursor-pointer hover:scale-[1.02] transition-transform relative`}
              onClick={() => setSelectedArticle(article.id)}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + index * 0.1 }}
              whileHover={{ y: -5 }}
            >
              {/* 프리미엄 배지 */}
              {article.isPremium && (
                <div className="absolute top-4 right-4 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-xs px-2 py-1 rounded-full">
                  💎
                </div>
              )}

              <div className="flex items-center gap-2 mb-3">
                <span className={`px-2 py-1 rounded text-xs font-medium bg-gradient-to-r ${
                  magazineCategories.find(cat => cat.id === article.category)?.color
                } text-white`}>
                  {magazineCategories.find(cat => cat.id === article.category)?.name}
                </span>
                <span className="text-4xl">{article.coverImage}</span>
              </div>

              <h3 className={`text-lg font-bold ${textClass} mb-2 line-clamp-2`}>
                {article.title}
              </h3>
              
              <p className={`${accentClass} text-sm mb-4 line-clamp-3`}>
                {article.excerpt}
              </p>

              <div className={`flex items-center justify-between text-xs ${textClass} opacity-75 mb-3`}>
                <div className="flex items-center gap-2">
                  <span>{article.authorImage}</span>
                  <span>{article.author}</span>
                </div>
                <span>{article.publishDate}</span>
              </div>

              <div className={`flex items-center justify-between text-xs ${textClass} opacity-75`}>
                <span>⏱️ {article.readTime}</span>
                <div className="flex items-center gap-3">
                  <span>👀 {article.views.toLocaleString()}</span>
                  <span>❤️ {article.likes.toLocaleString()}</span>
                  <span>💬 {article.comments}</span>
                </div>
              </div>
              
              {/* 태그 미리보기 */}
              <div className="flex flex-wrap gap-1 mt-3">
                {article.tags.slice(0, 3).map((tag, tagIndex) => (
                  <span 
                    key={tagIndex} 
                    className="px-2 py-0.5 rounded text-xs bg-white/25 text-white"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </motion.article>
          ))}
        </div>
        
        {filteredArticles.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📰</div>
            <p className={`${textClass} opacity-75`}>
              선택한 카테고리에 기사가 없습니다.
            </p>
          </div>
        )}
      </motion.section>
    </motion.div>
  )
}

export default Magazine