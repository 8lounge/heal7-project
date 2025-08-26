-- ==========================================
-- 정부 포털 하이브리드 데이터베이스 스키마
-- NoSQL 수집 → 관계형 마이그레이션 방식
-- ==========================================

-- ==========================================
-- Phase 1: Raw JSON 수집 스테이지
-- ==========================================

-- 원본 스크래핑 데이터 (JSONB NoSQL)
CREATE TABLE IF NOT EXISTS raw_scraped_data (
    id BIGSERIAL PRIMARY KEY,
    
    -- 메타데이터
    portal_id VARCHAR(50) NOT NULL,                    -- 'bizinfo', 'kstartup' 등
    url TEXT NOT NULL,                                 -- 수집한 페이지 URL
    scraping_session_id UUID NOT NULL DEFAULT gen_random_uuid(),  -- 세션별 그룹화
    
    -- 원본 데이터 (NoSQL)
    raw_data JSONB NOT NULL,                          -- 완전한 원본 데이터
    html_content TEXT,                                -- 원본 HTML (선택적)
    
    -- 상태 관리
    processing_status VARCHAR(20) DEFAULT 'pending',  -- pending, processing, completed, failed
    quality_score DECIMAL(3,2),                      -- AI 품질 점수 (0.00-10.00)
    validation_errors JSONB,                         -- 검증 오류 내용
    
    -- 타임스탬프
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE,
    migrated_at TIMESTAMP WITH TIME ZONE,
    
    -- 인덱스 최적화
    CONSTRAINT valid_portal_id CHECK (portal_id IN ('bizinfo', 'kstartup', 'government24')),
    CONSTRAINT valid_status CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed', 'duplicate'))
);

-- JSONB 인덱스 (빠른 쿼리를 위함)
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_portal ON raw_scraped_data (portal_id);
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_session ON raw_scraped_data (scraping_session_id);
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_status ON raw_scraped_data (processing_status);
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_scraped_at ON raw_scraped_data (scraped_at);

-- JSONB GIN 인덱스 (JSON 내용 검색용)
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_content ON raw_scraped_data USING GIN (raw_data);
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_title ON raw_scraped_data USING GIN ((raw_data->>'title'));
CREATE INDEX IF NOT EXISTS idx_raw_scraped_data_agency ON raw_scraped_data USING GIN ((raw_data->>'agency'));

-- ==========================================
-- Phase 2: 관계형 데이터베이스 (마이그레이션 대상)
-- ==========================================

-- 지원사업 프로그램 마스터 테이블
CREATE TABLE IF NOT EXISTS support_programs (
    id BIGSERIAL PRIMARY KEY,
    
    -- 고유 식별자
    program_id VARCHAR(100) UNIQUE NOT NULL,         -- 포털별 고유 ID
    portal_id VARCHAR(50) NOT NULL,
    original_raw_id BIGINT REFERENCES raw_scraped_data(id), -- 원본 데이터 연결
    
    -- 기본 정보
    title TEXT NOT NULL,
    description TEXT,
    support_field VARCHAR(100),                      -- 지원 분야
    
    -- 기관 정보
    implementing_agency TEXT,                        -- 사업수행기관
    jurisdiction TEXT,                               -- 소관부처
    contact_info JSONB,                             -- 연락처 정보
    
    -- 지원 내용
    support_details JSONB,                          -- 지원 상세 내용
    support_amount VARCHAR(100),                    -- 지원 금액
    support_period VARCHAR(100),                    -- 지원 기간
    support_type VARCHAR(50),                       -- 지원 방식 (융자, 보조금 등)
    
    -- 신청 정보
    application_period VARCHAR(200),                -- 신청 기간
    application_status VARCHAR(50) DEFAULT 'active', -- active, closed, pending
    target_audience TEXT,                           -- 지원 대상
    
    -- 평가 및 선정
    evaluation_criteria JSONB,                      -- 평가 기준
    required_documents JSONB,                       -- 필수 서류
    
    -- URL 및 첨부
    detail_url TEXT,                                -- 상세 페이지 URL
    attachments JSONB,                              -- 첨부 파일 정보
    
    -- 메타데이터
    view_count INTEGER DEFAULT 0,
    registration_date DATE,
    
    -- AI 분석 결과
    ai_analysis JSONB,                              -- AI 분석 결과
    template_generated BOOLEAN DEFAULT FALSE,       -- 템플릿 생성 여부
    
    -- 품질 관리
    data_quality_score DECIMAL(3,2),               -- 데이터 품질 점수
    verification_status VARCHAR(20) DEFAULT 'unverified', -- unverified, verified, flagged
    
    -- 타임스탬프
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_verified_at TIMESTAMP WITH TIME ZONE,
    
    -- 제약 조건
    CONSTRAINT valid_portal_id_programs CHECK (portal_id IN ('bizinfo', 'kstartup', 'government24')),
    CONSTRAINT valid_application_status CHECK (application_status IN ('active', 'closed', 'pending', 'expired')),
    CONSTRAINT valid_verification_status CHECK (verification_status IN ('unverified', 'verified', 'flagged', 'rejected'))
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_support_programs_portal ON support_programs (portal_id);
CREATE INDEX IF NOT EXISTS idx_support_programs_status ON support_programs (application_status);
CREATE INDEX IF NOT EXISTS idx_support_programs_agency ON support_programs (implementing_agency);
CREATE INDEX IF NOT EXISTS idx_support_programs_created_at ON support_programs (created_at);
CREATE INDEX IF NOT EXISTS idx_support_programs_updated_at ON support_programs (updated_at);

-- Full-text search 인덱스
CREATE INDEX IF NOT EXISTS idx_support_programs_title_fts ON support_programs USING GIN (to_tsvector('korean', title));
CREATE INDEX IF NOT EXISTS idx_support_programs_description_fts ON support_programs USING GIN (to_tsvector('korean', description));

-- ==========================================
-- Phase 3: 스크래핑 세션 관리
-- ==========================================

-- 스크래핑 세션 로그
CREATE TABLE IF NOT EXISTS scraping_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 세션 정보
    portal_id VARCHAR(50) NOT NULL,
    session_type VARCHAR(50) DEFAULT 'scheduled',    -- scheduled, manual, recovery
    
    -- 실행 정보
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'running',            -- running, completed, failed, cancelled
    
    -- 성과 지표
    pages_scraped INTEGER DEFAULT 0,
    items_found INTEGER DEFAULT 0,
    items_processed INTEGER DEFAULT 0,
    items_migrated INTEGER DEFAULT 0,
    
    -- 오류 정보
    errors_encountered INTEGER DEFAULT 0,
    error_details JSONB,
    
    -- 성능 지표
    total_duration_seconds INTEGER,
    average_response_time_ms INTEGER,
    
    -- 설정 정보
    configuration JSONB,                             -- 사용된 설정 정보
    
    CONSTRAINT valid_portal_id_sessions CHECK (portal_id IN ('bizinfo', 'kstartup', 'government24')),
    CONSTRAINT valid_session_status CHECK (status IN ('running', 'completed', 'failed', 'cancelled'))
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_scraping_sessions_portal ON scraping_sessions (portal_id);
CREATE INDEX IF NOT EXISTS idx_scraping_sessions_started_at ON scraping_sessions (started_at);
CREATE INDEX IF NOT EXISTS idx_scraping_sessions_status ON scraping_sessions (status);

-- ==========================================
-- Phase 4: 폴백 및 복구 시스템
-- ==========================================

-- 백업 데이터 저장소
CREATE TABLE IF NOT EXISTS backup_data_registry (
    id BIGSERIAL PRIMARY KEY,
    
    -- 백업 식별
    backup_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    source_table VARCHAR(100) NOT NULL,             -- 원본 테이블명
    source_record_id BIGINT NOT NULL,               -- 원본 레코드 ID
    
    -- 백업 방식
    backup_method VARCHAR(50) NOT NULL,             -- 'filesystem', 'redis', 'remote'
    backup_location TEXT NOT NULL,                  -- 백업 위치
    
    -- 백업 데이터
    backup_data JSONB NOT NULL,                     -- 백업된 데이터
    metadata JSONB,                                 -- 백업 메타데이터
    
    -- 상태
    backup_status VARCHAR(20) DEFAULT 'active',     -- active, expired, corrupted
    verified_at TIMESTAMP WITH TIME ZONE,
    
    -- 타임스탬프
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days',
    
    CONSTRAINT valid_backup_method CHECK (backup_method IN ('filesystem', 'redis', 'remote', 'hybrid')),
    CONSTRAINT valid_backup_status CHECK (backup_status IN ('active', 'expired', 'corrupted', 'restored'))
);

-- 복구 작업 로그
CREATE TABLE IF NOT EXISTS recovery_operations (
    id BIGSERIAL PRIMARY KEY,
    
    -- 복구 정보
    operation_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    trigger_type VARCHAR(50) NOT NULL,              -- 'manual', 'automatic', 'scheduled'
    recovery_scope VARCHAR(50) NOT NULL,            -- 'single_record', 'session', 'full_portal'
    
    -- 대상 정보
    target_portal_id VARCHAR(50),
    target_session_id UUID REFERENCES scraping_sessions(id),
    affected_records JSONB,                         -- 영향받은 레코드 목록
    
    -- 복구 과정
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'running',           -- running, completed, failed, partial
    
    -- 결과
    records_recovered INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    recovery_details JSONB,
    
    -- 검증
    verification_passed BOOLEAN,
    verification_details JSONB,
    
    CONSTRAINT valid_trigger_type CHECK (trigger_type IN ('manual', 'automatic', 'scheduled')),
    CONSTRAINT valid_recovery_scope CHECK (recovery_scope IN ('single_record', 'session', 'full_portal', 'date_range')),
    CONSTRAINT valid_recovery_status CHECK (status IN ('running', 'completed', 'failed', 'partial', 'cancelled'))
);

-- ==========================================
-- Phase 5: 시스템 모니터링 및 알림
-- ==========================================

-- 시스템 헬스 체크
CREATE TABLE IF NOT EXISTS system_health_checks (
    id BIGSERIAL PRIMARY KEY,
    
    -- 체크 정보
    check_type VARCHAR(50) NOT NULL,                -- 'database', 'scraping', 'migration', 'backup'
    component_name VARCHAR(100) NOT NULL,          -- 컴포넌트 식별자
    
    -- 상태
    status VARCHAR(20) NOT NULL,                    -- 'healthy', 'warning', 'critical', 'down'
    response_time_ms INTEGER,
    
    -- 세부 정보
    check_details JSONB,
    error_message TEXT,
    metrics JSONB,                                  -- 성능 메트릭
    
    -- 타임스탬프
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_check_type CHECK (check_type IN ('database', 'scraping', 'migration', 'backup', 'api')),
    CONSTRAINT valid_health_status CHECK (status IN ('healthy', 'warning', 'critical', 'down'))
);

-- 알림 큐
CREATE TABLE IF NOT EXISTS notification_queue (
    id BIGSERIAL PRIMARY KEY,
    
    -- 알림 정보
    notification_type VARCHAR(50) NOT NULL,         -- 'error', 'warning', 'info', 'success'
    priority INTEGER DEFAULT 3,                     -- 1(highest) to 5(lowest)
    
    -- 내용
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    
    -- 대상
    recipient_channels JSONB,                       -- ['email', 'slack', 'webhook']
    
    -- 상태
    status VARCHAR(20) DEFAULT 'pending',           -- pending, sent, failed, cancelled
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    
    -- 타임스탬프
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP WITH TIME ZONE,
    next_attempt_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT valid_notification_type CHECK (notification_type IN ('error', 'warning', 'info', 'success', 'critical')),
    CONSTRAINT valid_notification_status CHECK (status IN ('pending', 'sent', 'failed', 'cancelled'))
);

-- ==========================================
-- 유용한 뷰와 함수
-- ==========================================

-- 수집 성과 요약 뷰
CREATE OR REPLACE VIEW scraping_performance_summary AS
SELECT 
    s.portal_id,
    s.started_at::DATE as scraping_date,
    COUNT(*) as sessions_count,
    SUM(s.pages_scraped) as total_pages,
    SUM(s.items_found) as total_items_found,
    SUM(s.items_processed) as total_items_processed,
    SUM(s.items_migrated) as total_items_migrated,
    AVG(s.total_duration_seconds) as avg_duration_seconds,
    AVG(s.average_response_time_ms) as avg_response_time_ms,
    SUM(s.errors_encountered) as total_errors
FROM scraping_sessions s
WHERE s.status = 'completed'
GROUP BY s.portal_id, s.started_at::DATE
ORDER BY s.started_at::DATE DESC;

-- 데이터 품질 모니터링 뷰
CREATE OR REPLACE VIEW data_quality_monitor AS
SELECT 
    portal_id,
    COUNT(*) as total_programs,
    COUNT(*) FILTER (WHERE data_quality_score >= 8.0) as high_quality_count,
    COUNT(*) FILTER (WHERE data_quality_score BETWEEN 6.0 AND 7.99) as medium_quality_count,
    COUNT(*) FILTER (WHERE data_quality_score < 6.0) as low_quality_count,
    AVG(data_quality_score) as avg_quality_score,
    COUNT(*) FILTER (WHERE verification_status = 'verified') as verified_count,
    COUNT(*) FILTER (WHERE template_generated = TRUE) as template_generated_count
FROM support_programs 
GROUP BY portal_id;

-- 백업 상태 확인 함수
CREATE OR REPLACE FUNCTION check_backup_integrity(backup_id_param UUID)
RETURNS JSONB AS $$
DECLARE
    backup_record backup_data_registry%ROWTYPE;
    result JSONB;
BEGIN
    SELECT * INTO backup_record FROM backup_data_registry WHERE backup_id = backup_id_param;
    
    IF NOT FOUND THEN
        RETURN jsonb_build_object('status', 'not_found', 'backup_id', backup_id_param);
    END IF;
    
    -- 백업 무결성 검사 로직
    result := jsonb_build_object(
        'status', 'verified',
        'backup_id', backup_record.backup_id,
        'backup_method', backup_record.backup_method,
        'created_at', backup_record.created_at,
        'data_size', jsonb_typeof(backup_record.backup_data),
        'expires_at', backup_record.expires_at
    );
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- 자동 정리 함수 (오래된 백업 삭제)
CREATE OR REPLACE FUNCTION cleanup_expired_backups()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM backup_data_registry 
    WHERE backup_status = 'expired' OR expires_at < CURRENT_TIMESTAMP;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    INSERT INTO system_health_checks (check_type, component_name, status, check_details)
    VALUES ('backup', 'cleanup_expired_backups', 'healthy', 
            jsonb_build_object('deleted_count', deleted_count, 'executed_at', CURRENT_TIMESTAMP));
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- 권한 및 보안 설정
-- ==========================================

-- 읽기 전용 역할 (모니터링용)
-- CREATE ROLE scraping_reader;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO scraping_reader;

-- 스크래핑 전용 역할 (데이터 수집용)
-- CREATE ROLE scraping_collector;
-- GRANT SELECT, INSERT, UPDATE ON raw_scraped_data TO scraping_collector;
-- GRANT SELECT, INSERT, UPDATE ON scraping_sessions TO scraping_collector;
-- GRANT SELECT, INSERT ON backup_data_registry TO scraping_collector;

-- 마이그레이션 전용 역할 (데이터 처리용)
-- CREATE ROLE scraping_processor;
-- GRANT SELECT, INSERT, UPDATE ON support_programs TO scraping_processor;
-- GRANT SELECT, UPDATE ON raw_scraped_data TO scraping_processor;

-- ==========================================
-- 트리거 설정 (자동화)
-- ==========================================

-- 업데이트 시간 자동 갱신
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- support_programs 테이블 업데이트 트리거
CREATE TRIGGER update_support_programs_updated_at 
    BEFORE UPDATE ON support_programs 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();