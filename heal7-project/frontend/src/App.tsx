import { Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import Layout from './components/Layout'

// Lazy load components for better performance
const ViteSajuMain = lazy(() => import('./components/ViteSajuMain'))

// Enhanced placeholder components with proper navigation
const PlaceholderPage = ({ title, description, features }: { 
  title: string, 
  description?: string,
  features?: string[]
}) => (
  <div className="min-h-screen bg-heal7-surface">
    <div className="container py-20">
      <div className="max-w-4xl mx-auto text-center">
        {/* 아이콘 */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-heal7-gradient rounded-full blur-xl opacity-30 scale-110"></div>
            <div className="relative bg-heal7-gradient rounded-full p-6 shadow-heal7-lg">
              <div className="h-12 w-12 bg-white rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-xl drop-shadow-lg">✨</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* 제목 */}
        <h1 className="text-4xl md:text-5xl font-bold text-heal7-dark mb-6">
          <span className="text-heal7-gradient">{title}</span>
        </h1>
        
        {/* 설명 */}
        <p className="text-xl text-heal7-muted mb-8 leading-relaxed">
          {description || "더 나은 서비스를 위해 준비하고 있습니다."}
        </p>
        
        {/* 특징 (있는 경우) */}
        {features && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
            {features.map((feature, index) => (
              <div key={index} className="card-heal7 p-4">
                <p className="text-heal7-muted">{feature}</p>
              </div>
            ))}
          </div>
        )}
        
        {/* CTA */}
        <div className="space-y-4">
          <p className="text-heal7-muted">곧 여러분을 만날 수 있도록 최선을 다하겠습니다.</p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <button 
              onClick={() => window.location.href = '/'}
              className="btn-heal7-primary text-lg px-8 py-4"
            >
              메인으로 돌아가기
            </button>
            <button 
              onClick={() => window.location.href = '/saju/about'}
              className="btn-heal7-outline text-lg px-8 py-4"
            >
              철학과 가치 알아보기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
)

// Loading component with HEAL7 branding
const LoadingSpinner = () => (
  <div className="min-h-screen bg-heal7-surface flex items-center justify-center">
    <div className="text-center">
      <div className="relative mb-8">
        <div className="absolute inset-0 bg-heal7-gradient rounded-full blur-xl opacity-30 scale-110 animate-pulse"></div>
        <div className="relative bg-heal7-gradient rounded-full p-6 shadow-heal7-lg">
          <div className="h-12 w-12 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
      <p className="text-heal7-muted animate-pulse">천년의 지혜를 준비하고 있습니다...</p>
    </div>
  </div>
)


function App() {
  return (
    <div className="App">
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          {/* Main routes - without layout for hero sections */}
          <Route path="/" element={<ViteSajuMain />} />
          <Route path="/saju" element={<ViteSajuMain />} />
          
          {/* All other routes with Layout */}
          <Route path="/saju/about" element={
            <Layout>
              <PlaceholderPage 
                title="철학과 가치" 
                description="동양철학의 깊이와 현대적 성찰이 만나는 HEAL7의 인문학적 접근을 소개합니다."
                features={[
                  "천년의 전통 명리학",
                  "현대적 해석과 적용",
                  "자아실현 중심 접근",
                  "과학적 검증 시스템"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/saju/basic" element={
            <Layout>
              <PlaceholderPage 
                title="무료 사주 분석" 
                description="기본 사주 분석으로 자아 발견의 첫걸음을 시작하세요."
                features={[
                  "출생정보 기반 분석",
                  "성격과 기질 파악",
                  "잠재력 발견",
                  "기본 운세 제공"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/saju/compatibility" element={
            <Layout>
              <PlaceholderPage 
                title="궁합 분석" 
                description="두 사람의 조화로운 관계를 위한 깊이 있는 분석을 제공합니다."
                features={[
                  "관계 역학 분석",
                  "소통 패턴 파악",
                  "갈등 해결 방안",
                  "성장하는 사랑"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/saju/business" element={
            <Layout>
              <PlaceholderPage 
                title="사업운 분석" 
                description="지속 가능한 성공을 위한 사업 적합성과 타이밍을 분석합니다."
                features={[
                  "사업 적성 분석",
                  "성공 타이밍",
                  "파트너십 궁합",
                  "리스크 관리"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/saju/yearly" element={
            <Layout>
              <PlaceholderPage 
                title="연간 운세" 
                description="1년간의 흐름을 이해하고 각 시기에 맞는 지혜로운 선택을 하세요."
                features={[
                  "월별 운세 분석",
                  "주요 변화 시점",
                  "건강 관리 가이드",
                  "성장 기회 포착"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/learn" element={
            <Layout>
              <PlaceholderPage 
                title="학습 센터" 
                description="명리학의 기초부터 고급까지, 체계적인 학습을 제공합니다."
                features={[
                  "기초 이론 학습",
                  "실전 적용 방법",
                  "역사적 배경",
                  "현대적 해석"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/learn/basics" element={
            <Layout>
              <PlaceholderPage 
                title="명리학 기초" 
                description="명리학의 기본 원리와 핵심 개념을 쉽게 배워보세요."
                features={[
                  "음양오행 이론",
                  "십간십지 체계",
                  "사주팔자 구조",
                  "기본 해석법"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/faq" element={
            <Layout>
              <PlaceholderPage 
                title="자주 묻는 질문" 
                description="신비학 서비스와 HEAL7 플랫폼에 대한 모든 궁금증을 해결해드립니다."
                features={[
                  "사주·타로·별자리 서비스 안내",
                  "신비용품 주문 및 배송",
                  "결제 및 환불 정책",
                  "개인정보 보호 및 보안"
                ]}
              />
            </Layout>
          } />
          
          {/* 신비학 서비스 라우트 */}
          <Route path="/tarot" element={
            <Layout>
              <PlaceholderPage 
                title="🎭 타로 리딩" 
                description="78장의 타로카드를 통해 현재 상황과 미래의 가능성을 탐구합니다."
                features={[
                  "현재 상황 분석",
                  "미래 가능성 탐구",
                  "숨겨진 메시지 해독",
                  "행동 지침 제공"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/sasang" element={
            <Layout>
              <PlaceholderPage 
                title="🌿 사상체질 진단" 
                description="태양인, 태음인, 소양인, 소음인 - 당신의 타고난 체질을 발견하세요."
                features={[
                  "체질별 특성 분석",
                  "건강 관리법 제공",
                  "음식 궁합 가이드",
                  "라이프스타일 조언"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/astrology" element={
            <Layout>
              <PlaceholderPage 
                title="⭐ 서양 별자리" 
                description="12개 별자리와 행성의 움직임을 통해 당신의 성격과 운명을 알아보세요."
                features={[
                  "별자리별 성격 분석",
                  "행성의 영향력",
                  "월간 운세 제공",
                  "궁합 분석"
                ]}
              />
            </Layout>
          } />
          
          <Route path="/fengshui" element={
            <Layout>
              <PlaceholderPage 
                title="🧭 풍수지리" 
                description="집과 사무실의 기운을 개선하여 운을 높이는 풍수지리 컨설팅을 제공합니다."
                features={[
                  "공간 에너지 진단",
                  "가구 배치 조언",
                  "색채 치료법",
                  "개운법 제시"
                ]}
              />
            </Layout>
          } />
          
          {/* 스토어 라우트 */}
          <Route path="/store" element={
            <Layout>
              <PlaceholderPage 
                title="💎 신비로운 아이템 스토어" 
                description="영적 성장과 개운을 위한 특별한 아이템들을 만나보세요."
                features={[
                  "천연 크리스탈 컬렉션",
                  "전문가 작성 사주 해석서",
                  "개인 맞춤 개운 팔찌",
                  "타로카드 & 안내서"
                ]}
              />
            </Layout>
          } />
          
          {/* 매거진 라우트 */}
          <Route path="/magazine" element={
            <Layout>
              <PlaceholderPage 
                title="📚 HEAL7 매거진" 
                description="신비학과 영성에 관한 깊이 있는 인사이트와 전문 지식을 제공합니다."
                features={[
                  "사주명리 전문 콘텐츠",
                  "타로 및 점술 가이드",
                  "체질 맞춤 건강관리",
                  "별자리 월간 운세"
                ]}
              />
            </Layout>
          } />
          
          {/* 커뮤니티 라우트 */}
          <Route path="/community" element={
            <Layout>
              <PlaceholderPage 
                title="👥 HEAL7 커뮤니티" 
                description="같은 관심사를 가진 사람들과 신비로운 이야기를 나누어보세요."
                features={[
                  "사주 해석 경험 공유",
                  "타로 리딩 후기",
                  "전문가 Q&A 코너",
                  "월간 신비 이벤트"
                ]}
              />
            </Layout>
          } />
          
          {/* 404 fallback */}
          <Route path="*" element={<ViteSajuMain />} />
        </Routes>
      </Suspense>
    </div>
  )
}

export default App
