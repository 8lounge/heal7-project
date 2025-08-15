/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        // Healing & Nature Color Palette
        healing: {
          50: "#f8fafc",   // Slate 50
          100: "#f1f5f9",  // Slate 100
          200: "#e2e8f0",  // Slate 200
          300: "#cbd5e1",  // Slate 300
          400: "#94a3b8",  // Slate 400
          500: "#64748b",  // Slate 500 (Primary)
          600: "#475569",  // Slate 600 (Dark)
          700: "#334155",  // Slate 700 (Darker)
          800: "#1e293b",  // Slate 800 (Very Dark)
          900: "#0f172a",  // Slate 900 (Deepest)
        },
        earth: {
          50: "#fefdf9",   // Warm white
          100: "#fef7ed",  // Cream
          200: "#fed7aa",  // Light peach
          300: "#fdba74",  // Peach
          400: "#fb923c",  // Orange
          500: "#f97316",  // Primary orange
          600: "#ea580c",  // Dark orange
          700: "#c2410c",  // Darker orange
          800: "#9a3412",  // Very dark orange
          900: "#7c2d12",  // Deepest orange
        },
        sky: {
          50: "#f0f9ff",   // Very light blue
          100: "#e0f2fe",  // Light blue
          200: "#bae6fd",  // Soft blue
          300: "#7dd3fc",  // Medium blue
          400: "#38bdf8",  // Blue
          500: "#0ea5e9",  // Primary blue
          600: "#0284c7",  // Dark blue
          700: "#0369a1",  // Darker blue
          800: "#075985",  // Very dark blue
          900: "#0c4a6e",  // Deepest blue
        },
        lavender: {
          50: "#faf5ff",   // Very light purple
          100: "#f3e8ff",  // Light purple
          200: "#e9d5ff",  // Soft purple
          300: "#d8b4fe",  // Medium purple
          400: "#c084fc",  // Purple
          500: "#a855f7",  // Primary purple
          600: "#9333ea",  // Dark purple
          700: "#7c3aed",  // Darker purple
          800: "#6b21a8",  // Very dark purple
          900: "#581c87",  // Deepest purple
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0", transform: "translateY(10px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "scale-in": {
          from: { opacity: "0", transform: "scale(0.95)" },
          to: { opacity: "1", transform: "scale(1)" },
        },
        "slide-in-right": {
          from: { opacity: "0", transform: "translateX(20px)" },
          to: { opacity: "1", transform: "translateX(0)" },
        },
        "slide-in-left": {
          from: { opacity: "0", transform: "translateX(-20px)" },
          to: { opacity: "1", transform: "translateX(0)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
        "scale-in": "scale-in 0.2s ease-out",
        "slide-in-right": "slide-in-right 0.3s ease-out",
        "slide-in-left": "slide-in-left 0.3s ease-out",
      },
      fontFamily: {
        sans: ["Inter", "Noto Sans KR", "system-ui", "sans-serif"],
        serif: ["Crimson Text", "Noto Serif KR", "serif"],
        mono: ["JetBrains Mono", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
}