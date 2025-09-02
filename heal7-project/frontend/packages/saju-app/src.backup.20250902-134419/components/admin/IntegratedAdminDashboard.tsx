import React, { useState } from 'react';
import { motion } from 'framer-motion';

const IntegratedAdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('overview');

  // 탭 목록 정의
  const tabs = [
    { id: 'overview', label: '📊 개요', icon: '📈' },
    { id: 'users', label: '👥 회원관리', icon: '👤' },
    { id: 'contents', label: '📋 콘텐츠관리', icon: '📄' },
    { id: 'notifications', label: '🔔 알림관리', icon: '📢' },
    { id: 'saju-overview', label: '🔮 사주풀이', icon: '🔮' },
    { id: 'saju-time', label: '⏰ 시간설정', icon: '🕐' },
    { id: 'saju-geographic', label: '🗺️ 지역설정', icon: '🌍' },
    { id: 'saju-logic', label: '🧠 사주 논리', icon: '⚡' },
    { id: 'community', label: '👥 커뮤니티', icon: '💬' },
    { id: 'point-cash', label: '💰 포인트/캐시', icon: '💎' }
  ];

  // 샘플 데이터
  const stats = {
    totalUsers: 2847,
    premiumUsers: 567,
    vipUsers: 123,
    totalContents: 1248,
    notificationRate: 94.8,
    todayVisitors: 432,
    sajuCalculations: 156,
    revenue: 1234567
  };

  const recentActivities = [
    { time: '방금 전', action: '새 사용자 가입: user123@email.com', icon: '👤', type: 'user' },
    { time: '5분 전', action: '사주 계산 완료: 1990.03.15 생', icon: '🔮', type: 'saju' },
    { time: '10분 전', action: '프리미엄 결제 완료: ₩29,900', icon: '💰', type: 'payment' },
    { time: '15분 전', action: '새 콘텐츠 발행: "2025년 운세 전망"', icon: '📄', type: 'content' },
    { time: '20분 전', action: '커뮤니티 댓글 신고', icon: '⚠️', type: 'report' }
  ];

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <motion.div 
          className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* 헤더 */}
          <div className="p-6 border-b border-white/10">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  ✨ 통합 관리자 대시보드
                </h1>
                <p className="text-gray-300">사용자, 콘텐츠, 알림을 한 곳에서 관리</p>
                <p className="text-sm text-gray-400 mt-1">saju.heal7.com/admin</p>
              </div>
              <div className="text-6xl">⚙️</div>
            </div>
          </div>

          {/* 탭 네비게이션 */}
          <div className="border-b border-white/10 overflow-x-auto">
            <div className="flex min-w-max">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-shrink-0 px-4 py-4 text-sm font-medium transition-all duration-300 whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'bg-white/20 text-white border-b-2 border-purple-400'
                      : 'text-gray-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <span>{tab.icon}</span>
                    <span className="hidden sm:inline">{tab.label.split(' ')[1] || tab.label}</span>
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* 탭 콘텐츠 */}
          <div className="p-6">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  {/* 통계 카드 */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-xl p-6 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-gray-300 text-sm">전체 사용자</p>
                          <p className="text-2xl font-bold text-white">{stats.totalUsers.toLocaleString()}</p>
                        </div>
                        <div className="text-3xl">👥</div>
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-xl p-6 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-gray-300 text-sm">프리미엄 사용자</p>
                          <p className="text-2xl font-bold text-white">{stats.premiumUsers.toLocaleString()}</p>
                        </div>
                        <div className="text-3xl">💎</div>
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-r from-green-500/20 to-teal-500/20 rounded-xl p-6 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-gray-300 text-sm">전체 콘텐츠</p>
                          <p className="text-2xl font-bold text-white">{stats.totalContents.toLocaleString()}</p>
                        </div>
                        <div className="text-3xl">📄</div>
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-xl p-6 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-gray-300 text-sm">알림 성공률</p>
                          <p className="text-2xl font-bold text-white">{stats.notificationRate}%</p>
                        </div>
                        <div className="text-3xl">📢</div>
                      </div>
                    </div>
                  </div>

                  {/* 최근 활동 */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                      <h3 className="text-xl font-bold text-white mb-4">📋 최근 활동</h3>
                      <div className="space-y-3">
                        {recentActivities.map((activity, index) => (
                          <div key={index} className="flex items-center justify-between py-2 border-b border-white/5 last:border-b-0">
                            <div className="flex items-center space-x-3">
                              <div className="text-lg">{activity.icon}</div>
                              <div>
                                <p className="text-white text-sm">{activity.action}</p>
                                <p className="text-gray-400 text-xs">{activity.time}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                      <h3 className="text-xl font-bold text-white mb-4">📊 주요 지표</h3>
                      <div className="space-y-4">
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300">오늘 방문자</span>
                          <span className="text-white font-bold">{stats.todayVisitors}명</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300">사주 계산</span>
                          <span className="text-white font-bold">{stats.sajuCalculations}건</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300">일 매출</span>
                          <span className="text-white font-bold">₩{(stats.revenue / 30).toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-300">VIP 사용자</span>
                          <span className="text-white font-bold">{stats.vipUsers}명</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'users' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">👥 회원관리</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-6">
                    <div className="bg-blue-500/20 rounded-xl p-4 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-white/70 text-sm">무료 회원</p>
                          <p className="text-2xl font-bold text-blue-400">2,847</p>
                        </div>
                        <div className="text-2xl">👤</div>
                      </div>
                    </div>
                    <div className="bg-purple-500/20 rounded-xl p-4 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-white/70 text-sm">프리미엄</p>
                          <p className="text-2xl font-bold text-purple-400">567</p>
                        </div>
                        <div className="text-2xl">💎</div>
                      </div>
                    </div>
                    <div className="bg-yellow-500/20 rounded-xl p-4 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-white/70 text-sm">VIP</p>
                          <p className="text-2xl font-bold text-yellow-400">123</p>
                        </div>
                        <div className="text-2xl">👑</div>
                      </div>
                    </div>
                    <div className="bg-cyan-500/20 rounded-xl p-4 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-white/70 text-sm">운영관리자</p>
                          <p className="text-2xl font-bold text-cyan-400">12</p>
                        </div>
                        <div className="text-2xl">⚙️</div>
                      </div>
                    </div>
                    <div className="bg-red-500/20 rounded-xl p-4 border border-white/10">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-white/70 text-sm">슈퍼관리자</p>
                          <p className="text-2xl font-bold text-red-400">3</p>
                        </div>
                        <div className="text-2xl">🔑</div>
                      </div>
                    </div>
                  </div>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300">회원 관리 기능이 곧 추가될 예정입니다.</p>
                    <div className="mt-4 space-y-2 text-sm text-gray-400">
                      <p>• 회원 검색 및 필터링</p>
                      <p>• 등급 변경 및 권한 관리</p>
                      <p>• 포인트/캐시 지급 및 차감</p>
                      <p>• 회원 상세 정보 조회</p>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'contents' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">📋 콘텐츠관리</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300 mb-4">콘텐츠 관리 기능이 곧 추가될 예정입니다.</p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">📰</div>
                        <div className="text-white font-medium">매거진 관리</div>
                        <div className="text-gray-400 text-sm mt-1">기사 작성 및 편집</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">🔮</div>
                        <div className="text-white font-medium">사주 콘텐츠</div>
                        <div className="text-gray-400 text-sm mt-1">해석 템플릿 관리</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">🎯</div>
                        <div className="text-white font-medium">이벤트 관리</div>
                        <div className="text-gray-400 text-sm mt-1">프로모션 및 이벤트</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">🔔 알림관리</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300 mb-4">알림 시스템 관리 기능이 곧 추가될 예정입니다.</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">📱</div>
                        <div className="text-white font-medium">푸시 알림</div>
                        <div className="text-gray-400 text-sm mt-1">모바일 푸시 메시지</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">✉️</div>
                        <div className="text-white font-medium">이메일 알림</div>
                        <div className="text-gray-400 text-sm mt-1">이메일 발송 관리</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'saju-overview' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">🔮 사주풀이</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300 mb-4">사주 시스템 관리 기능이 곧 추가될 예정입니다.</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">📊</div>
                        <div className="text-white font-medium">사주 통계</div>
                        <div className="text-gray-400 text-sm mt-1">계산 건수 및 분석</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">🎯</div>
                        <div className="text-white font-medium">해석 품질</div>
                        <div className="text-gray-400 text-sm mt-1">AI 해석 정확도</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'saju-time' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">⏰ 시간설정</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300">사주 계산을 위한 시간 설정 기능이 곧 추가될 예정입니다.</p>
                  </div>
                </div>
              )}

              {activeTab === 'saju-geographic' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">🗺️ 지역설정</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300">지역별 사주 계산 설정 기능이 곧 추가될 예정입니다.</p>
                  </div>
                </div>
              )}

              {activeTab === 'saju-logic' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">🧠 사주 논리</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300">사주 해석 논리 및 알고리즘 관리 기능이 곧 추가될 예정입니다.</p>
                  </div>
                </div>
              )}

              {activeTab === 'community' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">👥 커뮤니티</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300">커뮤니티 관리 기능이 곧 추가될 예정입니다.</p>
                  </div>
                </div>
              )}

              {activeTab === 'point-cash' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">💰 포인트/캐시</h3>
                  <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <p className="text-gray-300 mb-4">포인트 및 캐시 관리 기능이 곧 추가될 예정입니다.</p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">💎</div>
                        <div className="text-white font-medium">포인트 관리</div>
                        <div className="text-gray-400 text-sm mt-1">적립 및 사용 내역</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">💰</div>
                        <div className="text-white font-medium">캐시 관리</div>
                        <div className="text-gray-400 text-sm mt-1">충전 및 결제 내역</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl mb-2">📊</div>
                        <div className="text-white font-medium">수익 분석</div>
                        <div className="text-gray-400 text-sm mt-1">매출 및 정산 관리</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default IntegratedAdminDashboard;