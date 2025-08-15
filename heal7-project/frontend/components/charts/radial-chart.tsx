'use client'

import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface RadialChartData {
  label: string
  value: number
  color: string
  description?: string
}

interface RadialChartProps {
  data: RadialChartData[]
  size?: number
  centerContent?: React.ReactNode
  interactive?: boolean
  pulseAnimation?: boolean
  showLabels?: boolean
  className?: string
}

export function RadialChart({
  data,
  size = 300,
  centerContent,
  interactive = false,
  pulseAnimation = false,
  showLabels = true,
  className,
}: RadialChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null)
  
  const total = data.reduce((sum, item) => sum + item.value, 0)
  const radius = size / 2 - 40
  const strokeWidth = 20
  const circumference = 2 * Math.PI * radius

  // 각 섹션의 각도 계산
  let cumulativePercentage = 0
  const sections = data.map((item, index) => {
    const percentage = item.value / total
    const startAngle = cumulativePercentage * 360
    const endAngle = (cumulativePercentage + percentage) * 360
    const arcLength = percentage * circumference
    
    cumulativePercentage += percentage
    
    return {
      ...item,
      percentage,
      startAngle,
      endAngle,
      arcLength,
      strokeDasharray: `${arcLength} ${circumference - arcLength}`,
      strokeDashoffset: -cumulativePercentage * circumference + arcLength,
    }
  })

  return (
    <div className={cn('relative inline-block', className)}>
      <svg width={size} height={size} className="transform -rotate-90">
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
        
        {/* 데이터 섹션들 */}
        {sections.map((section, index) => {
          const isHovered = hoveredIndex === index
          const isSelected = selectedIndex === index
          const currentStrokeWidth = isHovered || isSelected ? strokeWidth + 4 : strokeWidth
          
          return (
            <g key={section.label}>
              {/* 메인 아크 */}
              <motion.circle
                cx={size / 2}
                cy={size / 2}
                r={radius}
                fill="transparent"
                stroke={section.color}
                strokeWidth={currentStrokeWidth}
                strokeLinecap="round"
                strokeDasharray={section.strokeDasharray}
                strokeDashoffset={section.strokeDashoffset}
                initial={{ strokeDasharray: `0 ${circumference}` }}
                animate={{ 
                  strokeDasharray: section.strokeDasharray,
                  strokeWidth: currentStrokeWidth,
                }}
                transition={{ 
                  duration: 1,
                  delay: index * 0.1,
                  ease: 'easeOut'
                }}
                style={{
                  filter: isHovered || isSelected ? `drop-shadow(0 0 8px ${section.color})` : undefined,
                  cursor: interactive ? 'pointer' : 'default',
                }}
                onMouseEnter={() => interactive && setHoveredIndex(index)}
                onMouseLeave={() => interactive && setHoveredIndex(null)}
                onClick={() => interactive && setSelectedIndex(selectedIndex === index ? null : index)}
              />
              
              {/* 펄스 애니메이션 */}
              {pulseAnimation && (
                <motion.circle
                  cx={size / 2}
                  cy={size / 2}
                  r={radius}
                  fill="transparent"
                  stroke={section.color}
                  strokeWidth={2}
                  strokeDasharray={section.strokeDasharray}
                  strokeDashoffset={section.strokeDashoffset}
                  opacity={0}
                  animate={{
                    r: [radius, radius + 10],
                    opacity: [0.5, 0],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: index * 0.3,
                  }}
                />
              )}
            </g>
          )
        })}
      </svg>
      
      {/* 중앙 콘텐츠 */}
      {centerContent && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            {centerContent}
          </div>
        </div>
      )}
      
      {/* 라벨들 */}
      {showLabels && (
        <div className="absolute inset-0" style={{ pointerEvents: 'none' }}>
          {sections.map((section, index) => {
            const angle = ((section.startAngle + section.endAngle) / 2) * (Math.PI / 180)
            const labelRadius = radius + 30
            const x = size / 2 + Math.cos(angle - Math.PI / 2) * labelRadius
            const y = size / 2 + Math.sin(angle - Math.PI / 2) * labelRadius
            
            return (
              <motion.div
                key={section.label}
                className="absolute text-xs font-medium text-slate-300 text-center"
                style={{
                  left: x - 20,
                  top: y - 10,
                  width: 40,
                  transform: 'translate(-50%, -50%)',
                }}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 + 0.5 }}
              >
                <div>{section.label}</div>
                <div className="text-white font-bold">{section.value}</div>
              </motion.div>
            )
          })}
        </div>
      )}
      
      {/* 호버/선택 정보 표시 */}
      {interactive && (hoveredIndex !== null || selectedIndex !== null) && (
        <motion.div
          className="absolute top-full left-1/2 transform -translate-x-1/2 mt-4 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg p-3 shadow-xl min-w-[200px] z-20"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {(() => {
            const activeIndex = selectedIndex !== null ? selectedIndex : hoveredIndex
            const activeSection = sections[activeIndex!]
            return (
              <div className="text-center">
                <div className="text-sm font-medium text-slate-300 mb-1">
                  {activeSection.label}
                </div>
                <div className="text-lg font-bold text-white mb-1">
                  {activeSection.value} ({Math.round(activeSection.percentage * 100)}%)
                </div>
                {activeSection.description && (
                  <div className="text-xs text-slate-400">
                    {activeSection.description}
                  </div>
                )}
              </div>
            )
          })()}
        </motion.div>
      )}
    </div>
  )
}

// 십신 분석용 특화 컴포넌트
export const SIPSIN_COLORS = {
  비겁: { color: '#8b5cf6', label: '비견겁재' },
  식상: { color: '#06b6d4', label: '식신상관' },
  재성: { color: '#eab308', label: '편재정재' },
  관살: { color: '#ef4444', label: '편관정관' },
  인성: { color: '#22c55e', label: '편인정인' },
}

interface SipsinRadialChartProps {
  sipsinData: Record<string, number>
  className?: string
  size?: number
}

export function SipsinRadialChart({
  sipsinData,
  className,
  size = 250,
}: SipsinRadialChartProps) {
  const data: RadialChartData[] = Object.entries(sipsinData).map(([sipsin, value]) => ({
    label: sipsin,
    value,
    color: SIPSIN_COLORS[sipsin as keyof typeof SIPSIN_COLORS]?.color || '#8b5cf6',
    description: SIPSIN_COLORS[sipsin as keyof typeof SIPSIN_COLORS]?.label,
  }))

  const total = Object.values(sipsinData).reduce((sum, value) => sum + value, 0)

  return (
    <div className={className}>
      <RadialChart
        data={data}
        size={size}
        interactive
        pulseAnimation
        centerContent={
          <div>
            <motion.div
              className="text-2xl font-bold text-white mb-1"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.5 }}
            >
              {total}
            </motion.div>
            <div className="text-xs text-slate-400">총 십신</div>
          </div>
        }
      />
    </div>
  )
}

// 다층 방사형 차트
interface MultiLayerRadialChartProps {
  layers: Array<{
    data: RadialChartData[]
    radius: number
    strokeWidth: number
  }>
  size?: number
  className?: string
}

export function MultiLayerRadialChart({
  layers,
  size = 300,
  className,
}: MultiLayerRadialChartProps) {
  return (
    <div className={cn('relative inline-block', className)}>
      <svg width={size} height={size} className="transform -rotate-90">
        {layers.map((layer, layerIndex) => {
          const total = layer.data.reduce((sum, item) => sum + item.value, 0)
          const circumference = 2 * Math.PI * layer.radius
          
          let cumulativePercentage = 0
          
          return layer.data.map((item, itemIndex) => {
            const percentage = item.value / total
            const arcLength = percentage * circumference
            const strokeDasharray = `${arcLength} ${circumference - arcLength}`
            const strokeDashoffset = -cumulativePercentage * circumference
            
            cumulativePercentage += percentage
            
            return (
              <motion.circle
                key={`${layerIndex}-${itemIndex}`}
                cx={size / 2}
                cy={size / 2}
                r={layer.radius}
                fill="transparent"
                stroke={item.color}
                strokeWidth={layer.strokeWidth}
                strokeLinecap="round"
                strokeDasharray={strokeDasharray}
                strokeDashoffset={strokeDashoffset}
                initial={{ strokeDasharray: `0 ${circumference}` }}
                animate={{ strokeDasharray }}
                transition={{ 
                  duration: 1,
                  delay: layerIndex * 0.5 + itemIndex * 0.1,
                  ease: 'easeOut'
                }}
              />
            )
          })
        })}
      </svg>
    </div>
  )
}

// 태극 심볼 컴포넌트 (사주 차트 중앙용)
export function TaegeukSymbol({ 
  size = 40, 
  className 
}: { 
  size?: number
  className?: string 
}) {
  return (
    <motion.div 
      className={cn('rounded-full relative', className)}
      style={{ width: size, height: size }}
      initial={{ scale: 0, rotate: 0 }}
      animate={{ scale: 1, rotate: 360 }}
      transition={{ duration: 2, ease: 'easeOut' }}
    >
      <div className="w-full h-full rounded-full bg-gradient-to-br from-white via-slate-200 to-black relative overflow-hidden">
        <div className="absolute top-0 left-1/2 w-1/2 h-1/2 bg-white rounded-tl-full"></div>
        <div className="absolute bottom-0 right-1/2 w-1/2 h-1/2 bg-black rounded-br-full"></div>
        <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 w-1/5 h-1/5 bg-black rounded-full"></div>
        <div className="absolute bottom-1/4 right-1/2 transform translate-x-1/2 w-1/5 h-1/5 bg-white rounded-full"></div>
      </div>
    </motion.div>
  )
}