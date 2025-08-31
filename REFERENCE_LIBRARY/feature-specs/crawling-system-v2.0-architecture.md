# 🔍 HEAL7 크롤링 시스템 v2.0 - 완전 설계 문서

> **프로젝트**: HEAL7 3-Tier 크롤링 대시보드  
> **버전**: 2.0.0 (React 18 기반 완전 재설계)  
> **작성일**: 2025-08-31  
> **상태**: ✅ 프로덕션 배포 완료

## 🎯 시스템 개요

### 핵심 미션
고급 3-Tier 크롤링 시스템과 멀티모달 AI 분석을 통한 데이터 수집 플랫폼

### 주요 특징
- **3-Tier 크롤러**: httpx, Playwright, Selenium 통합 지원
- **멀티모달 AI**: Gemini Flash, GPT-4o, Claude Sonnet 활용
- **실시간 모니터링**: WebSocket 기반 라이브 업데이트
- **글래스모피즘 UI**: 현대적인 반투명 디자인
- **드래그 앤 드롭**: 직관적인 작업 관리
- **PWA 지원**: Service Worker 기반 오프라인 기능

## 🏗️ 아키텍처 구조

### 📁 컴포넌트 계층구조
```
CrawlingApp (루트)
├── CrawlingLayout (메인 레이아웃)
│   ├── CrawlingHeader (상단 헤더 + 시스템 메트릭)
│   ├── CrawlingSidebar (네비게이션 + 3-Tier 상태)
│   ├── main content area
│   │   ├── CrawlingDashboard (메인 대시보드)
│   │   ├── CrawlingManagement (작업 관리)
│   │   ├── AIAnalysis (AI 분석 패널)
│   │   └── DataManagement (데이터 관리)
│   ├── RealTimeLogs (실시간 로그 패널)
│   └── SystemAlerts (시스템 알림)
└── useRealTime hook (실시간 기능)
```

### 🧩 핵심 컴포넌트 상세

#### 1. **CrawlingApp.tsx** (엔트리 포인트)
```typescript
// 크롤링 시스템 전용 앱
function CrawlingApp() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900/50 to-slate-900">
      <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-blue-900/40 to-black/70" />
      <div className="relative z-10">
        <CrawlingDashboard />
      </div>
    </div>
  )
}
```

#### 2. **CrawlingLayout.tsx** (레이아웃 매니저)
- **역할**: 전체 레이아웃 관리, 실시간 데이터 통합
- **기능**: 
  - 사이드바 토글 (w-16 ↔ w-64)
  - 실시간 로그 패널 토글
  - 시스템 알림 패널 관리
  - 키보드 단축키 (Ctrl+1~5)
- **상태 관리**: useRealTime 훅 통합

#### 3. **CrawlingHeader.tsx** (시스템 상태 헤더)
- **표시 정보**:
  - 크롤러 상태 (활성/대기/오류)
  - 활성 작업 수
  - 수집 데이터 건수
  - 시스템 부하율
- **UI 패턴**: 글래스 효과, 상태별 색상 코딩

#### 4. **CrawlingSidebar.tsx** (네비게이션)
- **메뉴 구조**:
  - 대시보드 (BarChart3 아이콘)
  - 크롤링 관리 (Activity 아이콘) 
  - AI 분석 (Brain 아이콘)
  - 데이터 관리 (Database 아이콘)
  - 설정 (Settings 아이콘)
- **3-Tier 상태 표시**:
  - httpx: 빠른 수집 (활성 12개)
  - playwright: 동적 페이지 (대기 5개)  
  - selenium: 복잡한 SPA (오류 2개)

#### 5. **CrawlingManagement.tsx** (작업 관리)
- **작업 유형**:
  - 정부포털 일반공고 (httpx)
  - 꿈해몽 데이터베이스 (playwright)
  - 사주명리 포털 (selenium)
  - 운세 정보 수집 (httpx)
- **제어 기능**: 시작/일시정지/중지, 스케줄링, 진행률 모니터링

#### 6. **AIAnalysis.tsx** (AI 분석 패널)
- **지원 AI 모델**:
  - Gemini Flash: 1247건 처리, 96.8% 성공률, $1.25 비용
  - GPT-4o: 856건 처리, 94.2% 성공률, $4.28 비용
  - Claude Sonnet: 523건 처리, 97.1% 성공률, $1.57 비용
- **처리 타입**: document, table, image, OCR

#### 7. **useRealTime.ts** (실시간 기능 훅)
- **기능**: WebSocket 연결, 시스템 메트릭, 로그 스트리밍, 알림 관리
- **설정 옵션**: 로그 버퍼 크기, 업데이트 간격, 기능별 활성화

## 🎨 디자인 시스템

### 색상 팔레트
```css
Primary: slate-900, blue-900
Background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%)
Glass Effect: rgba(15, 23, 42, 0.3) + backdrop-blur(16px)
Status Colors:
  - Success: green-400 (활성)
  - Warning: blue-400 (대기)  
  - Error: red-400 (오류)
  - Text: slate-300, white
```

### 타이포그래피
- **주 폰트**: Pretendard (한글 최적화)
- **코드 폰트**: JetBrains Mono
- **크기**: text-sm (14px) ~ text-xl (20px)
- **굵기**: font-medium, font-bold

### 애니메이션 패턴
- **Framer Motion**: 페이지 전환, 호버 효과
- **진입 애니메이션**: opacity 0→1, y: 20→0
- **종료 애니메이션**: opacity 1→0, y: 0→-20
- **지속시간**: 0.3~0.5초

## 🛠️ 기술 스택

### Frontend Stack
```json
{
  "framework": "React 18 + TypeScript",
  "animation": "Framer Motion",
  "icons": "Lucide React",
  "styling": "Tailwind CSS + shadcn/ui",
  "drag-drop": "@dnd-kit/core",
  "state": "React Query + useState",
  "realtime": "Custom useRealTime hook"
}
```

### Backend Integration
```yaml
API Base: /api/
WebSocket: /ws
Health Check: /health
Docs: /docs (FastAPI 자동 생성)
```

## 📊 데이터 플로우

### 실시간 데이터 흐름
```
FastAPI Backend (포트 8003)
    ↓ WebSocket
useRealTime Hook
    ↓ 상태 업데이트
CrawlingLayout
    ↓ props drilling
├── CrawlingHeader (메트릭 표시)
├── CrawlingSidebar (3-Tier 상태)
└── 각 페이지 컴포넌트
```

### API 엔드포인트 구조
```
/api/health - 시스템 헬스체크
/api/crawling/ - 크롤링 작업 관리
/api/ai/ - AI 분석 요청
/api/data/ - 수집 데이터 관리
/ws - WebSocket 실시간 연결
```

## 🔧 재현 가능한 구현 가이드

### 1단계: 프로젝트 설정
```bash
npx create-react-app crawling-dashboard --template typescript
cd crawling-dashboard
npm install framer-motion @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
npm install lucide-react @tanstack/react-query
npm install tailwindcss @types/react @types/react-dom
```

### 2단계: 컴포넌트 구조 생성
```bash
mkdir -p src/components/crawling
mkdir -p src/hooks
# 각 컴포넌트 파일 생성 (위 구조 참조)
```

### 3단계: 핵심 훅 구현
```typescript
// useRealTime.ts - 실시간 기능의 핵심
export const useRealTime = (options) => {
  // WebSocket 연결
  // 시스템 메트릭 관리  
  // 로그 스트리밍
  // 알림 시스템
}
```

### 4단계: 디자인 시스템 적용
```css
/* Tailwind + 글래스 효과 */
.glass-effect {
  backdrop-filter: blur(16px);
  background: rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(148, 163, 184, 0.2);
}
```

## 🎮 사용자 경험 (UX)

### 인터랙션 패턴
1. **사이드바 토글**: 좁은 화면에서 자동 축소
2. **실시간 업데이트**: 2초 간격 자동 갱신  
3. **키보드 단축키**: Ctrl+숫자로 페이지 전환
4. **드래그 앤 드롭**: 작업 우선순위 변경
5. **상태 표시**: 색상 코딩으로 직관적 인식

### 성능 최적화
- **React Query**: 15분 캐시, 자동 재요청 방지
- **Lazy Loading**: 3D 컴포넌트 분리 로딩
- **Code Splitting**: 청크별 로딩
- **Service Worker**: PWA 캐싱

## 📈 확장성 고려사항

### 모듈화 설계
- 각 크롤링 티어별 독립적 컴포넌트
- AI 모델별 플러그인 구조
- 알림/로그 시스템 분리
- API 클라이언트 추상화

### 향후 확장 포인트
- 새로운 크롤링 엔진 추가
- AI 모델 교체/추가
- 사용자 권한 시스템
- 대시보드 위젯 커스터마이징

---

**🏆 성공 지표**: 직관적 UI, 실시간 반응성, 안정적인 3-Tier 통합  
**🎨 디자인 철학**: 기능성과 미학의 조화, 글래스모피즘의 현대적 적용

*이 문서로 동일한 크롤링 시스템 완전 재현 가능*