# 🏠 HEAL7 프로젝트 마스터 색인

> **빠른 시작**: 30분 내 전체 시스템 이해하기 | **최종 업데이트**: 2025-08-14

## 🚀 **긴급 상황 대응**
- 🔥 [시스템 장애 시](./docs/operations/troubleshooting.md#system-failure)
- ⚡ [서비스 재시작](./docs/operations/deployment.md#quick-restart)
- 🛠️ [사주 시스템 오류](./docs/saju-system/troubleshooting.md)
- 📞 **긴급 연락처**: arne40@heal7.com | 050-7722-7328

## 📊 **현재 시스템 상태** (실시간 업데이트: 2025-08-15 09:40 UTC)

### 🏠 **로컬 서버 (이 서버)** - 통합 프론트엔드 아키텍처 ✅ **운영 중**
- **🎯 heal7-unified-frontend**: ✅ **포트 3000** - 통합 웰니스 플랫폼
  - Next.js 14 + TypeScript + Tailwind CSS 🚀
  - 사주, 건강, 교육, 커뮤니티 통합 서비스 🔮
  - 실시간 동작 확인 완료 ✅
  - 프로세스 ID: 779456 (next-server v14.2.31)
- **🚀 heal7-project 통합 FastAPI**: ✅ **포트 8000** - AI 전용 백엔드
  - `/api/ai` - AI 해석 서비스 🤖
  - `/api/analytics` - 데이터 분석 📊  
  - `/api/admin` - 관리자 서비스 ✅
  - `/api/index` - 메인 서비스 ✅
- **서비스 위치**: `/home/ubuntu/heal7-project/frontend/` (실제 운영 중)
- **기술스택**: Next.js 14 + TypeScript + Tailwind CSS + Zustand
- **성능 개선**: React 19, 프레이머 모션, SWR 데이터 페칭

### 🏢 **원격 서버** - 도메인 기반 서비스
- **admin.heal7.com**: 관리자 대시보드
- **heal7.com**: 메인 프론트엔드  
- **www.heal7.com**: 메인 별칭
- **keywords.heal7.com**: 키워드 매트릭스

### 🗄️ **공통 인프라**
- **사주 v5.0**: ✅ **완전 가동** (KASI API, AI 검수)
- **M-PIS**: ✅ **442개 키워드 활성**
- **데이터베이스**: ✅ **PostgreSQL 최적화**
- **보안**: ✅ **SSL 인증서 유효**

## 🎯 **역할별 빠른 접근**

### 👨‍💼 **프로젝트 관리자** (3분 파악)
- [📋 전체 시스템 현황](./docs/system-architecture/overview.md)
- [📈 성능 지표 대시보드](./docs/operations/monitoring.md)
- [💰 비용 및 리소스](./docs/operations/resources.md)

### 👨‍💻 **개발자** (5분 시작)
- [🛠️ 개발 환경 설정](./docs/development/setup.md)
- [📚 코딩 가이드라인](./docs/development/guidelines.md)
- [🔧 API 문서 모음](./docs/saju-system/api-reference.md)

### 🤖 **AI 에이전트** (즉시 접근)
- [🧠 에이전트 오케스트레이션](./docs/agent-orchestration/README.md)
- [🔥 엔트로피 지양 정책](./docs/project_docs/operations/entropy-management-detailed-guidelines.md)
- [🚀 배포 시스템 v2.0](./docs/project_docs/operations/deployment-guidelines-v2.md)
- [🧹 클린마스터 정책](./docs/agent-orchestration/clean-master-smart-orchestration-policy.md)

## 🔥 **핵심 정책** (필수 준수)

### 🚫 **금지 명령어 (절대 금지)**
```bash
npm run dev          # OOM Kill 위험
next dev            # 메모리 부족 발생  
rm -rf .next        # 서비스 중단 위험
kill -9 $(pgrep nginx)  # 전체 웹서비스 중단
```

### ✅ **안전한 대안 명령어**
```bash
gh workflow run build-and-deploy.yml    # GitHub Actions 빌드
bash /home/ubuntu/scripts/deployment/heal7-deploy-master.sh   # 안전한 배포
bash /home/ubuntu/scripts/maintenance/heal7-enhanced-health-check.sh  # 상태 확인
```

### 📐 **반-생성 우선 원칙 (Anti-Generation First)**
**생성 전 필수 체크**:
1. **질문1**: "기존 파일을 재활용할 수 있는가?"
2. **질문2**: "생성이 꼭 필요한가?"
3. **질문3**: "생성 후 정리 계획이 있는가?"

### 🧹 **엔트로피 지양 핵심 규칙**
- **최상위 폴더 절대 금지**: `/home/ubuntu/*.{md,py,js,json}` (CLAUDE.md, *.pem 제외)
- **AI 에이전트 작업 완료 후 정리 의무**: 모든 파편 파일 적절한 폴더로 분류
- **자동 초기화 시스템**: 복잡도 임계치 달성 시 자동 정리 (3개 비허가 파일, 1개 비허가 폴더)

## 🏗️ **핵심 아키텍처** (실제 시스템 상태 기준)

### **🌐 도메인별 서버 분산 구조**
```
🏠 로컬 서버 (saju/test 특화):
   saju.heal7.com → FastAPI (8000) + Next.js (3004)
   test.heal7.com → FastAPI (8001) 
   heal7.com → FastAPI (백업)

🏢 원격 서버 (admin/main/keywords 특화):
   admin.heal7.com → FastAPI (8001)
   heal7.com → FastAPI (8000) - 메인
   www.heal7.com → FastAPI (8000) - 메인 별칭
   keywords.heal7.com → API 서비스
   
          ↓
    PostgreSQL + Redis
    442개 키워드 M-PIS
```

### **📍 현재 NGINX 설정 상태**

#### **로컬 서버 활성 사이트:**
- **heal7.com**: 메인 도메인 (sites-enabled)
- **saju.heal7.com**: 사주 서비스 (sites-enabled)  
- **test.heal7.com**: 테스트 환경 (sites-enabled)

#### **원격 서버 활성 사이트:**
- **admin.heal7.com**: 관리자 대시보드
- **heal7-main**: 메인 서비스 (heal7.com, www.heal7.com)
- **keywords.heal7.com**: 키워드 매트릭스

### **🔧 실제 구동 중인 서비스**

#### **로컬 서버:**
- **3000 포트**: next-server v14.2.31 (heal7-unified-frontend) - 메인 프론트엔드
- **8000 포트**: python simple_server.py (archive/duplicates)
- **8001 포트**: python simple_server.py (archive/duplicates)
- **8002 포트**: uvicorn main:app (archive/legacy) - Paperwork AI

#### **원격 서버:**
- **8000 포트**: python3 (메인 서비스)
- **8001 포트**: python3 (관리자 API)

### **⚠️ 현재 시스템 문제점**
- **서비스 실행 위치**: archive/duplicates, archive/legacy에서 구동 중 (정리 필요)
- **포트 비표준화**: 일부 서비스가 비표준 위치에서 실행
- **프로젝트 구조**: heal7-project/frontend는 정상 운영 중, 백엔드 부분 정리 필요

## 🔧 **시스템 설정 상태** (실제 운영 환경)

### **📂 배포 폴더 구조** (/var/www/)
```
/var/www/
├── admin.heal7.com/      # 관리자 정적 파일
├── heal7.com/           # 메인 사이트 정적 파일  
├── saju.heal7.com/      # 사주 서비스 정적 파일
├── test.heal7.com/      # 테스트 환경 정적 파일
└── shared/              # 공통 리소스
```

### **🗂️ 프로젝트 파일 구조** (/home/ubuntu/)
```
/home/ubuntu/
├── heal7-project/       # 메인 프로젝트
│   ├── backend/         # FastAPI 백엔드 (개발 중)
│   ├── frontend/        # Next.js 통합 프론트엔드 (✅ 운영 중, 포트 3000)
│   │   ├── src/app/     # 앱 라우터 구조
│   │   ├── src/components/ # 재사용 컴포넌트
│   │   └── src/lib/     # 유틸리티 및 API 클라이언트
│   └── deployment/      # 배포 스크립트
├── database/heal7-*/    # 각 서비스별 DB 설정
├── .heal7-session/      # 세션 관리
└── archive/             # 레거시 서비스 위치 (정리 필요)
    ├── projects/duplicates/  # 8000, 8001 포트 실행 위치
    └── legacy/platforms/     # 8002 포트 실행 위치
```

### **⚙️ Systemd 서비스 상태**
- **nginx.service**: ✅ running (리버스 프록시)
- **postgresql@16-main.service**: ✅ running (통합 데이터베이스 - PostgreSQL 16)
- **redis-server.service**: ✅ running (캐시)
- **heal7 관련 서비스**: ❌ 없음 (수동 실행 상태)

### **🔧 시스템 커널 설정** (sysctl)
```bash
vm.swappiness = 10          # 스왑 사용 최소화
vm.dirty_ratio = 10         # 메모리 10%에서 스왑 시작
vm.dirty_background_ratio = 5  # 백그라운드 정리 5%
```

### **🔄 백그라운드 프로세스**
- **총 Python/Node.js 프로세스**: 17개 실행 중
- **주요 서비스**: FastAPI (8000, 8001, 8002), Next.js (3000)
- **관리 방식**: 수동 실행 (systemd 미적용)
- **메인 프론트엔드**: 프로세스 779456 (next-server v14.2.31)

## 🔑 **AI API 키 통합 관리**
- **마스터 파일**: `/home/ubuntu/.env.ai` (600 권한, 보안 설정)
- **심볼릭 링크**: 모든 서비스에서 동일한 API 키 파일 참조
- **지원 모델**: Google Gemini 2.0, OpenAI GPT-4o, Anthropic Claude, Perplexity AI
- **비용 관리**: 일일 $50 USD 한도, 80% 도달 시 알림

## 🔍 **시스템별 빠른 검색**

| 시스템 | 상태 | 문서 | 마지막 업데이트 | 담당자 |
|--------|------|------|------------------|--------|
| 🔮 사주 v5.0 | ✅ | [📖 문서](./docs/saju-system/) | 2025-08-03 | AI팀 |
| 📝 설문 관리 | ✅ | [📖 문서](./docs/surveys/) | 2025-08-04 | 개발팀 |
| 🧠 M-PIS | ✅ | [📖 문서](./docs/mpis-framework/) | 2025-08-02 | 분석팀 |
| 🤖 에이전트 | ✅ | [📖 문서](./docs/agent-orchestration/) | 2025-08-14 | AI팀 |
| 📄 Paperwork-AI | ✅ | [📖 문서](./docs/operations/paperwork-ai.md) | 2025-08-05 | AI팀 |

## 🔥 **자주 찾는 정보**

### **API 엔드포인트**
```bash
# 키워드 관리
GET  /admin-api/keywords/search    # 키워드 검색

# 설문 관리
POST /admin-api/surveys/templates  # 새 설문 템플릿 생성
GET  /admin-api/surveys/templates  # 설문 템플릿 목록
POST /admin-api/surveys/sessions/start  # 설문 세션 시작
```

### **중요 파일 위치** (실제 현황)
- **통합 프론트엔드**: `/home/ubuntu/heal7-project/frontend/` (✅ 포트 3000 운영 중)
- **사주 시스템**: `/home/ubuntu/heal7-project/backend/saju_engines/saju_system/`
- **현재 실행 중인 서비스**: `/home/ubuntu/archive/projects/duplicates/` (8000, 8001)
- **Paperwork AI**: `/home/ubuntu/archive/legacy/platforms/` (8002)
- **정적 파일**: `/var/www/saju.heal7.com/`, `/var/www/test.heal7.com/`
- **메인 프로젝트**: `/home/ubuntu/heal7-project/` (프론트엔드 정상 운영, 백엔드 개발 중)

## 🆘 **응급 상황 체크리스트**

### **서비스 다운 시**
1. `systemctl status nginx` - Nginx 상태 확인
2. `sudo lsof -i :3000` - 메인 프론트엔드 확인 (통합 플랫폼)
3. `sudo lsof -i :8000` - 백엔드 서비스 확인 (로컬)
4. `sudo lsof -i :8001` - 테스트 서비스 확인 (로컬)
5. `sudo lsof -i :8002` - Paperwork AI 확인 (로컬)
6. `sudo -u postgres psql -c "\l"` - DB 연결 확인
7. **원격서버**: `ssh ubuntu@43.200.203.115 "sudo lsof -i :8000 -i :8001"`
8. [상세 복구 가이드](./docs/operations/emergency-recovery.md)

### **사주 계산 오류 시**
1. 한자↔한글 매핑 정상 확인
2. KASI API 연결 상태 확인
3. 무결성 검증 스크립트 실행
4. [사주 시스템 트러블슈팅](./docs/saju-system/troubleshooting.md)

## 📖 **전체 문서 구조**

```
/home/ubuntu/
├── 📋 CLAUDE.md (마스터 색인)
├── 🏗️ docs/ (문서 시스템)
│   ├── system-architecture/ (시스템 전체 구조)
│   ├── 🔮 saju-system/ (사주 명리학 v5.0)
│   ├── 🧠 mpis-framework/ (M-PIS 진단)
│   ├── 🤖 agent-orchestration/ (AI 에이전트 시스템)
│   ├── 🗄️ database/ (데이터베이스 관리)
│   ├── ⚙️ operations/ (운영 및 배포)
│   ├── 📚 development/ (개발 가이드)
│   └── 📅 project_docs/work-logs/ (업무 일지 시스템)
├── 🚀 project/ (메인 프로젝트)
│   ├── heal7-admin/ (관리자 - Next.js + FastAPI)
│   ├── heal7-keywords/ (키워드 - Next.js + FastAPI)  
│   └── heal7-index/ (메인 - FastAPI 단일)
└── 📊 logs/ (로그 파일)
```

## 📚 **상세 가이드 문서**

### **🔧 운영 및 배포**
- [메모리 최적화 시스템](./docs/operations/memory-optimization-system-v2.0.md)
- [AI API 키 관리](./docs/operations/ai-api-key-management.md)
- [시스템 기준점 문서](./docs/operations/baseline-docs/2025-08-13-system-baseline.md)

### **🤖 AI 에이전트 시스템**
- [통합 운영관리 체계](./docs/agent-orchestration/integrated-operations-management.md)
- [엔트로피 관리 세부 가이드](./docs/project_docs/operations/entropy-management-detailed-guidelines.md)

### **📅 최근 업무 이력**
- [2025-08-15 프론트엔드 중심 사주시스템 구현](./docs/project_docs/work-logs/2025/08/2025-08-15-frontend-centered-saju-system-implementation.md) ⭐
- [2025-08-12 Next.js 3D Globe 구현](./docs/project_docs/work-logs/2025/08/2025-08-12-nextjs-3d-globe-implementation.md)

---

**🔍 빠른 검색 팁**: `grep -r "키워드" /home/ubuntu/docs/`

*📝 이 문서는 시스템 변경 시 자동 업데이트됩니다 | 담당: HEAL7 개발팀*
*🧹 마지막 정리: 2025-08-14 17:15 UTC | 엔트로피 지양 정책 v8.0 적용*