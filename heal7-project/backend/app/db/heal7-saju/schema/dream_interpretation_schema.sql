-- ====================================
-- HEAL7 꿈풀이/해몽 데이터베이스 스키마
-- 
-- 대량의 꿈풀이 데이터를 저장하고 검색 최적화
-- 만세력 74,000개처럼 체계적인 해몽 데이터 관리
-- 
-- @author HEAL7 Team
-- @version 1.0.0
-- @license MIT
-- ====================================

-- 확장 프로그램 (전문 검색 및 인덱싱용)
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- 유사도 검색
CREATE EXTENSION IF NOT EXISTS "unaccent"; -- 악센트 제거

-- ====================================
-- 🌙 1. 꿈 카테고리 분류 체계
-- ====================================

/**
 * 꿈 대분류 테이블
 * 전통적인 해몽 분류 체계를 따름
 */
CREATE TABLE dream_categories (
  id SERIAL PRIMARY KEY,
  category_code VARCHAR(20) UNIQUE NOT NULL,
  korean_name VARCHAR(100) NOT NULL,
  english_name VARCHAR(100),
  emoji VARCHAR(10),
  description TEXT,
  parent_id INTEGER REFERENCES dream_categories(id),
  sort_order INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 기본 카테고리 데이터 삽입
INSERT INTO dream_categories (category_code, korean_name, english_name, emoji, description, sort_order) VALUES
('ANIMALS', '동물', 'Animals', '🐾', '동물이 나오는 꿈', 1),
('NATURE', '자연', 'Nature', '🌿', '자연 현상과 환경', 2),
('PEOPLE', '사람', 'People', '👥', '사람이 등장하는 꿈', 3),
('OBJECTS', '사물', 'Objects', '🏺', '물건이나 도구', 4),
('ACTIONS', '행동', 'Actions', '🏃‍♂️', '특정 행동을 하는 꿈', 5),
('EMOTIONS', '감정', 'Emotions', '😊', '감정 상태나 느낌', 6),
('BODY', '신체', 'Body', '👤', '몸과 관련된 꿈', 7),
('SPIRITUAL', '영적/신비', 'Spiritual', '🔮', '초자연적 현상', 8),
('PLACES', '장소', 'Places', '🏠', '특정 장소나 건물', 9),
('COLORS', '색깔', 'Colors', '🎨', '특정 색깔이 인상적인 꿈', 10);

-- 하위 카테고리 삽입
INSERT INTO dream_categories (category_code, korean_name, english_name, parent_id, sort_order) VALUES
-- 동물 하위 카테고리
('MAMMALS', '포유류', 'Mammals', 1, 1),
('BIRDS', '조류', 'Birds', 1, 2),
('FISH', '어류', 'Fish', 1, 3),
('INSECTS', '곤충류', 'Insects', 1, 4),
('REPTILES', '파충류', 'Reptiles', 1, 5),
('MYTHICAL', '상상동물', 'Mythical Animals', 1, 6),

-- 자연 하위 카테고리
('WEATHER', '날씨', 'Weather', 2, 1),
('LANDSCAPE', '산/바다', 'Landscape', 2, 2),
('PLANTS', '식물', 'Plants', 2, 3),
('CELESTIAL', '천체', 'Celestial', 2, 4),
('SEASONS', '계절', 'Seasons', 2, 5),
('DISASTERS', '재해', 'Disasters', 2, 6);

-- ====================================
-- 🌙 2. 꿈풀이 메인 데이터 테이블
-- ====================================

/**
 * 꿈풀이 메인 테이블
 * 대량의 해몽 데이터를 체계적으로 저장
 */
CREATE TABLE dream_interpretations (
  id BIGSERIAL PRIMARY KEY,
  
  -- 키워드 정보
  keyword VARCHAR(200) NOT NULL, -- 꿈의 주요 키워드
  keyword_variants TEXT[], -- 유사 키워드 배열
  category_id INTEGER REFERENCES dream_categories(id),
  subcategory_id INTEGER REFERENCES dream_categories(id),
  
  -- 해몽 내용
  traditional_meaning TEXT NOT NULL, -- 전통적 해석
  modern_meaning TEXT NOT NULL, -- 현대적 해석
  psychological_meaning TEXT, -- 심리학적 해석
  spiritual_meaning TEXT, -- 영적/종교적 해석
  
  -- 분류 및 메타데이터
  dream_type VARCHAR(50), -- 'prophetic', 'symbolic', 'psychological', 'spiritual'
  fortune_aspect VARCHAR(20), -- 'positive', 'neutral', 'negative', 'warning'
  confidence_score DECIMAL(3,2) DEFAULT 0.5, -- 해석의 신뢰도 (0.0-1.0)
  
  -- 연관 정보
  related_keywords TEXT[], -- 연관 키워드들
  lucky_numbers INTEGER[], -- 행운의 숫자
  lucky_colors VARCHAR(100)[], -- 행운의 색깔
  compatible_dreams TEXT[], -- 함께 나타나면 좋은 꿈
  conflicting_dreams TEXT[], -- 함께 나타나면 복잡한 꿈
  
  -- 통계 및 품질 관리
  search_frequency INTEGER DEFAULT 0, -- 검색된 횟수
  accuracy_rating DECIMAL(3,2) DEFAULT 0.0, -- 사용자 평가 (0.0-5.0)
  source_reliability INTEGER DEFAULT 1, -- 출처 신뢰도 (1-5)
  data_source VARCHAR(200), -- 데이터 출처
  
  -- 추가 속성
  seasonal_relevance VARCHAR(20)[], -- 계절별 연관성
  cultural_context VARCHAR(100), -- 문화적 맥락 (한국, 중국, 서양 등)
  gender_specific BOOLEAN DEFAULT false, -- 성별 특화 해석 여부
  age_group VARCHAR(50), -- 연령대별 해석 ('child', 'teen', 'adult', 'elder')
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_by VARCHAR(100),
  last_verified_at TIMESTAMP WITH TIME ZONE
);

-- ====================================
-- 🌙 3. 꿈 조합 해석 테이블
-- ====================================

/**
 * 꿈 조합 해석 테이블
 * 여러 꿈이 함께 나타날 때의 특별한 의미
 */
CREATE TABLE dream_combinations (
  id BIGSERIAL PRIMARY KEY,
  
  -- 조합 정보
  combination_name VARCHAR(200) NOT NULL,
  dream_keywords TEXT[] NOT NULL, -- 조합을 이루는 꿈 키워드들 (배열)
  combination_type VARCHAR(50), -- 'synergy', 'conflict', 'amplification', 'neutralization'
  
  -- 조합 해석
  combined_meaning TEXT NOT NULL,
  strength_level INTEGER DEFAULT 1 CHECK (strength_level BETWEEN 1 AND 5), -- 조합의 영향 강도
  
  -- 확률 및 통계
  occurrence_frequency DECIMAL(5,4) DEFAULT 0.0001, -- 이 조합이 나타날 확률
  cultural_significance INTEGER DEFAULT 1, -- 문화적 중요도 (1-5)
  
  -- 메타데이터
  source_reference VARCHAR(300), -- 출처 참조
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================
-- 🌙 4. 사용자 꿈 기록 테이블
-- ====================================

/**
 * 사용자가 꾼 꿈 기록
 */
CREATE TABLE user_dreams (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  
  -- 꿈 정보
  dream_date DATE NOT NULL,
  dream_keywords TEXT[] NOT NULL,
  dream_description TEXT,
  dream_mood VARCHAR(20), -- 'peaceful', 'scary', 'exciting', 'confusing'
  
  -- 해석 결과
  interpretation_ids BIGINT[] DEFAULT '{}', -- 적용된 해석 ID들
  overall_meaning TEXT,
  personal_notes TEXT,
  
  -- 개인화 정보
  user_rating INTEGER CHECK (user_rating BETWEEN 1 AND 5),
  came_true BOOLEAN DEFAULT NULL, -- 예언적 꿈이 실현되었는지
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================
-- 🌙 5. 꿈풀이 통계 및 분석 테이블
-- ====================================

/**
 * 꿈풀이 검색 통계
 */
CREATE TABLE dream_search_stats (
  id BIGSERIAL PRIMARY KEY,
  keyword VARCHAR(200) NOT NULL,
  search_count INTEGER DEFAULT 1,
  last_searched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  -- 통계 정보
  daily_searches INTEGER DEFAULT 1,
  weekly_searches INTEGER DEFAULT 1,
  monthly_searches INTEGER DEFAULT 1,
  
  -- 트렌드 분석
  trend_score DECIMAL(5,2) DEFAULT 0.0,
  seasonal_pattern JSONB DEFAULT '{}', -- 계절별 검색 패턴
  
  UNIQUE(keyword)
);

-- ====================================
-- 🌙 6. 인덱스 및 최적화
-- ====================================

-- 키워드 검색 최적화
CREATE INDEX idx_dreams_keyword ON dream_interpretations USING gin(to_tsvector('korean', keyword));
CREATE INDEX idx_dreams_keyword_variants ON dream_interpretations USING gin(keyword_variants);
CREATE INDEX idx_dreams_traditional ON dream_interpretations USING gin(to_tsvector('korean', traditional_meaning));
CREATE INDEX idx_dreams_modern ON dream_interpretations USING gin(to_tsvector('korean', modern_meaning));

-- 빠른 조회용 인덱스
CREATE INDEX idx_dreams_category ON dream_interpretations(category_id);
CREATE INDEX idx_dreams_fortune_aspect ON dream_interpretations(fortune_aspect);
CREATE INDEX idx_dreams_search_freq ON dream_interpretations(search_frequency DESC);
CREATE INDEX idx_dreams_confidence ON dream_interpretations(confidence_score DESC);

-- 유사도 검색 최적화
CREATE INDEX idx_dreams_keyword_trigram ON dream_interpretations USING gin(keyword gin_trgm_ops);

-- 조합 검색 최적화
CREATE INDEX idx_combinations_keywords ON dream_combinations USING gin(dream_keywords);

-- 사용자 꿈 조회 최적화
CREATE INDEX idx_user_dreams_user_id ON user_dreams(user_id);
CREATE INDEX idx_user_dreams_date ON user_dreams(dream_date DESC);
CREATE INDEX idx_user_dreams_keywords ON user_dreams USING gin(dream_keywords);

-- 검색 통계 최적화
CREATE INDEX idx_search_stats_keyword ON dream_search_stats(keyword);
CREATE INDEX idx_search_stats_trend ON dream_search_stats(trend_score DESC);

-- ====================================
-- 🌙 7. 전문 검색 함수들
-- ====================================

/**
 * 꿈 키워드 유사도 검색 함수
 */
CREATE OR REPLACE FUNCTION search_dreams_by_similarity(
  search_term TEXT,
  similarity_threshold REAL DEFAULT 0.3,
  max_results INTEGER DEFAULT 20
)
RETURNS TABLE(
  id BIGINT,
  keyword VARCHAR(200),
  traditional_meaning TEXT,
  modern_meaning TEXT,
  similarity_score REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    di.id,
    di.keyword,
    di.traditional_meaning,
    di.modern_meaning,
    similarity(di.keyword, search_term) as sim_score
  FROM dream_interpretations di
  WHERE similarity(di.keyword, search_term) > similarity_threshold
  ORDER BY sim_score DESC
  LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

/**
 * 복합 키워드 꿈 검색 함수
 */
CREATE OR REPLACE FUNCTION search_dreams_multiple_keywords(
  keywords TEXT[],
  search_mode VARCHAR(10) DEFAULT 'any' -- 'any' 또는 'all'
)
RETURNS TABLE(
  id BIGINT,
  keyword VARCHAR(200),
  match_count INTEGER,
  combined_meaning TEXT
) AS $$
BEGIN
  IF search_mode = 'all' THEN
    RETURN QUERY
    SELECT 
      di.id,
      di.keyword,
      array_length(array(SELECT unnest(keywords) INTERSECT SELECT unnest(di.keyword_variants || di.keyword)), 1) as match_count,
      di.traditional_meaning as combined_meaning
    FROM dream_interpretations di
    WHERE di.keyword_variants && keywords OR di.keyword = ANY(keywords)
    HAVING array_length(array(SELECT unnest(keywords) INTERSECT SELECT unnest(di.keyword_variants || di.keyword)), 1) = array_length(keywords, 1)
    ORDER BY match_count DESC;
  ELSE
    RETURN QUERY
    SELECT 
      di.id,
      di.keyword,
      array_length(array(SELECT unnest(keywords) INTERSECT SELECT unnest(di.keyword_variants || di.keyword)), 1) as match_count,
      di.traditional_meaning as combined_meaning
    FROM dream_interpretations di
    WHERE di.keyword_variants && keywords OR di.keyword = ANY(keywords)
    ORDER BY match_count DESC;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- ====================================
-- 🌙 8. 자동 업데이트 트리거
-- ====================================

/**
 * updated_at 자동 업데이트 함수
 */
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 트리거 적용
CREATE TRIGGER update_dream_interpretations_updated_at 
  BEFORE UPDATE ON dream_interpretations 
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_dreams_updated_at 
  BEFORE UPDATE ON user_dreams 
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ====================================
-- 🌙 9. 뷰(View) 생성
-- ====================================

/**
 * 인기 꿈풀이 뷰
 */
CREATE VIEW popular_dreams AS
SELECT 
  di.id,
  di.keyword,
  dc.korean_name as category_name,
  di.traditional_meaning,
  di.modern_meaning,
  di.search_frequency,
  di.accuracy_rating,
  di.confidence_score
FROM dream_interpretations di
LEFT JOIN dream_categories dc ON di.category_id = dc.id
ORDER BY di.search_frequency DESC, di.accuracy_rating DESC;

/**
 * 계절별 꿈풀이 뷰
 */
CREATE VIEW seasonal_dreams AS
SELECT 
  di.*,
  dc.korean_name as category_name,
  CASE 
    WHEN 'spring' = ANY(di.seasonal_relevance) THEN '봄'
    WHEN 'summer' = ANY(di.seasonal_relevance) THEN '여름'
    WHEN 'autumn' = ANY(di.seasonal_relevance) THEN '가을'
    WHEN 'winter' = ANY(di.seasonal_relevance) THEN '겨울'
    ELSE '사계절'
  END as season_label
FROM dream_interpretations di
LEFT JOIN dream_categories dc ON di.category_id = dc.id
WHERE di.seasonal_relevance IS NOT NULL AND array_length(di.seasonal_relevance, 1) > 0;

-- ====================================
-- 🌙 10. 초기 데이터 샘플
-- ====================================

/**
 * 샘플 꿈풀이 데이터 삽입 (테스트용)
 */
INSERT INTO dream_interpretations 
(keyword, keyword_variants, category_id, traditional_meaning, modern_meaning, psychological_meaning, 
 fortune_aspect, confidence_score, related_keywords, lucky_numbers, data_source) VALUES

('뱀', ARRAY['독사', '비단뱀', '구렁이', '코브라'], 5, 
 '뱀꿈은 전통적으로 길몽으로 여겨집니다. 재물운 상승, 지혜 획득, 치유의 의미가 있습니다.',
 '변화와 변신의 상징입니다. 새로운 시작이나 성장을 의미하며, 때로는 숨겨진 적이나 위험을 나타내기도 합니다.',
 '무의식의 힘, 원시적 에너지, 억압된 욕망의 상징입니다.',
 'positive', 0.85, 
 ARRAY['용', '도마뱀', '거북이', '물'], ARRAY[3, 7, 21],
 '전통 해몽서/주공해몽'),

('물', ARRAY['강물', '바닷물', '맑은물', '흐린물'], 2,
 '맑은 물은 재물과 복을, 흐린 물은 걱정과 근심을 의미합니다.',
 '감정의 흐름, 무의식의 세계, 정화와 재생을 상징합니다.',
 '감정 상태와 정서적 균형을 반영합니다.',
 'neutral', 0.78,
 ARRAY['비', '바다', '강', '호수', '뱀'], ARRAY[2, 6, 8],
 '한국전통문화포털'),

('돈', ARRAY['지폐', '동전', '화폐', '현금'], 4,
 '돈을 주워도 길몽, 잃어도 길몽으로 해석됩니다. 재물운의 변화를 의미합니다.',
 '성공욕구, 안정감 추구, 또는 경제적 불안감을 나타냅니다.',
 '자존감과 가치 인정에 대한 욕구를 반영합니다.',
 'positive', 0.70,
 ARRAY['금', '보석', '지갑', '은행'], ARRAY[1, 8, 18, 28],
 '민속 해몽 연구소');

-- ====================================
-- 🌙 11. 데이터 품질 관리
-- ====================================

/**
 * 데이터 품질 체크 함수
 */
CREATE OR REPLACE FUNCTION check_dream_data_quality()
RETURNS TABLE(
  issue_type TEXT,
  affected_count BIGINT,
  description TEXT
) AS $$
BEGIN
  -- 키워드가 비어있는 레코드 체크
  RETURN QUERY
  SELECT 
    'EMPTY_KEYWORD'::TEXT,
    COUNT(*),
    '키워드가 비어있는 해몽 데이터'::TEXT
  FROM dream_interpretations 
  WHERE keyword IS NULL OR trim(keyword) = '';
  
  -- 해석이 비어있는 레코드 체크
  RETURN QUERY
  SELECT 
    'EMPTY_MEANING'::TEXT,
    COUNT(*),
    '해석 내용이 비어있는 데이터'::TEXT
  FROM dream_interpretations 
  WHERE traditional_meaning IS NULL OR modern_meaning IS NULL;
  
  -- 중복 키워드 체크
  RETURN QUERY
  SELECT 
    'DUPLICATE_KEYWORD'::TEXT,
    COUNT(*) - COUNT(DISTINCT keyword),
    '중복된 키워드가 있는 데이터'::TEXT
  FROM dream_interpretations;
  
END;
$$ LANGUAGE plpgsql;

-- 마지막으로 테이블 소유자 권한 설정
-- ALTER TABLE dream_interpretations OWNER TO heal7_admin;
-- ALTER TABLE dream_categories OWNER TO heal7_admin;
-- ALTER TABLE dream_combinations OWNER TO heal7_admin;
-- ALTER TABLE user_dreams OWNER TO heal7_admin;
-- ALTER TABLE dream_search_stats OWNER TO heal7_admin;