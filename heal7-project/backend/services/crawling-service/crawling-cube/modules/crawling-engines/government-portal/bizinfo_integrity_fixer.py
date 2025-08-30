#!/usr/bin/env python3
"""
BIZINFO 데이터 무결성 오류 자동 수정기
데이터 품질 향상 및 오류 데이터 복구

Author: Paperwork AI Team
Version: 1.0.0
Date: 2025-08-24
"""

import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class IntegrityFixResult:
    """무결성 수정 결과"""
    original_data: Dict
    fixed_data: Dict
    fixes_applied: List[str]
    remaining_errors: List[str]
    quality_improvement: float
    is_recoverable: bool

class BizinfoIntegrityFixer:
    """BIZINFO 데이터 무결성 자동 수정기"""
    
    def __init__(self):
        # 기관명 정규화 매핑
        self.agency_normalization = {
            '중소벤처기업부': ['중기부', 'SME', '중소벤처부', '중소기업부'],
            '중소기업기술정보진흥원': ['TIPA', '중소기업진흥원', '기술정보진흥원'],
            '창업진흥원': ['KISED', '창진원'],
            '한국무역협회': ['KITA', '무역협회'],
            '한국산업기술진흥원': ['KIAT', '산기진'],
            '중소기업진흥공단': ['중진공', 'SBC'],
            '한국여성경제인협회': ['KWEA', '여경협'],
            '소상공인시장진흥공단': ['소진공', 'SEMAS']
        }
        
        # 지원형태 정규화
        self.support_type_normalization = {
            '융자': ['대출', '융자지원', '저리융자'],
            '보조금': ['지원금', '보조', '지원'],
            '투자': ['투자지원', '펀드'],
            '교육': ['교육지원', '연수', '프로그램'],
            '컨설팅': ['자문', '컨설팅지원', '멘토링'],
            '인프라': ['공간지원', '시설지원', '인프라지원']
        }
        
        # 지원대상 키워드
        self.target_keywords = {
            '중소기업': ['중소기업', 'SME', '소기업'],
            '소상공인': ['소상공인', '자영업'],
            '벤처기업': ['벤처', 'VC', '벤처기업'],
            '스타트업': ['스타트업', '창업기업', '신생기업'],
            '청년': ['청년', '청년창업', '39세이하'],
            '여성': ['여성', '여성기업'],
            '예비창업자': ['예비창업', '창업준비', '창업희망']
        }
        
        # 날짜 패턴
        self.date_patterns = [
            r'(\d{4})[.-](\d{1,2})[.-](\d{1,2})',  # YYYY.MM.DD, YYYY-MM-DD
            r'(\d{1,2})[.-](\d{1,2})[.-](\d{4})',  # MM.DD.YYYY, MM-DD-YYYY
            r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일',  # YYYY년 MM월 DD일
            r'(\d{1,2})월\s*(\d{1,2})일'  # MM월 DD일
        ]

    def fix_agency_name(self, agency: str) -> Tuple[str, bool]:
        """기관명 정규화 및 수정"""
        if not agency or len(agency.strip()) < 2:
            return agency, False
        
        agency_clean = agency.strip()
        
        # 정규화된 기관명으로 변환
        for standard_name, variations in self.agency_normalization.items():
            for variation in variations:
                if variation in agency_clean:
                    return standard_name, True
        
        # 기관명 패턴 보정
        fixes = []
        
        # 공통 오타 수정
        typo_fixes = {
            '기업진흠원': '기업진흥원',
            '중소기업청': '중소벤처기업부',
            '창업청': '창업진흥원',
            '중소기업부': '중소벤처기업부'
        }
        
        for typo, correction in typo_fixes.items():
            if typo in agency_clean:
                agency_clean = agency_clean.replace(typo, correction)
                fixes.append(f"기관명 오타 수정: {typo} → {correction}")
        
        # 불완전한 기관명 보완
        if '진흥원' in agency_clean and '기업' in agency_clean:
            if '중소기업' in agency_clean:
                agency_clean = '중소기업기술정보진흥원'
                fixes.append("불완전한 기관명 보완")
        
        return agency_clean, len(fixes) > 0

    def fix_title(self, title: str) -> Tuple[str, bool]:
        """제목 정규화 및 수정"""
        if not title:
            return title, False
        
        title_clean = title.strip()
        fixes = []
        
        # HTML 태그 제거
        if '<' in title_clean and '>' in title_clean:
            title_clean = re.sub(r'<[^>]+>', '', title_clean)
            fixes.append("HTML 태그 제거")
        
        # 특수문자 정리
        title_clean = re.sub(r'\s+', ' ', title_clean)  # 연속 공백 제거
        title_clean = re.sub(r'[^\w\s\-()[\].,:]', '', title_clean)  # 특수문자 제거
        
        # 제목 길이 확인 및 보정
        if len(title_clean) < 10 and '공고' not in title_clean:
            # 짧은 제목에 정보 보완
            if any(keyword in title_clean for keyword in ['지원', '모집', '사업']):
                title_clean += ' 공고'
                fixes.append("제목에 '공고' 추가")
        
        # 중요 키워드 누락 확인
        important_keywords = ['공고', '모집', '지원', '사업', '선정']
        if not any(keyword in title_clean for keyword in important_keywords):
            if '2025' in title_clean or '창업' in title_clean:
                title_clean += ' 지원사업 공고'
                fixes.append("중요 키워드 보완")
        
        return title_clean, len(fixes) > 0

    def fix_support_type(self, support_type: str) -> Tuple[str, bool]:
        """지원형태 정규화"""
        if not support_type:
            return support_type, False
        
        support_clean = support_type.strip()
        
        # 정규화된 지원형태로 변환
        for standard_type, variations in self.support_type_normalization.items():
            for variation in variations:
                if variation in support_clean:
                    return standard_type, True
        
        # 일반적이지 않은 형태 수정
        if '금융' in support_clean or '자금' in support_clean:
            return '융자', True
        elif '교육' in support_clean or '연수' in support_clean:
            return '교육', True
        elif '상담' in support_clean or '컨설' in support_clean:
            return '컨설팅', True
        
        return support_clean, False

    def fix_target(self, target: str) -> Tuple[str, bool]:
        """지원대상 정규화 및 보완"""
        if not target:
            return target, False
        
        target_clean = target.strip()
        fixes = []
        
        # 표준 대상 키워드로 정규화
        for standard_target, variations in self.target_keywords.items():
            for variation in variations:
                if variation in target_clean and standard_target not in target_clean:
                    target_clean = target_clean.replace(variation, standard_target)
                    fixes.append(f"지원대상 정규화: {variation} → {standard_target}")
        
        # 불명확한 대상 구체화
        vague_patterns = ['기업체', '업체', '법인', '단체']
        for pattern in vague_patterns:
            if pattern in target_clean and '중소기업' not in target_clean:
                target_clean = target_clean.replace(pattern, '중소기업')
                fixes.append("불명확한 대상 구체화")
        
        return target_clean, len(fixes) > 0

    def fix_application_period(self, period: str) -> Tuple[str, bool]:
        """신청기간 형식 정규화"""
        if not period:
            return period, False
        
        period_clean = period.strip()
        fixes = []
        
        # 날짜 패턴 정규화
        for pattern in self.date_patterns:
            matches = re.findall(pattern, period_clean)
            if matches:
                # 날짜 형식 표준화
                if '년' in period_clean and '월' in period_clean:
                    # 이미 한국어 형식
                    break
                else:
                    # 숫자 형식을 한국어 형식으로 변환
                    for match in matches:
                        if len(match) == 3:  # YYYY.MM.DD 형식
                            year, month, day = match
                            korean_date = f"{year}년 {int(month)}월 {int(day)}일"
                            period_clean = re.sub(pattern, korean_date, period_clean, count=1)
                            fixes.append("날짜 형식 한국어로 정규화")
        
        # 기간 표현 정리
        if '~' not in period_clean and '-' not in period_clean and '부터' not in period_clean:
            if '까지' in period_clean:
                period_clean = period_clean.replace('까지', '까지')
            else:
                # 단일 날짜인 경우 '까지' 추가
                if any(char.isdigit() for char in period_clean):
                    period_clean += '까지'
                    fixes.append("기간 표현 보완")
        
        return period_clean, len(fixes) > 0

    def fix_url(self, url: str) -> Tuple[str, bool]:
        """URL 형식 수정"""
        if not url:
            return url, False
        
        url_clean = url.strip()
        
        # HTTP/HTTPS 프로토콜 확인
        if url_clean and not url_clean.startswith(('http://', 'https://')):
            if url_clean.startswith('//'):
                url_clean = 'https:' + url_clean
            elif url_clean.startswith('www.') or 'bizinfo.go.kr' in url_clean:
                url_clean = 'https://' + url_clean
            else:
                return url_clean, False
            return url_clean, True
        
        return url_clean, False

    def calculate_quality_score(self, data: Dict) -> float:
        """데이터 품질 점수 계산"""
        score = 100.0
        
        # 필수 필드 확인
        required_fields = ['title', 'agency', 'support_type', 'application_period', 'target']
        for field in required_fields:
            if not data.get(field, '').strip():
                score -= 15
        
        # 각 필드별 품질 평가
        title = data.get('title', '')
        if title:
            if len(title) < 10:
                score -= 10
            elif len(title) > 200:
                score -= 5
            
            important_keywords = ['공고', '모집', '지원', '사업']
            if not any(keyword in title for keyword in important_keywords):
                score -= 8
        
        # 기관명 품질
        agency = data.get('agency', '')
        if agency and len(agency) < 3:
            score -= 10
        
        # URL 품질
        detail_url = data.get('detail_url', '')
        if detail_url:
            if not detail_url.startswith('http'):
                score -= 8
            elif 'bizinfo.go.kr' not in detail_url:
                score -= 3
        
        return max(0, min(100, score))

    def fix_bizinfo_data(self, data: Dict) -> IntegrityFixResult:
        """BIZINFO 데이터 무결성 종합 수정"""
        if not isinstance(data, dict):
            return IntegrityFixResult(
                original_data=data,
                fixed_data=data,
                fixes_applied=[],
                remaining_errors=["입력 데이터가 딕셔너리가 아닙니다"],
                quality_improvement=0.0,
                is_recoverable=False
            )
        
        original_quality = self.calculate_quality_score(data)
        fixed_data = data.copy()
        fixes_applied = []
        remaining_errors = []
        
        # 각 필드별 수정 적용
        if 'title' in fixed_data:
            fixed_title, title_fixed = self.fix_title(fixed_data['title'])
            if title_fixed:
                fixed_data['title'] = fixed_title
                fixes_applied.append("제목 정규화 및 보완")
        
        if 'agency' in fixed_data:
            fixed_agency, agency_fixed = self.fix_agency_name(fixed_data['agency'])
            if agency_fixed:
                fixed_data['agency'] = fixed_agency
                fixes_applied.append("기관명 정규화 및 수정")
        
        if 'support_type' in fixed_data:
            fixed_support, support_fixed = self.fix_support_type(fixed_data['support_type'])
            if support_fixed:
                fixed_data['support_type'] = fixed_support
                fixes_applied.append("지원형태 정규화")
        
        if 'target' in fixed_data:
            fixed_target, target_fixed = self.fix_target(fixed_data['target'])
            if target_fixed:
                fixed_data['target'] = fixed_target
                fixes_applied.append("지원대상 정규화 및 보완")
        
        if 'application_period' in fixed_data:
            fixed_period, period_fixed = self.fix_application_period(fixed_data['application_period'])
            if period_fixed:
                fixed_data['application_period'] = fixed_period
                fixes_applied.append("신청기간 형식 정규화")
        
        if 'detail_url' in fixed_data:
            fixed_url, url_fixed = self.fix_url(fixed_data['detail_url'])
            if url_fixed:
                fixed_data['detail_url'] = fixed_url
                fixes_applied.append("URL 형식 수정")
        
        # 수정 후 품질 점수 계산
        final_quality = self.calculate_quality_score(fixed_data)
        quality_improvement = final_quality - original_quality
        
        # 남은 오류 확인
        required_fields = ['title', 'agency', 'support_type', 'application_period', 'target']
        for field in required_fields:
            if not fixed_data.get(field, '').strip():
                remaining_errors.append(f"필수 필드 '{field}'가 여전히 비어있습니다")
        
        # 품질 검증
        if final_quality < 60:
            remaining_errors.append(f"품질 점수가 낮습니다: {final_quality:.1f}/100")
        
        # 복구 가능성 판단
        is_recoverable = len(remaining_errors) == 0 and final_quality >= 70
        
        # 수정 메타데이터 추가
        fixed_data['_integrity_fix_metadata'] = {
            'fixed_at': datetime.now().isoformat(),
            'original_quality': round(original_quality, 1),
            'final_quality': round(final_quality, 1),
            'fixes_applied': fixes_applied,
            'is_auto_fixed': True
        }
        
        return IntegrityFixResult(
            original_data=data,
            fixed_data=fixed_data,
            fixes_applied=fixes_applied,
            remaining_errors=remaining_errors,
            quality_improvement=round(quality_improvement, 1),
            is_recoverable=is_recoverable
        )

    def batch_fix_bizinfo_data(self, data_list: List[Dict]) -> Dict[str, any]:
        """BIZINFO 데이터 배치 수정"""
        if not isinstance(data_list, list):
            return {
                'error': '입력이 리스트가 아닙니다',
                'processed': 0,
                'results': []
            }
        
        results = []
        total_quality_improvement = 0.0
        recoverable_count = 0
        
        for i, data in enumerate(data_list):
            try:
                fix_result = self.fix_bizinfo_data(data)
                results.append({
                    'index': i,
                    'original_id': data.get('id', f'item_{i}'),
                    'fixes_applied': fix_result.fixes_applied,
                    'quality_improvement': fix_result.quality_improvement,
                    'is_recoverable': fix_result.is_recoverable,
                    'remaining_errors': fix_result.remaining_errors,
                    'fixed_data': fix_result.fixed_data
                })
                
                total_quality_improvement += fix_result.quality_improvement
                if fix_result.is_recoverable:
                    recoverable_count += 1
                    
            except Exception as e:
                results.append({
                    'index': i,
                    'original_id': data.get('id', f'item_{i}'),
                    'error': str(e),
                    'is_recoverable': False
                })
        
        return {
            'processed': len(data_list),
            'recoverable': recoverable_count,
            'total_quality_improvement': round(total_quality_improvement, 1),
            'average_quality_improvement': round(total_quality_improvement / len(data_list), 1) if data_list else 0,
            'results': results,
            'summary': {
                'recovery_rate': f"{recoverable_count}/{len(data_list)} ({100*recoverable_count/len(data_list):.1f}%)" if data_list else "0%",
                'most_common_fixes': self._get_most_common_fixes(results)
            }
        }

    def _get_most_common_fixes(self, results: List[Dict]) -> List[str]:
        """가장 일반적인 수정사항 집계"""
        fix_counts = {}
        
        for result in results:
            if 'fixes_applied' in result:
                for fix in result['fixes_applied']:
                    fix_counts[fix] = fix_counts.get(fix, 0) + 1
        
        # 빈도순 정렬
        sorted_fixes = sorted(fix_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{fix} ({count}회)" for fix, count in sorted_fixes[:5]]

# 사용 예시
def main():
    """메인 실행 함수"""
    fixer = BizinfoIntegrityFixer()
    
    # 테스트 데이터
    test_data = {
        'title': '2025 창업지원',  # 너무 짧은 제목
        'agency': '중기부',  # 약칭
        'support_type': '자금지원',  # 비표준 형태
        'target': '업체',  # 모호한 대상
        'application_period': '2025.3.1 ~ 2025.3.31',  # 숫자 형식
        'detail_url': 'www.bizinfo.go.kr/detail/123'  # 프로토콜 누락
    }
    
    print("=" * 60)
    print("🔧 BIZINFO 데이터 무결성 자동 수정 테스트")
    print("=" * 60)
    print()
    
    print("📋 원본 데이터:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    print()
    
    # 수정 실행
    result = fixer.fix_bizinfo_data(test_data)
    
    print("✅ 수정 결과:")
    print(f"  품질 개선: {result.quality_improvement:+.1f}점")
    print(f"  복구 가능: {'예' if result.is_recoverable else '아니오'}")
    print()
    
    print("🔧 적용된 수정사항:")
    for fix in result.fixes_applied:
        print(f"  - {fix}")
    print()
    
    print("📋 수정된 데이터:")
    for key, value in result.fixed_data.items():
        if key != '_integrity_fix_metadata':
            print(f"  {key}: {value}")
    print()
    
    if result.remaining_errors:
        print("⚠️ 남은 오류:")
        for error in result.remaining_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    main()