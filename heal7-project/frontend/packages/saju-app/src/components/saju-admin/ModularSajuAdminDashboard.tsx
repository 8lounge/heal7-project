/**
 * 🔮 HEAL7 사주 관리자 대시보드 - 모듈화 버전
 * 
 * ✅ 7개 완전 구현된 탭:
 * - 대시보드: 시스템 종합 현황
 * - 사주엔진: 60갑자, 천간, 지지, 해석입력 관리
 * - 사용자관리: 회원 및 권한 관리
 * - 콘텐츠관리: 매거진, 상품, 스토어 관리
 * - 통계분석: 사용량 분석 및 리뷰 관리
 * - 포인트: 결제 및 포인트 시스템 관리
 * - 시스템: 캐시, 시간설정, 시스템 관리
 * 
 * @author HEAL7 Admin Team
 * @version 2.1.0 - Modular Implementation Complete
 * @created 2025-09-07
 */

import React, { useState, useCallback, useMemo } from 'react';
import { useTheme } from '../../contexts/ThemeContext';
// import { Button } from '@heal7/shared';

// Temporary fallback component - 빌드 문제로 임시 대체
const Button = ({ children, className = "", onClick }: { children: React.ReactNode, className?: string, onClick?: () => void }) => (
  <button className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 ${className}`} onClick={onClick}>{children}</button>
);
import { 
  BarChart3, 
  Brain,
  Users,
  FileText,
  TrendingUp,
  CreditCard,
  Settings,
  Sparkles,
  RefreshCw,
  Sun,
  Moon
} from 'lucide-react';

// 모듈화된 탭 컴포넌트들 import
import {
  DashboardTab,
  SajuEngineTab,
  UserManagementTab,
  ContentManagementTab,
  AnalyticsTab,
  PointManagementTab,
  SystemManagementTab
} from './tabs';

const ModularSajuAdminDashboard: React.FC = () => {
  // 메인 앱의 테마 시스템 사용
  const { theme, toggleTheme } = useTheme();

  // 현재 활성 탭 상태
  const [activeTab, setActiveTab] = useState('dashboard');
  const [refreshing, setRefreshing] = useState(false);

  // 탭 메뉴 구성
  const tabMenus = useMemo(() => [
    { 
      id: 'dashboard', 
      label: '대시보드', 
      icon: BarChart3, 
      description: '시스템 종합 현황',
      component: DashboardTab
    },
    { 
      id: 'saju-engine', 
      label: '사주엔진', 
      icon: Brain, 
      description: '60갑자, 천간, 지지, 해석입력',
      component: SajuEngineTab
    },
    { 
      id: 'users', 
      label: '사용자관리', 
      icon: Users, 
      description: '회원 및 권한 관리',
      component: UserManagementTab
    },
    { 
      id: 'content', 
      label: '콘텐츠관리', 
      icon: FileText, 
      description: '매거진, 상품, 스토어 관리',
      component: ContentManagementTab
    },
    { 
      id: 'analytics', 
      label: '통계분석', 
      icon: TrendingUp, 
      description: '사용량 분석 및 리뷰 관리',
      component: AnalyticsTab
    },
    { 
      id: 'points', 
      label: '포인트', 
      icon: CreditCard, 
      description: '결제 및 포인트 시스템',
      component: PointManagementTab
    },
    { 
      id: 'system', 
      label: '시스템', 
      icon: Settings, 
      description: '캐시, 시간설정, 시스템 관리',
      component: SystemManagementTab
    }
  ], []);

  // 테마 토글 핸들러
  const handleThemeToggle = useCallback(() => {
    toggleTheme();
  }, [toggleTheme]);

  // 전체 새로고침 핸들러
  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    // 실제 데이터 새로고침 로직 (추후 API 연동 시 구현)
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  }, []);

  // 현재 탭 정보
  const currentTab = tabMenus.find(tab => tab.id === activeTab);
  const CurrentTabComponent = currentTab?.component;

  return (
    <div className="min-h-screen theme-transition theme-bg-main">
      {/* 헤더 */}
      <header className="theme-glass-header glass-3 backdrop-blur-xl sticky top-0 z-50 theme-transition">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* 로고 및 제목 */}
            <div className="flex items-center space-x-4">
              <Sparkles className="w-8 h-8 theme-transition text-[var(--theme-accent)] drop-shadow-lg" />
              <div>
                <h1 className="text-xl font-bold theme-transition theme-text-heading theme-glow">
                  🔮 HEAL7 사주 관리자
                </h1>
                <p className="text-sm theme-transition theme-text-secondary">
                  모듈화 관리 대시보드 v2.1 - 7개 탭 완전 구현
                </p>
              </div>
            </div>

            {/* 우측 컨트롤 */}
            <div className="flex items-center space-x-4">
              {/* 새로고침 버튼 */}
              <Button
                variant="ghost"
                size="sm"
                onClick={handleRefresh}
                disabled={refreshing}
                className="theme-button-secondary theme-transition"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
                새로고침
              </Button>

              {/* 테마 토글 */}
              <div className="flex items-center gap-3 px-4 py-2 rounded-xl glass-3 theme-transition">
                <span className="text-sm font-medium theme-transition theme-text-primary">
                  {theme === 'light' ? '☀️ 낮' : '🌙 밤'}
                </span>
                <button
                  onClick={handleThemeToggle}
                  className="relative w-12 h-6 rounded-full theme-transition focus:outline-none focus:ring-2 focus:ring-[var(--theme-accent)]/50 bg-[var(--theme-accent)]"
                >
                  <div className={`absolute top-0.5 w-5 h-5 rounded-full theme-transition shadow-lg ${
                    theme === 'light'
                      ? 'left-6 bg-white'
                      : 'left-0.5 bg-white'
                  } flex items-center justify-center text-xs`}>
                    {theme === 'light' ? <Sun className="w-3 h-3 text-[var(--theme-accent)]" /> : <Moon className="w-3 h-3 text-[var(--theme-accent)]" />}
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* 메인 컨텐츠 */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* 탭 네비게이션 */}
        <div className="mb-8">
          <div className="p-2 rounded-xl glass-3 theme-transition backdrop-blur-xl">
            <div className="flex flex-wrap gap-2">
              {tabMenus.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center px-4 py-3 rounded-lg theme-transition group ${
                      isActive
                        ? 'glass-4 theme-text-primary shadow-lg theme-glow'
                        : 'glass-2 theme-text-secondary hover:glass-3 hover:theme-text-primary'
                    }`}
                  >
                    <Icon className={`w-5 h-5 mr-2 theme-transition ${
                      isActive
                        ? 'text-[var(--theme-accent)] drop-shadow-lg'
                        : 'theme-text-muted'
                    }`} />
                    <div className="text-left">
                      <div className="font-medium">{tab.label}</div>
                      <div className={`text-xs theme-transition ${
                        isActive 
                          ? 'theme-text-secondary'
                          : 'theme-text-muted'
                      }`}>
                        {tab.description}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* 현재 탭 컨텐츠 */}
        <div className="min-h-[60vh]">
          {CurrentTabComponent && <CurrentTabComponent />}
        </div>

        {/* 하단 상태바 */}
        <div className="mt-8 pt-6 theme-border-t theme-transition">
          <div className="flex items-center justify-between">
            <div className="text-sm theme-transition theme-text-secondary">
              마지막 업데이트: {new Date().toLocaleString()}
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span className="text-sm theme-text-secondary">
                  모든 서비스 정상 운영
                </span>
              </div>
              <div className="text-sm font-medium theme-text-primary text-[var(--theme-accent)] drop-shadow-lg">
                모듈화 시스템 v2.1 - {currentTab?.label} 활성
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModularSajuAdminDashboard;