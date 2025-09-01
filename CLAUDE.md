# 🏠 HEAL7 프로젝트 마스터 색인

> **빠른 시작**: 30분 내 전체 시스템 이해하기 | **최종 업데이트**: 2025-08-30

## 🚀 **긴급 상황 대응**
- 🔥 [시스템 장애 시](./docs/operations/troubleshooting.md#system-failure)
- ⚡ [서비스 재시작](./docs/operations/deployment.md#quick-restart)
- 🛠️ [사주 시스템 오류](./docs/saju-system/troubleshooting.md)
- 📞 **긴급 연락처**: arne40@heal7.com | 050-7722-7328

## 📊 **현재 시스템 상태** (2025-08-29 기준)

### 🏠 **`heal7-project`**
- **위치**: `/home/ubuntu/heal7-project/`
- **구성**:
  - `backend/`: FastAPI 백엔드 애플리케이션
  - `frontend/`: Vite 기반 프론트엔드 애플리케이션
- **기술스택**: FastAPI, Vite, TypeScript, Tailwind CSS
- **주요 서비스**:
  - **🔮 saju-service**: 사주명리학 계산 및 해석 (saju.heal7.com)
  - **🕷️ crawling-service**: 데이터 수집 및 크롤링 (crawling.heal7.com) ⚡ **2025-08-31 React 시스템 교체 완료**
  
- **프론트엔드 미리보기 (포트 4173)**: ✅ **운영 중** - Vite Preview 서버

### 🏢 **원격 서버**
- **admin.heal7.com**: 관리자 대시보드
- **heal7.com**: 메인 프론트엔드
- **www.heal7.com**: 메인 별칭
- **keywords.heal7.com**: 키워드 매트릭스

### 🗄️ **공통 인프라**
- **데이터베이스**: ✅ PostgreSQL 최적화
- **보안**: ✅ SSL 인증서 유효

### 🕷️ **크롤링 시스템 대규모 업그레이드 완료** (2025-08-31) ⚡ **신규**
> 🏆 **Big Bang Replacement 성공**: 레거시 Alpine.js → 최신 React + TypeScript 완전 교체

#### **🎯 교체 결과**
- **✅ Phase 1-8 완료**: 모든 계획 단계 100% 완료
- **✅ 시스템 중단 시간**: < 5분 (무중단 배포 성공)  
- **✅ 코드 품질 혁신**: 1585줄 단일 HTML → 모듈화된 React 컴포넌트
- **✅ 실시간 기능**: WebSocket, 알림, 로그 스트리밍 구현
- **✅ 3-Tier 통합**: httpx, Playwright, Selenium 크롤러 완전 지원

#### **🏗️ 새로운 아키텍처 스택**
```typescript
Frontend: React 18 + TypeScript + Tailwind CSS + shadcn/ui + Framer Motion
Backend: FastAPI 3-Tier Crawler + MultiModal AI (Gemini, GPT-4o, Claude)
Real-time: Socket.io + WebSocket Server + Redis
Storage: PostgreSQL + Redis Cache
```

#### **📂 핵심 컴포넌트 위치**
- **React 시스템**: `/home/ubuntu/heal7-project/frontend/src/components/crawling/`
- **레거시 백업**: `/var/www/crawling.heal7.com.legacy-backup-20250830-172643/`
- **아카이브**: `/home/ubuntu/archive/crawling-legacy-20250831-003946/`
- **프로덕션**: `https://crawling.heal7.com` (React 시스템 운영 중)

### ⚡ **GitHub Actions 빌드 + 수동 배포 시스템** (2025-09-01 정책 변경) ⚡ **최신**
> 🚀 **하이브리드 모드**: 원격 빌드 + 수동 배포로 안정성 극대화

#### 🎼 **서비스별 그룹 분류 완료** ✅
- **🎨 frontend-build-deploy.yml**: 프론트엔드 전용 (Node.js 18, Vite)
- **🎼 backend-services-build.yml**: 6개 백엔드 서비스 병렬 빌드
  - 🎼 cube-modular-dashboard (포트 8000): 큐브모듈러 대시보드 ✅ **2025-08-31 재배치**
  - 📄 paperwork-service (포트 8001): 서류 처리 및 AI 분석 ✅ 
  - 🔮 saju-service (포트 8002): 사주명리 계산 및 해석 ✅ **2025-08-31 재배치**
  - 🕷️ crawling-service (포트 8003): 데이터 수집 및 크롤링  
  - 🧪 ai-monitoring-service (포트 8004): AI 성능 모니터링
  - 🎼 dashboard-service (포트 8005): 오케스트레이션 허브 ⭐
- **🚀 service-deployment.yml**: 배포 오케스트레이션 자동화
- **🎯 service-selector.yml**: 수동 서비스 선택 빌드 (관리자용)

#### 🔥 **빌드 & 배포 규칙** ⚡ **2025-09-01 수동 배포 모드**
```bash
# ✅ 1단계: 원격 빌드 (GitHub Actions)
gh workflow run frontend-build-deploy.yml      # 사주앱 + 크롤링앱 빌드
gh workflow run backend-services-build.yml     # 백엔드 서비스 빌드
gh workflow run service-selector.yml -f target_service=crawling-service    # 특정 서비스

# ✅ 2단계: 수동 배포 (Claude CLI 필수)
# 빌드 완료 후 아티팩트 다운로드하여 수동 배포
# 자동 배포는 비활성화됨 (안정성 향상)

# ⚠️ 금지 사항
pnpm build                                      # 로컬 빌드 금지
vite build                                      # 로컬 빌드 금지
npm run build                                   # 로컬 빌드 금지
```

#### 📋 **배포 자동화 트리거**
- **Push**: `main` 브랜치에 코드 푸시 시 자동 빌드
- **PR**: Pull Request 생성 시 테스트 빌드
- **Manual**: `workflow_dispatch`로 수동 실행 가능

## 🎯 **역할별 빠른 접근**

### 👨‍💼 **프로젝트 관리자** (3분 파악)
- [📋 전체 시스템 현황](./docs/system-architecture/overview.md)
- [📈 성능 지표 대시보드](./docs/operations/monitoring.md)
- [💰 비용 및 리소스](./docs/operations/resources.md)

### 👨‍💻 **개발자** (5분 시작)
- [🛠️ 개발 환경 설정](./docs/development/setup.md)
- [📚 코딩 가이드라인](./docs/development/guidelines.md)
- [🔧 API 문서 모음](./docs/saju-system/api-reference.md)

### 🧊 **큐브 모듈러 시스템** (핵심 아키텍처)
- [🎼 백엔드 종합 가이드](./heal7-project/backend/README(백엔드종합가이드).md)
- [🎼 오케스트레이션 허브 가이드](./heal7-project/backend/services/dashboard-service/README(오케스트레이션허브가이드).md)
- [🔮 사주 엔진 가이드](./heal7-project/backend/app/core/engines/saju_system/README(사주엔진가이드).md)

## 🔥 **핵심 정책** (필수 준수)

### 🚫 **금지 명령어 (절대 금지)**
```bash
npm run dev          # OOM Kill 위험
next dev            # 메모리 부족 발생
vite dev --host     # 메모리 부족 위험 (호스트 바인딩 시)
rm -rf .next        # 서비스 중단 위험
rm -rf dist         # Vite 빌드 결과물 삭제 위험
kill -9 $(pgrep nginx)  # 전체 웹서비스 중단
```

### ✅ **안전한 배포 프로세스** ⚡ **2025-09-01 수동 배포 모드 도입**
```bash
# 🎯 1단계: GitHub Actions 원격 빌드 (권장)
gh workflow run frontend-build-deploy.yml                                   # 프론트엔드 빌드
gh workflow run backend-services-build.yml                                  # 백엔드 빌드
gh workflow run service-selector.yml -f target_service=saju-service-only    # 특정 서비스만

# 🎯 2단계: Claude CLI와 함께 수동 배포
# GitHub Actions 아티팩트를 다운로드 후:
sudo cp -r ./saju-app-dist/* /var/www/saju.heal7.com/                      # 사주 서비스 배포
sudo cp -r ./crawling-app-dist/* /var/www/crawling.heal7.com/              # 크롤링 서비스 배포
sudo chown -R www-data:www-data /var/www/[service].heal7.com               # 권한 설정
sudo systemctl reload nginx                                                  # 서버 리로드

# ⚠️ 로컬 빌드 금지 - GitHub Actions 원격 빌드만 사용
```

### 🧹 **엔트로피 지양 핵심 규칙**
- **최상위 폴더 절대 금지**: `/home/ubuntu/*.{md,py,js,json}` (CLAUDE.md, *.pem 제외)
- **AI 에이전트 작업 완료 후 정리 의무**: 모든 파편 파일 적절한 폴더로 분류

## 📂 **프로젝트 전체 구조** (실제 파일 시스템 기준)
```
/home/ubuntu/
├── 📋 CLAUDE.md (이 파일)
├── 🏗️ heal7-project/ (메인 프로젝트)
│   ├── backend/
│   ├── frontend/
│   ├── deployment/
│   └── ...
├── 📚 REFERENCE_LIBRARY/ (프로젝트 참조 라이브러리)
│   ├── _guides/
│   ├── core-logic/
│   ├── feature-specs/
│   └── ...
├── 📄 docs/ (프로젝트 문서)
├── 📦 archive/ (오래된 파일 보관소)
├── 📜 scripts/ (유틸리티 스크립트)
├── 🪵 logs/ (로그 파일)
├── .git/
├── .github/
└── ... (기타 설정 파일)
```

## ⚙️ **Systemd 서비스 상태**
- **nginx.service**: ✅ running (리버스 프록시)
- **postgresql@16-main.service**: ✅ running (통합 데이터베이스)
- **redis-server.service**: ✅ running (캐시)
- **heal7 관련 서비스**: ❌ 없음 (수동 실행 상태)

## 🚀 **크롤링 시스템 React 교체 완료** (2025-08-31) ⚡ **최신**

### **🎉 Phase 8 Big Bang Replacement 성공**
- **✅ 레거시 시스템 교체**: Alpine.js (1585줄) → React + TypeScript
- **✅ 모든 기능 완성**: Phase 1-7 구현 → Phase 8 배포 완료
- **✅ 시스템 안정성**: 무중단 배포, 완전 백업, 롤백 계획 완비

## ✅ **AI 크롤링 시스템 검증 완료** (2025-08-30)

### 🔴 **긴급 완료 필요** - ✅ **완료**
1. **통합 API 엔드포인트 동작 확인** ✅
   - WebSocket 라우팅 403 오류 해결 ✅
   - AI 수집 API 테스트 완료 ✅
   - FastAPI `/docs` 페이지 전체 검증 ✅

2. **오류 처리 및 폴백 시스템 테스트** ✅
   - 404/200 응답 코드 정상 동작 확인 ✅
   - 네트워크 장애 시 복구 메커니즘 검증 ✅
   - 데이터베이스 연결 확인 ✅

3. **보안 검증 및 API 키 보호 체크** ✅
   - `.env.ai` 파일 존재 및 권한(644) 확인 ✅
   - API 키 3개(OpenAI, Anthropic, Gemini) 확인 ✅
   - 파일 보안 검증 완료 ✅

## 🔥 **자주 찾는 정보**

### **🕷️ 크롤링 시스템** (2025-09-01 수동 배포 모드) ⚡ **최신**
- **메인 서비스**: `crawling.heal7.com` (React + TypeScript 기반) ✅ **운영 중**
- **아키텍처**: React 18 + FastAPI 3-Tier + MultiModal AI
- **핵심 컴포넌트**: `/home/ubuntu/heal7-project/frontend/packages/crawling-app/`
- **백엔드 API**: 포트 8003 (`/api/`, `/ws`, `/docs` 경로)
- **실시간 기능**: WebSocket + 알림 시스템 + 로그 스트리밍
- **배포 모드**: ✅ **수동 배포** (GitHub 원격 빌드 + Claude CLI 배포)
- **빌드 아티팩트**: `crawling-app-dist` (GitHub Actions에서 생성)
- **완료 보고서**: `/home/ubuntu/docs/project_docs/work-logs/2025/08/2025-08-31-crawling-system-replacement-complete.md`

### **🔒 보안 및 백업 체계**
- **레거시 백업**: `/var/www/crawling.heal7.com.legacy-backup-20250830-172643/`
- **핵심 파일 아카이브**: `/home/ubuntu/archive/crawling-legacy-20250831-003946/`
- **NGINX 설정 백업**: `/tmp/crawling.heal7.com.backup`
- **API 키**: `/home/ubuntu/.env.ai` (Gemini, OpenAI, Anthropic)

### **🚀 수동 배포 프로세스** (2025-09-01 신규 정책) ⚡ **필수 숙지**

#### **1단계: GitHub Actions 원격 빌드**
```bash
# 프론트엔드 빌드 (사주앱 + 크롤링앱)
gh workflow run frontend-build-deploy.yml

# 백엔드 서비스 빌드
gh workflow run backend-services-build.yml

# 특정 서비스만 빌드
gh workflow run service-selector.yml -f target_service=crawling-service
```

#### **2단계: Claude CLI 수동 배포**
```bash
# GitHub Actions에서 아티팩트 다운로드 후:

# 크롤링 시스템 배포
sudo cp -r ./crawling-app-dist/* /var/www/crawling.heal7.com/
sudo chown -R www-data:www-data /var/www/crawling.heal7.com/
sudo systemctl reload nginx

# 사주 시스템 배포  
sudo cp -r ./saju-app-dist/* /var/www/saju.heal7.com/
sudo chown -R www-data:www-data /var/www/saju.heal7.com/
sudo systemctl reload nginx
```

#### **🔧 자동 배포 비활성화 상태**
- ✅ **service-deployment.yml**: 수동 모드로 변경 완료
- ✅ **frontend/scripts/deploy.sh**: 자동 복사 비활성화 완료
- ✅ **안정성 향상**: 예상치 못한 배포 중단 방지

### **중요 파일 위치**
- **Heal7 백엔드**: `/home/ubuntu/heal7-project/backend/`
- **Heal7 프론트엔드**: `/home/ubuntu/heal7-project/frontend/`
- **사주 핵심 로직**: `/home/ubuntu/heal7-project/backend/app/core/engines/saju_system/`
- **참조 라이브러리**: `/home/ubuntu/REFERENCE_LIBRARY/`
- **프로젝트 문서**: `/home/ubuntu/docs/`

## 🆘 **응급 상황 체크리스트**

### **서비스 다운 시** (2025-08-31 포트 재배치 완료)
1. `systemctl status nginx` - Nginx 상태 확인
2. `sudo lsof -i :8000` - 큐브모듈러 대시보드 ✅ **신규 추가**
3. `sudo lsof -i :8002` - 사주 서비스 (saju.heal7.com) ✅ **재배치 완료**
4. `sudo lsof -i :8003` - 크롤링 서비스 (crawling.heal7.com)
5. `sudo lsof -i :4173` - Vite 미리보기 (개발환경)
6. `sudo -u postgres psql -c "\l"` - DB 연결 확인
7. [상세 복구 가이드](./docs/operations/emergency-recovery.md)

### **사주 계산 오류 시**
1. 한자↔한글 매핑 정상 확인
2. KASI API 연결 상태 확인
3. 무결성 검증 스크립트 실행
4. [사주 시스템 트러블슈팅](./docs/saju-system/troubleshooting.md)

---

**🔍 빠른 검색 팁**: `grep -r "키워드" /home/ubuntu/REFERENCE_LIBRARY/`

*📝 이 문서는 시스템 변경 시 업데이트가 필요할 수 있습니다 | 담당: HEAL7 개발팀*
