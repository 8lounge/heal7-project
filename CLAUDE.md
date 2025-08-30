# 🏠 HEAL7 프로젝트 마스터 색인

> **빠른 시작**: 30분 내 전체 시스템 이해하기 | **최종 업데이트**: 2025-08-29

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
  - **🕷️ crawling-service**: 데이터 수집 및 크롤링 (crawling.heal7.com)
  
- **프론트엔드 미리보기 (포트 4173)**: ✅ **운영 중** - Vite Preview 서버

### 🏢 **원격 서버**
- **admin.heal7.com**: 관리자 대시보드
- **heal7.com**: 메인 프론트엔드
- **www.heal7.com**: 메인 별칭
- **keywords.heal7.com**: 키워드 매트릭스

### 🗄️ **공통 인프라**
- **데이터베이스**: ✅ PostgreSQL 최적화
- **보안**: ✅ SSL 인증서 유효

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

### ✅ **안전한 대안 명령어**
```bash
gh workflow run build-and-deploy.yml    # GitHub Actions 빌드/배포
vite build && vite preview --port 4173  # 안전한 Vite 빌드 & 미리보기
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

### **AI 크롤링 시스템**
- **메인 서비스**: `crawling.heal7.com` (포트 8004)
- **검증 로그**: `/home/ubuntu/AI_CRAWLING_VERIFICATION_LOG.md`
- **크롤링 엔진**: `/home/ubuntu/heal7-project/backend/services/crawling-service/crawling-cube/`
- **AI 엔진**: `modules/ai_research_engine.py`
- **WebSocket 모니터**: `modules/real_time_monitor.py`
- **API 키**: `/home/ubuntu/.env.ai` (보안 강화 필요)

### **중요 파일 위치**
- **Heal7 백엔드**: `/home/ubuntu/heal7-project/backend/`
- **Heal7 프론트엔드**: `/home/ubuntu/heal7-project/frontend/`
- **사주 핵심 로직**: `/home/ubuntu/heal7-project/backend/app/core/engines/saju_system/`
- **참조 라이브러리**: `/home/ubuntu/REFERENCE_LIBRARY/`
- **프로젝트 문서**: `/home/ubuntu/docs/`

## 🆘 **응급 상황 체크리스트**

### **서비스 다운 시**
1. `systemctl status nginx` - Nginx 상태 확인
2. `sudo lsof -i :8003` - 사주 서비스 (saju.heal7.com)
3. `sudo lsof -i :8004` - 크롤링 서비스 (crawling.heal7.com)
4. `sudo lsof -i :4173` - Vite 미리보기 (개발환경)
5. `sudo -u postgres psql -c "\l"` - DB 연결 확인
6. [상세 복구 가이드](./docs/operations/emergency-recovery.md)

### **사주 계산 오류 시**
1. 한자↔한글 매핑 정상 확인
2. KASI API 연결 상태 확인
3. 무결성 검증 스크립트 실행
4. [사주 시스템 트러블슈팅](./docs/saju-system/troubleshooting.md)

---

**🔍 빠른 검색 팁**: `grep -r "키워드" /home/ubuntu/REFERENCE_LIBRARY/`

*📝 이 문서는 시스템 변경 시 업데이트가 필요할 수 있습니다 | 담당: HEAL7 개발팀*
