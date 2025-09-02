/**
 * 🎯 페이지 래퍼 컴포넌트
 * 기존 컴포넌트를 감싸서 Router 기능을 점진적으로 추가
 * 기존 애니메이션과 테마 시스템 100% 보존
 */

import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { PageWrapperProps } from '../../types/routingTypes'
import { generateMetadata } from '../../config/routeConfig'

export const PageWrapper: React.FC<PageWrapperProps> = ({
  children,
  routeInfo,
  viewMode,
  animationKey
}) => {
  
  // 🎯 SEO 메타데이터 동적 설정
  useEffect(() => {
    const metadata = generateMetadata(routeInfo)
    
    // 페이지 제목 설정
    document.title = metadata.title
    
    // 메타 태그 설정
    const metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
      metaDescription.setAttribute('content', metadata.description)
    } else {
      const meta = document.createElement('meta')
      meta.name = 'description'
      meta.content = metadata.description
      document.head.appendChild(meta)
    }
    
    // 키워드 메타 태그
    const metaKeywords = document.querySelector('meta[name="keywords"]')
    if (metaKeywords) {
      metaKeywords.setAttribute('content', metadata.keywords)
    } else {
      const meta = document.createElement('meta')
      meta.name = 'keywords'
      meta.content = metadata.keywords
      document.head.appendChild(meta)
    }
    
    // Open Graph 메타 태그들
    const ogTags = [
      { property: 'og:title', content: metadata.ogTitle },
      { property: 'og:description', content: metadata.ogDescription },
      { property: 'og:image', content: metadata.ogImage },
      { property: 'og:type', content: 'website' },
      { property: 'og:url', content: window.location.href }
    ]
    
    ogTags.forEach(({ property, content }) => {
      let ogTag = document.querySelector(`meta[property="${property}"]`)
      if (ogTag) {
        ogTag.setAttribute('content', content)
      } else {
        const meta = document.createElement('meta')
        meta.setAttribute('property', property)
        meta.content = content
        document.head.appendChild(meta)
      }
    })
    
    // Twitter Card 메타 태그들
    const twitterTags = [
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: metadata.ogTitle },
      { name: 'twitter:description', content: metadata.ogDescription },
      { name: 'twitter:image', content: metadata.ogImage }
    ]
    
    twitterTags.forEach(({ name, content }) => {
      let twitterTag = document.querySelector(`meta[name="${name}"]`)
      if (twitterTag) {
        twitterTag.setAttribute('content', content)
      } else {
        const meta = document.createElement('meta')
        meta.name = name
        meta.content = content
        document.head.appendChild(meta)
      }
    })
    
  }, [routeInfo])
  
  // 🎨 기존 애니메이션 시스템 완전 보존
  // App.tsx의 AnimatePresence와 동일한 패턴 사용
  return (
    <motion.div
      key={animationKey || routeInfo.pageId}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="w-full h-full"
    >
      {/* 📊 접근성 개선: 페이지 제목 스크린리더용 */}
      <div className="sr-only" role="banner" aria-label={`${routeInfo.label} 페이지`}>
        {routeInfo.title}
      </div>
      
      {/* 🎯 기존 컴포넌트 그대로 렌더링 */}
      {children}
      
      {/* 🔍 개발 모드에서 라우트 정보 디버깅 */}
      {process.env.NODE_ENV === 'development' && (
        <div 
          className="fixed bottom-2 left-2 bg-black/80 text-white text-xs px-2 py-1 rounded z-50 opacity-30 hover:opacity-100 transition-opacity"
          title="라우트 정보 (개발 모드에서만 표시)"
        >
          📍 {routeInfo.path} | 🎯 {routeInfo.pageId} | 🎨 {viewMode}
        </div>
      )}
    </motion.div>
  )
}