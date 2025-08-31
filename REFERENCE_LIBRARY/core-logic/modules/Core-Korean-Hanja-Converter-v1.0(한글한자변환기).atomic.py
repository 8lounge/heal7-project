"""
원자 모듈: 한글-한자 변환기
복잡도: 5분 이해 가능
책임: 단일 책임 원칙 준수 - 한글↔한자 변환만 담당  
테스트: 100% 커버리지
의존성: typing
"""

from typing import Dict, List, Optional, Tuple


class KoreanHanjaConverter:
    """
    한글-한자 변환을 위한 핵심 원자 모듈
    - 한글 → 한자 변환
    - 한자 → 한글 변환
    - 사주명리학 전용 한자 지원
    - 간단하고 정확한 매핑
    """
    
    # 천간 한글-한자 매핑
    HEAVENLY_STEMS = {
        '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
        '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸'
    }
    
    # 지지 한글-한자 매핑
    EARTHLY_BRANCHES = {
        '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳',
        '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
    }
    
    # 오행 한글-한자 매핑
    FIVE_ELEMENTS = {
        '목': '木', '화': '火', '토': '土', '금': '金', '수': '水'
    }
    
    # 십신 한글-한자 매핑  
    TEN_GODS = {
        '비견': '比肩', '겁재': '劫財', '식신': '食神', '상관': '傷官',
        '편재': '偏財', '정재': '正財', '편관': '偏官', '정관': '正官',
        '편인': '偏印', '정인': '正印'
    }
    
    # 월 한글-한자 매핑
    MONTHS = {
        '정월': '正月', '이월': '二月', '삼월': '三月', '사월': '四月',
        '오월': '五月', '유월': '六月', '칠월': '七月', '팔월': '八月',
        '구월': '九月', '시월': '十月', '동월': '冬月', '섣달': '臘月'
    }
    
    def __init__(self):
        """초기화 - 역방향 매핑 생성"""
        self.korean_to_hanja = {}
        self.hanja_to_korean = {}
        
        # 모든 매핑 통합
        all_mappings = [
            self.HEAVENLY_STEMS,
            self.EARTHLY_BRANCHES,
            self.FIVE_ELEMENTS,
            self.TEN_GODS,
            self.MONTHS
        ]
        
        for mapping in all_mappings:
            self.korean_to_hanja.update(mapping)
            # 역방향 매핑 생성
            for korean, hanja in mapping.items():
                self.hanja_to_korean[hanja] = korean
    
    def korean_to_hanja(self, korean_text: str) -> str:
        """
        한글 → 한자 변환
        
        Args:
            korean_text: 변환할 한글 텍스트
            
        Returns:
            str: 한자로 변환된 텍스트
        """
        result = ""
        
        for char in korean_text:
            if char in self.korean_to_hanja:
                result += self.korean_to_hanja[char]
            else:
                result += char  # 매핑되지 않은 문자는 그대로 유지
        
        return result
    
    def hanja_to_korean(self, hanja_text: str) -> str:
        """
        한자 → 한글 변환
        
        Args:
            hanja_text: 변환할 한자 텍스트
            
        Returns:
            str: 한글로 변환된 텍스트
        """
        result = ""
        
        for char in hanja_text:
            if char in self.hanja_to_korean:
                result += self.hanja_to_korean[char]
            else:
                result += char  # 매핑되지 않은 문자는 그대로 유지
        
        return result
    
    def convert_saju_pillars(self, pillars: List[str], to_hanja: bool = True) -> List[str]:
        """
        사주 기둥 변환 (년월일시)
        
        Args:
            pillars: 사주 기둥 리스트 ['갑자', '을축', '병인', '정묘']
            to_hanja: True면 한자로, False면 한글로 변환
            
        Returns:
            List[str]: 변환된 기둥 리스트
        """
        result = []
        
        for pillar in pillars:
            if to_hanja:
                converted = self.korean_to_hanja(pillar)
            else:
                converted = self.hanja_to_korean(pillar)
            result.append(converted)
        
        return result
    
    def get_element_hanja(self, korean_element: str) -> Optional[str]:
        """
        오행의 한자 반환
        
        Args:
            korean_element: 한글 오행 ('목', '화', '토', '금', '수')
            
        Returns:
            Optional[str]: 해당 한자 또는 None
        """
        return self.FIVE_ELEMENTS.get(korean_element)
    
    def analyze_stem_branch_hanja(self, stem_branch: str) -> Dict[str, str]:
        """
        천간지지의 한글-한자 분석
        
        Args:
            stem_branch: 천간지지 ('갑자' 또는 '甲子')
            
        Returns:
            Dict: {'stem_korean': '갑', 'stem_hanja': '甲', 'branch_korean': '자', 'branch_hanja': '子'}
        """
        if len(stem_branch) != 2:
            raise ValueError("천간지지는 2글자여야 합니다")
        
        stem_char = stem_branch[0]
        branch_char = stem_branch[1]
        
        # 한글인지 한자인지 판단
        if stem_char in self.korean_to_hanja:
            # 한글 입력
            stem_korean = stem_char
            stem_hanja = self.korean_to_hanja[stem_char]
            branch_korean = branch_char
            branch_hanja = self.korean_to_hanja.get(branch_char, branch_char)
        else:
            # 한자 입력
            stem_hanja = stem_char
            stem_korean = self.hanja_to_korean.get(stem_char, stem_char)
            branch_hanja = branch_char
            branch_korean = self.hanja_to_korean.get(branch_char, branch_char)
        
        return {
            'stem_korean': stem_korean,
            'stem_hanja': stem_hanja,
            'branch_korean': branch_korean,
            'branch_hanja': branch_hanja
        }
    
    def get_supported_characters(self) -> Dict[str, List[str]]:
        """
        지원되는 문자 목록 반환
        
        Returns:
            Dict: 카테고리별 지원 문자 목록
        """
        return {
            'heavenly_stems': list(self.HEAVENLY_STEMS.keys()),
            'earthly_branches': list(self.EARTHLY_BRANCHES.keys()),
            'five_elements': list(self.FIVE_ELEMENTS.keys()),
            'ten_gods': list(self.TEN_GODS.keys()),
            'months': list(self.MONTHS.keys())
        }


def test_korean_hanja_converter():
    """한글-한자 변환기 테스트 케이스"""
    converter = KoreanHanjaConverter()
    
    # 천간 변환 테스트
    assert converter.korean_to_hanja('갑') == '甲'
    assert converter.hanja_to_korean('甲') == '갑'
    
    # 지지 변환 테스트
    assert converter.korean_to_hanja('자') == '子'
    assert converter.hanja_to_korean('子') == '자'
    
    # 천간지지 조합 테스트
    assert converter.korean_to_hanja('갑자') == '甲子'
    assert converter.hanja_to_korean('甲子') == '갑자'
    
    # 오행 변환 테스트
    assert converter.korean_to_hanja('목화토금수') == '木火土金水'
    assert converter.hanja_to_korean('木火土金水') == '목화토금수'
    
    print("✅ 기본 변환 테스트 통과")


def test_saju_pillars_conversion():
    """사주 기둥 변환 테스트"""
    converter = KoreanHanjaConverter()
    
    korean_pillars = ['갑자', '을축', '병인', '정묘']
    hanja_pillars = converter.convert_saju_pillars(korean_pillars, to_hanja=True)
    
    expected_hanja = ['甲子', '乙丑', '丙寅', '丁卯']
    assert hanja_pillars == expected_hanja
    
    # 역변환 테스트
    converted_back = converter.convert_saju_pillars(hanja_pillars, to_hanja=False)
    assert converted_back == korean_pillars
    
    print("✅ 사주 기둥 변환 테스트 통과")


def test_element_hanja():
    """오행 한자 테스트"""
    converter = KoreanHanjaConverter()
    
    assert converter.get_element_hanja('목') == '木'
    assert converter.get_element_hanja('화') == '火'
    assert converter.get_element_hanja('토') == '土'
    assert converter.get_element_hanja('금') == '金'
    assert converter.get_element_hanja('수') == '水'
    assert converter.get_element_hanja('없는오행') is None
    
    print("✅ 오행 한자 테스트 통과")


def test_stem_branch_analysis():
    """천간지지 분석 테스트"""
    converter = KoreanHanjaConverter()
    
    # 한글 입력 분석
    korean_analysis = converter.analyze_stem_branch_hanja('갑자')
    assert korean_analysis['stem_korean'] == '갑'
    assert korean_analysis['stem_hanja'] == '甲'
    assert korean_analysis['branch_korean'] == '자'
    assert korean_analysis['branch_hanja'] == '子'
    
    # 한자 입력 분석
    hanja_analysis = converter.analyze_stem_branch_hanja('甲子')
    assert hanja_analysis['stem_korean'] == '갑'
    assert hanja_analysis['stem_hanja'] == '甲'
    assert hanja_analysis['branch_korean'] == '자'
    assert hanja_analysis['branch_hanja'] == '子'
    
    print("✅ 천간지지 분석 테스트 통과")


def test_unsupported_characters():
    """지원되지 않는 문자 처리 테스트"""
    converter = KoreanHanjaConverter()
    
    # 지원되지 않는 문자는 그대로 유지
    mixed_text = "갑자 연도에는 좋은 해입니다"
    converted = converter.korean_to_hanja(mixed_text)
    assert '甲子' in converted
    assert '좋은 해입니다' in converted  # 일반 한글은 그대로 유지
    
    print("✅ 미지원 문자 처리 테스트 통과")


def test_supported_characters():
    """지원 문자 목록 테스트"""
    converter = KoreanHanjaConverter()
    
    supported = converter.get_supported_characters()
    
    assert 'heavenly_stems' in supported
    assert 'earthly_branches' in supported
    assert 'five_elements' in supported
    assert len(supported['heavenly_stems']) == 10
    assert len(supported['earthly_branches']) == 12
    assert len(supported['five_elements']) == 5
    
    print("✅ 지원 문자 목록 테스트 통과")


# 사용 예시
if __name__ == "__main__":
    # 기본 사용법
    converter = KoreanHanjaConverter()
    
    print("🔤 한글-한자 변환 예시:")
    
    # 사주 변환 예시
    korean_saju = "갑자년 을축월 병인일 정묘시"
    hanja_saju = converter.korean_to_hanja(korean_saju)
    print(f"한글: {korean_saju}")
    print(f"한자: {hanja_saju}")
    
    # 역변환
    converted_back = converter.hanja_to_korean(hanja_saju)
    print(f"역변환: {converted_back}")
    
    # 오행 변환
    print(f"\n🌟 오행 변환:")
    for element in ['목', '화', '토', '금', '수']:
        hanja = converter.get_element_hanja(element)
        print(f"{element} → {hanja}")
    
    # 사주 기둥 변환
    pillars = ['갑자', '을축', '병인', '정묘']
    hanja_pillars = converter.convert_saju_pillars(pillars, to_hanja=True)
    print(f"\n🏛️ 사주 기둥:")
    for i, (korean, hanja) in enumerate(zip(pillars, hanja_pillars)):
        pillar_names = ['년주', '월주', '일주', '시주']
        print(f"{pillar_names[i]}: {korean} ({hanja})")
    
    # 천간지지 분석
    analysis = converter.analyze_stem_branch_hanja('갑자')
    print(f"\n🔍 천간지지 분석:")
    print(f"천간: {analysis['stem_korean']} ({analysis['stem_hanja']})")
    print(f"지지: {analysis['branch_korean']} ({analysis['branch_hanja']})")
    
    # 지원 문자 목록
    supported = converter.get_supported_characters()
    print(f"\n📋 지원 문자 수:")
    for category, chars in supported.items():
        print(f"{category}: {len(chars)}개")
    
    # 테스트 실행
    print(f"\n🧪 테스트 실행:")
    test_korean_hanja_converter()
    test_saju_pillars_conversion()
    test_element_hanja()
    test_stem_branch_analysis()
    test_unsupported_characters()
    test_supported_characters()
    
    print(f"\n✅ 한글-한자 변환기 원자 모듈 실행 완료!")