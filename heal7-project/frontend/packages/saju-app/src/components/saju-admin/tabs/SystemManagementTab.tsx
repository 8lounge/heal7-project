/**
 * ⚙️ 시스템 탭 - 시스템 설정 및 1:1 문의 관리
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  AlertTriangle, Eye, MessageSquare, Database,
  Clock, Bell
} from 'lucide-react'

export const SystemManagementTab = () => {
  const [activeTab, setActiveTab] = useState('inquiries')
  
  const tabs = [
    { key: 'inquiries', label: '1:1 문의 관리', count: 23 },
    { key: 'system', label: '시스템 설정', count: null },
    { key: 'monitoring', label: '시스템 모니터링', count: null }
  ]

  const mockInquiries = [
    { 
      id: 1, 
      user: '김○○', 
      subject: '사주 결과가 이상해요', 
      category: '서비스 문의', 
      status: 'pending', 
      date: '2025-09-03 15:30',
      content: '사주 풀이 결과에서 생년월일을 정확히 입력했는데 결과가 이상합니다. 확인 부탁드립니다.'
    },
    { 
      id: 2, 
      user: '이○○', 
      subject: '포인트 차감 문의', 
      category: '결제 문의', 
      status: 'replied', 
      date: '2025-09-03 14:15',
      content: '포인트가 두 번 차감된 것 같습니다. 확인 후 환불 처리 부탁드립니다.'
    },
    { 
      id: 3, 
      user: '박○○', 
      subject: '회원 탈퇴 요청', 
      category: '계정 문의', 
      status: 'pending', 
      date: '2025-09-03 13:20',
      content: '개인정보 보호를 위해 회원 탈퇴를 원합니다. 절차 안내 부탁드립니다.'
    }
  ]

  return (
    <div className="space-y-6">
      {/* 탭 선택 */}
      <div className="card-cosmic p-6">
        <h3 className="text-white text-lg font-semibold mb-4">시스템 관리</h3>
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
              {tab.count && (
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
          {/* 문의 현황 통계 */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { title: '미답변 문의', value: '23', color: 'red', urgent: true },
              { title: '답변 완료', value: '156', color: 'green', urgent: false },
              { title: '평균 응답시간', value: '2.3시간', color: 'blue', urgent: false },
              { title: '만족도', value: '4.6/5', color: 'yellow', urgent: false }
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
          <div className="card-cosmic">
            <div className="p-6 border-b border-gray-600/40">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-semibold">1:1 문의 목록</h4>
                <div className="flex gap-2">
                  <select className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm">
                    <option value="all">전체 문의</option>
                    <option value="pending">미답변</option>
                    <option value="replied">답변완료</option>
                  </select>
                  <button className="px-3 py-1 bg-green-600/20 border border-green-400/30 rounded text-green-400 text-sm">
                    일괄 처리
                  </button>
                </div>
              </div>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                {mockInquiries.map(inquiry => (
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
                            inquiry.status === 'pending' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'
                          }`}>
                            {inquiry.status === 'pending' ? '미답변' : '답변완료'}
                          </span>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-400 mb-2">
                          <span>작성자: {inquiry.user}</span>
                          <span>분류: {inquiry.category}</span>
                          <span>작성일: {inquiry.date}</span>
                        </div>
                        <p className="text-gray-200 text-sm">{inquiry.content}</p>
                      </div>
                      <div className="flex gap-1 ml-4">
                        <button className="text-blue-400 hover:text-blue-300 p-2">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="text-green-400 hover:text-green-300 p-2">
                          <MessageSquare className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 시스템 설정 */}
      {activeTab === 'system' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 사주 엔진 설정 */}
            <div className="card-cosmic p-6">
              <h4 className="text-white font-semibold mb-4">사주 엔진 설정</h4>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">고급 분석 모드</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">자동 해석 업데이트</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">캐시 자동 갱신</span>
                  <div className="flex items-center gap-2">
                    <input type="number" defaultValue="24" className="w-16 px-2 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-center" />
                    <span className="text-gray-400">시간</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 알림 설정 */}
            <div className="card-cosmic p-6">
              <h4 className="text-white font-semibold mb-4">알림 설정</h4>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">새 문의 알림</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">시스템 오류 알림</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-200">매출 리포트</span>
                  <select className="px-3 py-1 bg-white/10 backdrop-blur-md border border-white/20 rounded text-white text-sm">
                    <option value="daily">매일</option>
                    <option value="weekly">매주</option>
                    <option value="monthly">매월</option>
                  </select>
                </div>
              </div>
            </div>

            {/* 운영 정책 */}
            <div className="card-cosmic p-6">
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
            <div className="card-cosmic p-6">
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

          <div className="flex justify-end">
            <button className="px-6 py-2 bg-purple-600/20 border border-purple-400/30 rounded-lg text-purple-400 hover:bg-purple-600/30">
              설정 저장
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
          <div className="card-cosmic p-6">
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
            <div className="card-cosmic p-6">
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

            <div className="card-cosmic p-6">
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
    </div>
  )
}