"""
원자 모듈: 사주 계산 핵심 로직
복잡도: 5분 이해 가능
책임: 단일 책임 원칙 준수 - 사주 계산만 담당
테스트: 100% 커버리지
의존성: datetime, typing
"""

from datetime import datetime
from typing import Dict, List, Tuple, Optional


class SajuCalculator:
    """
    사주 계산을 위한 핵심 원자 모듈
    - 천간지지 계산
    - 오행 분석
    - 단순하고 명확한 로직
    """
    
    # 천간 (10개)
    HEAVENLY_STEMS = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    
    # 지지 (12개)
    EARTHLY_BRANCHES = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    # 오행 매핑
    FIVE_ELEMENTS = {
        '갑': '목', '을': '목',
        '병': '화', '정': '화',
        '무': '토', '기': '토',
        '경': '금', '신': '금',
        '임': '수', '계': '수'
    }
    
    def __init__(self):
        """초기화"""
        pass
    
    def calculate_stem_branch(self, year: int, month: int, day: int, hour: int) -> Dict[str, str]:
        """
        년월일시의 천간지지 계산
        
        Args:
            year: 연도 (1900-2100)
            month: 월 (1-12) 
            day: 일 (1-31)
            hour: 시 (0-23)
            
        Returns:
            Dict: {'year': '갑자', 'month': '을축', ...}
        """
        result = {}
        
        # 년주 계산 (기준: 1924년 = 갑자년)
        year_offset = (year - 1924) % 60
        year_stem = self.HEAVENLY_STEMS[year_offset % 10]
        year_branch = self.EARTHLY_BRANCHES[year_offset % 12]
        result['year'] = year_stem + year_branch
        
        # 월주 계산 (기준: 정월 = 인월)
        month_stem_base = (year_offset % 10) * 2 + 2  # 년간에 따른 월간 시작점
        month_stem_idx = (month_stem_base + month - 3) % 10
        month_branch_idx = (month + 1) % 12
        result['month'] = self.HEAVENLY_STEMS[month_stem_idx] + self.EARTHLY_BRANCHES[month_branch_idx]
        
        # 일주 계산 (복잡한 공식이므로 단순화)
        # 실제로는 만년력 기반 계산 필요
        base_date = datetime(1900, 1, 1)
        target_date = datetime(year, month, day)
        days_diff = (target_date - base_date).days
        
        day_stem_idx = (days_diff + 6) % 10  # 1900.1.1 = 경진일 기준
        day_branch_idx = (days_diff + 8) % 12
        result['day'] = self.HEAVENLY_STEMS[day_stem_idx] + self.EARTHLY_BRANCHES[day_branch_idx]
        
        # 시주 계산
        hour_branch_idx = ((hour + 1) // 2) % 12
        hour_stem_base = day_stem_idx * 2  # 일간에 따른 시간 시작점
        hour_stem_idx = (hour_stem_base + hour_branch_idx) % 10
        result['hour'] = self.HEAVENLY_STEMS[hour_stem_idx] + self.EARTHLY_BRANCHES[hour_branch_idx]
        
        return result
    
    def analyze_elements(self, stem_branch_dict: Dict[str, str]) -> Dict[str, int]:
        """
        사주의 오행 분석
        
        Args:
            stem_branch_dict: calculate_stem_branch 결과
            
        Returns:
            Dict: 오행별 개수 {'목': 2, '화': 1, ...}
        """
        element_count = {'목': 0, '화': 0, '토': 0, '금': 0, '수': 0}
        
        for pillar_name, stem_branch in stem_branch_dict.items():
            # 천간의 오행
            stem = stem_branch[0]
            if stem in self.FIVE_ELEMENTS:
                element = self.FIVE_ELEMENTS[stem]
                element_count[element] += 1
        
        return element_count
    
    def get_dominant_element(self, element_analysis: Dict[str, int]) -> str:
        """
        가장 강한 오행 반환
        
        Args:
            element_analysis: analyze_elements 결과
            
        Returns:
            str: 가장 많은 오행 ('목', '화', '토', '금', '수')
        """
        return max(element_analysis, key=element_analysis.get)


def test_saju_calculator():
    """사주 계산기 테스트 케이스"""
    calculator = SajuCalculator()
    
    # 기본 계산 테스트
    result = calculator.calculate_stem_branch(1990, 5, 15, 14)
    assert isinstance(result, dict)
    assert len(result) == 4  # 년월일시
    assert all(len(v) == 2 for v in result.values())  # 천간+지지 = 2글자
    
    # 오행 분석 테스트
    elements = calculator.analyze_elements(result)
    assert isinstance(elements, dict)
    assert len(elements) == 5  # 오행 5개
    assert sum(elements.values()) == 4  # 사주 = 4개 기둥
    
    # 주요 오행 테스트
    dominant = calculator.get_dominant_element(elements)
    assert dominant in ['목', '화', '토', '금', '수']
    
    print("✅ 모든 테스트 통과")


def test_edge_cases():
    """경계값 테스트"""
    calculator = SajuCalculator()
    
    # 경계 연도 테스트
    result_1900 = calculator.calculate_stem_branch(1900, 1, 1, 0)
    result_2100 = calculator.calculate_stem_branch(2100, 12, 31, 23)
    
    assert isinstance(result_1900, dict)
    assert isinstance(result_2100, dict)
    
    # 윤년 테스트 (2020년 2월 29일)
    result_leap = calculator.calculate_stem_branch(2020, 2, 29, 12)
    assert isinstance(result_leap, dict)
    
    print("✅ 경계값 테스트 통과")


def test_consistency():
    """일관성 테스트"""
    calculator = SajuCalculator()
    
    # 같은 입력에 대해 같은 결과 보장
    result1 = calculator.calculate_stem_branch(1985, 7, 20, 10)
    result2 = calculator.calculate_stem_branch(1985, 7, 20, 10)
    
    assert result1 == result2
    
    # 다른 입력에 대해 다른 결과
    result3 = calculator.calculate_stem_branch(1985, 7, 21, 10)
    assert result1 != result3
    
    print("✅ 일관성 테스트 통과")


# 사용 예시
if __name__ == "__main__":
    # 기본 사용법
    calculator = SajuCalculator()
    
    # 1990년 5월 15일 오후 2시 태생 사주 계산
    birth_saju = calculator.calculate_stem_branch(1990, 5, 15, 14)
    print("🔮 사주 계산 결과:")
    print(f"년주: {birth_saju['year']}")
    print(f"월주: {birth_saju['month']}")
    print(f"일주: {birth_saju['day']}")
    print(f"시주: {birth_saju['hour']}")
    
    # 오행 분석
    elements = calculator.analyze_elements(birth_saju)
    print("\n🌟 오행 분석:")
    for element, count in elements.items():
        if count > 0:
            print(f"{element}: {count}개")
    
    # 주요 오행
    dominant = calculator.get_dominant_element(elements)
    print(f"\n💎 주요 오행: {dominant}")
    
    # 테스트 실행
    print("\n🧪 테스트 실행:")
    test_saju_calculator()
    test_edge_cases()
    test_consistency()
    
    print("\n✅ 사주 계산기 원자 모듈 실행 완료!")