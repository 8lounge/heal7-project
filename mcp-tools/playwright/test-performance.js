const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const baseUrl = 'http://localhost:5174';

  console.log('⚡ 성능 메트릭 측정 및 최적화 상태 분석');
  console.log('=' .repeat(50));

  const performanceResults = [];

  // 주요 페이지들에 대한 성능 테스트
  const testPages = [
    { path: '/', name: 'Dashboard', critical: true },
    { path: '/saju', name: 'Saju Calculator', critical: true },
    { path: '/tarot', name: 'Tarot Reader', critical: false },
    { path: '/zodiac', name: 'Zodiac Analysis', critical: false }
  ];

  for (const testPage of testPages) {
    console.log(`\n🚀 ${testPage.name} 성능 테스트`);
    
    try {
      // Navigation Timing API를 사용한 로딩 시간 측정
      const startTime = Date.now();
      
      await page.goto(baseUrl + testPage.path, { waitUntil: 'networkidle' });
      
      const endTime = Date.now();
      const totalTime = endTime - startTime;
      
      // 성능 메트릭 수집
      const metrics = await page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');
        
        return {
          // 핵심 로딩 메트릭
          domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
          loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
          
          // Paint 메트릭
          firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
          firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
          
          // 리소스 카운트
          resourceCount: performance.getEntriesByType('resource').length,
          
          // 메모리 사용량 (가능한 경우)
          memoryUsage: performance.memory ? {
            used: performance.memory.usedJSHeapSize,
            total: performance.memory.totalJSHeapSize,
            limit: performance.memory.jsHeapSizeLimit
          } : null
        };
      });
      
      // React 컴포넌트 렌더링 시간 추정
      await page.waitForTimeout(2000); // 애니메이션 완료 대기
      
      // 인터랙션 가능 여부 확인
      const interactiveElements = await page.$$('button:not([disabled])');
      const isInteractive = interactiveElements.length > 0;
      
      // 이미지 로딩 상태 확인
      const images = await page.$$('img');
      let imageLoadCount = 0;
      for (const img of images) {
        const isLoaded = await img.evaluate(el => el.complete && el.naturalHeight !== 0);
        if (isLoaded) imageLoadCount++;
      }
      
      const result = {
        page: testPage.name,
        path: testPage.path,
        critical: testPage.critical,
        totalTime: totalTime,
        metrics: metrics,
        interactive: isInteractive,
        imageLoadRate: images.length > 0 ? (imageLoadCount / images.length * 100).toFixed(1) : 100,
        status: 'success'
      };
      
      performanceResults.push(result);
      
      console.log(`   ⏱️  총 로딩 시간: ${totalTime}ms`);
      console.log(`   🎨 First Paint: ${metrics.firstPaint.toFixed(1)}ms`);
      console.log(`   📄 First Contentful Paint: ${metrics.firstContentfulPaint.toFixed(1)}ms`);
      console.log(`   📦 리소스 개수: ${metrics.resourceCount}개`);
      console.log(`   🖱️  인터랙션 가능: ${isInteractive ? '예' : '아니오'}`);
      console.log(`   🖼️  이미지 로딩률: ${result.imageLoadRate}%`);
      
      if (metrics.memoryUsage) {
        const memUsedMB = (metrics.memoryUsage.used / 1024 / 1024).toFixed(1);
        console.log(`   💾 메모리 사용: ${memUsedMB}MB`);
      }
      
      // 성능 등급 평가
      let grade = 'A';
      if (totalTime > 3000) grade = 'C';
      else if (totalTime > 2000) grade = 'B';
      else if (totalTime > 1000) grade = 'B+';
      
      console.log(`   📊 성능 등급: ${grade}`);
      
    } catch (error) {
      console.error(`   ❌ 성능 테스트 실패: ${error.message}`);
      performanceResults.push({
        page: testPage.name,
        path: testPage.path,
        error: error.message,
        status: 'failed'
      });
    }
  }

  // 번들 크기 및 최적화 상태 분석
  console.log(`\n📦 번들 크기 및 최적화 분석`);
  
  try {
    await page.goto(baseUrl, { waitUntil: 'networkidle' });
    
    const networkAnalysis = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource');
      const analysis = {
        jsFiles: resources.filter(r => r.name.includes('.js')),
        cssFiles: resources.filter(r => r.name.includes('.css')),
        imageFiles: resources.filter(r => r.name.match(/\.(png|jpg|jpeg|gif|webp|svg)$/i)),
        totalSize: 0,
        compressedSize: 0
      };
      
      // 전송 크기 계산 (가능한 경우)
      resources.forEach(resource => {
        if (resource.transferSize) {
          analysis.totalSize += resource.transferSize;
        }
        if (resource.encodedBodySize) {
          analysis.compressedSize += resource.encodedBodySize;
        }
      });
      
      return analysis;
    });
    
    console.log(`   🟨 JavaScript 파일: ${networkAnalysis.jsFiles.length}개`);
    console.log(`   🟦 CSS 파일: ${networkAnalysis.cssFiles.length}개`);
    console.log(`   🖼️  이미지 파일: ${networkAnalysis.imageFiles.length}개`);
    
    if (networkAnalysis.totalSize > 0) {
      const totalSizeKB = (networkAnalysis.totalSize / 1024).toFixed(1);
      console.log(`   📊 전체 전송 크기: ${totalSizeKB}KB`);
    }
    
  } catch (error) {
    console.error(`   ❌ 번들 분석 실패: ${error.message}`);
  }

  // 접근성 기본 체크
  console.log(`\n♿ 접근성 및 사용자 경험 체크`);
  
  try {
    await page.goto(baseUrl + '/saju', { waitUntil: 'networkidle' });
    
    // 키보드 네비게이션 테스트
    await page.keyboard.press('Tab');
    const focusedElement = await page.evaluate(() => document.activeElement.tagName);
    console.log(`   ⌨️  키보드 포커스: ${focusedElement || '없음'}`);
    
    // 색상 대비 (간접 확인 - 다크/라이트 테마)
    const themeToggle = await page.$('button:has-text("라이트")') || await page.$('button:has-text("다크")');
    console.log(`   🎨 테마 전환: ${themeToggle ? '지원' : '미지원'}`);
    
    // 반응형 디자인 확인
    await page.setViewportSize({ width: 375, height: 812 });
    await page.waitForTimeout(1000);
    
    const mobileElements = await page.$$('.sm\\:hidden');
    const responsiveDesign = mobileElements.length > 0;
    console.log(`   📱 반응형 디자인: ${responsiveDesign ? '구현됨' : '미구현'}`);
    
  } catch (error) {
    console.error(`   ❌ 접근성 체크 실패: ${error.message}`);
  }

  // 종합 평가 및 권장사항
  console.log(`\n📋 종합 평가 및 권장사항`);
  console.log('=' .repeat(40));
  
  const successfulTests = performanceResults.filter(r => r.status === 'success');
  const avgLoadTime = successfulTests.reduce((sum, r) => sum + r.totalTime, 0) / successfulTests.length;
  
  console.log(`✅ 테스트 성공률: ${successfulTests.length}/${performanceResults.length} (${Math.round(successfulTests.length/performanceResults.length*100)}%)`);
  console.log(`⏱️  평균 로딩 시간: ${avgLoadTime.toFixed(0)}ms`);
  
  // 권장사항
  console.log(`\n💡 최적화 권장사항:`);
  
  if (avgLoadTime > 2000) {
    console.log(`   🚨 로딩 시간 개선 필요 (현재 ${avgLoadTime.toFixed(0)}ms > 권장 2000ms)`);
    console.log(`   - 코드 스플리팅 적용 검토`);
    console.log(`   - 이미지 최적화 (WebP, 지연 로딩)`);
    console.log(`   - 불필요한 JavaScript 제거`);
  } else {
    console.log(`   ✅ 로딩 성능 양호 (${avgLoadTime.toFixed(0)}ms)`);
  }
  
  console.log(`   🔍 SEO 개선사항:`);
  console.log(`   - 동적 메타데이터 설정 개선 필요`);
  console.log(`   - Twitter Card 메타태그 추가`);
  console.log(`   - 접근성 ARIA 라벨 보강`);

  await browser.close();
  
  // 결과 파일 저장
  const reportPath = '/home/ubuntu/mcp-tools/shared-captures/performance-test-results.json';
  fs.writeFileSync(reportPath, JSON.stringify({
    summary: {
      totalTests: performanceResults.length,
      successfulTests: successfulTests.length,
      averageLoadTime: avgLoadTime,
      testDate: new Date().toISOString()
    },
    results: performanceResults
  }, null, 2));
  
  console.log(`\n📊 상세 결과: ${reportPath}`);
  console.log(`🏁 성능 분석 완료!`);
})();