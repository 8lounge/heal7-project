/**
 * Atomic API 통합 모듈
 * ===================
 * 
 * 백엔드 atomic 모듈과의 통합 및 하이브리드 시스템
 * - 설정 기반 atomic/로컬 전환
 * - 성능 모니터링
 * - 폴백 시스템
 */

// 🚀 Atomic API 전환 설정 (점진적 마이그레이션)
export const ATOMIC_API_CONFIG = {
  /** 
   * 🔥 Atomic API 사용 여부 (기본값: false - 기존 시스템 유지)
   * ⚠️  true로 설정 시 모든 계산이 백엔드 atomic 모듈로 이동
   * 📈 성능: 프론트엔드 로직 제거, 서버 중앙화
   */
  USE_ATOMIC_API: false, // 개발 단계에서는 false로 시작
  
  /** 
   * 🎯 부분적 전환 설정 (특정 기능만 atomic 사용)
   */
  ATOMIC_FEATURES: {
    GAPJA_CALCULATION: true,   // 60갑자 계산을 atomic으로
    YEAR_PILLAR: true,         // 년주 계산을 atomic으로
    LUNAR_CONVERSION: false,   // 음력 변환은 아직 기존 시스템
    COMPLETE_SAJU: false,      // 완전한 사주는 아직 기존 시스템
  },
  
  /** 
   * 🔧 폴백 설정 (atomic API 실패 시 기존 로직 사용)
   */
  ENABLE_FALLBACK: true,
  
  /** 
   * 📊 성능 모니터링 (atomic vs 기존 로직 비교)
   */
  ENABLE_PERFORMANCE_MONITORING: true,
} as const;

// 🚀 Atomic API 통합 (동적 import로 번들 크기 최적화)
let atomicAPIModule: any = null;

async function getAtomicAPI() {
  if (!atomicAPIModule) {
    try {
      atomicAPIModule = await import('../utils/atomicSajuAPI');
    } catch (error) {
      console.warn('Atomic API 모듈 로드 실패:', error);
      return null;
    }
  }
  return atomicAPIModule;
}

// 🎯 성능 모니터링을 위한 유틸리티
interface PerformanceMetric {
  method: 'local' | 'atomic';
  duration: number;
  success: boolean;
  timestamp: number;
}

const performanceMetrics: PerformanceMetric[] = [];

function recordPerformance(method: 'local' | 'atomic', duration: number, success: boolean) {
  if (ATOMIC_API_CONFIG.ENABLE_PERFORMANCE_MONITORING) {
    performanceMetrics.push({
      method,
      duration,
      success,
      timestamp: Date.now()
    });
    
    // 최근 100개 기록만 유지
    if (performanceMetrics.length > 100) {
      performanceMetrics.splice(0, 50);
    }
  }
}

export function getPerformanceMetrics() {
  return [...performanceMetrics];
}

// 🔥 하이브리드 60갑자 계산 함수 (Atomic API + 로컬 계산)
export const get60갑자Hybrid = async (date: Date, localCalculator: (date: Date) => string): Promise<string> => {
  const startTime = performance.now();
  
  // Atomic API 사용 여부 확인
  if (ATOMIC_API_CONFIG.ATOMIC_FEATURES.GAPJA_CALCULATION) {
    try {
      const atomicAPI = await getAtomicAPI();
      if (atomicAPI) {
        const result = await atomicAPI.get60갑자Atomic(date);
        const duration = performance.now() - startTime;
        recordPerformance('atomic', duration, result !== '❌오류');
        
        if (result !== '❌오류') {
          console.log(`🚀 Atomic 60갑자: ${date.toISOString().split('T')[0]} = ${result}`);
          return result;
        }
      }
    } catch (error) {
      console.warn('Atomic API 갑자 계산 실패, 로컬로 폴백:', error);
    }
  }
  
  // 폴백 또는 기본 로컬 계산
  if (ATOMIC_API_CONFIG.ENABLE_FALLBACK || !ATOMIC_API_CONFIG.ATOMIC_FEATURES.GAPJA_CALCULATION) {
    const result = localCalculator(date);
    const duration = performance.now() - startTime;
    recordPerformance('local', duration, true);
    
    // 🔍 9월 5-6일 디버깅 로그 (로컬 계산시에만)
    if (date.getMonth() === 8 && (date.getDate() === 5 || date.getDate() === 6)) {
      console.log(`🔍 로컬 60갑자 계산 (9월 ${date.getDate()}일): ${result}`);
    }
    
    return result;
  }
  
  return '❌오류';
};

// 🔥 하이브리드 년주 계산 함수
export const get년주Hybrid = async (date: Date, localCalculator: (date: Date) => string): Promise<string> => {
  const startTime = performance.now();
  
  // Atomic API 사용 여부 확인
  if (ATOMIC_API_CONFIG.ATOMIC_FEATURES.YEAR_PILLAR) {
    try {
      const atomicAPI = await getAtomicAPI();
      if (atomicAPI) {
        const result = await atomicAPI.get년주Atomic(date);
        const duration = performance.now() - startTime;
        recordPerformance('atomic', duration, result !== '❌오류');
        
        if (result !== '❌오류') {
          console.log(`🚀 Atomic 년주: ${date.toISOString().split('T')[0]} = ${result}`);
          return result;
        }
      }
    } catch (error) {
      console.warn('Atomic API 년주 계산 실패, 로컬로 폴백:', error);
    }
  }
  
  // 폴백 또는 기본 로컬 계산
  if (ATOMIC_API_CONFIG.ENABLE_FALLBACK || !ATOMIC_API_CONFIG.ATOMIC_FEATURES.YEAR_PILLAR) {
    const result = localCalculator(date);
    const duration = performance.now() - startTime;
    recordPerformance('local', duration, true);
    
    return result;
  }
  
  return '❌오류';
};

// 🎯 배치 갑자 계산 (월 전체) - 성능 최적화
export async function getBatchGapjaHybrid(year: number, month: number, localCalculator: (date: Date) => string): Promise<Map<number, string>> {
  const daysInMonth = new Date(year, month, 0).getDate();
  const results = new Map<number, string>();
  
  // Atomic API 배치 호출 시도
  if (ATOMIC_API_CONFIG.ATOMIC_FEATURES.GAPJA_CALCULATION) {
    try {
      const atomicAPI = await getAtomicAPI();
      if (atomicAPI) {
        const batchResults = await atomicAPI.getBatchGapja(year, month);
        if (batchResults.size > 0) {
          console.log(`🚀 Atomic 배치 갑자: ${year}년 ${month}월 (${batchResults.size}일)`);
          return batchResults;
        }
      }
    } catch (error) {
      console.warn('Atomic API 배치 갑자 계산 실패, 로컬로 폴백:', error);
    }
  }
  
  // 폴백: 로컬 계산
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month - 1, day);
    const gapja = localCalculator(date);
    results.set(day, gapja);
  }
  
  return results;
}

// 🔧 설정 변경 함수들
export function enableAtomicFeature(feature: keyof typeof ATOMIC_API_CONFIG.ATOMIC_FEATURES) {
  (ATOMIC_API_CONFIG.ATOMIC_FEATURES as any)[feature] = true;
  console.log(`✅ Atomic 기능 활성화: ${feature}`);
}

export function disableAtomicFeature(feature: keyof typeof ATOMIC_API_CONFIG.ATOMIC_FEATURES) {
  (ATOMIC_API_CONFIG.ATOMIC_FEATURES as any)[feature] = false;
  console.log(`❌ Atomic 기능 비활성화: ${feature}`);
}

export function toggleAtomicAPI() {
  (ATOMIC_API_CONFIG as any).USE_ATOMIC_API = !ATOMIC_API_CONFIG.USE_ATOMIC_API;
  console.log(`🔄 Atomic API 전환: ${ATOMIC_API_CONFIG.USE_ATOMIC_API ? '활성화' : '비활성화'}`);
}

// 📊 성능 리포트 생성
export function generatePerformanceReport() {
  const atomicMetrics = performanceMetrics.filter(m => m.method === 'atomic');
  const localMetrics = performanceMetrics.filter(m => m.method === 'local');
  
  const atomicAvg = atomicMetrics.reduce((sum, m) => sum + m.duration, 0) / atomicMetrics.length;
  const localAvg = localMetrics.reduce((sum, m) => sum + m.duration, 0) / localMetrics.length;
  
  const report = {
    totalCalls: performanceMetrics.length,
    atomicCalls: atomicMetrics.length,
    localCalls: localMetrics.length,
    atomicAvgDuration: atomicAvg || 0,
    localAvgDuration: localAvg || 0,
    performanceImprovement: localAvg && atomicAvg ? ((localAvg - atomicAvg) / localAvg * 100) : 0,
    successRate: {
      atomic: atomicMetrics.filter(m => m.success).length / atomicMetrics.length * 100 || 0,
      local: localMetrics.filter(m => m.success).length / localMetrics.length * 100 || 0
    }
  };
  
  console.log('📊 성능 리포트:', report);
  return report;
}

// 🧪 테스트 및 검증 함수
export async function testAtomicIntegration() {
  console.log('🧪 Atomic 통합 테스트 시작');
  
  try {
    // 설정 확인
    console.log('⚙️ 현재 설정:', ATOMIC_API_CONFIG);
    
    // API 모듈 로드 테스트
    const atomicAPI = await getAtomicAPI();
    if (atomicAPI) {
      console.log('✅ Atomic API 모듈 로드 성공');
      
      // 기본 기능 테스트
      await atomicAPI.testAtomicAPI();
    } else {
      console.log('❌ Atomic API 모듈 로드 실패');
    }
    
    // 성능 리포트 생성
    generatePerformanceReport();
    
    console.log('🎉 Atomic 통합 테스트 완료');
  } catch (error) {
    console.error('❌ Atomic 통합 테스트 실패:', error);
  }
}

export default {
  ATOMIC_API_CONFIG,
  getPerformanceMetrics,
  get60갑자Hybrid,
  get년주Hybrid,
  getBatchGapjaHybrid,
  enableAtomicFeature,
  disableAtomicFeature,
  toggleAtomicAPI,
  generatePerformanceReport,
  testAtomicIntegration
};