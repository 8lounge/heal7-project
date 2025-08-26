import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Button } from '../ui/button';
import { Switch } from '../ui/switch';
import { AlertCircle, Save, RefreshCw, Settings, Database, Globe, Clock, Brain, Book } from 'lucide-react';

// API 인터페이스
interface SajuAdminSettings {
  version: string;
  last_updated: string;
  updated_by: string;
  time_settings: TimeSettings;
  geographic_settings: GeographicSettings;
  logic_settings: SajuLogicSettings;
  kasi_settings: KasiSettings;
  cheongan_interpretations: Record<string, CheonganInterpretation>;
  jiji_interpretations: Record<string, JijiInterpretation>;
  gapja_interpretations: Record<string, GapjaInterpretation>;
}

interface TimeSettings {
  timezone_system: 'standard' | 'apparent_solar';
  use_sidubup: boolean;
  use_woldubup: boolean;
  calendar_system: 'julian' | 'gregorian';
}

interface GeographicSettings {
  default_country: 'KR' | 'US' | 'JP' | 'CN' | 'EU';
  longitude_offset: number;
  timezone_offset: number;
  country_longitudes: Record<string, number>;
}

interface SajuLogicSettings {
  logic_type: 'traditional' | 'modern' | 'hybrid';
  use_kasi_precision: boolean;
  manseeryeok_count: number;
  hybrid_voting_threshold: number;
}

interface KasiSettings {
  api_key: string;
  base_url: string;
  use_cache: boolean;
  cache_ttl: number;
}

interface CheonganInterpretation {
  korean_name: string;
  chinese_char: string;
  element: string;
  yin_yang: string;
  keywords: string[];
  description: string;
  personality_traits: string[];
}

interface JijiInterpretation {
  korean_name: string;
  chinese_char: string;
  zodiac_animal: string;
  element: string;
  season: string;
  keywords: string[];
  description: string;
  personality_traits: string[];
}

interface GapjaInterpretation {
  korean_name: string;
  cheongan: string;
  jiji: string;
  napyin: string;
  keywords: string[];
  description: string;
  compatibility: Record<string, string>;
  fortune_aspects: Record<string, string>;
}

const ADMIN_TOKEN = "heal7-admin-2025"; // 임시 토큰
const API_BASE = "/api/admin/saju";

export const SajuAdminDashboard: React.FC = () => {
  const [settings, setSettings] = useState<SajuAdminSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  // 설정 로드
  const loadSettings = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/settings`, {
        headers: {
          'Authorization': `Bearer ${ADMIN_TOKEN}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSettings(data);
      } else {
        console.error('설정 로드 실패:', await response.text());
      }
    } catch (error) {
      console.error('설정 로드 오류:', error);
    } finally {
      setLoading(false);
    }
  };

  // 설정 저장
  const saveSettings = async () => {
    if (!settings) return;
    
    setSaving(true);
    try {
      const response = await fetch(`${API_BASE}/settings`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${ADMIN_TOKEN}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
      });
      
      if (response.ok) {
        alert('설정이 성공적으로 저장되었습니다.');
      } else {
        alert('설정 저장에 실패했습니다.');
      }
    } catch (error) {
      console.error('설정 저장 오류:', error);
      alert('설정 저장 중 오류가 발생했습니다.');
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    loadSettings();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-6 h-6 animate-spin mr-2" />
        <span>설정을 불러오는 중...</span>
      </div>
    );
  }

  if (!settings) {
    return (
      <div className="flex items-center justify-center h-64">
        <AlertCircle className="w-6 h-6 text-red-500 mr-2" />
        <span>설정을 불러올 수 없습니다.</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">🔮 HEAL7 사주 관리자 대시보드</h1>
          <p className="text-white/80">사주 계산 로직의 모든 설정을 관리하는 중앙 통제 시스템</p>
          
          {/* 액션 버튼들 */}
          <div className="flex gap-4 mt-4">
            <Button onClick={loadSettings} variant="outline" size="sm">
              <RefreshCw className="w-4 h-4 mr-2" />
              새로고침
            </Button>
            <Button onClick={saveSettings} disabled={saving} size="sm">
              <Save className="w-4 h-4 mr-2" />
              {saving ? '저장 중...' : '설정 저장'}
            </Button>
          </div>
        </div>

        {/* 상태 정보 카드 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 text-center">
            <h3 className="font-semibold text-sm text-white/80">설정 버전</h3>
            <p className="text-2xl font-bold text-blue-300">{settings.version}</p>
          </div>
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 text-center">
            <h3 className="font-semibold text-sm text-white/80">로직 타입</h3>
            <div className="mt-1 px-2 py-1 bg-purple-500/30 text-purple-200 text-xs rounded-full inline-block">
              {settings.logic_settings.logic_type}
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 text-center">
            <h3 className="font-semibold text-sm text-white/80">만세력 데이터</h3>
            <p className="text-2xl font-bold text-green-300">
              {settings.logic_settings.manseeryeok_count.toLocaleString()}개
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 text-center">
            <h3 className="font-semibold text-sm text-white/80">최종 수정</h3>
            <p className="text-sm text-white/70">
              {new Date(settings.last_updated).toLocaleString('ko-KR')}
            </p>
          </div>
        </div>

        {/* 메인 탭 시스템 */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Settings className="w-4 h-4" />
              개요
            </TabsTrigger>
            <TabsTrigger value="time" className="flex items-center gap-2">
              <Clock className="w-4 h-4" />
              시간 설정
            </TabsTrigger>
            <TabsTrigger value="geographic" className="flex items-center gap-2">
              <Globe className="w-4 h-4" />
              지리 설정
            </TabsTrigger>
            <TabsTrigger value="logic" className="flex items-center gap-2">
              <Brain className="w-4 h-4" />
              로직 설정
            </TabsTrigger>
            <TabsTrigger value="kasi" className="flex items-center gap-2">
              <Database className="w-4 h-4" />
              KASI 설정
            </TabsTrigger>
            <TabsTrigger value="interpretations" className="flex items-center gap-2">
              <Book className="w-4 h-4" />
              해석 관리
            </TabsTrigger>
          </TabsList>

          {/* 개요 탭 */}
          <TabsContent value="overview">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                <h3 className="text-lg font-bold text-white mb-4">핵심 설정 현황</h3>
                <div className="space-y-4">
                  <div className="flex justify-between text-white">
                    <span>시간 체계:</span>
                    <div className={`px-2 py-1 rounded-full text-xs ${settings.time_settings.timezone_system === 'apparent_solar' ? 'bg-green-500/30 text-green-200' : 'bg-gray-500/30 text-gray-200'}`}>
                      {settings.time_settings.timezone_system === 'apparent_solar' ? '진태양시' : '표준시'}
                    </div>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>달력 시스템:</span>
                    <div className="px-2 py-1 bg-purple-500/30 text-purple-200 rounded-full text-xs">
                      {settings.time_settings.calendar_system === 'gregorian' ? '그레고리력' : '율리우스력'}
                    </div>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>시두법 적용:</span>
                    <div className={`px-2 py-1 rounded-full text-xs ${settings.time_settings.use_sidubup ? 'bg-green-500/30 text-green-200' : 'bg-gray-500/30 text-gray-200'}`}>
                      {settings.time_settings.use_sidubup ? '적용' : '미적용'}
                    </div>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>월두법 적용:</span>
                    <div className={`px-2 py-1 rounded-full text-xs ${settings.time_settings.use_woldubup ? 'bg-green-500/30 text-green-200' : 'bg-gray-500/30 text-gray-200'}`}>
                      {settings.time_settings.use_woldubup ? '적용' : '미적용'}
                    </div>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>기준 국가:</span>
                    <div className="px-2 py-1 bg-blue-500/30 text-blue-200 rounded-full text-xs">
                      {settings.geographic_settings.default_country}
                    </div>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>KASI 정밀 계산:</span>
                    <div className={`px-2 py-1 rounded-full text-xs ${settings.logic_settings.use_kasi_precision ? 'bg-green-500/30 text-green-200' : 'bg-gray-500/30 text-gray-200'}`}>
                      {settings.logic_settings.use_kasi_precision ? '사용' : '미사용'}
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                <h3 className="text-lg font-bold text-white mb-4">해석 데이터 통계</h3>
                <div className="space-y-4">
                  <div className="flex justify-between text-white">
                    <span>천간 해석:</span>
                    <span className="font-bold text-blue-300">{Object.keys(settings.cheongan_interpretations).length}개</span>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>지지 해석:</span>
                    <span className="font-bold text-green-300">{Object.keys(settings.jiji_interpretations).length}개</span>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>60갑자 해석:</span>
                    <span className="font-bold text-purple-300">{Object.keys(settings.gapja_interpretations).length}개</span>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>하이브리드 임계값:</span>
                    <span className="font-bold text-amber-300">{settings.logic_settings.hybrid_voting_threshold}</span>
                  </div>
                  <div className="flex justify-between text-white">
                    <span>캐시 TTL:</span>
                    <span className="font-bold text-pink-300">{settings.kasi_settings.cache_ttl}초</span>
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>

          {/* 시간 설정 탭 */}
          <TabsContent value="time">
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-4">⏰ 시간 관련 설정</h3>
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium mb-2 text-white">시간 체계</label>
                    <select
                      value={settings.time_settings.timezone_system}
                      onChange={(e) => setSettings({
                        ...settings,
                        time_settings: {
                          ...settings.time_settings,
                          timezone_system: e.target.value as 'standard' | 'apparent_solar'
                        }
                      })}
                      className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                    >
                      <option value="standard" className="text-gray-800">표준시 (Standard Time)</option>
                      <option value="apparent_solar" className="text-gray-800">진태양시 (Apparent Solar Time)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-white">달력 시스템</label>
                    <select
                      value={settings.time_settings.calendar_system}
                      onChange={(e) => setSettings({
                        ...settings,
                        time_settings: {
                          ...settings.time_settings,
                          calendar_system: e.target.value as 'julian' | 'gregorian'
                        }
                      })}
                      className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                    >
                      <option value="gregorian" className="text-gray-800">그레고리력 (Gregorian Calendar)</option>
                      <option value="julian" className="text-gray-800">율리우스력 (Julian Calendar)</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="flex items-center justify-between p-4 bg-white/10 border border-white/20 rounded-md">
                    <div>
                      <h3 className="font-medium text-white">시두법 적용</h3>
                      <p className="text-sm text-white/70">시간 계산에 시두법을 적용합니다</p>
                    </div>
                    <Switch
                      checked={settings.time_settings.use_sidubup}
                      onCheckedChange={(checked) => setSettings({
                        ...settings,
                        time_settings: {
                          ...settings.time_settings,
                          use_sidubup: checked
                        }
                      })}
                    />
                  </div>

                  <div className="flex items-center justify-between p-4 bg-white/10 border border-white/20 rounded-md">
                    <div>
                      <h3 className="font-medium text-white">월두법 적용</h3>
                      <p className="text-sm text-white/70">월 계산에 월두법을 적용합니다</p>
                    </div>
                    <Switch
                      checked={settings.time_settings.use_woldubup}
                      onCheckedChange={(checked) => setSettings({
                        ...settings,
                        time_settings: {
                          ...settings.time_settings,
                          use_woldubup: checked
                        }
                      })}
                    />
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>

          {/* 다른 탭들도 비슷하게 구현... */}
          {/* 지리적 설정, 로직 설정, KASI 설정, 해석 관리 탭들 */}

        </Tabs>
      </div>
    </div>
  );
};

export default SajuAdminDashboard;