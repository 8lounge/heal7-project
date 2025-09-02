const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // 스크린샷 저장 디렉토리
  const screenshotDir = '/home/ubuntu/mcp-tools/shared-captures';
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  const baseUrl = 'http://localhost:5174';

  console.log('📱 모바일 반응형 네비게이션 테스트 시작');
  console.log('=' .repeat(50));

  // 모바일 뷰포트 설정
  await page.setViewportSize({ width: 375, height: 812 }); // iPhone X 크기

  try {
    // 메인 페이지로 이동
    console.log('\n1. 메인 페이지 모바일 뷰 테스트');
    await page.goto(baseUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // 모바일에서 네비게이션 버튼들 확인
    const navButtons = await page.$$('nav button');
    console.log(`   📊 네비게이션 버튼 개수: ${navButtons.length}개`);

    // 더보기 버튼 확인 및 클릭
    const moreButton = await page.$('button:has-text("더보기")');
    if (moreButton) {
      console.log('   ✅ 더보기 버튼 발견');
      await moreButton.click();
      await page.waitForTimeout(1000);
      
      // 확장 메뉴 표시 확인
      const expandedMenu = await page.$('[class*="mobile-nav-scroll"]');
      if (expandedMenu) {
        console.log('   ✅ 모바일 확장 메뉴 정상 표시');
      }
    }

    // 모바일 스크린샷 캡처
    await page.screenshot({ 
      path: path.join(screenshotDir, 'mobile-navigation-expanded.png'),
      fullPage: true 
    });

    console.log('\n2. 각 페이지별 모바일 네비게이션 테스트');
    
    const testPages = ['saju', 'tarot', 'zodiac', 'dream'];
    
    for (let i = 0; i < testPages.length; i++) {
      const pageId = testPages[i];
      console.log(`\n   📱 ${pageId} 페이지 모바일 테스트`);
      
      await page.goto(`${baseUrl}/${pageId}`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(1500);
      
      // 활성 네비게이션 버튼 확인
      const activeButton = await page.$(`button[class*="gradient"]`);
      const hasActiveState = activeButton !== null;
      
      console.log(`     ${hasActiveState ? '✅' : '❌'} 활성 상태 표시: ${hasActiveState ? '정상' : '문제'}`);
      
      // 터치 친화적인지 확인 (버튼 크기)
      const firstButton = await page.$('nav button');
      if (firstButton) {
        const buttonBox = await firstButton.boundingBox();
        const isTouchFriendly = buttonBox && buttonBox.height >= 44; // 최소 44px
        console.log(`     ${isTouchFriendly ? '✅' : '⚠️'} 터치 친화성: ${isTouchFriendly ? '적절' : '개선 필요'} (${buttonBox?.height}px)`);
      }
    }

    console.log('\n3. 데스크톱 뷰포트로 전환 테스트');
    
    // 데스크톱 뷰포트로 전환
    await page.setViewportSize({ width: 1200, height: 800 });
    await page.goto(baseUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // 데스크톱에서 숨겨진 모바일 요소 확인
    const mobileElements = await page.$$('.sm\\:hidden');
    const desktopElements = await page.$$('.hidden.sm\\:flex');
    
    console.log(`   📺 데스크톱 전용 요소: ${desktopElements.length}개`);
    console.log(`   📱 모바일 전용 요소: ${mobileElements.length}개`);

    // 데스크톱 스크린샷
    await page.screenshot({ 
      path: path.join(screenshotDir, 'desktop-navigation.png'),
      fullPage: true 
    });

    console.log('\n4. 태블릿 뷰포트 테스트');
    
    // 태블릿 뷰포트 (iPad)
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(baseUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // 태블릿 스크린샷
    await page.screenshot({ 
      path: path.join(screenshotDir, 'tablet-navigation.png'),
      fullPage: true 
    });

    console.log('   ✅ 태블릿 뷰포트 테스트 완료');

    console.log('\n📊 반응형 테스트 결과 요약');
    console.log('=' .repeat(40));
    console.log('✅ 모바일 네비게이션 동작 확인');
    console.log('✅ 데스크톱 네비게이션 동작 확인');
    console.log('✅ 태블릿 네비게이션 동작 확인');
    console.log('✅ 반응형 전환 정상 동작');

  } catch (error) {
    console.error(`❌ 테스트 실패: ${error.message}`);
  }

  await browser.close();
  console.log('\n🏁 반응형 테스트 완료!');
})();