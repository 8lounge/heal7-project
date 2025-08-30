#!/usr/bin/env python3
"""
🧪 AI Research Engine 실제 통합 테스트 및 검증
실제 API 호출과 Playwright 연동 테스트

Author: HEAL7 Development Team  
Version: 1.0.0
Date: 2025-08-29
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from ai_research_engine import AIResearchEngine, create_ai_research_engine, analyze_site_and_generate_strategy
from playwright_dynamic_tester import PlaywrightDynamicTester, test_strategy_with_playwright


logger = logging.getLogger(__name__)


class RealWorldIntegrationTester:
    """🔬 실제 환경 통합 테스터"""
    
    def __init__(self, gemini_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        # 테스트 대상 사이트들 (실제 정부 포털)
        self.test_sites = [
            {
                "name": "기업마당 지원사업",
                "url": "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/list.do",
                "expected_fields": ["title", "agency", "category"]
            },
            {
                "name": "K-Startup 사업공고",
                "url": "https://www.k-startup.go.kr/web/contents/bizListPage.do",
                "expected_fields": ["title", "agency", "date"]
            }
        ]
        
        # 테스트 결과 저장
        self.test_results = []
    
    async def run_full_integration_test(self) -> Dict[str, Any]:
        """🚀 전체 통합 테스트 실행"""
        logger.info("🚀 실제 AI-Playwright 통합 테스트 시작")
        
        overall_results = {
            "test_started": datetime.now().isoformat(),
            "sites_tested": [],
            "total_success": 0,
            "total_failures": 0,
            "detailed_results": []
        }
        
        for site_config in self.test_sites:
            logger.info(f"🔍 테스트 사이트: {site_config['name']}")
            
            try:
                # Step 1: AI 분석 실행
                site_result = await self._test_single_site(site_config)
                overall_results["detailed_results"].append(site_result)
                
                if site_result["overall_success"]:
                    overall_results["total_success"] += 1
                else:
                    overall_results["total_failures"] += 1
                
                overall_results["sites_tested"].append(site_config["name"])
                
            except Exception as e:
                logger.error(f"❌ {site_config['name']} 테스트 실패: {str(e)}")
                
                error_result = {
                    "site_name": site_config["name"],
                    "site_url": site_config["url"],
                    "overall_success": False,
                    "error": str(e),
                    "ai_analysis_success": False,
                    "playwright_test_success": False
                }
                
                overall_results["detailed_results"].append(error_result)
                overall_results["total_failures"] += 1
        
        overall_results["test_completed"] = datetime.now().isoformat()
        overall_results["success_rate"] = overall_results["total_success"] / len(self.test_sites) if self.test_sites else 0
        
        # 결과 요약 출력
        self._print_test_summary(overall_results)
        
        return overall_results
    
    async def _test_single_site(self, site_config: Dict) -> Dict[str, Any]:
        """개별 사이트 통합 테스트"""
        site_result = {
            "site_name": site_config["name"],
            "site_url": site_config["url"],
            "expected_fields": site_config["expected_fields"],
            "overall_success": False,
            "ai_analysis_success": False,
            "playwright_test_success": False,
            "ai_analysis_result": None,
            "strategy_generated": None,
            "playwright_result": None,
            "extracted_sample_data": []
        }
        
        try:
            # Step 1: AI 분석 실행
            logger.info(f"  🤖 AI 분석 시작: {site_config['url']}")
            
            ai_engine = create_ai_research_engine(self.gemini_api_key)
            await ai_engine.initialize()
            
            try:
                # 실제 AI 분석 실행
                analysis_result = await ai_engine.analyze_website_structure(site_config["url"])
                strategy = await ai_engine.generate_collection_strategy(
                    analysis_result, site_config["expected_fields"]
                )
                
                site_result["ai_analysis_success"] = True
                site_result["ai_analysis_result"] = {
                    "site_type": analysis_result.site_type,
                    "confidence_score": analysis_result.confidence_score,
                    "recommended_selectors": analysis_result.recommended_selectors,
                    "strategy_confidence": strategy.confidence.value
                }
                site_result["strategy_generated"] = {
                    "strategy_id": strategy.strategy_id,
                    "selectors": strategy.selectors,
                    "pagination_enabled": strategy.pagination.get("enabled", False)
                }
                
                logger.info(f"  ✅ AI 분석 완료 - 신뢰도: {analysis_result.confidence_score:.1%}")
                
            finally:
                await ai_engine.close()
            
            # Step 2: Playwright 테스트 실행
            if site_result["ai_analysis_success"] and strategy:
                logger.info(f"  🎭 Playwright 테스트 시작")
                
                # 실제 Playwright 테스트 실행
                playwright_result = await test_strategy_with_playwright(
                    strategy=strategy,
                    headless=True,
                    pages_to_test=2
                )
                
                site_result["playwright_test_success"] = playwright_result.overall_result.value in ["success", "partial_success"]
                site_result["playwright_result"] = {
                    "overall_result": playwright_result.overall_result.value,
                    "total_items_found": playwright_result.metrics.total_items_found,
                    "valid_items_extracted": playwright_result.metrics.valid_items_extracted,
                    "selector_success_rate": playwright_result.metrics.selector_success_rate,
                    "data_quality_score": playwright_result.metrics.data_quality_score,
                    "test_duration": playwright_result.test_duration
                }
                site_result["extracted_sample_data"] = playwright_result.sample_data[:3]  # 샘플 3개
                
                logger.info(f"  ✅ Playwright 테스트 완료 - 결과: {playwright_result.overall_result.value}")
                logger.info(f"     추출된 아이템: {playwright_result.metrics.total_items_found}개")
                logger.info(f"     유효 아이템: {playwright_result.metrics.valid_items_extracted}개")
            
            # 전체 성공 여부 결정
            site_result["overall_success"] = (
                site_result["ai_analysis_success"] and 
                site_result["playwright_test_success"] and
                len(site_result["extracted_sample_data"]) > 0
            )
            
            return site_result
            
        except Exception as e:
            logger.error(f"  ❌ {site_config['name']} 테스트 중 오류: {str(e)}")
            site_result["error"] = str(e)
            return site_result
    
    def _print_test_summary(self, results: Dict[str, Any]):
        """테스트 결과 요약 출력"""
        print("\n" + "="*80)
        print("🧪 AI-Playwright 통합 테스트 결과 요약")
        print("="*80)
        
        print(f"📊 전체 성공률: {results['success_rate']:.1%}")
        print(f"✅ 성공: {results['total_success']}개")
        print(f"❌ 실패: {results['total_failures']}개")
        print(f"⏱️  테스트 시간: {results['test_started']} ~ {results['test_completed']}")
        
        print(f"\n📋 사이트별 상세 결과:")
        for result in results["detailed_results"]:
            print(f"\n🌐 {result['site_name']}")
            print(f"   URL: {result['site_url']}")
            print(f"   전체 성공: {'✅' if result['overall_success'] else '❌'}")
            print(f"   AI 분석: {'✅' if result['ai_analysis_success'] else '❌'}")
            print(f"   Playwright 테스트: {'✅' if result['playwright_test_success'] else '❌'}")
            
            if result.get("ai_analysis_result"):
                ai_result = result["ai_analysis_result"]
                print(f"   - 사이트 타입: {ai_result.get('site_type', 'unknown')}")
                print(f"   - AI 신뢰도: {ai_result.get('confidence_score', 0):.1%}")
                print(f"   - 전략 신뢰도: {ai_result.get('strategy_confidence', 'unknown')}")
            
            if result.get("playwright_result"):
                pw_result = result["playwright_result"]
                print(f"   - 추출 아이템: {pw_result.get('total_items_found', 0)}개")
                print(f"   - 유효 아이템: {pw_result.get('valid_items_extracted', 0)}개")
                print(f"   - 선택자 성공률: {pw_result.get('selector_success_rate', 0):.1%}")
                print(f"   - 데이터 품질: {pw_result.get('data_quality_score', 0):.1%}")
            
            if result.get("extracted_sample_data"):
                print(f"   - 샘플 데이터: {len(result['extracted_sample_data'])}개")
                for i, sample in enumerate(result["extracted_sample_data"][:2]):  # 최대 2개만
                    print(f"     [{i+1}] {sample.get('title', 'No Title')[:50]}")
            
            if result.get("error"):
                print(f"   ❌ 오류: {result['error']}")
        
        print("\n" + "="*80)
    
    async def test_ai_api_connectivity(self) -> Dict[str, Any]:
        """AI API 연결 테스트"""
        logger.info("🔌 AI API 연결성 테스트")
        
        connectivity_result = {
            "gemini_api_available": False,
            "claude_api_available": False,
            "local_pattern_available": True,  # 항상 사용 가능
            "test_timestamp": datetime.now().isoformat()
        }
        
        # Gemini API 테스트
        try:
            if self.gemini_api_key and self.gemini_api_key != "your-gemini-api-key":
                ai_engine = AIResearchEngine(gemini_api_key=self.gemini_api_key)
                await ai_engine.initialize()
                
                # 간단한 테스트 프롬프트
                test_prompt = "안녕하세요. 이것은 API 연결 테스트입니다."
                
                try:
                    response = await ai_engine._call_ai_model(test_prompt, "primary")
                    if response and len(response.strip()) > 0:
                        connectivity_result["gemini_api_available"] = True
                        logger.info("✅ Gemini API 연결 성공")
                    else:
                        logger.warning("⚠️ Gemini API 응답 없음")
                except Exception as e:
                    logger.warning(f"⚠️ Gemini API 연결 실패: {str(e)}")
                
                await ai_engine.close()
            else:
                logger.warning("⚠️ Gemini API 키가 설정되지 않음")
                
        except Exception as e:
            logger.error(f"❌ Gemini API 테스트 중 오류: {str(e)}")
        
        # Claude API 테스트 (선택사항)
        # 현재는 생략 (API 키 없음)
        
        print(f"\n🔌 API 연결성 테스트 결과:")
        print(f"   Gemini Flash 2.0: {'✅' if connectivity_result['gemini_api_available'] else '❌'}")
        print(f"   Claude API: {'✅' if connectivity_result['claude_api_available'] else '❌'}")
        print(f"   로컬 패턴: {'✅' if connectivity_result['local_pattern_available'] else '❌'}")
        
        return connectivity_result


# 실제 테스트 실행 함수들

async def run_quick_integration_test():
    """빠른 통합 테스트 (1개 사이트)"""
    logger.info("⚡ 빠른 통합 테스트 시작")
    
    tester = RealWorldIntegrationTester()
    
    # API 연결성 먼저 테스트
    connectivity = await tester.test_ai_api_connectivity()
    
    if not any([connectivity["gemini_api_available"], connectivity["local_pattern_available"]]):
        logger.error("❌ 사용 가능한 AI 모델이 없습니다")
        return
    
    # 1개 사이트만 테스트
    tester.test_sites = tester.test_sites[:1]  # 첫 번째 사이트만
    
    results = await tester.run_full_integration_test()
    
    # 성공 여부에 따른 결과
    if results["success_rate"] > 0:
        print(f"\n🎉 통합 테스트 성공! 성공률: {results['success_rate']:.1%}")
        return True
    else:
        print(f"\n❌ 통합 테스트 실패. 성공률: {results['success_rate']:.1%}")
        return False


async def run_comprehensive_integration_test():
    """전체 통합 테스트 (모든 사이트)"""
    logger.info("🔬 전체 통합 테스트 시작")
    
    tester = RealWorldIntegrationTester()
    
    # API 연결성 테스트
    await tester.test_ai_api_connectivity()
    
    # 전체 사이트 테스트
    results = await tester.run_full_integration_test()
    
    # 결과를 파일로 저장
    results_file = f"/home/ubuntu/logs/integration_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 테스트 결과 저장됨: {results_file}")
    except Exception as e:
        logger.error(f"❌ 결과 저장 실패: {str(e)}")
    
    return results


async def validate_current_implementation():
    """현재 구현의 유효성 검증"""
    print("🔍 현재 구현 유효성 검증")
    
    validation_results = {
        "ai_research_engine": False,
        "playwright_tester": False,
        "integration": False,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # 1. AI Research Engine 검증
        logger.info("1️⃣ AI Research Engine 검증")
        ai_engine = create_ai_research_engine()
        await ai_engine.initialize()
        await ai_engine.close()
        validation_results["ai_research_engine"] = True
        logger.info("✅ AI Research Engine 유효")
        
        # 2. Playwright Tester 검증
        logger.info("2️⃣ Playwright Tester 검증")
        tester = PlaywrightDynamicTester(headless=True)
        await tester.initialize()
        await tester.close()
        validation_results["playwright_tester"] = True
        logger.info("✅ Playwright Tester 유효")
        
        # 3. 통합 검증
        logger.info("3️⃣ 통합 시스템 검증")
        integration_success = await run_quick_integration_test()
        validation_results["integration"] = integration_success
        
        if integration_success:
            logger.info("✅ 통합 시스템 유효")
        else:
            logger.warning("⚠️ 통합 시스템 부분적 이슈")
        
    except Exception as e:
        logger.error(f"❌ 검증 중 오류: {str(e)}")
    
    # 검증 결과 출력
    print(f"\n🔍 구현 유효성 검증 결과:")
    print(f"   AI Research Engine: {'✅' if validation_results['ai_research_engine'] else '❌'}")
    print(f"   Playwright Tester: {'✅' if validation_results['playwright_tester'] else '❌'}")
    print(f"   통합 시스템: {'✅' if validation_results['integration'] else '❌'}")
    
    overall_valid = all(validation_results[k] for k in validation_results if k != "timestamp")
    print(f"   전체 평가: {'✅ 유효' if overall_valid else '❌ 이슈 있음'}")
    
    return validation_results


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def main():
        print("🚀 AI 기반 동적 크롤링 시스템 - 실제 통합 테스트")
        print("="*80)
        
        # 환경 변수 확인
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            print(f"🔑 Gemini API 키 발견: {gemini_key[:10]}...")
        else:
            print("⚠️ Gemini API 키가 설정되지 않았습니다. 로컬 패턴 모드로 실행됩니다.")
        
        print()
        
        # 구현 검증 실행
        await validate_current_implementation()
        
        print(f"\n{'='*80}")
        print("테스트 완료!")
    
    # 메인 테스트 실행
    asyncio.run(main())