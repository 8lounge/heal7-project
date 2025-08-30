# 🎼 HEAL7 오케스트레이션 허브 (Cube Dashboard Service)

> **포트**: 8015 (마스터 포트)  
> **역할**: 5개 서비스 중앙 관리 및 워크플로우 오케스트레이션  
> **상태**: ✅ 운영 중

## 🎯 **핵심 기능**

### **1. 서비스 오케스트레이션**
```bash
# 5개 관리 서비스 자동 시작/중지/상태 관리
POST /orchestration/start-all     # 모든 서비스 시작
POST /orchestration/stop-all      # 모든 서비스 중지  
GET  /orchestration/status        # 서비스 상태 조회
```

### **2. 통합 대시보드**
```bash
# 시각적 관리 인터페이스
GET /dashboard                    # 워크플로우 대시보드
GET /dashboard/services          # 서비스 상태 대시보드
GET /dashboard/metrics           # 성능 메트릭 대시보드
```

### **3. 워크플로우 관리**
```yaml
# 등록된 기본 워크플로우
saju_processing:        # 사주 처리 워크플로우
  - saju-service → ai-monitoring-service
  - test-service (품질 검증)

document_automation:    # 문서 자동화 워크플로우  
  - paperwork-service → crawling-service
  - ai-monitoring-service (성능 추적)

data_collection:        # 데이터 수집 워크플로우
  - crawling-service → ai-monitoring-service
  - test-service (데이터 검증)
```

## 🚀 **실행 방법**

### **오케스트레이션 허브 시작**
```bash
cd services/dashboard-service
python main.py
# → 포트 8015에서 실행
```

### **전체 시스템 시작** (권장)
```bash
# 오케스트레이션 스크립트 사용
bash scripts/start_heal7_services.sh

# 또는 REST API 사용
curl -X POST http://localhost:8015/orchestration/start-all
```

## 🔗 **주요 엔드포인트**

### **헬스체크**
```bash
curl http://localhost:8015/health
# Response: {"status":"healthy","role":"orchestration_hub","managed_services":5}
```

### **서비스 상태**
```bash
curl http://localhost:8015/orchestration/status  
# Response: {"orchestration_hub":"active","total_services":5}
```

### **대시보드 접근**
```bash
# 브라우저에서 접근
http://localhost:8015/dashboard
```

## 🏗️ **아키텍처 구조**

```
dashboard-service/              # 🎼 오케스트레이션 서비스
├── main.py                     # FastAPI 메인 애플리케이션
├── orchestration/              # 오케스트레이션 로직
│   └── SimpleOrchestrator     # 서비스 관리 클래스
├── admin-dashboard-cube/       # 🧊 관리자 대시보드 큐브
├── api-gateway-cube/           # 🧊 API 게이트웨이 큐브
├── auth-security-cube/         # 🧊 인증/보안 큐브
├── config-management-cube/     # 🧊 설정 관리 큐브
└── management-dashboard-cube/  # 🧊 관리 대시보드 큐브
```

## 🎼 **오케스트레이션 원리**

### **서비스 디스커버리**
- 5개 관리 서비스 자동 인식 (포트 8010-8014)
- 실시간 서비스 상태 모니터링
- 자동 장애 감지 및 복구 시도

### **워크플로우 엔진**
- 서비스 간 의존성 관리
- 순차적/병렬 작업 처리
- 실패 시 롤백 메커니즘

### **중앙집중 설정**
- 모든 서비스 설정 통합 관리
- 런타임 설정 변경 지원
- 환경별 설정 프로필 관리

## 📊 **관리되는 서비스**

1. **paperwork-service** (8010) - 서류 처리
2. **test-service** (8011) - 테스트 환경  
3. **saju-service** (8012) - 사주 시스템
4. **crawling-service** (8013) - 데이터 수집
5. **ai-monitoring-service** (8014) - AI 모니터링

## 🔧 **설정**

### **config.yaml**
```yaml
orchestration:
  managed_services:
    - name: "paperwork-service"
      port: 8010
      health_endpoint: "/health"
    - name: "test-service" 
      port: 8011
      health_endpoint: "/health"
    # ... 기타 서비스들

workflows:
  saju_processing:
    steps:
      - service: "saju-service"
        action: "calculate"
      - service: "ai-monitoring-service"
        action: "monitor"
```

## 🔍 **모니터링**

### **실시간 상태 추적**
- 서비스별 헬스체크 상태
- 포트 사용률 및 응답 시간
- 워크플로우 실행 상태

### **로그 통합**
- 모든 관리 서비스 로그 중앙 집중
- 오류 발생 시 자동 알림
- 성능 메트릭 수집 및 분석

---

**🎯 핵심**: 이 허브를 통해 HEAL7의 모든 백엔드 서비스를 중앙에서 조율합니다!  
**📍 접근**: http://localhost:8015/dashboard