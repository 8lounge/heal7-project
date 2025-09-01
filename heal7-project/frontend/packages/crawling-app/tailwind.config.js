/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // HEAL7 커스텀 컬러 팔레트
        cosmic: {
          50: '#f0f0ff',
          100: '#e5e5ff',
          200: '#d0d0ff',
          300: '#a6a6ff',
          400: '#7575ff',
          500: '#6366f1', // 기본 cosmic
          600: '#5248e3',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81'
        },
        mystic: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#8b5cf6', // 기본 mystic
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95'
        },
        fortune: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899', // 기본 fortune
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843'
        },
        energy: {
          50: '#ecfeff',
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#06b6d4', // 기본 energy
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63'
        },
        // 오행 컬러 시스템
        wood: '#22c55e',
        fire: '#ef4444',
        earth: '#f59e0b',
        metal: '#64748b',
        water: '#3b82f6',
        neon: '#00f5ff'
      },
      fontFamily: {
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        accent: ['Gmarket Sans', 'sans-serif'],
        mystical: ['Nanum Myeongjo', 'serif']
      },
      backgroundImage: {
        'cosmic-gradient': 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1))',
        'hologram': 'linear-gradient(45deg, #FF00FF, #00FFFF)',
        'crystal': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))'
      },
      backdropBlur: {
        xs: '2px'
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s infinite alternate',
        'hologram-scan': 'hologram-scan 3s infinite',
        'float': 'float 6s ease-in-out infinite',
        'rotate-slow': 'rotate-slow 20s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate'
      },
      keyframes: {
        'pulse-glow': {
          '0%': { boxShadow: '0 0 20px rgba(99, 102, 241, 0.5)' },
          '100%': { boxShadow: '0 0 30px rgba(139, 92, 246, 0.7)' }
        },
        'hologram-scan': {
          '0%': { backgroundPosition: '-100% 0' },
          '100%': { backgroundPosition: '100% 0' }
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        'rotate-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' }
        },
        'glow': {
          '0%': { textShadow: '0 0 10px currentColor' },
          '100%': { textShadow: '0 0 20px currentColor, 0 0 30px currentColor' }
        }
      },
      boxShadow: {
        'cosmic': '0 0 20px rgba(99, 102, 241, 0.5)',
        'mystic': '0 0 20px rgba(139, 92, 246, 0.5)',
        'fortune': '0 0 20px rgba(236, 72, 153, 0.5)',
        'neon': '0 0 20px #00f5ff',
        'inner-glow': 'inset 0 0 20px rgba(255, 255, 255, 0.1)'
      }
    },
  },
  plugins: [
    function({ addComponents }) {
      addComponents({
        '.card-glass': {
          '@apply backdrop-blur-sm bg-white/10 border border-white/20 rounded-xl shadow-xl': {}
        },
        '.card-cosmic': {
          '@apply bg-gradient-to-br from-indigo-900/50 via-purple-900/50 to-pink-900/50 backdrop-blur-sm border border-white/10 rounded-xl shadow-2xl': {}
        },
        '.card-crystal': {
          'background': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))',
          'backdrop-filter': 'blur(10px)',
          'border': '1px solid rgba(255, 255, 255, 0.2)',
          'border-radius': '12px',
          'box-shadow': '0 8px 32px 0 rgba(31, 38, 135, 0.37)'
        },
        '.btn-cosmic': {
          '@apply px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2': {}
        },
        '.btn-mystic': {
          '@apply px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-medium rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200': {}
        },
        '.btn-outline': {
          '@apply px-6 py-3 border-2 border-purple-500 text-purple-500 font-medium rounded-lg hover:bg-purple-500 hover:text-white transition-all duration-200': {}
        },
        '.text-cosmic': {
          'background': 'linear-gradient(45deg, #6366f1, #8b5cf6)',
          '-webkit-background-clip': 'text',
          '-webkit-text-fill-color': 'transparent',
          'background-clip': 'text'
        },
        '.text-mystic': {
          'background': 'linear-gradient(45deg, #8b5cf6, #ec4899)',
          '-webkit-background-clip': 'text',
          '-webkit-text-fill-color': 'transparent',
          'background-clip': 'text'
        },
        '.glow-effect': {
          'box-shadow': '0 0 20px rgba(99, 102, 241, 0.5)',
          'animation': 'pulse-glow 2s infinite alternate'
        },
        '.level-badge': {
          '@apply inline-flex items-center px-3 py-1 bg-gradient-to-r from-yellow-500 to-orange-500 text-white text-sm font-bold rounded-full shadow-lg': {}
        },
        '.progress-bar': {
          '@apply w-full bg-gray-700 rounded-full h-2 overflow-hidden': {}
        },
        '.progress-fill': {
          '@apply h-full bg-gradient-to-r from-green-500 to-blue-500 transition-all duration-500': {}
        }
      })
    }
  ],
}