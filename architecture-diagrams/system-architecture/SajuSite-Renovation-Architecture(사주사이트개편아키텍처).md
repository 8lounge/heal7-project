# 🔮 사주사이트 개편 아키텍처 설계서

> **프로젝트**: HEAL7 사주사이트 전면 개편  
> **설계일**: 2025-08-18  
> **목표**: 모듈러 레고블럭 시스템 기반 확장성 극대화  
> **컨셉**: 운세+타로+12지신+별자리+풍수지리+사상체질+커뮤니티+스토어+매거진+1:1상담+체험후기

## 🎯 **핵심 설계 원칙**

### **1. 아파트 모듈러 공법 원칙**
- **기능별 독립 모듈**: 각 기능을 완전히 독립적인 패키지로 구성
- **레고블럭 조립**: 모듈간 표준 인터페이스로 자유로운 조합
- **플러그인 아키텍처**: 새로운 기능 추가 시 기존 코드 수정 없이 확장
- **핫스왑 가능**: 운영 중 특정 모듈만 업데이트 가능

### **2. 확장성 & 유지보수성**
- **마이크로프론트엔드**: 각 서비스별 독립 배포 가능
- **API 게이트웨이**: 통합 라우팅 및 인증 처리
- **컨테이너화**: Docker 기반 모듈별 격리 실행
- **CDN 분산**: 정적 리소스 최적화 배포

## 🏗️ **전체 시스템 아키텍처**

### **🔵 프론트엔드 레이어 (React 19 + Vite)**

```
🌐 사주사이트 메인 플랫폼
├── 🏠 메인 허브 (Main Hub)
│   ├── 🎯 개인화 대시보드
│   ├── 🔮 오늘의 운세 요약
│   └── 📱 빠른 서비스 접근
│
├── 🔮 코어 운세 서비스 (Core Fortune Services)
│   ├── 📊 사주명리학 (기존 로직 활용)
│   ├── 🃏 타로카드 리딩
│   ├── 🐲 12지신 운세
│   ├── ⭐ 별자리 운세
│   ├── 🏔️ 풍수지리 분석
│   └── 🌿 사상체질 진단
│
├── 💬 소셜 & 커뮤니티 (Social & Community)
│   ├── 👥 커뮤니티 게시판
│   ├── 💭 운세 공유
│   ├── ⭐ 체험후기
│   └── 🤝 1:1 상담 매칭
│
├── 🛒 커머스 & 서비스 (Commerce & Services)
│   ├── 🛍️ 스토어 (부적, 굿즈, 전자책)
│   ├── 📚 매거진 (프리미엄 콘텐츠)
│   ├── 💳 구독 서비스
│   └── 💰 충전 시스템
│
└── 👤 사용자 & 관리 (User & Management)
    ├── 🔐 회원 관리
    ├── 📈 이용내역
    ├── ⚙️ 개인설정
    └── 🛠️ 관리자 대시보드
```

### **🔴 백엔드 레이어 (FastAPI + 마이크로서비스)**

```
🚀 API 게이트웨이 & 마이크로서비스
├── 🌐 API Gateway (Kong/Traefik)
│   ├── 🔐 통합 인증 (JWT + OAuth2)
│   ├── 🚦 라우팅 & 로드밸런싱
│   ├── 📊 API 모니터링
│   └── 🛡️ 보안 & Rate Limiting
│
├── 🔮 운세 서비스 클러스터
│   ├── 📊 사주명리 서비스 (포트 8100)
│   ├── 🃏 타로 서비스 (포트 8101)
│   ├── 🐲 12지신 서비스 (포트 8102)
│   ├── ⭐ 별자리 서비스 (포트 8103)
│   ├── 🏔️ 풍수지리 서비스 (포트 8104)
│   └── 🌿 사상체질 서비스 (포트 8105)
│
├── 💬 커뮤니티 서비스 클러스터
│   ├── 👥 게시판 서비스 (포트 8200)
│   ├── 💭 댓글 서비스 (포트 8201)
│   ├── ⭐ 평가 서비스 (포트 8202)
│   └── 🤝 매칭 서비스 (포트 8203)
│
├── 🛒 커머스 서비스 클러스터
│   ├── 🛍️ 스토어 서비스 (포트 8300)
│   ├── 💳 결제 서비스 (포트 8301)
│   ├── 📦 주문 서비스 (포트 8302)
│   └── 📚 콘텐츠 서비스 (포트 8303)
│
├── 🎯 개인화 & 분석 서비스
│   ├── 🤖 AI 추천 엔진 (포트 8400)
│   ├── 📊 분석 서비스 (포트 8401)
│   ├── 📈 통계 서비스 (포트 8402)
│   └── 🔔 알림 서비스 (포트 8403)
│
└── 🏗️ 공통 인프라 서비스
    ├── 👤 사용자 관리 (포트 8500)
    ├── 📁 파일 관리 (포트 8501)
    ├── 📧 이메일 서비스 (포트 8502)
    └── 💰 포인트 관리 (포트 8503)
```

### **🟡 데이터 레이어 (하이브리드 DB 아키텍처)**

```
🗃️ 하이브리드 데이터베이스 생태계
├── 📊 PostgreSQL 클러스터 (주 데이터베이스)
│   ├── 👤 사용자 DB (users, profiles, preferences)
│   ├── 🔮 운세결과 DB (saju_results, interpretations)
│   ├── 💬 커뮤니티 DB (posts, comments, reviews)
│   ├── 🛒 커머스 DB (products, orders, payments)
│   └── 📊 분석 DB (analytics, logs, statistics)
│
├── ⚡ Redis 클러스터 (캐시 & 세션)
│   ├── 🔥 핫데이터 캐시 (운세결과, 추천)
│   ├── 🎯 사용자 세션 (JWT, 임시데이터)
│   ├── 📊 실시간 통계 (접속자, 인기콘텐츠)
│   └── 🔔 실시간 알림 큐
│
├── 📁 MongoDB (비정형 데이터)
│   ├── 🤖 AI 학습데이터 (해석패턴, 피드백)
│   ├── 📚 콘텐츠 메타데이터 (매거진, 아티클)
│   ├── 🔍 검색 인덱스 (ElasticSearch 연동)
│   └── 📊 로그 데이터 (사용자 행동, 에러로그)
│
└── ☁️ 클라우드 스토리지
    ├── 🖼️ 미디어 파일 (이미지, 동영상)
    ├── 📄 문서 파일 (PDF, eBook)
    ├── 💾 백업 데이터
    └── 📊 빅데이터 아카이브
```

## 🧩 **모듈러 컴포넌트 시스템**

### **1. 프론트엔드 모듈 패키지**

#### **🎨 UI 컴포넌트 레고블럭**
```typescript
📦 @heal7/ui-components
├── 🎭 layouts/
│   ├── MainLayout.tsx
│   ├── MobileLayout.tsx
│   ├── DashboardLayout.tsx
│   └── ServiceLayout.tsx
│
├── 🎯 widgets/
│   ├── FortuneCard.tsx
│   ├── UserProfile.tsx
│   ├── PaymentModal.tsx
│   └── NotificationCenter.tsx
│
├── 📊 charts/
│   ├── SajuChart.tsx
│   ├── StatisticsChart.tsx
│   ├── TrendChart.tsx
│   └── InteractiveWheel.tsx
│
└── 🎮 interactive/
    ├── TarotCardDeck.tsx
    ├── ZodiacWheel.tsx
    ├── ElementSelector.tsx
    └── PersonalityTest.tsx
```

#### **🔮 운세 서비스 모듈**
```typescript
📦 @heal7/fortune-services
├── 📊 saju/
│   ├── SajuCalculator.ts
│   ├── SajuRenderer.tsx
│   ├── SajuTypes.ts
│   └── SajuAPI.ts
│
├── 🃏 tarot/
│   ├── TarotEngine.ts
│   ├── TarotDeck.tsx
│   ├── TarotReader.tsx
│   └── TarotAPI.ts
│
├── 🐲 zodiac/
│   ├── ZodiacCalculator.ts
│   ├── ZodiacDisplay.tsx
│   ├── ZodiacTypes.ts
│   └── ZodiacAPI.ts
│
└── 🌟 common/
    ├── FortuneBase.ts
    ├── ResultRenderer.tsx
    ├── ShareComponents.tsx
    └── FortuneAPI.ts
```

#### **💬 커뮤니티 모듈**
```typescript
📦 @heal7/community
├── 📝 board/
│   ├── PostEditor.tsx
│   ├── PostList.tsx
│   ├── PostDetail.tsx
│   └── BoardAPI.ts
│
├── 💭 comments/
│   ├── CommentTree.tsx
│   ├── CommentEditor.tsx
│   ├── CommentAPI.ts
│   └── CommentTypes.ts
│
├── ⭐ reviews/
│   ├── ReviewForm.tsx
│   ├── ReviewList.tsx
│   ├── RatingSystem.tsx
│   └── ReviewAPI.ts
│
└── 🤝 matching/
    ├── ConsultantList.tsx
    ├── BookingCalendar.tsx
    ├── ChatInterface.tsx
    └── MatchingAPI.ts
```

### **2. 백엔드 모듈 패키지**

#### **🚀 FastAPI 서비스 모듈**
```python
📦 heal7_core_services/
├── 🔮 fortune_services/
│   ├── saju_service.py
│   ├── tarot_service.py
│   ├── zodiac_service.py
│   ├── base_fortune.py
│   └── fortune_router.py
│
├── 💬 community_services/
│   ├── board_service.py
│   ├── comment_service.py
│   ├── review_service.py
│   ├── matching_service.py
│   └── community_router.py
│
├── 🛒 commerce_services/
│   ├── store_service.py
│   ├── payment_service.py
│   ├── order_service.py
│   ├── content_service.py
│   └── commerce_router.py
│
└── 🏗️ infrastructure/
    ├── database.py
    ├── cache.py
    ├── auth.py
    ├── monitoring.py
    └── config.py
```

### **3. 데이터베이스 모듈**

#### **📊 PostgreSQL 스키마 모듈**
```sql
-- 📦 heal7_database_schemas
├── 👤 user_management/
│   ├── users.sql
│   ├── profiles.sql
│   ├── preferences.sql
│   └── auth_tokens.sql
│
├── 🔮 fortune_data/
│   ├── saju_results.sql
│   ├── tarot_readings.sql
│   ├── interpretations.sql
│   └── fortune_history.sql
│
├── 💬 community_data/
│   ├── boards.sql
│   ├── posts.sql
│   ├── comments.sql
│   └── reviews.sql
│
└── 🛒 commerce_data/
    ├── products.sql
    ├── orders.sql
    ├── payments.sql
    └── subscriptions.sql
```

## 🎨 **디자인 시스템 아키텍처**

### **1. 테마 시스템**
```scss
🎭 Mystic Design System v2.0
├── 🌌 cosmic-theme/
│   ├── colors.scss      # 우주적 컬러 팔레트
│   ├── typography.scss  # 신비로운 폰트 시스템
│   ├── spacing.scss     # 황금비율 기반 spacing
│   └── animations.scss  # 별자리 애니메이션
│
├── 🔮 fortune-theme/
│   ├── saju-colors.scss
│   ├── tarot-colors.scss
│   ├── zodiac-colors.scss
│   └── element-colors.scss
│
└── 📱 responsive/
    ├── mobile.scss
    ├── tablet.scss
    ├── desktop.scss
    └── ultra-wide.scss
```

### **2. 컴포넌트 디자인 토큰**
```typescript
// 🎨 Design Tokens
export const DesignTokens = {
  colors: {
    primary: {
      cosmic: '#6366F1',     // 인디고 (지혜)
      mystic: '#8B5CF6',     // 바이올렛 (신비)
      fortune: '#EC4899',    // 핑크 (운명)
      energy: '#06B6D4'      // 사이안 (에너지)
    },
    fortune: {
      fire: '#EF4444',       // 화(火) - 빨강
      earth: '#F59E0B',      // 토(土) - 노랑  
      metal: '#6B7280',      // 금(金) - 회색
      water: '#3B82F6',      // 수(水) - 파랑
      wood: '#10B981'        // 목(木) - 초록
    }
  },
  typography: {
    headers: 'Noto Sans KR',
    body: 'Pretendard',
    accent: 'Gmarket Sans'
  },
  animations: {
    cosmic: 'twinkle 2s infinite',
    fortune: 'glow 1.5s ease-in-out infinite alternate',
    element: 'rotate 3s linear infinite'
  }
}
```

## 💳 **구독 & 충전 서비스 아키텍처**

### **1. 결제 시스템 모듈**
```typescript
📦 @heal7/payment-system
├── 💳 payment-gateway/
│   ├── KakaoPayProvider.ts
│   ├── NaverPayProvider.ts
│   ├── TossPayProvider.ts
│   └── PaymentManager.ts
│
├── 💰 subscription/
│   ├── SubscriptionManager.ts
│   ├── PlanManager.ts
│   ├── BillingCycle.ts
│   └── SubscriptionAPI.ts
│
├── 🎯 points/
│   ├── PointManager.ts
│   ├── PointHistory.ts
│   ├── RewardSystem.ts
│   └── PointAPI.ts
│
└── 🏪 store/
    ├── ProductManager.ts
    ├── CartManager.ts
    ├── OrderManager.ts
    └── StoreAPI.ts
```

### **2. 구독 플랜 구조**
```yaml
# 💎 구독 플랜 정의
subscription_plans:
  basic:
    name: "기본 운세"
    price: 9900
    features:
      - "월 10회 사주 분석"
      - "기본 타로 리딩"
      - "커뮤니티 참여"
    
  premium:
    name: "프리미엄 운세"
    price: 19900
    features:
      - "무제한 사주 분석"
      - "프리미엄 타로 + 12지신"
      - "1:1 상담 월 2회"
      - "매거진 전체 접근"
    
  master:
    name: "마스터 운세"
    price: 39900
    features:
      - "모든 서비스 무제한"
      - "전문가 1:1 상담 무제한"
      - "개인 맞춤 리포트"
      - "우선 고객지원"
```

## 🔧 **개발 & 운영 도구**

### **1. 개발 환경**
```yaml
# 🛠️ Development Stack
frontend:
  framework: "React 19 + Vite"
  styling: "Tailwind CSS + SCSS"
  state: "Zustand + React Query"
  testing: "Vitest + Testing Library"
  
backend:
  framework: "FastAPI + SQLAlchemy"
  database: "PostgreSQL + Redis + MongoDB"
  cache: "Redis Cluster"
  queue: "Celery + Redis"
  
infrastructure:
  containerization: "Docker + Docker Compose"
  orchestration: "Kubernetes (optional)"
  monitoring: "Prometheus + Grafana"
  logging: "ELK Stack"
```

### **2. 배포 & 모니터링**
```yaml
# 🚀 Deployment & Monitoring
deployment:
  strategy: "Blue-Green with Canary"
  automation: "GitHub Actions + ArgoCD"
  environments: ["dev", "staging", "prod"]
  
monitoring:
  performance: "New Relic + Sentry"
  uptime: "Pingdom + StatusPage"
  analytics: "Google Analytics + Mixpanel"
  
security:
  ssl: "Let's Encrypt + Cloudflare"
  auth: "Auth0 + JWT"
  api: "Kong Gateway + Rate Limiting"
```

## 📈 **확장 로드맵**

### **1단계: 핵심 기능 구현** (1-2개월)
- ✅ 기존 사주 시스템 모듈화
- 🔄 타로카드 서비스 추가
- 🎯 기본 UI/UX 컴포넌트 완성
- 💳 기본 결제 시스템 구축

### **2단계: 커뮤니티 & 서비스** (2-3개월)
- 👥 커뮤니티 플랫폼 구축
- 🛒 스토어 & 구독 서비스 완성
- 📚 매거진 콘텐츠 시스템
- 🤝 1:1 상담 매칭 시스템

### **3단계: AI & 개인화** (3-4개월)
- 🤖 AI 추천 엔진 고도화
- 🎯 개인화 대시보드 완성
- 📊 고급 분석 도구 추가
- 🌟 별자리 + 풍수지리 + 사상체질 확장

### **4단계: 고도화 & 최적화** (4-6개월)
- ⚡ 성능 최적화 및 CDN 적용
- 📱 모바일 앱 개발 (React Native)
- 🌐 다국어 지원 (일본, 중국)
- 🎮 게이미피케이션 요소 추가

---

*📅 설계 완료일: 2025-08-18*  
*🏗️ 설계자: HEAL7 AI Architecture Team*  
*📝 문서 위치: `/home/ubuntu/CORE/architecture-diagrams/system-architecture/`*