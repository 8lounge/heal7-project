# 🏛️ Government Portal Intelligence System v2.0

> **한국 정부 지원사업 포털을 24시간 자동 모니터링하여 AI가 템플릿을 생성하는 지능형 시스템**

## 🎯 **핵심 기능**

### 🔍 **실시간 포털 모니터링**
- **기업마당**: 매일 06:00 자동 스크래핑
- **K-Startup**: 매일 07:00 자동 스크래핑 (SPA 대응)
- **정부24**: 향후 확장 예정

### 🤖 **AI 기반 자동화**
- **패턴 학습**: 수집된 데이터에서 양식 패턴 자동 추출
- **템플릿 생성**: 새로운 지원사업 발견시 즉시 템플릿 자동 생성
- **기관별 맞춤화**: SBA, KOSMES, NIPA, TECHNO 각각의 특성 반영
- **품질 검증**: AI가 생성한 템플릿의 실용성 자동 평가

### 📡 **Paperwork AI 연동**
- **실시간 동기화**: 생성된 템플릿과 데이터 자동 전송
- **우선순위 관리**: 중요도에 따른 배치 처리
- **오류 복구**: 전송 실패시 자동 재시도

## 🏗️ **시스템 구조**

```
government-portal-scraper/
├── main.py                     # FastAPI 메인 서버
├── config/
│   └── settings.py            # 시스템 설정
├── scrapers/
│   ├── bizinfo_scraper.py     # 기업마당 스크래퍼
│   └── kstartup_scraper.py    # K-Startup SPA 스크래퍼
├── utils/
│   ├── rate_limiter.py        # 지능형 속도 제한
│   ├── content_cleaner.py     # 한국어 콘텐츠 정리
│   └── scheduler.py           # 매일 자동 스케줄러
├── api/
│   └── paperwork_connector.py # Paperwork AI 연동
└── requirements.txt           # 필요 패키지 목록
```

## 🚀 **설치 및 실행**

### 1. 의존성 설치
```bash
cd /home/ubuntu/heal7-project/backend/services/government-portal-scraper
pip install -r requirements.txt

# Playwright 브라우저 설치 (K-Startup SPA 스크래핑용)
playwright install chromium
```

### 2. 환경 변수 설정
```bash
# .env 파일 생성
cat > .env << EOF
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost:5432/government_portal_db

# Paperwork AI 연동
PAPERWORK_API_URL=https://paperwork.heal7.com
PAPERWORK_API_KEY=your-api-key
PAPERWORK_SECRET_KEY=your-secret-key

# AI 모델 (선택사항)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_AI_API_KEY=your-google-ai-key

# 환경 설정
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
EOF
```

### 3. 서버 실행
```bash
# 개발 모드
python main.py

# 프로덕션 모드
uvicorn main:app --host 0.0.0.0 --port 8005 --workers 2
```

## 📡 **API 엔드포인트**

### 📊 **모니터링**
- `GET /` - API 상태 확인
- `GET /health` - 시스템 헬스 체크
- `GET /programs/latest` - 최신 지원사업 조회
- `GET /templates/auto-generated` - 자동 생성된 템플릿 조회

### 🔧 **수동 제어**
- `POST /scrape/manual` - 수동 스크래핑 실행
- `POST /paperwork/sync` - Paperwork AI 수동 동기화

### 📈 **스케줄 관리**
- `GET /scheduler/status` - 스케줄러 상태 확인
- `POST /scheduler/jobs/{job_id}/run` - 작업 즉시 실행

## 📅 **자동 스케줄**

### 🌅 **일일 작업**
- **06:00** - 기업마당 전체 스크래핑
- **07:00** - K-Startup 전체 스크래핑  
- **13:00** - 전체 포털 종합 분석

### 🕒 **시간별 작업**
- **매 2시간** - 신속 업데이트 체크 (08:00-18:00)

### 📅 **주간 작업**
- **일요일 23:00** - 주간 종합 분석 및 리포트

## 🤖 **AI 모델 활용**

### 📝 **문서 분석**
- **GPT-4o**: 문서 구조 분석 및 콘텐츠 추출
- **Claude 3.5**: 섹션별 매핑 및 패턴 인식
- **Gemini Pro**: 품질 검증 및 최적화

### 🎯 **기관별 특화**
```python
기관별 AI 학습 패턴:
- SBA: "혁신", "차별화", "글로벌" 키워드 중시
- KOSMES: "실용화", "상용화", "안정성" 중심
- NIPA: "디지털", "플랫폼", "데이터" 강조
- TECHNO: "검증", "신뢰성", "지속성" 포커스
```

## 📊 **성능 지표**

### 🎯 **목표 성능**
- **수집 속도**: 시간당 1,000개 이상 프로그램 처리
- **정확도**: 95% 이상 데이터 정확성 
- **가용성**: 99.5% 이상 시스템 가동률
- **응답시간**: API 응답 1초 이내

### 📈 **실시간 모니터링**
- 포털별 스크래핑 성공률
- AI 템플릿 생성 품질 점수
- Paperwork AI 동기화 상태
- 시스템 리소스 사용량

## 🔒 **보안 및 안정성**

### 🛡️ **요청 제한**
- **기업마당**: 분당 20요청
- **K-Startup**: 분당 15요청 (SPA 특성 고려)
- **적응형 제한**: 서버 응답에 따른 자동 조정

### 🔄 **오류 복구**
- **자동 재시도**: 최대 3회 재시도
- **백오프 전략**: 지수적 지연 증가
- **우회 경로**: API 실패시 브라우저 스크래핑

### 📝 **로그 관리**
- **구조화된 로깅**: JSON 형식 로그
- **로테이션**: 10MB 단위 자동 회전
- **레벨 관리**: DEBUG/INFO/WARNING/ERROR

## 🌍 **확장 계획**

### 🇰🇷 **한국 (Phase 1 - 완료)**
- ✅ 기업마당 (bizinfo.go.kr)
- ✅ K-Startup (k-startup.go.kr)
- ⏳ 정부24 (gov.kr) - 개발 예정

### 🌏 **글로벌 확장 (Phase 2)**
- 🇺🇸 미국: SBA.gov, SBIR.gov
- 🇯🇵 일본: J-NET21, JETRO  
- 🇪🇺 유럽: EU Funding & Tenders Portal

## 🔧 **개발자 가이드**

### 🆕 **새로운 포털 추가**
1. `scrapers/` 폴더에 새 스크래퍼 클래스 생성
2. `config/settings.py`에 포털 설정 추가
3. `main.py`에서 스크래퍼 등록
4. 스케줄 설정 및 테스트

### 🧪 **테스트 실행**
```bash
# 단위 테스트
pytest tests/

# 스크래핑 테스트
python -m pytest tests/test_scrapers.py -v

# API 테스트  
python -m pytest tests/test_api.py -v
```

## 📞 **지원 및 문의**

- **이메일**: arne40@heal7.com
- **전화**: 050-7722-7328
- **문서**: [REFERENCE_LIBRARY 참조](../../../../../../REFERENCE_LIBRARY/)

---

**💡 핵심 가치**: "한 번 작성으로 모든 기관 대응" - AI가 24시간 정부 포털을 모니터링하여 사용자가 "SBA에서 떨어진 사업계획서를 KOSMES에 다시 내야 해요"라는 고민을 완전히 해결합니다.

*🎉 이제 정부 지원사업 신청이 더 이상 번거롭지 않습니다!*