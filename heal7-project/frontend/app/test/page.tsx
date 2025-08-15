import { Metadata } from 'next'
import Link from 'next/link'
import { TestTube, Activity, Database, Zap, CheckCircle, AlertTriangle } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Test Environment | Heal7',
  description: 'Heal7 플랫폼의 통합 테스트 환경',
}

const testSuites = [
  {
    icon: TestTube,
    title: 'API 테스트',
    description: '모든 API 엔드포인트의 기능 테스트',
    status: 'passing',
    tests: 24,
    passed: 24,
    href: '/test/api'
  },
  {
    icon: Database,
    title: '데이터베이스 테스트',
    description: '데이터베이스 연결 및 쿼리 성능 테스트',
    status: 'passing',
    tests: 12,
    passed: 12,
    href: '/test/database'
  },
  {
    icon: Activity,
    title: '성능 테스트',
    description: '시스템 성능 및 부하 테스트',
    status: 'warning',
    tests: 8,
    passed: 6,
    href: '/test/performance'
  },
  {
    icon: Zap,
    title: '통합 테스트',
    description: '서비스 간 연동 및 전체 시나리오 테스트',
    status: 'passing',
    tests: 15,
    passed: 15,
    href: '/test/integration'
  }
]

const systemStatus = {
  overall: 'healthy',
  uptime: '99.9%',
  lastDeployment: '2025-08-12T10:30:00Z',
  version: '2.0.0'
}

const recentTests = [
  {
    name: 'API Endpoint Validation',
    status: 'passed',
    duration: '2.3s',
    timestamp: '2025-08-12T10:45:00Z'
  },
  {
    name: 'Database Connection Pool',
    status: 'passed', 
    duration: '1.1s',
    timestamp: '2025-08-12T10:43:00Z'
  },
  {
    name: 'Memory Usage Check',
    status: 'warning',
    duration: '0.8s',
    timestamp: '2025-08-12T10:41:00Z'
  },
  {
    name: 'Saju Service Integration',
    status: 'passed',
    duration: '3.2s',
    timestamp: '2025-08-12T10:40:00Z'
  }
]

export default function TestPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-cyan-100">
      {/* Header */}
      <section className="relative py-20">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="mb-8 flex justify-center">
              <div className="rounded-full bg-gradient-to-r from-blue-600 to-cyan-600 p-3">
                <TestTube className="h-12 w-12 text-white" />
              </div>
            </div>
            <h1 className="mb-6 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
              Heal7 테스트 환경
              <span className="block text-gradient">Test Environment</span>
            </h1>
            <p className="mb-10 text-xl leading-8 text-gray-600">
              시스템의 안정성과 성능을 검증하는 통합 테스트 플랫폼입니다.
              <br />실시간으로 모든 서비스의 상태를 모니터링합니다.
            </p>
            
            {/* System Status Badge */}
            <div className="inline-flex items-center rounded-full bg-white px-6 py-3 shadow-lg">
              <CheckCircle className="mr-2 h-5 w-5 text-green-500" />
              <span className="font-semibold text-gray-900">
                시스템 상태: {systemStatus.overall.toUpperCase()}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                가동률 {systemStatus.uptime}
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Test Suites */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              테스트 스위트
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              각 영역별 테스트 결과를 확인하세요
            </p>
          </div>
          
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {testSuites.map((suite, index) => (
              <Link
                key={suite.title}
                href={suite.href}
                className="group block rounded-2xl bg-white p-8 shadow-lg hover:shadow-xl transition-all duration-300 border"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-center justify-between mb-6">
                  <suite.icon className="h-10 w-10 text-blue-600" />
                  <div className={`rounded-full p-2 ${
                    suite.status === 'passing' ? 'bg-green-100' :
                    suite.status === 'warning' ? 'bg-yellow-100' : 'bg-red-100'
                  }`}>
                    {suite.status === 'passing' ? (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    ) : suite.status === 'warning' ? (
                      <AlertTriangle className="h-5 w-5 text-yellow-600" />
                    ) : (
                      <TestTube className="h-5 w-5 text-red-600" />
                    )}
                  </div>
                </div>
                
                <h3 className="mb-3 text-xl font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                  {suite.title}
                </h3>
                <p className="mb-6 text-gray-600 text-sm">
                  {suite.description}
                </p>
                
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">
                    {suite.passed}/{suite.tests} 통과
                  </span>
                  <span className={`font-semibold ${
                    suite.status === 'passing' ? 'text-green-600' :
                    suite.status === 'warning' ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {suite.status.toUpperCase()}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Recent Tests */}
      <section className="bg-white py-20">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="mb-16 text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                최근 테스트 실행 결과
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                실시간으로 업데이트되는 테스트 결과입니다
              </p>
            </div>
            
            <div className="overflow-hidden rounded-2xl bg-gray-50 shadow-lg">
              <div className="px-6 py-4 bg-gray-100 border-b">
                <h3 className="text-lg font-semibold text-gray-900">
                  Test Execution Log
                </h3>
              </div>
              <div className="divide-y">
                {recentTests.map((test, index) => (
                  <div key={index} className="px-6 py-4 hover:bg-gray-100 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className={`rounded-full p-1 ${
                          test.status === 'passed' ? 'bg-green-100' :
                          test.status === 'warning' ? 'bg-yellow-100' : 'bg-red-100'
                        }`}>
                          {test.status === 'passed' ? (
                            <CheckCircle className="h-4 w-4 text-green-600" />
                          ) : test.status === 'warning' ? (
                            <AlertTriangle className="h-4 w-4 text-yellow-600" />
                          ) : (
                            <TestTube className="h-4 w-4 text-red-600" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{test.name}</p>
                          <p className="text-sm text-gray-500">
                            실행 시간: {test.duration}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`font-semibold text-sm ${
                          test.status === 'passed' ? 'text-green-600' :
                          test.status === 'warning' ? 'text-yellow-600' : 'text-red-600'
                        }`}>
                          {test.status.toUpperCase()}
                        </p>
                        <p className="text-xs text-gray-400">
                          {new Date(test.timestamp).toLocaleTimeString('ko-KR')}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="mt-8 text-center">
              <Link 
                href="/test/logs"
                className="btn-primary px-6 py-3"
              >
                전체 로그 보기
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-12">
              빠른 실행
            </h2>
            
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <Link 
                href="/test/run-all"
                className="btn-primary h-16 px-8 text-lg shadow-lg"
              >
                전체 테스트 실행
                <TestTube className="ml-2 h-6 w-6" />
              </Link>
              <Link 
                href="/test/performance"
                className="btn bg-white hover:bg-gray-50 h-16 px-8 text-lg border shadow-lg"
              >
                성능 테스트 실행
                <Activity className="ml-2 h-6 w-6" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}