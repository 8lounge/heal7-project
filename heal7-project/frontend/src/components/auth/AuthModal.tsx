// Updated 2025-08-07 for compact UI v2
import React, { useState } from 'react'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useAuth } from '@/contexts/AuthContext'
import { 
  X, 
  Mail, 
  Lock, 
  User, 
  Phone, 
  Eye, 
  EyeOff,
  Loader2,
  Heart,
  ExternalLink
} from 'lucide-react'

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
}

type AuthMode = 'login' | 'register'

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => { 
  const [mode, setMode] = useState<AuthMode>('login')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const pathname = usePathname()
  
  const { login, register } = useAuth()
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: ''
  })

  const [agreements, setAgreements] = useState({
    requiredAll: false, // 필수 약관 통합 동의
    marketing: false,
    showDetails: false // 상세 내용 표시 여부
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    // 회원가입 시 필수 동의 항목 검증
    if (mode === 'register') {
      if (!agreements.requiredAll) {
        setError('필수 약관에 모두 동의해주세요.')
        setLoading(false)
        return
      }
    }

    try {
      if (mode === 'login') {
        await login({
          email: formData.email,
          password: formData.password
        })
      } else {
        await register({
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name,
          phone: formData.phone || undefined
        })
      }
      
      // 성공 시 모달 닫기
      onClose()
      setFormData({ email: '', password: '', full_name: '', phone: '' })
      setAgreements({
        requiredAll: false,
        marketing: false,
        showDetails: false
      })
    } catch (err: any) {
      setError(err.message || '오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const switchMode = () => {
    setMode(mode === 'login' ? 'register' : 'login')
    setError(null)
    setFormData({ email: '', password: '', full_name: '', phone: '' })
    setAgreements({
      requiredAll: false,
      marketing: false,
      showDetails: false
    })
  }

  const goToLoginPage = () => {
    const currentPath = pathname
    window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`
  }

  const handleAgreementChange = (key: keyof typeof agreements) => {
    setAgreements(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  if (!isOpen) return null

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-md mx-4 bg-white dark:bg-gray-900 rounded-2xl shadow-2xl overflow-hidden"
        >
          {/* Header */}
          <div className="relative bg-gradient-to-r from-healing-500 to-sky-500 p-6 text-white">
            <button
              onClick={onClose}
              className="absolute top-4 right-4 p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            
            <div className="flex items-center space-x-2 mb-2">
              <Heart className="w-6 h-6" />
              <span className="text-lg font-semibold">HEALINGSPACE</span> 
            </div>
            
            <h2 className="text-2xl font-bold">
              {mode === 'login' ? '로그인' : '회원가입'}
            </h2>
            <p className="text-healing-100 mt-1">
              {mode === 'login' 
                ? '힐링 여정을 계속하세요' 
                : '새로운 힐링 여정을 시작하세요'}
            </p>
          </div>

          {/* Form */}
          <div className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === 'register' && (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    이름 *
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <Input
                      type="text"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleInputChange}
                      placeholder="이름을 입력하세요"
                      className="pl-10"
                      required
                    />
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  이메일 *
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <Input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="이메일을 입력하세요"
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              {mode === 'register' && (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    전화번호
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <Input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      placeholder="010-0000-0000"
                      className="pl-10"
                    />
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  비밀번호 *
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="비밀번호를 입력하세요"
                    className="pl-10 pr-10"
                    minLength={6}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {mode === 'register' && (
                  <p className="text-xs text-gray-500">
                    최소 6자 이상 입력해주세요
                  </p>
                )}
              </div>

              {/* 회원가입 동의 항목 - 컴팩트 버전 */}
              {mode === 'register' && (
                <div className="space-y-3">
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                      약관 동의
                    </h4>
                    
                    <div className="space-y-3">
                      {/* 통합 필수 동의 */}
                      <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                        <label className="flex items-start space-x-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={agreements.requiredAll}
                            onChange={() => handleAgreementChange('requiredAll')}
                            className="mt-1 w-4 h-4 text-healing-600 border-gray-300 rounded focus:ring-healing-500"
                          />
                          <div className="flex-1">
                            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                              필수 약관에 모두 동의합니다
                            </span>
                            <div className="text-xs text-gray-500 mt-1">
                              서비스 이용약관, 개인정보처리방침, 민감정보처리(사주분석용), 해외전송(AI분석용)
                            </div>
                            <button
                              type="button"
                              onClick={() => handleAgreementChange('showDetails')}
                              className="text-xs text-healing-600 hover:underline mt-1 inline-flex items-center"
                            >
                              {agreements.showDetails ? '간단히 보기' : '자세히 보기'} 
                              <span className={`ml-1 transition-transform ${agreements.showDetails ? 'rotate-180' : ''}`}>▼</span>
                            </button>
                          </div>
                        </label>
                      </div>

                      {/* 상세 동의 항목 (아코디언) */}
                      {agreements.showDetails && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="pl-6 space-y-2 text-xs text-gray-600 dark:text-gray-400"
                        >
                          <div className="flex items-center space-x-2">
                            <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                            <span><a href="/terms" target="_blank" className="text-healing-600 hover:underline">서비스 이용약관</a></span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                            <span><a href="/privacy" target="_blank" className="text-healing-600 hover:underline">개인정보 처리방침</a></span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                            <span>민감정보 처리: 생년월일시, 성향분석 결과</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                            <span>해외전송: Google, OpenAI, Anthropic AI 분석</span>
                          </div>
                        </motion.div>
                      )}
                      
                      {/* 선택 동의 */}
                      <label className="flex items-start space-x-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={agreements.marketing}
                          onChange={() => handleAgreementChange('marketing')}
                          className="mt-1 w-4 h-4 text-healing-600 border-gray-300 rounded focus:ring-healing-500"
                        />
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          [선택] 마케팅 정보 수신에 동의합니다
                        </span>
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-healing-500 to-sky-500 hover:from-healing-600 hover:to-sky-600"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    {mode === 'login' ? '로그인 중...' : '가입 중...'}
                  </>
                ) : (
                  mode === 'login' ? '로그인' : '회원가입'
                )}
              </Button>
            </form>

          </div>
          
          {/* Footer - Fixed */}
          <div className="flex-shrink-0 bg-gray-50 dark:bg-gray-800 px-4 py-4 sm:px-6">
            <div className="text-center space-y-3">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {mode === 'login' ? '아직 계정이 없으신가요?' : '이미 계정이 있으신가요?'}
                </p>
                <button
                  onClick={switchMode}
                  className="mt-1 text-sm font-medium text-healing-600 hover:text-healing-700 dark:text-healing-400 dark:hover:text-healing-300"
                >
                  {mode === 'login' ? '회원가입하기' : '로그인하기'}
                </button>
              </div>
              
              <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                <button
                  onClick={goToLoginPage}
                  className="inline-flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400 hover:text-healing-600 dark:hover:text-healing-400"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span>전용 로그인 페이지로 이동</span>
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}