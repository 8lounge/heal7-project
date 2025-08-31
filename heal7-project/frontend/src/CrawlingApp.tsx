import React from 'react'
import { motion } from 'framer-motion'
import CrawlingDashboard from './components/crawling/CrawlingDashboard'

// 크롤링 시스템 전용 앱
function CrawlingApp() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900/50 to-slate-900">
      {/* 배경 오버레이 */}
      <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-blue-900/40 to-black/70" />
      
      {/* 메인 콘텐츠 */}
      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <CrawlingDashboard />
        </motion.div>
      </div>
    </div>
  )
}

export default CrawlingApp