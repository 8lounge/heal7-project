# 🛠️ HEAL7 크롤링 시스템 기술 스택 v2.0

> **완전 재현을 위한 기술 명세서**  
> **Node.js 24+, React 19 기반 최신 스택**  
> **프로덕션 검증 완료**

## 🏗️ 핵심 기술 스택

### Frontend Framework
```json
{
  "runtime": {
    "node": ">=24.0.0",
    "npm": ">=11.0.0",
    "react": "^19.1.1",
    "typescript": "^5.9.2"
  },
  "bundler": {
    "vite": "^7.1.3",
    "build_target": "ES2022",
    "bundle_splitting": "automatic"
  }
}
```

### UI/Animation Libraries
```json
{
  "styling": {
    "tailwindcss": "^3.4.17",
    "autoprefixer": "^10.4.21",
    "postcss": "^8.5.6"
  },
  "components": {
    "@radix-ui/react-dialog": "^1.1.15",
    "@radix-ui/react-label": "^2.1.7", 
    "@radix-ui/react-select": "^2.2.6",
    "@radix-ui/react-toast": "^1.2.15"
  },
  "animation": {
    "framer-motion": "^11.18.2"
  },
  "icons": {
    "lucide-react": "^0.542.0"
  }
}
```

### State & Data Management
```json
{
  "data_fetching": {
    "@tanstack/react-query": "^5.85.5"
  },
  "forms": {
    "react-hook-form": "^7.62.0",
    "@hookform/resolvers": "^5.2.1",
    "zod": "^4.1.5"
  },
  "global_state": {
    "zustand": "^5.0.8"
  }
}
```

### Interactive Features  
```json
{
  "drag_drop": {
    "@dnd-kit/core": "^6.3.1",
    "@dnd-kit/sortable": "^10.0.0", 
    "@dnd-kit/utilities": "^3.2.2"
  },
  "3d_graphics": {
    "@react-three/fiber": "^9.3.0",
    "@react-three/drei": "^10.7.4",
    "three": "^0.179.1",
    "@types/three": "^0.179.0"
  }
}
```

### Utility Libraries
```json
{
  "styling_utils": {
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1", 
    "tailwind-merge": "^3.3.1"
  }
}
```

### Development Tools
```json
{
  "linting": {
    "eslint": "^9.34.0",
    "@typescript-eslint/eslint-plugin": "^8.41.0",
    "@typescript-eslint/parser": "^8.41.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.20"
  },
  "testing": {
    "@playwright/test": "^1.55.0",
    "playwright": "^1.55.0"
  }
}
```

## ⚙️ 빌드 설정

### Vite 구성
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'es2022',
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', 'framer-motion', 'lucide-react'],
          'three-vendor': ['three', '@react-three/fiber', '@react-three/drei']
        }
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 4173
  }
})
```

### TypeScript 설정
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext", 
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Tailwind CSS 설정
```javascript
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Pretendard', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      animation: {
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin': 'spin 1s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate'
      }
    }
  },
  plugins: []
}
```

## 🔌 Backend Integration

### FastAPI 연결
```python
# Backend: 포트 8003
# API Routes:
#   /api/health - 헬스체크
#   /api/crawling/ - 크롤링 작업 관리  
#   /api/ai/ - AI 분석 요청
#   /api/data/ - 수집 데이터 관리
#   /ws - WebSocket 실시간 연결
```

### WebSocket 실시간 연결
```typescript
// useRealTime.ts에서 구현
const ws = new WebSocket(`ws://localhost:8003/ws`);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // 실시간 메트릭, 로그, 알림 업데이트
};
```

## 📦 의존성 보안 & 버전 관리

### 핵심 의존성 고정 버전
```json
{
  "critical_versions": {
    "react": "19.1.1",
    "typescript": "5.9.2",
    "vite": "7.1.3",
    "framer-motion": "11.18.2",
    "@tanstack/react-query": "5.85.5"
  }
}
```

### 보안 체크포인트
```bash
# 의존성 취약점 검사
npm audit
npm audit fix

# 최신 버전 확인  
npm outdated

# 라이센스 호환성 확인
npx license-checker
```

## 🚀 성능 최적화 설정

### React Query 최적화
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 15,    // 15분 캐시
      gcTime: 1000 * 60 * 30,       // 30분 메모리 보관
      refetchOnWindowFocus: false,   // 포커스 재요청 방지
      refetchOnMount: false,         // 마운트 재요청 방지
      retry: 0,                      // 재시도 비활성화
    }
  }
});
```

### Lazy Loading 설정
```typescript
// 3D 컴포넌트 지연 로딩
const OptimizedCyberCrystal = lazy(() => import('./components/3d/OptimizedCyberCrystal'));
const OptimizedStars = lazy(() => import('./components/3d/OptimizedStars'));

// Suspense 래핑
<Suspense fallback={<div>Loading...</div>}>
  <OptimizedCyberCrystal />
</Suspense>
```

### Bundle 최적화 결과
```
📦 빌드 결과:
├── index.html                    3.06 kB (gzip: 1.41 kB)
├── index-DH_h9EfE.css          97.63 kB (gzip: 13.75 kB)  
├── react-vendor-gH-7aFTg.js    11.83 kB (gzip: 4.20 kB)
├── ui-vendor-BPHf8l7b.js      114.99 kB (gzip: 38.14 kB)
├── three-vendor-C_PKb3mE.js   173.84 kB (gzip: 54.98 kB)
└── index-B58TcJW3.js          183.69 kB (gzip: 46.22 kB)

총 크기: ~582 kB (gzip 압축 후)
```

## 🔍 개발 환경 설정

### 필수 VS Code 확장
```json
{
  "recommendations": [
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next", 
    "esbenp.prettier-vscode",
    "ms-playwright.playwright",
    "formulahendry.auto-rename-tag"
  ]
}
```

### 환경 변수
```bash
# .env.local
VITE_API_BASE_URL=http://localhost:8003
VITE_WS_URL=ws://localhost:8003/ws  
VITE_AUTO_DEPLOY=false
VITE_DRY_RUN=false
```

## 🎯 호환성 매트릭스

### 브라우저 지원
```yaml
Chrome: ✅ 100+ (권장)
Firefox: ✅ 100+
Safari: ✅ 16+
Edge: ✅ 100+
IE: ❌ 지원 안함
```

### 디바이스 지원  
```yaml
Desktop: ✅ 1920x1080+ (최적화)
Tablet: ✅ 768px+ (반응형)
Mobile: ✅ 375px+ (축소 UI)
```

---

**🔧 설치 명령어 요약**:
```bash
npm install react@19.1.1 react-dom@19.1.1 typescript@5.9.2
npm install framer-motion @tanstack/react-query lucide-react
npm install @dnd-kit/core @dnd-kit/sortable tailwindcss
npm install @react-three/fiber @react-three/drei three
npm install @radix-ui/react-dialog @radix-ui/react-toast
```

**⚡ 핵심 성능**: 빌드 37초, 번들 크기 582KB, 초기 로딩 2초 이내