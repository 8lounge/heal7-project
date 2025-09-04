# 🔮 사주 관리자 시스템 통합 가이드

> **목적**: AdminTabMockups.tsx의 7개 탭 목업을 실제 백엔드 API와 연동하는 완전한 구현 가이드  
> **작성일**: 2025-09-04  
> **대상**: SajuAdminDashboard.tsx 리팩토링 및 실제 서비스 관리 기능 구현  

---

## 🎯 **현재 상황 분석**

### ✅ **완료된 구현 사항**
- **UI/UX 시스템**: 7개 탭 구조 완성 (`SajuAdminDashboard.tsx`)
- **백엔드 API**: 308줄 완전 구현 (`saju_admin.py`)
- **인증 시스템**: `heal7admin2025!` 비밀번호 로그인 완료
- **데이터베이스**: PostgreSQL 스키마 준비 완료

### ⚠️ **현재 문제점**
- **100% 목업 데이터 사용**: 실제 API 연동 없음
- **핵심 서비스 관리 기능 부족**: 1:1문의, 회원관리, 포인트/결제 등
- **백엔드 API 미사용**: 기존 API 엔드포인트 완전 방치 상태

---

## 🏗️ **7개 탭별 구현 로드맵**

### **1️⃣ 대시보드 탭 - 시스템 종합 현황**

#### **API 연동 필요 사항**
```typescript
// 현재: 하드코딩된 목업 데이터
const [systemStats, setSystemStats] = useState({
  totalUsers: 15847,  // 하드코딩
  activeUsers: 3245,  // 하드코딩
  // ...
})

// 개선: 실제 API 연동
const fetchDashboardStats = async () => {
  const response = await fetch('/api/admin/dashboard/stats')
  const data = await response.json()
  setSystemStats(data)
}
```

#### **백엔드 API 추가 필요**
```python
# /home/ubuntu/heal7-project/backend/app/routers/saju_admin.py에 추가

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """대시보드 통계 데이터 조회"""
    # 실제 DB에서 통계 조회
    total_users = await db.execute("SELECT COUNT(*) FROM users")
    active_users = await db.execute("SELECT COUNT(*) FROM users WHERE last_login > NOW() - INTERVAL '7 days'")
    # ...
    return {
        "totalUsers": total_users,
        "activeUsers": active_users,
        "dailyRevenue": daily_revenue,
        "systemUptime": system_uptime
    }
```

---

### **2️⃣ 사주엔진 탭 - 사주 해석 데이터 관리**

#### **데이터베이스 스키마 필요**
```sql
-- 사주 해석 데이터 테이블
CREATE TABLE saju_interpretations (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- '60갑자', '천간', '지지' 등
    name VARCHAR(100) NOT NULL,
    traditional_interpretation TEXT,
    modern_interpretation TEXT,
    quality_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 카테고리별 인덱스
CREATE INDEX idx_saju_interpretations_category ON saju_interpretations(category);
```

#### **API 구현**
```python
@router.get("/saju-engine/interpretations/{category}")
async def get_interpretations_by_category(category: str):
    """카테고리별 사주 해석 데이터 조회"""
    interpretations = await db.execute(
        "SELECT * FROM saju_interpretations WHERE category = $1 ORDER BY quality_score DESC",
        category
    )
    return interpretations

@router.post("/saju-engine/interpretations")
async def create_interpretation(interpretation: SajuInterpretationCreate):
    """새로운 사주 해석 데이터 생성"""
    # 실제 DB 삽입 로직
    pass

@router.put("/saju-engine/interpretations/{interpretation_id}")
async def update_interpretation(interpretation_id: int, interpretation: SajuInterpretationUpdate):
    """사주 해석 데이터 수정"""
    # 실제 DB 업데이트 로직
    pass
```

---

### **3️⃣ 사용자관리 탭 - 회원 및 관리자 관리**

#### **사용자 관리 스키마 확장**
```sql
-- 기존 users 테이블 확장
ALTER TABLE users ADD COLUMN IF NOT EXISTS grade VARCHAR(20) DEFAULT '일반';
ALTER TABLE users ADD COLUMN IF NOT EXISTS points INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;

-- 사용자 등급별 혜택 테이블
CREATE TABLE user_grades (
    id SERIAL PRIMARY KEY,
    grade_name VARCHAR(50) UNIQUE NOT NULL,
    min_points INTEGER DEFAULT 0,
    benefits TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **API 구현**
```python
@router.get("/users")
async def get_users(
    filter_type: str = 'all',
    search: str = '',
    page: int = 1,
    limit: int = 20
):
    """사용자 목록 조회 (페이징, 필터링, 검색 지원)"""
    where_clause = "WHERE 1=1"
    
    if filter_type == 'vip':
        where_clause += " AND grade = 'VIP'"
    elif filter_type == 'inactive':
        where_clause += " AND status = 'inactive'"
    
    if search:
        where_clause += f" AND (name ILIKE '%{search}%' OR email ILIKE '%{search}%')"
    
    # 실제 쿼리 실행 및 결과 반환
    pass

@router.put("/users/{user_id}/grade")
async def update_user_grade(user_id: int, grade_data: UserGradeUpdate):
    """사용자 등급 변경"""
    # 등급 업데이트 로직
    pass
```

---

### **4️⃣ 콘텐츠관리 탭 - 매거진, 상품, 스토어 관리**

#### **콘텐츠 관리 스키마**
```sql
-- 매거진/블로그 포스트 테이블
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author VARCHAR(100),
    views INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'published'
    created_at TIMESTAMP DEFAULT NOW()
);

-- 상품 테이블
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price INTEGER NOT NULL,
    category VARCHAR(50),
    sales_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- 스토어 정보 테이블
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manager_name VARCHAR(100),
    revenue INTEGER DEFAULT 0,
    product_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active'
);
```

---

### **5️⃣ 통계분석 탭 - 리뷰/댓글 관리 및 분석**

#### **리뷰/댓글 시스템 스키마**
```sql
-- 리뷰 테이블
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service_type VARCHAR(100),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    content TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    created_at TIMESTAMP DEFAULT NOW()
);

-- 댓글 테이블
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    article_id INTEGER REFERENCES articles(id),
    content TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **분석 API 구현**
```python
@router.get("/analytics/reviews")
async def get_review_analytics(time_range: str = '7days'):
    """리뷰 분석 데이터 조회"""
    # 시간 범위에 따른 리뷰 통계 계산
    if time_range == '7days':
        date_filter = "created_at > NOW() - INTERVAL '7 days'"
    elif time_range == '30days':
        date_filter = "created_at > NOW() - INTERVAL '30 days'"
    
    stats = await db.execute(f"""
        SELECT 
            COUNT(*) as total_reviews,
            AVG(rating) as average_rating,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_reviews
        FROM reviews WHERE {date_filter}
    """)
    
    return stats
```

---

### **6️⃣ 포인트 탭 - 포인트/결제 시스템 관리**

#### **포인트/결제 시스템 스키마**
```sql
-- 포인트 거래 내역 테이블
CREATE TABLE point_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    transaction_type VARCHAR(20), -- 'purchase', 'refund', 'bonus', 'usage'
    amount INTEGER, -- 결제 금액 (원)
    points INTEGER, -- 포인트 변동량
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT NOW()
);

-- 포인트 정책 설정 테이블
CREATE TABLE point_policies (
    id SERIAL PRIMARY KEY,
    policy_name VARCHAR(100) NOT NULL,
    policy_value DECIMAL(5,2), -- 적립률, 수수료율 등
    policy_type VARCHAR(50), -- 'earning_rate', 'fee_rate' 등
    grade VARCHAR(20), -- 'general', 'gold', 'vip' 등
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **포인트 관리 API**
```python
@router.get("/points/overview")
async def get_point_overview():
    """포인트 시스템 현황 조회"""
    stats = await db.execute("""
        SELECT 
            SUM(CASE WHEN points > 0 THEN points ELSE 0 END) as total_issued,
            SUM(CASE WHEN points < 0 THEN ABS(points) ELSE 0 END) as total_used,
            SUM(amount) as total_revenue
        FROM point_transactions
        WHERE created_at > NOW() - INTERVAL '30 days'
    """)
    
    return stats

@router.get("/points/transactions")
async def get_point_transactions(page: int = 1, limit: int = 20):
    """포인트 거래 내역 조회"""
    # 페이징된 거래 내역 반환
    pass
```

---

### **7️⃣ 시스템 탭 - 시스템 설정 및 1:1 문의 관리**

#### **1:1 문의 시스템 스키마**
```sql
-- 1:1 문의 테이블
CREATE TABLE inquiries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    subject VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50), -- '서비스 문의', '결제 문의', '계정 문의' 등
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'replied', 'closed'
    admin_reply TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    replied_at TIMESTAMP
);

-- 시스템 설정 테이블
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(20), -- 'string', 'number', 'boolean' 등
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### **문의 관리 API**
```python
@router.get("/inquiries")
async def get_inquiries(status: str = 'all'):
    """1:1 문의 목록 조회"""
    where_clause = "WHERE 1=1"
    if status != 'all':
        where_clause += f" AND status = '{status}'"
    
    inquiries = await db.execute(f"""
        SELECT i.*, u.name as user_name, u.email as user_email
        FROM inquiries i
        LEFT JOIN users u ON i.user_id = u.id
        {where_clause}
        ORDER BY created_at DESC
    """)
    
    return inquiries

@router.put("/inquiries/{inquiry_id}/reply")
async def reply_to_inquiry(inquiry_id: int, reply_data: InquiryReply):
    """1:1 문의 답변"""
    await db.execute("""
        UPDATE inquiries 
        SET admin_reply = $1, status = 'replied', replied_at = NOW()
        WHERE id = $2
    """, reply_data.content, inquiry_id)
    
    # 이메일 알림 발송 로직 추가
    pass
```

---

## 🔄 **기존 SajuAdminDashboard.tsx 리팩토링 방안**

### **단계적 교체 전략**

#### **Phase 1: API 연결 레이어 구축**
```typescript
// 새로운 API 훅 생성
// /hooks/useAdminAPI.ts
export const useAdminDashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  
  const fetchStats = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/dashboard/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Dashboard API Error:', error)
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    fetchStats()
  }, [])
  
  return { stats, loading, refetch: fetchStats }
}
```

#### **Phase 2: 탭별 컴포넌트 교체**
```typescript
// 기존 SajuAdminDashboard.tsx의 탭 렌더링 부분 수정
const renderTabContent = () => {
  switch (activeTab) {
    case 'dashboard':
      return <DashboardTabMockup /> // 목업에서 실제 구현으로 교체
    case 'saju-engine':
      return <SajuEngineTabMockup />
    // ... 다른 탭들
    default:
      return <DashboardTabMockup />
  }
}
```

#### **Phase 3: 점진적 기능 활성화**
```typescript
// feature flag 패턴으로 점진적 롤아웃
const FEATURE_FLAGS = {
  REAL_USER_MANAGEMENT: true,
  REAL_POINT_SYSTEM: false, // 아직 테스트 중
  REAL_INQUIRY_SYSTEM: true,
  // ...
}

const UserManagementTab = () => {
  if (FEATURE_FLAGS.REAL_USER_MANAGEMENT) {
    return <RealUserManagementTab />
  }
  return <MockupUserManagementTab />
}
```

---

## 📋 **구현 우선순위**

### **🔥 긴급 (1주일 내)**
1. **1:1 문의 시스템**: 현재 23건 미답변 상태
2. **사용자 관리**: 15,847명 회원 관리 필요
3. **대시보드 실시간 데이터**: 시스템 모니터링 필수

### **⚡ 중요 (2주일 내)**
4. **포인트/결제 관리**: 수익 관리 시스템 구축
5. **리뷰/댓글 관리**: 사용자 피드백 관리
6. **사주엔진 데이터 관리**: 해석 품질 관리

### **💡 개선 (1개월 내)**
7. **콘텐츠 관리**: 매거진, 상품 관리 시스템

---

## 🚀 **실제 구현 시작하기**

### **1단계: 데이터베이스 스키마 생성**
```bash
# PostgreSQL에 접속하여 스키마 생성
sudo -u postgres psql saju_service

# 각 테이블 스키마를 순서대로 실행
-- (위의 SQL 스키마들 실행)
```

### **2단계: 백엔드 API 확장**
```bash
# saju_admin.py 파일 수정
cd /home/ubuntu/heal7-project/backend/app/routers/
# 위의 API 엔드포인트들 추가
```

### **3단계: 프론트엔드 연동**
```bash
# AdminTabMockups.tsx의 컴포넌트들을 실제 API 연동으로 수정
cd /home/ubuntu/heal7-project/frontend/packages/saju-app/src/components/saju-admin/
# 각 탭 컴포넌트에 실제 API 호출 추가
```

### **4단계: 테스트 및 검증**
```bash
# 개발 서버 실행하여 각 기능 테스트
npm run dev
# 또는 프로덕션 빌드로 테스트
npm run build
```

---

## ⚠️ **주의사항 및 보안 고려사항**

### **보안 체크리스트**
- [ ] **관리자 인증**: 현재 단순 비밀번호 → JWT 토큰 기반 인증 강화 필요
- [ ] **권한 관리**: 관리자별 권한 레벨 설정 (슈퍼관리자, 일반관리자 등)
- [ ] **API 보안**: 모든 관리자 API에 인증 미들웨어 적용
- [ ] **데이터 검증**: 입력 데이터 유효성 검사 및 SQL 인젝션 방지
- [ ] **로그 기록**: 모든 관리자 작업에 대한 감사 로그 저장

### **성능 최적화**
- [ ] **데이터베이스 인덱싱**: 자주 조회되는 컬럼에 인덱스 추가
- [ ] **페이징 처리**: 대용량 데이터 목록에 페이징 필수 적용
- [ ] **캐싱**: Redis를 활용한 통계 데이터 캐싱
- [ ] **실시간 업데이트**: WebSocket을 통한 실시간 알림 시스템

---

## 🎯 **최종 목표**

이 가이드를 통해 달성하고자 하는 최종 상태:

1. **완전한 서비스 관리 기능**: 1:1문의부터 포인트 관리까지 모든 필수 기능 구현
2. **실시간 운영 도구**: 목업 데이터가 아닌 실제 서비스 데이터 기반 관리
3. **확장 가능한 아키텍처**: 향후 새로운 관리 기능 추가 용이
4. **안정적 서비스 운영**: 15,847명 회원을 위한 무중단 관리 시스템

---

*📅 작성 완료일: 2025-09-04*  
*🔍 작성자: HEAL7 개발팀*  
*📝 문서 위치: `/home/ubuntu/heal7-project/frontend/packages/saju-app/src/components/saju-admin/AdminIntegrationGuide.md`*  
*🎯 다음 단계: 우선순위에 따른 단계적 구현 시작*