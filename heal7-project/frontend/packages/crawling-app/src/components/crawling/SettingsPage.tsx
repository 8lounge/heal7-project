/**
 * ⚙️ 크롤링 시스템 설정 페이지
 * - 시스템 설정 관리
 * - API 키 관리
 * - 크롤러 설정
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { crawlingAPI } from '../../api/CrawlingAPIClient';
import {
  Settings,
  Key,
  Globe,
  Clock,
  Shield,
  Database,
  Zap,
  Save,
  RefreshCw,
  AlertCircle,
  CheckCircle,
  Eye,
  EyeOff,
  Server,
  Bell,
  Volume2,
  Monitor
} from 'lucide-react';

interface SystemSettings {
  autoRefresh: boolean;
  refreshInterval: number;
  notifications: boolean;
  soundAlerts: boolean;
  realTimeUpdates: boolean;
  darkMode: boolean;
  maxRetries: number;
  timeout: number;
  concurrentConnections: number;
  logLevel: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
}

interface CrawlerSettings {
  httpx: {
    enabled: boolean;
    timeout: number;
    maxRetries: number;
    userAgent: string;
  };
  playwright: {
    enabled: boolean;
    headless: boolean;
    timeout: number;
    viewport: { width: number; height: number };
  };
  httpx_bs: {
    enabled: boolean;
    parser: 'lxml' | 'html.parser' | 'html5lib';
    timeout: number;
    encoding: 'auto' | 'utf-8' | 'gbk';
  };
}

interface APIKeys {
  openai: string;
  anthropic: string;
  google: string;
}

const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'system' | 'crawler' | 'api' | 'security'>('system');
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({});

  // 설정 상태들
  const [systemSettings, setSystemSettings] = useState<SystemSettings>({
    autoRefresh: true,
    refreshInterval: 5000,
    notifications: true,
    soundAlerts: false,
    realTimeUpdates: true,
    darkMode: true,
    maxRetries: 3,
    timeout: 30000,
    concurrentConnections: 10,
    logLevel: 'INFO'
  });

  const [crawlerSettings, setCrawlerSettings] = useState<CrawlerSettings>({
    httpx: {
      enabled: true,
      timeout: 30,
      maxRetries: 3,
      userAgent: 'heal7-crawler/2.1'
    },
    playwright: {
      enabled: true,
      headless: true,
      timeout: 60,
      viewport: { width: 1920, height: 1080 }
    },
    httpx_bs: {
      enabled: true,
      parser: 'lxml',
      timeout: 30,
      encoding: 'auto'
    }
  });

  const [apiKeys, setAPIKeys] = useState<APIKeys>({
    openai: '',
    anthropic: '',
    google: ''
  });

  // 설정 로드
  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await crawlingAPI.getSettings();
      if (data) {
        setSystemSettings(data.system);
        setCrawlerSettings(data.crawler);
        console.log('설정 로드 완료');
      }
    } catch (error) {
      console.error('설정 로드 실패:', error);
    }
  };

  const saveSettings = async () => {
    setIsSaving(true);
    setSaveStatus('idle');

    try {
      const success = await crawlingAPI.updateSettings({
        system: systemSettings,
        crawler: crawlerSettings,
        apiKeys: apiKeys
      });
      
      setSaveStatus(success ? 'success' : 'error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } catch (error) {
      console.error('설정 저장 실패:', error);
      setSaveStatus('error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } finally {
      setIsSaving(false);
    }
  };

  const resetToDefaults = () => {
    setSystemSettings({
      autoRefresh: true,
      refreshInterval: 5000,
      notifications: true,
      soundAlerts: false,
      realTimeUpdates: true,
      darkMode: true,
      maxRetries: 3,
      timeout: 30000,
      concurrentConnections: 10,
      logLevel: 'INFO'
    });
  };

  const togglePasswordVisibility = (field: string) => {
    setShowPasswords(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  const GlassBox: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
    <motion.div
      className={`
        relative bg-gradient-to-br from-slate-900/40 via-slate-800/30 to-slate-900/40
        backdrop-blur-xl border border-slate-600/30
        rounded-2xl overflow-hidden
        shadow-2xl shadow-black/20
        before:absolute before:inset-0 before:bg-gradient-to-br 
        before:from-white/5 before:via-transparent before:to-transparent
        before:rounded-2xl before:pointer-events-none
        ${className}
      `}
      whileHover={{ 
        scale: 1.01,
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.4)'
      }}
    >
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );

  const renderSystemSettings = () => (
    <div className="space-y-6">
      <GlassBox className="p-6">
        <h3 className="flex items-center text-lg font-semibold text-slate-200 mb-4">
          <Monitor className="w-5 h-5 mr-2 text-blue-400" />
          모니터링 설정
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="flex items-center text-sm text-slate-300">
              <input
                type="checkbox"
                checked={systemSettings.autoRefresh}
                onChange={(e) => setSystemSettings(prev => ({ ...prev, autoRefresh: e.target.checked }))}
                className="mr-2 rounded border-slate-600 bg-slate-700 text-blue-500"
              />
              자동 새로고침 활성화
            </label>
          </div>
          
          <div className="space-y-2">
            <label className="block text-sm text-slate-300">
              새로고침 간격 (초)
            </label>
            <input
              type="number"
              min="1"
              max="60"
              value={systemSettings.refreshInterval / 1000}
              onChange={(e) => setSystemSettings(prev => ({ ...prev, refreshInterval: parseInt(e.target.value) * 1000 }))}
              className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </GlassBox>

      <GlassBox className="p-6">
        <h3 className="flex items-center text-lg font-semibold text-slate-200 mb-4">
          <Bell className="w-5 h-5 mr-2 text-yellow-400" />
          알림 설정
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <label className="flex items-center text-sm text-slate-300">
              <input
                type="checkbox"
                checked={systemSettings.notifications}
                onChange={(e) => setSystemSettings(prev => ({ ...prev, notifications: e.target.checked }))}
                className="mr-2 rounded border-slate-600 bg-slate-700 text-yellow-500"
              />
              알림 활성화
            </label>
          </div>
          
          <div className="space-y-2">
            <label className="flex items-center text-sm text-slate-300">
              <input
                type="checkbox"
                checked={systemSettings.soundAlerts}
                onChange={(e) => setSystemSettings(prev => ({ ...prev, soundAlerts: e.target.checked }))}
                className="mr-2 rounded border-slate-600 bg-slate-700 text-yellow-500"
              />
              소리 알림
            </label>
          </div>
          
          <div className="space-y-2">
            <label className="flex items-center text-sm text-slate-300">
              <input
                type="checkbox"
                checked={systemSettings.realTimeUpdates}
                onChange={(e) => setSystemSettings(prev => ({ ...prev, realTimeUpdates: e.target.checked }))}
                className="mr-2 rounded border-slate-600 bg-slate-700 text-yellow-500"
              />
              실시간 업데이트
            </label>
          </div>
        </div>
      </GlassBox>

      <GlassBox className="p-6">
        <h3 className="flex items-center text-lg font-semibold text-slate-200 mb-4">
          <Server className="w-5 h-5 mr-2 text-green-400" />
          서버 설정
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <label className="block text-sm text-slate-300">최대 재시도</label>
            <input
              type="number"
              min="1"
              max="10"
              value={systemSettings.maxRetries}
              onChange={(e) => setSystemSettings(prev => ({ ...prev, maxRetries: parseInt(e.target.value) }))}
              className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-green-500"
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-sm text-slate-300">타임아웃 (초)</label>
            <input
              type="number"
              min="5"
              max="300"
              value={systemSettings.timeout / 1000}
              onChange={(e) => setSystemSettings(prev => ({ ...prev, timeout: parseInt(e.target.value) * 1000 }))}
              className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-green-500"
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-sm text-slate-300">동시 연결 수</label>
            <input
              type="number"
              min="1"
              max="50"
              value={systemSettings.concurrentConnections}
              onChange={(e) => setSystemSettings(prev => ({ ...prev, concurrentConnections: parseInt(e.target.value) }))}
              className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-green-500"
            />
          </div>
        </div>
      </GlassBox>
    </div>
  );

  const renderCrawlerSettings = () => (
    <div className="space-y-6">
      {Object.entries(crawlerSettings).map(([tier, settings]) => (
        <GlassBox key={tier} className="p-6">
          <h3 className="flex items-center text-lg font-semibold text-slate-200 mb-4">
            <Zap className={`w-5 h-5 mr-2 ${
              tier === 'httpx' ? 'text-blue-400' :
              tier === 'playwright' ? 'text-purple-400' :
              'text-orange-400'
            }`} />
            {tier.toUpperCase()} 크롤러
          </h3>
          
          <div className="space-y-4">
            <label className="flex items-center text-sm text-slate-300">
              <input
                type="checkbox"
                checked={settings.enabled}
                onChange={(e) => setCrawlerSettings(prev => ({
                  ...prev,
                  [tier]: { ...prev[tier as keyof CrawlerSettings], enabled: e.target.checked }
                }))}
                className="mr-2 rounded border-slate-600 bg-slate-700 text-blue-500"
              />
              {tier} 크롤러 활성화
            </label>
            
            {settings.enabled && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <label className="block text-sm text-slate-300 mb-1">타임아웃 (초)</label>
                  <input
                    type="number"
                    min="10"
                    max="300"
                    value={settings.timeout}
                    onChange={(e) => setCrawlerSettings(prev => ({
                      ...prev,
                      [tier]: { ...prev[tier as keyof CrawlerSettings], timeout: parseInt(e.target.value) }
                    }))}
                    className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-blue-500"
                  />
                </div>
                
                {tier === 'httpx' && 'maxRetries' in settings && (
                  <div>
                    <label className="block text-sm text-slate-300 mb-1">최대 재시도</label>
                    <input
                      type="number"
                      min="1"
                      max="10"
                      value={settings.maxRetries}
                      onChange={(e) => setCrawlerSettings(prev => {
                        const tierKey = tier as keyof CrawlerSettings;
                        return {
                          ...prev,
                          [tierKey]: { ...prev[tierKey], maxRetries: parseInt(e.target.value) }
                        };
                      })}
                      className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-blue-500"
                    />
                  </div>
                )}
                
                {tier === 'playwright' && 'headless' in settings && (
                  <div>
                    <label className="flex items-center text-sm text-slate-300">
                      <input
                        type="checkbox"
                        checked={settings.headless}
                        onChange={(e) => setCrawlerSettings(prev => ({
                          ...prev,
                          [tier]: { ...prev[tier as keyof CrawlerSettings], headless: e.target.checked }
                        }))}
                        className="mr-2 rounded border-slate-600 bg-slate-700 text-blue-500"
                      />
                      헤드리스 모드
                    </label>
                  </div>
                )}
              </div>
            )}
          </div>
        </GlassBox>
      ))}
    </div>
  );

  const renderAPISettings = () => (
    <div className="space-y-6">
      <GlassBox className="p-6">
        <h3 className="flex items-center text-lg font-semibold text-slate-200 mb-4">
          <Key className="w-5 h-5 mr-2 text-purple-400" />
          AI 모델 API 키
        </h3>
        
        <div className="space-y-4">
          {Object.entries(apiKeys).map(([provider, key]) => (
            <div key={provider} className="space-y-2">
              <label className="block text-sm text-slate-300 capitalize">
                {provider === 'google' ? 'Google Gemini' : provider === 'openai' ? 'OpenAI' : 'Anthropic'} API 키
              </label>
              <div className="relative">
                <input
                  type={showPasswords[provider] ? 'text' : 'password'}
                  value={key}
                  onChange={(e) => setAPIKeys(prev => ({ ...prev, [provider]: e.target.value }))}
                  className="w-full px-3 py-2 pr-10 bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-200 focus:outline-none focus:border-purple-500"
                  placeholder={`${provider} API 키를 입력하세요`}
                />
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility(provider)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-200"
                >
                  {showPasswords[provider] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
          <div className="flex items-start">
            <AlertCircle className="w-4 h-4 text-yellow-400 mr-2 mt-0.5" />
            <div className="text-sm text-yellow-200">
              <p className="font-medium">보안 주의사항</p>
              <p className="text-yellow-300/80">API 키는 암호화되어 저장되며, 절대 로그에 기록되지 않습니다.</p>
            </div>
          </div>
        </div>
      </GlassBox>
    </div>
  );

  const tabs = [
    { id: 'system', label: '시스템', icon: Settings },
    { id: 'crawler', label: '크롤러', icon: Globe },
    { id: 'api', label: 'API 키', icon: Key },
    { id: 'security', label: '보안', icon: Shield }
  ];

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-red-400 bg-clip-text text-transparent">
            시스템 설정
          </h1>
          <p className="text-slate-400 mt-1">크롤링 시스템 구성 및 관리</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <motion.button
            onClick={resetToDefaults}
            className="flex items-center px-3 py-2 bg-slate-600/50 hover:bg-slate-600/70 rounded-lg text-sm text-slate-300 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <RefreshCw className="w-4 h-4 mr-1" />
            기본값 복원
          </motion.button>
          
          <motion.button
            onClick={saveSettings}
            disabled={isSaving}
            className={`flex items-center px-4 py-2 rounded-lg text-sm transition-colors ${
              saveStatus === 'success' ? 'bg-green-500/20 text-green-300 border border-green-500/30' :
              saveStatus === 'error' ? 'bg-red-500/20 text-red-300 border border-red-500/30' :
              'bg-blue-500/20 text-blue-300 border border-blue-500/30 hover:bg-blue-500/30'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isSaving ? (
              <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
            ) : saveStatus === 'success' ? (
              <CheckCircle className="w-4 h-4 mr-1" />
            ) : saveStatus === 'error' ? (
              <AlertCircle className="w-4 h-4 mr-1" />
            ) : (
              <Save className="w-4 h-4 mr-1" />
            )}
            {isSaving ? '저장 중...' : 
             saveStatus === 'success' ? '저장 완료' :
             saveStatus === 'error' ? '저장 실패' : '설정 저장'}
          </motion.button>
        </div>
      </div>

      {/* 탭 메뉴 */}
      <GlassBox className="p-4">
        <div className="flex space-x-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center px-4 py-2 rounded-lg text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                }`}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon className="w-4 h-4 mr-2" />
                {tab.label}
              </motion.button>
            );
          })}
        </div>
      </GlassBox>

      {/* 탭 컨텐츠 */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {activeTab === 'system' && renderSystemSettings()}
        {activeTab === 'crawler' && renderCrawlerSettings()}
        {activeTab === 'api' && renderAPISettings()}
        {activeTab === 'security' && (
          <GlassBox className="p-6">
            <h3 className="flex items-center text-lg font-semibold text-slate-200 mb-6">
              <Shield className="w-5 h-5 mr-2 text-green-400" />
              보안 설정
            </h3>
            
            <div className="space-y-6">
              <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                <div className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-400 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-green-300 mb-2">현재 보안 상태</h4>
                    <div className="space-y-1 text-sm text-green-200/80">
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                        SSL/TLS 암호화 연결 활성화
                      </div>
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                        API 키 안전 저장 및 암호화
                      </div>
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                        CORS 보안 정책 적용
                      </div>
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                        세션 기반 인증 시스템
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                <div className="flex items-start">
                  <AlertCircle className="w-5 h-5 text-blue-400 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-blue-300 mb-2">보안 권장사항</h4>
                    <div className="space-y-1 text-sm text-blue-200/80">
                      <p>• API 키는 정기적으로 교체하세요</p>
                      <p>• 크롤링 대상 사이트의 robots.txt를 준수하세요</p>
                      <p>• 시스템 로그를 정기적으로 모니터링하세요</p>
                      <p>• 의심스러운 활동 발견 시 즉시 관리자에게 연락하세요</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-slate-500/10 border border-slate-500/30 rounded-lg">
                <div className="flex items-start">
                  <Clock className="w-5 h-5 text-slate-400 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-slate-300 mb-2">시스템 정보</h4>
                    <div className="space-y-1 text-sm text-slate-400">
                      <p>마지막 보안 업데이트: 2025-08-31</p>
                      <p>보안 프로토콜: TLS 1.3</p>
                      <p>데이터 암호화: AES-256</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </GlassBox>
        )}
      </motion.div>
    </div>
  );
};

export default SettingsPage;