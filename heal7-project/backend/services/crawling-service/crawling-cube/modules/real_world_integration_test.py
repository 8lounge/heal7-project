#!/usr/bin/env python3
"""
🧪 실제 정부 포털 사이트 AI 크롤링 통합 테스트
실제 접근 가능한 사이트들로 AI + Playwright 시스템 검증

Author: HEAL7 Development Team
Version: 2.0.0
Date: 2025-08-29
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealWorldTester:
    """🌍 실제 환경 크롤링 테스터"""
    
    def __init__(self):
        self.results_dir = Path(__file__).parent.parent / "test_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # 실제 접근 가능한 정부 포털 사이트들
        self.accessible_test_sites = [
            {
                "name": "기업마당 메인",
                "url": "https://www.bizinfo.go.kr",
                "expected_fields": ["title", "content", "links"],
                "site_type": "government_portal",
                "accessible": True
            },
            {
                "name": "K-Startup 메인",
                "url": "https://www.k-startup.go.kr", 
                "expected_fields": ["title", "programs", "announcements"],
                "site_type": "startup_support",
                "accessible": True
            },
            # 실제 뉴스 사이트 (크롤링 허용)
            {
                "name": "정부24 메인",
                "url": "https://www.gov.kr",
                "expected_fields": ["title", "services", "notices"],
                "site_type": "government_services",
                "accessible": True
            }
        ]
        
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """🚀 종합 통합 테스트 실행"""
        logger.info("🚀 실제 정부 포털 AI 크롤링 통합 테스트 시작")
        
        test_results = {
            "test_started": datetime.now().isoformat(),
            "total_sites": len(self.accessible_test_sites),
            "successful_sites": 0,
            "failed_sites": 0,
            "api_key_status": {},
            "detailed_results": []
        }
        
        # Step 1: API 키 상태 확인
        api_status = await self._check_api_keys_status()
        test_results["api_key_status"] = api_status
        
        # Step 2: 각 사이트별 테스트 실행
        for site_config in self.accessible_test_sites:
            logger.info(f"🔍 테스트 사이트: {site_config['name']}")
            
            site_result = await self._test_single_accessible_site(site_config)
            test_results["detailed_results"].append(site_result)
            
            if site_result["overall_success"]:
                test_results["successful_sites"] += 1
            else:
                test_results["failed_sites"] += 1
        
        # Step 3: 결과 요약 및 저장
        test_results["test_completed"] = datetime.now().isoformat()
        test_results["success_rate"] = (
            test_results["successful_sites"] / test_results["total_sites"] 
            if test_results["total_sites"] > 0 else 0
        )
        
        # 결과 파일 저장
        await self._save_test_results(test_results)
        
        # 결과 요약 출력
        self._print_comprehensive_summary(test_results)
        
        return test_results
    
    async def _check_api_keys_status(self) -> Dict[str, Any]:
        """🔑 API 키 상태 확인"""
        try:
            import sys
            from pathlib import Path
            
            # 부모 디렉토리를 sys.path에 추가
            parent_dir = Path(__file__).parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            from config.api_keys_config import create_api_keys_manager
            
            api_manager = create_api_keys_manager()
            status = api_manager.get_api_status()
            
            logger.info(f"🔑 API 키 상태: Gemini {'✅' if status['gemini_configured'] else '❌'}, "
                       f"Claude {'✅' if status['claude_configured'] else '❌'}")
            
            return {
                "gemini_available": status['gemini_configured'],
                "claude_available": status['claude_configured'], 
                "any_api_available": status['has_any_valid_keys'],
                "fallback_mode": status['fallback_mode_required'],
                "check_successful": True
            }
            
        except Exception as e:
            logger.error(f"❌ API 키 상태 확인 실패: {str(e)}")
            return {
                "gemini_available": False,
                "claude_available": False,
                "any_api_available": False, 
                "fallback_mode": True,
                "check_successful": False,
                "error": str(e)
            }
    
    async def _test_single_accessible_site(self, site_config: Dict) -> Dict[str, Any]:
        """개별 접근 가능한 사이트 테스트"""
        site_result = {
            "site_name": site_config["name"],
            "site_url": site_config["url"],
            "site_type": site_config["site_type"],
            "expected_accessible": site_config["accessible"],
            "overall_success": False,
            "steps_completed": [],
            "errors": []
        }
        
        try:
            # Step 1: 사이트 접근성 테스트
            logger.info(f"  📡 사이트 접근성 확인: {site_config['url']}")
            accessibility_result = await self._test_site_accessibility(site_config["url"])
            site_result["accessibility_test"] = accessibility_result
            
            if accessibility_result["accessible"]:
                site_result["steps_completed"].append("accessibility_check")
                logger.info("  ✅ 사이트 접근 가능")
            else:
                site_result["errors"].append("Site not accessible")
                logger.warning("  ❌ 사이트 접근 불가")
                return site_result
            
            # Step 2: AI 분석 테스트
            logger.info("  🤖 AI 분석 시작")
            ai_result = await self._test_ai_analysis(site_config)
            site_result["ai_analysis"] = ai_result
            
            if ai_result["success"]:
                site_result["steps_completed"].append("ai_analysis")
                logger.info(f"  ✅ AI 분석 완료 - 모델: {ai_result['model_used']}")
            else:
                site_result["errors"].append(f"AI analysis failed: {ai_result.get('error')}")
                logger.warning("  ❌ AI 분석 실패")
            
            # Step 3: Playwright 테스트 (AI 성공 시에만)
            if ai_result["success"]:
                logger.info("  🎭 Playwright 테스트 시작")
                playwright_result = await self._test_playwright_extraction(
                    site_config, ai_result["strategy"]
                )
                site_result["playwright_test"] = playwright_result
                
                if playwright_result["success"]:
                    site_result["steps_completed"].append("playwright_test")
                    logger.info(f"  ✅ Playwright 테스트 완료 - 추출: {playwright_result['items_found']}개")
                else:
                    site_result["errors"].append(f"Playwright failed: {playwright_result.get('error')}")
                    logger.warning("  ❌ Playwright 테스트 실패")
            
            # 전체 성공 여부 결정
            site_result["overall_success"] = len(site_result["steps_completed"]) >= 2
            
        except Exception as e:
            site_result["errors"].append(f"Unexpected error: {str(e)}")
            logger.error(f"  ❌ 예외 발생: {str(e)}")
        
        return site_result
    
    async def _test_site_accessibility(self, url: str) -> Dict[str, Any]:
        """사이트 접근성 테스트"""
        try:
            import aiohttp
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    return {
                        "accessible": response.status == 200,
                        "status_code": response.status,
                        "content_length": len(await response.text()),
                        "content_type": response.headers.get("Content-Type", "")
                    }
                    
        except Exception as e:
            return {
                "accessible": False,
                "error": str(e)
            }
    
    async def _test_ai_analysis(self, site_config: Dict) -> Dict[str, Any]:
        """AI 분석 테스트"""
        try:
            import sys
            from pathlib import Path
            
            # 부모 디렉토리를 sys.path에 추가
            parent_dir = Path(__file__).parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            from modules.ai_research_engine import create_ai_research_engine
            
            # AI 엔진 생성 및 초기화
            ai_engine = create_ai_research_engine()
            await ai_engine.initialize()
            
            try:
                # 웹사이트 구조 분석
                analysis_result = await ai_engine.analyze_website_structure(site_config["url"])
                
                # 수집 전략 생성
                strategy = await ai_engine.generate_collection_strategy(
                    analysis_result, site_config["expected_fields"]
                )
                
                return {
                    "success": True,
                    "model_used": ai_engine.current_model,
                    "confidence_score": analysis_result.confidence_score,
                    "strategy": {
                        "strategy_id": strategy.strategy_id,
                        "selectors": strategy.selectors,
                        "confidence": strategy.confidence.value
                    }
                }
                
            finally:
                await ai_engine.close()
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": "none"
            }
    
    async def _test_playwright_extraction(self, site_config: Dict, strategy_data: Dict) -> Dict[str, Any]:
        """Playwright 추출 테스트"""
        try:
            import sys
            from pathlib import Path
            
            # 부모 디렉토리를 sys.path에 추가
            parent_dir = Path(__file__).parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            from modules.playwright_dynamic_tester import PlaywrightDynamicTester
            from modules.ai_research_engine import CollectionStrategy, ConfidenceLevel
            
            # 전략 객체 재구성 (간단한 버전)
            strategy = type('Strategy', (), {
                'strategy_id': strategy_data['strategy_id'],
                'site_url': site_config['url'],
                'selectors': strategy_data['selectors'],
                'confidence': type('Confidence', (), {'value': strategy_data['confidence']})()
            })()
            
            # Playwright 테스터 실행
            tester = PlaywrightDynamicTester()
            await tester.initialize()
            
            try:
                result = await tester.test_collection_strategy(strategy, pages_to_test=1)
                
                return {
                    "success": result.overall_result.value in ["success", "partial_success"],
                    "items_found": result.metrics.total_items_found,
                    "valid_items": result.metrics.valid_items_extracted,
                    "success_rate": result.metrics.selector_success_rate
                }
                
            finally:
                await tester.close()
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "items_found": 0
            }
    
    async def _save_test_results(self, results: Dict[str, Any]):
        """테스트 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"real_world_test_results_{timestamp}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 테스트 결과 저장: {filepath}")
    
    def _print_comprehensive_summary(self, results: Dict[str, Any]):
        """종합 결과 요약 출력"""
        print("\n" + "="*80)
        print("🧪 실제 정부 포털 AI 크롤링 통합 테스트 결과")
        print("="*80)
        
        # API 키 상태
        api_status = results["api_key_status"]
        print(f"🔑 API 키 상태:")
        print(f"   Gemini Flash 2.0: {'✅ 설정됨' if api_status.get('gemini_available') else '❌ 미설정'}")
        print(f"   Claude API: {'✅ 설정됨' if api_status.get('claude_available') else '❌ 미설정'}")
        print(f"   실행 모드: {'🚀 AI 모드' if api_status.get('any_api_available') else '🔄 로컬 패턴 모드'}")
        
        # 전체 결과
        print(f"\n📊 전체 결과:")
        print(f"   성공률: {results['success_rate']:.1%}")
        print(f"   성공: {results['successful_sites']}개")
        print(f"   실패: {results['failed_sites']}개")
        
        # 개별 사이트 결과
        print(f"\n🌐 개별 사이트 결과:")
        for site_result in results["detailed_results"]:
            status = "✅" if site_result["overall_success"] else "❌"
            steps = len(site_result["steps_completed"])
            print(f"   {status} {site_result['site_name']}: {steps}/3 단계 완료")
            
            if site_result["errors"]:
                for error in site_result["errors"][:2]:  # 최대 2개 오류만 표시
                    print(f"      ⚠️ {error}")
        
        # 결론
        if results["success_rate"] >= 0.5:
            print(f"\n🎉 테스트 성공! AI 크롤링 시스템이 정상 작동합니다.")
        else:
            print(f"\n⚠️ 시스템 개선 필요. API 키 설정을 확인하세요.")
        
        print("="*80)


async def main():
    """메인 테스트 실행"""
    tester = RealWorldTester()
    results = await tester.run_comprehensive_test()
    return results


if __name__ == "__main__":
    asyncio.run(main())