-- ====================================
-- HEAL7 꿈풀이 다각도 해석 시스템 스키마
-- 
-- 같은 꿈에 대해 다양한 출처와 관점의 해석을 제공
-- 사용자가 여러 해석을 비교하고 선택할 수 있는 시스템
-- 
-- @author HEAL7 Team
-- @version 2.0.0
-- @license MIT
-- ====================================

-- ====================================
-- 🎭 1. 해석 관점/출처 분류 체계
-- ====================================

/**
 * 해석 관점 테이블
 * 다양한 문화권과 학문적 관점을 분류
 */
CREATE TABLE interpretation_perspectives (
  id SERIAL PRIMARY KEY,
  perspective_code VARCHAR(50) UNIQUE NOT NULL,
  korean_name VARCHAR(100) NOT NULL,
  english_name VARCHAR(100),
  description TEXT,
  cultural_origin VARCHAR(50), -- 'korean', 'chinese', 'western', 'indian', 'arabic' 등
  approach_type VARCHAR(50), -- 'traditional', 'psychological', 'spiritual', 'modern', 'scientific'
  reliability_score INTEGER DEFAULT 3 CHECK (reliability_score BETWEEN 1 AND 5), -- 신뢰도 점수
  color_theme VARCHAR(20), -- UI 테마 색상
  icon_emoji VARCHAR(10),
  is_active BOOLEAN DEFAULT true,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 기본 관점 데이터 삽입
INSERT INTO interpretation_perspectives 
(perspective_code, korean_name, english_name, description, cultural_origin, approach_type, reliability_score, color_theme, icon_emoji, sort_order) 
VALUES
('KOREAN_TRADITIONAL', '한국 전통 해몽', 'Korean Traditional', '한국의 전통적인 꿈해몽 해석', 'korean', 'traditional', 5, 'blue', '🇰🇷', 1),
('CHINESE_TRADITIONAL', '중국 전통 해몽', 'Chinese Traditional', '중국 고전 해몽서 기반 해석', 'chinese', 'traditional', 5, 'red', '🇨🇳', 2),
('WESTERN_PSYCHOLOGY', '서양 심리학', 'Western Psychology', '프로이드, 융 등 서양 심리학적 해석', 'western', 'psychological', 4, 'purple', '🧠', 3),
('MODERN_SPIRITUAL', '현대 영성학', 'Modern Spiritual', '현대 영성학과 뉴에이지 관점', 'western', 'spiritual', 3, 'indigo', '🔮', 4),
('ISLAMIC_INTERPRETATION', '이슬람 해몽', 'Islamic Interpretation', '이슬람 전통 꿈해석학', 'arabic', 'spiritual', 4, 'green', '☪️', 5),
('SCIENTIFIC_ANALYSIS', '과학적 분석', 'Scientific Analysis', '현대 신경과학과 수면학 기반', 'western', 'scientific', 4, 'gray', '🔬', 6),
('BUDDHIST_PERSPECTIVE', '불교적 관점', 'Buddhist Perspective', '불교 경전과 선승들의 해석', 'indian', 'spiritual', 4, 'orange', '☸️', 7),
('FOLK_WISDOM', '민간 전승', 'Folk Wisdom', '각 지역의 민간 전승과 속담', 'korean', 'traditional', 2, 'amber', '🏚️', 8);

-- ====================================
-- 🎭 2. 다각도 해석 메인 테이블 (개선)
-- ====================================

/**
 * 기존 dream_interpretations 테이블 개선
 * 다양한 관점의 해석을 저장할 수 있도록 수정
 */
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS perspective_id INTEGER REFERENCES interpretation_perspectives(id);
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS interpretation_priority INTEGER DEFAULT 1; -- 같은 키워드 내에서 우선순위
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS source_institution VARCHAR(200); -- 출처 기관
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS source_author VARCHAR(100); -- 저자/전문가
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS publication_year INTEGER; -- 출간/발표 연도
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS isbn_or_doi VARCHAR(100); -- 출처 식별자
ALTER TABLE dream_interpretations ADD COLUMN IF NOT EXISTS interpretation_detail JSONB; -- 상세 해석 (구조화된 데이터)

-- 기존 인덱스에 추가
CREATE INDEX IF NOT EXISTS idx_dreams_perspective ON dream_interpretations(perspective_id);
CREATE INDEX IF NOT EXISTS idx_dreams_keyword_perspective ON dream_interpretations(keyword, perspective_id);

-- ====================================
-- 🎭 3. 관점별 해석 비교 뷰
-- ====================================

/**
 * 같은 키워드에 대한 다양한 관점의 해석을 한번에 조회하는 뷰
 */
CREATE VIEW dream_multi_perspective_view AS
SELECT 
  di.keyword,
  di.id as interpretation_id,
  ip.perspective_code,
  ip.korean_name as perspective_name,
  ip.cultural_origin,
  ip.approach_type,
  ip.reliability_score,
  ip.color_theme,
  ip.icon_emoji,
  di.traditional_meaning,
  di.modern_meaning,
  di.psychological_meaning,
  di.spiritual_meaning,
  di.fortune_aspect,
  di.confidence_score,
  di.related_keywords,
  di.lucky_numbers,
  di.source_institution,
  di.source_author,
  di.interpretation_priority,
  di.search_frequency
FROM dream_interpretations di
LEFT JOIN interpretation_perspectives ip ON di.perspective_id = ip.id
WHERE ip.is_active = true
ORDER BY di.keyword, di.interpretation_priority, ip.sort_order;

-- ====================================
-- 🎭 4. 해석 비교 분석 테이블
-- ====================================

/**
 * 같은 꿈에 대한 관점별 해석의 일치도/차이점 분석
 */
CREATE TABLE interpretation_comparisons (
  id BIGSERIAL PRIMARY KEY,
  keyword VARCHAR(200) NOT NULL,
  perspective_1_id INTEGER REFERENCES interpretation_perspectives(id),
  perspective_2_id INTEGER REFERENCES interpretation_perspectives(id),
  
  -- 비교 결과
  similarity_score DECIMAL(3,2) DEFAULT 0.0, -- 유사도 점수 (0.0-1.0)
  agreement_level VARCHAR(20), -- 'high', 'medium', 'low', 'conflicting'
  key_differences JSONB, -- 주요 차이점들
  common_elements JSONB, -- 공통 요소들
  
  -- 분석 메타데이터
  analysis_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  analysis_method VARCHAR(50), -- 'manual', 'ai_assisted', 'automated'
  analyst_id UUID, -- 분석자 ID
  
  UNIQUE(keyword, perspective_1_id, perspective_2_id)
);

-- ====================================
-- 🎭 5. 사용자 선호도 추적
-- ====================================

/**
 * 사용자가 어떤 관점의 해석을 선호하는지 추적
 */
CREATE TABLE user_perspective_preferences (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  perspective_id INTEGER REFERENCES interpretation_perspectives(id),
  
  -- 선호도 정보
  preference_score INTEGER DEFAULT 0, -- 누적 점수 (좋아요/선택 횟수)
  total_views INTEGER DEFAULT 0, -- 총 조회 횟수
  total_selections INTEGER DEFAULT 0, -- 총 선택 횟수
  average_rating DECIMAL(3,2) DEFAULT 0.0, -- 평균 평점
  
  -- 통계 정보
  last_viewed_at TIMESTAMP WITH TIME ZONE,
  first_viewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, perspective_id)
);

-- ====================================
-- 🎭 6. 관점별 통계 및 분석
-- ====================================

/**
 * 각 관점별 인기도와 정확도 통계
 */
CREATE TABLE perspective_statistics (
  id SERIAL PRIMARY KEY,
  perspective_id INTEGER REFERENCES interpretation_perspectives(id),
  
  -- 사용 통계
  total_interpretations INTEGER DEFAULT 0, -- 총 해석 개수
  total_searches INTEGER DEFAULT 0, -- 총 검색 횟수
  total_user_ratings INTEGER DEFAULT 0, -- 총 사용자 평가 수
  average_user_rating DECIMAL(3,2) DEFAULT 0.0, -- 평균 사용자 평점
  
  -- 품질 지표
  accuracy_score DECIMAL(3,2) DEFAULT 0.0, -- 정확도 점수
  completeness_score DECIMAL(3,2) DEFAULT 0.0, -- 완성도 점수
  uniqueness_score DECIMAL(3,2) DEFAULT 0.0, -- 독창성 점수
  
  -- 트렌드 정보
  monthly_growth_rate DECIMAL(5,2) DEFAULT 0.0, -- 월간 성장률
  trend_direction VARCHAR(20) DEFAULT 'stable', -- 'rising', 'falling', 'stable'
  
  -- 업데이트 정보
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(perspective_id)
);

-- ====================================
-- 🎭 7. 고급 검색 및 비교 함수들
-- ====================================

/**
 * 키워드별 모든 관점의 해석 조회 함수
 */
CREATE OR REPLACE FUNCTION get_multi_perspective_interpretations(
  search_keyword TEXT,
  include_perspectives TEXT[] DEFAULT NULL -- 특정 관점만 포함할 경우
)
RETURNS TABLE(
  keyword TEXT,
  perspective_code TEXT,
  perspective_name TEXT,
  cultural_origin TEXT,
  approach_type TEXT,
  interpretation_content JSONB,
  confidence_score DECIMAL,
  reliability_score INTEGER,
  color_theme TEXT,
  icon_emoji TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    dmpv.keyword::TEXT,
    dmpv.perspective_code::TEXT,
    dmpv.perspective_name::TEXT,
    dmpv.cultural_origin::TEXT,
    dmpv.approach_type::TEXT,
    jsonb_build_object(
      'traditional', dmpv.traditional_meaning,
      'modern', dmpv.modern_meaning,
      'psychological', dmpv.psychological_meaning,
      'spiritual', dmpv.spiritual_meaning,
      'fortune_aspect', dmpv.fortune_aspect,
      'related_keywords', dmpv.related_keywords,
      'lucky_numbers', dmpv.lucky_numbers,
      'source_institution', dmpv.source_institution,
      'source_author', dmpv.source_author
    ) as interpretation_content,
    dmpv.confidence_score,
    dmpv.reliability_score,
    dmpv.color_theme::TEXT,
    dmpv.icon_emoji::TEXT
  FROM dream_multi_perspective_view dmpv
  WHERE dmpv.keyword ILIKE '%' || search_keyword || '%'
    AND (include_perspectives IS NULL OR dmpv.perspective_code = ANY(include_perspectives))
  ORDER BY dmpv.interpretation_priority, dmpv.reliability_score DESC;
END;
$$ LANGUAGE plpgsql;

/**
 * 관점 간 해석 비교 분석 함수
 */
CREATE OR REPLACE FUNCTION analyze_perspective_differences(
  target_keyword TEXT,
  perspective_1 TEXT,
  perspective_2 TEXT
)
RETURNS JSONB AS $$
DECLARE
  interp_1 RECORD;
  interp_2 RECORD;
  result JSONB;
BEGIN
  -- 첫 번째 관점 해석 조회
  SELECT * INTO interp_1 
  FROM dream_multi_perspective_view 
  WHERE keyword = target_keyword AND perspective_code = perspective_1
  LIMIT 1;
  
  -- 두 번째 관점 해석 조회
  SELECT * INTO interp_2 
  FROM dream_multi_perspective_view 
  WHERE keyword = target_keyword AND perspective_code = perspective_2
  LIMIT 1;
  
  -- 비교 결과 생성
  result := jsonb_build_object(
    'keyword', target_keyword,
    'perspective_1', jsonb_build_object(
      'code', perspective_1,
      'name', interp_1.perspective_name,
      'cultural_origin', interp_1.cultural_origin,
      'fortune_aspect', interp_1.fortune_aspect,
      'confidence', interp_1.confidence_score,
      'interpretation', interp_1.modern_meaning
    ),
    'perspective_2', jsonb_build_object(
      'code', perspective_2,
      'name', interp_2.perspective_name,
      'cultural_origin', interp_2.cultural_origin,
      'fortune_aspect', interp_2.fortune_aspect,
      'confidence', interp_2.confidence_score,
      'interpretation', interp_2.modern_meaning
    ),
    'comparison', jsonb_build_object(
      'fortune_agreement', CASE 
        WHEN interp_1.fortune_aspect = interp_2.fortune_aspect THEN true 
        ELSE false 
      END,
      'confidence_gap', ABS(interp_1.confidence_score - interp_2.confidence_score),
      'cultural_difference', CASE 
        WHEN interp_1.cultural_origin = interp_2.cultural_origin THEN 'same_culture'
        ELSE 'cross_cultural'
      END
    )
  );
  
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- ====================================
-- 🎭 8. 다각도 해석 샘플 데이터
-- ====================================

/**
 * 같은 꿈("뱀")에 대한 다양한 관점의 해석 샘플
 */

-- 한국 전통 해몽
INSERT INTO dream_interpretations 
(keyword, keyword_variants, category_id, traditional_meaning, modern_meaning, fortune_aspect, confidence_score, 
 perspective_id, source_institution, source_author, interpretation_priority, data_source) VALUES
('뱀', ARRAY['독사', '비단뱀', '구렁이'], 5,
 '뱀은 전통적으로 길몽의 대표격입니다. 특히 집으로 들어오는 뱀은 재물과 복이 들어온다는 의미로, 사업 번창과 금전적 이익을 상징합니다.',
 '새로운 기회와 재물운이 상승하는 시기입니다. 특히 투자나 사업에서 좋은 결과를 얻을 수 있는 길몽입니다.',
 'positive', 0.9, 1, '한국전통문화포털', '주공', 1, '주공해몽'),

-- 중국 전통 해몽  
('뱀', ARRAY['蛇', '龙蛇'], 5,
 '중국 고전에서 뱀은 지혜와 변화의 상징입니다. 특히 용과 함께 나타나는 뱀은 승천과 출세를 의미하며, 학문적 성취나 관운을 나타냅니다.',
 '지혜가 증가하고 학습능력이 향상되는 시기입니다. 시험이나 승진에서 좋은 결과를 기대할 수 있습니다.',
 'positive', 0.85, 2, '중국몽서대전', '주공단', 2, '중국 고전 해몽서'),

-- 서양 심리학
('뱀', ARRAY['serpent', 'snake'], 5,
 '융의 분석심리학에서 뱀은 무의식의 원시적 에너지와 생명력을 상징합니다. 개인의 그림자 원형이나 억압된 욕망이 의식으로 떠오르는 과정을 나타냅니다.',
 '내면의 변화와 성장 과정을 겪고 있습니다. 억압되었던 감정이나 욕구가 표면화되어 새로운 자아를 발견하게 됩니다.',
 'neutral', 0.75, 3, '융 연구소', '칼 구스타프 융', 3, '분석심리학 이론'),

-- 이슬람 해몽
('뱀', ARRAY['ثعبان', 'حية'], 5,
 '이슬람 전통에서 뱀은 적이나 유혹자를 상징하기도 하지만, 맥락에 따라 지혜로운 조언자나 치유의 상징이 되기도 합니다.',
 '주변 환경을 주의깊게 살펴보고 현명한 판단이 필요한 시기입니다. 특히 인간관계에서 신중함이 요구됩니다.',
 'warning', 0.7, 5, '이슬람 해몽학회', '이븐 시린', 4, '이슬람 꿈해석서');

-- ====================================
-- 🎭 9. 관점별 통계 초기화
-- ====================================

/**
 * 각 관점별 기본 통계 데이터 생성
 */
INSERT INTO perspective_statistics (perspective_id, total_interpretations)
SELECT ip.id, COUNT(di.id)
FROM interpretation_perspectives ip
LEFT JOIN dream_interpretations di ON ip.id = di.perspective_id
GROUP BY ip.id;

-- ====================================
-- 🎭 10. 자동 업데이트 트리거들
-- ====================================

/**
 * 새로운 해석 추가 시 통계 업데이트
 */
CREATE OR REPLACE FUNCTION update_perspective_stats()
RETURNS TRIGGER AS $$
BEGIN
  -- 새 해석 추가 시
  IF TG_OP = 'INSERT' AND NEW.perspective_id IS NOT NULL THEN
    INSERT INTO perspective_statistics (perspective_id, total_interpretations)
    VALUES (NEW.perspective_id, 1)
    ON CONFLICT (perspective_id) 
    DO UPDATE SET 
      total_interpretations = perspective_statistics.total_interpretations + 1,
      last_updated = CURRENT_TIMESTAMP;
  END IF;
  
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_perspective_stats
  AFTER INSERT OR UPDATE ON dream_interpretations
  FOR EACH ROW
  EXECUTE FUNCTION update_perspective_stats();

-- ====================================
-- 🎭 11. 관리자용 품질 관리 뷰
-- ====================================

/**
 * 관점별 데이터 품질 현황 뷰
 */
CREATE VIEW perspective_quality_report AS
SELECT 
  ip.korean_name,
  ip.perspective_code,
  ps.total_interpretations,
  ps.average_user_rating,
  ps.accuracy_score,
  COUNT(DISTINCT di.keyword) as unique_keywords_covered,
  AVG(di.confidence_score) as avg_confidence,
  STRING_AGG(DISTINCT dc.korean_name, ', ') as covered_categories
FROM interpretation_perspectives ip
LEFT JOIN perspective_statistics ps ON ip.id = ps.perspective_id
LEFT JOIN dream_interpretations di ON ip.id = di.perspective_id
LEFT JOIN dream_categories dc ON di.category_id = dc.id
GROUP BY ip.id, ip.korean_name, ip.perspective_code, ps.total_interpretations, 
         ps.average_user_rating, ps.accuracy_score
ORDER BY ps.total_interpretations DESC;