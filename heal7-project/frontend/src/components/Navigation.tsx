import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { 
  Menu, 
  X, 
  User, 
  BookOpen, 
  HelpCircle,
  Compass,
  ShoppingCart,
  NewspaperIcon,
  Users,
  ChevronDown,
  Sparkles
} from 'lucide-react'

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [, setServicesOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  // 주요 내비게이션 아이템들
  const mainNavItems = [
    { name: '내 운명 보기', href: '/saju/basic', icon: User, badge: 'FREE' },
    { name: '신비용품', href: '/store', icon: ShoppingCart, badge: 'HOT' },
    { name: '매거진', href: '/magazine', icon: NewspaperIcon },
    { name: '커뮤니티', href: '/community', icon: Users },
  ]
  
  // 신비학 서비스 메뉴
  const mysticalServices = [
    { name: '🎆 사주명리', href: '/saju/basic', description: '내 운명을 알아보세요' },
    { name: '🎭 타로리딩', href: '/tarot', description: '카드가 전하는 메시지' },
    { name: '🌿 사상체질', href: '/sasang', description: '내 몸에 맞는 건강법' },
    { name: '⭐ 별자리운세', href: '/astrology', description: '별들이 속삭이는 이야기' },
    { name: '🧿 풍수지리', href: '/fengshui', description: '공간의 에너지 개선' },
  ]

  // 보조 메뉴
  const secondaryNavItems = [
    { name: '학습센터', href: '/learn', icon: BookOpen },
    { name: 'FAQ', href: '/faq', icon: HelpCircle },
  ]

  const handleNavigation = (href: string) => {
    navigate(href)
    setIsOpen(false)
  }

  return (
    <nav className="bg-white/95 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="container">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <button 
            onClick={() => handleNavigation('/')}
            className="flex items-center space-x-2 text-heal7-primary font-bold text-xl"
          >
            <div className="bg-heal7-gradient rounded-lg p-2">
              <Compass className="h-5 w-5 text-white" />
            </div>
            <span className="text-heal7-gradient">HEAL7</span>
          </button>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-6">
            {/* 서비스 드롭다운 */}
            <div className="relative group">
              <button
                className="flex items-center space-x-2 px-4 py-2 text-heal7-muted hover:text-heal7-primary transition-all duration-200 rounded-lg hover:bg-heal7-surface"
                onMouseEnter={() => setServicesOpen(true)}
              >
                <Sparkles className="h-4 w-4" />
                <span className="font-medium">신비서비스</span>
                <ChevronDown className="h-3 w-3" />
              </button>
              
              {/* 드롭다운 메뉴 */}
              <div 
                className="absolute top-full left-0 w-80 bg-white rounded-2xl shadow-2xl border border-gray-200 py-4 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-2 group-hover:translate-y-0 z-50"
                onMouseEnter={() => setServicesOpen(true)}
                onMouseLeave={() => setServicesOpen(false)}
              >
                <div className="px-4 pb-3 mb-3 border-b border-gray-100">
                  <h3 className="text-sm font-bold text-heal7-primary">🌟 신비학의 세계</h3>
                  <p className="text-xs text-heal7-muted mt-1">천년의 지혜를 만나보세요</p>
                </div>
                <div className="space-y-1">
                  {mysticalServices.map((service) => (
                    <button
                      key={service.name}
                      onClick={() => handleNavigation(service.href)}
                      className="w-full px-4 py-3 text-left hover:bg-heal7-surface transition-colors rounded-lg mx-2"
                    >
                      <div className="text-sm font-medium text-heal7-dark">{service.name}</div>
                      <div className="text-xs text-heal7-muted mt-1">{service.description}</div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            {/* 메인 메뉴들 */}
            {mainNavItems.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <button
                  key={item.name}
                  onClick={() => handleNavigation(item.href)}
                  className={`relative px-4 py-2 rounded-lg transition-all duration-200 flex items-center space-x-2 text-sm font-medium ${
                    isActive
                      ? 'bg-heal7-gradient text-white shadow-heal7-md'
                      : 'text-heal7-muted hover:text-heal7-primary hover:bg-heal7-surface'
                  }`}
                >
                  <item.icon className="h-4 w-4" />
                  <span>{item.name}</span>
                  {item.badge && (
                    <span className="absolute -top-2 -right-2 bg-gradient-to-r from-pink-500 to-red-500 text-white text-xs px-2 py-0.5 rounded-full font-bold">
                      {item.badge}
                    </span>
                  )}
                </button>
              )
            })}
            
            {/* 보조 메뉴 */}
            <div className="flex items-center space-x-2 pl-4 border-l border-gray-200">
              {secondaryNavItems.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <button
                    key={item.name}
                    onClick={() => handleNavigation(item.href)}
                    className={`px-3 py-2 rounded-lg transition-all duration-200 text-sm font-medium ${
                      isActive
                        ? 'bg-heal7-primary text-white'
                        : 'text-heal7-muted hover:text-heal7-primary hover:bg-heal7-surface'
                    }`}
                  >
                    <item.icon className="h-4 w-4" />
                  </button>
                )
              })}
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="lg:hidden p-2 rounded-lg text-heal7-muted hover:text-heal7-primary hover:bg-heal7-surface transition-all duration-200"
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="lg:hidden py-6 border-t border-gray-200 bg-gradient-to-b from-white to-heal7-surface">
            {/* 신비서비스 섹션 */}
            <div className="mb-6">
              <h3 className="px-4 text-sm font-bold text-heal7-primary mb-3 flex items-center">
                <Sparkles className="h-4 w-4 mr-2" />
                🌟 신비서비스
              </h3>
              <div className="space-y-1">
                {mysticalServices.map((service) => (
                  <button
                    key={service.name}
                    onClick={() => handleNavigation(service.href)}
                    className="w-full px-4 py-3 rounded-lg transition-all duration-200 text-left hover:bg-white hover:shadow-sm"
                  >
                    <div className="text-sm font-medium text-heal7-dark">{service.name}</div>
                    <div className="text-xs text-heal7-muted mt-1">{service.description}</div>
                  </button>
                ))}
              </div>
            </div>
            
            {/* 메인 메뉴 */}
            <div className="mb-6">
              <h3 className="px-4 text-sm font-bold text-heal7-primary mb-3">🏠 메인 메뉴</h3>
              <div className="space-y-2">
                {mainNavItems.map((item) => {
                  const isActive = location.pathname === item.href
                  return (
                    <button
                      key={item.name}
                      onClick={() => handleNavigation(item.href)}
                      className={`w-full px-4 py-3 rounded-lg transition-all duration-200 flex items-center justify-between text-left ${
                        isActive
                          ? 'bg-heal7-gradient text-white shadow-heal7-md'
                          : 'text-heal7-muted hover:text-heal7-primary hover:bg-white hover:shadow-sm'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <item.icon className="h-5 w-5" />
                        <span className="font-medium">{item.name}</span>
                      </div>
                      {item.badge && (
                        <span className="bg-gradient-to-r from-pink-500 to-red-500 text-white text-xs px-2 py-1 rounded-full font-bold">
                          {item.badge}
                        </span>
                      )}
                    </button>
                  )
                })}
              </div>
            </div>
            
            {/* 보조 메뉴 */}
            <div className="border-t border-gray-200 pt-4">
              <div className="flex space-x-2">
                {secondaryNavItems.map((item) => {
                  const isActive = location.pathname === item.href
                  return (
                    <button
                      key={item.name}
                      onClick={() => handleNavigation(item.href)}
                      className={`flex-1 px-3 py-2 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-sm font-medium ${
                        isActive
                          ? 'bg-heal7-primary text-white'
                          : 'text-heal7-muted hover:text-heal7-primary hover:bg-white'
                      }`}
                    >
                      <item.icon className="h-4 w-4" />
                      <span>{item.name}</span>
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navigation