# 🏗️ HEAL7 프론트엔드 모노레포

> **전체 시스템을 독립된 서비스별 앱으로 완전 분리한 모노레포 구조**

## 📦 워크스페이스 구조

```
heal7-project/frontend/
├── packages/
│   ├── shared/           # 🔄 공통 모듈 (UI 컴포넌트, 3D, 유틸리티)
│   ├── saju-app/         # 🔮 사주명리 서비스 (포트 5173)
│   ├── crawling-app/     # 🕷️ 크롤링 시스템 (포트 5174)
│   ├── admin-app/        # 🛠️ 관리자 대시보드 (포트 5175)
│   └── cube-module-app/  # 🎼 큐브 모듈러 (포트 5176)
├── scripts/              # 개발/배포 스크립트
├── pnpm-workspace.yaml   # pnpm 워크스페이스 설정
└── package.json          # 루트 패키지 설정
```

## 🚀 빠른 시작

### 의존성 설치
```bash
pnpm install
```

### 개발 서버 실행
```bash
# 모든 서비스 동시 실행
pnpm dev

# 개별 서비스 실행
pnpm dev:saju        # 🔮 사주 (http://localhost:5173)
pnpm dev:crawling    # 🕷️ 크롤링 (http://localhost:5174)
pnpm dev:admin       # 🛠️ 관리자 (http://localhost:5175)
pnpm dev:cube        # 🎼 큐브 모듈 (http://localhost:5176)

# 스크립트 사용
./scripts/dev-servers.sh all        # 모든 서비스
./scripts/dev-servers.sh saju       # 사주만
./scripts/dev-servers.sh crawling   # 크롤링만
```

## 🔨 빌드

### 개별 서비스 빌드
```bash
pnpm build:saju      # 사주 앱 빌드
pnpm build:crawling  # 크롤링 앱 빌드
pnpm build:admin     # 관리자 앱 빌드
pnpm build:cube      # 큐브 모듈 앱 빌드
```

### 전체 빌드
```bash
pnpm build           # 모든 서비스 빌드
```

## 🚀 배포

### 로컬 배포
```bash
pnpm deploy:saju     # saju.heal7.com으로 배포
pnpm deploy:crawling # crawling.heal7.com으로 배포

# 스크립트 사용
./scripts/deploy.sh saju      # 로컬 배포
./scripts/deploy.sh crawling  # 로컬 배포
```

### GitHub Actions 배포
```bash
./scripts/deploy.sh saju --github     # GitHub Actions 트리거
./scripts/deploy.sh crawling --github # GitHub Actions 트리거
```

## 🌐 서비스별 접근 주소

### 개발 환경
- **사주 서비스**: http://localhost:5173
- **크롤링 시스템**: http://localhost:5174  
- **관리자 대시보드**: http://localhost:5175
- **큐브 모듈러**: http://localhost:5176

### 프로덕션 환경
- **사주 서비스**: https://saju.heal7.com
- **크롤링 시스템**: https://crawling.heal7.com
- **관리자 대시보드**: https://admin.heal7.com

## 📋 주요 특징

### ✅ 완전한 서비스 분리
- 각 서비스별 독립적인 개발/빌드/배포
- 서비스별 포트, 프록시 설정 분리
- 메타데이터, manifest.json 독립 관리

### ✅ 공통 모듈 재사용
- @heal7/shared 패키지로 UI 컴포넌트 공유
- shadcn/ui, 3D 컴포넌트, 유틸리티 공유
- 워크스페이스 내부 의존성으로 빠른 개발

### ✅ 확장성
- 새 서비스 추가 시 packages/ 아래 새 패키지만 생성
- 기존 서비스에 영향 없음
- 무한 확장 가능

### ✅ 배포 안정성
- 서비스별 독립 배포로 실수 방지
- 원자적 배포 (임시 디렉토리 → 원자적 교체)
- 자동 백업 및 롤백 지원

## 🔧 개발 가이드

### 새 서비스 추가
```bash
mkdir -p packages/new-service/src
cd packages/new-service
# package.json 생성
# vite.config.ts 설정
# 독립 포트 할당
```

### 공통 모듈 사용
```typescript
// shared 모듈에서 UI 컴포넌트 import
import { Button, Card } from '@heal7/shared'

// shared 모듈에서 3D 컴포넌트 import  
import { OptimizedCyberCrystal } from '@heal7/shared'
```

### 타입 체크
```bash
pnpm type-check    # 모든 패키지 타입 체크
```

### 린트
```bash
pnpm lint          # 모든 패키지 린트
```

## 🎯 마이그레이션 완료

### ✅ Phase 0: 긴급 안정화
- 환경변수 기반 앱 분기로 혼동 문제 해결
- `VITE_APP_TYPE`으로 안전한 빌드

### ✅ Phase 1-2: 인프라 구축
- pnpm 워크스페이스 구조 완성
- shared 패키지 분리 완료

### ✅ Phase 3-5: 서비스별 분리
- 사주 앱 완전 독립화
- 크롤링 앱 독립화
- 관리자, 큐브 모듈 앱 분리

### ✅ Phase 6: CI/CD 전환
- GitHub Actions 워크플로우 분리
- 개발/배포 스크립트 완성

---

**🎉 모든 서비스가 완전히 독립된 구조로 전환 완료!**

이제 각 서비스별로 안전하고 독립적인 개발/배포가 가능합니다.