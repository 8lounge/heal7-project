import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-sans'
})

export const metadata: Metadata = {
  title: {
    default: 'Heal7 - 통합 웰니스 플랫폼',
    template: '%s | Heal7'
  },
  description: '사주명리학, 건강관리, 교육 서비스를 제공하는 통합 웰니스 플랫폼입니다.',
  keywords: ['heal7', '사주', '명리학', '건강', '웰니스', '교육'],
  authors: [{ name: 'Heal7 Team' }],
  creator: 'Heal7',
  publisher: 'Heal7',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
  alternates: {
    canonical: 'https://heal7.com',
  },
  openGraph: {
    type: 'website',
    locale: 'ko_KR',
    url: 'https://heal7.com',
    siteName: 'Heal7',
    title: 'Heal7 - 통합 웰니스 플랫폼',
    description: '사주명리학, 건강관리, 교육 서비스를 제공하는 통합 웰니스 플랫폼입니다.',
    images: [
      {
        url: 'https://heal7.com/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Heal7 통합 웰니스 플랫폼',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    site: '@heal7platform',
    creator: '@heal7platform',
  },
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="ko" className={cn('antialiased', inter.variable)}>
      <head>
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        
        {/* 성능 최적화 */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="//fonts.googleapis.com" />
        
        {/* PWA */}
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#2563eb" />
      </head>
      <body className={cn(
        'min-h-screen bg-background font-sans antialiased',
        'selection:bg-heal7-primary selection:text-white'
      )}>
        <div className="relative flex min-h-screen flex-col">
          {children}
        </div>
        
        {/* 글로벌 스크립트 */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // 다크모드 플리커 방지
              (function() {
                try {
                  const theme = localStorage.getItem('theme')
                  if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                    document.documentElement.classList.add('dark')
                  }
                } catch {}
              })()
            `,
          }}
        />
      </body>
    </html>
  )
}