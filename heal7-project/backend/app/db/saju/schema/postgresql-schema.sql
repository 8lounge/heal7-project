-- ====================================
-- HEAL7 사주명리학 PostgreSQL 데이터베이스 스키마
-- 
-- 프론트엔드 직접 연동용 DB 설계
-- PostgreSQL을 주 저장소로, Redis를 캐시로 활용하는 하이브리드 구조
-- 
-- @author HEAL7 Team
-- @version 1.0.0
-- @license MIT
-- ====================================

-- 데이터베이스 생성 (필요시)
-- CREATE DATABASE heal7_saju_db;
-- \c heal7_saju_db;

-- 확장 프로그램 설치
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "hstore";

-- ====================================
-- 🎯 1. 사용자 관리 테이블
-- ====================================

/**
 * 사용자 정보 테이블
 * 사주 서비스 이용자들의 기본 정보 저장
 */
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  
  -- 개인 정보
  full_name VARCHAR(100),
  birth_date DATE,
  birth_time TIME,
  birth_location JSONB, -- { "city": "서울", "district": "강남구", "lat": 37.5665, "lng": 126.9780 }
  gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
  
  -- 사용자 설정
  preferred_language VARCHAR(10) DEFAULT 'ko',
  timezone VARCHAR(50) DEFAULT 'Asia/Seoul',
  notification_settings JSONB DEFAULT '{}',
  privacy_settings JSONB DEFAULT '{}',
  
  -- 계정 상태
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  last_login_at TIMESTAMP WITH TIME ZONE,
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_birth_date ON users(birth_date);
CREATE INDEX idx_users_created_at ON users(created_at);

/**
 * 사용자 세션 테이블
 * JWT 토큰과 연계하여 세션 관리
 */
CREATE TABLE user_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_token VARCHAR(255) UNIQUE NOT NULL,
  refresh_token VARCHAR(255) UNIQUE,
  
  -- 세션 정보
  ip_address INET,
  user_agent TEXT,
  device_info JSONB,
  
  -- 만료 관리
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  is_active BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- ====================================
-- 🎯 2. 사주 데이터 테이블
-- ====================================

/**
 * 사주 정보 메인 테이블
 * 계산된 사주의 핵심 정보 저장
 */
CREATE TABLE saju_charts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  
  -- 기본 정보
  name VARCHAR(100) NOT NULL, -- 사주 주인 이름
  birth_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
  birth_location JSONB, -- 출생지 정보
  gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
  
  -- 시간대 보정 정보
  original_datetime TIMESTAMP WITH TIME ZONE NOT NULL, -- 원본 시간
  corrected_datetime TIMESTAMP WITH TIME ZONE NOT NULL, -- 보정된 시간 (진태양시)
  timezone_correction_minutes INTEGER DEFAULT 0,
  
  -- 사주 4기둥 정보
  year_pillar JSONB NOT NULL, -- { "heavenly": "갑", "earthly": "자", "sixtyGapja": "갑자", "wuxing": "목", "yinyang": "양" }
  month_pillar JSONB NOT NULL,
  day_pillar JSONB NOT NULL,
  hour_pillar JSONB NOT NULL,
  
  -- 핵심 분석 결과
  day_master VARCHAR(5) NOT NULL, -- 일간 (본인의 기본 성격)
  saju_formatted VARCHAR(50) NOT NULL, -- "갑자 병인 정묘 무진" 형태
  
  -- 오행 분석
  wuxing_balance JSONB NOT NULL, -- { "목": 2.5, "화": 1.0, "토": 2.0, "금": 1.5, "수": 1.0 }
  wuxing_score INTEGER NOT NULL CHECK (wuxing_score >= 0 AND wuxing_score <= 100),
  wuxing_recommendation TEXT,
  
  -- 십신 분석
  sipsin_analysis JSONB, -- 각 기둥별 십신 정보
  
  -- 메타데이터
  calculation_version VARCHAR(20) DEFAULT '1.0.0',
  is_public BOOLEAN DEFAULT false, -- 공개 사주 여부
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX idx_saju_charts_user_id ON saju_charts(user_id);
CREATE INDEX idx_saju_charts_birth_datetime ON saju_charts(birth_datetime);
CREATE INDEX idx_saju_charts_day_master ON saju_charts(day_master);
CREATE INDEX idx_saju_charts_created_at ON saju_charts(created_at);
CREATE INDEX idx_saju_charts_is_public ON saju_charts(is_public);

/**
 * 대운(大運) 정보 테이블
 * 10년 단위 큰 운세 정보
 */
CREATE TABLE daewoon_periods (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL REFERENCES saju_charts(id) ON DELETE CASCADE,
  
  -- 대운 기간
  period_order INTEGER NOT NULL, -- 1, 2, 3... (몇 번째 대운인지)
  start_age INTEGER NOT NULL,
  end_age INTEGER NOT NULL,
  start_date DATE,
  end_date DATE,
  
  -- 대운 기둥 정보
  heavenly_stem VARCHAR(5) NOT NULL,
  earthly_branch VARCHAR(5) NOT NULL,
  sixty_gapja VARCHAR(10) NOT NULL,
  wuxing VARCHAR(5) NOT NULL,
  yinyang VARCHAR(5) NOT NULL,
  
  -- 십신 분석
  sipsin VARCHAR(10) NOT NULL,
  sipsin_description TEXT,
  
  -- 운세 분석
  general_fortune TEXT,
  career_fortune TEXT,
  relationship_fortune TEXT,
  health_fortune TEXT,
  financial_fortune TEXT,
  
  -- 추천 사항
  recommendations JSONB,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_daewoon_saju_chart_id ON daewoon_periods(saju_chart_id);
CREATE INDEX idx_daewoon_period_order ON daewoon_periods(period_order);

/**
 * 세운(歲運) 정보 테이블
 * 연도별 운세 정보
 */
CREATE TABLE sewoon_years (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL REFERENCES saju_charts(id) ON DELETE CASCADE,
  
  -- 세운 연도
  target_year INTEGER NOT NULL,
  user_age INTEGER NOT NULL,
  
  -- 세운 기둥 정보
  heavenly_stem VARCHAR(5) NOT NULL,
  earthly_branch VARCHAR(5) NOT NULL,
  sixty_gapja VARCHAR(10) NOT NULL,
  wuxing VARCHAR(5) NOT NULL,
  yinyang VARCHAR(5) NOT NULL,
  
  -- 십신 분석
  sipsin VARCHAR(10) NOT NULL,
  
  -- 상세 운세 분석
  overall_fortune_score INTEGER CHECK (overall_fortune_score >= 0 AND overall_fortune_score <= 100),
  fortune_description TEXT,
  advice TEXT,
  
  -- 월별 세부 운세 (선택사항)
  monthly_fortune JSONB, -- { "1": {...}, "2": {...}, ... }
  
  -- 중요 시기 표시
  is_critical_year BOOLEAN DEFAULT false,
  critical_events JSONB, -- 주요 사건들
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sewoon_saju_chart_id ON sewoon_years(saju_chart_id);
CREATE INDEX idx_sewoon_target_year ON sewoon_years(target_year);
CREATE UNIQUE INDEX idx_sewoon_chart_year ON sewoon_years(saju_chart_id, target_year);

-- ====================================
-- 🎯 3. 궁합 분석 테이블
-- ====================================

/**
 * 궁합 분석 결과 테이블
 * 두 사주 간의 궁합 분석 정보
 */
CREATE TABLE compatibility_analysis (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- 분석 대상
  primary_chart_id UUID NOT NULL REFERENCES saju_charts(id) ON DELETE CASCADE,
  secondary_chart_id UUID NOT NULL REFERENCES saju_charts(id) ON DELETE CASCADE,
  analysis_type VARCHAR(20) NOT NULL CHECK (analysis_type IN ('romantic', 'business', 'friendship', 'family')),
  
  -- 궁합 점수
  overall_score INTEGER NOT NULL CHECK (overall_score >= 0 AND overall_score <= 100),
  
  -- 세부 점수
  day_master_compatibility INTEGER CHECK (day_master_compatibility >= 0 AND day_master_compatibility <= 100),
  wuxing_balance_score INTEGER CHECK (wuxing_balance_score >= 0 AND wuxing_balance_score <= 100),
  year_pillar_harmony INTEGER CHECK (year_pillar_harmony >= 0 AND year_pillar_harmony <= 100),
  
  -- 분석 결과
  compatibility_grade VARCHAR(10) NOT NULL, -- 'excellent', 'good', 'average', 'challenging'
  summary_description TEXT NOT NULL,
  
  -- 장점과 개선점
  strengths JSONB NOT NULL, -- ["서로를 성장시키는 상생의 관계", ...]
  improvements JSONB NOT NULL, -- ["상극 관계이므로 서로를 이해하려는 노력이 필요", ...]
  
  -- 관계별 조언
  relationship_advice TEXT,
  conflict_resolution_tips JSONB,
  
  -- 메타데이터
  analyzed_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  is_public BOOLEAN DEFAULT false,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_compatibility_primary_chart ON compatibility_analysis(primary_chart_id);
CREATE INDEX idx_compatibility_secondary_chart ON compatibility_analysis(secondary_chart_id);
CREATE INDEX idx_compatibility_type ON compatibility_analysis(analysis_type);
CREATE INDEX idx_compatibility_score ON compatibility_analysis(overall_score);

-- ====================================
-- 🎯 4. AI 분석 및 예측 테이블
-- ====================================

/**
 * AI 분석 결과 테이블
 * 머신러닝/AI 모델의 분석 결과 저장
 */
CREATE TABLE ai_analysis_results (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL REFERENCES saju_charts(id) ON DELETE CASCADE,
  
  -- AI 모델 정보
  model_name VARCHAR(100) NOT NULL, -- 'gpt-4', 'gemini-pro', 'claude-3' 등
  model_version VARCHAR(50),
  analysis_type VARCHAR(50) NOT NULL, -- 'personality', 'career', 'health', 'fortune'
  
  -- 분석 요청 정보
  input_prompt TEXT,
  analysis_parameters JSONB, -- 모델별 설정값들
  
  -- AI 분석 결과
  raw_response TEXT NOT NULL, -- AI의 원본 응답
  structured_result JSONB, -- 구조화된 분석 결과
  confidence_score DECIMAL(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
  
  -- 결과 분류
  key_insights JSONB, -- 핵심 통찰들
  predictions JSONB, -- 예측 결과들
  recommendations JSONB, -- 추천 사항들
  
  -- 품질 관리
  human_validation_status VARCHAR(20) DEFAULT 'pending' CHECK (human_validation_status IN ('pending', 'approved', 'rejected', 'needs_review')),
  validation_notes TEXT,
  validated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  validated_at TIMESTAMP WITH TIME ZONE,
  
  -- 사용 통계
  view_count INTEGER DEFAULT 0,
  feedback_score DECIMAL(3,2), -- 사용자 피드백 점수 (1.00 ~ 5.00)
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_analysis_saju_chart ON ai_analysis_results(saju_chart_id);
CREATE INDEX idx_ai_analysis_model ON ai_analysis_results(model_name);
CREATE INDEX idx_ai_analysis_type ON ai_analysis_results(analysis_type);
CREATE INDEX idx_ai_analysis_confidence ON ai_analysis_results(confidence_score);

/**
 * AI 모델 성능 추적 테이블
 * 각 AI 모델의 성능을 모니터링
 */
CREATE TABLE ai_model_performance (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- 모델 정보
  model_name VARCHAR(100) NOT NULL,
  model_version VARCHAR(50),
  analysis_type VARCHAR(50) NOT NULL,
  
  -- 성능 지표
  total_analyses INTEGER DEFAULT 0,
  average_confidence DECIMAL(5,4),
  average_user_rating DECIMAL(3,2),
  accuracy_rate DECIMAL(5,4), -- 검증된 결과 기준
  
  -- 비용 정보
  total_tokens_used BIGINT DEFAULT 0,
  total_cost DECIMAL(10,4) DEFAULT 0.00,
  average_response_time_ms INTEGER,
  
  -- 시간 범위
  measurement_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
  measurement_period_end TIMESTAMP WITH TIME ZONE NOT NULL,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_performance_model ON ai_model_performance(model_name);
CREATE INDEX idx_ai_performance_period ON ai_model_performance(measurement_period_start, measurement_period_end);

-- ====================================
-- 🎯 5. 통계 및 분석 테이블
-- ====================================

/**
 * 사주 통계 테이블
 * 다양한 사주 패턴의 통계 정보
 */
CREATE TABLE saju_statistics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- 통계 분류
  statistic_type VARCHAR(50) NOT NULL, -- 'day_master_frequency', 'wuxing_distribution', 'birth_year_trend'
  category VARCHAR(100), -- 세부 카테고리
  
  -- 통계 데이터
  data_point VARCHAR(50) NOT NULL, -- '갑', '목', '1990' 등
  count INTEGER NOT NULL DEFAULT 0,
  percentage DECIMAL(5,2),
  
  -- 추가 메타데이터
  additional_data JSONB,
  
  -- 집계 정보
  calculation_date DATE NOT NULL,
  total_sample_size INTEGER NOT NULL,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_saju_statistics_type ON saju_statistics(statistic_type);
CREATE INDEX idx_saju_statistics_category ON saju_statistics(category);
CREATE INDEX idx_saju_statistics_data_point ON saju_statistics(data_point);
CREATE UNIQUE INDEX idx_saju_statistics_unique ON saju_statistics(statistic_type, category, data_point, calculation_date);

/**
 * 사용자 활동 로그 테이블
 * 사용자의 서비스 이용 패턴 분석용
 */
CREATE TABLE user_activity_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  session_id UUID REFERENCES user_sessions(id) ON DELETE SET NULL,
  
  -- 활동 정보
  activity_type VARCHAR(50) NOT NULL, -- 'saju_calculation', 'compatibility_analysis', 'page_view'
  activity_details JSONB,
  
  -- 요청 정보
  request_ip INET,
  user_agent TEXT,
  referrer TEXT,
  page_url TEXT,
  
  -- 성능 정보
  response_time_ms INTEGER,
  status_code INTEGER,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_logs_user_id ON user_activity_logs(user_id);
CREATE INDEX idx_activity_logs_activity_type ON user_activity_logs(activity_type);
CREATE INDEX idx_activity_logs_created_at ON user_activity_logs(created_at);

-- ====================================
-- 🎯 6. 시스템 관리 테이블
-- ====================================

/**
 * 시스템 설정 테이블
 * 애플리케이션의 전역 설정값들
 */
CREATE TABLE system_settings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- 설정 키-값
  setting_key VARCHAR(100) UNIQUE NOT NULL,
  setting_value TEXT,
  setting_type VARCHAR(20) DEFAULT 'string' CHECK (setting_type IN ('string', 'number', 'boolean', 'json')),
  
  -- 설정 메타데이터
  description TEXT,
  is_public BOOLEAN DEFAULT false, -- 프론트엔드에서 접근 가능한지
  requires_restart BOOLEAN DEFAULT false, -- 변경시 서버 재시작 필요한지
  
  -- 변경 추적
  created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  updated_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_system_settings_key ON system_settings(setting_key);
CREATE INDEX idx_system_settings_is_public ON system_settings(is_public);

/**
 * 데이터베이스 마이그레이션 테이블
 * 스키마 변경 이력 관리
 */
CREATE TABLE db_migrations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- 마이그레이션 정보
  migration_name VARCHAR(255) UNIQUE NOT NULL,
  migration_version VARCHAR(50) NOT NULL,
  migration_description TEXT,
  
  -- 실행 정보
  executed_sql TEXT,
  execution_time_ms INTEGER,
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'rolled_back')),
  error_message TEXT,
  
  -- 실행자 정보
  executed_by VARCHAR(100),
  
  executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_db_migrations_version ON db_migrations(migration_version);
CREATE INDEX idx_db_migrations_status ON db_migrations(status);

-- ====================================
-- 🎯 7. 트리거 및 함수
-- ====================================

/**
 * 업데이트 시간 자동 갱신 트리거 함수
 */
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- 각 테이블에 업데이트 트리거 적용
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_saju_charts_updated_at BEFORE UPDATE ON saju_charts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_compatibility_analysis_updated_at BEFORE UPDATE ON compatibility_analysis
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_analysis_results_updated_at BEFORE UPDATE ON ai_analysis_results
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE ON system_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

/**
 * 사주 통계 자동 업데이트 함수
 */
CREATE OR REPLACE FUNCTION update_saju_statistics()
RETURNS TRIGGER AS $$
BEGIN
  -- 새로운 사주가 생성될 때 통계 업데이트
  IF TG_OP = 'INSERT' THEN
    -- 일간 통계 업데이트
    INSERT INTO saju_statistics (statistic_type, category, data_point, count, calculation_date, total_sample_size)
    VALUES ('day_master_frequency', 'general', NEW.day_master, 1, CURRENT_DATE, 1)
    ON CONFLICT (statistic_type, category, data_point, calculation_date)
    DO UPDATE SET 
      count = saju_statistics.count + 1,
      total_sample_size = saju_statistics.total_sample_size + 1;
    
    -- 오행 분포 통계 업데이트
    -- (여기서는 간단히 처리, 실제로는 더 복잡한 로직 필요)
    
    RETURN NEW;
  END IF;
  
  RETURN NULL;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_saju_statistics 
  AFTER INSERT ON saju_charts
  FOR EACH ROW EXECUTE FUNCTION update_saju_statistics();

-- ====================================
-- 🎯 8. 뷰(View) 정의
-- ====================================

/**
 * 사주 요약 뷰
 * 프론트엔드에서 자주 사용하는 사주 정보를 한 번에 조회
 */
CREATE VIEW v_saju_summary AS
SELECT 
  sc.id,
  sc.name,
  sc.birth_datetime,
  sc.day_master,
  sc.saju_formatted,
  sc.wuxing_score,
  sc.wuxing_recommendation,
  sc.is_public,
  sc.created_at,
  
  -- 사용자 정보 (있는 경우)
  u.username,
  u.email,
  
  -- 최신 AI 분석 결과 (있는 경우)
  (SELECT jsonb_agg(
    jsonb_build_object(
      'analysis_type', aar.analysis_type,
      'key_insights', aar.key_insights,
      'confidence_score', aar.confidence_score
    )
  )
  FROM ai_analysis_results aar 
  WHERE aar.saju_chart_id = sc.id 
    AND aar.human_validation_status = 'approved'
  ORDER BY aar.created_at DESC 
  LIMIT 3) as recent_ai_analysis

FROM saju_charts sc
LEFT JOIN users u ON sc.user_id = u.id;

/**
 * 사용자 대시보드 뷰
 * 사용자별 활동 요약 정보
 */
CREATE VIEW v_user_dashboard AS
SELECT 
  u.id as user_id,
  u.username,
  u.full_name,
  u.created_at as joined_at,
  u.last_login_at,
  
  -- 사주 관련 통계
  COUNT(DISTINCT sc.id) as total_saju_charts,
  COUNT(DISTINCT ca.id) as total_compatibility_analyses,
  COUNT(DISTINCT aar.id) as total_ai_analyses,
  
  -- 최근 활동
  MAX(sc.created_at) as last_saju_created,
  MAX(ca.created_at) as last_compatibility_analysis,
  
  -- 평균 점수들
  AVG(sc.wuxing_score) as avg_wuxing_score,
  AVG(ca.overall_score) as avg_compatibility_score

FROM users u
LEFT JOIN saju_charts sc ON u.id = sc.user_id
LEFT JOIN compatibility_analysis ca ON u.id = ca.analyzed_by_user_id
LEFT JOIN ai_analysis_results aar ON sc.id = aar.saju_chart_id
GROUP BY u.id, u.username, u.full_name, u.created_at, u.last_login_at;

-- ====================================
-- 🎯 9. 초기 데이터 삽입
-- ====================================

/**
 * 기본 시스템 설정값들
 */
INSERT INTO system_settings (setting_key, setting_value, setting_type, description, is_public) VALUES
('app_version', '1.0.0', 'string', '애플리케이션 버전', true),
('maintenance_mode', 'false', 'boolean', '점검 모드 여부', true),
('max_saju_per_user', '10', 'number', '사용자당 최대 사주 개수', false),
('ai_analysis_enabled', 'true', 'boolean', 'AI 분석 기능 활성화', true),
('default_timezone', 'Asia/Seoul', 'string', '기본 시간대', true),
('cache_ttl_seconds', '3600', 'number', '캐시 만료 시간 (초)', false);

/**
 * 기본 사주 통계 초기화
 */
INSERT INTO saju_statistics (statistic_type, category, data_point, count, calculation_date, total_sample_size) VALUES
-- 일간 빈도 초기화
('day_master_frequency', 'general', '갑', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '을', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '병', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '정', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '무', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '기', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '경', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '신', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '임', 0, CURRENT_DATE, 0),
('day_master_frequency', 'general', '계', 0, CURRENT_DATE, 0),

-- 오행 분포 초기화
('wuxing_distribution', 'general', '목', 0, CURRENT_DATE, 0),
('wuxing_distribution', 'general', '화', 0, CURRENT_DATE, 0),
('wuxing_distribution', 'general', '토', 0, CURRENT_DATE, 0),
('wuxing_distribution', 'general', '금', 0, CURRENT_DATE, 0),
('wuxing_distribution', 'general', '수', 0, CURRENT_DATE, 0);

-- ====================================
-- 🎯 10. 권한 및 보안 설정
-- ====================================

/**
 * 데이터베이스 사용자 및 권한 설정
 * (실제 배포시에는 별도 스크립트로 관리)
 */

-- 읽기 전용 사용자 (분석용)
-- CREATE USER heal7_readonly WITH PASSWORD 'secure_readonly_password';
-- GRANT CONNECT ON DATABASE heal7_saju_db TO heal7_readonly;
-- GRANT USAGE ON SCHEMA public TO heal7_readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO heal7_readonly;

-- 애플리케이션 사용자 (읽기/쓰기)
-- CREATE USER heal7_app WITH PASSWORD 'secure_app_password';
-- GRANT CONNECT ON DATABASE heal7_saju_db TO heal7_app;
-- GRANT USAGE ON SCHEMA public TO heal7_app;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO heal7_app;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO heal7_app;

/**
 * 행 레벨 보안 정책 (Row Level Security)
 * 사용자별 데이터 접근 제어
 */

-- 사주 차트에 대한 행 레벨 보안
ALTER TABLE saju_charts ENABLE ROW LEVEL SECURITY;

CREATE POLICY saju_charts_user_policy ON saju_charts
  FOR ALL
  TO heal7_app
  USING (user_id = current_setting('app.current_user_id')::uuid OR is_public = true);

-- 궁합 분석에 대한 행 레벨 보안
ALTER TABLE compatibility_analysis ENABLE ROW LEVEL SECURITY;

CREATE POLICY compatibility_analysis_user_policy ON compatibility_analysis
  FOR ALL 
  TO heal7_app
  USING (analyzed_by_user_id = current_setting('app.current_user_id')::uuid OR is_public = true);

-- ====================================
-- 🎯 마이그레이션 완료 기록
-- ====================================

INSERT INTO db_migrations (
  migration_name, 
  migration_version, 
  migration_description, 
  executed_sql, 
  status, 
  executed_by
) VALUES (
  'initial_schema_v1.0.0',
  '1.0.0',
  'HEAL7 사주명리학 초기 데이터베이스 스키마 생성',
  'Full schema creation with all tables, indexes, triggers, and initial data',
  'completed',
  'heal7_system'
);

-- ====================================
-- 🎯 스키마 검증 및 마무리
-- ====================================

/**
 * 스키마 무결성 검증
 */
DO $$
DECLARE
  table_count INTEGER;
  index_count INTEGER;
  trigger_count INTEGER;
BEGIN
  -- 테이블 수 확인
  SELECT COUNT(*) INTO table_count FROM information_schema.tables 
  WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
  
  -- 인덱스 수 확인  
  SELECT COUNT(*) INTO index_count FROM pg_indexes 
  WHERE schemaname = 'public';
  
  -- 트리거 수 확인
  SELECT COUNT(*) INTO trigger_count FROM information_schema.triggers 
  WHERE trigger_schema = 'public';
  
  RAISE NOTICE '스키마 생성 완료: 테이블 %, 인덱스 %, 트리거 %', table_count, index_count, trigger_count;
  
  IF table_count < 10 THEN
    RAISE EXCEPTION '테이블 생성이 완전하지 않습니다.';
  END IF;
END $$;

-- 스키마 버전 정보
COMMENT ON SCHEMA public IS 'HEAL7 사주명리학 데이터베이스 스키마 v1.0.0 - PostgreSQL 메인 저장소';

-- 테이블별 코멘트
COMMENT ON TABLE users IS '사용자 정보 및 인증 관리 테이블';
COMMENT ON TABLE saju_charts IS '사주 4기둥 및 분석 결과 메인 테이블';
COMMENT ON TABLE daewoon_periods IS '10년 단위 대운 정보 테이블';
COMMENT ON TABLE sewoon_years IS '연도별 세운 정보 테이블';
COMMENT ON TABLE compatibility_analysis IS '사주 궁합 분석 결과 테이블';
COMMENT ON TABLE ai_analysis_results IS 'AI 모델 분석 결과 저장 테이블';
COMMENT ON TABLE saju_statistics IS '사주 패턴 통계 및 빈도 분석 테이블';
COMMENT ON TABLE user_activity_logs IS '사용자 활동 추적 및 분석 테이블';
COMMENT ON TABLE system_settings IS '시스템 전역 설정 관리 테이블';

RAISE NOTICE '🎯 HEAL7 사주명리학 PostgreSQL 스키마 생성이 완료되었습니다!';
RAISE NOTICE '📊 총 % 개의 테이블이 생성되었으며, Redis 캐시와 연동하여 최적의 성능을 제공합니다.', 
  (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE');