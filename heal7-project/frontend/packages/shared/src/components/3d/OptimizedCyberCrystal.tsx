import React, { useRef, useMemo, Suspense, useEffect, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Mesh } from 'three'
import { MeshDistortMaterial } from '@react-three/drei'

// 성능 감지 및 품질 설정
const getPerformanceLevel = (): 'low' | 'medium' | 'high' => {
  try {
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl') as WebGLRenderingContext | null
    
    if (!gl) return 'low'
    
    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info')
    if (debugInfo) {
      const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) as string
      // GPU 성능 추정
      if (renderer.includes('Intel HD') || renderer.includes('Mali')) return 'low'
      if (renderer.includes('GTX') || renderer.includes('RTX') || renderer.includes('Radeon')) return 'high'
    }
  } catch (error) {
    // WebGL 감지 실패 시 메모리로만 판단
  }
  
  // 메모리 기반 추정
  const memory = (navigator as any).deviceMemory || 4
  if (memory < 4) return 'low'
  if (memory >= 8) return 'high'
  
  return 'medium'
}

// 품질별 설정
const QUALITY_SETTINGS = {
  low: {
    starCount: 500,
    crystalCount: 3,
    animationSpeed: 0.5,
    materialQuality: 'basic'
  },
  medium: {
    starCount: 1500,
    crystalCount: 5,
    animationSpeed: 0.8,
    materialQuality: 'standard'
  },
  high: {
    starCount: 2000,
    crystalCount: 8,
    animationSpeed: 1.0,
    materialQuality: 'premium'
  }
}

interface OptimizedCyberCrystalProps {
  isVisible?: boolean
  reduced?: boolean
}

const OptimizedCyberCrystal: React.FC<OptimizedCyberCrystalProps> = ({ 
  isVisible = true, 
  reduced = false 
}) => {
  const meshRef = useRef<Mesh>(null!)
  const { viewport, camera } = useThree()
  const [isPageVisible, setIsPageVisible] = useState(true)
  const [performanceLevel] = useState(() => getPerformanceLevel())
  
  // 페이지 가시성 API - 백그라운드에서 애니메이션 정지
  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsPageVisible(!document.hidden)
    }
    
    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange)
  }, [])

  // 성능 기반 설정
  const settings = reduced ? QUALITY_SETTINGS.low : QUALITY_SETTINGS[performanceLevel]
  
  // 메모이제이션된 크리스탈 위치
  const crystalPositions = useMemo(() => 
    Array.from({ length: settings.crystalCount }, (_, index) => ({
      position: [
        (Math.random() - 0.5) * viewport.width * 0.6,
        (Math.random() - 0.5) * viewport.height * 0.6,
        (Math.random() - 0.5) * 8
      ] as [number, number, number],
      rotation: [Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI] as [number, number, number],
      scale: 0.2 + Math.random() * 0.4,
      color: index % 3 === 0 ? "#8B5CF6" : index % 3 === 1 ? "#EC4899" : "#06B6D4"
    }))
  , [viewport.width, viewport.height, settings.crystalCount])

  // 최적화된 애니메이션 루프
  useFrame((state, delta) => {
    // 페이지가 보이지 않으면 애니메이션 정지
    if (!meshRef.current || !isPageVisible || !isVisible) return
    
    const adjustedDelta = delta * settings.animationSpeed
    
    meshRef.current.rotation.x += adjustedDelta * 0.15
    meshRef.current.rotation.y += adjustedDelta * 0.08
    
    // 부유 효과 (더 부드럽게)
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.2
  })

  // 카메라 거리에 따른 LOD (Level of Detail)
  const cameraDistance = camera.position.distanceTo({ x: 0, y: 0, z: 0 })
  const shouldRenderDetails = cameraDistance < 10

  if (!isVisible) return null

  return (
    <Suspense fallback={null}>
      {/* 메인 크리스탈 */}
      <mesh ref={meshRef} position={[0, 0, 0]}>
        <octahedronGeometry args={[0.8, shouldRenderDetails ? 1 : 0]} />
        {settings.materialQuality === 'basic' ? (
          <meshStandardMaterial
            color="#6366F1"
            transparent
            opacity={0.7}
            metalness={0.6}
            roughness={0.2}
          />
        ) : (
          <MeshDistortMaterial
            color="#6366F1"
            transparent
            opacity={0.8}
            distort={performanceLevel === 'low' ? 0.1 : 0.3}
            speed={settings.animationSpeed}
            roughness={0.1}
            metalness={0.8}
          />
        )}
      </mesh>

      {/* 주변 소형 크리스탈들 */}
      {crystalPositions.map((crystal, index) => (
        <mesh
          key={index}
          position={crystal.position}
          rotation={crystal.rotation}
          scale={crystal.scale}
        >
          <octahedronGeometry args={[0.3, 0]} />
          {settings.materialQuality === 'basic' ? (
            <meshStandardMaterial
              color={crystal.color}
              transparent
              opacity={0.5}
              metalness={0.4}
              roughness={0.3}
            />
          ) : (
            <MeshDistortMaterial
              color={crystal.color}
              transparent
              opacity={0.4}
              distort={0.1}
              speed={0.5 + index * 0.05}
              roughness={0.2}
              metalness={0.6}
            />
          )}
        </mesh>
      ))}

      {/* 조건부 조명 - 고성능에서만 */}
      {performanceLevel !== 'low' && (
        <>
          <pointLight 
            position={[5, 5, 5]} 
            intensity={0.6} 
            color="#6366F1" 
            distance={20}
            decay={2}
          />
          <pointLight 
            position={[-5, -5, -5]} 
            intensity={0.4} 
            color="#EC4899" 
            distance={15}
            decay={2}
          />
        </>
      )}
      
    </Suspense>
  )
}

export default OptimizedCyberCrystal