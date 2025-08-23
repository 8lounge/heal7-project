# 🚀 HEAL7 사주사이트 백엔드 API 아키텍처 v1.0

> **프로젝트**: HEAL7 사주사이트 백엔드 시스템 설계  
> **버전**: v1.0.0  
> **설계일**: 2025-08-18  
> **최종 수정**: 2025-08-18 15:00 KST  
> **설계자**: HEAL7 Backend Architecture Team  
> **목표**: 모듈러 마이크로서비스 기반 확장 가능한 백엔드 시스템

## 🏗️ **시스템 아키텍처 개요**

### **🎯 설계 원칙**
- **모듈러 마이크로서비스**: 각 운세 서비스별 독립적 배포
- **API-First 설계**: 프론트엔드와 완전 분리
- **확장성 우선**: 수평적 확장 가능한 구조
- **장애 격리**: 한 서비스 장애가 전체에 영향 없음
- **데이터 일관성**: ACID 보장과 최종 일관성의 균형

### **🔧 기술 스택**
```yaml
# 🛠️ Technology Stack
api_gateway: "Kong Gateway / Traefik"
backend: "FastAPI 0.104+ (Python 3.11+)"
database: 
  primary: "PostgreSQL 16"
  cache: "Redis 7.0"
  search: "ElasticSearch 8.0"
  nosql: "MongoDB 7.0"
queue: "RabbitMQ / Celery + Redis"
monitoring: "Prometheus + Grafana"
logging: "ELK Stack"
containerization: "Docker + Kubernetes"
```

## 🌐 **API 게이트웨이 설계**

### **🚦 게이트웨이 구성**
```yaml
# 🌐 API Gateway Configuration
api_gateway:
  port: 80/443
  ssl: "Let's Encrypt + Cloudflare"
  
  # 🔐 인증 & 보안
  authentication:
    jwt_validation: true
    oauth2_providers: ["google", "kakao", "naver", "apple"]
    rate_limiting:
      anonymous: "100/hour"
      authenticated: "1000/hour"
      premium: "10000/hour"
  
  # 🚥 라우팅 규칙
  routing:
    "/api/v1/auth/*": "auth-service:8001"
    "/api/v1/saju/*": "saju-service:8100"
    "/api/v1/tarot/*": "tarot-service:8101"
    "/api/v1/zodiac/*": "zodiac-service:8102"
    "/api/v1/astrology/*": "astrology-service:8103"
    "/api/v1/fengshui/*": "fengshui-service:8104"
    "/api/v1/constitution/*": "constitution-service:8105"
    "/api/v1/community/*": "community-service:8200"
    "/api/v1/commerce/*": "commerce-service:8300"
    "/api/v1/payment/*": "payment-service:8301"
    "/api/v1/subscription/*": "subscription-service:8302"
    "/api/v1/analytics/*": "analytics-service:8400"
    "/api/v1/notifications/*": "notification-service:8500"
    "/api/v1/users/*": "user-service:8501"
    "/api/v1/files/*": "file-service:8502"
  
  # 📊 로드밸런싱
  load_balancing:
    algorithm: "least_connections"
    health_checks: 
      interval: "10s"
      timeout: "5s"
      retries: 3
  
  # 🛡️ 보안 헤더
  security_headers:
    cors_enabled: true
    csrf_protection: true
    content_security_policy: "strict"
    rate_limit_headers: true
```

### **🔐 인증 & 인가 시스템**
```python
# 🛡️ Authentication & Authorization Service
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(hours=24)
        self.refresh_token_expire = timedelta(days=30)
    
    # 🎫 JWT 토큰 생성
    def create_access_token(self, user_id: int, scopes: List[str]) -> str:
        payload = {
            "user_id": user_id,
            "scopes": scopes,
            "exp": datetime.utcnow() + self.access_token_expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    # 🔄 토큰 갱신
    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + self.refresh_token_expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    # ✅ 토큰 검증
    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                raise HTTPException(status_code=401, detail="Invalid token type")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

# 🎯 권한 스코프 정의
class Scopes:
    # 🔮 운세 서비스 권한
    SAJU_READ = "saju:read"
    SAJU_PREMIUM = "saju:premium" 
    TAROT_READ = "tarot:read"
    TAROT_PREMIUM = "tarot:premium"
    
    # 💬 커뮤니티 권한
    COMMUNITY_READ = "community:read"
    COMMUNITY_WRITE = "community:write"
    COMMUNITY_MODERATE = "community:moderate"
    
    # 🛒 상거래 권한
    COMMERCE_PURCHASE = "commerce:purchase"
    PAYMENT_PROCESS = "payment:process"
    
    # 👤 사용자 권한
    USER_PROFILE = "user:profile"
    USER_PREMIUM = "user:premium"
    USER_ADMIN = "user:admin"

# 🔒 의존성 주입을 통한 권한 확인
def require_scope(required_scope: str):
    def scope_checker(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        auth_service: AuthService = Depends()
    ):
        payload = auth_service.verify_token(credentials.credentials)
        scopes = payload.get("scopes", [])
        
        if required_scope not in scopes:
            raise HTTPException(
                status_code=403, 
                detail=f"Insufficient permissions. Required: {required_scope}"
            )
        
        return payload
    
    return scope_checker
```

## 🔮 **운세 서비스 아키텍처**

### **📊 사주명리 서비스 (포트 8100)**
```python
# 🔮 Saju Service API
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

app = FastAPI(
    title="HEAL7 Saju Service",
    version="2.0.0",
    description="사주명리학 계산 및 해석 서비스"
)

# 📊 사주 계산 요청 모델
class SajuCalculationRequest(BaseModel):
    birth_year: int
    birth_month: int  
    birth_day: int
    birth_hour: int
    birth_minute: int
    gender: str  # "male" | "female"
    calendar_type: str = "solar"  # "solar" | "lunar"
    timezone: str = "Asia/Seoul"
    precision_level: str = "advanced"  # "basic" | "advanced" | "expert"

# 🎯 사주 결과 모델
class SajuResult(BaseModel):
    request_id: str
    user_id: int
    birth_info: SajuCalculationRequest
    
    # 🏛️ 기본 사주 정보
    four_pillars: Dict[str, Any]  # 년월일시 기둥
    wuxing_analysis: Dict[str, Any]  # 오행 분석
    sipsin_analysis: Dict[str, Any]  # 십신 분석
    
    # 🔮 해석 결과
    personality_analysis: str
    career_fortune: str
    wealth_fortune: str
    health_analysis: str
    relationship_analysis: str
    
    # 📊 메타데이터
    calculation_time: datetime
    accuracy_score: float
    data_source: str = "KASI_API"

# 🚀 사주 계산 엔드포인트
@app.post("/calculate", response_model=SajuResult)
async def calculate_saju(
    request: SajuCalculationRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(require_scope(Scopes.SAJU_READ)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 요청 ID 생성
    request_id = f"saju_{int(time.time())}_{current_user['user_id']}"
    
    try:
        # 2️⃣ 기존 결과 캐시 확인
        cached_result = await cache_service.get_saju_result(request)
        if cached_result:
            return cached_result
        
        # 3️⃣ KASI API 호출 (한국천문연구원)
        astronomical_data = await kasi_service.get_astronomical_data(
            request.birth_year, request.birth_month, request.birth_day,
            request.birth_hour, request.birth_minute
        )
        
        # 4️⃣ 사주 계산 엔진 실행
        calculator = SajuCalculator(precision_level=request.precision_level)
        four_pillars = await calculator.calculate_four_pillars(
            astronomical_data, request
        )
        
        # 5️⃣ 오행/십신 분석
        analyzer = SajuAnalyzer()
        wuxing_analysis = await analyzer.analyze_wuxing(four_pillars)
        sipsin_analysis = await analyzer.analyze_sipsin(four_pillars)
        
        # 6️⃣ AI 해석 생성
        interpreter = AIInterpreter()
        interpretations = await interpreter.generate_interpretations({
            "four_pillars": four_pillars,
            "wuxing": wuxing_analysis,
            "sipsin": sipsin_analysis,
            "user_context": current_user
        })
        
        # 7️⃣ 결과 구성
        result = SajuResult(
            request_id=request_id,
            user_id=current_user["user_id"],
            birth_info=request,
            four_pillars=four_pillars,
            wuxing_analysis=wuxing_analysis,
            sipsin_analysis=sipsin_analysis,
            **interpretations,
            calculation_time=datetime.utcnow(),
            accuracy_score=0.95
        )
        
        # 8️⃣ 데이터베이스 저장
        await db_service.save_saju_result(result)
        
        # 9️⃣ 캐시 저장 (백그라운드)
        background_tasks.add_task(
            cache_service.cache_saju_result, 
            request, result, expire_hours=24
        )
        
        # 🔟 분석 로그 (백그라운드)
        background_tasks.add_task(
            analytics_service.log_saju_calculation,
            current_user["user_id"], request, result
        )
        
        return result
        
    except Exception as e:
        # ❌ 에러 로깅
        logger.error(f"Saju calculation failed: {str(e)}", extra={
            "request_id": request_id,
            "user_id": current_user["user_id"],
            "request": request.dict()
        })
        
        raise HTTPException(
            status_code=500,
            detail="사주 계산 중 오류가 발생했습니다."
        )

# 📖 사주 해석 상세 조회
@app.get("/interpretation/{result_id}")
async def get_saju_interpretation(
    result_id: str,
    section: Optional[str] = None,  # "personality" | "career" | "wealth" | "health" | "relationship"
    current_user = Depends(require_scope(Scopes.SAJU_READ)),
    db: Session = Depends(get_db)
):
    # 권한 확인 & 데이터 조회 로직
    pass

# 📊 사주 이력 조회
@app.get("/history", response_model=List[SajuResult])
async def get_saju_history(
    limit: int = 10,
    offset: int = 0,
    current_user = Depends(require_scope(Scopes.SAJU_READ)),
    db: Session = Depends(get_db)
):
    # 사용자 사주 계산 이력 조회
    pass

# 🔄 사주 재해석 요청
@app.post("/reinterpret/{result_id}")
async def reinterpret_saju(
    result_id: str,
    interpretation_type: str,  # "detailed" | "simplified" | "professional"
    current_user = Depends(require_scope(Scopes.SAJU_PREMIUM)),
    db: Session = Depends(get_db)
):
    # 프리미엄 기능: AI 재해석
    pass
```

### **🃏 타로카드 서비스 (포트 8101)**
```python
# 🃏 Tarot Service API
app = FastAPI(
    title="HEAL7 Tarot Service", 
    version="1.0.0",
    description="타로카드 리딩 및 해석 서비스"
)

# 🎴 타로 리딩 요청 모델
class TarotReadingRequest(BaseModel):
    spread_type: str  # "single", "three_card", "celtic_cross", "custom"
    question: str
    question_category: str  # "love", "career", "health", "general"
    card_count: int = 3
    reading_style: str = "intuitive"  # "traditional" | "intuitive" | "psychological"

# 🎯 타로 카드 모델
class TarotCard(BaseModel):
    id: int
    name: str
    suit: str  # "major_arcana", "cups", "wands", "swords", "pentacles"
    number: Optional[int]
    position: str  # "upright" | "reversed"
    image_url: str
    keywords: List[str]
    meanings: Dict[str, str]  # upright, reversed meanings

# 🔮 타로 리딩 결과
class TarotReading(BaseModel):
    reading_id: str
    user_id: int
    question: str
    spread_type: str
    cards: List[TarotCard]
    interpretations: List[str]
    overall_reading: str
    advice: str
    confidence_score: float
    created_at: datetime

# 🎴 타로 리딩 실행
@app.post("/reading", response_model=TarotReading)
async def perform_tarot_reading(
    request: TarotReadingRequest,
    current_user = Depends(require_scope(Scopes.TAROT_READ))
):
    # 1️⃣ 덱에서 카드 뽑기
    deck = TarotDeck.load_rider_waite_deck()
    drawn_cards = deck.draw_cards(
        count=request.card_count,
        spread=request.spread_type
    )
    
    # 2️⃣ AI 해석 생성
    interpreter = TarotInterpreter()
    reading_result = await interpreter.interpret_cards(
        cards=drawn_cards,
        question=request.question,
        style=request.reading_style
    )
    
    # 3️⃣ 결과 저장 및 반환
    pass

# 📚 타로 덱 관리
@app.get("/decks")
async def get_tarot_decks():
    # 사용 가능한 타로 덱 목록
    pass

# 🎴 개별 카드 정보
@app.get("/cards/{card_id}")
async def get_card_info(card_id: int):
    # 특정 카드의 상세 정보
    pass
```

### **🐲 12지신 서비스 (포트 8102)**
```python
# 🐲 Zodiac Service API  
app = FastAPI(
    title="HEAL7 Zodiac Service",
    version="1.0.0", 
    description="12지신 및 동양 점성술 서비스"
)

# 🐉 12지신 모델
class ZodiacSign(BaseModel):
    animal: str  # "rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "goat", "monkey", "rooster", "dog", "pig"
    element: str  # "wood", "fire", "earth", "metal", "water"
    yin_yang: str  # "yin", "yang"
    characteristics: List[str]
    lucky_numbers: List[int]
    lucky_colors: List[str]
    compatible_signs: List[str]
    incompatible_signs: List[str]

# 🎯 12지신 분석 요청
class ZodiacAnalysisRequest(BaseModel):
    birth_year: int
    analysis_type: str = "comprehensive"  # "basic" | "comprehensive" | "compatibility"
    partner_birth_year: Optional[int] = None  # 궁합 분석용

# 📊 12지신 분석 결과
class ZodiacAnalysis(BaseModel):
    birth_year: int
    zodiac_sign: ZodiacSign
    personality_traits: List[str]
    fortune_forecast: Dict[str, str]  # career, love, health, wealth
    yearly_fortune: str
    monthly_fortune: Dict[int, str]
    compatibility_analysis: Optional[Dict[str, Any]]
    
# 🐲 12지신 분석 실행
@app.post("/analyze", response_model=ZodiacAnalysis)
async def analyze_zodiac(
    request: ZodiacAnalysisRequest,
    current_user = Depends(require_scope(Scopes.ZODIAC_READ))
):
    # 12지신 분석 로직
    pass

# 💑 궁합 분석
@app.post("/compatibility")
async def analyze_compatibility(
    person1_year: int,
    person2_year: int,
    current_user = Depends(require_scope(Scopes.ZODIAC_READ))
):
    # 12지신 궁합 분석
    pass
```

## 💬 **커뮤니티 서비스 아키텍처**

### **📝 게시판 서비스 (포트 8200)**
```python
# 💬 Community Service API
app = FastAPI(
    title="HEAL7 Community Service",
    version="1.5.0",
    description="커뮤니티 및 게시판 서비스"
)

# 📄 게시글 모델
class Post(BaseModel):
    id: int
    title: str
    content: str
    category: str  # "saju", "tarot", "zodiac", "general", "review"
    author_id: int
    author_nickname: str
    tags: List[str]
    images: List[str] = []
    likes_count: int = 0
    comments_count: int = 0
    views_count: int = 0
    is_pinned: bool = False
    is_featured: bool = False
    created_at: datetime
    updated_at: datetime
    status: str = "published"  # "draft", "published", "hidden", "deleted"

# ✍️ 게시글 작성 요청
class CreatePostRequest(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str] = []
    images: List[str] = []
    is_anonymous: bool = False

# 📝 게시글 작성
@app.post("/posts", response_model=Post)
async def create_post(
    request: CreatePostRequest,
    current_user = Depends(require_scope(Scopes.COMMUNITY_WRITE)),
    db: Session = Depends(get_db)
):
    # 게시글 작성 로직
    pass

# 📋 게시글 목록 조회
@app.get("/posts", response_model=List[Post])
async def get_posts(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",  # "created_at", "likes", "views", "comments"
    order: str = "desc",  # "asc", "desc"
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    # 게시글 목록 조회 (검색, 필터링, 정렬)
    pass

# 👀 게시글 상세 조회
@app.get("/posts/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    # 조회수 증가 및 게시글 상세 정보 반환
    pass

# 💬 댓글 모델
class Comment(BaseModel):
    id: int
    post_id: int
    parent_id: Optional[int] = None  # 대댓글용
    author_id: int
    author_nickname: str
    content: str
    likes_count: int = 0
    is_anonymous: bool = False
    created_at: datetime
    updated_at: datetime
    status: str = "published"

# 💬 댓글 작성
@app.post("/posts/{post_id}/comments", response_model=Comment)
async def create_comment(
    post_id: int,
    content: str,
    parent_id: Optional[int] = None,
    is_anonymous: bool = False,
    current_user = Depends(require_scope(Scopes.COMMUNITY_WRITE)),
    db: Session = Depends(get_db)
):
    # 댓글 작성 로직
    pass

# ❤️ 좋아요/싫어요
@app.post("/posts/{post_id}/like")
async def like_post(
    post_id: int,
    action: str,  # "like", "unlike" 
    current_user = Depends(require_scope(Scopes.COMMUNITY_READ)),
    db: Session = Depends(get_db)
):
    # 좋아요 처리
    pass
```

## 🛒 **커머스 서비스 아키텍처**

### **🛍️ 스토어 서비스 (포트 8300)**
```python
# 🛒 Commerce Service API
app = FastAPI(
    title="HEAL7 Commerce Service",
    version="1.2.0",
    description="스토어 및 상품 관리 서비스"
)

# 🎁 상품 모델
class Product(BaseModel):
    id: int
    name: str
    description: str
    category: str  # "amulet", "book", "consultation", "premium_content"
    type: str  # "physical", "digital", "service"
    price: Decimal
    sale_price: Optional[Decimal] = None
    currency: str = "KRW"
    images: List[str]
    tags: List[str]
    stock_quantity: Optional[int] = None  # None = unlimited
    is_digital: bool = False
    download_url: Optional[str] = None
    consultation_duration: Optional[int] = None  # minutes
    rating: float = 0.0
    review_count: int = 0
    created_at: datetime
    status: str = "active"  # "active", "inactive", "out_of_stock"

# 🛒 장바구니 모델
class CartItem(BaseModel):
    product_id: int
    quantity: int
    options: Dict[str, Any] = {}  # 상품 옵션 (색상, 크기 등)

class Cart(BaseModel):
    user_id: int
    items: List[CartItem]
    total_amount: Decimal
    updated_at: datetime

# 📦 주문 모델
class Order(BaseModel):
    id: str  # UUID
    user_id: int
    items: List[CartItem]
    shipping_address: Dict[str, str]
    payment_method: str
    total_amount: Decimal
    status: str  # "pending", "paid", "shipped", "delivered", "cancelled"
    created_at: datetime
    estimated_delivery: Optional[datetime]

# 🛍️ 상품 목록 조회
@app.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    # 상품 목록 조회
    pass

# 🛒 장바구니에 추가
@app.post("/cart/add")
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    options: Dict[str, Any] = {},
    current_user = Depends(require_scope(Scopes.COMMERCE_PURCHASE)),
    db: Session = Depends(get_db)
):
    # 장바구니 추가 로직
    pass

# 📦 주문 생성
@app.post("/orders", response_model=Order)
async def create_order(
    cart_items: List[CartItem],
    shipping_address: Dict[str, str],
    payment_method: str,
    current_user = Depends(require_scope(Scopes.COMMERCE_PURCHASE)),
    db: Session = Depends(get_db)
):
    # 주문 생성 로직
    pass
```

### **💳 결제 서비스 (포트 8301)**
```python
# 💳 Payment Service API
app = FastAPI(
    title="HEAL7 Payment Service",
    version="1.2.0",
    description="통합 결제 처리 서비스"
)

# 💰 결제 요청 모델
class PaymentRequest(BaseModel):
    order_id: str
    amount: Decimal
    currency: str = "KRW"
    payment_method: str  # "card", "kakao_pay", "naver_pay", "toss_pay", "bank_transfer"
    return_url: str
    cancel_url: str
    metadata: Dict[str, Any] = {}

# 💳 결제 결과 모델  
class PaymentResult(BaseModel):
    payment_id: str
    order_id: str
    status: str  # "pending", "completed", "failed", "cancelled"
    amount: Decimal
    payment_method: str
    transaction_id: str
    paid_at: Optional[datetime]
    failure_reason: Optional[str]

# 💰 결제 처리
@app.post("/process", response_model=PaymentResult)
async def process_payment(
    request: PaymentRequest,
    current_user = Depends(require_scope(Scopes.PAYMENT_PROCESS)),
    db: Session = Depends(get_db)
):
    # 결제 처리 로직 (PG사 연동)
    pass

# ✅ 결제 확인/취소
@app.post("/verify/{payment_id}")
async def verify_payment(
    payment_id: str,
    db: Session = Depends(get_db)
):
    # 결제 검증 로직
    pass

@app.post("/cancel/{payment_id}")
async def cancel_payment(
    payment_id: str,
    reason: str,
    current_user = Depends(require_scope(Scopes.PAYMENT_PROCESS)),
    db: Session = Depends(get_db)
):
    # 결제 취소 로직
    pass
```

## 📊 **데이터베이스 스키마 설계**

### **🗃️ PostgreSQL 스키마**
```sql
-- 👤 사용자 관리 스키마
CREATE SCHEMA user_management;

-- 사용자 기본 정보
CREATE TABLE user_management.users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    birth_date DATE,
    gender VARCHAR(10),
    timezone VARCHAR(50) DEFAULT 'Asia/Seoul',
    language VARCHAR(10) DEFAULT 'ko',
    profile_image_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 🔐 계정 보안
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    phone_verified_at TIMESTAMP WITH TIME ZONE,
    
    -- 📊 메타데이터
    metadata JSONB DEFAULT '{}',
    preferences JSONB DEFAULT '{}'
);

-- 사용자 권한 및 구독
CREATE TABLE user_management.user_subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES user_management.users(id),
    plan_type VARCHAR(50) NOT NULL, -- 'basic', 'premium', 'master'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'cancelled', 'expired'
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    auto_renew BOOLEAN DEFAULT TRUE,
    payment_method VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🔮 운세 서비스 스키마
CREATE SCHEMA fortune_services;

-- 사주 계산 결과
CREATE TABLE fortune_services.saju_results (
    id BIGSERIAL PRIMARY KEY,
    request_id VARCHAR(100) UNIQUE NOT NULL,
    user_id BIGINT NOT NULL REFERENCES user_management.users(id),
    
    -- 📅 생년월일시 정보
    birth_year INTEGER NOT NULL,
    birth_month INTEGER NOT NULL,
    birth_day INTEGER NOT NULL,
    birth_hour INTEGER NOT NULL,
    birth_minute INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    calendar_type VARCHAR(10) DEFAULT 'solar',
    timezone VARCHAR(50) DEFAULT 'Asia/Seoul',
    
    -- 🏛️ 사주 계산 결과 (JSONB)
    four_pillars JSONB NOT NULL, -- 년월일시 기둥
    wuxing_analysis JSONB NOT NULL, -- 오행 분석
    sipsin_analysis JSONB NOT NULL, -- 십신 분석
    
    -- 🔮 AI 해석 결과
    personality_analysis TEXT,
    career_fortune TEXT,
    wealth_fortune TEXT,
    health_analysis TEXT,
    relationship_analysis TEXT,
    
    -- 📊 메타데이터
    calculation_engine VARCHAR(50) DEFAULT 'HEAL7_v2',
    precision_level VARCHAR(20) DEFAULT 'advanced',
    accuracy_score DECIMAL(3,2),
    data_source VARCHAR(50) DEFAULT 'KASI_API',
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 🔍 인덱스
    INDEX idx_saju_user_created (user_id, created_at DESC),
    INDEX idx_saju_birth_info (birth_year, birth_month, birth_day)
);

-- 타로 리딩 결과
CREATE TABLE fortune_services.tarot_readings (
    id BIGSERIAL PRIMARY KEY,
    reading_id VARCHAR(100) UNIQUE NOT NULL,
    user_id BIGINT NOT NULL REFERENCES user_management.users(id),
    
    -- 🃏 리딩 정보
    question TEXT NOT NULL,
    question_category VARCHAR(50),
    spread_type VARCHAR(50) NOT NULL,
    reading_style VARCHAR(50) DEFAULT 'intuitive',
    
    -- 🎴 뽑힌 카드들 (JSONB)
    cards JSONB NOT NULL, -- [{"id": 1, "name": "The Fool", "position": "upright", ...}]
    
    -- 🔮 해석 결과
    card_interpretations JSONB NOT NULL, -- 각 카드별 해석
    overall_reading TEXT,
    advice TEXT,
    confidence_score DECIMAL(3,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_tarot_user_created (user_id, created_at DESC)
);

-- 12지신 분석 결과
CREATE TABLE fortune_services.zodiac_analyses (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES user_management.users(id),
    
    -- 🐲 12지신 정보
    birth_year INTEGER NOT NULL,
    zodiac_animal VARCHAR(20) NOT NULL,
    zodiac_element VARCHAR(20) NOT NULL,
    yin_yang VARCHAR(10) NOT NULL,
    
    -- 📊 분석 결과 (JSONB)
    personality_traits JSONB,
    fortune_forecast JSONB, -- {career, love, health, wealth}
    yearly_fortune TEXT,
    monthly_fortune JSONB, -- {1: "fortune for Jan", 2: "Feb", ...}
    
    -- 💑 궁합 분석 (선택적)
    compatibility_partner_year INTEGER,
    compatibility_analysis JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_zodiac_user_year (user_id, birth_year)
);

-- 💬 커뮤니티 스키마
CREATE SCHEMA community;

-- 게시판 카테고리
CREATE TABLE community.categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id INTEGER REFERENCES community.categories(id),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 게시글
CREATE TABLE community.posts (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    excerpt VARCHAR(1000), -- 자동 생성되는 요약
    
    -- 👤 작성자 정보
    author_id BIGINT NOT NULL REFERENCES user_management.users(id),
    author_nickname VARCHAR(100),
    is_anonymous BOOLEAN DEFAULT FALSE,
    
    -- 📂 분류 및 태그
    category_id INTEGER NOT NULL REFERENCES community.categories(id),
    tags TEXT[], -- PostgreSQL 배열
    
    -- 📊 통계
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    
    -- 🎯 상태 관리
    status VARCHAR(20) DEFAULT 'published', -- draft, published, hidden, deleted
    is_pinned BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    featured_until TIMESTAMP WITH TIME ZONE,
    
    -- 🖼️ 미디어
    images TEXT[], -- 이미지 URL 배열
    attachments JSONB DEFAULT '[]', -- 첨부파일 정보
    
    -- ⏰ 시간 정보
    published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 🔍 전문 검색용 (PostgreSQL Full Text Search)
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('korean', title || ' ' || content)
    ) STORED,
    
    -- 인덱스
    INDEX idx_posts_category_published (category_id, published_at DESC),
    INDEX idx_posts_author (author_id, created_at DESC),
    INDEX idx_posts_status (status, published_at DESC),
    INDEX idx_posts_search USING gin(search_vector),
    INDEX idx_posts_tags USING gin(tags)
);

-- 댓글
CREATE TABLE community.comments (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL REFERENCES community.posts(id) ON DELETE CASCADE,
    parent_id BIGINT REFERENCES community.comments(id), -- 대댓글용
    
    -- 👤 작성자
    author_id BIGINT NOT NULL REFERENCES user_management.users(id),
    author_nickname VARCHAR(100),
    is_anonymous BOOLEAN DEFAULT FALSE,
    
    -- 💬 내용
    content TEXT NOT NULL,
    
    -- 📊 통계
    likes_count INTEGER DEFAULT 0,
    replies_count INTEGER DEFAULT 0,
    
    -- 🎯 상태
    status VARCHAR(20) DEFAULT 'published',
    is_highlighted BOOLEAN DEFAULT FALSE, -- 베스트 댓글
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 인덱스
    INDEX idx_comments_post (post_id, created_at),
    INDEX idx_comments_parent (parent_id, created_at),
    INDEX idx_comments_author (author_id, created_at DESC)
);

-- 🛒 커머스 스키마
CREATE SCHEMA commerce;

-- 상품 카테고리
CREATE TABLE commerce.product_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES commerce.product_categories(id),
    image_url TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 상품
CREATE TABLE commerce.products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    description TEXT,
    short_description VARCHAR(1000),
    
    -- 💰 가격 정보
    price DECIMAL(12,2) NOT NULL,
    sale_price DECIMAL(12,2),
    currency VARCHAR(3) DEFAULT 'KRW',
    
    -- 📂 분류
    category_id INTEGER NOT NULL REFERENCES commerce.product_categories(id),
    tags TEXT[],
    
    -- 📦 재고 및 타입
    type VARCHAR(20) NOT NULL, -- physical, digital, service
    stock_quantity INTEGER, -- NULL = unlimited
    track_quantity BOOLEAN DEFAULT TRUE,
    
    -- 🎁 디지털 상품 정보
    is_digital BOOLEAN DEFAULT FALSE,
    download_url TEXT,
    download_limit INTEGER, -- 다운로드 횟수 제한
    
    -- 💼 서비스 상품 정보
    service_duration INTEGER, -- 서비스 지속시간 (분)
    booking_required BOOLEAN DEFAULT FALSE,
    
    -- 🖼️ 미디어
    images JSONB DEFAULT '[]', -- [{"url": "...", "alt": "...", "order": 1}]
    videos JSONB DEFAULT '[]',
    
    -- 📊 통계 및 평가
    rating DECIMAL(2,1) DEFAULT 0.0,
    review_count INTEGER DEFAULT 0,
    sales_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    
    -- 🎯 상태 및 노출
    status VARCHAR(20) DEFAULT 'active', -- active, inactive, out_of_stock
    is_featured BOOLEAN DEFAULT FALSE,
    featured_until TIMESTAMP WITH TIME ZONE,
    
    -- ⏰ 시간 정보
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- SEO 최적화
    meta_title VARCHAR(200),
    meta_description VARCHAR(500),
    
    -- 🔍 검색 최적화
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('korean', name || ' ' || COALESCE(description, '') || ' ' || array_to_string(tags, ' '))
    ) STORED,
    
    -- 인덱스
    INDEX idx_products_category (category_id, status, created_at DESC),
    INDEX idx_products_price (price, status),
    INDEX idx_products_featured (is_featured, featured_until DESC),
    INDEX idx_products_search USING gin(search_vector)
);

-- 주문
CREATE TABLE commerce.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL, -- 주문번호 (사용자용)
    
    -- 👤 주문자 정보
    user_id BIGINT NOT NULL REFERENCES user_management.users(id),
    
    -- 💰 결제 정보
    subtotal DECIMAL(12,2) NOT NULL, -- 상품 총액
    shipping_cost DECIMAL(12,2) DEFAULT 0,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    discount_amount DECIMAL(12,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL, -- 최종 결제 금액
    currency VARCHAR(3) DEFAULT 'KRW',
    
    -- 📦 배송 정보
    shipping_address JSONB NOT NULL, -- {name, phone, address, zipcode, message}
    billing_address JSONB, -- 다를 경우만
    
    -- 🎯 주문 상태
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, preparing, shipped, delivered, cancelled, refunded
    payment_status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed, refunded
    shipping_status VARCHAR(20) DEFAULT 'not_shipped', -- not_shipped, preparing, shipped, delivered
    
    -- ⏰ 시간 정보
    ordered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    paid_at TIMESTAMP WITH TIME ZONE,
    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    estimated_delivery TIMESTAMP WITH TIME ZONE,
    
    -- 📝 메모 및 메타데이터
    customer_notes TEXT,
    admin_notes TEXT,
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 인덱스
    INDEX idx_orders_user_status (user_id, status, ordered_at DESC),
    INDEX idx_orders_status (status, ordered_at DESC),
    INDEX idx_orders_payment_status (payment_status, paid_at DESC)
);

-- 주문 상품 (Order Items)
CREATE TABLE commerce.order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES commerce.orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES commerce.products(id),
    
    -- 📦 상품 정보 (주문 시점 스냅샷)
    product_name VARCHAR(500) NOT NULL,
    product_image_url TEXT,
    
    -- 💰 가격 정보 (주문 시점)
    unit_price DECIMAL(12,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    total_price DECIMAL(12,2) NOT NULL,
    
    -- 🎛️ 상품 옵션 (색상, 크기 등)
    options JSONB DEFAULT '{}',
    
    -- 📦 배송 및 상태
    shipping_required BOOLEAN DEFAULT TRUE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, preparing, shipped, delivered, cancelled
    
    -- 🎁 디지털 상품 관련
    download_url TEXT,
    download_count INTEGER DEFAULT 0,
    download_expires_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_order_items_order (order_id),
    INDEX idx_order_items_product (product_id)
);

-- 💳 결제 정보
CREATE TABLE commerce.payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES commerce.orders(id),
    
    -- 💰 결제 정보
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'KRW',
    payment_method VARCHAR(50) NOT NULL, -- card, kakao_pay, naver_pay, toss_pay, bank_transfer
    
    -- 🏦 PG사 정보
    pg_provider VARCHAR(50), -- iamport, toss, kakao, naver 등
    pg_transaction_id VARCHAR(200), -- PG사 거래 ID
    
    -- 🎯 결제 상태
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed, cancelled, refunded
    
    -- ⏰ 시간 정보
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    failed_at TIMESTAMP WITH TIME ZONE,
    
    -- 📝 결제 상세 정보
    failure_reason TEXT,
    refund_reason TEXT,
    refund_amount DECIMAL(12,2),
    
    -- 🔐 보안 및 메타데이터
    receipt_url TEXT,
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_payments_order (order_id),
    INDEX idx_payments_status (status, completed_at DESC),
    INDEX idx_payments_pg_transaction (pg_provider, pg_transaction_id)
);
```

### **⚡ Redis 캐시 구조**
```yaml
# 🔥 Redis Cache Architecture
redis_structure:
  # 🔮 사주 결과 캐시
  saju_cache:
    key_pattern: "saju:{user_id}:{birth_hash}"
    ttl: 86400  # 24시간
    data_structure: "hash"
    fields:
      - four_pillars
      - wuxing_analysis
      - sipsin_analysis
      - interpretations
  
  # 🃏 타로 덱 캐시
  tarot_cache:
    key_pattern: "tarot:deck:{deck_type}"
    ttl: 3600   # 1시간
    data_structure: "list"
    
  # 👤 사용자 세션
  user_sessions:
    key_pattern: "session:{session_id}"
    ttl: 7200   # 2시간
    data_structure: "hash"
    
  # 📊 실시간 통계
  realtime_stats:
    key_pattern: "stats:{type}:{date}"
    ttl: 86400  # 24시간
    data_structure: "sorted_set"
    
  # 🔔 알림 큐
  notification_queue:
    key_pattern: "notifications:{user_id}"
    ttl: 604800  # 7일
    data_structure: "list"
```

## 🔧 **성능 최적화 전략**

### **📊 데이터베이스 최적화**
```sql
-- 🔍 인덱스 최적화
CREATE INDEX CONCURRENTLY idx_saju_results_composite 
ON fortune_services.saju_results (user_id, created_at DESC, precision_level);

CREATE INDEX CONCURRENTLY idx_posts_full_text_search 
ON community.posts USING gin(search_vector);

-- 📈 파티셔닝 (대용량 데이터)
CREATE TABLE fortune_services.saju_results_2025 
PARTITION OF fortune_services.saju_results 
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- 🗃️ 아카이빙 (오래된 데이터)
CREATE TABLE fortune_services.saju_results_archive AS 
SELECT * FROM fortune_services.saju_results 
WHERE created_at < NOW() - INTERVAL '2 years';
```

### **⚡ 캐싱 전략**
```python
# 🔥 Multi-Level Caching Strategy
class CacheManager:
    def __init__(self):
        self.redis = Redis(host="redis-cluster")
        self.local_cache = TTLCache(maxsize=1000, ttl=300)  # 5분 로컬 캐시
    
    async def get_saju_result(self, user_id: int, birth_hash: str):
        # 1️⃣ 로컬 캐시 확인
        local_key = f"saju:{user_id}:{birth_hash}"
        if local_key in self.local_cache:
            return self.local_cache[local_key]
        
        # 2️⃣ Redis 캐시 확인
        redis_data = await self.redis.hgetall(f"saju_cache:{user_id}:{birth_hash}")
        if redis_data:
            result = SajuResult.parse_obj(redis_data)
            self.local_cache[local_key] = result  # 로컬 캐시에도 저장
            return result
        
        # 3️⃣ 데이터베이스 조회
        return None
    
    async def cache_saju_result(self, user_id: int, birth_hash: str, result: SajuResult):
        # Redis에 저장
        await self.redis.hset(
            f"saju_cache:{user_id}:{birth_hash}",
            mapping=result.dict()
        )
        await self.redis.expire(f"saju_cache:{user_id}:{birth_hash}", 86400)
        
        # 로컬 캐시에도 저장
        self.local_cache[f"saju:{user_id}:{birth_hash}"] = result
```

---

## 📈 **모니터링 및 로깅**

### **📊 메트릭 수집**
```python
# 📈 Prometheus Metrics
from prometheus_client import Counter, Histogram, Gauge

# API 호출 메트릭
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status_code']
)

# 응답 시간 메트릭
api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

# 활성 사용자 메트릭
active_users = Gauge(
    'active_users_total',
    'Number of active users'
)

# 사주 계산 메트릭
saju_calculations_total = Counter(
    'saju_calculations_total',
    'Total saju calculations',
    ['precision_level', 'status']
)
```

### **📝 구조화된 로깅**
```python
# 📝 Structured Logging
import structlog

logger = structlog.get_logger()

# 사주 계산 로그
logger.info(
    "saju_calculation_completed",
    user_id=user_id,
    request_id=request_id,
    precision_level=precision_level,
    processing_time_ms=processing_time,
    accuracy_score=accuracy_score,
    data_source="KASI_API"
)

# 에러 로그
logger.error(
    "saju_calculation_failed", 
    user_id=user_id,
    request_id=request_id,
    error_type="KASI_API_ERROR",
    error_message=str(error),
    stack_trace=traceback.format_exc()
)
```

---

*📅 설계 완료일: 2025-08-18*  
*🚀 설계자: HEAL7 Backend Architecture Team*  
*📝 문서 위치: `/home/ubuntu/CORE/architecture-diagrams/service-architecture/`*  
*🔄 다음 버전: v1.1 (2025-08-25 예정)*