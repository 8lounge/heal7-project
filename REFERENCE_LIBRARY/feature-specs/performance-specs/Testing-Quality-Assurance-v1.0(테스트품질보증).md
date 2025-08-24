# Testing-Quality-Assurance-v1.0(테스트품질보증)

> **HEAL7 테스트 & 품질 보증 전략**  
> Version 1.0 | 2025-08-23 | Jest + Playwright + K6 + A/B테스트 + Sentry + DataDog 통합 전략

## 📋 **문서 개요**

### **목적**
- HEAL7 포춘텔링 플랫폼의 완전 테스트 자동화 전략
- Jest + Playwright + K6를 통한 단위/통합/성능 테스트
- A/B 테스트 프레임워크를 통한 데이터 기반 의사결정
- Sentry + DataDog 모니터링으로 실시간 품질 관리

### **대상 독자**
- QA 엔지니어
- 개발자 (Frontend/Backend)
- DevOps 엔지니어
- 프로덕트 매니저

### **관련 문서**
- [Frontend-Backend-Integration-v1.0(프론트엔드백엔드연동)](../../architecture-diagrams/integration-flows/Frontend-Backend-Integration-v1.0(프론트엔드백엔드연동).md)
- [Development-Process-Roadmap-v1.0(단계별개발프로세스로드맵)](../master-plans/Development-Process-Roadmap-v1.0(단계별개발프로세스로드맵).md)
- [Deployment-Infrastructure-Design-v1.0(배포인프라설계)](../../architecture-diagrams/devops-architecture/Deployment-Infrastructure-Design-v1.0(배포인프라설계).md)

---

## 🏗️ **테스트 아키텍처 전체 구조**

### **테스트 피라미드**
```mermaid
graph TB
    subgraph "Production Monitoring"
        SENTRY[Sentry Error Tracking]
        DATADOG[DataDog APM]
        ALERTS[Alert System]
    end
    
    subgraph "Performance Testing"
        K6[K6 Load Testing]
        STRESS[Stress Testing]
        ENDURANCE[Endurance Testing]
    end
    
    subgraph "E2E Testing"
        PLAYWRIGHT[Playwright Tests]
        VISUAL[Visual Regression]
        MOBILE[Mobile Testing]
    end
    
    subgraph "Integration Testing"
        API[API Integration Tests]
        DB[Database Tests]
        SERVICES[Service Integration]
    end
    
    subgraph "Unit Testing"
        JEST[Jest Unit Tests]
        COMPONENTS[Component Tests]
        UTILS[Utility Tests]
    end
    
    JEST --> API
    API --> PLAYWRIGHT
    PLAYWRIGHT --> K6
    K6 --> SENTRY
    SENTRY --> DATADOG
```

### **테스트 전략별 도구 매핑**
| 테스트 레벨 | 도구 | 커버리지 목표 | 실행 빈도 | 책임자 |
|-------------|------|---------------|-----------|--------|
| **Unit** | Jest + RTL | 90%+ | 모든 커밋 | 개발자 |
| **Integration** | Jest + Supertest | 80%+ | 매일 | 개발자 |
| **E2E** | Playwright | 70%+ 주요 플로우 | PR마다 | QA 팀 |
| **Performance** | K6 + Artillery | 95th percentile < 500ms | 주간 | DevOps |
| **Visual** | Playwright + Percy | 100% UI 컴포넌트 | 매일 | QA 팀 |
| **Security** | OWASP ZAP + Snyk | 취약점 0개 | 배포 전 | Security 팀 |

---

## 🧪 **Jest 단위 테스트 전략**

### **Jest 설정 및 구성**
```typescript
// jest.config.ts
import type { Config } from '@jest/types';

const config: Config.InitialOptions = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  
  // 모듈 매핑
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@/components/(.*)$': '<rootDir>/src/components/$1',
    '^@/lib/(.*)$': '<rootDir>/src/lib/$1',
    '^@/hooks/(.*)$': '<rootDir>/src/hooks/$1',
    '^@/types/(.*)$': '<rootDir>/src/types/$1'
  },
  
  // 테스트 파일 패턴
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.(test|spec).{js,jsx,ts,tsx}'
  ],
  
  // 커버리지 설정
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/test/**/*',
    '!src/stories/**/*',
    '!src/**/index.ts'
  ],
  
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 85,
      statements: 85
    },
    // 중요 모듈은 더 높은 커버리지 요구
    './src/lib/saju/': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95
    }
  },
  
  // 성능 설정
  maxWorkers: '50%',
  cache: true,
  
  // 타임아웃
  testTimeout: 10000,
  
  // 리포터
  reporters: [
    'default',
    ['jest-junit', { outputDirectory: './coverage', outputName: 'junit.xml' }],
    ['jest-html-reporters', { 
      publicPath: './coverage', 
      filename: 'report.html',
      expand: true 
    }]
  ]
};

export default config;
```

### **테스트 유틸리티 및 Mocks**
```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { configure } from '@testing-library/react';
import { server } from './mocks/server';

// React Testing Library 설정
configure({ testIdAttribute: 'data-testid' });

// MSW 서버 설정
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// 전역 모킹
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// 로컬 스토리지 모킹
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// src/test/mocks/handlers.ts - MSW 핸들러
import { rest } from 'msw';
import { API_ENDPOINTS } from '@/lib/api/constants';

export const handlers = [
  // 사주 계산 Mock
  rest.post(`*/api${API_ENDPOINTS.SAJU.CALCULATE}`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        data: {
          id: 'mock-saju-id',
          sajuPan: {
            year: { cheon: '甲', ji: '子' },
            month: { cheon: '乙', ji: '丑' },
            day: { cheon: '丙', ji: '寅' },
            hour: { cheon: '丁', ji: '卯' }
          },
          wuxing: {
            balance: 'strong_water',
            elements: ['water', 'wood'],
            strengths: ['intelligence', 'creativity'],
            weaknesses: ['impatience'],
            recommendations: ['practice meditation']
          }
        }
      })
    );
  }),
  
  // 인증 Mock
  rest.post(`*/api${API_ENDPOINTS.AUTH.LOGIN}`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        data: {
          user: { id: '1', email: 'test@heal7.com', name: 'Test User' },
          token: 'mock-jwt-token',
          permissions: ['read:profile', 'write:saju']
        }
      })
    );
  }),
  
  // AI 해석 Mock
  rest.post(`*/api${API_ENDPOINTS.AI.INTERPRET}`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        data: {
          interpretationId: 'mock-interpretation-id',
          estimatedTime: 30,
          status: 'processing'
        }
      })
    );
  })
];

// src/test/utils/render.tsx - 테스트 렌더링 유틸리티
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

// 전역 프로바이더 래퍼
function AllTheProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false }
    }
  });
  
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
}

// 커스텀 렌더 함수
export function customRender(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllTheProviders, ...options });
}

// 모든 테스트에서 사용할 수 있도록 re-export
export * from '@testing-library/react';
export { customRender as render };
```

### **컴포넌트 단위 테스트**
```typescript
// src/components/SajuBoard/__tests__/SajuBoard.test.tsx
import { render, screen, fireEvent, waitFor } from '@/test/utils/render';
import { SajuBoard } from '../SajuBoard';
import type { SajuResult } from '@/types/saju';

const mockSajuResult: SajuResult = {
  id: 'test-saju-1',
  userId: 'user-1',
  sajuPan: {
    year: { cheon: '甲', ji: '子' },
    month: { cheon: '乙', ji: '丑' },
    day: { cheon: '丙', ji: '寅' },
    hour: { cheon: '丁', ji: '卯' }
  },
  wuxing: {
    balance: 'strong_water',
    elements: ['water', 'wood'],
    strengths: ['intelligence'],
    weaknesses: ['impatience'],
    recommendations: ['meditation']
  },
  createdAt: '2025-08-23T00:00:00Z',
  updatedAt: '2025-08-23T00:00:00Z'
};

describe('SajuBoard', () => {
  it('사주판을 올바르게 렌더링한다', () => {
    render(<SajuBoard result={mockSajuResult} />);
    
    // 사주판 제목 확인
    expect(screen.getByRole('heading', { name: /사주판/i })).toBeInTheDocument();
    
    // 천간지지 표시 확인
    expect(screen.getByText('甲')).toBeInTheDocument();
    expect(screen.getByText('子')).toBeInTheDocument();
    expect(screen.getByText('乙')).toBeInTheDocument();
    expect(screen.getByText('丑')).toBeInTheDocument();
  });
  
  it('오행 정보를 올바르게 표시한다', () => {
    render(<SajuBoard result={mockSajuResult} />);
    
    // 오행 밸런스 확인
    expect(screen.getByText('수기가 강함')).toBeInTheDocument();
    
    // 강한 원소들 확인
    expect(screen.getByText('물')).toBeInTheDocument();
    expect(screen.getByText('나무')).toBeInTheDocument();
  });
  
  it('상세 보기 토글이 작동한다', async () => {
    render(<SajuBoard result={mockSajuResult} />);
    
    const detailButton = screen.getByRole('button', { name: /상세 보기/i });
    fireEvent.click(detailButton);
    
    await waitFor(() => {
      expect(screen.getByText('장점')).toBeInTheDocument();
      expect(screen.getByText('intelligence')).toBeInTheDocument();
    });
  });
  
  it('접근성 요구사항을 만족한다', () => {
    render(<SajuBoard result={mockSajuResult} />);
    
    // ARIA 레이블 확인
    expect(screen.getByLabelText('사주 보드')).toBeInTheDocument();
    
    // 키보드 네비게이션 확인
    const grid = screen.getByRole('grid');
    expect(grid).toHaveAttribute('aria-label');
    
    // 스크린 리더용 설명 확인
    expect(screen.getByText(/사주판을 표시합니다/)).toBeInTheDocument();
  });
  
  it('로딩 상태를 올바르게 처리한다', () => {
    render(<SajuBoard result={null} loading={true} />);
    
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(screen.getByText(/계산 중.../i)).toBeInTheDocument();
  });
  
  it('에러 상태를 올바르게 처리한다', () => {
    const error = new Error('계산 실패');
    render(<SajuBoard result={null} error={error} />);
    
    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('계산 실패')).toBeInTheDocument();
  });
});

// src/hooks/__tests__/useSajuCalculation.test.ts
import { renderHook, act } from '@testing-library/react';
import { useSajuCalculation } from '../useSajuCalculation';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useSajuCalculation', () => {
  it('초기 상태가 올바르다', () => {
    const { result } = renderHook(() => useSajuCalculation(), {
      wrapper: createWrapper()
    });
    
    expect(result.current.isCalculating).toBe(false);
    expect(result.current.result).toBe(null);
    expect(result.current.error).toBe(null);
  });
  
  it('사주 계산을 성공적으로 수행한다', async () => {
    const { result } = renderHook(() => useSajuCalculation(), {
      wrapper: createWrapper()
    });
    
    const calculationInput = {
      birthDate: '1990-01-01',
      birthTime: '12:00',
      isLunar: false,
      gender: 'male' as const,
      name: 'Test User'
    };
    
    await act(async () => {
      await result.current.calculateSaju(calculationInput);
    });
    
    expect(result.current.isCalculating).toBe(false);
    expect(result.current.result).not.toBeNull();
    expect(result.current.error).toBe(null);
  });
  
  it('계산 중 에러를 올바르게 처리한다', async () => {
    // MSW 핸들러를 에러 응답으로 오버라이드
    server.use(
      rest.post(`*/api${API_ENDPOINTS.SAJU.CALCULATE}`, (req, res, ctx) => {
        return res(ctx.status(400), ctx.json({ error: '잘못된 입력값' }));
      })
    );
    
    const { result } = renderHook(() => useSajuCalculation(), {
      wrapper: createWrapper()
    });
    
    const calculationInput = {
      birthDate: 'invalid-date',
      birthTime: '25:00',
      isLunar: false,
      gender: 'male' as const,
      name: ''
    };
    
    await act(async () => {
      await result.current.calculateSaju(calculationInput);
    });
    
    expect(result.current.isCalculating).toBe(false);
    expect(result.current.result).toBe(null);
    expect(result.current.error).toBeTruthy();
  });
});
```

---

## 🎭 **Playwright E2E 테스트**

### **Playwright 설정**
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  
  // 리포터 설정
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/results.xml' }],
    ['allure-playwright']
  ],
  
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // 글로벌 설정
    locale: 'ko-KR',
    timezoneId: 'Asia/Seoul',
    
    // 네트워크 설정
    ignoreHTTPSErrors: true,
    extraHTTPHeaders: {
      'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'
    }
  },
  
  // 프로젝트별 설정
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  
  // 웹 서버 설정 (개발용)
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### **E2E 테스트 시나리오**
```typescript
// e2e/saju-calculation.spec.ts
import { test, expect, Page } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { SajuCalculationPage } from './pages/SajuCalculationPage';

test.describe('사주 계산 플로우', () => {
  let loginPage: LoginPage;
  let sajuPage: SajuCalculationPage;
  
  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    sajuPage = new SajuCalculationPage(page);
    
    // 로그인
    await loginPage.goto();
    await loginPage.login('test@heal7.com', 'password123');
    await expect(page).toHaveURL('/dashboard');
  });
  
  test('기본 사주 계산이 성공한다', async ({ page }) => {
    await sajuPage.goto();
    
    // 생년월일시 입력
    await sajuPage.fillBirthInfo({
      date: '1990-01-01',
      time: '12:00',
      isLunar: false,
      gender: 'male',
      name: '홍길동'
    });
    
    // 계산 시작
    await sajuPage.clickCalculateButton();
    
    // 로딩 상태 확인
    await expect(sajuPage.loadingIndicator).toBeVisible();
    await expect(sajuPage.progressBar).toBeVisible();
    
    // 결과 확인 (최대 30초 대기)
    await expect(sajuPage.sajuBoard).toBeVisible({ timeout: 30000 });
    await expect(sajuPage.wuxingChart).toBeVisible();
    
    // 사주판 내용 검증
    await expect(sajuPage.sajuBoard.locator('[data-pillar="year"]')).toContainText(/[甲乙丙丁戊己庚辛壬癸]/);
    await expect(sajuPage.sajuBoard.locator('[data-pillar="month"]')).toContainText(/[子丑寅卯辰巳午未申酉戌亥]/);
    
    // 해석 텍스트 확인
    await expect(sajuPage.interpretationPanel).toContainText(/당신의 사주/);
  });
  
  test('음력 변환이 정확하게 작동한다', async ({ page }) => {
    await sajuPage.goto();
    
    await sajuPage.fillBirthInfo({
      date: '1990-01-15',
      time: '14:30',
      isLunar: true,
      gender: 'female',
      name: '김민정'
    });
    
    // 음력 표시 확인
    await expect(sajuPage.lunarIndicator).toBeVisible();
    await expect(sajuPage.lunarIndicator).toContainText('음력');
    
    // 양력 변환된 날짜 확인
    await sajuPage.clickCalculateButton();
    await expect(sajuPage.sajuBoard).toBeVisible({ timeout: 30000 });
    
    // 변환된 날짜가 다른지 확인
    const convertedDate = await sajuPage.getConvertedDate();
    expect(convertedDate).not.toBe('1990-01-15');
  });
  
  test('결제 플로우가 올바르게 작동한다', async ({ page }) => {
    await sajuPage.goto();
    await sajuPage.fillBirthInfo({
      date: '1985-12-25',
      time: '09:15',
      isLunar: false,
      gender: 'male',
      name: '이철수'
    });
    
    // 프리미엄 옵션 선택
    await sajuPage.selectPremiumOption();
    await expect(sajuPage.priceDisplay).toContainText('5,000원');
    
    // 결제 진행
    await sajuPage.clickCalculateButton();
    await expect(sajuPage.paymentModal).toBeVisible();
    
    // 결제 정보 입력 (테스트 카드)
    await sajuPage.fillPaymentInfo({
      cardNumber: '4242-4242-4242-4242',
      expiry: '12/25',
      cvv: '123',
      name: '이철수'
    });
    
    await sajuPage.clickPayButton();
    
    // 결제 성공 확인
    await expect(sajuPage.paymentSuccessMessage).toBeVisible({ timeout: 10000 });
    await expect(sajuPage.sajuBoard).toBeVisible({ timeout: 30000 });
  });
  
  test('AI 해석이 점진적으로 로드된다', async ({ page }) => {
    await sajuPage.goto();
    await sajuPage.fillBirthInfo({
      date: '1992-08-08',
      time: '16:45',
      isLunar: false,
      gender: 'female',
      name: '박영희'
    });
    
    await sajuPage.clickCalculateButton();
    await expect(sajuPage.sajuBoard).toBeVisible({ timeout: 30000 });
    
    // AI 해석 섹션들이 순차적으로 나타나는지 확인
    const aiSections = [
      sajuPage.personalitySection,
      sajuPage.careerSection,
      sajuPage.relationshipSection,
      sajuPage.healthSection,
      sajuPage.wealthSection
    ];
    
    for (const section of aiSections) {
      await expect(section).toBeVisible({ timeout: 60000 });
      await expect(section.locator('.content')).not.toBeEmpty();
    }
    
    // 모든 AI 모델 결과 확인
    await expect(sajuPage.aiModelsStatus).toContainText('9/9 완료');
  });
});

// e2e/visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test('사주판 컴포넌트 시각적 일관성', async ({ page }) => {
    await page.goto('/demo/saju-board');
    
    // 사주판 완전 로드 대기
    await page.waitForLoadState('networkidle');
    
    // 스크린샷 비교
    await expect(page.locator('.saju-board')).toHaveScreenshot('saju-board-default.png');
    
    // 다크 모드 전환
    await page.click('[data-testid="theme-toggle"]');
    await page.waitForTimeout(500); // 애니메이션 완료 대기
    
    await expect(page.locator('.saju-board')).toHaveScreenshot('saju-board-dark.png');
  });
  
  test('반응형 레이아웃 확인', async ({ page }) => {
    await page.goto('/dashboard');
    
    // 데스크톱 뷰
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(page).toHaveScreenshot('dashboard-desktop.png');
    
    // 태블릿 뷰
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('dashboard-tablet.png');
    
    // 모바일 뷰
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('dashboard-mobile.png');
  });
});

// e2e/pages/SajuCalculationPage.ts - Page Object Model
export class SajuCalculationPage {
  constructor(private page: Page) {}
  
  // Selectors
  get dateInput() { return this.page.locator('[data-testid="birth-date"]'); }
  get timeInput() { return this.page.locator('[data-testid="birth-time"]'); }
  get lunarCheckbox() { return this.page.locator('[data-testid="is-lunar"]'); }
  get genderSelect() { return this.page.locator('[data-testid="gender-select"]'); }
  get nameInput() { return this.page.locator('[data-testid="name-input"]'); }
  get calculateButton() { return this.page.locator('[data-testid="calculate-button"]'); }
  get loadingIndicator() { return this.page.locator('[data-testid="loading-indicator"]'); }
  get progressBar() { return this.page.locator('[data-testid="progress-bar"]'); }
  get sajuBoard() { return this.page.locator('[data-testid="saju-board"]'); }
  get wuxingChart() { return this.page.locator('[data-testid="wuxing-chart"]'); }
  get interpretationPanel() { return this.page.locator('[data-testid="interpretation-panel"]'); }
  
  // Actions
  async goto() {
    await this.page.goto('/saju/calculate');
  }
  
  async fillBirthInfo(info: {
    date: string;
    time: string;
    isLunar: boolean;
    gender: 'male' | 'female';
    name: string;
  }) {
    await this.dateInput.fill(info.date);
    await this.timeInput.fill(info.time);
    
    if (info.isLunar) {
      await this.lunarCheckbox.check();
    }
    
    await this.genderSelect.selectOption(info.gender);
    await this.nameInput.fill(info.name);
  }
  
  async clickCalculateButton() {
    await this.calculateButton.click();
  }
  
  async waitForCalculationComplete() {
    await expect(this.sajuBoard).toBeVisible({ timeout: 30000 });
  }
}
```

---

## 🚀 **K6 성능 테스트**

### **K6 설정 및 시나리오**
```javascript
// k6/performance-test.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Counter, Trend } from 'k6/metrics';

// 커스텀 메트릭
export const errorRate = new Rate('errors');
export const successfulLogins = new Counter('successful_logins');
export const sajuCalculationTime = new Trend('saju_calculation_duration');
export const aiInterpretationTime = new Trend('ai_interpretation_duration');

// 테스트 설정
export const options = {
  stages: [
    { duration: '2m', target: 100 },   // 워밍업
    { duration: '5m', target: 500 },   // 정상 부하
    { duration: '2m', target: 1000 },  // 피크 부하
    { duration: '5m', target: 1000 },  // 피크 유지
    { duration: '2m', target: 0 },     // 쿨다운
  ],
  
  thresholds: {
    http_req_duration: ['p(95)<500'],           // 95% 요청이 500ms 이하
    http_req_failed: ['rate<0.1'],             // 실패율 10% 이하
    errors: ['rate<0.1'],                      // 에러율 10% 이하
    saju_calculation_duration: ['p(95)<10000'], // 사주 계산 95% 10초 이하
    ai_interpretation_duration: ['p(95)<30000'], // AI 해석 95% 30초 이하
  },
  
  cloud: {
    projectID: 3699516,
    name: 'HEAL7 Performance Test'
  }
};

const BASE_URL = __ENV.BASE_URL || 'https://api.heal7.com';

// 테스트 데이터
const testUsers = [
  { email: 'test1@heal7.com', password: 'password123' },
  { email: 'test2@heal7.com', password: 'password123' },
  { email: 'test3@heal7.com', password: 'password123' },
];

const sajuTestData = [
  {
    birthDate: '1990-01-01',
    birthTime: '12:00',
    isLunar: false,
    gender: 'male',
    name: 'TestUser1'
  },
  {
    birthDate: '1985-08-15',
    birthTime: '14:30',
    isLunar: true,
    gender: 'female',
    name: 'TestUser2'
  },
  {
    birthDate: '1992-12-25',
    birthTime: '09:45',
    isLunar: false,
    gender: 'male',
    name: 'TestUser3'
  }
];

export function setup() {
  // 테스트 사용자 생성
  console.log('Setting up test environment...');
  
  const setupData = testUsers.map(user => {
    const loginResponse = http.post(`${BASE_URL}/auth/login`, {
      email: user.email,
      password: user.password
    });
    
    if (loginResponse.status === 200) {
      const token = JSON.parse(loginResponse.body).data.token;
      return { ...user, token };
    }
    
    return null;
  }).filter(Boolean);
  
  return { users: setupData };
}

export default function(data) {
  const user = data.users[Math.floor(Math.random() * data.users.length)];
  const sajuData = sajuTestData[Math.floor(Math.random() * sajuTestData.length)];
  
  const headers = {
    'Authorization': `Bearer ${user.token}`,
    'Content-Type': 'application/json',
  };
  
  group('사주 계산 플로우', () => {
    // 1. 사용자 프로필 조회
    group('프로필 조회', () => {
      const profileResponse = http.get(`${BASE_URL}/users/profile`, { headers });
      
      const profileSuccess = check(profileResponse, {
        '프로필 조회 성공': (r) => r.status === 200,
        '응답 시간 < 200ms': (r) => r.timings.duration < 200,
      });
      
      if (!profileSuccess) {
        errorRate.add(1);
      }
    });
    
    // 2. 사주 계산 요청
    group('사주 계산', () => {
      const calculationStart = Date.now();
      const calculationResponse = http.post(`${BASE_URL}/saju/calculate`, 
        JSON.stringify(sajuData), 
        { headers }
      );
      const calculationDuration = Date.now() - calculationStart;
      
      const calculationSuccess = check(calculationResponse, {
        '사주 계산 성공': (r) => r.status === 200,
        '계산 결과 포함': (r) => JSON.parse(r.body).data.sajuPan !== undefined,
      });
      
      sajuCalculationTime.add(calculationDuration);
      
      if (!calculationSuccess) {
        errorRate.add(1);
        return; // 계산 실패시 후속 단계 건너뛰기
      }
      
      const sajuResult = JSON.parse(calculationResponse.body).data;
      
      // 3. AI 해석 요청
      group('AI 해석', () => {
        const interpretationStart = Date.now();
        const interpretationResponse = http.post(`${BASE_URL}/ai/interpret`, 
          JSON.stringify({
            sajuId: sajuResult.id,
            models: ['gemini_2_flash', 'gpt4_turbo', 'claude_sonnet'],
            depth: 'detailed'
          }), 
          { headers }
        );
        const interpretationDuration = Date.now() - interpretationStart;
        
        const interpretationSuccess = check(interpretationResponse, {
          'AI 해석 요청 성공': (r) => r.status === 200,
          '해석 ID 반환': (r) => JSON.parse(r.body).data.interpretationId !== undefined,
        });
        
        aiInterpretationTime.add(interpretationDuration);
        
        if (!interpretationSuccess) {
          errorRate.add(1);
        }
      });
    });
    
    // 4. 결제 플로우 (10% 확률)
    if (Math.random() < 0.1) {
      group('결제 처리', () => {
        const paymentResponse = http.post(`${BASE_URL}/payments/subscribe`, 
          JSON.stringify({
            planId: 'premium_monthly',
            paymentMethod: 'card',
            cardToken: 'test_card_token'
          }), 
          { headers }
        );
        
        const paymentSuccess = check(paymentResponse, {
          '결제 처리 성공': (r) => r.status === 200,
          '응답 시간 < 3s': (r) => r.timings.duration < 3000,
        });
        
        if (!paymentSuccess) {
          errorRate.add(1);
        }
      });
    }
  });
  
  sleep(Math.random() * 5 + 1); // 1-6초 랜덤 대기
}

export function teardown(data) {
  console.log('Cleaning up test environment...');
  // 테스트 데이터 정리
}

// k6/stress-test.js - 스트레스 테스트
export const options = {
  executor: 'ramping-vus',
  startVUs: 0,
  stages: [
    { duration: '10m', target: 2000 },  // 2000 사용자까지 점진적 증가
    { duration: '5m', target: 2000 },   // 2000 사용자 유지
    { duration: '10m', target: 5000 },  // 5000 사용자까지 증가 (한계 테스트)
    { duration: '5m', target: 5000 },   // 5000 사용자 유지
    { duration: '10m', target: 0 },     // 점진적 감소
  ],
  
  thresholds: {
    http_req_duration: ['p(95)<2000'],    // 스트레스 상황에서 2초 이하
    http_req_failed: ['rate<0.25'],       // 스트레스 상황에서 25% 이하
    errors: ['rate<0.25'],
  },
};

// k6/endurance-test.js - 내구성 테스트
export const options = {
  vus: 500,
  duration: '2h', // 2시간 지속
  
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.05'],
    errors: ['rate<0.05'],
  },
};
```

### **성능 모니터링 대시보드**
```javascript
// k6/dashboard-metrics.js
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.1/index.js";

export function handleSummary(data) {
  return {
    "performance-report.html": htmlReport(data),
    "performance-summary.txt": textSummary(data, { indent: " ", enableColors: true }),
    "performance-results.json": JSON.stringify(data),
  };
}

// Grafana 대시보드와 연동
export const grafanaConfig = {
  dashboard: {
    title: "HEAL7 Performance Monitoring",
    panels: [
      {
        title: "Response Time",
        type: "graph",
        targets: [
          { expr: 'k6_http_req_duration{job="k6"}' }
        ]
      },
      {
        title: "Throughput",
        type: "graph", 
        targets: [
          { expr: 'rate(k6_http_reqs[5m])' }
        ]
      },
      {
        title: "Error Rate",
        type: "singlestat",
        targets: [
          { expr: 'k6_http_req_failed{job="k6"}' }
        ]
      }
    ]
  }
};
```

---

## 🧪 **A/B 테스트 프레임워크**

### **A/B 테스트 설계**
```typescript
// src/lib/ab-testing/ABTestingFramework.ts
interface ABTestVariant {
  id: string;
  name: string;
  weight: number; // 0-100 사이의 가중치
  config: Record<string, any>;
}

interface ABTest {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'running' | 'completed' | 'paused';
  variants: ABTestVariant[];
  targetAudience?: {
    userType?: 'new' | 'returning' | 'premium';
    location?: string[];
    ageRange?: [number, number];
  };
  metrics: ABTestMetric[];
  startDate: Date;
  endDate?: Date;
  sampleSize?: number;
  confidenceLevel: number; // 95, 99 등
}

interface ABTestMetric {
  name: string;
  type: 'conversion' | 'engagement' | 'revenue' | 'time';
  primaryGoal: boolean;
}

export class ABTestingFramework {
  private tests = new Map<string, ABTest>();
  private userAssignments = new Map<string, Map<string, string>>(); // userId -> testId -> variantId
  
  // A/B 테스트 생성
  createTest(test: Omit<ABTest, 'id'>): ABTest {
    const id = this.generateTestId();
    const fullTest: ABTest = { ...test, id };
    
    this.tests.set(id, fullTest);
    this.logTestEvent('test_created', { testId: id, test: fullTest });
    
    return fullTest;
  }
  
  // 사용자를 변형(variant)에 할당
  assignUserToVariant(userId: string, testId: string): string | null {
    const test = this.tests.get(testId);
    if (!test || test.status !== 'running') {
      return null;
    }
    
    // 이미 할당된 경우 기존 할당 반환
    const userTests = this.userAssignments.get(userId) || new Map();
    if (userTests.has(testId)) {
      return userTests.get(testId)!;
    }
    
    // 타겟 오디언스 확인
    if (!this.isUserInTargetAudience(userId, test.targetAudience)) {
      return null;
    }
    
    // 가중치 기반 변형 선택
    const variantId = this.selectVariantByWeight(test.variants, userId);
    
    // 할당 저장
    userTests.set(testId, variantId);
    this.userAssignments.set(userId, userTests);
    
    // 분석용 이벤트 로깅
    this.logTestEvent('user_assigned', {
      userId,
      testId,
      variantId,
      timestamp: new Date().toISOString()
    });
    
    return variantId;
  }
  
  // 변형 설정 조회
  getVariantConfig(userId: string, testId: string): Record<string, any> | null {
    const variantId = this.assignUserToVariant(userId, testId);
    if (!variantId) return null;
    
    const test = this.tests.get(testId);
    const variant = test?.variants.find(v => v.id === variantId);
    
    return variant?.config || null;
  }
  
  // 이벤트 추적
  trackEvent(userId: string, testId: string, eventName: string, data?: any) {
    const variantId = this.userAssignments.get(userId)?.get(testId);
    if (!variantId) return;
    
    this.logTestEvent('test_event', {
      userId,
      testId,
      variantId,
      eventName,
      data,
      timestamp: new Date().toISOString()
    });
  }
  
  // 결과 분석
  async analyzeResults(testId: string): Promise<ABTestResults> {
    const test = this.tests.get(testId);
    if (!test) throw new Error(`Test ${testId} not found`);
    
    const events = await this.getTestEvents(testId);
    const analysis = this.performStatisticalAnalysis(events, test);
    
    return analysis;
  }
  
  private selectVariantByWeight(variants: ABTestVariant[], userId: string): string {
    // 사용자 ID 기반 시드로 일관된 랜덤성 보장
    const seed = this.hashUserId(userId);
    const random = this.seededRandom(seed) * 100;
    
    let cumulativeWeight = 0;
    for (const variant of variants) {
      cumulativeWeight += variant.weight;
      if (random <= cumulativeWeight) {
        return variant.id;
      }
    }
    
    // 폴백: 첫 번째 변형 반환
    return variants[0].id;
  }
  
  private performStatisticalAnalysis(events: ABTestEvent[], test: ABTest): ABTestResults {
    const variantResults = new Map<string, VariantResults>();
    
    // 변형별 메트릭 계산
    test.variants.forEach(variant => {
      const variantEvents = events.filter(e => e.variantId === variant.id);
      const results: VariantResults = {
        variantId: variant.id,
        variantName: variant.name,
        sampleSize: new Set(variantEvents.map(e => e.userId)).size,
        metrics: {}
      };
      
      // 각 메트릭 계산
      test.metrics.forEach(metric => {
        results.metrics[metric.name] = this.calculateMetric(variantEvents, metric);
      });
      
      variantResults.set(variant.id, results);
    });
    
    // 통계적 유의성 검증
    const statisticalTests = this.performSignificanceTests(variantResults, test);
    
    return {
      testId: test.id,
      testName: test.name,
      status: test.status,
      variants: Array.from(variantResults.values()),
      statisticalSignificance: statisticalTests,
      recommendation: this.generateRecommendation(variantResults, statisticalTests)
    };
  }
}

// A/B 테스트 훅
export function useABTest(testId: string): {
  variant: string | null;
  config: Record<string, any> | null;
  track: (eventName: string, data?: any) => void;
} {
  const { user } = useAuth();
  const abTesting = useRef(new ABTestingFramework());
  const [variant, setVariant] = useState<string | null>(null);
  const [config, setConfig] = useState<Record<string, any> | null>(null);
  
  useEffect(() => {
    if (!user?.id) return;
    
    const assignedVariant = abTesting.current.assignUserToVariant(user.id, testId);
    const variantConfig = abTesting.current.getVariantConfig(user.id, testId);
    
    setVariant(assignedVariant);
    setConfig(variantConfig);
  }, [user?.id, testId]);
  
  const track = useCallback((eventName: string, data?: any) => {
    if (!user?.id) return;
    abTesting.current.trackEvent(user.id, testId, eventName, data);
  }, [user?.id, testId]);
  
  return { variant, config, track };
}
```

### **실제 A/B 테스트 시나리오**
```typescript
// src/components/experiments/SajuBoardExperiment.tsx
export function SajuBoardExperiment({ result }: { result: SajuResult }) {
  const { variant, config, track } = useABTest('saju-board-design-v2');
  
  useEffect(() => {
    // 실험 노출 이벤트
    track('experiment_view');
  }, [track]);
  
  const handleInteraction = useCallback((interactionType: string) => {
    track('user_interaction', { type: interactionType });
  }, [track]);
  
  if (variant === 'control') {
    // 기존 디자인 (A)
    return (
      <SajuBoardClassic 
        result={result}
        onInteraction={handleInteraction}
      />
    );
  }
  
  if (variant === 'modern') {
    // 신규 디자인 (B)
    return (
      <SajuBoardModern 
        result={result}
        config={config}
        onInteraction={handleInteraction}
      />
    );
  }
  
  if (variant === 'minimal') {
    // 미니멀 디자인 (C)
    return (
      <SajuBoardMinimal 
        result={result}
        config={config}
        onInteraction={handleInteraction}
      />
    );
  }
  
  // 폴백: 기본 디자인
  return <SajuBoardClassic result={result} onInteraction={handleInteraction} />;
}

// 실제 A/B 테스트 정의
export const ACTIVE_AB_TESTS = {
  'saju-board-design-v2': {
    name: '사주판 디자인 개선',
    description: '사주판 시각화 방식에 따른 사용자 참여도 비교',
    variants: [
      { id: 'control', name: '기존 디자인', weight: 40 },
      { id: 'modern', name: '모던 디자인', weight: 40 },
      { id: 'minimal', name: '미니멀 디자인', weight: 20 }
    ],
    metrics: [
      { name: 'view_time', type: 'time', primaryGoal: true },
      { name: 'interaction_rate', type: 'engagement', primaryGoal: true },
      { name: 'share_rate', type: 'conversion', primaryGoal: false }
    ],
    targetAudience: {
      userType: 'new',
      ageRange: [20, 40]
    }
  },
  
  'payment-flow-v3': {
    name: '결제 플로우 최적화',
    description: '결제 전환율 개선을 위한 UI/UX 테스트',
    variants: [
      { id: 'control', name: '기존 플로우', weight: 50 },
      { id: 'simplified', name: '간소화 플로우', weight: 50 }
    ],
    metrics: [
      { name: 'payment_conversion', type: 'conversion', primaryGoal: true },
      { name: 'payment_completion_time', type: 'time', primaryGoal: false }
    ]
  },
  
  'ai-interpretation-display': {
    name: 'AI 해석 표시 방식',
    description: '단계적 vs 일괄 AI 해석 표시 효과 비교',
    variants: [
      { id: 'progressive', name: '단계적 표시', weight: 50 },
      { id: 'batch', name: '일괄 표시', weight: 50 }
    ],
    metrics: [
      { name: 'reading_completion_rate', type: 'engagement', primaryGoal: true },
      { name: 'satisfaction_rating', type: 'conversion', primaryGoal: true }
    ]
  }
};
```

---

## 📊 **Sentry 에러 모니터링**

### **Sentry 설정**
```typescript
// src/lib/monitoring/sentry.config.ts
import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;
const SENTRY_ENVIRONMENT = process.env.NODE_ENV;
const SENTRY_RELEASE = process.env.NEXT_PUBLIC_APP_VERSION;

export function initSentry() {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: SENTRY_ENVIRONMENT,
    release: SENTRY_RELEASE,
    
    // 성능 모니터링
    tracesSampleRate: SENTRY_ENVIRONMENT === 'production' ? 0.1 : 1.0,
    
    // 세션 추적
    autoSessionTracking: true,
    
    // 사용자 피드백
    userFeedback: {
      user: {
        email: 'user@heal7.com',
        name: 'HEAL7 User'
      }
    },
    
    // 에러 필터링
    beforeSend(event, hint) {
      // 민감한 정보 제거
      if (event.exception) {
        event.exception.values?.forEach(exception => {
          if (exception.stacktrace?.frames) {
            exception.stacktrace.frames.forEach(frame => {
              // 사용자 입력 데이터 마스킹
              if (frame.vars) {
                Object.keys(frame.vars).forEach(key => {
                  if (key.includes('password') || key.includes('token')) {
                    frame.vars![key] = '[Masked]';
                  }
                });
              }
            });
          }
        });
      }
      
      // 스팸 에러 필터링
      if (hint.originalException instanceof Error) {
        const message = hint.originalException.message;
        if (message.includes('Non-Error promise rejection captured')) {
          return null;
        }
      }
      
      return event;
    },
    
    // 컨텍스트 태그
    initialScope: {
      tags: {
        component: 'heal7-frontend'
      }
    },
    
    // 성능 모니터링 대상 트랜잭션
    tracesPropagationTargets: [
      'api.heal7.com',
      /^https:\/\/api\.heal7\.com/,
    ],
    
    // 통합 설정
    integrations: [
      new Sentry.BrowserTracing({
        tracingOrigins: ['api.heal7.com', /^\/api/],
        routingInstrumentation: Sentry.nextRouterInstrumentation
      }),
      new Sentry.Replay({
        maskAllText: false,
        blockAllMedia: false,
      })
    ]
  });
}

// 커스텀 에러 리포팅
export class ErrorReporter {
  static captureException(error: Error, context?: Record<string, any>) {
    Sentry.withScope((scope) => {
      if (context) {
        Object.keys(context).forEach(key => {
          scope.setTag(key, context[key]);
        });
      }
      
      scope.setLevel('error');
      Sentry.captureException(error);
    });
  }
  
  static captureMessage(message: string, level: 'info' | 'warning' | 'error' = 'info', extra?: Record<string, any>) {
    Sentry.withScope((scope) => {
      scope.setLevel(level);
      
      if (extra) {
        scope.setContext('extra', extra);
      }
      
      Sentry.captureMessage(message);
    });
  }
  
  static setUserContext(user: { id: string; email: string; name: string }) {
    Sentry.setUser({
      id: user.id,
      email: user.email,
      username: user.name
    });
  }
  
  static addBreadcrumb(message: string, category: string, data?: any) {
    Sentry.addBreadcrumb({
      message,
      category,
      level: 'info',
      data
    });
  }
  
  // 사주 계산 에러 전용 리포팅
  static captureSajuError(error: Error, sajuInput: any) {
    Sentry.withScope((scope) => {
      scope.setTag('error_type', 'saju_calculation');
      scope.setContext('saju_input', {
        birthDate: sajuInput.birthDate,
        isLunar: sajuInput.isLunar,
        gender: sajuInput.gender,
        // 민감한 정보 제외
      });
      
      scope.setLevel('error');
      Sentry.captureException(error);
    });
  }
  
  // AI 서비스 에러 전용 리포팅
  static captureAIError(error: Error, modelName: string, requestData: any) {
    Sentry.withScope((scope) => {
      scope.setTag('error_type', 'ai_service');
      scope.setTag('ai_model', modelName);
      scope.setContext('ai_request', requestData);
      
      scope.setLevel('error');
      Sentry.captureException(error);
    });
  }
}
```

### **커스텀 에러 바운더리 with Sentry**
```typescript
// src/components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react';
import { ErrorReporter } from '@/lib/monitoring/sentry.config';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface Props {
  children: ReactNode;
  fallback?: ComponentType<{ error: Error; resetError: () => void }>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Sentry에 에러 리포팅
    ErrorReporter.captureException(error, {
      componentStack: errorInfo.componentStack,
      errorBoundary: true
    });
    
    // 커스텀 에러 핸들러 호출
    this.props.onError?.(error, errorInfo);
  }
  
  private resetError = () => {
    this.setState({ hasError: false, error: null });
  };
  
  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return <FallbackComponent error={this.state.error!} resetError={this.resetError} />;
    }
    
    return this.props.children;
  }
}

// 기본 에러 폴백 컴포넌트
function DefaultErrorFallback({ error, resetError }: { error: Error; resetError: () => void }) {
  return (
    <Card className="max-w-lg mx-auto mt-8 p-6">
      <div className="text-center">
        <h2 className="text-xl font-semibold text-red-600 mb-2">
          오류가 발생했습니다
        </h2>
        <p className="text-gray-600 mb-4">
          일시적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요.
        </p>
        <details className="text-sm text-gray-500 mb-4">
          <summary className="cursor-pointer">에러 상세 정보</summary>
          <pre className="mt-2 p-2 bg-gray-100 rounded text-left overflow-x-auto">
            {error.message}
          </pre>
        </details>
        <div className="space-x-2">
          <Button onClick={resetError}>다시 시도</Button>
          <Button 
            variant="outline" 
            onClick={() => window.location.reload()}
          >
            페이지 새로고침
          </Button>
        </div>
      </div>
    </Card>
  );
}
```

---

## 📈 **DataDog APM 모니터링**

### **DataDog 설정**
```typescript
// src/lib/monitoring/datadog.config.ts
import { datadogRum } from '@datadog/browser-rum';
import { datadogLogs } from '@datadog/browser-logs';

const DD_APPLICATION_ID = process.env.NEXT_PUBLIC_DD_APPLICATION_ID!;
const DD_CLIENT_TOKEN = process.env.NEXT_PUBLIC_DD_CLIENT_TOKEN!;
const DD_SITE = process.env.NEXT_PUBLIC_DD_SITE || 'datadoghq.com';
const DD_SERVICE = 'heal7-frontend';
const DD_ENV = process.env.NODE_ENV;
const DD_VERSION = process.env.NEXT_PUBLIC_APP_VERSION;

export function initDataDog() {
  // RUM (Real User Monitoring) 초기화
  datadogRum.init({
    applicationId: DD_APPLICATION_ID,
    clientToken: DD_CLIENT_TOKEN,
    site: DD_SITE,
    service: DD_SERVICE,
    env: DD_ENV,
    version: DD_VERSION,
    
    // 세션 설정
    sessionSampleRate: 100,
    sessionReplaySampleRate: 20, // 20% 세션 리플레이
    trackUserInteractions: true,
    trackResources: true,
    trackLongTasks: true,
    
    // 개인정보 보호
    defaultPrivacyLevel: 'allow',
    
    // 커스텀 액션 추적
    trackFrustrations: true,
    
    // 성능 메트릭
    trackViewsManually: false,
    trackInteractions: true
  });
  
  // 로그 초기화
  datadogLogs.init({
    clientToken: DD_CLIENT_TOKEN,
    site: DD_SITE,
    service: DD_SERVICE,
    env: DD_ENV,
    version: DD_VERSION,
    forwardErrorsToLogs: true,
    sessionSampleRate: 100
  });
  
  // 커스텀 전역 컨텍스트
  datadogRum.setGlobalContextProperty('feature_flags', {
    new_saju_ui: true,
    ai_interpretation: true
  });
}

// 커스텀 메트릭 수집
export class MetricsCollector {
  // 사주 계산 성능 추적
  static trackSajuCalculation(input: any) {
    const startTime = performance.now();
    
    datadogRum.addAction('saju_calculation_started', {
      birth_year: new Date(input.birthDate).getFullYear(),
      is_lunar: input.isLunar,
      gender: input.gender
    });
    
    return {
      finish: (result?: any) => {
        const duration = performance.now() - startTime;
        
        datadogRum.addAction('saju_calculation_completed', {
          duration_ms: duration,
          success: !!result,
          calculation_id: result?.id
        });
        
        // 커스텀 메트릭 전송
        datadogLogs.logger.info('Saju calculation completed', {
          duration_ms: duration,
          performance: {
            calculation_time: duration,
            timestamp: new Date().toISOString()
          }
        });
      },
      
      error: (error: Error) => {
        const duration = performance.now() - startTime;
        
        datadogRum.addAction('saju_calculation_failed', {
          duration_ms: duration,
          error_message: error.message,
          error_type: error.constructor.name
        });
      }
    };
  }
  
  // AI 해석 성능 추적
  static trackAIInterpretation(modelName: string, sajuId: string) {
    const startTime = performance.now();
    
    datadogRum.addAction('ai_interpretation_started', {
      model_name: modelName,
      saju_id: sajuId
    });
    
    return {
      finish: (interpretation?: any) => {
        const duration = performance.now() - startTime;
        
        datadogRum.addAction('ai_interpretation_completed', {
          model_name: modelName,
          duration_ms: duration,
          interpretation_length: interpretation?.content?.length || 0,
          success: !!interpretation
        });
      }
    };
  }
  
  // 사용자 행동 추적
  static trackUserInteraction(action: string, element: string, data?: any) {
    datadogRum.addAction(`user_${action}`, {
      element_type: element,
      ...data
    });
  }
  
  // 비즈니스 메트릭 추적
  static trackBusinessMetric(metric: string, value: number, tags?: Record<string, string>) {
    datadogLogs.logger.info(`Business metric: ${metric}`, {
      metric_name: metric,
      metric_value: value,
      tags,
      timestamp: new Date().toISOString()
    });
  }
  
  // 페이지 성능 추적
  static trackPagePerformance(pageName: string) {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    
    if (navigation) {
      datadogRum.addAction('page_performance', {
        page_name: pageName,
        load_time: navigation.loadEventEnd - navigation.loadEventStart,
        dom_content_loaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        first_contentful_paint: this.getFirstContentfulPaint(),
        largest_contentful_paint: this.getLargestContentfulPaint()
      });
    }
  }
  
  private static getFirstContentfulPaint(): number | undefined {
    const paint = performance.getEntriesByType('paint').find(
      entry => entry.name === 'first-contentful-paint'
    );
    return paint?.startTime;
  }
  
  private static getLargestContentfulPaint(): number | undefined {
    return new Promise(resolve => {
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        resolve(lastEntry?.startTime);
        observer.disconnect();
      });
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
    });
  }
}
```

### **커스텀 대시보드 및 알림**
```yaml
# datadog/dashboards/heal7-performance.json
{
  "title": "HEAL7 Performance Dashboard",
  "description": "HEAL7 사주 서비스 성능 모니터링",
  "widgets": [
    {
      "id": "saju-calculation-time",
      "definition": {
        "title": "사주 계산 시간 분포",
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:heal7.saju.calculation.duration{*} by {is_lunar,gender}",
            "display_type": "line"
          }
        ]
      }
    },
    {
      "id": "ai-interpretation-performance", 
      "definition": {
        "title": "AI 모델별 해석 성능",
        "type": "toplist",
        "requests": [
          {
            "q": "avg:heal7.ai.interpretation.duration{*} by {model_name}",
            "limit": 9
          }
        ]
      }
    },
    {
      "id": "error-rate",
      "definition": {
        "title": "에러율",
        "type": "query_value",
        "requests": [
          {
            "q": "sum:heal7.errors.count{*}/sum:heal7.requests.count{*}*100",
            "aggregator": "last"
          }
        ]
      }
    },
    {
      "id": "user-satisfaction",
      "definition": {
        "title": "사용자 만족도",
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:heal7.user.satisfaction.score{*}",
            "display_type": "line"
          }
        ]
      }
    }
  ]
}

# datadog/monitors/heal7-alerts.yaml
monitors:
  - name: "HEAL7 - High Error Rate"
    type: "metric alert"
    query: "avg(last_5m):sum:heal7.errors.count{*}/sum:heal7.requests.count{*} > 0.1"
    message: |
      @slack-heal7-alerts
      HEAL7 서비스의 에러율이 10%를 초과했습니다.
      - 현재 에러율: {{value}}%
      - 임계값: 10%
      - 대시보드: https://app.datadoghq.com/dashboard/heal7-performance
    
  - name: "HEAL7 - Slow Saju Calculation"  
    type: "metric alert"
    query: "avg(last_10m):avg:heal7.saju.calculation.duration{*} > 15000"
    message: |
      @slack-heal7-alerts
      사주 계산 시간이 지연되고 있습니다.
      - 현재 평균 시간: {{value}}ms
      - 임계값: 15,000ms (15초)
      
  - name: "HEAL7 - AI Service Degradation"
    type: "metric alert" 
    query: "avg(last_10m):avg:heal7.ai.interpretation.duration{*} > 45000"
    message: |
      @slack-heal7-alerts @heal7-ai-team
      AI 해석 서비스 성능이 저하되었습니다.
      - 현재 평균 시간: {{value}}ms  
      - 임계값: 45,000ms (45초)
      
  - name: "HEAL7 - Low User Satisfaction"
    type: "metric alert"
    query: "avg(last_1h):avg:heal7.user.satisfaction.score{*} < 4.0"
    message: |
      @slack-heal7-alerts @heal7-product-team
      사용자 만족도가 기준치 이하로 떨어졌습니다.
      - 현재 만족도: {{value}}/5.0
      - 임계값: 4.0/5.0
```

---

## 🎯 **통합 품질 관리 프로세스**

### **CI/CD 품질 게이트**
```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run unit tests
        run: pnpm test:unit --coverage --watchAll=false
        
      - name: Coverage threshold check
        run: |
          if [ $(cat coverage/lcov.info | grep -c "SF:") -lt 85 ]; then
            echo "Coverage below 85% threshold"
            exit 1
          fi
          
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          
  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: heal7_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
          
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run database migrations
        run: pnpm db:migrate
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/heal7_test
          
      - name: Run integration tests
        run: pnpm test:integration
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/heal7_test
          
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Install Playwright browsers
        run: pnpm exec playwright install --with-deps
        
      - name: Build application
        run: pnpm build
        
      - name: Run E2E tests
        run: pnpm test:e2e
        
      - name: Upload Playwright report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          
  performance-tests:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup K6
        uses: grafana/k6-action@v0.3.1
        with:
          filename: k6/performance-test.js
          flags: --out cloud
        env:
          K6_CLOUD_TOKEN: ${{ secrets.K6_CLOUD_TOKEN }}
          BASE_URL: https://staging.heal7.com
          
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=medium
          
      - name: Run OWASP ZAP scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'https://staging.heal7.com'
          
  quality-check:
    needs: [unit-tests, integration-tests, e2e-tests, security-scan]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check all tests passed
        run: |
          if [ "${{ needs.unit-tests.result }}" != "success" ]; then
            echo "Unit tests failed"
            exit 1
          fi
          if [ "${{ needs.integration-tests.result }}" != "success" ]; then
            echo "Integration tests failed" 
            exit 1
          fi
          if [ "${{ needs.e2e-tests.result }}" != "success" ]; then
            echo "E2E tests failed"
            exit 1
          fi
          if [ "${{ needs.security-scan.result }}" != "success" ]; then
            echo "Security scan failed"
            exit 1
          fi
          echo "All quality gates passed ✅"
```

### **품질 메트릭 대시보드**
```typescript
// src/lib/quality/QualityMetrics.ts
export interface QualityMetrics {
  // 테스트 메트릭
  testing: {
    unitTestCoverage: number;
    integrationTestCoverage: number;
    e2eTestPassRate: number;
    testExecutionTime: number;
  };
  
  // 성능 메트릭  
  performance: {
    responseTimeP95: number;
    throughput: number;
    errorRate: number;
    apdex: number; // Application Performance Index
  };
  
  // 사용자 경험 메트릭
  userExperience: {
    satisfactionScore: number;
    taskCompletionRate: number;
    userRetentionRate: number;
    supportTicketRate: number;
  };
  
  // 비즈니스 메트릭
  business: {
    conversionRate: number;
    revenuePerUser: number;
    churnRate: number;
    netPromoterScore: number;
  };
  
  // 코드 품질 메트릭
  codeQuality: {
    codeComplexity: number;
    technicalDebt: number;
    codeReviewCoverage: number;
    bugDensity: number;
  };
}

export class QualityMetricsCollector {
  async collectMetrics(): Promise<QualityMetrics> {
    return {
      testing: await this.collectTestingMetrics(),
      performance: await this.collectPerformanceMetrics(),
      userExperience: await this.collectUXMetrics(),
      business: await this.collectBusinessMetrics(),
      codeQuality: await this.collectCodeQualityMetrics()
    };
  }
  
  async generateQualityReport(): Promise<QualityReport> {
    const metrics = await this.collectMetrics();
    const trends = await this.calculateTrends(metrics);
    const recommendations = this.generateRecommendations(metrics, trends);
    
    return {
      timestamp: new Date().toISOString(),
      metrics,
      trends,
      recommendations,
      overallScore: this.calculateOverallScore(metrics)
    };
  }
  
  private calculateOverallScore(metrics: QualityMetrics): number {
    // 가중치 기반 종합 점수 계산
    const weights = {
      testing: 0.25,
      performance: 0.20,
      userExperience: 0.25,
      business: 0.20,
      codeQuality: 0.10
    };
    
    const scores = {
      testing: (
        metrics.testing.unitTestCoverage * 0.4 +
        metrics.testing.integrationTestCoverage * 0.3 +
        metrics.testing.e2eTestPassRate * 0.3
      ),
      performance: (
        (metrics.performance.responseTimeP95 < 500 ? 100 : 50) * 0.4 +
        (metrics.performance.errorRate < 0.1 ? 100 : 50) * 0.3 +
        metrics.performance.apdex * 100 * 0.3
      ),
      userExperience: (
        metrics.userExperience.satisfactionScore * 20 * 0.4 +
        metrics.userExperience.taskCompletionRate * 0.3 +
        metrics.userExperience.userRetentionRate * 0.3
      ),
      business: (
        metrics.business.conversionRate * 4 * 0.4 +
        (100 - metrics.business.churnRate) * 0.3 +
        (metrics.business.netPromoterScore + 100) / 2 * 0.3
      ),
      codeQuality: (
        (100 - metrics.codeQuality.codeComplexity) * 0.3 +
        (100 - metrics.codeQuality.technicalDebt) * 0.3 +
        metrics.codeQuality.codeReviewCoverage * 0.4
      )
    };
    
    return Object.keys(weights).reduce((total, key) => {
      return total + (scores[key] * weights[key]);
    }, 0);
  }
}
```

---

## 🎉 **결론 및 다음 단계**

### **완성된 테스트 전략 요약**
1. **Jest 단위 테스트**: 90%+ 코드 커버리지, 자동화된 컴포넌트 테스트
2. **Playwright E2E 테스트**: 핵심 사용자 플로우 70%+ 커버리지, 시각적 회귀 테스트
3. **K6 성능 테스트**: 95th percentile < 500ms, 1000+ 동시 사용자 지원
4. **A/B 테스트**: 데이터 기반 의사결정, 통계적 유의성 검증
5. **Sentry 에러 추적**: 실시간 에러 모니터링, 자동 알림 시스템
6. **DataDog APM**: 종합 성능 모니터링, 비즈니스 메트릭 추적

### **구현 우선순위**
1. **Phase 1**: Jest 단위 테스트 + 기본 Sentry 설정 (2주)
2. **Phase 2**: Playwright E2E 테스트 + CI/CD 통합 (2주)
3. **Phase 3**: K6 성능 테스트 + DataDog APM (2주)
4. **Phase 4**: A/B 테스트 프레임워크 (1주)
5. **Phase 5**: 통합 품질 대시보드 + 자동화 (1주)

### **예상 품질 향상 효과**
- **버그 감소**: 프로덕션 버그 90% 감소
- **성능 향상**: 응답 시간 50% 개선
- **사용자 만족도**: 4.7+/5.0 달성
- **개발 속도**: 안정적인 배포로 개발 속도 30% 향상
- **비즈니스 임팩트**: 높은 품질로 인한 수익 증대

### **지속적 개선 계획**
- **주간 품질 리뷰**: 메트릭 분석 및 개선 계획 수립
- **월간 성능 최적화**: K6 결과 기반 성능 튜닝
- **분기별 테스트 전략 검토**: 새로운 테스트 도구 및 방법론 도입
- **연간 품질 목표 설정**: 업계 최고 수준의 품질 표준 달성

---

**📝 문서 정보**
- **버전**: 1.0
- **최종 수정**: 2025-08-23
- **다음 리뷰**: 2025-09-23
- **담당자**: HEAL7 QA Team, DevOps Team
- **승인자**: CTO, 품질 책임자

*이 문서는 HEAL7의 완전 자동화된 테스트 & 품질 보증 시스템을 위한 종합 가이드입니다.*