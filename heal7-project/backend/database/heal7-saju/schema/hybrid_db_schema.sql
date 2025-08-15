-- HEAL7 사주 시스템 - PostgreSQL 스키마 설계
-- 프론트엔드 Next.js + 백엔드 FastAPI 완전 분리 아키텍처
-- 생성일: 2025-08-12

-- ================================
-- 1. 사용자 관리 테이블
-- ================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preferences JSONB DEFAULT '{}'::jsonb,
    user_mode VARCHAR(20) DEFAULT 'simple' CHECK (user_mode IN ('simple', 'expert'))
);

-- 사용자 설정 인덱스
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ================================
-- 2. 사주 계산 결과 테이블
-- ================================

CREATE TABLE saju_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    birth_year INTEGER NOT NULL,
    birth_month INTEGER NOT NULL,
    birth_day INTEGER NOT NULL,
    birth_hour INTEGER NOT NULL,
    birth_minute INTEGER NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')),
    
    -- 사주 4기둥
    year_pillar JSONB NOT NULL,     -- {천간, 지지, 한자천간, 한자지지}
    month_pillar JSONB NOT NULL,
    day_pillar JSONB NOT NULL,
    hour_pillar JSONB NOT NULL,
    
    -- 분석 결과
    wuxing_analysis JSONB NOT NULL, -- {목, 화, 토, 금, 수}
    sipsin_analysis JSONB NOT NULL, -- {비겁, 식상, 재성, 관살, 인성}
    
    -- 메타 정보
    calculation_engine VARCHAR(50) DEFAULT 'frontend',
    accuracy_score INTEGER DEFAULT 95,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 사주 결과 인덱스
CREATE INDEX idx_saju_results_user_id ON saju_results(user_id);
CREATE INDEX idx_saju_results_created_at ON saju_results(created_at);
CREATE INDEX idx_saju_results_birth ON saju_results(birth_year, birth_month, birth_day);

-- ================================
-- 3. 사주 해석 및 분석 테이블
-- ================================

CREATE TABLE saju_interpretations (
    id SERIAL PRIMARY KEY,
    saju_result_id INTEGER REFERENCES saju_results(id) ON DELETE CASCADE,
    
    -- 기본 해석
    personality_analysis TEXT,
    wealth_analysis TEXT,
    health_analysis TEXT,
    relationship_analysis TEXT,
    
    -- 고급 분석 (전문가 모드)
    lifecycle_analysis JSONB,      -- 대운, 세운 분석
    compatibility_notes TEXT,
    recommendation TEXT,
    
    -- AI 생성 여부
    ai_generated BOOLEAN DEFAULT false,
    analysis_source VARCHAR(50) DEFAULT 'frontend',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_interpretations_saju_result ON saju_interpretations(saju_result_id);

-- ================================
-- 4. KASI 데이터 캐시 테이블
-- ================================

CREATE TABLE kasi_cache (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    solar_terms JSONB NOT NULL,     -- 24절기 데이터
    lunar_calendar JSONB,           -- 음력 변환 데이터
    
    data_source VARCHAR(50) DEFAULT 'kasi_api',
    cache_expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- KASI 캐시 인덱스
CREATE UNIQUE INDEX idx_kasi_cache_year_month ON kasi_cache(year, month);
CREATE INDEX idx_kasi_cache_expires ON kasi_cache(cache_expires_at);

-- ================================
-- 5. 시스템 설정 테이블
-- ================================

CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value JSONB NOT NULL,
    setting_type VARCHAR(50) NOT NULL, -- 'frontend', 'backend', 'shared'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 기본 설정 데이터 삽입
INSERT INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
('frontend_cache_ttl', '{"hours": 24}', 'frontend', '프론트엔드 캐시 유효시간'),
('redis_key_prefix', '{"saju": "saju:", "user": "user:", "kasi": "kasi:"}', 'shared', 'Redis 키 prefix 설정'),
('calculation_engines', '["frontend", "hybrid", "validation"]', 'shared', '사용 가능한 계산 엔진 목록');

CREATE INDEX idx_system_settings_key ON system_settings(setting_key);
CREATE INDEX idx_system_settings_type ON system_settings(setting_type);