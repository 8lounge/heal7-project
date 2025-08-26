import React, { useRef, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Mesh } from 'three'
import { Text, MeshDistortMaterial } from '@react-three/drei'

const CyberCrystal: React.FC = () => {
  const meshRef = useRef<Mesh>(null!)
  const { viewport } = useThree()

  // 크리스탈 위치 (무작위 배치)
  const crystalPositions = useMemo(() => 
    Array.from({ length: 8 }, () => ({
      position: [
        (Math.random() - 0.5) * viewport.width * 0.8,
        (Math.random() - 0.5) * viewport.height * 0.8,
        (Math.random() - 0.5) * 10
      ] as [number, number, number],
      rotation: [Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI] as [number, number, number],
      scale: 0.3 + Math.random() * 0.7
    }))
  , [viewport])

  // 애니메이션 루프
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.2
      meshRef.current.rotation.y += delta * 0.1
      
      // 부유 효과
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.3
    }
  })

  return (
    <>
      {/* 메인 크리스탈 */}
      <mesh ref={meshRef} position={[0, 0, 0]}>
        <octahedronGeometry args={[1, 0]} />
        <MeshDistortMaterial
          color="#6366F1"
          transparent
          opacity={0.8}
          distort={0.3}
          speed={2}
          roughness={0.1}
          metalness={0.8}
        />
      </mesh>

      {/* 주변 소형 크리스탈들 */}
      {crystalPositions.map((crystal, index) => (
        <mesh
          key={index}
          position={crystal.position}
          rotation={crystal.rotation}
          scale={crystal.scale}
        >
          <octahedronGeometry args={[0.5, 0]} />
          <MeshDistortMaterial
            color={index % 3 === 0 ? "#8B5CF6" : index % 3 === 1 ? "#EC4899" : "#06B6D4"}
            transparent
            opacity={0.4}
            distort={0.2}
            speed={1 + index * 0.1}
            roughness={0.2}
            metalness={0.6}
          />
        </mesh>
      ))}

      {/* 환경 조명 효과 */}
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={0.8} color="#6366F1" />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#EC4899" />
      
      {/* 홀로그래픽 텍스트 */}
      <Text
        position={[0, 2, 0]}
        fontSize={0.5}
        color="#00F5FF"
        anchorX="center"
        anchorY="middle"
        font="/fonts/NanumMyeongjo-Regular.woff"
      >
        🔮 HEAL7 CYBER FORTUNE
      </Text>
      
      <Text
        position={[0, -2, 0]}
        fontSize={0.3}
        color="#FF00FF"
        anchorX="center"
        anchorY="middle"
        font="/fonts/Pretendard-Regular.woff"
      >
        디지털 운명학의 새로운 차원
      </Text>
    </>
  )
}

export default CyberCrystal