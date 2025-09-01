# 🎨 크롤링 대시보드 디자인 시스템 v2.0

> **완전 재현 가능한 UI/UX 설계도**  
> **스타일가이드**: 글래스모피즘 + 사이버 테마  
> **반응형**: Mobile-First + Desktop 최적화

## 🌈 색상 시스템

### 기본 팔레트
```css
/* 배경 그라디언트 */
.primary-bg {
  background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
}

.overlay-bg {
  background: linear-gradient(135deg, rgba(0,0,0,0.6) 0%, rgba(59,130,246,0.4) 50%, rgba(0,0,0,0.7) 100%);
}

/* 글래스 효과 */
.glass-effect {
  backdrop-filter: blur(16px);
  background: rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
}

/* 상태별 색상 */
.status-active { color: #4ADE80; background: rgba(74, 222, 128, 0.2); }
.status-idle { color: #60A5FA; background: rgba(96, 165, 250, 0.2); }
.status-error { color: #F87171; background: rgba(248, 113, 113, 0.2); }
```

### 계층별 색상 코딩
```css
/* 3-Tier 크롤러별 색상 */
.tier-httpx { 
  primary: #10B981;    /* 빠른 수집 - 녹색 */
  background: rgba(16, 185, 129, 0.1);
}

.tier-playwright { 
  primary: #3B82F6;    /* 동적 페이지 - 파랑 */
  background: rgba(59, 130, 246, 0.1);
}

.tier-selenium { 
  primary: #8B5CF6;    /* 복잡한 SPA - 보라 */
  background: rgba(139, 92, 246, 0.1);
}
```

## 🎭 컴포넌트 UI 패턴

### 1. **헤더 컴포넌트**
```css
.crawling-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
}

/* 상태 배지 */
.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-badge::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}
```

### 2. **사이드바 네비게이션**
```css
.sidebar {
  width: 16rem; /* 확장 상태 */
  width: 4rem;  /* 축소 상태 */
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(8px);
  transition: width 0.3s ease;
}

.nav-item {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
  cursor: pointer;
}

.nav-item.active {
  background: rgba(59, 130, 246, 0.2);
  border-left: 4px solid #3B82F6;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}
```

### 3. **글래스 카드 컴포넌트**
```css
.glass-card {
  background: rgba(15, 23, 42, 0.3);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.glass-card:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 12px 48px rgba(59, 130, 246, 0.2);
}
```

### 4. **작업 상태 표시**
```css
/* 진행률 바 */
.progress-bar {
  height: 8px;
  background: rgba(71, 85, 105, 0.5);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10B981 0%, #3B82F6 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* 티어별 배지 */
.tier-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.tier-httpx { background: #10B981; color: white; }
.tier-playwright { background: #3B82F6; color: white; }
.tier-selenium { background: #8B5CF6; color: white; }
```

## ✨ 애니메이션 라이브러리

### Framer Motion 설정
```typescript
// 페이지 전환 애니메이션
const pageTransition = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.3 }
};

// 호버 애니메이션
const hoverScale = {
  whileHover: { scale: 1.02 },
  whileTap: { scale: 0.98 }
};

// 진입 애니메이션 (stagger)
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};
```

### 로딩 애니메이션
```css
/* 펄스 애니메이션 */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 회전 애니메이션 */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 글로우 효과 */
@keyframes glow {
  0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
  50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.8); }
}
```

## 📱 반응형 디자인

### 브레이크포인트
```css
/* Tailwind 기본 브레이크포인트 */
sm: 640px   /* 모바일 가로 */
md: 768px   /* 태블릿 */
lg: 1024px  /* 데스크탑 */
xl: 1280px  /* 대형 화면 */
2xl: 1536px /* 초대형 화면 */
```

### 모바일 최적화
```css
/* 사이드바 모바일 처리 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 40;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
}

/* 카드 그리드 반응형 */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 640px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
```

## 🔤 타이포그래피 시스템

### 폰트 계층구조
```css
/* 헤더 */
.title-primary { 
  font-size: 1.25rem; /* text-xl */
  font-weight: 700;    /* font-bold */
  color: white;
  font-family: 'Pretendard', sans-serif;
}

.title-secondary {
  font-size: 0.875rem; /* text-sm */
  color: #94A3B8;      /* slate-400 */
}

/* 본문 */
.body-text {
  font-size: 0.875rem; /* text-sm */
  font-weight: 500;    /* font-medium */
  color: #CBD5E1;      /* slate-300 */
}

/* 메트릭 숫자 */
.metric-number {
  font-size: 1.875rem; /* text-3xl */
  font-weight: 700;    /* font-bold */
  font-family: 'JetBrains Mono', monospace;
}
```

## 🎛️ 인터랙션 디자인

### 버튼 스타일
```css
/* 주요 액션 버튼 */
.btn-primary {
  background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
}

/* 보조 버튼 */
.btn-secondary {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.3);
  color: #E2E8F0;
  backdrop-filter: blur(8px);
}

.btn-secondary:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(59, 130, 246, 0.5);
}
```

### 상태 표시 패턴
```css
/* 활성 상태 */
.status-active::before {
  content: '';
  width: 8px;
  height: 8px;
  background: #4ADE80;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

/* 로딩 스피너 */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid #3B82F6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

## 🎪 드래그 앤 드롭 스타일

### DND Kit 커스터마이징
```css
/* 드래그 중인 아이템 */
.dragging {
  opacity: 0.8;
  transform: rotate(5deg);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

/* 드롭 영역 */
.drop-zone {
  border: 2px dashed rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.1);
  border-radius: 12px;
}

/* 드래그 핸들 */
.drag-handle {
  cursor: grab;
  color: #64748B;
  transition: color 0.2s;
}

.drag-handle:hover {
  color: #3B82F6;
}

.drag-handle:active {
  cursor: grabbing;
}
```

## 📊 메트릭 표시 디자인

### KPI 카드
```css
.kpi-card {
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
}

.kpi-value {
  font-size: 2.25rem; /* text-4xl */
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### 차트 스타일
```css
/* 진행률 바 */
.progress-container {
  background: rgba(71, 85, 105, 0.4);
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #10B981 0%, #3B82F6 100%);
  border-radius: 4px;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 도넛 차트 컨테이너 */
.chart-container {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(8px);
}
```

## 🎯 모션 디자인

### 페이지 전환 패턴
```typescript
// 기본 페이지 전환
const pageVariants = {
  initial: { opacity: 0, y: 20, scale: 0.98 },
  animate: { 
    opacity: 1, 
    y: 0, 
    scale: 1,
    transition: { duration: 0.4, ease: "easeOut" }
  },
  exit: { 
    opacity: 0, 
    y: -20, 
    scale: 0.98,
    transition: { duration: 0.3, ease: "easeIn" }
  }
};

// 스태거 애니메이션 (목록)
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      delayChildren: 0.1,
      staggerChildren: 0.05
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.3 }
  }
};
```

### 마이크로인터랙션
```typescript
// 버튼 호버 효과
const buttonHover = {
  whileHover: { 
    scale: 1.05, 
    boxShadow: "0 10px 25px rgba(59, 130, 246, 0.4)" 
  },
  whileTap: { scale: 0.95 }
};

// 카드 호버 효과
const cardHover = {
  whileHover: { 
    y: -4,
    boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)"
  }
};
```

## 🔧 컴포넌트별 스타일 가이드

### CrawlingHeader
```css
.header-logo {
  background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.header-metrics {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #CBD5E1;
}
```

### CrawlingSidebar  
```css
.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
}

.tier-status {
  margin-top: 1rem;
  padding: 1rem;
}

.tier-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 0.875rem;
}
```

### 작업 관리 카드
```css
.job-card {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.job-card:hover {
  border-color: rgba(59, 130, 246, 0.4);
  background: rgba(30, 41, 59, 0.6);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.job-controls {
  display: flex;
  gap: 0.5rem;
}
```

## 🎨 아이콘 시스템

### Lucide React 아이콘 매핑
```typescript
const iconMap = {
  dashboard: BarChart3,
  crawling: Activity,
  ai: Brain,
  data: Database,
  settings: Settings,
  status: {
    active: CheckCircle,
    error: XCircle,
    loading: RefreshCw
  },
  tier: {
    httpx: Zap,
    playwright: Globe, 
    selenium: Layers
  }
};
```

### 아이콘 스타일링
```css
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }

.icon-status {
  color: currentColor;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.icon-status:hover {
  opacity: 1;
}
```

## 🌊 실시간 UI 업데이트

### 실시간 표시 패턴
```css
/* 실시간 데이터 깜빡임 */
.realtime-update {
  animation: flash 0.3s ease-in-out;
}

@keyframes flash {
  0% { background-color: rgba(59, 130, 246, 0.2); }
  50% { background-color: rgba(59, 130, 246, 0.4); }
  100% { background-color: transparent; }
}

/* 연결 상태 표시 */
.connection-status {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 100;
}

.connected { color: #10B981; }
.disconnected { color: #F87171; }
.reconnecting { color: #F59E0B; }
```

---

**🎨 디자인 철학**: 기능성 우선, 직관적 인터페이스, 현대적 글래스모피즘  
**⚡ 성능 목표**: 60fps 유지, 200ms 이하 응답시간, 부드러운 애니메이션

*이 가이드로 동일한 디자인 완전 재현 가능*