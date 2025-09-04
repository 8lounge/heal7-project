#!/usr/bin/env python3
"""
🔮 꿈풀이 시스템 고도화 PostgreSQL 스키마 설계
- 다중 해석 시스템 지원
- 고성능 검색 최적화
- 카테고리별 인덱싱
- 품질 관리 시스템
"""

import psycopg2
import logging
from typing import List, Dict, Optional
import json
from datetime import datetime

class EnhancedDreamSchema:
    """향상된 꿈풀이 데이터베이스 스키마 관리"""
    
    def __init__(self, db_name: str = "dream_service"):
        self.db_name = db_name
        self.logger = logging.getLogger(__name__)
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def get_connection(self):
        """PostgreSQL 연결"""
        try:
            conn = psycopg2.connect(
                host="localhost",
                database=self.db_name,
                user="postgres",
                password=""  # 로컬 postgres 설정
            )
            return conn
        except Exception as e:
            self.logger.error(f"DB 연결 실패: {e}")
            return None
    
    def create_enhanced_schema(self):
        """고도화된 스키마 생성"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                # 1. 카테고리 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_categories (
                        id SERIAL PRIMARY KEY,
                        category_id VARCHAR(50) UNIQUE NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        name_en VARCHAR(100),
                        description TEXT,
                        parent_category VARCHAR(50),
                        cultural_weight INTEGER DEFAULT 1,
                        estimated_keywords INTEGER DEFAULT 0,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (parent_category) REFERENCES dream_categories(category_id)
                    );
                """)
                
                # 2. 키워드 테이블 (메인)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_keywords (
                        id SERIAL PRIMARY KEY,
                        keyword VARCHAR(255) NOT NULL,
                        keyword_normalized VARCHAR(255) NOT NULL,  -- 검색 최적화용
                        category_id VARCHAR(50) NOT NULL,
                        variations TEXT[],  -- 키워드 변형들
                        quality_score DECIMAL(3,2) DEFAULT 8.0,
                        frequency_score INTEGER DEFAULT 0,  -- 검색 빈도
                        status VARCHAR(20) DEFAULT 'active',  -- active, inactive, pending
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES dream_categories(category_id),
                        UNIQUE(keyword, category_id)
                    );
                """)
                
                # 3. 다중 해석 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_interpretations (
                        id SERIAL PRIMARY KEY,
                        keyword_id INTEGER NOT NULL,
                        interpretation_type VARCHAR(30) NOT NULL,  -- traditional, modern, psychological
                        interpretation_text TEXT NOT NULL,
                        sentiment VARCHAR(20),  -- positive, negative, neutral
                        confidence_score DECIMAL(3,2) DEFAULT 8.0,
                        author_type VARCHAR(30) DEFAULT 'system',  -- system, human, ai
                        metadata JSONB,  -- 추가 메타데이터
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (keyword_id) REFERENCES dream_keywords(id) ON DELETE CASCADE
                    );
                """)
                
                # 4. 관련 키워드 관계 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_keyword_relations (
                        id SERIAL PRIMARY KEY,
                        source_keyword_id INTEGER NOT NULL,
                        target_keyword_id INTEGER NOT NULL,
                        relation_type VARCHAR(30) NOT NULL,  -- related, opposite, similar
                        strength DECIMAL(3,2) DEFAULT 5.0,  -- 관계 강도 1-10
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (source_keyword_id) REFERENCES dream_keywords(id) ON DELETE CASCADE,
                        FOREIGN KEY (target_keyword_id) REFERENCES dream_keywords(id) ON DELETE CASCADE,
                        UNIQUE(source_keyword_id, target_keyword_id, relation_type)
                    );
                """)
                
                # 5. 검색 로그 테이블 (성능 분석용)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_search_logs (
                        id SERIAL PRIMARY KEY,
                        search_term VARCHAR(255) NOT NULL,
                        keyword_id INTEGER,
                        result_count INTEGER DEFAULT 0,
                        response_time_ms INTEGER,
                        user_agent TEXT,
                        ip_address INET,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (keyword_id) REFERENCES dream_keywords(id)
                    );
                """)
                
                # 6. 키워드 통계 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dream_keyword_stats (
                        id SERIAL PRIMARY KEY,
                        keyword_id INTEGER NOT NULL UNIQUE,
                        search_count INTEGER DEFAULT 0,
                        last_searched TIMESTAMP WITH TIME ZONE,
                        avg_quality_score DECIMAL(3,2),
                        interpretation_count INTEGER DEFAULT 0,
                        relation_count INTEGER DEFAULT 0,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (keyword_id) REFERENCES dream_keywords(id) ON DELETE CASCADE
                    );
                """)
                
                # 인덱스 생성
                self.create_indexes(cur)
                
                conn.commit()
                self.logger.info("✅ 고도화된 꿈풀이 스키마 생성 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"스키마 생성 실패: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def create_indexes(self, cursor):
        """성능 최적화 인덱스 생성"""
        indexes = [
            # 키워드 검색 최적화
            "CREATE INDEX IF NOT EXISTS idx_dream_keywords_normalized ON dream_keywords USING gin(to_tsvector('korean', keyword_normalized));",
            "CREATE INDEX IF NOT EXISTS idx_dream_keywords_category ON dream_keywords(category_id);",
            "CREATE INDEX IF NOT EXISTS idx_dream_keywords_quality ON dream_keywords(quality_score DESC);",
            "CREATE INDEX IF NOT EXISTS idx_dream_keywords_status ON dream_keywords(status);",
            
            # 해석 검색 최적화
            "CREATE INDEX IF NOT EXISTS idx_dream_interpretations_keyword ON dream_interpretations(keyword_id);",
            "CREATE INDEX IF NOT EXISTS idx_dream_interpretations_type ON dream_interpretations(interpretation_type);",
            "CREATE INDEX IF NOT EXISTS idx_dream_interpretations_sentiment ON dream_interpretations(sentiment);",
            
            # 관계 검색 최적화
            "CREATE INDEX IF NOT EXISTS idx_dream_relations_source ON dream_keyword_relations(source_keyword_id);",
            "CREATE INDEX IF NOT EXISTS idx_dream_relations_target ON dream_keyword_relations(target_keyword_id);",
            "CREATE INDEX IF NOT EXISTS idx_dream_relations_strength ON dream_keyword_relations(strength DESC);",
            
            # 통계 및 로그 최적화
            "CREATE INDEX IF NOT EXISTS idx_dream_search_logs_term ON dream_search_logs(search_term);",
            "CREATE INDEX IF NOT EXISTS idx_dream_search_logs_created ON dream_search_logs(created_at DESC);",
            "CREATE INDEX IF NOT EXISTS idx_dream_stats_search_count ON dream_keyword_stats(search_count DESC);",
            
            # 카테고리 최적화
            "CREATE INDEX IF NOT EXISTS idx_dream_categories_parent ON dream_categories(parent_category);",
            "CREATE INDEX IF NOT EXISTS idx_dream_categories_weight ON dream_categories(cultural_weight DESC);",
            
            # 복합 인덱스 (고성능 검색)
            "CREATE INDEX IF NOT EXISTS idx_keywords_category_quality ON dream_keywords(category_id, quality_score DESC);",
            "CREATE INDEX IF NOT EXISTS idx_interpretations_keyword_type ON dream_interpretations(keyword_id, interpretation_type);",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except Exception as e:
                self.logger.warning(f"인덱스 생성 경고: {e}")
    
    def insert_categories(self):
        """카테고리 데이터 삽입"""
        # JSON 파일에서 카테고리 로드
        try:
            with open('/home/ubuntu/heal7-project/backend/services/crawling-service/scripts/dream-processing/dream_category_system.json', 'r', encoding='utf-8') as f:
                category_data = json.load(f)
        except FileNotFoundError:
            self.logger.error("카테고리 JSON 파일을 찾을 수 없습니다.")
            return False
        
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                categories = category_data['categories']
                
                for cat_id, cat_info in categories.items():
                    cur.execute("""
                        INSERT INTO dream_categories 
                        (category_id, name, name_en, description, parent_category, cultural_weight, estimated_keywords)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (category_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        description = EXCLUDED.description,
                        cultural_weight = EXCLUDED.cultural_weight,
                        estimated_keywords = EXCLUDED.estimated_keywords;
                    """, (
                        cat_info['id'],
                        cat_info['name'],
                        cat_info['name_en'],
                        cat_info['description'],
                        cat_info.get('parent_category'),
                        cat_info['cultural_weight'],
                        cat_info['estimated_keywords']
                    ))
                
                conn.commit()
                self.logger.info(f"✅ {len(categories)}개 카테고리 데이터 삽입 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"카테고리 삽입 실패: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def create_sample_keywords(self, count: int = 50):
        """샘플 키워드 생성 (테스트용)"""
        sample_keywords = [
            ("물", "water", "맑은 물을 마시는 것은 좋은 일이 생길 징조입니다.", "물은 무의식과 감정을 상징합니다."),
            ("바다", "water", "넓은 바다는 무한한 가능성을 나타냅니다.", "바다는 집단무의식의 상징입니다."),
            ("강", "water", "흐르는 강물은 시간의 흐름과 변화를 의미합니다.", "강은 인생의 여정을 나타냅니다."),
            ("불", "fire", "타오르는 불은 열정과 변화를 상징합니다.", "불은 정화와 재생의 원동력입니다."),
            ("호랑이", "zodiac_animals", "호랑이는 권위와 용맹을 나타냅니다.", "호랑이는 강한 의지력을 상징합니다."),
            ("용", "mythology", "용꿈은 출세와 성공을 예고합니다.", "용은 잠재된 창조력을 나타냅니다."),
            ("돈", "money", "돈을 줍는 꿈은 실제로는 손해를 의미합니다.", "돈은 자아가치와 안정성을 상징합니다."),
            ("집", "home", "새 집은 새로운 시작을 의미합니다.", "집은 자아와 정체성의 공간입니다."),
            ("가족", "family", "가족과 함께하는 꿈은 화목을 뜻합니다.", "가족은 소속감과 안정감을 나타냅니다."),
            ("죽음", "death_birth", "죽음의 꿈은 새로운 시작을 의미합니다.", "죽음은 변화와 재탄생을 상징합니다.")
        ]
        
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                for keyword, category, traditional, modern in sample_keywords:
                    # 키워드 삽입
                    cur.execute("""
                        INSERT INTO dream_keywords (keyword, keyword_normalized, category_id, quality_score)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (keyword, category_id) DO NOTHING
                        RETURNING id;
                    """, (keyword, keyword.lower(), category, 9.0))
                    
                    result = cur.fetchone()
                    if result:
                        keyword_id = result[0]
                        
                        # 전통적 해석 삽입
                        cur.execute("""
                            INSERT INTO dream_interpretations 
                            (keyword_id, interpretation_type, interpretation_text, sentiment, confidence_score)
                            VALUES (%s, %s, %s, %s, %s);
                        """, (keyword_id, 'traditional', traditional, 'positive', 8.5))
                        
                        # 현대적 해석 삽입
                        cur.execute("""
                            INSERT INTO dream_interpretations 
                            (keyword_id, interpretation_type, interpretation_text, sentiment, confidence_score)
                            VALUES (%s, %s, %s, %s, %s);
                        """, (keyword_id, 'modern', modern, 'neutral', 8.0))
                        
                        # 통계 초기화
                        cur.execute("""
                            INSERT INTO dream_keyword_stats (keyword_id, interpretation_count)
                            VALUES (%s, 2)
                            ON CONFLICT (keyword_id) DO NOTHING;
                        """, (keyword_id,))
                
                conn.commit()
                self.logger.info(f"✅ {len(sample_keywords)}개 샘플 키워드 생성 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"샘플 키워드 생성 실패: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_schema_stats(self):
        """스키마 통계 조회"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cur:
                stats = {}
                
                # 테이블별 레코드 수
                tables = ['dream_categories', 'dream_keywords', 'dream_interpretations', 
                         'dream_keyword_relations', 'dream_keyword_stats']
                
                for table in tables:
                    cur.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cur.fetchone()[0]
                    stats[table] = count
                
                # 카테고리별 키워드 수
                cur.execute("""
                    SELECT c.name, COUNT(k.id) as keyword_count
                    FROM dream_categories c
                    LEFT JOIN dream_keywords k ON c.category_id = k.category_id
                    WHERE c.parent_category IS NULL
                    GROUP BY c.name
                    ORDER BY keyword_count DESC;
                """)
                
                category_stats = cur.fetchall()
                stats['category_breakdown'] = category_stats
                
                return stats
                
        except Exception as e:
            self.logger.error(f"통계 조회 실패: {e}")
            return None
        finally:
            conn.close()

if __name__ == "__main__":
    # 스키마 관리 시스템 실행
    schema_manager = EnhancedDreamSchema()
    
    print("🔮 꿈풀이 시스템 고도화 스키마 설정")
    print("=" * 50)
    
    # 1. 스키마 생성
    if schema_manager.create_enhanced_schema():
        print("✅ 데이터베이스 스키마 생성 완료")
    else:
        print("❌ 스키마 생성 실패")
        exit(1)
    
    # 2. 카테고리 삽입
    if schema_manager.insert_categories():
        print("✅ 카테고리 데이터 삽입 완료")
    else:
        print("❌ 카테고리 삽입 실패")
    
    # 3. 샘플 키워드 생성
    if schema_manager.create_sample_keywords():
        print("✅ 샘플 키워드 생성 완료")
    
    # 4. 통계 조회
    stats = schema_manager.get_schema_stats()
    if stats:
        print("\n📊 데이터베이스 현황:")
        for table, count in stats.items():
            if table != 'category_breakdown':
                print(f"   {table}: {count:,}개")
        
        print("\n📂 카테고리별 키워드 현황:")
        for category, count in stats['category_breakdown']:
            print(f"   {category}: {count}개")
    
    print("\n🎯 다음 단계: 1,000개 키워드 확장 준비 완료")