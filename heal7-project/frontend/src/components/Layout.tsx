import React from 'react'
import { Link } from 'react-router-dom'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-2xl font-bold text-blue-600">
                HEAL7
              </Link>
            </div>
            <div className="flex items-center space-x-8">
              <Link 
                href="/store/books" 
                className="text-gray-700 hover:text-blue-600 transition-colors"
              >
                스토어
              </Link>
            </div>
          </div>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  )
}