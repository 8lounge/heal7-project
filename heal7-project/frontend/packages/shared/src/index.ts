// UI Components
export * from './components/ui/badge'
export * from './components/ui/button'
export * from './components/ui/card'
export * from './components/ui/dialog'
export * from './components/ui/input'
export * from './components/ui/label'
export * from './components/ui/progress'
export * from './components/ui/select'
export * from './components/ui/switch'
export * from './components/ui/tabs'
export * from './components/ui/toast'
export * from './components/ui/use-toast'

// 3D Components
export { default as OptimizedCyberCrystal } from './components/3d/OptimizedCyberCrystal'
export { default as OptimizedStars } from './components/3d/OptimizedStars'

// Three.js Core Components (re-export to prevent duplication)
export { Canvas } from '@react-three/fiber'
export { OrbitControls } from '@react-three/drei'

// Utilities
export * from './lib/utils'