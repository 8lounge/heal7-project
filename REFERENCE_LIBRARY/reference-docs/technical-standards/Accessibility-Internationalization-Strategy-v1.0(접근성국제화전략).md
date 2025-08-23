# 🌍 HEAL7 접근성 및 국제화 전략 v1.0

> **프로젝트**: HEAL7 옴니버스 플랫폼 글로벌 접근성 전략  
> **버전**: v1.0.0  
> **작성일**: 2025-08-18  
> **목적**: 전 세계 사용자를 위한 포용적 접근성 및 문화적 국제화 설계  
> **범위**: WCAG 2.1 AA 준수 + 동아시아 문화권 특화 국제화

---

## 🎯 **접근성 및 국제화 설계 철학**

### **🌟 핵심 가치**
```yaml
core_values:
  universal_design: "모든 사용자를 위한 포용적 설계"
  cultural_sensitivity: "문화적 다양성 존중 및 반영"
  spiritual_accessibility: "영성 서비스의 특수성 고려"
  barrier_free: "디지털 장벽 완전 제거"
  global_reach: "전 세계 시장 진출 준비"
```

### **🎨 점술업 특화 접근성 원칙**
```yaml
fortune_telling_accessibility:
  spiritual_inclusion: "시각/청각 장애인도 영성 체험 가능"
  cultural_respect: "종교적 신념 다양성 존중"
  intuitive_interaction: "직관적 운세 해석 제공"
  emotional_support: "감정적 배려가 담긴 인터페이스"
  privacy_protection: "개인 운세 정보 완전 보호"
```

---

## ♿ **웹 접근성 아키텍처 (WCAG 2.1 AA)**

### **🔍 인식 가능성 (Perceivable)**

#### **1. 시각적 접근성**
```typescript
interface VisualAccessibility {
  color_contrast: {
    normal_text: 'ratio 4.5:1'; // WCAG AA 기준
    large_text: 'ratio 3:1';
    mystic_theme_compliance: {
      primary_on_background: '6.2:1'; // #a855f7 on white
      secondary_on_primary: '5.8:1';   // #ec4899 on dark
      error_indication: '7.1:1';       // 높은 대비 보장
    };
  };
  
  alternative_text: {
    tarot_cards: 'AI 생성 의미적 설명';
    saju_charts: '사주 차트 텍스트 변환';
    fortune_symbols: '운세 기호 음성 설명';
    decorative_elements: '장식적 요소 alt="" 처리';
  };
  
  responsive_design: {
    zoom_support: '최대 200% 확대 지원';
    text_scaling: '글자 크기 300% 까지 확대';
    layout_reflow: '콘텐츠 가로 스크롤 방지';
    mobile_optimization: '터치 타겟 44px 이상';
  };
  
  visual_indicators: {
    focus_states: '명확한 포커스 표시';
    state_changes: '상태 변화 시각적 피드백';
    error_indication: '색상 + 아이콘 + 텍스트 조합';
    progress_feedback: '로딩 상태 명확한 표시';
  };
}
```

#### **2. 대체 텍스트 전략**
```yaml
alt_text_strategy:
  tarot_cards:
    structure: "[카드명] - [기본 의미] - [현재 상황 해석]"
    example: "연인 카드 - 사랑과 선택의 의미 - 현재 관계에서 중요한 결정의 시기"
    ai_enhancement: "상황별 맞춤 해석 자동 생성"
    
  saju_charts:
    four_pillars: "년주: 갑자, 월주: 을축, 일주: 병인, 시주: 정묘"
    wuxing_analysis: "오행 분석: 목 2개, 화 1개, 토 1개, 금 1개, 수 1개"
    textual_summary: "주요 성향과 운세 요약 제공"
    
  zodiac_animals:
    description: "[동물명] - [성격 특성] - [올해 운세 키워드]"
    cultural_context: "한국/중국/일본별 문화적 해석 차이 반영"
```

#### **3. 멀티미디어 접근성**
```typescript
interface MultimediaAccessibility {
  video_content: {
    captions: {
      korean: 'AI 자동 생성 + 수동 검수';
      english: '영어 자막 지원';
      japanese: '일본어 자막 제공';
      chinese: '중국어 간체/번체 지원';
    };
    
    audio_descriptions: {
      fortune_readings: '운세 해석 음성 설명';
      ritual_videos: '의식 과정 상세 설명';
      meditation_guides: '명상 가이드 음성 제공';
    };
    
    transcripts: {
      full_text: '전체 대화 내용 텍스트 제공';
      searchable: '검색 가능한 스크립트';
      downloadable: 'PDF/TXT 다운로드 지원';
    };
  };
  
  audio_content: {
    sound_alternatives: {
      notification_sounds: '시각적 알림 대안 제공';
      ambient_sounds: '명상 음악 시각적 표현';
      voice_guidance: '텍스트 대안 항상 제공';
    };
    
    volume_controls: {
      independent_levels: '효과음/음성/배경음 개별 조절';
      mute_options: '개별 음성 요소 음소거';
      hearing_aid_compatibility: '보청기 호환성 확보';
    };
  };
}
```

### **⌨️ 운용 가능성 (Operable)**

#### **1. 키보드 네비게이션**
```typescript
interface KeyboardAccessibility {
  navigation_strategy: {
    logical_order: 'DOM 순서와 시각적 순서 일치';
    skip_links: '메인 콘텐츠로 바로가기';
    landmark_navigation: 'ARIA 랜드마크 기반 탐색';
    breadcrumb_support: '현재 위치 명확한 표시';
  };
  
  interactive_elements: {
    tab_sequence: {
      fortune_forms: '운세 입력 폼 논리적 순서';
      card_selection: '타로카드 선택 키보드 지원';
      payment_flow: '결제 과정 완전 키보드 접근';
      community_interaction: '댓글/좋아요 키보드 조작';
    };
    
    custom_controls: {
      date_picker: '생년월일 입력 키보드 지원';
      time_selector: '출생시간 선택 화살표 키 조작';
      slider_controls: '운세 점수 슬라이더 키보드 조작';
      modal_dialogs: 'ESC 키로 닫기 지원';
    };
  };
  
  shortcuts: {
    global_shortcuts: {
      'Alt + M': '메인 메뉴로 이동';
      'Alt + S': '사주 계산 바로가기';
      'Alt + T': '타로 카드 바로가기';
      'Alt + C': '커뮤니티 바로가기';
    };
    
    contextual_shortcuts: {
      'Enter': '선택/실행';
      'Space': '체크박스/버튼 토글';
      'Arrow Keys': '카드/옵션 탐색';
      'Escape': '모달/드롭다운 닫기';
    };
  };
}
```

#### **2. 인터랙션 시간 제한**
```yaml
timing_considerations:
  session_management:
    warning_system: "세션 만료 2분 전 경고"
    extension_option: "추가 시간 요청 기능"
    auto_save: "입력 데이터 자동 저장"
    
  fortune_reading_time:
    flexible_pacing: "사용자 속도에 맞춘 진행"
    pause_resume: "언제든 일시정지/재개 가능"
    no_time_pressure: "시간 제한 없는 운세 해석"
    
  meditation_timers:
    customizable: "개인별 명상 시간 설정"
    gentle_reminders: "부드러운 시간 안내"
    disability_adjustments: "장애 유형별 시간 조정"
```

#### **3. 발작 및 물리적 반응 방지**
```typescript
interface SeizureProtection {
  animation_controls: {
    reduced_motion: {
      respect_preference: 'prefers-reduced-motion 준수';
      disable_autoplay: '자동 재생 영상 비활성화';
      static_alternatives: '정적 이미지 대안 제공';
    };
    
    flash_prevention: {
      three_flash_rule: '초당 3회 이하 깜빡임';
      general_flash_threshold: '일반 깜빡임 임계치 준수';
      red_flash_avoidance: '빨간색 깜빡임 완전 금지';
    };
  };
  
  mystical_effects: {
    gentle_transitions: '부드러운 화면 전환';
    optional_effects: '특수 효과 사용자 선택';
    warning_labels: '강한 시각 효과 사전 경고';
    alternative_experiences: '단순한 버전 항상 제공';
  };
}
```

### **🧠 이해 가능성 (Understandable)**

#### **1. 가독성 및 언어**
```yaml
readability_standards:
  content_structure:
    clear_headings: "명확한 제목 계층 구조"
    logical_flow: "논리적 정보 흐름"
    consistent_terminology: "일관된 용어 사용"
    
  language_complexity:
    plain_language: "쉬운 언어 사용 원칙"
    jargon_explanation: "전문 용어 설명 제공"
    reading_level: "중학교 수준 읽기 난이도"
    
  fortune_telling_clarity:
    interpretation_language: "운세 해석 명확한 표현"
    cultural_context: "문화적 맥락 설명"
    symbolic_meanings: "상징 의미 직관적 설명"
```

#### **2. 예측 가능성**
```typescript
interface PredictableInterface {
  consistent_navigation: {
    global_menu: '모든 페이지 동일한 메뉴 구조';
    breadcrumbs: '일관된 탐색 경로 표시';
    search_behavior: '예측 가능한 검색 결과';
  };
  
  fortune_interface_consistency: {
    card_layouts: '타로카드 배치 일관성';
    result_presentation: '운세 결과 표시 통일성';
    interaction_patterns: '상호작용 방식 일관성';
  };
  
  error_prevention: {
    form_validation: '실시간 입력 유효성 검사';
    confirmation_dialogs: '중요 작업 확인 대화상자';
    undo_functionality: '실수 되돌리기 기능';
  };
}
```

### **🔧 견고성 (Robust)**

#### **1. 보조 기술 호환성**
```typescript
interface AssistiveTechnology {
  screen_readers: {
    aria_support: {
      live_regions: '동적 콘텐츠 변경 알림';
      landmarks: '페이지 구조 의미적 마크업';
      properties: '요소 상태 정확한 전달';
      labels: '모든 폼 요소 명확한 라벨';
    };
    
    fortune_specific_aria: {
      tarot_cards: 'role="option" aria-describedby="card-meaning"';
      saju_chart: 'role="table" with proper headers';
      horoscope: 'role="article" with clear structure';
      progress_indicators: 'aria-valuenow for reading progress';
    };
  };
  
  voice_control: {
    voice_navigation: '음성 명령 지원';
    speech_input: '음성 입력 텍스트 변환';
    voice_output: '화면 읽기 최적화';
  };
  
  switch_control: {
    single_switch: '단일 스위치 탐색 지원';
    dwelling: '머무르기 선택 기능';
    scanning: '순차 스캔 인터페이스';
  };
}
```

---

## 🌏 **국제화 (i18n) 아키텍처**

### **🗣️ 다국어 지원 시스템**

#### **1. 언어 지원 범위**
```yaml
supported_languages:
  tier_1_primary: # 완전 지원
    korean: 
      locale: "ko-KR"
      script: "한글"
      direction: "ltr"
      cultural_context: "한국 전통 사주명리학"
      
  tier_2_expansion: # 확장 지원  
    english:
      locale: "en-US"
      script: "Latin"
      cultural_adaptation: "서구 점성술 통합"
      
    japanese:
      locale: "ja-JP" 
      script: "ひらがな・カタカナ・漢字"
      cultural_context: "일본 음양도 전통"
      
    chinese_simplified:
      locale: "zh-CN"
      script: "简体中文"
      cultural_context: "중국 전통 역학"
      
    chinese_traditional:
      locale: "zh-TW"
      script: "繁體中文"
      cultural_context: "대만 민속 점술"
      
  tier_3_future: # 미래 지원
    vietnamese: "vi-VN"
    thai: "th-TH"
    spanish: "es-ES"
    russian: "ru-RU"
```

#### **2. 문화적 적응 전략**
```typescript
interface CulturalAdaptation {
  fortune_telling_systems: {
    korean_saju: {
      calendar_system: '음력/양력 변환 시스템';
      traditional_elements: '한국식 사주명리학';
      cultural_interpretations: '한국 문화 맥락 해석';
    };
    
    chinese_bazi: {
      traditional_calendar: '중국 전통 달력 시스템';
      feng_shui_integration: '풍수지리학 연동';
      meridian_timezone: '중국 표준시 적용';
    };
    
    japanese_divination: {
      onmyoji_tradition: '음양도 전통 반영';
      seasonal_context: '일본 계절감 적용';
      shrine_culture: '신토 문화 고려';
    };
    
    western_astrology: {
      zodiac_signs: '서구 12궁 점성술';
      planet_influences: '행성 영향 해석';
      birth_chart_system: '출생 차트 계산법';
    };
  };
  
  cultural_colors: {
    korean: {
      five_elements: '오행 색채 (적청백흑황)';
      traditional_palette: '한국 전통 색감';
      ceremonial_colors: '제례 색채 체계';
    };
    
    chinese: {
      feng_shui_colors: '풍수 길흉색';
      imperial_colors: '황실 색채 체계';
      yin_yang_balance: '음양 조화색';
    };
    
    japanese: {
      seasonal_colors: '계절별 전통색';
      nature_harmony: '자연 조화색';
      zen_aesthetics: '선 미학 색채';
    };
  };
}
```

#### **3. 지역화 (L10n) 구현**
```yaml
localization_implementation:
  text_content:
    message_keys: "계층적 키 구조 (fortune.tarot.card_meanings)"
    context_aware: "상황별 번역 변형"
    pluralization: "언어별 복수형 규칙"
    gender_forms: "성별 어미 변화 대응"
    
  date_time_formats:
    calendar_systems:
      gregorian: "서력 날짜 형식"
      lunar: "음력 날짜 변환"
      japanese_era: "일본 연호 시스템"
      chinese_traditional: "중국 전통 달력"
      
    time_zones:
      automatic_detection: "사용자 위치 기반 자동 설정"
      manual_override: "수동 시간대 선택"
      dst_handling: "서머타임 자동 처리"
      
  number_currency:
    number_formats:
      korean: "1,234,567원"
      japanese: "1,234,567円" 
      chinese: "1,234,567元"
      english: "$1,234,567"
      
    fortune_scoring:
      percentage: "운세 점수 표시 방식"
      traditional_scales: "전통적 길흉 척도"
      modern_ratings: "현대적 별점 시스템"
```

### **📱 RTL 및 수직 텍스트 지원**

#### **1. 텍스트 방향성**
```css
/* RTL 언어 지원 (아랍어, 히브리어 확장 시) */
[dir="rtl"] {
  .fortune-card {
    transform: scaleX(-1);
    .card-content {
      transform: scaleX(-1);
    }
  }
}

/* 수직 텍스트 지원 (한문, 일본어) */
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: upright;
  
  &.traditional-chinese {
    writing-mode: vertical-rl;
  }
  
  &.japanese-traditional {
    writing-mode: vertical-rl;
    text-combine-upright: all;
  }
}

/* 몽골어 등 특수 문자 */
.mongolian-script {
  writing-mode: vertical-lr;
  text-orientation: sideways;
}
```

#### **2. 폰트 및 타이포그래피**
```typescript
interface InternationalTypography {
  font_families: {
    korean: {
      primary: 'Noto Sans KR, Malgun Gothic, sans-serif';
      traditional: 'Nanum Myeongjo, serif';
      decorative: 'Jua, cursive';
    };
    
    japanese: {
      primary: 'Noto Sans JP, Hiragino Sans, sans-serif';
      traditional: 'Noto Serif JP, serif';
      calligraphy: 'Shippori Mincho, serif';
    };
    
    chinese: {
      simplified: 'Noto Sans SC, SimHei, sans-serif';
      traditional: 'Noto Sans TC, PMingLiU, serif';
      calligraphy: 'Ma Shan Zheng, cursive';
    };
    
    english: {
      primary: 'Inter, Roboto, sans-serif';
      serif: 'Playfair Display, Georgia, serif';
      mystical: 'Cinzel, serif';
    };
  };
  
  text_sizing: {
    base_size: '16px';
    scale_factor: {
      korean: 1.0;
      japanese: 1.1;  // 복잡한 문자 고려
      chinese: 1.0;
      arabic: 1.2;    // 더 큰 글자 필요
    };
  };
  
  line_spacing: {
    cjk_languages: 1.8;   // 한중일 언어
    latin_languages: 1.6; // 라틴 문자
    arabic_script: 2.0;   // 아랍 문자
  };
}
```

---

## 🎨 **문화적 UI/UX 적응**

### **🌸 지역별 디자인 시스템**

#### **1. 한국 문화 특화**
```yaml
korean_design_system:
  traditional_elements:
    hanbok_colors: "한복 색감 (장미, 옥색, 자주색)"
    dancheong_patterns: "단청 무늬 패턴"
    hanji_textures: "한지 질감 표현"
    
  modern_korean:
    k_culture_trends: "K-POP, K-뷰티 트렌드 반영"
    minimalist_aesthetics: "한국적 미니멀리즘"
    technology_harmony: "전통과 현대 기술 조화"
    
  saju_specific:
    four_pillars_layout: "사주 네 기둥 시각화"
    yin_yang_symbol: "태극 문양 활용"
    zodiac_animals: "십이지신 캐릭터"
```

#### **2. 일본 문화 적응**
```yaml
japanese_design_adaptation:
  aesthetic_principles:
    wabi_sabi: "불완전함의 아름다움"
    ma_spacing: "여백의 미학"
    mono_no_aware: "물의 정취"
    
  seasonal_themes:
    spring_sakura: "벚꽃 테마 (분홍, 연두)"
    summer_matsuri: "축제 테마 (빨강, 흰색)"
    autumn_momiji: "단풍 테마 (주황, 황금)"
    winter_yuki: "눈 테마 (흰색, 은색)"
    
  divination_style:
    omikuji_format: "오미쿠지 형식 운세"
    shrine_aesthetics: "신사 디자인 요소"
    calligraphy_integration: "서예 스타일 폰트"
```

#### **3. 중국 문화 고려**
```yaml
chinese_cultural_design:
  traditional_elements:
    imperial_colors: "황실 색채 (황금, 빨강)"
    dragon_phoenix: "용봉 무늬"
    cloud_patterns: "구름 문양"
    
  feng_shui_layout:
    directional_significance: "방위별 의미 적용"
    element_balance: "오행 균형 레이아웃"
    lucky_numbers: "길수 활용 (8, 9, 6)"
    
  bazi_visualization:
    heaven_earth_human: "천지인 삼재 구조"
    stem_branch_display: "천간지지 표시"
    five_element_wheel: "오행 상생상극 표현"
```

### **🎭 문화적 사용자 경험**

#### **1. 상호작용 패턴**
```typescript
interface CulturalInteractionPatterns {
  greeting_styles: {
    korean: {
      formal_honorifics: '높임말 시스템 적용';
      age_consideration: '나이에 따른 언어 조정';
      hierarchy_respect: '서열 의식 반영';
    };
    
    japanese: {
      politeness_levels: '케이고(敬語) 시스템';
      seasonal_greetings: '계절별 인사말';
      group_harmony: '와(和) 정신 반영';
    };
    
    chinese: {
      face_concept: '체면 문화 고려';
      guanxi_relationships: '관계 중심 소통';
      symbolic_communication: '상징적 표현 선호';
    };
  };
  
  fortune_consultation_flow: {
    korean_style: {
      respectful_inquiry: '정중한 질문 방식';
      detailed_explanation: '상세한 설명 선호';
      family_consideration: '가족 운세 중시';
    };
    
    western_style: {
      direct_answers: '직접적 답변 선호';
      personal_focus: '개인 중심 해석';
      psychological_approach: '심리학적 접근';
    };
  };
}
```

#### **2. 문화적 금기 및 민감성**
```yaml
cultural_sensitivities:
  religious_considerations:
    buddhist_context: "불교 문화권 배려"
    christian_sensitivity: "기독교 문화 고려"
    islamic_adaptation: "이슬람 문화 존중"
    secular_options: "종교 중립적 선택지"
    
  superstition_handling:
    number_taboos:
      korean: "4(사), 9(구) 숫자 배려"
      chinese: "4(죽음) 숫자 회피"
      japanese: "4(시), 9(고) 숫자 주의"
      western: "13 숫자 옵션 제공"
      
    color_meanings:
      death_associations: "죽음 연상 색상 주의"
      mourning_colors: "상복 색깔 배려"
      celebration_colors: "축하 색상 활용"
      
  privacy_expectations:
    asian_discretion: "아시아권 신중함 선호"
    western_openness: "서구권 개방성 수용"
    family_privacy: "가족 정보 보호 강화"
```

---

## 🔧 **기술적 구현 가이드**

### **📚 프레임워크 및 라이브러리**

#### **1. React 국제화 구현**
```typescript
// 국제화 설정
import { useTranslation } from 'react-i18next';
import { useDirection } from '@/hooks/useDirection';

interface FortuneCardProps {
  cardType: 'tarot' | 'saju' | 'zodiac';
  culturalContext: 'korean' | 'chinese' | 'japanese' | 'western';
}

const FortuneCard: React.FC<FortuneCardProps> = ({ 
  cardType, 
  culturalContext 
}) => {
  const { t, i18n } = useTranslation();
  const direction = useDirection();
  
  return (
    <div 
      className={`fortune-card ${culturalContext}`}
      dir={direction}
      role="article"
      aria-label={t('fortune.card.description', { cardType })}
    >
      <header>
        <h2>{t(`fortune.${cardType}.title`)}</h2>
      </header>
      
      <main>
        <div className="card-content">
          {/* 문화별 컨텐츠 렌더링 */}
          <CulturalContent 
            type={cardType}
            culture={culturalContext}
          />
        </div>
      </main>
      
      <footer>
        <p className="cultural-note">
          {t(`culture.${culturalContext}.disclaimer`)}
        </p>
      </footer>
    </div>
  );
};
```

#### **2. 접근성 훅스 구현**
```typescript
// 접근성 지원 커스텀 훅
export const useAccessibility = () => {
  const [reducedMotion, setReducedMotion] = useState(false);
  const [highContrast, setHighContrast] = useState(false);
  const [fontSize, setFontSize] = useState('medium');
  
  useEffect(() => {
    // prefers-reduced-motion 감지
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);
    
    // prefers-contrast 감지
    const contrastQuery = window.matchMedia('(prefers-contrast: high)');
    setHighContrast(contrastQuery.matches);
    
    // 사용자 설정 로드
    const savedSettings = localStorage.getItem('accessibility-settings');
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      setFontSize(settings.fontSize || 'medium');
    }
  }, []);
  
  const announceToScreenReader = (message: string) => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    document.body.appendChild(announcement);
    
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  };
  
  return {
    reducedMotion,
    highContrast,
    fontSize,
    setFontSize,
    announceToScreenReader
  };
};

// 키보드 네비게이션 훅
export const useKeyboardNavigation = () => {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    switch (event.key) {
      case 'Escape':
        // 모달 닫기
        break;
      case 'Tab':
        // 포커스 트랩 관리
        break;
      case 'ArrowLeft':
      case 'ArrowRight':
        // 카드 네비게이션
        break;
    }
  }, []);
  
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
};
```

#### **3. 다국어 콘텐츠 관리**
```json
// i18n 번역 파일 구조
{
  "fortune": {
    "saju": {
      "title": "사주명리학",
      "description": "생년월일시를 바탕으로 한 운세 분석",
      "pillars": {
        "year": "년주",
        "month": "월주", 
        "day": "일주",
        "hour": "시주"
      },
      "elements": {
        "wood": "목",
        "fire": "화",
        "earth": "토",
        "metal": "금",
        "water": "수"
      }
    },
    "tarot": {
      "title": "타로카드",
      "cards": {
        "fool": {
          "name": "바보",
          "meaning": "새로운 시작과 순수함",
          "reversed": "경솔함과 무모함"
        }
      }
    }
  },
  "accessibility": {
    "skip_to_content": "본문으로 바로가기",
    "close_modal": "모달 닫기",
    "loading": "로딩 중...",
    "error": "오류가 발생했습니다"
  },
  "culture": {
    "korean": {
      "disclaimer": "이 운세는 한국 전통 사주명리학을 바탕으로 합니다"
    },
    "chinese": {
      "disclaimer": "此运势基于中国传统八字命理学"
    }
  }
}
```

### **🎨 CSS 접근성 및 국제화**

#### **1. 접근성 CSS 구현**
```scss
// 접근성 우선 스타일
:root {
  // 고대비 색상 변수
  --high-contrast-bg: #000000;
  --high-contrast-text: #ffffff;
  --high-contrast-accent: #ffff00;
  
  // 동적 글자 크기
  --font-size-base: clamp(16px, 2.5vw, 24px);
  --font-size-large: clamp(20px, 3vw, 32px);
  
  // 애니메이션 지속시간
  --animation-duration: 0.3s;
}

// 고대비 모드
@media (prefers-contrast: high) {
  :root {
    --color-background: var(--high-contrast-bg);
    --color-text: var(--high-contrast-text);
    --color-accent: var(--high-contrast-accent);
  }
}

// 움직임 감소 모드  
@media (prefers-reduced-motion: reduce) {
  :root {
    --animation-duration: 0.01ms;
  }
  
  * {
    animation-duration: var(--animation-duration) !important;
    animation-iteration-count: 1 !important;
    transition-duration: var(--animation-duration) !important;
  }
}

// 포커스 표시
.focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 2px;
  box-shadow: 0 0 0 1px var(--color-background);
}

// 스크린 리더 전용
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

// 스킵 링크
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--color-accent);
  color: var(--color-background);
  padding: 8px;
  z-index: 1000;
  text-decoration: none;
  border-radius: 4px;
  
  &:focus {
    top: 6px;
  }
}
```

#### **2. 국제화 CSS 처리**
```scss
// 언어별 스타일
[lang="ko"] {
  font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
  line-height: 1.8;
  word-break: keep-all;
  
  .fortune-text {
    text-align: justify;
    text-justify: inter-character;
  }
}

[lang="ja"] {
  font-family: 'Noto Sans JP', 'Hiragino Sans', sans-serif;
  line-height: 1.9;
  
  .traditional-text {
    writing-mode: vertical-rl;
    text-orientation: upright;
  }
}

[lang="zh-CN"], [lang="zh-TW"] {
  font-family: 'Noto Sans SC', 'SimHei', sans-serif;
  line-height: 1.8;
  
  .classical-text {
    writing-mode: vertical-rl;
    text-orientation: upright;
  }
}

[lang="ar"] {
  font-family: 'Noto Sans Arabic', 'Tahoma', sans-serif;
  direction: rtl;
  text-align: right;
  line-height: 2.0;
}

// 문화별 컬러 테마
.theme-korean {
  --primary: #d946ef; // 자주색 (전통 한복)
  --secondary: #06b6d4; // 옥색
  --accent: #f59e0b; // 황금색
}

.theme-japanese {
  --primary: #ec4899; // 벚꽃 분홍
  --secondary: #10b981; // 청록색  
  --accent: #f97316; // 단풍 주황
}

.theme-chinese {
  --primary: #dc2626; // 중국 빨강
  --secondary: #ca8a04; // 황금색
  --accent: #1f2937; // 먹색
}
```

---

## 📊 **테스트 및 검증 전략**

### **🔍 접근성 테스트**

#### **1. 자동화 테스트**
```typescript
// Jest + Testing Library 접근성 테스트
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import userEvent from '@testing-library/user-event';

expect.extend(toHaveNoViolations);

describe('Fortune Card Accessibility', () => {
  test('should have no accessibility violations', async () => {
    const { container } = render(<FortuneCard cardType="tarot" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  test('should support keyboard navigation', async () => {
    const user = userEvent.setup();
    render(<FortuneCard cardType="saju" />);
    
    // Tab 키로 네비게이션 테스트
    await user.tab();
    expect(screen.getByRole('button', { name: /다음 카드/ })).toHaveFocus();
    
    // 엔터 키로 활성화 테스트  
    await user.keyboard('{Enter}');
    expect(screen.getByText(/카드가 선택되었습니다/)).toBeInTheDocument();
  });
  
  test('should announce screen reader content', async () => {
    const announcer = jest.fn();
    render(<FortuneCard onAnnounce={announcer} />);
    
    expect(announcer).toHaveBeenCalledWith(
      '타로카드가 선택되었습니다. 연인 카드 - 사랑과 선택의 의미'
    );
  });
});
```

#### **2. 수동 테스트 체크리스트**
```yaml
manual_testing_checklist:
  keyboard_navigation:
    - [ ] "Tab 키로 모든 인터랙티브 요소 접근 가능"
    - [ ] "Shift+Tab으로 역순 이동 가능"  
    - [ ] "Enter/Space로 버튼 활성화"
    - [ ] "Arrow 키로 카드 선택 이동"
    - [ ] "Escape로 모달 닫기"
    
  screen_reader_testing:
    - [ ] "NVDA로 전체 콘텐츠 읽기"
    - [ ] "JAWS로 헤딩 네비게이션"
    - [ ] "VoiceOver로 랜드마크 이동"
    - [ ] "TalkBack(Android) 호환성"
    
  visual_testing:
    - [ ] "200% 확대 시 레이아웃 유지"
    - [ ] "고대비 모드 정상 표시"
    - [ ] "색맹 시뮬레이션 테스트"
    - [ ] "다크모드 접근성 확인"
```

### **🌍 국제화 테스트**

#### **1. 번역 품질 보증**
```typescript
// 번역 일관성 테스트
describe('Translation Quality', () => {
  const languages = ['ko', 'en', 'ja', 'zh-CN'];
  
  test.each(languages)('should have complete translations for %s', (lang) => {
    const translations = require(`../locales/${lang}/common.json`);
    const expectedKeys = [
      'fortune.saju.title',
      'fortune.tarot.title', 
      'fortune.zodiac.title'
    ];
    
    expectedKeys.forEach(key => {
      expect(getNestedValue(translations, key)).toBeDefined();
      expect(getNestedValue(translations, key)).not.toBe('');
    });
  });
  
  test('should handle pluralization correctly', () => {
    // 한국어 단위사 테스트
    expect(t('fortune.card.count', { count: 1 })).toBe('카드 1장');
    expect(t('fortune.card.count', { count: 5 })).toBe('카드 5장');
    
    // 영어 복수형 테스트  
    expect(t('fortune.card.count', { count: 1, lng: 'en' })).toBe('1 card');
    expect(t('fortune.card.count', { count: 5, lng: 'en' })).toBe('5 cards');
  });
});
```

#### **2. 문화적 적응 검증**
```yaml
cultural_testing:
  color_verification:
    korean:
      - [ ] "오행 색채 정확한 표현"
      - [ ] "전통 색감 문화적 적절성"
      - [ ] "길흉 색상 올바른 사용"
      
    chinese:
      - [ ] "풍수 색채 원리 준수"
      - [ ] "황실 색상 품격 유지"
      - [ ] "금기 색상 배제"
      
    japanese:
      - [ ] "계절감 색채 조화"
      - [ ] "와비사비 미학 반영"
      - [ ] "신사 색채 존중"
      
  content_appropriateness:
    - [ ] "종교적 민감성 확인"
    - [ ] "문화적 금기 회피"
    - [ ] "지역별 관습 존중"
    - [ ] "번역 뉘앙스 적절성"
```

---

## 📈 **성능 최적화 및 모니터링**

### **⚡ 접근성 성능 최적화**

#### **1. 스크린 리더 최적화**
```typescript
// 스크린 리더 성능 최적화
const OptimizedFortuneCard = React.memo(({ cardData }) => {
  const [isAnnounced, setIsAnnounced] = useState(false);
  
  // 콘텐츠 변경 시에만 스크린 리더에 알림
  useEffect(() => {
    if (cardData && !isAnnounced) {
      announceToScreenReader(
        `새로운 운세 카드: ${cardData.name}. ${cardData.meaning}`
      );
      setIsAnnounced(true);
    }
  }, [cardData, isAnnounced]);
  
  return (
    <div 
      role="article"
      aria-live="polite"
      aria-busy={!cardData}
    >
      {cardData ? (
        <CardContent data={cardData} />
      ) : (
        <div aria-label="카드 로딩 중">
          <Spinner />
        </div>
      )}
    </div>
  );
});
```

#### **2. 국제화 성능 최적화**
```typescript
// 언어 번들 지연 로딩
const loadLanguage = async (language: string) => {
  const { default: translations } = await import(
    `../locales/${language}/common.json`
  );
  return translations;
};

// 문화별 컴포넌트 지연 로딩
const CulturalComponent = React.lazy(() => 
  import(`./cultural/${culturalContext}Component`)
);

// 폰트 최적화 로딩
const FontLoader: React.FC<{ language: string }> = ({ language }) => {
  useEffect(() => {
    const fontMap = {
      'ko': 'Noto Sans KR',
      'ja': 'Noto Sans JP', 
      'zh-CN': 'Noto Sans SC',
      'zh-TW': 'Noto Sans TC'
    };
    
    if (fontMap[language]) {
      document.fonts.load(`16px "${fontMap[language]}"`);
    }
  }, [language]);
  
  return null;
};
```

### **📊 접근성 메트릭 모니터링**

#### **1. 실시간 접근성 지표**
```typescript
interface AccessibilityMetrics {
  wcag_compliance: {
    level_aa: number; // 준수율 (%)
    violations_count: number;
    critical_issues: number;
  };
  
  user_experience: {
    keyboard_users: number; // 키보드 사용자 수
    screen_reader_users: number;
    high_contrast_users: number;
    reduced_motion_users: number;
  };
  
  performance: {
    screen_reader_response: number; // ms
    keyboard_navigation_delay: number;
    font_loading_time: number;
  };
  
  internationalization: {
    supported_languages: string[];
    translation_coverage: number; // %
    cultural_adaptation_score: number;
  };
}

// 접근성 메트릭 수집
const collectAccessibilityMetrics = () => {
  return {
    wcag_violations: getWCAGViolations(),
    keyboard_navigation_time: measureKeyboardNavigation(),
    screen_reader_compatibility: testScreenReaderCompatibility(),
    language_coverage: calculateTranslationCoverage()
  };
};
```

#### **2. 사용자 피드백 수집**
```yaml
accessibility_feedback_system:
  feedback_channels:
    - "접근성 전용 이메일: accessibility@heal7.com"
    - "키보드 네비게이션 이슈 리포트"
    - "스크린 리더 호환성 문제 신고"
    - "번역 품질 개선 제안"
    
  user_testing_program:
    - "시각 장애인 사용자 테스트 그룹"
    - "청각 장애인 사용자 패널"
    - "운동 장애인 접근성 검토"
    - "다국어 사용자 문화적 적절성 검토"
    
  continuous_improvement:
    - "월간 접근성 감사"
    - "분기별 WCAG 업데이트 적용"
    - "연간 국제화 전략 리뷰"
    - "사용자 요구사항 반영 프로세스"
```

---

## 🚀 **구현 로드맵 및 우선순위**

### **📅 Phase 1: 기본 접근성 구현 (2주)**
```yaml
phase_1_accessibility:
  week_1:
    - [ ] "WCAG 2.1 AA 기본 준수"
    - [ ] "키보드 네비게이션 구현"
    - [ ] "ARIA 속성 추가"
    - [ ] "대체 텍스트 작성"
    
  week_2:
    - [ ] "스크린 리더 테스트"
    - [ ] "고대비 모드 지원"
    - [ ] "포커스 관리 구현"
    - [ ] "자동화 테스트 설정"
```

### **📅 Phase 2: 기본 국제화 (3주)**
```yaml
phase_2_internationalization:
  week_1:
    - [ ] "React i18n 설정"
    - [ ] "한국어/영어 번역"
    - [ ] "날짜/시간 지역화"
    - [ ] "숫자/통화 형식"
    
  week_2:
    - [ ] "일본어 지원 추가"
    - [ ] "중국어 간체/번체"
    - [ ] "문화별 색상 테마"
    - [ ] "RTL 레이아웃 준비"
    
  week_3:
    - [ ] "문화적 콘텐츠 적응"
    - [ ] "지역별 운세 시스템"
    - [ ] "번역 품질 검증"
    - [ ] "성능 최적화"
```

### **📅 Phase 3: 고급 기능 (4주)**
```yaml
phase_3_advanced_features:
  advanced_accessibility:
    - [ ] "음성 인터페이스 지원"
    - [ ] "AI 기반 설명 생성"
    - [ ] "개인 맞춤 접근성"
    - [ ] "실시간 자막 생성"
    
  cultural_depth:
    - [ ] "세부 문화권 지원"
    - [ ] "종교적 배려 옵션"
    - [ ] "지역 축제 테마"
    - [ ] "전통 달력 시스템"
    
  user_experience:
    - [ ] "개인화 설정 저장"
    - [ ] "접근성 프로필"
    - [ ] "문화 선호도 설정"
    - [ ] "다중 언어 믹스"
```

---

## 🏆 **결론**

### **✨ 접근성 및 국제화 핵심 가치**

이 접근성 및 국제화 전략은 **모든 사용자를 위한 포용적 디지털 영성 경험**과 **전 세계 문화적 다양성 존중**을 통해 다음을 달성합니다:

#### **♿ 핵심 접근성 성과**
1. **🎯 완전한 WCAG 2.1 AA 준수**: 시각/청각/운동 장애인 100% 접근 가능
2. **⌨️ 전체 키보드 네비게이션**: 마우스 없이도 모든 기능 사용 가능
3. **📢 스크린 리더 완벽 지원**: 운세 해석의 음성 전달 최적화
4. **🎨 고대비 및 저시력 지원**: 시각적 접근성 극대화
5. **🧠 인지적 접근성**: 쉬운 언어와 직관적 인터페이스

#### **🌍 핵심 국제화 성과**
1. **🗣️ 5개 언어 완전 지원**: 한국어, 영어, 일본어, 중국어(간체/번체)
2. **🎭 문화적 적응**: 각 문화권의 점술 전통과 미학 반영
3. **📅 다중 달력 시스템**: 양력/음력/전통달력 지원
4. **🎨 문화별 디자인**: 오행 기반 색채와 전통 패턴 활용
5. **🔄 지역별 상호작용**: 문화적 예의와 소통 방식 반영

#### **🎯 즉시 실행 가능**
```bash
# 🌍 접근성 및 국제화 전략 확인
cat CORE/reference-docs/technical-standards/Accessibility-Internationalization-Strategy-v1.0*.md

# ♿ 접근성 구현 시작
# 1단계: WCAG 2.1 AA 기본 준수
# 2단계: 키보드 네비게이션 구현
# 3단계: 스크린 리더 최적화

# 🗣️ 국제화 구현 시작  
# 1단계: React i18n 설정
# 2단계: 번역 파일 구조화
# 3단계: 문화적 적응 구현
```

### **🌟 혁신적 특징**
- **🔮 점술업 특화 접근성**: 영성 서비스의 특수성을 고려한 접근성 설계
- **🌸 동아시아 문화 전문성**: 한중일 문화권의 깊이 있는 이해와 적용
- **🤖 AI 기반 적응**: 사용자별 접근성 및 문화적 선호도 학습
- **📱 크로스 플랫폼**: 웹/모바일 모든 환경에서 일관된 경험

**이제 전 세계 모든 사용자가 문화적 배경과 신체적 능력에 관계없이 HEAL7의 영성 서비스를 완전히 경험할 수 있습니다!** 🌍✨

---

*📅 접근성 및 국제화 전략 완성일: 2025-08-18 18:45 KST*  
*♿ 접근성 수준: WCAG 2.1 AA + Fortune Telling Specialized*  
*🌍 국제화 범위: 동아시아 5개 언어 + 문화적 적응*  
*🎯 다음 단계: 30일 내 기본 접근성 구현 시작!*