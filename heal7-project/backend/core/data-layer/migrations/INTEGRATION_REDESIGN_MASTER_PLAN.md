# 🏗️ HEAL7 데이터베이스 재구성 후 백엔드 연동 재설정 마스터 플랜

> **작성일**: 2025-08-29  
> **상태**: 기획 완료, 실행 대기  
> **예상 소요 시간**: 3-4시간  
> **위험도**: 중간 (백업 완료)

---

## 📋 **현재 상황 분석**

### 🔴 **주요 변경사항**
1. **heal7_saju** → **heal7.saju_service** 이관 완료
2. **public 스키마 혼재** → **7개 서비스별 스키마** 분리
3. **새로운 고급 스키마** 적용 (240줄 사주 + 450줄 꿈풀이)
4. **Redis 네임스페이스** 재구성 (DB 0-6)

### 🔍 **영향도 분석 결과**

#### **High Impact (긴급 수정 필요)**
- **데이터베이스 연결 설정**: `psycopg2`, `asyncpg` 사용 모듈 (10개 파일)
- **SQL 쿼리 경로**: `public.` → `스키마명.` 변경 필요
- **ORM/쿼리 빌더**: 스키마 접두사 추가 필요

#### **Medium Impact (점진적 수정)**
- **캐시 키 구조**: Redis 네임스페이스 변경
- **마이그레이션 스크립트**: 기존 스키마 참조 수정
- **테스트 코드**: Mock 데이터 경로 업데이트

#### **Low Impact (추후 최적화)**
- **로깅 및 모니터링**: 스키마 정보 포함
- **문서화**: API 스키마 참조 업데이트

---

## 🎯 **백엔드 연동 재설정 기획**

### **Phase 1: 즉시 수정 (서비스 중단 위험 방지)**

#### **1.1 데이터베이스 연결 설정 수정**
```python
# 기존 (문제)
DATABASE_URL = "postgresql://user:pass@localhost/heal7_saju"

# 신규 (해결)
DATABASE_URL = "postgresql://user:pass@localhost/heal7"
DEFAULT_SCHEMA = "saju_service"  # 서비스별 설정
```

#### **1.2 테이블 참조 경로 수정**
```sql
-- 기존 (문제)
SELECT * FROM users;
SELECT * FROM kasi_cache;

-- 신규 (해결) 
SELECT * FROM shared_common.users;
SELECT * FROM saju_service.kasi_cache;
```

### **Phase 2: 점진적 개선 (기능 향상)**

#### **2.1 스키마별 연결 관리자 구현**
```python
class SchemaAwareDBManager:
    def __init__(self):
        self.schema_mapping = {
            'users': 'shared_common',
            'saju_charts': 'saju_service', 
            'dream_interpretations': 'dream_service',
            # ... 전체 매핑
        }
    
    def get_table_with_schema(self, table_name: str) -> str:
        schema = self.schema_mapping.get(table_name, 'public')
        return f"{schema}.{table_name}"
```

#### **2.2 Redis 네임스페이스 재설정**
```python
# 기존
redis.set("saju:cache:key", data)

# 신규
redis.set("saju_service:cache:key", data)  # DB 1
redis.set("shared_common:session:key", data)  # DB 0
```

### **Phase 3: 최적화 및 확장**

#### **3.1 동적 스키마 라우팅**
- 서비스별 자동 스키마 선택
- 쿼리 성능 최적화 적용
- 장애 복구 매커니즘 구현

#### **3.2 큐브별 독립 연결 풀**
- 서비스별 독립적인 DB 연결
- 부하 분산 및 격리
- 모니터링 및 알림 체계

---

## 🛠️ **구체적 실행 계획**

### **Step 1: 중요 서비스 먼저 수정 (30분)**
1. **사주 서비스** (포트 8003)
   - `/app/core/engines/saju_system/saju_data_manager.py`
   - 테이블 경로: `saju_service.*`
   
2. **관리자 서비스** (포트 8006)  
   - `/services/dashboard-service/api-gateway-cube/modules/user_management.py`
   - 테이블 경로: `shared_common.users`

### **Step 2: 설정 파일 통합 업데이트 (20분)**
```yaml
# config/database.yaml
databases:
  heal7:
    host: localhost
    port: 5432
    database: heal7
    schemas:
      shared_common: {tables: [users, attachments]}
      saju_service: {tables: [saju_charts, kasi_cache]}
      dream_service: {tables: [dream_categories]}
      # ... 전체 매핑
```

### **Step 3: 연결 테스트 및 검증 (30분)**
```python
# 테스트 스크립트
async def test_all_schema_connections():
    for schema in ['shared_common', 'saju_service', 'dream_service']:
        try:
            result = await db.fetch(f"SELECT 1 FROM {schema}.* LIMIT 1")
            print(f"✅ {schema}: OK")
        except Exception as e:
            print(f"❌ {schema}: {e}")
```

### **Step 4: 단계적 서비스 재시작 (60분)**
1. **사주 서비스 재시작** → 기능 테스트
2. **관리자 서비스 재시작** → 사용자 관리 테스트  
3. **크롤링 서비스 재시작** → 데이터 수집 테스트
4. **전체 통합 테스트**

---

## 🚨 **리스크 관리**

### **롤백 계획**
```bash
# 긴급 롤백 시 
sudo -u postgres psql heal7 < /home/ubuntu/heal7-project/backend/database-migration/backups/heal7_backup_20250829_140418.sql
```

### **부분 장애 대응**
- **서비스별 독립 실행**: 한 스키마 문제가 전체에 영향 안 줌
- **Graceful Degradation**: Mock 데이터로 일시 대체
- **실시간 모니터링**: 각 스키마별 상태 체크

### **데이터 무결성 보장**
- **Foreign Key 제약**: 스키마 간 참조 관계 유지
- **트랜잭션 경계**: 다중 스키마 작업 시 원자성 보장
- **백업 자동화**: 매일 스키마별 백업

---

## 📊 **성공 지표**

### **기술적 지표**
- ✅ **모든 서비스 정상 기동** (8003, 8006 포트)
- ✅ **API 응답 시간** < 2초 유지
- ✅ **데이터베이스 연결 오류** 0건
- ✅ **스키마별 쿼리 성공률** 99% 이상

### **비즈니스 지표**
- ✅ **사주 계산 기능** 정상 작동
- ✅ **사용자 로그인/관리** 정상 작동  
- ✅ **관리자 대시보드** 접근 가능
- ✅ **데이터 수집/크롤링** 지속 실행

---

## 🎉 **기대 효과**

### **즉시 효과**
- **체계적인 데이터 관리**: 서비스별 명확한 분리
- **확장성 향상**: 새 서비스 추가 용이
- **유지보수 효율성**: 스키마별 독립적 관리

### **장기 효과**  
- **성능 최적화**: 스키마별 인덱스 전략
- **보안 강화**: 스키마별 접근 권한 관리
- **모니터링 고도화**: 서비스별 상세 추적

---

**🚀 준비 완료! 실행 명령 대기 중**