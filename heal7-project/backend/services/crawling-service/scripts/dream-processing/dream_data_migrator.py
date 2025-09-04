#!/usr/bin/env python3
"""
HEAL7 꿈풀이 데이터 정형화 및 이전 시스템
3,557개 dream_interpretations → clean_dream_interpretations 정형화 이전
"""

import asyncio
import asyncpg
import logging
import re
from typing import List, Dict, Set, Tuple
from datetime import datetime
import json

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/dream_migrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DreamDataMigrator:
    def __init__(self):
        self.conn = None
        self.category_mapping = {
            '물': '자연',
            '바다': '자연',
            '강': '자연',
            '호수': '자연',
            '산': '자연',
            '나무': '자연',
            '꽃': '자연',
            '해': '자연',
            '달': '자연',
            '별': '자연',
            '눈': '자연',
            '비': '자연',
            '바람': '자연',
            '돈': '재물',
            '금': '재물',
            '보석': '재물',
            '통장': '재물',
            '뱀': '동물',
            '호랑이': '동물',
            '용': '동물',
            '새': '동물',
            '개': '동물',
            '고양이': '동물',
            '죽음': '생사',
            '살인': '생사',
            '죽이다': '생사',
            '병원': '건강',
            '의사': '건강',
            '약': '건강',
            '집': '주거',
            '방': '주거',
            '문': '주거',
            '계단': '주거',
            '차': '교통',
            '기차': '교통',
            '비행기': '교통',
            '배': '교통',
            '음식': '음식',
            '밥': '음식',
            '과일': '음식',
            '고기': '음식',
        }
        
        self.quality_score_mapping = {
            'traditional': 8.5,
            'modern': 8.0,
            'psychological': 9.0
        }

    async def connect_db(self):
        """데이터베이스 연결"""
        try:
            self.conn = await asyncpg.connect(
                host='localhost',
                database='dream_service',
                user='postgres',
                password='heal7!',
                port=5432
            )
            logger.info("✅ PostgreSQL 연결 성공")
        except Exception as e:
            logger.error(f"❌ DB 연결 실패: {e}")
            raise

    async def analyze_existing_data(self) -> Dict:
        """기존 데이터 분석"""
        logger.info("🔍 기존 데이터 분석 시작...")
        
        # 키워드별 해석 통계
        query = """
        SELECT 
            dk.keyword,
            di.interpretation_type,
            COUNT(*) as count,
            AVG(di.confidence_score) as avg_confidence
        FROM dream_interpretations di
        JOIN dream_keywords dk ON di.keyword_id = dk.id
        GROUP BY dk.keyword, di.interpretation_type
        ORDER BY COUNT(*) DESC
        """
        
        results = await self.conn.fetch(query)
        analysis = {}
        
        for row in results:
            keyword = row['keyword']
            if keyword not in analysis:
                analysis[keyword] = {}
            analysis[keyword][row['interpretation_type']] = {
                'count': row['count'],
                'avg_confidence': float(row['avg_confidence']) if row['avg_confidence'] else 8.0
            }
        
        logger.info(f"📊 분석 완료: {len(analysis)}개 키워드")
        return analysis

    def categorize_keyword(self, keyword: str) -> str:
        """키워드 카테고리 분류"""
        # 직접 매핑
        if keyword in self.category_mapping:
            return self.category_mapping[keyword]
        
        # 패턴 기반 분류
        if any(word in keyword for word in ['뜨거운', '차가운', '깨끗한', '더러운']):
            return '상태'
        elif any(word in keyword for word in ['크다', '작다', '큰', '작은', '거대한']):
            return '크기'
        elif any(word in keyword for word in ['빨간', '파란', '노란', '검은', '흰']):
            return '색깔'
        elif any(word in keyword for word in ['아름다운', '무서운', '슬픈', '기쁜']):
            return '감정'
        else:
            return '기타'

    def extract_related_keywords(self, keyword: str, all_keywords: Set[str]) -> List[str]:
        """관련 키워드 추출"""
        related = []
        base_keyword = re.sub(r'(뜨거운|차가운|큰|작은|아름다운|더러운|깨끗한)\s*', '', keyword).strip()
        
        for other_keyword in all_keywords:
            if other_keyword != keyword:
                # 같은 베이스 키워드
                other_base = re.sub(r'(뜨거운|차가운|큰|작은|아름다운|더러운|깨끗한)\s*', '', other_keyword).strip()
                if base_keyword == other_base:
                    related.append(other_keyword)
                # 포함 관계
                elif base_keyword in other_keyword or other_keyword in base_keyword:
                    if len(abs(len(base_keyword) - len(other_keyword))) <= 2:
                        related.append(other_keyword)
        
        return related[:5]  # 최대 5개

    def calculate_quality_score(self, interpretations: Dict, keyword: str) -> float:
        """품질 점수 계산"""
        base_score = 8.0
        
        # 해석 타입 다양성
        type_bonus = len(interpretations) * 0.5
        
        # 키워드 길이 보너스 (구체적일수록 높음)
        length_bonus = min(len(keyword) / 10, 1.0)
        
        # 신뢰도 점수
        confidence_avg = sum(
            data['avg_confidence'] for data in interpretations.values()
        ) / len(interpretations)
        
        final_score = min(base_score + type_bonus + length_bonus + (confidence_avg - 8.0), 10.0)
        return round(final_score, 1)

    async def migrate_data(self, analysis: Dict):
        """데이터 이전 실행"""
        logger.info("🚀 데이터 이전 시작...")
        
        all_keywords = set(analysis.keys())
        migrated_count = 0
        
        for keyword, interpretations in analysis.items():
            try:
                # 해석 텍스트 통합
                traditional_texts = []
                modern_texts = []
                psychological_texts = []
                
                # 각 타입별 해석 수집
                for interp_type, data in interpretations.items():
                    query = """
                    SELECT di.interpretation_text
                    FROM dream_interpretations di
                    JOIN dream_keywords dk ON di.keyword_id = dk.id
                    WHERE dk.keyword = $1 AND di.interpretation_type = $2
                    """
                    
                    texts = await self.conn.fetch(query, keyword, interp_type)
                    text_list = [row['interpretation_text'] for row in texts]
                    
                    if interp_type == 'traditional':
                        traditional_texts.extend(text_list)
                    elif interp_type == 'modern':
                        modern_texts.extend(text_list)
                    elif interp_type == 'psychological':
                        psychological_texts.extend(text_list)
                
                # 중복 제거 및 통합
                traditional_interpretation = ' | '.join(set(traditional_texts)) if traditional_texts else None
                modern_interpretation = ' | '.join(set(modern_texts)) if modern_texts else None
                
                # 심리학적 해석이 있으면 현대적 해석에 포함
                if psychological_texts:
                    psych_text = ' | '.join(set(psychological_texts))
                    if modern_interpretation:
                        modern_interpretation += f" | {psych_text}"
                    else:
                        modern_interpretation = psych_text
                
                # 관련 키워드 및 메타데이터
                related_keywords = self.extract_related_keywords(keyword, all_keywords)
                category = self.categorize_keyword(keyword)
                quality_score = self.calculate_quality_score(interpretations, keyword)
                
                # clean_dream_interpretations에 삽입
                insert_query = """
                INSERT INTO clean_dream_interpretations 
                (keyword, modern_interpretation, traditional_interpretation, 
                 related_keywords, category, quality_score, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $7)
                ON CONFLICT (keyword) DO UPDATE SET
                    modern_interpretation = EXCLUDED.modern_interpretation,
                    traditional_interpretation = EXCLUDED.traditional_interpretation,
                    related_keywords = EXCLUDED.related_keywords,
                    category = EXCLUDED.category,
                    quality_score = EXCLUDED.quality_score,
                    updated_at = EXCLUDED.updated_at
                """
                
                await self.conn.execute(
                    insert_query,
                    keyword,
                    modern_interpretation,
                    traditional_interpretation,
                    related_keywords,
                    category,
                    quality_score,
                    datetime.now()
                )
                
                migrated_count += 1
                if migrated_count % 100 == 0:
                    logger.info(f"📊 진행 상황: {migrated_count}/{len(analysis)} 완료")
                
            except Exception as e:
                logger.error(f"❌ {keyword} 이전 실패: {e}")
                continue
        
        logger.info(f"✅ 이전 완료: {migrated_count}개 키워드 처리")
        return migrated_count

    async def verify_migration(self) -> Dict:
        """이전 결과 검증"""
        logger.info("🔍 이전 결과 검증...")
        
        # 기본 통계
        count_query = "SELECT COUNT(*) FROM clean_dream_interpretations"
        total_count = await self.conn.fetchval(count_query)
        
        # 카테고리별 분포
        category_query = """
        SELECT category, COUNT(*) as count 
        FROM clean_dream_interpretations 
        GROUP BY category 
        ORDER BY count DESC
        """
        categories = await self.conn.fetch(category_query)
        
        # 품질 점수 분포
        quality_query = """
        SELECT 
            ROUND(quality_score) as score_range,
            COUNT(*) as count
        FROM clean_dream_interpretations 
        GROUP BY ROUND(quality_score)
        ORDER BY score_range
        """
        quality_dist = await self.conn.fetch(quality_query)
        
        # 샘플 데이터
        sample_query = """
        SELECT keyword, category, quality_score, 
               LEFT(traditional_interpretation, 50) as traditional_preview,
               LEFT(modern_interpretation, 50) as modern_preview
        FROM clean_dream_interpretations 
        ORDER BY quality_score DESC 
        LIMIT 5
        """
        samples = await self.conn.fetch(sample_query)
        
        verification = {
            'total_count': total_count,
            'categories': {row['category']: row['count'] for row in categories},
            'quality_distribution': {row['score_range']: row['count'] for row in quality_dist},
            'top_samples': [dict(row) for row in samples]
        }
        
        logger.info(f"📊 검증 완료: {total_count}개 데이터")
        logger.info(f"📂 카테고리: {len(verification['categories'])}개")
        
        return verification

    async def close(self):
        """리소스 정리"""
        if self.conn:
            await self.conn.close()
            logger.info("🔐 DB 연결 해제")

async def main():
    """메인 실행 함수"""
    migrator = DreamDataMigrator()
    
    try:
        # 1. DB 연결
        await migrator.connect_db()
        
        # 2. 기존 데이터 분석
        analysis = await migrator.analyze_existing_data()
        
        # 3. 데이터 이전
        migrated_count = await migrator.migrate_data(analysis)
        
        # 4. 결과 검증
        verification = await migrator.verify_migration()
        
        # 5. 결과 리포트
        print("\n" + "="*60)
        print("🎉 HEAL7 꿈풀이 데이터 이전 완료!")
        print("="*60)
        print(f"📊 이전된 키워드: {migrated_count}개")
        print(f"📊 최종 데이터: {verification['total_count']}개")
        print(f"📂 카테고리 분포:")
        for category, count in verification['categories'].items():
            print(f"   - {category}: {count}개")
        
        print(f"\n🌟 상위 품질 키워드 샘플:")
        for sample in verification['top_samples']:
            print(f"   - {sample['keyword']} ({sample['category']}) - 점수: {sample['quality_score']}")
        
        # 결과를 파일로도 저장
        with open('/tmp/dream_migration_report.json', 'w', encoding='utf-8') as f:
            json.dump(verification, f, ensure_ascii=False, indent=2)
        
        logger.info("📄 상세 리포트: /tmp/dream_migration_report.json")
        
    except Exception as e:
        logger.error(f"💥 이전 과정 오류: {e}")
        raise
    finally:
        await migrator.close()

if __name__ == "__main__":
    asyncio.run(main())