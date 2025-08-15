'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, useAnimation } from 'framer-motion'
import { cn } from '@/lib/utils'
import { RotateCcw, Maximize2, Info } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { TaegeukSymbol } from './radial-chart'

interface WheelSection {
  id: string
  label: string
  value: string
  description?: string
  color: string
  position: {
    angle: number
    radius: number
  }
  metadata?: Record<string, any>
}

interface InteractiveWheelProps {
  sections: WheelSection[]
  centerContent?: React.ReactNode
  size?: number
  className?: string
  interactive?: boolean
  autoRotate?: boolean
  showControls?: boolean
  onSectionClick?: (section: WheelSection) => void
}

export function InteractiveWheel({
  sections,
  centerContent,
  size = 400,
  className,
  interactive = true,
  autoRotate = false,
  showControls = true,
  onSectionClick,
}: InteractiveWheelProps) {
  const [selectedSection, setSelectedSection] = useState<string | null>(null)
  const [isRotating, setIsRotating] = useState(false)
  const [rotationAngle, setRotationAngle] = useState(0)
  const wheelRef = useRef<HTMLDivElement>(null)
  const controls = useAnimation()

  // 자동 회전 효과
  useEffect(() => {
    if (autoRotate && !isRotating) {
      const interval = setInterval(() => {
        setRotationAngle(prev => prev + 1)
      }, 50)
      return () => clearInterval(interval)
    }
  }, [autoRotate, isRotating])

  // 수동 회전 트리거
  const startRotation = async () => {
    setIsRotating(true)
    await controls.start({ 
      rotate: rotationAngle + 360,
      transition: { duration: 2, ease: 'easeOut' }
    })
    setRotationAngle(prev => prev + 360)
    setIsRotating(false)
  }

  // 섹션 클릭 핸들러
  const handleSectionClick = (section: WheelSection) => {
    if (!interactive) return
    
    setSelectedSection(selectedSection === section.id ? null : section.id)
    onSectionClick?.(section)
  }

  // 섹션별 위치 계산
  const getSectionPosition = (section: WheelSection, index: number) => {
    const baseAngle = section.position?.angle ?? (360 / sections.length) * index
    const radius = section.position?.radius ?? size / 3
    const angle = (baseAngle + rotationAngle) * (Math.PI / 180)
    
    return {
      x: size / 2 + Math.cos(angle) * radius,
      y: size / 2 + Math.sin(angle) * radius,
      angle: baseAngle + rotationAngle,
    }
  }

  return (
    <div className={cn('relative', className)}>
      {/* 컨트롤 버튼들 */}
      {showControls && (
        <div className="absolute top-4 right-4 flex gap-2 z-20">
          <Button
            variant="ghost"
            size="sm"
            onClick={startRotation}
            disabled={isRotating}
            className="bg-slate-800/80 backdrop-blur-sm hover:bg-slate-700/80"
          >
            <RotateCcw className={cn('w-4 h-4', isRotating && 'animate-spin')} />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="bg-slate-800/80 backdrop-blur-sm hover:bg-slate-700/80"
          >
            <Maximize2 className="w-4 h-4" />
          </Button>
        </div>
      )}

      {/* 메인 휠 컨테이너 */}
      <motion.div
        ref={wheelRef}
        className="relative"
        style={{ width: size, height: size }}
        animate={controls}
      >
        {/* 배경 원들 */}
        <div className="absolute inset-0">
          {/* 외부 링 */}
          <div 
            className="absolute border-4 border-purple-500/30 rounded-full"
            style={{
              width: size,
              height: size,
              background: `conic-gradient(
                from 0deg,
                #8b5cf6 0deg,
                #06b6d4 90deg,
                #eab308 180deg,
                #ef4444 270deg,
                #8b5cf6 360deg
              )`,
              padding: '4px'
            }}
          >
            <div className="w-full h-full rounded-full bg-slate-900/90 backdrop-blur-sm" />
          </div>
          
          {/* 중간 링 */}
          <div 
            className="absolute border-2 border-slate-600/50 rounded-full bg-slate-800/30"
            style={{
              width: size * 0.8,
              height: size * 0.8,
              top: size * 0.1,
              left: size * 0.1,
            }}
          />
          
          {/* 내부 링 */}
          <div 
            className="absolute border border-slate-700/50 rounded-full bg-slate-900/50"
            style={{
              width: size * 0.6,
              height: size * 0.6,
              top: size * 0.2,
              left: size * 0.2,
            }}
          />
        </div>

        {/* 섹션들 */}
        {sections.map((section, index) => {
          const position = getSectionPosition(section, index)
          const isSelected = selectedSection === section.id
          
          return (
            <motion.div
              key={section.id}
              className={cn(
                'absolute cursor-pointer transition-all duration-300',
                isSelected ? 'scale-110 z-10' : 'hover:scale-105',
                interactive ? 'pointer-events-auto' : 'pointer-events-none'
              )}
              style={{
                left: position.x - 40,
                top: position.y - 40,
                width: 80,
                height: 80,
              }}
              animate={{
                rotate: -position.angle, // 텍스트가 항상 수평이 되도록
              }}
              onClick={() => handleSectionClick(section)}
              whileHover={interactive ? { scale: 1.1 } : undefined}
              whileTap={interactive ? { scale: 0.95 } : undefined}
            >
              <Card 
                className={cn(
                  'w-full h-full border-slate-600/50 bg-slate-800/90 backdrop-blur-sm',
                  isSelected && 'ring-2 ring-purple-400/50'
                )}
              >
                <CardContent className="p-3 text-center flex flex-col justify-center h-full">
                  <div className="text-xs text-slate-400 mb-1">{section.label}</div>
                  <div 
                    className="text-lg font-bold text-white"
                    style={{ color: section.color }}
                  >
                    {section.value}
                  </div>
                </CardContent>
              </Card>
              
              {/* 글로우 효과 */}
              {isSelected && (
                <div 
                  className="absolute inset-0 rounded-lg blur-xl -z-10 animate-pulse"
                  style={{ backgroundColor: `${section.color}40` }}
                />
              )}
            </motion.div>
          )
        })}

        {/* 중앙 콘텐츠 */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.div
            className="text-center"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            {centerContent || <TaegeukSymbol size={60} />}
          </motion.div>
        </div>

        {/* 연결선들 (옵션) */}
        <svg 
          className="absolute inset-0 pointer-events-none"
          width={size}
          height={size}
        >
          {sections.map((section, index) => {
            const position = getSectionPosition(section, index)
            const centerX = size / 2
            const centerY = size / 2
            
            return (
              <motion.line
                key={`line-${section.id}`}
                x1={centerX}
                y1={centerY}
                x2={position.x}
                y2={position.y}
                stroke="url(#lineGradient)"
                strokeWidth="1"
                opacity="0.3"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
              />
            )
          })}
          
          <defs>
            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#8b5cf6" />
              <stop offset="100%" stopColor="transparent" />
            </linearGradient>
          </defs>
        </svg>
      </motion.div>

      {/* 선택된 섹션 정보 표시 */}
      {selectedSection && (
        <motion.div
          className="absolute top-full left-1/2 transform -translate-x-1/2 mt-6 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg p-4 shadow-xl min-w-[300px] z-20"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
          {(() => {
            const section = sections.find(s => s.id === selectedSection)
            if (!section) return null
            
            return (
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Info className="w-4 h-4 text-purple-400" />
                  <h4 className="text-slate-200 font-medium">{section.label} 상세정보</h4>
                </div>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-400">값:</span>
                    <span className="text-white font-medium">{section.value}</span>
                  </div>
                  
                  {section.description && (
                    <div className="flex justify-between">
                      <span className="text-slate-400">설명:</span>
                      <span className="text-slate-300">{section.description}</span>
                    </div>
                  )}
                  
                  {section.metadata && Object.entries(section.metadata).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-slate-400">{key}:</span>
                      <span className="text-slate-300">{String(value)}</span>
                    </div>
                  ))}
                </div>
                
                <button
                  onClick={() => setSelectedSection(null)}
                  className="mt-3 text-xs text-slate-500 hover:text-slate-300 transition-colors"
                >
                  닫기
                </button>
              </div>
            )
          })()}
        </motion.div>
      )}
    </div>
  )
}

// 사주 기둥용 특화 휠
interface SajuPillar {
  천간: string
  지지: string
  한자천간: string
  한자지지: string
}

interface SajuWheelProps {
  pillars: {
    년주: SajuPillar
    월주: SajuPillar
    일주: SajuPillar
    시주: SajuPillar
  }
  className?: string
  size?: number
}

// 천간지지 한자 매핑
const CHEONGAN_HANJA = {
  '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
  '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸'
}

const JIJI_HANJA = {
  '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳',
  '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
}

export function SajuWheel({ pillars, className, size = 350 }: SajuWheelProps) {
  const sections: WheelSection[] = [
    {
      id: '년주',
      label: '年柱 (년주)',
      value: `${CHEONGAN_HANJA[pillars.년주.천간 as keyof typeof CHEONGAN_HANJA]}${JIJI_HANJA[pillars.년주.지지 as keyof typeof JIJI_HANJA]}`,
      description: '조상·유년기 운세',
      color: '#ef4444',
      position: { angle: 0, radius: size / 3 },
      metadata: {
        천간: pillars.년주.천간,
        지지: pillars.년주.지지,
        한자: `${pillars.년주.한자천간}${pillars.년주.한자지지}`,
      }
    },
    {
      id: '월주',
      label: '月柱 (월주)',
      value: `${CHEONGAN_HANJA[pillars.월주.천간 as keyof typeof CHEONGAN_HANJA]}${JIJI_HANJA[pillars.월주.지지 as keyof typeof JIJI_HANJA]}`,
      description: '부모·청년기 운세',
      color: '#eab308',
      position: { angle: 90, radius: size / 3 },
      metadata: {
        천간: pillars.월주.천간,
        지지: pillars.월주.지지,
        한자: `${pillars.월주.한자천간}${pillars.월주.한자지지}`,
      }
    },
    {
      id: '일주',
      label: '日柱 (일주)',
      value: `${CHEONGAN_HANJA[pillars.일주.천간 as keyof typeof CHEONGAN_HANJA]}${JIJI_HANJA[pillars.일주.지지 as keyof typeof JIJI_HANJA]}`,
      description: '본인·배우자 운세',
      color: '#8b5cf6',
      position: { angle: 180, radius: size / 3 },
      metadata: {
        천간: pillars.일주.천간,
        지지: pillars.일주.지지,
        한자: `${pillars.일주.한자천간}${pillars.일주.한자지지}`,
        특이사항: '가장 중요한 기둥',
      }
    },
    {
      id: '시주',
      label: '時柱 (시주)',
      value: `${CHEONGAN_HANJA[pillars.시주.천간 as keyof typeof CHEONGAN_HANJA]}${JIJI_HANJA[pillars.시주.지지 as keyof typeof JIJI_HANJA]}`,
      description: '자식·노년기 운세',
      color: '#06b6d4',
      position: { angle: 270, radius: size / 3 },
      metadata: {
        천간: pillars.시주.천간,
        지지: pillars.시주.지지,
        한자: `${pillars.시주.한자천간}${pillars.시주.한자지지}`,
      }
    },
  ]

  return (
    <div className={className}>
      <InteractiveWheel
        sections={sections}
        size={size}
        centerContent={
          <div className="text-center">
            <TaegeukSymbol size={50} />
            <div className="mt-2 text-xs text-slate-400">사주 4기둥</div>
          </div>
        }
        showControls
        interactive
      />
    </div>
  )
}