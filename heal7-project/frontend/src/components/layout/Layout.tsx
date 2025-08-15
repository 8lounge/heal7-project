import React from 'react'
import { Navigation } from './Navigation'
import { Footer } from './Footer'

interface LayoutProps {
  children: React.ReactNode
  className?: string
}

export const Layout: React.FC<LayoutProps> = ({ children, className }) => {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />
      <main className={className}>
        {children}
      </main>
      <Footer />
    </div>
  )
}