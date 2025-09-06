-- 꿈풀이 다각도 해석 시스템 테이블 생성
-- 6개 문화적 관점별 해석 데이터를 저장

CREATE TABLE IF NOT EXISTS dream_service.multi_perspective_interpretations (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(50) NOT NULL,
    keyword_id INTEGER NOT NULL, -- 1-50번 키워드 번호
    category VARCHAR(30) NOT NULL, -- 동물, 자연현상, 인간관계, 상황감정, 사물
    
    -- 6개 관점별 해석 데이터
    korean_traditional JSONB NOT NULL, -- {interpretation, fortune_type, confidence_score}
    chinese_traditional JSONB NOT NULL,
    western_psychology JSONB NOT NULL,
    islamic_perspective JSONB NOT NULL,
    buddhist_perspective JSONB NOT NULL,
    scientific_perspective JSONB NOT NULL,
    
    -- 메타데이터
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    quality_score DECIMAL(3,1) DEFAULT 8.0, -- 전체 품질 점수 (6.0-10.0)
    
    -- 인덱스용 필드
    primary_fortune_type VARCHAR(20), -- 주요 길흉 판별 (길몽/흉몽/길흉반반/중립)
    average_confidence DECIMAL(3,1), -- 6개 관점 평균 신뢰도
    
    UNIQUE(keyword_id),
    UNIQUE(keyword)
);

-- 인덱스 생성
CREATE INDEX idx_multi_perspective_keyword ON dream_service.multi_perspective_interpretations(keyword);
CREATE INDEX idx_multi_perspective_category ON dream_service.multi_perspective_interpretations(category);
CREATE INDEX idx_multi_perspective_fortune_type ON dream_service.multi_perspective_interpretations(primary_fortune_type);
CREATE INDEX idx_multi_perspective_quality ON dream_service.multi_perspective_interpretations(quality_score DESC);

-- 코멘트 추가
COMMENT ON TABLE dream_service.multi_perspective_interpretations IS '꿈풀이 6개 관점별 해석 시스템 - 50개 핵심 키워드';
COMMENT ON COLUMN dream_service.multi_perspective_interpretations.korean_traditional IS '한국전통 관점 해석 (JSON: interpretation, fortune_type, confidence_score)';
COMMENT ON COLUMN dream_service.multi_perspective_interpretations.chinese_traditional IS '중국전통 관점 해석 (주공해몽, 풍수지리)';
COMMENT ON COLUMN dream_service.multi_perspective_interpretations.western_psychology IS '서구심리학 관점 해석 (프로이드, 융)';
COMMENT ON COLUMN dream_service.multi_perspective_interpretations.islamic_perspective IS '이슬람 관점 해석 (쿠란, 하디스)';
COMMENT ON COLUMN dream_service.multi_perspective_interpretations.buddhist_perspective IS '불교 관점 해석 (업보론, 윤회사상)';
COMMENT ON COLUMN dream_service.multi_perspective_interpretations.scientific_perspective IS '과학적 관점 해석 (신경과학, 진화심리학)';

-- 업데이트 트리거 함수 생성
CREATE OR REPLACE FUNCTION update_multi_perspective_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 업데이트 트리거 생성
DROP TRIGGER IF EXISTS trigger_update_multi_perspective_timestamp 
    ON dream_service.multi_perspective_interpretations;
    
CREATE TRIGGER trigger_update_multi_perspective_timestamp
    BEFORE UPDATE ON dream_service.multi_perspective_interpretations
    FOR EACH ROW
    EXECUTE FUNCTION update_multi_perspective_timestamp();

-- 샘플 조회 쿼리
/*
-- 특정 키워드의 모든 관점 조회
SELECT 
    keyword,
    category,
    korean_traditional->>'interpretation' as korean_interp,
    korean_traditional->>'fortune_type' as korean_fortune,
    chinese_traditional->>'interpretation' as chinese_interp,
    western_psychology->>'interpretation' as western_interp,
    primary_fortune_type,
    average_confidence,
    quality_score
FROM dream_service.multi_perspective_interpretations 
WHERE keyword = '뱀';

-- 카테고리별 키워드 목록 조회
SELECT category, array_agg(keyword ORDER BY keyword_id) as keywords
FROM dream_service.multi_perspective_interpretations 
GROUP BY category;

-- 길몽 키워드 상위 10개 (신뢰도 순)
SELECT keyword, primary_fortune_type, average_confidence, quality_score
FROM dream_service.multi_perspective_interpretations 
WHERE primary_fortune_type = '길몽' 
ORDER BY average_confidence DESC, quality_score DESC 
LIMIT 10;
*/