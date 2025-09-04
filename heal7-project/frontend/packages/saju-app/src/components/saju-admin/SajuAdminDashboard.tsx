/**
 * 🔮 HEAL7 사주 관리자 대시보드 
 * ⚠️ DEPRECATED: 이 파일은 UnifiedSajuAdminDashboard.tsx로 통합 예정
 * 
 * Phase 1 리팩토링 진행 중:
 * - 중복 코드 제거
 * - 기술 부채 해결  
 * - 무중단 서비스 보장
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@heal7/shared';
import { Button } from '@heal7/shared';
import { Badge } from '@heal7/shared';
// Removed Tabs system - using conditional rendering instead
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

// 타입 정의
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
  // 사주 해석 카테고리 추가
  gapja_60: number;  // 60갑자
  heavenly_stems: number;  // 천간 10개
  earthly_branches: number;  // 지지 12개
  hidden_stems: number;  // 지장간
  five_elements: number;  // 오행
  destiny_patterns: number;  // 격국
  compatibility_data: number;  // 궁합
}

interface SystemHealth {
  api_status: 'healthy' | 'warning' | 'critical';
  database_status: 'healthy' | 'warning' | 'critical';
  response_time: number;
  uptime: number;
  memory_usage: number;
  cpu_usage: number;
  redis_status: 'healthy' | 'warning' | 'critical';
  cache_hit_rate: number;
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

// 포인트 관리 타입 추가
interface PointStats {
  total_points_issued: number;
  total_points_used: number;
  active_point_balance: number;
  daily_transactions: number;
  payment_success_rate: number;
}

// 사주 해석 데이터 타입
interface InterpretationData {
  id: string;
  category: 'gapja' | 'heavenly_stem' | 'earthly_branch' | 'hidden_stem' | 'five_element' | 'destiny_pattern' | 'compatibility';
  key: string;
  title: string;
  content: string;
  quality_score: number;
  last_updated: Date;
  created_by: string;
}

// 해석 카테고리 정의
interface InterpretationCategory {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  count: number;
  examples: string[];
}

const SajuAdminDashboard: React.FC = () => {
  // 상태 관리 - 개별 로딩 상태로 세분화
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sajuEngine, setSajuEngine] = useState<SajuEngineStatus | null>(null);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [contentStats, setContentStats] = useState<ContentStats | null>(null);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [pointStats, setPointStats] = useState<PointStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [refreshingSection, setRefreshingSection] = useState<string | null>(null);
  
  // 사주 해석 시스템 상태
  const [selectedInterpretationCategory, setSelectedInterpretationCategory] = useState<string>('gapja');
  const [interpretationData, setInterpretationData] = useState<InterpretationData[]>([]);
  const [editingInterpretation, setEditingInterpretation] = useState<InterpretationData | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isEditing, setIsEditing] = useState(false);
  
  // 해석 카테고리 정의
  const interpretationCategories: InterpretationCategory[] = [
    {
      id: 'gapja',
      name: '60갑자',
      description: '갑자부터 계해까지 60개 갑자별 상세 해석',
      icon: <Hash className="w-4 h-4" />,
      count: 60,
      examples: ['갑자(甲子)', '을축(乙丑)', '병인(丙寅)', '정묘(丁卯)']
    },
    {
      id: 'heavenly_stem',
      name: '천간',
      description: '갑을병정무기경신임계 10천간 해석',
      icon: <Star className="w-4 h-4" />,
      count: 10,
      examples: ['갑(甲)', '을(乙)', '병(丙)', '정(丁)']
    },
    {
      id: 'earthly_branch',
      name: '지지',
      description: '자축인묘진사오미신유술해 12지지 해석',
      icon: <Globe className="w-4 h-4" />,
      count: 12,
      examples: ['자(子)', '축(丑)', '인(寅)', '묘(卯)']
    },
    {
      id: 'hidden_stem',
      name: '지장간',
      description: '각 지지에 숨어있는 천간들의 해석',
      icon: <Bookmark className="w-4 h-4" />,
      count: 36,
      examples: ['자→계', '축→기정신', '인→갑병무']
    },
    {
      id: 'five_element',
      name: '오행',
      description: '목화토금수 오행의 상생상극 해석',
      icon: <Palette className="w-4 h-4" />,
      count: 25,
      examples: ['목생화', '화생토', '토생금', '금생수']
    },
    {
      id: 'destiny_pattern',
      name: '격국',
      description: '정관격, 편관격, 정재격 등 각 격국별 해석',
      icon: <BookOpen className="w-4 h-4" />,
      count: 18,
      examples: ['정관격', '편관격', '정재격', '편재격']
    },
    {
      id: 'compatibility',
      name: '궁합',
      description: '남녀 사주 조합별 궁합 해석 데이터베이스',
      icon: <Heart className="w-4 h-4" />,
      count: 144,
      examples: ['갑자-을축', '병인-정묘', '무진-기사']
    }
  ];

  // 개별 데이터 업데이트 함수들 - state 기반 업데이트로 변경
  const updateSajuEngine = useCallback(async () => {
    setRefreshingSection('saju-engine');
    // 실제로는 API 호출, 지금은 모의 데이터
    await new Promise(resolve => setTimeout(resolve, 500));
    setSajuEngine({
      calculation_accuracy: 99.7 + (Math.random() - 0.5) * 0.1,
      total_calculations: 15847 + Math.floor(Math.random() * 10),
      avg_response_time: 245 + Math.floor(Math.random() * 20) - 10,
      error_rate: 0.3 + (Math.random() - 0.5) * 0.1,
      active_algorithms: ['전통사주', 'AI보정', '띠운세', '꿈풀이']
    });
    setRefreshingSection(null);
  }, []);

  const updateUserStats = useCallback(async () => {
    setRefreshingSection('users');
    await new Promise(resolve => setTimeout(resolve, 300));
    setUserStats({
      total_users: 3245 + Math.floor(Math.random() * 5),
      active_today: 187 + Math.floor(Math.random() * 20) - 10,
      premium_users: 542 + Math.floor(Math.random() * 3),
      new_signups: 23 + Math.floor(Math.random() * 5),
      retention_rate: 78.5 + (Math.random() - 0.5) * 2
    });
    setRefreshingSection(null);
  }, []);

  const updateSystemHealth = useCallback(async () => {
    setRefreshingSection('system');
    await new Promise(resolve => setTimeout(resolve, 200));
    setSystemHealth({
      api_status: 'healthy',
      database_status: 'healthy',
      response_time: 189 + Math.floor(Math.random() * 40) - 20,
      uptime: 99.8,
      memory_usage: 67 + Math.floor(Math.random() * 10) - 5,
      cpu_usage: 23 + Math.floor(Math.random() * 20) - 10,
      redis_status: 'healthy',
      cache_hit_rate: 87.3 + (Math.random() - 0.5) * 4
    });
    setRefreshingSection(null);
  }, []);

  const updateAnalytics = useCallback(async () => {
    setRefreshingSection('analytics');
    await new Promise(resolve => setTimeout(resolve, 400));
    setAnalytics({
      popular_features: [
        { name: '사주명리', usage_count: 4523 + Math.floor(Math.random() * 50), growth_rate: 12.5 },
        { name: '띠운세', usage_count: 3421 + Math.floor(Math.random() * 30), growth_rate: 8.7 },
        { name: '꿈풀이', usage_count: 2847 + Math.floor(Math.random() * 20), growth_rate: -2.1 },
        { name: '타로카드', usage_count: 1923 + Math.floor(Math.random() * 40), growth_rate: 18.3 }
      ],
      daily_active_users: 187 + Math.floor(Math.random() * 20) - 10,
      peak_hours: ['오후 8-10시', '점심 12-1시'],
      conversion_rate: 15.7 + (Math.random() - 0.5) * 2
    });
    setRefreshingSection(null);
  }, []);

  // 초기 데이터 로드 함수
  const initializeData = useCallback(() => {
    setSajuEngine({
      calculation_accuracy: 99.7,
      total_calculations: 15847,
      avg_response_time: 245,
      error_rate: 0.3,
      active_algorithms: ['전통사주', 'AI보정', '띠운세', '꿈풀이']
    });

    setUserStats({
      total_users: 3245,
      active_today: 187,
      premium_users: 542,
      new_signups: 23,
      retention_rate: 78.5
    });

    setContentStats({
      total_interpretations: 8921,
      zodiac_images: 144,
      dream_interpretations: 2847,
      fortune_texts: 5930,
      last_updated: '2025-09-03 14:23',
      gapja_60: 60,
      heavenly_stems: 10,
      earthly_branches: 12,
      hidden_stems: 36,
      five_elements: 25,
      destiny_patterns: 18,
      compatibility_data: 144
    });

    setSystemHealth({
      api_status: 'healthy',
      database_status: 'healthy',
      response_time: 189,
      uptime: 99.8,
      memory_usage: 67,
      cpu_usage: 23,
      redis_status: 'healthy',
      cache_hit_rate: 87.3
    });

    setPointStats({
      total_points_issued: 1250000,
      total_points_used: 987000,
      active_point_balance: 263000,
      daily_transactions: 423,
      payment_success_rate: 96.8
    });

    const mockInterpretations: InterpretationData[] = [
      {
        id: '1',
        category: 'gapja',
        key: '갑자',
        title: '갑자(甲子) 해석',
        content: '갑자는 60갑자의 첫 번째로, 새로운 시작을 의미합니다. 갑목이 자수를 만나 생기를 얻어 성장력이 뛰어나며...',
        quality_score: 95,
        last_updated: new Date('2025-09-03'),
        created_by: 'admin'
      },
      {
        id: '2',
        category: 'heavenly_stem',
        key: '갑',
        title: '갑(甲) - 양목',
        content: '갑목은 큰 나무, 동쪽을 상징하며 봄의 기운을 담고 있습니다. 리더십이 강하고 직진적인 성향...',
        quality_score: 92,
        last_updated: new Date('2025-09-02'),
        created_by: 'admin'
      },
      {
        id: '3',
        category: 'earthly_branch',
        key: '자',
        title: '자(子) - 양수',
        content: '자수는 12지지의 첫 번째로 북쪽, 겨울을 상징합니다. 지혜롭고 적응력이 뛰어나며...',
        quality_score: 89,
        last_updated: new Date('2025-09-01'),
        created_by: 'admin'
      }
    ];
    
    setInterpretationData(mockInterpretations);

    setAnalytics({
      popular_features: [
        { name: '사주명리', usage_count: 4523, growth_rate: 12.5 },
        { name: '띠운세', usage_count: 3421, growth_rate: 8.7 },
        { name: '꿈풀이', usage_count: 2847, growth_rate: -2.1 },
        { name: '타로카드', usage_count: 1923, growth_rate: 18.3 }
      ],
      daily_active_users: 187,
      peak_hours: ['오후 8-10시', '점심 12-1시'],
      conversion_rate: 15.7
    });
  }, []);

  // 초기 데이터 로딩 - 한 번만 실행
  useEffect(() => {
    const fetchInitialData = async () => {
      setLoading(true);
      await new Promise(resolve => setTimeout(resolve, 1000));
      initializeData();
      setLastUpdate(new Date());
      setLoading(false);
    };

    fetchInitialData();
  }, [initializeData]);

  // 자동 새로고침을 보다 효율적으로 변경 - 개별 섹션만 업데이트
  useEffect(() => {
    const interval = setInterval(() => {
      // 현재 활성화된 탭에 따라 필요한 데이터만 업데이트
      switch(activeTab) {
        case 'saju-engine':
          updateSajuEngine();
          break;
        case 'users':
          updateUserStats();
          break;
        case 'system':
          updateSystemHealth();
          break;
        case 'analytics':
          updateAnalytics();
          break;
        default:
          // 대시보드에서는 핵심 지표만 업데이트
          updateSystemHealth();
          break;
      }
      setLastUpdate(new Date());
    }, 60000); // 1분마다 현재 탭의 데이터만 업데이트

    return () => clearInterval(interval);
  }, [activeTab, updateSajuEngine, updateUserStats, updateSystemHealth, updateAnalytics]);

  // 상태 배지 컴포넌트 - React.memo로 최적화
  const StatusBadge: React.FC<{ status: string; children: React.ReactNode }> = React.memo(({ status, children }) => {
    const variant = status === 'healthy' ? 'default' : status === 'warning' ? 'secondary' : 'destructive';
    const icon = status === 'healthy' ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />;
    
    return (
      <Badge variant={variant} className="flex items-center gap-1">
        {icon}
        {children}
      </Badge>
    );
  });

  // 통계 카드 컴포넌트 - React.memo로 최적화 및 로딩 상태 추가
  const StatsCard: React.FC<{
    title: string;
    value: string | number;
    description: string;
    icon: React.ReactNode;
    trend?: number;
    color?: string;
    isRefreshing?: boolean;
  }> = React.memo(({ title, value, description, icon, trend, color = "text-purple-600", isRefreshing = false }) => {
    return (
      <Card className={`cyber-card hover:glow-border-purple transition-all duration-500 group ${isRefreshing ? 'animate-pulse' : ''}`}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-white/90">{title}</CardTitle>
          <div className={`${color} group-hover:text-purple-400 transition-colors ${isRefreshing ? 'animate-spin' : ''}`}>
            {isRefreshing ? <RefreshCw className="w-4 h-4" /> : icon}
          </div>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-white mb-1 glow-text-purple">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </div>
          <div className="flex items-center justify-between">
            <p className="text-xs text-white/60">{description}</p>
            {trend !== undefined && (
              <Badge 
                variant={trend >= 0 ? "default" : "secondary"} 
                className={`text-xs ${trend >= 0 
                  ? 'bg-green-500/20 text-green-300 border-green-400/30' 
                  : 'bg-red-500/20 text-red-300 border-red-400/30'
                } backdrop-blur-sm`}
              >
                {trend >= 0 ? '+' : ''}{trend}%
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>
    );
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-slate-900 to-indigo-900 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-8 shadow-2xl border border-white/20">
          <RefreshCw className="w-8 h-8 animate-spin text-purple-400 mx-auto mb-4" />
          <p className="text-white/90 text-center">관리자 대시보드 로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-slate-900 to-indigo-900">
      {/* 사이버 판타지 글래스모피즘 컨테이너 */}
      <div className="container mx-auto p-6">
        {/* 헤더 */}
        <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 mb-6 shadow-2xl border border-white/20 glow-border-purple">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2 glow-text-purple">🔮 사주 관리자 대시보드</h1>
              <p className="text-white/80">
                마지막 업데이트: {lastUpdate.toLocaleTimeString('ko-KR')} | 
                시스템 상태: <StatusBadge status="healthy">정상</StatusBadge>
              </p>
            </div>
            <Button 
              onClick={() => {
                // 현재 탭에 따라 해당 데이터만 새로고침
                switch(activeTab) {
                  case 'saju-engine':
                    updateSajuEngine();
                    break;
                  case 'users':
                    updateUserStats();
                    break;
                  case 'system':
                    updateSystemHealth();
                    break;
                  case 'analytics':
                    updateAnalytics();
                    break;
                  default:
                    // 대시보드에서는 모든 핵심 데이터 업데이트
                    updateSajuEngine();
                    updateUserStats();
                    updateSystemHealth();
                    updateAnalytics();
                    break;
                }
                setLastUpdate(new Date());
              }}
              disabled={refreshingSection !== null}
              className="bg-purple-600/80 hover:bg-purple-500/90 backdrop-blur-sm border border-purple-400/50 text-white shadow-lg hover:shadow-purple-500/20 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${refreshingSection ? 'animate-spin' : ''}`} />
              {refreshingSection ? '새로고침 중...' : '새로고침'}
            </Button>
          </div>
        </div>

        {/* 메인 네비게이션 - 개별 버튼 스타일 */}
        <div className="cyber-card p-6 mb-6">
          <h2 className="text-lg font-semibold text-white/90 mb-4 glow-text-purple">관리 메뉴</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'dashboard'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">📊</span>
              <span className={`${activeTab === 'dashboard' ? 'glow-text-purple' : ''}`}>대시보드</span>
            </button>
            <button
              onClick={() => setActiveTab('saju-engine')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'saju-engine'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">🔮</span>
              <span className={`${activeTab === 'saju-engine' ? 'glow-text-purple' : ''}`}>사주엔진</span>
            </button>
            <button
              onClick={() => setActiveTab('users')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'users'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">👤</span>
              <span className={`${activeTab === 'users' ? 'glow-text-purple' : ''}`}>사용자</span>
            </button>
            <button
              onClick={() => setActiveTab('content')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'content'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">🌟</span>
              <span className={`${activeTab === 'content' ? 'glow-text-purple' : ''}`}>콘텐츠</span>
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'analytics'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">📈</span>
              <span className={`${activeTab === 'analytics' ? 'glow-text-purple' : ''}`}>통계</span>
            </button>
            <button
              onClick={() => setActiveTab('points')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'points'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">💎</span>
              <span className={`${activeTab === 'points' ? 'glow-text-purple' : ''}`}>포인트</span>
            </button>
            <button
              onClick={() => setActiveTab('system')}
              className={`
                px-4 py-3 rounded-xl font-medium text-sm transition-all duration-500 group h-20 flex flex-col items-center justify-center
                ${activeTab === 'system'
                  ? 'bg-gradient-to-br from-purple-600 via-purple-500 to-indigo-600 text-white shadow-2xl shadow-purple-500/50 glow-border-purple scale-105'
                  : 'text-white/60 hover:text-white/90 hover:bg-white/10 hover:shadow-lg hover:scale-102 border border-white/20'
                }
              `}
            >
              <span className="text-lg mb-1">🗄️</span>
              <span className={`${activeTab === 'system' ? 'glow-text-purple' : ''}`}>시스템</span>
            </button>
          </div>
        </div>

        {/* 컨텐츠 영역 */}
        <div className="space-y-6">
          {/* 📊 대시보드 */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
            {/* 핵심 지표 카드 (4개) */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatsCard
                title="오늘 활성 사용자"
                value={userStats?.active_today || 0}
                description="전일 대비"
                icon={<Users className="h-4 w-4" />}
                trend={12}
                color="text-blue-600"
                isRefreshing={refreshingSection === 'users'}
              />
              <StatsCard
                title="사주 계산 정확도"
                value={`${sajuEngine?.calculation_accuracy ? sajuEngine.calculation_accuracy.toFixed(1) : 0}%`}
                description="알고리즘 성능"
                icon={<Brain className="h-4 w-4" />}
                trend={0.2}
                color="text-green-600"
                isRefreshing={refreshingSection === 'saju-engine'}
              />
              <StatsCard
                title="평균 응답시간"
                value={`${sajuEngine?.avg_response_time || 0}ms`}
                description="API 성능"
                icon={<Zap className="h-4 w-4" />}
                trend={-5}
                color="text-yellow-600"
                isRefreshing={refreshingSection === 'saju-engine'}
              />
              <StatsCard
                title="시스템 가동률"
                value={`${systemHealth?.uptime || 0}%`}
                description="30일 평균"
                icon={<Shield className="h-4 w-4" />}
                trend={0.1}
                color="text-purple-600"
                isRefreshing={refreshingSection === 'system'}
              />
            </div>

            {/* 상세 모니터링 카드 (2개) */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 시스템 상태 */}
              <Card className={`cyber-card hover:glow-border-purple transition-all duration-500 group ${refreshingSection === 'system' ? 'animate-pulse border-purple-400/50' : ''}`}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <Server className={`w-5 h-5 text-purple-400 group-hover:text-purple-300 ${refreshingSection === 'system' ? 'animate-spin' : ''}`} />
                    시스템 상태 {refreshingSection === 'system' && <span className="text-xs text-purple-300">(업데이트 중)</span>}
                  </CardTitle>
                  <CardDescription className="text-white/60">실시간 서버 모니터링</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-white/70">CPU 사용률</span>
                      <span className="text-sm font-medium text-white/90 glow-text-purple">{systemHealth?.cpu_usage}%</span>
                    </div>
                    <Progress value={systemHealth?.cpu_usage} className="h-2" />
                    
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-white/70">메모리 사용률</span>
                      <span className="text-sm font-medium text-white/90 glow-text-purple">{systemHealth?.memory_usage}%</span>
                    </div>
                    <Progress value={systemHealth?.memory_usage} className="h-2" />
                  </div>
                </CardContent>
              </Card>

              {/* 인기 기능 */}
              <Card className={`cyber-card hover:glow-border-purple transition-all duration-500 group ${refreshingSection === 'analytics' ? 'animate-pulse border-purple-400/50' : ''}`}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <Star className={`w-5 h-5 text-purple-400 group-hover:text-purple-300 ${refreshingSection === 'analytics' ? 'animate-spin' : ''}`} />
                    인기 기능 TOP 4 {refreshingSection === 'analytics' && <span className="text-xs text-purple-300">(업데이트 중)</span>}
                  </CardTitle>
                  <CardDescription className="text-white/60">사용자 선호도 순위</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {analytics?.popular_features.map((feature, index) => (
                      <div key={feature.name} className="flex items-center justify-between p-2 rounded-lg bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="text-xs bg-purple-500/20 text-purple-300 border-purple-400/50">
                            {index + 1}
                          </Badge>
                          <span className="text-sm text-white/80">{feature.name}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-white/60">{feature.usage_count.toLocaleString()}</span>
                          <Badge variant={feature.growth_rate >= 0 ? "default" : "secondary"} className={`text-xs ${
                            feature.growth_rate >= 0 
                              ? 'bg-green-500/20 text-green-300 border-green-400/50' 
                              : 'bg-red-500/20 text-red-300 border-red-400/50'
                          }`}>
                            {feature.growth_rate >= 0 ? '+' : ''}{feature.growth_rate}%
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
            </div>

          )}

          {/* 🔮 사주엔진 탭 */}
          {activeTab === 'saju-engine' && (
            <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatsCard
                title="총 계산 횟수"
                value={sajuEngine?.total_calculations || 0}
                description="누적 사주 계산"
                icon={<Brain className="h-4 w-4" />}
                color="text-purple-600"
              />
              <StatsCard
                title="계산 정확도"
                value={`${sajuEngine?.calculation_accuracy || 0}%`}
                description="알고리즘 성능"
                icon={<CheckCircle className="h-4 w-4" />}
                color="text-green-600"
              />
              <StatsCard
                title="평균 응답시간"
                value={`${sajuEngine?.avg_response_time || 0}ms`}
                description="계산 속도"
                icon={<Clock className="h-4 w-4" />}
                color="text-blue-600"
              />
              <StatsCard
                title="오류율"
                value={`${sajuEngine?.error_rate || 0}%`}
                description="시스템 안정성"
                icon={<AlertCircle className="h-4 w-4" />}
                color="text-red-600"
              />
            </div>

            {/* 알고리즘 상태 */}
            <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                  <Sparkles className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                  활성 알고리즘 모니터링
                </CardTitle>
                <CardDescription className="text-white/60">사주 계산 엔진 상태</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  {sajuEngine?.active_algorithms.map((algorithm) => (
                    <div key={algorithm} className="flex items-center justify-between p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:bg-white/10 hover:glow-border-purple transition-all duration-300">
                      <span className="text-sm font-medium text-white/80">{algorithm}</span>
                      <StatusBadge status="healthy">정상</StatusBadge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            </div>
          )}

          {/* 👤 사용자관리 탭 */}
          {activeTab === 'users' && (
            <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatsCard
                title="전체 사용자"
                value={userStats?.total_users || 0}
                description="등록된 회원 수"
                icon={<Users className="h-4 w-4" />}
                color="text-blue-600"
              />
              <StatsCard
                title="프리미엄 사용자"
                value={userStats?.premium_users || 0}
                description="구독 중인 회원"
                icon={<Star className="h-4 w-4" />}
                color="text-yellow-600"
              />
              <StatsCard
                title="신규 가입"
                value={userStats?.new_signups || 0}
                description="오늘 가입자"
                icon={<UserCheck className="h-4 w-4" />}
                color="text-green-600"
              />
              <StatsCard
                title="사용자 유지율"
                value={`${userStats?.retention_rate || 0}%`}
                description="30일 기준"
                icon={<Heart className="h-4 w-4" />}
                color="text-red-600"
              />
            </div>

            {/* 사용자 관리 도구 */}
            <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                  <Settings className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                  사용자 관리 도구
                </CardTitle>
                <CardDescription className="text-white/60">회원 데이터 및 개인정보 관리</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Users className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">회원 목록</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Shield className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">개인정보 관리</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Database className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">데이터 백업</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <AlertCircle className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">신고 처리</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
            </div>
          )}

          {/* 🌟 콘텐츠관리 탭 - 사주 해석 입력 시스템 통합 */}
          {activeTab === 'content' && (
            <div className="space-y-6">
            {/* 사주 해석 데이터 통계 */}
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
              {interpretationCategories.map((category) => (
                <StatsCard
                  key={category.id}
                  title={category.name}
                  value={category.count}
                  description={"개 해석 데이터"}
                  icon={category.icon}
                  color="text-purple-600"
                />
              ))}
            </div>

            {/* 사주 해석 카테고리 선택 */}
            <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                  <PenTool className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                  사주 해석 데이터 관리시스템
                </CardTitle>
                <CardDescription className="text-white/60">60갑자, 천간지지, 오행, 격국, 궁합 데이터 입력 및 관리</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* 카테고리 선택 내비게이션 */}
                <div className="flex flex-wrap gap-2">
                  {interpretationCategories.map((category) => (
                    <Button
                      key={category.id}
                      onClick={() => setSelectedInterpretationCategory(category.id)}
                      variant={selectedInterpretationCategory === category.id ? "default" : "outline"}
                      className={`h-auto py-2 px-3 transition-all duration-300 ${
                        selectedInterpretationCategory === category.id
                          ? 'bg-gradient-to-r from-purple-600 to-indigo-600 glow-border-purple text-white shadow-lg'
                          : 'bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        {category.icon}
                        <div className="text-left">
                          <div className="text-sm font-medium">{category.name}</div>
                          <div className="text-xs opacity-70">{category.count}개</div>
                        </div>
                      </div>
                    </Button>
                  ))}
                </div>

                {/* 선택된 카테고리 상세 정보 */}
                {(() => {
                  const selectedCategory = interpretationCategories.find(c => c.id === selectedInterpretationCategory);
                  return (
                    <Card className="bg-white/5 backdrop-blur-sm border-white/10 hover:bg-white/10 transition-all duration-300">
                      <CardHeader className="pb-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            {selectedCategory?.icon}
                            <div>
                              <CardTitle className="text-lg text-white/90 glow-text-purple">
                                {selectedCategory?.name} 해석 데이터
                              </CardTitle>
                              <CardDescription className="text-white/60">
                                {selectedCategory?.description}
                              </CardDescription>
                            </div>
                          </div>
                          <div className="flex gap-2">
                            <Button 
                              onClick={() => setIsEditing(true)}
                              size="sm" 
                              className="bg-green-600/20 text-green-300 border-green-400/50 hover:bg-green-500/30 hover:glow-border-green transition-all duration-300"
                            >
                              <Plus className="w-4 h-4 mr-1" />
                              새 해석 추가
                            </Button>
                            <Button 
                              size="sm" 
                              variant="outline"
                              className="bg-blue-600/20 text-blue-300 border-blue-400/50 hover:bg-blue-500/30 hover:glow-border-blue transition-all duration-300"
                            >
                              <Download className="w-4 h-4 mr-1" />
                              내보내기
                            </Button>
                            <Button 
                              size="sm" 
                              variant="outline"
                              className="bg-orange-600/20 text-orange-300 border-orange-400/50 hover:bg-orange-500/30 hover:glow-border-orange transition-all duration-300"
                            >
                              <Upload className="w-4 h-4 mr-1" />
                              가져오기
                            </Button>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        {/* 검색 및 필터 */}
                        <div className="flex gap-2 mb-4">
                          <div className="flex-1 relative">
                            <Search className="w-4 h-4 absolute left-3 top-3 text-white/40" />
                            <input
                              type="text"
                              placeholder="해석 내용 검색..."
                              value={searchTerm}
                              onChange={(e) => setSearchTerm(e.target.value)}
                              className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/20 rounded-lg text-white/90 placeholder:text-white/40 focus:outline-none focus:border-purple-400/50 focus:glow-border-purple transition-all duration-300"
                            />
                          </div>
                          <Button 
                            size="sm" 
                            variant="outline"
                            className="px-4 bg-white/5 border-white/20 text-white/80 hover:bg-white/10 hover:border-purple-400/50 hover:text-white transition-all duration-300"
                          >
                            <Filter className="w-4 h-4" />
                            필터
                          </Button>
                        </div>

                        {/* 해석 데이터 리스트 */}
                        <div className="space-y-2">
                          {interpretationData
                            .filter(item => item.category === selectedInterpretationCategory)
                            .filter(item => searchTerm === '' || item.content.toLowerCase().includes(searchTerm.toLowerCase()))
                            .map((item) => (
                            <Card key={item.id} className="bg-white/3 backdrop-blur-sm border-white/10 hover:bg-white/8 hover:glow-border-purple transition-all duration-300">
                              <CardContent className="p-4">
                                <div className="flex items-start justify-between">
                                  <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                      <Badge className="bg-purple-500/20 text-purple-300 border-purple-400/50">
                                        {item.key}
                                      </Badge>
                                      <h4 className="text-white/90 font-medium">{item.title}</h4>
                                      <div className="flex items-center gap-1 text-xs text-white/50">
                                        <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                                        <span>{item.quality_score}/100</span>
                                      </div>
                                    </div>
                                    <p className="text-white/70 text-sm leading-relaxed mb-2 line-clamp-2">
                                      {item.content}
                                    </p>
                                    <div className="flex items-center gap-4 text-xs text-white/50">
                                      <span>마지막 수정: {item.last_updated.toLocaleDateString('ko-KR')}</span>
                                      <span>작성자: {item.created_by}</span>
                                    </div>
                                  </div>
                                  <div className="flex gap-1 ml-4">
                                    <Button 
                                      onClick={() => setEditingInterpretation(item)}
                                      size="sm" 
                                      variant="ghost"
                                      className="h-8 w-8 p-0 text-white/60 hover:text-white hover:bg-white/10 transition-all duration-300"
                                    >
                                      <Edit className="w-3 h-3" />
                                    </Button>
                                    <Button 
                                      size="sm" 
                                      variant="ghost"
                                      className="h-8 w-8 p-0 text-red-400/60 hover:text-red-400 hover:bg-red-500/10 transition-all duration-300"
                                    >
                                      <Trash2 className="w-3 h-3" />
                                    </Button>
                                  </div>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                          
                          {/* 데이터가 없는 경우 */}
                          {interpretationData.filter(item => item.category === selectedInterpretationCategory).length === 0 && (
                            <div className="text-center py-12 text-white/50">
                              <BookOpen className="w-12 h-12 mx-auto mb-4 opacity-50" />
                              <p className="text-lg mb-2">아직 {selectedCategory?.name} 해석 데이터가 없습니다.</p>
                              <p className="text-sm">새 해석 추가 버튼을 눌러 첫 해석을 작성해보세요.</p>
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  );
                })()}

                {/* 해석 에디터 모달 */}
                {(isEditing || editingInterpretation) && (
                  <Card className="bg-gradient-to-br from-purple-900/50 to-indigo-900/50 backdrop-blur-xl border-purple-400/30 glow-border-purple">
                    <CardHeader>
                      <CardTitle className="text-white/90 glow-text-purple">
                        {editingInterpretation ? '해석 수정' : '새 해석 추가'}
                      </CardTitle>
                      <CardDescription className="text-white/60">
                        {interpretationCategories.find(c => c.id === selectedInterpretationCategory)?.name} 카테고리
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium text-white/80 mb-2 block">키워드</label>
                          <input
                            type="text"
                            placeholder={interpretationCategories.find(c => c.id === selectedInterpretationCategory)?.examples[0]}
                            defaultValue={editingInterpretation?.key || ''}
                            className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white/90 placeholder:text-white/40 focus:outline-none focus:border-purple-400/50 focus:glow-border-purple transition-all duration-300"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-white/80 mb-2 block">제목</label>
                          <input
                            type="text"
                            placeholder="해석 제목을 입력하세요"
                            defaultValue={editingInterpretation?.title || ''}
                            className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white/90 placeholder:text-white/40 focus:outline-none focus:border-purple-400/50 focus:glow-border-purple transition-all duration-300"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-white/80 mb-2 block">해석 내용</label>
                        <textarea
                          placeholder="상세한 해석 내용을 입력하세요. 마크다운 형식을 지원합니다."
                          rows={8}
                          defaultValue={editingInterpretation?.content || ''}
                          className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white/90 placeholder:text-white/40 focus:outline-none focus:border-purple-400/50 focus:glow-border-purple transition-all duration-300 resize-none"
                        />
                      </div>
                      <div className="flex justify-between items-center pt-4 border-t border-white/10">
                        <div className="text-sm text-white/50">
                          문자 수: 0 | 품질 점수: {editingInterpretation?.quality_score || 0}/100
                        </div>
                        <div className="flex gap-2">
                          <Button 
                            onClick={() => {
                              setIsEditing(false);
                              setEditingInterpretation(null);
                            }}
                            variant="outline"
                            className="bg-white/5 border-white/20 text-white/80 hover:bg-white/10 hover:border-white/30 hover:text-white transition-all duration-300"
                          >
                            취소
                          </Button>
                          <Button 
                            className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white shadow-lg hover:shadow-purple-500/20 hover:glow-border-purple transition-all duration-300"
                          >
                            <Save className="w-4 h-4 mr-2" />
                            {editingInterpretation ? '수정 저장' : '해석 추가'}
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </CardContent>
            </Card>

            {/* 기타 콘텐츠 관리 도구 */}
            <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                  <FileText className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                  기타 콘텐츠 관리
                </CardTitle>
                <CardDescription className="text-white/60">이미지, 또랅춘세, 꿈풀이 등 기타 콘텐츠 관리</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <ImageIcon className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">띠 이미지</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Sparkles className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">꿈풀이</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Calendar className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">일일 운세</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Globe className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">타로카드</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
            </div>
          )}

          {/* 💎 포인트/결제 관리 탭 */}
          {activeTab === 'points' && (
            <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <StatsCard
                title="총 발행 포인트"
                value={pointStats?.total_points_issued.toLocaleString() || '0'}
                description="누적 발행량"
                icon={<Coins className="h-4 w-4" />}
                color="text-yellow-600"
              />
              <StatsCard
                title="사용된 포인트"
                value={pointStats?.total_points_used.toLocaleString() || '0'}
                description="누적 사용량"
                icon={<DollarSign className="h-4 w-4" />}
                color="text-green-600"
              />
              <StatsCard
                title="활성 뱸런스"
                value={pointStats?.active_point_balance.toLocaleString() || '0'}
                description="현재 사용 가능"
                icon={<CreditCard className="h-4 w-4" />}
                color="text-blue-600"
              />
              <StatsCard
                title="일일 거래"
                value={pointStats?.daily_transactions || 0}
                description="오늘 거래 건수"
                icon={<Receipt className="h-4 w-4" />}
                color="text-purple-600"
              />
              <StatsCard
                title="결제 성공률"
                value={`${pointStats?.payment_success_rate || 0}%`}
                description="30일 평균"
                icon={<CheckCircle className="h-4 w-4" />}
                color="text-emerald-600"
                trend={2.3}
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 포인트 관리 */}
              <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <Coins className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                    포인트 관리 시스템
                  </CardTitle>
                  <CardDescription className="text-white/60">사용자 포인트 및 결제 관리</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <Button 
                      variant="outline" 
                      className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                    >
                      <Users className="w-6 h-6 mb-2 text-purple-400" />
                      <span className="text-sm">사용자 포인트</span>
                    </Button>
                    <Button 
                      variant="outline" 
                      className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                    >
                      <DollarSign className="w-6 h-6 mb-2 text-purple-400" />
                      <span className="text-sm">결제 내역</span>
                    </Button>
                    <Button 
                      variant="outline" 
                      className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                    >
                      <Receipt className="w-6 h-6 mb-2 text-purple-400" />
                      <span className="text-sm">환불 처리</span>
                    </Button>
                    <Button 
                      variant="outline" 
                      className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                    >
                      <BarChart3 className="w-6 h-6 mb-2 text-purple-400" />
                      <span className="text-sm">매출 분석</span>
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* 결제 수단 관리 */}
              <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <CreditCard className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                    결제 수단 관리
                  </CardTitle>
                  <CardDescription className="text-white/60">결제 옵션 및 수수료 설정</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:bg-white/10 transition-all duration-300">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                          <CreditCard className="w-4 h-4 text-blue-400" />
                        </div>
                        <div>
                          <div className="text-sm font-medium text-white/90">카드 결제</div>
                          <div className="text-xs text-white/60">수수료 2.9%</div>
                        </div>
                      </div>
                      <StatusBadge status="healthy">정상</StatusBadge>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:bg-white/10 transition-all duration-300">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                          <DollarSign className="w-4 h-4 text-yellow-400" />
                        </div>
                        <div>
                          <div className="text-sm font-medium text-white/90">계좌 이체</div>
                          <div className="text-xs text-white/60">수수료 1.5%</div>
                        </div>
                      </div>
                      <StatusBadge status="healthy">정상</StatusBadge>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:bg-white/10 transition-all duration-300">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                          <Coins className="w-4 h-4 text-green-400" />
                        </div>
                        <div>
                          <div className="text-sm font-medium text-white/90">무통장 입금</div>
                          <div className="text-xs text-white/60">수수료 0%</div>
                        </div>
                      </div>
                      <StatusBadge status="healthy">정상</StatusBadge>
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t border-white/10">
                    <Button 
                      className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white shadow-lg hover:shadow-purple-500/20 hover:glow-border-purple transition-all duration-300"
                    >
                      <Settings className="w-4 h-4 mr-2" />
                      결제 설정 관리
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
            </div>
          )}

          {/* 🗄️ 시스템관리 탭 */}
          {activeTab === 'system' && (
            <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatsCard
                title="Redis 캐시"
                value={systemHealth?.redis_status === 'healthy' ? '정상' : '오류'}
                description={`사용률 ${systemHealth?.cache_hit_rate || 0}%`}
                icon={<MemoryStick className="h-4 w-4" />}
                color="text-red-600"
              />
              <StatsCard
                title="데이터베이스"
                value={systemHealth?.database_status === 'healthy' ? '정상' : '오류'}
                description="PostgreSQL 연결 상태"
                icon={<Database className="h-4 w-4" />}
                color="text-blue-600"
              />
              <StatsCard
                title="스토리지"
                value="78%"
                description="디스크 사용률"
                icon={<HardDrive className="h-4 w-4" />}
                color="text-orange-600"
              />
              <StatsCard
                title="백업 상태"
                value="정상"
                description="마지막 백업: 어제"
                icon={<Shield className="h-4 w-4" />}
                color="text-green-600"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 캐시 관리 */}
              <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <MemoryStick className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                    Redis 캐시 관리
                  </CardTitle>
                  <CardDescription className="text-white/60">캐시 성능 모니터링 및 관리</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-white/70">캐시 히트률</span>
                      <span className="text-sm font-medium text-white/90 glow-text-purple">{systemHealth?.cache_hit_rate}%</span>
                    </div>
                    <Progress value={systemHealth?.cache_hit_rate} className="h-2" />
                    
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-white/70">메모리 사용률</span>
                      <span className="text-sm font-medium text-white/90 glow-text-purple">45.2MB</span>
                    </div>
                    <Progress value={75} className="h-2" />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2 pt-4 border-t border-white/10">
                    <Button 
                      size="sm" 
                      variant="outline"
                      className="bg-white/5 border-white/20 text-white/80 hover:bg-red-500/20 hover:border-red-400/50 hover:text-white transition-all duration-300"
                    >
                      <Trash2 className="w-3 h-3 mr-1" />
                      캐시 초기화
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline"
                      className="bg-white/5 border-white/20 text-white/80 hover:bg-blue-500/20 hover:border-blue-400/50 hover:text-white transition-all duration-300"
                    >
                      <RefreshCw className="w-3 h-3 mr-1" />
                      캐시 새로고침
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* 데이터베이스 관리 */}
              <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <Database className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                    데이터베이스 관리
                  </CardTitle>
                  <CardDescription className="text-white/60">PostgreSQL 성능 및 백업 관리</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10">
                        <div className="text-xs text-white/60 mb-1">사주 데이터</div>
                        <div className="text-lg font-bold text-white/90">15.8K</div>
                      </div>
                      <div className="p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10">
                        <div className="text-xs text-white/60 mb-1">사용자 데이터</div>
                        <div className="text-lg font-bold text-white/90">3.2K</div>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-2 pt-4 border-t border-white/10">
                      <Button 
                        size="sm" 
                        variant="outline"
                        className="bg-white/5 border-white/20 text-white/80 hover:bg-green-500/20 hover:border-green-400/50 hover:text-white transition-all duration-300"
                      >
                        <Download className="w-3 h-3 mr-1" />
                        데이터 백업
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        className="bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white transition-all duration-300"
                      >
                        <BarChart3 className="w-3 h-3 mr-1" />
                        성능 분석
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* 시스템 도구 */}
            <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                  <Wrench className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                  시스템 관리 도구
                </CardTitle>
                <CardDescription className="text-white/60">서버 관리 및 유지보수 도구</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Server className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">서버 상태</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <FileText className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">로그 보기</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <Settings className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">설정 관리</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-20 flex flex-col bg-white/5 border-white/20 text-white/80 hover:bg-purple-500/20 hover:border-purple-400/50 hover:text-white hover:glow-border-purple transition-all duration-300"
                  >
                    <AlertCircle className="w-6 h-6 mb-2 text-purple-400" />
                    <span className="text-sm">경고 알림</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
            </div>
          )}

          {/* 📈 통계분석 탭 */}
          {activeTab === 'analytics' && (
            <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatsCard
                title="일일 활성 사용자"
                value={analytics?.daily_active_users || 0}
                description="오늘 접속자"
                icon={<Activity className="h-4 w-4" />}
                color="text-blue-600"
              />
              <StatsCard
                title="전환율"
                value={`${analytics?.conversion_rate || 0}%`}
                description="방문자 → 회원"
                icon={<TrendingUp className="h-4 w-4" />}
                color="text-green-600"
              />
              <StatsCard
                title="피크 시간대"
                value={analytics?.peak_hours.length || 0}
                description="주요 이용 시간"
                icon={<Clock className="h-4 w-4" />}
                color="text-purple-600"
              />
              <StatsCard
                title="인기 기능 수"
                value={analytics?.popular_features.length || 0}
                description="활발한 서비스"
                icon={<Star className="h-4 w-4" />}
                color="text-yellow-600"
              />
            </div>

            {/* 상세 분석 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 기능별 사용 통계 */}
              <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <BarChart3 className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                    기능별 사용 통계
                  </CardTitle>
                  <CardDescription className="text-white/60">인기 기능 분석 및 성장률</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {analytics?.popular_features.map((feature, index) => (
                      <div key={feature.name} className="space-y-2 p-3 rounded-lg bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
                        <div className="flex justify-between items-center">
                          <span className="text-sm font-medium text-white/80">{feature.name}</span>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-white/60">{feature.usage_count.toLocaleString()}</span>
                            <Badge variant={feature.growth_rate >= 0 ? "default" : "secondary"} className={`text-xs ${
                              feature.growth_rate >= 0 
                                ? 'bg-green-500/20 text-green-300 border-green-400/50' 
                                : 'bg-red-500/20 text-red-300 border-red-400/50'
                            }`}>
                              {feature.growth_rate >= 0 ? '+' : ''}{feature.growth_rate}%
                            </Badge>
                          </div>
                        </div>
                        <Progress 
                          value={(feature.usage_count / 5000) * 100} 
                          className="h-2"
                        />
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 시간대별 분석 */}
              <Card className="cyber-card hover:glow-border-purple transition-all duration-500 group">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white/90 group-hover:glow-text-purple transition-all duration-300">
                    <Clock className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
                    시간대별 이용 패턴
                  </CardTitle>
                  <CardDescription className="text-white/60">사용자 활동 시간 분석</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="text-center p-4 rounded-lg bg-white/5 backdrop-blur-sm border border-white/10">
                      <div className="text-2xl font-bold text-white/90 glow-text-purple mb-2">
                        {analytics?.daily_active_users}명
                      </div>
                      <p className="text-sm text-white/60 mb-4">오늘 활성 사용자</p>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-medium text-white/80 mb-3">주요 피크 시간대</h4>
                      <div className="space-y-2">
                        {analytics?.peak_hours.map((hour, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:bg-white/10 transition-all duration-300">
                            <span className="text-sm text-white/80">{hour}</span>
                            <Badge variant="outline" className="bg-purple-500/20 text-purple-300 border-purple-400/50">피크</Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
            </div>
          )}
        </div>

        {/* 하단 상태 바 - 사이버 판타지 스타일 */}
        <div className="cyber-card p-4 mt-6 hover:glow-border-purple transition-all duration-500">
          <div className="flex items-center justify-between text-sm text-white/80">
            <div className="flex items-center gap-4">
              <span className="glow-text-purple">🔮 HEAL7 사주 관리자 시스템 v2.0.0</span>
              <StatusBadge status="healthy">서비스 정상</StatusBadge>
              <Badge className="bg-purple-500/20 text-purple-300 border-purple-400/50">
                7개 탭 관리 시스템
              </Badge>
            </div>
            <div className="flex items-center gap-4 text-white/60">
              <span>사주 해석 DB: {interpretationData.length}개</span>
              <span>© 2025 HEAL7</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SajuAdminDashboard;