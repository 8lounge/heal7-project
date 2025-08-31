-- ====================================
-- 꿈풀이 원시 데이터 대량 수집 테이블
-- "무분별한 수집 → 체계적 분류" 전략
-- ====================================

-- JSONB 확장 프로그램 활성화
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ====================================
-- 📦 원시 데이터 수집 테이블
-- ====================================
CREATE TABLE IF NOT EXISTS dream_raw_collection (
    id BIGSERIAL PRIMARY KEY,
    
    -- 수집 메타데이터
    source_site VARCHAR(200) NOT NULL,
    source_url TEXT,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scraper_version VARCHAR(20) DEFAULT 'v1.0',
    
    -- 원시 데이터 (완전 자유형식 JSONB)
    raw_content JSONB NOT NULL,
    
    -- 수집 품질 관리
    collection_status VARCHAR(20) DEFAULT 'collected', -- collected, processing, processed, failed
    quality_hints JSONB DEFAULT '{}', -- 품질 힌트 (키워드 개수, 텍스트 길이 등)
    
    -- 처리 상태 관리  
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed, skipped
    processed_at TIMESTAMP WITH TIME ZONE,
    processing_notes TEXT,
    
    -- 분류 후 연결
    final_dream_id BIGINT REFERENCES dream_interpretations(id),
    
    -- 에러 처리
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    
    -- 중복 체크용 해시
    content_hash VARCHAR(64) UNIQUE, -- 중복 방지용
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================
-- 🔍 검색 및 성능 최적화 인덱스
-- ====================================

-- 기본 조회 인덱스
CREATE INDEX idx_dream_raw_source ON dream_raw_collection(source_site);
CREATE INDEX idx_dream_raw_scraped_at ON dream_raw_collection(scraped_at DESC);
CREATE INDEX idx_dream_raw_collection_status ON dream_raw_collection(collection_status);
CREATE INDEX idx_dream_raw_processing_status ON dream_raw_collection(processing_status);

-- JSONB 검색 최적화
CREATE INDEX idx_dream_raw_content_gin ON dream_raw_collection USING gin(raw_content);
CREATE INDEX idx_dream_raw_quality_hints ON dream_raw_collection USING gin(quality_hints);

-- 중복 체크 최적화
CREATE INDEX idx_dream_raw_content_hash ON dream_raw_collection(content_hash);

-- 복합 인덱스 (자주 사용되는 쿼리용)
CREATE INDEX idx_dream_raw_site_status ON dream_raw_collection(source_site, processing_status);
CREATE INDEX idx_dream_raw_pending ON dream_raw_collection(processing_status) WHERE processing_status = 'pending';

-- ====================================
-- 🔧 자동 업데이트 트리거
-- ====================================
CREATE OR REPLACE FUNCTION update_dream_raw_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_dream_raw_updated_at
    BEFORE UPDATE ON dream_raw_collection
    FOR EACH ROW EXECUTE FUNCTION update_dream_raw_updated_at();

-- ====================================
-- 📊 수집 통계 뷰
-- ====================================
CREATE OR REPLACE VIEW dream_collection_stats AS
SELECT 
    source_site,
    COUNT(*) as total_collected,
    COUNT(*) FILTER (WHERE processing_status = 'pending') as pending_count,
    COUNT(*) FILTER (WHERE processing_status = 'completed') as completed_count,
    COUNT(*) FILTER (WHERE processing_status = 'in_progress') as processing_count,
    COUNT(*) FILTER (WHERE error_count > 0) as error_count,
    AVG((quality_hints->>'text_length')::int) as avg_text_length,
    MAX(scraped_at) as last_scraped,
    MIN(scraped_at) as first_scraped
FROM dream_raw_collection 
GROUP BY source_site
ORDER BY total_collected DESC;

-- ====================================
-- 🧹 관리용 함수들
-- ====================================

-- 중복 데이터 정리 함수
CREATE OR REPLACE FUNCTION clean_duplicate_raw_dreams()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    WITH duplicates AS (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY content_hash ORDER BY scraped_at DESC) as rn
        FROM dream_raw_collection
        WHERE content_hash IS NOT NULL
    )
    DELETE FROM dream_raw_collection 
    WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 오래된 에러 데이터 정리
CREATE OR REPLACE FUNCTION clean_old_error_dreams(days_old INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM dream_raw_collection 
    WHERE error_count >= 5 
      AND scraped_at < CURRENT_TIMESTAMP - INTERVAL '1 day' * days_old;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 통계 요약 함수
CREATE OR REPLACE FUNCTION get_collection_summary()
RETURNS TABLE(
    metric VARCHAR(50),
    value BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'total_collected'::VARCHAR(50), COUNT(*)::BIGINT FROM dream_raw_collection
    UNION ALL
    SELECT 'pending_processing'::VARCHAR(50), COUNT(*)::BIGINT FROM dream_raw_collection WHERE processing_status = 'pending'
    UNION ALL
    SELECT 'completed_processing'::VARCHAR(50), COUNT(*)::BIGINT FROM dream_raw_collection WHERE processing_status = 'completed'
    UNION ALL
    SELECT 'unique_sources'::VARCHAR(50), COUNT(DISTINCT source_site)::BIGINT FROM dream_raw_collection
    UNION ALL
    SELECT 'today_collected'::VARCHAR(50), COUNT(*)::BIGINT FROM dream_raw_collection WHERE DATE(scraped_at) = CURRENT_DATE;
END;
$$ LANGUAGE plpgsql;

-- ====================================
-- 📝 샘플 데이터 (테스트용)
-- ====================================
INSERT INTO dream_raw_collection (source_site, source_url, raw_content, content_hash) VALUES
('test_site.com', 'https://test_site.com/dream/1', 
 '{"title": "물꿈해몽", "content": "맑은 물을 마시는 꿈은 좋은 운을 의미합니다", "category": "자연"}', 
 md5('{"title": "물꿈해몽", "content": "맑은 물을 마시는 꿈은 좋은 운을 의미합니다", "category": "자연"}')
),
('test_site.com', 'https://test_site.com/dream/2', 
 '{"keyword": "뱀", "traditional": "뱀꿈은 재물운 상승", "modern": "변화와 성장의 상징"}', 
 md5('{"keyword": "뱀", "traditional": "뱀꿈은 재물운 상승", "modern": "변화와 성장의 상징"}')
);

-- 권한 설정
-- ALTER TABLE dream_raw_collection OWNER TO heal7_admin;
-- GRANT ALL PRIVILEGES ON dream_raw_collection TO heal7_admin;

COMMENT ON TABLE dream_raw_collection IS '꿈풀이 원시 데이터 대량 수집 테이블 - 무분별 수집 후 체계적 분류 전략';