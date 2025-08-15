#!/usr/bin/env python3
"""
사주 계산 시스템 시뮬레이션 비교 분석기
하드코딩 제거 및 동적 비교 검증 시스템

기능:
- 랜덤 케이스 생성 및 비교
- 다중 시스템 동시 검증
- 성능 및 정확도 분석
- 통계적 신뢰성 검증
"""

import asyncio
import random
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
import statistics
from dataclasses import dataclass

# 시스템 모듈
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .comprehensive_myeongrihak_analyzer import ComprehensiveMyeongRiHakAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """테스트 케이스 데이터 클래스"""
    id: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    is_lunar: bool
    description: str
    era: str  # 시대 구분

@dataclass
class CalculationResult:
    """계산 결과 데이터 클래스"""
    system_name: str
    status: str
    pillars: Dict[str, Any]
    ilgan: str
    processing_time_ms: float
    calculation_method: str
    accuracy_score: float = 0.0
    error_message: str = ""

class SimulationAnalyzer:
    """사주 계산 시스템 시뮬레이션 분석기"""
    
    def __init__(self):
        # 시스템 인스턴스
        self.kasi_calculator = KasiPrecisionSajuCalculator()
        self.v5_analyzer = ComprehensiveMyeongRiHakAnalyzer()
        
        # 시뮬레이션 설정
        self.systems = {
            "KASI_DIRECT": "KASI API 직접 호출",
            "V5_INTEGRATED": "v5.0 통합 시스템", 
            "FALLBACK_MATH": "수학적 폴백 로직",
            "LEGACY_SIMULATION": "74000 만세력 시뮬레이션"
        }
        
        # 결과 저장
        self.test_results = []
        self.performance_stats = {}
        self.accuracy_matrix = {}
    
    def generate_random_cases(self, count: int = 10) -> List[TestCase]:
        """랜덤 테스트 케이스 생성 (하드코딩 제거)"""
        
        cases = []
        
        # 시대별 가중치 (더 현실적인 분포)
        era_config = [
            {"name": "1950s", "range": (1950, 1959), "weight": 1},
            {"name": "1960s", "range": (1960, 1969), "weight": 1}, 
            {"name": "1970s", "range": (1970, 1979), "weight": 2},
            {"name": "1980s", "range": (1980, 1989), "weight": 3},
            {"name": "1990s", "range": (1990, 1999), "weight": 3},
            {"name": "2000s", "range": (2000, 2009), "weight": 2},
            {"name": "2010s", "range": (2010, 2019), "weight": 2},
            {"name": "2020s", "range": (2020, 2024), "weight": 1}
        ]
        
        # 가중치 기반 케이스 분배
        total_weight = sum(era["weight"] for era in era_config)
        
        for i in range(count):
            # 시대 선택 (가중치 적용)
            rand_weight = random.randint(1, total_weight)
            current_weight = 0
            selected_era = era_config[0]
            
            for era in era_config:
                current_weight += era["weight"]
                if rand_weight <= current_weight:
                    selected_era = era
                    break
            
            # 날짜 생성
            year_range = selected_era["range"]
            year = random.randint(year_range[0], year_range[1])
            month = random.randint(1, 12)
            
            # 월별 적절한 일수
            if month == 2:
                # 윤년 고려
                is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
                max_day = 29 if is_leap else 28
            elif month in [4, 6, 9, 11]:
                max_day = 30
            else:
                max_day = 31
                
            day = random.randint(1, max_day)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            
            # 음력 확률 (시대별 차등)
            lunar_prob = 0.15 if year < 1980 else 0.05
            is_lunar = random.random() < lunar_prob
            
            case = TestCase(
                id=f"SIM_{i+1:02d}",
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                is_lunar=is_lunar,
                description=f"{year}년 {'음력' if is_lunar else '양력'} {month}월 {day}일 {hour:02d}:{minute:02d}",
                era=selected_era["name"]
            )
            cases.append(case)
        
        return cases
    
    async def calculate_with_system(self, test_case: TestCase, system_name: str) -> CalculationResult:
        """특정 시스템으로 계산 실행"""
        
        start_time = time.time()
        
        try:
            if system_name == "KASI_DIRECT":
                result = self.kasi_calculator.calculate_saju(
                    test_case.year, test_case.month, test_case.day,
                    test_case.hour, test_case.minute, test_case.is_lunar
                )
                method = "KASI_API"
                
            elif system_name == "V5_INTEGRATED":
                result = self.v5_analyzer.analyze_complete_myeongrihak(
                    test_case.year, test_case.month, test_case.day,
                    test_case.hour, test_case.minute, test_case.is_lunar
                )
                method = "V5_COMPREHENSIVE"
                
            elif system_name == "FALLBACK_MATH":
                result = self.kasi_calculator._fallback_calculation(
                    test_case.year, test_case.month, test_case.day,
                    test_case.hour, test_case.minute, test_case.is_lunar
                )
                method = "MATHEMATICAL"
                
            elif system_name == "LEGACY_SIMULATION":
                result = self._simulate_legacy_calculation(test_case)
                method = "LEGACY_SIMULATION"
                
            else:
                raise ValueError(f"Unknown system: {system_name}")
            
            processing_time = (time.time() - start_time) * 1000
            
            if result and result.get("pillars") and result.get("ilgan"):
                return CalculationResult(
                    system_name=system_name,
                    status="success",
                    pillars=result.get("pillars", {}),
                    ilgan=result.get("ilgan", ""),
                    processing_time_ms=processing_time,
                    calculation_method=method
                )
            else:
                return CalculationResult(
                    system_name=system_name,
                    status="failed",
                    pillars={},
                    ilgan="",
                    processing_time_ms=processing_time,
                    calculation_method=method,
                    error_message="Empty or invalid result"
                )
                
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return CalculationResult(
                system_name=system_name,
                status="error",
                pillars={},
                ilgan="",
                processing_time_ms=processing_time,
                calculation_method="ERROR",
                error_message=str(e)
            )
    
    def _simulate_legacy_calculation(self, test_case: TestCase) -> Dict[str, Any]:
        """74000 만세력 시뮬레이션 (실제 DB 없이)"""
        
        # 전통 만세력 계산 시뮬레이션
        # 중국식 기준, 표준시 135도, 다른 절기 기준
        
        # 갑자 순환 (기준점 다름)
        base_date = datetime(1900, 1, 1).date()  # 전통 기준
        target_date = datetime(test_case.year, test_case.month, test_case.day).date()
        date_diff = (target_date - base_date).days
        
        # 전통 계산법 (HEAL7과 차이)
        day_index = date_diff % 60
        cheongan_idx = day_index % 10
        jiji_idx = day_index % 12
        
        from .myeongrihak_constants import CHEONGAN, JIJI
        
        day_cheongan = CHEONGAN[cheongan_idx]
        day_jiji = JIJI[jiji_idx]
        day_gapja = day_cheongan + day_jiji
        
        # 임시 년월시주 (실제로는 복잡한 계산)
        year_gapja = "甲子"
        month_gapja = "乙丑" 
        hour_gapja = "丙寅"
        
        return {
            "pillars": {
                "year": {"gapja": year_gapja, "cheongan": year_gapja[0], "jiji": year_gapja[1]},
                "month": {"gapja": month_gapja, "cheongan": month_gapja[0], "jiji": month_gapja[1]},
                "day": {"gapja": day_gapja, "cheongan": day_cheongan, "jiji": day_jiji},
                "hour": {"gapja": hour_gapja, "cheongan": hour_gapja[0], "jiji": hour_gapja[1]}
            },
            "ilgan": day_cheongan,
            "_method": "legacy_simulation",
            "_note": "전통 만세력 시뮬레이션 (중국 기준)"
        }
    
    def calculate_accuracy(self, reference: CalculationResult, target: CalculationResult) -> float:
        """정확도 계산 (KASI 기준)"""
        
        if reference.status != "success" or target.status != "success":
            return 0.0
        
        score = 0.0
        total_points = 4.0
        
        # 일간 일치 (가장 중요) - 2점
        if reference.ilgan == target.ilgan:
            score += 2.0
        
        # 일주 일치 - 1점
        ref_day = reference.pillars.get("day", {}).get("gapja", "")
        tar_day = target.pillars.get("day", {}).get("gapja", "")
        if ref_day == tar_day:
            score += 1.0
        
        # 시주 일치 - 1점  
        ref_hour = reference.pillars.get("hour", {}).get("gapja", "")
        tar_hour = target.pillars.get("hour", {}).get("gapja", "")
        if ref_hour == tar_hour:
            score += 1.0
        
        return (score / total_points) * 100
    
    async def run_simulation(self, case_count: int = 10):
        """시뮬레이션 실행"""
        
        print("🎲 사주 계산 시스템 시뮬레이션 분석 시작")
        print("=" * 60)
        print(f"테스트 케이스: {case_count}개 (동적 생성)")
        print(f"비교 시스템: {len(self.systems)}개")
        print(f"하드코딩 제거: 동적 케이스 생성 및 비교")
        print("=" * 60)
        
        # 테스트 케이스 생성
        test_cases = self.generate_random_cases(case_count)
        
        # 통계 초기화
        system_stats = {name: {
            "success_count": 0,
            "total_tests": 0,
            "processing_times": [],
            "accuracy_scores": []
        } for name in self.systems.keys()}
        
        # 각 테스트 케이스 실행
        for idx, test_case in enumerate(test_cases, 1):
            print(f"\n🎯 테스트 {idx}/{case_count}: {test_case.description} ({test_case.era})")
            print("-" * 50)
            
            # 모든 시스템으로 계산
            system_results = {}
            
            for system_name in self.systems.keys():
                result = await self.calculate_with_system(test_case, system_name)
                system_results[system_name] = result
                
                # 통계 업데이트
                system_stats[system_name]["total_tests"] += 1
                if result.status == "success":
                    system_stats[system_name]["success_count"] += 1
                    system_stats[system_name]["processing_times"].append(result.processing_time_ms)
                
                print(f"  {system_name}: {result.status} ({result.processing_time_ms:.1f}ms)")
            
            # KASI를 기준으로 정확도 계산
            kasi_result = system_results.get("KASI_DIRECT")
            if kasi_result and kasi_result.status == "success":
                print(f"\n📊 KASI 기준 일간: {kasi_result.ilgan}")
                
                for system_name, result in system_results.items():
                    if system_name != "KASI_DIRECT":
                        accuracy = self.calculate_accuracy(kasi_result, result)
                        result.accuracy_score = accuracy
                        system_stats[system_name]["accuracy_scores"].append(accuracy)
                        
                        match_status = "✅" if accuracy >= 75 else "⚠️" if accuracy >= 50 else "❌"
                        print(f"  {system_name} 정확도: {accuracy:.1f}% {match_status}")
            
            # 결과 저장
            self.test_results.append({
                "test_case": test_case,
                "results": system_results
            })
            
            # API 과부하 방지
            await asyncio.sleep(0.3)
        
        # 최종 분석
        await self._generate_final_analysis(system_stats)
    
    async def _generate_final_analysis(self, system_stats: Dict):
        """최종 분석 결과 생성"""
        
        print("\n" + "=" * 60)
        print("📊 시뮬레이션 최종 분석 결과")
        print("=" * 60)
        
        # 시스템별 성능 요약
        print("\n🎯 시스템별 성능 요약:")
        for system_name, stats in system_stats.items():
            total = stats["total_tests"]
            success = stats["success_count"]
            success_rate = (success / total * 100) if total > 0 else 0
            
            print(f"\n📍 {system_name} ({self.systems[system_name]}):")
            print(f"  - 성공률: {success_rate:.1f}% ({success}/{total})")
            
            if stats["processing_times"]:
                avg_time = statistics.mean(stats["processing_times"])
                min_time = min(stats["processing_times"])
                max_time = max(stats["processing_times"])
                print(f"  - 처리시간: 평균 {avg_time:.1f}ms (최소 {min_time:.1f}ms, 최대 {max_time:.1f}ms)")
            
            if stats["accuracy_scores"]:
                avg_accuracy = statistics.mean(stats["accuracy_scores"])
                min_accuracy = min(stats["accuracy_scores"])
                max_accuracy = max(stats["accuracy_scores"])
                print(f"  - 정확도: 평균 {avg_accuracy:.1f}% (최소 {min_accuracy:.1f}%, 최대 {max_accuracy:.1f}%)")
        
        # 권장사항
        print(f"\n💡 분석 결과 권장사항:")
        
        # 최고 성능 시스템
        best_performance = min(
            [(name, stats) for name, stats in system_stats.items() 
             if stats["processing_times"]], 
            key=lambda x: statistics.mean(x[1]["processing_times"])
        )
        print(f"  ⚡ 최고 성능: {best_performance[0]} (평균 {statistics.mean(best_performance[1]['processing_times']):.1f}ms)")
        
        # 최고 정확도 시스템
        best_accuracy = max(
            [(name, stats) for name, stats in system_stats.items() 
             if stats["accuracy_scores"]], 
            key=lambda x: statistics.mean(x[1]["accuracy_scores"])
        )
        print(f"  🎯 최고 정확도: {best_accuracy[0]} (평균 {statistics.mean(best_accuracy[1]['accuracy_scores']):.1f}%)")
        
        # 균형잡힌 시스템
        balanced_scores = {}
        for name, stats in system_stats.items():
            if stats["processing_times"] and stats["accuracy_scores"]:
                # 성능과 정확도의 조화점수
                perf_score = 100 - min(100, statistics.mean(stats["processing_times"]) / 10)
                acc_score = statistics.mean(stats["accuracy_scores"])
                balanced_scores[name] = (perf_score + acc_score) / 2
        
        if balanced_scores:
            best_balanced = max(balanced_scores.items(), key=lambda x: x[1])
            print(f"  ⚖️ 최적 균형: {best_balanced[0]} (균형점수 {best_balanced[1]:.1f})")


async def main():
    """메인 실행 함수"""
    
    analyzer = SimulationAnalyzer()
    await analyzer.run_simulation(10)  # 랜덤 10명
    
    # 결과 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"/tmp/simulation_analysis_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(analyzer.test_results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n💾 시뮬레이션 결과 저장: /tmp/simulation_analysis_{timestamp}.json")


if __name__ == "__main__":
    asyncio.run(main())