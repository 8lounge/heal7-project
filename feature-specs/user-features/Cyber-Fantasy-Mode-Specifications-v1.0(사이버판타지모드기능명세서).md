# 🌌 사이버 판타지 모드 기능 명세서 v1.0

> **프로젝트**: HEAL7 사이버 판타지 운명학 플랫폼  
> **버전**: v1.0.0  
> **작성일**: 2025-08-19  
> **범위**: 사이버 판타지 모드 전용 기능 상세 스펙  
> **참조**: `Cyber-Fantasy-Fortune-Platform-Architecture-v1.0.md`

## 🎯 **핵심 기능 개요**

### **💫 모드 전환 시스템**

```typescript
interface ModeToggleSpec {
  component: "ExperienceModeSelector"
  location: "메인 페이지 우상단"
  animation: "morphing_toggle_switch"
  states: {
    basic: {
      icon: "📱",
      label: "실용 모드", 
      description: "빠르고 간편한 운세 확인"
    },
    fantasy: {
      icon: "🌌", 
      label: "사이버 판타지",
      description: "몰입형 3D 우주 경험"
    }
  }
  transition: {
    duration: "1.5s",
    effect: "particle_warp_transition",
    sound: "cosmic_chime.mp3"
  }
}
```

### **🔮 명리 Crystal Core 모듈**

#### **기능 사양**
```typescript
interface SajuCrystalSpec {
  // 3D 크리스탈 렌더링
  crystal: {
    geometry: "OctahedronGeometry(radius: 2)"
    material: "MeshDistortMaterial"
    distortion: {
      speed: 2,
      distort: 0.5,
      radius: 1
    }
    colors: "오행별 동적 그라데이션"
  }
  
  // 사용자 인터랙션
  interactions: {
    rotation: "OrbitControls 자동 회전"
    zoom: "마우스 휠 확대/축소"
    hover: "크리스탈 면 하이라이트"
    click: "해당 기둥 상세 정보 표시"
  }
  
  // 파티클 시스템
  particles: {
    count: 1000,
    behavior: "orbital", // 십성이 크리스탈 주위 궤도 운동
    colors: "사주 오행에 따른 동적 색상",
    interactive: true // 클릭시 십성 설명
  }
  
  // 데이터 연동
  data_source: "기존 heal7-project 사주 계산 결과"
  mapping: {
    년주: "크리스탈 상단면",
    월주: "크리스탈 우측면", 
    일주: "크리스탈 정면",
    시주: "크리스탈 좌측면"
  }
}
```

#### **구현 예시 코드**
```jsx
// 즉시 사용 가능한 레고블럭 컴포넌트
function SajuCrystal({ sajuData, onInteraction }) {
  const meshRef = useRef()
  const { size, viewport } = useThree()
  
  // 오행별 색상 매핑
  const getElementColor = (element) => {
    const colors = {
      목: '#00FF41', // 사이버 그린
      화: '#FF0040', // 네온 레드  
      토: '#FFD700', // 사이버 골드
      금: '#00FFFF', // 사이버 시안
      수: '#8B00FF'  // 네온 퍼플
    }
    return colors[element] || '#FFFFFF'
  }
  
  return (
    <group>
      {/* 메인 크리스탈 */}
      <mesh ref={meshRef} rotation={[0, useTime() * 0.5, 0]}>
        <octahedronGeometry args={[2, 0]} />
        <MeshDistortMaterial
          color={getElementColor(sajuData.dominant_element)}
          speed={2}
          distort={0.5}
          radius={1}
        >
          <GradientTexture
            stops={[0, 0.5, 1]}
            colors={['#00FFFF', '#FF00FF', '#FFD700']}
          />
        </MeshDistortMaterial>
      </mesh>
      
      {/* 십성 궤도 파티클 */}
      <SipsinOrbitParticles 
        data={sajuData.sipsin}
        radius={3}
        count={1000}
      />
      
      {/* 상호작용 감지 */}
      <InteractionHandler 
        onHover={(face) => showPillarInfo(face)}
        onClick={(face) => onInteraction(face)}
      />
    </group>
  )
}
```

### **🃏 타로 홀로그램 덱**

#### **기능 사양**
```typescript
interface TarotHologramSpec {
  // 카드 레이아웃
  layouts: {
    "one_card": "오늘의 카드",
    "three_card": "과거-현재-미래", 
    "celtic_cross": "완전한 켈틱 크로스",
    "star_spread": "7차크라 별자리 배치"
  }
  
  // 홀로그램 효과
  hologram: {
    material: "HolographicMaterial",
    shimmer: "무지갯빛 홀로그램 효과",
    transparency: 0.8,
    glow: "카드 테두리 네온 글로우"
  }
  
  // 애니메이션
  animations: {
    draw: "카드가 데크에서 홀로그램으로 나타남",
    flip: "3D 회전으로 카드 뒷면→앞면",
    reveal: "파티클 폭발 후 의미 텍스트 표시"
  }
  
  // AI 해석
  interpretation: {
    tone: "희망적이고 건설적",
    focus: "강점과 기회 중심",
    personalization: "사용자 히스토리 기반 맞춤",
    voice: "신비롭지만 친근한 톤"
  }
}
```

### **⭐ 별자리 Constellation Map**

#### **기능 사양**
```typescript
interface ConstellationMapSpec {
  // 개인 별자리 생성
  personal_constellation: {
    algorithm: "생년월일 기반 별 배치",
    stars: "개인의 특성을 나타내는 12개 별",
    connections: "네온 라인으로 별들 연결",
    pattern: "고유한 개인 별자리 패턴"
  }
  
  // 인터랙티브 요소  
  interactions: {
    star_hover: "별 정보 툴팁 표시",
    star_click: "해당 특성 상세 설명",
    constellation_rotate: "3D 공간에서 자유 회전",
    zoom: "특정 별자리 영역 확대"
  }
  
  // AR 모드
  ar_mode: {
    api: "WebXR API",
    trigger: "실제 밤하늘에 개인 별자리 오버레이",
    interaction: "실제 별과 가상 별자리 정보 연결",
    fallback: "AR 미지원시 VR 모드로 대체"
  }
  
  // 시각 효과
  visual_effects: {
    stars: "반짝이는 파티클",
    connections: "흐르는 네온 라인",
    background: "우주 성운 배경",
    atmosphere: "희미한 우주 먼지 효과"
  }
}
```

### **🏠 풍수 Energy Grid**

#### **기능 사양**
```typescript
interface FengShuiGridSpec {
  // 3D 에너지 맵
  energy_visualization: {
    grid: "9x9 구궁도 3D 히트맵",
    colors: "에너지 강도별 색상 그라데이션",
    height: "에너지 레벨을 높이로 표현",
    flow: "에너지 흐름 벡터 화살표"
  }
  
  // 개인화 분석
  personalization: {
    birth_data: "사주 기반 개인 에너지 타입",
    space_scan: "현재 위치 또는 입력된 공간 정보",
    matching: "개인 에너지 vs 공간 에너지 매칭도",
    optimization: "최적 배치 추천"
  }
  
  // 추천 시스템
  recommendations: {
    furniture: "가구 배치 최적화",
    colors: "개인에게 맞는 색상 팔레트", 
    direction: "유리한 방향 가이드",
    items: "에너지 증폭 아이템 추천"
  }
  
  // 실시간 업데이트
  dynamic_analysis: {
    time_factor: "시간대별 에너지 변화",
    season_factor: "계절별 에너지 흐름",
    personal_cycle: "개인 바이오리듬 연동"
  }
}
```

### **🧬 Bio-Energy Scanner (사상체질)**

#### **기능 사양**
```typescript
interface BioEnergyScannerSpec {
  // 입력 방식
  input_methods: {
    questionnaire: "전통 사상체질 설문 (선택형)",
    facial_analysis: "얼굴 인식 기반 분석 (선택적)",
    combination: "설문 + AI 분석 융합"
  }
  
  // AI 분석
  ai_analysis: {
    model: "사상체질 분류 커스텀 모델",
    features: "얼굴 특징점 추출",
    accuracy: "설문과 AI 분석 가중 평균",
    confidence: "분석 신뢰도 표시"
  }
  
  // 에너지 시각화
  energy_flow: {
    system: "파티클 시스템",
    meridians: "경락을 따른 기 흐름 표현",
    colors: "체질별 고유 색상",
    animation: "흐르는 에너지 애니메이션"
  }
  
  // 건강 매트릭스
  health_matrix: {
    constitution: "태양인/태음인/소양인/소음인",
    strengths: "체질별 강점",
    weaknesses: "주의할 건강 포인트",
    recommendations: "맞춤 건강 관리법"
  }
}
```

## 🎮 **게이미피케이션 시스템**

### **일일 퀘스트**
```typescript
const dailyQuests = [
  {
    id: "daily_tarot",
    title: "오늘의 타로 카드 뽑기",
    reward: "Cosmic Points +10",
    unlock: "새로운 카드 스킨"
  },
  {
    id: "energy_scan", 
    title: "바이오 에너지 스캔",
    reward: "Health Insight +1",
    unlock: "체질별 건강 팁"
  },
  {
    id: "constellation_explore",
    title: "개인 별자리 탐험",
    reward: "Star Fragments +5", 
    unlock: "새로운 별자리 패턴"
  }
]
```

### **레벨 시스템**
```typescript
const userLevels = {
  1: { title: "Seeker of Truth", points: 0 },
  10: { title: "Cosmic Navigator", points: 1000 },
  25: { title: "Oracle Master", points: 5000 },
  50: { title: "Universe Whisperer", points: 15000 }
}
```

### **컬렉션 시스템**
```typescript
const collections = {
  tarot_decks: ["Classic", "Cyberpunk", "Ethereal", "Cosmic"],
  crystals: ["Fire Ruby", "Water Sapphire", "Earth Emerald"],
  constellations: ["Personal Stars", "Destiny Patterns", "Lucky Alignments"]
}
```

## 🔧 **성능 및 최적화**

### **3D 렌더링 최적화**
```typescript
const optimizations = {
  lod: "거리별 디테일 레벨 자동 조정",
  culling: "화면 밖 객체 렌더링 제외",
  texture_compression: "모바일 환경 최적화",
  shader_optimization: "미리 컴파일된 셰이더"
}
```

### **모바일 대응**
```typescript
const mobileOptimizations = {
  adaptive_quality: "기기 성능에 따른 품질 조정",
  touch_gestures: "터치 제스처 지원",
  battery_aware: "배터리 절약 모드",
  offline_mode: "오프라인 기본 기능"
}
```

---

**🎯 구현 우선순위**: 명리 Crystal Core → 타로 홀로그램 → 게이미피케이션 → 별자리 맵 → 풍수 그리드 → 바이오 스캐너