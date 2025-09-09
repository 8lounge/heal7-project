import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@shared': resolve(__dirname, '../shared/src')
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // 메모리 최적화 설정
    chunkSizeWarningLimit: 1000,
    minify: 'esbuild', // terser 대신 esbuild 사용 (더 빠르고 메모리 효율적)
    target: 'es2015',
    rollupOptions: {
      output: {
        manualChunks: {
          // 핵심 라이브러리
          'react-core': ['react', 'react-dom'],
          'react-utils': ['@tanstack/react-query', 'framer-motion'],
          // 3D 관련 (큰 라이브러리)
          'three-js': ['three', '@react-three/fiber', '@react-three/drei'],
          // 관리자 시스템 (지연 로딩)
          'admin-system': [
            './src/components/saju-admin/SajuAdminDashboard.tsx',
            './src/components/saju-admin/AdminLogin.tsx',
            './src/hooks/useSajuAdmin.ts',
            './src/types/sajuAdminTypes.ts',
            './src/utils/sajuAdminMockData.ts'
          ],
          // 콘텐츠 페이지들
          'content-pages': [
            './src/components/magazine/Magazine.tsx',
            './src/components/consultation/Consultation.tsx',
            './src/components/store/Store.tsx',
            './src/components/notices/Notices.tsx'
          ],
          // 사주 관련 핵심 기능
          'saju-core': [
            './src/components/fortune/SajuCalculator.tsx',
            './src/components/fortune/DreamInterpretation.tsx',
            './src/components/fortune/FortuneCalendar.tsx'
          ]
        }
      }
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api/auth': 'http://127.0.0.1:8002',
      '/api/saju': 'http://127.0.0.1:8002',
      '/api': 'http://127.0.0.1:8005'
    }
  }
})