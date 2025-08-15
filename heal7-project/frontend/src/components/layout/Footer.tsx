import React from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  Heart, 
  Mail, 
  Phone, 
  MapPin, 
  Facebook, 
  Instagram, 
  Youtube,
  ArrowRight
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const footerLinks = {
  services: [
    { title: '3D 성향 분석', href: '/diagnosis/personality' },
    { title: 'AI 심리 분석', href: '/diagnosis/psychology' },
    { title: '명리학 v5.0', href: '/diagnosis/saju' },
    { title: '체험아카데미', href: '/academy' }
  ],
  support: [
    { title: '공지사항', href: '/community/notices' },
    { title: '1:1 문의', href: '/community/inquiry' },
    { title: '이용약관', href: '/terms' },
    { title: '개인정보처리방침', href: '/privacy' }
  ],
  company: [
    { title: '회사소개', href: '/about' },
    { title: '채용정보', href: '/careers' },
    { title: '제휴문의', href: '/partnership' },
    { title: '언론보도', href: '/press' }
  ]
}

const socialLinks = [
  { icon: Facebook, href: '#', label: 'Facebook' },
  { icon: Instagram, href: '#', label: 'Instagram' },
  { icon: Youtube, href: '#', label: 'YouTube' }
]

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
      {/* Newsletter Section */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-900 text-white">
        <div className="container mx-auto px-4 py-12">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="space-y-4"
            >
              <h3 className="heading-md text-white">
                마음의 평화를 전해드립니다
              </h3>
              <p className="text-slate-300 max-w-2xl mx-auto">
                힐링과 성장에 관한 최신 소식과 특별한 혜택을 가장 먼저 받아보세요.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                <Input
                  type="email"
                  placeholder="이메일 주소를 입력하세요"
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/70"
                />
                <Button variant="secondary" className="whitespace-nowrap">
                  구독하기
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Main Footer Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center space-x-2">
              <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-r from-sky-500 to-sky-600 shadow-lg">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold bg-gradient-to-r from-slate-600 to-slate-800 bg-clip-text text-transparent">
                  HEALINGSPACE
                </span>
                <span className="text-xs text-muted-foreground -mt-1">
                  마음의 평화를 찾아가는 여정
                </span>
              </div>
            </div>
            
            <p className="text-muted-foreground max-w-md">
              HEALINGSPACE는 현대인의 마음의 평화와 성장을 위해 과학적이고 체계적인 
              분석 솔루션과 힐링 서비스를 제공합니다.
            </p>

            {/* Contact Info */}
            <div className="space-y-3 text-sm">
              <div className="flex items-center space-x-3 text-muted-foreground">
                <Mail className="w-4 h-4" />
                <span>nibcosmetic@gmail.com</span>
              </div>
              <div className="flex items-center space-x-3 text-muted-foreground">
                <MapPin className="w-4 h-4" />
                <span>인천광역시 미추홀구 석정로 38, 2층(숭의동)</span>
              </div>
            </div>

            {/* Social Links */}
            <div className="flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon
                return (
                  <Button
                    key={social.label}
                    variant="ghost"
                    size="icon"
                    className="rounded-full hover:bg-slate-100 hover:text-sky-600"
                    asChild
                  >
                    <a
                      href={social.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      aria-label={social.label}
                    >
                      <Icon className="w-5 h-5" />
                    </a>
                  </Button>
                )
              })}
            </div>
          </div>

          {/* Services */}
          <div className="space-y-4">
            <h4 className="font-semibold text-gray-900 dark:text-gray-100">
              서비스
            </h4>
            <ul className="space-y-2">
              {footerLinks.services.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-muted-foreground hover:text-sky-600 transition-colors text-sm"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-4">
            <h4 className="font-semibold text-gray-900 dark:text-gray-100">
              고객지원
            </h4>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-muted-foreground hover:text-sky-600 transition-colors text-sm"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div className="space-y-4">
            <h4 className="font-semibold text-gray-900 dark:text-gray-100">
              회사
            </h4>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-muted-foreground hover:text-sky-600 transition-colors text-sm"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-200 dark:border-gray-800">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <div className="text-sm text-muted-foreground">
              © 2025 (주)닙코스. All rights reserved. (대표자: 김효원)
            </div>
            <div className="flex flex-col md:flex-row items-center md:space-x-4 text-sm text-muted-foreground">
              <span>사업자등록번호: 616-88-00652</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
