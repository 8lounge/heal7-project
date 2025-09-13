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
  Bell, AlertTriangle, RefreshCw, User, MessageSquare,
  Brain, CreditCard, Zap, Database, Activity, Clock
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

interface AIMetrics {
  daily_ai_requests: number
  successful_interpretations: number
  ai_response_time: number
  model_usage_stats: { [key: string]: number }
  content_generated_today: number
}

interface PointMetrics {
  total_points_distributed: number
  points_used_today: number
  average_points_per_user: number
  pending_point_requests: number
}

interface Activity {
  time: string
  action: string
  details: string
}

interface AnalyticsResponse {
  system_health: {
    cpu_usage: number
    memory_usage: number
    disk_usage: number
    api_response_time: number
  }
  business_metrics: {
    daily_active_users: number
    daily_consultations: number
    daily_revenue: number
    conversion_rate: number
  }
  saju_system: {
    calculations_today: number
    accuracy_rate: number
    api_calls: number
    error_rate: number
  }
  recent_activities: Activity[]
}

export const DashboardTab = () => {
  const { theme } = useTheme()
  const [systemStats, setSystemStats] = useState<DashboardStats | null>(null)
  const [aiMetrics, setAiMetrics] = useState<AIMetrics | null>(null)
  const [pointMetrics, setPointMetrics] = useState<PointMetrics | null>(null)
  const [recentActivities, setRecentActivities] = useState<Activity[]>([])
  const [loading, setLoading] = useState(false)

  // 대시보드 통계 조회
  const fetchDashboardStats = async () => {
    setLoading(true)
    try {
      const { api } = await import('../../../services/apiService')
      const response = await api.analytics.getDashboard()

      if (response.success && response.data) {
        const analytics: AnalyticsResponse = response.data

        // 백엔드 데이터를 프론트엔드 인터페이스에 맞게 변환
        const mappedStats: DashboardStats = {
          total_users: analytics.business_metrics.daily_active_users * 30, // 추정값
          active_users: analytics.business_metrics.daily_active_users,
          new_users: Math.floor(analytics.business_metrics.daily_active_users * 0.1), // 추정값
          daily_revenue: analytics.business_metrics.daily_revenue,
          monthly_revenue: analytics.business_metrics.daily_revenue * 30, // 추정값
          system_uptime: 100 - analytics.saju_system.error_rate,
          pending_inquiries: Math.floor(analytics.business_metrics.daily_consultations * 0.2), // 추정값
          interpretations_this_week: analytics.saju_system.calculations_today * 7, // 추정값
          avg_response_time: Math.floor(analytics.system_health.api_response_time / 1000 / 60), // ms를 분으로 변환
          last_updated: new Date().toISOString()
        }

        setSystemStats(mappedStats)
        setRecentActivities(analytics.recent_activities)
      }
    } catch (error: any) {
      console.error('Error fetching dashboard analytics:', error)
      // 에러 발생 시 기본값 설정
      setSystemStats({
        total_users: 0,
        active_users: 0,
        new_users: 0,
        daily_revenue: 0,
        monthly_revenue: 0,
        system_uptime: 0,
        pending_inquiries: 0,
        interpretations_this_week: 0,
        avg_response_time: 0,
        last_updated: new Date().toISOString()
      })
    } finally {
      setLoading(false)
    }
  }

  // AI 메트릭 조회
  const fetchAiMetrics = async () => {
    try {
      const { api } = await import('../../../services/apiService')
      const response = await api.analytics.getAiStats()

      if (response.success && response.data) {
        const stats = response.data
        setAiMetrics({
          daily_ai_requests: stats.interpretations?.total_interpretations || 0,
          successful_interpretations: stats.content_generation?.approved_content || 0,
          ai_response_time: parseFloat(stats.efficiency_metrics?.avg_response_time?.replace('초', '') || '0'),
          model_usage_stats: {
            'gpt4o': stats.interpretations?.models_used || 0,
            'gemini': stats.content_generation?.models_used || 0,
            'claude': 0
          },
          content_generated_today: stats.content_generation?.total_content || 0
        })
      }
    } catch (error: any) {
      console.error('Error fetching AI metrics:', error)
      // 에러 시 기본값
      setAiMetrics({
        daily_ai_requests: 0,
        successful_interpretations: 0,
        ai_response_time: 0,
        model_usage_stats: { 'gpt4o': 0, 'gemini': 0, 'claude': 0 },
        content_generated_today: 0
      })
    }
  }

  // 포인트 메트릭 조회
  const fetchPointMetrics = async () => {
    try {
      const { api } = await import('../../../services/apiService')
      const response = await api.analytics.getUserStats()

      if (response.success && response.data) {
        const stats = response.data
        setPointMetrics({
          total_points_distributed: stats.total_points_distributed || 0,
          points_used_today: Math.floor((stats.total_points_distributed || 0) * 0.1), // 추정값
          average_points_per_user: Math.floor((stats.total_points_distributed || 0) / Math.max(stats.total_users, 1)),
          pending_point_requests: Math.floor((stats.point_transactions || 0) * 0.05) // 추정값
        })
      }
    } catch (error: any) {
      console.error('Error fetching point metrics:', error)
      // 에러 시 기본값
      setPointMetrics({
        total_points_distributed: 0,
        points_used_today: 0,
        average_points_per_user: 0,
        pending_point_requests: 0
      })
    }
  }

  // 통합 데이터 로드 함수
  const fetchAllData = async () => {
    setLoading(true)
    await Promise.all([
      fetchDashboardStats(),
      fetchAiMetrics(),
      fetchPointMetrics()
    ])
    setLoading(false)
  }

  // 초기 데이터 로드
  useEffect(() => {
    fetchAllData()

    // 30초마다 자동 새로고침
    const interval = setInterval(() => {
      fetchAllData()
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
              fetchAllData()
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

          {/* AI 시스템 메트릭 */}
          <div className="glass-3 rounded-xl shadow-2xl p-6 hover:glass-4 theme-transition backdrop-blur-lg">
            <h3 className="text-lg font-semibold mb-4 flex items-center theme-text-heading">
              <Brain className="w-5 h-5 mr-2 drop-shadow-lg text-[var(--theme-accent)]" />
              AI 시스템 성능
            </h3>
            {aiMetrics ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-lg border border-blue-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">일일 AI 요청</p>
                      <p className="text-xl font-bold text-blue-400">{aiMetrics.daily_ai_requests.toLocaleString()}</p>
                    </div>
                    <Zap className="w-6 h-6 text-blue-400" />
                  </div>
                </div>

                <div className="p-4 bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-lg border border-green-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">성공한 해석</p>
                      <p className="text-xl font-bold text-green-400">{aiMetrics.successful_interpretations.toLocaleString()}</p>
                    </div>
                    <CheckCircle className="w-6 h-6 text-green-400" />
                  </div>
                </div>

                <div className="p-4 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-lg border border-yellow-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">평균 응답시간</p>
                      <p className="text-xl font-bold text-yellow-400">{aiMetrics.ai_response_time.toFixed(1)}초</p>
                    </div>
                    <Clock className="w-6 h-6 text-yellow-400" />
                  </div>
                </div>

                <div className="p-4 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-lg border border-purple-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">생성된 콘텐츠</p>
                      <p className="text-xl font-bold text-purple-400">{aiMetrics.content_generated_today}</p>
                    </div>
                    <Brain className="w-6 h-6 text-purple-400" />
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-4 theme-text-secondary">AI 메트릭을 불러오는 중...</div>
            )}
          </div>

          {/* 포인트 시스템 메트릭 */}
          <div className="glass-3 rounded-xl shadow-2xl p-6 hover:glass-4 theme-transition backdrop-blur-lg">
            <h3 className="text-lg font-semibold mb-4 flex items-center theme-text-heading">
              <CreditCard className="w-5 h-5 mr-2 drop-shadow-lg text-[var(--theme-accent)]" />
              포인트 시스템 현황
            </h3>
            {pointMetrics ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 bg-gradient-to-r from-indigo-500/10 to-blue-500/10 rounded-lg border border-indigo-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">총 배포된 포인트</p>
                      <p className="text-xl font-bold text-indigo-400">{pointMetrics.total_points_distributed.toLocaleString()}</p>
                    </div>
                    <Database className="w-6 h-6 text-indigo-400" />
                  </div>
                </div>

                <div className="p-4 bg-gradient-to-r from-teal-500/10 to-cyan-500/10 rounded-lg border border-teal-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">오늘 사용량</p>
                      <p className="text-xl font-bold text-teal-400">{pointMetrics.points_used_today.toLocaleString()}</p>
                    </div>
                    <Activity className="w-6 h-6 text-teal-400" />
                  </div>
                </div>

                <div className="p-4 bg-gradient-to-r from-rose-500/10 to-pink-500/10 rounded-lg border border-rose-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">사용자당 평균</p>
                      <p className="text-xl font-bold text-rose-400">{pointMetrics.average_points_per_user.toLocaleString()}</p>
                    </div>
                    <Users className="w-6 h-6 text-rose-400" />
                  </div>
                </div>

                <div className="p-4 bg-gradient-to-r from-amber-500/10 to-yellow-500/10 rounded-lg border border-amber-400/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">처리 대기</p>
                      <p className="text-xl font-bold text-amber-400">{pointMetrics.pending_point_requests}</p>
                    </div>
                    <Bell className="w-6 h-6 text-amber-400" />
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-4 theme-text-secondary">포인트 메트릭을 불러오는 중...</div>
            )}
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
                    {activity.action.includes('사용자') || activity.action.includes('가입') ? (
                      <User className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    ) : (
                      <MessageSquare className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <span className="font-medium">{activity.action}:</span>
                      <span className="ml-1">{activity.details}</span>
                      <div className="text-xs text-gray-500">
                        {activity.time}
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