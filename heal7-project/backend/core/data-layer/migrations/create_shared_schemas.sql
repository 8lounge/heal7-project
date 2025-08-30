-- ====================================
-- 공통 스키마 및 기본 테이블 생성
-- ====================================

-- shared_common 스키마에 기본 users 테이블 생성
CREATE TABLE IF NOT EXISTS shared_common.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    phone VARCHAR(20),
    birth_date DATE,
    gender VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE
);

-- dashboard_service 스키마에 기본 테이블들 생성
CREATE TABLE IF NOT EXISTS dashboard_service.system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(12,4),
    metric_data JSONB,
    service_name VARCHAR(50),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dashboard_service.service_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(50) NOT NULL,
    log_level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ai_monitoring_service 스키마에 기본 테이블들 생성
CREATE TABLE IF NOT EXISTS ai_monitoring_service.ai_usage_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    request_count INTEGER DEFAULT 1,
    total_tokens INTEGER DEFAULT 0,
    cost_usd DECIMAL(10,6) DEFAULT 0.00,
    date_recorded DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_users_email ON shared_common.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON shared_common.users(username);
CREATE INDEX IF NOT EXISTS idx_system_metrics_service ON dashboard_service.system_metrics(service_name);
CREATE INDEX IF NOT EXISTS idx_service_logs_service ON dashboard_service.service_logs(service_name, created_at);
CREATE INDEX IF NOT EXISTS idx_ai_stats_service ON ai_monitoring_service.ai_usage_stats(service_name, date_recorded);