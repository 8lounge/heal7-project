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
  server: {
    port: 5176,
    proxy: {
      '/api': 'http://127.0.0.1:8000'
    }
  }
})