#!/usr/bin/env python3
"""
🎯 스마트 키워드 기반 꿈풀이 수집 시스템
- 카테고리별 핵심 키워드 기반 타겟 수집
- 5분 간격으로 천천히 수집 (일일 5,000개 목표)
- 지능형 키워드 확장 및 카테고리 분류
"""

import requests
import json
import hashlib
import time
import random
import logging
import threading
import subprocess
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import urllib.parse
import os
from typing import List, Dict, Tuple

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/logs/smart_keyword_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SmartKeywordCollector:
    def __init__(self):
        self.collected_count = 0
        self.error_count = 0
        self.duplicate_count = 0
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 카테고리별 핵심 키워드 데이터베이스
        self.dream_keywords = {
            "동물": [
                "호랑이", "사자", "용", "뱀", "새", "개", "고양이", "말", "소", "돼지", 
                "원숭이", "코끼리", "곰", "늑대", "여우", "토끼", "쥐", "사슴", "기린",
                "물고기", "상어", "고래", "거북이", "개구리", "나비", "벌", "거미"
            ],
            "자연": [
                "산", "바다", "강", "호수", "나무", "꽃", "불", "물", "바람", "비",
                "눈", "번개", "무지개", "해", "달", "별", "구름", "폭풍", "지진"
            ],
            "음식": [
                "밥", "고기", "생선", "과일", "빵", "술", "물", "차", "커피", "케이크",
                "국수", "떡", "김치", "사탕", "초콜릿", "계란", "우유", "꿀"
            ],
            "사물": [
                "집", "자동차", "돈", "금", "은", "보석", "옷", "신발", "가방", "휴대폰",
                "컴퓨터", "책", "칼", "총", "거울", "시계", "열쇠", "다리", "문", "창문"
            ],
            "사람": [
                "가족", "엄마", "아빠", "형제", "자매", "친구", "연인", "아기", "노인",
                "선생님", "의사", "경찰", "군인", "도둑", "유명인", "죽은사람", "임신"
            ],
            "행동": [
                "날다", "달리다", "수영", "춤", "노래", "울다", "웃다", "싸우다", "도망",
                "숨다", "찾다", "잃다", "떨어지다", "올라가다", "내려가다", "결혼", "이혼"
            ],
            "신체": [
                "머리", "눈", "코", "입", "귀", "손", "발", "배", "가슴", "등", "피",
                "뼈", "치아", "머리카락", "상처", "병", "죽음", "치료", "수술"
            ],
            "장소": [
                "학교", "병원", "회사", "시장", "공원", "교회", "절", "공항", "기차역",
                "화장실", "목욕탕", "방", "부엌", "마당", "무덤", "감옥", "극장"
            ],
            "감정상황": [
                "무섭다", "기쁘다", "슬프다", "화나다", "놀라다", "걱정", "두려움",
                "사랑", "미움", "질투", "외로움", "행복", "고통", "평화", "스트레스"
            ]
        }
        
        # 키워드 풀 생성 (가중치 적용)
        self.weighted_keywords = self._create_weighted_keywords()
        
        # 수집 사이트 설정
        self.sites = {
            'unse2u': {
                'base_url': 'https://www.unse2u.co.kr',
                'search_pattern': 'search.php?keyword={}',
                'list_pattern': 'dreamview.php?c1=1&c2={}'
            }
        }

    def _create_weighted_keywords(self) -> List[Tuple[str, str, int]]:
        """카테고리별 키워드를 가중치와 함께 생성"""
        weighted = []
        
        # 카테고리별 가중치 (인기도/중요도 기준)
        category_weights = {
            "동물": 10,
            "사람": 9,
            "사물": 8,
            "자연": 7,
            "행동": 6,
            "감정상황": 5,
            "음식": 4,
            "장소": 4,
            "신체": 3
        }
        
        for category, keywords in self.dream_keywords.items():
            base_weight = category_weights.get(category, 1)
            for keyword in keywords:
                # 키워드별 개별 가중치 (길이, 인기도 고려)
                keyword_weight = base_weight + (5 - min(len(keyword), 5))
                weighted.append((keyword, category, keyword_weight))
        
        return sorted(weighted, key=lambda x: x[2], reverse=True)

    def select_target_keywords(self, count: int = 17) -> List[Tuple[str, str]]:
        """5분간 수집할 타겟 키워드 선택 (가중치 기반 랜덤)"""
        # 가중치 기반 선택
        total_weight = sum(item[2] for item in self.weighted_keywords)
        selected = []
        
        for _ in range(count):
            rand_weight = random.randint(1, total_weight)
            current_weight = 0
            
            for keyword, category, weight in self.weighted_keywords:
                current_weight += weight
                if current_weight >= rand_weight:
                    selected.append((keyword, category))
                    break
        
        # 중복 제거하면서 카테고리 다양성 보장
        unique_selected = []
        used_keywords = set()
        category_counts = {}
        
        for keyword, category in selected:
            if keyword not in used_keywords and category_counts.get(category, 0) < 3:
                unique_selected.append((keyword, category))
                used_keywords.add(keyword)
                category_counts[category] = category_counts.get(category, 0) + 1
                
                if len(unique_selected) >= count:
                    break
        
        return unique_selected

    def search_keyword_data(self, keyword: str, category: str) -> List[Dict]:
        """키워드 기반 꿈풀이 데이터 검색 및 수집"""
        results = []
        
        try:
            # 키워드별 매핑된 URL 범위 생성 (기존 동작하는 패턴 활용)
            # 키워드를 숫자 범위로 매핑하여 실제 존재하는 페이지 접근
            keyword_hash = abs(hash(keyword)) % 500 + 1  # 1~500 범위
            base_urls = []
            
            # 키워드 해시 기반으로 여러 URL 생성
            for i in range(3):  # 키워드당 3개 URL
                url_id = (keyword_hash + i * 50) % 500 + 1
                base_urls.append(f"https://www.unse2u.co.kr/dreamview.php?c1=1&c2={url_id}")
            
            for url in base_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        # 키워드가 포함된 내용인지 확인 후 수집
                        dream_data = self._extract_keyword_dream_content(url, keyword, category, response)
                        if dream_data:
                            results.append(dream_data)
                            logger.info(f"✅ 키워드 매칭: {keyword} → {url}")
                        
                    time.sleep(random.uniform(2, 4))  # 요청 간격
                    
                except Exception as e:
                    logger.debug(f"URL 접근 실패 ({url}): {e}")
                    continue
                
        except Exception as e:
            logger.error(f"키워드 '{keyword}' 검색 오류: {e}")
            with self.lock:
                self.error_count += 1
        
        return results

    def _extract_dream_links(self, soup: BeautifulSoup, keyword: str) -> List[str]:
        """검색 결과에서 꿈풀이 관련 링크 추출"""
        links = []
        
        # 다양한 링크 패턴 검색
        link_patterns = [
            'a[href*="dreamview"]',
            'a[href*="dream"]',
            'a[href*="interpretation"]',
            'a[href*="meaning"]'
        ]
        
        for pattern in link_patterns:
            for link in soup.select(pattern):
                href = link.get('href')
                if href and keyword in link.get_text().lower():
                    if href.startswith('/'):
                        href = 'https://www.unse2u.co.kr' + href
                    links.append(href)
                    
                if len(links) >= 5:  # 키워드당 최대 5개 링크
                    break
        
        return list(set(links))  # 중복 제거

    def _extract_keyword_dream_content(self, url: str, keyword: str, category: str, response) -> Dict:
        """키워드 기반 꿈풀이 페이지 내용 추출"""
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 제목과 내용 추출
            title = soup.title.string if soup.title else ""
            content = soup.get_text(separator=' ', strip=True)
            
            # 꿈풀이 관련 내용 확인
            dream_indicators = ['꿈', '해몽', '길몽', '흉몽', '태몽', '의미', '징조']
            if not any(indicator in content for indicator in dream_indicators):
                return None
            
            # 키워드 또는 관련 키워드가 포함되어 있는지 확인
            if not self._contains_relevant_keyword(content, keyword, category):
                return None
            
            # 구조화된 데이터 생성
            structured_data = {
                "url": url,
                "keyword": keyword,
                "category": category,
                "title": title[:200],
                "content": content[:2000],
                "content_length": len(content),
                "collection_method": "smart_keyword_mapping",
                "target_keyword": keyword,
                "target_category": category,
                "extracted_at": datetime.now().isoformat(),
                "quality_score": self._calculate_quality_score(content, keyword, category),
                "keyword_match_type": self._get_keyword_match_type(content, keyword, category)
            }
            
            return structured_data
            
        except Exception as e:
            logger.error(f"키워드 컨텐츠 추출 오류 ({url}): {e}")
            return None

    def _contains_relevant_keyword(self, content: str, target_keyword: str, category: str) -> bool:
        """관련 키워드 포함 여부 확인"""
        content_lower = content.lower()
        target_lower = target_keyword.lower()
        
        # 1. 정확한 키워드 매칭
        if target_lower in content_lower:
            return True
        
        # 2. 카테고리별 관련 키워드 매칭
        category_keywords = self.dream_keywords.get(category, [])
        related_matches = sum(1 for kw in category_keywords if kw.lower() in content_lower)
        
        # 같은 카테고리 키워드가 2개 이상 포함되면 관련성 있다고 판단
        if related_matches >= 2:
            return True
            
        # 3. 부분 매칭 (2글자 이상 키워드의 경우)
        if len(target_keyword) >= 2:
            if target_keyword[:2] in content or target_keyword[1:] in content:
                return True
        
        return False

    def _get_keyword_match_type(self, content: str, keyword: str, category: str) -> str:
        """키워드 매칭 타입 반환"""
        if keyword.lower() in content.lower():
            return "exact_match"
        
        category_keywords = self.dream_keywords.get(category, [])
        matches = [kw for kw in category_keywords if kw.lower() in content.lower()]
        
        if matches:
            return f"category_match({','.join(matches[:3])})"
        
        return "partial_match"

    def _extract_dream_content(self, url: str, keyword: str, category: str) -> Dict:
        """개별 꿈풀이 페이지에서 내용 추출"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 제목과 내용 추출
            title = soup.title.string if soup.title else ""
            content = soup.get_text(separator=' ', strip=True)
            
            # 꿈풀이 관련 내용 확인
            dream_indicators = ['꿈', '해몽', '길몽', '흉몽', '태몽', '의미', '징조']
            if not any(indicator in content for indicator in dream_indicators):
                return None
            
            # 키워드가 포함되어 있는지 확인
            if keyword not in content:
                return None
            
            # 구조화된 데이터 생성
            structured_data = {
                "url": url,
                "keyword": keyword,
                "category": category,
                "title": title[:200],
                "content": content[:2000],
                "content_length": len(content),
                "collection_method": "smart_keyword_search",
                "target_keyword": keyword,
                "target_category": category,
                "extracted_at": datetime.now().isoformat(),
                "quality_score": self._calculate_quality_score(content, keyword, category)
            }
            
            return structured_data
            
        except Exception as e:
            logger.error(f"컨텐츠 추출 오류 ({url}): {e}")
            return None

    def _calculate_quality_score(self, content: str, keyword: str, category: str) -> float:
        """내용 품질 점수 계산"""
        score = 0.5  # 기본 점수
        
        # 키워드 포함 점수
        if keyword in content:
            score += 0.2
            
        # 내용 길이 점수
        if len(content) > 500:
            score += 0.1
        if len(content) > 1000:
            score += 0.1
            
        # 꿈풀이 전문 용어 점수
        specialized_terms = ['길몽', '흉몽', '태몽', '해몽', '징조', '의미', '상징', '운세']
        found_terms = sum(1 for term in specialized_terms if term in content)
        score += min(found_terms * 0.05, 0.2)
        
        return min(score, 1.0)

    def save_to_database(self, dream_data: Dict) -> bool:
        """PostgreSQL에 안전하게 저장"""
        try:
            # 중복 확인용 해시
            content_hash = hashlib.md5(
                (dream_data['url'] + dream_data['content']).encode()
            ).hexdigest()
            
            # JSON 임시 파일 생성
            temp_file = f'/tmp/dream_data_{int(time.time())}_{random.randint(1000,9999)}.json'
            
            # JSONB 데이터 준비
            jsonb_data = {
                **dream_data,
                "content_hash": content_hash
            }
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(jsonb_data, f, ensure_ascii=False, indent=2)
            
            # PostgreSQL 저장
            query = f"""
            INSERT INTO dream_raw_collection (source_site, source_url, raw_content, content_hash, collection_status)
            SELECT 
                'smart_keyword_search',
                '{dream_data['url']}',
                content::jsonb,
                '{content_hash}',
                'collected'
            FROM (
                SELECT pg_read_file('{temp_file}') as content
            ) as file_data
            WHERE NOT EXISTS (
                SELECT 1 FROM dream_raw_collection WHERE content_hash = '{content_hash}'
            );
            """
            
            result = subprocess.run([
                'sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-c', query
            ], capture_output=True, text=True, timeout=30)
            
            # 임시 파일 정리
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            if result.returncode == 0:
                if "INSERT 0 1" in result.stdout:
                    with self.lock:
                        self.collected_count += 1
                    logger.info(f"✅ 저장 성공: {dream_data['keyword']} ({dream_data['category']})")
                    return True
                else:
                    with self.lock:
                        self.duplicate_count += 1
                    logger.debug(f"⚠️ 중복 데이터: {dream_data['keyword']}")
                    return True  # 중복도 성공으로 처리
            else:
                logger.error(f"❌ DB 저장 오류: {result.stderr}")
                with self.lock:
                    self.error_count += 1
                return False
                
        except Exception as e:
            logger.error(f"❌ 저장 프로세스 오류: {e}")
            with self.lock:
                self.error_count += 1
            return False

    def collect_batch(self, target_count: int = 17) -> Dict:
        """5분간 배치 수집 실행"""
        start_time = datetime.now()
        logger.info(f"🚀 배치 수집 시작: 목표 {target_count}개")
        
        # 타겟 키워드 선택
        target_keywords = self.select_target_keywords(target_count)
        logger.info(f"📋 선택된 키워드: {[f'{kw}({cat})' for kw, cat in target_keywords]}")
        
        # 병렬 수집 실행
        all_results = []
        with ThreadPoolExecutor(max_workers=3) as executor:  # 동시 3개로 제한
            futures = []
            
            for keyword, category in target_keywords:
                future = executor.submit(self.search_keyword_data, keyword, category)
                futures.append(future)
            
            for future in as_completed(futures):
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    logger.error(f"배치 수집 오류: {e}")
        
        # 데이터베이스 저장
        saved_count = 0
        for dream_data in all_results:
            if self.save_to_database(dream_data):
                saved_count += 1
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        # 결과 리포트
        result = {
            "collected": saved_count,
            "target": target_count,
            "elapsed_seconds": elapsed_time,
            "keywords_processed": len(target_keywords),
            "total_results": len(all_results),
            "success_rate": (saved_count / target_count * 100) if target_count > 0 else 0
        }
        
        logger.info(f"📊 배치 완료: {saved_count}/{target_count}개 수집 ({elapsed_time:.1f}초)")
        return result

def main():
    """메인 실행 함수"""
    collector = SmartKeywordCollector()
    
    # 단일 배치 테스트
    logger.info("🎯 스마트 키워드 수집기 테스트 시작")
    result = collector.collect_batch(17)  # 5분간 17개 목표
    
    logger.info(f"🏁 테스트 완료: {result}")

if __name__ == "__main__":
    main()