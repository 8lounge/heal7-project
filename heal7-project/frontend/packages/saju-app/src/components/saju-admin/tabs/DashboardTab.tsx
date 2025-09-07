/**
 * 🔮 대시보드 탭 - 시스템 종합 현황
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useTheme } from '../../../contexts/ThemeContext'
import {
  Users, CheckCircle, TrendingUp, DollarSign,
  Bell, AlertTriangle
} from 'lucide-react'

export const DashboardTab = () => {
  const { theme } = useTheme()
  const [systemStats, setSystemStats] = useState({
    totalUsers: 15847,
    activeUsers: 3245,
    newUsers: 542,
    dailyRevenue: 1247000,
    monthlyRevenue: 34560000,
    systemUptime: '99.8%',
    pendingInquiries: 23,
    unreadReviews: 15
  })

  return (
    <div className="space-y-6">
      {/* 핵심 지표 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: '총 회원수', value: systemStats.totalUsers.toLocaleString(), icon: Users, color: 'blue' },
          { title: '활성 회원', value: systemStats.activeUsers.toLocaleString(), icon: CheckCircle, color: 'green' },
          { title: '신규 가입', value: systemStats.newUsers.toLocaleString(), icon: TrendingUp, color: 'purple' },
          { title: '일일 매출', value: `₩${Math.floor(systemStats.dailyRevenue / 10000)}만원`, icon: DollarSign, color: 'yellow' }
        ].map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className={`theme-bg-card theme-border rounded-xl theme-shadow p-6 hover:theme-shadow transition-all duration-300 backdrop-blur-lg ${
              theme === 'dark' 
                ? 'bg-gradient-to-br from-purple-500/20 via-violet-500/10 to-fuchsia-500/20 border-purple-400/30' 
                : 'bg-gradient-to-br from-pink-500/20 via-rose-500/10 to-orange-500/20 border-pink-400/30'
            }`}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="theme-text-secondary text-sm font-medium">{stat.title}</p>
                <p className="theme-text-primary text-2xl font-bold">{stat.value}</p>
              </div>
              <stat.icon className={`w-8 h-8 drop-shadow-lg ${
                theme === 'dark' ? 'text-purple-400' : 'text-pink-500'
              }`} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* 실시간 알림 영역 */}
      <div className={`backdrop-blur-lg rounded-xl shadow-2xl p-6 transition-all duration-300 ${
        theme === 'dark' 
          ? 'bg-gradient-to-br from-purple-500/20 via-violet-500/10 to-fuchsia-500/20 border border-purple-400/30 shadow-purple-500/10 hover:shadow-purple-500/20' 
          : 'bg-gradient-to-br from-pink-500/20 via-rose-500/10 to-orange-500/20 border border-pink-400/30 shadow-pink-500/10 hover:shadow-pink-500/20'
      }`}>
        <h3 className={`text-lg font-semibold mb-4 flex items-center ${
          theme === 'dark' ? 'text-white' : 'text-gray-900'
        }`}>
          <Bell className={`w-5 h-5 mr-2 drop-shadow-lg ${
            theme === 'dark' ? 'text-purple-300' : 'text-pink-500'
          }`} />
          긴급 알림 & 대기 중인 업무
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-red-500/20 backdrop-blur-sm rounded-lg border border-red-400/40 shadow-lg">
            <span className="text-red-200">⚠️ 1:1 문의 {systemStats.pendingInquiries}건 답변 대기 중</span>
            <button className="text-red-300 hover:text-red-200 text-sm underline font-medium transition-colors">확인</button>
          </div>
          <div className="flex items-center justify-between p-3 bg-blue-500/20 backdrop-blur-sm rounded-lg border border-blue-400/40 shadow-lg">
            <span className="text-blue-200">📝 신규 리뷰 {systemStats.unreadReviews}건 검토 필요</span>
            <button className="text-blue-300 hover:text-blue-200 text-sm underline font-medium transition-colors">검토</button>
          </div>
        </div>
      </div>

      {/* 시스템 상태 모니터링 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className={`backdrop-blur-lg rounded-xl shadow-2xl p-6 transition-all duration-300 ${
          theme === 'dark' 
            ? 'bg-gradient-to-br from-purple-500/20 via-violet-500/10 to-fuchsia-500/20 border border-purple-400/30 shadow-purple-500/10 hover:shadow-purple-500/20' 
            : 'bg-gradient-to-br from-pink-500/20 via-rose-500/10 to-orange-500/20 border border-pink-400/30 shadow-pink-500/10 hover:shadow-pink-500/20'
        }`}>
          <h3 className={`text-lg font-semibold mb-4 ${
            theme === 'dark' ? 'text-white' : 'text-gray-900'
          }`}>서버 상태</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className={`font-medium ${
                theme === 'dark' ? 'text-purple-200' : 'text-pink-600'
              }`}>시스템 가동률</span>
              <span className="text-green-400 font-semibold drop-shadow-lg">{systemStats.systemUptime}</span>
            </div>
            <div className="flex justify-between">
              <span className={`font-medium ${
                theme === 'dark' ? 'text-purple-200' : 'text-pink-600'
              }`}>사주 엔진 상태</span>
              <span className="text-green-400 drop-shadow-lg">정상</span>
            </div>
            <div className="flex justify-between">
              <span className={`font-medium ${
                theme === 'dark' ? 'text-purple-200' : 'text-pink-600'
              }`}>데이터베이스</span>
              <span className="text-green-400 drop-shadow-lg">연결됨</span>
            </div>
          </div>
        </div>

        <div className={`backdrop-blur-lg rounded-xl shadow-2xl p-6 transition-all duration-300 ${
          theme === 'dark' 
            ? 'bg-gradient-to-br from-purple-500/20 via-violet-500/10 to-fuchsia-500/20 border border-purple-400/30 shadow-purple-500/10 hover:shadow-purple-500/20' 
            : 'bg-gradient-to-br from-pink-500/20 via-rose-500/10 to-orange-500/20 border border-pink-400/30 shadow-pink-500/10 hover:shadow-pink-500/20'
        }`}>
          <h3 className={`text-lg font-semibold mb-4 ${
            theme === 'dark' ? 'text-white' : 'text-gray-900'
          }`}>최근 활동</h3>
          <div className="space-y-2 text-sm">
            <div className={theme === 'dark' ? 'text-purple-200' : 'text-pink-600'}>• 신규 회원가입: 김○○님 (3분전)</div>
            <div className={theme === 'dark' ? 'text-purple-200' : 'text-pink-600'}>• 사주풀이 결제: 이○○님 (5분전)</div>
            <div className={theme === 'dark' ? 'text-purple-200' : 'text-pink-600'}>• 1:1 문의: 박○○님 (12분전)</div>
            <div className={theme === 'dark' ? 'text-purple-200' : 'text-pink-600'}>• 리뷰 작성: 최○○님 (18분전)</div>
          </div>
        </div>
      </div>
    </div>
  )
}