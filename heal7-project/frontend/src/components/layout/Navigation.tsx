import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { AuthModal } from '@/components/auth/AuthModal'
import { useAuth } from '@/contexts/AuthContext'
import { 
  Menu, 
  X, 
  Heart, 
  Sparkles, 
  ShoppingBag, 
  Users, 
  BookOpen,
  User,
  Sun,
  Moon,
  LogOut,
  Zap
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface NavigationProps {
  className?: string
}

const navigationItems = [
  {
    title: '분석 솔루션',
    href: '/diagnosis',
    icon: Sparkles,
    description: '3D 성향 분석 & AI 심리 분석',
    badge: 'NEW'
  },
  {
    title: '아카데미',
    href: '/academy',
    icon: BookOpen,
    description: '강의 공동구매 & 체험강좌'
  },
  {
    title: '구독서비스',
    href: '/subscription',
    icon: Zap,
    description: '월간/분기/연간 구독',
    badge: 'HOT'
  },
  {
    title: '힐링샵',
    href: '/store',
    icon: ShoppingBag,
    description: '힐링 상품 & 도서'
  },
  {
    title: '커뮤니티',
    href: '/community',
    icon: Users,
    description: '공지사항 & 1:1 문의'
  }
]

export const Navigation: React.FC<NavigationProps> = ({ className }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const [isDark, setIsDark] = useState(true) // 다크모드를 기본값으로 설정
  const [authModalOpen, setAuthModalOpen] = useState(false)
  const pathname = usePathname()
  const { user, logout } = useAuth()

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // 테마 초기화 및 로컬스토리지 동기화
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    
    if (savedTheme) {
      // 저장된 테마가 있으면 사용
      const isDarkSaved = savedTheme === 'dark'
      setIsDark(isDarkSaved)
      
      if (isDarkSaved) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    } else {
      // 저장된 테마가 없으면 다크모드를 기본값으로 설정
      setIsDark(true)
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    }
  }, [])

  const toggleTheme = () => {
    const newIsDark = !isDark
    setIsDark(newIsDark)
    
    if (newIsDark) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        scrolled 
          ? 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg shadow-lg border-b border-gray-200/20' 
          : 'bg-transparent',
        className
      )}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 group">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-r from-healing-500 to-healing-600 shadow-lg group-hover:shadow-xl transition-shadow">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold bg-gradient-to-r from-healing-600 to-healing-800 bg-clip-text text-transparent">
                HEALINGSPACE
              </span>
              <span className="text-xs text-muted-foreground -mt-1">
                마음의 평화를 찾아가는 여정
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-8">
            {navigationItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'group relative flex flex-col items-center p-3 rounded-lg transition-all duration-200',
                    isActive 
                      ? 'text-healing-600' 
                      : 'text-gray-600 dark:text-gray-300 hover:text-healing-600'
                  )}
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.title}</span>
                    {item.badge && (
                      <Badge variant="healing" className="text-xs">
                        {item.badge}
                      </Badge>
                    )}
                  </div>
                  <span className="text-xs text-muted-foreground mt-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    {item.description}
                  </span>
                  {isActive && (
                    <motion.div
                      layoutId="activeIndicator"
                      className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-healing-500 rounded-full"
                    />
                  )}
                </Link>
              )
            })}
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-3 min-w-0 flex-shrink-0">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className="rounded-full"
            >
              {isDark ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </Button>

            {/* User Menu */}
            {user ? (
              <div className="hidden md:flex items-center space-x-2 min-w-0">
                <span className="text-sm text-muted-foreground truncate max-w-24">
                  {user.full_name}님
                </span>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={logout}
                  className="flex items-center space-x-1 flex-shrink-0"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="hidden lg:inline">로그아웃</span>
                </Button>
              </div>
            ) : (
              <Button 
                variant="ghost" 
                onClick={() => setAuthModalOpen(true)}
                className="hidden md:flex items-center space-x-2 flex-shrink-0"
              >
                <User className="w-5 h-5" />
                <span>로그인</span>
              </Button>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg border-t border-gray-200/20"
          >
            <div className="container mx-auto px-4 py-4">
              <div className="flex flex-col space-y-4">
                {navigationItems.map((item) => {
                  const Icon = item.icon
                  const isActive = pathname === item.href
                  
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setIsOpen(false)}
                      className={cn(
                        'flex items-center space-x-3 p-3 rounded-lg transition-colors',
                        isActive 
                          ? 'bg-healing-50 text-healing-600 dark:bg-healing-900/20' 
                          : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                      )}
                    >
                      <Icon className="w-5 h-5" />
                      <div className="flex-1">
                        <div className="flex items-center space-x-2">
                          <span className="font-medium">{item.title}</span>
                          {item.badge && (
                            <Badge variant="healing" className="text-xs">
                              {item.badge}
                            </Badge>
                          )}
                        </div>
                        <span className="text-sm text-muted-foreground">
                          {item.description}
                        </span>
                      </div>
                    </Link>
                  )
                })}
                
                <div className="border-t border-gray-200/20 pt-4">
                  {user ? (
                    <div className="space-y-3">
                      <div className="text-center text-sm text-muted-foreground">
                        {user.full_name}님
                      </div>
                      <Button 
                        onClick={logout}
                        className="w-full" 
                        variant="outline"
                      >
                        <LogOut className="w-4 h-4 mr-2" />
                        로그아웃
                      </Button>
                    </div>
                  ) : (
                    <Button 
                      onClick={() => {
                        setAuthModalOpen(true)
                        setIsOpen(false)
                      }}
                      className="w-full" 
                      variant="healing"
                    >
                      <User className="w-4 h-4 mr-2" />
                      로그인
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Auth Modal */}
      <AuthModal 
        isOpen={authModalOpen} 
        onClose={() => setAuthModalOpen(false)} 
      />
    </motion.nav>
  )
}