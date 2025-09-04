/**
 * 💎 포인트 탭 - 포인트/결제 시스템 관리
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState } from 'react'
import { TrendingUp, CreditCard, Settings, Download } from 'lucide-react'

export const PointManagementTab = () => {
  const [activeSection, setActiveSection] = useState('overview')
  
  const sections = [
    { key: 'overview', label: '포인트 현황', icon: TrendingUp },
    { key: 'transactions', label: '거래 내역', icon: CreditCard },
    { key: 'policies', label: '정책 설정', icon: Settings }
  ]

  const mockTransactions = [
    { id: 1, user: '김○○', type: 'purchase', amount: 10000, points: 10000, method: '카드', status: 'completed', date: '2025-09-03 14:30' },
    { id: 2, user: '이○○', type: 'refund', amount: -5000, points: -5000, method: '환불', status: 'completed', date: '2025-09-03 13:15' },
    { id: 3, user: '박○○', type: 'bonus', amount: 0, points: 2000, method: '보너스', status: 'completed', date: '2025-09-03 12:00' }
  ]

  return (
    <div className="space-y-6">
      {/* 섹션 선택 */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
        <h3 className="text-white text-lg font-semibold mb-4">포인트 & 결제 관리</h3>
        <div className="flex gap-2">
          {sections.map(section => (
            <button
              key={section.key}
              onClick={() => setActiveSection(section.key)}
              className={`px-4 py-2 rounded-lg border flex items-center gap-2 ${
                activeSection === section.key
                  ? 'bg-purple-500/30 border-purple-400 text-purple-300'
                  : 'bg-white/5 border-white/20 text-gray-300 hover:bg-white/10'
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
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { title: '총 발행 포인트', value: '₩124,560,000', color: 'blue', change: '+15.2%' },
              { title: '사용된 포인트', value: '₩98,340,000', color: 'green', change: '+12.8%' },
              { title: '잔여 포인트', value: '₩26,220,000', color: 'purple', change: '+18.9%' },
              { title: '일일 거래액', value: '₩2,450,000', color: 'yellow', change: '+5.2%' }
            ].map((stat, idx) => (
              <div key={idx} className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                <div className="mb-2">
                  <p className="text-gray-300 text-sm">{stat.title}</p>
                  <p className="text-white text-xl font-bold">{stat.value}</p>
                </div>
                <p className={`text-xs text-${stat.color}-400`}>전월 대비 {stat.change}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 결제 수단별 통계 */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <h4 className="text-white font-semibold mb-4">결제 수단별 현황</h4>
              <div className="space-y-3">
                {[
                  { method: '카드 결제', amount: '₩15,600,000', percentage: 68, color: 'blue' },
                  { method: '계좌이체', amount: '₩5,200,000', percentage: 23, color: 'green' },
                  { method: '무통장입금', amount: '₩2,100,000', percentage: 9, color: 'yellow' }
                ].map((payment, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-gray-300 text-sm">{payment.method}</span>
                        <span className="text-white text-sm">{payment.amount}</span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div 
                          className={`bg-${payment.color}-500 h-2 rounded-full`}
                          style={{ width: `${payment.percentage}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-gray-400 text-sm ml-4">{payment.percentage}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* 포인트 사용 패턴 */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <h4 className="text-white font-semibold mb-4">포인트 사용 패턴</h4>
              <div className="space-y-3">
                {[
                  { service: '사주 풀이', usage: '₩8,900,000', percentage: 45 },
                  { service: '궁합 분석', usage: '₩5,600,000', percentage: 28 },
                  { service: '꿈 해몽', usage: '₩3,200,000', percentage: 16 },
                  { service: '기타 서비스', usage: '₩2,200,000', percentage: 11 }
                ].map((usage, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <span className="text-gray-300 text-sm">{usage.service}</span>
                    <div className="flex items-center gap-3">
                      <span className="text-white text-sm">{usage.usage}</span>
                      <span className="text-purple-400 text-xs">{usage.percentage}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 거래 내역 */}
      {activeSection === 'transactions' && (
        <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20">
          <div className="p-6 border-b border-white/20">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold">거래 내역</h4>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="회원명 또는 거래ID 검색..."
                  className="px-3 py-1 bg-white/10 border border-white/20 rounded text-white placeholder-gray-400 text-sm"
                />
                <button className="px-3 py-1 bg-blue-600/20 border border-blue-400/30 rounded text-blue-400 text-sm">
                  <Download className="w-4 h-4 mr-1 inline" />
                  내보내기
                </button>
              </div>
            </div>
          </div>
          
          <div className="p-6">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/20">
                    <th className="text-left text-gray-300 py-3">회원</th>
                    <th className="text-left text-gray-300 py-3">거래 유형</th>
                    <th className="text-left text-gray-300 py-3">결제 금액</th>
                    <th className="text-left text-gray-300 py-3">포인트 변동</th>
                    <th className="text-left text-gray-300 py-3">결제 방법</th>
                    <th className="text-left text-gray-300 py-3">상태</th>
                    <th className="text-left text-gray-300 py-3">일시</th>
                  </tr>
                </thead>
                <tbody>
                  {mockTransactions.map(transaction => (
                    <tr key={transaction.id} className="border-b border-white/10 hover:bg-white/5">
                      <td className="py-3 text-white">{transaction.user}</td>
                      <td className="py-3 text-gray-300">
                        <span className={`px-2 py-1 rounded text-xs ${
                          transaction.type === 'purchase' ? 'bg-blue-500/20 text-blue-400' :
                          transaction.type === 'refund' ? 'bg-red-500/20 text-red-400' :
                          'bg-green-500/20 text-green-400'
                        }`}>
                          {transaction.type === 'purchase' ? '구매' : transaction.type === 'refund' ? '환불' : '보너스'}
                        </span>
                      </td>
                      <td className="py-3 text-white">{transaction.amount > 0 ? `₩${transaction.amount.toLocaleString()}` : transaction.amount < 0 ? `-₩${Math.abs(transaction.amount).toLocaleString()}` : '-'}</td>
                      <td className="py-3">
                        <span className={transaction.points >= 0 ? 'text-green-400' : 'text-red-400'}>
                          {transaction.points >= 0 ? '+' : ''}{transaction.points.toLocaleString()}P
                        </span>
                      </td>
                      <td className="py-3 text-gray-300">{transaction.method}</td>
                      <td className="py-3">
                        <span className="px-2 py-1 rounded text-xs bg-green-500/20 text-green-400">완료</span>
                      </td>
                      <td className="py-3 text-gray-300 text-sm">{transaction.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 정책 설정 */}
      {activeSection === 'policies' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 포인트 정책 */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <h4 className="text-white font-semibold mb-4">포인트 적립/사용 정책</h4>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <span className="text-gray-300">기본 적립률</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="1" className="w-16 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <span className="text-gray-300">VIP 적립률</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="3" className="w-16 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <span className="text-gray-300">포인트 유효기간</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="12" className="w-16 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">개월</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 결제 수수료 설정 */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <h4 className="text-white font-semibold mb-4">결제 수수료 설정</h4>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <span className="text-gray-300">카드 결제</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="2.9" step="0.1" className="w-20 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <span className="text-gray-300">계좌이체</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="500" className="w-20 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">원</span>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/5 rounded border border-white/10">
                  <span className="text-gray-300">무통장입금</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="0" className="w-20 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">원</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button className="px-6 py-2 bg-purple-600/20 border border-purple-400/30 rounded-lg text-purple-400 hover:bg-purple-600/30">
              정책 저장
            </button>
          </div>
        </div>
      )}
    </div>
  )
}