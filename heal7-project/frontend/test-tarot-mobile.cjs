// 78타로 카드 서비스 및 반응형 레이아웃 테스트
const { chromium } = require('playwright');

async function testTarotService() {
  console.log('🚀 78타로 카드 서비스 테스트 시작...\n');
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  
  // 데스크톱 뷰포트
  console.log('📱 데스크톱 뷰포트 테스트 (1920x1080)');
  const desktopPage = await browser.newPage({
    viewport: { width: 1920, height: 1080 }
  });
  
  try {
    await desktopPage.goto('http://localhost:4173');
    await desktopPage.waitForTimeout(2000);
    
    console.log('✅ 메인 페이지 로드 성공');
    
    // 타로 섹션으로 이동
    const tarotButton = await desktopPage.locator('text=타로').first();
    if (await tarotButton.isVisible()) {
      await tarotButton.click();
      await desktopPage.waitForTimeout(2000);
      console.log('✅ 타로 섹션 접속 성공');
      
      // 78타로 카드 데이터 확인
      const cardElements = await desktopPage.locator('[data-testid*="tarot"], .tarot, [class*="tarot"]').count();
      console.log(`📋 타로 관련 요소 개수: ${cardElements}`);
      
      // 스프레드 선택 확인
      const spreadElements = await desktopPage.locator('text=/스프레드|배치|카드|원 카드|쓰리 카드/', { timeout: 5000 }).count();
      console.log(`🃏 스프레드 선택 요소: ${spreadElements}개`);
      
    } else {
      console.log('⚠️  타로 버튼을 찾을 수 없음');
    }
    
    // 스크린샷 촬영
    await desktopPage.screenshot({ 
      path: '/tmp/desktop-view.png', 
      fullPage: true 
    });
    console.log('📸 데스크톱 스크린샷 저장: /tmp/desktop-view.png');
    
  } catch (error) {
    console.error('❌ 데스크톱 테스트 오류:', error.message);
  }
  
  // 모바일 뷰포트 테스트
  console.log('\n📱 모바일 뷰포트 테스트 (375x667 - iPhone SE)');
  const mobilePage = await browser.newPage({
    viewport: { width: 375, height: 667 }
  });
  
  try {
    await mobilePage.goto('http://localhost:4173');
    await mobilePage.waitForTimeout(2000);
    
    console.log('✅ 모바일 페이지 로드 성공');
    
    // 메뉴 오버플로우 확인
    const navigation = await mobilePage.locator('nav, [role="navigation"], .navigation, .menu');
    if (await navigation.count() > 0) {
      const navBox = await navigation.first().boundingBox();
      console.log(`📐 네비게이션 크기: ${navBox ? `${navBox.width}x${navBox.height}` : '측정 불가'}`);
      
      // 메뉴 항목들 확인
      const menuItems = await mobilePage.locator('nav a, nav button, .menu a, .menu button').count();
      console.log(`📋 메뉴 항목 개수: ${menuItems}개`);
      
      // 스크롤 가능성 확인
      const isScrollable = await mobilePage.evaluate(() => {
        const nav = document.querySelector('nav, [role="navigation"], .navigation, .menu');
        return nav ? nav.scrollWidth > nav.clientWidth : false;
      });
      
      console.log(`🔄 가로 스크롤 필요: ${isScrollable ? '예 (메뉴가 잘림)' : '아니오'}`);
      
      if (isScrollable) {
        console.log('⚠️  모바일에서 메뉴 항목이 잘리고 있음 - 개선 필요!');
      }
    }
    
    // 타로 기능 모바일 테스트
    const tarotButton = await mobilePage.locator('text=타로').first();
    if (await tarotButton.isVisible()) {
      await tarotButton.click();
      await mobilePage.waitForTimeout(2000);
      console.log('✅ 모바일 타로 섹션 접속 성공');
      
      // 모바일에서 카드 레이아웃 확인
      const cardLayout = await mobilePage.evaluate(() => {
        const cards = document.querySelectorAll('[class*="card"], .tarot');
        return cards.length > 0 ? 'cards found' : 'no cards';
      });
      console.log(`🃏 모바일 카드 레이아웃: ${cardLayout}`);
      
    } else {
      console.log('⚠️  모바일에서 타로 버튼을 찾을 수 없음');
    }
    
    // 모바일 스크린샷 촬영
    await mobilePage.screenshot({ 
      path: '/tmp/mobile-view.png', 
      fullPage: true 
    });
    console.log('📸 모바일 스크린샷 저장: /tmp/mobile-view.png');
    
  } catch (error) {
    console.error('❌ 모바일 테스트 오류:', error.message);
  }
  
  // 태블릿 뷰포트 테스트 (iPad)
  console.log('\n📱 태블릿 뷰포트 테스트 (768x1024 - iPad)');
  const tabletPage = await browser.newPage({
    viewport: { width: 768, height: 1024 }
  });
  
  try {
    await tabletPage.goto('http://localhost:4173');
    await tabletPage.waitForTimeout(2000);
    
    const tarotButton = await tabletPage.locator('text=타로').first();
    if (await tarotButton.isVisible()) {
      await tarotButton.click();
      await tabletPage.waitForTimeout(2000);
      console.log('✅ 태블릿 타로 섹션 접속 성공');
    }
    
    await tabletPage.screenshot({ 
      path: '/tmp/tablet-view.png', 
      fullPage: true 
    });
    console.log('📸 태블릿 스크린샷 저장: /tmp/tablet-view.png');
    
  } catch (error) {
    console.error('❌ 태블릿 테스트 오류:', error.message);
  }
  
  await browser.close();
  
  console.log('\n🏁 테스트 완료!');
  console.log('스크린샷 파일:');
  console.log('- 데스크톱: /tmp/desktop-view.png');
  console.log('- 모바일: /tmp/mobile-view.png');  
  console.log('- 태블릿: /tmp/tablet-view.png');
}

testTarotService().catch(console.error);