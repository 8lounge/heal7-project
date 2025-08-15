import type { Metadata } from 'next'
import { Providers } from '@/components/providers'
import '@/styles/index.css'

export const metadata: Metadata = {
  title: 'Heal7 - 힐링스페이스',
  description: '당신만의 힐링 공간, Heal7에서 시작하세요.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}