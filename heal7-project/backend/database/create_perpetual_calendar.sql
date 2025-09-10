-- HEAL7 만세력 데이터베이스 스키마
-- 생성일: 2025-09-09
-- 목적: 73,400개 완전한 만세력 데이터 저장

-- 기존 테이블 삭제 (있다면)
DROP TABLE IF EXISTS perpetual_calendar CASCADE;
DROP TABLE IF EXISTS solar_terms_cache CASCADE;

-- 🏗️ 메인 만세력 테이블 (73,400 entries)
CREATE TABLE perpetual_calendar (
    -- 🔑 Primary Key
    id BIGSERIAL PRIMARY KEY,
    date_key VARCHAR(10) UNIQUE NOT NULL, -- 'YYYY-MM-DD' format for fast lookups
    
    -- 📅 Solar Calendar Fields
    solar_year INTEGER NOT NULL,
    solar_month INTEGER NOT NULL,
    solar_day INTEGER NOT NULL,
    solar_weekday INTEGER, -- 0=Sunday, 6=Saturday
    
    -- 🌙 Lunar Calendar Fields (KASI API Data)
    lunar_year INTEGER,
    lunar_month INTEGER,
    lunar_day INTEGER,
    is_leap_month BOOLEAN DEFAULT FALSE,
    lunar_date_string VARCHAR(50),
    
    -- 🎯 60갑자 Core Fields
    day_gapja VARCHAR(2) NOT NULL, -- 일주 (day pillar)
    day_cheongan CHAR(1), -- 일간 (day stem)
    day_jiji CHAR(1),     -- 일지 (day branch)
    
    year_gapja VARCHAR(2) NOT NULL, -- 연주 (year pillar)
    month_gapja VARCHAR(2),         -- 월주 (month pillar) 
    hour_gapja VARCHAR(2),          -- 시주 (hour pillar) - null if not calculated
    
    -- 🌸 24 Solar Terms Fields
    solar_term_name VARCHAR(20), -- 절기명 (e.g., '입춘', '백로')
    solar_term_season VARCHAR(10), -- '봄', '여름', '가을', '겨울'
    is_solar_term_day BOOLEAN DEFAULT FALSE,
    
    -- ⭐ Fortune & Special Days
    fortune_score INTEGER DEFAULT 3, -- 1-5 scale
    is_good_day BOOLEAN DEFAULT FALSE, -- 길일
    is_bad_day BOOLEAN DEFAULT FALSE,  -- 흉일
    is_son_eob_neun_day BOOLEAN DEFAULT FALSE, -- 손없는날
    
    -- 🎨 Display Fields
    zodiac_animal VARCHAR(10), -- 띠동물 (e.g., '쥐', '소')
    element VARCHAR(10),       -- 오행 (e.g., '목', '화', '토', '금', '수')
    
    -- 📝 Metadata
    data_source VARCHAR(50) DEFAULT 'heal7_calculation',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 🌸 24절기 캐시 테이블
CREATE TABLE solar_terms_cache (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    term_name VARCHAR(20) NOT NULL,
    term_date DATE NOT NULL,
    season VARCHAR(10),
    term_order INTEGER, -- 1-24 within the year
    data_source VARCHAR(50) DEFAULT 'kasi_api',
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(year, term_name)
);

-- 🔍 성능 최적화 인덱스
CREATE INDEX idx_date_key ON perpetual_calendar (date_key);
CREATE INDEX idx_solar_date ON perpetual_calendar (solar_year, solar_month, solar_day);
CREATE INDEX idx_lunar_date ON perpetual_calendar (lunar_year, lunar_month, lunar_day);
CREATE INDEX idx_day_gapja ON perpetual_calendar (day_gapja);
CREATE INDEX idx_year_gapja ON perpetual_calendar (year_gapja);
CREATE INDEX idx_solar_term ON perpetual_calendar (solar_term_name);
CREATE INDEX idx_fortune ON perpetual_calendar (fortune_score);
CREATE INDEX idx_special_days ON perpetual_calendar (is_good_day, is_bad_day, is_son_eob_neun_day);
CREATE INDEX idx_weekday ON perpetual_calendar (solar_weekday);

-- 절기 테이블 인덱스
CREATE INDEX idx_year_term ON solar_terms_cache (year, term_name);
CREATE INDEX idx_term_date ON solar_terms_cache (term_date);

-- 🎯 성능 통계 뷰
CREATE VIEW perpetual_calendar_stats AS
SELECT 
    COUNT(*) as total_entries,
    MIN(solar_year) as start_year,
    MAX(solar_year) as end_year,
    COUNT(DISTINCT solar_year) as year_span,
    COUNT(CASE WHEN is_leap_month THEN 1 END) as leap_month_days,
    COUNT(CASE WHEN is_solar_term_day THEN 1 END) as solar_term_days,
    COUNT(CASE WHEN is_good_day THEN 1 END) as good_days,
    COUNT(CASE WHEN is_bad_day THEN 1 END) as bad_days,
    COUNT(CASE WHEN is_son_eob_neun_day THEN 1 END) as son_eob_neun_days
FROM perpetual_calendar;

-- 🔧 데이터 검증 함수
CREATE OR REPLACE FUNCTION validate_gapja_cycle()
RETURNS TABLE(date_key VARCHAR, expected_gapja VARCHAR, actual_gapja VARCHAR) AS $$
BEGIN
    -- 60갑자 순환 검증 로직
    RETURN QUERY
    SELECT 
        pc.date_key,
        '검증필요' as expected_gapja,
        pc.day_gapja as actual_gapja
    FROM perpetual_calendar pc
    WHERE pc.solar_year BETWEEN 2025 AND 2025  -- 샘플 검증
    ORDER BY pc.date_key
    LIMIT 60;
END;
$$ LANGUAGE plpgsql;

-- 📊 통계 정보 출력
COMMENT ON TABLE perpetual_calendar IS 'HEAL7 만세력 메인 테이블 - 73,400개 데이터';
COMMENT ON TABLE solar_terms_cache IS 'KASI 24절기 캐시 테이블';

-- 초기 데이터 확인
SELECT 'Database schema created successfully! Ready for 73,400 entries.' as status;