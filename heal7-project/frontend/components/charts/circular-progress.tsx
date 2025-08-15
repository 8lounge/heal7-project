'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface CircularProgressProps {
  value: number
  max?: number
  size?: number
  strokeWidth?: number
  gradient?: string
  glowEffect?: boolean
  animationDuration?: number
  showValue?: boolean
  className?: string
  children?: React.ReactNode
}

export function CircularProgress({
  value,
  max = 100,
  size = 120,
  strokeWidth = 8,
  gradient = 'from-purple-500 to-cyan-500',
  glowEffect = false,
  animationDuration = 2000,
  showValue = true,
  className,
  children,
}: CircularProgressProps) {
  const [animatedValue, setAnimatedValue] = useState(0)
  
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const percentage = (value / max) * 100
  const strokeDashoffset = circumference - (animatedValue / 100) * circumference

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedValue(percentage)
    }, 100)
    return () => clearTimeout(timer)
  }, [percentage])

  const gradientId = `gradient-${Math.random().toString(36).substr(2, 9)}`

  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg
        width={size}
        height={size}
        className={cn('transform -rotate-90', glowEffect && 'filter drop-shadow-lg')}
      >
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" className={`text-purple-500`} stopColor="currentColor" />
            <stop offset="100%" className={`text-cyan-500`} stopColor="currentColor" />
          </linearGradient>
        </defs>
        
        {/* 배경 원 */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-slate-700"
        />
        
        {/* 진행 원 */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke={`url(#${gradientId})`}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          animate={{ strokeDashoffset }}
          transition={{
            duration: animationDuration / 1000,
            ease: 'easeOut',
          }}
          style={{
            filter: glowEffect ? `drop-shadow(0 0 8px var(--glow-color, #8b5cf6))` : undefined,
          }}
        />
      </svg>
      
      {/* 중앙 내용 */}
      <div className="absolute inset-0 flex items-center justify-center">
        {children || (showValue && (
          <div className="text-center">
            <motion.div
              className="text-2xl font-bold text-white"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.5, duration: 0.5 }}
            >
              {Math.round(animatedValue)}
            </motion.div>
            {max === 100 && (
              <div className="text-xs text-slate-400">점</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

// 다중 링 진행률 컴포넌트
interface MultiRingProgressProps {
  data: Array<{
    label: string
    value: number
    max?: number
    color: string
  }>
  size?: number
  className?: string
}

export function MultiRingProgress({
  data,
  size = 150,
  className,
}: MultiRingProgressProps) {
  const strokeWidth = 6
  const gap = 12
  const centerRadius = 20

  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg width={size} height={size} className="transform -rotate-90">
        {data.map((item, index) => {
          const radius = centerRadius + (index * gap)
          const circumference = 2 * Math.PI * radius
          const percentage = (item.value / (item.max || 100)) * 100
          const strokeDashoffset = circumference - (percentage / 100) * circumference

          return (
            <g key={item.label}>
              {/* 배경 원 */}
              <circle
                cx={size / 2}
                cy={size / 2}
                r={radius}
                fill="transparent"
                stroke="currentColor"
                strokeWidth={strokeWidth}
                className="text-slate-700"
              />
              
              {/* 진행 원 */}
              <motion.circle
                cx={size / 2}
                cy={size / 2}
                r={radius}
                fill="transparent"
                stroke={item.color}
                strokeWidth={strokeWidth}
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={circumference}
                animate={{ strokeDashoffset }}
                transition={{
                  duration: 2,
                  delay: index * 0.2,
                  ease: 'easeOut',
                }}
              />
            </g>
          )
        })}
      </svg>
      
      {/* 중앙 레이블 */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg font-bold text-white">
            {data.reduce((sum, item) => sum + item.value, 0)}
          </div>
          <div className="text-xs text-slate-400">총합</div>
        </div>
      </div>
    </div>
  )
}

// 반원형 진행률 컴포넌트
interface SemiCircularProgressProps {
  value: number
  max?: number
  size?: number
  thickness?: number
  color?: string
  label?: string
  className?: string
}

export function SemiCircularProgress({
  value,
  max = 100,
  size = 120,
  thickness = 8,
  color = '#8b5cf6',
  label,
  className,
}: SemiCircularProgressProps) {
  const [animatedValue, setAnimatedValue] = useState(0)
  
  const radius = (size - thickness) / 2
  const circumference = Math.PI * radius // 반원이므로 π * r
  const percentage = (value / max) * 100
  const strokeDashoffset = circumference - (animatedValue / 100) * circumference

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedValue(percentage)
    }, 100)
    return () => clearTimeout(timer)
  }, [percentage])

  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg
        width={size}
        height={size / 2 + 20}
        className="transform"
        viewBox={`0 0 ${size} ${size / 2 + 20}`}
      >
        {/* 배경 반원 */}
        <path
          d={`M ${thickness / 2} ${size / 2} A ${radius} ${radius} 0 0 1 ${size - thickness / 2} ${size / 2}`}
          fill="transparent"
          stroke="currentColor"
          strokeWidth={thickness}
          className="text-slate-700"
        />
        
        {/* 진행 반원 */}
        <motion.path
          d={`M ${thickness / 2} ${size / 2} A ${radius} ${radius} 0 0 1 ${size - thickness / 2} ${size / 2}`}
          fill="transparent"
          stroke={color}
          strokeWidth={thickness}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          animate={{ strokeDashoffset }}
          transition={{
            duration: 2,
            ease: 'easeOut',
          }}
        />
      </svg>
      
      {/* 중앙 값 표시 */}
      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 text-center">
        <motion.div
          className="text-xl font-bold text-white"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          {Math.round(animatedValue)}%
        </motion.div>
        {label && (
          <div className="text-xs text-slate-400">{label}</div>
        )}
      </div>
    </div>
  )
}