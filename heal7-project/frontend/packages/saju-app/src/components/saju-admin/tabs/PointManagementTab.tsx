/**
 * 💎 포인트 탭 - 포인트/결제 시스템 관리
 * @author HEAL7 Admin Team
 * @version 3.0.0 - Real API Integration
 */

import React, { useState, useEffect } from 'react'
import { TrendingUp, CreditCard, Settings, Download, RefreshCw } from 'lucide-react'
import { useAuth } from '../../../hooks/useSajuAdmin'

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
  const { token } = useAuth()
  const [activeSection, setActiveSection] = useState('overview')
  const [overview, setOverview] = useState<PointOverview | null>(null)
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([])
  const [usagePatterns, setUsagePatterns] = useState<UsagePattern[]>([])
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [pagination, setPagination] = useState<PaginationInfo | null>(null)
  const [policies, setPolicies] = useState<any>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
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
    setError(null)
    try {
      if (!token) {
        setError('인증 토큰이 없습니다')
        return
      }

      // 실제 포인트 정책 API 호출
      const policiesResponse = await fetch('http://localhost:8002/api/points/policies', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (policiesResponse.ok) {
        const policiesData = await policiesResponse.json()
        
        // 정책 데이터를 카테고리별로 그룹화
        const groupedPolicies = policiesData.reduce((acc: any, policy: any) => {
          if (!acc[policy.policy_type]) {
            acc[policy.policy_type] = []
          }
          acc[policy.policy_type].push(policy)
          return acc
        }, {})
        
        setPolicies(groupedPolicies)
        
        // 실제 포인트 잔액 및 통계 데이터 가져오기
        const testUserId = '123e4567-e89b-12d3-a456-426614174000'
        
        // 잔액 조회
        const balanceResponse = await fetch(`http://localhost:8002/api/points/balance/${testUserId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (balanceResponse.ok) {
          const balanceData = await balanceResponse.json()
          
          // 거래 내역 통계 계산
          const historyResponse = await fetch(`http://localhost:8002/api/points/history/${testUserId}?page=1&page_size=1000`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })
          
          let totalIssued = 0
          let totalUsed = 0
          let totalRevenue = 0
          let totalTransactions = 0
          let paymentMethodStats: { [key: string]: { amount: number, count: number } } = {}
          let serviceUsageStats: { [key: string]: { points_used: number, count: number } } = {}
          
          if (historyResponse.ok) {
            const historyData = await historyResponse.json()
            totalTransactions = historyData.total_count
            
            historyData.transactions.forEach((tx: any) => {
              if (tx.transaction_type === 'charge') {
                totalIssued += Math.abs(tx.amount)
                if (tx.source === 'charge') {
                  totalRevenue += Math.abs(tx.amount)
                  const method = '카드결제'
                  if (!paymentMethodStats[method]) {
                    paymentMethodStats[method] = { amount: 0, count: 0 }
                  }
                  paymentMethodStats[method].amount += Math.abs(tx.amount)
                  paymentMethodStats[method].count += 1
                }
              } else if (tx.transaction_type === 'spend') {
                totalUsed += Math.abs(tx.amount)
                const service = tx.description || '사주 서비스'
                if (!serviceUsageStats[service]) {
                  serviceUsageStats[service] = { points_used: 0, count: 0 }
                }
                serviceUsageStats[service].points_used += Math.abs(tx.amount)
                serviceUsageStats[service].count += 1
              }
            })
          }
          
          const overview = {
            total_issued: totalIssued,
            total_used: totalUsed,
            total_revenue: totalRevenue,
            remaining_points: balanceData.total_balance || 0,
            total_transactions: totalTransactions
          }
          setOverview(overview)
          
          // 결제 방법 통계
          const paymentMethods = Object.entries(paymentMethodStats).map(([method, stats]) => ({
            method,
            amount: stats.amount,
            count: stats.count
          }))
          setPaymentMethods(paymentMethods.length > 0 ? paymentMethods : [
            { method: '데이터 없음', amount: 0, count: 0 }
          ])
          
          // 서비스 사용 패턴
          const usagePatterns = Object.entries(serviceUsageStats).map(([service, stats]) => ({
            service,
            points_used: stats.points_used,
            usage_count: stats.count
          }))
          setUsagePatterns(usagePatterns.length > 0 ? usagePatterns : [
            { service: '데이터 없음', points_used: 0, usage_count: 0 }
          ])
          
        } else {
          setError('포인트 잔액 정보를 불러올 수 없습니다')
        }
        
      } else {
        setError('포인트 정책 데이터를 불러올 수 없습니다')
      }
    } catch (error) {
      setError('네트워크 오류가 발생했습니다')
      console.error('Error fetching overview:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTransactions = async (page = 1, search = '') => {
    setLoading(true)
    setError(null)
    try {
      if (!token) {
        setError('인증 토큰이 없습니다')
        return
      }

      // 테스트 사용자 ID로 포인트 거래 내역 조회
      const testUserId = '123e4567-e89b-12d3-a456-426614174000'
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: '20'
      })
      
      const response = await fetch(`http://localhost:8002/api/points/history/${testUserId}?${params}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        
        // 백엔드 데이터를 프론트엔드 형식으로 변환
        const transformedTransactions = data.transactions.map((tx: any, index: number) => ({
          id: index + 1,
          user_name: '테스트 사용자',
          email: 'test@heal7.com',
          transaction_type: tx.transaction_type === 'charge' ? '충전' : 
                          tx.transaction_type === 'spend' ? '사용' : 
                          tx.transaction_type === 'earn' ? '적립' : '기타',
          amount: Math.abs(tx.amount),
          points: tx.amount,
          payment_method: tx.source === 'charge' ? '카드결제' : 
                        tx.source === 'purchase' ? '서비스이용' : '기타',
          status: '완료',
          description: tx.description || '포인트 거래',
          created_at: new Date(tx.created_at).toLocaleString('ko-KR')
        }))
        
        setTransactions(transformedTransactions)
        setPagination({
          current_page: data.page,
          per_page: data.page_size,
          total_count: data.total_count,
          total_pages: Math.ceil(data.total_count / data.page_size)
        })
        
      } else {
        setError('포인트 거래 내역을 불러올 수 없습니다')
      }
    } catch (error) {
      setError('네트워크 오류가 발생했습니다')
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPolicies = async () => {
    setLoading(true)
    setError(null)
    try {
      if (!token) {
        setError('인증 토큰이 없습니다')
        return
      }

      // 실제 포인트 정책 API 호출
      const response = await fetch('http://localhost:8002/api/points/policies', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const policiesData = await response.json()
        
        // 정책 데이터를 카테고리별로 그룹화
        const groupedPolicies = policiesData.reduce((acc: any, policy: any) => {
          if (!acc[policy.policy_type]) {
            acc[policy.policy_type] = []
          }
          acc[policy.policy_type].push(policy)
          return acc
        }, {})
        
        setPolicies(groupedPolicies)
      } else {
        setError('포인트 정책 데이터를 불러올 수 없습니다')
      }
    } catch (error) {
      setError('네트워크 오류가 발생했습니다')
      console.error('Error fetching policies:', error)
    } finally {
      setLoading(false)
    }
  }

  // 포인트 충전 함수 (TossPayments 테스트 연동)
  const handlePointCharge = async (amount: number) => {
    if (!token) {
      setError('인증 토큰이 없습니다')
      return
    }

    try {
      const testUserId = '123e4567-e89b-12d3-a456-426614174000'
      
      // 포인트 충전 API 호출 (테스트 결제)
      const chargeData = {
        user_id: testUserId,
        charge_amount: amount,
        payment_method: 'test_card',
        payment_id: `test-payment-${Date.now()}`,
        pg_name: 'tosspayments_test'
      }

      const response = await fetch('http://localhost:8002/api/points/charge', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(chargeData)
      })

      if (response.ok) {
        const result = await response.json()
        console.log('포인트 충전 성공:', result)
        
        // 충전 후 데이터 새로고침
        if (activeSection === 'overview') {
          fetchOverview()
        } else if (activeSection === 'transactions') {
          fetchTransactions(currentPage, searchTerm)
        }
        
        // 성공 메시지 표시
        setError(null)
        alert(`${amount}원 포인트 충전이 완료되었습니다! (보너스 포함: ${result.total_charged_points}P)`)
      } else {
        const errorData = await response.json()
        setError(`포인트 충전 실패: ${errorData.detail || '알 수 없는 오류'}`)
      }
    } catch (error) {
      setError('포인트 충전 중 네트워크 오류가 발생했습니다')
      console.error('Point charge error:', error)
    }
  }

  // 포인트 사용 함수 (테스트용)
  const handlePointUsage = async (amount: number, description: string) => {
    if (!token) {
      setError('인증 토큰이 없습니다')
      return
    }

    try {
      const testUserId = '123e4567-e89b-12d3-a456-426614174000'
      
      const usageData = {
        user_id: testUserId,
        amount: amount,
        service_type: 'saju_basic',
        description: description
      }

      const response = await fetch('http://localhost:8002/api/points/use', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(usageData)
      })

      if (response.ok) {
        const result = await response.json()
        console.log('포인트 사용 성공:', result)
        
        // 사용 후 데이터 새로고침
        if (activeSection === 'overview') {
          fetchOverview()
        } else if (activeSection === 'transactions') {
          fetchTransactions(currentPage, searchTerm)
        }
        
        setError(null)
        alert(`${amount}P 포인트 사용이 완료되었습니다!`)
      } else {
        const errorData = await response.json()
        setError(`포인트 사용 실패: ${errorData.detail || '알 수 없는 오류'}`)
      }
    } catch (error) {
      setError('포인트 사용 중 네트워크 오류가 발생했습니다')
      console.error('Point usage error:', error)
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
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-yellow-400 mb-2">⚠️ 포인트 관리 시스템</p>
              <p className="text-gray-400 text-sm">{error}</p>
              <p className="text-gray-500 text-xs mt-2">현재 Phase 1 (관리자 기본 기능)이 완료된 상태입니다</p>
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

              {/* 포인트 충전/사용 테스트 버튼 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 포인트 충전 섹션 */}
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">💳 포인트 충전 (TossPayments 테스트)</h4>
                  <p className="text-gray-400 text-sm mb-4">테스트 환경에서 포인트를 충전할 수 있습니다. 실제 결제는 발생하지 않습니다.</p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <button 
                      onClick={() => handlePointCharge(50000)}
                      className="px-4 py-3 bg-blue-600/20 border border-blue-400/30 rounded-lg text-blue-400 hover:bg-blue-600/30 transition-colors"
                    >
                      <div className="text-center">
                        <div className="text-lg font-bold">₩50,000</div>
                        <div className="text-xs">→ 53,000P</div>
                      </div>
                    </button>
                    <button 
                      onClick={() => handlePointCharge(100000)}
                      className="px-4 py-3 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30 transition-colors"
                    >
                      <div className="text-center">
                        <div className="text-lg font-bold">₩100,000</div>
                        <div className="text-xs">→ 106,000P</div>
                      </div>
                    </button>
                    <button 
                      onClick={() => handlePointCharge(200000)}
                      className="px-4 py-3 bg-purple-600/20 border border-purple-400/30 rounded-lg text-purple-400 hover:bg-purple-600/30 transition-colors"
                    >
                      <div className="text-center">
                        <div className="text-lg font-bold">₩200,000</div>
                        <div className="text-xs">→ 212,000P</div>
                      </div>
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-3">※ 6% 보너스 포인트 자동 적용</p>
                </div>

                {/* 포인트 사용 섹션 */}
                <div className="card-base p-6">
                  <h4 className="text-white font-semibold mb-4">💎 포인트 사용 테스트</h4>
                  <p className="text-gray-400 text-sm mb-4">사주 서비스 이용 시뮬레이션을 테스트할 수 있습니다.</p>
                  <div className="space-y-3">
                    <button 
                      onClick={() => handlePointUsage(3000, '기본 사주 해석 서비스')}
                      className="w-full px-4 py-3 bg-yellow-600/20 border border-yellow-400/30 rounded-lg text-yellow-400 hover:bg-yellow-600/30 transition-colors"
                    >
                      <div className="flex justify-between items-center">
                        <span>기본 사주 해석</span>
                        <span className="font-bold">3,000P</span>
                      </div>
                    </button>
                    <button 
                      onClick={() => handlePointUsage(5000, '프리미엄 사주 해석 서비스')}
                      className="w-full px-4 py-3 bg-orange-600/20 border border-orange-400/30 rounded-lg text-orange-400 hover:bg-orange-600/30 transition-colors"
                    >
                      <div className="flex justify-between items-center">
                        <span>프리미엄 사주 해석</span>
                        <span className="font-bold">5,000P</span>
                      </div>
                    </button>
                    <button 
                      onClick={() => handlePointUsage(8000, '궁합 분석 서비스')}
                      className="w-full px-4 py-3 bg-red-600/20 border border-red-400/30 rounded-lg text-red-400 hover:bg-red-600/30 transition-colors"
                    >
                      <div className="flex justify-between items-center">
                        <span>궁합 분석</span>
                        <span className="font-bold">8,000P</span>
                      </div>
                    </button>
                  </div>
                </div>
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
            ) : error ? (
              <div className="text-center py-12">
                <p className="text-yellow-400 mb-2">⚠️ 포인트 거래 시스템</p>
                <p className="text-gray-400 text-sm">{error}</p>
                <p className="text-gray-500 text-xs mt-2">Phase 2에서 구현 예정입니다</p>
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
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-yellow-400 mb-2">⚠️ 포인트 정책 시스템</p>
              <p className="text-gray-400 text-sm">{error}</p>
              <p className="text-gray-500 text-xs mt-2">Phase 2에서 구현 예정입니다</p>
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