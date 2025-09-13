/**
 * ⚙️ 시스템 탭 - 시스템 설정 및 1:1 문의 관리
 * @author HEAL7 Admin Team
 * @version 3.0.0 - Real API Integration
 */

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  AlertTriangle, Eye, MessageSquare, Database,
  Clock, Bell, RefreshCw, Send, X, Save
} from 'lucide-react'
import { useSajuSettings, useSaveSettings, useAuth } from '../../../hooks/useSajuAdmin'

interface InquiryOverview {
  status_stats: { status: string; count: number }[]
  category_stats: { category: string; count: number }[]
  priority_stats: { priority: string; count: number }[]
  avg_response_time: number
  total_pending: number
}

interface Inquiry {
  id: number
  subject: string
  content: string
  category: string
  status: string
  priority: string
  admin_reply: string | null
  user_name: string
  user_email: string
  created_at: string
  replied_at: string | null
}

interface PaginationInfo {
  current_page: number
  per_page: number
  total_count: number
  total_pages: number
}

export const SystemManagementTab = () => {
  const [activeTab, setActiveTab] = useState('inquiries')
  const [overview, setOverview] = useState<InquiryOverview | null>(null)
  const [inquiries, setInquiries] = useState<Inquiry[]>([])
  const [pagination, setPagination] = useState<PaginationInfo | null>(null)
  const [loading, setLoading] = useState(false)
  const [selectedInquiry, setSelectedInquiry] = useState<Inquiry | null>(null)
  const [replyText, setReplyText] = useState('')
  const [showReplyModal, setShowReplyModal] = useState(false)
  
  // Real API integration for settings
  const { token } = useAuth()
  const { data: settings, error: settingsError, isLoading: settingsLoading, mutate } = useSajuSettings(token)
  const { saveSettings, saving } = useSaveSettings(token, mutate)
  const [localSettings, setLocalSettings] = useState(settings)
  
  // 필터 상태
  const [statusFilter, setStatusFilter] = useState('all')
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  
  const tabs = [
    { key: 'inquiries', label: '1:1 문의 관리', count: overview?.total_pending || 0 },
    { key: 'system', label: '시스템 설정', count: null },
    { key: 'monitoring', label: '시스템 모니터링', count: null }
  ]

  // API 호출 함수들
  const fetchInquiryOverview = async () => {
    try {
      const response = await fetch('/api/admin/saju/inquiries/overview', {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setOverview(data)
      } else {
        console.error('Failed to fetch inquiry overview:', response.status)
      }
    } catch (error) {
      console.error('Error fetching inquiry overview:', error)
    }
  }

  const fetchInquiries = async (page = 1, status = 'all', category = 'all', priority = 'all', search = '') => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: '20',
        status,
        category,
        priority,
        search
      })
      
      const response = await fetch(`/api/admin/saju/inquiries?${params}`, {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setInquiries(data.inquiries)
        setPagination(data.pagination)
      } else {
        console.error('Failed to fetch inquiries:', response.status)
      }
    } catch (error) {
      console.error('Error fetching inquiries:', error)
    } finally {
      setLoading(false)
    }
  }

  const submitReply = async (inquiryId: number, replyContent: string) => {
    try {
      const response = await fetch(`/api/admin/saju/inquiries/${inquiryId}/reply`, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ admin_reply: replyContent })
      })
      
      if (response.ok) {
        // 성공 시 목록 새로고침
        await fetchInquiries(currentPage, statusFilter, categoryFilter, priorityFilter, searchTerm)
        await fetchInquiryOverview()
        setShowReplyModal(false)
        setSelectedInquiry(null)
        setReplyText('')
        return true
      } else {
        console.error('Failed to submit reply:', response.status)
        return false
      }
    } catch (error) {
      console.error('Error submitting reply:', error)
      return false
    }
  }

  // 초기 데이터 로드
  useEffect(() => {
    if (activeTab === 'inquiries') {
      fetchInquiryOverview()
      fetchInquiries(currentPage, statusFilter, categoryFilter, priorityFilter, searchTerm)
    }
  }, [activeTab, currentPage, statusFilter, categoryFilter, priorityFilter])

  // Update local settings when settings change
  useEffect(() => {
    if (settings) {
      setLocalSettings(settings)
    }
  }, [settings])

  // 검색 처리
  const handleSearch = (term: string) => {
    setSearchTerm(term)
    setCurrentPage(1)
    fetchInquiries(1, statusFilter, categoryFilter, priorityFilter, term)
  }

  // 답변 모달 열기
  const openReplyModal = (inquiry: Inquiry) => {
    setSelectedInquiry(inquiry)
    setReplyText(inquiry.admin_reply || '')
    setShowReplyModal(true)
  }

  // 데이터 새로고침
  const handleRefresh = () => {
    if (activeTab === 'inquiries') {
      fetchInquiryOverview()
      fetchInquiries(currentPage, statusFilter, categoryFilter, priorityFilter, searchTerm)
    } else if (activeTab === 'system') {
      mutate() // Refresh settings
    }
  }

  // 설정 저장
  const handleSaveSettings = async () => {
    if (localSettings) {
      const success = await saveSettings(localSettings)
      if (success) {
        alert('설정이 성공적으로 저장되었습니다.')
      } else {
        alert('설정 저장에 실패했습니다. 다시 시도해주세요.')
      }
    }
  }

  // 설정 값 업데이트 헬퍼
  const updateSettingValue = (category: string, key: string, value: any) => {
    if (!localSettings) return
    
    setLocalSettings({
      ...localSettings,
      [category]: {
        ...localSettings[category as keyof typeof localSettings],
        [key]: value
      }
    })
  }

  return (
    <div className="space-y-6">
      {/* 탭 선택 */}
      <div className="card-base p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white text-lg font-semibold">시스템 관리</h3>
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="px-3 py-1 bg-blue-600/20 border border-blue-400/30 rounded text-blue-400 text-sm hover:bg-blue-600/30 disabled:opacity-50 flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            새로고침
          </button>
        </div>
        <div className="flex gap-2">
          {tabs.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2 rounded-lg border flex items-center gap-2 ${
                activeTab === tab.key
                  ? 'bg-purple-500/30 border-purple-400 text-purple-300'
                  : 'bg-white/5 border-gray-600/40 text-gray-200 hover:bg-gray-900/80'
              }`}
            >
              {tab.label}
              {tab.count && tab.count > 0 && (
                <span className="px-2 py-1 bg-red-500/20 text-red-400 text-xs rounded-full">
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* 1:1 문의 관리 */}
      {activeTab === 'inquiries' && (
        <div className="space-y-6">
          {loading && !overview ? (
            <div className="flex justify-center items-center py-12">
              <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
              <span className="ml-2 text-gray-200">데이터를 불러오는 중...</span>
            </div>
          ) : (
            <>
              {/* 문의 현황 통계 */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {overview && [
                  { 
                    title: '미답변 문의', 
                    value: overview.total_pending.toString(), 
                    color: 'red', 
                    urgent: overview.total_pending > 0 
                  },
                  { 
                    title: '답변 완료', 
                    value: overview.status_stats.find(s => s.status === 'replied')?.count.toString() || '0', 
                    color: 'green', 
                    urgent: false 
                  },
                  { 
                    title: '평균 응답시간', 
                    value: `${overview.avg_response_time}시간`, 
                    color: 'blue', 
                    urgent: false 
                  },
                  { 
                    title: '전체 문의', 
                    value: overview.status_stats.reduce((sum, s) => sum + s.count, 0).toString(), 
                    color: 'yellow', 
                    urgent: false 
                  }
                ].map((stat, idx) => (
                  <div key={idx} className={`bg-gray-900/80 backdrop-blur-sm rounded-lg p-4 border ${
                    stat.urgent ? 'border-red-400/50' : 'border-gray-600/40'
                  }`}>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-200 text-sm">{stat.title}</p>
                        <p className="text-white text-xl font-bold">{stat.value}</p>
                      </div>
                      {stat.urgent && (
                        <AlertTriangle className="w-6 h-6 text-red-400" />
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* 문의 목록 */}
              <div className="card-base">
                <div className="p-6 border-b border-gray-600/40">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-white font-semibold">1:1 문의 목록</h4>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        placeholder="제목, 내용, 작성자 검색..."
                        value={searchTerm}
                        onChange={(e) => handleSearch(e.target.value)}
                        className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white placeholder-gray-400 text-sm"
                      />
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <select 
                      value={statusFilter} 
                      onChange={(e) => setStatusFilter(e.target.value)}
                      className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm"
                    >
                      <option value="all">전체 상태</option>
                      <option value="pending">미답변</option>
                      <option value="replied">답변완료</option>
                      <option value="closed">종료</option>
                    </select>
                    <select 
                      value={categoryFilter} 
                      onChange={(e) => setCategoryFilter(e.target.value)}
                      className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm"
                    >
                      <option value="all">전체 분류</option>
                      <option value="서비스문의">서비스문의</option>
                      <option value="결제문의">결제문의</option>
                      <option value="계정문의">계정문의</option>
                      <option value="일반문의">일반문의</option>
                    </select>
                    <select 
                      value={priorityFilter} 
                      onChange={(e) => setPriorityFilter(e.target.value)}
                      className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm"
                    >
                      <option value="all">전체 우선순위</option>
                      <option value="urgent">긴급</option>
                      <option value="high">높음</option>
                      <option value="normal">보통</option>
                      <option value="low">낮음</option>
                    </select>
                  </div>
                </div>
                
                <div className="p-6">
                  {loading ? (
                    <div className="flex justify-center items-center py-12">
                      <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
                      <span className="ml-2 text-gray-200">문의 목록을 불러오는 중...</span>
                    </div>
                  ) : (
                    <>
                      <div className="space-y-4">
                        {inquiries.length > 0 ? inquiries.map(inquiry => (
                          <motion.div
                            key={inquiry.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="p-4 bg-white/5 rounded-lg border border-white/10 hover:bg-gray-900/80 transition-all"
                          >
                            <div className="flex items-start justify-between mb-3">
                              <div className="flex-1">
                                <div className="flex items-center gap-3 mb-1">
                                  <h5 className="text-white font-semibold">{inquiry.subject}</h5>
                                  <span className={`px-2 py-1 rounded text-xs ${
                                    inquiry.status === 'pending' ? 'bg-red-500/20 text-red-400' : 
                                    inquiry.status === 'replied' ? 'bg-green-500/20 text-green-400' :
                                    'bg-gray-500/20 text-gray-400'
                                  }`}>
                                    {inquiry.status === 'pending' ? '미답변' : 
                                     inquiry.status === 'replied' ? '답변완료' : '종료'}
                                  </span>
                                  <span className={`px-2 py-1 rounded text-xs ${
                                    inquiry.priority === 'urgent' ? 'bg-red-500/20 text-red-400' :
                                    inquiry.priority === 'high' ? 'bg-orange-500/20 text-orange-400' :
                                    inquiry.priority === 'normal' ? 'bg-blue-500/20 text-blue-400' :
                                    'bg-gray-500/20 text-gray-400'
                                  }`}>
                                    {inquiry.priority === 'urgent' ? '긴급' :
                                     inquiry.priority === 'high' ? '높음' :
                                     inquiry.priority === 'normal' ? '보통' : '낮음'}
                                  </span>
                                </div>
                                <div className="flex items-center gap-4 text-sm text-gray-400 mb-2">
                                  <span>작성자: {inquiry.user_name}</span>
                                  <span>분류: {inquiry.category}</span>
                                  <span>작성일: {new Date(inquiry.created_at).toLocaleDateString('ko-KR')}</span>
                                  {inquiry.replied_at && (
                                    <span>답변일: {new Date(inquiry.replied_at).toLocaleDateString('ko-KR')}</span>
                                  )}
                                </div>
                                <p className="text-gray-200 text-sm mb-2">{inquiry.content}</p>
                                {inquiry.admin_reply && (
                                  <div className="mt-2 p-3 bg-blue-500/10 border border-blue-400/20 rounded">
                                    <p className="text-blue-400 text-sm font-medium mb-1">관리자 답변:</p>
                                    <p className="text-gray-200 text-sm">{inquiry.admin_reply}</p>
                                  </div>
                                )}
                              </div>
                              <div className="flex gap-1 ml-4">
                                <button 
                                  onClick={() => openReplyModal(inquiry)}
                                  className="text-green-400 hover:text-green-300 p-2"
                                  title={inquiry.admin_reply ? "답변 수정" : "답변 작성"}
                                >
                                  <MessageSquare className="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                          </motion.div>
                        )) : (
                          <div className="text-center py-12">
                            <p className="text-gray-400">문의가 없습니다.</p>
                          </div>
                        )}
                      </div>

                      {/* 페이징 */}
                      {pagination && pagination.total_pages > 1 && (
                        <div className="mt-6 flex items-center justify-between">
                          <div className="text-sm text-gray-400">
                            총 {pagination.total_count.toLocaleString()}건 중 {((pagination.current_page - 1) * pagination.per_page + 1).toLocaleString()}-{Math.min(pagination.current_page * pagination.per_page, pagination.total_count).toLocaleString()}건
                          </div>
                          <div className="flex gap-2">
                            <button
                              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                              disabled={currentPage === 1}
                              className="px-3 py-1 bg-white/10 border border-white/20 rounded text-white text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              이전
                            </button>
                            <span className="px-3 py-1 text-gray-200 text-sm">
                              {currentPage} / {pagination.total_pages}
                            </span>
                            <button
                              onClick={() => setCurrentPage(Math.min(pagination.total_pages, currentPage + 1))}
                              disabled={currentPage === pagination.total_pages}
                              className="px-3 py-1 bg-white/10 border border-white/20 rounded text-white text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              다음
                            </button>
                          </div>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* 시스템 설정 */}
      {activeTab === 'system' && (
        <div className="space-y-6">
          {settingsLoading ? (
            <div className="flex justify-center items-center py-12">
              <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
              <span className="ml-2 text-gray-200">설정을 불러오는 중...</span>
            </div>
          ) : settingsError ? (
            <div className="text-center py-12">
              <p className="text-red-400 mb-2">설정 로드 실패</p>
              <p className="text-gray-400 text-sm">{settingsError}</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 사주 엔진 설정 */}
              <div className="card-base p-6">
                <h4 className="text-white font-semibold mb-4">사주 엔진 설정</h4>
                {localSettings && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-200">로직 타입</span>
                      <select 
                        value={localSettings.logic_settings?.logic_type || 'hybrid'}
                        onChange={(e) => updateSettingValue('logic_settings', 'logic_type', e.target.value)}
                        className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm"
                      >
                        <option value="hybrid">하이브리드</option>
                        <option value="traditional">전통 방식</option>
                        <option value="modern">현대 방식</option>
                      </select>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-200">치유마녀 만세력 DB 연동</span>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input 
                          type="checkbox" 
                          checked={localSettings.logic_settings?.use_healwitch_perpetual_calendar || true}
                          onChange={(e) => updateSettingValue('logic_settings', 'use_healwitch_perpetual_calendar', e.target.checked)}
                          className="sr-only peer" 
                        />
                        <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                      </label>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-200 text-sm">📊 73,442개 레코드 (1900-2100)</span>
                      <span className="text-green-400 text-xs">✅ 활성화됨</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-200">시두법 사용</span>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input 
                          type="checkbox" 
                          checked={localSettings.time_settings?.use_sidubup || false}
                          onChange={(e) => updateSettingValue('time_settings', 'use_sidubup', e.target.checked)}
                          className="sr-only peer" 
                        />
                        <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                      </label>
                    </div>
                  </div>
                )}
              </div>

            {/* 지리적 설정 */}
            <div className="card-base p-6">
              <h4 className="text-white font-semibold mb-4">지리적 설정</h4>
              {localSettings && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-200">기본 국가</span>
                    <select 
                      value={localSettings.geographic_settings?.default_country || 'KR'}
                      onChange={(e) => updateSettingValue('geographic_settings', 'default_country', e.target.value)}
                      className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm"
                    >
                      <option value="KR">한국</option>
                      <option value="US">미국</option>
                      <option value="JP">일본</option>
                      <option value="CN">중국</option>
                    </select>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-200">경도 오프셋</span>
                    <div className="flex items-center gap-2">
                      <input 
                        type="number" 
                        value={localSettings.geographic_settings?.longitude_offset || 127.0}
                        onChange={(e) => updateSettingValue('geographic_settings', 'longitude_offset', parseFloat(e.target.value))}
                        className="w-20 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" 
                      />
                      <span className="text-gray-400">°E</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-200">시간대 시스템</span>
                    <select 
                      value={localSettings.time_settings?.timezone_system || 'apparent_solar'}
                      onChange={(e) => updateSettingValue('time_settings', 'timezone_system', e.target.value)}
                      className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm"
                    >
                      <option value="apparent_solar">진태양시</option>
                      <option value="mean_solar">평균태양시</option>
                      <option value="standard">표준시</option>
                    </select>
                  </div>
                </div>
              )}
            </div>

            {/* 운영 정책 */}
            <div className="card-base p-6">
              <h4 className="text-white font-semibold mb-4">운영 정책</h4>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">최대 동시 접속자</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="1000" className="w-20 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">명</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">세션 유지 시간</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="30" className="w-16 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">분</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">API 요청 제한</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="100" className="w-16 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">req/min</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 백업 설정 */}
            <div className="card-base p-6">
              <h4 className="text-white font-semibold mb-4">백업 & 보안</h4>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">자동 백업</span>
                  <select className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm">
                    <option value="daily">매일</option>
                    <option value="weekly">매주</option>
                    <option value="monthly">매월</option>
                  </select>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">백업 보관 기간</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="30" className="w-16 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">일</span>
                  </div>
                </div>
                <button className="w-full px-4 py-2 bg-blue-600/20 border border-blue-400/30 rounded-lg text-blue-400 hover:bg-blue-600/30">
                  <Database className="w-4 h-4 mr-2 inline" />
                  수동 백업 실행
                </button>
              </div>
            </div>
          </div>
          )}
          
          <div className="flex justify-end">
              <button 
                onClick={handleSaveSettings}
                disabled={saving || !localSettings}
                className="px-6 py-2 bg-purple-600/20 border border-purple-400/30 rounded-lg text-purple-400 hover:bg-purple-600/30 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {saving ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    저장 중...
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4" />
                    설정 저장
                  </>
                )}
              </button>
            </div>
        </div>
      )}

      {/* 시스템 모니터링 */}
      {activeTab === 'monitoring' && (
        <div className="space-y-6">
          {/* 실시간 상태 */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { title: 'CPU 사용률', value: '23%', status: 'normal', color: 'green' },
              { title: '메모리 사용률', value: '67%', status: 'warning', color: 'yellow' },
              { title: '디스크 사용률', value: '45%', status: 'normal', color: 'green' },
              { title: '네트워크', value: '156Mbps', status: 'normal', color: 'green' }
            ].map((metric, idx) => (
              <div key={idx} className="bg-gray-900/80 backdrop-blur-sm rounded-lg p-4 border border-gray-600/40">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-200 text-sm">{metric.title}</p>
                    <p className="text-white text-xl font-bold">{metric.value}</p>
                  </div>
                  <div className={`w-3 h-3 rounded-full bg-${metric.color}-400`}></div>
                </div>
              </div>
            ))}
          </div>

          {/* 서비스 상태 */}
          <div className="card-base p-6">
            <h4 className="text-white font-semibold mb-4">서비스 상태</h4>
            <div className="space-y-3">
              {[
                { service: '사주 엔진', status: 'running', uptime: '15일 3시간', load: '23%' },
                { service: '결제 시스템', status: 'running', uptime: '30일 12시간', load: '12%' },
                { service: '데이터베이스', status: 'running', uptime: '45일 8시간', load: '67%' },
                { service: '캐시 서버', status: 'running', uptime: '25일 16시간', load: '34%' }
              ].map((service, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-green-400"></div>
                    <span className="text-white">{service.service}</span>
                  </div>
                  <div className="flex items-center gap-6 text-sm text-gray-400">
                    <span>가동시간: {service.uptime}</span>
                    <span>부하: {service.load}</span>
                    <span className="text-green-400">정상</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 로그 및 경고 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card-base p-6">
              <h4 className="text-white font-semibold mb-4">최근 로그</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <Clock className="w-3 h-3 text-gray-400" />
                  <span className="text-gray-400">15:30</span>
                  <span className="text-green-400">INFO</span>
                  <span className="text-gray-200">사용자 로그인: 김○○</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-3 h-3 text-gray-400" />
                  <span className="text-gray-400">15:28</span>
                  <span className="text-blue-400">INFO</span>
                  <span className="text-gray-200">사주 분석 완료: ID#12345</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-3 h-3 text-gray-400" />
                  <span className="text-gray-400">15:25</span>
                  <span className="text-yellow-400">WARN</span>
                  <span className="text-gray-200">메모리 사용률 증가: 67%</span>
                </div>
              </div>
            </div>

            <div className="card-base p-6">
              <h4 className="text-white font-semibold mb-4">시스템 경고</h4>
              <div className="space-y-3">
                <div className="flex items-start gap-2 p-3 bg-yellow-500/10 border border-yellow-400/20 rounded">
                  <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5" />
                  <div>
                    <p className="text-yellow-400 text-sm font-medium">메모리 사용률 주의</p>
                    <p className="text-gray-200 text-xs">현재 67% 사용 중, 모니터링 필요</p>
                  </div>
                </div>
                <div className="flex items-start gap-2 p-3 bg-blue-500/10 border border-blue-400/20 rounded">
                  <Bell className="w-4 h-4 text-blue-400 mt-0.5" />
                  <div>
                    <p className="text-blue-400 text-sm font-medium">백업 완료</p>
                    <p className="text-gray-200 text-xs">일일 백업이 성공적으로 완료됨</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 답변 작성 모달 */}
      {showReplyModal && selectedInquiry && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-900/95 backdrop-blur-md rounded-lg border border-gray-600/40 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-600/40">
              <div className="flex items-center justify-between">
                <h3 className="text-white text-lg font-semibold">
                  {selectedInquiry.admin_reply ? '답변 수정' : '답변 작성'}
                </h3>
                <button
                  onClick={() => {
                    setShowReplyModal(false)
                    setSelectedInquiry(null)
                    setReplyText('')
                  }}
                  className="text-gray-400 hover:text-gray-200"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            <div className="p-6">
              {/* 문의 내용 */}
              <div className="mb-6 p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="flex items-center gap-3 mb-2">
                  <h4 className="text-white font-semibold">{selectedInquiry.subject}</h4>
                  <span className={`px-2 py-1 rounded text-xs ${
                    selectedInquiry.priority === 'urgent' ? 'bg-red-500/20 text-red-400' :
                    selectedInquiry.priority === 'high' ? 'bg-orange-500/20 text-orange-400' :
                    selectedInquiry.priority === 'normal' ? 'bg-blue-500/20 text-blue-400' :
                    'bg-gray-500/20 text-gray-400'
                  }`}>
                    {selectedInquiry.priority === 'urgent' ? '긴급' :
                     selectedInquiry.priority === 'high' ? '높음' :
                     selectedInquiry.priority === 'normal' ? '보통' : '낮음'}
                  </span>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-400 mb-3">
                  <span>작성자: {selectedInquiry.user_name} ({selectedInquiry.user_email})</span>
                  <span>분류: {selectedInquiry.category}</span>
                  <span>작성일: {new Date(selectedInquiry.created_at).toLocaleDateString('ko-KR')}</span>
                </div>
                <p className="text-gray-200 text-sm">{selectedInquiry.content}</p>
              </div>

              {/* 답변 작성 */}
              <div className="space-y-4">
                <label className="text-white text-sm font-medium">답변 내용</label>
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  placeholder="고객에게 전달할 답변을 입력해주세요..."
                  className="w-full h-32 px-3 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white placeholder-gray-400 text-sm resize-none"
                />
              </div>
            </div>

            <div className="p-6 border-t border-gray-600/40 flex justify-end gap-2">
              <button
                onClick={() => {
                  setShowReplyModal(false)
                  setSelectedInquiry(null)
                  setReplyText('')
                }}
                className="px-4 py-2 bg-white/10 border border-white/20 rounded text-gray-200 hover:bg-white/20"
              >
                취소
              </button>
              <button
                onClick={async () => {
                  if (replyText.trim()) {
                    const success = await submitReply(selectedInquiry.id, replyText.trim())
                    if (success) {
                      alert('답변이 성공적으로 저장되었습니다.')
                    } else {
                      alert('답변 저장에 실패했습니다. 다시 시도해주세요.')
                    }
                  } else {
                    alert('답변 내용을 입력해주세요.')
                  }
                }}
                className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded text-green-400 hover:bg-green-600/30 flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                {selectedInquiry.admin_reply ? '답변 수정' : '답변 전송'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SystemManagementTab;