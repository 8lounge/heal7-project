'use client';

import { useState, useEffect, useRef, ReactNode } from 'react';
import { motion, AnimatePresence, useInView } from 'framer-motion';

// 파티클 애니메이션 컴포넌트
export function ParticleBackground({ color = '#8b5cf6' }: { color?: string }) {
  const [particles, setParticles] = useState<Array<{
    id: number;
    x: number;
    y: number;
    size: number;
    speedX: number;
    speedY: number;
  }>>([]);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // 파티클 초기화
    const initParticles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 3 + 1,
      speedX: (Math.random() - 0.5) * 0.5,
      speedY: (Math.random() - 0.5) * 0.5
    }));
    
    setParticles(initParticles);
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      setParticles(prevParticles => 
        prevParticles.map(particle => {
          let newX = particle.x + particle.speedX;
          let newY = particle.y + particle.speedY;
          
          // 경계 처리
          if (newX < 0 || newX > canvas.width) particle.speedX *= -1;
          if (newY < 0 || newY > canvas.height) particle.speedY *= -1;
          
          newX = Math.max(0, Math.min(canvas.width, newX));
          newY = Math.max(0, Math.min(canvas.height, newY));
          
          // 파티클 그리기
          ctx.beginPath();
          ctx.arc(newX, newY, particle.size, 0, Math.PI * 2);
          ctx.fillStyle = color + '20';
          ctx.fill();
          
          return { ...particle, x: newX, y: newY };
        })
      );
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }, [color]);
  
  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={600}
      className="absolute inset-0 pointer-events-none opacity-30"
    />
  );
}

// 호버 글로우 효과
export function GlowCard({ 
  children, 
  glowColor = '#8b5cf6',
  className = ''
}: { 
  children: ReactNode;
  glowColor?: string;
  className?: string;
}) {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <div
      className={`relative ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative z-10">
        {children}
      </div>
      <AnimatePresence>
        {isHovered && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="absolute inset-0 rounded-lg blur-xl -z-10"
            style={{
              background: `radial-gradient(circle, ${glowColor}40 0%, transparent 70%)`,
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

// 타이핑 애니메이션
export function TypewriterText({ 
  text, 
  speed = 50,
  className = ''
}: { 
  text: string;
  speed?: number;
  className?: string;
}) {
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true });
  
  useEffect(() => {
    if (!inView) return;
    
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setDisplayText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);
      
      return () => clearTimeout(timer);
    }
  }, [currentIndex, text, speed, inView]);
  
  return (
    <div ref={ref} className={className}>
      {displayText}
      <span className="animate-pulse">|</span>
    </div>
  );
}

// 카운트업 애니메이션
export function CountUp({
  end,
  duration = 2000,
  className = ''
}: {
  end: number;
  duration?: number;
  className?: string;
}) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true });
  
  useEffect(() => {
    if (!inView) return;
    
    const startTime = Date.now();
    const startValue = 0;
    
    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // easeOut 함수
      const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);
      
      const currentValue = Math.round(startValue + (end - startValue) * easeOut(progress));
      setCount(currentValue);
      
      if (progress >= 1) {
        clearInterval(timer);
      }
    }, 16);
    
    return () => clearInterval(timer);
  }, [end, duration, inView]);
  
  return <span ref={ref} className={className}>{count}</span>;
}

// 맥동 효과
export function PulseOrb({ 
  size = 'w-4 h-4',
  color = 'bg-purple-500',
  pulseColor = 'bg-purple-500/20',
  className = ''
}: {
  size?: string;
  color?: string;
  pulseColor?: string;
  className?: string;
}) {
  return (
    <div className={`relative ${size} ${className}`}>
      <div className={`absolute inset-0 rounded-full ${color}`}></div>
      <div className={`absolute inset-0 rounded-full ${pulseColor} animate-ping`}></div>
    </div>
  );
}

// 프로그레스 링
export function ProgressRing({
  progress,
  size = 80,
  strokeWidth = 8,
  color = '#8b5cf6',
  bgColor = '#374151',
  className = ''
}: {
  progress: number;
  size?: number;
  strokeWidth?: number;
  color?: string;
  bgColor?: string;
  className?: string;
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * Math.PI * 2;
  const strokeDashoffset = circumference - (progress / 100) * circumference;
  
  return (
    <div className={`relative ${className}`}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
      >
        {/* 배경 링 */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={bgColor}
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        {/* 진행 링 */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-white font-bold text-sm">{progress}%</span>
      </div>
    </div>
  );
}

// 웨이브 애니메이션
export function WaveBackground({ 
  color = '#8b5cf6',
  opacity = 0.1,
  className = ''
}: {
  color?: string;
  opacity?: number;
  className?: string;
}) {
  return (
    <div className={`absolute inset-0 overflow-hidden ${className}`}>
      <svg
        className="absolute w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 1440 320"
      >
        <path
          fill={color}
          fillOpacity={opacity}
          d="M0,32L48,80C96,128,192,224,288,224C384,224,480,128,576,90.7C672,53,768,75,864,96C960,117,1056,139,1152,149.3C1248,160,1344,160,1392,160L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        >
          <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0; 50 0; 0 0"
            dur="10s"
            repeatCount="indefinite"
          />
        </path>
      </svg>
    </div>
  );
}

// 플로팅 요소
export function FloatingElement({
  children,
  intensity = 1,
  duration = 3,
  className = ''
}: {
  children: ReactNode;
  intensity?: number;
  duration?: number;
  className?: string;
}) {
  return (
    <motion.div
      className={className}
      animate={{
        y: [-intensity * 10, intensity * 10, -intensity * 10],
        rotate: [-intensity, intensity, -intensity]
      }}
      transition={{
        duration,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      {children}
    </motion.div>
  );
}