import { ReactNode } from 'react'
import Navigation from './Navigation'
import Footer from './Footer'

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-heal7-surface">
      <Navigation />
      <main className="relative">
        {children}
      </main>
      <Footer />
    </div>
  )
}

export default Layout