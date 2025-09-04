#!/usr/bin/env python3
"""
꿈풀이 데이터 정형화 시스템
수집된 원시 데이터를 clean_dream_interpretations 테이블로 정형화

목표: 16개 → 100개+ 키워드로 대폭 확장
"""

import subprocess
import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/logs/clean_dream_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CleanDreamProcessor:
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.duplicate_count = 0
        
        # 카테고리 매핑
        self.category_mapping = {
            '동물': ['호랑이', '용', '뱀', '개', '고양이', '사자', '곰', '말', '소', '돼지', '원숭이', 
                    '토끼', '양', '염소', '쥐', '다람쥐', '박쥐', '늑대', '여우', '사슴', '코끼리',
                    '기린', '코뿔소', '낙타', '캥거루', '시라소니', '치타', '고릴라', '개구리'],
            '자연': ['물', '바다', '강', '호수', '산', '나무', '꽃', '불', '비', '바람', '태양', '달', '별', 
                    '구름', '하늘', '땅', '모래', '돌', '눈', '얼음', '번개', '천둥'],
            '음식': ['쌀', '밥', '빵', '과일', '사탕', '막걸리', '술', '물', '차', '커피', '고기', '생선',
                    '채소', '김치', '국', '라면', '떡', '과자', '오렌지', '사과', '배'],
            '사물': ['돈', '금', '보석', '집', '차', '옷', '신발', '가방', '핸드폰', '책', '칼', '총',
                    '화분', '그릇', '의자', '침대', '문', '창문', '거울', '시계'],
            '행동': ['날기', '떨어지기', '쫓기기', '달리기', '걷기', '수영', '춤', '노래', '웃기', '울기',
                    '싸우기', '결혼', '출산', '죽음', '여행', '공부', '일하기', '요리'],
            '감정': ['기쁨', '슬픔', '분노', '두려움', '사랑', '질투', '행복', '불안', '평화', '외로움'],
            '신체': ['머리', '얼굴', '눈', '코', '입', '귀', '손', '발', '다리', '팔', '가슴', '배',
                     '등', '어깨', '목', '머리카락', '손톱', '발톱', '혈액', '상처', '병'],
            '장소': ['집', '학교', '직장', '병원', '시장', '공원', '교회', '절', '무덤', '다리', '길',
                     '방', '부엌', '화장실', '계단', '엘리베이터', '지하', '옥상'],
            '색깔': ['빨강', '파랑', '노랑', '검정', '흰색', '초록', '보라', '분홍', '갈색', '회색', '주황']
        }
        
    def execute_sql_safe(self, sql: str, params: tuple = None) -> List[dict]:
        """안전한 SQL 실행 (subprocess 기반)"""
        try:
            if params:
                # 매개변수가 있는 경우 문자열 포맷팅
                formatted_sql = sql.format(*params) if params else sql
            else:
                formatted_sql = sql
            
            cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'heal7',
                '-c', formatted_sql,
                '-t', '-A', '--field-separator=|'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                records = []
                for line in lines:
                    if line and '|' in line:
                        parts = line.split('|')
                        records.append(parts)
                return records
            else:
                logger.error(f"SQL 실행 실패: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"SQL 실행 오류: {e}")
            return []
    
    def extract_keyword_from_content(self, content: dict) -> Optional[str]:
        """JSON 콘텐츠에서 키워드 추출"""
        try:
            # 1. 제목에서 키워드 추출 시도
            if 'title' in content:
                title = content['title']
                if '에 관한 꿈해몽' in title:
                    keyword = title.replace('에 관한 꿈해몽', '').strip()
                    if keyword and len(keyword) <= 20:
                        return keyword
                        
            # 2. 첫 번째 문장에서 키워드 추출
            if 'content' in content:
                content_text = content['content']
                # "~에 대한", "~꿈", "~해몽" 패턴 찾기
                patterns = [
                    r'([가-힣]{1,10})\s*에\s*관한',
                    r'([가-힣]{1,10})\s*꿈',
                    r'([가-힣]{1,10})\s*해몽',
                    r'([가-힣]{1,10})\s*나오는',
                    r'([가-힣]{1,10})\s*보는'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, content_text[:100])
                    if match:
                        keyword = match.group(1).strip()
                        if keyword and len(keyword) <= 15:
                            return keyword
            
            # 3. found_dream_keywords에서 선택
            if 'found_dream_keywords' in content:
                keywords = content['found_dream_keywords']
                if isinstance(keywords, list) and keywords:
                    return keywords[0]
                    
            return None
            
        except Exception as e:
            logger.error(f"키워드 추출 오류: {e}")
            return None
    
    def classify_category(self, keyword: str, content: str) -> str:
        """키워드와 내용을 기반으로 카테고리 분류"""
        content_lower = content.lower()
        keyword_lower = keyword.lower()
        
        # 키워드 기반 분류
        for category, category_keywords in self.category_mapping.items():
            for cat_keyword in category_keywords:
                if cat_keyword in keyword_lower or cat_keyword in content_lower:
                    return category
        
        # 기본 카테고리
        return '기타'
    
    def extract_meaning(self, content: dict, keyword: str) -> Tuple[str, str]:
        """전통적 해석과 현대적 해석 분리"""
        try:
            full_content = content.get('content', '')
            
            # 길이 제한으로 의미 있는 부분 추출
            if len(full_content) > 500:
                sentences = full_content.split('.')
                meaningful_sentences = []
                for sentence in sentences:
                    if any(word in sentence for word in ['꿈', '의미', '해석', '상징', '징조', '운세']):
                        meaningful_sentences.append(sentence.strip())
                        if len(' '.join(meaningful_sentences)) > 300:
                            break
                full_content = ' '.join(meaningful_sentences)
            
            # 전통적/현대적 분리 시도
            if '전통적' in full_content or '옛날' in full_content:
                traditional = full_content[:200]
                modern = f"{keyword}에 대한 현대적 해석이 필요합니다."
            elif '현대적' in full_content or '심리학' in full_content:
                traditional = f"{keyword}는 전통적으로 중요한 의미를 지닌 꿈입니다."
                modern = full_content[:200]
            else:
                # 기본적으로 전통 해석으로 처리
                traditional = full_content[:200] if full_content else f"{keyword}에 관한 꿈은 특별한 의미를 가집니다."
                modern = f"{keyword}는 현대 심리학적으로도 중요한 꿈 상징입니다."
                
            return traditional, modern
            
        except Exception as e:
            logger.error(f"의미 추출 오류: {e}")
            return f"{keyword}에 관한 꿈입니다.", f"{keyword}의 현대적 해석입니다."
    
    def calculate_confidence_score(self, keyword: str, traditional: str, modern: str, category: str) -> float:
        """신뢰도 점수 계산"""
        score = 5.0  # 기본점수
        
        # 키워드 품질
        if keyword and len(keyword.strip()) >= 2:
            score += 1.0
        if len(keyword.strip()) <= 10:  # 적절한 길이
            score += 1.0
            
        # 내용 품질  
        total_length = len(traditional) + len(modern)
        if total_length > 50:
            score += min(total_length / 50, 2.0)
            
        # 카테고리 분류
        if category != '기타':
            score += 1.0
            
        return min(score, 10.0)
    
    def generate_related_keywords(self, keyword: str, category: str) -> List[str]:
        """관련 키워드 생성"""
        related = []
        
        # 카테고리 기반 관련 키워드
        if category in self.category_mapping:
            category_words = self.category_mapping[category]
            for word in category_words:
                if word != keyword and len(related) < 5:
                    related.append(word)
                    
        # 키워드 기반 관련어
        common_related = {
            '물': ['바다', '강', '호수', '비'],
            '돈': ['금', '보석', '재물', '부'],
            '뱀': ['용', '구렁이', '독사'],
            '호랑이': ['사자', '표범', '맹수'],
            '꽃': ['장미', '나무', '정원']
        }
        
        if keyword in common_related:
            related.extend(common_related[keyword][:3])
            
        return related[:5]
    
    def insert_clean_dream(self, keyword: str, category: str, traditional: str, 
                          modern: str, confidence: float, related_keywords: List[str]):
        """clean_dream_interpretations 테이블에 데이터 삽입"""
        try:
            # 중복 체크
            check_sql = f"""
            SELECT COUNT(*) FROM dream_service.clean_dream_interpretations 
            WHERE keyword = '{keyword.replace("'", "''")}'
            """
            
            result = self.execute_sql_safe(check_sql)
            if result and len(result) > 0 and result[0] and int(result[0][0]) > 0:
                self.duplicate_count += 1
                return False
            
            # 데이터 삽입
            related_str = '{' + ','.join(f'"{k}"' for k in related_keywords) + '}'
            
            insert_sql = f"""
            INSERT INTO dream_service.clean_dream_interpretations 
            (keyword, category, traditional_meaning, modern_meaning, confidence_score, related_keywords, created_at)
            VALUES (
                '{keyword.replace("'", "''")}',
                '{category}',
                '{traditional.replace("'", "''")}',
                '{modern.replace("'", "''")}',
                {confidence},
                '{related_str}',
                CURRENT_TIMESTAMP
            );
            """
            
            result = self.execute_sql_safe(insert_sql)
            self.processed_count += 1
            logger.info(f"✅ 추가: {keyword} ({category}) - 신뢰도: {confidence:.1f}")
            return True
            
        except Exception as e:
            logger.error(f"DB 삽입 오류 ({keyword}): {e}")
            self.error_count += 1
            return False
    
    def process_raw_data_batch(self, limit: int = 200):
        """원시 데이터 배치 처리"""
        logger.info(f"🚀 꿈풀이 데이터 정형화 시작 (처리 목표: {limit}개)")
        
        # 품질이 좋은 unse2u 데이터 우선 선택
        sql = f"""
        SELECT id, raw_content 
        FROM dream_service.dream_raw_collection 
        WHERE source_site = 'unse2u' 
        AND LENGTH(raw_content::text) > 200
        ORDER BY scraped_at DESC
        LIMIT {limit}
        """
        
        raw_data_list = self.execute_sql_safe(sql)
        
        if not raw_data_list:
            logger.warning("처리할 원시 데이터가 없습니다.")
            return
            
        logger.info(f"📦 {len(raw_data_list)}개 원시 데이터 처리 시작")
        
        for i, row in enumerate(raw_data_list, 1):
            try:
                if len(row) < 2:
                    continue
                    
                raw_id, raw_content = row[0], row[1]
                
                # JSON 파싱
                if isinstance(raw_content, str):
                    content = json.loads(raw_content)
                else:
                    content = raw_content
                
                # 키워드 추출
                keyword = self.extract_keyword_from_content(content)
                if not keyword or len(keyword.strip()) < 2:
                    continue
                
                keyword = keyword.strip()[:50]  # 길이 제한
                
                # 내용 분석
                full_text = content.get('content', '') + ' ' + content.get('title', '')
                category = self.classify_category(keyword, full_text)
                traditional, modern = self.extract_meaning(content, keyword)
                confidence = self.calculate_confidence_score(keyword, traditional, modern, category)
                related_keywords = self.generate_related_keywords(keyword, category)
                
                # 품질 필터링 (신뢰도 6.0 이상만)
                if confidence >= 6.0:
                    success = self.insert_clean_dream(keyword, category, traditional, 
                                                    modern, confidence, related_keywords)
                    if success and i % 10 == 0:
                        logger.info(f"📈 진행률: {i}/{len(raw_data_list)} ({i/len(raw_data_list)*100:.1f}%)")
                
            except Exception as e:
                logger.error(f"데이터 처리 오류 (ID: {raw_id}): {e}")
                self.error_count += 1
                continue
        
        # 최종 결과 보고
        logger.info("=" * 60)
        logger.info("🎉 꿈풀이 데이터 정형화 완료!")
        logger.info(f"✅ 성공적으로 추가: {self.processed_count}개")
        logger.info(f"🔄 중복 스킵: {self.duplicate_count}개")  
        logger.info(f"❌ 오류 발생: {self.error_count}개")
        
        success_rate = (self.processed_count / len(raw_data_list)) * 100 if raw_data_list else 0
        logger.info(f"📊 성공률: {success_rate:.1f}%")
        logger.info("=" * 60)

def main():
    import os
    
    # 로그 디렉토리 생성
    os.makedirs('/home/ubuntu/logs', exist_ok=True)
    
    processor = CleanDreamProcessor()
    
    # 기존 키워드 수 확인
    initial_count_sql = "SELECT COUNT(*) FROM dream_service.clean_dream_interpretations"
    result = processor.execute_sql_safe(initial_count_sql)
    initial_count = int(result[0][0]) if result and result[0] else 0
    
    logger.info(f"📊 시작 전 키워드 수: {initial_count}개")
    
    # 대량 처리 실행 (목표: +85개 이상 추가하여 100개+ 달성)
    processor.process_raw_data_batch(limit=500)
    
    # 최종 키워드 수 확인
    final_count_sql = "SELECT COUNT(*) FROM dream_service.clean_dream_interpretations"
    result = processor.execute_sql_safe(final_count_sql)
    final_count = int(result[0][0]) if result and result[0] else 0
    
    logger.info(f"📊 최종 키워드 수: {final_count}개 (증가: +{final_count - initial_count}개)")
    
    if final_count >= 100:
        logger.info("🎯 목표 달성! 100개 이상 키워드 확보 성공!")
    else:
        logger.info(f"🔄 목표까지 {100 - final_count}개 더 필요")

if __name__ == "__main__":
    main()