#!/usr/bin/env python3
"""
🎯 Smart Crawler 시스템 데모
3-Tier 크롤링 시스템과 멀티모달 AI 분석 테스트

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import asyncio
import logging
import time
from pathlib import Path

from core.smart_crawler import SmartCrawler, CrawlStrategy
from multimodal.ai_analyzer import MultimodalAnalyzer
from multimodal.document_processor import DocumentProcessor


# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_basic_crawling():
    """기본 크롤링 데모"""
    logger.info("🎯 기본 크롤링 데모 시작")
    
    crawler = SmartCrawler()
    
    try:
        await crawler.initialize()
        
        # 테스트할 URL들
        test_urls = [
            "https://httpbin.org/json",  # JSON API (httpx 테스트)
            "https://example.com",       # 정적 사이트 (httpx/playwright)
            "https://www.google.com"     # 동적 사이트 (playwright)
        ]
        
        for url in test_urls:
            logger.info(f"📡 크롤링 테스트: {url}")
            
            result = await crawler.crawl(url, strategy=CrawlStrategy.AUTO)
            
            if result.success:
                logger.info(f"✅ 성공 - {result.crawler_used.value}")
                logger.info(f"   응답 크기: {len(result.html) if result.html else 0} bytes")
                logger.info(f"   응답 시간: {result.response_time:.2f}초")
            else:
                logger.error(f"❌ 실패 - {result.error}")
            
            print("-" * 60)
    
    finally:
        await crawler.cleanup()


async def demo_batch_crawling():
    """배치 크롤링 데모"""
    logger.info("🚀 배치 크롤링 데모 시작")
    
    crawler = SmartCrawler()
    
    try:
        await crawler.initialize()
        
        # 여러 URL 동시 크롤링
        urls = [
            "https://httpbin.org/status/200",
            "https://httpbin.org/json",
            "https://httpbin.org/html",
            "https://httpbin.org/xml",
            "https://httpbin.org/delay/1"
        ]
        
        start_time = time.time()
        results = await crawler.batch_crawl(urls, max_concurrent=3)
        end_time = time.time()
        
        # 결과 분석
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        logger.info(f"📊 배치 크롤링 완료:")
        logger.info(f"   총 소요 시간: {end_time - start_time:.2f}초")
        logger.info(f"   성공: {len(successful)}/{len(urls)}")
        logger.info(f"   실패: {len(failed)}/{len(urls)}")
        
        # 크롤러별 사용 통계
        crawler_usage = {}
        for result in successful:
            crawler_type = result.crawler_used.value
            crawler_usage[crawler_type] = crawler_usage.get(crawler_type, 0) + 1
        
        logger.info(f"   크롤러 사용: {crawler_usage}")
    
    finally:
        await crawler.cleanup()


async def demo_strategy_comparison():
    """크롤링 전략 비교 데모"""
    logger.info("⚖️ 크롤링 전략 비교 데모")
    
    crawler = SmartCrawler()
    test_url = "https://httpbin.org/html"
    
    try:
        await crawler.initialize()
        
        strategies = [
            CrawlStrategy.FAST,
            CrawlStrategy.RENDER,
            CrawlStrategy.AUTO
        ]
        
        for strategy in strategies:
            logger.info(f"🎯 전략 테스트: {strategy.value}")
            
            start_time = time.time()
            result = await crawler.crawl(test_url, strategy=strategy)
            end_time = time.time()
            
            if result.success:
                logger.info(f"   ✅ 성공 - {result.crawler_used.value}")
                logger.info(f"   응답 시간: {end_time - start_time:.2f}초")
            else:
                logger.info(f"   ❌ 실패 - {result.error}")
    
    finally:
        await crawler.cleanup()


async def demo_health_check():
    """시스템 상태 확인 데모"""
    logger.info("🏥 시스템 상태 확인 데모")
    
    crawler = SmartCrawler()
    
    try:
        await crawler.initialize()
        
        health = await crawler.health_check()
        
        logger.info(f"시스템 상태: {'✅ 건강' if health['system_healthy'] else '❌ 문제'}")
        logger.info(f"초기화 상태: {health['initialized']}")
        logger.info(f"사용 가능한 크롤러: {health['available_crawlers']}")
        
        # 크롤러별 상세 정보
        for crawler_name, crawler_health in health['crawler_health'].items():
            status = "✅" if crawler_health['healthy'] else "❌"
            logger.info(f"  {status} {crawler_name}: {crawler_health}")
        
        # 성능 요약
        performance = health['performance_summary']
        logger.info(f"성능 요약:")
        logger.info(f"  전체 성공률: {performance['overall_success_rate']:.1%}")
        logger.info(f"  총 요청 수: {performance['total_requests']}")
        logger.info(f"  최고 성능: {performance['best_performer']}")
    
    finally:
        await crawler.cleanup()


async def demo_multimodal_ai():
    """멀티모달 AI 분석 데모"""
    logger.info("🤖 멀티모달 AI 분석 데모")
    
    analyzer = MultimodalAnalyzer()
    
    try:
        await analyzer.initialize()
        
        # 사용 가능한 모델 확인
        stats = analyzer.get_usage_stats()
        logger.info(f"사용 가능한 AI 모델: {stats['available_models']}")
        
        # 간단한 텍스트 이미지 분석 (API 키가 있는 경우)
        if stats['available_models']:
            logger.info("🎨 텍스트 이미지 생성 및 분석 테스트")
            
            # 간단한 테스트 이미지 생성 (PIL 사용)
            from PIL import Image, ImageDraw, ImageFont
            
            # 테스트 이미지 생성
            img = Image.new('RGB', (400, 200), 'white')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            draw.text((20, 50), "HEAL7 크롤링 시스템", fill='black', font=font)
            draw.text((20, 100), "Smart Crawler Test", fill='blue', font=font)
            
            # 이미지를 바이트로 변환
            import io
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()
            
            # AI 분석
            result = await analyzer.analyze_image(
                img_bytes, 
                "이 이미지에서 모든 텍스트를 추출하세요."
            )
            
            if result['success']:
                logger.info(f"✅ AI 분석 성공 ({result['model_used']})")
                logger.info(f"   추출된 텍스트: {result['content'][:100]}...")
            else:
                logger.warning(f"❌ AI 분석 실패: {result.get('error')}")
        
        else:
            logger.info("⚠️ API 키가 설정되지 않아 AI 분석을 건너뜁니다")
    
    except Exception as e:
        logger.error(f"AI 분석 데모 오류: {e}")


async def demo_document_processing():
    """문서 처리 데모"""
    logger.info("📄 문서 처리 데모")
    
    processor = DocumentProcessor()
    
    try:
        await processor.initialize()
        
        # 지원하는 문서 형식
        formats = processor.get_supported_formats()
        logger.info(f"지원하는 문서 형식: {formats}")
        
        # 테스트용 텍스트 파일 생성
        test_file = Path("/tmp/test_document.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("""HEAL7 크롤링 시스템 문서

이것은 테스트 문서입니다.

주요 기능:
1. 3-Tier 크롤링 시스템
2. 멀티모달 AI 분석
3. 자동 폴백 시스템

결론:
강력하고 안정적인 크롤링 솔루션입니다.
""")
        
        # 문서 처리 (AI 분석 제외 - API 키가 없을 수 있음)
        result = await processor.process_document(str(test_file), include_ai_analysis=False)
        
        if result.success:
            logger.info(f"✅ 문서 처리 성공")
            logger.info(f"   문서 타입: {result.document_type.value}")
            logger.info(f"   처리 시간: {result.processing_time:.2f}초")
            logger.info(f"   텍스트 블록 수: {len(result.text_content)}")
            logger.info(f"   테이블 수: {len(result.tables)}")
        else:
            logger.error(f"❌ 문서 처리 실패: {result.error}")
        
        # 테스트 파일 정리
        test_file.unlink()
    
    except Exception as e:
        logger.error(f"문서 처리 데모 오류: {e}")


async def main():
    """메인 데모 실행"""
    logger.info("🎉 HEAL7 Smart Crawler 시스템 데모 시작")
    
    demos = [
        ("기본 크롤링", demo_basic_crawling),
        ("배치 크롤링", demo_batch_crawling),
        ("전략 비교", demo_strategy_comparison),
        ("상태 확인", demo_health_check),
        ("멀티모달 AI", demo_multimodal_ai),
        ("문서 처리", demo_document_processing)
    ]
    
    for demo_name, demo_func in demos:
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"🚀 {demo_name} 데모 시작")
            logger.info(f"{'='*60}")
            
            await demo_func()
            
            logger.info(f"✅ {demo_name} 데모 완료")
            
        except Exception as e:
            logger.error(f"❌ {demo_name} 데모 실패: {e}")
        
        # 데모 간 잠시 대기
        await asyncio.sleep(1)
    
    logger.info(f"\n{'='*60}")
    logger.info("🎊 모든 데모 완료!")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())