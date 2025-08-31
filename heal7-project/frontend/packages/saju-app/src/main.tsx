import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import './index.css'

// React Query 설정 - 서버 로드 최적화
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 15, // 15분 (캐시 유지 시간 연장)
      gcTime: 1000 * 60 * 30, // 30분 (메모리 캐시 시간)
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
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)