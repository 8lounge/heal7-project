import { Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Layout } from '@/components/layout/Layout'
import { AuthProvider } from '@/contexts/AuthContext'
import { HomePage } from '@/pages/HomePage'
import { DiagnosisPage } from '@/pages/DiagnosisPage'
import { AcademyPage } from '@/pages/AcademyPage'
import { AcademyDetailPage } from '@/pages/AcademyDetailPage'
import { SubscriptionPage } from '@/pages/SubscriptionPage'
import { StorePage } from '@/pages/StorePage'
import { CommunityPage } from '@/pages/CommunityPage'
import { BookDetailPage } from '@/pages/BookDetailPage'
import { LoginPage } from '@/pages/LoginPage'
import PaymentSuccessPage from '@/pages/PaymentSuccessPage'
import PrivacyPolicyPage from '@/pages/PrivacyPolicyPage'
import TermsOfServicePage from '@/pages/TermsOfServicePage'

// React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Routes>
          {/* 로그인 페이지는 Layout 없이 독립 실행 */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* 나머지 모든 페이지는 Layout으로 감쌈 */}
          <Route path="/*" element={
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/diagnosis" element={<DiagnosisPage />} />
                <Route path="/academy" element={<AcademyPage />} />
                <Route path="/academy/projects/:id" element={<AcademyDetailPage />} />
                <Route path="/subscription" element={<SubscriptionPage />} />
                <Route path="/store" element={<StorePage />} />
                <Route path="/store/books" element={<StorePage />} />
                <Route path="/store/books/:id" element={<BookDetailPage />} />
                <Route path="/community" element={<CommunityPage />} />
                <Route path="/payment/success" element={<PaymentSuccessPage />} />
                <Route path="/payment/fail" element={<PaymentSuccessPage />} />
                <Route path="/privacy" element={<PrivacyPolicyPage />} />
                <Route path="/terms" element={<TermsOfServicePage />} />
                <Route path="/about" element={<div className="pt-20 p-8">서비스 소개 페이지 (구현 예정)</div>} />
              </Routes>
            </Layout>
          } />
        </Routes>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App// Cache bust: 1754580033
