# 🌌 HEAL7 신비+판타지+SF 퓨전 디자인 언어 v1.0

> **브랜드 철학**: "당신의 마음을 치유한다" - 우주적 치유의 경험  
> **디자인 정신**: 신비로운 동양 사상 + 판타지 모험 + SF 미래 기술  
> **최종 업데이트**: 2025-08-23

## 🎨 **디자인 세계관**

### **🌟 브랜드 유니버스**
```
🔮 신비 (Mystic)     → 동양 명리학, 우주의 신비, 고대 지혜
🏰 판타지 (Fantasy)   → 마법적 경험, 모험, 꿈과 희망
🚀 SF (Sci-Fi)       → 미래 기술, AI, 홀로그램, 사이버 공간
                            ↓
                    🌈 퓨전 (Fusion)
              "우주적 치유의 경험" (Cosmic Healing Experience)
```

### **🎭 감성적 톤 & 무드**

| 감성 영역 | 키워드 | 색상 팔레트 | 시각적 언어 |
|----------|-------|------------|------------|
| **🔮 신비** | 깊이, 통찰, 지혜, 평온 | 보라, 인디고, 금색 | 원형, 나선, 만다라 |
| **🏰 판타지** | 모험, 마법, 꿈, 희망 | 에메랄드, 사파이어, 은색 | 크리스탈, 룬, 별자리 |
| **🚀 SF** | 미래, 기술, 정밀, 혁신 | 네온, 사이버, 홀로그램 | 그리드, 회로, 광선 |

## 🎨 **네뷸라 컬러 시스템**

### **🌌 프라이머리 컬러 팔레트**

```css
/* 🌟 네뷸라 프라이머리 (Nebula Primary) */
:root {
  /* 신비 네뷸라 (Mystic Nebula) */
  --mystic-deep-violet: #4A0E8F;      /* 깊은 보라 - 우주의 신비 */
  --mystic-amethyst: #7B2CBF;         /* 자수정 - 영적 통찰 */
  --mystic-aurora: #C77DFF;           /* 오로라 - 신성한 빛 */
  --mystic-gold: #FFD700;             /* 황금 - 고대의 지혜 */
  
  /* 판타지 네뷸라 (Fantasy Nebula) */
  --fantasy-emerald: #059669;         /* 에메랄드 - 치유의 숲 */
  --fantasy-sapphire: #1E40AF;        /* 사파이어 - 모험의 바다 */
  --fantasy-crystal: #A5B4FC;         /* 크리스탈 - 마법의 빛 */
  --fantasy-silver: #E5E7EB;          /* 은빛 - 달의 축복 */
  
  /* SF 네뷸라 (Sci-Fi Nebula) */
  --sf-neon-blue: #00D9FF;           /* 네온 블루 - 사이버 공간 */
  --sf-hologram: #8B5CF6;            /* 홀로그램 - 미래 기술 */
  --sf-plasma: #F59E0B;              /* 플라즈마 - 에너지 */
  --sf-quantum: #EC4899;             /* 퀀텀 - 차원의 문 */
}

/* 🎨 세컨더리 컬러 팔레트 */
:root {
  /* 치유 그라데이션 (Healing Gradients) */
  --healing-sunset: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --healing-ocean: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  --healing-cosmos: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #43e97b 100%);
  --healing-aurora: linear-gradient(135deg, #fa709a 0%, #fee140 50%, #43e97b 100%);
  
  /* 네뷸라 그라데이션 (Nebula Gradients) */
  --nebula-mystic: radial-gradient(circle, #4A0E8F 0%, #7B2CBF 50%, #C77DFF 100%);
  --nebula-fantasy: radial-gradient(circle, #059669 0%, #1E40AF 50%, #A5B4FC 100%);
  --nebula-scifi: radial-gradient(circle, #00D9FF 0%, #8B5CF6 50%, #EC4899 100%);
}

/* 🌙 다크모드 최적화 */
[data-theme="dark"] {
  --mystic-deep-violet: #6B46C1;
  --mystic-amethyst: #9333EA;
  --fantasy-emerald: #10B981;
  --fantasy-sapphire: #3B82F6;
  --sf-neon-blue: #06B6D4;
  --sf-hologram: #A855F7;
}
```

### **🎨 컬러 사용 가이드라인**

```tsx
// components/ColorSystem.tsx - 컬러 시스템 컴포넌트
export const ColorSystem = {
  // 🌟 브랜드 컬러 (Brand Colors)
  brand: {
    primary: 'var(--mystic-amethyst)',    // 메인 브랜드 컬러
    secondary: 'var(--fantasy-sapphire)', // 보조 브랜드 컬러
    accent: 'var(--sf-neon-blue)',        // 강조 컬러
  },
  
  // 🎯 기능별 컬러 (Functional Colors)
  functional: {
    success: 'var(--fantasy-emerald)',    // 성공 상태
    warning: 'var(--sf-plasma)',          // 경고 상태
    error: 'var(--sf-quantum)',           // 오류 상태
    info: 'var(--fantasy-crystal)',       // 정보 상태
  },
  
  // 🎨 UI 컬러 (Interface Colors)
  ui: {
    background: {
      primary: '#0F0F23',                 // 우주 배경
      secondary: '#1A1A2E',              // 카드 배경
      elevated: '#16213E',               // 상승 배경
    },
    text: {
      primary: '#FFFFFF',                 // 주 텍스트
      secondary: 'var(--fantasy-silver)', // 보조 텍스트
      muted: '#9CA3AF',                  // 비활성 텍스트
    },
    border: {
      default: 'var(--mystic-aurora)',    // 기본 테두리
      focus: 'var(--sf-neon-blue)',       // 포커스 테두리
      hover: 'var(--fantasy-crystal)',    // 호버 테두리
    }
  },
  
  // 🌈 그라데이션 매트릭스 (Gradient Matrix)
  gradients: {
    mystic: 'var(--nebula-mystic)',       // 신비로운 배경
    fantasy: 'var(--nebula-fantasy)',     // 판타지 배경
    scifi: 'var(--nebula-scifi)',         // SF 배경
    healing: 'var(--healing-cosmos)',     // 치유 배경
  }
};

// 🎨 컬러 유틸리티 함수
export const colorUtils = {
  // 투명도 적용
  alpha: (color: string, opacity: number) => `${color}${Math.round(opacity * 255).toString(16)}`,
  
  // 컬러 믹싱
  mix: (color1: string, color2: string, ratio: number) => {
    // CSS color-mix 함수 활용
    return `color-mix(in srgb, ${color1} ${ratio * 100}%, ${color2})`;
  },
  
  // 동적 컬러 생성
  generateNebulaColor: (hue: number, saturation: number, lightness: number) => {
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  }
};
```

## ✨ **홀로그램 UI 시스템**

### **🔮 홀로그램 효과 라이브러리**

```css
/* 🌟 홀로그램 베이스 효과 */
.hologram-base {
  position: relative;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
  background-size: 20px 20px;
  animation: hologram-scan 3s ease-in-out infinite;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.2);
}

.hologram-base::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 217, 255, 0.3),
    transparent
  );
  animation: hologram-sweep 2s ease-in-out infinite;
}

.hologram-base::after {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0, 217, 255, 0.03) 2px,
      rgba(0, 217, 255, 0.03) 4px
    );
  pointer-events: none;
}

@keyframes hologram-scan {
  0%, 100% { background-position: 0 0; }
  50% { background-position: 40px 40px; }
}

@keyframes hologram-sweep {
  0% { left: -100%; opacity: 0; }
  50% { opacity: 1; }
  100% { left: 100%; opacity: 0; }
}

/* 🎨 홀로그램 컴포넌트 변형 */

/* 1️⃣ 홀로그램 카드 */
.hologram-card {
  @apply hologram-base;
  background: radial-gradient(
    circle at center,
    rgba(123, 44, 191, 0.1) 0%,
    rgba(74, 14, 143, 0.05) 50%,
    transparent 100%
  );
  box-shadow: 
    0 0 20px rgba(123, 44, 191, 0.3),
    inset 0 0 20px rgba(0, 217, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.hologram-card:hover {
  box-shadow: 
    0 0 40px rgba(123, 44, 191, 0.5),
    inset 0 0 30px rgba(0, 217, 255, 0.2);
  transform: translateY(-4px) scale(1.02);
}

/* 2️⃣ 홀로그램 버튼 */
.hologram-button {
  @apply hologram-base;
  padding: 12px 24px;
  background: linear-gradient(
    135deg,
    rgba(0, 217, 255, 0.2) 0%,
    rgba(139, 92, 246, 0.2) 50%,
    rgba(236, 72, 153, 0.2) 100%
  );
  border-radius: 8px;
  font-family: 'Orbitron', monospace;
  font-weight: 600;
  color: #FFFFFF;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  overflow: hidden;
}

.hologram-button:hover {
  background: linear-gradient(
    135deg,
    rgba(0, 217, 255, 0.4) 0%,
    rgba(139, 92, 246, 0.4) 50%,
    rgba(236, 72, 153, 0.4) 100%
  );
}

.hologram-button:active {
  transform: scale(0.98);
  box-shadow: inset 0 0 20px rgba(0, 217, 255, 0.5);
}

/* 3️⃣ 홀로그램 인풋 */
.hologram-input {
  @apply hologram-base;
  padding: 16px;
  background: rgba(26, 26, 46, 0.8);
  border-radius: 12px;
  color: #FFFFFF;
  font-family: 'Space Mono', monospace;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
}

.hologram-input:focus {
  border-color: var(--sf-neon-blue);
  box-shadow: 
    0 0 20px rgba(0, 217, 255, 0.4),
    inset 0 0 10px rgba(0, 217, 255, 0.1);
}

.hologram-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
  font-style: italic;
}

/* 4️⃣ 홀로그램 패널 */
.hologram-panel {
  @apply hologram-base;
  padding: 32px;
  border-radius: 16px;
  background: 
    radial-gradient(circle at top left, rgba(74, 14, 143, 0.1) 0%, transparent 50%),
    radial-gradient(circle at bottom right, rgba(0, 217, 255, 0.1) 0%, transparent 50%),
    rgba(15, 15, 35, 0.9);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}
```

### **🎮 인터랙티브 홀로그램 컴포넌트**

```tsx
// components/HologramUI.tsx - 홀로그램 UI 컴포넌트
import React, { useState, useRef, useEffect } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';

interface HologramCardProps {
  children: React.ReactNode;
  glowColor?: string;
  intensity?: number;
}

export const HologramCard: React.FC<HologramCardProps> = ({ 
  children, 
  glowColor = '#00D9FF',
  intensity = 0.3 
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  
  const rotateX = useSpring(mouseY, { stiffness: 300, damping: 30 });
  const rotateY = useSpring(mouseX, { stiffness: 300, damping: 30 });
  
  const handleMouseMove = (e: React.MouseEvent) => {
    if (!cardRef.current) return;
    
    const rect = cardRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const rotateXValue = (e.clientY - centerY) / (rect.height / 2) * -10;
    const rotateYValue = (e.clientX - centerX) / (rect.width / 2) * 10;
    
    mouseX.set(rotateYValue);
    mouseY.set(rotateXValue);
  };
  
  const handleMouseLeave = () => {
    mouseX.set(0);
    mouseY.set(0);
  };
  
  return (
    <motion.div
      ref={cardRef}
      className="hologram-card"
      style={{
        rotateX,
        rotateY,
        transformStyle: 'preserve-3d',
        '--glow-color': glowColor,
        '--intensity': intensity,
      } as React.CSSProperties}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
    >
      {children}
      
      {/* 홀로그램 파티클 효과 */}
      <HologramParticles color={glowColor} intensity={intensity} />
    </motion.div>
  );
};

// 🌟 홀로그램 파티클 시스템
const HologramParticles: React.FC<{ color: string; intensity: number }> = ({ 
  color, 
  intensity 
}) => {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {Array.from({ length: 20 }).map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 rounded-full opacity-70"
          style={{
            backgroundColor: color,
            boxShadow: `0 0 4px ${color}`,
          }}
          animate={{
            x: [0, Math.random() * 200 - 100],
            y: [0, Math.random() * 200 - 100],
            opacity: [0, intensity, 0],
            scale: [0, 1, 0],
          }}
          transition={{
            duration: 3 + Math.random() * 2,
            repeat: Infinity,
            delay: Math.random() * 2,
            ease: 'easeInOut',
          }}
          initial={{
            x: Math.random() * 100 - 50,
            y: Math.random() * 100 - 50,
          }}
        />
      ))}
    </div>
  );
};

// 🔮 홀로그램 텍스트 효과
export const HologramText: React.FC<{ 
  children: string;
  className?: string;
}> = ({ children, className = '' }) => {
  return (
    <div className={`hologram-text ${className}`}>
      <span className="hologram-text-main">{children}</span>
      <span className="hologram-text-glow" aria-hidden="true">{children}</span>
      <span className="hologram-text-shadow" aria-hidden="true">{children}</span>
    </div>
  );
};
```

## 🌠 **파티클 효과 시스템**

### **✨ 파티클 애니메이션 엔진**

```css
/* 🌟 파티클 베이스 시스템 */
.particle-system {
  position: relative;
  overflow: hidden;
}

.particle-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

/* 🎨 파티클 타입별 애니메이션 */

/* 1️⃣ 별빛 파티클 (Starlight Particles) */
@keyframes starlight-twinkle {
  0%, 100% { 
    opacity: 0.3; 
    transform: scale(0.8) rotate(0deg); 
  }
  50% { 
    opacity: 1; 
    transform: scale(1.2) rotate(180deg); 
  }
}

.particle-starlight {
  position: absolute;
  width: 4px;
  height: 4px;
  background: radial-gradient(circle, #FFD700 0%, transparent 70%);
  border-radius: 50%;
  animation: starlight-twinkle 3s ease-in-out infinite;
}

.particle-starlight::before,
.particle-starlight::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 1px;
  background: linear-gradient(90deg, transparent, #FFD700, transparent);
  transform: translate(-50%, -50%);
}

.particle-starlight::after {
  transform: translate(-50%, -50%) rotate(90deg);
}

/* 2️⃣ 오브 파티클 (Energy Orbs) */
@keyframes orb-float {
  0%, 100% { 
    transform: translateY(0) scale(1); 
    opacity: 0.6; 
  }
  25% { 
    transform: translateY(-20px) scale(1.1); 
    opacity: 0.8; 
  }
  50% { 
    transform: translateY(-10px) scale(0.9); 
    opacity: 1; 
  }
  75% { 
    transform: translateY(-30px) scale(1.05); 
    opacity: 0.7; 
  }
}

.particle-orb {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(0, 217, 255, 0.8) 0%,
    rgba(139, 92, 246, 0.6) 50%,
    transparent 100%
  );
  box-shadow: 
    0 0 10px rgba(0, 217, 255, 0.6),
    inset 0 0 10px rgba(255, 255, 255, 0.3);
  animation: orb-float 4s ease-in-out infinite;
}

/* 3️⃣ 네뷸라 먼지 (Nebula Dust) */
@keyframes nebula-drift {
  0% { 
    transform: translateX(-100px) translateY(0) rotate(0deg);
    opacity: 0;
  }
  10%, 90% { 
    opacity: 0.4;
  }
  100% { 
    transform: translateX(calc(100vw + 100px)) translateY(-50px) rotate(360deg);
    opacity: 0;
  }
}

.particle-nebula {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(199, 125, 255, 0.6);
  border-radius: 50%;
  animation: nebula-drift 8s linear infinite;
  filter: blur(1px);
}

/* 4️⃣ 에너지 스트림 (Energy Streams) */
@keyframes energy-stream {
  0% {
    transform: translateX(-20px) scaleX(0);
    opacity: 0;
  }
  20% {
    opacity: 1;
    transform: translateX(0) scaleX(1);
  }
  80% {
    opacity: 1;
    transform: translateX(80px) scaleX(1);
  }
  100% {
    transform: translateX(100px) scaleX(0);
    opacity: 0;
  }
}

.particle-stream {
  position: absolute;
  width: 40px;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(0, 217, 255, 0.8) 50%,
    transparent 100%
  );
  animation: energy-stream 2s ease-in-out infinite;
  filter: blur(0.5px);
}
```

### **🎬 파티클 시스템 React 컴포넌트**

```tsx
// components/ParticleSystem.tsx - 파티클 시스템
import React, { useEffect, useRef, useState } from 'react';

interface ParticleSystemProps {
  type: 'starlight' | 'orbs' | 'nebula' | 'streams';
  density?: number;
  color?: string;
  speed?: number;
  className?: string;
}

export const ParticleSystem: React.FC<ParticleSystemProps> = ({
  type,
  density = 50,
  color = '#00D9FF',
  speed = 1,
  className = '',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [particles, setParticles] = useState<Array<{
    id: number;
    x: number;
    y: number;
    delay: number;
    size: number;
  }>>([]);

  useEffect(() => {
    const generateParticles = () => {
      const newParticles = Array.from({ length: density }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        delay: Math.random() * 5,
        size: 0.5 + Math.random() * 1.5,
      }));
      setParticles(newParticles);
    };

    generateParticles();
  }, [density]);

  const getParticleClass = () => {
    switch (type) {
      case 'starlight': return 'particle-starlight';
      case 'orbs': return 'particle-orb';
      case 'nebula': return 'particle-nebula';
      case 'streams': return 'particle-stream';
      default: return 'particle-starlight';
    }
  };

  return (
    <div 
      ref={containerRef}
      className={`particle-system ${className}`}
    >
      <div className="particle-container">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className={getParticleClass()}
            style={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              animationDelay: `${particle.delay}s`,
              animationDuration: `${3 / speed}s`,
              transform: `scale(${particle.size})`,
              '--particle-color': color,
            } as React.CSSProperties}
          />
        ))}
      </div>
    </div>
  );
};

// 🌌 배경 네뷸라 컴포넌트
export const NebulaBackground: React.FC<{ 
  variant?: 'mystic' | 'fantasy' | 'scifi';
}> = ({ variant = 'mystic' }) => {
  const getNebulaGradient = () => {
    switch (variant) {
      case 'mystic':
        return 'radial-gradient(ellipse at center, rgba(74, 14, 143, 0.3) 0%, rgba(123, 44, 191, 0.1) 50%, transparent 100%)';
      case 'fantasy':
        return 'radial-gradient(ellipse at center, rgba(5, 150, 105, 0.3) 0%, rgba(30, 64, 175, 0.1) 50%, transparent 100%)';
      case 'scifi':
        return 'radial-gradient(ellipse at center, rgba(0, 217, 255, 0.3) 0%, rgba(139, 92, 246, 0.1) 50%, transparent 100%)';
      default:
        return 'radial-gradient(ellipse at center, rgba(74, 14, 143, 0.3) 0%, transparent 100%)';
    }
  };

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* 메인 네뷸라 배경 */}
      <div 
        className="absolute inset-0"
        style={{ background: getNebulaGradient() }}
      />
      
      {/* 파티클 레이어들 */}
      <ParticleSystem type="starlight" density={30} speed={0.5} />
      <ParticleSystem type="nebula" density={20} speed={0.3} />
      <ParticleSystem type="orbs" density={10} speed={0.8} />
      
      {/* 추가 네뷸라 레이어 */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 opacity-20">
        <div 
          className="w-full h-full rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(199, 125, 255, 0.4) 0%, transparent 70%)',
            filter: 'blur(40px)',
          }}
        />
      </div>
      
      <div className="absolute bottom-1/4 right-1/4 w-64 h-64 opacity-15">
        <div 
          className="w-full h-full rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(0, 217, 255, 0.4) 0%, transparent 70%)',
            filter: 'blur(30px)',
          }}
        />
      </div>
    </div>
  );
};
```

## 🌌 **우주적 타이포그래피**

### **📝 폰트 시스템**

```css
/* 🌟 우주적 폰트 임포트 */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,300;0,400;0,600;0,800;1,300;1,400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

/* 🎨 폰트 패밀리 정의 */
:root {
  /* 메인 브랜드 폰트 */
  --font-brand: 'Orbitron', 'Noto Sans KR', sans-serif;
  
  /* UI 시스템 폰트 */
  --font-ui: 'Exo 2', 'Noto Sans KR', sans-serif;
  
  /* 코드/데이터 폰트 */
  --font-mono: 'Space Mono', 'Noto Sans KR', monospace;
  
  /* 본문 폰트 */
  --font-body: 'Noto Sans KR', -apple-system, system-ui, sans-serif;
}

/* 🌟 타이포그래피 스케일 시스템 */
.text-scale {
  /* 🎯 헤드라인 (Headlines) */
  --text-hero: clamp(3rem, 8vw, 6rem);        /* 48px → 96px */
  --text-h1: clamp(2.5rem, 6vw, 4rem);        /* 40px → 64px */
  --text-h2: clamp(2rem, 5vw, 3rem);          /* 32px → 48px */
  --text-h3: clamp(1.5rem, 4vw, 2.25rem);     /* 24px → 36px */
  --text-h4: clamp(1.25rem, 3vw, 1.875rem);   /* 20px → 30px */
  --text-h5: clamp(1.125rem, 2.5vw, 1.5rem);  /* 18px → 24px */
  --text-h6: clamp(1rem, 2vw, 1.25rem);       /* 16px → 20px */
  
  /* 📝 본문 (Body Text) */
  --text-lg: clamp(1.125rem, 2vw, 1.25rem);   /* 18px → 20px */
  --text-base: clamp(1rem, 1.5vw, 1.125rem);  /* 16px → 18px */
  --text-sm: clamp(0.875rem, 1.2vw, 1rem);    /* 14px → 16px */
  --text-xs: clamp(0.75rem, 1vw, 0.875rem);   /* 12px → 14px */
  
  /* 🎨 디스플레이 (Display) */
  --text-display: clamp(4rem, 10vw, 8rem);    /* 64px → 128px */
}

/* 🎭 브랜드 타이포그래피 클래스 */
.typography-hero {
  font-family: var(--font-brand);
  font-size: var(--text-hero);
  font-weight: 900;
  line-height: 0.9;
  letter-spacing: -0.02em;
  background: linear-gradient(
    135deg,
    var(--mystic-gold) 0%,
    var(--mystic-aurora) 50%,
    var(--sf-neon-blue) 100%
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
}

.typography-display {
  font-family: var(--font-brand);
  font-size: var(--text-display);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.015em;
  background: var(--healing-cosmos);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 
    0 0 20px rgba(123, 44, 191, 0.5),
    0 0 40px rgba(0, 217, 255, 0.3);
}

.typography-heading {
  font-family: var(--font-ui);
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.01em;
  color: #FFFFFF;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.typography-body {
  font-family: var(--font-body);
  font-weight: 400;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
}

.typography-mono {
  font-family: var(--font-mono);
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.025em;
  color: var(--sf-neon-blue);
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(0, 217, 255, 0.3);
}

/* ✨ 홀로그램 텍스트 효과 */
.hologram-text {
  position: relative;
  display: inline-block;
  font-family: var(--font-brand);
}

.hologram-text-main {
  position: relative;
  z-index: 3;
  color: #FFFFFF;
  text-shadow: 0 0 10px rgba(0, 217, 255, 0.8);
}

.hologram-text-glow {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 2;
  color: var(--sf-neon-blue);
  opacity: 0.7;
  filter: blur(2px);
  animation: hologram-flicker 3s ease-in-out infinite;
}

.hologram-text-shadow {
  position: absolute;
  top: 2px;
  left: 2px;
  z-index: 1;
  color: var(--mystic-amethyst);
  opacity: 0.5;
  filter: blur(4px);
}

@keyframes hologram-flicker {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 0.3; }
  75% { opacity: 0.9; }
}

/* 🌟 글리치 텍스트 효과 */
.glitch-text {
  position: relative;
  font-family: var(--font-brand);
  color: #FFFFFF;
  animation: glitch-color 2s ease-in-out infinite;
}

.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch-text::before {
  color: var(--sf-quantum);
  animation: glitch-1 0.3s ease-in-out infinite;
  z-index: -1;
}

.glitch-text::after {
  color: var(--sf-neon-blue);
  animation: glitch-2 0.3s ease-in-out infinite;
  z-index: -2;
}

@keyframes glitch-1 {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
}

@keyframes glitch-2 {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(2px, 0); }
  40% { transform: translate(-2px, 0); }
  60% { transform: translate(0, 2px); }
  80% { transform: translate(0, -2px); }
}

@keyframes glitch-color {
  0%, 100% { filter: hue-rotate(0deg); }
  50% { filter: hue-rotate(90deg); }
}
```

### **📱 반응형 타이포그래피**

```tsx
// components/Typography.tsx - 타이포그래피 컴포넌트
import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const typographyVariants = cva('', {
  variants: {
    variant: {
      hero: 'typography-hero',
      display: 'typography-display', 
      h1: 'typography-heading text-h1',
      h2: 'typography-heading text-h2',
      h3: 'typography-heading text-h3',
      h4: 'typography-heading text-h4',
      h5: 'typography-heading text-h5',
      h6: 'typography-heading text-h6',
      body: 'typography-body text-base',
      large: 'typography-body text-lg',
      small: 'typography-body text-sm',
      mono: 'typography-mono text-sm',
    },
    effect: {
      none: '',
      hologram: 'hologram-text',
      glitch: 'glitch-text',
      glow: 'text-shadow-glow',
    },
    align: {
      left: 'text-left',
      center: 'text-center',
      right: 'text-right',
      justify: 'text-justify',
    },
  },
  defaultVariants: {
    variant: 'body',
    effect: 'none',
    align: 'left',
  },
});

interface TypographyProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof typographyVariants> {
  as?: keyof JSX.IntrinsicElements;
  glitchText?: string;
}

export const Typography: React.FC<TypographyProps> = ({
  className,
  variant,
  effect,
  align,
  as: Component = 'p',
  children,
  glitchText,
  ...props
}) => {
  const classes = cn(
    typographyVariants({ variant, effect, align }),
    className
  );

  const glitchProps = effect === 'glitch' ? { 'data-text': glitchText || children } : {};

  return (
    <Component className={classes} {...glitchProps} {...props}>
      {children}
    </Component>
  );
};

// 🎯 미리 정의된 타이포그래피 컴포넌트들
export const HeroText: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Typography variant="hero" effect="hologram" align="center" as="h1">
    {children}
  </Typography>
);

export const DisplayText: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Typography variant="display" effect="glow" align="center" as="h2">
    {children}
  </Typography>
);

export const GlitchTitle: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Typography 
    variant="h2" 
    effect="glitch" 
    glitchText={children?.toString()} 
    as="h2"
  >
    {children}
  </Typography>
);

// 📏 반응형 텍스트 스케일링 유틸리티
export const useResponsiveText = (baseSize: number) => {
  const [fontSize, setFontSize] = React.useState(baseSize);
  
  React.useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      let scale = 1;
      
      if (width < 640) {          // mobile
        scale = 0.8;
      } else if (width < 1024) {  // tablet
        scale = 0.9;
      } else if (width > 1440) {  // desktop large
        scale = 1.1;
      }
      
      setFontSize(baseSize * scale);
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    
    return () => window.removeEventListener('resize', handleResize);
  }, [baseSize]);
  
  return fontSize;
};
```

## 🎮 **인터랙션 & 애니메이션**

### **✨ 마이크로 인터랙션**

```css
/* 🌟 버튼 호버 효과 */
.btn-cosmic {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--mystic-amethyst), var(--sf-neon-blue));
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  font-family: var(--font-ui);
  font-weight: 600;
  padding: 16px 32px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-cosmic::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s ease;
}

.btn-cosmic:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(123, 44, 191, 0.4),
    0 0 20px rgba(0, 217, 255, 0.3);
}

.btn-cosmic:hover::before {
  left: 100%;
}

.btn-cosmic:active {
  transform: translateY(0);
  box-shadow: 
    0 4px 12px rgba(123, 44, 191, 0.6),
    inset 0 0 20px rgba(0, 0, 0, 0.2);
}

/* 🔮 카드 호버 효과 */
.card-mystic {
  background: rgba(26, 26, 46, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  position: relative;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
}

.card-mystic::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2px;
  background: linear-gradient(
    45deg,
    var(--mystic-amethyst),
    var(--sf-neon-blue),
    var(--fantasy-emerald)
  );
  border-radius: 16px;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card-mystic:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.3),
    0 0 30px rgba(123, 44, 191, 0.2);
}

.card-mystic:hover::before {
  opacity: 1;
}

/* 📱 인풋 포커스 효과 */
.input-cosmic {
  background: rgba(15, 15, 35, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-family: var(--font-body);
  font-size: 16px;
  outline: none;
  padding: 16px 20px;
  position: relative;
  transition: all 0.3s ease;
  width: 100%;
}

.input-cosmic:focus {
  border-color: var(--sf-neon-blue);
  box-shadow: 
    0 0 0 3px rgba(0, 217, 255, 0.1),
    0 0 20px rgba(0, 217, 255, 0.3);
  transform: scale(1.02);
}

.input-cosmic::placeholder {
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.3s ease;
}

.input-cosmic:focus::placeholder {
  color: rgba(0, 217, 255, 0.6);
}

/* 🌊 로딩 애니메이션 */
.loading-cosmic {
  position: relative;
  width: 60px;
  height: 60px;
  margin: 0 auto;
}

.loading-cosmic::before,
.loading-cosmic::after {
  content: '';
  position: absolute;
  inset: 0;
  border: 3px solid transparent;
  border-top-color: var(--sf-neon-blue);
  border-radius: 50%;
  animation: loading-spin 1.5s linear infinite;
}

.loading-cosmic::after {
  border-top-color: var(--mystic-amethyst);
  animation-delay: -0.75s;
  animation-duration: 3s;
}

@keyframes loading-spin {
  to { transform: rotate(360deg); }
}

/* 🎯 진행률 바 */
.progress-cosmic {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  overflow: hidden;
  position: relative;
}

.progress-cosmic-fill {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--sf-neon-blue) 0%,
    var(--mystic-amethyst) 50%,
    var(--sf-quantum) 100%
  );
  border-radius: 20px;
  position: relative;
  transition: width 0.3s ease;
}

.progress-cosmic-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 100%
  );
  animation: progress-shine 2s ease-in-out infinite;
}

@keyframes progress-shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
```

### **🎬 페이지 전환 애니메이션**

```tsx
// components/PageTransition.tsx - 페이지 전환 효과
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/router';

export const PageTransition: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const router = useRouter();
  
  const pageVariants = {
    initial: {
      opacity: 0,
      y: 20,
      scale: 0.98,
      filter: 'blur(4px)',
    },
    in: {
      opacity: 1,
      y: 0,
      scale: 1,
      filter: 'blur(0px)',
    },
    out: {
      opacity: 0,
      y: -20,
      scale: 1.02,
      filter: 'blur(4px)',
    },
  };
  
  const pageTransition = {
    type: 'tween',
    ease: 'anticipate',
    duration: 0.6,
  };
  
  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={router.route}
        initial="initial"
        animate="in"
        exit="out"
        variants={pageVariants}
        transition={pageTransition}
        className="w-full min-h-screen"
      >
        {children}
        
        {/* 홀로그램 전환 효과 */}
        <motion.div
          className="fixed inset-0 pointer-events-none z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 0.6, times: [0, 0.5, 1] }}
        >
          <div 
            className="w-full h-full"
            style={{
              background: 'linear-gradient(45deg, transparent 30%, rgba(0, 217, 255, 0.1) 50%, transparent 70%)',
              backgroundSize: '20px 20px',
            }}
          />
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

// 🌟 섹션별 애니메이션
export const AnimatedSection: React.FC<{
  children: React.ReactNode;
  delay?: number;
}> = ({ children, delay = 0 }) => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{
        duration: 0.6,
        delay,
        ease: [0.25, 0.8, 0.25, 1],
      }}
    >
      {children}
    </motion.section>
  );
};
```

## 📱 **반응형 디자인 가이드라인**

### **📐 브레이크포인트 시스템**

```css
/* 🌟 HEAL7 브레이크포인트 시스템 */
:root {
  /* 디바이스 브레이크포인트 */
  --bp-mobile: 375px;      /* 모바일 세로 */
  --bp-mobile-lg: 414px;   /* 모바일 세로 큰 화면 */
  --bp-tablet: 768px;      /* 태블릿 세로 */
  --bp-tablet-lg: 1024px;  /* 태블릿 가로 */
  --bp-desktop: 1280px;    /* 데스크톱 */
  --bp-desktop-lg: 1440px; /* 데스크톱 큰 화면 */
  --bp-desktop-xl: 1920px; /* 초대형 화면 */
  
  /* 컨텐츠 최대 너비 */
  --max-width-sm: 640px;
  --max-width-md: 768px;
  --max-width-lg: 1024px;
  --max-width-xl: 1280px;
  --max-width-2xl: 1536px;
}

/* 📱 모바일 우선 반응형 */
.responsive-container {
  width: 100%;
  max-width: var(--max-width-2xl);
  margin: 0 auto;
  padding: 0 16px;
}

/* 🎨 반응형 컴포넌트 스타일 */
@media (min-width: 375px) {
  .responsive-container {
    padding: 0 20px;
  }
  
  .text-scale {
    --text-hero: 3.5rem;
    --text-h1: 2.8rem;
  }
}

@media (min-width: 768px) {
  .responsive-container {
    padding: 0 32px;
  }
  
  .text-scale {
    --text-hero: 4.5rem;
    --text-h1: 3.5rem;
  }
  
  /* 태블릿에서 홀로그램 효과 강화 */
  .hologram-card {
    backdrop-filter: blur(12px);
  }
}

@media (min-width: 1024px) {
  .responsive-container {
    padding: 0 48px;
  }
  
  .text-scale {
    --text-hero: 5.5rem;
    --text-h1: 4rem;
  }
  
  /* 데스크톱에서 파티클 효과 증가 */
  .particle-system {
    --particle-density: 1.5;
  }
}

@media (min-width: 1440px) {
  .text-scale {
    --text-hero: 6rem;
    --text-h1: 4.5rem;
  }
}
```

## 📋 **결론 및 구현 가이드**

### **✅ 디자인 시스템 핵심 요소**

| 카테고리 | 구성 요소 | 구현 상태 | 활용도 |
|----------|----------|-----------|--------|
| **🎨 컬러** | 네뷸라 팔레트, 그라데이션 | ✅ 완료 | 높음 |
| **✨ UI** | 홀로그램 효과, 파티클 | ✅ 완료 | 높음 |
| **📝 타이포** | 우주적 폰트, 이펙트 | ✅ 완료 | 중간 |
| **🎬 애니메이션** | 인터랙션, 전환 효과 | ✅ 완료 | 높음 |
| **📱 반응형** | 브레이크포인트, 최적화 | ✅ 완료 | 필수 |

### **🚀 구현 우선순위**
1. **1단계**: 네뷸라 컬러 시스템 + 기본 홀로그램 UI (2주)
2. **2단계**: 파티클 효과 + 타이포그래피 (2주)
3. **3단계**: 고급 애니메이션 + 인터랙션 (3주)
4. **4단계**: 성능 최적화 + 접근성 개선 (1주)

### **🎯 브랜드 임팩트**
- **차별화**: 업계 유일의 신비+판타지+SF 퓨전 디자인
- **몰입감**: 우주적 치유 경험, 90% 사용자 몰입도 목표
- **기술력**: 최신 웹 기술 활용, 포스텔러 대비 70% 향상된 UX

---

**🔄 다음 문서**: [8. 반응형 컴포넌트 라이브러리 v1.0](./Responsive-Component-Library-v1.0.md)

**📧 문의사항**: arne40@heal7.com | **📞 연락처**: 050-7722-7328

*🤖 AI 생성 문서 | HEAL7 디자인팀 | 최종 검토: 2025-08-23*