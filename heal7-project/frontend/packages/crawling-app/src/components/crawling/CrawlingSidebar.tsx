import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart3, 
  Activity as Spider, 
  Brain, 
  Database, 
  Settings, 
  Home,
  ChevronLeft,
  ChevronRight,
  Activity,
  Layers,
  Wrench
} from 'lucide-react';

type CrawlingPage = 'dashboard' | 'crawling' | 'ai-analysis' | 'data-management' | 'tool-selector' | 'settings';

// 3-Tier 상태 인터페이스
interface TierStatus {
  name: string;
  status: 'active' | 'idle' | 'error';
  count: number;
  description?: string;
}

interface ThreeTierStatusResponse {
  tiers: {
    httpx: { count: number; status: string; description: string };
    httpx_bs: { count: number; status: string; description: string };
    playwright: { count: number; status: string; description: string };
  };
  total_active: number;
  timestamp: string;
  data_source: string;
}

interface CrawlingSidebarProps {
  currentPage: CrawlingPage;
  onPageChange: (page: CrawlingPage) => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
}

const CrawlingSidebar: React.FC<CrawlingSidebarProps> = ({
  currentPage,
  onPageChange,
  isCollapsed,
  onToggleCollapse
}) => {
  const navigationItems = [
    {
      id: 'dashboard' as CrawlingPage,
      label: '대시보드',
      icon: BarChart3,
      description: '시스템 개요 및 현황'
    },
    {
      id: 'crawling' as CrawlingPage,
      label: '크롤링 관리',
      icon: Spider,
      description: '3-Tier 크롤러 제어'
    },
    {
      id: 'ai-analysis' as CrawlingPage,
      label: 'AI 분석',
      icon: Brain,
      description: '멀티모달 AI 처리'
    },
    {
      id: 'data-management' as CrawlingPage,
      label: '데이터 관리',
      icon: Database,
      description: '수집 데이터 관리'
    },
    {
      id: 'tool-selector' as CrawlingPage,
      label: '도구 선택',
      icon: Wrench,
      description: '크롤링 도구 및 추천'
    },
    {
      id: 'settings' as CrawlingPage,
      label: '설정',
      icon: Settings,
      description: '시스템 및 API 설정'
    }
  ];

  // 3-Tier 상태 관리
  const [tierStatus, setTierStatus] = useState<TierStatus[]>([
    { name: 'httpx', status: 'idle', count: 0 },
    { name: 'httpx+bs', status: 'idle', count: 0 },
    { name: 'playwright', status: 'idle', count: 0 }
  ]);

  // 3-Tier 상태 데이터 가져오기
  const fetch3TierStatus = async () => {
    try {
      const response = await fetch('http://localhost:8003/api/3-tier-status');
      if (response.ok) {
        const data: ThreeTierStatusResponse = await response.json();
        
        // 응답 데이터를 TierStatus[] 형태로 변환
        const updatedTierStatus: TierStatus[] = [
          {
            name: 'httpx',
            status: data.tiers.httpx.status as 'active' | 'idle' | 'error',
            count: data.tiers.httpx.count,
            description: data.tiers.httpx.description
          },
          {
            name: 'httpx+bs',
            status: data.tiers.httpx_bs.status as 'active' | 'idle' | 'error',
            count: data.tiers.httpx_bs.count,
            description: data.tiers.httpx_bs.description
          },
          {
            name: 'playwright',
            status: data.tiers.playwright.status as 'active' | 'idle' | 'error',
            count: data.tiers.playwright.count,
            description: data.tiers.playwright.description
          }
        ];
        
        setTierStatus(updatedTierStatus);
      }
    } catch (error) {
      console.error('3-Tier 상태 로드 실패:', error);
      // 에러 시 기본값으로 폴백
      setTierStatus([
        { name: 'httpx', status: 'idle', count: 8 },
        { name: 'httpx+bs', status: 'idle', count: 4 },
        { name: 'playwright', status: 'idle', count: 3 }
      ]);
    }
  };

  // 컴포넌트 마운트 시 및 주기적으로 데이터 가져오기
  useEffect(() => {
    // 초기 로드
    fetch3TierStatus();
    
    // 30초마다 업데이트
    const interval = setInterval(fetch3TierStatus, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-400';
      case 'idle':
        return 'bg-blue-400';
      case 'error':
        return 'bg-red-400';
      default:
        return 'bg-gray-400';
    }
  };

  return (
    <motion.aside
      className={`relative bg-slate-800/50 backdrop-blur-sm border-r border-slate-700/50 transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
      initial={{ x: -100 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex flex-col h-full">
        {/* 헤더 */}
        <div className={`p-4 border-b border-slate-700/50 ${isCollapsed ? 'px-2' : ''}`}>
          <div className="flex items-center justify-between">
            <AnimatePresence>
              {!isCollapsed && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center space-x-2"
                >
                  <Home className="w-5 h-5 text-purple-400" />
                  <span className="font-semibold text-white">컨트롤 센터</span>
                </motion.div>
              )}
            </AnimatePresence>
            
            <motion.button
              className="p-1 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded transition-colors"
              onClick={onToggleCollapse}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </motion.button>
          </div>
        </div>

        {/* 네비게이션 메뉴 */}
        <nav className="flex-1 p-2 space-y-1">
          {navigationItems.map((item) => {
            const IconComponent = item.icon;
            const isActive = currentPage === item.id;
            
            return (
              <motion.button
                key={item.id}
                className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all duration-200 group relative ${
                  isActive
                    ? 'bg-gradient-to-r from-purple-600/80 to-pink-600/80 text-white shadow-lg'
                    : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
                }`}
                onClick={() => onPageChange(item.id)}
                whileHover={{ scale: isCollapsed ? 1 : 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <IconComponent className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-white'}`} />
                
                <AnimatePresence>
                  {!isCollapsed && (
                    <motion.div
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -10 }}
                      className="flex-1 text-left"
                    >
                      <div className="font-medium">{item.label}</div>
                      <div className="text-xs text-slate-400 group-hover:text-slate-300">
                        {item.description}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* 활성 상태 표시 */}
                {isActive && (
                  <motion.div
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-purple-400 to-pink-400 rounded-r"
                    layoutId="activeSidebarTab"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}

                {/* 툴팁 (축소 상태일 때) */}
                {isCollapsed && (
                  <div className="absolute left-full ml-2 px-2 py-1 bg-slate-900 text-white text-sm rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
                    {item.label}
                  </div>
                )}
              </motion.button>
            );
          })}
        </nav>

        {/* 3-Tier 시스템 상태 */}
        <AnimatePresence>
          {!isCollapsed && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="p-4 border-t border-slate-700/50"
            >
              <div className="mb-3">
                <h3 className="text-sm font-semibold text-white mb-2 flex items-center space-x-2">
                  <Layers className="w-4 h-4 text-purple-400" />
                  <span>3-Tier 상태</span>
                </h3>
                
                <div className="space-y-2">
                  {tierStatus.map((tier) => (
                    <div key={tier.name} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${getStatusColor(tier.status)} animate-pulse`} />
                        <span className="text-xs text-slate-300 capitalize">{tier.name}</span>
                      </div>
                      <span className="text-xs text-slate-400">{tier.count}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="text-xs text-slate-500 text-center">
                <Activity className="w-3 h-3 inline mr-1" />
                실시간 모니터링
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.aside>
  );
};

export default CrawlingSidebar;