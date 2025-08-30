-- ====================================
-- HEAL7 데이터베이스 스키마 분류 마이그레이션
-- 
-- PostgreSQL SCHEMA 기능을 활용한 서비스 큐브별 분류
-- 기존 public 스키마의 혼재된 테이블들을 논리적으로 분리
-- 
-- @author HEAL7 Team  
-- @version 2.0.0 (큐브 모듈러 아키텍처)
-- ====================================

-- ====================================
-- 1️⃣ 서비스별 SCHEMA 생성
-- ====================================

-- 사주명리학 서비스 스키마
CREATE SCHEMA IF NOT EXISTS saju_service;
COMMENT ON SCHEMA saju_service IS '사주명리학 계산 및 해석 관련 테이블';

-- 크롤링 서비스 스키마  
CREATE SCHEMA IF NOT EXISTS crawling_service;
COMMENT ON SCHEMA crawling_service IS '데이터 수집 및 크롤링 관련 테이블 (JSONB 중심)';

-- 대시보드 서비스 스키마
CREATE SCHEMA IF NOT EXISTS dashboard_service;
COMMENT ON SCHEMA dashboard_service IS '관리자 대시보드 및 시스템 관리 테이블';

-- 서류 처리 서비스 스키마
CREATE SCHEMA IF NOT EXISTS paperwork_service;
COMMENT ON SCHEMA paperwork_service IS '서류 처리 및 OCR 관련 테이블';

-- AI 모니터링 서비스 스키마
CREATE SCHEMA IF NOT EXISTS ai_monitoring_service;
COMMENT ON SCHEMA ai_monitoring_service IS 'AI 성능 모니터링 및 로그 테이블';

-- 공통 스키마 (모든 서비스가 참조하는 공통 데이터)
CREATE SCHEMA IF NOT EXISTS shared_common;
COMMENT ON SCHEMA shared_common IS '모든 서비스가 공유하는 공통 테이블';

-- ====================================
-- 2️⃣ 사주 서비스 (saju_service) 테이블
-- ====================================

-- 사주 차트 기본 정보 (기존 public.saju_charts 이동)
CREATE TABLE saju_service.saju_charts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL, -- shared_common.users 참조
  
  -- 출생 정보
  birth_year INTEGER NOT NULL,
  birth_month INTEGER NOT NULL, 
  birth_day INTEGER NOT NULL,
  birth_hour INTEGER NOT NULL,
  birth_minute INTEGER DEFAULT 0,
  
  -- 사주 구성 요소 (간지)
  year_cheongan VARCHAR(2) NOT NULL,
  year_jiji VARCHAR(2) NOT NULL,
  month_cheongan VARCHAR(2) NOT NULL,
  month_jiji VARCHAR(2) NOT NULL,
  day_cheongan VARCHAR(2) NOT NULL,
  day_jiji VARCHAR(2) NOT NULL,
  hour_cheongan VARCHAR(2) NOT NULL,
  hour_jiji VARCHAR(2) NOT NULL,
  
  -- 오행 균형
  wood_count INTEGER DEFAULT 0,
  fire_count INTEGER DEFAULT 0,
  earth_count INTEGER DEFAULT 0,
  metal_count INTEGER DEFAULT 0,
  water_count INTEGER DEFAULT 0,
  
  -- 계산 메타데이터
  kasi_solar_term VARCHAR(20),
  lunar_calendar_date DATE,
  solar_calendar_date DATE,
  
  calculated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  calculator_version VARCHAR(10) DEFAULT '2.0.0'
);

-- 대운 정보 (기존 public.daewoon_cycles 이동)
CREATE TABLE saju_service.daewoon_cycles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL REFERENCES saju_service.saju_charts(id) ON DELETE CASCADE,
  
  cycle_number INTEGER NOT NULL,
  start_age INTEGER NOT NULL,
  end_age INTEGER NOT NULL,
  cheongan VARCHAR(2) NOT NULL,
  jiji VARCHAR(2) NOT NULL,
  wuxing_element VARCHAR(10),
  strength_score DECIMAL(3,1),
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 세운 정보 (기존 public.sewoon_cycles 이동)
CREATE TABLE saju_service.sewoon_cycles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL REFERENCES saju_service.saju_charts(id) ON DELETE CASCADE,
  
  target_year INTEGER NOT NULL,
  age INTEGER NOT NULL,
  cheongan VARCHAR(2) NOT NULL,
  jiji VARCHAR(2) NOT NULL,
  wuxing_element VARCHAR(10),
  fortune_score DECIMAL(3,1),
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(saju_chart_id, target_year)
);

-- 궁합 분석 결과 (기존 public.compatibility_analyses 이동)
CREATE TABLE saju_service.compatibility_analyses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  primary_chart_id UUID NOT NULL REFERENCES saju_service.saju_charts(id) ON DELETE CASCADE,
  secondary_chart_id UUID NOT NULL REFERENCES saju_service.saju_charts(id) ON DELETE CASCADE,
  
  overall_score DECIMAL(3,1) NOT NULL,
  personality_score DECIMAL(3,1),
  career_score DECIMAL(3,1),
  health_score DECIMAL(3,1),
  wealth_score DECIMAL(3,1),
  
  analysis_type VARCHAR(20) NOT NULL DEFAULT 'romantic',
  analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  analyzer_version VARCHAR(10) DEFAULT '2.0.0'
);

-- ====================================
-- 3️⃣ 크롤링 서비스 (crawling_service) 테이블
-- ====================================

-- 정부포털 스크래핑 데이터 (JSONB)
CREATE TABLE crawling_service.government_portal_data (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  portal_source VARCHAR(50) NOT NULL, -- 'bizinfo', 'kstartup' 등
  source_url TEXT NOT NULL,
  scraping_session_id UUID NOT NULL DEFAULT uuid_generate_v4(),
  
  -- JSONB 원본 데이터
  raw_data JSONB NOT NULL,
  
  processing_status VARCHAR(20) DEFAULT 'raw',
  quality_score DECIMAL(3,2),
  validation_errors JSONB,
  
  scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  processed_at TIMESTAMP WITH TIME ZONE
);

-- 꿈풀이 데이터 (JSONB) - 기존 dream 테이블들 통합
CREATE TABLE crawling_service.dream_interpretation_data (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  source_website VARCHAR(100) NOT NULL,
  source_url TEXT NOT NULL,
  dream_category VARCHAR(50),
  
  -- JSONB 꿈풀이 데이터
  dream_data JSONB NOT NULL,
  
  interpretation_type VARCHAR(20) DEFAULT 'traditional',
  quality_rating INTEGER CHECK (quality_rating BETWEEN 1 AND 10),
  duplicate_check_hash VARCHAR(64),
  
  scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 스크래핑 세션 관리
CREATE TABLE crawling_service.scraping_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  session_name VARCHAR(100) NOT NULL,
  scraping_target VARCHAR(100) NOT NULL,
  scraping_type VARCHAR(50) NOT NULL,
  
  total_urls INTEGER DEFAULT 0,
  completed_urls INTEGER DEFAULT 0,
  failed_urls INTEGER DEFAULT 0,
  success_rate DECIMAL(5,2) DEFAULT 0.00,
  
  scraping_config JSONB NOT NULL,
  session_stats JSONB DEFAULT '{}',
  session_status VARCHAR(20) DEFAULT 'pending',
  
  started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP WITH TIME ZONE
);

-- ====================================
-- 4️⃣ 대시보드 서비스 (dashboard_service) 테이블
-- ====================================

-- 관리자 사용자 (기존 public.admin_users 이동)
CREATE TABLE dashboard_service.admin_users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  
  full_name VARCHAR(100),
  role VARCHAR(20) DEFAULT 'admin', -- admin, super_admin, viewer
  permissions JSONB DEFAULT '{}',
  
  last_login_at TIMESTAMP WITH TIME ZONE,
  is_active BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 시스템 로그 (기존 public.system_logs 이동)
CREATE TABLE dashboard_service.system_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  log_level VARCHAR(10) NOT NULL, -- DEBUG, INFO, WARN, ERROR, CRITICAL
  service_name VARCHAR(50) NOT NULL, -- saju_service, crawling_service 등
  log_message TEXT NOT NULL,
  log_data JSONB,
  
  user_id UUID, -- 사용자 관련 로그인 경우
  ip_address INET,
  user_agent TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 큐브 상태 모니터링 (새로 추가)
CREATE TABLE dashboard_service.cube_status (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  cube_name VARCHAR(50) NOT NULL, -- saju-service, crawling-service 등
  cube_type VARCHAR(50) NOT NULL, -- main, fortune-cube, dream-cube 등
  status VARCHAR(20) DEFAULT 'running', -- running, stopped, error, maintenance
  
  health_check_data JSONB DEFAULT '{}',
  performance_metrics JSONB DEFAULT '{}',
  last_heartbeat TIMESTAMP WITH TIME ZONE,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================
-- 5️⃣ 서류 처리 서비스 (paperwork_service) 테이블
-- ====================================

-- 문서 메타데이터 (새로 추가)
CREATE TABLE paperwork_service.documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  user_id UUID NOT NULL, -- shared_common.users 참조
  file_name VARCHAR(255) NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  
  document_type VARCHAR(50), -- contract, invoice, certificate 등
  processing_status VARCHAR(20) DEFAULT 'uploaded', -- uploaded, processing, completed, failed
  
  upload_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  processed_timestamp TIMESTAMP WITH TIME ZONE
);

-- OCR 결과 (JSONB 사용)
CREATE TABLE paperwork_service.ocr_results (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID NOT NULL REFERENCES paperwork_service.documents(id) ON DELETE CASCADE,
  
  -- OCR 원본 결과 (JSONB)
  raw_ocr_data JSONB NOT NULL,
  
  -- 추출된 텍스트
  extracted_text TEXT,
  confidence_score DECIMAL(3,2),
  
  ocr_engine VARCHAR(50), -- tesseract, google_vision, aws_textract
  processing_time_seconds DECIMAL(5,2),
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================
-- 6️⃣ AI 모니터링 서비스 (ai_monitoring_service) 테이블
-- ====================================

-- AI 모델 성능 로그 (새로 추가)
CREATE TABLE ai_monitoring_service.ai_performance_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  model_name VARCHAR(100) NOT NULL, -- gpt-4, claude-3, local_model 등
  service_context VARCHAR(50) NOT NULL, -- saju_interpretation, ocr_processing 등
  
  request_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  response_time_ms INTEGER NOT NULL,
  token_usage JSONB, -- {input_tokens: 100, output_tokens: 50, total_cost: 0.02}
  
  success BOOLEAN DEFAULT true,
  error_message TEXT,
  confidence_score DECIMAL(3,2),
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI 모델 메트릭 (새로 추가)  
CREATE TABLE ai_monitoring_service.model_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  model_name VARCHAR(100) NOT NULL,
  metric_date DATE DEFAULT CURRENT_DATE,
  
  total_requests INTEGER DEFAULT 0,
  successful_requests INTEGER DEFAULT 0,
  failed_requests INTEGER DEFAULT 0,
  average_response_time_ms DECIMAL(8,2),
  total_tokens_used INTEGER DEFAULT 0,
  estimated_cost DECIMAL(10,4),
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(model_name, metric_date)
);

-- ====================================
-- 7️⃣ 공통 스키마 (shared_common) 테이블
-- ====================================

-- 사용자 정보 (모든 서비스가 참조)
CREATE TABLE shared_common.users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  
  full_name VARCHAR(100),
  birth_date DATE,
  birth_time TIME,
  birth_location JSONB,
  gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
  
  preferred_language VARCHAR(10) DEFAULT 'ko',
  timezone VARCHAR(50) DEFAULT 'Asia/Seoul',
  notification_settings JSONB DEFAULT '{}',
  privacy_settings JSONB DEFAULT '{}',
  
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  last_login_at TIMESTAMP WITH TIME ZONE,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 세션 (모든 서비스가 참조)
CREATE TABLE shared_common.user_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES shared_common.users(id) ON DELETE CASCADE,
  session_token VARCHAR(255) UNIQUE NOT NULL,
  refresh_token VARCHAR(255) UNIQUE,
  
  ip_address INET,
  user_agent TEXT,
  device_info JSONB,
  
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  is_active BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================
-- 8️⃣ 인덱스 생성
-- ====================================

-- saju_service 인덱스
CREATE INDEX idx_saju_charts_user_id ON saju_service.saju_charts(user_id);
CREATE INDEX idx_saju_charts_birth_date ON saju_service.saju_charts(birth_year, birth_month, birth_day);
CREATE INDEX idx_daewoon_chart_id ON saju_service.daewoon_cycles(saju_chart_id);
CREATE INDEX idx_sewoon_chart_id ON saju_service.sewoon_cycles(saju_chart_id);
CREATE INDEX idx_compatibility_primary ON saju_service.compatibility_analyses(primary_chart_id);

-- crawling_service 인덱스 (JSONB GIN 인덱스)
CREATE INDEX idx_govt_data_gin ON crawling_service.government_portal_data USING GIN (raw_data);
CREATE INDEX idx_dream_data_gin ON crawling_service.dream_interpretation_data USING GIN (dream_data);
CREATE INDEX idx_govt_portal_source ON crawling_service.government_portal_data(portal_source);
CREATE INDEX idx_dream_source ON crawling_service.dream_interpretation_data(source_website);

-- dashboard_service 인덱스
CREATE INDEX idx_admin_users_email ON dashboard_service.admin_users(email);
CREATE INDEX idx_system_logs_level ON dashboard_service.system_logs(log_level);
CREATE INDEX idx_system_logs_service ON dashboard_service.system_logs(service_name);
CREATE INDEX idx_cube_status_name ON dashboard_service.cube_status(cube_name);

-- paperwork_service 인덱스
CREATE INDEX idx_documents_user_id ON paperwork_service.documents(user_id);
CREATE INDEX idx_documents_status ON paperwork_service.documents(processing_status);
CREATE INDEX idx_ocr_document_id ON paperwork_service.ocr_results(document_id);
CREATE INDEX idx_ocr_data_gin ON paperwork_service.ocr_results USING GIN (raw_ocr_data);

-- ai_monitoring_service 인덱스
CREATE INDEX idx_ai_perf_model ON ai_monitoring_service.ai_performance_logs(model_name);
CREATE INDEX idx_ai_perf_context ON ai_monitoring_service.ai_performance_logs(service_context);
CREATE INDEX idx_ai_metrics_model ON ai_monitoring_service.model_metrics(model_name);

-- shared_common 인덱스
CREATE INDEX idx_users_email ON shared_common.users(email);
CREATE INDEX idx_users_username ON shared_common.users(username);
CREATE INDEX idx_sessions_user_id ON shared_common.user_sessions(user_id);
CREATE INDEX idx_sessions_token ON shared_common.user_sessions(session_token);

-- ====================================
-- 9️⃣ 권한 및 보안 설정
-- ====================================

-- 각 서비스별 사용자 생성 (운영환경 권장)
-- CREATE USER saju_service_user WITH PASSWORD 'secure_password';
-- CREATE USER crawling_service_user WITH PASSWORD 'secure_password';
-- CREATE USER dashboard_service_user WITH PASSWORD 'secure_password';
-- CREATE USER paperwork_service_user WITH PASSWORD 'secure_password';
-- CREATE USER ai_monitoring_service_user WITH PASSWORD 'secure_password';

-- 스키마별 권한 부여 예시
-- GRANT USAGE ON SCHEMA saju_service TO saju_service_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA saju_service TO saju_service_user;
-- GRANT USAGE ON SCHEMA shared_common TO saju_service_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA shared_common TO saju_service_user;

-- ====================================
-- 🔟 마이그레이션 가이드
-- ====================================

/*
기존 public 스키마의 테이블들을 새 스키마로 이동하는 방법:

1. 데이터 백업
   pg_dump -h localhost -U postgres -d heal7_db > backup_$(date +%Y%m%d).sql

2. 기존 테이블 이름 변경 (안전한 마이그레이션)
   ALTER TABLE public.saju_charts RENAME TO saju_charts_old;
   ALTER TABLE public.users RENAME TO users_old;

3. 새 스키마 구조 생성 (이 파일 실행)
   psql -h localhost -U postgres -d heal7_db -f DATABASE_SCHEMA_MIGRATION.sql

4. 데이터 마이그레이션
   INSERT INTO saju_service.saju_charts SELECT * FROM public.saju_charts_old;
   INSERT INTO shared_common.users SELECT * FROM public.users_old;

5. 검증 후 기존 테이블 삭제
   DROP TABLE public.saju_charts_old;
   DROP TABLE public.users_old;

6. 애플리케이션 코드 업데이트 (스키마 경로 포함)
   FROM: SELECT * FROM saju_charts
   TO:   SELECT * FROM saju_service.saju_charts
*/