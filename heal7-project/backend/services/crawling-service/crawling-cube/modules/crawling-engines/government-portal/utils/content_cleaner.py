"""
Content Cleaner for Government Portal Data
정부 포털 데이터 정리 및 정규화 유틸리티

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ContentCleaner:
    """스크래핑한 콘텐츠 정리 및 정규화"""
    
    def __init__(self):
        # 한국어 정부 문서 특화 패턴
        self.korean_patterns = {
            'agencies': [
                '중소벤처기업부', '중소기업진흥공단', '정보통신산업진흥원', '기술보증기금',
                '창업진흥원', '산업기술진흥원', '한국산업기술평가관리원', '코트라',
                '중소기업청', '벤처기업부', 'SBA', 'KOSMES', 'NIPA', 'TECHNO', 'KOTRA'
            ],
            'support_types': [
                '융자', '보조금', '지원금', '바우처', '세액공제', '투자', '출연금',
                '컨설팅', '멘토링', '교육', '코칭', '인큐베이팅', '액셀러레이팅',
                '공간지원', '시설지원', '장비지원', '네트워킹', '마케팅', '홍보'
            ],
            'business_stages': [
                '예비창업자', '초기창업자', '창업기업', '벤처기업', '중소기업', '소상공인',
                '스타트업', '청년창업', '여성창업', '시니어창업', '재도전기업'
            ]
        }
        
        # 정규식 패턴
        self.regex_patterns = {
            'phone': re.compile(r'\b(\d{2,3}[-.]?\d{3,4}[-.]?\d{4})\b'),
            'email': re.compile(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'),
            'url': re.compile(r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?'),
            'date_range': re.compile(r'(\d{4})\.(\d{1,2})\.(\d{1,2})\s*[~-]\s*(\d{4})\.(\d{1,2})\.(\d{1,2})'),
            'amount': re.compile(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(억|만원|원|천만원|백만원)'),
            'period': re.compile(r'(\d+)\s*(개월|년|일)')
        }
        
        # 불필요한 문자열 패턴
        self.cleanup_patterns = [
            # HTML 태그 잔여물
            re.compile(r'<[^>]+>'),
            # 연속된 공백, 탭, 줄바꿈
            re.compile(r'\s+'),
            # 특수 문자 정리
            re.compile(r'[^\w\s가-힣\.\,\-\(\)\[\]\/\:]+'),
            # 괄호 안의 영어/숫자만 있는 경우 (예: "(English)", "(123)")
            re.compile(r'\([a-zA-Z0-9\s]+\)'),
            # 불필요한 기호 반복
            re.compile(r'[-\.\,]{2,}')
        ]
    
    def clean_text(self, text: str) -> str:
        """기본 텍스트 정리"""
        if not text or not isinstance(text, str):
            return ""
        
        # 1. HTML 태그 제거
        cleaned = re.sub(self.cleanup_patterns[0], ' ', text)
        
        # 2. 연속된 공백 정리
        cleaned = re.sub(self.cleanup_patterns[1], ' ', cleaned)
        
        # 3. 앞뒤 공백 제거
        cleaned = cleaned.strip()
        
        # 4. 특수 패턴 정리
        for pattern in self.cleanup_patterns[2:]:
            cleaned = re.sub(pattern, ' ', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned)  # 다시 공백 정리
        
        return cleaned.strip()
    
    def extract_structured_info(self, text: str) -> Dict:
        """텍스트에서 구조화된 정보 추출"""
        if not text:
            return {}
        
        info = {
            'phones': [],
            'emails': [],
            'urls': [],
            'dates': [],
            'amounts': [],
            'periods': [],
            'agencies': [],
            'support_types': [],
            'business_stages': []
        }
        
        # 정규식 패턴 매칭
        for key, pattern in self.regex_patterns.items():
            matches = pattern.findall(text)
            if key == 'phone':
                info['phones'] = [self.normalize_phone(match) for match in matches]
            elif key == 'email':
                info['emails'] = matches
            elif key == 'url':
                info['urls'] = matches
            elif key == 'date_range':
                info['dates'] = [self.format_date_range(match) for match in matches]
            elif key == 'amount':
                info['amounts'] = [f"{match[0]}{match[1]}" for match in matches]
            elif key == 'period':
                info['periods'] = [f"{match[0]}{match[1]}" for match in matches]
        
        # 키워드 매칭
        for category, keywords in self.korean_patterns.items():
            found_keywords = []
            for keyword in keywords:
                if keyword in text:
                    found_keywords.append(keyword)
            
            if category == 'agencies':
                info['agencies'] = found_keywords
            elif category == 'support_types':
                info['support_types'] = found_keywords
            elif category == 'business_stages':
                info['business_stages'] = found_keywords
        
        # 빈 리스트 제거
        return {k: v for k, v in info.items() if v}
    
    def normalize_phone(self, phone: str) -> str:
        """전화번호 정규화"""
        # 숫자만 추출
        digits = re.sub(r'\D', '', phone)
        
        # 국번에 따른 형식 적용
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return phone  # 원본 반환
    
    def format_date_range(self, date_match: tuple) -> str:
        """날짜 범위 형식화"""
        try:
            start_year, start_month, start_day = date_match[:3]
            end_year, end_month, end_day = date_match[3:]
            
            return f"{start_year}.{start_month.zfill(2)}.{start_day.zfill(2)} ~ {end_year}.{end_month.zfill(2)}.{end_day.zfill(2)}"
        except:
            return str(date_match)
    
    def clean_title(self, title: str) -> str:
        """제목 특화 정리"""
        if not title:
            return ""
        
        cleaned = self.clean_text(title)
        
        # 제목 특화 정리
        patterns = [
            # 번호 제거 (예: "1. 사업명", "[1] 사업명")
            re.compile(r'^[\[\(]?\d+[\]\)]?\.\s*'),
            # 불필요한 접두사 제거
            re.compile(r'^(공고|모집|신청|지원)\s*[:\-]?\s*'),
            # 연도 정리 (예: "2024년도" -> "2024")
            re.compile(r'(\d{4})년도'),
            # 과도한 대괄호나 괄호 정리
            re.compile(r'\[([^\[\]]+)\]'),
            re.compile(r'\(([^\(\)]+)\)')
        ]
        
        for pattern in patterns:
            cleaned = pattern.sub(lambda m: m.group(1) if len(m.groups()) > 0 else '', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def clean_agency_name(self, agency: str) -> str:
        """기관명 정리 및 표준화"""
        if not agency:
            return ""
        
        cleaned = self.clean_text(agency)
        
        # 기관명 표준화 매핑
        agency_mapping = {
            '중소벤처기업부': '중소벤처기업부',
            '중기부': '중소벤처기업부',
            'MSS': '중소벤처기업부',
            '중소기업진흥공단': '중소기업진흥공단',
            'KOSMES': '중소기업진흥공단',
            'SBC': '중소기업진흥공단',
            '정보통신산업진흥원': '정보통신산업진흥원',
            'NIPA': '정보통신산업진흥원',
            '기술보증기금': '기술보증기금',
            'KIBO': '기술보증기금',
            'TECHNO': '기술보증기금'
        }
        
        # 매핑된 표준명 반환
        for variant, standard in agency_mapping.items():
            if variant in cleaned:
                return standard
        
        return cleaned
    
    def extract_application_period(self, text: str) -> Dict:
        """신청기간 추출 및 파싱"""
        if not text:
            return {}
        
        period_info = {}
        
        # 날짜 범위 패턴
        date_patterns = [
            # 2024.01.01 ~ 2024.12.31
            re.compile(r'(\d{4})\.(\d{1,2})\.(\d{1,2})\s*[~\-]\s*(\d{4})\.(\d{1,2})\.(\d{1,2})'),
            # 2024년 1월 1일 ~ 12월 31일
            re.compile(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일\s*[~\-]\s*(\d{1,2})월\s*(\d{1,2})일'),
            # 1월 1일 ~ 12월 31일 (당해년도)
            re.compile(r'(\d{1,2})월\s*(\d{1,2})일\s*[~\-]\s*(\d{1,2})월\s*(\d{1,2})일')
        ]
        
        for pattern in date_patterns:
            match = pattern.search(text)
            if match:
                groups = match.groups()
                if len(groups) == 6:  # Full date range
                    period_info = {
                        'start_date': f"{groups[0]}.{groups[1].zfill(2)}.{groups[2].zfill(2)}",
                        'end_date': f"{groups[3]}.{groups[4].zfill(2)}.{groups[5].zfill(2)}",
                        'format': 'date_range'
                    }
                elif len(groups) == 5:  # Year + month/day range
                    year = groups[0]
                    period_info = {
                        'start_date': f"{year}.{groups[1].zfill(2)}.{groups[2].zfill(2)}",
                        'end_date': f"{year}.{groups[3].zfill(2)}.{groups[4].zfill(2)}",
                        'format': 'same_year_range'
                    }
                break
        
        # 특수 키워드 감지
        special_keywords = {
            '상시': 'continuous',
            '연중': 'year_round', 
            '수시': 'anytime',
            '마감': 'deadline',
            '접수중': 'accepting',
            '종료': 'closed',
            '예정': 'planned'
        }
        
        for keyword, status in special_keywords.items():
            if keyword in text:
                period_info['status'] = status
                period_info['keyword'] = keyword
        
        return period_info
    
    def categorize_support_content(self, content: str) -> Dict:
        """지원 내용 카테고리 분류"""
        if not content:
            return {}
        
        categories = {
            'financial_support': [],  # 자금지원
            'service_support': [],    # 서비스지원  
            'infrastructure_support': [], # 인프라지원
            'education_support': []   # 교육지원
        }
        
        # 카테고리별 키워드 매핑
        category_keywords = {
            'financial_support': ['융자', '보조금', '지원금', '투자', '출연금', '바우처', '세액공제'],
            'service_support': ['컨설팅', '멘토링', '마케팅', '홍보', '판로', '수출지원'],
            'infrastructure_support': ['공간', '시설', '장비', '인프라', '네트워크', '플랫폼'],
            'education_support': ['교육', '연수', '세미나', '워크숍', '강의', '코칭']
        }
        
        for category, keywords in category_keywords.items():
            found_items = []
            for keyword in keywords:
                if keyword in content:
                    # 해당 키워드 주변 문맥 추출 (± 50자)
                    context = self.extract_context(content, keyword, window=50)
                    found_items.append({
                        'keyword': keyword,
                        'context': context
                    })
            
            if found_items:
                categories[category] = found_items
        
        return {k: v for k, v in categories.items() if v}  # 빈 카테고리 제거
    
    def extract_context(self, text: str, keyword: str, window: int = 50) -> str:
        """키워드 주변 문맥 추출"""
        if keyword not in text:
            return ""
        
        start_index = text.find(keyword)
        context_start = max(0, start_index - window)
        context_end = min(len(text), start_index + len(keyword) + window)
        
        context = text[context_start:context_end].strip()
        
        # 문장 경계에서 자르기
        sentences = re.split(r'[.!?]\s+', context)
        if len(sentences) > 1:
            # 키워드가 포함된 문장 찾기
            for sentence in sentences:
                if keyword in sentence:
                    return sentence.strip()
        
        return context
    
    def standardize_document_types(self, doc_list: List[str]) -> List[Dict]:
        """문서 유형 표준화"""
        if not doc_list:
            return []
        
        # 표준 문서 유형 매핑
        doc_type_mapping = {
            '사업계획서': 'business_plan',
            '신청서': 'application_form',
            '사업자등록증': 'business_license',
            '법인등기부등본': 'corporate_registry',
            '재무제표': 'financial_statement',
            '손익계산서': 'income_statement',
            '대차대조표': 'balance_sheet',
            '특허증': 'patent_certificate',
            '기술개발계획서': 'tech_development_plan',
            '시제품': 'prototype',
            '추천서': 'recommendation_letter',
            '이력서': 'resume',
            '경력증명서': 'career_certificate'
        }
        
        standardized_docs = []
        for doc in doc_list:
            if not doc or not isinstance(doc, str):
                continue
                
            cleaned_doc = self.clean_text(doc)
            
            # 매핑된 표준 유형 찾기
            doc_type = None
            for standard_name, type_code in doc_type_mapping.items():
                if standard_name in cleaned_doc:
                    doc_type = type_code
                    break
            
            standardized_docs.append({
                'original': doc,
                'cleaned': cleaned_doc,
                'type': doc_type or 'other',
                'required': '필수' in cleaned_doc or '반드시' in cleaned_doc,
                'optional': '선택' in cleaned_doc or '해당시' in cleaned_doc
            })
        
        return standardized_docs
    
    def validate_content_quality(self, content: Dict) -> Dict:
        """콘텐츠 품질 검증"""
        quality_score = 0
        max_score = 100
        issues = []
        
        # 1. 필수 필드 존재 여부 (30점)
        required_fields = ['title', 'agency', 'application_period']
        present_fields = sum(1 for field in required_fields if content.get(field))
        quality_score += (present_fields / len(required_fields)) * 30
        
        if present_fields < len(required_fields):
            missing = [field for field in required_fields if not content.get(field)]
            issues.append(f"필수 필드 누락: {', '.join(missing)}")
        
        # 2. 콘텐츠 길이 및 의미있는 정보 (25점)
        title_length = len(content.get('title', ''))
        if title_length > 10:
            quality_score += 10
        elif title_length < 5:
            issues.append("제목이 너무 짧음")
        
        if content.get('support_details') and len(content['support_details']) > 50:
            quality_score += 15
        else:
            issues.append("지원내용 정보 부족")
        
        # 3. 구조화된 정보 존재 (20점)
        structured_info = self.extract_structured_info(str(content))
        structured_score = min(20, len(structured_info) * 4)
        quality_score += structured_score
        
        # 4. 데이터 일관성 (15점)
        consistency_score = self.check_data_consistency(content)
        quality_score += consistency_score
        
        # 5. 중복 및 오류 검사 (10점)
        if not self.has_obvious_errors(content):
            quality_score += 10
        else:
            issues.append("명백한 오류 발견")
        
        return {
            'quality_score': min(quality_score, max_score),
            'max_score': max_score,
            'grade': self.get_quality_grade(quality_score),
            'issues': issues,
            'structured_data_count': len(structured_info)
        }
    
    def check_data_consistency(self, content: Dict) -> float:
        """데이터 일관성 검사"""
        score = 0
        
        # 기관명과 제목의 일관성 검사
        title = content.get('title', '')
        agency = content.get('agency', '')
        
        if agency and agency != 'N/A':
            # 제목에 기관명이나 관련 키워드가 있는지 확인
            agency_keywords = agency.split()
            if any(keyword in title for keyword in agency_keywords):
                score += 5
        
        # 날짜 형식의 일관성
        period = content.get('application_period', '')
        if period and re.search(r'\d{4}[\.\-]\d{1,2}[\.\-]\d{1,2}', period):
            score += 5
        
        # 연락처 정보의 유효성
        contact = content.get('contact_info', {})
        if isinstance(contact, dict):
            if contact.get('phone') and re.match(r'\d{2,3}-\d{3,4}-\d{4}', contact['phone']):
                score += 2.5
            if contact.get('email') and '@' in contact.get('email', ''):
                score += 2.5
        
        return score
    
    def has_obvious_errors(self, content: Dict) -> bool:
        """명백한 오류 검사"""
        title = content.get('title', '')
        
        # 너무 짧거나 긴 제목
        if len(title) < 3 or len(title) > 200:
            return True
        
        # 의미없는 반복 문자
        if re.search(r'(.)\1{5,}', title):  # 같은 문자 6번 이상 반복
            return True
        
        # HTML 태그 잔여물
        if '<' in title or '>' in title:
            return True
        
        # 특수문자만으로 구성
        if re.match(r'^[^가-힣a-zA-Z0-9\s]+$', title):
            return True
        
        return False
    
    def get_quality_grade(self, score: float) -> str:
        """품질 점수를 등급으로 변환"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B+'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C+'
        elif score >= 40:
            return 'C'
        else:
            return 'D'