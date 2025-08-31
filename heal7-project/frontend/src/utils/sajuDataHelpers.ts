import { SajuAdminSettings, SajuLogicSettings } from '../types/sajuAdminTypes';

/**
 * 사주 데이터 안전한 접근을 위한 헬퍼 함수들
 */

// 타입 가드 함수
export const isSajuAdminSettings = (data: any): data is SajuAdminSettings => {
  return data && 
    typeof data === 'object' &&
    typeof data.version === 'string' &&
    data.logic_settings &&
    typeof data.logic_settings === 'object';
};

export const hasLogicSettings = (settings: any): settings is { logic_settings: SajuLogicSettings } => {
  return settings && 
    settings.logic_settings && 
    typeof settings.logic_settings === 'object';
};

// 안전한 데이터 접근 헬퍼
export const safeGetLogicType = (settings: SajuAdminSettings | null): string => {
  if (!settings) return 'hybrid';
  if (!hasLogicSettings(settings)) return 'hybrid';
  return settings.logic_settings?.logic_type || 'hybrid';
};

export const safeGetLogicSettings = (settings: SajuAdminSettings | null): SajuLogicSettings => {
  if (!settings || !hasLogicSettings(settings)) {
    return {
      logic_type: 'hybrid',
      use_kasi_precision: true,
      manseeryeok_count: 60,
      hybrid_voting_threshold: 0.7,
      accuracy_priority: 'balanced',
      calendar_system: 'lunar_solar_hybrid',
      solar_term_method: 'astronomical',
      leap_month_handling: 'traditional_rules',
      ai_validation: true,
      parallel_computation: true,
      apply_sidubup: true,
      apply_woldubup: false,
      detailed_jijanggan: true
    };
  }
  
  return {
    ...settings.logic_settings,
    // 기본값 보장
    logic_type: settings.logic_settings?.logic_type || 'hybrid',
    use_kasi_precision: settings.logic_settings?.use_kasi_precision ?? true,
    manseeryeok_count: settings.logic_settings?.manseeryeok_count || 60,
    hybrid_voting_threshold: settings.logic_settings?.hybrid_voting_threshold || 0.7,
    accuracy_priority: settings.logic_settings?.accuracy_priority || 'balanced',
    calendar_system: settings.logic_settings?.calendar_system || 'lunar_solar_hybrid',
    solar_term_method: settings.logic_settings?.solar_term_method || 'astronomical',
    leap_month_handling: settings.logic_settings?.leap_month_handling || 'traditional_rules',
    ai_validation: settings.logic_settings?.ai_validation ?? true,
    parallel_computation: settings.logic_settings?.parallel_computation ?? true,
    apply_sidubup: settings.logic_settings?.apply_sidubup ?? true,
    apply_woldubup: settings.logic_settings?.apply_woldubup ?? false,
    detailed_jijanggan: settings.logic_settings?.detailed_jijanggan ?? true
  };
};

export const safeGetTimeSettings = (settings: SajuAdminSettings | null) => {
  if (!settings || !settings.time_settings) {
    return {
      timezone_system: 'standard' as const,
      use_sidubup: true,
      use_woldubup: false,
      calendar_system: 'gregorian' as const
    };
  }
  
  return {
    timezone_system: settings.time_settings?.timezone_system || 'standard',
    use_sidubup: settings.time_settings?.use_sidubup ?? true,
    use_woldubup: settings.time_settings?.use_woldubup ?? false,
    calendar_system: settings.time_settings?.calendar_system || 'gregorian'
  };
};

export const safeGetGeographicSettings = (settings: SajuAdminSettings | null) => {
  if (!settings || !settings.geographic_settings) {
    return {
      default_country: 'KR' as const,
      longitude_offset: 126.978,
      latitude_offset: 37.5665,
      timezone_offset: 9,
      altitude: 50,
      auto_detect_location: true,
      consider_dst: true,
      use_local_mean_time: false,
      apply_equation_of_time: true,
      atmospheric_refraction: true,
      country_longitudes: { KR: 126.978 }
    };
  }
  
  return {
    ...settings.geographic_settings,
    default_country: settings.geographic_settings?.default_country || 'KR',
    longitude_offset: settings.geographic_settings?.longitude_offset || 126.978,
    latitude_offset: settings.geographic_settings?.latitude_offset || 37.5665,
    timezone_offset: settings.geographic_settings?.timezone_offset || 9,
    country_longitudes: settings.geographic_settings?.country_longitudes || { KR: 126.978 }
  };
};

export const safeGetKasiSettings = (settings: SajuAdminSettings | null) => {
  if (!settings || !settings.kasi_settings) {
    return {
      api_key: '***',
      base_url: 'https://astro.kasi.re.kr',
      use_cache: true,
      cache_ttl: 3600,
      api_version: 'v1',
      show_api_key: false,
      request_timeout: 10000,
      retry_attempts: 3,
      max_concurrent: 5,
      ssl_verify: true,
      log_level: 'INFO',
      enabled_bodies: {
        sun: true,
        moon: true,
        mercury: true,
        venus: true,
        mars: true,
        jupiter: true,
        saturn: true,
        uranus: false,
        neptune: false,
        pluto: false
      }
    };
  }
  
  return {
    ...settings.kasi_settings,
    api_key: settings.kasi_settings?.api_key || '***',
    base_url: settings.kasi_settings?.base_url || 'https://astro.kasi.re.kr',
    use_cache: settings.kasi_settings?.use_cache ?? true,
    cache_ttl: settings.kasi_settings?.cache_ttl || 3600,
    enabled_bodies: settings.kasi_settings?.enabled_bodies || {
      sun: true, moon: true, mercury: true, venus: true, mars: true,
      jupiter: true, saturn: true, uranus: false, neptune: false, pluto: false
    }
  };
};

// 안전한 설정 업데이트 헬퍼
export const safeUpdateLogicSettings = (
  settings: SajuAdminSettings | null, 
  updates: Partial<SajuLogicSettings>
): SajuAdminSettings => {
  const currentSettings: SajuAdminSettings = settings || {
    version: '2.0.0',
    last_updated: new Date().toISOString(),
    updated_by: 'admin',
    time_settings: safeGetTimeSettings(null),
    geographic_settings: safeGetGeographicSettings(null),
    logic_settings: safeGetLogicSettings(null),
    kasi_settings: safeGetKasiSettings(null),
    cheongan_interpretations: {},
    jiji_interpretations: {},
    gapja_interpretations: {}
  };

  const updatedLogicSettings: SajuLogicSettings = {
    ...safeGetLogicSettings(currentSettings),
    ...updates,
    // logic_type이 항상 정의되도록 보장
    logic_type: updates.logic_type || safeGetLogicSettings(currentSettings).logic_type
  };

  return {
    ...currentSettings,
    logic_settings: updatedLogicSettings,
    last_updated: new Date().toISOString()
  };
};

// 에러 바운더리용 안전한 렌더링 헬퍼
export const renderSafeValue = (value: any, fallback: string = 'N/A'): string => {
  if (value === null || value === undefined) return fallback;
  if (typeof value === 'boolean') return value ? '활성' : '비활성';
  if (typeof value === 'number') return value.toString();
  if (typeof value === 'string') return value;
  return fallback;
};

// 설정 유효성 검증
export const validateSajuSettings = (settings: any): { isValid: boolean; errors: string[] } => {
  const errors: string[] = [];
  
  if (!settings) {
    errors.push('설정 데이터가 없습니다');
    return { isValid: false, errors };
  }
  
  if (!settings.logic_settings) {
    errors.push('logic_settings가 누락되었습니다');
  } else {
    if (!settings.logic_settings.logic_type) {
      errors.push('logic_settings.logic_type이 누락되었습니다');
    }
  }
  
  if (!settings.time_settings) {
    errors.push('time_settings가 누락되었습니다');
  }
  
  if (!settings.geographic_settings) {
    errors.push('geographic_settings가 누락되었습니다');
  }
  
  if (!settings.kasi_settings) {
    errors.push('kasi_settings가 누락되었습니다');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};