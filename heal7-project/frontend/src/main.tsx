import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import CrawlingApp from './CrawlingApp'
import './index.css'

// 환경변수 기반 앱 선택 (Phase 0: 긴급 안정화)
const APP_TYPE = import.meta.env.VITE_APP_TYPE || 'saju'
const AppComponent = APP_TYPE === 'crawling' ? CrawlingApp : App

console.log(`🚀 Loading ${APP_TYPE} app...`)

// React Query 설정 - 서버 로드 최적화
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 15, // 15분 (캐시 유지 시간 연장)
      gcTime: 1000 * 60 * 30, // 30분 (메모리 캐시 시간) - React Query v5에서는 cacheTime → gcTime
      refetchOnWindowFocus: false, // 윈도우 포커스 시 재요청 방지
      refetchOnMount: false, // 컴포넌트 마운트 시 재요청 방지
      refetchOnReconnect: false, // 네트워크 재연결 시 재요청 방지
      retry: 0, // 재시도 비활성화 (서버 로드 최소화)
      retryOnMount: false // 마운트 시 재시도 방지
    }
  }
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AppComponent />
    </QueryClientProvider>
  </React.StrictMode>,
)