import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Switch } from '../ui/switch';
import { Users, FileText, Bell, Settings, TrendingUp, Database, Globe, Brain, Save, RefreshCw, AlertCircle, Coins, CreditCard, BarChart3, MessageSquare } from 'lucide-react';
import { SajuAdminSettings } from '../../types/sajuAdminTypes';
// import type { 
//   SajuInterpretationManagement
// } from '../../types/sajuInterpretationTypes';
import { useAuth, useSajuSettings, useSaveSettings } from '../../hooks/useSajuAdmin';
import { getDummySettings } from '../../utils/sajuAdminMockData';
import { getSajuSystemStats, getRecentCalculationLogs } from '../../utils/sajuSystemStats';
import { 
  safeGetLogicType, 
  safeUpdateLogicSettings
} from '../../utils/sajuDataHelpers';

interface User {
  id: number;
  email: string;
  username: string;
  grade: 'free' | 'premium' | 'vip';
  status: 'active' | 'inactive' | 'suspended';
  cash_balance: number;
  created_at: string;
  last_login: string;
}

interface Content {
  id: number;
  title: string;
  content_type: 'magazine' | 'notice' | 'consultation';
  status: 'draft' | 'published' | 'archived';
  author_name: string;
  views: number;
  created_at: string;
}

interface NotificationStats {
  total_notifications: number;
  success_rate: number;
  type_distribution: { [key: string]: number };
}

const IntegratedAdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [users, setUsers] = useState<User[]>([]);
  const [contents, setContents] = useState<Content[]>([]);
  const [userStats, setUserStats] = useState<any>(null);
  const [contentStats, setContentStats] = useState<any>(null);
  const [notificationStats, setNotificationStats] = useState<NotificationStats | null>(null);
  
  // 사주 풀이 관리 상태 (미사용 - 향후 확장용)
  // const [sajuCategory, setSajuCategory] = useState<'sipsin' | 'cheongan' | 'jiji' | 'gapja' | 'geokguk' | 'ohaeng'>('sipsin');
  // const [editingInterpretation, setEditingInterpretation] = useState<SajuInterpretationManagement | null>(null);
  // const [interpretationForm, setInterpretationForm] = useState<any>({});
  
  // 사주 관리 설정 상태
  const { token } = useAuth();
  const { data: apiSettings, isLoading: apiLoading, mutate } = useSajuSettings(token);
  const { saveSettings, saving } = useSaveSettings(token, mutate);
  const [sajuSettings, setSajuSettings] = useState<SajuAdminSettings | null>(apiSettings);
  const [sajuLoading, setSajuLoading] = useState(apiLoading);
  
  // Point/Cash policy state
  const [refundEnabled, setRefundEnabled] = useState(true);
  const [freeTrialEnabled, setFreeTrialEnabled] = useState(true);
  const [guestAccessEnabled, setGuestAccessEnabled] = useState(true);
  const [maintenanceMode, setMaintenanceMode] = useState(false);
  const [autoBlockEnabled, setAutoBlockEnabled] = useState(true);
  const [autoResponseEnabled, setAutoResponseEnabled] = useState(true);

  // 사주 시스템 통계 데이터 
  const [sajuStats, setSajuStats] = useState<any>(null);
  const [calculationLogs] = useState(() => getRecentCalculationLogs());
  const [statsLoading, setStatsLoading] = useState(true);

  // 데이터 로딩
  useEffect(() => {
    loadDashboardData();
  }, []);

  // 사주 설정 데이터 동기화
  useEffect(() => {
    setSajuSettings(apiSettings || getDummySettings());
    setSajuLoading(apiLoading);
  }, [apiSettings, apiLoading]);

  const loadDashboardData = async () => {
    try {
      // 사주 시스템 통계 데이터 로드
      setStatsLoading(true);
      const stats = await getSajuSystemStats();
      setSajuStats(stats);
      setStatsLoading(false);
      
      // Saju Admin Service 관리자 API 호출
      const usersResponse = await fetch('/api/user-management/users?limit=10');
      if (usersResponse.ok) {
        const usersData = await usersResponse.json();
        setUsers(usersData.users || []);
      }

      const userStatsResponse = await fetch('/api/user-management/stats');
      if (userStatsResponse.ok) {
        const stats = await userStatsResponse.json();
        setUserStats(stats);
      }

      // 콘텐츠 관리 API 호출
      const contentsResponse = await fetch('/api/content-management/contents?limit=10');
      if (contentsResponse.ok) {
        const contentsData = await contentsResponse.json();
        setContents(contentsData.contents || []);
      }

      const contentStatsResponse = await fetch('/api/content-management/stats');
      if (contentStatsResponse.ok) {
        const stats = await contentStatsResponse.json();
        setContentStats(stats);
      }

      // 알림 시스템 통계
      const notificationStatsResponse = await fetch('/api/notification/stats');
      if (notificationStatsResponse.ok) {
        const stats = await notificationStatsResponse.json();
        setNotificationStats(stats);
      }
    } catch (error) {
      console.error('데이터 로딩 실패:', error);
    }
  };

  const handleGradeChange = async (userId: number, newGrade: string, reason: string) => {
    try {
      const response = await fetch(`/api/user-management/users/${userId}/grade`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_grade: newGrade, reason })
      });

      if (response.ok) {
        alert('사용자 등급이 변경되었습니다');
        loadDashboardData(); // 데이터 새로고침
      }
    } catch (error) {
      alert('등급 변경에 실패했습니다');
    }
  };

  const sendBulkNotification = async (userIds: number[], message: string, type: 'email' | 'kakao' | 'both') => {
    try {
      const response = await fetch('/api/notification/bulk-send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          notification_type: type,
          user_ids: userIds,
          content: message
        })
      });

      if (response.ok) {
        alert(`${userIds.length}명에게 ${type} 알림이 발송 예약되었습니다`);
      }
    } catch (error) {
      alert('알림 발송에 실패했습니다');
    }
  };

  // 사주 설정 저장
  const handleSajuSave = async () => {
    if (!sajuSettings) return;
    
    const success = await saveSettings(sajuSettings);
    if (success) {
      alert('사주 설정이 성공적으로 저장되었습니다.');
    } else {
      alert('설정 저장에 실패했습니다.');
    }
  };

  // 사주 풀이 관리 핸들러들 (미사용 - 향후 확장용)
  /*
  const handleInterpretationSave = async (interpretationData: any) => {
    // 구현 예정
  };

  const handleInterpretationEdit = (item: any) => {
    // 구현 예정
  };

  const handleFormChange = (field: string, value: any) => {
    // 구현 예정
  };
  */

  return (
    <div className="min-h-screen bg-transparent p-6 relative overflow-hidden">
      {/* Glass morphism 배경 */}
      <div className="fixed inset-0 bg-gradient-to-br from-blue-600/20 via-purple-600/10 to-indigo-600/20"></div>
      <div className="fixed inset-0 top-20 backdrop-blur-3xl bg-white/5"></div>
      
      {/* 떠다니는 유리 구체들 */}
      <div className="fixed top-10 left-10 w-32 h-32 bg-gradient-to-br from-blue-400/30 to-purple-400/30 rounded-full blur-xl animate-pulse"></div>
      <div className="fixed top-1/2 right-20 w-24 h-24 bg-gradient-to-br from-purple-400/30 to-pink-400/30 rounded-full blur-xl animate-pulse delay-1000"></div>
      <div className="fixed bottom-20 left-1/3 w-40 h-40 bg-gradient-to-br from-indigo-400/20 to-blue-400/20 rounded-full blur-2xl animate-pulse delay-2000"></div>
      
      <div className="max-w-7xl mx-auto relative z-10 -mt-8">
        {/* 헤더 */}
        <div className="mb-8">
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
            {/* 내부 글래스 효과 */}
            <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-white/5 rounded-3xl"></div>
            <div className="relative z-10">
              <h1 className="text-5xl font-bold text-white mb-3 drop-shadow-lg">
                ✨ 통합 관리자 대시보드
              </h1>
              <p className="text-white/80 text-lg">사용자, 콘텐츠, 알림을 한 곳에서 관리</p>
            </div>
          </div>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-4 lg:grid-cols-10 mb-8 backdrop-blur-xl bg-white/15 border border-white/25 rounded-2xl shadow-2xl p-2">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              <span className="hidden sm:inline">개요</span>
            </TabsTrigger>
            <TabsTrigger value="users" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              <span className="hidden sm:inline">회원관리</span>
            </TabsTrigger>
            <TabsTrigger value="contents" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              <span className="hidden sm:inline">콘텐츠관리</span>
            </TabsTrigger>
            <TabsTrigger value="notifications" className="flex items-center gap-2">
              <Bell className="w-4 h-4" />
              <span className="hidden sm:inline">알림관리</span>
            </TabsTrigger>
            <TabsTrigger value="saju-overview" className="flex items-center gap-2">
              <Database className="w-4 h-4" />
              <span className="hidden sm:inline">사주풀이</span>
            </TabsTrigger>
            <TabsTrigger value="saju-time" className="flex items-center gap-2">
              <Settings className="w-4 h-4" />
              <span className="hidden sm:inline">시간설정</span>
            </TabsTrigger>
            <TabsTrigger value="saju-geographic" className="flex items-center gap-2">
              <Globe className="w-4 h-4" />
              <span className="hidden sm:inline">지역설정</span>
            </TabsTrigger>
            <TabsTrigger value="saju-logic" className="flex items-center gap-2">
              <Brain className="w-4 h-4" />
              <span className="hidden sm:inline">사주 논리</span>
            </TabsTrigger>
            <TabsTrigger value="community" className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              <span className="hidden sm:inline">커뮤니티</span>
            </TabsTrigger>
            <TabsTrigger value="point-cash" className="flex items-center gap-2">
              <Coins className="w-4 h-4" />
              <span className="hidden sm:inline">포인트/캐시</span>
            </TabsTrigger>
          </TabsList>

          {/* 개요 탭 */}
          <TabsContent value="overview">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl hover:bg-white/15 hover:scale-105 transition-all duration-300 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl group-hover:from-white/10"></div>
                <div className="relative z-10">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">전체 사용자</p>
                      <p className="text-4xl font-bold text-white drop-shadow-lg">{userStats?.total_users || 0}</p>
                    </div>
                    <Users className="w-10 h-10 text-blue-300 drop-shadow-lg" />
                  </div>
                </div>
              </Card>

              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl hover:bg-white/15 hover:scale-105 transition-all duration-300 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl group-hover:from-white/10"></div>
                <div className="relative z-10">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">프리미엄 사용자</p>
                      <p className="text-4xl font-bold text-white drop-shadow-lg">{userStats?.active_premium_users || 0}</p>
                    </div>
                    <TrendingUp className="w-10 h-10 text-purple-300 drop-shadow-lg" />
                  </div>
                </div>
              </Card>

              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl hover:bg-white/15 hover:scale-105 transition-all duration-300 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl group-hover:from-white/10"></div>
                <div className="relative z-10">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">전체 콘텐츠</p>
                      <p className="text-4xl font-bold text-white drop-shadow-lg">{contentStats?.total_contents || 0}</p>
                    </div>
                    <FileText className="w-10 h-10 text-green-300 drop-shadow-lg" />
                  </div>
                </div>
              </Card>

              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl hover:bg-white/15 hover:scale-105 transition-all duration-300 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl group-hover:from-white/10"></div>
                <div className="relative z-10">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">알림 성공률</p>
                      <p className="text-4xl font-bold text-white drop-shadow-lg">{notificationStats?.success_rate?.toFixed(1) || 0}%</p>
                    </div>
                    <Bell className="w-10 h-10 text-orange-300 drop-shadow-lg" />
                  </div>
                </div>
              </Card>
            </div>

            {/* 최근 활동 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl"></div>
                <div className="relative z-10">
                  <h3 className="text-xl font-semibold text-white mb-4 drop-shadow-lg">최근 가입 사용자</h3>
                  <div className="space-y-3">
                    {users.slice(0, 5).map(user => (
                      <div key={user.id} className="flex items-center justify-between p-4 bg-white/10 rounded-xl border border-white/15 backdrop-blur-sm hover:bg-white/15 transition-all">
                        <div>
                          <p className="text-white font-semibold">{user.username}</p>
                          <p className="text-white/70 text-sm">{user.email}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs backdrop-blur-md font-medium ${
                          user.grade === 'vip' ? 'bg-yellow-400/40 text-yellow-100 border border-yellow-300/30' :
                          user.grade === 'premium' ? 'bg-purple-400/40 text-purple-100 border border-purple-300/30' : 'bg-gray-400/40 text-gray-100 border border-gray-300/30'
                        }`}>
                          {user.grade}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>

              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl"></div>
                <div className="relative z-10">
                  <h3 className="text-xl font-semibold text-white mb-4 drop-shadow-lg">최근 콘텐츠</h3>
                  <div className="space-y-3">
                    {contents.slice(0, 5).map(content => (
                      <div key={content.id} className="flex items-center justify-between p-4 bg-white/10 rounded-xl border border-white/15 backdrop-blur-sm hover:bg-white/15 transition-all">
                        <div>
                          <p className="text-white font-semibold">{content.title}</p>
                          <p className="text-white/70 text-sm">
                            {content.content_type} • {content.author_name} • 조회 {content.views}회
                          </p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs backdrop-blur-md font-medium ${
                          content.status === 'published' ? 'bg-green-400/40 text-green-100 border border-green-300/30' :
                          content.status === 'draft' ? 'bg-yellow-400/40 text-yellow-100 border border-yellow-300/30' : 'bg-gray-400/40 text-gray-100 border border-gray-300/30'
                        }`}>
                          {content.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* 회원관리 탭 */}
          <TabsContent value="users">
            <div className="space-y-6">
              
              {/* 회원 통계 개요 */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">무료 회원</p>
                      <p className="text-3xl font-bold text-blue-400">2,847</p>
                    </div>
                    <Users className="w-8 h-8 text-blue-400" />
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">프리미엄</p>
                      <p className="text-3xl font-bold text-purple-400">567</p>
                    </div>
                    <span className="text-2xl">💎</span>
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">VIP</p>
                      <p className="text-3xl font-bold text-yellow-400">123</p>
                    </div>
                    <span className="text-2xl">👑</span>
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">운영관리자</p>
                      <p className="text-3xl font-bold text-cyan-400">12</p>
                    </div>
                    <span className="text-2xl">⚙️</span>
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">슈퍼관리자</p>
                      <p className="text-3xl font-bold text-red-400">3</p>
                    </div>
                    <span className="text-2xl">🔑</span>
                  </div>
                </Card>
              </div>

              {/* 회원 검색 및 필터 */}
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <div className="flex flex-col md:flex-row gap-4 mb-4">
                  <div className="flex-1">
                    <input 
                      type="text"
                      placeholder="이메일, 이름으로 검색..."
                      className="admin-input w-full p-3"
                    />
                  </div>
                  <div className="flex gap-2">
                    <select className="admin-select px-4 py-3">
                      <option value="">모든 등급</option>
                      <option value="free">무료</option>
                      <option value="premium">프리미엄</option>
                      <option value="vip">VIP</option>
                      <option value="operator">운영관리자</option>
                      <option value="super_admin">슈퍼관리자</option>
                    </select>
                    <select className="admin-select px-4 py-3">
                      <option value="">모든 상태</option>
                      <option value="active">활성</option>
                      <option value="inactive">비활성</option>
                      <option value="suspended">정지</option>
                    </select>
                    <Button className="btn-cosmic px-4 py-3">
                      검색
                    </Button>
                  </div>
                </div>
              </Card>

              {/* 상세 회원 목록 */}
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-white">회원 목록</h3>
                  <div className="flex gap-2">
                    <Button className="btn-outline px-4 py-2 text-sm">
                      일괄 관리
                    </Button>
                    <Button className="btn-cosmic px-4 py-2 text-sm">
                      회원 추가
                    </Button>
                  </div>
                </div>
                
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-white/20">
                        <th className="text-left text-gray-300 p-3 font-medium">회원 정보</th>
                        <th className="text-left text-gray-300 p-3 font-medium">등급/상태</th>
                        <th className="text-left text-gray-300 p-3 font-medium">포인트/캐시</th>
                        <th className="text-left text-gray-300 p-3 font-medium">상담/리뷰</th>
                        <th className="text-left text-gray-300 p-3 font-medium">활동</th>
                        <th className="text-left text-gray-300 p-3 font-medium">관리</th>
                      </tr>
                    </thead>
                    <tbody>
                      {[
                        { 
                          id: 1, username: "김정미", email: "kim@email.com", grade: "vip", status: "active", 
                          points: 15650, cash: 45000, consultations: 12, reviews: 8,
                          lastLogin: "2025-08-29", joinDate: "2023-05-15", phone: "010-1234-5678"
                        },
                        { 
                          id: 2, username: "이수현", email: "lee@email.com", grade: "premium", status: "active", 
                          points: 8400, cash: 25000, consultations: 5, reviews: 3,
                          lastLogin: "2025-08-28", joinDate: "2024-01-20", phone: "010-2345-6789"
                        },
                        { 
                          id: 3, username: "박민수", email: "park@email.com", grade: "free", status: "active", 
                          points: 2100, cash: 0, consultations: 2, reviews: 1,
                          lastLogin: "2025-08-27", joinDate: "2025-08-01", phone: "010-3456-7890"
                        },
                        { 
                          id: 4, username: "관리자", email: "admin@heal7.com", grade: "super_admin", status: "active", 
                          points: 0, cash: 0, consultations: 0, reviews: 0,
                          lastLogin: "2025-08-29", joinDate: "2023-01-01", phone: "050-7722-7328"
                        },
                        { 
                          id: 5, username: "정은혜", email: "jung@email.com", grade: "premium", status: "suspended", 
                          points: 550, cash: 12000, consultations: 8, reviews: 0,
                          lastLogin: "2025-08-20", joinDate: "2024-06-10", phone: "010-4567-8901"
                        }
                      ].map((user) => (
                        <tr key={user.id} className="border-b border-white/10 hover:bg-white/5">
                          <td className="p-3">
                            <div>
                              <div className="flex items-center gap-2">
                                <h4 className="text-white font-medium">{user.username}</h4>
                                {user.grade === 'super_admin' && <span className="text-red-400">🔑</span>}
                                {user.grade === 'operator' && <span className="text-cyan-400">⚙️</span>}
                                {user.grade === 'vip' && <span className="text-yellow-400">👑</span>}
                                {user.grade === 'premium' && <span className="text-purple-400">💎</span>}
                              </div>
                              <p className="text-gray-400 text-sm">{user.email}</p>
                              <p className="text-gray-500 text-xs">{user.phone}</p>
                            </div>
                          </td>
                          <td className="p-3">
                            <div className="space-y-2">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                user.grade === 'super_admin' ? 'bg-red-400/20 text-red-400' :
                                user.grade === 'operator' ? 'bg-cyan-400/20 text-cyan-400' :
                                user.grade === 'vip' ? 'bg-yellow-400/20 text-yellow-400' :
                                user.grade === 'premium' ? 'bg-purple-400/20 text-purple-400' : 
                                'bg-blue-400/20 text-blue-400'
                              }`}>
                                {user.grade === 'super_admin' ? '슈퍼관리자' :
                                 user.grade === 'operator' ? '운영관리자' :
                                 user.grade === 'vip' ? 'VIP' :
                                 user.grade === 'premium' ? '프리미엄' : '무료'}
                              </span>
                              <div>
                                <span className={`px-2 py-1 rounded text-xs ${
                                  user.status === 'active' ? 'bg-green-400/20 text-green-400' :
                                  user.status === 'suspended' ? 'bg-red-400/20 text-red-400' : 
                                  'bg-gray-400/20 text-gray-400'
                                }`}>
                                  {user.status === 'active' ? '활성' :
                                   user.status === 'suspended' ? '정지' : '비활성'}
                                </span>
                              </div>
                            </div>
                          </td>
                          <td className="p-3">
                            <div className="space-y-1">
                              <div className="flex items-center gap-2">
                                <Coins className="w-4 h-4 text-yellow-400" />
                                <span className="text-white text-sm font-medium">{user.points.toLocaleString()}P</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <CreditCard className="w-4 h-4 text-green-400" />
                                <span className="text-white text-sm font-medium">{user.cash.toLocaleString()}원</span>
                              </div>
                            </div>
                          </td>
                          <td className="p-3">
                            <div className="flex gap-2">
                              <button 
                                className={`px-2 py-1 rounded border text-xs ${
                                  user.consultations > 0 
                                    ? 'border-blue-400 text-blue-400 hover:bg-blue-400/10' 
                                    : 'border-gray-400 text-gray-400'
                                }`}
                                onClick={() => {
                                  if (user.consultations > 0) {
                                    alert(`${user.username}님의 1:1 상담 내역 ${user.consultations}개:\n\n• 프리미엄 사주 분석 (답변완료)\n• 궁합 분석 (답변완료)\n• 타로 리딩 (답변 대기중)\n...(${user.consultations}개 중 3개 표시)`);
                                  }
                                }}
                              >
                                상담 {user.consultations}
                              </button>
                              <button 
                                className={`px-2 py-1 rounded border text-xs ${
                                  user.reviews > 0 
                                    ? 'border-purple-400 text-purple-400 hover:bg-purple-400/10' 
                                    : 'border-gray-400 text-gray-400'
                                }`}
                                onClick={() => {
                                  if (user.reviews > 0) {
                                    alert(`${user.username}님의 리뷰 ${user.reviews}개:\n\n• 사주 분석 - ★★★★★ (승인됨)\n• 타로 카드 - ★★★★☆ (승인됨)\n• 궁합 분석 - ★★★★★ (승인 대기)\n...(${user.reviews}개 중 3개 표시)`);
                                  }
                                }}
                              >
                                리뷰 {user.reviews}
                              </button>
                            </div>
                          </td>
                          <td className="p-3">
                            <div className="text-xs text-gray-400">
                              <div>가입: {user.joinDate}</div>
                              <div>최근: {user.lastLogin}</div>
                            </div>
                          </td>
                          <td className="p-3">
                            <div className="flex gap-1">
                              <Button 
                                className="text-xs px-3 py-1 bg-blue-400/20 text-blue-400 hover:bg-blue-400/30"
                                onClick={() => alert(`${user.username} 상세 정보 조회`)}
                              >
                                상세
                              </Button>
                              <Button 
                                className="text-xs px-3 py-1 bg-purple-400/20 text-purple-400 hover:bg-purple-400/30"
                                onClick={() => handleGradeChange(user.id, 'premium', '관리자 변경')}
                              >
                                등급
                              </Button>
                              {user.status === 'active' ? (
                                <Button 
                                  className="text-xs px-3 py-1 bg-red-400/20 text-red-400 hover:bg-red-400/30"
                                  onClick={() => alert(`${user.username} 계정 정지`)}
                                >
                                  정지
                                </Button>
                              ) : (
                                <Button 
                                  className="text-xs px-3 py-1 bg-green-400/20 text-green-400 hover:bg-green-400/30"
                                  onClick={() => alert(`${user.username} 계정 활성화`)}
                                >
                                  활성화
                                </Button>
                              )}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* 페이지네이션 */}
                <div className="flex items-center justify-between mt-6">
                  <div className="flex items-center gap-2 text-sm text-gray-400">
                    <span>총 3,552명 중 1-5명 표시</span>
                  </div>
                  <div className="flex gap-2">
                    <Button className="btn-outline px-3 py-1 text-sm">이전</Button>
                    <Button className="btn-cosmic px-3 py-1 text-sm">1</Button>
                    <Button className="btn-outline px-3 py-1 text-sm">2</Button>
                    <Button className="btn-outline px-3 py-1 text-sm">3</Button>
                    <Button className="btn-outline px-3 py-1 text-sm">다음</Button>
                  </div>
                </div>
              </Card>

            </div>
          </TabsContent>

          {/* 콘텐츠관리 탭 */}
          <TabsContent value="contents">
            <div className="space-y-6">
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-4">콘텐츠 통계</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-400">{contentStats?.by_type?.magazine || 0}</p>
                    <p className="text-gray-400 text-sm">매거진</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-400">{contentStats?.by_type?.notice || 0}</p>
                    <p className="text-gray-400 text-sm">공지사항</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-purple-400">{contentStats?.consultation_stats?.total || 0}</p>
                    <p className="text-gray-400 text-sm">상담</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-orange-400">{contentStats?.total_views?.toLocaleString() || 0}</p>
                    <p className="text-gray-400 text-sm">총 조회수</p>
                  </div>
                </div>
              </Card>

              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-4">콘텐츠 목록</h3>
                <div className="space-y-3">
                  {contents.map(content => (
                    <div key={content.id} className="flex items-center justify-between p-4 bg-white/10 rounded-xl border border-white/15 backdrop-blur-sm hover:bg-white/15 transition-all">
                      <div className="flex-1">
                        <h4 className="text-white font-medium">{content.title}</h4>
                        <p className="text-gray-400 text-sm">
                          {content.content_type} • {content.author_name} • 조회 {content.views}회
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          content.status === 'published' ? 'bg-green-600' :
                          content.status === 'draft' ? 'bg-yellow-500/80 backdrop-blur-sm' : 'bg-white/20 backdrop-blur-sm'
                        } text-white`}>
                          {content.status}
                        </span>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs">
                          편집
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* 알림관리 탭 */}
          <TabsContent value="notifications">
            <div className="space-y-6">
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-4">알림 발송</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-gray-400 text-sm mb-2">발송 대상</label>
                    <select className="w-full p-2 bg-white/10 border border-white/20 rounded backdrop-blur-sm text-white focus:bg-white/15 transition-all">
                      <option>전체 사용자</option>
                      <option>프리미엄 사용자</option>
                      <option>VIP 사용자</option>
                      <option>무료 사용자</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-gray-400 text-sm mb-2">발송 방식</label>
                    <select className="w-full p-2 bg-white/10 border border-white/20 rounded backdrop-blur-sm text-white focus:bg-white/15 transition-all">
                      <option>이메일</option>
                      <option>카카오톡</option>
                      <option>이메일 + 카카오톡</option>
                    </select>
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-gray-400 text-sm mb-2">메시지 내용</label>
                    <textarea 
                      className="w-full p-3 bg-white/10 border border-white/20 rounded backdrop-blur-sm text-white focus:bg-white/15 transition-all" 
                      rows={4}
                      placeholder="발송할 메시지를 입력하세요..."
                    />
                  </div>
                  <div className="md:col-span-2">
                    <button
                      onClick={() => {
                        const userIds = users.map(u => u.id);
                        sendBulkNotification(userIds, '테스트 메시지입니다', 'both');
                      }}
                      className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded"
                    >
                      <Bell className="w-4 h-4 inline mr-2" />
                      알림 발송
                    </button>
                  </div>
                </div>
              </Card>

              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-4">알림 통계</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-400">{notificationStats?.total_notifications || 0}</p>
                    <p className="text-gray-400 text-sm">총 발송</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-400">{notificationStats?.success_rate?.toFixed(1) || 0}%</p>
                    <p className="text-gray-400 text-sm">성공률</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-purple-400">{notificationStats?.type_distribution?.email || 0}</p>
                    <p className="text-gray-400 text-sm">이메일</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-orange-400">{notificationStats?.type_distribution?.kakao || 0}</p>
                    <p className="text-gray-400 text-sm">카카오톡</p>
                  </div>
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* 사주 시스템 개요 탭 */}
          <TabsContent value="saju-overview">
            {sajuLoading ? (
              <div className="flex items-center justify-center h-64">
                <RefreshCw className="w-6 h-6 animate-spin mr-2" />
                <span className="text-white">사주 설정을 불러오는 중...</span>
              </div>
            ) : !sajuSettings ? (
              <div className="flex items-center justify-center h-64">
                <AlertCircle className="w-6 h-6 text-red-500 mr-2" />
                <span className="text-white">설정을 불러올 수 없습니다.</span>
              </div>
            ) : (
              <div className="space-y-6">
                {/* 사주 설정 저장 버튼 */}
                <div className="flex justify-end">
                  <Button 
                    onClick={handleSajuSave} 
                    disabled={saving}
                    className="bg-purple-600 hover:bg-purple-700"
                  >
                    {saving ? (
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Save className="w-4 h-4 mr-2" />
                    )}
                    {saving ? '저장 중...' : '사주 설정 저장'}
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                    <h3 className="text-xl font-semibold text-white mb-4">시스템 정보</h3>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-300">버전:</span>
                        <span className="text-white font-mono">{sajuSettings.version}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-300">마지막 업데이트:</span>
                        <span className="text-white text-sm">
                          {new Date(sajuSettings.last_updated).toLocaleString('ko-KR')}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-300">업데이트자:</span>
                        <span className="text-white">{sajuSettings.updated_by}</span>
                      </div>
                    </div>
                  </Card>

                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                    <h3 className="text-xl font-semibold text-white mb-4">현재 설정 상태</h3>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-300">시두법 사용:</span>
                        <span className={`px-2 py-1 rounded text-sm ${sajuSettings.time_settings?.use_sidubup ? 'bg-green-600' : 'bg-red-600'}`}>
                          {sajuSettings.time_settings?.use_sidubup ? '활성' : '비활성'}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-300">KASI 정밀도:</span>
                        <span className={`px-2 py-1 rounded text-sm ${sajuSettings.logic_settings?.use_kasi_precision ? 'bg-green-600' : 'bg-red-600'}`}>
                          {sajuSettings.logic_settings?.use_kasi_precision ? '활성' : '비활성'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-300">기본 국가:</span>
                        <span className="text-white">{sajuSettings.geographic_settings?.default_country || 'KR'}</span>
                      </div>
                    </div>
                  </Card>
                </div>

                {/* 실시간 성능 지표 */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-transparent rounded-2xl"></div>
                    <div className="relative z-10">
                      <h4 className="text-white font-semibold mb-2">계산 속도</h4>
                      <p className="text-3xl font-bold text-blue-300">
                        {statsLoading ? '...' : (sajuStats?.performance?.calculation_speed || '0')}초
                      </p>
                      <p className="text-white/70 text-sm mt-1">평균 처리 시간</p>
                    </div>
                  </Card>

                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-green-500/20 to-transparent rounded-2xl"></div>
                    <div className="relative z-10">
                      <h4 className="text-white font-semibold mb-2">정확도</h4>
                      <p className="text-3xl font-bold text-green-300">
                        {statsLoading ? '...' : (sajuStats?.performance?.accuracy_rate || '0')}%
                      </p>
                      <p className="text-white/70 text-sm mt-1">AI 검증 통과율</p>
                    </div>
                  </Card>

                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 to-transparent rounded-2xl"></div>
                    <div className="relative z-10">
                      <h4 className="text-white font-semibold mb-2">오늘 계산</h4>
                      <p className="text-3xl font-bold text-purple-300">
                        {statsLoading ? '...' : (sajuStats?.usage?.total_calculations_today?.toLocaleString() || '0')}
                      </p>
                      <p className="text-white/70 text-sm mt-1">총 처리 건수</p>
                    </div>
                  </Card>

                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-orange-500/20 to-transparent rounded-2xl"></div>
                    <div className="relative z-10">
                      <h4 className="text-white font-semibold mb-2">활성 사용자</h4>
                      <p className="text-3xl font-bold text-orange-300">
                        {statsLoading ? '...' : (sajuStats?.usage?.active_users || '0')}
                      </p>
                      <p className="text-white/70 text-sm mt-1">현재 접속 중</p>
                    </div>
                  </Card>
                </div>

                {/* 최근 계산 로그 */}
                <div className="mt-8">
                  <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-2xl"></div>
                    <div className="relative z-10">
                      <h3 className="text-xl font-semibold text-white mb-4 drop-shadow-lg">🔍 최근 사주 계산 로그</h3>
                      <div className="space-y-3">
                        {calculationLogs.slice(0, 5).map(log => (
                          <div key={log.id} className="flex items-center justify-between p-4 bg-white/10 rounded-xl border border-white/15 backdrop-blur-sm">
                            <div className="flex-1">
                              <div className="flex items-center gap-3">
                                <span className={`w-3 h-3 rounded-full ${
                                  log.status === 'success' ? 'bg-green-400' :
                                  log.status === 'warning' ? 'bg-yellow-400' : 'bg-red-400'
                                }`}></span>
                                <span className="text-white font-medium">{log.calculation_type}</span>
                                <span className="text-white/70 text-sm">{log.user_id}</span>
                              </div>
                              <div className="mt-1 text-white/60 text-sm">
                                {log.birth_info.year}.{log.birth_info.month}.{log.birth_info.day} 
                                {log.birth_info.hour && ` ${log.birth_info.hour}:${log.birth_info.minute?.toString().padStart(2, '0')}`} 
                                • {log.processing_time}ms • 정확도 {log.accuracy_score}%
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="text-white/70 text-xs">{log.timestamp.split(' ')[1]}</span>
                              {log.ai_validated && <div className="text-green-400 text-xs">AI 검증</div>}
                              {log.error_message && <div className="text-red-400 text-xs">{log.error_message}</div>}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </Card>
                </div>
              </div>
            )}
          </TabsContent>

          {/* 사주 시간 설정 탭 */}
          <TabsContent value="saju-time">
            {!sajuSettings ? (
              <div className="flex items-center justify-center h-64">
                <AlertCircle className="w-6 h-6 text-red-500 mr-2" />
                <span className="text-white">설정을 불러올 수 없습니다.</span>
              </div>
            ) : (
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-6">시간 시스템 설정</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        시간 시스템
                      </label>
                      <select 
                        value={sajuSettings.time_settings?.timezone_system || 'standard'}
                        onChange={(e) => setSajuSettings({
                          ...sajuSettings,
                          time_settings: {
                            ...sajuSettings.time_settings,
                            timezone_system: e.target.value as 'standard' | 'apparent_solar'
                          }
                        })}
                        className="admin-select w-full p-2"
                      >
                        <option value="standard">표준시</option>
                        <option value="apparent_solar">진태양시</option>
                      </select>
                    </div>

                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-gray-300">
                        시두법 사용
                      </label>
                      <Switch
                        checked={sajuSettings.time_settings?.use_sidubup || false}
                        onCheckedChange={(checked) => setSajuSettings({
                          ...sajuSettings,
                          time_settings: {
                            ...sajuSettings.time_settings,
                            use_sidubup: checked
                          }
                        })}
                      />
                    </div>
                  </div>

                  <div className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-white/15">
                    <h4 className="text-white font-medium mb-3">시간 설정 설명</h4>
                    <div className="space-y-2 text-sm text-gray-300">
                      <p><strong>표준시:</strong> 국가별 표준 시간대 적용</p>
                      <p><strong>진태양시:</strong> 실제 태양의 위치 기준 시간</p>
                      <p><strong>시두법:</strong> 전통 명리학의 시간 보정 방법</p>
                    </div>
                  </div>
                </div>
              </Card>
            )}
          </TabsContent>

          {/* 사주 지역 설정 탭 */}
          <TabsContent value="saju-geographic">
            {!sajuSettings ? (
              <div className="flex items-center justify-center h-64">
                <AlertCircle className="w-6 h-6 text-red-500 mr-2" />
                <span className="text-white">설정을 불러올 수 없습니다.</span>
              </div>
            ) : (
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-6">지역 시스템 설정</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        기본 국가
                      </label>
                      <select 
                        value={sajuSettings.geographic_settings?.default_country || 'KR'}
                        onChange={(e) => setSajuSettings({
                          ...sajuSettings,
                          geographic_settings: {
                            ...sajuSettings.geographic_settings,
                            default_country: e.target.value as any
                          }
                        })}
                        className="admin-select w-full p-2"
                      >
                        <option value="KR">대한민국</option>
                        <option value="CN">중국</option>
                        <option value="JP">일본</option>
                        <option value="US">미국</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        시간대 오프셋 (시간)
                      </label>
                      <input 
                        type="number"
                        value={sajuSettings.geographic_settings?.timezone_offset || 9}
                        onChange={(e) => setSajuSettings({
                          ...sajuSettings,
                          geographic_settings: {
                            ...sajuSettings.geographic_settings,
                            timezone_offset: parseFloat(e.target.value) || 9
                          }
                        })}
                        className="admin-select w-full p-2"
                        step="0.5"
                        min="-12"
                        max="12"
                      />
                    </div>
                  </div>

                  <div className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-white/15">
                    <h4 className="text-white font-medium mb-3">지역 설정 안내</h4>
                    <div className="space-y-2 text-sm text-gray-300">
                      <p><strong>기본 국가:</strong> 사주 계산시 적용할 기본 국가</p>
                      <p><strong>시간대:</strong> 출생지 시간 계산의 기준</p>
                      <p><strong>위도/경도:</strong> 정밀한 시간 보정을 위해 사용</p>
                    </div>
                  </div>
                </div>
              </Card>
            )}
          </TabsContent>

          {/* 사주 논리 설정 탭 */}
          <TabsContent value="saju-logic">
            {!sajuSettings ? (
              <div className="flex items-center justify-center h-64">
                <AlertCircle className="w-6 h-6 text-red-500 mr-2" />
                <span className="text-white">설정을 불러올 수 없습니다.</span>
              </div>
            ) : (
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-6">사주 논리 시스템</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        논리 유형
                      </label>
                      <select 
                        value={safeGetLogicType(sajuSettings)}
                        onChange={(e) => {
                          const updatedSettings = safeUpdateLogicSettings(sajuSettings, {
                            logic_type: e.target.value as 'traditional' | 'modern' | 'hybrid'
                          });
                          setSajuSettings(updatedSettings);
                        }}
                        className="admin-select w-full p-2"
                      >
                        <option value="traditional">전통 논리</option>
                        <option value="modern">현대 논리</option>
                        <option value="hybrid">혼합 논리</option>
                      </select>
                    </div>

                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-gray-300">
                        KASI 정밀도 사용
                      </label>
                      <Switch
                        checked={sajuSettings.logic_settings?.use_kasi_precision || false}
                        onCheckedChange={(checked) => setSajuSettings({
                          ...sajuSettings,
                          logic_settings: {
                            ...sajuSettings.logic_settings,
                            use_kasi_precision: checked
                          }
                        })}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-gray-300">
                        AI 검증 사용
                      </label>
                      <Switch
                        checked={sajuSettings.logic_settings?.ai_validation || false}
                        onCheckedChange={(checked) => setSajuSettings({
                          ...sajuSettings,
                          logic_settings: {
                            ...sajuSettings.logic_settings,
                            ai_validation: checked
                          }
                        })}
                      />
                    </div>
                  </div>

                  <div className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-white/15">
                    <h4 className="text-white font-medium mb-3">논리 시스템 설명</h4>
                    <div className="space-y-2 text-sm text-gray-300">
                      <p><strong>전통 논리:</strong> 고전 명리학 기반</p>
                      <p><strong>현대 논리:</strong> 현대적 해석 적용</p>
                      <p><strong>혼합 논리:</strong> 전통과 현대의 조화</p>
                      <p><strong>KASI 정밀도:</strong> 한국천문연구원 데이터 활용</p>
                    </div>
                  </div>
                </div>
              </Card>
            )}
          </TabsContent>

          {/* 커뮤니티 관리 탭 */}
          <TabsContent value="community">
            <div className="space-y-6">
              
              {/* 커뮤니티 개요 통계 */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">총 매거진</p>
                      <p className="text-3xl font-bold text-white">127</p>
                    </div>
                    <FileText className="w-8 h-8 text-blue-400" />
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">미답변 상담</p>
                      <p className="text-3xl font-bold text-orange-400">23</p>
                    </div>
                    <MessageSquare className="w-8 h-8 text-orange-400" />
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">승인 대기 리뷰</p>
                      <p className="text-3xl font-bold text-yellow-400">12</p>
                    </div>
                    <AlertCircle className="w-8 h-8 text-yellow-400" />
                  </div>
                </Card>
                
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/70 text-sm font-medium">활성 공지사항</p>
                      <p className="text-3xl font-bold text-green-400">8</p>
                    </div>
                    <Bell className="w-8 h-8 text-green-400" />
                  </div>
                </Card>
              </div>

              {/* 커뮤니티 관리 섹션 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* 매거진 관리 */}
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-white">매거진 관리</h3>
                    <Button className="btn-cosmic px-4 py-2 text-sm">
                      새 매거진 작성
                    </Button>
                  </div>
                  
                  <div className="space-y-3">
                    {[
                      { title: "2025년 운세 대예측", status: "발행됨", views: 1234, date: "2025-08-28" },
                      { title: "사주로 보는 연애운", status: "검토중", views: 0, date: "2025-08-27" },
                      { title: "12지신별 성격 분석", status: "초안", views: 0, date: "2025-08-26" }
                    ].map((article, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex-1">
                          <h4 className="text-white font-medium">{article.title}</h4>
                          <div className="flex items-center gap-4 mt-1">
                            <span className={`text-xs px-2 py-1 rounded ${
                              article.status === '발행됨' ? 'bg-green-400/20 text-green-400' :
                              article.status === '검토중' ? 'bg-yellow-400/20 text-yellow-400' :
                              'bg-gray-400/20 text-gray-400'
                            }`}>
                              {article.status}
                            </span>
                            <span className="text-xs text-gray-400">{article.views} 조회</span>
                            <span className="text-xs text-gray-400">{article.date}</span>
                          </div>
                        </div>
                        <Button className="text-xs text-white/70 hover:text-white">
                          편집
                        </Button>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* 1:1 상담 관리 */}
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-white">1:1 상담 관리</h3>
                    <div className="flex gap-2">
                      <Button className="btn-outline px-3 py-1 text-xs">
                        전체
                      </Button>
                      <Button className="btn-cosmic px-3 py-1 text-xs">
                        미답변만
                      </Button>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    {[
                      { user: "김○○", type: "프리미엄 사주", status: "미답변", priority: "높음", date: "08-29", responses: 0 },
                      { user: "이○○", type: "궁합 분석", status: "답변완료", priority: "보통", date: "08-28", responses: 2 },
                      { user: "박○○", type: "타로 리딩", status: "진행중", priority: "낮음", date: "08-28", responses: 1 }
                    ].map((consultation, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex-1">
                          <div className="flex items-center gap-3">
                            <h4 className="text-white font-medium">{consultation.user}</h4>
                            <span className="text-xs px-2 py-1 bg-blue-400/20 text-blue-400 rounded">
                              {consultation.type}
                            </span>
                          </div>
                          <div className="flex items-center gap-4 mt-1">
                            <span className={`text-xs px-2 py-1 rounded ${
                              consultation.status === '미답변' ? 'bg-red-400/20 text-red-400' :
                              consultation.status === '답변완료' ? 'bg-green-400/20 text-green-400' :
                              'bg-yellow-400/20 text-yellow-400'
                            }`}>
                              {consultation.status}
                            </span>
                            <span className={`text-xs px-2 py-1 rounded ${
                              consultation.priority === '높음' ? 'bg-red-400/20 text-red-400' :
                              consultation.priority === '보통' ? 'bg-yellow-400/20 text-yellow-400' :
                              'bg-green-400/20 text-green-400'
                            }`}>
                              {consultation.priority}
                            </span>
                            <span className="text-xs text-gray-400">{consultation.date}</span>
                            <button 
                              className={`text-xs px-2 py-1 rounded border ${
                                consultation.responses > 0 
                                  ? 'border-blue-400 text-blue-400 hover:bg-blue-400/10' 
                                  : 'border-gray-400 text-gray-400'
                              }`}
                              onClick={() => {
                                if (consultation.responses > 0) {
                                  // 레이어 팝업 열기 로직 (추후 구현)
                                  alert(`${consultation.user}님의 상담 이력 ${consultation.responses}개`);
                                }
                              }}
                            >
                              {consultation.responses}
                            </button>
                          </div>
                        </div>
                        <Button className="text-xs text-white/70 hover:text-white">
                          답변
                        </Button>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>

              {/* 공지사항 & 리뷰 관리 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* 공지사항 관리 */}
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-white">공지사항</h3>
                    <Button className="btn-cosmic px-4 py-2 text-sm">
                      공지 작성
                    </Button>
                  </div>
                  
                  <div className="space-y-3">
                    {[
                      { title: "시스템 점검 안내", type: "긴급", pinned: true, date: "08-29" },
                      { title: "추석 연휴 서비스 안내", type: "일반", pinned: false, date: "08-28" },
                      { title: "새로운 기능 업데이트", type: "일반", pinned: true, date: "08-27" }
                    ].map((notice, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            {notice.pinned && <span className="text-yellow-400">📌</span>}
                            <h4 className="text-white font-medium">{notice.title}</h4>
                          </div>
                          <div className="flex items-center gap-3 mt-1">
                            <span className={`text-xs px-2 py-1 rounded ${
                              notice.type === '긴급' ? 'bg-red-400/20 text-red-400' : 'bg-blue-400/20 text-blue-400'
                            }`}>
                              {notice.type}
                            </span>
                            <span className="text-xs text-gray-400">{notice.date}</span>
                          </div>
                        </div>
                        <Button className="text-xs text-white/70 hover:text-white">
                          편집
                        </Button>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* 리뷰 관리 */}
                <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-white">리뷰 관리</h3>
                    <div className="flex gap-2">
                      <Button className="btn-outline px-3 py-1 text-xs">
                        전체
                      </Button>
                      <Button className="btn-cosmic px-3 py-1 text-xs">
                        승인 대기
                      </Button>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    {[
                      { user: "정○○", service: "기본 사주", rating: 5, status: "승인", featured: true, date: "08-29" },
                      { user: "최○○", service: "타로 리딩", rating: 4, status: "대기", featured: false, date: "08-28" },
                      { user: "한○○", service: "프리미엄 사주", rating: 5, status: "승인", featured: false, date: "08-27" }
                    ].map((review, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex-1">
                          <div className="flex items-center gap-3">
                            <h4 className="text-white font-medium">{review.user}</h4>
                            <div className="flex text-yellow-400">
                              {Array.from({ length: 5 }, (_, i) => (
                                <span key={i}>{i < review.rating ? '★' : '☆'}</span>
                              ))}
                            </div>
                            {review.featured && <span className="text-xs px-2 py-1 bg-purple-400/20 text-purple-400 rounded">베스트</span>}
                          </div>
                          <div className="flex items-center gap-4 mt-1">
                            <span className="text-xs px-2 py-1 bg-gray-400/20 text-gray-400 rounded">
                              {review.service}
                            </span>
                            <span className={`text-xs px-2 py-1 rounded ${
                              review.status === '승인' ? 'bg-green-400/20 text-green-400' : 'bg-yellow-400/20 text-yellow-400'
                            }`}>
                              {review.status}
                            </span>
                            <span className="text-xs text-gray-400">{review.date}</span>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          {review.status === '대기' && (
                            <>
                              <Button className="text-xs px-3 py-1 bg-green-400/20 text-green-400 hover:bg-green-400/30">
                                승인
                              </Button>
                              <Button className="text-xs px-3 py-1 bg-red-400/20 text-red-400 hover:bg-red-400/30">
                                거부
                              </Button>
                            </>
                          )}
                          <Button className="text-xs text-white/70 hover:text-white">
                            상세
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>

            </div>
          </TabsContent>

          {/* 포인트/캐시 관리 탭 */}
          <TabsContent value="point-cash">
            <div className="space-y-6">
              
              {/* 💰 포인트 정책 관리 */}
              <Card className="backdrop-blur-xl bg-white/10 p-8 border border-white/20 rounded-3xl shadow-2xl relative overflow-hidden">
                {/* 배경 장식 */}
                <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/10 to-orange-500/10 rounded-3xl"></div>
                <div className="absolute top-4 right-4 w-16 h-16 bg-yellow-400/20 rounded-full blur-xl"></div>
                
                <div className="relative z-10">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h3 className="text-2xl font-bold text-white mb-2 flex items-center gap-3">
                        <div className="p-2 bg-yellow-400/20 rounded-lg">
                          <Coins className="w-6 h-6 text-yellow-300" />
                        </div>
                        💰 포인트 정책 관리
                      </h3>
                      <p className="text-white/70">사용자 포인트 적립 및 소모 정책을 설정하고 관리합니다</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-white/60">현재 총 포인트</p>
                      <p className="text-2xl font-bold text-yellow-300">12,345,678 P</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                    {/* 📈 포인트 적립 정책 */}
                    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                      <h4 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                        📈 적립 정책
                      </h4>
                      <p className="text-white/60 text-sm mb-6">사용자 활동에 따른 포인트 적립 규칙을 설정합니다</p>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          가입 보너스
                        </label>
                        <input 
                          type="number"
                          placeholder="1000"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          일일 로그인
                        </label>
                        <input 
                          type="number"
                          placeholder="50"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          첫 콘텐츠 이용
                        </label>
                        <input 
                          type="number"
                          placeholder="200"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          리뷰 작성
                        </label>
                        <input 
                          type="number"
                          placeholder="100"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          콘텐츠 공유
                        </label>
                        <input 
                          type="number"
                          placeholder="30"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          추천인 보너스
                        </label>
                        <input 
                          type="number"
                          placeholder="500"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                    </div>
                  </div>

                    {/* 📉 포인트 소모 정책 */}
                    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                      <h4 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                        <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                        📉 소모 정책
                      </h4>
                      <p className="text-white/60 text-sm mb-6">서비스 이용 시 필요한 포인트 금액을 설정합니다</p>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          기본 사주
                        </label>
                        <input 
                          type="number"
                          placeholder="100"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          프리미엄 사주
                        </label>
                        <input 
                          type="number"
                          placeholder="300"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          궁합 분석
                        </label>
                        <input 
                          type="number"
                          placeholder="200"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          타로 리딩
                        </label>
                        <input 
                          type="number"
                          placeholder="150"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          꿈풀이
                        </label>
                        <input 
                          type="number"
                          placeholder="80"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          개인 상담
                        </label>
                        <input 
                          type="number"
                          placeholder="500"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* 포인트 제한 설정 */}
                <div className="mt-6 pt-6 border-t border-white/10">
                  <h4 className="text-lg font-medium text-white mb-4">제한 및 유효기간</h4>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        포인트 유효기간 (일)
                      </label>
                      <input 
                        type="number"
                        placeholder="365"
                        className="admin-input w-full p-2"
                        min="1"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        일일 적립 한도
                      </label>
                      <input 
                        type="number"
                        placeholder="1000"
                        className="admin-input w-full p-2"
                        min="0"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        일일 사용 한도
                      </label>
                      <input 
                        type="number"
                        placeholder="5000"
                        className="admin-input w-full p-2"
                        min="0"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        최소 사용 포인트
                      </label>
                      <input 
                        type="number"
                        placeholder="10"
                        className="admin-input w-full p-2"
                        min="1"
                      />
                    </div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* 💳 캐시 정책 관리 */}
              <Card className="backdrop-blur-xl bg-white/10 p-8 border border-white/20 rounded-3xl shadow-2xl relative overflow-hidden">
                {/* 배경 장식 */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-3xl"></div>
                <div className="absolute top-4 right-4 w-16 h-16 bg-blue-400/20 rounded-full blur-xl"></div>
                
                <div className="relative z-10">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h3 className="text-2xl font-bold text-white mb-2 flex items-center gap-3">
                        <div className="p-2 bg-blue-400/20 rounded-lg">
                          <CreditCard className="w-6 h-6 text-blue-300" />
                        </div>
                        💳 캐시 정책 관리
                      </h3>
                      <p className="text-white/70">현금 충전 및 결제 정책을 설정하고 관리합니다</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-white/60">현재 총 캐시</p>
                      <p className="text-2xl font-bold text-blue-300">98,765,432원</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                    {/* 💰 충전 정책 */}
                    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                      <h4 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                        💰 충전 정책
                      </h4>
                      <p className="text-white/60 text-sm mb-6">캐시 충전 금액 및 보너스 정책을 설정합니다</p>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          최소 충전 금액 (원)
                        </label>
                        <input 
                          type="number"
                          placeholder="1000"
                          className="admin-input w-full p-2"
                          min="0"
                          step="1000"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          최대 충전 금액 (원)
                        </label>
                        <input 
                          type="number"
                          placeholder="100000"
                          className="admin-input w-full p-2"
                          min="0"
                          step="1000"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        충전 보너스율 설정
                      </label>
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <input 
                            type="number"
                            placeholder="10000"
                            className="admin-input flex-1 p-2"
                            min="0"
                          />
                          <span className="text-gray-300">원 이상 충전시</span>
                          <input 
                            type="number"
                            placeholder="5"
                            className="admin-input w-20 p-2"
                            min="0"
                            max="100"
                          />
                          <span className="text-gray-300">% 보너스</span>
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <input 
                            type="number"
                            placeholder="50000"
                            className="admin-input flex-1 p-2"
                            min="0"
                          />
                          <span className="text-gray-300">원 이상 충전시</span>
                          <input 
                            type="number"
                            placeholder="10"
                            className="admin-input w-20 p-2"
                            min="0"
                            max="100"
                          />
                          <span className="text-gray-300">% 보너스</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* 환불 및 교환 정책 */}
                  <div className="space-y-4">
                    <h4 className="text-lg font-medium text-white mb-3">환불 및 교환</h4>
                    
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-300">
                          환불 허용
                        </label>
                        <Switch 
                          checked={refundEnabled}
                          onCheckedChange={setRefundEnabled}
                        />
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            환불 수수료율 (%)
                          </label>
                          <input 
                            type="number"
                            placeholder="5"
                            className="admin-input w-full p-2"
                            min="0"
                            max="100"
                            step="0.1"
                          />
                        </div>
                        
                        <div>
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            환불 신청 기한 (일)
                          </label>
                          <input 
                            type="number"
                            placeholder="7"
                            className="admin-input w-full p-2"
                            min="1"
                          />
                        </div>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          캐시 → 포인트 환율
                        </label>
                        <div className="flex items-center gap-2">
                          <input 
                            type="number"
                            placeholder="1"
                            className="admin-input flex-1 p-2"
                            min="0"
                            step="0.01"
                          />
                          <span className="text-gray-300">원당</span>
                          <input 
                            type="number"
                            placeholder="1"
                            className="admin-input flex-1 p-2"
                            min="0"
                            step="0.01"
                          />
                          <span className="text-gray-300">포인트</span>
                        </div>
                      </div>
                    </div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* 운영 정책 관리 */}
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  운영 정책 관리
                </h3>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* 서비스 운영 정책 */}
                  <div className="space-y-4">
                    <h4 className="text-lg font-medium text-white mb-3">서비스 정책</h4>
                    
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-300">
                          무료 체험 제공
                        </label>
                        <Switch 
                          checked={freeTrialEnabled}
                          onCheckedChange={setFreeTrialEnabled}
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          무료 체험 횟수
                        </label>
                        <input 
                          type="number"
                          placeholder="3"
                          className="admin-input w-full p-2"
                          min="0"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-300">
                          비회원 접근 허용
                        </label>
                        <Switch 
                          checked={guestAccessEnabled}
                          onCheckedChange={setGuestAccessEnabled}
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-300">
                          점검 모드
                        </label>
                        <Switch 
                          checked={maintenanceMode}
                          onCheckedChange={setMaintenanceMode}
                        />
                      </div>
                    </div>
                  </div>

                  {/* 보안 정책 */}
                  <div className="space-y-4">
                    <h4 className="text-lg font-medium text-white mb-3">보안 정책</h4>
                    
                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          의심 활동 임계값
                        </label>
                        <input 
                          type="number"
                          placeholder="10"
                          className="admin-input w-full p-2"
                          min="1"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-300">
                          자동 차단 활성화
                        </label>
                        <Switch 
                          checked={autoBlockEnabled}
                          onCheckedChange={setAutoBlockEnabled}
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          최대 실패 시도 횟수
                        </label>
                        <input 
                          type="number"
                          placeholder="5"
                          className="admin-input w-full p-2"
                          min="1"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          임시 차단 시간 (시간)
                        </label>
                        <input 
                          type="number"
                          placeholder="24"
                          className="admin-input w-full p-2"
                          min="1"
                        />
                      </div>
                    </div>
                  </div>

                  {/* 고객 지원 */}
                  <div className="space-y-4">
                    <h4 className="text-lg font-medium text-white mb-3">고객 지원</h4>
                    
                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          지원 시간
                        </label>
                        <select className="admin-select w-full p-2">
                          <option value="24/7">24시간 연중무휴</option>
                          <option value="9-18">평일 9시~18시</option>
                          <option value="9-21">평일 9시~21시</option>
                          <option value="weekend">주말 포함</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          응답 시간 목표 (시간)
                        </label>
                        <input 
                          type="number"
                          placeholder="24"
                          className="admin-input w-full p-2"
                          min="1"
                        />
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-300">
                          자동 응답 활성화
                        </label>
                        <Switch 
                          checked={autoResponseEnabled}
                          onCheckedChange={setAutoResponseEnabled}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* 통계 및 모니터링 */}
              <Card className="backdrop-blur-xl bg-white/10 p-6 border border-white/20 rounded-2xl shadow-2xl">
                <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  통계 및 모니터링
                </h3>
                
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold text-green-400">₩1,234,567</div>
                    <div className="text-sm text-gray-300">일일 매출</div>
                  </div>
                  
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold text-blue-400">123,456P</div>
                    <div className="text-sm text-gray-300">발행 포인트</div>
                  </div>
                  
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold text-purple-400">98,765P</div>
                    <div className="text-sm text-gray-300">사용 포인트</div>
                  </div>
                  
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold text-cyan-400">1,234명</div>
                    <div className="text-sm text-gray-300">활성 사용자</div>
                  </div>
                </div>

                <div className="flex justify-between items-center">
                  <div className="flex gap-2">
                    <button className="btn-cosmic px-4 py-2 text-sm">
                      정책 저장
                    </button>
                    <button className="btn-outline px-4 py-2 text-sm">
                      초기화
                    </button>
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm text-gray-300">
                    <AlertCircle className="w-4 h-4" />
                    <span>마지막 업데이트: 방금 전</span>
                  </div>
                </div>
              </Card>

            </div>
          </TabsContent>

        </Tabs>
      </div>
    </div>
  );
};

export default IntegratedAdminDashboard;