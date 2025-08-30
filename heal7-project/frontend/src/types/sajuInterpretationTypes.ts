// 사주 풀이 내용 입력 타입 정의

// 십신 (10개)
export type SipsinType = '비견' | '겁재' | '식신' | '상관' | '편재' | '정재' | '칠살' | '정관' | '편인' | '정인';

export interface SipsinInterpretation {
  name: SipsinType;
  korean_name: string;
  description: string;
  personality_traits: string[];
  fortune_aspects: {
    career: string;
    money: string;
    relationship: string;
    health: string;
  };
  compatibility: string[];
  keywords: string[];
  advice: string;
}

// 천간 (10개) - 갑을병정무기경신임계
export type CheonganType = '갑' | '을' | '병' | '정' | '무' | '기' | '경' | '신' | '임' | '계';

export interface CheonganInterpretation {
  name: CheonganType;
  chinese_char: string;
  element: '목' | '화' | '토' | '금' | '수';
  yin_yang: '양' | '음';
  description: string;
  personality_traits: string[];
  career_aptitude: string[];
  relationships: string;
  health_points: string[];
  keywords: string[];
}

// 지지 (12개) - 자축인묘진사오미신유술해
export type JijiType = '자' | '축' | '인' | '묘' | '진' | '사' | '오' | '미' | '신' | '유' | '술' | '해';

export interface JijiInterpretation {
  name: JijiType;
  chinese_char: string;
  zodiac_animal: string;
  element: '목' | '화' | '토' | '금' | '수';
  season: '봄' | '여름' | '가을' | '겨울';
  direction: '동' | '서' | '남' | '북' | '중앙';
  time_period: string;
  description: string;
  personality_traits: string[];
  fortune_tendency: string;
  compatibility: string[];
  keywords: string[];
}

// 60갑자
export type GapjaType = string; // 갑자, 을축, 병인, ... (60개)

export interface GapjaInterpretation {
  name: GapjaType;
  cheongan: CheonganType;
  jiji: JijiType;
  napyin: string; // 납음
  element_combination: string;
  description: string;
  personality_summary: string;
  life_pattern: string;
  fortune_cycle: {
    youth: string;
    middle_age: string;
    later_life: string;
  };
  compatibility_ratings: Record<GapjaType, number>; // 1-5 점수
  keywords: string[];
  advice: string;
}

// 지장간
export interface JijangganInterpretation {
  jiji: JijiType;
  main_gan: CheonganType;
  sub_gans: CheonganType[];
  energy_distribution: Record<CheonganType, number>; // 에너지 비율
  description: string;
  influence_on_personality: string[];
  seasonal_effects: string;
}

// 격국 (格局)
export type GeokgukType = '건록격' | '양인격' | '식신격' | '상관격' | '편재격' | '정재격' | '칠살격' | '정관격' | '편인격' | '정인격' | '특수격';

export interface GeokgukInterpretation {
  name: GeokgukType;
  description: string;
  formation_conditions: string[];
  personality_characteristics: string[];
  life_tendencies: string[];
  career_directions: string[];
  fortune_patterns: string[];
  strengths: string[];
  weaknesses: string[];
  advice: string[];
  keywords: string[];
}

// 오행
export type OhaengType = '목' | '화' | '토' | '금' | '수';

export interface OhaengInterpretation {
  name: OhaengType;
  color: string;
  direction: string;
  season: string;
  characteristics: string[];
  personality_when_strong: string[];
  personality_when_weak: string[];
  health_aspects: string[];
  career_fields: string[];
  relationships: {
    generates: OhaengType; // 생성 관계
    generated_by: OhaengType;
    controls: OhaengType; // 극복 관계
    controlled_by: OhaengType;
  };
  balance_advice: string[];
  keywords: string[];
}

// 전체 사주 풀이 데이터 구조
export interface SajuInterpretationData {
  sipsin: Record<SipsinType, SipsinInterpretation>;
  cheongan: Record<CheonganType, CheonganInterpretation>;
  jiji: Record<JijiType, JijiInterpretation>;
  gapja: Record<GapjaType, GapjaInterpretation>;
  jijanggan: Record<JijiType, JijangganInterpretation>;
  geokguk: Record<GeokgukType, GeokgukInterpretation>;
  ohaeng: Record<OhaengType, OhaengInterpretation>;
}

// 사주 풀이 관리 API 인터페이스
export interface SajuInterpretationManagement {
  id: string;
  category: 'sipsin' | 'cheongan' | 'jiji' | 'gapja' | 'jijanggan' | 'geokguk' | 'ohaeng';
  name: string;
  content: any; // 각 카테고리별 interpretation 타입
  created_at: string;
  updated_at: string;
  created_by: string;
  status: 'draft' | 'published' | 'archived';
  version: number;
}

// 사주 풀이 검색 필터
export interface SajuInterpretationFilter {
  category?: ('sipsin' | 'cheongan' | 'jiji' | 'gapja' | 'jijanggan' | 'geokguk' | 'ohaeng')[];
  name?: string;
  status?: ('draft' | 'published' | 'archived')[];
  created_from?: string;
  created_to?: string;
  search_query?: string;
}

// 사주 풀이 통계
export interface SajuInterpretationStats {
  total_entries: number;
  by_category: Record<string, number>;
  by_status: Record<string, number>;
  recent_updates: number;
  completion_rate: number;
}