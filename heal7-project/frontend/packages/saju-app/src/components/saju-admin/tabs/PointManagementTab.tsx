/**
 * 💎 포인트 탭 - 포인트/결제 시스템 관리
 * @author HEAL7 Admin Team
 * @version 3.0.0 - Real API Integration
 */

import React, { useState, useEffect } from 'react'
import { TrendingUp, CreditCard, Settings, Download, RefreshCw } from 'lucide-react'

interface PointOverview {
  total_issued: number
  total_used: number
  total_revenue: number
  remaining_points: number
  total_transactions: number
}

interface PaymentMethod {
  method: string
  amount: number
  count: number
}

interface UsagePattern {
  service: string
  points_used: number
  usage_count: number
}

interface Transaction {
  id: number
  user_name: string
  email: string
  transaction_type: string
  amount: number
  points: number
  payment_method: string
  status: string
  description: string
  created_at: string
}

interface PaginationInfo {
  current_page: number
  per_page: number
  total_count: number
  total_pages: number
}

export const PointManagementTab = () => {
  const [activeSection, setActiveSection] = useState('overview')
  const [overview, setOverview] = useState<PointOverview | null>(null)
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([])
  const [usagePatterns, setUsagePatterns] = useState<UsagePattern[]>([])
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [pagination, setPagination] = useState<PaginationInfo | null>(null)
  const [policies, setPolicies] = useState<any>({})
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  
  const sections = [
    { key: 'overview', label: '포인트 현황', icon: TrendingUp },
    { key: 'transactions', label: '거래 내역', icon: CreditCard },
    { key: 'policies', label: '정책 설정', icon: Settings }
  ]

  // API 호출 함수들
  const fetchOverview = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/saju/points/overview', {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setOverview(data.overview)
        setPaymentMethods(data.payment_methods)
        setUsagePatterns(data.usage_patterns)
      } else {
        console.error('Failed to fetch overview:', response.status)
      }
    } catch (error) {
      console.error('Error fetching overview:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTransactions = async (page = 1, search = '') => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: '20',
        search: search
      })
      
      const response = await fetch(`/api/admin/saju/points/transactions?${params}`, {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setTransactions(data.transactions)
        setPagination(data.pagination)
      } else {
        console.error('Failed to fetch transactions:', response.status)
      }
    } catch (error) {
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPolicies = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/saju/points/policies', {
        headers: {
          'Authorization': 'Bearer heal7-admin-2025',
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setPolicies(data.policies)
      } else {
        console.error('Failed to fetch policies:', response.status)
      }
    } catch (error) {
      console.error('Error fetching policies:', error)
    } finally {
      setLoading(false)
    }
  }

  // 초기 데이터 로드 및 섹션 변경 시 데이터 로드
  useEffect(() => {
    switch (activeSection) {
      case 'overview':
        fetchOverview()
        break
      case 'transactions':
        fetchTransactions(currentPage, searchTerm)
        break
      case 'policies':
        fetchPolicies()
        break
    }
  }, [activeSection, currentPage])

  // 검색 처리
  const handleSearch = (term: string) => {
    setSearchTerm(term)
    setCurrentPage(1)
    if (activeSection === 'transactions') {
      fetchTransactions(1, term)
    }
  }

  // 데이터 새로고침
  const handleRefresh = () => {
    switch (activeSection) {
      case 'overview':
        fetchOverview()
        break
      case 'transactions':
        fetchTransactions(currentPage, searchTerm)
        break
      case 'policies':
        fetchPolicies()
        break
    }
  }

  return (
    <div className="space-y-6">
      {/* 섹션 선택 */}
      <div className="card-base p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white text-lg font-semibold">포인트 & 결제 관리</h3>
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
          {sections.map(section => (
            <button
              key={section.key}
              onClick={() => setActiveSection(section.key)}
              className={`px-4 py-2 rounded-lg border flex items-center gap-2 ${
                activeSection === section.key
                  ? 'bg-purple-500/30 border-purple-400 text-purple-300'
                  : 'bg-white/5 border-gray-600/40 text-gray-200 hover:bg-gray-900/80'
              }`}
            >
              <section.icon className="w-4 h-4" />
              {section.label}
            </button>
          ))}
        </div>
      </div>

      {/* 포인트 현황 */}
      {activeSection === 'overview' && (
        <div className="space-y-6">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
              <span className="ml-2 text-gray-200">데이터를 불러오는 중...</span>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {overview && [
                  { title: '총 발행 포인트', value: `${overview.total_issued.toLocaleString()}P`, color: 'blue' },
                  { title: '사용된 포인트', value: `${overview.total_used.toLocaleString()}P`, color: 'green' },
                  { title: '잔여 포인트', value: `${overview.remaining_points.toLocaleString()}P`, color: 'purple' },
                  { title: '총 거래 수', value: `${overview.total_transactions.toLocaleString()}건`, color: 'yellow' }
                ].map((stat, idx) => (
                  <div key={idx} className="bg-gray-900/80 backdrop-blur-sm rounded-lg p-4 border border-gray-600/40">
                    <div className="mb-2">
                      <p className="text-gray-200 text-sm">{stat.title}</p>
                      <p className="text-white text-xl font-bold">{stat.value}</p>
                    </div>
                    <p className="text-xs text-gray-400">최근 30일 기준</p>
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 결제 수단별 통계 */}
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">결제 수단별 현황</h4>
                  <div className="space-y-3">
                    {paymentMethods.length > 0 ? paymentMethods.map((payment, idx) => {
                      const totalAmount = paymentMethods.reduce((sum, p) => sum + p.amount, 0)
                      const percentage = totalAmount > 0 ? Math.round((payment.amount / totalAmount) * 100) : 0
                      const colors = ['blue', 'green', 'yellow', 'purple', 'red']
                      const color = colors[idx % colors.length]
                      
                      return (
                        <div key={idx} className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex justify-between mb-1">
                              <span className="text-gray-200 text-sm">{payment.method}</span>
                              <span className="text-white text-sm">₩{payment.amount.toLocaleString()}</span>
                            </div>
                            <div className="w-full bg-gray-700 rounded-full h-2">
                              <div 
                                className={`bg-${color}-500 h-2 rounded-full`}
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                          </div>
                          <span className="text-gray-400 text-sm ml-4">{percentage}%</span>
                        </div>
                      )
                    }) : (
                      <p className="text-gray-400 text-center py-4">데이터가 없습니다</p>
                    )}
                  </div>
                </div>

                {/* 포인트 사용 패턴 */}
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">포인트 사용 패턴</h4>
                  <div className="space-y-3">
                    {usagePatterns.length > 0 ? usagePatterns.map((usage, idx) => {
                      const totalUsed = usagePatterns.reduce((sum, u) => sum + u.points_used, 0)
                      const percentage = totalUsed > 0 ? Math.round((usage.points_used / totalUsed) * 100) : 0
                      
                      return (
                        <div key={idx} className="flex items-center justify-between">
                          <span className="text-gray-200 text-sm">{usage.service}</span>
                          <div className="flex items-center gap-3">
                            <span className="text-white text-sm">{usage.points_used.toLocaleString()}P</span>
                            <span className="text-purple-400 text-xs">{percentage}%</span>
                          </div>
                        </div>
                      )
                    }) : (
                      <p className="text-gray-400 text-center py-4">데이터가 없습니다</p>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      )}
        </div>
      )}

      {/* 거래 내역 */}
      {activeSection === 'transactions' && (
        <div className="card-base">
          <div className="p-6 border-b border-gray-600/40">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold">거래 내역</h4>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="회원명 또는 거래설명 검색..."
                  value={searchTerm}
                  onChange={(e) => handleSearch(e.target.value)}
                  className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white placeholder-gray-400 text-sm"
                />
                <button className="px-3 py-1 bg-blue-600/20 border border-blue-400/30 rounded text-blue-400 text-sm">
                  <Download className="w-4 h-4 mr-1 inline" />
                  내보내기
                </button>
              </div>
            </div>
          </div>
          
          <div className="p-6">
            {loading ? (
              <div className="flex justify-center items-center py-12">
                <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
                <span className="ml-2 text-gray-200">거래 내역을 불러오는 중...</span>
              </div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-600/40">
                        <th className="text-left text-gray-200 py-3">회원</th>
                        <th className="text-left text-gray-200 py-3">거래 유형</th>
                        <th className="text-left text-gray-200 py-3">결제 금액</th>
                        <th className="text-left text-gray-200 py-3">포인트 변동</th>
                        <th className="text-left text-gray-200 py-3">결제 방법</th>
                        <th className="text-left text-gray-200 py-3">상태</th>
                        <th className="text-left text-gray-200 py-3">일시</th>
                      </tr>
                    </thead>
                    <tbody>
                      {transactions.length > 0 ? transactions.map(transaction => (
                        <tr key={transaction.id} className="border-b border-white/10 hover:bg-white/5">
                          <td className="py-3 text-white">
                            <div>
                              <div className="font-medium">{transaction.user_name}</div>
                              <div className="text-xs text-gray-400">{transaction.email}</div>
                            </div>
                          </td>
                          <td className="py-3 text-gray-200">
                            <span className={`px-2 py-1 rounded text-xs ${
                              transaction.transaction_type === 'purchase' ? 'bg-blue-500/20 text-blue-400' :
                              transaction.transaction_type === 'refund' ? 'bg-red-500/20 text-red-400' :
                              transaction.transaction_type === 'bonus' ? 'bg-green-500/20 text-green-400' :
                              'bg-yellow-500/20 text-yellow-400'
                            }`}>
                              {transaction.transaction_type === 'purchase' ? '구매' : 
                               transaction.transaction_type === 'refund' ? '환불' : 
                               transaction.transaction_type === 'bonus' ? '보너스' : '사용'}
                            </span>
                          </td>
                          <td className="py-3 text-white">
                            {transaction.amount > 0 ? `₩${transaction.amount.toLocaleString()}` : 
                             transaction.amount < 0 ? `-₩${Math.abs(transaction.amount).toLocaleString()}` : '-'}
                          </td>
                          <td className="py-3">
                            <span className={transaction.points >= 0 ? 'text-green-400' : 'text-red-400'}>
                              {transaction.points >= 0 ? '+' : ''}{transaction.points.toLocaleString()}P
                            </span>
                          </td>
                          <td className="py-3 text-gray-200">{transaction.payment_method}</td>
                          <td className="py-3">
                            <span className={`px-2 py-1 rounded text-xs ${
                              transaction.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                              transaction.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
                              'bg-red-500/20 text-red-400'
                            }`}>
                              {transaction.status === 'completed' ? '완료' : 
                               transaction.status === 'pending' ? '대기' : '실패'}
                            </span>
                          </td>
                          <td className="py-3 text-gray-200 text-sm">
                            {new Date(transaction.created_at).toLocaleString('ko-KR')}
                          </td>
                        </tr>
                      )) : (
                        <tr>
                          <td colSpan={7} className="py-12 text-center text-gray-400">
                            거래 내역이 없습니다
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
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
      )}

      {/* 정책 설정 */}
      {activeSection === 'policies' && (
        <div className="space-y-6">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <RefreshCw className="w-8 h-8 animate-spin text-purple-400" />
              <span className="ml-2 text-gray-200">정책 데이터를 불러오는 중...</span>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 포인트 적립률 정책 */}
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">포인트 적립률 정책</h4>
                  <div className="space-y-4">
                    {policies.earning_rate?.map((policy: any, idx: number) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                        <span className="text-gray-200">{policy.name}</span>
                        <div className="flex items-center gap-2">
                          <input 
                            type="number" 
                            defaultValue={policy.value} 
                            step="0.1"
                            className="w-16 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" 
                          />
                          <span className="text-gray-400">%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 결제 수수료 설정 */}
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">결제 수수료 설정</h4>
                  <div className="space-y-4">
                    {policies.fee_rate?.map((policy: any, idx: number) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                        <span className="text-gray-200">{policy.name}</span>
                        <div className="flex items-center gap-2">
                          <input 
                            type="number" 
                            defaultValue={policy.value} 
                            step={policy.name.includes('카드') ? '0.1' : '1'}
                            className="w-20 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" 
                          />
                          <span className="text-gray-400">
                            {policy.name.includes('카드') ? '%' : '원'}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* 기타 정책 */}
              {policies.validity_period && (
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">기타 정책</h4>
                  <div className="space-y-4">
                    {policies.validity_period.map((policy: any, idx: number) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                        <span className="text-gray-200">{policy.name}</span>
                        <div className="flex items-center gap-2">
                          <input 
                            type="number" 
                            defaultValue={policy.value} 
                            className="w-16 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" 
                          />
                          <span className="text-gray-400">개월</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex justify-end">
                <button 
                  onClick={() => {
                    // TODO: 정책 저장 API 호출
                    alert('정책 저장 기능은 곧 구현 예정입니다.')
                  }}
                  className="px-6 py-2 bg-purple-600/20 border border-purple-400/30 rounded-lg text-purple-400 hover:bg-purple-600/30"
                >
                  정책 저장
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default PointManagementTab;