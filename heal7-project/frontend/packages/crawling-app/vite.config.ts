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
          socket: ['socket.io-client'],
          motion: ['framer-motion']
        }
      }
    }
  },
  server: {
    port: 5174,
    proxy: {
      '/api': 'http://127.0.0.1:8003',
      '/ws': {
        target: 'ws://127.0.0.1:8003',
        ws: true
      }
    }
  }
})