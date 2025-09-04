/**
 * 🔮 대시보드 탭 - 시스템 종합 현황
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  Users, CheckCircle, TrendingUp, DollarSign,
  Bell, AlertTriangle
} from 'lucide-react'

export const DashboardTab = () => {
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
            className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">{stat.title}</p>
                <p className="text-white text-2xl font-bold">{stat.value}</p>
              </div>
              <stat.icon className={`w-8 h-8 text-${stat.color}-400`} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* 실시간 알림 영역 */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
        <h3 className="text-white text-lg font-semibold mb-4 flex items-center">
          <Bell className="w-5 h-5 mr-2 text-yellow-400" />
          긴급 알림 & 대기 중인 업무
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-red-500/20 rounded border border-red-400/30">
            <span className="text-red-300">⚠️ 1:1 문의 {systemStats.pendingInquiries}건 답변 대기 중</span>
            <button className="text-red-400 hover:text-red-300 text-sm underline">확인</button>
          </div>
          <div className="flex items-center justify-between p-3 bg-blue-500/20 rounded border border-blue-400/30">
            <span className="text-blue-300">📝 신규 리뷰 {systemStats.unreadReviews}건 검토 필요</span>
            <button className="text-blue-400 hover:text-blue-300 text-sm underline">검토</button>
          </div>
        </div>
      </div>

      {/* 시스템 상태 모니터링 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <h3 className="text-white text-lg font-semibold mb-4">서버 상태</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-300">시스템 가동률</span>
              <span className="text-green-400 font-semibold">{systemStats.systemUptime}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">사주 엔진 상태</span>
              <span className="text-green-400">정상</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">데이터베이스</span>
              <span className="text-green-400">연결됨</span>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <h3 className="text-white text-lg font-semibold mb-4">최근 활동</h3>
          <div className="space-y-2 text-sm">
            <div className="text-gray-300">• 신규 회원가입: 김○○님 (3분전)</div>
            <div className="text-gray-300">• 사주풀이 결제: 이○○님 (5분전)</div>
            <div className="text-gray-300">• 1:1 문의: 박○○님 (12분전)</div>
            <div className="text-gray-300">• 리뷰 작성: 최○○님 (18분전)</div>
          </div>
        </div>
      </div>
    </div>
  )
}