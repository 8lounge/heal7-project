const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const baseUrl = 'http://localhost:5174';
  const results = [];

  console.log('🔍 SEO 메타데이터 및 동적 설정 테스트');
  console.log('=' .repeat(50));

  // 테스트할 라우트와 예상 메타데이터
  const testRoutes = [
    {
      path: '/',
      pageId: 'dashboard',
      expectedTitle: '치유마녀 - HEAL-WITCH',
      expectedKeywords: ['운세', '사주명리', '타로카드', '꿈풀이', '치유마녀']
    },
    {
      path: '/saju',
      pageId: 'saju',
      expectedTitle: '사주명리 | 치유마녀',
      expectedKeywords: ['사주', '명리', '팔자', '대운', '세운']
    },
    {
      path: '/zodiac',
      pageId: 'zodiac',
      expectedTitle: '띠운세 | 치유마녀',
      expectedKeywords: ['띠운세', '12띠', '간지']
    },
    {
      path: '/tarot',
      pageId: 'tarot',
      expectedTitle: '타로카드 | 치유마녀',
      expectedKeywords: ['타로', '카드', '리딩']
    }
  ];

  for (let i = 0; i < testRoutes.length; i++) {
    const route = testRoutes[i];
    
    try {
      console.log(`\n📍 ${route.pageId.toUpperCase()} 페이지 SEO 테스트`);
      
      await page.goto(baseUrl + route.path, { waitUntil: 'networkidle' });
      await page.waitForTimeout(3000); // 동적 메타데이터 설정 대기
      
      // 페이지 제목 확인
      const title = await page.title();
      const titleMatch = title.includes(route.expectedTitle.split(' |')[0]);
      
      console.log(`   📝 페이지 제목: "${title}"`);
      console.log(`   ${titleMatch ? '✅' : '❌'} 제목 매칭: ${titleMatch ? '정상' : '불일치'}`);
      
      // Meta Description 확인
      const description = await page.$eval('meta[name="description"]', el => el.content).catch(() => null);
      const hasDescription = description && description.length > 0;
      
      console.log(`   📄 Description: ${hasDescription ? '존재' : '없음'} (${description?.length || 0}자)`);
      
      // Meta Keywords 확인
      const keywords = await page.$eval('meta[name="keywords"]', el => el.content).catch(() => null);
      const hasKeywords = keywords && keywords.length > 0;
      
      if (hasKeywords) {
        const keywordMatch = route.expectedKeywords.some(keyword => 
          keywords.toLowerCase().includes(keyword.toLowerCase())
        );
        console.log(`   🔑 Keywords: ${keywordMatch ? '매칭' : '불일치'} - "${keywords.substring(0, 50)}..."`);
      } else {
        console.log(`   🔑 Keywords: 설정되지 않음`);
      }
      
      // Open Graph 메타태그 확인
      const ogTitle = await page.$eval('meta[property="og:title"]', el => el.content).catch(() => null);
      const ogDescription = await page.$eval('meta[property="og:description"]', el => el.content).catch(() => null);
      const ogImage = await page.$eval('meta[property="og:image"]', el => el.content).catch(() => null);
      
      console.log(`   📱 OG Title: ${ogTitle ? '설정됨' : '없음'}`);
      console.log(`   📱 OG Description: ${ogDescription ? '설정됨' : '없음'}`);
      console.log(`   📱 OG Image: ${ogImage ? '설정됨' : '없음'}`);
      
      // Twitter Card 메타태그 확인
      const twitterCard = await page.$eval('meta[name="twitter:card"]', el => el.content).catch(() => null);
      const twitterTitle = await page.$eval('meta[name="twitter:title"]', el => el.content).catch(() => null);
      
      console.log(`   🐦 Twitter Card: ${twitterCard ? '설정됨' : '없음'}`);
      console.log(`   🐦 Twitter Title: ${twitterTitle ? '설정됨' : '없음'}`);
      
      // 접근성 관련 요소 확인
      const srOnlyElements = await page.$$('.sr-only');
      const ariaLabels = await page.$$('[aria-label]');
      
      console.log(`   ♿ 접근성: SR-Only ${srOnlyElements.length}개, ARIA Labels ${ariaLabels.length}개`);
      
      // 결과 기록
      results.push({
        path: route.path,
        pageId: route.pageId,
        title: title,
        titleMatch: titleMatch,
        hasDescription: hasDescription,
        hasKeywords: hasKeywords,
        hasOgTags: !!(ogTitle && ogDescription),
        hasTwitterTags: !!(twitterCard && twitterTitle),
        accessibilityElements: srOnlyElements.length + ariaLabels.length,
        status: 'success'
      });
      
    } catch (error) {
      console.error(`   ❌ 실패: ${error.message}`);
      results.push({
        path: route.path,
        pageId: route.pageId,
        error: error.message,
        status: 'failed'
      });
    }
  }

  // 개발 모드 디버깅 정보 확인
  console.log(`\n🔧 개발 모드 디버깅 요소 확인`);
  await page.goto(baseUrl + '/saju', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  const debugElement = await page.$('[title*="라우트 정보"]');
  const hasDebugInfo = debugElement !== null;
  console.log(`   🐛 디버깅 정보: ${hasDebugInfo ? '표시됨 (개발 모드)' : '숨겨짐'}`);

  // 라우터 기능 동작 확인
  console.log(`\n🔄 동적 라우팅 기능 테스트`);
  
  // 페이지 변경 시 URL 업데이트 확인
  await page.goto(baseUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  
  const initialUrl = page.url();
  console.log(`   🏠 초기 URL: ${initialUrl}`);
  
  // 네비게이션 버튼 클릭 (사주 메뉴)
  const sajuButton = await page.$('button:has-text("사주명리")');
  if (sajuButton) {
    await sajuButton.click();
    await page.waitForTimeout(1500);
    
    const newUrl = page.url();
    const urlChanged = newUrl !== initialUrl;
    console.log(`   🔮 사주 클릭 후 URL: ${newUrl}`);
    console.log(`   ${urlChanged ? '✅' : '❌'} URL 변경: ${urlChanged ? '정상' : '실패'}`);
  }

  // 최종 결과 요약
  console.log(`\n📊 SEO 및 라우팅 테스트 결과 요약`);
  console.log('=' .repeat(40));
  
  const successCount = results.filter(r => r.status === 'success').length;
  const withTitleCount = results.filter(r => r.titleMatch).length;
  const withMetaCount = results.filter(r => r.hasDescription && r.hasKeywords).length;
  const withOgCount = results.filter(r => r.hasOgTags).length;
  
  console.log(`✅ 성공한 페이지: ${successCount}/${results.length}개`);
  console.log(`📝 올바른 제목: ${withTitleCount}/${successCount}개`);
  console.log(`📄 기본 메타태그: ${withMetaCount}/${successCount}개`);
  console.log(`📱 Open Graph: ${withOgCount}/${successCount}개`);

  await browser.close();
  
  console.log(`\n🏁 SEO 테스트 완료!`);
  
  // 결과 파일 저장
  const reportPath = '/home/ubuntu/mcp-tools/shared-captures/seo-test-results.json';
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
  console.log(`📋 상세 결과: ${reportPath}`);
})();