import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus,
  Play,
  Pause,
  Square,
  Settings,
  Target,
  Layers,
  Zap,
  Globe,
  Activity,
  Clock,
  CheckCircle,
  XCircle,
  Eye
} from 'lucide-react';

interface CrawlingJob {
  id: string;
  name: string;
  tier: 'httpx' | 'playwright' | 'selenium';
  status: 'running' | 'paused' | 'completed' | 'failed' | 'queued';
  url: string;
  schedule: string;
  progress: number;
  itemsCollected: number;
  lastRun: string;
  nextRun: string;
  duration: string;
}

interface NewJobForm {
  name: string;
  tier: 'httpx' | 'playwright' | 'selenium';
  url: string;
  schedule: 'once' | 'daily' | 'weekly' | 'monthly';
  selectors: string;
  maxPages: number;
}

const CrawlingManagement: React.FC = () => {
  const [showNewJobModal, setShowNewJobModal] = useState(false);
  const [selectedTier, setSelectedTier] = useState<'all' | 'httpx' | 'playwright' | 'selenium'>('all');
  // const [selectedJob, setSelectedJob] = useState<string | null>(null);
  
  const [jobs, setJobs] = useState<CrawlingJob[]>([
    {
      id: '1',
      name: '정부포털 일반공고',
      tier: 'httpx',
      status: 'running',
      url: 'https://www.gov.kr/portal/ntnadmNews',
      schedule: 'daily',
      progress: 75,
      itemsCollected: 1420,
      lastRun: '2025-08-30 14:30',
      nextRun: '2025-08-31 14:30',
      duration: '45분'
    },
    {
      id: '2',
      name: '꿈해몽 데이터베이스',
      tier: 'playwright',
      status: 'completed',
      url: 'https://dream.co.kr/search',
      schedule: 'weekly',
      progress: 100,
      itemsCollected: 890,
      lastRun: '2025-08-30 12:00',
      nextRun: '2025-09-06 12:00',
      duration: '2시간 15분'
    },
    {
      id: '3',
      name: '사주명리 포털',
      tier: 'selenium',
      status: 'failed',
      url: 'https://saju.example.com',
      schedule: 'daily',
      progress: 30,
      itemsCollected: 245,
      lastRun: '2025-08-30 08:00',
      nextRun: '재시도 필요',
      duration: '15분'
    },
    {
      id: '4',
      name: '운세 정보 수집',
      tier: 'httpx',
      status: 'queued',
      url: 'https://fortune.kr/daily',
      schedule: 'daily',
      progress: 0,
      itemsCollected: 0,
      lastRun: '없음',
      nextRun: '2025-08-30 18:00',
      duration: '예상 30분'
    }
  ]);

  const [newJob, setNewJob] = useState<NewJobForm>({
    name: '',
    tier: 'httpx',
    url: '',
    schedule: 'daily',
    selectors: '',
    maxPages: 10
  });

  const getStatusColor = (status: CrawlingJob['status']) => {
    switch (status) {
      case 'running':
        return 'bg-green-500/20 text-green-300 border border-green-500/30';
      case 'completed':
        return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      case 'paused':
        return 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30';
      case 'failed':
        return 'bg-red-500/20 text-red-300 border border-red-500/30';
      case 'queued':
        return 'bg-gray-500/20 text-gray-300 border border-gray-500/30';
      default:
        return 'bg-gray-500/20 text-gray-300 border border-gray-500/30';
    }
  };

  const getStatusIcon = (status: CrawlingJob['status']) => {
    switch (status) {
      case 'running':
        return <Play className="w-4 h-4" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'paused':
        return <Pause className="w-4 h-4" />;
      case 'failed':
        return <XCircle className="w-4 h-4" />;
      case 'queued':
        return <Clock className="w-4 h-4" />;
      default:
        return <Square className="w-4 h-4" />;
    }
  };

  const getTierIcon = (tier: CrawlingJob['tier']) => {
    switch (tier) {
      case 'httpx':
        return <Zap className="w-5 h-5 text-blue-400" />;
      case 'playwright':
        return <Globe className="w-5 h-5 text-purple-400" />;
      case 'selenium':
        return <Activity className="w-5 h-5 text-orange-400" />;
    }
  };

  const getTierColor = (tier: CrawlingJob['tier']) => {
    switch (tier) {
      case 'httpx':
        return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      case 'playwright':
        return 'bg-purple-500/20 text-purple-300 border border-purple-500/30';
      case 'selenium':
        return 'bg-orange-500/20 text-orange-300 border border-orange-500/30';
    }
  };

  const filteredJobs = selectedTier === 'all' ? jobs : jobs.filter(job => job.tier === selectedTier);

  const handleJobAction = (jobId: string, action: 'start' | 'pause' | 'stop' | 'delete') => {
    setJobs(prev => prev.map(job => {
      if (job.id === jobId) {
        switch (action) {
          case 'start':
            return { ...job, status: 'running' as const };
          case 'pause':
            return { ...job, status: 'paused' as const };
          case 'stop':
            return { ...job, status: 'queued' as const, progress: 0 };
          default:
            return job;
        }
      }
      return job;
    }).filter(job => !(action === 'delete' && job.id === jobId)));
  };

  const handleCreateJob = () => {
    const newJobData: CrawlingJob = {
      id: Date.now().toString(),
      name: newJob.name,
      tier: newJob.tier,
      status: 'queued',
      url: newJob.url,
      schedule: newJob.schedule,
      progress: 0,
      itemsCollected: 0,
      lastRun: '없음',
      nextRun: '대기 중',
      duration: '예상 시간 계산 중'
    };

    setJobs(prev => [...prev, newJobData]);
    setNewJob({
      name: '',
      tier: 'httpx',
      url: '',
      schedule: 'daily',
      selectors: '',
      maxPages: 10
    });
    setShowNewJobModal(false);
  };

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            크롤링 관리
          </h1>
          <p className="text-slate-400 mt-2">작업 생성, 스케줄링 및 3-Tier 시스템 제어</p>
        </div>
        
        <motion.button
          className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg text-white font-medium flex items-center space-x-2"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowNewJobModal(true)}
        >
          <Plus className="w-4 h-4" />
          <span>새 작업 생성</span>
        </motion.button>
      </div>

      {/* 필터 및 통계 */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
        {/* Tier 필터 */}
        <div className="lg:col-span-2 bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-4 border border-slate-600/50">
          <h3 className="text-sm font-semibold text-slate-300 mb-3 flex items-center">
            <Layers className="w-4 h-4 mr-2" />
            Tier 필터
          </h3>
          <div className="flex space-x-2">
            {(['all', 'httpx', 'playwright', 'selenium'] as const).map((tier) => (
              <button
                key={tier}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  selectedTier === tier
                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                    : 'bg-slate-700/50 text-slate-400 hover:text-slate-200 hover:bg-slate-700'
                }`}
                onClick={() => setSelectedTier(tier)}
              >
                {tier === 'all' ? '전체' : tier.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {/* 통계 카드 */}
        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-4 border border-slate-600/50">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-300">{jobs.filter(j => j.status === 'running').length}</div>
            <div className="text-xs text-slate-400">실행 중</div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-4 border border-slate-600/50">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-300">{jobs.filter(j => j.status === 'completed').length}</div>
            <div className="text-xs text-slate-400">완료</div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-4 border border-slate-600/50">
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-300">{jobs.filter(j => j.status === 'queued').length}</div>
            <div className="text-xs text-slate-400">대기 중</div>
          </div>
        </div>
      </div>

      {/* 작업 목록 */}
      <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold flex items-center">
            <Target className="w-5 h-5 mr-2 text-blue-400" />
            작업 목록
          </h2>
          <div className="text-sm text-slate-400">
            총 {filteredJobs.length}개 작업
          </div>
        </div>

        <div className="space-y-4">
          {filteredJobs.map((job) => (
            <motion.div
              key={job.id}
              className="p-4 bg-slate-900/30 rounded-lg border border-slate-700/50 hover:bg-slate-900/50 transition-colors"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              whileHover={{ scale: 1.01 }}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  {getTierIcon(job.tier)}
                  <div>
                    <h3 className="font-semibold text-white">{job.name}</h3>
                    <p className="text-xs text-slate-400 truncate max-w-md">{job.url}</p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-mono ${getTierColor(job.tier)}`}>
                    {job.tier.toUpperCase()}
                  </span>
                </div>

                <div className="flex items-center space-x-3">
                  <div className={`px-3 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(job.status)}`}>
                    {getStatusIcon(job.status)}
                    <span>{job.status === 'running' ? '실행 중' : 
                           job.status === 'completed' ? '완료' :
                           job.status === 'paused' ? '일시정지' :
                           job.status === 'failed' ? '실패' : '대기 중'}</span>
                  </div>

                  <div className="flex items-center space-x-1">
                    {job.status === 'queued' && (
                      <button
                        onClick={() => handleJobAction(job.id, 'start')}
                        className="p-1.5 text-green-400 hover:bg-green-400/20 rounded transition-colors"
                        title="시작"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}
                    
                    {job.status === 'running' && (
                      <button
                        onClick={() => handleJobAction(job.id, 'pause')}
                        className="p-1.5 text-yellow-400 hover:bg-yellow-400/20 rounded transition-colors"
                        title="일시정지"
                      >
                        <Pause className="w-4 h-4" />
                      </button>
                    )}

                    <button
                      onClick={() => handleJobAction(job.id, 'stop')}
                      className="p-1.5 text-red-400 hover:bg-red-400/20 rounded transition-colors"
                      title="정지"
                    >
                      <Square className="w-4 h-4" />
                    </button>

                    <button className="p-1.5 text-slate-400 hover:bg-slate-400/20 rounded transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>

                    <button className="p-1.5 text-slate-400 hover:bg-slate-400/20 rounded transition-colors">
                      <Settings className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 text-sm">
                <div>
                  <span className="text-slate-400">진행률:</span>
                  <div className="flex items-center space-x-2 mt-1">
                    <div className="flex-1 bg-slate-700/50 rounded-full h-1.5">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${job.progress}%` }}
                      />
                    </div>
                    <span className="text-xs text-slate-300 font-mono">{job.progress}%</span>
                  </div>
                </div>

                <div>
                  <span className="text-slate-400">수집량:</span>
                  <div className="text-white font-semibold">{job.itemsCollected.toLocaleString()}</div>
                </div>

                <div>
                  <span className="text-slate-400">스케줄:</span>
                  <div className="text-white">{job.schedule === 'daily' ? '매일' : job.schedule === 'weekly' ? '매주' : job.schedule === 'monthly' ? '매월' : '한번'}</div>
                </div>

                <div>
                  <span className="text-slate-400">마지막 실행:</span>
                  <div className="text-white text-xs">{job.lastRun}</div>
                </div>

                <div>
                  <span className="text-slate-400">다음 실행:</span>
                  <div className="text-white text-xs">{job.nextRun}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* 새 작업 생성 모달 */}
      <AnimatePresence>
        {showNewJobModal && (
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowNewJobModal(false)}
          >
            <motion.div
              className="bg-slate-800 rounded-xl p-6 w-full max-w-2xl border border-slate-700"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                <Plus className="w-6 h-6 mr-2 text-blue-400" />
                새 크롤링 작업 생성
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">작업 이름</label>
                  <input
                    type="text"
                    value={newJob.name}
                    onChange={(e) => setNewJob({ ...newJob, name: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    placeholder="예: 정부포털 데이터 수집"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">크롤러 Tier</label>
                  <select
                    value={newJob.tier}
                    onChange={(e) => setNewJob({ ...newJob, tier: e.target.value as any })}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="httpx">Tier 1 - httpx (빠름)</option>
                    <option value="playwright">Tier 2 - Playwright (중간)</option>
                    <option value="selenium">Tier 3 - Selenium (복잡)</option>
                  </select>
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-slate-300 mb-2">대상 URL</label>
                  <input
                    type="url"
                    value={newJob.url}
                    onChange={(e) => setNewJob({ ...newJob, url: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    placeholder="https://example.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">스케줄</label>
                  <select
                    value={newJob.schedule}
                    onChange={(e) => setNewJob({ ...newJob, schedule: e.target.value as any })}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="once">한 번만</option>
                    <option value="daily">매일</option>
                    <option value="weekly">매주</option>
                    <option value="monthly">매월</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">최대 페이지</label>
                  <input
                    type="number"
                    value={newJob.maxPages}
                    onChange={(e) => setNewJob({ ...newJob, maxPages: parseInt(e.target.value) || 10 })}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    min="1"
                    max="1000"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-slate-300 mb-2">CSS 선택자 (선택사항)</label>
                  <textarea
                    value={newJob.selectors}
                    onChange={(e) => setNewJob({ ...newJob, selectors: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500 resize-none"
                    rows={3}
                    placeholder=".article-title, .content-body, .date"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowNewJobModal(false)}
                  className="px-4 py-2 text-slate-300 hover:text-white transition-colors"
                >
                  취소
                </button>
                <button
                  onClick={handleCreateJob}
                  disabled={!newJob.name || !newJob.url}
                  className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  작업 생성
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CrawlingManagement;