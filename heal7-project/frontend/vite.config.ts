import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
// import { deployPlugin } from './vite-deploy-plugin.js'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react()
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@components": path.resolve(__dirname, "./src/components"),
      "@hooks": path.resolve(__dirname, "./src/hooks"),
      "@lib": path.resolve(__dirname, "./src/lib"),
      "@utils": path.resolve(__dirname, "./src/utils"),
      "@types": path.resolve(__dirname, "./src/types"),
      "@assets": path.resolve(__dirname, "./src/assets")
    }
  },
  server: {
    host: '0.0.0.0',
    port: 4173,
    proxy: {
      // 📄 Paperwork API → paperwork-service:8001
      '/api/paperwork': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/paperwork/, '')
      },
      // 🧪 Test API → test-service:8002
      '/api/test': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/test/, '')
      },
      // 🔮 사주 관련 API → saju-service:8003
      '/api/saju': {
        target: 'http://localhost:8003',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/saju/, '')
      },
      // 🕷️ 크롤링 API → crawling-service:8004
      '/api/crawling': {
        target: 'http://localhost:8004',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/crawling/, '/api')
      },
      // 📊 AI 모니터링 API → ai-monitoring-service:8005  
      '/api/ai-monitoring': {
        target: 'http://localhost:8005',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/ai-monitoring/, '')
      },
      // 🎼 관리자/대시보드 API → dashboard-service:8006
      '/api/admin': {
        target: 'http://localhost:8006',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/admin/, '')
      },
      // 🎼 기타 API → dashboard-service:8006 (오케스트레이션 허브)
      '/api/auth': {
        target: 'http://localhost:8004',
        changeOrigin: true,
        secure: false
      },
      '/api/admin/users': {
        target: 'http://localhost:8004',
        changeOrigin: true,
        secure: false
      },
      '/api': {
        target: 'http://localhost:8006',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    outDir: './dist',
    emptyOutDir: true,
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['framer-motion', 'zustand'],
          'three-vendor': ['three', '@react-three/fiber', '@react-three/drei']
        }
      }
    }
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'three', '@react-three/fiber']
  }
})