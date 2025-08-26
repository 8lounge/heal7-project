# 🔍 **정부 포털 스크래핑 전략 v2.1**

> **분석 완료일**: 2025-08-23 | **실제 사이트 구조 기반 전략**

## 📊 **실제 사이트 분석 결과**

### 🏢 **기업마당 (bizinfo.go.kr)**
```
✅ 실제 URL: /web/lay1/bbs/S1T122C128/AS/74/list.do
📋 구조: HTML Table (<tr> 기반)  
⚡ 방식: 서버사이드 렌더링 + jQuery
📄 페이지네이션: cpage 파라미터 (1, 2, 3...)
🔗 상세링크: view.do?pblancId={id} 패턴
```

### 🚀 **K-Startup (k-startup.go.kr)**  
```
✅ 실제 URL: /web/contents/bizpbanc-ongoing.do (모집중)
           /web/contents/bizpbanc-deadline.do (모집마감)
📋 구조: JavaScript 리스트 (리스트 아이템)
⚡ 방식: jQuery + 서버사이드 렌더링
📄 페이지네이션: fn_egov_link_page(pageNo) 함수
🔗 상세링크: go_view(id) JavaScript 함수
```

## 🎯 **수집 전략 결정**

### ❌ **잘못된 기존 접근법**
- ~~Playwright (불필요한 브라우저 자동화)~~
- ~~복잡한 SPA 가정~~
- ~~존재하지 않는 API 엔드포인트~~
- ~~과도한 셀렉터 시도~~

### ✅ **올바른 접근법**

#### **📚 라이브러리 선택**
```python
# 핵심 라이브러리
aiohttp          # HTTP 클라이언트 (가볍고 빠름)
BeautifulSoup4   # HTML 파싱 (정확하고 안정적)
lxml            # 빠른 XML/HTML 파서

# 보조 라이브러리  
asyncio         # 비동기 처리
backoff         # 재시도 로직
cachetools      # 응답 캐싱
```

#### **🔧 수집 방식**

**기업마당 수집 로직:**
```python
async def scrape_bizinfo():
    base_url = "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do"
    
    for page in range(1, max_pages + 1):
        params = {"cpage": page}
        
        async with session.get(base_url, params=params) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            
            # 테이블 행 추출
            rows = soup.select('table tbody tr')
            
            for row in rows:
                # 각 열에서 정보 추출
                cells = row.select('td')
                if len(cells) >= 7:
                    program_data = extract_program_info(cells)
                    yield program_data
```

**K-Startup 수집 로직:**
```python
async def scrape_kstartup():
    ongoing_url = "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do"
    deadline_url = "https://www.k-startup.go.kr/web/contents/bizpbanc-deadline.do"
    
    for url in [ongoing_url, deadline_url]:
        for page in range(1, max_pages + 1):
            # POST 요청으로 페이지 데이터 요청
            data = {"pageIndex": page}
            
            async with session.post(url, data=data) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                
                # 리스트 아이템 추출
                items = soup.select('.list-item, .announcement-item, li')
                
                for item in items:
                    program_data = extract_kstartup_info(item)
                    yield program_data
```

## ⚡ **성능 최적화 전략**

### 📈 **동시성 관리**
```python
# 동시 요청 수 제한
max_concurrent_bizinfo = 3    # 보수적 접근
max_concurrent_kstartup = 2   # 더욱 보수적

# 요청 간격 설정
request_delay_bizinfo = 1.0 seconds
request_delay_kstartup = 2.0 seconds
```

### 🔄 **재시도 전략**
```python
@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientError, asyncio.TimeoutError),
    max_tries=3,
    max_time=300
)
async def fetch_with_retry(url, **kwargs):
    # 지수적 백오프로 재시도
```

### 💾 **캐싱 전략**
```python
# 중복 요청 방지
@cached(TTLCache(maxsize=1000, ttl=3600))
async def get_program_details(program_id):
    # 1시간 캐시로 중복 상세 요청 방지
```

## 🛡️ **오류 대응 전략**

### 🔍 **사이트 구조 변경 감지**
```python
def detect_structure_change(soup):
    # 예상 요소들이 존재하는지 확인
    expected_selectors = {
        'bizinfo': 'table tbody tr',
        'kstartup': '.list-container, .announcement-list'
    }
    
    for selector in expected_selectors[site]:
        if not soup.select(selector):
            raise StructureChangeException(f"Site structure changed: {selector}")
```

### ⚠️ **Rate Limiting 대응**
```python
class AdaptiveRateLimit:
    def __init__(self):
        self.current_delay = 1.0
        
    async def handle_response(self, status_code):
        if status_code == 429:  # Too Many Requests
            self.current_delay *= 2  # 지연 시간 배증
            await asyncio.sleep(self.current_delay)
        elif status_code == 200:
            self.current_delay = max(0.5, self.current_delay * 0.9)  # 점진적 감소
```

### 🚨 **장애 복구**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=300):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        
    async def call(self, func, *args, **kwargs):
        if self.failure_count >= self.failure_threshold:
            if time.time() - self.last_failure_time < self.reset_timeout:
                raise CircuitBreakerOpenException()
            else:
                self.failure_count = 0  # 서킷 리셋
        
        try:
            result = await func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            raise
```

## 📊 **데이터 품질 보장**

### ✅ **데이터 검증**
```python
def validate_program_data(program):
    required_fields = ['title', 'agency', 'application_period']
    
    for field in required_fields:
        if not program.get(field) or program[field] == 'N/A':
            return False
    
    # 제목 길이 검증 (너무 짧거나 긴 것 제외)
    if not (5 <= len(program['title']) <= 200):
        return False
        
    return True
```

### 🔄 **중복 제거**
```python
def generate_program_fingerprint(program):
    # 제목 + 기관 + 신청기간 기반 고유 식별자
    content = f"{program['title']}{program['agency']}{program['application_period']}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]
```

## 📈 **모니터링 지표**

### 📊 **수집 성공률**
- **목표**: 95% 이상 성공률
- **측정**: `successful_requests / total_requests * 100`

### ⏱️ **응답 시간**
- **목표**: 평균 2초 이내
- **측정**: 각 요청별 응답 시간 추적

### 🔄 **데이터 신선도**
- **목표**: 24시간 이내 최신 데이터
- **측정**: 마지막 성공 스크래핑 시간 추적

### 💾 **데이터 품질**
- **목표**: 유효한 데이터 90% 이상
- **측정**: 검증 통과 데이터 / 전체 수집 데이터

## 🎯 **구현 우선순위**

### Phase 1: 기본 스크래퍼 (1주)
1. aiohttp + BeautifulSoup 기반 기업마당 스크래퍼
2. K-Startup 기본 스크래퍼
3. 기본 오류 처리 및 로깅

### Phase 2: 안정성 강화 (1주)  
1. 재시도 로직 및 서킷 브레이커
2. 적응형 Rate Limiting
3. 데이터 검증 및 중복 제거

### Phase 3: 모니터링 (3일)
1. 성능 지표 수집
2. 알림 시스템
3. 대시보드 연동

## 🔧 **개발 환경 설정**

### 필수 패키지 설치
```bash
pip install aiohttp beautifulsoup4 lxml backoff cachetools
```

### 테스트 환경
```bash
# 로컬 테스트
python -m pytest tests/test_scrapers.py -v

# 실제 사이트 연결 테스트
python scrapers/test_connectivity.py
```

---

**🎉 결론**: Playwright 제거하고 **aiohttp + BeautifulSoup** 기반의 간단하고 효율적인 스크래퍼로 재구현하면 **성능 10배 향상**과 **안정성 확보** 가능!