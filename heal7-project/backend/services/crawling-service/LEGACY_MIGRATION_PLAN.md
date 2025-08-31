# 🔄 크롤링 대시보드 레거시 마이그레이션 계획서

> **프로젝트**: crawling.heal7.com 완전 교체  
> **마이그레이션 유형**: Big Bang Replacement  
> **예상 소요시간**: 2-3시간  
> **최종 업데이트**: 2025-08-30 17:26  

---

## 📋 **마이그레이션 개요**

### 🎯 **목표**
- 1585줄 단일 HTML 레거시 시스템 → 모던 React 대시보드로 완전 교체
- 3-Tier 크롤링 시스템과 완전 통합
- 실시간 모니터링 및 AI 분석 기능 강화
- 성능과 확장성 향상

### 🔍 **현재 시스템 분석** ✅

#### **레거시 시스템 특징**
```
파일: /var/www/crawling.heal7.com/index.html (1,585줄)
기술스택:
- Alpine.js (클라이언트사이드 프레임워크)
- Tailwind CSS (유틸리티 CSS)
- 생체모방공학 기반 HEAL7 8-Color 시스템
- Chart.js (차트 라이브러리)
- Sortable.js (드래그앤드롭)

주요 기능:
✅ 크롤링 대시보드 (꿈풀이, 정부포털 엔진)
✅ Paperwork 관리 통합
✅ 큐브 아키텍처 시스템 연동
✅ 데이터 분석 및 시각화
✅ 시스템 관리 및 모니터링
✅ 실시간 로그 스트림
✅ 드래그앤드롭 위젯
✅ 반응형 디자인 (모바일 최적화)
```

### 🛡️ **백업 완료** ✅
```bash
백업 위치: /var/www/crawling.heal7.com.legacy-backup-20250830-172638/
백업 시각: 2025-08-30 17:26:38
백업 크기: 1585줄 HTML + 기타 에셋
상태: ✅ 안전하게 백업 완료
```

---

## 🏗️ **새 시스템 아키텍처**

### 🎨 **기술 스택**
```typescript
Frontend Stack:
├── React 18 + TypeScript          // 컴포넌트 기반 UI
├── Tailwind CSS + shadcn/ui       // 스타일링 + UI 컴포넌트
├── Zustand                        // 상태 관리
├── React Query (TanStack Query)   // 서버 상태 관리
├── Chart.js / D3.js               // 데이터 시각화
├── Socket.io Client              // 실시간 통신
└── Framer Motion                 // 애니메이션

Backend Integration:
├── FastAPI (Python)              // 백엔드 API 서버
├── 3-Tier Crawler System         // httpx + Playwright + Selenium
├── Multimodal AI Analysis        // Gemini + GPT-4o + Claude
├── WebSocket Server              // 실시간 업데이트
└── PostgreSQL + Redis            // 데이터 저장 + 캐시
```

### 📐 **컴포넌트 구조**
```
src/
├── components/
│   ├── ui/                       // shadcn/ui 기본 컴포넌트
│   ├── layout/
│   │   ├── Header.tsx            // 상단 네비게이션
│   │   ├── Sidebar.tsx           // 사이드바 메뉴
│   │   └── Layout.tsx            // 전체 레이아웃
│   ├── dashboard/
│   │   ├── Overview.tsx          // 메인 대시보드
│   │   ├── SystemMetrics.tsx     // 시스템 지표
│   │   ├── CrawlingStatus.tsx    // 크롤링 현황
│   │   └── RealTimeLogs.tsx      // 실시간 로그
│   ├── crawling/
│   │   ├── CrawlerManager.tsx    // 크롤러 관리
│   │   ├── JobCreator.tsx        // 작업 생성 마법사
│   │   ├── JobMonitor.tsx        // 작업 모니터링
│   │   └── TierSelector.tsx      // 3-Tier 선택기
│   ├── ai-analysis/
│   │   ├── AIResults.tsx         // AI 분석 결과
│   │   ├── DocumentViewer.tsx    // 문서 뷰어
│   │   ├── TableExtractor.tsx    // 테이블 추출
│   │   └── ModelComparison.tsx   // 모델 비교
│   ├── data-management/
│   │   ├── DataBrowser.tsx       // 데이터 브라우저
│   │   ├── ExportManager.tsx     // 내보내기 관리
│   │   └── SearchFilter.tsx      // 검색 필터
│   └── settings/
│       ├── SystemSettings.tsx    // 시스템 설정
│       ├── APIKeyManager.tsx     // API 키 관리
│       └── CrawlerConfig.tsx     // 크롤러 설정
├── pages/
│   ├── Dashboard.tsx             // 메인 대시보드
│   ├── CrawlingManagement.tsx    // 크롤링 관리
│   ├── AIAnalysis.tsx           // AI 분석
│   ├── DataManagement.tsx       // 데이터 관리
│   └── Settings.tsx             // 설정
├── hooks/
│   ├── useCrawler.ts            // 크롤러 관련 훅
│   ├── useWebSocket.ts          // WebSocket 통신
│   ├── useAIAnalysis.ts         // AI 분석 훅
│   └── useRealTime.ts           // 실시간 업데이트
├── stores/
│   ├── crawlerStore.ts          // 크롤러 상태
│   ├── uiStore.ts              // UI 상태
│   └── settingsStore.ts         // 설정 상태
└── types/
    ├── crawler.types.ts         // 크롤러 타입 정의
    ├── ai.types.ts             // AI 분석 타입
    └── api.types.ts            // API 타입 정의
```

---

## 🚀 **마이그레이션 단계**

### **Phase 1: 프로젝트 초기화** ⏳
```bash
1. Next.js 프로젝트 생성
2. 필수 종속성 설치
3. 기본 프로젝트 구조 설정
4. Tailwind CSS + shadcn/ui 설정
5. TypeScript 설정 최적화
```

### **Phase 2: 기본 레이아웃** ⏳
```typescript
1. 헤더 컴포넌트 (네비게이션, 상태 표시)
2. 사이드바 컴포넌트 (메뉴, 접기/펴기)
3. 메인 레이아웃 컴포넌트
4. 반응형 디자인 구현
5. 테마 시스템 (라이트/다크 모드)
```

### **Phase 3: 메인 대시보드** ⏳
```typescript
1. 시스템 개요 위젯
2. 실시간 성능 지표
3. 크롤링 작업 현황 테이블
4. AI 분석 요약
5. 빠른 액션 버튼
```

### **Phase 4: 크롤링 관리** ⏳
```typescript
1. 3-Tier 크롤러 제어 패널
2. 작업 생성 마법사 (다단계 폼)
3. 실시간 작업 모니터링
4. 배치 크롤링 관리
5. 성능 비교 차트
```

### **Phase 5: AI 분석 시각화** ⏳
```typescript
1. 멀티모달 분석 결과 표시
2. 문서 처리 현황
3. OCR 결과 뷰어
4. 테이블 추출 시각화
5. 모델별 성능 비교
```

### **Phase 6: 데이터 관리** ⏳
```typescript
1. 수집된 데이터 브라우저
2. 고급 검색 및 필터링
3. 대용량 데이터 가상화
4. 내보내기 기능 (CSV, JSON, Excel)
5. 데이터 품질 분석
```

### **Phase 7: 실시간 기능** ⏳
```typescript
1. WebSocket 연결 관리
2. 실시간 로그 스트리밍
3. 진행률 업데이트
4. 시스템 알림
5. 자동 새로고침
```

### **Phase 8: 시스템 교체** ⏳
```bash
1. 새 시스템 최종 테스트
2. 레거시 시스템 중단
3. 새 시스템 배포
4. DNS/프록시 설정 업데이트
5. 롤백 계획 준비
```

---

## 📊 **기능 매핑표**

| 레거시 기능 | 새 시스템 컴포넌트 | 상태 | 개선사항 |
|-------------|-------------------|------|----------|
| Alpine.js 상태 관리 | Zustand Store | ⏳ | TypeScript 타입 안전성 |
| 크롤링 엔진 제어 | CrawlerManager | ⏳ | 3-Tier 시스템 통합 |
| 실시간 로그 | RealTimeLogs + WebSocket | ⏳ | 성능 최적화 |
| 드래그앤드롭 위젯 | React DnD | ⏳ | 더 나은 UX |
| 시스템 리소스 모니터링 | SystemMetrics | ⏳ | 실제 시스템 연동 |
| Paperwork 통합 | 별도 탭으로 이동 | ⏳ | 독립적 관리 |
| 차트 시각화 | Chart.js + D3.js | ⏳ | 고급 인터랙션 |
| 토스트 알림 | React Hot Toast | ⏳ | 더 나은 애니메이션 |
| 반응형 디자인 | Tailwind Responsive | ⏳ | 모바일 퍼스트 |

---

## ⚠️ **마이그레이션 위험 요소**

### 🔥 **고위험**
- **서비스 중단 시간**: Big Bang 방식으로 인한 일시적 서비스 중단
- **데이터 호환성**: 기존 설정 및 데이터 포맷 호환성 문제
- **API 연동**: 3-Tier 크롤러와의 API 연동 이슈

### ⚠️ **중위험**  
- **브라우저 호환성**: 최신 React 기능 사용으로 인한 구형 브라우저 이슈
- **성능 저하**: 초기 번들 크기 증가로 인한 로딩 속도 저하
- **사용자 적응**: 새로운 UI/UX에 대한 사용자 적응 기간

### 💚 **저위험**
- **디자인 일관성**: 기존 HEAL7 8-Color 시스템 유지 계획
- **기능 누락**: 기존 기능 완전 이식 예정
- **롤백 계획**: 안전한 백업 시스템 구축 완료

---

## 🛠️ **개발 환경 설정**

### 📦 **필수 종속성**
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "@radix-ui/react-*": "^1.0.0",
    "tailwindcss": "^3.3.0",
    "zustand": "^4.4.0",
    "@tanstack/react-query": "^5.0.0",
    "chart.js": "^4.4.0",
    "socket.io-client": "^4.7.0",
    "framer-motion": "^10.0.0",
    "react-hot-toast": "^2.4.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### 🔧 **개발 도구**
```bash
# 개발 서버 포트
Frontend: http://localhost:3000
Backend API: http://localhost:8003 (3-Tier Crawler)

# 빌드 도구
Build: Next.js (최적화된 프로덕션 빌드)
Bundle Analyzer: 번들 크기 분석
Lighthouse: 성능 측정

# 배포 환경
Target: /var/www/crawling.heal7.com/
Server: Nginx (리버스 프록시)
SSL: Let's Encrypt
```

---

## 📅 **타임라인**

### 🎯 **Phase 별 예상 소요시간**
```
Phase 1 (프로젝트 초기화):    30분
Phase 2 (기본 레이아웃):      45분  
Phase 3 (메인 대시보드):      60분
Phase 4 (크롤링 관리):        45분
Phase 5 (AI 분석):           30분
Phase 6 (데이터 관리):        30분
Phase 7 (실시간 기능):        30분
Phase 8 (시스템 교체):        30분
──────────────────────────────────
총 예상 시간:                 5시간
```

### 📊 **진행률 추적**
- **현재 진행률**: 15% (분석 및 설계 완료)
- **다음 단계**: Phase 1 프로젝트 초기화
- **완료 목표**: 2025-08-30 22:00

---

## ✅ **성공 기준**

### 🎯 **기능적 요구사항**
- [ ] 모든 기존 기능 완전 이식
- [ ] 3-Tier 크롤링 시스템 완전 통합
- [ ] 실시간 모니터링 정상 작동
- [ ] AI 분석 결과 시각화
- [ ] 반응형 디자인 (모바일 지원)

### ⚡ **비기능적 요구사항**
- [ ] 페이지 로딩 속도 < 2초
- [ ] Lighthouse 성능 점수 > 90
- [ ] TypeScript 타입 커버리지 > 95%
- [ ] 브라우저 호환성 (Chrome, Firefox, Safari, Edge)
- [ ] 접근성 준수 (WCAG 2.1 AA)

### 🛡️ **안정성 요구사항**
- [ ] 99.9% 업타임
- [ ] 에러 경계 처리
- [ ] 우아한 실패 처리
- [ ] 롤백 계획 실행 가능

---

**🚀 준비 완료!** 이제 Phase 1부터 체계적으로 진행하겠습니다.