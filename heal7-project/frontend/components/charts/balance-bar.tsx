'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

// 오행 색상 매핑 (사주 시스템에서 가져옴)
export const WUXING_COLORS = {
  목: { primary: '#22c55e', secondary: '#16a34a', glow: 'rgba(34, 197, 94, 0.3)' },
  화: { primary: '#ef4444', secondary: '#dc2626', glow: 'rgba(239, 68, 68, 0.3)' },
  토: { primary: '#eab308', secondary: '#ca8a04', glow: 'rgba(234, 179, 8, 0.3)' },
  금: { primary: '#f3f4f6', secondary: '#d1d5db', glow: 'rgba(243, 244, 246, 0.3)' },
  수: { primary: '#3b82f6', secondary: '#2563eb', glow: 'rgba(59, 130, 246, 0.3)' },
}

interface BalanceBarItem {
  label: string
  value: number
  max?: number
  color?: {
    primary: string
    secondary?: string
    glow?: string
  }
}

interface BalanceBarProps {
  items: BalanceBarItem[]
  showGlow?: boolean
  interactive?: boolean
  animationDelay?: number
  className?: string
  variant?: 'horizontal' | 'vertical'
  showValues?: boolean
  showPercentages?: boolean
}

export function BalanceBar({
  items,
  showGlow = false,
  interactive = false,
  animationDelay = 100,
  className,
  variant = 'horizontal',
  showValues = true,
  showPercentages = false,
}: BalanceBarProps) {
  const [animatedValues, setAnimatedValues] = useState<number[]>(new Array(items.length).fill(0))
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)

  const maxValue = Math.max(...items.map(item => item.max || 100))

  useEffect(() => {
    items.forEach((item, index) => {
      setTimeout(() => {
        setAnimatedValues(prev => {
          const newValues = [...prev]
          newValues[index] = item.value
          return newValues
        })
      }, index * animationDelay)
    })
  }, [items, animationDelay])

  if (variant === 'vertical') {
    return (
      <div className={cn('flex gap-4', className)}>
        {items.map((item, index) => {
          const percentage = (animatedValues[index] / maxValue) * 100
          const isHovered = hoveredIndex === index

          return (
            <div
              key={item.label}
              className="flex flex-col items-center"
              onMouseEnter={() => interactive && setHoveredIndex(index)}
              onMouseLeave={() => interactive && setHoveredIndex(null)}
            >
              {/* 세로 바 */}
              <div className="relative w-8 h-32 bg-slate-700 rounded-full overflow-hidden">
                <motion.div
                  className="absolute bottom-0 w-full rounded-full"
                  style={{
                    background: item.color?.secondary 
                      ? `linear-gradient(to top, ${item.color.primary}, ${item.color.secondary})`
                      : item.color?.primary || '#8b5cf6',
                    boxShadow: showGlow && item.color?.glow 
                      ? `0 0 15px ${item.color.glow}`
                      : undefined,
                  }}
                  initial={{ height: 0 }}
                  animate={{ 
                    height: `${percentage}%`,
                    boxShadow: showGlow && isHovered && item.color?.glow
                      ? `0 0 25px ${item.color.glow}`
                      : showGlow && item.color?.glow
                      ? `0 0 15px ${item.color.glow}`
                      : undefined,
                  }}
                  transition={{ 
                    duration: 1,
                    ease: 'easeOut',
                    delay: index * (animationDelay / 1000)
                  }}
                />
                
                {/* 값 표시 */}
                {showValues && (
                  <motion.div
                    className="absolute inset-0 flex items-end justify-center pb-1"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: (index * animationDelay / 1000) + 0.5 }}
                  >
                    <span className="text-xs font-bold text-white rotate-90 origin-center">
                      {showPercentages ? `${Math.round(percentage)}%` : animatedValues[index]}
                    </span>
                  </motion.div>
                )}
              </div>
              
              {/* 라벨 */}
              <div className="mt-2 text-center">
                <div className="text-sm font-medium text-white">{item.label}</div>
              </div>
            </div>
          )
        })}
      </div>
    )
  }

  return (
    <div className={cn('space-y-3', className)}>
      {items.map((item, index) => {
        const itemMax = item.max || maxValue
        const percentage = (animatedValues[index] / itemMax) * 100
        const isHovered = hoveredIndex === index

        return (
          <div
            key={item.label}
            className={cn(
              'flex items-center gap-3',
              interactive && 'cursor-pointer'
            )}
            onMouseEnter={() => interactive && setHoveredIndex(index)}
            onMouseLeave={() => interactive && setHoveredIndex(null)}
          >
            {/* 라벨 */}
            <div className="w-8 text-sm text-slate-300 font-medium flex-shrink-0">
              {item.label}
            </div>
            
            {/* 진행 바 */}
            <div className="flex-1 relative">
              <div className="h-6 bg-slate-700 rounded-full overflow-hidden">
                <motion.div
                  className="h-full rounded-full relative"
                  style={{
                    background: item.color?.secondary 
                      ? `linear-gradient(90deg, ${item.color.primary}, ${item.color.secondary})`
                      : item.color?.primary || '#8b5cf6',
                    boxShadow: showGlow && item.color?.glow 
                      ? `0 0 10px ${item.color.glow}`
                      : undefined,
                  }}
                  initial={{ width: 0 }}
                  animate={{ 
                    width: `${Math.min(percentage, 100)}%`,
                    boxShadow: showGlow && isHovered && item.color?.glow
                      ? `0 0 20px ${item.color.glow}`
                      : showGlow && item.color?.glow
                      ? `0 0 10px ${item.color.glow}`
                      : undefined,
                  }}
                  transition={{ 
                    duration: 1,
                    ease: 'easeOut',
                    delay: index * (animationDelay / 1000)
                  }}
                >
                  {/* 내부 하이라이트 효과 */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                </motion.div>
              </div>
              
              {/* 값 표시 */}
              {showValues && (
                <motion.div
                  className="absolute right-2 top-0 h-6 flex items-center"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: (index * animationDelay / 1000) + 0.5 }}
                >
                  <span className="text-xs text-white font-medium">
                    {showPercentages ? `${Math.round(percentage)}%` : animatedValues[index]}
                  </span>
                </motion.div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

// 오행 분석용 특화 컴포넌트
interface WuxingBalanceProps {
  wuxingData: Record<string, number>
  className?: string
  interactive?: boolean
  showAnalysis?: boolean
}

export function WuxingBalance({
  wuxingData,
  className,
  interactive = true,
  showAnalysis = true,
}: WuxingBalanceProps) {
  const items: BalanceBarItem[] = Object.entries(wuxingData).map(([wuxing, value]) => ({
    label: wuxing,
    value,
    color: WUXING_COLORS[wuxing as keyof typeof WUXING_COLORS] || {
      primary: '#8b5cf6',
      secondary: '#7c3aed',
      glow: 'rgba(139, 92, 246, 0.3)',
    },
  }))

  // 오행 균형 분석
  const analysis = showAnalysis ? analyzeWuxingBalance(wuxingData) : null

  return (
    <div className={className}>
      <BalanceBar
        items={items}
        showGlow
        interactive={interactive}
        showValues
        animationDelay={150}
      />
      
      {analysis && (
        <motion.div
          className="mt-4 p-3 bg-slate-800/50 rounded-lg"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
        >
          <h4 className="text-sm font-medium text-slate-200 mb-2">🔍 오행 균형 분석</h4>
          <div className="space-y-1 text-xs text-slate-400">
            <p>• 강한 오행: <span className="text-white font-medium">{analysis.strongest}</span></p>
            <p>• 약한 오행: <span className="text-white font-medium">{analysis.weakest}</span></p>
            <p>• 균형도: <span className="text-white font-medium">{analysis.balance}%</span></p>
            <p>• 조언: <span className="text-slate-300">{analysis.advice}</span></p>
          </div>
        </motion.div>
      )}
    </div>
  )
}

// 오행 균형 분석 함수
function analyzeWuxingBalance(wuxingData: Record<string, number>) {
  const values = Object.values(wuxingData)
  const entries = Object.entries(wuxingData)
  
  const max = Math.max(...values)
  const min = Math.min(...values)
  const strongest = entries.find(([, value]) => value === max)?.[0] || '목'
  const weakest = entries.find(([, value]) => value === min)?.[0] || '수'
  
  const balance = Math.round(100 - ((max - min) / max) * 100)
  
  const getAdvice = () => {
    if (balance >= 80) return '매우 균형잡힌 오행 분포입니다'
    if (balance >= 60) return `${weakest} 기운을 보강하면 더욱 좋습니다`
    if (balance >= 40) return `${strongest} 기운이 너무 강하니 조화를 이루세요`
    return '오행의 균형을 맞추는 것이 중요합니다'
  }

  return {
    strongest,
    weakest,
    balance,
    advice: getAdvice(),
  }
}

// 스택형 바 차트 컴포넌트
interface StackedBarProps {
  data: Array<{
    label: string
    segments: Array<{
      label: string
      value: number
      color: string
    }>
  }>
  height?: number
  className?: string
}

export function StackedBar({
  data,
  height = 32,
  className,
}: StackedBarProps) {
  const [animated, setAnimated] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setAnimated(true), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className={cn('space-y-4', className)}>
      {data.map((item, index) => {
        const total = item.segments.reduce((sum, segment) => sum + segment.value, 0)
        
        return (
          <div key={item.label} className="space-y-1">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-slate-300">{item.label}</span>
              <span className="text-xs text-slate-400">총 {total}</span>
            </div>
            
            <div 
              className="relative bg-slate-700 rounded-full overflow-hidden flex"
              style={{ height }}
            >
              {item.segments.map((segment, segmentIndex) => {
                const percentage = (segment.value / total) * 100
                
                return (
                  <motion.div
                    key={segment.label}
                    className="relative"
                    style={{ backgroundColor: segment.color }}
                    initial={{ width: 0 }}
                    animate={{ width: animated ? `${percentage}%` : 0 }}
                    transition={{ 
                      duration: 0.8,
                      delay: index * 0.1 + segmentIndex * 0.05,
                      ease: 'easeOut'
                    }}
                  >
                    {/* 세그먼트 라벨 (공간이 충분할 때만) */}
                    {percentage > 15 && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-xs font-medium text-white">
                          {segment.value}
                        </span>
                      </div>
                    )}
                  </motion.div>
                )
              })}
            </div>
            
            {/* 범례 */}
            <div className="flex flex-wrap gap-2 mt-2">
              {item.segments.map((segment) => (
                <div key={segment.label} className="flex items-center gap-1">
                  <div 
                    className="w-3 h-3 rounded-sm"
                    style={{ backgroundColor: segment.color }}
                  />
                  <span className="text-xs text-slate-400">{segment.label}</span>
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}