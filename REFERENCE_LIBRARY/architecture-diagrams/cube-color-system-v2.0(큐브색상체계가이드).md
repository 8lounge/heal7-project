# 🌈 큐브 색상 체계 가이드 v2.0

> **시각적 아키텍처**: 색상으로 분류하는 직관적 큐브 시스템  
> **생체모방 원리**: 인체 기관별 색상 매핑 + 화학 원소 분류법 응용  
> **표준화 철학**: 개발자가 한눈에 알아볼 수 있는 색상 기반 역할 분담  
> **최종 업데이트**: 2025-08-20 16:00 UTC

## 🎨 **색상 체계 개요**

### **🧠 색상 선택의 과학적 근거**

```yaml
color_psychology_mapping:
  🟦 Blue (파랑): 
    psychology: "신뢰성, 논리적 사고, 비즈니스"
    metaphor: "뇌(논리), 심장(핵심 기능)"
    responsibility: "비즈니스 로직의 중추"
    
  🟩 Green (초록):
    psychology: "성장, 연결, 소통"
    metaphor: "순환계(혈관), 신경망"
    responsibility: "데이터와 서비스를 연결하는 통로"
    
  🟨 Yellow (노랑):
    psychology: "지식, 저장, 기억"
    metaphor: "뼈(골격), 지방(저장소)"
    responsibility: "데이터의 안전한 저장과 관리"
    
  🟥 Red (빨강):
    psychology: "경고, 보호, 방어"
    metaphor: "면역계, 백혈구"
    responsibility: "시스템을 위협으로부터 보호"
    
  🟪 Purple (보라):
    psychology: "관찰, 통찰, 분석"
    metaphor: "감각기관, 신경계 모니터링"
    responsibility: "시스템 상태의 관찰과 분석"
    
  🟧 Orange (주황):
    psychology: "상호작용, 활력, 표현"
    metaphor: "피부, 얼굴(표현)"
    responsibility: "사용자와의 인터페이스"
    
  🟫 Brown (갈색):
    psychology: "안정성, 외부 연결, 토대"
    metaphor: "소화계(외부 영양 흡수)"
    responsibility: "외부 시스템과의 연동"
```

### **🔬 화학 주기율표 원리 적용**

```
큐브 색상 주기율표
┌─────────────────────────────────────────────────────────────────┐
│                        핵심 그룹 (Core Group)                    │
│  🟦 Feature    🟩 Network    🟨 Data      🟥 Security           │
│  (비즈니스)     (통신)        (저장)       (보안)               │
│                                                                 │
│                      지원 그룹 (Support Group)                  │
│       🟪 Monitoring    🟧 UI         🟫 Integration             │
│       (관찰)           (인터페이스)   (연동)                    │
└─────────────────────────────────────────────────────────────────┘

화학_원리:
  족(Group): 수직 그룹 - 비슷한 성질
  주기(Period): 수평 그룹 - 상호작용 레벨
  전자각(Electron Shell): 큐브의 레이어 구조
  원자가(Valence): 큐브간 결합 능력
```

## 🟦 **Feature Cubes (비즈니스 로직 큐브)**

### **🎯 역할과 책임**

```yaml
feature_cubes:
  purpose: "비즈니스 도메인 로직의 핵심 구현"
  metaphor: "인체의 뇌와 심장 - 생각하고 판단하는 중추"
  color_meaning: "신뢰할 수 있는 비즈니스 핵심"
  
  primary_responsibilities:
    - "도메인 특화 비즈니스 로직 처리"
    - "복잡한 알고리즘 구현 (사주 계산 등)"
    - "비즈니스 규칙 검증"
    - "워크플로우 오케스트레이션"
    - "도메인 이벤트 발생"
    
  technology_stack:
    preferred_languages:
      - "Rust: 고성능 계산 (사주 엔진)"
      - "Python: AI/ML 로직 (해석 엔진)"
      - "Go: 빠른 비즈니스 로직"
      - "TypeScript: 클라이언트 비즈니스 로직"
    
  performance_targets:
    response_time: "< 10ms"
    cpu_utilization: "< 70%"
    memory_efficiency: "최적화 필수"
    error_tolerance: "< 0.01%"
```

### **🧩 Feature Cube 구현 예시**

```rust
// 🟦 사주 계산 Feature Cube
#[derive(Clone)]
pub struct SajuCalculationCube {
    cube_info: CubeInfo,
    calculation_engine: SajuEngine,
    validation_rules: ValidationRules,
    event_publisher: EventPublisher,
}

impl FeatureCube for SajuCalculationCube {
    fn cube_color(&self) -> CubeColor {
        CubeColor::Blue
    }
    
    fn business_domain(&self) -> &str {
        "fortune_telling"
    }
    
    async fn process_business_logic(&self, input: BusinessInput) -> Result<BusinessOutput> {
        // 1. 입력 검증
        self.validation_rules.validate(&input)?;
        
        // 2. 사주 계산 실행
        let saju_result = self.calculation_engine.calculate_comprehensive(&input.birth_data).await?;
        
        // 3. 비즈니스 이벤트 발생
        self.event_publisher.publish(
            "saju_calculated", 
            SajuCalculatedEvent {
                user_id: input.user_id,
                result: saju_result.clone(),
                timestamp: Utc::now(),
            }
        ).await?;
        
        // 4. 결과 반환
        Ok(BusinessOutput {
            result: saju_result,
            confidence: self.calculate_confidence(&saju_result),
            processing_time: self.performance_counter.elapsed(),
        })
    }
}
```

### **🔧 Feature Cube 설계 패턴**

```yaml
design_patterns:
  domain_driven_design:
    - "Aggregate Root 패턴"
    - "Domain Service 패턴"
    - "Value Object 패턴"
    - "Domain Event 패턴"
    
  business_logic_patterns:
    - "Strategy 패턴 (알고리즘 교체)"
    - "Chain of Responsibility (워크플로우)"
    - "Command 패턴 (비즈니스 명령)"
    - "Observer 패턴 (이벤트 처리)"
    
  validation_patterns:
    - "Specification 패턴"
    - "Validator Chain 패턴"
    - "Business Rules Engine"
```

## 🟩 **Network Cubes (네트워크 통신 큐브)**

### **🌐 역할과 책임**

```yaml
network_cubes:
  purpose: "큐브간 통신과 외부 네트워크 인터페이스"
  metaphor: "인체의 순환계 - 혈관을 통한 영양소 전달"
  color_meaning: "성장과 연결의 통로"
  
  primary_responsibilities:
    - "HTTP/HTTPS 서버 운영"
    - "WebSocket 실시간 통신"
    - "gRPC 고성능 RPC"
    - "GraphQL API 게이트웨이"
    - "로드 밸런싱"
    - "API 레이트 리미팅"
    - "프록시 및 리버스 프록시"
    
  technology_stack:
    primary_language: "Go (고성능 네트워킹)"
    frameworks:
      - "Fiber: HTTP 프레임워크"
      - "gRPC-Go: RPC 통신"
      - "Gorilla WebSocket: 실시간 통신"
      - "GraphQL-Go: API 게이트웨이"
    
  performance_targets:
    concurrent_connections: "300,000+"
    latency: "< 1ms"
    throughput: "100K RPS"
    uptime: "99.99%"
```

### **⚡ Network Cube 구현 예시**

```go
// 🟩 HTTP 서버 Network Cube
package network

import (
    "context"
    "time"
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/cors"
    "github.com/gofiber/fiber/v2/middleware/limiter"
)

type HTTPServerCube struct {
    CubeInfo
    
    server      *fiber.App
    config      NetworkConfig
    metrics     *NetworkMetrics
    
    // 연결된 Feature Cube들
    connectedCubes map[string]FeatureCube
}

func NewHTTPServerCube(config NetworkConfig) *HTTPServerCube {
    // 고성능 Fiber 설정
    app := fiber.New(fiber.Config{
        Concurrency:       300_000,  // 30만 동접
        DisableKeepalive:  false,    // Keep-alive 활성화
        ReadTimeout:       time.Second * 10,
        WriteTimeout:      time.Second * 10,
        IdleTimeout:       time.Second * 120,
        ServerHeader:      "HEAL7-NetworkCube/2.0",
        BodyLimit:         10 * 1024 * 1024, // 10MB
        CompressedFileSuffix: ".gz",
        ProxyHeader:       fiber.HeaderXForwardedFor,
        GETOnly:          false,
        ErrorHandler:     customErrorHandler,
    })
    
    return &HTTPServerCube{
        server: app,
        config: config,
        metrics: NewNetworkMetrics(),
        connectedCubes: make(map[string]FeatureCube),
    }
}

func (hsc *HTTPServerCube) SetupMiddleware() {
    // CORS 설정
    hsc.server.Use(cors.New(cors.Config{
        AllowOrigins: "*",
        AllowHeaders: "Origin, Content-Type, Accept, Authorization",
        AllowMethods: "GET, POST, PUT, DELETE, OPTIONS",
    }))
    
    // Rate Limiting
    hsc.server.Use(limiter.New(limiter.Config{
        Max:        1000,  // 분당 1000 요청
        Expiration: time.Minute,
        KeyGenerator: func(c *fiber.Ctx) string {
            return c.Get("X-Forwarded-For", c.IP())
        },
        LimitReached: func(c *fiber.Ctx) error {
            return c.Status(429).JSON(fiber.Map{
                "error": "Rate limit exceeded",
            })
        },
    }))
    
    // 메트릭 수집 미들웨어
    hsc.server.Use(hsc.metricsMiddleware)
}

// Feature Cube와 자동 연결
func (hsc *HTTPServerCube) ConnectFeatureCube(cube FeatureCube) error {
    cubeName := cube.GetName()
    hsc.connectedCubes[cubeName] = cube
    
    // 자동 엔드포인트 생성
    basePath := fmt.Sprintf("/api/%s", cubeName)
    
    // RESTful 엔드포인트 자동 등록
    hsc.server.Post(basePath, hsc.createHandler(cube, "CREATE"))
    hsc.server.Get(basePath+"/:id", hsc.createHandler(cube, "READ"))
    hsc.server.Put(basePath+"/:id", hsc.createHandler(cube, "UPDATE"))
    hsc.server.Delete(basePath+"/:id", hsc.createHandler(cube, "DELETE"))
    
    // 비즈니스 로직별 커스텀 엔드포인트
    methods := cube.GetBusinessMethods()
    for _, method := range methods {
        hsc.server.Post(
            fmt.Sprintf("%s/%s", basePath, method.Name),
            hsc.createHandler(cube, method.Name),
        )
    }
    
    return nil
}

// 지능적 라우팅 핸들러
func (hsc *HTTPServerCube) createHandler(cube FeatureCube, operation string) fiber.Handler {
    return func(c *fiber.Ctx) error {
        startTime := time.Now()
        
        // 요청 파싱
        request := ParseRequest(c, operation)
        
        // Feature Cube 호출
        result, err := cube.ProcessBusinessLogic(request)
        if err != nil {
            hsc.metrics.RecordError(operation)
            return c.Status(500).JSON(fiber.Map{"error": err.Error()})
        }
        
        // 응답 생성
        response := CreateResponse(result)
        
        // 메트릭 기록
        hsc.metrics.RecordRequest(operation, time.Since(startTime))
        
        return c.JSON(response)
    }
}
```

### **🔄 실시간 통신 Network Cube**

```go
// 🟩 WebSocket Network Cube
type WebSocketCube struct {
    CubeInfo
    
    connections sync.Map  // 연결 관리
    broadcaster *MessageBroadcaster
    rooms       map[string]*Room
    
    // 실시간 이벤트 스트림
    eventStream chan Event
}

func (wsc *WebSocketCube) HandleConnection(c *websocket.Conn) {
    defer c.Close()
    
    // 연결 등록
    connectionID := generateConnectionID()
    wsc.connections.Store(connectionID, c)
    
    // 실시간 이벤트 스트리밍
    go wsc.streamEvents(c, connectionID)
    
    // 메시지 처리 루프
    for {
        var message WSMessage
        if err := c.ReadJSON(&message); err != nil {
            break
        }
        
        // 메시지 타입별 처리
        switch message.Type {
        case "SUBSCRIBE_CUBE":
            wsc.subscribeToCube(connectionID, message.Data["cube_name"])
        case "BUSINESS_REQUEST":
            wsc.forwardToFeatureCube(message)
        case "ROOM_JOIN":
            wsc.joinRoom(connectionID, message.Data["room_id"])
        }
    }
    
    // 연결 해제
    wsc.connections.Delete(connectionID)
}

// 실시간 큐브 이벤트 스트리밍
func (wsc *WebSocketCube) streamEvents(conn *websocket.Conn, connID string) {
    for event := range wsc.eventStream {
        // 연결별 필터링
        if wsc.shouldSendEvent(connID, event) {
            conn.WriteJSON(WSMessage{
                Type: "CUBE_EVENT",
                Data: event.ToMap(),
                Timestamp: time.Now(),
            })
        }
    }
}
```

## 🟨 **Data Cubes (데이터 저장 큐브)**

### **💾 역할과 책임**

```yaml
data_cubes:
  purpose: "데이터의 안전한 저장, 조회, 관리"
  metaphor: "인체의 골격과 지방 - 구조 지지와 에너지 저장"
  color_meaning: "지식과 기억의 보관소"
  
  primary_responsibilities:
    - "데이터베이스 연결 관리"
    - "CRUD 연산 최적화"
    - "트랜잭션 관리"
    - "데이터 마이그레이션"
    - "백업 및 복구"
    - "캐싱 전략"
    - "데이터 검증"
    
  technology_stack:
    primary_language: "Rust (메모리 안전성 + 고성능)"
    secondary: "Go (연결 풀 관리)"
    databases:
      - "PostgreSQL: 관계형 데이터"
      - "Redis: 캐시 및 세션"
      - "MongoDB: 문서형 데이터"
      - "Elasticsearch: 검색 엔진"
      - "S3: 객체 저장소"
    
  performance_targets:
    query_time: "< 5ms"
    connection_pool: "1000+ connections"
    cache_hit_ratio: "> 95%"
    data_integrity: "100%"
```

### **🔍 Data Cube 구현 예시**

```rust
// 🟨 PostgreSQL Data Cube
use sqlx::{PgPool, Row, Transaction, Postgres};
use serde::{Serialize, Deserialize};
use async_trait::async_trait;

pub struct PostgreSQLCube {
    cube_info: CubeInfo,
    pool: PgPool,
    cache: Arc<RwLock<LRUCache<String, CachedData>>>,
    metrics: DataMetrics,
    migration_manager: MigrationManager,
}

impl PostgreSQLCube {
    pub async fn new(database_url: &str, max_connections: u32) -> Result<Self> {
        // 최적화된 연결 풀 설정
        let pool = PgPool::builder()
            .max_connections(max_connections)
            .min_connections(10)
            .acquire_timeout(Duration::from_secs(10))
            .idle_timeout(Some(Duration::from_secs(600)))
            .max_lifetime(Some(Duration::from_secs(1800)))
            .build(database_url)
            .await?;
        
        // 연결 테스트
        sqlx::query("SELECT 1").fetch_one(&pool).await?;
        
        Ok(Self {
            cube_info: CubeInfo {
                name: "postgresql-data-cube".to_string(),
                color: CubeColor::Yellow,
                version: "2.0.0".to_string(),
            },
            pool,
            cache: Arc::new(RwLock::new(LRUCache::new(10_000))),
            metrics: DataMetrics::new(),
            migration_manager: MigrationManager::new(),
        })
    }
    
    // 고성능 쿼리 (캐시 + prepared statements)
    pub async fn query_optimized<T>(&self, query: &str, params: &[&(dyn ToSql + Sync)]) -> Result<Vec<T>>
    where
        T: for<'r> FromRow<'r, PgRow> + Send + Unpin + Serialize + DeserializeOwned,
    {
        // 1. 캐시 확인
        let cache_key = self.generate_cache_key(query, params);
        if let Some(cached) = self.get_from_cache(&cache_key).await {
            self.metrics.record_cache_hit();
            return Ok(cached);
        }
        
        // 2. 데이터베이스 쿼리
        let start_time = Instant::now();
        let mut query_builder = sqlx::query_as::<_, T>(query);
        
        // 파라미터 바인딩
        for param in params {
            query_builder = query_builder.bind(param);
        }
        
        let results = query_builder.fetch_all(&self.pool).await?;
        
        // 3. 메트릭 기록
        self.metrics.record_query(query, start_time.elapsed());
        
        // 4. 캐시 저장 (비동기)
        let results_clone = results.clone();
        let cache_clone = Arc::clone(&self.cache);
        tokio::spawn(async move {
            let mut cache = cache_clone.write().await;
            cache.put(cache_key, results_clone);
        });
        
        Ok(results)
    }
    
    // 트랜잭션 관리
    pub async fn execute_transaction<F, T>(&self, f: F) -> Result<T>
    where
        F: FnOnce(&mut Transaction<Postgres>) -> Pin<Box<dyn Future<Output = Result<T>> + Send>> + Send,
        T: Send,
    {
        let mut tx = self.pool.begin().await?;
        
        match f(&mut tx).await {
            Ok(result) => {
                tx.commit().await?;
                self.metrics.record_transaction_success();
                Ok(result)
            }
            Err(e) => {
                tx.rollback().await?;
                self.metrics.record_transaction_failure();
                Err(e)
            }
        }
    }
    
    // 자동 마이그레이션
    pub async fn auto_migrate(&self) -> Result<()> {
        self.migration_manager.run_pending_migrations(&self.pool).await
    }
}

// 사주 데이터 특화 메서드
impl PostgreSQLCube {
    pub async fn store_saju_result(&self, user_id: i64, saju_data: &SajuResult) -> Result<i64> {
        let query = r#"
            INSERT INTO saju_results (user_id, birth_data, pillars, wuxing_analysis, 
                                    sipsin_analysis, interpretation, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
            RETURNING id
        "#;
        
        let row = sqlx::query(query)
            .bind(user_id)
            .bind(serde_json::to_value(&saju_data.birth_data)?)
            .bind(serde_json::to_value(&saju_data.pillars)?)
            .bind(serde_json::to_value(&saju_data.wuxing_analysis)?)
            .bind(serde_json::to_value(&saju_data.sipsin_analysis)?)
            .bind(&saju_data.interpretation)
            .fetch_one(&self.pool)
            .await?;
        
        Ok(row.get("id"))
    }
    
    pub async fn get_user_saju_history(&self, user_id: i64, limit: i32) -> Result<Vec<SajuHistoryItem>> {
        let query = r#"
            SELECT id, birth_data, pillars, interpretation, created_at
            FROM saju_results 
            WHERE user_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2
        "#;
        
        self.query_optimized(query, &[&user_id, &limit]).await
    }
}
```

### **⚡ Redis Cache Data Cube**

```rust
// 🟨 Redis Cache Data Cube
pub struct RedisCacheCube {
    cube_info: CubeInfo,
    client: redis::Client,
    connection_manager: ConnectionManager,
    serializer: SerializationEngine,
}

impl RedisCacheCube {
    // 지능형 캐싱 전략
    pub async fn set_with_strategy<T>(&self, key: &str, value: &T, strategy: CacheStrategy) -> Result<()>
    where
        T: Serialize,
    {
        let mut conn = self.connection_manager.get_connection().await?;
        let serialized = self.serializer.serialize(value)?;
        
        match strategy {
            CacheStrategy::ShortTerm => {
                // 5분 TTL
                redis::cmd("SET")
                    .arg(key)
                    .arg(serialized)
                    .arg("EX")
                    .arg(300)
                    .execute_async(&mut conn)
                    .await?;
            }
            CacheStrategy::LongTerm => {
                // 1일 TTL
                redis::cmd("SET")
                    .arg(key)
                    .arg(serialized)
                    .arg("EX")
                    .arg(86400)
                    .execute_async(&mut conn)
                    .await?;
            }
            CacheStrategy::Permanent => {
                // TTL 없음
                redis::cmd("SET")
                    .arg(key)
                    .arg(serialized)
                    .execute_async(&mut conn)
                    .await?;
            }
            CacheStrategy::Adaptive(usage_pattern) => {
                // AI 기반 적응형 TTL
                let ttl = self.calculate_adaptive_ttl(usage_pattern);
                redis::cmd("SET")
                    .arg(key)
                    .arg(serialized)
                    .arg("EX")
                    .arg(ttl)
                    .execute_async(&mut conn)
                    .await?;
            }
        }
        
        Ok(())
    }
    
    // 배치 처리 최적화
    pub async fn batch_get<T>(&self, keys: &[&str]) -> Result<Vec<Option<T>>>
    where
        T: DeserializeOwned,
    {
        let mut conn = self.connection_manager.get_connection().await?;
        
        // 파이프라인으로 배치 처리
        let mut pipe = redis::pipe();
        for key in keys {
            pipe.get(*key);
        }
        
        let results: Vec<Option<String>> = pipe.query_async(&mut conn).await?;
        
        // 병렬 역직렬화
        let deserialized = futures::future::try_join_all(
            results.into_iter().map(|opt_str| async {
                match opt_str {
                    Some(s) => self.serializer.deserialize(&s).map(Some),
                    None => Ok(None),
                }
            })
        ).await?;
        
        Ok(deserialized)
    }
}
```

## 🟥 **Security Cubes (보안 인증 큐브)**

### **🛡️ 역할과 책임**

```yaml
security_cubes:
  purpose: "시스템 보안과 접근 제어"
  metaphor: "인체의 면역계 - 외부 침입자로부터 보호"
  color_meaning: "경고와 방어의 레드 얼럿"
  
  primary_responsibilities:
    - "사용자 인증 (Authentication)"
    - "권한 부여 (Authorization)"  
    - "API 키 관리"
    - "토큰 검증 (JWT, OAuth2)"
    - "레이트 리미팅"
    - "데이터 암호화"
    - "보안 감사 로깅"
    - "취약점 스캔"
    
  technology_stack:
    primary_language: "Rust (메모리 안전성) + Go (동시성)"
    cryptography: "Ring, RustCrypto"
    authentication: "JWT, OAuth2, SAML"
    encryption: "AES-256-GCM, ChaCha20-Poly1305"
    
  security_standards:
    - "OWASP Top 10 준수"
    - "GDPR 컴플라이언스"
    - "SOC 2 Type II"
    - "ISO 27001"
```

### **🔐 Security Cube 구현 예시**

```rust
// 🟥 JWT Authentication Security Cube
use jsonwebtoken::{encode, decode, Header, Algorithm, Validation, EncodingKey, DecodingKey};
use ring::rand::{SecureRandom, SystemRandom};
use argon2::{Argon2, PasswordHash, PasswordHasher, PasswordVerifier};

pub struct JWTSecurityCube {
    cube_info: CubeInfo,
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    algorithm: Algorithm,
    token_expiry: Duration,
    refresh_expiry: Duration,
    
    // 보안 강화 기능
    blacklisted_tokens: Arc<RwLock<HashSet<String>>>,
    failed_attempts: Arc<RwLock<HashMap<String, FailedAttempt>>>,
    rate_limiter: RateLimiter,
}

impl JWTSecurityCube {
    pub fn new(secret: &str) -> Self {
        Self {
            cube_info: CubeInfo {
                name: "jwt-security-cube".to_string(),
                color: CubeColor::Red,
                version: "2.0.0".to_string(),
            },
            encoding_key: EncodingKey::from_secret(secret.as_ref()),
            decoding_key: DecodingKey::from_secret(secret.as_ref()),
            algorithm: Algorithm::HS256,
            token_expiry: Duration::from_secs(3600),     // 1시간
            refresh_expiry: Duration::from_secs(604800), // 7일
            blacklisted_tokens: Arc::new(RwLock::new(HashSet::new())),
            failed_attempts: Arc::new(RwLock::new(HashMap::new())),
            rate_limiter: RateLimiter::new(100, Duration::from_secs(60)), // 분당 100회
        }
    }
    
    // 보안 강화된 사용자 인증
    pub async fn authenticate_user(&self, credentials: &UserCredentials) -> Result<AuthResult> {
        // 1. Rate Limiting 체크
        if !self.rate_limiter.check_rate(&credentials.username) {
            return Err(SecurityError::RateLimitExceeded);
        }
        
        // 2. 계정 잠금 체크
        if self.is_account_locked(&credentials.username).await {
            return Err(SecurityError::AccountLocked);
        }
        
        // 3. 비밀번호 검증 (Argon2)
        let user = self.get_user_securely(&credentials.username).await?;
        let password_hash = PasswordHash::new(&user.password_hash)?;
        
        match Argon2::default().verify_password(credentials.password.as_bytes(), &password_hash) {
            Ok(_) => {
                // 성공: 실패 카운터 리셋
                self.reset_failed_attempts(&credentials.username).await;
                
                // JWT 토큰 생성
                let tokens = self.generate_token_pair(&user).await?;
                
                // 보안 이벤트 로깅
                self.log_security_event(SecurityEvent::LoginSuccess {
                    user_id: user.id,
                    ip_address: credentials.ip_address.clone(),
                    user_agent: credentials.user_agent.clone(),
                    timestamp: Utc::now(),
                }).await;
                
                Ok(AuthResult::Success(tokens))
            }
            Err(_) => {
                // 실패: 카운터 증가
                self.increment_failed_attempts(&credentials.username).await;
                
                // 보안 이벤트 로깅
                self.log_security_event(SecurityEvent::LoginFailed {
                    username: credentials.username.clone(),
                    ip_address: credentials.ip_address.clone(),
                    reason: "Invalid password".to_string(),
                    timestamp: Utc::now(),
                }).await;
                
                Err(SecurityError::InvalidCredentials)
            }
        }
    }
    
    // 토큰 검증 (보안 강화)
    pub async fn validate_token(&self, token: &str) -> Result<Claims> {
        // 1. 블랙리스트 체크
        let blacklisted = self.blacklisted_tokens.read().await;
        if blacklisted.contains(token) {
            return Err(SecurityError::TokenBlacklisted);
        }
        
        // 2. JWT 구조 검증
        let validation = Validation {
            algorithms: vec![self.algorithm],
            validate_exp: true,
            validate_nbf: true,
            validate_aud: false,
            leeway: 60, // 1분 여유
            ..Validation::default()
        };
        
        // 3. 서명 검증
        match decode::<Claims>(token, &self.decoding_key, &validation) {
            Ok(token_data) => {
                let claims = token_data.claims;
                
                // 4. 추가 보안 검증
                if self.is_token_suspicious(&claims).await {
                    self.log_security_event(SecurityEvent::SuspiciousToken {
                        token_id: claims.jti.clone(),
                        user_id: claims.sub,
                        reason: "Suspicious activity detected".to_string(),
                        timestamp: Utc::now(),
                    }).await;
                    
                    return Err(SecurityError::SuspiciousActivity);
                }
                
                Ok(claims)
            }
            Err(e) => {
                self.log_security_event(SecurityEvent::TokenValidationFailed {
                    error: e.to_string(),
                    timestamp: Utc::now(),
                }).await;
                
                Err(SecurityError::InvalidToken)
            }
        }
    }
    
    // 토큰 무효화 (로그아웃)
    pub async fn invalidate_token(&self, token: &str) -> Result<()> {
        // 토큰 파싱 (서명 검증 없이)
        let header = decode_header(token)?;
        let claims: Claims = decode(token, &self.decoding_key, &Validation::new(header.alg))?
            .claims;
        
        // 블랙리스트에 추가 (만료까지)
        let mut blacklisted = self.blacklisted_tokens.write().await;
        blacklisted.insert(token.to_string());
        
        // 보안 이벤트 로깅
        self.log_security_event(SecurityEvent::TokenInvalidated {
            token_id: claims.jti,
            user_id: claims.sub,
            timestamp: Utc::now(),
        }).await;
        
        Ok(())
    }
    
    // 의심스러운 활동 탐지
    async fn is_token_suspicious(&self, claims: &Claims) -> bool {
        // 1. 비정상적인 위치에서의 접근
        if self.detect_unusual_location(&claims.ip_address).await {
            return true;
        }
        
        // 2. 과도한 권한 사용
        if self.detect_privilege_escalation(claims.sub).await {
            return true;
        }
        
        // 3. 비정상적인 시간대 접근
        if self.detect_unusual_timing(claims.sub).await {
            return true;
        }
        
        false
    }
}
```

### **🚨 Rate Limiting Security Cube**

```go
// 🟥 고급 Rate Limiting Security Cube
package security

import (
    "sync"
    "time"
    "golang.org/x/time/rate"
)

type RateLimiterCube struct {
    CubeInfo
    
    // 계층적 Rate Limiting
    globalLimiter    *rate.Limiter           // 전체 시스템 레벨
    userLimiters     map[string]*rate.Limiter // 사용자별 레벨
    endpointLimiters map[string]*rate.Limiter // 엔드포인트별 레벨
    ipLimiters       map[string]*rate.Limiter // IP별 레벨
    
    // 동적 조정
    adaptiveLimiting bool
    metrics          *RateLimitMetrics
    
    mu sync.RWMutex
}

func NewRateLimiterCube() *RateLimiterCube {
    return &RateLimiterCube{
        globalLimiter:    rate.NewLimiter(10000, 20000), // 초당 1만, 버스트 2만
        userLimiters:     make(map[string]*rate.Limiter),
        endpointLimiters: make(map[string]*rate.Limiter),
        ipLimiters:       make(map[string]*rate.Limiter),
        adaptiveLimiting: true,
        metrics:          NewRateLimitMetrics(),
    }
}

// 다층 Rate Limiting 검사
func (rlc *RateLimiterCube) CheckRateLimit(ctx context.Context, req *RateLimitRequest) error {
    // 1. 글로벌 레벨 체크
    if !rlc.globalLimiter.Allow() {
        rlc.metrics.RecordRateLimitHit("global", req.IP)
        return ErrGlobalRateLimitExceeded
    }
    
    // 2. IP 레벨 체크
    if !rlc.checkIPRateLimit(req.IP) {
        rlc.metrics.RecordRateLimitHit("ip", req.IP)
        return ErrIPRateLimitExceeded
    }
    
    // 3. 사용자 레벨 체크 (인증된 경우)
    if req.UserID != "" {
        if !rlc.checkUserRateLimit(req.UserID) {
            rlc.metrics.RecordRateLimitHit("user", req.UserID)
            return ErrUserRateLimitExceeded
        }
    }
    
    // 4. 엔드포인트 레벨 체크
    if !rlc.checkEndpointRateLimit(req.Endpoint) {
        rlc.metrics.RecordRateLimitHit("endpoint", req.Endpoint)
        return ErrEndpointRateLimitExceeded
    }
    
    return nil
}

// 적응형 Rate Limiting (AI 기반)
func (rlc *RateLimiterCube) AdaptRateLimits() {
    if !rlc.adaptiveLimiting {
        return
    }
    
    ticker := time.NewTicker(time.Minute * 5) // 5분마다 조정
    defer ticker.Stop()
    
    for range ticker.C {
        // 시스템 부하 분석
        systemLoad := rlc.metrics.GetSystemLoad()
        
        // 동적 한도 계산
        newGlobalLimit := rlc.calculateOptimalLimit(systemLoad)
        
        // 한도 조정
        rlc.globalLimiter.SetLimit(rate.Limit(newGlobalLimit))
        
        log.Printf("Rate limit adjusted to %d/sec based on system load %.2f", 
                   newGlobalLimit, systemLoad)
    }
}

// DDoS 공격 탐지 및 차단
func (rlc *RateLimiterCube) DetectAndBlockDDoS() {
    // 실시간 트래픽 패턴 분석
    go func() {
        for {
            suspiciousIPs := rlc.analyzeSuspiciousTraffic()
            
            for _, ip := range suspiciousIPs {
                // 의심스러운 IP 자동 차단
                rlc.blockIP(ip, time.Hour) // 1시간 차단
                
                // 보안 이벤트 발생
                rlc.emitSecurityEvent(SecurityEvent{
                    Type:      "DDoS_DETECTED",
                    IP:        ip,
                    Timestamp: time.Now(),
                    Details: map[string]interface{}{
                        "requests_per_second": rlc.metrics.GetIPRequestRate(ip),
                        "blocked_duration":    time.Hour,
                    },
                })
            }
            
            time.Sleep(time.Second * 10) // 10초마다 분석
        }
    }()
}
```

이후 나머지 색상 큐브들(🟪 Monitoring, 🟧 UI, 🟫 Integration)과 종합 정리를 계속 작성하겠습니다. 

## 🟪 **Monitoring Cubes (관찰성 큐브)**

### **📊 역할과 책임**

```yaml
monitoring_cubes:
  purpose: "시스템 상태 관찰과 성능 분석"
  metaphor: "인체의 감각기관 - 눈, 귀, 피부로 상황 파악"
  color_meaning: "통찰과 분석의 보라빛 지혜"
  
  primary_responsibilities:
    - "메트릭 수집 및 저장"
    - "분산 트레이싱"
    - "로그 집계 및 분석"
    - "실시간 알림"
    - "대시보드 시각화"
    - "성능 프로파일링"
    - "SLA 모니터링"
    - "예측 분석"
    
  technology_stack:
    metrics: "Prometheus, InfluxDB"
    tracing: "Jaeger, Zipkin"
    logging: "ELK Stack, Loki"
    alerting: "AlertManager, PagerDuty"
    visualization: "Grafana, Custom Dashboards"
    
  observability_targets:
    metric_resolution: "1초 간격"
    trace_sampling: "100% (critical paths)"
    log_retention: "90일"
    alert_latency: "< 10초"
```

### **📈 Monitoring Cube 구현 예시**

```go
// 🟪 Prometheus Metrics Monitoring Cube
package monitoring

import (
    "context"
    "time"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/trace"
)

type PrometheusMonitoringCube struct {
    CubeInfo
    
    // 메트릭 컬렉터들
    requestCounter    *prometheus.CounterVec
    responseTime      *prometheus.HistogramVec
    activeConnections prometheus.Gauge
    errorRate         *prometheus.GaugeVec
    cubeHealth        *prometheus.GaugeVec
    
    // 분산 트레이싱
    tracer trace.Tracer
    
    // 알림 매니저
    alertManager *AlertManager
    
    // 예측 엔진
    predictor *PerformancePredictor
}

func NewPrometheusMonitoringCube() *PrometheusMonitoringCube {
    return &PrometheusMonitoringCube{
        // 요청 카운터
        requestCounter: promauto.NewCounterVec(
            prometheus.CounterOpts{
                Name: "heal7_cube_requests_total",
                Help: "Total number of cube requests",
            },
            []string{"cube_name", "cube_color", "method", "status"},
        ),
        
        // 응답 시간 히스토그램
        responseTime: promauto.NewHistogramVec(
            prometheus.HistogramOpts{
                Name:    "heal7_cube_request_duration_seconds",
                Help:    "Request duration in seconds",
                Buckets: []float64{.001, .005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
            },
            []string{"cube_name", "cube_color", "method"},
        ),
        
        // 활성 연결 수
        activeConnections: promauto.NewGauge(
            prometheus.GaugeOpts{
                Name: "heal7_active_connections",
                Help: "Number of active connections",
            },
        ),
        
        // 에러율
        errorRate: promauto.NewGaugeVec(
            prometheus.GaugeOpts{
                Name: "heal7_cube_error_rate",
                Help: "Error rate by cube",
            },
            []string{"cube_name", "cube_color"},
        ),
        
        // 큐브 헬스
        cubeHealth: promauto.NewGaugeVec(
            prometheus.GaugeOpts{
                Name: "heal7_cube_health_score",
                Help: "Health score of each cube (0-100)",
            },
            []string{"cube_name", "cube_color"},
        ),
        
        tracer:       otel.Tracer("heal7-monitoring"),
        alertManager: NewAlertManager(),
        predictor:    NewPerformancePredictor(),
    }
}

// 큐브 메트릭 자동 수집
func (pmc *PrometheusMonitoringCube) MonitorCube(cube CubeInterface) error {
    cubeName := cube.GetName()
    cubeColor := cube.GetColor().String()
    
    // 주기적 헬스 체크
    go pmc.periodicHealthCheck(cubeName, cubeColor, cube)
    
    // 메트릭 수집
    go pmc.collectCubeMetrics(cubeName, cubeColor, cube)
    
    // 성능 예측
    go pmc.predictPerformance(cubeName, cube)
    
    return nil
}

// 실시간 헬스 체크
func (pmc *PrometheusMonitoringCube) periodicHealthCheck(name, color string, cube CubeInterface) {
    ticker := time.NewTicker(10 * time.Second) // 10초마다
    defer ticker.Stop()
    
    for range ticker.C {
        ctx, span := pmc.tracer.Start(context.Background(), "health-check")
        
        health := cube.GetHealth()
        healthScore := pmc.calculateHealthScore(health)
        
        pmc.cubeHealth.WithLabelValues(name, color).Set(float64(healthScore))
        
        // 헬스 점수가 낮으면 알림
        if healthScore < 70 {
            pmc.alertManager.SendAlert(Alert{
                Severity:    "warning",
                Summary:     fmt.Sprintf("Cube %s health degraded", name),
                Description: fmt.Sprintf("Health score: %d/100", healthScore),
                Labels: map[string]string{
                    "cube_name":  name,
                    "cube_color": color,
                },
            })
        }
        
        span.End()
    }
}

// 성능 예측 및 자동 스케일링
func (pmc *PrometheusMonitoringCube) predictPerformance(name string, cube CubeInterface) {
    ticker := time.NewTicker(5 * time.Minute) // 5분마다
    defer ticker.Stop()
    
    for range ticker.C {
        // 현재 메트릭 수집
        metrics := cube.GetMetrics()
        
        // 성능 예측
        prediction := pmc.predictor.PredictLoad(name, metrics)
        
        // 예측 결과에 따른 권장사항
        if prediction.ExpectedLoad > 0.8 { // 80% 부하 예상
            pmc.alertManager.SendAlert(Alert{
                Severity: "info",
                Summary:  fmt.Sprintf("High load predicted for cube %s", name),
                Description: fmt.Sprintf(
                    "Expected load: %.1f%% in next %s", 
                    prediction.ExpectedLoad*100,
                    prediction.TimeWindow,
                ),
                Labels: map[string]string{
                    "cube_name": name,
                    "action":    "scale_up_recommended",
                },
            })
        }
    }
}
```

## 🟧 **UI Cubes (사용자 인터페이스 큐브)**

### **🎨 역할과 책임**

```yaml
ui_cubes:
  purpose: "사용자와의 상호작용 인터페이스"
  metaphor: "인체의 피부와 얼굴 - 외부와의 소통 창구"
  color_meaning: "활력과 상호작용의 주황빛 에너지"
  
  primary_responsibilities:
    - "사용자 인터페이스 렌더링"
    - "상호작용 이벤트 처리"
    - "실시간 데이터 시각화"
    - "반응형 디자인"
    - "접근성 보장"
    - "성능 최적화"
    - "오프라인 지원"
    
  technology_stack:
    primary: "TypeScript, React/Vue"
    styling: "Tailwind CSS, Styled Components"
    3d_graphics: "Three.js, WebGL"
    charts: "D3.js, Chart.js"
    mobile: "React Native, Flutter"
    
  ux_targets:
    loading_time: "< 2초"
    interaction_delay: "< 100ms"
    lighthouse_score: "> 95"
    accessibility: "WCAG 2.1 AA"
```

## 🟫 **Integration Cubes (외부 연동 큐브)**

### **🔗 역할과 책임**

```yaml
integration_cubes:
  purpose: "외부 시스템과의 연동 및 데이터 교환"
  metaphor: "인체의 소화계 - 외부 영양소 흡수 및 처리"
  color_meaning: "안정성과 신뢰성의 갈색 기반"
  
  primary_responsibilities:
    - "외부 API 호출"
    - "데이터 형식 변환"
    - "프로토콜 어댑터"
    - "에러 처리 및 재시도"
    - "써드파티 서비스 래핑"
    - "웹훅 처리"
    - "이벤트 스트리밍"
    
  integration_types:
    payment: "결제 게이트웨이 (PG)"
    social: "소셜 로그인 (OAuth2)"
    notification: "이메일, SMS, 푸시"
    ai_services: "OpenAI, Anthropic, Google"
    storage: "AWS S3, Google Cloud"
    
  reliability_targets:
    retry_attempts: "3회 (지수 백오프)"
    timeout: "30초"
    circuit_breaker: "5회 실패 시 차단"
    uptime: "99.9%"
```

## 🎯 **색상별 큐브 조합 패턴**

### **📊 서비스 타입별 권장 조합**

```yaml
service_patterns:
  simple_api:
    required: [🟦 Feature, 🟩 Network, 🟨 Data]
    optional: [🟥 Security]
    complexity: "Low"
    
  enterprise_app:
    required: [🟦 Feature, 🟩 Network, 🟨 Data, 🟥 Security, 🟪 Monitoring]
    optional: [🟧 UI, 🟫 Integration]
    complexity: "Medium"
    
  full_platform:
    required: "All 7 colors"
    complexity: "High"
    scalability: "Maximum"
    
  microservice:
    core: [🟦 Feature, 🟩 Network]
    support: [🟥 Security, 🟪 Monitoring]
    complexity: "Medium"
    
  data_pipeline:
    core: [🟨 Data, 🟫 Integration]
    support: [🟪 Monitoring, 🟥 Security]
    complexity: "Medium"
```

### **🔄 큐브 상호작용 매트릭스**

```
       🟦 🟩 🟨 🟥 🟪 🟧 🟫
    🟦 ❌ ⭐ ⭐ ⭐ ⚡ ⚡ ⭐
    🟩 ⭐ ❌ ⭐ ⭐ ⭐ ⭐ ⭐
    🟨 ⭐ ⭐ ❌ ⭐ ⭐ ⚡ ⭐
    🟥 ⭐ ⭐ ⭐ ❌ ⚡ ⚡ ⭐
    🟪 ⚡ ⭐ ⚡ ⚡ ❌ ⚡ ⚡
    🟧 ⚡ ⭐ ⚡ ⚡ ⚡ ❌ ⚡
    🟫 ⭐ ⭐ ⭐ ⭐ ⚡ ⚡ ❌

범례:
⭐ 강한 결합 (직접 통신)
⚡ 약한 결합 (이벤트 기반)
❌ 자기 자신
```

## 💡 **색상 체계의 혁신적 특징**

### **🧠 인지 과학 기반 설계**

```yaml
cognitive_benefits:
  pattern_recognition:
    - "개발자가 한눈에 모듈 역할 파악"
    - "시각적 아키텍처 다이어그램"
    - "색상 기반 빠른 디버깅"
    
  team_collaboration:
    - "색상별 팀 전문화 가능"
    - "명확한 책임 경계"
    - "효과적인 코드 리뷰"
    
  learning_curve:
    - "새 개발자 빠른 온보딩"
    - "직관적인 시스템 이해"
    - "실수 방지 효과"
```

### **🎨 확장성과 유연성**

```yaml
extensibility:
  new_colors:
    - "필요시 새로운 색상 추가 가능"
    - "하위 색상 분류 (Light Blue, Dark Blue)"
    - "그래디언트를 통한 하이브리드 큐브"
    
  color_evolution:
    - "큐브 성숙도에 따른 색상 진화"
    - "알파(투명) → 베타(반투명) → 프로덕션(불투명)"
    - "성능에 따른 색상 밝기 조절"
```

## 🎯 **결론 및 활용 가이드**

### **🚀 색상 체계의 핵심 가치**

큐브 색상 체계 v2.0은 단순한 시각적 분류를 넘어, **인지과학과 생체모방공학을 기반으로 한 혁신적인 아키텍처 도구**입니다.

```yaml
핵심_가치:
  직관성: "색상만 보고도 역할 이해 가능"
  확장성: "새로운 도메인에 쉽게 적용"
  표준화: "팀간 일관된 아키텍처 언어"
  효율성: "빠른 의사결정과 문제 해결"
  
실무_적용:
  설계단계: "색상으로 아키텍처 스케치"
  개발단계: "색상별 팀 분업"
  운영단계: "색상 기반 모니터링"
  유지보수: "색상으로 빠른 문제 위치 파악"
```

**HEAL7 큐브 색상 체계**는 복잡한 분산 시스템을 **직관적이고 관리하기 쉬운 컬러풀한 레고 블록**으로 변환하여, 개발 생산성과 시스템 이해도를 혁신적으로 향상시킵니다.

---

*🌈 이 색상 체계는 과학적 근거와 실무 경험을 바탕으로 설계되었습니다.*  
*🎨 모든 색상 선택은 인지과학과 사용자 경험을 고려한 결과입니다.*  
*🔄 지속적 개선: 실제 사용 피드백을 반영하여 체계를 진화시킵니다.*