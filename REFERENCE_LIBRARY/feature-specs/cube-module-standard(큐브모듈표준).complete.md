# 🧩 큐브모듈 표준 명세서

> **핵심 철학**: 책처럼 자체 문서화된 완전 자율 모듈  
> **조립 원칙**: 레고블럭처럼 간단한 조합으로 복잡한 시스템 구성  
> **표준 버전**: v1.0.0  
> **최종 업데이트**: 2025-08-20 06:15 UTC

## 📚 **큐브모듈 핵심 개념**

### **🧠 레고블럭 철학**

큐브모듈은 단순한 코드 패키지가 아닌, **완전한 기능을 담은 자율적 단위**입니다:

```
📖 책 (Book) = 🧩 큐브모듈 (Cube Module)
├── 📋 차례 (INDEX.md)          = 모든 구성요소 목록
├── 📖 머릿말 (README.md)        = 목적, 기능, 사용법
├── 📄 본문 (Core Files)        = 실제 구현 코드
├── 📚 부록 (Examples)          = 사용 예제
├── 🧪 연습문제 (Tests)          = 검증 및 테스트
└── 📝 맺음말 (CHANGELOG.md)     = 버전 변경 이력
```

### **🎯 큐브모듈 특징**

1. **완전 자율성**: 외부 설명서 없이 독립적으로 이해 가능
2. **즉시 사용성**: 복사-붙여넣기로 바로 동작
3. **언어 통합**: 하나의 모듈에 모든 언어 계층 포함
4. **목적 중심**: 기술이 아닌 비즈니스 기능 중심

## 🏗️ **표준 디렉토리 구조**

### **📁 필수 구조**

```
cube-module-name/
├── 📋 INDEX.md                 # 📚 차례 (필수)
├── 📖 README.md                # 📖 머릿말 (필수)
├── 🦀 core.cube.rs             # 🦀 Rust 핵심 로직 (선택)
├── 🐹 service.cube.go          # 🐹 Go 서비스 레이어 (선택)  
├── 🐍 ai.cube.py               # 🐍 Python AI 처리 (선택)
├── ⚡ ui.cube.ts               # ⚡ TypeScript UI (선택)
├── 💾 schema.cube.sql          # 💾 데이터베이스 스키마 (선택)
├── 🔧 config.cube.yaml         # 🔧 설정 파일 (선택)
├── 📚 examples/                # 📚 사용 예제 (권장)
│   ├── basic.example.ts
│   ├── advanced.example.go
│   └── integration.example.py
├── 🧪 tests/                   # 🧪 테스트 suite (권장)
│   ├── unit.test.rs
│   ├── integration.test.go
│   └── e2e.test.ts
├── 📊 docs/                    # 📊 상세 문서 (선택)
│   ├── api-reference.md
│   └── architecture.md
└── 📝 CHANGELOG.md             # 📝 변경 이력 (필수)
```

### **📝 파일 명명 규칙**

```yaml
패턴: "{기능}.cube.{확장자}"

예시:
  - auth.cube.rs         # 인증 기능의 Rust 구현
  - payment.cube.go      # 결제 기능의 Go 구현
  - analysis.cube.py     # 분석 기능의 Python 구현
  - dashboard.cube.ts    # 대시보드 UI의 TypeScript 구현
  - users.cube.sql       # 사용자 관련 DB 스키마

특수파일:
  - INDEX.md            # 차례 (모듈 전체 구성 설명)
  - README.md           # 머릿말 (모듈 소개 및 사용법)
  - CHANGELOG.md        # 맺음말 (변경 이력)
```

## 📖 **문서화 표준**

### **📋 INDEX.md (차례) 템플릿**

```markdown
# 📋 [모듈명] 큐브모듈 차례

> **모듈 개요**: [한 줄 설명]  
> **버전**: v[x.y.z]  
> **카테고리**: [feature|core|ui|data|utility]

## 📚 구성 요소

### 🎯 핵심 파일
| 파일명 | 언어 | 설명 | 크기 | 상태 |
|--------|------|------|------|------|
| core.cube.rs | Rust | 핵심 로직 | 245줄 | ✅ |
| service.cube.go | Go | 서비스 레이어 | 180줄 | ✅ |
| ai.cube.py | Python | AI 처리 | 156줄 | ✅ |
| ui.cube.ts | TypeScript | UI 컴포넌트 | 298줄 | ✅ |

### 📊 지원 파일
| 파일명 | 목적 | 설명 |
|--------|------|------|
| schema.cube.sql | 데이터 | 테이블 및 인덱스 정의 |
| config.cube.yaml | 설정 | 환경별 설정값 |

### 📚 예제 및 테스트
- `examples/` - 3개 사용 예제
- `tests/` - 단위/통합/E2E 테스트
- `docs/` - API 레퍼런스 및 아키텍처

## 🔗 의존성
- **필수**: [필수 의존성 목록]
- **선택**: [선택적 의존성 목록]
- **충돌**: [알려진 충돌 사항]

## ⚡ 빠른 시작
1. [1단계 설명]
2. [2단계 설명]  
3. [3단계 설명]

## 📞 연락처
- **개발자**: [개발자명]
- **이슈 트래킹**: [GitHub URL]
- **문서 위키**: [Wiki URL]
```

### **📖 README.md (머릿말) 템플릿**

```markdown
# 📖 [모듈명] 큐브모듈

> **🎯 목적**: [이 모듈이 해결하는 문제]  
> **💡 핵심 가치**: [사용자에게 제공하는 가치]  
> **🚀 주요 기능**: [핵심 기능 3-5개]

## 🤔 **왜 이 모듈을 사용해야 하나요?**

### 😰 기존 방식의 문제점
- [문제점 1]: [구체적 설명]
- [문제점 2]: [구체적 설명]
- [문제점 3]: [구체적 설명]

### ✨ 이 모듈의 해결책
- [해결책 1]: [어떻게 해결하는지]
- [해결책 2]: [어떻게 해결하는지]
- [해결책 3]: [어떻게 해결하는지]

## 🚀 **빠른 시작 (30초 설정)**

### 1️⃣ 설치
```bash
# npm 방식
npm install @heal7/[모듈명]-cube

# 직접 복사 방식
cp -r cube-modules/[모듈명] ./src/modules/
```

### 2️⃣ 기본 사용법
```typescript
import { [ModuleName]Cube } from '@heal7/[모듈명]-cube';

// 즉시 사용 가능한 간단한 예제
const cube = new [ModuleName]Cube({
    // 최소한의 설정
});

const result = await cube.execute();
console.log(result); // 예상 결과 출력
```

### 3️⃣ 실제 결과
```
✅ [예상 결과 1]
✅ [예상 결과 2]
✅ [예상 결과 3]
```

## 🧩 **모듈 구성**

### 🎭 다언어 통합 구조
```
[모듈명] 큐브 = 완전한 기능 단위
├── 🦀 Rust: [역할 설명]
├── 🐹 Go: [역할 설명]
├── 🐍 Python: [역할 설명]
├── ⚡ TypeScript: [역할 설명]
└── 💾 Database: [역할 설명]
```

### 🔌 표준 인터페이스
```typescript
interface [ModuleName]Cube {
    // 생명주기
    initialize(config: CubeConfig): Promise<void>;
    start(): Promise<void>;
    stop(): Promise<void>;
    
    // 핵심 기능
    [mainFunction](input: InputType): Promise<OutputType>;
    
    // 상태 관리
    getHealth(): HealthStatus;
    getMetrics(): ModuleMetrics;
}
```

## 📚 **사용 예제**

### 🎯 기본 사용법
```typescript
// [구체적이고 실용적인 예제]
```

### 🔧 고급 설정
```typescript
// [고급 기능 사용 예제]
```

### 🏗️ 다른 모듈과 조합
```typescript
// [다른 큐브모듈과 조합 사용 예제]
```

## ⚙️ **설정 옵션**

| 옵션명 | 타입 | 기본값 | 설명 |
|--------|------|--------|------|
| [option1] | string | "default" | [설명] |
| [option2] | number | 100 | [설명] |
| [option3] | boolean | true | [설명] |

## 🧪 **테스트 실행**

```bash
# 모든 테스트 실행
npm test

# 언어별 테스트
cargo test          # Rust 테스트
go test ./...       # Go 테스트  
pytest              # Python 테스트
npm run test:ts     # TypeScript 테스트
```

## 🔧 **문제 해결**

### 자주 묻는 질문

**Q: [일반적인 질문]**  
A: [명확한 답변]

**Q: [기술적인 질문]**  
A: [상세한 해결책]

### 알려진 이슈
- **[이슈 제목]**: [해결 방법]
- **[이슈 제목]**: [해결 방법]

## 📊 **성능 정보**

| 지표 | 값 | 비고 |
|------|----|----- |
| 초기화 시간 | [X]ms | 첫 실행 시 |
| 평균 응답시간 | [X]ms | 일반적 요청 |
| 메모리 사용량 | [X]MB | 안정 상태 |
| 동시 처리 수 | [X]개 | 최대 동시 요청 |

## 🔗 **관련 모듈**

- **[관련모듈1]**: [관계 설명]
- **[관련모듈2]**: [관계 설명]
- **[관련모듈3]**: [관계 설명]

## 🤝 **기여하기**

1. 이슈 리포팅: [GitHub Issues URL]
2. 기능 제안: [Feature Request Process]
3. 코드 기여: [Contribution Guidelines]

## 📜 **라이선스**

[라이선스 정보]

---

*🧩 이 모듈은 HEAL7 큐브모듈러 아키텍처 표준을 준수합니다.*  
*📚 더 많은 정보: [Documentation Portal URL]*
```

### **📝 CHANGELOG.md (맺음말) 템플릿**

```markdown
# 📝 [모듈명] 변경 이력

모든 중요한 변경사항이 이 파일에 기록됩니다.

[Semantic Versioning](https://semver.org/lang/ko/) 형식을 따릅니다.

## [Unreleased]

### Added
- [추가된 기능]

### Changed  
- [변경된 기능]

### Deprecated
- [곧 제거될 기능]

### Removed
- [제거된 기능]

### Fixed
- [수정된 버그]

### Security
- [보안 관련 변경]

## [1.0.0] - 2025-08-20

### Added
- 초기 큐브모듈 릴리스
- [핵심 기능 1] 구현
- [핵심 기능 2] 구현
- [핵심 기능 3] 구현

### Documentation
- README.md 초기 작성
- API 레퍼런스 문서 추가
- 사용 예제 5개 추가

### Tests
- 단위 테스트 커버리지 95% 달성
- 통합 테스트 구현
- E2E 테스트 자동화

---

*변경 이력 형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 기반으로 합니다.*
```

## 🔌 **표준 인터페이스 정의**

### **🧩 기본 큐브모듈 인터페이스**

```typescript
// 모든 큐브모듈이 구현해야 하는 기본 인터페이스
interface CubeModule {
    // 메타데이터
    readonly name: string;
    readonly version: string;
    readonly category: CubeCategory;
    readonly dependencies: readonly string[];
    readonly capabilities: readonly string[];
    
    // 생명주기 관리
    initialize(config: CubeConfig): Promise<CubeInitResult>;
    start(): Promise<void>;
    stop(): Promise<void>;
    destroy(): Promise<void>;
    
    // 상태 관리
    getHealth(): Promise<CubeHealthStatus>;
    getMetrics(): Promise<CubeMetrics>;
    getInfo(): CubeInfo;
    
    // 핵심 기능
    process(request: CubeRequest): Promise<CubeResponse>;
    validate(input: unknown): Promise<CubeValidationResult>;
    
    // 이벤트 처리
    on(event: CubeEvent, handler: CubeEventHandler): void;
    off(event: CubeEvent, handler: CubeEventHandler): void;
    emit(event: CubeEvent, data: unknown): void;
    
    // 로깅 및 모니터링
    log(level: LogLevel, message: string, context?: object): void;
    trace(operationId: string, data: object): void;
}

// 큐브모듈 카테고리
type CubeCategory = 
    | 'feature'    // 비즈니스 기능
    | 'core'       // 핵심 로직
    | 'ui'         // 사용자 인터페이스
    | 'data'       // 데이터 처리
    | 'utility'    // 유틸리티
    | 'connector'; // 외부 연동

// 설정 인터페이스
interface CubeConfig {
    environment: 'development' | 'staging' | 'production';
    features: Record<string, boolean>;
    settings: Record<string, unknown>;
    resources: CubeResources;
}

// 리소스 정의
interface CubeResources {
    memory: {
        max: number;     // 최대 메모리 (MB)
        warning: number; // 경고 임계치 (MB)
    };
    cpu: {
        max: number;     // 최대 CPU 사용률 (%)
        cores: number;   // 사용 가능 코어 수
    };
    network: {
        maxConnections: number;
        timeoutMs: number;
    };
}
```

### **🦀 Rust 모듈 표준**

```rust
// Rust 큐브모듈 표준 트레이트
use async_trait::async_trait;
use serde::{Deserialize, Serialize};

#[async_trait]
pub trait RustCubeModule: Send + Sync {
    type Config: for<'de> Deserialize<'de> + Send + Sync;
    type Input: for<'de> Deserialize<'de> + Send + Sync;
    type Output: Serialize + Send + Sync;
    type Error: std::error::Error + Send + Sync;

    // 모듈 메타데이터
    fn name(&self) -> &'static str;
    fn version(&self) -> &'static str;
    fn capabilities(&self) -> Vec<&'static str>;

    // 생명주기
    async fn initialize(&mut self, config: Self::Config) -> Result<(), Self::Error>;
    async fn shutdown(&mut self) -> Result<(), Self::Error>;

    // 핵심 처리
    async fn process(&self, input: Self::Input) -> Result<Self::Output, Self::Error>;
    
    // 상태 확인
    fn health_check(&self) -> HealthStatus;
    fn get_metrics(&self) -> ModuleMetrics;
}

// 표준 에러 타입
#[derive(Debug, thiserror::Error)]
pub enum CubeError {
    #[error("Configuration error: {0}")]
    Config(String),
    
    #[error("Processing error: {0}")]
    Processing(String),
    
    #[error("Resource exhausted: {0}")]
    ResourceExhausted(String),
    
    #[error("External dependency error: {0}")]
    ExternalDependency(String),
}

// 헬스 상태
#[derive(Debug, Serialize, Deserialize)]
pub struct HealthStatus {
    pub status: HealthLevel,
    pub checks: Vec<HealthCheck>,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Serialize, Deserialize)]
pub enum HealthLevel {
    Healthy,
    Warning,
    Critical,
    Unknown,
}

// 메트릭스
#[derive(Debug, Serialize, Deserialize)]
pub struct ModuleMetrics {
    pub requests_total: u64,
    pub requests_per_second: f64,
    pub average_response_time_ms: f64,
    pub error_rate: f64,
    pub memory_usage_mb: f64,
    pub cpu_usage_percent: f64,
}
```

### **🐹 Go 모듈 표준**

```go
// Go 큐브모듈 표준 인터페이스
package cube

import (
    "context"
    "time"
)

// CubeModule 인터페이스
type CubeModule interface {
    // 메타데이터
    Name() string
    Version() string
    Category() CubeCategory
    Dependencies() []string
    
    // 생명주기
    Initialize(ctx context.Context, config CubeConfig) error
    Start(ctx context.Context) error
    Stop(ctx context.Context) error
    
    // 핵심 기능
    Process(ctx context.Context, req CubeRequest) (CubeResponse, error)
    Validate(input interface{}) error
    
    // 상태 관리
    Health() HealthStatus
    Metrics() Metrics
    
    // 이벤트
    On(event string, handler EventHandler)
    Emit(event string, data interface{})
}

// 서비스 레이어 인터페이스
type ServiceLayer interface {
    CubeModule
    
    // 서비스 특화 기능
    RegisterRoute(method, path string, handler HandlerFunc)
    Middleware(middleware MiddlewareFunc)
    LoadBalance(strategy LoadBalanceStrategy)
    RateLimit(limit RateLimit)
}

// 설정 구조체
type CubeConfig struct {
    Environment string                 `yaml:"environment"`
    Features    map[string]bool       `yaml:"features"`
    Settings    map[string]interface{} `yaml:"settings"`
    Resources   ResourceConfig        `yaml:"resources"`
}

type ResourceConfig struct {
    Memory struct {
        MaxMB     int `yaml:"max_mb"`
        WarningMB int `yaml:"warning_mb"`
    } `yaml:"memory"`
    
    CPU struct {
        MaxPercent int `yaml:"max_percent"`
        Cores      int `yaml:"cores"`
    } `yaml:"cpu"`
    
    Network struct {
        MaxConnections int           `yaml:"max_connections"`
        Timeout        time.Duration `yaml:"timeout"`
    } `yaml:"network"`
}

// 요청/응답 구조체
type CubeRequest struct {
    ID        string                 `json:"id"`
    Method    string                 `json:"method"`
    Path      string                 `json:"path"`
    Headers   map[string]string      `json:"headers"`
    Body      interface{}            `json:"body"`
    Context   map[string]interface{} `json:"context"`
    Timestamp time.Time              `json:"timestamp"`
}

type CubeResponse struct {
    ID          string                 `json:"id"`
    Status      int                    `json:"status"`
    Headers     map[string]string      `json:"headers"`
    Body        interface{}            `json:"body"`
    Metadata    map[string]interface{} `json:"metadata"`
    ProcessTime time.Duration          `json:"process_time"`
    Timestamp   time.Time              `json:"timestamp"`
}
```

### **🐍 Python 모듈 표준**

```python
# Python 큐브모듈 표준 인터페이스
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
import asyncio
import time

# 제네릭 타입
TConfig = TypeVar('TConfig')
TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')

class CubeCategory(Enum):
    FEATURE = "feature"
    CORE = "core"
    UI = "ui"
    DATA = "data" 
    UTILITY = "utility"
    CONNECTOR = "connector"

@dataclass
class CubeInfo:
    name: str
    version: str
    category: CubeCategory
    dependencies: List[str]
    capabilities: List[str]
    description: str

class CubeModule(ABC, Generic[TConfig, TInput, TOutput]):
    """모든 Python 큐브모듈의 기본 클래스"""
    
    def __init__(self):
        self._initialized = False
        self._running = False
        self._config: Optional[TConfig] = None
        
    @property
    @abstractmethod
    def info(self) -> CubeInfo:
        """모듈 정보 반환"""
        pass
    
    @abstractmethod
    async def initialize(self, config: TConfig) -> None:
        """모듈 초기화"""
        pass
    
    @abstractmethod
    async def start(self) -> None:
        """모듈 시작"""
        pass
    
    @abstractmethod  
    async def stop(self) -> None:
        """모듈 중지"""
        pass
    
    @abstractmethod
    async def process(self, input_data: TInput) -> TOutput:
        """핵심 처리 로직"""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """헬스 체크"""
        return {
            "status": "healthy" if self._running else "stopped",
            "initialized": self._initialized,
            "running": self._running,
            "timestamp": time.time()
        }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """메트릭 수집"""
        return {
            "requests_total": getattr(self, '_requests_total', 0),
            "average_response_time": getattr(self, '_avg_response_time', 0),
            "error_rate": getattr(self, '_error_rate', 0),
            "memory_usage_mb": self._get_memory_usage(),
        }
    
    def _get_memory_usage(self) -> float:
        """메모리 사용량 조회"""
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

# AI 특화 큐브모듈
class AICubeModule(CubeModule[TConfig, TInput, TOutput]):
    """AI 기능이 포함된 큐브모듈"""
    
    def __init__(self):
        super().__init__()
        self._model_cache: Dict[str, Any] = {}
        
    @abstractmethod
    async def load_models(self) -> None:
        """AI 모델 로딩"""
        pass
    
    @abstractmethod
    async def predict(self, input_data: TInput) -> TOutput:
        """AI 예측 수행"""
        pass
    
    async def warm_up_models(self) -> None:
        """모델 워밍업"""
        # 더미 데이터로 모델 워밍업
        pass

# 데이터 처리 특화 큐브모듈  
class DataCubeModule(CubeModule[TConfig, TInput, TOutput]):
    """데이터 처리 특화 큐브모듈"""
    
    @abstractmethod
    async def validate_data(self, data: Any) -> bool:
        """데이터 유효성 검증"""
        pass
    
    @abstractmethod
    async def transform_data(self, data: TInput) -> TOutput:
        """데이터 변환"""
        pass
    
    @abstractmethod
    async def store_data(self, data: TOutput) -> str:
        """데이터 저장"""
        pass
```

### **⚡ TypeScript 모듈 표준**

```typescript
// TypeScript 큐브모듈 표준 인터페이스

// 기본 타입 정의
export type CubeCategory = 'feature' | 'core' | 'ui' | 'data' | 'utility' | 'connector';

export interface CubeInfo {
    readonly name: string;
    readonly version: string;
    readonly category: CubeCategory;
    readonly dependencies: readonly string[];
    readonly capabilities: readonly string[];
    readonly description: string;
}

export interface CubeConfig {
    environment: 'development' | 'staging' | 'production';
    features: Record<string, boolean>;
    settings: Record<string, unknown>;
    resources: {
        memory: { maxMB: number; warningMB: number };
        cpu: { maxPercent: number; cores: number };
        network: { maxConnections: number; timeoutMs: number };
    };
}

// 기본 큐브모듈 인터페이스
export interface CubeModule<TConfig = CubeConfig, TInput = unknown, TOutput = unknown> {
    readonly info: CubeInfo;
    
    // 생명주기
    initialize(config: TConfig): Promise<void>;
    start(): Promise<void>;
    stop(): Promise<void>;
    destroy(): Promise<void>;
    
    // 핵심 기능
    process(input: TInput): Promise<TOutput>;
    validate(input: unknown): Promise<boolean>;
    
    // 상태 관리
    getHealth(): Promise<HealthStatus>;
    getMetrics(): Promise<CubeMetrics>;
    
    // 이벤트
    on(event: string, handler: EventHandler): void;
    off(event: string, handler: EventHandler): void;
    emit(event: string, data: unknown): void;
}

// UI 특화 큐브모듈
export interface UICubeModule<TProps = unknown> extends CubeModule {
    // 렌더링
    render(container: HTMLElement, props: TProps): Promise<void>;
    update(props: Partial<TProps>): Promise<void>;
    unmount(): Promise<void>;
    
    // 상태 관리
    getState(): unknown;
    setState(state: unknown): void;
    
    // 이벤트 처리
    handleEvent(event: Event): void;
    bindEvents(): void;
    unbindEvents(): void;
}

// 추상 기본 클래스
export abstract class BaseCubeModule<TConfig = CubeConfig, TInput = unknown, TOutput = unknown> 
    implements CubeModule<TConfig, TInput, TOutput> {
    
    protected _initialized = false;
    protected _running = false;
    protected _config?: TConfig;
    protected _eventHandlers = new Map<string, EventHandler[]>();
    
    abstract readonly info: CubeInfo;
    
    async initialize(config: TConfig): Promise<void> {
        this._config = config;
        await this.onInitialize(config);
        this._initialized = true;
    }
    
    async start(): Promise<void> {
        if (!this._initialized) {
            throw new Error('Module must be initialized before starting');
        }
        await this.onStart();
        this._running = true;
    }
    
    async stop(): Promise<void> {
        await this.onStop();
        this._running = false;
    }
    
    async destroy(): Promise<void> {
        if (this._running) {
            await this.stop();
        }
        await this.onDestroy();
        this._eventHandlers.clear();
    }
    
    abstract process(input: TInput): Promise<TOutput>;
    
    async validate(input: unknown): Promise<boolean> {
        return this.onValidate(input);
    }
    
    async getHealth(): Promise<HealthStatus> {
        return {
            status: this._running ? 'healthy' : 'stopped',
            initialized: this._initialized,
            running: this._running,
            timestamp: Date.now(),
            checks: await this.performHealthChecks()
        };
    }
    
    async getMetrics(): Promise<CubeMetrics> {
        return {
            requestsTotal: this.getRequestCount(),
            averageResponseTime: this.getAverageResponseTime(),
            errorRate: this.getErrorRate(),
            memoryUsage: this.getMemoryUsage()
        };
    }
    
    on(event: string, handler: EventHandler): void {
        if (!this._eventHandlers.has(event)) {
            this._eventHandlers.set(event, []);
        }
        this._eventHandlers.get(event)!.push(handler);
    }
    
    off(event: string, handler: EventHandler): void {
        const handlers = this._eventHandlers.get(event);
        if (handlers) {
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }
    
    emit(event: string, data: unknown): void {
        const handlers = this._eventHandlers.get(event) || [];
        handlers.forEach(handler => handler(data));
    }
    
    // 하위 클래스에서 구현할 훅 메서드들
    protected abstract onInitialize(config: TConfig): Promise<void>;
    protected abstract onStart(): Promise<void>;
    protected abstract onStop(): Promise<void>;
    protected abstract onDestroy(): Promise<void>;
    protected abstract onValidate(input: unknown): Promise<boolean>;
    protected abstract performHealthChecks(): Promise<HealthCheck[]>;
    
    // 메트릭 관련 메서드들 (하위 클래스에서 오버라이드 가능)
    protected getRequestCount(): number { return 0; }
    protected getAverageResponseTime(): number { return 0; }
    protected getErrorRate(): number { return 0; }
    protected getMemoryUsage(): number { return 0; }
}

// 지원 타입들
export interface HealthStatus {
    status: 'healthy' | 'warning' | 'critical' | 'stopped';
    initialized: boolean;
    running: boolean;
    timestamp: number;
    checks: HealthCheck[];
}

export interface HealthCheck {
    name: string;
    status: 'pass' | 'fail' | 'warn';
    message?: string;
    duration?: number;
}

export interface CubeMetrics {
    requestsTotal: number;
    averageResponseTime: number;
    errorRate: number;
    memoryUsage: number;
}

export type EventHandler = (data: unknown) => void;
```

## 🔗 **모듈 의존성 관리**

### **📦 의존성 선언**

```yaml
# cube.yaml - 큐브모듈 메타데이터 파일
name: "user-authentication"
version: "1.2.3"
category: "feature"
description: "JWT 기반 사용자 인증 시스템"

# 의존성 정의
dependencies:
  required:
    - "@heal7/crypto-utils@^2.0.0"      # 암호화 유틸리티
    - "@heal7/database-connector@^1.5.0" # DB 연결
    - "@heal7/logging@^3.1.0"            # 로깅 시스템
  
  optional:
    - "@heal7/redis-cache@^1.0.0"       # 캐시 (성능 향상용)
    - "@heal7/oauth-provider@^2.3.0"    # OAuth 지원
  
  development:
    - "@heal7/test-utils@^1.0.0"        # 테스트 도구
    - "@heal7/mock-data@^0.5.0"         # 모의 데이터

# 호환성 정보
compatibility:
  node: ">=16.0.0"
  rust: ">=1.70.0"
  go: ">=1.19.0"
  python: ">=3.9.0"

# 리소스 요구사항
resources:
  memory:
    min: 64      # 최소 메모리 (MB)
    recommended: 128
    max: 256
  cpu:
    cores: 1
    usage: 20    # 평균 CPU 사용률 (%)

# 설정 스키마
config_schema:
  type: "object"
  properties:
    jwt_secret:
      type: "string"
      description: "JWT 서명용 비밀키"
      required: true
    token_expiry:
      type: "number" 
      description: "토큰 만료 시간 (초)"
      default: 3600
    enable_refresh:
      type: "boolean"
      description: "리프레시 토큰 사용 여부"
      default: true
```

### **🔄 의존성 해결 알고리즘**

```typescript
// 의존성 해결 및 로딩 시스템
class CubeDependencyResolver {
    private modules = new Map<string, CubeModule>();
    private loadOrder: string[] = [];
    
    async resolveDependencies(moduleConfig: CubeConfig): Promise<string[]> {
        const visited = new Set<string>();
        const visiting = new Set<string>();
        const order: string[] = [];
        
        const visit = async (moduleName: string) => {
            if (visiting.has(moduleName)) {
                throw new Error(`Circular dependency detected: ${moduleName}`);
            }
            
            if (visited.has(moduleName)) {
                return;
            }
            
            visiting.add(moduleName);
            
            const dependencies = await this.getDependencies(moduleName);
            for (const dep of dependencies.required) {
                await visit(dep);
            }
            
            visiting.delete(moduleName);
            visited.add(moduleName);
            order.push(moduleName);
        };
        
        await visit(moduleConfig.name);
        return order;
    }
    
    async loadModule(moduleName: string): Promise<CubeModule> {
        // 의존성 순서대로 모듈 로딩
        const loadOrder = await this.resolveDependencies({ name: moduleName });
        
        for (const name of loadOrder) {
            if (!this.modules.has(name)) {
                const module = await this.createModule(name);
                await this.initializeModule(module);
                this.modules.set(name, module);
            }
        }
        
        return this.modules.get(moduleName)!;
    }
}
```

## 🧪 **테스트 및 검증 가이드라인**

### **📊 테스트 구조**

```
tests/
├── unit/                   # 단위 테스트
│   ├── rust/
│   │   └── core.test.rs
│   ├── go/
│   │   └── service_test.go  
│   ├── python/
│   │   └── test_ai.py
│   └── typescript/
│       └── ui.test.ts
├── integration/            # 통합 테스트
│   ├── api.integration.test.ts
│   ├── database.integration.test.ts
│   └── languages.integration.test.ts
├── e2e/                   # E2E 테스트
│   ├── user-journey.e2e.test.ts
│   └── performance.e2e.test.ts
├── fixtures/              # 테스트 데이터
│   ├── sample-data.json
│   └── mock-responses.json
└── utils/                 # 테스트 유틸리티
    ├── test-helpers.ts
    └── mock-factory.ts
```

### **🎯 테스트 표준**

```typescript
// 큐브모듈 테스트 표준 인터페이스
interface CubeModuleTest {
    // 기본 기능 테스트
    testInitialization(): Promise<void>;
    testBasicFunctionality(): Promise<void>;
    testErrorHandling(): Promise<void>;
    testResourceManagement(): Promise<void>;
    
    // 성능 테스트
    testPerformance(): Promise<void>;
    testMemoryUsage(): Promise<void>;
    testConcurrency(): Promise<void>;
    
    // 호환성 테스트
    testDependencyCompatibility(): Promise<void>;
    testVersionCompatibility(): Promise<void>;
    
    // 보안 테스트
    testInputValidation(): Promise<void>;
    testAuthenticationSecurity(): Promise<void>;
}

// 테스트 유틸리티
class CubeTestUtils {
    static async createTestModule<T extends CubeModule>(
        moduleClass: new () => T,
        config?: Partial<CubeConfig>
    ): Promise<T> {
        const module = new moduleClass();
        const testConfig = {
            environment: 'test' as const,
            features: {},
            settings: {},
            resources: {
                memory: { maxMB: 100, warningMB: 80 },
                cpu: { maxPercent: 50, cores: 1 },
                network: { maxConnections: 10, timeoutMs: 5000 }
            },
            ...config
        };
        
        await module.initialize(testConfig);
        return module;
    }
    
    static async measurePerformance<T>(
        operation: () => Promise<T>,
        iterations: number = 100
    ): Promise<{ averageTime: number; minTime: number; maxTime: number; result: T }> {
        const times: number[] = [];
        let result: T;
        
        for (let i = 0; i < iterations; i++) {
            const start = performance.now();
            result = await operation();
            const end = performance.now();
            times.push(end - start);
        }
        
        return {
            averageTime: times.reduce((a, b) => a + b) / times.length,
            minTime: Math.min(...times),
            maxTime: Math.max(...times),
            result: result!
        };
    }
}
```

### **✅ 품질 기준**

```yaml
코드_품질:
  테스트_커버리지: ">= 90%"
  타입_안전성: "100% (TypeScript, Rust)"
  문서화_완성도: ">= 95%"
  
성능_기준:
  초기화_시간: "< 100ms"
  평균_응답시간: "< 50ms" 
  메모리_사용량: "< 100MB (기본 설정)"
  동시_처리: ">= 1000 requests/sec"

보안_기준:
  입력_검증: "모든 외부 입력 검증"
  인증_보안: "JWT + HTTPS 필수"
  데이터_암호화: "민감 데이터 암호화"
  접근_제어: "최소 권한 원칙"

호환성_기준:
  언어_호환성: "명시된 최소 버전 지원"
  플랫폼_호환성: "Linux, macOS, Windows"
  브라우저_호환성: "Chrome 100+, Firefox 100+, Safari 15+"
```

## 🚀 **배포 및 버전 관리**

### **📦 패키징 표준**

```bash
# 큐브모듈 패키징 구조
cube-module-package/
├── cube.yaml              # 모듈 메타데이터
├── README.md              # 사용 가이드
├── LICENSE                # 라이선스
├── src/                   # 소스 코드
│   ├── rust/
│   ├── go/
│   ├── python/
│   └── typescript/
├── dist/                  # 빌드된 결과물
│   ├── rust/target/
│   ├── go/bin/
│   ├── python/__pycache__/
│   └── typescript/build/
├── docs/                  # 문서
├── examples/              # 예제
├── tests/                 # 테스트
└── scripts/               # 빌드/배포 스크립트
    ├── build.sh
    ├── test.sh
    ├── package.sh
    └── deploy.sh
```

### **🏷️ 버전 관리 전략**

```yaml
# 시맨틱 버저닝 적용
버전_형식: "MAJOR.MINOR.PATCH"

MAJOR: 
  - 호환성 없는 API 변경
  - 아키텍처 대폭 변경
  - 의존성 메이저 업데이트

MINOR:
  - 하위 호환 가능한 기능 추가
  - 성능 개선
  - 새로운 언어 지원

PATCH:
  - 버그 수정
  - 문서 개선
  - 작은 최적화

# 태깅 규칙
git_tags:
  - "v1.0.0"              # 정식 릴리스
  - "v1.0.0-rc.1"         # 릴리스 후보
  - "v1.0.0-beta.1"       # 베타 버전
  - "v1.0.0-alpha.1"      # 알파 버전
```

### **🔄 배포 파이프라인**

```yaml
# GitHub Actions 배포 워크플로우
name: Deploy Cube Module

on:
  push:
    tags: [ 'v*' ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          # Rust 테스트
          cargo test
          # Go 테스트  
          go test ./...
          # Python 테스트
          pytest
          # TypeScript 테스트
          npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build all languages
        run: |
          # Rust 빌드
          cargo build --release
          # Go 빌드
          go build -o bin/
          # Python 패키징
          python setup.py bdist_wheel
          # TypeScript 빌드
          npm run build

  package:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Create cube package
        run: |
          ./scripts/package.sh
          
  deploy:
    needs: package
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to registry
        run: |
          # 큐브 레지스트리에 업로드
          cube-cli publish ./dist/package.tar.gz
```

## 🎯 **결론**

### **📈 큐브모듈러의 핵심 가치**

1. **개발 생산성 극대화**: 레고블럭 조립으로 복잡한 시스템을 빠르게 구성
2. **코드 품질 향상**: 표준화된 구조와 철저한 테스트로 안정성 확보
3. **유지보수 효율성**: 모듈별 독립적 업데이트로 변경 영향도 최소화
4. **학습 비용 절감**: 일관된 패턴과 완전한 문서화로 빠른 온보딩
5. **확장성 극대화**: 언어별 특화와 무한 조합 가능성

### **🚀 적용 가이드라인**

```typescript
// 큐브모듈 선택 기준
const selectCubeModule = (requirement: BusinessRequirement) => {
    if (requirement.performance === 'critical') {
        return 'rust-core-module';
    } else if (requirement.type === 'ai-processing') {
        return 'python-ai-module';
    } else if (requirement.type === 'user-interface') {
        return 'typescript-ui-module';
    } else if (requirement.type === 'service-orchestration') {
        return 'go-service-module';
    }
};

// 큐브모듈 조합 예시
const buildFeature = async (featureName: string) => {
    const modules = [
        await loadCube('rust-core-calculation'),
        await loadCube('python-ai-interpretation'),
        await loadCube('go-api-gateway'),
        await loadCube('typescript-user-interface')
    ];
    
    return assembleCubes(modules, featureName);
};
```

이 표준을 따라 개발된 큐브모듈은 **HEAL7 큐브모듈러 아키텍처**의 구성 요소로서 완벽하게 동작하며, 레고블럭처럼 자유자재로 조합하여 혁신적인 시스템을 구축할 수 있습니다.

---

*🧩 이 명세서는 HEAL7 큐브모듈러 생태계의 기반이 되는 표준입니다.*  
*📚 실제 적용 시 이 표준을 기준으로 모든 모듈을 개발해주세요.*