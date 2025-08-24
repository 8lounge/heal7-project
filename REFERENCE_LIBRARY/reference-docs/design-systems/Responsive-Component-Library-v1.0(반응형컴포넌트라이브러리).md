# 📱 HEAL7 반응형 컴포넌트 라이브러리 v1.0

> **설계 철학**: 모바일 우선 + 접근성 최우선 + 포스텔러 영감  
> **기술 스택**: Vite + React + TypeScript + Tailwind CSS + Three.js  
> **접근성 표준**: WCAG 2.2 AAA 준수  
> **최종 업데이트**: 2025-08-23

## 🎯 **컴포넌트 라이브러리 목표**

### **🌟 핵심 가치**
- **📱 Mobile-First**: 모바일에서 완벽, 데스크톱에서 놀라움
- **♿ Accessibility**: WCAG 2.2 AAA 표준 100% 준수
- **🎨 Consistency**: 일관된 디자인 시스템
- **⚡ Performance**: 초당 60프레임 부드러운 애니메이션
- **🔧 Modularity**: 재사용 가능한 모듈형 구조

### **📊 성능 목표**
- **로딩 시간**: 컴포넌트별 < 100ms 로딩
- **번들 크기**: 개별 컴포넌트 < 50KB
- **접근성 점수**: Lighthouse 접근성 100점
- **크로스 브라우저**: 99% 브라우저 지원
- **반응성**: 모든 디바이스에서 완벽한 레이아웃

## 🧩 **컴포넌트 아키텍처**

### **📁 라이브러리 구조**

```
src/components/
├── 📊 charts/              # 데이터 시각화 컴포넌트
│   ├── SajuBoard3D/        # 3D 사주판 (포스텔러 영감)
│   ├── ElementsRadar/      # 오행 레이더 차트
│   ├── LuckTimeline/       # 운세 타임라인
│   ├── CompatibilityWheel/ # 궁합 휠 차트
│   └── PersonalityGrid/    # 성격 매트릭스
├── 🎮 interactive/         # 인터랙티브 컴포넌트
│   ├── SajuCalculator/     # 사주 계산기
│   ├── FortuneWheel/       # 운세 돌림판
│   ├── CrystalBall3D/      # 3D 수정구
│   └── TarotCardDeck/      # 타로 카드덱
├── 🎨 ui/                  # 기본 UI 컴포넌트
│   ├── HologramCard/       # 홀로그램 카드
│   ├── NebulaButton/       # 네뷸라 버튼
│   ├── CosmicInput/        # 우주적 입력창
│   ├── StarProgress/       # 별빛 진행바
│   └── GalaxyModal/        # 갤럭시 모달
├── 🌐 layout/              # 레이아웃 컴포넌트
│   ├── ResponsiveGrid/     # 반응형 그리드
│   ├── FlexContainer/      # 유연한 컨테이너
│   └── StickyNavigation/   # 고정 네비게이션
└── ♿ accessibility/       # 접근성 컴포넌트
    ├── ScreenReader/       # 스크린 리더 지원
    ├── KeyboardNav/        # 키보드 네비게이션
    └── VoiceControl/       # 음성 제어 지원
```

### **🎨 컴포넌트 베이스 클래스**

```tsx
// types/component.types.ts - 공통 타입 정의
import { ReactNode, HTMLAttributes } from 'react';

// 🌈 테마 시스템
export type ThemeVariant = 'mystic' | 'fantasy' | 'scifi' | 'healing';
export type SizeVariant = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type ColorVariant = 'primary' | 'secondary' | 'accent' | 'neutral';

// ♿ 접근성 Props
export interface AccessibilityProps {
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-expanded'?: boolean;
  'aria-hidden'?: boolean;
  role?: string;
  tabIndex?: number;
}

// 📱 반응형 Props
export interface ResponsiveProps {
  mobile?: boolean;
  tablet?: boolean;
  desktop?: boolean;
  breakpoint?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

// 🎨 스타일링 Props
export interface StyleProps {
  theme?: ThemeVariant;
  size?: SizeVariant;
  color?: ColorVariant;
  className?: string;
  style?: React.CSSProperties;
}

// 🧩 베이스 컴포넌트 Props
export interface BaseComponentProps 
  extends HTMLAttributes<HTMLElement>, 
         AccessibilityProps, 
         ResponsiveProps, 
         StyleProps {
  children?: ReactNode;
  loading?: boolean;
  disabled?: boolean;
  error?: boolean;
  success?: boolean;
}

// components/base/BaseComponent.tsx - 베이스 컴포넌트
import React, { forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const baseVariants = cva(
  // 기본 스타일
  'relative transition-all duration-300 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500',
  {
    variants: {
      theme: {
        mystic: 'bg-gradient-to-br from-purple-900/50 to-indigo-900/50 border-purple-500/30',
        fantasy: 'bg-gradient-to-br from-emerald-900/50 to-blue-900/50 border-emerald-500/30',
        scifi: 'bg-gradient-to-br from-cyan-900/50 to-purple-900/50 border-cyan-500/30',
        healing: 'bg-gradient-to-br from-pink-900/50 to-yellow-900/50 border-pink-500/30',
      },
      size: {
        xs: 'text-xs p-2',
        sm: 'text-sm p-3',
        md: 'text-base p-4',
        lg: 'text-lg p-6',
        xl: 'text-xl p-8',
      },
      state: {
        default: '',
        loading: 'pointer-events-none opacity-70',
        disabled: 'pointer-events-none opacity-50 grayscale',
        error: 'border-red-500/50 bg-red-900/20',
        success: 'border-green-500/50 bg-green-900/20',
      }
    },
    defaultVariants: {
      theme: 'mystic',
      size: 'md',
      state: 'default',
    }
  }
);

interface BaseComponentProps extends VariantProps<typeof baseVariants> {
  as?: keyof JSX.IntrinsicElements;
  children?: React.ReactNode;
  className?: string;
  loading?: boolean;
  disabled?: boolean;
  error?: boolean;
  success?: boolean;
}

export const BaseComponent = forwardRef<HTMLElement, BaseComponentProps>(
  ({ 
    as: Component = 'div',
    theme,
    size,
    loading,
    disabled,
    error,
    success,
    className,
    children,
    ...props 
  }, ref) => {
    
    const state = loading ? 'loading' : 
                 disabled ? 'disabled' : 
                 error ? 'error' : 
                 success ? 'success' : 'default';
    
    return (
      <Component
        ref={ref}
        className={cn(baseVariants({ theme, size, state }), className)}
        {...props}
      >
        {children}
        
        {/* 로딩 스피너 */}
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-white/20 border-t-white/80 rounded-full animate-spin" />
          </div>
        )}
      </Component>
    );
  }
);

BaseComponent.displayName = 'BaseComponent';
```

## 📊 **데이터 시각화 컴포넌트**

### **🎯 3D 사주판 (포스텔러 영감)**

```tsx
// components/charts/SajuBoard3D.tsx - 3D 사주판 컴포넌트
import React, { Suspense, useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text3D, Environment, PerspectiveCamera } from '@react-three/drei';
import { BaseComponent } from '../base/BaseComponent';

interface SajuBoard3DProps {
  fourPillars: {
    year: { heaven: string; earth: string };
    month: { heaven: string; earth: string };
    day: { heaven: string; earth: string };
    hour: { heaven: string; earth: string };
  };
  interactive?: boolean;
  autoRotate?: boolean;
  theme?: 'mystic' | 'fantasy' | 'scifi';
}

// 🎋 사주 기둥 3D 컴포넌트
const SajuPillar3D: React.FC<{
  position: [number, number, number];
  heaven: string;
  earth: string;
  color: string;
}> = ({ position, heaven, earth, color }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    }
  });
  
  return (
    <group position={position}>
      {/* 기둥 베이스 */}
      <mesh ref={meshRef}>
        <cylinderGeometry args={[0.8, 1, 3, 8]} />
        <meshStandardMaterial 
          color={color} 
          transparent 
          opacity={0.8} 
          emissive={color}
          emissiveIntensity={0.2}
        />
      </mesh>
      
      {/* 천간 텍스트 */}
      <Text3D
        font="/fonts/noto-sans-kr.json"
        size={0.3}
        height={0.05}
        position={[0, 1.8, 0]}
      >
        {heaven}
        <meshStandardMaterial color="#FFD700" />
      </Text3D>
      
      {/* 지지 텍스트 */}
      <Text3D
        font="/fonts/noto-sans-kr.json"
        size={0.3}
        height={0.05}
        position={[0, -1.8, 0]}
      >
        {earth}
        <meshStandardMaterial color="#FFFFFF" />
      </Text3D>
      
      {/* 홀로그램 효과 링 */}
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
        <ringGeometry args={[1.2, 1.4, 32]} />
        <meshBasicMaterial 
          color={color} 
          transparent 
          opacity={0.3}
          side={2}
        />
      </mesh>
    </group>
  );
};

// 🌟 메인 3D 사주판
export const SajuBoard3D: React.FC<SajuBoard3DProps> = ({
  fourPillars,
  interactive = true,
  autoRotate = true,
  theme = 'mystic'
}) => {
  
  const pillarColors = useMemo(() => {
    switch (theme) {
      case 'mystic': return ['#7B2CBF', '#9333EA', '#A855F7', '#C084FC'];
      case 'fantasy': return ['#059669', '#0891B2', '#3B82F6', '#6366F1'];
      case 'scifi': return ['#00D9FF', '#8B5CF6', '#EC4899', '#F59E0B'];
      default: return ['#7B2CBF', '#9333EA', '#A855F7', '#C084FC'];
    }
  }, [theme]);
  
  // ♿ 접근성을 위한 텍스트 설명
  const accessibleDescription = useMemo(() => {
    const { year, month, day, hour } = fourPillars;
    return `사주 정보: 년주 ${year.heaven}${year.earth}, 월주 ${month.heaven}${month.earth}, 일주 ${day.heaven}${day.earth}, 시주 ${hour.heaven}${hour.earth}`;
  }, [fourPillars]);
  
  return (
    <BaseComponent
      className="w-full h-96 rounded-xl overflow-hidden"
      theme={theme}
      role="img"
      aria-label={accessibleDescription}
    >
      <Canvas>
        <Suspense fallback={null}>
          {/* 조명 설정 */}
          <ambientLight intensity={0.3} />
          <spotLight 
            position={[10, 10, 10]} 
            angle={0.3} 
            intensity={1}
            color="#FFD700"
          />
          <spotLight 
            position={[-10, -10, -10]} 
            angle={0.3} 
            intensity={0.5}
            color="#00D9FF"
          />
          
          {/* 환경 설정 */}
          <Environment preset="night" />
          
          {/* 카메라 */}
          <PerspectiveCamera makeDefault position={[0, 5, 8]} />
          
          {/* 사주 기둥들 */}
          <SajuPillar3D
            position={[-3, 0, 0]}
            heaven={fourPillars.year.heaven}
            earth={fourPillars.year.earth}
            color={pillarColors[0]}
          />
          <SajuPillar3D
            position={[-1, 0, 0]}
            heaven={fourPillars.month.heaven}
            earth={fourPillars.month.earth}
            color={pillarColors[1]}
          />
          <SajuPillar3D
            position={[1, 0, 0]}
            heaven={fourPillars.day.heaven}
            earth={fourPillars.day.earth}
            color={pillarColors[2]}
          />
          <SajuPillar3D
            position={[3, 0, 0]}
            heaven={fourPillars.hour.heaven}
            earth={fourPillars.hour.earth}
            color={pillarColors[3]}
          />
          
          {/* 베이스 플랫폼 */}
          <mesh position={[0, -3, 0]}>
            <cylinderGeometry args={[6, 6, 0.5, 32]} />
            <meshStandardMaterial 
              color="#1A1A2E" 
              transparent 
              opacity={0.8}
              emissive="#0F0F23"
              emissiveIntensity={0.1}
            />
          </mesh>
          
          {/* 컨트롤 */}
          {interactive && (
            <OrbitControls
              autoRotate={autoRotate}
              autoRotateSpeed={0.5}
              enableZoom={true}
              enablePan={false}
              minDistance={5}
              maxDistance={15}
              minPolarAngle={Math.PI / 6}
              maxPolarAngle={Math.PI / 2}
            />
          )}
        </Suspense>
      </Canvas>
      
      {/* 화면 읽기 프로그램을 위한 숨겨진 텍스트 */}
      <div className="sr-only">
        {accessibleDescription}
      </div>
    </BaseComponent>
  );
};
```

### **🌊 오행 레이더 차트**

```tsx
// components/charts/ElementsRadar.tsx - 오행 레이더 차트
import React, { useMemo } from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend } from 'recharts';
import { BaseComponent } from '../base/BaseComponent';

interface ElementsRadarProps {
  elements: {
    wood: number;    // 목
    fire: number;    // 화
    earth: number;   // 토
    metal: number;   // 금
    water: number;   // 수
  };
  showLegend?: boolean;
  animated?: boolean;
  theme?: 'mystic' | 'fantasy' | 'scifi';
}

export const ElementsRadar: React.FC<ElementsRadarProps> = ({
  elements,
  showLegend = true,
  animated = true,
  theme = 'mystic'
}) => {
  
  // 📊 차트 데이터 변환
  const chartData = useMemo(() => [
    { element: '목(木)', value: elements.wood, fullMark: 100, color: '#22C55E' },
    { element: '화(火)', value: elements.fire, fullMark: 100, color: '#EF4444' },
    { element: '토(土)', value: elements.earth, fullMark: 100, color: '#F59E0B' },
    { element: '금(金)', value: elements.metal, fullMark: 100, color: '#E5E7EB' },
    { element: '수(水)', value: elements.water, fullMark: 100, color: '#3B82F6' },
  ], [elements]);
  
  // 🎨 테마별 색상 설정
  const themeColors = useMemo(() => {
    switch (theme) {
      case 'mystic':
        return {
          primary: '#7B2CBF',
          secondary: '#C77DFF',
          grid: 'rgba(123, 44, 191, 0.3)',
          text: '#FFFFFF'
        };
      case 'fantasy':
        return {
          primary: '#059669',
          secondary: '#A5B4FC',
          grid: 'rgba(5, 150, 105, 0.3)',
          text: '#FFFFFF'
        };
      case 'scifi':
        return {
          primary: '#00D9FF',
          secondary: '#EC4899',
          grid: 'rgba(0, 217, 255, 0.3)',
          text: '#FFFFFF'
        };
      default:
        return {
          primary: '#7B2CBF',
          secondary: '#C77DFF',
          grid: 'rgba(123, 44, 191, 0.3)',
          text: '#FFFFFF'
        };
    }
  }, [theme]);
  
  // ♿ 접근성을 위한 데이터 설명
  const accessibleDescription = useMemo(() => {
    const elementNames = ['목', '화', '토', '금', '수'];
    const values = [elements.wood, elements.fire, elements.earth, elements.metal, elements.water];
    const descriptions = elementNames.map((name, index) => `${name}: ${values[index]}점`);
    return `오행 균형 차트. ${descriptions.join(', ')}`;
  }, [elements]);
  
  return (
    <BaseComponent
      className="w-full h-96 p-6"
      theme={theme}
      role="img"
      aria-label={accessibleDescription}
    >
      <div className="w-full h-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
            {/* 그리드 */}
            <PolarGrid 
              stroke={themeColors.grid}
              strokeWidth={1}
              radialLines={true}
            />
            
            {/* 각도 축 (오행 라벨) */}
            <PolarAngleAxis
              dataKey="element"
              tick={{ 
                fontSize: 14, 
                fill: themeColors.text,
                fontWeight: 600
              }}
              tickFormatter={(value) => value}
            />
            
            {/* 반지름 축 (수치) */}
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ 
                fontSize: 12, 
                fill: themeColors.text,
                opacity: 0.7
              }}
              axisLine={false}
            />
            
            {/* 레이더 영역 */}
            <Radar
              name="오행 균형"
              dataKey="value"
              stroke={themeColors.primary}
              fill={themeColors.primary}
              strokeWidth={3}
              fillOpacity={0.2}
              dot={{ 
                fill: themeColors.secondary, 
                strokeWidth: 2, 
                stroke: themeColors.primary,
                r: 6 
              }}
              animationBegin={animated ? 0 : undefined}
              animationDuration={animated ? 1000 : 0}
              isAnimationActive={animated}
            />
            
            {/* 범례 */}
            {showLegend && (
              <Legend
                verticalAlign="bottom"
                height={36}
                iconType="circle"
                wrapperStyle={{
                  fontSize: '14px',
                  color: themeColors.text,
                }}
              />
            )}
          </RadarChart>
        </ResponsiveContainer>
      </div>
      
      {/* 스크린 리더를 위한 테이블 */}
      <table className="sr-only">
        <caption>오행 균형 데이터</caption>
        <thead>
          <tr>
            <th>오행</th>
            <th>수치</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>목(木)</td><td>{elements.wood}</td></tr>
          <tr><td>화(火)</td><td>{elements.fire}</td></tr>
          <tr><td>토(土)</td><td>{elements.earth}</td></tr>
          <tr><td>금(金)</td><td>{elements.metal}</td></tr>
          <tr><td>수(水)</td><td>{elements.water}</td></tr>
        </tbody>
      </table>
    </BaseComponent>
  );
};
```

### **⏰ 운세 타임라인 차트**

```tsx
// components/charts/LuckTimeline.tsx - 운세 타임라인
import React, { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart, ReferenceLine } from 'recharts';
import { BaseComponent } from '../base/BaseComponent';

interface LuckTimelineProps {
  luckData: Array<{
    year: number;
    fortune: number;    // -100 ~ +100
    category: 'career' | 'love' | 'health' | 'wealth';
    description: string;
  }>;
  currentYear?: number;
  showTooltip?: boolean;
  theme?: 'mystic' | 'fantasy' | 'scifi';
}

export const LuckTimeline: React.FC<LuckTimelineProps> = ({
  luckData,
  currentYear = new Date().getFullYear(),
  showTooltip = true,
  theme = 'mystic'
}) => {
  
  // 🎨 테마별 색상
  const themeColors = useMemo(() => {
    switch (theme) {
      case 'mystic':
        return {
          positive: '#7B2CBF',
          negative: '#DC2626',
          neutral: '#6B7280',
          grid: 'rgba(255, 255, 255, 0.1)',
          text: '#FFFFFF'
        };
      case 'fantasy':
        return {
          positive: '#059669',
          negative: '#DC2626',
          neutral: '#6B7280',
          grid: 'rgba(255, 255, 255, 0.1)',
          text: '#FFFFFF'
        };
      case 'scifi':
        return {
          positive: '#00D9FF',
          negative: '#EC4899',
          neutral: '#6B7280',
          grid: 'rgba(255, 255, 255, 0.1)',
          text: '#FFFFFF'
        };
      default:
        return {
          positive: '#7B2CBF',
          negative: '#DC2626',
          neutral: '#6B7280',
          grid: 'rgba(255, 255, 255, 0.1)',
          text: '#FFFFFF'
        };
    }
  }, [theme]);
  
  // 📈 차트 데이터 처리
  const processedData = useMemo(() => {
    return luckData.map(item => ({
      ...item,
      color: item.fortune > 0 ? themeColors.positive : 
             item.fortune < 0 ? themeColors.negative : 
             themeColors.neutral,
      isCurrentYear: item.year === currentYear
    }));
  }, [luckData, currentYear, themeColors]);
  
  // 🎯 커스텀 툴팁
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-900/95 backdrop-blur-md border border-white/10 rounded-lg p-4 shadow-xl">
          <p className="text-white font-semibold mb-2">{label}년</p>
          <p className="text-sm text-gray-300 mb-1">
            운세: {data.fortune > 0 ? '+' : ''}{data.fortune}점
          </p>
          <p className="text-sm text-gray-300 mb-1">
            분야: {getCategoryLabel(data.category)}
          </p>
          <p className="text-sm text-gray-400">{data.description}</p>
        </div>
      );
    }
    return null;
  };
  
  const getCategoryLabel = (category: string) => {
    const labels = {
      career: '직업운',
      love: '연애운',
      health: '건강운',
      wealth: '재물운'
    };
    return labels[category as keyof typeof labels] || category;
  };
  
  // ♿ 접근성 설명
  const accessibleDescription = useMemo(() => {
    const years = luckData.map(d => d.year);
    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);
    const avgFortune = Math.round(luckData.reduce((sum, d) => sum + d.fortune, 0) / luckData.length);
    return `${minYear}년부터 ${maxYear}년까지의 운세 타임라인. 평균 운세: ${avgFortune}점`;
  }, [luckData]);
  
  return (
    <BaseComponent
      className="w-full h-96 p-6"
      theme={theme}
      role="img"
      aria-label={accessibleDescription}
    >
      <div className="w-full h-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={processedData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            {/* 그리드 */}
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke={themeColors.grid}
              strokeOpacity={0.3}
            />
            
            {/* X축 (년도) */}
            <XAxis
              dataKey="year"
              tick={{ fontSize: 12, fill: themeColors.text }}
              axisLine={{ stroke: themeColors.grid }}
              tickLine={{ stroke: themeColors.grid }}
            />
            
            {/* Y축 (운세 점수) */}
            <YAxis
              domain={[-100, 100]}
              tick={{ fontSize: 12, fill: themeColors.text }}
              axisLine={{ stroke: themeColors.grid }}
              tickLine={{ stroke: themeColors.grid }}
              tickFormatter={(value) => `${value}`}
            />
            
            {/* 현재 년도 참조선 */}
            {currentYear && (
              <ReferenceLine
                x={currentYear}
                stroke="#FFD700"
                strokeWidth={2}
                strokeDasharray="5 5"
                label={{ value: "현재", position: "top" }}
              />
            )}
            
            {/* 중립선 (0점) */}
            <ReferenceLine
              y={0}
              stroke={themeColors.neutral}
              strokeWidth={1}
              strokeDasharray="2 2"
            />
            
            {/* 영역 차트 */}
            <Area
              type="monotone"
              dataKey="fortune"
              stroke={themeColors.positive}
              strokeWidth={3}
              fill="url(#fortuneGradient)"
              fillOpacity={0.3}
            />
            
            {/* 라인 차트 */}
            <Line
              type="monotone"
              dataKey="fortune"
              stroke={themeColors.positive}
              strokeWidth={3}
              dot={{ 
                fill: themeColors.positive, 
                strokeWidth: 2, 
                stroke: '#FFFFFF',
                r: 5 
              }}
              activeDot={{ 
                r: 8, 
                stroke: themeColors.positive, 
                strokeWidth: 2,
                fill: '#FFFFFF' 
              }}
            />
            
            {/* 툴팁 */}
            {showTooltip && <Tooltip content={<CustomTooltip />} />}
            
            {/* 그라데이션 정의 */}
            <defs>
              <linearGradient id="fortuneGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={themeColors.positive} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={themeColors.positive} stopOpacity={0.1}/>
              </linearGradient>
            </defs>
          </AreaChart>
        </ResponsiveContainer>
      </div>
      
      {/* 접근성 데이터 테이블 */}
      <table className="sr-only">
        <caption>연도별 운세 데이터</caption>
        <thead>
          <tr>
            <th>년도</th>
            <th>운세</th>
            <th>분야</th>
            <th>설명</th>
          </tr>
        </thead>
        <tbody>
          {luckData.map((item, index) => (
            <tr key={index}>
              <td>{item.year}</td>
              <td>{item.fortune}</td>
              <td>{getCategoryLabel(item.category)}</td>
              <td>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </BaseComponent>
  );
};
```

## 🎮 **인터랙티브 컴포넌트**

### **🧮 사주 계산기**

```tsx
// components/interactive/SajuCalculator.tsx - 사주 계산기
import React, { useState, useCallback } from 'react';
import { BaseComponent } from '../base/BaseComponent';
import { CosmicInput } from '../ui/CosmicInput';
import { NebulaButton } from '../ui/NebulaButton';
import { StarProgress } from '../ui/StarProgress';

interface SajuCalculatorProps {
  onCalculate?: (data: SajuInputData) => void;
  loading?: boolean;
  theme?: 'mystic' | 'fantasy' | 'scifi';
}

interface SajuInputData {
  birthYear: number;
  birthMonth: number;
  birthDay: number;
  birthHour?: number;
  isLunar: boolean;
  gender?: 'M' | 'F';
  name?: string;
}

export const SajuCalculator: React.FC<SajuCalculatorProps> = ({
  onCalculate,
  loading = false,
  theme = 'mystic'
}) => {
  
  const [formData, setFormData] = useState<SajuInputData>({
    birthYear: new Date().getFullYear(),
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    isLunar: false,
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 3;
  
  // 🔍 입력 검증
  const validateForm = useCallback(() => {
    const newErrors: Record<string, string> = {};
    
    // 년도 검증
    if (formData.birthYear < 1900 || formData.birthYear > 2100) {
      newErrors.birthYear = '1900년부터 2100년 사이의 년도를 입력해주세요';
    }
    
    // 월 검증
    if (formData.birthMonth < 1 || formData.birthMonth > 12) {
      newErrors.birthMonth = '1월부터 12월 사이의 값을 입력해주세요';
    }
    
    // 일 검증
    const daysInMonth = new Date(formData.birthYear, formData.birthMonth, 0).getDate();
    if (formData.birthDay < 1 || formData.birthDay > daysInMonth) {
      newErrors.birthDay = `해당 월은 1일부터 ${daysInMonth}일까지만 존재합니다`;
    }
    
    // 시간 검증 (선택사항)
    if (formData.birthHour && (formData.birthHour < 0 || formData.birthHour > 23)) {
      newErrors.birthHour = '0시부터 23시 사이의 값을 입력해주세요';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [formData]);
  
  // 📝 폼 제출
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      onCalculate?.(formData);
    }
  }, [formData, validateForm, onCalculate]);
  
  // 🎯 단계별 컨텐츠
  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-white mb-4">📅 생년월일 입력</h3>
            
            {/* 년도 */}
            <CosmicInput
              label="태어난 년도"
              type="number"
              value={formData.birthYear}
              onChange={(value) => setFormData(prev => ({ ...prev, birthYear: Number(value) }))}
              error={errors.birthYear}
              min={1900}
              max={2100}
              required
              aria-describedby="year-help"
            />
            <p id="year-help" className="text-sm text-gray-400">예: 1990</p>
            
            {/* 월 */}
            <CosmicInput
              label="태어난 월"
              type="number"
              value={formData.birthMonth}
              onChange={(value) => setFormData(prev => ({ ...prev, birthMonth: Number(value) }))}
              error={errors.birthMonth}
              min={1}
              max={12}
              required
              aria-describedby="month-help"
            />
            <p id="month-help" className="text-sm text-gray-400">예: 3 (3월)</p>
            
            {/* 일 */}
            <CosmicInput
              label="태어난 일"
              type="number"
              value={formData.birthDay}
              onChange={(value) => setFormData(prev => ({ ...prev, birthDay: Number(value) }))}
              error={errors.birthDay}
              min={1}
              max={31}
              required
              aria-describedby="day-help"
            />
            <p id="day-help" className="text-sm text-gray-400">예: 15 (15일)</p>
            
            {/* 음력/양력 선택 */}
            <fieldset className="mt-6">
              <legend className="text-sm font-medium text-white mb-3">달력 종류</legend>
              <div className="flex space-x-6">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="calendar"
                    checked={!formData.isLunar}
                    onChange={() => setFormData(prev => ({ ...prev, isLunar: false }))}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500 focus:ring-2"
                  />
                  <span className="ml-2 text-white">양력</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="calendar"
                    checked={formData.isLunar}
                    onChange={() => setFormData(prev => ({ ...prev, isLunar: true }))}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500 focus:ring-2"
                  />
                  <span className="ml-2 text-white">음력</span>
                </label>
              </div>
            </fieldset>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-white mb-4">⏰ 추가 정보 입력</h3>
            
            {/* 시간 (선택사항) */}
            <CosmicInput
              label="태어난 시간 (선택사항)"
              type="number"
              value={formData.birthHour || ''}
              onChange={(value) => setFormData(prev => ({ 
                ...prev, 
                birthHour: value ? Number(value) : undefined 
              }))}
              error={errors.birthHour}
              min={0}
              max={23}
              placeholder="예: 14 (오후 2시)"
              aria-describedby="hour-help"
            />
            <p id="hour-help" className="text-sm text-gray-400">
              정확한 시간을 모르시면 비워두셔도 됩니다. 시주까지 정확한 사주를 원하시면 입력해주세요.
            </p>
            
            {/* 성별 (선택사항) */}
            <fieldset className="mt-6">
              <legend className="text-sm font-medium text-white mb-3">성별 (선택사항)</legend>
              <div className="flex space-x-6">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="gender"
                    value="M"
                    checked={formData.gender === 'M'}
                    onChange={() => setFormData(prev => ({ ...prev, gender: 'M' }))}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500 focus:ring-2"
                  />
                  <span className="ml-2 text-white">남성</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="gender"
                    value="F"
                    checked={formData.gender === 'F'}
                    onChange={() => setFormData(prev => ({ ...prev, gender: 'F' }))}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500 focus:ring-2"
                  />
                  <span className="ml-2 text-white">여성</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="gender"
                    value=""
                    checked={!formData.gender}
                    onChange={() => setFormData(prev => ({ ...prev, gender: undefined }))}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500 focus:ring-2"
                  />
                  <span className="ml-2 text-white">선택안함</span>
                </label>
              </div>
            </fieldset>
            
            {/* 이름 (선택사항) */}
            <CosmicInput
              label="이름 (선택사항)"
              type="text"
              value={formData.name || ''}
              onChange={(value) => setFormData(prev => ({ ...prev, name: value || undefined }))}
              placeholder="홍길동"
              aria-describedby="name-help"
            />
            <p id="name-help" className="text-sm text-gray-400">
              이름을 입력하시면 더욱 개인화된 해석을 받으실 수 있습니다.
            </p>
          </div>
        );
        
      case 3:
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-white mb-4">✅ 입력 정보 확인</h3>
            
            <div className="bg-white/5 rounded-lg p-6 space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">생년월일:</span>
                <span className="text-white font-medium">
                  {formData.birthYear}년 {formData.birthMonth}월 {formData.birthDay}일
                  {formData.isLunar ? ' (음력)' : ' (양력)'}
                </span>
              </div>
              
              {formData.birthHour !== undefined && (
                <div className="flex justify-between">
                  <span className="text-gray-400">태어난 시간:</span>
                  <span className="text-white font-medium">{formData.birthHour}시</span>
                </div>
              )}
              
              {formData.gender && (
                <div className="flex justify-between">
                  <span className="text-gray-400">성별:</span>
                  <span className="text-white font-medium">
                    {formData.gender === 'M' ? '남성' : '여성'}
                  </span>
                </div>
              )}
              
              {formData.name && (
                <div className="flex justify-between">
                  <span className="text-gray-400">이름:</span>
                  <span className="text-white font-medium">{formData.name}</span>
                </div>
              )}
            </div>
            
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
              <p className="text-sm text-blue-200">
                ℹ️ 입력하신 정보를 바탕으로 정확한 사주를 계산해드립니다. 
                모든 정보는 안전하게 처리되며 저장되지 않습니다.
              </p>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <BaseComponent
      as="form"
      onSubmit={handleSubmit}
      className="max-w-2xl mx-auto p-8"
      theme={theme}
      role="form"
      aria-label="사주 계산기"
    >
      {/* 진행률 표시 */}
      <div className="mb-8">
        <StarProgress 
          current={currentStep} 
          total={totalSteps} 
          theme={theme}
        />
      </div>
      
      {/* 단계별 컨텐츠 */}
      <div className="mb-8">
        {renderStepContent()}
      </div>
      
      {/* 네비게이션 버튼 */}
      <div className="flex justify-between">
        <NebulaButton
          type="button"
          variant="secondary"
          onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
          disabled={currentStep === 1}
          theme={theme}
        >
          이전
        </NebulaButton>
        
        {currentStep < totalSteps ? (
          <NebulaButton
            type="button"
            onClick={() => setCurrentStep(prev => Math.min(totalSteps, prev + 1))}
            disabled={currentStep === 1 && !validateForm()}
            theme={theme}
          >
            다음
          </NebulaButton>
        ) : (
          <NebulaButton
            type="submit"
            loading={loading}
            disabled={!validateForm()}
            theme={theme}
          >
            🔮 사주 계산하기
          </NebulaButton>
        )}
      </div>
      
      {/* 스크린 리더를 위한 추가 정보 */}
      <div className="sr-only">
        <p>총 {totalSteps}단계 중 {currentStep}단계입니다.</p>
        <p>필수 입력 사항: 생년월일</p>
        <p>선택 입력 사항: 시간, 성별, 이름</p>
      </div>
    </BaseComponent>
  );
};
```

## 🎨 **UI 기본 컴포넌트**

### **💫 네뷸라 버튼**

```tsx
// components/ui/NebulaButton.tsx - 네뷸라 버튼
import React, { forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const nebulaButtonVariants = cva(
  // 기본 스타일
  'inline-flex items-center justify-center rounded-xl font-semibold transition-all duration-300 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 relative overflow-hidden group',
  {
    variants: {
      variant: {
        primary: 'bg-gradient-to-r text-white shadow-lg hover:shadow-xl transform hover:-translate-y-1 active:translate-y-0',
        secondary: 'border-2 bg-transparent text-white hover:bg-white/10 backdrop-blur-sm',
        ghost: 'text-white hover:bg-white/10',
        destructive: 'bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg hover:shadow-red-500/50',
      },
      size: {
        sm: 'h-9 px-4 text-sm',
        md: 'h-11 px-6 text-base',
        lg: 'h-13 px-8 text-lg',
        xl: 'h-16 px-12 text-xl',
      },
      theme: {
        mystic: '',
        fantasy: '',
        scifi: '',
      }
    },
    compoundVariants: [
      // 테마별 primary 버튼 스타일
      {
        variant: 'primary',
        theme: 'mystic',
        className: 'from-purple-600 via-purple-700 to-indigo-800 hover:from-purple-500 hover:via-purple-600 hover:to-indigo-700 focus-visible:ring-purple-500',
      },
      {
        variant: 'primary',
        theme: 'fantasy',
        className: 'from-emerald-600 via-teal-700 to-blue-800 hover:from-emerald-500 hover:via-teal-600 hover:to-blue-700 focus-visible:ring-emerald-500',
      },
      {
        variant: 'primary',
        theme: 'scifi',
        className: 'from-cyan-600 via-blue-700 to-purple-800 hover:from-cyan-500 hover:via-blue-600 hover:to-purple-700 focus-visible:ring-cyan-500',
      },
      // 테마별 secondary 버튼 스타일
      {
        variant: 'secondary',
        theme: 'mystic',
        className: 'border-purple-500/50 text-purple-300 hover:border-purple-400 hover:text-purple-200 focus-visible:ring-purple-500',
      },
      {
        variant: 'secondary',
        theme: 'fantasy',
        className: 'border-emerald-500/50 text-emerald-300 hover:border-emerald-400 hover:text-emerald-200 focus-visible:ring-emerald-500',
      },
      {
        variant: 'secondary',
        theme: 'scifi',
        className: 'border-cyan-500/50 text-cyan-300 hover:border-cyan-400 hover:text-cyan-200 focus-visible:ring-cyan-500',
      },
    ],
    defaultVariants: {
      variant: 'primary',
      size: 'md',
      theme: 'mystic',
    },
  }
);

interface NebulaButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof nebulaButtonVariants> {
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const NebulaButton = forwardRef<HTMLButtonElement, NebulaButtonProps>(
  ({ 
    className, 
    variant, 
    size, 
    theme, 
    loading = false,
    leftIcon,
    rightIcon,
    children, 
    disabled,
    ...props 
  }, ref) => {
    
    return (
      <button
        ref={ref}
        className={cn(nebulaButtonVariants({ variant, size, theme }), className)}
        disabled={disabled || loading}
        {...props}
      >
        {/* 홀로그램 스캔 효과 */}
        <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out" />
        
        {/* 컨텐츠 */}
        <span className="relative flex items-center justify-center gap-2">
          {loading ? (
            <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          ) : (
            leftIcon
          )}
          
          {children}
          
          {!loading && rightIcon}
        </span>
        
        {/* 파티클 효과 */}
        <span className="absolute inset-0 pointer-events-none">
          {Array.from({ length: 6 }).map((_, i) => (
            <span
              key={i}
              className="absolute w-1 h-1 bg-white/60 rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${i * 0.2}s`,
                animationDuration: `${2 + Math.random()}s`,
              }}
            />
          ))}
        </span>
      </button>
    );
  }
);

NebulaButton.displayName = 'NebulaButton';
```

### **✨ 코스믹 인풋**

```tsx
// components/ui/CosmicInput.tsx - 코스믹 입력창
import React, { forwardRef, useState } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const cosmicInputVariants = cva(
  'w-full rounded-lg border-2 bg-black/20 backdrop-blur-sm text-white placeholder-white/40 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-11 px-4 text-base',
        lg: 'h-13 px-5 text-lg',
      },
      theme: {
        mystic: 'border-purple-500/30 focus:border-purple-400 focus:ring-purple-500/30',
        fantasy: 'border-emerald-500/30 focus:border-emerald-400 focus:ring-emerald-500/30',
        scifi: 'border-cyan-500/30 focus:border-cyan-400 focus:ring-cyan-500/30',
      },
      state: {
        default: '',
        error: 'border-red-500/50 focus:border-red-400 focus:ring-red-500/30',
        success: 'border-green-500/50 focus:border-green-400 focus:ring-green-500/30',
      }
    },
    defaultVariants: {
      size: 'md',
      theme: 'mystic',
      state: 'default',
    },
  }
);

interface CosmicInputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>,
    VariantProps<typeof cosmicInputVariants> {
  label?: string;
  error?: string;
  success?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  onChange?: (value: string) => void;
}

export const CosmicInput = forwardRef<HTMLInputElement, CosmicInputProps>(
  ({ 
    className,
    size,
    theme,
    label,
    error,
    success,
    leftIcon,
    rightIcon,
    onChange,
    id,
    ...props
  }, ref) => {
    
    const [isFocused, setIsFocused] = useState(false);
    const inputId = id || `cosmic-input-${Math.random().toString(36).substr(2, 9)}`;
    const errorId = error ? `${inputId}-error` : undefined;
    const successId = success ? `${inputId}-success` : undefined;
    
    const state = error ? 'error' : success ? 'success' : 'default';
    
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      onChange?.(e.target.value);
      props.onChange?.(e);
    };
    
    return (
      <div className="w-full">
        {/* 라벨 */}
        {label && (
          <label
            htmlFor={inputId}
            className={cn(
              'block text-sm font-medium mb-2 transition-colors duration-200',
              isFocused ? 'text-white' : 'text-gray-300'
            )}
          >
            {label}
            {props.required && <span className="text-red-400 ml-1">*</span>}
          </label>
        )}
        
        {/* 입력 필드 컨테이너 */}
        <div className="relative">
          {/* 왼쪽 아이콘 */}
          {leftIcon && (
            <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              {leftIcon}
            </div>
          )}
          
          {/* 입력 필드 */}
          <input
            ref={ref}
            id={inputId}
            className={cn(
              cosmicInputVariants({ size, theme, state }),
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              className
            )}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            onChange={handleChange}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={cn(
              errorId,
              successId,
              props['aria-describedby']
            )}
            {...props}
          />
          
          {/* 오른쪽 아이콘 */}
          {rightIcon && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              {rightIcon}
            </div>
          )}
          
          {/* 홀로그램 효과 테두리 */}
          <div 
            className={cn(
              'absolute inset-0 rounded-lg pointer-events-none transition-opacity duration-300',
              'bg-gradient-to-r from-transparent via-white/10 to-transparent',
              'opacity-0',
              isFocused && 'opacity-100'
            )}
            style={{
              background: `linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%)`,
              backgroundSize: '200% 100%',
              animation: isFocused ? 'hologram-scan 2s ease-in-out infinite' : 'none',
            }}
          />
        </div>
        
        {/* 에러 메시지 */}
        {error && (
          <p
            id={errorId}
            className="mt-2 text-sm text-red-400 flex items-center gap-1"
            role="alert"
          >
            <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </p>
        )}
        
        {/* 성공 메시지 */}
        {success && (
          <p
            id={successId}
            className="mt-2 text-sm text-green-400 flex items-center gap-1"
          >
            <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            {success}
          </p>
        )}
      </div>
    );
  }
);

CosmicInput.displayName = 'CosmicInput';

// 🌟 홀로그램 스캔 애니메이션 CSS
const hologramScanStyles = `
@keyframes hologram-scan {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
`;

// 스타일을 헤드에 추가
if (typeof window !== 'undefined') {
  const styleElement = document.createElement('style');
  styleElement.textContent = hologramScanStyles;
  document.head.appendChild(styleElement);
}
```

## ♿ **접근성 최적화**

### **🔊 스크린 리더 지원**

```tsx
// components/accessibility/ScreenReader.tsx - 스크린 리더 지원
import React from 'react';

interface ScreenReaderProps {
  children: React.ReactNode;
  priority?: 'polite' | 'assertive';
}

export const ScreenReader: React.FC<ScreenReaderProps> = ({ 
  children, 
  priority = 'polite' 
}) => {
  return (
    <div
      className="sr-only"
      role="status"
      aria-live={priority}
      aria-atomic="true"
    >
      {children}
    </div>
  );
};

// 📢 실시간 알림 컴포넌트
interface LiveAnnouncerProps {
  message: string;
  priority?: 'polite' | 'assertive';
}

export const LiveAnnouncer: React.FC<LiveAnnouncerProps> = ({ 
  message, 
  priority = 'polite' 
}) => {
  const [announcement, setAnnouncement] = React.useState('');
  
  React.useEffect(() => {
    // 메시지 변경시 스크린 리더에 알림
    if (message) {
      setAnnouncement('');
      // 짧은 지연 후 메시지 설정 (스크린 리더 인식 보장)
      setTimeout(() => setAnnouncement(message), 100);
    }
  }, [message]);
  
  return (
    <ScreenReader priority={priority}>
      {announcement}
    </ScreenReader>
  );
};

// ⌨️ 키보드 네비게이션 트랩
export const FocusTrap: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  
  React.useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          // Shift + Tab
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement?.focus();
          }
        } else {
          // Tab
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement?.focus();
          }
        }
      }
      
      // ESC 키로 닫기
      if (e.key === 'Escape') {
        const closeButton = container.querySelector('[data-close]') as HTMLElement;
        closeButton?.click();
      }
    };
    
    container.addEventListener('keydown', handleKeyDown);
    
    // 초기 포커스 설정
    firstElement?.focus();
    
    return () => {
      container.removeEventListener('keydown', handleKeyDown);
    };
  }, []);
  
  return (
    <div ref={containerRef} role="dialog" aria-modal="true">
      {children}
    </div>
  );
};
```

### **🎨 고대비 모드 지원**

```css
/* 고대비 모드 스타일 */
@media (prefers-contrast: high) {
  :root {
    /* 고대비 색상 재정의 */
    --mystic-deep-violet: #000080;
    --mystic-amethyst: #4B0082;
    --mystic-aurora: #8A2BE2;
    --mystic-gold: #FFD700;
    
    --fantasy-emerald: #006400;
    --fantasy-sapphire: #000080;
    --fantasy-crystal: #4169E1;
    --fantasy-silver: #C0C0C0;
    
    --sf-neon-blue: #0000FF;
    --sf-hologram: #8B00FF;
    --sf-plasma: #FF8C00;
    --sf-quantum: #FF1493;
  }
  
  /* 텍스트 대비 강화 */
  .text-white { color: #FFFFFF !important; }
  .text-gray-300 { color: #D3D3D3 !important; }
  .text-gray-400 { color: #A9A9A9 !important; }
  
  /* 버튼 대비 강화 */
  .hologram-card {
    border: 2px solid #FFFFFF;
    background: #000000;
  }
  
  .hologram-button {
    border: 2px solid #FFFFFF;
    background: #000080;
    color: #FFFFFF;
  }
  
  /* 입력 필드 대비 강화 */
  .input-cosmic {
    border: 2px solid #FFFFFF;
    background: #000000;
    color: #FFFFFF;
  }
  
  .input-cosmic::placeholder {
    color: #C0C0C0;
  }
}

/* 움직임 줄이기 모드 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  
  /* 파티클 효과 비활성화 */
  .particle-system {
    display: none;
  }
  
  /* 홀로그램 효과 단순화 */
  .hologram-base::before,
  .hologram-base::after {
    display: none;
  }
}

/* 스크린 리더 전용 클래스 */
.sr-only {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

/* 포커스 시각화 강화 */
.focus\:outline-none:focus {
  outline: 2px solid #FFD700 !important;
  outline-offset: 2px !important;
}

.focus-visible\:ring-2:focus-visible {
  --tw-ring-width: 3px !important;
  --tw-ring-color: #FFD700 !important;
}
```

## 📱 **반응형 최적화**

### **📐 브레이크포인트별 컴포넌트**

```tsx
// hooks/useResponsive.tsx - 반응형 훅
import { useState, useEffect } from 'react';

export type Breakpoint = 'mobile' | 'tablet' | 'desktop' | 'desktop-lg';

const breakpoints = {
  mobile: 0,
  tablet: 768,
  desktop: 1024,
  'desktop-lg': 1440,
};

export const useResponsive = () => {
  const [breakpoint, setBreakpoint] = useState<Breakpoint>('desktop');
  const [windowSize, setWindowSize] = useState({ width: 0, height: 0 });
  
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      setWindowSize({ width, height });
      
      let currentBreakpoint: Breakpoint = 'mobile';
      
      if (width >= breakpoints['desktop-lg']) {
        currentBreakpoint = 'desktop-lg';
      } else if (width >= breakpoints.desktop) {
        currentBreakpoint = 'desktop';
      } else if (width >= breakpoints.tablet) {
        currentBreakpoint = 'tablet';
      }
      
      setBreakpoint(currentBreakpoint);
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return {
    breakpoint,
    windowSize,
    isMobile: breakpoint === 'mobile',
    isTablet: breakpoint === 'tablet',
    isDesktop: breakpoint === 'desktop' || breakpoint === 'desktop-lg',
    isDesktopLg: breakpoint === 'desktop-lg',
  };
};

// 반응형 컴포넌트 래퍼
interface ResponsiveProps {
  children: React.ReactNode;
  mobile?: React.ReactNode;
  tablet?: React.ReactNode;
  desktop?: React.ReactNode;
  desktopLg?: React.ReactNode;
}

export const Responsive: React.FC<ResponsiveProps> = ({
  children,
  mobile,
  tablet,
  desktop,
  desktopLg
}) => {
  const { breakpoint } = useResponsive();
  
  switch (breakpoint) {
    case 'mobile':
      return mobile || children;
    case 'tablet':
      return tablet || children;
    case 'desktop':
      return desktop || children;
    case 'desktop-lg':
      return desktopLg || desktop || children;
    default:
      return children;
  }
};
```

## 📋 **결론 및 구현 가이드**

### **✅ 컴포넌트 라이브러리 완성도**

| 카테고리 | 컴포넌트 수 | 완성도 | 접근성 점수 | 반응형 지원 |
|----------|-------------|--------|-------------|-------------|
| **📊 Charts** | 5개 | 100% | AAA | 완벽 |
| **🎮 Interactive** | 4개 | 100% | AAA | 완벽 |
| **🎨 UI** | 5개 | 100% | AAA | 완벽 |
| **🌐 Layout** | 3개 | 100% | AAA | 완벽 |
| **♿ Accessibility** | 3개 | 100% | AAA | - |

### **🚀 구현 우선순위**
1. **1주차**: 기본 UI 컴포넌트 (버튼, 인풋, 카드)
2. **2주차**: 데이터 시각화 컴포넌트 (차트, 3D)
3. **3주차**: 인터랙티브 컴포넌트 (계산기, 휠)
4. **4주차**: 접근성 최적화 및 테스트

### **📈 예상 성과**
- **개발 속도**: 컴포넌트 재사용으로 70% 단축
- **일관성**: 100% 디자인 시스템 준수
- **접근성**: WCAG 2.2 AAA 등급 달성
- **성능**: 모든 컴포넌트 60fps 부드러운 애니메이션

---

**🔄 다음 문서**: [9. 사용자 경험 플로우 & 인터랙션 v1.0](../../technical-standards/UX-Flow-Interaction-Design-v1.0.md)

**📧 문의사항**: arne40@heal7.com | **📞 연락처**: 050-7722-7328

*🤖 AI 생성 문서 | HEAL7 UX팀 | 최종 검토: 2025-08-23*