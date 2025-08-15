/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        // 사주 전용 색상
        saju: {
          wood: '#10b981', // 목 - 초록색
          fire: '#ef4444', // 화 - 빨간색
          earth: '#f59e0b', // 토 - 노란색
          metal: '#6b7280', // 금 - 회색
          water: '#3b82f6', // 수 - 파란색
          yang: '#fbbf24', // 양 - 밝은 노란색
          yin: '#6366f1', // 음 - 보라색
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
        // 한글 폰트
        korean: ['Noto Sans KR', 'Apple SD Gothic Neo', 'sans-serif'],
        // 한자 폰트
        chinese: ['Noto Sans CJK KR', 'serif'],
      },
      keyframes: {
        'accordion-down': {
          from: { height: 0 },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: 0 },
        },
        'fade-in': {
          '0%': { opacity: 0, transform: 'translateY(10px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        'saju-glow': {
          '0%, 100%': { 
            boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)' 
          },
          '50%': { 
            boxShadow: '0 0 20px rgba(59, 130, 246, 0.8)' 
          },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.5s ease-out',
        'slide-up': 'slide-up 0.3s ease-out',
        'saju-glow': 'saju-glow 2s ease-in-out infinite',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        // 사주 관련 그라디언트
        'saju-earth': 'linear-gradient(135deg, #f59e0b, #d97706)',
        'saju-water': 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        'saju-wood': 'linear-gradient(135deg, #10b981, #059669)',
        'saju-fire': 'linear-gradient(135deg, #ef4444, #dc2626)',
        'saju-metal': 'linear-gradient(135deg, #6b7280, #4b5563)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};