const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // 스크린샷 저장 디렉토리
  const screenshotDir = '/home/ubuntu/mcp-tools/shared-captures';
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  const baseUrl = 'http://localhost:5174';
  const results = [];

  // 테스트할 경로들
  const testRoutes = [
    { path: '/', pageId: 'dashboard', label: '메인 대시보드' },
    { path: '/saju', pageId: 'saju', label: '사주명리' },
    { path: '/tarot', pageId: 'tarot', label: '타로카드' },
    { path: '/zodiac', pageId: 'zodiac', label: '띠운세' },
    { path: '/dream', pageId: 'dream', label: '꿈풀이' },
    { path: '/fortune', pageId: 'fortune', label: '종합운세' },
    { path: '/consultation', pageId: 'consultation', label: '상담' },
    { path: '/calendar', pageId: 'calendar', label: '운세달력' },
    { path: '/magazine', pageId: 'magazine', label: '매거진' },
    { path: '/store', pageId: 'store', label: '스토어' },
    { path: '/notices', pageId: 'notices', label: '공지사항' }
  ];

  console.log(`\n🧪 사주앱 라우팅 종합 테스트 시작 (${testRoutes.length}개 페이지)`);
  console.log('=' * 60);

  for (let i = 0; i < testRoutes.length; i++) {
    const route = testRoutes[i];
    const url = baseUrl + route.path;
    
    try {
      console.log(`\n📍 테스트 ${i + 1}/${testRoutes.length}: ${route.label} (${route.path})`);
      
      // 페이지 이동
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.waitForTimeout(2000); // 애니메이션 완료 대기
      
      // 페이지 제목 확인
      const title = await page.title();
      
      // URL 확인
      const currentUrl = page.url();
      
      // 네비게이션 요소 확인
      const navButtons = await page.$$('button');
      const navButtonCount = navButtons.length;
      
      // 메인 콘텐츠 확인
      const mainContent = await page.$('main');
      const hasMainContent = mainContent !== null;
      
      // 로딩 상태 확인 (로딩 중이 아니어야 함)
      const loadingElements = await page.$$('[class*="loading"]');
      const isLoading = loadingElements.length > 0;
      
      // 스크린샷 캡처
      const screenshotPath = path.join(screenshotDir, `saju-routing-${route.pageId}.png`);
      await page.screenshot({ 
        path: screenshotPath,
        fullPage: true 
      });
      
      // 결과 기록
      const result = {
        route: route.path,
        pageId: route.pageId,
        label: route.label,
        title: title,
        currentUrl: currentUrl,
        navButtonCount: navButtonCount,
        hasMainContent: hasMainContent,
        isLoading: isLoading,
        screenshot: screenshotPath,
        status: 'success'
      };
      
      results.push(result);
      
      console.log(`  ✅ 성공: ${title}`);
      console.log(`  📊 네비게이션 버튼: ${navButtonCount}개`);
      console.log(`  🎯 메인 콘텐츠: ${hasMainContent ? '존재' : '없음'}`);
      console.log(`  📸 스크린샷: ${screenshotPath}`);
      
    } catch (error) {
      console.error(`  ❌ 실패: ${route.label} - ${error.message}`);
      results.push({
        route: route.path,
        pageId: route.pageId,
        label: route.label,
        error: error.message,
        status: 'failed'
      });
    }
  }

  // 브라우저 히스토리 테스트
  console.log(`\n🔄 브라우저 히스토리 테스트`);
  try {
    await page.goto(baseUrl + '/saju');
    await page.waitForTimeout(1000);
    
    await page.goto(baseUrl + '/tarot');
    await page.waitForTimeout(1000);
    
    // 뒤로가기
    await page.goBack();
    await page.waitForTimeout(1000);
    const backUrl = page.url();
    
    // 앞으로가기
    await page.goForward();
    await page.waitForTimeout(1000);
    const forwardUrl = page.url();
    
    console.log(`  ✅ 뒤로가기: ${backUrl.includes('/saju') ? '성공' : '실패'}`);
    console.log(`  ✅ 앞으로가기: ${forwardUrl.includes('/tarot') ? '성공' : '실패'}`);
    
  } catch (error) {
    console.error(`  ❌ 히스토리 테스트 실패: ${error.message}`);
  }

  // 결과 요약
  console.log(`\n📊 테스트 결과 요약`);
  console.log('=' * 40);
  
  const successCount = results.filter(r => r.status === 'success').length;
  const failCount = results.filter(r => r.status === 'failed').length;
  
  console.log(`총 테스트: ${results.length}개`);
  console.log(`성공: ${successCount}개`);
  console.log(`실패: ${failCount}개`);
  console.log(`성공률: ${Math.round((successCount / results.length) * 100)}%`);
  
  // 결과를 JSON 파일로 저장
  const reportPath = path.join(screenshotDir, 'saju-routing-test-results.json');
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
  console.log(`\n📋 상세 결과: ${reportPath}`);
  
  await browser.close();
  
  console.log(`\n🏁 테스트 완료!`);
})();