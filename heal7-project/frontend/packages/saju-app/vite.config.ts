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
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          query: ['@tanstack/react-query'],
          motion: ['framer-motion'],
          three: ['three', '@react-three/fiber', '@react-three/drei'],
          'saju-admin': [
            './src/components/saju-admin/SajuAdminDashboard.tsx',
            './src/components/saju-admin/AdminLogin.tsx',
            './src/hooks/useSajuAdmin.ts',
            './src/types/sajuAdminTypes.ts',
            './src/utils/sajuAdminMockData.ts'
          ],
          'content-pages': [
            './src/components/magazine/Magazine.tsx',
            './src/components/consultation/Consultation.tsx',
            './src/components/store/Store.tsx',
            './src/components/notices/Notices.tsx'
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