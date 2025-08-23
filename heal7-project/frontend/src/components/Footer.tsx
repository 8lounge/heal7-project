import { useNavigate } from 'react-router-dom'
import { 
  Compass,
  Mail,
  MapPin,
  Heart,
  BookOpen,
  HelpCircle
} from 'lucide-react'

const Footer = () => {
  const navigate = useNavigate()

  const handleNavigation = (href: string) => {
    navigate(href)
  }

  return (
    <footer className="bg-heal7-dark text-white relative overflow-hidden">
      {/* 배경 패턴 */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(var(--heal7-secondary),0.1),transparent_70%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(var(--heal7-accent),0.1),transparent_70%)]" />
      
      <div className="container relative">
        <div className="py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* 브랜드 섹션 */}
            <div className="md:col-span-2">
              <div className="flex items-center space-x-3 mb-6">
                <div className="bg-heal7-gradient rounded-xl p-3">
                  <Compass className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-heal7-gradient">HEAL7</h3>
                  <p className="text-sm text-gray-300">운명을 읽고, 삶을 쓰다</p>
                </div>
              </div>
              <p className="text-gray-300 leading-relaxed mb-6 max-w-md">
                천년의 지혜와 현대적 성찰이 만나는 곳에서<br />
                진정한 자아실현의 여정을 함께 걸어갑니다.
              </p>
              <div className="space-y-2">
                <div className="flex items-center space-x-3 text-sm text-gray-300">
                  <Mail className="h-4 w-4 text-heal7-secondary" />
                  <span>contact@heal7.com</span>
                </div>
                <div className="flex items-center space-x-3 text-sm text-gray-300">
                  <MapPin className="h-4 w-4 text-heal7-secondary" />
                  <span>서울특별시 강남구</span>
                </div>
              </div>
            </div>

            {/* 서비스 링크 */}
            <div>
              <h4 className="text-lg font-semibold mb-4 text-heal7-secondary">서비스</h4>
              <div className="space-y-3">
                {[
                  { name: '자아 발견', href: '/saju/basic' },
                  { name: '궁합 분석', href: '/saju/compatibility' },
                  { name: '사업운 분석', href: '/saju/business' },
                  { name: '연간 운세', href: '/saju/yearly' },
                ].map((item) => (
                  <button
                    key={item.name}
                    onClick={() => handleNavigation(item.href)}
                    className="block text-gray-300 hover:text-heal7-accent transition-colors text-sm"
                  >
                    {item.name}
                  </button>
                ))}
              </div>
            </div>

            {/* 정보 링크 */}
            <div>
              <h4 className="text-lg font-semibold mb-4 text-heal7-secondary">정보</h4>
              <div className="space-y-3">
                {[
                  { name: '철학과 가치', href: '/saju/about', icon: BookOpen },
                  { name: '학습 센터', href: '/learn', icon: BookOpen },
                  { name: '자주 묻는 질문', href: '/faq', icon: HelpCircle },
                ].map((item) => (
                  <button
                    key={item.name}
                    onClick={() => handleNavigation(item.href)}
                    className="flex items-center space-x-2 text-gray-300 hover:text-heal7-accent transition-colors text-sm group"
                  >
                    <item.icon className="h-4 w-4 group-hover:text-heal7-accent" />
                    <span>{item.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 하단 정보 */}
        <div className="py-6 border-t border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-sm text-gray-400">
              © 2025 HEAL7. 모든 권리 보유.
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <span>Made with</span>
              <Heart className="h-4 w-4 text-heal7-accent" />
              <span>and ancient wisdom</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer