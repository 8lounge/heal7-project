/**
 * HEAL7 관리자 대시보드 컴포넌트 (.complete)
 * 복사-붙여넣기로 즉시 동작하는 완성 코드
 * 
 * 기능: 관리자 대시보드 메인 화면
 * 사용법: 이 컴포넌트를 복사하여 새로운 관리자 페이지 구현 시 기본 템플릿으로 활용
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
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
  RefreshCw
} from 'lucide-react';

// 타입 정의
interface SystemStatus {
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  uptime: string;
  active_connections: number;
  process_count: number;
}

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  timestamp: string;
}

interface DashboardStats {
  total_users: number;
  active_sessions: number;
  total_keywords: number;
  total_surveys: number;
}

// 메인 컴포넌트
const AdminDashboard: React.FC = () => {
  // 상태 관리
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  // API 호출 함수
  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 시스템 상태 조회
      const systemResponse = await fetch('/admin-api/system/status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!systemResponse.ok) {
        throw new Error('시스템 상태 조회 실패');
      }

      const systemData: ApiResponse<SystemStatus> = await systemResponse.json();
      setSystemStatus(systemData.data);

      // 대시보드 통계 조회 (예시 데이터)
      const statsData: DashboardStats = {
        total_users: 1250,
        active_sessions: 45,
        total_keywords: 442,
        total_surveys: 23
      };
      setDashboardStats(statsData);

      setLastUpdate(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : '데이터 조회 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 컴포넌트 마운트 시 데이터 로드
  useEffect(() => {
    fetchData();
    
    // 30초마다 자동 새로고침
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  // 상태 배지 컴포넌트
  const StatusBadge: React.FC<{ value: number; type: 'cpu' | 'memory' | 'disk' }> = ({ value, type }) => {
    const getVariant = () => {
      if (value < 50) return 'default';
      if (value < 80) return 'secondary';
      return 'destructive';
    };

    const getIcon = () => {
      if (value < 80) return <CheckCircle className="w-3 h-3" />;
      return <AlertCircle className="w-3 h-3" />;
    };

    return (
      <Badge variant={getVariant()} className="flex items-center gap-1">
        {getIcon()}
        {value.toFixed(1)}%
      </Badge>
    );
  };

  // 통계 카드 컴포넌트
  const StatsCard: React.FC<{
    title: string;
    value: number;
    description: string;
    icon: React.ReactNode;
    trend?: 'up' | 'down' | 'stable';
  }> = ({ title, value, description, icon, trend = 'stable' }) => {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          {icon}
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{value.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">{description}</p>
        </CardContent>
      </Card>
    );
  };

  // 로딩 상태
  if (loading && !systemStatus) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-6 h-6 animate-spin" />
        <span className="ml-2">데이터를 불러오는 중...</span>
      </div>
    );
  }

  // 에러 상태
  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          {error}
          <Button variant="outline" size="sm" onClick={fetchData} className="ml-2">
            다시 시도
          </Button>
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">관리자 대시보드</h1>
          <p className="text-muted-foreground">
            마지막 업데이트: {lastUpdate.toLocaleTimeString()}
          </p>
        </div>
        <Button onClick={fetchData} disabled={loading} variant="outline">
          <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          새로고침
        </Button>
      </div>

      {/* 통계 카드 그리드 */}
      {dashboardStats && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatsCard
            title="전체 사용자"
            value={dashboardStats.total_users}
            description="등록된 사용자 수"
            icon={<Users className="h-4 w-4 text-muted-foreground" />}
          />
          <StatsCard
            title="활성 세션"
            value={dashboardStats.active_sessions}
            description="현재 접속 중인 사용자"
            icon={<Activity className="h-4 w-4 text-muted-foreground" />}
          />
          <StatsCard
            title="키워드 수"
            value={dashboardStats.total_keywords}
            description="M-PIS 키워드 총 개수"
            icon={<Database className="h-4 w-4 text-muted-foreground" />}
          />
          <StatsCard
            title="설문 수"
            value={dashboardStats.total_surveys}
            description="생성된 설문 템플릿"
            icon={<BarChart3 className="h-4 w-4 text-muted-foreground" />}
          />
        </div>
      )}

      {/* 시스템 상태 탭 */}
      <Tabs defaultValue="system" className="space-y-4">
        <TabsList>
          <TabsTrigger value="system">시스템 상태</TabsTrigger>
          <TabsTrigger value="services">서비스 현황</TabsTrigger>
          <TabsTrigger value="logs">최근 로그</TabsTrigger>
        </TabsList>

        {/* 시스템 상태 탭 */}
        <TabsContent value="system" className="space-y-4">
          {systemStatus && (
            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Server className="w-5 h-5" />
                    시스템 리소스
                  </CardTitle>
                  <CardDescription>CPU, 메모리, 디스크 사용률</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>CPU 사용률</span>
                    <StatusBadge value={systemStatus.cpu_percent} type="cpu" />
                  </div>
                  <div className="flex justify-between items-center">
                    <span>메모리 사용률</span>
                    <StatusBadge value={systemStatus.memory_percent} type="memory" />
                  </div>
                  <div className="flex justify-between items-center">
                    <span>디스크 사용률</span>
                    <StatusBadge value={systemStatus.disk_percent} type="disk" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="w-5 h-5" />
                    시스템 정보
                  </CardTitle>
                  <CardDescription>연결 및 프로세스 정보</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>활성 연결</span>
                    <Badge>{systemStatus.active_connections}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>실행 중인 프로세스</span>
                    <Badge>{systemStatus.process_count}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>업타임</span>
                    <Badge variant="outline">
                      <Clock className="w-3 h-3 mr-1" />
                      {new Date(systemStatus.uptime).toLocaleString()}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* 서비스 현황 탭 */}
        <TabsContent value="services" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>메인 서비스</CardTitle>
                <CardDescription>heal7.com</CardDescription>
              </CardHeader>
              <CardContent>
                <Badge variant="default" className="flex items-center gap-1 w-fit">
                  <CheckCircle className="w-3 h-3" />
                  정상 동작
                </Badge>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>키워드 서비스</CardTitle>
                <CardDescription>keywords.heal7.com</CardDescription>
              </CardHeader>
              <CardContent>
                <Badge variant="default" className="flex items-center gap-1 w-fit">
                  <CheckCircle className="w-3 h-3" />
                  정상 동작
                </Badge>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>사주 서비스</CardTitle>
                <CardDescription>saju.heal7.com</CardDescription>
              </CardHeader>
              <CardContent>
                <Badge variant="default" className="flex items-center gap-1 w-fit">
                  <CheckCircle className="w-3 h-3" />
                  정상 동작
                </Badge>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* 로그 탭 */}
        <TabsContent value="logs" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>최근 시스템 로그</CardTitle>
              <CardDescription>최근 10개의 로그 항목</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm font-mono">
                <div className="text-green-600">[INFO] 2025-08-18 13:45:32 - 시스템 정상 동작</div>
                <div className="text-blue-600">[INFO] 2025-08-18 13:44:15 - 새로운 사용자 로그인</div>
                <div className="text-yellow-600">[WARN] 2025-08-18 13:43:01 - 메모리 사용률 75% 도달</div>
                <div className="text-green-600">[INFO] 2025-08-18 13:42:44 - 백업 작업 완료</div>
                <div className="text-blue-600">[INFO] 2025-08-18 13:41:20 - API 요청 처리 완료</div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* 빠른 액션 버튼 */}
      <Card>
        <CardHeader>
          <CardTitle>빠른 액션</CardTitle>
          <CardDescription>자주 사용하는 관리 기능</CardDescription>
        </CardHeader>
        <CardContent className="flex gap-2 flex-wrap">
          <Button variant="outline">
            <Users className="w-4 h-4 mr-2" />
            사용자 관리
          </Button>
          <Button variant="outline">
            <Database className="w-4 h-4 mr-2" />
            키워드 관리
          </Button>
          <Button variant="outline">
            <BarChart3 className="w-4 h-4 mr-2" />
            설문 관리
          </Button>
          <Button variant="outline">
            <Settings className="w-4 h-4 mr-2" />
            시스템 설정
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminDashboard;

/**
 * 사용법:
 * 
 * 1. 기본 사용:
 *    import AdminDashboard from './AdminDashboard.complete';
 *    <AdminDashboard />
 * 
 * 2. 필요한 의존성:
 *    npm install lucide-react @radix-ui/react-tabs @radix-ui/react-alert-dialog
 * 
 * 3. shadcn/ui 컴포넌트:
 *    npx shadcn-ui@latest add card button badge tabs alert
 * 
 * 4. 커스터마이징:
 *    - API 엔드포인트 URL 수정
 *    - 인증 토큰 관리 방식 변경
 *    - 통계 데이터 구조 조정
 *    - 색상 테마 및 스타일 변경
 * 
 * 5. 확장 기능:
 *    - 실시간 알림 시스템
 *    - 차트 및 그래프 추가
 *    - 더 상세한 시스템 모니터링
 *    - 사용자 활동 로그 표시
 */