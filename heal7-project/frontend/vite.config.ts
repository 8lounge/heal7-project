import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, '.'),
      '@/components': resolve(__dirname, './components'),
      '@/lib': resolve(__dirname, './lib'),
      '@/stores': resolve(__dirname, './lib/stores'),
      '@/types': resolve(__dirname, './lib/types'),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    rollupOptions: {
      external: ['react-is'],
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['lucide-react', 'framer-motion']
        }
      }
    }
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true
  },
  preview: {
    host: true,
    port: 4173,
    strictPort: true
  }
})