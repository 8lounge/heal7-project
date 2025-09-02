/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cosmic: {
          50: '#f0f0ff',
          100: '#e5e5ff',
          200: '#d0d0ff',
          300: '#a6a6ff',
          400: '#7575ff',
          500: '#6366f1',
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
          500: '#8b5cf6',
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
          500: '#ec4899',
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
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63'
        },
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
      animation: {
        'pulse-glow': 'pulse-glow 2s infinite alternate',
        'hologram-scan': 'hologram-scan 3s infinite',
        'float': 'float 6s ease-in-out infinite',
        'rotate-slow': 'rotate-slow 20s linear infinite'
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
  plugins: [],
}