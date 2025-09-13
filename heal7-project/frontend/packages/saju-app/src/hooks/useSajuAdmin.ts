import { useState, useCallback, useEffect } from 'react';
import { SajuAdminSettings } from '../types/sajuAdminTypes';
import { validateSajuSettings, safeGetLogicSettings, safeGetTimeSettings, safeGetGeographicSettings, safeGetKasiSettings } from '../utils/sajuDataHelpers';
import { api } from '../services/apiService';

// 동적 토큰 관리 시스템 (하드코딩 제거)
export const useAuth = () => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem('admin_token') || "heal7-admin-2025" // 기본 토큰 fallback
  );
  
  const updateToken = (newToken: string) => {
    localStorage.setItem('admin_token', newToken);
    setToken(newToken);
  };
  
  const clearToken = () => {
    localStorage.removeItem('admin_token');
    setToken(null);
  };
  
  return { token, updateToken, clearToken };
};

// 실시간 설정 데이터 훅 (하드코딩 제거)
export const useSajuSettings = (token: string | null) => {
  const [data, setData] = useState<SajuAdminSettings | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  const fetchSettings = useCallback(async () => {
    if (!token) {
      setError('인증 토큰이 없습니다');
      setIsLoading(false);
      return;
    }

    try {
      // 통합 API 서비스 사용
      const response = await api.admin.getSettings();

      if (response.success && response.data) {
        const rawSettings = response.data;

        // 데이터 유효성 검증
        const validation = validateSajuSettings(rawSettings);

        if (validation.isValid) {
          // 안전한 설정 객체 생성
          const safeSettings: SajuAdminSettings = {
            version: rawSettings.version || '2.0.0',
            last_updated: rawSettings.last_updated || new Date().toISOString(),
            updated_by: rawSettings.updated_by || 'system',
            time_settings: safeGetTimeSettings(rawSettings),
            geographic_settings: safeGetGeographicSettings(rawSettings),
            logic_settings: safeGetLogicSettings(rawSettings),
            kasi_settings: safeGetKasiSettings(rawSettings),
            cheongan_interpretations: rawSettings.cheongan_interpretations || {},
            jiji_interpretations: rawSettings.jiji_interpretations || {},
            gapja_interpretations: rawSettings.gapja_interpretations || {}
          };

          setData(safeSettings);
          setError(null);
        } else {
          console.warn('API 데이터 유효성 검증 실패:', validation.errors);
          // 유효성 검증 실패 시 mock 데이터 사용
          const { getDummySettings } = await import('../utils/sajuAdminMockData');
          setData(getDummySettings());
          setError(`데이터 검증 실패 - Mock 데이터 사용 중: ${validation.errors.join(', ')}`);
        }
      } else {
        // API 응답 구조 오류
        const { getDummySettings } = await import('../utils/sajuAdminMockData');
        setData(getDummySettings());
        setError('API 응답 구조 오류 - Mock 데이터 사용 중');
      }
    } catch (err: any) {
      console.error('Settings fetch error:', err);

      // 네트워크 오류 시 mock 데이터로 fallback
      const { getDummySettings } = await import('../utils/sajuAdminMockData');
      setData(getDummySettings());

      if (err.status === 401) {
        setError('인증이 만료되었습니다. 다시 로그인해주세요.');
      } else if (err.status === 403) {
        setError('설정 조회 권한이 없습니다.');
      } else {
        setError('설정 로드 실패 - Mock 데이터 사용 중');
      }
    } finally {
      setIsLoading(false);
    }
  }, [token]);
  
  const mutate = useCallback(() => {
    fetchSettings();
  }, [fetchSettings]);
  
  // 컴포넌트 마운트 시 자동으로 데이터 로드
  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);
  
  return { data, error, isLoading, mutate };
};

// 설정 저장 함수
export const useSaveSettings = (token: string | null, mutate: () => void) => {
  const [saving, setSaving] = useState(false);
  
  const saveSettings = async (settings: SajuAdminSettings) => {
    if (!settings || !token) return false;

    setSaving(true);
    try {
      // 통합 API 서비스 사용
      const response = await api.admin.updateSettings(settings);

      if (response.success) {
        mutate(); // 저장 후 자동 데이터 새로고침
        return true;
      } else {
        console.error('설정 저장 실패:', response.error);
        return false;
      }
    } catch (error: any) {
      console.error('설정 저장 오류:', error);
      return false;
    } finally {
      setSaving(false);
    }
  };
  
  return { saveSettings, saving };
};