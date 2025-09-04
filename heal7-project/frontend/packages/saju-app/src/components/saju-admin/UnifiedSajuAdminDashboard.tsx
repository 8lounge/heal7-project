/**
 * 🔮 HEAL7 사주 관리자 통합 대시보드 
 * Phase 1 리팩토링: 중복 컴포넌트 통합 및 기술 부채 해결
 * 
 * 기능:
 * - 7개 탭 구조 (대시보드, 사주엔진, 사용자관리, 콘텐츠관리, 통계분석, 포인트, 시스템)
 * - 점진적 백엔드 연동 (Phase 2에서 완료 예정)
 * - 무중단 서비스 보장
 * - 코드 품질 A등급 달성
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@heal7/shared';
import { Button } from '@heal7/shared';
import { Badge } from '@heal7/shared';
import { Progress } from '@heal7/shared';
import { 
  Users, 
  Activity, 
  Database, 
  Server, 
  AlertCircle, 
  CheckCircle,
  Clock,
  BarChart3,
  Settings,
  RefreshCw,
  Star,
  TrendingUp,
  Calendar,
  Shield,
  Zap,
  FileText,
  Globe,
  Heart,
  Sparkles,
  Brain,
  UserCheck,
  ImageIcon,
  CreditCard,
  DollarSign,
  Trash2,
  Edit,
  Plus,
  Save,
  Download,
  Upload,
  Search,
  Filter,
  HardDrive,
  MemoryStick,
  Coins,
  Receipt,
  Wrench,
  Bookmark,
  Hash,
  Tag,
  BookOpen,
  PenTool,
  Palette
} from 'lucide-react';

// 통합 타입 정의 (기존 두 컴포넌트에서 병합)
interface SajuEngineStatus {
  calculation_accuracy: number;
  total_calculations: number;
  avg_response_time: number;
  error_rate: number;
  active_algorithms: string[];
}

interface UserStats {
  total_users: number;
  active_today: number;
  premium_users: number;
  new_signups: number;
  retention_rate: number;
}

interface ContentStats {
  total_interpretations: number;
  zodiac_images: number;
  dream_interpretations: number;
  fortune_texts: number;
  last_updated: string;
  // 사주 해석 카테고리
  gapja_60: number;
  heavenly_stems: number;
  earthly_branches: number;
  hidden_stems: number;
  five_elements: number;
  destiny_patterns: number;
  compatibility_data: number;
}

interface SystemHealth {
  api_status: 'healthy' | 'warning' | 'critical';
  database_status: 'healthy' | 'warning' | 'critical';
  response_time: number;
  uptime: number;
  memory_usage: number;
  cpu_usage: number;
}

interface AnalyticsData {
  popular_features: Array<{
    name: string;
    usage_count: number;
    growth_rate: number;
  }>;
  daily_active_users: number;
  peak_hours: string[];
  conversion_rate: number;
}

interface InterpretationData {
  id: string;
  category: string;
  title: string;
  content: string;
  quality_score: number;
  created_at: string;
  updated_at: string;
  author: string;
}

interface PointSystemData {
  total_points_issued: number;
  total_points_used: number;
  remaining_points: number;
  daily_transactions: number;
  success_rate: number;
  payment_methods: {
    card: number;
    bank_transfer: number;
    virtual_account: number;
  };
}

const UnifiedSajuAdminDashboard: React.FC = () => {
  // 통합 상태 관리
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sajuEngine, setSajuEngine] = useState<SajuEngineStatus | null>(null);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [contentStats, setContentStats] = useState<ContentStats | null>(null);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [interpretationData, setInterpretationData] = useState<InterpretationData[]>([]);
  const [pointSystem, setPointSystem] = useState<PointSystemData | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [refreshing, setRefreshing] = useState(false);

  // Phase 1: 목업 데이터 (Phase 2에서 실제 API로 교체 예정)
  const initializeData = useCallback(async () => {
    try {
      setLoading(true);
      
      // TODO: Phase 2에서 실제 API 호출로 교체
      // 현재는 서비스 중단 방지를 위한 목업 데이터 유지
      
      setSajuEngine({
        calculation_accuracy: 97.8,
        total_calculations: 125847,
        avg_response_time: 0.34,
        error_rate: 0.12,
        active_algorithms: ['천간지지 매칭', '오행 순환', '격국 분석', '궁합 계산']
      });

      setUserStats({
        total_users: 15847,
        active_today: 3245,
        premium_users: 1892,
        new_signups: 542,
        retention_rate: 68.5
      });

      setContentStats({
        total_interpretations: 8421,
        zodiac_images: 12,
        dream_interpretations: 1188,
        fortune_texts: 2847,
        last_updated: new Date().toISOString(),
        gapja_60: 60,
        heavenly_stems: 10,
        earthly_branches: 12,
        hidden_stems: 156,
        five_elements: 25,
        destiny_patterns: 48,
        compatibility_data: 144
      });

      setSystemHealth({
        api_status: 'healthy',
        database_status: 'healthy',
        response_time: 124,
        uptime: 99.97,
        memory_usage: 67.3,
        cpu_usage: 23.8
      });

      setAnalytics({
        popular_features: [
          { name: '사주분석', usage_count: 45231, growth_rate: 12.3 },
          { name: '12띠운세', usage_count: 38947, growth_rate: 8.7 },
          { name: '꿈풀이', usage_count: 29384, growth_rate: 15.2 },
          { name: '궁합분석', usage_count: 21673, growth_rate: 6.8 }
        ],
        daily_active_users: 3245,
        peak_hours: ['20:00-22:00', '12:00-14:00'],
        conversion_rate: 4.2
      });

      setPointSystem({
        total_points_issued: 2847593,
        total_points_used: 2203847,
        remaining_points: 643746,
        daily_transactions: 1847,
        success_rate: 98.4,
        payment_methods: {
          card: 67,
          bank_transfer: 23,
          virtual_account: 10
        }
      });

      const mockInterpretations: InterpretationData[] = [
        {
          id: '1',
          category: '60갑자',
          title: '갑자(甲子) 해석',
          content: '하늘의 갑목과 땅의 자수가 만나는 조합...',
          quality_score: 9.2,
          created_at: '2024-09-01T10:00:00Z',
          updated_at: '2024-09-03T14:30:00Z',
          author: '사주전문가1'
        },
        {
          id: '2',
          category: '천간',
          title: '갑목(甲木) 성격',
          content: '큰 나무의 기운을 가진 갑목은...',
          quality_score: 8.9,
          created_at: '2024-09-02T11:00:00Z',
          updated_at: '2024-09-03T15:00:00Z',
          author: '사주전문가2'
        },
        {
          id: '3',
          category: '지지',
          title: '자수(子水) 해석',
          content: '겨울의 차가운 물 기운...',
          quality_score: 8.7,
          created_at: '2024-09-01T16:00:00Z',
          updated_at: '2024-09-03T16:00:00Z',
          author: '사주전문가3'
        }
      ];
      
      setInterpretationData(mockInterpretations);
      setLastUpdate(new Date());
      
    } catch (error) {
      console.error('데이터 초기화 실패:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  // 데이터 새로고침
  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    await initializeData();
    setRefreshing(false);
  }, [initializeData]);

  // 초기 데이터 로드
  useEffect(() => {
    initializeData();
  }, [initializeData]);

  // 자동 새로고침 (30초마다)
  useEffect(() => {
    const interval = setInterval(() => {
      handleRefresh();
    }, 30000);

    return () => clearInterval(interval);
  }, [handleRefresh]);

  // 탭 메뉴 구성
  const tabMenus = useMemo(() => [
    { id: 'dashboard', label: '대시보드', icon: BarChart3, description: '시스템 현황' },
    { id: 'saju-engine', label: '사주엔진', icon: Brain, description: '사주 해석 시스템' },
    { id: 'users', label: '사용자관리', icon: Users, description: '회원 및 권한 관리' },
    { id: 'content', label: '콘텐츠관리', icon: FileText, description: '해석 데이터 관리' },
    { id: 'analytics', label: '통계분석', icon: TrendingUp, description: '사용량 분석' },
    { id: 'points', label: '포인트', icon: CreditCard, description: '결제 및 포인트' },
    { id: 'system', label: '시스템', icon: Settings, description: '시스템 관리' }
  ], []);

  // 상태 색상 헬퍼
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-400';
      case 'warning': return 'text-yellow-400';
      case 'critical': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-500/20';
      case 'warning': return 'bg-yellow-500/20';
      case 'critical': return 'bg-red-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-950 via-blue-900 to-indigo-950 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 border-4 border-purple-400 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-white/80">관리자 대시보드 로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-950 via-blue-900 to-indigo-950">
      {/* 헤더 */}
      <header className="border-b border-white/10 bg-black/20 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Sparkles className="w-8 h-8 text-purple-400" />
              <div>
                <h1 className="text-xl font-bold text-white">🔮 HEAL7 사주 관리자</h1>
                <p className="text-sm text-white/60">통합 관리 대시보드 v2.0</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-400 border-green-400">
                서비스 정상 운영 중
              </Badge>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleRefresh}
                disabled={refreshing}
                className="text-white border-white/20 hover:bg-white/10"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
                {refreshing ? '새로고침 중...' : '새로고침'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-6">
        {/* 탭 네비게이션 */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2">
            {tabMenus.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    flex items-center space-x-2 px-4 py-3 rounded-lg transition-all duration-200
                    ${activeTab === tab.id 
                      ? 'bg-purple-500/80 text-white shadow-lg shadow-purple-500/25' 
                      : 'bg-white/10 text-white/70 hover:bg-white/20 hover:text-white'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* 탭 콘텐츠 */}
        <div className="space-y-6">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white mb-6">시스템 대시보드</h2>
              
              {/* 시스템 상태 카드들 */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* 사주 엔진 상태 */}
                <Card className="bg-white/10 border-white/20 backdrop-blur-md">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-white/80">사주 엔진</CardTitle>
                    <Brain className="h-4 w-4 text-purple-400" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-white">{sajuEngine?.calculation_accuracy}%</div>
                    <p className="text-xs text-white/60">계산 정확도</p>
                    <div className="mt-2">
                      <div className="text-xs text-white/60 mb-1">총 계산: {sajuEngine?.total_calculations?.toLocaleString()}</div>
                      <Progress value={sajuEngine?.calculation_accuracy} className="h-2" />
                    </div>
                  </CardContent>
                </Card>

                {/* 사용자 통계 */}
                <Card className="bg-white/10 border-white/20 backdrop-blur-md">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-white/80">활성 사용자</CardTitle>
                    <Users className="h-4 w-4 text-blue-400" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-white">{userStats?.active_today?.toLocaleString()}</div>
                    <p className="text-xs text-white/60">오늘 활동 중</p>
                    <div className="mt-2">
                      <div className="text-xs text-white/60 mb-1">총 사용자: {userStats?.total_users?.toLocaleString()}</div>
                      <Progress value={(userStats?.active_today || 0) / (userStats?.total_users || 1) * 100} className="h-2" />
                    </div>
                  </CardContent>
                </Card>

                {/* 시스템 상태 */}
                <Card className="bg-white/10 border-white/20 backdrop-blur-md">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-white/80">시스템 상태</CardTitle>
                    <Server className="h-4 w-4 text-green-400" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-white">{systemHealth?.uptime}%</div>
                    <p className="text-xs text-white/60">가동률</p>
                    <div className="mt-2">
                      <div className="flex justify-between text-xs">
                        <span className={getStatusColor(systemHealth?.api_status || '')}>API</span>
                        <span className={getStatusColor(systemHealth?.database_status || '')}>DB</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* 콘텐츠 통계 */}
                <Card className="bg-white/10 border-white/20 backdrop-blur-md">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-white/80">콘텐츠</CardTitle>
                    <FileText className="h-4 w-4 text-orange-400" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-white">{contentStats?.total_interpretations?.toLocaleString()}</div>
                    <p className="text-xs text-white/60">총 해석 데이터</p>
                    <div className="mt-2">
                      <div className="text-xs text-white/60">꿈풀이: {contentStats?.dream_interpretations}</div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* 최근 활동 및 시스템 메트릭 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="bg-white/10 border-white/20 backdrop-blur-md">
                  <CardHeader>
                    <CardTitle className="text-white">인기 기능</CardTitle>
                    <CardDescription className="text-white/60">사용량 기준 순위</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {analytics?.popular_features.map((feature, index) => (
                        <div key={feature.name} className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className={`w-2 h-2 rounded-full ${
                              index === 0 ? 'bg-yellow-400' :
                              index === 1 ? 'bg-gray-300' :
                              index === 2 ? 'bg-orange-400' : 'bg-purple-400'
                            }`} />
                            <span className="text-white text-sm">{feature.name}</span>
                          </div>
                          <div className="text-right">
                            <div className="text-white text-sm font-medium">
                              {feature.usage_count.toLocaleString()}
                            </div>
                            <div className={`text-xs ${
                              feature.growth_rate > 0 ? 'text-green-400' : 'text-red-400'
                            }`}>
                              {feature.growth_rate > 0 ? '+' : ''}{feature.growth_rate}%
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-white/10 border-white/20 backdrop-blur-md">
                  <CardHeader>
                    <CardTitle className="text-white">시스템 리소스</CardTitle>
                    <CardDescription className="text-white/60">실시간 사용률</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-white/80">메모리 사용률</span>
                          <span className="text-white">{systemHealth?.memory_usage}%</span>
                        </div>
                        <Progress value={systemHealth?.memory_usage} className="h-2" />
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-white/80">CPU 사용률</span>
                          <span className="text-white">{systemHealth?.cpu_usage}%</span>
                        </div>
                        <Progress value={systemHealth?.cpu_usage} className="h-2" />
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-white/80">응답 시간</span>
                          <span className="text-white">{systemHealth?.response_time}ms</span>
                        </div>
                        <Progress value={Math.max(0, 100 - (systemHealth?.response_time || 0) / 10)} className="h-2" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {/* 다른 탭들도 동일한 패턴으로 구현 예정 (Phase 1에서 점진적 완성) */}
          {activeTab !== 'dashboard' && (
            <div className="text-center py-12">
              <div className="text-white/60 mb-4">
                <Settings className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-medium mb-2">{tabMenus.find(tab => tab.id === activeTab)?.label} 개발 중</h3>
                <p>Phase 1 리팩토링 후 Phase 2에서 완성 예정입니다.</p>
              </div>
              <Button 
                variant="outline" 
                onClick={() => setActiveTab('dashboard')}
                className="text-white border-white/20 hover:bg-white/10"
              >
                대시보드로 돌아가기
              </Button>
            </div>
          )}
        </div>

        {/* 하단 상태바 */}
        <div className="mt-8 pt-6 border-t border-white/10">
          <div className="flex items-center justify-between text-sm text-white/60">
            <div>
              마지막 업데이트: {lastUpdate.toLocaleString()}
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>서비스 정상</span>
              </div>
              <div>
                Phase 1 통합 완료 - 기술 부채 해결 진행 중
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UnifiedSajuAdminDashboard;