import type { Metadata } from 'next'
import { Inter, Noto_Sans_KR } from 'next/font/google'
import './globals.css'

import { Providers } from '@/components/providers'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['300', '400', '500', '700'],
  variable: '--font-korean',
})

export const metadata: Metadata = {
  title: {
    default: 'HEAL7 사주명리학',
    template: '%s | HEAL7 사주명리학',
  },
  description: '정확하고 과학적인 사주명리학 서비스 - KASI 데이터 기반 프론트엔드 계산',
  keywords: [
    '사주',
    '명리학',
    '사주팔자',
    '운세',
    '궁합',
    '사주해석',
    'HEAL7',
    'KASI',
  ],
  authors: [{ name: 'HEAL7 Development Team' }],
  creator: 'HEAL7',
  publisher: 'HEAL7',
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
  openGraph: {
    type: 'website',
    locale: 'ko_KR',
    url: 'https://saju.heal7.com',
    title: 'HEAL7 사주명리학',
    description: '정확하고 과학적인 사주명리학 서비스',
    siteName: 'HEAL7',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'HEAL7 사주명리학',
    description: '정확하고 과학적인 사주명리학 서비스',
  },
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body
        className={`${inter.variable} ${notoSansKR.variable} font-sans antialiased`}
      >
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <div className="flex-1">{children}</div>
          </div>
        </Providers>
      </body>
    </html>
  )
}