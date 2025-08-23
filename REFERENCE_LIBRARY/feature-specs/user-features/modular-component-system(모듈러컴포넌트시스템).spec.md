# 🧩 모듈러 컴포넌트 시스템 상세 설계서

> **목표**: 레고블럭 조립 방식의 확장 가능한 컴포넌트 아키텍처  
> **설계일**: 2025-08-18  
> **원칙**: 아파트 모듈러 공법처럼 독립적이면서 표준 인터페이스로 연결

## 🎯 **핵심 설계 원칙**

### **1. 표준 인터페이스 정의**
모든 모듈은 동일한 인터페이스를 구현하여 상호 호환성 보장

### **2. 의존성 역전 원칙**
상위 모듈이 하위 모듈에 의존하지 않고, 추상화에 의존

### **3. 단일 책임 원칙**
각 모듈은 하나의 명확한 기능만 담당

### **4. 개방-폐쇄 원칙**
확장에는 열려있고, 수정에는 닫혀있는 구조

## 🏗️ **모듈 아키텍처 구조**

### **📦 기본 모듈 패키지 구조**
```typescript
// 🧩 표준 모듈 인터페이스
interface Heal7Module {
  // 📋 모듈 메타데이터
  metadata: {
    name: string;           // 모듈명
    version: string;        // 버전
    author: string;         // 개발자
    description: string;    // 설명
    dependencies: string[]; // 의존성
    category: ModuleCategory; // 카테고리
  };
  
  // 🔧 생명주기 메서드
  initialize(): Promise<void>;    // 초기화
  activate(): Promise<void>;      // 활성화
  deactivate(): Promise<void>;    // 비활성화
  destroy(): Promise<void>;       // 정리
  
  // 📡 이벤트 시스템
  on(event: string, handler: Function): void;     // 이벤트 리스너
  emit(event: string, data: any): void;           // 이벤트 발생
  off(event: string, handler: Function): void;   // 리스너 제거
  
  // 🔌 인터페이스 제공
  getInterface(): ModuleInterface;  // 외부 인터페이스
  getComponent(): React.ComponentType; // React 컴포넌트
}

// 🏷️ 모듈 카테고리
enum ModuleCategory {
  FORTUNE = 'fortune',       // 운세 관련
  UI = 'ui',                // UI 컴포넌트
  SERVICE = 'service',      // 서비스 로직
  PAYMENT = 'payment',      // 결제 관련
  COMMUNITY = 'community',  // 커뮤니티
  ANALYTICS = 'analytics'   // 분석 도구
}
```

### **🔮 운세 모듈 실제 구현 예시**

#### **1. 사주명리 모듈**
```typescript
// 📊 @heal7/saju-module
export class SajuModule implements Heal7Module {
  metadata = {
    name: 'saju-calculator',
    version: '2.0.0',
    author: 'HEAL7 AI Team',
    description: '사주명리학 계산 및 해석 모듈',
    dependencies: ['@heal7/core', '@heal7/kasi-api'],
    category: ModuleCategory.FORTUNE
  };

  // 🏗️ 내부 상태 관리
  private calculator: SajuCalculator;
  private interpreter: SajuInterpreter;
  private cache: SajuCache;

  async initialize(): Promise<void> {
    // 📡 KASI API 연결
    await this.initializeKasiConnection();
    
    // 🗃️ 캐시 시스템 준비
    this.cache = new SajuCache();
    
    // 🧮 계산기 초기화
    this.calculator = new SajuCalculator();
    
    // 🔮 해석기 초기화 (AI 모델 로드)
    this.interpreter = new SajuInterpreter();
  }

  async activate(): Promise<void> {
    // 🔄 이벤트 리스너 등록
    this.on('calculate-saju', this.handleSajuCalculation.bind(this));
    this.on('interpret-result', this.handleSajuInterpretation.bind(this));
    
    console.log('✅ 사주 모듈 활성화 완료');
  }

  getComponent(): React.ComponentType {
    return SajuCalculatorWidget;
  }

  // 🧮 핵심 계산 로직
  private async handleSajuCalculation(userData: UserBirthData) {
    try {
      // 1️⃣ 기본 사주 계산
      const basicSaju = await this.calculator.calculate(userData);
      
      // 2️⃣ 오행 분석
      const wuxingAnalysis = await this.calculator.analyzeWuxing(basicSaju);
      
      // 3️⃣ 십신 분석
      const sipsinAnalysis = await this.calculator.analyzeSipsin(basicSaju);
      
      // 4️⃣ 결과 종합
      const result = {
        basic: basicSaju,
        wuxing: wuxingAnalysis,
        sipsin: sipsinAnalysis,
        timestamp: new Date()
      };
      
      // 🔄 결과 이벤트 발생
      this.emit('saju-calculated', result);
      
      return result;
    } catch (error) {
      this.emit('saju-error', error);
      throw error;
    }
  }
}

// 🎨 사주 위젯 컴포넌트
const SajuCalculatorWidget: React.FC = () => {
  const [result, setResult] = useState<SajuResult | null>(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="saju-calculator-widget">
      <SajuInputForm onSubmit={handleCalculation} />
      {loading && <LoadingSpinner />}
      {result && <SajuResultDisplay result={result} />}
    </div>
  );
};
```

#### **2. 타로카드 모듈**
```typescript
// 🃏 @heal7/tarot-module
export class TarotModule implements Heal7Module {
  metadata = {
    name: 'tarot-reader',
    version: '1.0.0',
    author: 'HEAL7 AI Team',
    description: '타로카드 리딩 및 해석 모듈',
    dependencies: ['@heal7/core', '@heal7/ai-interpreter'],
    category: ModuleCategory.FORTUNE
  };

  private deck: TarotDeck;
  private reader: TarotReader;
  private cardDatabase: TarotCardDB;

  async initialize(): Promise<void> {
    // 🃏 타로 덱 로드 (78장 풀세트)
    this.deck = await TarotDeck.loadStandardDeck();
    
    // 🔮 AI 해석기 초기화
    this.reader = new TarotReader();
    
    // 📚 카드 의미 데이터베이스
    this.cardDatabase = await TarotCardDB.load();
  }

  getComponent(): React.ComponentType {
    return TarotReaderWidget;
  }

  // 🎴 카드 뽑기 및 해석
  async drawCards(spread: TarotSpread, question: string): Promise<TarotReading> {
    // 1️⃣ 스프레드에 맞게 카드 뽑기
    const drawnCards = this.deck.drawCards(spread.cardCount);
    
    // 2️⃣ 각 카드 위치별 의미 분석
    const cardInterpretations = await Promise.all(
      drawnCards.map((card, index) => 
        this.reader.interpretCard(card, spread.positions[index], question)
      )
    );
    
    // 3️⃣ 전체적인 리딩 생성
    const overallReading = await this.reader.synthesizeReading(
      cardInterpretations, question
    );
    
    return {
      spread,
      cards: drawnCards,
      interpretations: cardInterpretations,
      overallReading,
      timestamp: new Date()
    };
  }
}

// 🎴 타로 위젯 컴포넌트
const TarotReaderWidget: React.FC = () => {
  const [reading, setReading] = useState<TarotReading | null>(null);
  const [selectedSpread, setSelectedSpread] = useState<TarotSpread>();

  return (
    <div className="tarot-reader-widget">
      <SpreadSelector onSelect={setSelectedSpread} />
      <QuestionInput onSubmit={handleReading} />
      {reading && <TarotReadingDisplay reading={reading} />}
    </div>
  );
};
```

### **🔌 모듈 레지스트리 시스템**

```typescript
// 🏪 모듈 레지스트리 (모듈 스토어)
class ModuleRegistry {
  private modules = new Map<string, Heal7Module>();
  private dependencies = new Map<string, string[]>();
  
  // 📦 모듈 등록
  async register(module: Heal7Module): Promise<void> {
    const { name, dependencies } = module.metadata;
    
    // 🔍 의존성 검증
    await this.validateDependencies(dependencies);
    
    // 📋 모듈 등록
    this.modules.set(name, module);
    this.dependencies.set(name, dependencies);
    
    // 🔧 초기화 및 활성화
    await module.initialize();
    await module.activate();
    
    console.log(`✅ 모듈 '${name}' 등록 완료`);
  }
  
  // 🔌 모듈 가져오기
  getModule<T extends Heal7Module>(name: string): T | null {
    return this.modules.get(name) as T || null;
  }
  
  // 🧩 컴포넌트 가져오기
  getComponent(moduleName: string): React.ComponentType | null {
    const module = this.modules.get(moduleName);
    return module?.getComponent() || null;
  }
  
  // 🔄 핫스왑 (런타임 모듈 교체)
  async hotSwap(oldModuleName: string, newModule: Heal7Module): Promise<void> {
    const oldModule = this.modules.get(oldModuleName);
    
    if (oldModule) {
      // 1️⃣ 기존 모듈 비활성화
      await oldModule.deactivate();
      await oldModule.destroy();
    }
    
    // 2️⃣ 새 모듈 등록
    await this.register(newModule);
    
    // 3️⃣ 전역 이벤트 발생
    globalEventBus.emit('module-swapped', {
      old: oldModuleName,
      new: newModule.metadata.name
    });
  }
  
  // 🔍 의존성 검증
  private async validateDependencies(deps: string[]): Promise<void> {
    for (const dep of deps) {
      if (!this.modules.has(dep)) {
        throw new Error(`의존성 모듈 '${dep}'를 찾을 수 없습니다.`);
      }
    }
  }
}

// 🌐 전역 모듈 레지스트리
export const moduleRegistry = new ModuleRegistry();
```

### **🎨 UI 컴포넌트 모듈 시스템**

```typescript
// 🎭 UI 컴포넌트 표준 인터페이스
interface UIComponentModule extends Heal7Module {
  // 🎨 테마 지원
  applyTheme(theme: Theme): void;
  
  // 📱 반응형 지원
  setBreakpoint(breakpoint: Breakpoint): void;
  
  // 🔄 상태 관리
  getState(): ComponentState;
  setState(state: Partial<ComponentState>): void;
  
  // 🎯 이벤트 핸들링
  bindEvents(eventMap: EventMap): void;
}

// 🃏 포춘 카드 컴포넌트 모듈
export class FortuneCardModule implements UIComponentModule {
  metadata = {
    name: 'fortune-card',
    version: '1.2.0',
    author: 'HEAL7 UI Team',
    description: '범용 운세 카드 컴포넌트',
    dependencies: ['@heal7/design-system'],
    category: ModuleCategory.UI
  };

  private theme: Theme;
  private state: CardState;

  getComponent(): React.ComponentType {
    // 🎨 테마와 상태를 주입한 컴포넌트 반환
    return (props: any) => (
      <FortuneCard 
        {...props} 
        theme={this.theme} 
        state={this.state}
        onEvent={this.handleEvent.bind(this)}
      />
    );
  }

  applyTheme(theme: Theme): void {
    this.theme = theme;
    this.emit('theme-changed', theme);
  }

  private handleEvent(event: string, data: any): void {
    // 🔄 이벤트를 상위로 전파
    this.emit(`card-${event}`, data);
  }
}

// 🎨 실제 포춘 카드 컴포넌트
const FortuneCard: React.FC<FortuneCardProps> = ({ 
  title, 
  content, 
  theme, 
  state,
  onEvent 
}) => {
  return (
    <motion.div 
      className={`fortune-card ${theme.cardClass}`}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => onEvent('click', { title, content })}
    >
      <div className="card-header">
        <h3 style={{ color: theme.colors.primary }}>{title}</h3>
      </div>
      <div className="card-content">
        {content}
      </div>
      <div className="card-footer">
        <button 
          className={theme.buttonClass}
          onClick={() => onEvent('action', 'details')}
        >
          자세히 보기
        </button>
      </div>
    </motion.div>
  );
};
```

### **🔧 모듈 설정 시스템**

```typescript
// ⚙️ 모듈 설정 관리자
class ModuleConfigManager {
  private configs = new Map<string, ModuleConfig>();
  
  // 📋 설정 등록
  registerConfig(moduleName: string, config: ModuleConfig): void {
    this.configs.set(moduleName, config);
  }
  
  // 🔧 설정 가져오기
  getConfig(moduleName: string): ModuleConfig | null {
    return this.configs.get(moduleName) || null;
  }
  
  // 💾 설정 저장 (로컬스토리지 + 서버)
  async saveConfig(moduleName: string, config: ModuleConfig): Promise<void> {
    // 1️⃣ 로컬 저장
    localStorage.setItem(`module-config-${moduleName}`, JSON.stringify(config));
    
    // 2️⃣ 서버 동기화
    await fetch('/api/module-configs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ moduleName, config })
    });
    
    // 3️⃣ 설정 업데이트
    this.configs.set(moduleName, config);
    
    // 4️⃣ 모듈에 변경사항 알림
    const module = moduleRegistry.getModule(moduleName);
    if (module) {
      module.emit('config-changed', config);
    }
  }
}

// 🎛️ 사주 모듈 설정 예시
interface SajuModuleConfig extends ModuleConfig {
  // 🔮 계산 옵션
  calculation: {
    useKasiApi: boolean;
    cacheResults: boolean;
    precisionLevel: 'basic' | 'advanced' | 'expert';
  };
  
  // 🎨 UI 옵션
  display: {
    showDetailedAnalysis: boolean;
    animationEnabled: boolean;
    colorTheme: 'cosmic' | 'traditional' | 'modern';
  };
  
  // 🔔 알림 옵션
  notifications: {
    dailyFortune: boolean;
    majorTransits: boolean;
    personalAnalysis: boolean;
  };
}
```

### **🚀 모듈 로더 시스템**

```typescript
// 📦 동적 모듈 로더
class ModuleLoader {
  private loadedModules = new Set<string>();
  
  // 🔄 모듈 동적 로딩
  async loadModule(moduleName: string): Promise<Heal7Module> {
    // 1️⃣ 이미 로드된 모듈 체크
    if (this.loadedModules.has(moduleName)) {
      return moduleRegistry.getModule(moduleName)!;
    }
    
    try {
      // 2️⃣ 모듈 동적 import
      const moduleExport = await import(`@heal7/${moduleName}`);
      const ModuleClass = moduleExport.default;
      
      // 3️⃣ 모듈 인스턴스 생성
      const moduleInstance = new ModuleClass();
      
      // 4️⃣ 레지스트리에 등록
      await moduleRegistry.register(moduleInstance);
      
      // 5️⃣ 로드 완료 표시
      this.loadedModules.add(moduleName);
      
      console.log(`✅ 모듈 '${moduleName}' 동적 로딩 완료`);
      return moduleInstance;
      
    } catch (error) {
      console.error(`❌ 모듈 '${moduleName}' 로딩 실패:`, error);
      throw error;
    }
  }
  
  // 📋 모듈 목록 로딩
  async loadModulesFromManifest(manifest: ModuleManifest): Promise<void> {
    const { modules, loadOrder } = manifest;
    
    // 🔄 의존성 순서대로 로딩
    for (const moduleName of loadOrder) {
      if (modules[moduleName]) {
        await this.loadModule(moduleName);
      }
    }
  }
  
  // 🔧 모듈 언로딩
  async unloadModule(moduleName: string): Promise<void> {
    const module = moduleRegistry.getModule(moduleName);
    
    if (module) {
      // 1️⃣ 모듈 비활성화
      await module.deactivate();
      await module.destroy();
      
      // 2️⃣ 레지스트리에서 제거
      moduleRegistry.unregister(moduleName);
      
      // 3️⃣ 로드 목록에서 제거
      this.loadedModules.delete(moduleName);
      
      console.log(`✅ 모듈 '${moduleName}' 언로딩 완료`);
    }
  }
}

// 📋 모듈 매니페스트 예시
const SajuSiteManifest: ModuleManifest = {
  modules: {
    'core': { version: '1.0.0', required: true },
    'design-system': { version: '2.0.0', required: true },
    'saju-calculator': { version: '2.0.0', required: false },
    'tarot-reader': { version: '1.0.0', required: false },
    'zodiac-analyzer': { version: '1.0.0', required: false },
    'community-board': { version: '1.5.0', required: false },
    'payment-system': { version: '1.2.0', required: false }
  },
  loadOrder: [
    'core',
    'design-system', 
    'saju-calculator',
    'tarot-reader',
    'zodiac-analyzer',
    'community-board',
    'payment-system'
  ]
};
```

### **🎯 실제 사용 예시**

```typescript
// 🚀 앱 초기화 시 모듈 시스템 구동
async function initializeApp() {
  // 1️⃣ 모듈 로더 초기화
  const loader = new ModuleLoader();
  
  // 2️⃣ 매니페스트에서 모듈들 로딩
  await loader.loadModulesFromManifest(SajuSiteManifest);
  
  // 3️⃣ 메인 앱 컴포넌트 렌더링
  ReactDOM.render(<App />, document.getElementById('root'));
}

// 🎨 메인 앱에서 모듈 컴포넌트 사용
const App: React.FC = () => {
  // 🧩 필요한 모듈 컴포넌트들 가져오기
  const SajuWidget = moduleRegistry.getComponent('saju-calculator');
  const TarotWidget = moduleRegistry.getComponent('tarot-reader');
  const CommunityBoard = moduleRegistry.getComponent('community-board');

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        {/* 🔮 운세 서비스 영역 */}
        <section className="fortune-services">
          {SajuWidget && <SajuWidget />}
          {TarotWidget && <TarotWidget />}
        </section>
        
        {/* 👥 커뮤니티 영역 */}
        <section className="community">
          {CommunityBoard && <CommunityBoard />}
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

// 🔄 런타임에 새 모듈 추가
async function addNewFeature() {
  // 🆕 새로운 별자리 모듈 동적 로딩
  const zodiacModule = await moduleLoader.loadModule('zodiac-analyzer');
  
  // 🎨 UI에 새 위젯 추가
  const ZodiacWidget = moduleRegistry.getComponent('zodiac-analyzer');
  
  // 🔄 앱 상태 업데이트 (새 컴포넌트 표시)
  appStateManager.addWidget('zodiac', ZodiacWidget);
}
```

---

## 📊 **성능 최적화 전략**

### **1. 지연 로딩 (Lazy Loading)**
- 🎯 필요한 모듈만 런타임에 로딩
- 📦 번들 크기 최소화
- ⚡ 초기 로딩 속도 향상

### **2. 캐싱 전략**
- 🗃️ 모듈 결과 캐싱
- 🔄 스마트 무효화
- 📊 메모리 효율성

### **3. 번들링 최적화**
- 🔧 Webpack Module Federation
- 📦 마이크로프론트엔드 지원
- 🚀 CDN 최적화

---

*📅 설계 완료일: 2025-08-18*  
*🧩 설계자: HEAL7 Architecture Team*  
*📝 문서 위치: `/home/ubuntu/CORE/feature-specs/user-features/`*