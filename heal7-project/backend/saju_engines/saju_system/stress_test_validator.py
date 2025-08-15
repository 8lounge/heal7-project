#!/usr/bin/env python3
"""
사주 계산 시스템 스트레스 테스트 및 비교 검증
HEAL7 과학적 명리학 기준 검증 시스템

검증 기준:
1. KASI API - 천문학적 정밀 기준 (기준점)
2. v5.0 통합 시스템 - KASI 기반 튜닝 로직
3. 폴백 로직 - 수학적 갑자 순환
4. 74000 만세력 DB - 정통 만세력 참조

HEAL7 기준:
- 그레고리력 기반
- 24절기 기준 월주 계산
- 진태양시 127도 (한국 경도)
- 천문대 API가 최종 기준
"""

import asyncio
import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
import sqlite3
from pathlib import Path

# 시스템 모듈 import
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .comprehensive_myeongrihak_analyzer import ComprehensiveMyeongRiHakAnalyzer
from .hybrid_saju_engine import HybridSajuEngine

logger = logging.getLogger(__name__)

class StressTestValidator:
    """사주 계산 시스템 스트레스 테스트 및 검증"""
    
    def __init__(self):
        # 각 시스템 초기화
        self.kasi_calculator = KasiPrecisionSajuCalculator()
        self.v5_analyzer = ComprehensiveMyeongRiHakAnalyzer()
        self.hybrid_engine = HybridSajuEngine()
        
        # 74000 만세력 DB 경로 (실제 경로로 수정 필요)
        self.manseryeok_db_path = "/home/ubuntu/archive/manseryeok_74000.db"
        
        # 테스트 결과 저장
        self.test_results = []
        
    def generate_random_test_cases(self, count: int = 30) -> List[Dict]:
        """랜덤 테스트 케이스 생성"""
        
        test_cases = []
        
        # 시대별 분포
        era_ranges = [
            (1950, 1969, 6),  # 50-60년대 (6명)
            (1970, 1989, 8),  # 70-80년대 (8명)
            (1990, 2009, 10), # 90-00년대 (10명)
            (2010, 2024, 6),  # 10-20년대 (6명)
        ]
        
        for start_year, end_year, num_cases in era_ranges:
            for _ in range(num_cases):
                year = random.randint(start_year, end_year)
                month = random.randint(1, 12)
                
                # 월별 일수 고려
                if month in [1, 3, 5, 7, 8, 10, 12]:
                    day = random.randint(1, 31)
                elif month in [4, 6, 9, 11]:
                    day = random.randint(1, 30)
                else:  # 2월
                    day = random.randint(1, 28)
                
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                
                # 10% 확률로 음력
                is_lunar = random.random() < 0.1
                
                test_cases.append({
                    "id": f"TEST_{len(test_cases)+1:03d}",
                    "year": year,
                    "month": month,
                    "day": day,
                    "hour": hour,
                    "minute": minute,
                    "is_lunar": is_lunar,
                    "description": f"{year}년 {'음력' if is_lunar else '양력'} {month}월 {day}일 {hour:02d}:{minute:02d}"
                })
        
        return test_cases
    
    async def test_kasi_api(self, test_case: Dict) -> Dict:
        """KASI API 직접 테스트 (기준점)"""
        
        start_time = time.time()
        
        try:
            result = self.kasi_calculator.calculate_saju(
                test_case["year"], test_case["month"], test_case["day"],
                test_case["hour"], test_case["minute"], test_case["is_lunar"]
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if result:
                return {
                    "status": "success",
                    "pillars": result.get("pillars"),
                    "ilgan": result.get("ilgan"),
                    "processing_time_ms": processing_time,
                    "method": "KASI_DIRECT",
                    "accuracy": "100%_reference"
                }
            else:
                return {
                    "status": "failed",
                    "error": "KASI API 응답 없음",
                    "processing_time_ms": processing_time
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "processing_time_ms": (time.time() - start_time) * 1000
            }
    
    async def test_v5_integrated(self, test_case: Dict) -> Dict:
        """v5.0 통합 시스템 테스트"""
        
        start_time = time.time()
        
        try:
            result = self.v5_analyzer.analyze_complete_myeongrihak(
                test_case["year"], test_case["month"], test_case["day"],
                test_case["hour"], test_case["minute"], test_case["is_lunar"]
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if result:
                return {
                    "status": "success",
                    "pillars": result.get("pillars"),
                    "ilgan": result.get("ilgan"),
                    "gyeokguk": result.get("gyeokguk"),
                    "processing_time_ms": processing_time,
                    "method": "V5_INTEGRATED",
                    "calculation_method": result.get("_calculation_method", "unknown")
                }
            else:
                return {
                    "status": "failed",
                    "error": "v5.0 계산 실패",
                    "processing_time_ms": processing_time
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "processing_time_ms": (time.time() - start_time) * 1000
            }
    
    async def test_fallback_logic(self, test_case: Dict) -> Dict:
        """폴백 로직 테스트 (수학적 계산)"""
        
        start_time = time.time()
        
        try:
            # 강제로 폴백 모드 실행
            result = self.kasi_calculator._fallback_calculation(
                test_case["year"], test_case["month"], test_case["day"],
                test_case["hour"], test_case["minute"], test_case["is_lunar"]
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if result:
                return {
                    "status": "success",
                    "pillars": result.get("pillars"),
                    "ilgan": result.get("ilgan"),
                    "processing_time_ms": processing_time,
                    "method": "FALLBACK_MATH",
                    "accuracy_warning": result.get("_accuracy_warning")
                }
            else:
                return {
                    "status": "failed",
                    "error": "폴백 계산 실패",
                    "processing_time_ms": processing_time
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "processing_time_ms": (time.time() - start_time) * 1000
            }
    
    def test_74000_manseryeok(self, test_case: Dict) -> Dict:
        """74000 만세력 DB 조회"""
        
        start_time = time.time()
        
        try:
            # DB 존재 여부 확인
            if not Path(self.manseryeok_db_path).exists():
                # 시뮬레이션 데이터 반환
                return {
                    "status": "simulated",
                    "pillars": {
                        "year": {"gapja": "甲子"},
                        "month": {"gapja": "乙丑"},
                        "day": {"gapja": "丙寅"},
                        "hour": {"gapja": "丁卯"}
                    },
                    "ilgan": "丙",
                    "processing_time_ms": 5.0,
                    "method": "74000_DB_SIMULATED",
                    "note": "실제 DB 없음 - 시뮬레이션"
                }
            
            # 실제 DB 조회 (구현 필요)
            with sqlite3.connect(self.manseryeok_db_path) as conn:
                # 쿼리 로직 구현
                pass
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "processing_time_ms": (time.time() - start_time) * 1000
            }
    
    def compare_results(self, kasi: Dict, v5: Dict, fallback: Dict, manseryeok: Dict) -> Dict:
        """결과 비교 분석"""
        
        comparison = {
            "일간_일치": {
                "kasi_v5": False,
                "kasi_fallback": False,
                "kasi_manseryeok": False,
                "v5_fallback": False,
                "v5_manseryeok": False,
                "fallback_manseryeok": False
            },
            "일주_일치": {
                "kasi_v5": False,
                "kasi_fallback": False,
                "kasi_manseryeok": False
            },
            "처리시간": {
                "kasi": kasi.get("processing_time_ms", 0),
                "v5": v5.get("processing_time_ms", 0),
                "fallback": fallback.get("processing_time_ms", 0),
                "manseryeok": manseryeok.get("processing_time_ms", 0)
            },
            "정확도_평가": {}
        }
        
        # KASI를 기준으로 비교
        if kasi.get("status") == "success":
            kasi_ilgan = kasi.get("ilgan")
            kasi_day_gapja = kasi.get("pillars", {}).get("day", {}).get("gapja")
            
            # v5와 비교
            if v5.get("status") == "success":
                comparison["일간_일치"]["kasi_v5"] = kasi_ilgan == v5.get("ilgan")
                v5_day_gapja = v5.get("pillars", {}).get("day", {}).get("gapja")
                comparison["일주_일치"]["kasi_v5"] = kasi_day_gapja == v5_day_gapja
            
            # 폴백과 비교
            if fallback.get("status") == "success":
                comparison["일간_일치"]["kasi_fallback"] = kasi_ilgan == fallback.get("ilgan")
                fb_day_gapja = fallback.get("pillars", {}).get("day", {}).get("gapja")
                comparison["일주_일치"]["kasi_fallback"] = kasi_day_gapja == fb_day_gapja
            
            # 만세력과 비교
            if manseryeok.get("status") in ["success", "simulated"]:
                comparison["일간_일치"]["kasi_manseryeok"] = kasi_ilgan == manseryeok.get("ilgan")
                ms_day_gapja = manseryeok.get("pillars", {}).get("day", {}).get("gapja")
                comparison["일주_일치"]["kasi_manseryeok"] = kasi_day_gapja == ms_day_gapja
        
        # 정확도 평가 (KASI 기준)
        if kasi.get("status") == "success":
            # v5 정확도
            v5_matches = sum([
                comparison["일간_일치"]["kasi_v5"],
                comparison["일주_일치"]["kasi_v5"]
            ])
            comparison["정확도_평가"]["v5"] = f"{v5_matches/2*100:.1f}%"
            
            # 폴백 정확도
            fb_matches = sum([
                comparison["일간_일치"]["kasi_fallback"],
                comparison["일주_일치"]["kasi_fallback"]
            ])
            comparison["정확도_평가"]["fallback"] = f"{fb_matches/2*100:.1f}%"
            
            # 만세력 정확도
            ms_matches = sum([
                comparison["일간_일치"]["kasi_manseryeok"],
                comparison["일주_일치"]["kasi_manseryeok"]
            ])
            comparison["정확도_평가"]["manseryeok"] = f"{ms_matches/2*100:.1f}%"
        
        return comparison
    
    async def run_stress_test(self, test_count: int = 30):
        """스트레스 테스트 실행"""
        
        print("🧪 사주 계산 시스템 스트레스 테스트 시작")
        print("=" * 60)
        print(f"테스트 케이스: {test_count}개")
        print(f"비교 시스템: KASI API vs v5.0 vs 폴백 vs 74000 만세력")
        print(f"기준점: KASI API (천문학적 정밀 계산)")
        print("=" * 60)
        
        # 테스트 케이스 생성
        test_cases = self.generate_random_test_cases(test_count)
        
        # 통계 초기화
        stats = {
            "total_tests": test_count,
            "successful_tests": 0,
            "failed_tests": 0,
            "accuracy_stats": {
                "v5_vs_kasi": [],
                "fallback_vs_kasi": [],
                "manseryeok_vs_kasi": []
            },
            "performance_stats": {
                "kasi": [],
                "v5": [],
                "fallback": [],
                "manseryeok": []
            }
        }
        
        # 각 테스트 케이스 실행
        for idx, test_case in enumerate(test_cases, 1):
            print(f"\n📝 테스트 {idx}/{test_count}: {test_case['description']}")
            print("-" * 40)
            
            # 각 시스템 테스트 (병렬 실행)
            kasi_task = asyncio.create_task(self.test_kasi_api(test_case))
            v5_task = asyncio.create_task(self.test_v5_integrated(test_case))
            fallback_task = asyncio.create_task(self.test_fallback_logic(test_case))
            
            # 동기 실행 (만세력 DB)
            manseryeok_result = self.test_74000_manseryeok(test_case)
            
            # 비동기 결과 수집
            kasi_result = await kasi_task
            v5_result = await v5_task
            fallback_result = await fallback_task
            
            # 결과 비교
            comparison = self.compare_results(
                kasi_result, v5_result, fallback_result, manseryeok_result
            )
            
            # 결과 출력
            print(f"📊 KASI: {kasi_result.get('status')} ({kasi_result.get('processing_time_ms', 0):.1f}ms)")
            print(f"📊 v5.0: {v5_result.get('status')} ({v5_result.get('processing_time_ms', 0):.1f}ms)")
            print(f"📊 폴백: {fallback_result.get('status')} ({fallback_result.get('processing_time_ms', 0):.1f}ms)")
            print(f"📊 만세력: {manseryeok_result.get('status')} ({manseryeok_result.get('processing_time_ms', 0):.1f}ms)")
            
            if kasi_result.get("status") == "success":
                print(f"\n🎯 KASI 기준 일간: {kasi_result.get('ilgan')}")
                print(f"  - v5.0 일치: {comparison['일간_일치']['kasi_v5']}")
                print(f"  - 폴백 일치: {comparison['일간_일치']['kasi_fallback']}")
                print(f"  - 만세력 일치: {comparison['일간_일치']['kasi_manseryeok']}")
            
            # 통계 업데이트
            if kasi_result.get("status") == "success":
                stats["successful_tests"] += 1
                
                # 정확도 통계
                if comparison["정확도_평가"].get("v5"):
                    stats["accuracy_stats"]["v5_vs_kasi"].append(
                        float(comparison["정확도_평가"]["v5"].rstrip("%"))
                    )
                if comparison["정확도_평가"].get("fallback"):
                    stats["accuracy_stats"]["fallback_vs_kasi"].append(
                        float(comparison["정확도_평가"]["fallback"].rstrip("%"))
                    )
                if comparison["정확도_평가"].get("manseryeok"):
                    stats["accuracy_stats"]["manseryeok_vs_kasi"].append(
                        float(comparison["정확도_평가"]["manseryeok"].rstrip("%"))
                    )
            else:
                stats["failed_tests"] += 1
            
            # 성능 통계
            for system in ["kasi", "v5", "fallback", "manseryeok"]:
                time_ms = comparison["처리시간"].get(system, 0)
                if time_ms > 0:
                    stats["performance_stats"][system].append(time_ms)
            
            # 결과 저장
            self.test_results.append({
                "test_case": test_case,
                "results": {
                    "kasi": kasi_result,
                    "v5": v5_result,
                    "fallback": fallback_result,
                    "manseryeok": manseryeok_result
                },
                "comparison": comparison
            })
            
            # API 과부하 방지
            await asyncio.sleep(0.5)
        
        # 최종 통계 출력
        print("\n" + "=" * 60)
        print("📊 스트레스 테스트 최종 결과")
        print("=" * 60)
        
        # 성공률
        success_rate = (stats["successful_tests"] / stats["total_tests"]) * 100
        print(f"\n✅ 테스트 성공률: {success_rate:.1f}% ({stats['successful_tests']}/{stats['total_tests']})")
        
        # 정확도 평균
        print(f"\n🎯 KASI 기준 평균 정확도:")
        for system, accuracies in stats["accuracy_stats"].items():
            if accuracies:
                avg_accuracy = sum(accuracies) / len(accuracies)
                print(f"  - {system}: {avg_accuracy:.1f}%")
        
        # 성능 평균
        print(f"\n⚡ 평균 처리 시간:")
        for system, times in stats["performance_stats"].items():
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                print(f"  - {system}: 평균 {avg_time:.1f}ms (최소 {min_time:.1f}ms, 최대 {max_time:.1f}ms)")
        
        # 권장사항
        print(f"\n💡 권장사항:")
        
        # v5 정확도 체크
        if stats["accuracy_stats"]["v5_vs_kasi"]:
            v5_accuracy = sum(stats["accuracy_stats"]["v5_vs_kasi"]) / len(stats["accuracy_stats"]["v5_vs_kasi"])
            if v5_accuracy >= 95:
                print("  ✅ v5.0 시스템 정확도 우수 (95% 이상)")
            elif v5_accuracy >= 90:
                print("  ⚠️ v5.0 시스템 정확도 양호 (90-95%)")
            else:
                print("  ❌ v5.0 시스템 정확도 개선 필요 (90% 미만)")
        
        # 폴백 정확도 체크
        if stats["accuracy_stats"]["fallback_vs_kasi"]:
            fb_accuracy = sum(stats["accuracy_stats"]["fallback_vs_kasi"]) / len(stats["accuracy_stats"]["fallback_vs_kasi"])
            if fb_accuracy >= 80:
                print("  ✅ 폴백 로직 사용 가능 (80% 이상)")
            else:
                print("  ⚠️ 폴백 로직 개선 필요 (80% 미만)")
        
        # 성능 체크
        if stats["performance_stats"]["v5"]:
            v5_avg_time = sum(stats["performance_stats"]["v5"]) / len(stats["performance_stats"]["v5"])
            if v5_avg_time < 100:
                print("  ✅ v5.0 성능 우수 (100ms 미만)")
            elif v5_avg_time < 500:
                print("  ⚠️ v5.0 성능 양호 (100-500ms)")
            else:
                print("  ❌ v5.0 성능 최적화 필요 (500ms 초과)")
        
        return stats
    
    def save_test_results(self, filename: str = "stress_test_results.json"):
        """테스트 결과 저장"""
        
        output_path = f"/tmp/{filename}"
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 테스트 결과 저장: {output_path}")


async def main():
    """메인 테스트 실행"""
    
    validator = StressTestValidator()
    
    # 30명 스트레스 테스트
    stats = await validator.run_stress_test(30)
    
    # 결과 저장
    validator.save_test_results(f"stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    return stats


if __name__ == "__main__":
    asyncio.run(main())