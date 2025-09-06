/**
 * 👤 사용자관리 탭 - 회원 및 관리자 관리
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState } from 'react'
import { Search, Download, Eye, Mail, Edit } from 'lucide-react'

export const UserManagementTab = () => {
  const [userFilter, setUserFilter] = useState('all')
  const [selectedUsers, setSelectedUsers] = useState<number[]>([])
  
  const mockUsers = [
    { id: 1, name: '김○○', email: 'kim***@gmail.com', grade: 'VIP', points: 15000, joinDate: '2025-08-15', status: 'active', lastLogin: '2시간 전' },
    { id: 2, name: '이○○', email: 'lee***@naver.com', grade: '일반', points: 3200, joinDate: '2025-07-22', status: 'active', lastLogin: '1일 전' },
    { id: 3, name: '박○○', email: 'park***@daum.net', grade: '골드', points: 8500, joinDate: '2025-06-10', status: 'inactive', lastLogin: '7일 전' }
  ]

  const filters = [
    { key: 'all', label: '전체 회원', count: 15847 },
    { key: 'vip', label: 'VIP 회원', count: 234 },
    { key: 'gold', label: '골드 회원', count: 1456 },
    { key: 'regular', label: '일반 회원', count: 14157 },
    { key: 'inactive', label: '휴면 계정', count: 892 }
  ]

  return (
    <div className="space-y-6">
      {/* 회원 통계 및 필터 */}
      <div className="card-cosmic p-6">
        <h3 className="text-white text-lg font-semibold mb-4">회원 관리</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          {filters.map(filter => (
            <button
              key={filter.key}
              onClick={() => setUserFilter(filter.key)}
              className={`p-4 rounded-lg border transition-all text-left ${
                userFilter === filter.key
                  ? 'bg-purple-500/30 border-purple-400'
                  : 'bg-white/5 border-gray-600/40 hover:bg-gray-900/80'
              }`}
            >
              <div className="text-white font-semibold">{filter.count.toLocaleString()}</div>
              <div className="text-gray-200 text-sm">{filter.label}</div>
            </button>
          ))}
        </div>

        <div className="flex gap-4 items-center">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="이름, 이메일로 회원 검색..."
              className="w-full pl-10 pr-4 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg text-white placeholder-gray-400"
            />
          </div>
          <button className="px-4 py-2 bg-blue-600/20 border border-blue-400/30 rounded-lg text-blue-400 hover:bg-blue-600/30">
            <Download className="w-4 h-4 mr-2 inline" />
            Excel 내보내기
          </button>
        </div>
      </div>

      {/* 회원 목록 테이블 */}
      <div className="card-cosmic">
        <div className="p-6 border-b border-gray-600/40">
          <div className="flex items-center justify-between">
            <h4 className="text-white font-semibold">회원 목록</h4>
            <div className="flex gap-2">
              <button className="px-3 py-1 bg-green-600/20 border border-green-400/30 rounded text-green-400 text-sm">
                일괄 메시지 발송
              </button>
              <button className="px-3 py-1 bg-red-600/20 border border-red-400/30 rounded text-red-400 text-sm">
                선택 계정 정지
              </button>
            </div>
          </div>
        </div>

        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-600/40">
                  <th className="text-left text-gray-200 py-3 px-2">
                    <input type="checkbox" className="rounded" />
                  </th>
                  <th className="text-left text-gray-200 py-3">회원명</th>
                  <th className="text-left text-gray-200 py-3">이메일</th>
                  <th className="text-left text-gray-200 py-3">등급</th>
                  <th className="text-left text-gray-200 py-3">포인트</th>
                  <th className="text-left text-gray-200 py-3">가입일</th>
                  <th className="text-left text-gray-200 py-3">상태</th>
                  <th className="text-left text-gray-200 py-3">관리</th>
                </tr>
              </thead>
              <tbody>
                {mockUsers.map(user => (
                  <tr key={user.id} className="border-b border-white/10 hover:bg-white/5">
                    <td className="py-3 px-2">
                      <input type="checkbox" className="rounded" />
                    </td>
                    <td className="py-3">
                      <div className="text-white">{user.name}</div>
                      <div className="text-gray-400 text-xs">최근 접속: {user.lastLogin}</div>
                    </td>
                    <td className="py-3 text-gray-200">{user.email}</td>
                    <td className="py-3">
                      <span className={`px-2 py-1 rounded text-xs ${
                        user.grade === 'VIP' ? 'bg-yellow-500/20 text-yellow-400' :
                        user.grade === '골드' ? 'bg-amber-500/20 text-amber-400' :
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {user.grade}
                      </span>
                    </td>
                    <td className="py-3 text-green-400">{user.points.toLocaleString()}P</td>
                    <td className="py-3 text-gray-200">{user.joinDate}</td>
                    <td className="py-3">
                      <span className={`px-2 py-1 rounded text-xs ${
                        user.status === 'active' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        {user.status === 'active' ? '활성' : '비활성'}
                      </span>
                    </td>
                    <td className="py-3">
                      <div className="flex gap-1">
                        <button className="text-blue-400 hover:text-blue-300 p-1">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="text-green-400 hover:text-green-300 p-1">
                          <Mail className="w-4 h-4" />
                        </button>
                        <button className="text-yellow-400 hover:text-yellow-300 p-1">
                          <Edit className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* 회원 등급 관리 */}
      <div className="card-cosmic p-6">
        <h4 className="text-white font-semibold mb-4">회원 등급 설정</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { grade: 'VIP', color: 'yellow', minPoints: 50000, benefits: '모든 서비스 20% 할인, 우선 상담' },
            { grade: '골드', color: 'amber', minPoints: 20000, benefits: '유료 서비스 10% 할인' },
            { grade: '일반', color: 'gray', minPoints: 0, benefits: '기본 서비스 이용' }
          ].map(tier => (
            <div key={tier.grade} className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center justify-between mb-2">
                <span className={`text-${tier.color}-400 font-semibold`}>{tier.grade} 등급</span>
                <button className="text-blue-400 hover:text-blue-300">
                  <Edit className="w-4 h-4" />
                </button>
              </div>
              <div className="text-sm text-gray-200 mb-2">
                최소 포인트: {tier.minPoints.toLocaleString()}P
              </div>
              <div className="text-xs text-gray-400">
                {tier.benefits}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}