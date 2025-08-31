import { SajuAdminSettings } from '../types/sajuAdminTypes';

// 더미 설정 데이터 (API 실패 시 사용) - fallback 용도로 유지
export const getDummySettings = (): SajuAdminSettings => ({
  version: "v2.1.0",
  last_updated: new Date().toISOString(),
  updated_by: "admin",
  time_settings: {
    timezone_system: "apparent_solar",
    use_sidubup: true,
    use_woldubup: false,
    calendar_system: "gregorian"
  },
  geographic_settings: {
    default_country: "KR",
    longitude_offset: 127.0,
    latitude_offset: 37.5,
    timezone_offset: 9,
    altitude: 50,
    auto_detect_location: true,
    consider_dst: false,
    use_local_mean_time: true,
    apply_equation_of_time: true,
    atmospheric_refraction: true,
    country_longitudes: {
      KR: 127.0,
      US: -95.7,
      JP: 139.7,
      CN: 116.4,
      EU: 9.5,
      IN: 77.2,
      AU: 133.8,
      CA: -106.3,
      BR: -47.9,
      RU: 105.3,
      ID: 113.9,
      HK: 114.2
    }
  },
  logic_settings: {
    logic_type: "hybrid",
    use_kasi_precision: true,
    manseeryeok_count: 60,
    hybrid_voting_threshold: 0.7,
    accuracy_priority: "balanced",
    calendar_system: "lunar_solar_hybrid",
    solar_term_method: "astronomical",
    leap_month_handling: "traditional_rules",
    ai_validation: true,
    parallel_computation: true,
    apply_sidubup: true,
    apply_woldubup: false,
    detailed_jijanggan: true
  },
  kasi_settings: {
    api_key: "***",
    base_url: "https://astro.kasi.re.kr",
    use_cache: true,
    cache_ttl: 3600,
    api_version: "v1",
    show_api_key: false,
    request_timeout: 10000,
    retry_attempts: 3,
    max_concurrent: 5,
    ssl_verify: true,
    log_level: "INFO",
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
  },
  cheongan_interpretations: {
    갑: { korean_name: "갑", chinese_char: "甲", element: "목", yin_yang: "양", keywords: ["리더십"], description: "갑목", personality_traits: ["강인함"] },
    을: { korean_name: "을", chinese_char: "乙", element: "목", yin_yang: "음", keywords: ["유연함"], description: "을목", personality_traits: ["온화함"] },
    병: { korean_name: "병", chinese_char: "丙", element: "화", yin_yang: "양", keywords: ["열정"], description: "병화", personality_traits: ["활발함"] },
    정: { korean_name: "정", chinese_char: "丁", element: "화", yin_yang: "음", keywords: ["섬세함"], description: "정화", personality_traits: ["세심함"] },
    무: { korean_name: "무", chinese_char: "戊", element: "토", yin_yang: "양", keywords: ["안정"], description: "무토", personality_traits: ["신뢰성"] },
    기: { korean_name: "기", chinese_char: "己", element: "토", yin_yang: "음", keywords: ["포용"], description: "기토", personality_traits: ["포용력"] },
    경: { korean_name: "경", chinese_char: "庚", element: "금", yin_yang: "양", keywords: ["강직"], description: "경금", personality_traits: ["결단력"] },
    신: { korean_name: "신", chinese_char: "辛", element: "금", yin_yang: "음", keywords: ["정교함"], description: "신금", personality_traits: ["정밀함"] },
    임: { korean_name: "임", chinese_char: "壬", element: "수", yin_yang: "양", keywords: ["지혜"], description: "임수", personality_traits: ["지적"] },
    계: { korean_name: "계", chinese_char: "癸", element: "수", yin_yang: "음", keywords: ["직관"], description: "계수", personality_traits: ["감성적"] }
  },
  jiji_interpretations: {
    자: { korean_name: "자", chinese_char: "子", zodiac_animal: "쥐", element: "수", season: "겨울", keywords: ["시작"], description: "자수", personality_traits: ["적응력"] },
    축: { korean_name: "축", chinese_char: "丑", zodiac_animal: "소", element: "토", season: "겨울", keywords: ["인내"], description: "축토", personality_traits: ["끈기"] },
    인: { korean_name: "인", chinese_char: "寅", zodiac_animal: "호랑이", element: "목", season: "봄", keywords: ["용기"], description: "인목", personality_traits: ["대담함"] },
    묘: { korean_name: "묘", chinese_char: "卯", zodiac_animal: "토끼", element: "목", season: "봄", keywords: ["성장"], description: "묘목", personality_traits: ["성장성"] },
    진: { korean_name: "진", chinese_char: "辰", zodiac_animal: "용", element: "토", season: "봄", keywords: ["변화"], description: "진토", personality_traits: ["변혁성"] },
    사: { korean_name: "사", chinese_char: "巳", zodiac_animal: "뱀", element: "화", season: "여름", keywords: ["지혜"], description: "사화", personality_traits: ["직관력"] },
    오: { korean_name: "오", chinese_char: "午", zodiac_animal: "말", element: "화", season: "여름", keywords: ["역동"], description: "오화", personality_traits: ["활동력"] },
    미: { korean_name: "미", chinese_char: "未", zodiac_animal: "양", element: "토", season: "여름", keywords: ["온화"], description: "미토", personality_traits: ["친화력"] },
    신: { korean_name: "신", chinese_char: "申", zodiac_animal: "원숭이", element: "금", season: "가을", keywords: ["민첩"], description: "신금", personality_traits: ["기민함"] },
    유: { korean_name: "유", chinese_char: "酉", zodiac_animal: "닭", element: "금", season: "가을", keywords: ["정확"], description: "유금", personality_traits: ["정확성"] },
    술: { korean_name: "술", chinese_char: "戌", zodiac_animal: "개", element: "토", season: "가을", keywords: ["충성"], description: "술토", personality_traits: ["충실함"] },
    해: { korean_name: "해", chinese_char: "亥", zodiac_animal: "돼지", element: "수", season: "겨울", keywords: ["풍요"], description: "해수", personality_traits: ["풍부함"] }
  },
  gapja_interpretations: {
    갑자: { korean_name: "갑자", cheongan: "갑", jiji: "자", napyin: "해중금", keywords: ["새로운 시작", "창조"], description: "갑자 해중금 - 새로운 시작과 창조의 에너지", compatibility: { best: ["을축", "병인"], worst: ["무오", "기미"] }, fortune_aspects: { career: "창업", love: "새로운 만남", health: "활력증진" } },
    을축: { korean_name: "을축", cheongan: "을", jiji: "축", napyin: "해중금", keywords: ["끈기", "신뢰"], description: "을축 해중금 - 신뢰할 수 있는 안정감", compatibility: { best: ["갑자", "정묘"], worst: ["신미", "임신"] }, fortune_aspects: { career: "안정", love: "장기연애", health: "점진적 회복" } },
    병인: { korean_name: "병인", cheongan: "병", jiji: "인", napyin: "로중화", keywords: ["열정", "용기"], description: "병인 로중화 - 불같은 열정과 용기", compatibility: { best: ["갑자", "정묘"], worst: ["경신", "신유"] }, fortune_aspects: { career: "도전", love: "열정적 사랑", health: "에너지 충만" } },
    정묘: { korean_name: "정묘", cheongan: "정", jiji: "묘", napyin: "로중화", keywords: ["섬세함", "예술"], description: "정묘 로중화 - 섬세하고 예술적 감각", compatibility: { best: ["을축", "병인"], worst: ["유유", "임술"] }, fortune_aspects: { career: "예술", love: "로맨틱", health: "정신건강" } },
    무진: { korean_name: "무진", cheongan: "무", jiji: "진", napyin: "대림목", keywords: ["변화", "성장"], description: "무진 대림목 - 변화 속에서 성장", compatibility: { best: ["기사", "경오"], worst: ["갑술", "을해"] }, fortune_aspects: { career: "변화관리", love: "성장하는 관계", health: "체력증진" } },
    기사: { korean_name: "기사", cheongan: "기", jiji: "사", napyin: "대림목", keywords: ["지혜", "직관"], description: "기사 대림목 - 지혜롭고 직관적인", compatibility: { best: ["무진", "신미"], worst: ["계해", "갑자"] }, fortune_aspects: { career: "상담", love: "영적인 만남", health: "내적 평화" } },
    경오: { korean_name: "경오", cheongan: "경", jiji: "오", napyin: "로방토", keywords: ["강직", "역동"], description: "경오 로방토 - 강직하고 역동적인", compatibility: { best: ["무진", "임신"], worst: ["병자", "정축"] }, fortune_aspects: { career: "리더십", love: "활발한 연애", health: "운동" } },
    신미: { korean_name: "신미", cheongan: "신", jiji: "미", napyin: "로방토", keywords: ["정교함", "온화"], description: "신미 로방토 - 정교하고 온화한", compatibility: { best: ["기사", "계해"], worst: ["을축", "무진"] }, fortune_aspects: { career: "기술", love: "안정된 관계", health: "균형" } },
    임신: { korean_name: "임신", cheongan: "임", jiji: "신", napyin: "검봉금", keywords: ["지혜", "민첩"], description: "임신 검봉금 - 지혜롭고 민첩한", compatibility: { best: ["경오", "갑술"], worst: ["병인", "정묘"] }, fortune_aspects: { career: "전략", love: "지적 매력", health: "정신력" } },
    계유: { korean_name: "계유", cheongan: "계", jiji: "유", napyin: "검봉금", keywords: ["직관", "정확"], description: "계유 검봉금 - 직관적이고 정확한", compatibility: { best: ["을해", "정축"], worst: ["신미", "임신"] }, fortune_aspects: { career: "분석", love: "이해심", health: "세심한 관리" } }
  }
});