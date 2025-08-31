// 사주 관리자 대시보드 타입 정의
export interface SajuAdminSettings {
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

export interface TimeSettings {
  timezone_system: 'standard' | 'apparent_solar';
  use_sidubup: boolean;
  use_woldubup: boolean;
  calendar_system: 'julian' | 'gregorian';
}

export interface GeographicSettings {
  default_country: 'KR' | 'US' | 'JP' | 'CN' | 'EU' | 'IN' | 'AU' | 'CA' | 'BR' | 'RU' | 'ID' | 'HK';
  longitude_offset: number;
  latitude_offset?: number;
  timezone_offset: number;
  altitude?: number;
  auto_detect_location?: boolean;
  consider_dst?: boolean;
  use_local_mean_time?: boolean;
  apply_equation_of_time?: boolean;
  atmospheric_refraction?: boolean;
  country_longitudes: Record<string, number>;
}

export interface SajuLogicSettings {
  logic_type: 'traditional' | 'modern' | 'hybrid';
  use_kasi_precision: boolean;
  manseeryeok_count: number;
  hybrid_voting_threshold: number;
  accuracy_priority?: 'speed' | 'balanced' | 'precision';
  calendar_system?: 'pure_lunar' | 'solar_based' | 'lunar_solar_hybrid';
  solar_term_method?: 'fixed_dates' | 'astronomical' | 'precise_astronomical';
  leap_month_handling?: 'ignore' | 'traditional_rules' | 'modern_calculation';
  ai_validation?: boolean;
  parallel_computation?: boolean;
  apply_sidubup?: boolean;
  apply_woldubup?: boolean;
  detailed_jijanggan?: boolean;
}

export interface KasiSettings {
  api_key: string;
  base_url: string;
  use_cache: boolean;
  cache_ttl: number;
  api_version?: string;
  show_api_key?: boolean;
  request_timeout?: number;
  retry_attempts?: number;
  max_concurrent?: number;
  ssl_verify?: boolean;
  log_level?: string;
  enabled_bodies?: Record<string, boolean>;
}

export interface CheonganInterpretation {
  korean_name: string;
  chinese_char: string;
  element: string;
  yin_yang: string;
  keywords: string[];
  description: string;
  personality_traits: string[];
}

export interface JijiInterpretation {
  korean_name: string;
  chinese_char: string;
  zodiac_animal: string;
  element: string;
  season: string;
  keywords: string[];
  description: string;
  personality_traits: string[];
}

export interface GapjaInterpretation {
  korean_name: string;
  cheongan: string;
  jiji: string;
  napyin: string;
  keywords: string[];
  description: string;
  compatibility: Record<string, any>;
  fortune_aspects: Record<string, any>;
}