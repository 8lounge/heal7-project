# 🗄️ HEAL7 실제 DB 기반 Core 아키텍처

> **현실 기반 접근**: 운영 중인 실제 DB 구조를 안전하게 개선

## 📊 **실제 DB 현황** (2025-08-30 분석)

**총 8개 스키마, 26개 테이블, 약 80MB 데이터**

```sql
heal7 데이터베이스:
├── crawling_service (6개 테이블, 216KB) - 🔥 활발한 운영
├── dream_service (3개 테이블, 79MB) - 🔥 최대 데이터
├── saju_service (4개 테이블, 200KB) - 🔥 핵심 비즈니스
├── shared_common (2개 테이블, 64KB) - 공통 인프라
├── dashboard_service (2개 테이블, 32KB)
├── paperwork_service (1개 테이블, 64KB) 
├── ai_monitoring_service (1개 테이블, 8KB)
└── public (7개 테이블) - 레거시, 점진적 마이그레이션 필요
```

## 🎯 **5개 서비스 도메인 구조**

```
core/
├── 🔮 saju-service/              # 사주명리학 + 꿈풀이 통합
│   ├── saju-schemas/            # saju_service 스키마 (4개 테이블)
│   ├── dream-schemas/           # dream_service 스키마 (3개 테이블)
│   ├── legacy-migration/        # public 스키마 사주 관련 테이블
│   └── calculations/            # 계산 로직
├── 🕷️ crawling-service/          # 데이터 수집
│   ├── schemas/                 # crawling_service 스키마 (6개 테이블)  
│   ├── engines/                 # 크롤링 엔진들
│   └── ai-integration/          # AI 연구 엔진
├── 📄 paperwork-service/         # 서류 처리
│   ├── schemas/                 # paperwork_service 스키마 (1개 테이블)
│   ├── ai-integration/          # AI 분석
│   └── ocr-processing/          # OCR 처리
├── 🧪 ai-monitoring-service/     # AI 모니터링  
│   ├── schemas/                 # ai_monitoring_service 스키마 (1개 테이블)
│   ├── performance-monitoring/  # 성능 모니터링
│   └── alerting/                # 알림 시스템
└── 🎼 cube-modular-service/      # 큐브 모듈러 + 공통 인프라
    ├── dashboard-schemas/       # dashboard_service 스키마 (2개 테이블)
    ├── shared-schemas/          # shared_common 스키마 (2개 테이블)
    ├── orchestration/           # 큐브 오케스트레이션
    └── registry/                # 아키텍처 레지스트리
```

## 🔒 **안전한 개선 방안**

### ✅ **Phase 1: 현재 구조 그대로 매핑** (완료)
- 실제 운영 중인 스키마 구조 그대로 유지
- core 폴더는 논리적 분류만 제공
- **중단 위험: 0%**

### 📋 **Phase 2: 점진적 레거시 정리** (선택사항)
```sql
-- public 스키마의 사주 관련 테이블들을 saju_service로 점진적 이동
-- 예: public.saju_cache → saju_service.saju_cache_legacy
```

### 🚀 **Phase 3: 서비스별 최적화** (향후)
- 인덱스 최적화
- 쿼리 성능 개선
- 필요 시 서비스별 DB 분리

## 📈 **실제 데이터 기반 인사이트**

### 🔥 **핵심 발견**
- **dream_service**: 79MB로 최대 데이터 보유 → 사주서비스 통합 타당
- **crawling_service**: 6개 테이블로 가장 활발 → 독립성 유지 필요
- **public 스키마**: 레거시 정리 시 주의 필요

### 💡 **개선 포인트**
- `dream_raw_collection` 테이블 파티셔닝 고려
- `crawl_logs` 테이블 로그 로테이션 적용
- public 스키마 점진적 마이그레이션

## 🎯 **GitHub Actions 호환성**

현재 빌드 시스템과 완벽 호환:
- **saju-service** (포트 8002) ✅
- **crawling-service** (포트 8003) ✅  
- **paperwork-service** (포트 8001) ✅
- **ai-monitoring-service** (포트 8004) ✅
- **cube-modular-service** (포트 8005) ✅