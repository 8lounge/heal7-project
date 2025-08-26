#!/usr/bin/env python3
"""
사주 시스템 종합 검증 실행기 v1.0
AI 교차검증 + 핵심 원리 검증 통합 실행

특징:
- AI 모델들과 함께 교차검증
- 핵심 원리별 심층 검증
- 통합 리포트 자동 생성
- 하드코딩 완전 제거된 동적 검증
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

# 검증 엔진들
from .ai_cross_validation_engine import AICrossValidationEngine
from .saju_core_principle_validator import SajuCorePrincipleValidator

logger = logging.getLogger(__name__)

class ComprehensiveValidationRunner:
    """종합 검증 실행기"""
    
    def __init__(self):
        self.ai_engine = AICrossValidationEngine()
        self.principle_validator = SajuCorePrincipleValidator()
        
    async def run_full_validation(self):
        """전체 검증 실행"""
        
        print("🚀 사주 시스템 종합 검증 시작")
        print("=" * 100)
        print("AI 교차검증 + 핵심 원리 검증 + 통합 분석")
        print("=" * 100)
        
        validation_start = datetime.now()
        
        # 1단계: AI 교차검증
        print("\n🤖 1단계: AI 교차검증 실행")
        print("-" * 50)
        
        try:
            ai_report = await self.ai_engine.run_cross_validation()
            ai_success = True
            print("✅ AI 교차검증 완료")
        except Exception as e:
            logger.error(f"AI 교차검증 실패: {e}")
            ai_report = None
            ai_success = False
            print("❌ AI 교차검증 실패")
        
        # 2단계: 원리 검증
        print("\n🎯 2단계: 핵심 원리 검증 실행")
        print("-" * 50)
        
        try:
            principle_report = await self.principle_validator.run_comprehensive_validation()
            principle_success = True
            print("✅ 핵심 원리 검증 완료")
        except Exception as e:
            logger.error(f"원리 검증 실패: {e}")
            principle_report = None
            principle_success = False
            print("❌ 핵심 원리 검증 실패")
        
        # 3단계: 통합 분석
        print("\n📊 3단계: 통합 분석 및 최종 리포트")
        print("-" * 50)
        
        integrated_report = await self._generate_integrated_report(
            ai_report, principle_report, validation_start
        )
        
        # 4단계: 최종 출력
        await self._output_final_integrated_report(integrated_report)
        
        total_time = (datetime.now() - validation_start).total_seconds()
        print(f"\n⏱️ 총 검증 시간: {total_time:.1f}초")
        print("🎉 종합 검증 완료!")
        
        return integrated_report
    
    async def _generate_integrated_report(self, ai_report: Dict[str, Any], 
                                        principle_report: Dict[str, Any], 
                                        validation_start: datetime) -> Dict[str, Any]:
        """통합 리포트 생성"""
        
        total_time = (datetime.now() - validation_start).total_seconds()
        
        # AI 검증 결과 요약
        ai_summary = {
            "available": ai_report is not None,
            "total_cases": ai_report.get("total_cases", 0) if ai_report else 0,
            "reliability_score": ai_report.get("overall_reliability_score", 0) if ai_report else 0,
            "consensus_rate": ai_report.get("consensus_analysis", {}).get("overall_consensus_rate", 0) if ai_report else 0,
            "models_used": ai_report.get("ai_models_used", []) if ai_report else []
        }
        
        # 원리 검증 결과 요약
        principle_summary = {
            "available": principle_report is not None,
            "total_principles": principle_report.get("total_principles", 0) if principle_report else 0,
            "total_cases": principle_report.get("total_cases", 0) if principle_report else 0,
            "overall_accuracy": principle_report.get("overall_accuracy", 0) if principle_report else 0,
            "grade": principle_report.get("grade", "N/A") if principle_report else "N/A",
            "excellent_principles": principle_report.get("excellent_principles", []) if principle_report else [],
            "problem_principles": principle_report.get("problem_principles", []) if principle_report else []
        }
        
        # 통합 신뢰성 점수 계산
        reliability_components = []
        
        if ai_summary["available"]:
            reliability_components.append(ai_summary["reliability_score"])
        
        if principle_summary["available"]:
            reliability_components.append(principle_summary["overall_accuracy"])
        
        integrated_reliability = sum(reliability_components) / len(reliability_components) if reliability_components else 0
        
        # 통합 등급 산정
        if integrated_reliability >= 95:
            integrated_grade = "S+ (완벽한 시스템)"
        elif integrated_reliability >= 90:
            integrated_grade = "S (매우 우수)"
        elif integrated_reliability >= 85:
            integrated_grade = "A (우수)"
        elif integrated_reliability >= 80:
            integrated_grade = "B+ (양호)"
        elif integrated_reliability >= 75:
            integrated_grade = "B (보통)"
        elif integrated_reliability >= 70:
            integrated_grade = "C (개선 필요)"
        else:
            integrated_grade = "D (전면 개선 필요)"
        
        # 주요 발견사항
        key_findings = []
        
        if principle_summary["excellent_principles"]:
            key_findings.append(f"✅ 우수 원리: {len(principle_summary['excellent_principles'])}개")
        
        if principle_summary["problem_principles"]:
            key_findings.append(f"⚠️ 개선 필요: {len(principle_summary['problem_principles'])}개")
        
        if ai_summary["available"] and ai_summary["consensus_rate"] >= 90:
            key_findings.append(f"🤝 AI 높은 합의율: {ai_summary['consensus_rate']:.1f}%")
        
        if ai_summary["available"] and ai_summary["models_used"]:
            key_findings.append(f"🤖 AI 모델 활용: {len(ai_summary['models_used'])}개")
        
        # 권장사항 생성
        recommendations = []
        
        if integrated_reliability >= 90:
            recommendations.append("🎉 시스템이 매우 안정적입니다. 현재 품질을 유지하세요.")
        elif integrated_reliability >= 80:
            recommendations.append("✅ 시스템이 전반적으로 양호합니다. 일부 영역의 미세 조정을 권장합니다.")
        else:
            recommendations.append("🔧 시스템에 중요한 개선이 필요합니다.")
        
        if principle_summary["problem_principles"]:
            recommendations.append(f"📌 우선 개선 영역: {', '.join(principle_summary['problem_principles'][:3])}")
        
        if not ai_summary["available"]:
            recommendations.append("🤖 AI 교차검증 시스템 설정을 권장합니다.")
        
        # 비교 분석
        comparison_analysis = {}
        
        if ai_summary["available"] and principle_summary["available"]:
            accuracy_diff = abs(ai_summary["reliability_score"] - principle_summary["overall_accuracy"])
            
            if accuracy_diff <= 5:
                comparison_analysis["consistency"] = "높음 - AI와 원리 검증 결과가 일치"
            elif accuracy_diff <= 15:
                comparison_analysis["consistency"] = "보통 - 일부 차이 존재"
            else:
                comparison_analysis["consistency"] = "낮음 - 상당한 차이 존재, 추가 분석 필요"
            
            comparison_analysis["ai_vs_principle"] = {
                "ai_score": ai_summary["reliability_score"],
                "principle_score": principle_summary["overall_accuracy"],
                "difference": accuracy_diff
            }
        
        return {
            "report_id": f"integrated_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "validation_duration": total_time,
            "ai_validation": ai_summary,
            "principle_validation": principle_summary,
            "integrated_analysis": {
                "overall_reliability": integrated_reliability,
                "integrated_grade": integrated_grade,
                "key_findings": key_findings,
                "recommendations": recommendations,
                "comparison_analysis": comparison_analysis
            },
            "detailed_reports": {
                "ai_report": ai_report,
                "principle_report": principle_report
            }
        }
    
    async def _output_final_integrated_report(self, report: Dict[str, Any]):
        """최종 통합 리포트 출력"""
        
        print("\n" + "=" * 100)
        print("🎯 사주 시스템 종합 검증 통합 리포트")
        print("=" * 100)
        
        print(f"\n📊 검증 개요:")
        print(f"   - 리포트 ID: {report['report_id']}")
        print(f"   - 검증 완료: {report['timestamp']}")
        print(f"   - 총 소요 시간: {report['validation_duration']:.1f}초")
        
        print(f"\n🏆 통합 성과:")
        print(f"   - 통합 신뢰성: {report['integrated_analysis']['overall_reliability']:.1f}%")
        print(f"   - 시스템 등급: {report['integrated_analysis']['integrated_grade']}")
        
        print(f"\n🤖 AI 교차검증 결과:")
        ai_val = report['ai_validation']
        if ai_val['available']:
            print(f"   ✅ 실행 성공")
            print(f"   - 검증 케이스: {ai_val['total_cases']}개")
            print(f"   - 신뢰성 점수: {ai_val['reliability_score']:.1f}%")
            print(f"   - AI 합의율: {ai_val['consensus_rate']:.1f}%")
            print(f"   - 활용 모델: {', '.join(ai_val['models_used'])}")
        else:
            print(f"   ❌ 실행 실패 또는 미사용")
        
        print(f"\n🎯 핵심 원리 검증 결과:")
        prin_val = report['principle_validation']
        if prin_val['available']:
            print(f"   ✅ 실행 성공")
            print(f"   - 검증 원리: {prin_val['total_principles']}개")
            print(f"   - 검증 케이스: {prin_val['total_cases']}개")
            print(f"   - 전체 정확도: {prin_val['overall_accuracy']:.1f}%")
            print(f"   - 등급: {prin_val['grade']}")
            
            if prin_val['excellent_principles']:
                print(f"   - 우수 원리: {', '.join(prin_val['excellent_principles'][:3])}{'...' if len(prin_val['excellent_principles']) > 3 else ''}")
            
            if prin_val['problem_principles']:
                print(f"   - 문제 원리: {', '.join(prin_val['problem_principles'])}")
        else:
            print(f"   ❌ 실행 실패")
        
        print(f"\n🔍 주요 발견사항:")
        for finding in report['integrated_analysis']['key_findings']:
            print(f"   {finding}")
        
        print(f"\n💡 통합 권장사항:")
        for i, recommendation in enumerate(report['integrated_analysis']['recommendations'], 1):
            print(f"   {i}. {recommendation}")
        
        # 비교 분석
        comparison = report['integrated_analysis']['comparison_analysis']
        if comparison:
            print(f"\n📈 AI vs 원리검증 비교:")
            print(f"   - 일관성: {comparison.get('consistency', 'N/A')}")
            
            if 'ai_vs_principle' in comparison:
                comp_data = comparison['ai_vs_principle']
                print(f"   - AI 점수: {comp_data['ai_score']:.1f}%")
                print(f"   - 원리 점수: {comp_data['principle_score']:.1f}%")
                print(f"   - 차이: {comp_data['difference']:.1f}%p")
        
        print(f"\n📋 최종 결론:")
        reliability = report['integrated_analysis']['overall_reliability']
        
        if reliability >= 95:
            print("   🎉 사주 시스템이 AI와 원리 검증을 통해 최고 수준의 신뢰성을 확인했습니다!")
            print("   🌟 현재 시스템을 프로덕션 환경에서 안심하고 사용할 수 있습니다.")
        elif reliability >= 85:
            print("   ✅ 사주 시스템이 높은 신뢰성을 보이며 안정적으로 작동합니다.")
            print("   🔧 일부 영역의 미세 조정으로 완벽한 시스템이 될 수 있습니다.")
        elif reliability >= 75:
            print("   ⚠️ 사주 시스템이 기본적으로 작동하나 중요한 개선이 필요합니다.")
            print("   🛠️ 문제 영역을 우선적으로 개선하여 신뢰성을 높이세요.")
        else:
            print("   🚨 사주 시스템에 중대한 문제가 발견되었습니다.")
            print("   🔧 전면적인 시스템 점검과 개선이 필요합니다.")
        
        # 리포트 저장
        import json
        report_filename = f"/tmp/{report['report_id']}.json"
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 상세 통합 리포트 저장: {report_filename}")
        print("=" * 100)
        
        return report


# 메인 실행 함수
async def run_comprehensive_validation():
    """종합 검증 실행 메인 함수"""
    
    runner = ComprehensiveValidationRunner()
    return await runner.run_full_validation()


if __name__ == "__main__":
    asyncio.run(run_comprehensive_validation())