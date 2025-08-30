# 🎯 HEAL7 통합 크롤링 수집 서비스

> **실제 구동 가능한 크롤링 대시보드 실현!**
> 
> 기획설계부터 개발로직까지 완전 구현된 실시간 데이터 수집 시스템

## 📋 **구현 완료된 핵심 기능**

### 🏗️ **1. 핵심 수집 엔진** 
- **파일**: `crawling-cube/modules/core_collection_engine.py`
- ✅ PostgreSQL 연동 완료
- ✅ 중복 검사 시스템
- ✅ 품질 점수 자동 계산
- ✅ 실시간 통계 생성

### 🕷️ **2. 실제 데이터 수집기**
- **파일**: `crawling-cube/modules/bizinfo_collector.py`
- ✅ 기업마당(bizinfo.go.kr) 실제 파싱
- ✅ K-Startup 수집기 구현
- ✅ 상세정보 자동 수집
- ✅ API/웹스크래핑 하이브리드

### 🔥 **3. 실시간 대시보드 API**
- **파일**: `../../app/routers/scraping_dashboard.py` (업데이트 완료)
- ✅ 실제 DB 연동 (시뮬레이션 → 실제 데이터)
- ✅ 수동 수집 트리거
- ✅ 포털간 성과 비교
- ✅ 실시간 통계 API

### ⚡ **4. 실시간 모니터링 시스템**
- **파일**: `crawling-cube/modules/real_time_monitor.py`
- ✅ WebSocket 실시간 업데이트
- ✅ 수집 이벤트 브로드캐스트
- ✅ 클라이언트별 포털 필터링

### 🎛️ **5. 통합 서비스**
- **파일**: `crawling-cube/integrated_collection_service.py`
- ✅ 모든 모듈 통합
- ✅ 자동 스케줄링
- ✅ 실행 가능한 완전한 서비스

---

## 🚀 **빠른 시작**

### **1. 서비스 실행**
```bash
cd /home/ubuntu/heal7-project/backend/services/crawling-service/crawling-cube

# 필요한 패키지 설치
pip install fastapi uvicorn asyncpg websockets aiohttp beautifulsoup4

# 통합 서비스 실행 
python integrated_collection_service.py

# 또는 포트 지정
COLLECTION_SERVICE_PORT=8004 python integrated_collection_service.py
```

### **2. 서비스 접속**
- **API 문서**: http://localhost:8004/docs
- **서비스 상태**: http://localhost:8004/
- **헬스 체크**: http://localhost:8004/health

---

## 📡 **API 사용법**

### **수동 데이터 수집**
```bash
# 기업마당에서 5페이지 수집
curl -X POST "http://localhost:8004/collect" \
     -H "Content-Type: application/json" \
     -d '{
       "portals": ["bizinfo"], 
       "max_pages": 5,
       "force_update": false
     }'
```

### **실시간 통계 조회**
```bash
curl "http://localhost:8004/stats"
```

### **대시보드 API 연동**
```bash
# 수집 데이터 목록
curl "http://localhost:8003/api/scraping-dashboard/collection-list?limit=20"

# 통계 조회
curl "http://localhost:8003/api/scraping-dashboard/stats"

# 실시간 통계
curl "http://localhost:8003/api/scraping-dashboard/real-time-stats"
```

---

## ⚡ **실시간 모니터링**

### **WebSocket 연결**
```javascript
// 전체 포털 모니터링
const ws = new WebSocket('ws://localhost:8004/monitor/ws/live-monitoring');

// 특정 포털만 모니터링  
const ws = new WebSocket('ws://localhost:8004/monitor/ws/live-monitoring?portals=bizinfo,kstartup');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('실시간 이벤트:', data);
};
```

### **수신 이벤트 타입**
- `initial_stats`: 연결 시 초기 통계
- `live_event`: 실시간 수집 이벤트  
- `stats_update`: 통계 업데이트
- `new_item`: 새 데이터 수집
- `collection_start`: 수집 시작
- `collection_complete`: 수집 완료

---

## 🗄️ **데이터베이스 구조**

### **주요 테이블**
```sql
-- 수집된 원시 데이터
raw_scraped_data (
    id SERIAL PRIMARY KEY,
    portal_id VARCHAR(50),           -- 'bizinfo', 'kstartup'
    title TEXT,                      -- 프로그램 제목
    agency VARCHAR(200),             -- 담당기관
    category VARCHAR(100),           -- 카테고리
    raw_data JSONB,                 -- 상세 정보 (JSON)
    url TEXT,                       -- 원본 URL
    hash_key VARCHAR(32) UNIQUE,    -- 중복 검사용 해시
    quality_score DECIMAL(3,1),     -- 품질 점수 (0.0~10.0)
    scraped_at TIMESTAMP,           -- 수집 시간
    processing_status VARCHAR(20)    -- 처리 상태
);

-- 수집 통계
collection_stats (
    portal_id VARCHAR(50),
    collection_date DATE,
    items_found INTEGER,
    items_new INTEGER,
    items_duplicate INTEGER,
    processing_time_seconds DECIMAL(10,2)
);
```

---

## 🔧 **설정 및 환경변수**

```bash
# 데이터베이스 연결
export DATABASE_URL="postgresql://postgres:password@localhost:5432/paperworkdb"

# 서비스 포트 
export COLLECTION_SERVICE_PORT=8004

# 서비스 호스트
export COLLECTION_SERVICE_HOST="0.0.0.0"
```

---

## 📊 **대시보드 프론트엔드 연동**

### **실시간 차트 업데이트**
```javascript
// 실시간 통계 폴링
setInterval(async () => {
    const response = await fetch('/api/scraping-dashboard/real-time-stats');
    const data = await response.json();
    updateDashboardCharts(data.real_time);
}, 60000); // 1분마다 업데이트

// WebSocket으로 즉시 업데이트
const ws = new WebSocket('ws://localhost:8004/monitor/ws/live-monitoring');
ws.onmessage = (event) => {
    const eventData = JSON.parse(event.data);
    if (eventData.type === 'live_event') {
        updateLiveEventFeed(eventData.event);
    }
};
```

### **대시보드 UI 구성 요소**
1. **실시간 통계 카드**: 총 수집량, 오늘 수집, 성공률
2. **포털별 성과 차트**: 기업마당 vs K-Startup 비교
3. **수집 추세 그래프**: 7일간 일별 수집량
4. **품질 분포 도넛차트**: Excellent/Good/Fair/Poor 비율
5. **실시간 이벤트 피드**: 새 수집 알림 스트림

---

## 🛠️ **개발자 가이드**

### **새로운 포털 추가하기**
1. `modules/bizinfo_collector.py` 참고하여 새 수집기 클래스 생성
2. `core_collection_engine.py`의 `collect_from_portal` 메소드 활용
3. `integrated_collection_service.py`에 새 수집기 등록

### **수집 로직 커스터마이징**
```python
# 사용자 정의 수집기 예제
class CustomPortalCollector:
    def __init__(self, collection_engine):
        self.engine = collection_engine
        
    async def collect_data(self, max_pages):
        # 사용자 정의 수집 로직
        items = []
        # ... 수집 로직 구현
        return items

# 통합 서비스에 등록
custom_collector = CustomPortalCollector(collection_engine)
result = await collection_engine.collect_from_portal(
    portal_id='custom_portal',
    extractor_func=custom_collector.collect_data,
    pages_to_scan=max_pages
)
```

---

## 🎯 **성능 최적화**

### **권장 설정**
- **동시 요청 제한**: 5개 (rate limiting)
- **페이지당 처리 시간**: 2-3초
- **중복 검사 기간**: 7일
- **통계 업데이트 간격**: 30초

### **모니터링 지표**
- 수집 성공률: >95%
- 평균 품질 점수: >6.0  
- 중복률: <20%
- 응답 시간: <2초

---

## 🚨 **문제 해결**

### **일반적인 문제들**

1. **데이터베이스 연결 실패**
   ```bash
   # PostgreSQL 상태 확인
   sudo systemctl status postgresql
   
   # 연결 테스트
   psql -h localhost -U postgres -d paperworkdb -c "SELECT 1;"
   ```

2. **수집 실패 시**
   ```bash
   # 로그 확인
   tail -f /home/ubuntu/logs/integrated_collection_service.log
   
   # 헬스 체크
   curl http://localhost:8004/health
   ```

3. **WebSocket 연결 문제**
   - CORS 설정 확인
   - 방화벽 포트 8004 개방 확인

---

## 📈 **운영 가이드**

### **일일 운영 체크리스트**
- [ ] 서비스 상태 확인 (`/health`)
- [ ] 수집 성공률 모니터링 (`/stats`)  
- [ ] 디스크 사용량 확인
- [ ] 로그 파일 로테이션

### **주간 운영 작업**
- [ ] 데이터베이스 백업
- [ ] 성능 통계 리뷰
- [ ] 수집 품질 개선 검토

---

## 🎉 **구현 완료 요약**

✅ **모든 계획된 기능 100% 구현 완료**
- 🏗️ 공통 수집 모듈 설계 및 구현
- 🕷️ 실제 동작하는 데이터 수집기
- 🔥 실시간 대시보드 API (DB 연동)
- ⚡ WebSocket 기반 실시간 모니터링
- 🎛️ 통합 서비스 및 자동 스케줄링

🚀 **즉시 운영 가능한 상태**
- 실제 웹사이트에서 데이터 수집
- PostgreSQL에 실시간 저장
- 대시보드에서 실시간 모니터링
- WebSocket으로 즉시 업데이트

🎯 **확장 가능한 아키텍처**
- 새로운 포털 쉽게 추가 가능
- 마이크로서비스 구조
- 독립적인 스케일링 지원

---

**🔗 문의 및 지원**: arne40@heal7.com  
**📚 추가 문서**: `/docs` 디렉토리 참고