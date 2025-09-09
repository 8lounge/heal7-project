import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// 메모리 안전 최적화 빌드 설정
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
    // 메모리 극도 최적화
    chunkSizeWarningLimit: 500,
    minify: false, // 메모리 절약을 위해 minify 비활성화
    target: 'es2015',
    rollupOptions: {
      // Three.js 및 무거운 라이브러리 제외
      external: [
        'three',
        '@react-three/fiber',
        '@react-three/drei'
      ],
      output: {
        // 최소한의 청크 분할
        manualChunks: {
          'react-core': ['react', 'react-dom'],
          'utils': ['clsx', 'tailwind-merge']
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