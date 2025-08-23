# 🧩 큐브 조립 패턴 v2.0

> **레고마스터 가이드**: 큐브들을 어떻게 조립할 것인가  
> **체계적 접근**: 8가지 핵심 조립 패턴과 실전 구현법  
> **HEAL7 적용**: 실제 서비스에서 사용할 수 있는 구체적 예시  
> **최종 업데이트**: 2025-08-20 17:30 UTC

## 🎯 **큐브 조립의 철학**

### **🧠 조립 설계 원칙**

```yaml
assembly_philosophy:
  핵심_원칙:
    single_responsibility: "하나의 큐브는 하나의 책임만"
    loose_coupling: "큐브간 느슨한 결합"
    high_cohesion: "큐브 내부는 강한 응집력"
    interface_segregation: "인터페이스는 작고 명확하게"
    
  조립_목표:
    scalability: "무한 확장 가능한 구조"
    maintainability: "유지보수 용이성"
    testability: "개별 테스트 가능성"
    replaceability: "교체 가능성"
    
  금지_사항:
    tight_coupling: "큐브간 강한 의존성 금지"
    god_cube: "모든 기능을 담은 거대 큐브 금지"
    circular_dependency: "순환 의존성 절대 금지"
    shared_state: "큐브간 상태 공유 금지"
```

### **🔧 조립 레벨 정의**

```yaml
assembly_levels:
  Level_1_Atomic: "원자적 큐브 (단일 기능)"
    - 예시: "로그인 큐브, 계산 큐브, 저장 큐브"
    - 특징: "독립적 실행 가능"
    - 언어: "성능에 최적화된 언어 선택"
    
  Level_2_Molecular: "분자적 큐브 (기능 조합)"
    - 예시: "인증 플로우, 데이터 파이프라인"
    - 특징: "여러 원자 큐브의 조합"
    - 언어: "조합 로직에 적합한 언어"
    
  Level_3_Organism: "생물체적 큐브 (서비스 단위)"
    - 예시: "사주 서비스, 결제 서비스"
    - 특징: "완전한 비즈니스 기능"
    - 언어: "비즈니스 로직에 최적화"
    
  Level_4_Ecosystem: "생태계적 큐브 (전체 시스템)"
    - 예시: "HEAL7 플랫폼 전체"
    - 특징: "서비스들의 조합"
    - 언어: "오케스트레이션에 최적화"
```

## 🎨 **8대 핵심 조립 패턴**

### **1️⃣ Pipeline Pattern (파이프라인 패턴)**

```yaml
pipeline_pattern:
  개념: "데이터가 큐브들을 순차적으로 통과"
  적용_시나리오: "데이터 변환, 처리 파이프라인"
  
  구조:
    Input → [Cube A] → [Cube B] → [Cube C] → Output
    
  장점:
    - "명확한 데이터 흐름"
    - "단계별 디버깅 용이"
    - "부분 실패 격리"
    
  단점:
    - "순차 처리로 인한 지연"
    - "중간 단계 장애시 전체 중단"
```

**실제 구현 예시: HEAL7 사주 계산 파이프라인**

```rust
// Rust - 생년월일 검증 큐브
#[derive(Debug)]
pub struct DateValidationCube;

impl DateValidationCube {
    pub fn process(&self, input: &str) -> Result<ValidatedDate, ValidationError> {
        // 한국 전통 달력 검증 로직
        let parsed = self.parse_korean_date(input)?;
        self.validate_range(parsed)?;
        Ok(ValidatedDate::new(parsed))
    }
}

// Go - 사주 변환 큐브
type SajuConversionCube struct {
    astroEngine *AstrologyEngine
    cache       *redis.Client
}

func (s *SajuConversionCube) Process(date ValidatedDate) (*SajuComponents, error) {
    // 캐시 확인
    if cached := s.getCachedSaju(date); cached != nil {
        return cached, nil
    }
    
    // KASI API 호출 및 변환
    components := s.astroEngine.Convert(date)
    s.cache.Set(date.String(), components, 24*time.Hour)
    
    return components, nil
}

// Python - AI 해석 큐브
class SajuInterpretationCube:
    def __init__(self, ai_model: str):
        self.model = load_ai_model(ai_model)
        
    def process(self, saju_components: SajuComponents) -> SajuReading:
        # AI 모델을 통한 해석
        interpretation = self.model.interpret(
            saju_components.heavenly_stems,
            saju_components.earthly_branches,
            saju_components.elements
        )
        
        return SajuReading(
            components=saju_components,
            interpretation=interpretation,
            confidence=self.calculate_confidence(interpretation)
        )

// TypeScript - 결과 포맷팅 큐브
export class ResultFormattingCube {
    async process(reading: SajuReading): Promise<FormattedResult> {
        const formatted = {
            basicInfo: this.formatBasicInfo(reading.components),
            personality: this.formatPersonality(reading.interpretation),
            compatibility: this.formatCompatibility(reading.interpretation),
            recommendations: this.formatRecommendations(reading.interpretation),
            visualData: await this.generateCharts(reading)
        };
        
        return new FormattedResult(formatted);
    }
}
```

### **2️⃣ Hub Pattern (허브 패턴)**

```yaml
hub_pattern:
  개념: "중앙 허브를 통해 모든 큐브가 통신"
  적용_시나리오: "API Gateway, 메시지 브로커"
  
  구조:
           [Cube A]
              ↕
    [Cube D] ← [HUB] → [Cube B]
              ↕
           [Cube C]
           
  장점:
    - "중앙집중식 관리"
    - "라우팅 로직 분리"
    - "모니터링 용이"
    
  단점:
    - "허브가 단일점 장애"
    - "허브에 부하 집중"
```

**실제 구현 예시: HEAL7 API Gateway Hub**

```go
// Go - 중앙 허브 큐브
type APIGatewayHub struct {
    routes      map[string]ServiceCube
    rateLimiter *RateLimiter
    auth        *AuthenticationCube
    monitor     *MonitoringCube
}

func (h *APIGatewayHub) HandleRequest(req *http.Request) (*Response, error) {
    // 1. 인증 검증
    if !h.auth.ValidateToken(req.Header.Get("Authorization")) {
        return nil, ErrUnauthorized
    }
    
    // 2. 요율 제한
    if !h.rateLimiter.Allow(req.RemoteAddr) {
        return nil, ErrRateLimited
    }
    
    // 3. 라우팅
    service, exists := h.routes[req.URL.Path]
    if !exists {
        return nil, ErrNotFound
    }
    
    // 4. 요청 전달 및 응답 처리
    response, err := service.Process(req)
    h.monitor.RecordMetrics(req.URL.Path, err)
    
    return response, err
}

func (h *APIGatewayHub) RegisterService(path string, cube ServiceCube) {
    h.routes[path] = cube
}

// 서비스 큐브들을 허브에 등록
func (h *APIGatewayHub) Initialize() {
    h.RegisterService("/api/saju", &SajuServiceCube{})
    h.RegisterService("/api/health", &HealthServiceCube{})
    h.RegisterService("/api/ai", &AIServiceCube{})
    h.RegisterService("/api/user", &UserServiceCube{})
}
```

### **3️⃣ Event-Driven Pattern (이벤트 드리븐 패턴)**

```yaml
event_driven_pattern:
  개념: "이벤트 발생시 관련 큐브들이 반응"
  적용_시나리오: "실시간 알림, 비동기 처리"
  
  구조:
    [Event Producer] → [Event Bus] → [Event Consumers]
                                     ↓
                               [Cube A, Cube B, Cube C]
                               
  장점:
    - "높은 확장성"
    - "느슨한 결합"
    - "실시간 반응성"
    
  단점:
    - "복잡한 디버깅"
    - "이벤트 순서 보장 어려움"
```

**실제 구현 예시: HEAL7 사용자 행동 이벤트 시스템**

```python
# Python - 이벤트 버스 큐브
import asyncio
from typing import Dict, List, Callable
from dataclasses import dataclass

@dataclass
class Event:
    type: str
    user_id: str
    data: dict
    timestamp: float

class EventBusCube:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_store = []
    
    async def publish(self, event: Event):
        # 이벤트 저장
        self.event_store.append(event)
        
        # 구독자들에게 전파
        if event.type in self.subscribers:
            tasks = []
            for handler in self.subscribers[event.type]:
                tasks.append(asyncio.create_task(handler(event)))
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

# 사용자 행동 분석 큐브
class UserAnalyticsCube:
    def __init__(self, event_bus: EventBusCube):
        self.event_bus = event_bus
        self.user_sessions = {}
        
        # 이벤트 구독
        event_bus.subscribe("user.page_view", self.handle_page_view)
        event_bus.subscribe("user.saju_calculated", self.handle_saju_calculation)
        event_bus.subscribe("user.purchase", self.handle_purchase)
    
    async def handle_page_view(self, event: Event):
        # 페이지 뷰 분석
        user_id = event.user_id
        page = event.data.get('page')
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = UserSession(user_id)
        
        self.user_sessions[user_id].add_page_view(page, event.timestamp)
        
        # 관심도 스코어 업데이트
        await self.update_interest_score(user_id, page)
    
    async def handle_saju_calculation(self, event: Event):
        # 사주 계산 이벤트 처리
        await self.track_service_usage(event.user_id, "saju", event.data)
        
        # 추천 시스템에 이벤트 전파
        recommendation_event = Event(
            type="recommendation.update_profile",
            user_id=event.user_id,
            data={"service": "saju", "preferences": event.data},
            timestamp=event.timestamp
        )
        await self.event_bus.publish(recommendation_event)
```

### **4️⃣ Layered Pattern (계층화 패턴)**

```yaml
layered_pattern:
  개념: "큐브들을 계층별로 분리"
  적용_시나리오: "전통적인 웹 아키텍처"
  
  구조:
    ┌─────────────────┐ Presentation Layer
    │  [UI Cubes]     │
    ├─────────────────┤ Business Layer  
    │ [Logic Cubes]   │
    ├─────────────────┤ Data Layer
    │ [Storage Cubes] │
    └─────────────────┘
    
  장점:
    - "명확한 책임 분리"
    - "계층별 테스트 용이"
    - "익숙한 구조"
    
  단점:
    - "계층간 강한 의존성"
    - "성능 오버헤드"
```

**실제 구현 예시: HEAL7 웹 서비스 계층화**

```typescript
// TypeScript - Presentation Layer (프레젠테이션 계층)
export class SajuUIController {
    constructor(
        private sajuService: SajuBusinessService,
        private userService: UserBusinessService
    ) {}
    
    @Get('/saju/calculate')
    async calculateSaju(@Query() params: SajuCalculationParams): Promise<SajuUIResponse> {
        try {
            // 비즈니스 계층 호출
            const result = await this.sajuService.calculateUserSaju(
                params.userId,
                params.birthDate,
                params.birthTime
            );
            
            // UI 형태로 변환
            return this.formatForUI(result);
        } catch (error) {
            return this.handleUIError(error);
        }
    }
    
    private formatForUI(sajuResult: SajuResult): SajuUIResponse {
        return {
            personality: this.formatPersonality(sajuResult.traits),
            compatibility: this.formatCompatibility(sajuResult.relationships),
            forecast: this.formatForecast(sajuResult.predictions),
            visualData: this.generateChartData(sajuResult)
        };
    }
}

// Business Layer (비즈니스 계층)
export class SajuBusinessService {
    constructor(
        private sajuCalculator: SajuCalculationCube,
        private userRepository: UserDataRepository,
        private cacheService: CacheService
    ) {}
    
    async calculateUserSaju(userId: string, birthDate: Date, birthTime: string): Promise<SajuResult> {
        // 1. 사용자 정보 검증
        const user = await this.userRepository.findById(userId);
        if (!user) {
            throw new UserNotFoundError(userId);
        }
        
        // 2. 캐시 확인
        const cacheKey = `saju:${userId}:${birthDate.toISOString()}:${birthTime}`;
        const cached = await this.cacheService.get(cacheKey);
        if (cached) {
            return cached;
        }
        
        // 3. 사주 계산 수행
        const sajuData = await this.sajuCalculator.calculate({
            birthDate,
            birthTime,
            timezone: user.timezone || 'Asia/Seoul'
        });
        
        // 4. 비즈니스 규칙 적용
        const result = this.applyBusinessRules(sajuData, user);
        
        // 5. 캐시 저장
        await this.cacheService.set(cacheKey, result, 3600); // 1시간
        
        return result;
    }
    
    private applyBusinessRules(sajuData: RawSajuData, user: User): SajuResult {
        // 사용자 레벨에 따른 상세도 조정
        const detailLevel = user.subscriptionTier === 'premium' ? 'detailed' : 'basic';
        
        return {
            traits: this.processPersonalityTraits(sajuData, detailLevel),
            relationships: this.processCompatibility(sajuData, detailLevel),
            predictions: this.processForecast(sajuData, detailLevel),
            metadata: {
                calculatedAt: new Date(),
                accuracy: this.calculateAccuracy(sajuData),
                tier: user.subscriptionTier
            }
        };
    }
}

// Data Layer (데이터 계층)
export class UserDataRepository {
    constructor(private db: Database) {}
    
    async findById(userId: string): Promise<User | null> {
        const query = `
            SELECT u.*, p.subscription_tier, p.timezone
            FROM users u
            LEFT JOIN user_profiles p ON u.id = p.user_id
            WHERE u.id = $1 AND u.deleted_at IS NULL
        `;
        
        const result = await this.db.query(query, [userId]);
        return result.rows[0] ? this.mapToUser(result.rows[0]) : null;
    }
    
    async saveSajuCalculation(userId: string, calculation: SajuCalculation): Promise<void> {
        const query = `
            INSERT INTO saju_calculations (user_id, birth_date, birth_time, result_data, created_at)
            VALUES ($1, $2, $3, $4, NOW())
            ON CONFLICT (user_id, birth_date, birth_time) 
            DO UPDATE SET result_data = $4, updated_at = NOW()
        `;
        
        await this.db.query(query, [
            userId,
            calculation.birthDate,
            calculation.birthTime,
            JSON.stringify(calculation.result)
        ]);
    }
}
```

### **5️⃣ Micro-kernel Pattern (마이크로 커널 패턴)**

```yaml
micro_kernel_pattern:
  개념: "핵심 커널 + 플러그인 큐브들"
  적용_시나리오: "확장 가능한 플랫폼"
  
  구조:
         [Plugin A] [Plugin B] [Plugin C]
                 ↓       ↓       ↓
              [Micro-kernel Core]
                      ↓
                 [Core Services]
                 
  장점:
    - "무한한 확장성"
    - "플러그인 독립 개발"
    - "핵심 기능 안정성"
    
  단점:
    - "플러그인간 통신 복잡"
    - "버전 호환성 문제"
```

**실제 구현 예시: HEAL7 AI 서비스 플랫폼**

```python
# Python - 마이크로 커널 코어
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import importlib

class AIServicePlugin(ABC):
    """AI 서비스 플러그인 인터페이스"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        pass
    
    @abstractmethod
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        pass

class AIServiceKernel:
    """AI 서비스 마이크로 커널"""
    
    def __init__(self):
        self.plugins: Dict[str, AIServicePlugin] = {}
        self.core_services = {
            'auth': AuthenticationService(),
            'monitor': MonitoringService(),
            'cache': CacheService(),
            'queue': QueueService()
        }
    
    def register_plugin(self, plugin: AIServicePlugin):
        """플러그인 등록"""
        name = plugin.get_name()
        
        # 버전 호환성 검사
        if not self._check_compatibility(plugin):
            raise PluginCompatibilityError(f"Plugin {name} is not compatible")
        
        self.plugins[name] = plugin
        self.core_services['monitor'].log_plugin_registered(name, plugin.get_version())
    
    async def process_request(self, service_name: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """요청 처리"""
        
        # 1. 인증 확인
        if not await self.core_services['auth'].validate(request.get('token')):
            raise AuthenticationError()
        
        # 2. 플러그인 찾기
        if service_name not in self.plugins:
            raise ServiceNotFoundError(f"Service {service_name} not found")
        
        plugin = self.plugins[service_name]
        
        # 3. 캐시 확인
        cache_key = f"{service_name}:{hash(str(request))}"
        cached = await self.core_services['cache'].get(cache_key)
        if cached:
            return cached
        
        # 4. 플러그인 실행
        try:
            result = await plugin.process(request)
            
            # 5. 결과 캐싱
            await self.core_services['cache'].set(cache_key, result, ttl=3600)
            
            return result
            
        except Exception as e:
            await self.core_services['monitor'].log_error(service_name, e)
            raise
    
    def _check_compatibility(self, plugin: AIServicePlugin) -> bool:
        """플러그인 호환성 검사"""
        required_version = "2.0"
        plugin_version = plugin.get_version()
        
        # 간단한 버전 체크 (실제로는 더 복잡한 로직)
        return plugin_version.startswith(required_version[:3])

# 실제 AI 플러그인 구현 예시
class SajuInterpretationPlugin(AIServicePlugin):
    """사주 해석 AI 플러그인"""
    
    def __init__(self):
        self.model = self._load_saju_model()
    
    def get_name(self) -> str:
        return "saju_interpretation"
    
    def get_version(self) -> str:
        return "2.0.1"
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        saju_data = request.get('saju_data')
        interpretation_type = request.get('type', 'basic')
        
        if interpretation_type == 'personality':
            result = await self._interpret_personality(saju_data)
        elif interpretation_type == 'compatibility':
            result = await self._interpret_compatibility(saju_data)
        elif interpretation_type == 'forecast':
            result = await self._interpret_forecast(saju_data)
        else:
            result = await self._interpret_basic(saju_data)
        
        return {
            'interpretation': result,
            'confidence': self._calculate_confidence(result),
            'source': 'ai_model_v2.0.1'
        }
    
    def get_capabilities(self) -> List[str]:
        return ['personality', 'compatibility', 'forecast', 'basic']

class HealthAnalysisPlugin(AIServicePlugin):
    """건강 분석 AI 플러그인"""
    
    def get_name(self) -> str:
        return "health_analysis"
    
    def get_version(self) -> str:
        return "2.0.0"
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        health_data = request.get('health_data')
        user_profile = request.get('user_profile')
        
        # 건강 데이터 분석
        analysis = await self._analyze_health_patterns(health_data, user_profile)
        recommendations = await self._generate_recommendations(analysis)
        
        return {
            'analysis': analysis,
            'recommendations': recommendations,
            'risk_factors': self._identify_risks(analysis),
            'confidence': self._calculate_confidence(analysis)
        }
    
    def get_capabilities(self) -> List[str]:
        return ['pattern_analysis', 'risk_assessment', 'recommendations']

# 커널 사용 예시
async def main():
    kernel = AIServiceKernel()
    
    # 플러그인 등록
    kernel.register_plugin(SajuInterpretationPlugin())
    kernel.register_plugin(HealthAnalysisPlugin())
    
    # 사주 해석 요청
    saju_request = {
        'token': 'user_auth_token',
        'saju_data': {
            'heavenly_stems': ['갑', '을', '병', '정'],
            'earthly_branches': ['자', '축', '인', '묘']
        },
        'type': 'personality'
    }
    
    result = await kernel.process_request('saju_interpretation', saju_request)
    print(f"Saju interpretation: {result}")
```

### **6️⃣ Service Mesh Pattern (서비스 메시 패턴)**

```yaml
service_mesh_pattern:
  개념: "큐브간 통신을 별도 레이어로 분리"
  적용_시나리오: "마이크로서비스 간 통신"
  
  구조:
    [Cube A] ↔ [Proxy] ↔ [Service Mesh] ↔ [Proxy] ↔ [Cube B]
                            ↕
                      [Control Plane]
                      
  장점:
    - "통신 로직 분리"
    - "보안, 모니터링 중앙화"
    - "언어 독립적"
    
  단점:
    - "복잡한 설정"
    - "추가 네트워크 홉"
```

**실제 구현 예시: HEAL7 큐브간 통신 메시**

```go
// Go - 서비스 메시 프록시
package servicemesh

import (
    "context"
    "fmt"
    "net/http"
    "time"
)

type ServiceMeshProxy struct {
    serviceName     string
    serviceRegistry *ServiceRegistry
    circuitBreaker  *CircuitBreaker
    rateLimiter     *RateLimiter
    metrics         *MetricsCollector
    tracer          *DistributedTracer
}

func NewServiceMeshProxy(serviceName string) *ServiceMeshProxy {
    return &ServiceMeshProxy{
        serviceName:     serviceName,
        serviceRegistry: NewServiceRegistry(),
        circuitBreaker:  NewCircuitBreaker(),
        rateLimiter:     NewRateLimiter(1000), // 1000 req/sec
        metrics:         NewMetricsCollector(),
        tracer:          NewDistributedTracer(),
    }
}

func (p *ServiceMeshProxy) Forward(ctx context.Context, targetService string, req *http.Request) (*http.Response, error) {
    span := p.tracer.StartSpan(fmt.Sprintf("%s -> %s", p.serviceName, targetService))
    defer span.Finish()
    
    // 1. 요율 제한 확인
    if !p.rateLimiter.Allow() {
        p.metrics.RecordRateLimited(targetService)
        return nil, ErrRateLimited
    }
    
    // 2. 서비스 디스커버리
    endpoint, err := p.serviceRegistry.Discover(targetService)
    if err != nil {
        return nil, fmt.Errorf("service discovery failed: %w", err)
    }
    
    // 3. 서킷 브레이커 확인
    if !p.circuitBreaker.Allow(targetService) {
        p.metrics.RecordCircuitOpen(targetService)
        return nil, ErrCircuitOpen
    }
    
    // 4. 실제 요청 전송
    start := time.Now()
    resp, err := p.sendRequest(ctx, endpoint, req)
    duration := time.Since(start)
    
    // 5. 메트릭 기록
    p.metrics.RecordRequest(targetService, duration, err)
    
    // 6. 서킷 브레이커 상태 업데이트
    if err != nil {
        p.circuitBreaker.RecordFailure(targetService)
    } else {
        p.circuitBreaker.RecordSuccess(targetService)
    }
    
    return resp, err
}

// 서비스 레지스트리
type ServiceRegistry struct {
    services map[string][]ServiceEndpoint
    mu       sync.RWMutex
}

type ServiceEndpoint struct {
    Address     string
    Port        int
    Health      HealthStatus
    LoadFactor  float64
}

func (sr *ServiceRegistry) Register(serviceName string, endpoint ServiceEndpoint) {
    sr.mu.Lock()
    defer sr.mu.Unlock()
    
    if sr.services[serviceName] == nil {
        sr.services[serviceName] = []ServiceEndpoint{}
    }
    
    sr.services[serviceName] = append(sr.services[serviceName], endpoint)
}

func (sr *ServiceRegistry) Discover(serviceName string) (ServiceEndpoint, error) {
    sr.mu.RLock()
    defer sr.mu.RUnlock()
    
    endpoints := sr.services[serviceName]
    if len(endpoints) == 0 {
        return ServiceEndpoint{}, ErrServiceNotFound
    }
    
    // 로드 밸런싱 (가중 라운드 로빈)
    return sr.selectEndpoint(endpoints), nil
}

func (sr *ServiceRegistry) selectEndpoint(endpoints []ServiceEndpoint) ServiceEndpoint {
    healthyEndpoints := make([]ServiceEndpoint, 0)
    
    for _, ep := range endpoints {
        if ep.Health == HealthStatusHealthy {
            healthyEndpoints = append(healthyEndpoints, ep)
        }
    }
    
    if len(healthyEndpoints) == 0 {
        // 모든 엔드포인트가 불건전하면 가장 덜 나쁜 것 선택
        return endpoints[0]
    }
    
    // 로드 팩터가 가장 낮은 엔드포인트 선택
    best := healthyEndpoints[0]
    for _, ep := range healthyEndpoints[1:] {
        if ep.LoadFactor < best.LoadFactor {
            best = ep
        }
    }
    
    return best
}
```

### **7️⃣ CQRS Pattern (명령-조회 분리 패턴)**

```yaml
cqrs_pattern:
  개념: "명령(쓰기)과 조회(읽기) 큐브 분리"
  적용_시나리오: "읽기 쓰기 성능 최적화"
  
  구조:
    [Command Cubes] → [Write DB]
                            ↓
                     [Event Stream]
                            ↓
                      [Read DB] ← [Query Cubes]
                      
  장점:
    - "읽기/쓰기 독립 최적화"
    - "높은 확장성"
    - "복잡한 쿼리 최적화"
    
  단점:
    - "데이터 일관성 복잡"
    - "이벤트 sourcing 필요"
```

**실제 구현 예시: HEAL7 사용자 데이터 CQRS**

```python
# Python - Command Side (쓰기 큐브들)
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any
import asyncio
import json

@dataclass
class Command:
    user_id: str
    command_type: str
    data: dict
    timestamp: float
    correlation_id: str

@dataclass 
class Event:
    aggregate_id: str
    event_type: str
    data: dict
    timestamp: float
    version: int

class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> List[Event]:
        pass

class UserProfileCommandHandler(CommandHandler):
    def __init__(self, event_store):
        self.event_store = event_store
    
    async def handle(self, command: Command) -> List[Event]:
        if command.command_type == "update_profile":
            return await self._handle_update_profile(command)
        elif command.command_type == "calculate_saju":
            return await self._handle_calculate_saju(command)
        else:
            raise ValueError(f"Unknown command type: {command.command_type}")
    
    async def _handle_update_profile(self, command: Command) -> List[Event]:
        # 비즈니스 로직 실행
        user_id = command.user_id
        profile_data = command.data
        
        # 유효성 검증
        if not self._validate_profile_data(profile_data):
            raise ValidationError("Invalid profile data")
        
        # 이벤트 생성
        events = [
            Event(
                aggregate_id=user_id,
                event_type="UserProfileUpdated",
                data={
                    "old_data": await self._get_current_profile(user_id),
                    "new_data": profile_data,
                    "updated_fields": self._get_updated_fields(profile_data)
                },
                timestamp=command.timestamp,
                version=await self._get_next_version(user_id)
            )
        ]
        
        # 이벤트 저장
        await self.event_store.save_events(user_id, events)
        
        return events

class SajuCalculationCommandHandler(CommandHandler):
    def __init__(self, event_store, saju_calculator):
        self.event_store = event_store
        self.saju_calculator = saju_calculator
    
    async def handle(self, command: Command) -> List[Event]:
        user_id = command.user_id
        calculation_request = command.data
        
        # 사주 계산 실행
        result = await self.saju_calculator.calculate(
            birth_date=calculation_request['birth_date'],
            birth_time=calculation_request['birth_time'],
            location=calculation_request.get('location')
        )
        
        # 이벤트 생성
        events = [
            Event(
                aggregate_id=user_id,
                event_type="SajuCalculated",
                data={
                    "request": calculation_request,
                    "result": result,
                    "calculation_id": result['id']
                },
                timestamp=command.timestamp,
                version=await self._get_next_version(user_id)
            )
        ]
        
        # 사용 통계 이벤트도 생성
        events.append(Event(
            aggregate_id=user_id,
            event_type="ServiceUsed",
            data={
                "service_type": "saju_calculation",
                "usage_count": await self._get_usage_count(user_id) + 1
            },
            timestamp=command.timestamp,
            version=await self._get_next_version(user_id)
        ))
        
        await self.event_store.save_events(user_id, events)
        return events

# Query Side (읽기 큐브들)
class UserProfileQueryHandler:
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def get_user_profile(self, user_id: str) -> dict:
        """사용자 프로필 조회"""
        profile = await self.read_db.query(
            "SELECT * FROM user_profiles WHERE user_id = %s",
            [user_id]
        )
        return profile[0] if profile else None
    
    async def get_user_saju_history(self, user_id: str, limit: int = 10) -> List[dict]:
        """사용자 사주 계산 기록 조회"""
        history = await self.read_db.query(
            """
            SELECT calculation_id, birth_date, birth_time, 
                   calculated_at, result_summary
            FROM saju_calculations 
            WHERE user_id = %s 
            ORDER BY calculated_at DESC 
            LIMIT %s
            """,
            [user_id, limit]
        )
        return history
    
    async def get_popular_saju_types(self, limit: int = 10) -> List[dict]:
        """인기 사주 유형 조회"""
        popular = await self.read_db.query(
            """
            SELECT saju_type, COUNT(*) as count,
                   AVG(user_rating) as avg_rating
            FROM saju_calculations 
            WHERE calculated_at >= NOW() - INTERVAL '30 days'
            GROUP BY saju_type
            ORDER BY count DESC
            LIMIT %s
            """,
            [limit]
        )
        return popular

# Event Projector (이벤트를 읽기 모델로 투영)
class UserProfileProjector:
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle_event(self, event: Event):
        if event.event_type == "UserProfileUpdated":
            await self._project_profile_update(event)
        elif event.event_type == "SajuCalculated":
            await self._project_saju_calculation(event)
        elif event.event_type == "ServiceUsed":
            await self._project_service_usage(event)
    
    async def _project_profile_update(self, event: Event):
        user_id = event.aggregate_id
        new_data = event.data['new_data']
        
        # 사용자 프로필 테이블 업데이트
        await self.read_db.execute(
            """
            INSERT INTO user_profiles (user_id, name, birth_date, preferences, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                name = EXCLUDED.name,
                birth_date = EXCLUDED.birth_date,
                preferences = EXCLUDED.preferences,
                updated_at = EXCLUDED.updated_at
            """,
            [
                user_id,
                new_data.get('name'),
                new_data.get('birth_date'),
                json.dumps(new_data.get('preferences', {})),
                event.timestamp
            ]
        )
    
    async def _project_saju_calculation(self, event: Event):
        user_id = event.aggregate_id
        calculation_data = event.data
        
        # 사주 계산 기록 테이블에 추가
        await self.read_db.execute(
            """
            INSERT INTO saju_calculations 
            (user_id, calculation_id, birth_date, birth_time, 
             result_summary, full_result, calculated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            [
                user_id,
                calculation_data['result']['id'],
                calculation_data['request']['birth_date'],
                calculation_data['request']['birth_time'],
                calculation_data['result']['summary'],
                json.dumps(calculation_data['result']),
                event.timestamp
            ]
        )

# 전체 CQRS 시스템 통합
class CQRSSystem:
    def __init__(self):
        self.command_handlers = {}
        self.query_handlers = {}
        self.projectors = []
        self.event_bus = EventBus()
    
    def register_command_handler(self, command_type: str, handler: CommandHandler):
        self.command_handlers[command_type] = handler
    
    def register_query_handler(self, query_type: str, handler):
        self.query_handlers[query_type] = handler
    
    def register_projector(self, projector):
        self.projectors.append(projector)
    
    async def execute_command(self, command: Command) -> List[Event]:
        handler = self.command_handlers.get(command.command_type)
        if not handler:
            raise ValueError(f"No handler for command: {command.command_type}")
        
        events = await handler.handle(command)
        
        # 이벤트를 프로젝터들에게 전파
        for event in events:
            await self.event_bus.publish(event)
            for projector in self.projectors:
                await projector.handle_event(event)
        
        return events
    
    async def execute_query(self, query_type: str, **kwargs):
        handler = self.query_handlers.get(query_type)
        if not handler:
            raise ValueError(f"No handler for query: {query_type}")
        
        return await handler.handle_query(**kwargs)
```

### **8️⃣ Saga Pattern (사가 패턴)**

```yaml
saga_pattern:
  개념: "분산 트랜잭션을 여러 단계로 분해"
  적용_시나리오: "복잡한 비즈니스 프로세스"
  
  구조:
    [Step 1] → [Step 2] → [Step 3] → [Success]
        ↓         ↓         ↓
    [Compensate] [Compensate] [Compensate]
    
  장점:
    - "분산 트랜잭션 가능"
    - "부분 실패 처리"
    - "비즈니스 프로세스 명시적"
    
  단점:
    - "복잡한 보상 로직"
    - "일시적 불일치 허용"
```

**실제 구현 예시: HEAL7 결제 프로세스 사가**

```typescript
// TypeScript - 사가 패턴 구현
interface SagaStep {
    name: string;
    execute: (context: SagaContext) => Promise<any>;
    compensate: (context: SagaContext) => Promise<void>;
}

interface SagaContext {
    userId: string;
    orderId: string;
    paymentAmount: number;
    data: Record<string, any>;
    completedSteps: string[];
}

class SagaOrchestrator {
    private steps: SagaStep[] = [];
    
    addStep(step: SagaStep): void {
        this.steps.push(step);
    }
    
    async execute(context: SagaContext): Promise<boolean> {
        const executedSteps: string[] = [];
        
        try {
            // 순차적으로 단계 실행
            for (const step of this.steps) {
                console.log(`Executing step: ${step.name}`);
                
                const result = await step.execute(context);
                context.data[step.name] = result;
                executedSteps.push(step.name);
                context.completedSteps = [...executedSteps];
                
                console.log(`Step ${step.name} completed successfully`);
            }
            
            return true; // 모든 단계 성공
            
        } catch (error) {
            console.error(`Saga failed at step: ${error.step || 'unknown'}`);
            
            // 보상 트랜잭션 실행 (역순)
            await this.compensate(context, executedSteps);
            
            return false; // 사가 실패
        }
    }
    
    private async compensate(context: SagaContext, executedSteps: string[]): Promise<void> {
        console.log('Starting compensation process...');
        
        // 실행된 단계들을 역순으로 보상
        for (let i = executedSteps.length - 1; i >= 0; i--) {
            const stepName = executedSteps[i];
            const step = this.steps.find(s => s.name === stepName);
            
            if (step) {
                try {
                    console.log(`Compensating step: ${stepName}`);
                    await step.compensate(context);
                    console.log(`Step ${stepName} compensated successfully`);
                } catch (compensationError) {
                    console.error(`Failed to compensate step ${stepName}:`, compensationError);
                    // 보상 실패는 로그만 남기고 계속 진행
                }
            }
        }
        
        console.log('Compensation process completed');
    }
}

// 실제 결제 프로세스 사가 단계들
class ReservePremiumServiceStep implements SagaStep {
    name = 'reservePremiumService';
    
    constructor(private serviceManager: ServiceManager) {}
    
    async execute(context: SagaContext): Promise<any> {
        const reservation = await this.serviceManager.reservePremiumAccess(
            context.userId,
            context.data.serviceType,
            context.data.duration
        );
        
        if (!reservation.success) {
            throw new Error('Failed to reserve premium service');
        }
        
        return {
            reservationId: reservation.id,
            expiresAt: reservation.expiresAt
        };
    }
    
    async compensate(context: SagaContext): Promise<void> {
        const reservationId = context.data[this.name]?.reservationId;
        if (reservationId) {
            await this.serviceManager.cancelReservation(reservationId);
        }
    }
}

class ProcessPaymentStep implements SagaStep {
    name = 'processPayment';
    
    constructor(private paymentGateway: PaymentGateway) {}
    
    async execute(context: SagaContext): Promise<any> {
        const payment = await this.paymentGateway.processPayment({
            userId: context.userId,
            amount: context.paymentAmount,
            currency: 'KRW',
            orderId: context.orderId,
            paymentMethod: context.data.paymentMethod
        });
        
        if (!payment.success) {
            throw new Error(`Payment failed: ${payment.errorMessage}`);
        }
        
        return {
            transactionId: payment.transactionId,
            processedAt: payment.processedAt,
            gatewayResponse: payment.gatewayResponse
        };
    }
    
    async compensate(context: SagaContext): Promise<void> {
        const transactionId = context.data[this.name]?.transactionId;
        if (transactionId) {
            await this.paymentGateway.refundPayment(transactionId, context.paymentAmount);
        }
    }
}

class ActivatePremiumServiceStep implements SagaStep {
    name = 'activatePremiumService';
    
    constructor(private userService: UserService, private notificationService: NotificationService) {}
    
    async execute(context: SagaContext): Promise<any> {
        // 사용자 계정을 프리미엄으로 업그레이드
        const activation = await this.userService.activatePremiumSubscription(
            context.userId,
            {
                serviceType: context.data.serviceType,
                duration: context.data.duration,
                orderId: context.orderId,
                paymentTransactionId: context.data.processPayment.transactionId
            }
        );
        
        // 활성화 알림 발송
        await this.notificationService.sendPremiumActivationNotification(
            context.userId,
            activation.details
        );
        
        return {
            subscriptionId: activation.subscriptionId,
            activatedAt: activation.activatedAt,
            expiresAt: activation.expiresAt
        };
    }
    
    async compensate(context: SagaContext): Promise<void> {
        const subscriptionId = context.data[this.name]?.subscriptionId;
        if (subscriptionId) {
            await this.userService.deactivatePremiumSubscription(subscriptionId);
            await this.notificationService.sendSubscriptionCancelledNotification(context.userId);
        }
    }
}

class UpdateAnalyticsStep implements SagaStep {
    name = 'updateAnalytics';
    
    constructor(private analyticsService: AnalyticsService) {}
    
    async execute(context: SagaContext): Promise<any> {
        // 결제 및 구독 분석 데이터 업데이트
        await this.analyticsService.recordPremiumSubscription({
            userId: context.userId,
            serviceType: context.data.serviceType,
            paymentAmount: context.paymentAmount,
            subscriptionDuration: context.data.duration,
            timestamp: new Date()
        });
        
        // 사용자 행동 분석 업데이트
        await this.analyticsService.updateUserSegment(context.userId, 'premium_user');
        
        return {
            analyticsRecorded: true,
            segmentUpdated: true
        };
    }
    
    async compensate(context: SagaContext): Promise<void> {
        // 분석 데이터 롤백
        await this.analyticsService.rollbackPremiumSubscriptionRecord(
            context.userId,
            context.orderId
        );
        
        await this.analyticsService.updateUserSegment(context.userId, 'free_user');
    }
}

// 사가 사용 예시
export class PremiumSubscriptionSaga {
    private saga: SagaOrchestrator;
    
    constructor(
        serviceManager: ServiceManager,
        paymentGateway: PaymentGateway,
        userService: UserService,
        notificationService: NotificationService,
        analyticsService: AnalyticsService
    ) {
        this.saga = new SagaOrchestrator();
        
        // 사가 단계들 등록
        this.saga.addStep(new ReservePremiumServiceStep(serviceManager));
        this.saga.addStep(new ProcessPaymentStep(paymentGateway));
        this.saga.addStep(new ActivatePremiumServiceStep(userService, notificationService));
        this.saga.addStep(new UpdateAnalyticsStep(analyticsService));
    }
    
    async subscribeToPremium(subscriptionRequest: PremiumSubscriptionRequest): Promise<boolean> {
        const context: SagaContext = {
            userId: subscriptionRequest.userId,
            orderId: subscriptionRequest.orderId,
            paymentAmount: subscriptionRequest.amount,
            data: {
                serviceType: subscriptionRequest.serviceType,
                duration: subscriptionRequest.duration,
                paymentMethod: subscriptionRequest.paymentMethod
            },
            completedSteps: []
        };
        
        return await this.saga.execute(context);
    }
}

// 사용 예시
async function handlePremiumSubscription(request: PremiumSubscriptionRequest) {
    const saga = new PremiumSubscriptionSaga(
        serviceManager,
        paymentGateway,
        userService,
        notificationService,
        analyticsService
    );
    
    const success = await saga.subscribeToPremium(request);
    
    if (success) {
        console.log('Premium subscription completed successfully');
        return { success: true, message: 'Premium subscription activated' };
    } else {
        console.log('Premium subscription failed, all changes have been compensated');
        return { success: false, message: 'Subscription failed, please try again' };
    }
}
```

## 🎯 **조립 패턴 선택 가이드**

### **📊 패턴별 적용 시나리오**

```yaml
pattern_selection_guide:
  Pipeline_Pattern:
    적합한_경우:
      - "데이터 변환이 주목적"
      - "단계별 처리가 명확"
      - "디버깅이 중요"
    예시: "사주 계산, 이미지 처리, ETL"
    
  Hub_Pattern:
    적합한_경우:
      - "중앙집중식 관리 필요"
      - "API Gateway 역할"
      - "단순한 라우팅"
    예시: "API 게이트웨이, 메시지 라우터"
    
  Event_Driven_Pattern:
    적합한_경우:
      - "실시간 반응성 중요"
      - "확장성이 핵심"
      - "비동기 처리"
    예시: "실시간 알림, 사용자 행동 추적"
    
  Layered_Pattern:
    적합한_경우:
      - "전통적인 웹 애플리케이션"
      - "명확한 계층 구조"
      - "팀이 익숙한 구조"
    예시: "일반적인 CRUD 애플리케이션"
    
  Micro_kernel_Pattern:
    적합한_경우:
      - "플러그인 시스템"
      - "확장 가능한 플랫폼"
      - "서드파티 통합"
    예시: "AI 서비스 플랫폼, CMS"
    
  Service_Mesh_Pattern:
    적합한_경우:
      - "복잡한 마이크로서비스"
      - "통신 보안 중요"
      - "관찰성 필요"
    예시: "대규모 분산 시스템"
    
  CQRS_Pattern:
    적합한_경우:
      - "읽기/쓰기 성능 차이"
      - "복잡한 쿼리"
      - "이벤트 기반 아키텍처"
    예시: "분석 시스템, 이벤트 소싱"
    
  Saga_Pattern:
    적합한_경우:
      - "분산 트랜잭션"
      - "복잡한 비즈니스 프로세스"
      - "부분 실패 허용"
    예시: "결제 시스템, 주문 처리"
```

### **🎪 HEAL7 서비스별 권장 패턴**

```yaml
heal7_service_patterns:
  사주_계산_서비스:
    주_패턴: "Pipeline Pattern"
    이유: "입력 → 검증 → 계산 → 해석 → 출력의 명확한 흐름"
    보조_패턴: "Cache Layer, Circuit Breaker"
    
  사용자_관리_서비스:
    주_패턴: "Layered Pattern + CQRS"
    이유: "전통적 CRUD + 복잡한 분석 쿼리"
    보조_패턴: "Event Driven (사용자 행동 추적)"
    
  AI_서비스_플랫폼:
    주_패턴: "Micro-kernel Pattern"
    이유: "다양한 AI 모델을 플러그인으로 관리"
    보조_패턴: "Pipeline (AI 추론 과정)"
    
  결제_시스템:
    주_패턴: "Saga Pattern"
    이유: "복잡한 결제 프로세스와 보상 트랜잭션"
    보조_패턴: "Event Driven (결제 상태 알림)"
    
  실시간_채팅:
    주_패턴: "Event Driven Pattern"
    이유: "실시간 메시지 전파와 확장성"
    보조_패턴: "Hub Pattern (메시지 라우팅)"
    
  분석_대시보드:
    주_패턴: "CQRS Pattern"
    이유: "복잡한 분석 쿼리와 실시간 데이터"
    보조_패턴: "Event Driven (실시간 업데이트)"
```

## 🧪 **패턴 조합 전략**

### **🔗 하이브리드 패턴 조합**

```yaml
hybrid_combinations:
  Pipeline_+_Event_Driven:
    구조: "파이프라인 각 단계에서 이벤트 발생"
    장점: "처리 추적 + 실시간 알림"
    예시: "사주 계산 진행상황 실시간 알림"
    
  Hub_+_Circuit_Breaker:
    구조: "허브에 서킷 브레이커 통합"
    장점: "중앙 관리 + 장애 격리"
    예시: "API Gateway with Resilience"
    
  CQRS_+_Event_Sourcing:
    구조: "명령은 이벤트로, 조회는 투영으로"
    장점: "완전한 감사 기록 + 성능"
    예시: "사용자 행동 분석 시스템"
    
  Saga_+_Event_Driven:
    구조: "사가 각 단계가 이벤트 기반"
    장점: "분산 트랜잭션 + 실시간 추적"
    예시: "복잡한 주문 처리 시스템"
```

### **📈 점진적 패턴 적용 전략**

```yaml
progressive_adoption:
  Phase_1_단순_시작:
    패턴: "Layered Pattern"
    기간: "3개월"
    목표: "기본 기능 구현 및 안정화"
    
  Phase_2_성능_최적화:
    패턴: "Pipeline Pattern 추가"
    기간: "2개월"
    목표: "핵심 프로세스 성능 향상"
    
  Phase_3_확장성_확보:
    패턴: "Event Driven Pattern 추가"
    기간: "3개월"
    목표: "실시간 기능 및 확장성"
    
  Phase_4_고도화:
    패턴: "CQRS, Saga Pattern 추가"
    기간: "4개월"
    목표: "복잡한 비즈니스 로직 최적화"
    
  Phase_5_플랫폼화:
    패턴: "Micro-kernel, Service Mesh 추가"
    기간: "6개월"
    목표: "플랫폼으로 진화"
```

## 💡 **조립 베스트 프랙티스**

### **✅ 성공하는 조립 원칙**

```yaml
success_principles:
  Start_Simple:
    원칙: "단순하게 시작해서 점진적 복잡화"
    이유: "조기 최적화는 복잡성만 증가"
    실행: "먼저 Layered Pattern으로 시작"
    
  Measure_First:
    원칙: "측정 후 최적화"
    이유: "추측이 아닌 데이터 기반 결정"
    실행: "성능 병목 지점 파악 후 패턴 적용"
    
  Decouple_Gradually:
    원칙: "점진적 분리"
    이유: "한번에 모든 것을 분리하면 실패"
    실행: "가장 독립적인 부분부터 큐브화"
    
  Test_Boundaries:
    원칙: "경계면 집중 테스트"
    이유: "큐브간 통신이 가장 취약"
    실행: "인터페이스 계약 테스트 우선"
    
  Monitor_Everything:
    원칙: "모든 것을 모니터링"
    이유: "분산 시스템은 가시성이 생명"
    실행: "큐브별 메트릭, 분산 추적"
```

### **🚫 피해야 할 안티패턴**

```yaml
anti_patterns:
  God_Cube:
    문제: "모든 기능을 하나의 큐브에"
    해결: "Single Responsibility Principle 적용"
    
  Chatty_Interface:
    문제: "큐브간 과도한 통신"
    해결: "배치 처리, 메시지 집계"
    
  Distributed_Monolith:
    문제: "분산됐지만 강하게 결합"
    해결: "진정한 독립성 확보"
    
  Data_Inconsistency:
    문제: "큐브간 데이터 불일치"
    해결: "이벤트 소싱, CQRS 패턴"
    
  Premature_Optimization:
    문제: "성능 문제 없는데 복잡한 패턴"
    해결: "문제 발생 후 최적화"
```

---

**🧩 큐브 조립 패턴**은 레고 블록의 무한한 가능성을 소프트웨어 아키텍처로 구현하는 핵심 기법입니다.

*🎯 올바른 패턴 선택이 성공의 90%를 결정합니다.*  
*🔧 단순함에서 시작해서 필요에 따라 진화시키세요.*  
*📊 항상 측정하고, 데이터에 기반해서 의사결정하세요.*