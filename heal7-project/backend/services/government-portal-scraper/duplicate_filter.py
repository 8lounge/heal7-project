#!/usr/bin/env python3
"""
중복 데이터 필터링 시스템
해시 기반 + 유사도 기반 중복 검출
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from difflib import SequenceMatcher
import re

logger = logging.getLogger(__name__)

@dataclass
class DuplicateDetectionResult:
    """중복 검출 결과"""
    is_duplicate: bool
    confidence_score: float  # 0.0-1.0
    duplicate_type: str  # 'exact', 'hash', 'content_similarity', 'title_similarity'
    original_record_id: Optional[str] = None
    similarity_details: Dict = field(default_factory=dict)

class AdvancedDuplicateFilter:
    """고급 중복 데이터 필터"""
    
    def __init__(self):
        # 해시 캐시 (메모리 기반)
        self.content_hashes: Set[str] = set()
        self.title_hashes: Set[str] = set()
        
        # 유사도 검사 설정
        self.title_similarity_threshold = 0.85
        self.content_similarity_threshold = 0.80
        self.url_similarity_threshold = 0.95
        
        # 정규화 패턴
        self.normalization_patterns = [
            (r'\s+', ' '),  # 다중 공백을 단일 공백으로
            (r'[^\w\s가-힣]', ''),  # 특수문자 제거 (한글, 영문, 숫자만)
            (r'^\s+|\s+$', ''),  # 앞뒤 공백 제거
        ]
        
        # 무시할 단어들 (중복 판정 시 제외)
        self.stop_words = {
            '공고', '사업', '지원', '신청', '모집', '안내', '공지',
            '년도', '월', '일', '시행', '접수', '마감', '종료'
        }
        
        logger.info("🔍 고급 중복 데이터 필터 초기화 완료")
    
    async def detect_duplicate(self, new_record: Dict, existing_records: List[Dict] = None) -> DuplicateDetectionResult:
        """
        종합적인 중복 검출
        
        Args:
            new_record: 검사할 신규 레코드
            existing_records: 기존 레코드들 (선택적)
        
        Returns:
            중복 검출 결과
        """
        # 1단계: 완전 일치 해시 검사
        exact_hash_result = await self._check_exact_hash_duplicate(new_record)
        if exact_hash_result.is_duplicate:
            return exact_hash_result
        
        # 2단계: 제목 해시 검사
        title_hash_result = await self._check_title_hash_duplicate(new_record)
        if title_hash_result.is_duplicate:
            return title_hash_result
        
        # 3단계: 내용 유사도 검사
        if existing_records:
            similarity_result = await self._check_content_similarity_duplicate(new_record, existing_records)
            if similarity_result.is_duplicate:
                return similarity_result
        
        # 4단계: URL 유사도 검사
        if existing_records:
            url_similarity_result = await self._check_url_similarity_duplicate(new_record, existing_records)
            if url_similarity_result.is_duplicate:
                return url_similarity_result
        
        # 중복이 아님
        return DuplicateDetectionResult(
            is_duplicate=False,
            confidence_score=0.0,
            duplicate_type='none'
        )
    
    async def _check_exact_hash_duplicate(self, record: Dict) -> DuplicateDetectionResult:
        """완전 일치 해시 중복 검사"""
        content_hash = self._generate_content_hash(record)
        
        if content_hash in self.content_hashes:
            return DuplicateDetectionResult(
                is_duplicate=True,
                confidence_score=1.0,
                duplicate_type='exact',
                similarity_details={'content_hash': content_hash}
            )
        
        # 새로운 해시 등록
        self.content_hashes.add(content_hash)
        
        return DuplicateDetectionResult(
            is_duplicate=False,
            confidence_score=0.0,
            duplicate_type='none'
        )
    
    async def _check_title_hash_duplicate(self, record: Dict) -> DuplicateDetectionResult:
        """제목 해시 중복 검사"""
        title = record.get('title', '')
        if not title:
            return DuplicateDetectionResult(is_duplicate=False, confidence_score=0.0, duplicate_type='none')
        
        normalized_title = self._normalize_text(title)
        title_hash = hashlib.sha256(normalized_title.encode()).hexdigest()[:16]
        
        if title_hash in self.title_hashes:
            return DuplicateDetectionResult(
                is_duplicate=True,
                confidence_score=0.9,
                duplicate_type='title_hash',
                similarity_details={
                    'title_hash': title_hash,
                    'normalized_title': normalized_title
                }
            )
        
        # 새로운 제목 해시 등록
        self.title_hashes.add(title_hash)
        
        return DuplicateDetectionResult(
            is_duplicate=False,
            confidence_score=0.0,
            duplicate_type='none'
        )
    
    async def _check_content_similarity_duplicate(self, new_record: Dict, existing_records: List[Dict]) -> DuplicateDetectionResult:
        """내용 유사도 기반 중복 검사"""
        new_title = self._normalize_text(new_record.get('title', ''))
        new_content = self._normalize_text(new_record.get('description', ''))
        
        if not new_title:
            return DuplicateDetectionResult(is_duplicate=False, confidence_score=0.0, duplicate_type='none')
        
        max_similarity = 0.0
        best_match_record = None
        
        for existing_record in existing_records:
            existing_title = self._normalize_text(existing_record.get('title', ''))
            existing_content = self._normalize_text(existing_record.get('description', ''))
            
            # 제목 유사도
            title_similarity = SequenceMatcher(None, new_title, existing_title).ratio()
            
            # 내용 유사도 (있는 경우)
            content_similarity = 0.0
            if new_content and existing_content:
                content_similarity = SequenceMatcher(None, new_content, existing_content).ratio()
            
            # 종합 유사도 (제목 가중치 70%, 내용 30%)
            overall_similarity = title_similarity * 0.7 + content_similarity * 0.3
            
            if overall_similarity > max_similarity:
                max_similarity = overall_similarity
                best_match_record = existing_record
        
        # 임계값 이상이면 중복으로 판정
        if max_similarity >= self.content_similarity_threshold:
            return DuplicateDetectionResult(
                is_duplicate=True,
                confidence_score=max_similarity,
                duplicate_type='content_similarity',
                original_record_id=best_match_record.get('id') if best_match_record else None,
                similarity_details={
                    'similarity_score': max_similarity,
                    'threshold': self.content_similarity_threshold,
                    'matching_title': best_match_record.get('title') if best_match_record else None
                }
            )
        
        return DuplicateDetectionResult(
            is_duplicate=False,
            confidence_score=max_similarity,
            duplicate_type='none'
        )
    
    async def _check_url_similarity_duplicate(self, new_record: Dict, existing_records: List[Dict]) -> DuplicateDetectionResult:
        """URL 유사도 기반 중복 검사"""
        new_url = new_record.get('detail_url', '')
        if not new_url:
            return DuplicateDetectionResult(is_duplicate=False, confidence_score=0.0, duplicate_type='none')
        
        normalized_new_url = self._normalize_url(new_url)
        
        for existing_record in existing_records:
            existing_url = existing_record.get('detail_url', '')
            if not existing_url:
                continue
            
            normalized_existing_url = self._normalize_url(existing_url)
            url_similarity = SequenceMatcher(None, normalized_new_url, normalized_existing_url).ratio()
            
            if url_similarity >= self.url_similarity_threshold:
                return DuplicateDetectionResult(
                    is_duplicate=True,
                    confidence_score=url_similarity,
                    duplicate_type='url_similarity',
                    original_record_id=existing_record.get('id'),
                    similarity_details={
                        'url_similarity': url_similarity,
                        'new_url': normalized_new_url,
                        'existing_url': normalized_existing_url
                    }
                )
        
        return DuplicateDetectionResult(
            is_duplicate=False,
            confidence_score=0.0,
            duplicate_type='none'
        )
    
    def _generate_content_hash(self, record: Dict) -> str:
        """레코드의 종합 해시 생성"""
        # 핵심 필드들을 조합해서 해시 생성
        key_fields = ['title', 'implementing_agency', 'agency', 'application_period', 'detail_url']
        content_parts = []
        
        for field in key_fields:
            value = record.get(field, '')
            if value and value != 'N/A':
                content_parts.append(self._normalize_text(str(value)))
        
        combined_content = '|'.join(content_parts)
        return hashlib.sha256(combined_content.encode()).hexdigest()[:32]
    
    def _normalize_text(self, text: str) -> str:
        """텍스트 정규화"""
        if not text:
            return ''
        
        text = str(text).lower()
        
        # 정규화 패턴 적용
        for pattern, replacement in self.normalization_patterns:
            text = re.sub(pattern, replacement, text)
        
        # 불용어 제거
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        
        return ' '.join(filtered_words)
    
    def _normalize_url(self, url: str) -> str:
        """URL 정규화"""
        if not url:
            return ''
        
        # URL에서 쿼리 파라미터 제거
        url = url.split('?')[0]
        url = url.split('#')[0]
        
        # 프로토콜 제거
        url = re.sub(r'^https?://', '', url)
        
        # 끝 슬래시 제거
        url = url.rstrip('/')
        
        return url.lower()
    
    def add_processed_record(self, record: Dict):
        """처리된 레코드를 캐시에 추가"""
        content_hash = self._generate_content_hash(record)
        self.content_hashes.add(content_hash)
        
        title = record.get('title', '')
        if title:
            normalized_title = self._normalize_text(title)
            title_hash = hashlib.sha256(normalized_title.encode()).hexdigest()[:16]
            self.title_hashes.add(title_hash)
    
    def get_filter_statistics(self) -> Dict:
        """필터 통계 조회"""
        return {
            'content_hashes_count': len(self.content_hashes),
            'title_hashes_count': len(self.title_hashes),
            'thresholds': {
                'title_similarity': self.title_similarity_threshold,
                'content_similarity': self.content_similarity_threshold,
                'url_similarity': self.url_similarity_threshold
            },
            'stop_words_count': len(self.stop_words)
        }
    
    def clear_cache(self):
        """캐시 초기화"""
        self.content_hashes.clear()
        self.title_hashes.clear()
        logger.info("🧹 중복 필터 캐시 초기화 완료")

# 전역 중복 필터 인스턴스
duplicate_filter = AdvancedDuplicateFilter()