import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { storeCategories, products, bestsellers, newProducts, saleEvents } from '../../data/storeData'

type ViewMode = 'basic' | 'cyber_fantasy'

interface StoreProps {
  viewMode: ViewMode
}

const Store: React.FC<StoreProps> = ({ viewMode }) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null)
  const [activeFilter, setActiveFilter] = useState<'all' | 'bestseller' | 'new' | 'sale'>('all')

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
  const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white'
  const accentClass = viewMode === 'cyber_fantasy' ? 'text-pink-300' : 'text-purple-300'

  let filteredProducts = products

  if (selectedCategory !== 'all') {
    filteredProducts = filteredProducts.filter(product => product.category === selectedCategory)
  }

  if (activeFilter === 'bestseller') {
    filteredProducts = filteredProducts.filter(product => product.isBestseller)
  } else if (activeFilter === 'new') {
    filteredProducts = filteredProducts.filter(product => product.isNew)
  } else if (activeFilter === 'sale') {
    filteredProducts = filteredProducts.filter(product => product.discount > 0)
  }

  if (selectedProduct) {
    const product = products.find(p => p.id === selectedProduct)
    if (!product) return null

    return (
      <motion.div
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.button
          onClick={() => setSelectedProduct(null)}
          className={`mb-6 px-4 py-2 rounded-lg ${
            viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 스토어로 돌아가기
        </motion.button>

        <motion.div
          className={`${cardClass} p-8`}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex flex-col lg:flex-row gap-8">
            {/* 상품 이미지 */}
            <div className="lg:w-1/2">
              <div className="text-center mb-6">
                <div className="text-8xl mb-4">{product.images[0]}</div>
                <div className="flex justify-center gap-2">
                  {product.images.map((image, index) => (
                    <div key={index} className="text-2xl p-2 bg-white/10 rounded-lg">
                      {image}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 상품 정보 */}
            <div className="lg:w-1/2">
              <div className="mb-4">
                <span className={`px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r ${
                  storeCategories.find(cat => cat.id === product.category)?.color
                } text-white`}>
                  {storeCategories.find(cat => cat.id === product.category)?.name}
                </span>
                {product.isNew && (
                  <span className="ml-2 px-3 py-1 rounded-full text-sm font-medium bg-green-500 text-white">
                    🆕 신상품
                  </span>
                )}
                {product.isBestseller && (
                  <span className="ml-2 px-3 py-1 rounded-full text-sm font-medium bg-red-500 text-white">
                    🔥 베스트셀러
                  </span>
                )}
              </div>

              <h1 className={`text-3xl font-bold ${textClass} mb-4`}>
                {product.name}
              </h1>

              <p className={`${textClass} opacity-75 mb-6`}>
                {product.description}
              </p>

              {/* 가격 */}
              <div className="mb-6">
                <div className={`text-3xl font-bold ${accentClass} mb-2`}>
                  {product.price.toLocaleString()}원
                </div>
                {product.discount > 0 && (
                  <div className="flex items-center gap-3">
                    <span className={`${textClass} opacity-75 line-through`}>
                      {product.originalPrice.toLocaleString()}원
                    </span>
                    <span className="px-2 py-1 rounded-full bg-red-500 text-white text-sm font-bold">
                      {product.discount}% 할인
                    </span>
                  </div>
                )}
              </div>

              {/* 평점 및 리뷰 */}
              <div className="flex items-center gap-4 mb-6">
                <div className="flex items-center gap-1">
                  <span className="text-yellow-400">⭐</span>
                  <span className={`${textClass} font-medium`}>{product.rating}</span>
                </div>
                <span className={`${textClass} opacity-75`}>
                  리뷰 {product.reviewCount.toLocaleString()}개
                </span>
                <span className={`${textClass} opacity-75`}>
                  판매 {product.salesCount.toLocaleString()}개
                </span>
              </div>

              {/* 주요 기능 */}
              <div className="mb-6">
                <h3 className={`font-bold ${textClass} mb-3`}>✨ 주요 기능</h3>
                <ul className={`${textClass} space-y-2`}>
                  {product.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <span className="mr-2">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              {/* 구매 버튼 */}
              <div className="space-y-3">
                <motion.button
                  className={`w-full py-4 rounded-lg text-lg font-bold ${
                    viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  🛒 장바구니 담기
                </motion.button>
                
                <motion.button
                  className="w-full py-4 rounded-lg text-lg font-bold bg-gradient-to-r from-green-500 to-teal-500 text-white hover:from-green-600 hover:to-teal-600 transition-colors"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  💳 바로 구매하기
                </motion.button>
              </div>

              {/* 배송 정보 */}
              <div className={`mt-6 p-4 bg-white/5 rounded-lg ${textClass}`}>
                <h4 className="font-bold mb-2">📦 배송 정보</h4>
                <p className="text-sm opacity-75">{product.deliveryInfo}</p>
                {product.stock && (
                  <p className="text-sm opacity-75 mt-1">
                    재고: {product.stock}개 남음
                  </p>
                )}
              </div>

              {/* 태그 */}
              <div className="mt-6">
                <div className="flex flex-wrap gap-2">
                  {product.tags.map((tag, index) => (
                    <span key={index} className="px-2 py-1 rounded text-sm bg-white/10 text-gray-400">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
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
        <h1 className={`text-4xl md:text-5xl font-bold mb-6 ${
          viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic'
        }`}>
          🛍️ {viewMode === 'cyber_fantasy' ? '사이버 스토어' : 'HEAL7 스토어'}
        </h1>
        <p className="text-gray-300 text-lg">
          {viewMode === 'cyber_fantasy' 
            ? '미래형 운세 상품과 디지털 콘텐츠'
            : '운세와 개운을 위한 모든 것'
          }
        </p>
      </motion.div>

      {/* 이벤트 배너 */}
      {saleEvents.length > 0 && (
        <motion.div
          className="mb-8"
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className={`bg-gradient-to-r ${saleEvents[0].bannerColor} p-6 rounded-xl text-white`}>
            <h2 className="text-2xl font-bold mb-2">🎉 {saleEvents[0].name}</h2>
            <p className="text-lg mb-4">{saleEvents[0].description}</p>
            <div className="flex items-center justify-between">
              <span className="text-3xl font-bold">{saleEvents[0].discount}% 할인!</span>
              <span className="text-sm opacity-90">~{saleEvents[0].endDate}까지</span>
            </div>
          </div>
        </motion.div>
      )}

      {/* 필터 버튼 */}
      <motion.div
        className="flex flex-wrap gap-3 justify-center mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {[
          { key: 'all', label: '🌟 전체', count: products.length },
          { key: 'bestseller', label: '🔥 베스트', count: bestsellers.length },
          { key: 'new', label: '🆕 신상품', count: newProducts.length },
          { key: 'sale', label: '💰 할인', count: products.filter(p => p.discount > 0).length }
        ].map((filter) => (
          <motion.button
            key={filter.key}
            onClick={() => setActiveFilter(filter.key as any)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeFilter === filter.key
                ? viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
                : 'bg-white/10 hover:bg-white/20 text-gray-300'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {filter.label} ({filter.count})
          </motion.button>
        ))}
      </motion.div>

      {/* 카테고리 필터 */}
      <motion.div
        className="flex flex-wrap gap-3 justify-center mb-8"
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
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
          전체 카테고리
        </motion.button>
        {storeCategories.map((category) => (
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
            {category.icon} {category.name} ({category.productCount})
          </motion.button>
        ))}
      </motion.div>

      {/* 상품 목록 */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        {filteredProducts.map((product, index) => (
          <motion.div
            key={product.id}
            className={`${cardClass} p-6 cursor-pointer hover:scale-[1.02] transition-transform relative`}
            onClick={() => setSelectedProduct(product.id)}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 + index * 0.05 }}
            whileHover={{ y: -5 }}
          >
            {/* 상품 배지 */}
            <div className="absolute top-4 right-4 flex flex-col gap-1">
              {product.isNew && (
                <span className="px-2 py-1 rounded-full text-xs bg-green-500 text-white">
                  NEW
                </span>
              )}
              {product.isBestseller && (
                <span className="px-2 py-1 rounded-full text-xs bg-red-500 text-white">
                  BEST
                </span>
              )}
              {product.discount > 0 && (
                <span className="px-2 py-1 rounded-full text-xs bg-orange-500 text-white">
                  -{product.discount}%
                </span>
              )}
            </div>

            {/* 상품 이미지 */}
            <div className="text-center mb-4">
              <div className="text-6xl mb-2">{product.images[0]}</div>
              <span className={`px-2 py-1 rounded text-xs bg-gradient-to-r ${
                storeCategories.find(cat => cat.id === product.category)?.color
              } text-white`}>
                {storeCategories.find(cat => cat.id === product.category)?.name}
              </span>
            </div>

            {/* 상품 정보 */}
            <h3 className={`text-lg font-bold ${textClass} mb-2 line-clamp-2`}>
              {product.name}
            </h3>
            
            <p className={`${textClass} opacity-75 text-sm mb-3 line-clamp-2`}>
              {product.description}
            </p>

            {/* 평점 */}
            <div className="flex items-center gap-2 mb-3">
              <div className="flex items-center">
                <span className="text-yellow-400 text-sm">⭐</span>
                <span className={`${textClass} text-sm ml-1`}>{product.rating}</span>
              </div>
              <span className={`${textClass} opacity-75 text-sm`}>
                ({product.reviewCount.toLocaleString()})
              </span>
            </div>

            {/* 가격 */}
            <div className="mb-4">
              <div className={`text-xl font-bold ${accentClass}`}>
                {product.price.toLocaleString()}원
              </div>
              {product.discount > 0 && (
                <div className={`${textClass} opacity-75 text-sm line-through`}>
                  {product.originalPrice.toLocaleString()}원
                </div>
              )}
            </div>

            {/* 구매 버튼 */}
            <motion.button
              className={`w-full py-2 rounded-lg font-medium ${
                viewMode === 'cyber_fantasy' ? 'btn-mystic' : 'btn-cosmic'
              }`}
              onClick={(e) => {
                e.stopPropagation()
                setSelectedProduct(product.id)
              }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              자세히 보기
            </motion.button>

            {/* 배송 정보 */}
            <p className={`${textClass} opacity-75 text-xs mt-2 text-center`}>
              {product.deliveryInfo}
            </p>
          </motion.div>
        ))}
      </motion.div>

      {filteredProducts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🛍️</div>
          <p className={`${textClass} opacity-75`}>
            선택한 조건에 맞는 상품이 없습니다.
          </p>
        </div>
      )}
    </motion.div>
  )
}

export default Store