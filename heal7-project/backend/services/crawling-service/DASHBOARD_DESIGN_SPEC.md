# 🎯 HEAL7 크롤링 대시보드 설계 명세서

> **프로젝트**: Modern Crawling Dashboard v2.0  
> **대상**: crawling.heal7.com  
> **최종 업데이트**: 2025-08-30  

---

## 📋 **프로젝트 개요**

### 🎯 **목표**
3-Tier 지능형 크롤링 시스템을 위한 차세대 웹 대시보드 구축
- 실시간 크롤링 모니터링 및 제어
- AI 기반 멀티모달 분석 결과 시각화
- 직관적이고 현대적인 사용자 경험 제공

### 🏗️ **핵심 아키텍처**
- **Backend**: 3-Tier Crawler + AI Analysis Engine
- **Frontend**: React 19 + TypeScript + Tailwind CSS
- **Real-time**: WebSocket + Server-Sent Events
- **Database**: PostgreSQL + Redis Cache
- **Charts**: Chart.js + D3.js 하이브리드

---

## 🎨 **UI/UX 설계 원칙**

### 🧠 **Design Philosophy**
```
"데이터의 복잡성을 단순함으로 변환하는 인터페이스"
- 직관성 (Intuitive)
- 효율성 (Efficient) 
- 미학성 (Aesthetic)
- 확장성 (Scalable)
```

### 🎨 **디자인 시스템**

#### **컬러 팔레트**
```scss
// Primary Colors
--primary-blue: #3b82f6      // 메인 액션, 링크
--primary-indigo: #6366f1    // 크롤링 상태
--success-green: #10b981     // 성공, 완료
--warning-orange: #f59e0b    // 경고, 대기
--error-red: #ef4444         // 에러, 실패
--info-purple: #8b5cf6       // 정보, AI 분석

// Neutral Colors
--gray-50: #f9fafb          // 배경
--gray-100: #f3f4f6         // 카드 배경
--gray-200: #e5e7eb         // 구분선
--gray-500: #6b7280         // 부차 텍스트
--gray-900: #111827         // 메인 텍스트

// Dark Theme
--dark-bg: #0f172a          // 다크 배경
--dark-surface: #1e293b     // 다크 카드
--dark-border: #334155      // 다크 구분선
```

#### **타이포그래피**
```scss
// Font Stack
font-family: 'Inter', 'Pretendard', -apple-system, sans-serif;

// Hierarchy
--text-hero: 3rem/1.1          // 메인 제목
--text-h1: 2.25rem/1.2         // 섹션 제목
--text-h2: 1.875rem/1.3        // 서브 섹션
--text-h3: 1.5rem/1.4          // 카드 제목
--text-body: 1rem/1.5          // 본문
--text-small: 0.875rem/1.4     // 라벨, 캡션
--text-xs: 0.75rem/1.3         // 상태, 메타
```

#### **간격 시스템**
```scss
// Spacing Scale (Tailwind 기반)
--space-1: 0.25rem    // 4px
--space-2: 0.5rem     // 8px
--space-3: 0.75rem    // 12px
--space-4: 1rem       // 16px
--space-6: 1.5rem     // 24px
--space-8: 2rem       // 32px
--space-12: 3rem      // 48px
--space-16: 4rem      // 64px
```

---

## 📐 **레이아웃 아키텍처**

### 🏛️ **전체 구조**
```
┌─────────────────────────────────────────────────┐
│ Header Navigation (64px)                        │
├─────────────┬───────────────────────────────────┤
│ Sidebar     │ Main Content Area                 │
│ (280px)     │                                   │
│             │ ┌─────────────────────────────────┐ │
│ 🏠 Dashboard │ │ Page Content                    │ │
│ 🕷️ Crawling  │ │                                 │ │
│ 🤖 AI Analysis│ │                                 │ │
│ 📊 Data Mgmt │ │                                 │ │
│ ⚙️ Settings  │ │                                 │ │
│             │ │                                 │ │
│             │ └─────────────────────────────────┘ │
├─────────────┴───────────────────────────────────┤
│ Status Bar (32px) - 실시간 상태 표시              │
└─────────────────────────────────────────────────┘
```

### 📱 **반응형 브레이크포인트**
```scss
// Mobile First Approach
--mobile: 320px - 768px     // 사이드바 숨김, 풀 스택
--tablet: 768px - 1024px    // 사이드바 축소, 2컬럼
--desktop: 1024px - 1440px  // 풀 레이아웃, 3컬럼
--large: 1440px+            // 와이드 레이아웃, 4컬럼
```

---

## 🏗️ **페이지별 상세 설계**

### 1. 🏠 **메인 대시보드**

#### **레이아웃 구조**
```
┌─────────────────┬─────────────────┬─────────────────┐
│ 📊 시스템 개요    │ 🚀 실시간 성능   │ 📈 성공률 트렌드  │
│ - 활성 크롤러    │ - CPU/메모리     │ - 24시간 추이    │  
│ - 진행중 작업    │ - 응답시간       │ - 크롤러별 비교  │
│ - 완료/실패 수   │ - 처리량         │ - 에러 분류      │
└─────────────────┴─────────────────┴─────────────────┘
┌─────────────────────────────────────────────────────┐
│ 🎯 크롤링 작업 현황                                  │
│ ┌─────────┬───────────┬─────────┬─────────┬────────┐ │
│ │ 작업명   │ 상태      │ 진행률   │ 크롤러   │ 액션   │ │  
│ │ Site A  │ ⚡ 진행중   │ ████ 65% │ httpx   │ ⏸️ ❌  │ │
│ │ Site B  │ ✅ 완료    │ ████ 100%│ playwright│ 📊 💾 │ │
│ │ Site C  │ ⚠️ 대기     │ ──── 0%  │ selenium │ ▶️    │ │
│ └─────────┴───────────┴─────────┴─────────┴────────┘ │
└─────────────────────────────────────────────────────┘
┌─────────────────┬─────────────────┬─────────────────┐
│ 🤖 AI 분석 요약  │ 💾 저장소 현황   │ ⚡ 빠른 액션     │
│ - 처리된 문서    │ - 사용 공간      │ - 새 작업 시작  │
│ - OCR 정확도     │ - 파일 수        │ - 시스템 점검   │
│ - 테이블 추출    │ - 백업 상태      │ - 설정 바로가기 │
└─────────────────┴─────────────────┴─────────────────┘
```

#### **실시간 위젯 컴포넌트**
```typescript
// 주요 KPI 위젯들
interface DashboardWidget {
  id: string;
  title: string;
  type: 'metric' | 'chart' | 'table' | 'status';
  data: any;
  updateInterval: number;
  priority: 'high' | 'medium' | 'low';
}

// 실시간 업데이트 구조
const realtimeWidgets = [
  'systemOverview',    // 시스템 개요 (1초)
  'performanceMetrics', // 성능 지표 (2초)  
  'activeJobs',        // 활성 작업 (5초)
  'successTrends',     // 성공률 추이 (10초)
];
```

### 2. 🕷️ **크롤링 관리 페이지**

#### **작업 생성 마법사**
```
┌─────────────────────────────────────────────────────┐
│ 🆕 새 크롤링 작업 생성                               │
│                                                     │
│ Step 1: 기본 정보                                   │  
│ ┌─ 작업명: [Site Analytics Crawl ___________] ───┐  │
│ │ 설명: [Daily analytics data collection___] │  │
│ │ 태그: #analytics #daily #automated        │  │  
│ └─────────────────────────────────────────────┘  │
│                                                   │
│ Step 2: 대상 URL 설정                              │
│ ┌─ URL 목록 ─────────────────────────────────────┐ │
│ │ https://example.com/analytics              │ │
│ │ https://example.com/reports               │ │  
│ │ [+ URL 추가] [CSV 업로드] [사이트맵 가져오기] │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ Step 3: 크롤링 전략                              │
│ ┌─ 전략 선택 ─────────────────────────────────┐  │
│ │ ○ AUTO    - 자동 선택 (추천)               │  │
│ │ ● FAST    - 빠른 정적 크롤링 (httpx)       │  │  
│ │ ○ RENDER  - 동적 콘텐츠 포함 (playwright)   │  │
│ │ ○ STEALTH - Anti-bot 우회 (selenium)       │  │
│ └─────────────────────────────────────────────┘  │
│                                                   │
│ Step 4: 스케줄링                                   │
│ ┌─ 실행 방식 ─────────────────────────────────┐   │
│ │ ● 즉시 실행                                │   │
│ │ ○ 예약 실행: [2025-08-30 18:00] [반복설정] │   │
│ │ ○ 주기적: 매 [6] 시간마다               │   │
│ └─────────────────────────────────────────────┘   │
│                                                   │
│          [취소]    [미리보기]    [🚀 시작]         │
└─────────────────────────────────────────────────────┘
```

#### **작업 모니터링 뷰**
```
┌─────────────────────────────────────────────────────┐
│ 📊 작업 진행 상황                                    │
│                                                     │
│ Job: "Site Analytics Crawl" (ID: #CR-2025-001)     │
│ Status: ⚡ 진행중 | Started: 2025-08-30 16:30:15    │
│                                                     │
│ ┌─ 전체 진행률 ─────────────────────────────────┐    │
│ │ ████████████████████░░░░░░░░ 73% (146/200)   │    │  
│ │ ETA: 12분 35초 남음                         │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ ┌─ 크롤러별 성능 ─────────────────────────────┐      │
│ │ httpx:     █████████████████████ 95% (✅)   │      │
│ │ playwright: ████████████░░░░░░░░ 60% (⚡)   │      │
│ │ selenium:   ░░░░░░░░░░░░░░░░░░░░  0% (💤)   │      │
│ └─────────────────────────────────────────────┘      │
│                                                       │
│ ┌─ 실시간 로그 ─────────────────────────────────┐    │
│ │ 16:35:42 ✅ httpx: example.com/page1 (0.3s) │    │
│ │ 16:35:43 ⚡ playwright: Loading JS content   │    │  
│ │ 16:35:45 ⚠️  Rate limit hit, waiting 5s...   │    │
│ │ 16:35:50 ✅ playwright: example.com/page2     │    │
│ │ [📜 전체 로그] [⏸️ 일시정지] [❌ 중단]         │    │
│ └─────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

### 3. 🤖 **AI 분석 결과 페이지**

#### **멀티모달 분석 대시보드**
```
┌─────────────────────────────────────────────────────┐
│ 🧠 AI 분석 종합 현황                                 │
│                                                     │
│ ┌─ 모델별 처리량 ─────┬─ 정확도 지표 ─────┬─ 비용 ─┐ │
│ │ 🟡 Gemini Flash    │ OCR: 94.2%       │ $0.00 │ │
│ │ ████████░░ 89%     │ Table: 91.7%     │ Free  │ │
│ │                   │ Summary: 96.1%   │       │ │
│ ├─────────────────── ├─────────────────── ├───────┤ │  
│ │ 🔵 GPT-4o Vision   │ OCR: 97.8%       │ $2.35 │ │
│ │ ████░░░░░░ 45%     │ Chart: 89.4%     │ Today │ │
│ │                   │ Image: 95.3%     │       │ │
│ ├─────────────────── ├─────────────────── ├───────┤ │
│ │ 🟣 Claude Sonnet   │ Document: 98.2%  │ $1.87 │ │  
│ │ ████████░░ 78%     │ Analysis: 94.6%  │ Today │ │
│ └───────────────────┴─────────────────── ┴───────┘ │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 📄 문서 분석 결과                                    │
│                                                     │
│ ┌─ 최근 처리된 문서 ───────────────────────────────┐ │
│ │ 📊 sales_report.xlsx    ✅ 테이블 5개 추출       │ │
│ │ 📄 contract_2025.pdf    ✅ 텍스트 + 이미지       │ │  
│ │ 📸 screenshot_001.png   ✅ OCR 완료             │ │
│ │ 📝 meeting_notes.docx   ⚡ 처리중...            │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─ 추출된 데이터 미리보기 ─────────────────────────┐ │  
│ │ Table 1: Sales Performance Q3 2025              │ │
│ │ ┌────────┬─────────┬─────────┬─────────────────┐ │ │
│ │ │ Month  │ Revenue │ Growth  │ Forecast        │ │ │
│ │ ├────────┼─────────┼─────────┼─────────────────┤ │ │  
│ │ │ Jul    │ $125K   │ +12.3%  │ $140K          │ │ │
│ │ │ Aug    │ $143K   │ +14.4%  │ $160K          │ │ │
│ │ │ Sep    │ $159K   │ +11.2%  │ $180K          │ │ │
│ │ └────────┴─────────┴─────────┴─────────────────┘ │ │
│ │                                                 │ │
│ │ [📊 차트 보기] [💾 CSV 내보내기] [🔗 원본 링크]  │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### 4. 📊 **데이터 관리 페이지**

#### **수집 데이터 브라우저**
```
┌─────────────────────────────────────────────────────┐
│ 💾 데이터 저장소                                     │
│                                                     │
│ ┌─ 필터 및 검색 ─────────────────────────────────┐   │
│ │ 🔍 [검색어 입력___________________] [🎯 필터]  │   │
│ │ 📅 날짜: [2025-08-01] ~ [2025-08-30]          │   │  
│ │ 🏷️ 태그: #sales #analytics #daily            │   │
│ │ 📁 형식: ☑️PDF ☑️XLSX ☑️HTML ☑️JSON ☑️이미지   │   │
│ └─────────────────────────────────────────────────┘   │
│                                                       │
│ ┌─ 데이터 목록 ─────────────────────────────────────┐ │  
│ │┌─┬────────────────┬─────────┬──────────┬─────────┐│ │
│ ││✓│ 파일명         │ 크기    │ 수집일시  │ 상태    ││ │
│ │├─┼────────────────┼─────────┼──────────┼─────────┤│ │
│ ││☐│📊 sales_q3.xlsx│ 2.3 MB  │08-30 14:22│✅ 분석됨││ │  
│ ││☐│📄 report.pdf   │ 856 KB  │08-30 13:15│✅ 분석됨││ │
│ ││☐│🌐 homepage.html│ 1.2 MB  │08-30 12:08│⚡ 처리중││ │
│ ││☐│📸 chart.png    │ 445 KB  │08-30 11:30│✅ OCR완료││ │
│ │└─┴────────────────┴─────────┴──────────┴─────────┘│ │
│ │                                                  │ │
│ │ [🎯 선택: 4개] [💾 다운로드] [🗑️ 삭제] [📊 분석] │ │  
│ └──────────────────────────────────────────────────┘ │
│                                                      │
│ ┌─ 저장소 통계 ─────────────────────────────────┐    │
│ │ 📁 전체 파일: 1,247개                        │    │
│ │ 💾 사용 공간: 12.4 GB / 100 GB (12%)         │    │  
│ │ 🔄 백업 상태: ✅ 최신 (2시간 전)              │    │
│ │ 🧹 정리 예정: 30일 이상 된 파일 156개         │    │
│ └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### 5. ⚙️ **시스템 설정 페이지**

#### **설정 관리 인터페이스**
```
┌─────────────────────────────────────────────────────┐
│ ⚙️ 시스템 설정                                       │
│                                                     │
│ ┌─ 🤖 AI 모델 설정 ────────────────────────────────┐ │
│ │                                                 │ │
│ │ Gemini API Key: [●●●●●●●●●●●●●●●●] [✅ 유효]      │ │  
│ │ OpenAI API Key: [●●●●●●●●●●●●●●●●] [✅ 유효]      │ │
│ │ Anthropic Key:  [●●●●●●●●●●●●●●●●] [✅ 유효]      │ │
│ │                                                 │ │
│ │ 모델 우선순위:                                   │ │  
│ │ 1순위: 🟡 Gemini Flash (무료)                   │ │
│ │ 2순위: 🔵 GPT-4o Vision (이미지 특화)           │ │
│ │ 3순위: 🟣 Claude Sonnet (문서 특화)             │ │
│ │                                                 │ │
│ │ [💾 저장] [🧪 연결 테스트] [🔄 초기화]           │ │  
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─ 🕷️ 크롤링 설정 ────────────────────────────────┐ │
│ │                                                 │ │
│ │ 기본 크롤링 전략: [AUTO ▼]                      │ │  
│ │ 동시 실행 수: [3] 작업                          │ │
│ │ 타임아웃: [30]초                                │ │
│ │ 재시도 횟수: [3]회                              │ │
│ │                                                 │ │  
│ │ User-Agent:                                     │ │
│ │ [Mozilla/5.0 (Windows NT 10.0; Win64; x64)...] │ │
│ │                                                 │ │
│ │ Rate Limiting:                                  │ │  
│ │ ☑️ 활성화 - 요청당 [1]초 간격                    │ │
│ │ ☑️ 로봇 배제 표준 준수                          │ │
│ │                                                 │ │
│ │ [💾 저장] [🔧 고급 설정] [📄 도움말]             │ │  
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─ 💾 저장소 설정 ────────────────────────────────┐ │
│ │                                                 │ │
│ │ 저장 경로: [/var/data/crawling] [📁]            │ │  
│ │ 최대 용량: [100] GB                             │ │
│ │ 자동 정리: [30]일 후 삭제                       │ │
│ │                                                 │ │
│ │ 백업 설정:                                      │ │  
│ │ ☑️ 자동 백업 활성화                             │ │
│ │ 빈도: [매일] 새벽 [2]시                         │ │
│ │ 보관 기간: [7]일                                │ │
│ │                                                 │ │
│ │ [💾 저장] [🗂️ 지금 백업] [🧹 정리 실행]          │ │  
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 **고급 기능 설계**

### 🔄 **실시간 업데이트 시스템**
```typescript
// WebSocket 이벤트 구조
interface RealtimeEvent {
  type: 'crawling_progress' | 'ai_analysis' | 'system_status';
  data: {
    jobId?: string;
    progress?: number;
    status?: 'running' | 'completed' | 'failed';
    metrics?: SystemMetrics;
    timestamp: number;
  };
}

// Server-Sent Events for status updates
const eventStream = new EventSource('/api/sse/status');
eventStream.onmessage = (event) => {
  const update = JSON.parse(event.data);
  updateDashboard(update);
};
```

### 📊 **차트 및 시각화**
```typescript
// Chart.js 설정 예시 
const performanceChart = {
  type: 'line',
  data: {
    labels: timeLabels,
    datasets: [{
      label: 'httpx',
      data: httpxData,
      borderColor: '#3b82f6',
      tension: 0.4
    }, {
      label: 'playwright', 
      data: playwrightData,
      borderColor: '#8b5cf6',
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: '크롤러 성능 비교' }
    },
    scales: {
      y: { beginAtZero: true, title: { display: true, text: '응답시간 (ms)' }}
    }
  }
};
```

### 🎨 **테마 시스템**
```typescript
// 테마 전환 시스템
interface Theme {
  name: 'light' | 'dark' | 'auto';
  colors: ColorPalette;
  spacing: SpacingScale;
  typography: TypographyScale;
}

const themeManager = {
  current: 'light',
  toggle: () => {
    document.documentElement.setAttribute('data-theme', 
      themeManager.current === 'light' ? 'dark' : 'light');
  },
  auto: () => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    themeManager.current = prefersDark.matches ? 'dark' : 'light';
  }
};
```

---

## 📱 **반응형 디자인**

### 📱 **모바일 최적화**
```scss
// 모바일 우선 접근법
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    position: fixed;
    z-index: 1000;
    
    &.open {
      transform: translateX(0);
    }
  }
  
  .main-content {
    padding: 1rem;
    
    .dashboard-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }
  }
  
  .chart-container {
    height: 200px; // 모바일에서 높이 축소
  }
}

// 태블릿 최적화
@media (min-width: 768px) and (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .sidebar {
    width: 200px;
  }
}
```

### ⚡ **성능 최적화**
```typescript
// 가상화된 테이블 (대용량 데이터)
import { FixedSizeList as List } from 'react-window';

const VirtualizedDataTable = ({ data, height = 400 }) => {
  const Row = ({ index, style }) => (
    <div style={style}>
      <DataRow data={data[index]} />
    </div>
  );
  
  return (
    <List
      height={height}
      itemCount={data.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </List>
  );
};

// 지연 로딩 컴포넌트
const LazyChart = lazy(() => import('./components/Chart'));
const ChartSection = () => (
  <Suspense fallback={<ChartSkeleton />}>
    <LazyChart />
  </Suspense>
);
```

---

## 🔐 **보안 및 인증**

### 🛡️ **API 키 보안**
```typescript
// 안전한 API 키 관리
class SecureKeyManager {
  private keys: Map<string, string> = new Map();
  
  setKey(service: string, key: string) {
    // 클라이언트에서는 마스킹된 버전만 표시
    const masked = key.slice(0, 4) + '●'.repeat(key.length - 8) + key.slice(-4);
    this.keys.set(service, masked);
    
    // 실제 키는 안전한 백엔드 저장소에 암호화 저장
    this.saveToSecureStorage(service, this.encrypt(key));
  }
  
  private encrypt(data: string): string {
    // AES 암호화 구현
    return CryptoJS.AES.encrypt(data, process.env.ENCRYPTION_KEY).toString();
  }
}
```

### 👤 **사용자 세션 관리**
```typescript
// JWT 기반 인증
interface UserSession {
  userId: string;
  role: 'admin' | 'operator' | 'viewer';
  permissions: string[];
  expiresAt: number;
}

const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET) as UserSession;
    req.user = payload;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Unauthorized' });
  }
};
```

---

## 🚀 **배포 및 운영**

### 🐳 **Docker 컨테이너화**
```dockerfile
# Frontend Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 📊 **모니터링 및 로깅**
```typescript
// 성능 모니터링
class PerformanceMonitor {
  trackPageLoad(pageName: string) {
    const start = performance.now();
    
    return () => {
      const loadTime = performance.now() - start;
      this.sendMetric('page_load_time', loadTime, { page: pageName });
    };
  }
  
  trackUserAction(action: string, metadata?: Record<string, any>) {
    this.sendMetric('user_action', 1, { action, ...metadata });
  }
  
  private sendMetric(name: string, value: number, labels: Record<string, any>) {
    // Prometheus/Grafana 연동
    fetch('/api/metrics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, value, labels, timestamp: Date.now() })
    });
  }
}
```

---

## 🎯 **다음 단계**

### 📋 **구현 우선순위**
1. **Phase 1**: 기본 레이아웃 및 메인 대시보드
2. **Phase 2**: 크롤링 관리 및 실시간 모니터링
3. **Phase 3**: AI 분석 결과 시각화
4. **Phase 4**: 데이터 관리 및 내보내기
5. **Phase 5**: 고급 설정 및 최적화

### 🔧 **기술 스택 확정**
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **UI Components**: shadcn/ui + Headless UI
- **Charts**: Chart.js + D3.js
- **State**: Zustand + React Query
- **Real-time**: Socket.io + Server-Sent Events

---

> **🎊 준비 완료!** 이제 실제 구현 단계로 넘어가겠습니다.