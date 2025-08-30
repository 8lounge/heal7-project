# 🏗️ HEAL7 백엔드 핵심 아키텍처

> **핵심 원칙**: 단일 진실 소스 (Single Source of Truth)

## 📐 **완전 통합 구조**

```
core/
├── 🗄️ data-layer/              # 모든 데이터 스키마의 단일 진실 소스
│   ├── schemas/
│   │   ├── shared/             # 공통 스키마 (users, auth, etc)
│   │   ├── saju/               # 사주 스키마
│   │   ├── crawling/           # 크롤링 스키마
│   │   ├── dream/              # 꿈풀이 스키마
│   │   ├── paperwork/          # 서류 스키마
│   │   └── monitoring/         # 모니터링 스키마
│   ├── migrations/             # 모든 마이그레이션 스크립트
│   └── connections.yaml        # 데이터베이스 연결 설정
│
├── 🎯 cube-registry/           # 큐브 메타데이터 관리
│   ├── registry.json           # 마스터 큐브 레지스트리
│   ├── service-configs/        # 각 서비스별 설정
│   └── routing-rules.yaml      # 큐브 간 라우팅 규칙
│
└── 🛡️ backup-system/          # 백업 및 복구 시스템
    ├── automated/              # 자동 백업
    ├── manual/                 # 수동 백업
    └── recovery-scripts/       # 복구 스크립트
```

## 🎯 **핵심 장점**

1. **단일 진실 소스**: 모든 스키마가 `core/data-layer/`에만 존재
2. **명확한 책임 분리**: 핵심 데이터 vs 비즈니스 로직
3. **중앙 집중 관리**: 백업, 마이그레이션, 레지스트리 통합
4. **참조 일관성**: 모든 서비스는 `core/`를 참조

## 🔄 **이전 구조와의 관계**

- **`/services/`**: 비즈니스 로직만 (스키마 제거)
- **`/data-cubes/`**: 추상화 레이어만 (스키마 제거)
- **`/app/`**: FastAPI 애플리케이션만
- **`/core/`**: 모든 데이터 관련 파일의 중앙 저장소