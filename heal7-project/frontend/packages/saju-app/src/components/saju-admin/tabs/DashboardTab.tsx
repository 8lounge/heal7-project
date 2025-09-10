/**
 * 🔮 대시보드 탭 - 시스템 종합 현황
 * @author HEAL7 Admin Team
 * @version 3.0.0 - Real API Integration
 */

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useTheme } from '../../../contexts/ThemeContext'
import {
  Users, CheckCircle, TrendingUp, DollarSign,
  Bell, AlertTriangle, RefreshCw, User, MessageSquare
} from 'lucide-react'

interface DashboardStats {
  total_users: number
  active_users: number
  new_users: number
  daily_revenue: number
  monthly_revenue: number
  system_uptime: number
  pending_inquiries: number
  interpretations_this_week: number
  avg_response_time: number
  last_updated: string
}

interface Activity {
  type: string
  title: string
  description: string
  timestamp: string
  icon: string
  status?: string
}

export const DashboardTab = () => {
  const { theme } = useTheme()
  const [systemStats, setSystemStats] = useState<DashboardStats | null>(null)
  const [recentActivities, setRecentActivities] = useState<Activity[]>([])
  const [loading, setLoading] = useState(false)

  // 대시보드 통계 조회
  const fetchDashboardStats = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/saju/dashboard/stats', {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setSystemStats(data)
      } else {
        console.error('Failed to fetch dashboard stats:', response.status)
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  // 최근 활동 조회
  const fetchRecentActivities = async () => {
    try {
      const response = await fetch('/api/admin/saju/dashboard/recent-activities?limit=10', {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setRecentActivities(data.activities)
      } else {
        console.error('Failed to fetch recent activities:', response.status)
      }
    } catch (error) {
      console.error('Error fetching recent activities:', error)
    }
  }

  // 초기 데이터 로드
  useEffect(() => {
    fetchDashboardStats()
    fetchRecentActivities()
    
    // 30초마다 자동 새로고침
    const interval = setInterval(() => {
      fetchDashboardStats()
      fetchRecentActivities()
    }, 30000)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <h2 className="text-white text-2xl font-bold">관리자 대시보드</h2>
        <div className="flex items-center gap-4">
          {systemStats && (
            <span className="text-sm text-gray-400">
              마지막 업데이트: {new Date(systemStats.last_updated).toLocaleTimeString('ko-KR')}
            </span>
          )}
          <button
            onClick={() => {
              fetchDashboardStats()
              fetchRecentActivities()
            }}
            disabled={loading}
            className="px-3 py-1 bg-blue-600/20 border border-blue-400/30 rounded text-blue-400 text-sm hover:bg-blue-600/30 disabled:opacity-50 flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            새로고침
          </button>
        </div>
      </div>

      {loading && !systemStats ? (
        <div className="flex justify-center items-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
          <span className="ml-2 text-gray-200">대시보드 데이터를 불러오는 중...</span>
        </div>
      ) : (
        <>
          {/* 핵심 지표 카드 */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {systemStats && [
              { title: '총 회원수', value: systemStats.total_users.toLocaleString(), icon: Users, color: 'blue' },
              { title: '활성 회원', value: systemStats.active_users.toLocaleString(), icon: CheckCircle, color: 'green' },
              { title: '신규 가입 (7일)', value: systemStats.new_users.toLocaleString(), icon: TrendingUp, color: 'purple' },
              { title: '일일 매출', value: `₩${Math.floor(systemStats.daily_revenue / 10000).toLocaleString()}만원`, icon: DollarSign, color: 'yellow' }
            ].map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="glass-3 rounded-xl p-6 hover:glass-4 theme-transition backdrop-blur-lg"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="theme-text-secondary text-sm font-medium">{stat.title}</p>
                    <p className="theme-text-primary text-2xl font-bold">{stat.value}</p>
                  </div>
                  <stat.icon className="w-8 h-8 drop-shadow-lg text-[var(--theme-accent)]" />
            </div>
          </motion.div>
        ))}
      </div>

          {/* 실시간 알림 영역 */}
          <div className="glass-3 rounded-xl shadow-2xl p-6 hover:glass-4 theme-transition backdrop-blur-lg">
            <h3 className="text-lg font-semibold mb-4 flex items-center theme-text-heading">
              <Bell className="w-5 h-5 mr-2 drop-shadow-lg text-[var(--theme-accent)]" />
              긴급 알림 & 대기 중인 업무
            </h3>
            <div className="space-y-3">
              {systemStats && systemStats.pending_inquiries > 0 && (
                <div className={`flex items-center justify-between p-3 backdrop-blur-sm rounded-lg shadow-lg border ${
                  theme === 'light' 
                    ? 'bg-orange-100/60 border-orange-300/40 text-orange-800'
                    : 'bg-red-500/20 border-red-400/40 text-red-200'
                }`}>
                  <span>⚠️ 1:1 문의 {systemStats.pending_inquiries}건 답변 대기 중</span>
                  <button className={`text-sm underline font-medium transition-colors ${
                    theme === 'light' 
                      ? 'text-orange-700 hover:text-orange-900'
                      : 'text-red-300 hover:text-red-200'
                  }`}>확인</button>
                </div>
              )}
              {systemStats && (
                <div className={`flex items-center justify-between p-3 backdrop-blur-sm rounded-lg shadow-lg border ${
                  theme === 'light' 
                    ? 'bg-blue-100/60 border-blue-300/40 text-blue-800'
                    : 'bg-blue-500/20 border-blue-400/40 text-blue-200'
                }`}>
                  <span>📊 사주 해석 {systemStats.interpretations_this_week}건 (7일간)</span>
                  <span className="text-sm">평균 응답시간: {systemStats.avg_response_time}시간</span>
                </div>
              )}
              {systemStats && systemStats.system_uptime < 99.0 && (
                <div className={`flex items-center justify-between p-3 backdrop-blur-sm rounded-lg shadow-lg border ${
                  theme === 'light' 
                    ? 'bg-yellow-100/60 border-yellow-300/40 text-yellow-800'
                    : 'bg-yellow-500/20 border-yellow-400/40 text-yellow-200'
                }`}>
                  <span>⚠️ 시스템 가동률 주의: {systemStats.system_uptime}%</span>
                  <AlertTriangle className="w-4 h-4" />
                </div>
              )}
            </div>
          </div>

          {/* 시스템 상태 모니터링 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass-3 rounded-xl shadow-2xl p-6 hover:glass-4 theme-transition backdrop-blur-lg">
              <h3 className="text-lg font-semibold mb-4 theme-text-heading">서버 상태</h3>
              {systemStats ? (
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="font-medium theme-text-secondary">시스템 가동률</span>
                    <span className={`font-semibold drop-shadow-lg ${
                      systemStats.system_uptime >= 99.0 
                        ? theme === 'light' ? 'text-green-600' : 'text-green-400'
                        : theme === 'light' ? 'text-yellow-600' : 'text-yellow-400'
                    }`}>{systemStats.system_uptime}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium theme-text-secondary">월간 매출</span>
                    <span className={`drop-shadow-lg ${
                      theme === 'light' ? 'text-blue-600' : 'text-blue-400'
                    }`}>₩{Math.floor(systemStats.monthly_revenue / 10000).toLocaleString()}만원</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium theme-text-secondary">데이터베이스</span>
                    <span className={`drop-shadow-lg ${
                      theme === 'light' ? 'text-green-600' : 'text-green-400'
                    }`}>연결됨</span>
                  </div>
                </div>
              ) : (
                <div className="theme-text-secondary text-center py-4">
                  서버 상태 데이터를 불러오는 중...
                </div>
              )}
            </div>

            <div className="glass-3 rounded-xl shadow-2xl p-6 hover:glass-4 theme-transition backdrop-blur-lg">
              <h3 className="text-lg font-semibold mb-4 theme-text-heading">최근 활동</h3>
              <div className="space-y-2 text-sm max-h-40 overflow-y-auto">
                {recentActivities.length > 0 ? recentActivities.map((activity, idx) => (
                  <div key={idx} className="theme-text-secondary flex items-start gap-2">
                    {activity.icon === 'user' ? (
                      <User className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    ) : (
                      <MessageSquare className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <span className="font-medium">{activity.title}:</span>
                      <span className="ml-1">{activity.description}</span>
                      <div className="text-xs text-gray-500">
                        {new Date(activity.timestamp).toLocaleString('ko-KR')}
                      </div>
                    </div>
                  </div>
                )) : (
                  <div className="theme-text-secondary text-center py-4">
                    최근 활동이 없습니다.
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}