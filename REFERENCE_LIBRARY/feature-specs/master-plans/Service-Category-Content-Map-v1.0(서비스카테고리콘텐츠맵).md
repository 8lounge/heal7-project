# 🗺️ HEAL7 서비스 카테고리 & 콘텐츠 맵 v1.0

> **프로젝트**: HEAL7 서비스 구조 설계 및 콘텐츠 전략  
> **버전**: v1.0.0  
> **작성일**: 2025-08-23  
> **핵심 목표**: 17개 서비스를 체계적으로 분류하여 최적의 사용자 여정 구현  
> **전략**: 포스텔러 6,000+ 콘텐츠 대비 HEAL7 10,000+ 콘텐츠 목표

## 🌟 **서비스 전체 맵 개요**

### **📊 서비스 분류 체계**

```yaml
Service_Classification:
  total_services: 17개
  
  core_fortune_services: 7개  # 핵심 운세 서비스
    - 종합운세
    - 연애운 
    - 취업운
    - 성격분석
    - 금전운
    - 사업운
    - 사상체질분석
    
  entertainment_content: 10개  # 재미 & 힐링 콘텐츠
    - 타로
    - 별자리
    - 12지신
    - 바이오리듬
    - 오늘의운세
    - 힐링매거진
    - 1:1상담
    - 공지사항
    - 힐링스토어
    - 고민상담
    
  user_journey_stages:
    discovery: "오늘의운세, 별자리, 바이오리듬"  # 가벼운 시작
    exploration: "종합운세, 성격분석, 타로"      # 본격적 탐색
    engagement: "전문 운세, 1:1상담, 힐링매거진" # 깊은 참여
    loyalty: "정기구독, 힐링스토어, 커뮤니티"    # 충성 고객
```

---

## 🔮 **핵심 운세 서비스 (7개)**

### **1️⃣ 종합운세 (메인 서비스)**

```yaml
종합운세:
  service_id: "comprehensive_fortune"
  priority: "최우선 (메인 랜딩)"
  target_users: "모든 연령층"
  
  sub_services:
    기본사주: 
      content: "사주팔자 기본 분석"
      depth: "초급자용 해석"
      duration: "3-5분"
      
    심층사주:
      content: "상세 사주팔자 + AI 해석"
      depth: "전문가급 분석"
      duration: "10-15분"
      
    연간운세:
      content: "1년간 월별 상세 운세"
      depth: "장기 계획 수립용"
      duration: "15-20분"
  
  visualization:
    basic: "2D 사주판 + 오행 차트"
    premium: "3D 홀로그램 사주판 + 파티클 효과"
    
  ai_features:
    models: "GPT-4 + Claude + Gemini (3개 AI 융합)"
    personalization: "과거 이용 패턴 반영"
    language_style: "사용자 선호도 기반 말투"
    
  pricing:
    basic: "무료 (월 3회)"
    premium: "구독 서비스 (무제한)"
```

### **2️⃣ 연애운 (로맨스)**

```yaml
연애운:
  service_id: "love_fortune"
  target_users: "20-40대 (특히 여성 70%)"
  emotional_keywords: ["설렘", "로맨스", "소울메이트", "운명"]
  
  content_types:
    solo_fortune:
      title: "솔로를 위한 연애운"
      features: ["만남 시기", "이상형 분석", "매력 포인트"]
      
    couple_fortune:
      title: "커플을 위한 궁합"
      features: ["궁합 점수", "갈등 해결", "미래 전망"]
      
    marriage_fortune:
      title: "결혼운 & 배우자운"
      features: ["결혼 시기", "배우자 특징", "결혼 후 생활"]
  
  special_features:
    compatibility_3d: "3D 궁합 시각화"
    love_timeline: "연애 타임라인 예측"
    couple_dashboard: "커플 전용 대시보드"
    
  cross_services:
    - "타로 연애 카드"
    - "별자리별 연애 스타일"
    - "1:1 연애 상담"
```

### **3️⃣ 취업운 (커리어)**

```yaml
취업운:
  service_id: "career_fortune"
  target_users: "20-35대 직장인, 구직자"
  emotional_keywords: ["성공", "성취", "인정", "안정"]
  
  content_categories:
    job_seeking:
      title: "구직자를 위한 취업운"
      features: ["합격 시기", "유리한 업종", "면접 팁"]
      
    career_development:
      title: "직장인 승진운"
      features: ["승진 시기", "상사 관계", "업무 운"]
      
    career_change:
      title: "이직 & 전직운"
      features: ["이직 타이밍", "새로운 분야", "연봉 전망"]
      
    entrepreneur:
      title: "창업 & 사업 시작"
      features: ["창업 시기", "사업 아이템", "파트너십"]
  
  data_integration:
    job_market: "실시간 채용 정보 연동"
    industry_trends: "산업 동향 분석"
    skill_matching: "개인 역량 vs 시장 수요"
    
  ai_coaching:
    resume_tips: "AI 이력서 피드백"
    interview_prep: "맞춤형 면접 준비"
    career_roadmap: "개인별 커리어 로드맵"
```

### **4️⃣ 성격분석 (자기이해)**

```yaml
성격분석:
  service_id: "personality_analysis"
  target_users: "전 연령층 (자기계발 관심자)"
  emotional_keywords: ["이해", "깨달음", "성장", "발견"]
  
  analysis_frameworks:
    traditional_saju:
      method: "사주 기반 성격 분석"
      aspects: ["기본 성향", "대인관계", "의사결정 스타일"]
      
    modern_psychology:
      method: "심리학 이론 융합"
      frameworks: ["MBTI", "빅파이브", "애니어그램"]
      
    ai_deep_analysis:
      method: "AI 행동 패턴 분석"
      data: ["사용 패턴", "선택 이력", "관심사"]
  
  visualization_types:
    personality_wheel: "3D 성격 다이어그램"
    strength_radar: "강점 레이더 차트"
    growth_path: "성장 경로 시각화"
    
  practical_applications:
    relationship_tips: "대인관계 개선 조언"
    career_guidance: "성격 기반 진로 가이드"
    self_development: "개인 성장 계획"
    conflict_resolution: "갈등 해결 전략"
```

### **5️⃣ 금전운 (재물운)**

```yaml
금전운:
  service_id: "money_fortune"
  target_users: "30-60대 (재정 관심층)"
  emotional_keywords: ["풍요", "안정", "투자", "성공"]
  
  fortune_categories:
    wealth_accumulation:
      title: "재물 축적운"
      focus: ["저축 능력", "투자 적성", "부의 축적 시기"]
      
    investment_fortune:
      title: "투자운 & 재테크"
      focus: ["투자 타이밍", "유리한 투자처", "위험 관리"]
      
    business_profit:
      title: "사업 수익운"
      focus: ["매출 증대", "수익성 개선", "자금 흐름"]
      
    lottery_luck:
      title: "횡재운 & 로또운"
      focus: ["의외의 수익", "보너스", "행운의 숫자"]
  
  market_integration:
    stock_correlation: "주식 시장 운세 연동"
    crypto_timing: "암호화폐 투자 타이밍"
    real_estate: "부동산 매매 시기"
    
  risk_management:
    warning_system: "위험 신호 조기 경고"
    diversification: "분산 투자 조언"
    emergency_fund: "비상금 관리 가이드"
```

### **6️⃣ 사업운 (창업/경영)**

```yaml
사업운:
  service_id: "business_fortune"
  target_users: "창업가, 사업자, 경영진"
  emotional_keywords: ["성공", "확장", "리더십", "혁신"]
  
  business_stages:
    startup_phase:
      title: "창업 초기 운세"
      focus: ["사업 아이템", "시장 진입", "초기 자금"]
      
    growth_phase:
      title: "사업 확장기 운세"
      focus: ["매출 증대", "직원 채용", "마케팅"]
      
    maturity_phase:
      title: "안정기 경영운"
      focus: ["지속 가능성", "경쟁 우위", "다각화"]
      
    crisis_management:
      title: "위기 관리 운세"
      focus: ["리스크 대응", "구조조정", "회생 전략"]
  
  business_types:
    retail: "소매업/서비스업"
    manufacturing: "제조업/생산업"
    tech_startup: "기술 스타트업"
    franchise: "프랜차이즈"
    online_business: "온라인 비즈니스"
    
  leadership_analysis:
    management_style: "경영진 리더십 스타일"
    team_harmony: "팀워크 및 조직 화합"
    decision_timing: "중요 결정 최적 타이밍"
    partnership: "사업 파트너십 궁합"
```

### **7️⃣ 사상체질분석 (건강운)**

```yaml
사상체질분석:
  service_id: "constitution_analysis"
  target_users: "30대+ (건강 관심층)"
  emotional_keywords: ["건강", "균형", "조화", "치유"]
  
  constitution_types:
    taeumin: 
      characteristics: "태음인 - 침착하고 인내심 강함"
      health_focus: ["비만 관리", "순환계", "소화기계"]
      
    soeumin:
      characteristics: "소음인 - 섬세하고 신중함"
      health_focus: ["소화기능", "체력 증진", "면역력"]
      
    taeyangin:
      characteristics: "태양인 - 적극적이고 활동적"
      health_focus: ["간 기능", "열 조절", "스트레스"]
      
    soyangin:
      characteristics: "소양인 - 빠르고 민첩함"
      health_focus: ["신장", "순환기", "감정 조절"]
  
  health_recommendations:
    diet_guidance: "체질별 맞춤 식단"
    exercise_plan: "개인별 운동 처방"
    lifestyle: "생활 습관 개선"
    seasonal_care: "계절별 건강 관리"
    
  integration_services:
    health_fortune: "건강운 + 체질 분석"
    diet_planning: "사주 기반 다이어트"
    wellness_coaching: "개인별 웰니스 플랜"
```

---

## 🎪 **재미 & 힐링 콘텐츠 (10개)**

### **8️⃣ 타로 (Tarot Reading)**

```yaml
타로:
  service_id: "tarot_reading"
  target_users: "20-40대 (특히 여성 80%)"
  emotional_keywords: ["직감", "신비", "안내", "깨달음"]
  
  reading_types:
    daily_card: 
      title: "오늘의 타로 카드"
      method: "1장 뽑기"
      duration: "1-2분"
      
    love_spread:
      title: "연애 타로 (3장 스프레드)"
      method: "과거-현재-미래"
      duration: "5-7분"
      
    decision_making:
      title: "선택의 기로 (5장 스프레드)"
      method: "상황분석 + 결과 예측"
      duration: "10-12분"
      
    celtic_cross:
      title: "전체 운세 (켈틱 크로스)"
      method: "10장 완전 해석"
      duration: "15-20분"
  
  interactive_features:
    3d_card_selection: "3D 카드덱에서 직접 선택"
    animated_reveal: "카드 뒤집기 애니메이션"
    personal_deck: "개인 맞춤 카드덱"
    history_tracking: "과거 뽑은 카드 이력"
    
  ai_interpretation:
    context_aware: "개인 상황 맞춤 해석"
    multiple_perspectives: "다각도 메시지 제공"
    actionable_advice: "실행 가능한 조언"
```

### **9️⃣ 별자리 (Astrology)**

```yaml
별자리:
  service_id: "astrology"
  target_users: "10-40대 (별자리 관심층)"
  emotional_keywords: ["우주", "별빛", "운명", "성향"]
  
  astrology_services:
    daily_horoscope:
      title: "오늘의 별자리운세"
      content: "12성좌별 일일 운세"
      update: "매일 새벽 4시"
      
    monthly_forecast:
      title: "이달의 별자리 운세"
      content: "월간 상세 예측"
      themes: ["연애", "직업", "건강", "인간관계"]
      
    compatibility:
      title: "별자리 궁합"
      pairs: "연인, 친구, 직장동료 궁합"
      analysis: "성격 충돌 & 조화 포인트"
      
    birth_chart:
      title: "개인 성격 분석"
      method: "출생 시간 기반 정밀 분석"
      depth: "태양/달/상승 성좌 종합"
  
  visual_elements:
    constellation_map: "3D 별자리 지도"
    planet_position: "행성 위치 실시간 반영"
    cosmic_animation: "우주 공간 애니메이션"
    
  scientific_integration:
    astronomy_data: "실제 천문학 데이터 반영"
    planet_transit: "행성 이동 주기 연동"
    eclipse_events: "일식/월식 특별 이벤트"
```

### **🔟 12지신 (띠별 운세)**

```yaml
띠별운세:
  service_id: "zodiac_animals"
  target_users: "전 연령층 (전통 문화 친숙층)"
  emotional_keywords: ["전통", "조상", "지혜", "특성"]
  
  zodiac_animals:
    동물별_특성:
      - "쥐띠: 영리하고 적응력 강함"
      - "소띠: 성실하고 끈기 있음" 
      - "호랑이띠: 용맹하고 리더십"
      - "토끼띠: 온순하고 평화주의"
      - "용띠: 역동적이고 카리스마"
      - "뱀띠: 지혜롭고 직관적"
      - "말띠: 자유롭고 활동적"
      - "양띠: 친절하고 예술적"
      - "원숭이띠: 재치있고 창의적"
      - "닭띠: 정확하고 계획적"
      - "개띠: 충실하고 정직함"
      - "돼지띠: 관대하고 성실함"
  
  content_types:
    yearly_fortune: "연간 띠별 종합 운세"
    monthly_guide: "월별 주의사항과 길일"
    compatibility: "띠별 궁합과 상극관계"
    lucky_items: "띠별 행운의 아이템/색상/숫자"
    
  cultural_elements:
    traditional_story: "12지신 전설과 유래"
    historical_context: "역사 속 유명 인물들"
    korean_adaptation: "한국적 해석과 특징"
    
  modern_application:
    career_guidance: "띠별 직업 적성"
    relationship_tips: "띠별 연애 스타일"
    parenting: "아이의 띠별 교육법"
```

### **1️⃣1️⃣ 바이오리듬**

```yaml
바이오리듬:
  service_id: "biorhythm"
  target_users: "20-50대 (과학적 관심층)"
  emotional_keywords: ["주기", "리듬", "최적화", "균형"]
  
  rhythm_types:
    physical_cycle:
      period: "23일 주기"
      focus: "체력, 건강, 운동 능력"
      applications: "운동 계획, 다이어트, 건강 관리"
      
    emotional_cycle:
      period: "28일 주기"
      focus: "감정, 기분, 직감력"
      applications: "인간관계, 의사결정, 창작 활동"
      
    intellectual_cycle:
      period: "33일 주기"
      focus: "사고력, 집중력, 학습 능력"
      applications: "업무, 시험, 프로젝트"
  
  visualization:
    wave_chart: "사인파 형태의 리듬 차트"
    calendar_view: "달력 형태 일일 상태"
    predictive_graph: "향후 30일 예측"
    optimal_timing: "최적 타이밍 알림"
    
  practical_applications:
    workout_planner: "바이오리듬 기반 운동 계획"
    study_schedule: "학습 효율 최적화"
    meeting_scheduler: "중요 미팅 최적 일정"
    creative_timing: "창작 활동 최적기"
```

### **1️⃣2️⃣ 오늘의운세 (데일리)**

```yaml
오늘의운세:
  service_id: "daily_fortune"
  target_users: "전 연령층 (일일 방문자)"
  emotional_keywords: ["오늘", "현재", "즉시", "실용"]
  
  daily_content:
    comprehensive:
      title: "오늘의 종합 운세"
      scores: "총운(100점), 애정(5★), 직업(5★), 금전(5★)"
      
    specific_guidance:
      lucky_time: "행운의 시간대"
      lucky_direction: "길한 방향"
      lucky_color: "행운의 색상"
      lucky_number: "행운의 숫자"
      
    practical_tips:
      morning_routine: "아침 시작 의식"
      important_decisions: "중요 결정 타이밍"
      social_interactions: "인간관계 주의사항"
      evening_reflection: "저녁 마무리 의식"
  
  personalization:
    birth_based: "생년월일 기반 개인화"
    history_learning: "과거 피드백 학습"
    preference_adaptation: "사용자 선호도 반영"
    
  engagement_features:
    push_notification: "매일 아침 8시 알림"
    social_sharing: "SNS 운세 공유"
    fortune_streak: "연속 확인일 기록"
    daily_mission: "오늘의 행운 미션"
```

### **1️⃣3️⃣ 힐링매거진**

```yaml
힐링매거진:
  service_id: "healing_magazine"
  target_users: "30-60대 (깊이 있는 콘텐츠 선호층)"
  emotional_keywords: ["위로", "치유", "성찰", "지혜"]
  
  content_categories:
    life_wisdom:
      title: "삶의 지혜 에세이"
      topics: ["인생 철학", "마음 다스리기", "관계의 지혜"]
      format: "3,000-5,000자 깊이 있는 글"
      
    healing_stories:
      title: "치유의 이야기"
      topics: ["극복 스토리", "변화의 순간", "깨달음의 경험"]
      format: "실제 경험담 + 전문가 해석"
      
    meditation_guide:
      title: "명상 & 마음 수행"
      topics: ["일일 명상", "호흡법", "마음챙김"]
      format: "가이드 + 오디오/비디오"
      
    seasonal_healing:
      title: "계절별 힐링 가이드"
      topics: ["절기별 마음관리", "자연과 함께하는 치유"]
      format: "계절감 있는 비주얼 + 실천법"
  
  multimedia_content:
    audio_meditation: "명상 가이드 오디오"
    healing_video: "치유 영상 콘텐츠"
    nature_sounds: "자연의 소리 모음"
    calming_music: "힐링 배경음악"
    
  community_features:
    reader_stories: "독자 경험담 공유"
    expert_qna: "전문가 Q&A 코너"
    healing_challenge: "30일 힐링 챌린지"
    discussion_forum: "주제별 토론방"
```

### **1️⃣4️⃣ 1:1상담**

```yaml
일대일상담:
  service_id: "personal_consultation"
  target_users: "모든 연령층 (개인화 서비스 니즈)"
  emotional_keywords: ["전문성", "개인화", "깊이", "해결"]
  
  consultation_types:
    text_chat:
      method: "실시간 텍스트 채팅"
      duration: "30분-1시간"
      price: "30,000-50,000원"
      
    voice_call:
      method: "음성 통화 상담"
      duration: "30분-1시간"  
      price: "50,000-80,000원"
      
    video_session:
      method: "화상 상담 (얼굴 보고)"
      duration: "1시간"
      price: "80,000-120,000원"
      
    premium_package:
      method: "패키지 상담 (3회 연속)"
      duration: "3주간 3회 세션"
      price: "200,000-300,000원"
  
  expert_categories:
    saju_master: "사주명리학 전문가"
    psychology_counselor: "심리 상담사"
    life_coach: "인생 코칭 전문가"
    relationship_expert: "연애/결혼 전문가"
    career_consultant: "커리어 컨설턴트"
    spiritual_guide: "영성/철학 가이드"
    
  quality_assurance:
    expert_verification: "전문가 자격 검증"
    rating_system: "상담사별 평점 시스템"
    satisfaction_guarantee: "불만족 시 재상담 보장"
    privacy_protection: "완전한 개인정보 보호"
    
  booking_system:
    availability_calendar: "상담사별 예약 가능 시간"
    instant_matching: "즉시 상담 가능한 전문가 매칭"
    scheduled_session: "사전 예약 시스템"
    emergency_consultation: "긴급 상담 서비스"
```

### **1️⃣5️⃣ 힐링스토어**

```yaml
힐링스토어:
  service_id: "healing_store"
  target_users: "30-60대 (구매력 있는 힐링 관심층)"
  emotional_keywords: ["특별함", "정성", "에너지", "변화"]
  
  product_categories:
    gemstones:
      title: "개인 맞춤 보석/크리스탈"
      items: ["탄생석", "행운석", "차크라 스톤"]
      price_range: "30,000-500,000원"
      
    accessories:
      title: "풍수/운세 액세서리"
      items: ["브레이슬릿", "목걸이", "반지", "부적"]
      price_range: "50,000-300,000원"
      
    home_items:
      title: "집안 운기 개선 용품"
      items: ["풍수 거울", "수정 장식", "향", "그림"]
      price_range: "100,000-1,000,000원"
      
    books_media:
      title: "심리/철학/운세 도서"
      items: ["운세책", "명상 가이드", "오디오북"]
      price_range: "20,000-100,000원"
      
    digital_products:
      title: "디지털 상품"
      items: ["프리미엄 운세", "명상앱", "맞춤 음성"]
      price_range: "5,000-50,000원"
  
  personalization_service:
    saju_based_recommendation: "사주 기반 상품 추천"
    color_therapy: "개인 컬러 테라피 상품"
    energy_matching: "에너지 궁합 상품"
    
  shopping_experience:
    ar_try_on: "AR로 액세서리 착용 체험"
    energy_scanner: "상품의 에너지 분석"
    expert_curation: "전문가 추천 큐레이션"
    gift_wrapping: "특별한 포장 서비스"
```

### **1️⃣6️⃣ 고민상담**

```yaml
고민상담:
  service_id: "worry_consultation"
  target_users: "전 연령층 (고민 해결 니즈)"
  emotional_keywords: ["해결", "공감", "조언", "방향"]
  
  consultation_methods:
    anonymous_forum:
      method: "익명 게시판 상담"
      response_time: "24시간 내"
      cost: "무료"
      
    ai_counseling:
      method: "AI 챗봇 즉시 상담"
      response_time: "실시간"
      cost: "무료 (기본) / 유료 (심화)"
      
    peer_support:
      method: "또래 상담 그룹"
      response_time: "그룹 활동 시간"
      cost: "무료"
      
    expert_consultation:
      method: "전문가 직접 상담"
      response_time: "예약제"
      cost: "유료"
  
  worry_categories:
    relationships:
      title: "인간관계 고민"
      subtopics: ["가족", "친구", "연인", "직장"]
      
    career:
      title: "진로/직업 고민"
      subtopics: ["취업", "이직", "승진", "창업"]
      
    personal_growth:
      title: "자기계발 고민"
      subtopics: ["성격", "습관", "목표", "자존감"]
      
    life_decisions:
      title: "인생 선택 고민"
      subtopics: ["결혼", "이주", "투자", "교육"]
  
  support_features:
    emotion_analysis: "감정 상태 분석"
    solution_pathway: "단계별 해결 방안 제시"
    progress_tracking: "고민 해결 과정 추적"
    resource_library: "관련 자료 추천"
    
  privacy_safety:
    complete_anonymity: "완전 익명 보장"
    content_moderation: "부적절 내용 필터링"
    crisis_intervention: "위기 상황 전문가 개입"
    community_guidelines: "건전한 소통 문화"
```

### **1️⃣7️⃣ 공지사항**

```yaml
공지사항:
  service_id: "announcements"
  target_users: "전체 사용자"
  emotional_keywords: ["소통", "투명성", "참여", "공동체"]
  
  announcement_types:
    service_updates:
      title: "서비스 업데이트"
      content: "새 기능, 개선사항, 버그 수정"
      frequency: "주 1-2회"
      
    special_events:
      title: "특별 이벤트"
      content: "할인, 무료체험, 경품이벤트"
      frequency: "월 2-3회"
      
    maintenance:
      title: "시스템 점검"
      content: "서버 점검, 업데이트, 장애 공지"
      frequency: "필요시"
      
    community_news:
      title: "커뮤니티 소식"
      content: "회원 이야기, 성공사례, 피드백"
      frequency: "월 1회"
  
  engagement_features:
    comment_system: "공지사항 댓글 시스템"
    reaction_buttons: "좋아요/도움됨/관심없음"
    notification_preference: "알림 설정 개인화"
    read_tracking: "읽음 확인 기능"
    
  design_elements:
    priority_badges: "중요도별 배지 (긴급/중요/일반)"
    visual_alerts: "시각적 알림 표시"
    categorization: "카테고리별 필터링"
    search_function: "공지사항 검색"
```

---

## 🔀 **서비스 간 연결 플로우**

### **🌟 사용자 여정별 서비스 연결**

```yaml
User_Journey_Flow:
  # 단계 1: 첫 방문 (Discovery)
  entry_points:
    - "오늘의운세 (가벼운 시작)"
    - "별자리 (친숙한 콘텐츠)"
    - "바이오리듬 (과학적 관심)"
    
  next_steps:
    - "흥미 → 타로 체험"
    - "만족 → 종합운세 시도"
    - "궁금 → 성격분석 참여"
  
  # 단계 2: 탐색 (Exploration)
  exploration_phase:
    primary_services:
      - "종합운세 (메인 서비스)"
      - "연애운/취업운 (관심 영역)"
      - "성격분석 (자기이해)"
      
    supporting_content:
      - "12지신 (문화적 친숙함)"
      - "힐링매거진 (깊이 있는 콘텐츠)"
      - "타로 (재미 요소)"
  
  # 단계 3: 참여 (Engagement)
  engagement_phase:
    premium_transition:
      - "전문 운세 서비스"
      - "1:1 개인 상담"
      - "맞춤형 심층 분석"
      
    community_participation:
      - "고민상담 참여"
      - "힐링매거진 댓글"
      - "경험 공유"
  
  # 단계 4: 충성도 (Loyalty)
  loyalty_phase:
    subscription_services:
      - "프리미엄 구독"
      - "정기 상담 패키지"
      - "VIP 멤버십"
      
    ecosystem_engagement:
      - "힐링스토어 구매"
      - "지인 추천 활동"
      - "커뮤니티 리더 역할"
```

### **🔄 교차 판매 (Cross-Selling) 전략**

```typescript
interface CrossSellingMatrix {
  // 종합운세 → 연관 서비스
  comprehensive_fortune: {
    immediate: ["성격분석", "연애운", "취업운"];
    suggested: ["타로", "1:1상담"];
    premium: ["심층사주", "연간운세"];
  };
  
  // 연애운 → 연관 서비스  
  love_fortune: {
    immediate: ["타로연애", "별자리궁합", "12지신궁합"];
    suggested: ["1:1연애상담", "고민상담"];
    premium: ["커플전용대시보드", "프리미엄궁합"];
  };
  
  // 타로 → 연관 서비스
  tarot: {
    immediate: ["오늘의운세", "별자리"];
    suggested: ["연애운", "고민상담"];
    premium: ["전문타로상담", "개인덱구매"];
  };
  
  // 1:1상담 → 연관 서비스
  consultation: {
    immediate: ["고민상담게시판", "힐링매거진"];
    suggested: ["관련운세서비스", "힐링스토어"];
    premium: ["정기상담패키지", "VIP멤버십"];
  };
}
```

---

## 📊 **콘텐츠 생산 전략**

### **🎯 월별 콘텐츠 목표**

```yaml
Monthly_Content_Goals:
  총_콘텐츠_목표: "월 500개+ (연 6,000개+)"
  
  content_breakdown:
    daily_content: "일 15개 × 30일 = 450개"
      - "오늘의운세: 12성좌 × 30일 = 360개"
      - "바이오리듬: 일 1개 × 30일 = 30개"  
      - "타로일일카드: 일 1개 × 30일 = 30개"
      - "힐링메시지: 일 1개 × 30일 = 30개"
      
    weekly_content: "주 10개 × 4주 = 40개"
      - "심층운세: 12성좌 × 4주 = 48개 (겹침 조정)"
      - "타로스프레드: 주 2개 × 4주 = 8개"
      - "전문가칼럼: 주 1개 × 4주 = 4개"
      
    monthly_content: "월 10개"
      - "월간운세: 12성좌 = 12개 (2개 초과)"
      - "힐링매거진: 월 4개"
      - "특별기획: 월 2개"
      
  quality_control:
    ai_generation: "60% (자동화된 기본 콘텐츠)"
    human_curation: "30% (전문가 검토 및 수정)"
    premium_handcraft: "10% (전문가 직접 작성)"
```

### **🤖 AI 기반 콘텐츠 생산 시스템**

```typescript
interface ContentGenerationSystem {
  ai_models: {
    basic_fortune: "GPT-4 Turbo (빠른 일일 운세)";
    detailed_analysis: "Claude-3 Opus (심층 분석)";
    creative_content: "Gemini-1.5 Pro (창의적 해석)";
    korean_optimization: "HyperCLOVA X (한국어 특화)";
  };
  
  content_templates: {
    daily_horoscope: "표준화된 12성좌 템플릿";
    tarot_interpretation: "78장 타로카드 해석 DB";
    biorhythm_analysis: "3주기 조합별 메시지";
    personality_insights: "MBTI×사주 조합 분석";
  };
  
  personalization_engine: {
    user_history: "과거 이용 패턴 분석";
    preference_learning: "피드백 기반 학습";
    cultural_adaptation: "연령대/성별/지역별 맞춤화";
    seasonal_adjustment: "계절/절기/이벤트 반영";
  };
}
```

---

*📅 문서 작성일: 2025-08-23*  
*🎯 총 서비스: 17개 (핵심 7개 + 재미콘텐츠 10개)*  
*📊 콘텐츠 목표: 월 500개+ (포스텔러 6,000+ 대비 10,000+ 목표)*  
*🔄 교차판매: 16개 연결 플로우 설계*  
*📍 문서 위치: `/home/ubuntu/REFERENCE_LIBRARY/feature-specs/master-plans/`*