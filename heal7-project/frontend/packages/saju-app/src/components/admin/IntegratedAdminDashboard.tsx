import React, { useState } from 'react';

const IntegratedAdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'saju' | 'analytics'>('overview');

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
          {/* 헤더 */}
          <div className="p-6 border-b border-white/10">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  🔐 사주 관리자 대시보드
                </h1>
                <p className="text-gray-300">saju.heal7.com/admin</p>
              </div>
              <div className="text-6xl">⚙️</div>
            </div>
          </div>

          {/* 탭 네비게이션 */}
          <div className="flex border-b border-white/10">
            {[
              { id: 'overview', label: '📊 개요', icon: '📈' },
              { id: 'users', label: '👥 사용자', icon: '👤' },
              { id: 'saju', label: '🔮 사주시스템', icon: '🔮' },
              { id: 'analytics', label: '📈 분석', icon: '📊' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex-1 px-6 py-4 text-sm font-medium transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-white/20 text-white border-b-2 border-purple-400'
                    : 'text-gray-300 hover:text-white hover:bg-white/10'
                }`}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </div>

          {/* 탭 콘텐츠 */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* 통계 카드 */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-xl p-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-300 text-sm">총 사용자</p>
                        <p className="text-2xl font-bold text-white">1,234</p>
                      </div>
                      <div className="text-3xl">👥</div>
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-xl p-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-300 text-sm">오늘 방문자</p>
                        <p className="text-2xl font-bold text-white">567</p>
                      </div>
                      <div className="text-3xl">📊</div>
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-green-500/20 to-teal-500/20 rounded-xl p-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-300 text-sm">사주 계산</p>
                        <p className="text-2xl font-bold text-white">890</p>
                      </div>
                      <div className="text-3xl">🔮</div>
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-xl p-6 border border-white/10">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-300 text-sm">매출</p>
                        <p className="text-2xl font-bold text-white">₩123,456</p>
                      </div>
                      <div className="text-3xl">💰</div>
                    </div>
                  </div>
                </div>

                {/* 최근 활동 */}
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="text-xl font-bold text-white mb-4">📋 최근 활동</h3>
                  <div className="space-y-3">
                    {[
                      { time: '방금 전', action: '새 사용자 가입: user123@email.com', icon: '👤' },
                      { time: '5분 전', action: '사주 계산 완료: 1990.03.15 생', icon: '🔮' },
                      { time: '10분 전', action: '결제 완료: 프리미엄 사주 해석', icon: '💰' },
                      { time: '15분 전', action: '타로 카드 상담 예약', icon: '🃏' }
                    ].map((activity, index) => (
                      <div key={index} className="flex items-center justify-between py-2 border-b border-white/5 last:border-b-0">
                        <div className="flex items-center space-x-3">
                          <div className="text-lg">{activity.icon}</div>
                          <div>
                            <p className="text-white">{activity.action}</p>
                            <p className="text-gray-400 text-sm">{activity.time}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'users' && (
              <div className="space-y-6">
                <h3 className="text-xl font-bold text-white">👥 사용자 관리</h3>
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <p className="text-gray-300">사용자 관리 기능이 곧 추가될 예정입니다.</p>
                </div>
              </div>
            )}

            {activeTab === 'saju' && (
              <div className="space-y-6">
                <h3 className="text-xl font-bold text-white">🔮 사주 시스템 관리</h3>
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <p className="text-gray-300">사주 시스템 설정 및 모니터링 기능이 곧 추가될 예정입니다.</p>
                </div>
              </div>
            )}

            {activeTab === 'analytics' && (
              <div className="space-y-6">
                <h3 className="text-xl font-bold text-white">📈 분석 및 통계</h3>
                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <p className="text-gray-300">상세 분석 및 리포트 기능이 곧 추가될 예정입니다.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntegratedAdminDashboard;