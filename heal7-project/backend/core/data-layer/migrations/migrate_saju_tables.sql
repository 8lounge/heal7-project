-- ====================================
-- HEAL7_SAJU -> HEAL7 테이블 마이그레이션
-- 날짜: 2025-08-29
-- ====================================

-- heal7 데이터베이스에 연결
\c heal7;

-- saju_service 스키마가 있는지 확인
CREATE SCHEMA IF NOT EXISTS saju_service;

-- heal7_saju 데이터베이스에서 테이블 구조와 데이터 복사

-- 1. KASI 캐시 테이블
CREATE TABLE saju_service.kasi_cache AS 
SELECT * FROM dblink('host=localhost dbname=heal7_saju user=postgres', 
    'SELECT * FROM kasi_cache') AS t(
        id text,
        cache_key text,
        cache_data text,
        created_at timestamp,
        expires_at timestamp
    );

-- 2. 사주 해석 테이블
CREATE TABLE saju_service.saju_interpretations AS
SELECT * FROM dblink('host=localhost dbname=heal7_saju user=postgres',
    'SELECT * FROM saju_interpretations') AS t(
        id text,
        user_id text,
        birth_info text,
        interpretation_data text,
        created_at timestamp
    );

-- 3. 사주 결과 테이블  
CREATE TABLE saju_service.saju_results AS
SELECT * FROM dblink('host=localhost dbname=heal7_saju user=postgres',
    'SELECT * FROM saju_results') AS t(
        id text,
        user_id text,
        calculation_data text,
        result_data text,
        created_at timestamp
    );

-- 4. 시스템 설정 테이블
CREATE TABLE saju_service.system_settings AS
SELECT * FROM dblink('host=localhost dbname=heal7_saju user=postgres',
    'SELECT * FROM system_settings') AS t(
        id text,
        setting_key text,
        setting_value text,
        created_at timestamp,
        updated_at timestamp
    );

-- 5. 사주DB의 사용자 테이블은 shared_common으로 이관
CREATE SCHEMA IF NOT EXISTS shared_common;
CREATE TABLE shared_common.saju_users AS
SELECT * FROM dblink('host=localhost dbname=heal7_saju user=postgres',
    'SELECT * FROM users') AS t(
        id text,
        username text,
        email text,
        created_at timestamp
    );