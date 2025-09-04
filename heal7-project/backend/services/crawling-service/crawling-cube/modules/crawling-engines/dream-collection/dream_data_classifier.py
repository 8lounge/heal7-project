#!/usr/bin/env python3
"""
꿈풀이 데이터 순차적 분류 시스템
수집된 원시 JSONB 데이터를 체계적으로 분류하여 구조화된 테이블로 이관

전략: 무분별 수집 → AI 기반 체계적 분류 → 최종 DB 이관
"""

import psycopg2
import json
import re
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
# import openai  # AI 기능 사용시 주석 해제
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass 
class ProcessedDreamData:
    """처리된 꿈풀이 데이터 구조"""
    keyword: str
    category: str
    subcategory: str
    emoji: str
    traditional_interpretation: str
    modern_interpretation: str
    psychology_interpretation: str
    keywords: List[str]
    related_dreams: List[str]
    lucky_numbers: List[int]
    mood: str  # positive, neutral, negative, warning
    frequency: int
    tags: List[str]
    variations: List[str]
    confidence_score: float
    source_sites: List[str]

class DreamDataClassifier:
    """꿈풀이 데이터 분류기"""
    
    def __init__(self, db_config: Dict[str, str], use_ai: bool = False):
        self.db_config = db_config
        self.use_ai = use_ai
        self.processed_count = 0
        self.error_count = 0
        
        # 카테고리 매핑
        self.category_mapping = {
            '동물': ['동물', '짐승', '새', '물고기', '곤충', '뱀', '호랑이', '용', '개', '고양이'],
            '자연': ['물', '바다', '산', '나무', '꽃', '불', '비', '바람', '태양', '달'],
            '사람': ['가족', '친구', '연인', '아이', '어른', '죽은사람', '유명인'],
            '사물': ['집', '돈', '차', '옷', '음식', '책', '핸드폰', '컴퓨터'],
            '행동': ['날기', '떨어지기', '쫓기기', '싸우기', '결혼', '출산', '죽음'],
            '감정': ['기쁨', '슬픔', '분노', '두려움', '사랑', '질투'],
            '신체': ['머리', '눈', '손', '발', '혈액', '상처', '병'],
            '영적': ['신', '부처', '귀신', '천사', '지옥', '천국', '절'],
            '장소': ['집', '학교', '직장', '병원', '공원', '바다', '산'],
            '색깔': ['빨강', '파랑', '노랑', '검정', '흰색', '초록']
        }
        
        # 감정 키워드
        self.mood_keywords = {
            'positive': ['좋은', '행운', '길몽', '성공', '발전', '기쁨', '축복', '번영'],
            'negative': ['나쁜', '불운', '흉몽', '실패', '손실', '슬픔', '재앙', '위험'],
            'warning': ['주의', '경고', '조심', '위험', '신중', '각성'],
            'neutral': ['평범한', '일반적인', '보통의', '중간', '평상']
        }
    
    def get_connection(self):
        """DB 연결"""
        # postgres 사용자로 직접 연결
        import subprocess
        import os
        
        # postgres 사용자 권한으로 DB 연결을 위해 subprocess 활용
        return psycopg2.connect(
            host=self.db_config['host'],
            database=self.db_config['database'],
            user='postgres',
            port=self.db_config['port']
        )
    
    def extract_keywords_from_text(self, text: str) -> List[str]:
        """텍스트에서 키워드 추출"""
        if not text:
            return []
        
        # 한국어 명사 추출 (간단한 패턴 매칭)
        korean_words = re.findall(r'[가-힣]{2,}', text)
        
        # 꿈풀이 관련 핵심 키워드 필터링
        dream_related = []
        for word in korean_words:
            if any(category_word in word for category_list in self.category_mapping.values() 
                   for category_word in category_list):
                dream_related.append(word)
            elif any(keyword in word for mood_list in self.mood_keywords.values() 
                     for keyword in mood_list):
                dream_related.append(word)
        
        return list(set(dream_related))[:10]  # 상위 10개
    
    def classify_category(self, text: str, keywords: List[str]) -> Tuple[str, str]:
        """카테고리 분류"""
        text_lower = text.lower()
        
        # 키워드 기반 분류
        for category, category_keywords in self.category_mapping.items():
            for keyword in category_keywords:
                if keyword in text_lower or any(keyword in kw for kw in keywords):
                    return category, keyword
        
        # 기본값
        return '기타', ''
    
    def determine_mood(self, text: str) -> str:
        """감정/운세 분류"""
        text_lower = text.lower()
        
        mood_scores = {}
        for mood, mood_keywords in self.mood_keywords.items():
            score = sum(1 for keyword in mood_keywords if keyword in text_lower)
            if score > 0:
                mood_scores[mood] = score
        
        if mood_scores:
            return max(mood_scores, key=mood_scores.get)
        return 'neutral'
    
    def generate_emoji(self, category: str, keyword: str) -> str:
        """카테고리별 이모지 생성"""
        emoji_map = {
            '동물': '🐾', '자연': '🌿', '사람': '👥', '사물': '🏺',
            '행동': '🏃‍♂️', '감정': '😊', '신체': '👤', '영적': '🔮',
            '장소': '🏠', '색깔': '🎨'
        }
        
        return emoji_map.get(category, '✨')
    
    def generate_lucky_numbers(self, text: str) -> List[int]:
        """행운의 숫자 생성 (텍스트 해시 기반)"""
        hash_value = hashlib.md5(text.encode('utf-8')).hexdigest()
        numbers = []
        for i in range(0, len(hash_value), 2):
            num = int(hash_value[i:i+2], 16) % 45 + 1  # 1-45 범위
            numbers.append(num)
        return sorted(list(set(numbers)))[:6]  # 상위 6개
    
    def calculate_confidence_score(self, raw_data: Dict[str, Any]) -> float:
        """신뢰도 점수 계산"""
        score = 5.0  # 기본 점수
        
        # 데이터 완성도
        field_count = len([v for v in raw_data.values() if v and str(v).strip()])
        score += min(field_count * 0.3, 2.0)
        
        # 텍스트 길이
        total_text = ' '.join(str(v) for v in raw_data.values() if v)
        if len(total_text) > 100:
            score += min(len(total_text) / 100, 2.0)
        
        # 한국어 비율
        korean_ratio = len(re.findall(r'[가-힣]', total_text)) / len(total_text) if total_text else 0
        score += korean_ratio * 1.0
        
        return min(score, 10.0)
    
    def process_raw_item(self, raw_item: Tuple) -> Optional[ProcessedDreamData]:
        """개별 원시 데이터 처리"""
        try:
            raw_id, source_site, raw_content, quality_hints = raw_item
            
            # JSON 데이터 파싱
            if isinstance(raw_content, str):
                content = json.loads(raw_content)
            else:
                content = raw_content
            
            # 주요 텍스트 추출
            main_text = ""
            keyword_candidates = []
            
            for key, value in content.items():
                if isinstance(value, str) and value.strip():
                    main_text += value + " "
                    if key in ['title', 'keyword', 'name', 'subject']:
                        keyword_candidates.append(value.strip())
                elif isinstance(value, list):
                    main_text += " ".join(str(v) for v in value) + " "
            
            if not main_text.strip():
                return None
            
            # 키워드 결정
            if keyword_candidates:
                main_keyword = keyword_candidates[0][:50]  # 첫 번째 후보, 최대 50자
            else:
                # 첫 번째 문장에서 추출
                sentences = main_text.split('.')
                main_keyword = sentences[0][:30].strip() if sentences else "꿈"
            
            # 분류 작업
            keywords = self.extract_keywords_from_text(main_text)
            category, subcategory = self.classify_category(main_text, keywords)
            mood = self.determine_mood(main_text)
            emoji = self.generate_emoji(category, main_keyword)
            lucky_numbers = self.generate_lucky_numbers(main_text)
            
            # 해석 분리 시도
            traditional = content.get('traditional', content.get('traditional_meaning', ''))
            modern = content.get('modern', content.get('modern_meaning', ''))
            
            # 없으면 main_text에서 분리 시도
            if not traditional and not modern:
                if '전통적으로' in main_text or '옛날부터' in main_text:
                    traditional = main_text[:200]
                    modern = "현대적 관점에서 재해석이 필요한 꿈입니다."
                else:
                    traditional = "전통적 해석이 필요한 꿈입니다."
                    modern = main_text[:200]
            
            # 신뢰도 계산
            confidence = self.calculate_confidence_score(content)
            
            return ProcessedDreamData(
                keyword=main_keyword,
                category=category,
                subcategory=subcategory,
                emoji=emoji,
                traditional_interpretation=traditional[:500],
                modern_interpretation=modern[:500], 
                psychology_interpretation=f"{main_keyword}는 무의식의 메시지를 담고 있습니다.",
                keywords=keywords,
                related_dreams=[],
                lucky_numbers=lucky_numbers,
                mood=mood,
                frequency=1,
                tags=[category, mood],
                variations=[main_keyword],
                confidence_score=confidence,
                source_sites=[source_site]
            )
            
        except Exception as e:
            logger.error(f"처리 오류 (ID: {raw_item[0]}): {e}")
            self.error_count += 1
            return None
    
    def save_processed_data(self, processed_data: ProcessedDreamData, original_id: int):
        """처리된 데이터를 최종 테이블에 저장"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                
                # dream_interpretations 테이블이 있는지 확인, 없으면 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_interpretations (
                        id BIGSERIAL PRIMARY KEY,
                        keyword VARCHAR(200) NOT NULL,
                        keyword_variants TEXT[],
                        category_id INTEGER,
                        subcategory_id INTEGER,
                        traditional_meaning TEXT,
                        modern_meaning TEXT,
                        psychological_meaning TEXT,
                        spiritual_meaning TEXT,
                        dream_type VARCHAR(50),
                        fortune_aspect VARCHAR(20),
                        confidence_score DECIMAL(3,2) DEFAULT 0.5,
                        related_keywords TEXT[],
                        lucky_numbers INTEGER[],
                        lucky_colors VARCHAR(100)[],
                        compatible_dreams TEXT[],
                        conflicting_dreams TEXT[],
                        search_frequency INTEGER DEFAULT 0,
                        accuracy_rating DECIMAL(3,2) DEFAULT 0.0,
                        source_reliability INTEGER DEFAULT 1,
                        data_source VARCHAR(200),
                        seasonal_relevance VARCHAR(20)[],
                        cultural_context VARCHAR(100),
                        gender_specific BOOLEAN DEFAULT false,
                        age_group VARCHAR(50),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        created_by VARCHAR(100),
                        last_verified_at TIMESTAMP WITH TIME ZONE
                    )
                """)
                
                # 데이터 삽입
                insert_sql = """
                INSERT INTO dream_service.dream_interpretations 
                (keyword, traditional_meaning, modern_meaning, psychological_meaning,
                 fortune_aspect, confidence_score, related_keywords, lucky_numbers,
                 data_source, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """
                
                cur.execute(insert_sql, (
                    processed_data.keyword,
                    processed_data.traditional_interpretation,
                    processed_data.modern_interpretation,
                    processed_data.psychology_interpretation,
                    processed_data.mood,
                    processed_data.confidence_score,
                    processed_data.keywords,
                    processed_data.lucky_numbers,
                    ','.join(processed_data.source_sites),
                    'dream_classifier_v2'
                ))
                
                final_id = cur.fetchone()[0]
                
                # 원본 raw_collection 업데이트
                cur.execute("""
                    UPDATE dream_service.dream_raw_collection 
                    SET processing_status = 'completed',
                        processed_at = CURRENT_TIMESTAMP,
                        processing_notes = %s
                    WHERE id = %s
                """, (f'Processed to dream_interpretations id: {final_id}', original_id))
                
                conn.commit()
                self.processed_count += 1
                
        except Exception as e:
            logger.error(f"저장 오류: {e}")
            self.error_count += 1
    
    def get_pending_items(self, limit: int = 100) -> List[Tuple]:
        """처리 대기 중인 원시 데이터 가져오기"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, source_site, raw_content, quality_hints
                FROM dream_service.dream_raw_collection 
                WHERE processing_status = 'pending'
                AND (quality_hints->>'estimated_quality')::float >= 5.0
                ORDER BY (quality_hints->>'estimated_quality')::float DESC
                LIMIT %s
            """, (limit,))
            
            return cur.fetchall()
    
    def run_classification_batch(self, batch_size: int = 50):
        """배치 분류 실행"""
        logger.info(f"🤖 꿈풀이 데이터 분류 시작 (배치 크기: {batch_size})")
        
        while True:
            # 처리 대기 데이터 가져오기
            pending_items = self.get_pending_items(batch_size)
            
            if not pending_items:
                logger.info("✅ 처리할 데이터가 없습니다.")
                break
            
            logger.info(f"📦 {len(pending_items)}개 항목 처리 중...")
            
            # 병렬 처리
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    executor.submit(self.process_raw_item, item): item[0] 
                    for item in pending_items
                }
                
                for future in as_completed(futures):
                    original_id = futures[future]
                    try:
                        processed_data = future.result()
                        if processed_data:
                            self.save_processed_data(processed_data, original_id)
                            if self.processed_count % 10 == 0:
                                logger.info(f"✨ 진행률: {self.processed_count}개 완료")
                    except Exception as e:
                        logger.error(f"배치 처리 오류 (ID: {original_id}): {e}")
            
            time.sleep(1)  # 부하 방지
        
        logger.info(f"🎉 분류 완료! 총 처리: {self.processed_count}개, 에러: {self.error_count}개")
    
    def get_classification_stats(self) -> Dict[str, Any]:
        """분류 통계 반환"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            # 처리 상태별 통계
            cur.execute("""
                SELECT processing_status, COUNT(*) 
                FROM dream_service.dream_raw_collection 
                GROUP BY processing_status
            """)
            status_stats = dict(cur.fetchall())
            
            # 최종 테이블 통계
            cur.execute("SELECT COUNT(*) FROM dream_service.dream_interpretations")
            final_count = cur.fetchone()[0] if cur.rowcount > 0 else 0
            
            return {
                'raw_data_stats': status_stats,
                'final_interpretations': final_count,
                'processed_count': self.processed_count,
                'error_count': self.error_count,
                'updated_at': datetime.now().isoformat()
            }

def main():
    parser = argparse.ArgumentParser(description='꿈풀이 데이터 분류기')
    parser.add_argument('--batch-size', type=int, default=50, help='배치 크기')
    parser.add_argument('--stats', action='store_true', help='통계만 표시')
    parser.add_argument('--db-name', default='heal7', help='데이터베이스 이름')
    
    args = parser.parse_args()
    
    # DB 설정 - postgres 사용자로 연결
    db_config = {
        'host': 'localhost',
        'database': args.db_name,
        'user': 'postgres', 
        'password': '',
        'port': 5432
    }
    
    classifier = DreamDataClassifier(db_config)
    
    try:
        if args.stats:
            stats = classifier.get_classification_stats()
            print("📊 분류 통계:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            classifier.run_classification_batch(args.batch_size)
            
    except Exception as e:
        logger.error(f"실행 오류: {e}")

if __name__ == "__main__":
    main()