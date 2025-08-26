import React, { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Points, PointMaterial } from '@react-three/drei'
import { Points as ThreePoints, BufferAttribute } from 'three'

interface OptimizedStarsProps {
  radius?: number
  depth?: number
  count?: number
  factor?: number
  saturation?: number
  fade?: boolean
  speed?: number
  performanceLevel?: 'low' | 'medium' | 'high'
}

const OptimizedStars: React.FC<OptimizedStarsProps> = ({
  radius = 100,
  depth = 50,
  count = 1000,
  factor = 4,
  fade = false,
  speed = 1,
  performanceLevel = 'medium'
}) => {
  const ref = useRef<ThreePoints>(null!)
  const opacityRef = useRef<Float32Array>(null!)
  
  // 성능 기반 별 개수 조정
  const adjustedCount = useMemo(() => {
    const multiplier = {
      low: 0.3,
      medium: 0.6,
      high: 1.0
    }[performanceLevel]
    
    return Math.floor(count * multiplier)
  }, [count, performanceLevel])

  // 메모이제이션된 별 위치와 투명도 생성
  const { positions, opacities, twinklePhases } = useMemo(() => {
    const positions = new Float32Array(adjustedCount * 3)
    const opacities = new Float32Array(adjustedCount)
    const twinklePhases = new Float32Array(adjustedCount)
    
    for (let i = 0; i < adjustedCount; i++) {
      const r = radius + Math.random() * depth
      const theta = 2 * Math.PI * Math.random()
      const phi = Math.acos(2 * Math.random() - 1)
      
      const x = r * Math.sin(phi) * Math.cos(theta)
      const y = r * Math.sin(phi) * Math.sin(theta)
      const z = r * Math.cos(phi)
      
      positions[i * 3] = x
      positions[i * 3 + 1] = y
      positions[i * 3 + 2] = z
      
      // 초기 투명도와 반짝임 위상 설정
      opacities[i] = 0.3 + Math.random() * 0.7
      twinklePhases[i] = Math.random() * Math.PI * 2
    }
    
    opacityRef.current = opacities
    
    return { positions, opacities, twinklePhases }
  }, [adjustedCount, radius, depth])

  // 최적화된 애니메이션 (저성능에서는 제한)
  useFrame((state, delta) => {
    if (!ref.current) return
    
    // 회전 애니메이션 (저성능에서는 제한)
    if (performanceLevel !== 'low') {
      ref.current.rotation.x -= delta * 0.05 * speed
      ref.current.rotation.y -= delta * 0.075 * speed
    }
    
    // 반짝임 효과 (모든 성능 레벨에서 실행)
    if (opacityRef.current && ref.current.geometry.attributes.opacity) {
      const time = state.clock.elapsedTime
      
      for (let i = 0; i < adjustedCount; i++) {
        const baseOpacity = 0.3 + Math.random() * 0.1
        const twinkle = Math.sin(time * 2 + twinklePhases[i]) * 0.4 + 0.6
        opacityRef.current[i] = baseOpacity * twinkle
      }
      
      ;(ref.current.geometry.attributes.opacity as BufferAttribute).needsUpdate = true
    }
  })

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points
        ref={ref}
        positions={positions}
        stride={3}
        frustumCulled={true}
      >
        <bufferAttribute
          attach="geometry-attributes-opacity"
          array={opacities}
          count={adjustedCount}
          itemSize={1}
        />
        <PointMaterial
          transparent
          color={fade ? "#ffffff" : "#ddddff"}
          size={factor * 0.2}
          sizeAttenuation={true}
          depthWrite={false}
          vertexColors={false}
        />
      </Points>
    </group>
  )
}

export default OptimizedStars