-- ====================================
-- HEAL7 사주명리학 서비스 JSONB 스키마
-- 
-- 복잡한 구조의 사주 해석 및 AI 분석 결과 저장
-- PostgreSQL의 JSONB 타입을 활용한 NoSQL 스타일 저장
-- 
-- @author HEAL7 Team  
-- @version 2.0.0 (큐브 모듈러 아키텍처)
-- @service saju-service
-- ====================================

-- JSONB 관련 확장 프로그램
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- JSONB 인덱스 최적화

-- ====================================
-- 🔮 1. 사주 해석 데이터
-- ====================================

/**
 * 사주 상세 해석 결과
 * AI 및 전통 명리학 해석을 JSONB로 저장
 */
CREATE TABLE saju_interpretations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL, -- core_schema의 saju_charts 참조
  
  -- 해석 카테고리
  interpretation_type VARCHAR(50) NOT NULL, -- personality, career, health, wealth, marriage
  
  -- JSONB 해석 데이터
  interpretation_data JSONB NOT NULL,
  /*
  예시 구조:
  {
    "overall": {
      "summary": "일간이 갑목으로 강한 생명력을...",
      "keywords": ["리더십", "창의성", "독립성"],
      "score": 8.5
    },
    "detailed_analysis": {
      "personality_traits": {
        "strengths": ["강한 의지력", "책임감"],
        "weaknesses": ["고집이 셈", "감정 기복"],
        "description": "..."
      },
      "fortune_periods": {
        "good_periods": [
          {"age_range": "30-40", "description": "사업운 상승기"}
        ],
        "caution_periods": [
          {"age_range": "50-55", "description": "건강 주의 필요"}  
        ]
      }
    },
    "ai_analysis": {
      "model_version": "gpt-4-turbo",
      "confidence_score": 0.92,
      "analysis_timestamp": "2024-03-15T10:30:00Z",
      "modern_interpretation": "...",
      "life_advice": "..."
    }
  }
  */
  
  -- 메타데이터
  analysis_engine VARCHAR(50), -- traditional, ai_gpt4, ai_claude, hybrid
  confidence_score DECIMAL(3,2), -- 0.00-1.00
  language VARCHAR(10) DEFAULT 'ko',
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_by VARCHAR(100), -- system, user_request, scheduled_analysis
  
  CONSTRAINT valid_confidence CHECK (confidence_score BETWEEN 0.00 AND 1.00)
);

-- JSONB 인덱스 (성능 최적화)
CREATE INDEX idx_saju_interp_chart_id ON saju_interpretations(saju_chart_id);
CREATE INDEX idx_saju_interp_type ON saju_interpretations(interpretation_type);
CREATE INDEX idx_saju_interp_data_gin ON saju_interpretations USING GIN (interpretation_data);

-- 특정 JSONB 필드 인덱스
CREATE INDEX idx_saju_interp_keywords ON saju_interpretations USING GIN ((interpretation_data->'overall'->'keywords'));
CREATE INDEX idx_saju_interp_score ON saju_interpretations ((interpretation_data->'overall'->>'score')::numeric);

-- ====================================
-- 🔮 2. 궁합 상세 해석
-- ====================================

/**
 * 궁합 분석 상세 해석
 * 두 사주 간의 상세한 궁합 분석 결과
 */
CREATE TABLE compatibility_interpretations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  compatibility_analysis_id UUID NOT NULL, -- core_schema의 compatibility_analyses 참조
  
  -- 궁합 해석 데이터
  compatibility_data JSONB NOT NULL,
  /*
  예시 구조:
  {
    "overall_analysis": {
      "summary": "두 사주는 목화상생의 관계로...",
      "compatibility_level": "excellent",
      "key_strengths": ["가치관 일치", "성격 보완"],
      "potential_issues": ["고집 충돌", "금전관 차이"]
    },
    "detailed_aspects": {
      "personality_match": {
        "score": 8.7,
        "analysis": "...",
        "interaction_style": "complementary"
      },
      "career_synergy": {
        "score": 7.2, 
        "business_potential": "high",
        "leadership_dynamic": "shared_leadership"
      },
      "life_goals": {
        "alignment_score": 9.1,
        "shared_values": ["가족", "성장", "안정"],
        "different_priorities": ["여행 vs 안정"]
      }
    },
    "relationship_advice": {
      "dos": ["서로의 의견 존중", "정기적인 대화"],
      "donts": ["금전 문제로 다투지 말 것"],
      "growth_opportunities": ["함께하는 취미 활동"]
    },
    "astrological_details": {
      "wuxing_interaction": {
        "primary_elements": ["wood", "fire"],
        "interaction_type": "generative",
        "strength": "strong"
      },
      "stem_branch_relations": [
        {
          "type": "천간합",
          "elements": ["갑기", "을경"],
          "effect": "화합"
        }
      ]
    }
  }
  */
  
  -- 메타데이터
  analysis_depth VARCHAR(20) DEFAULT 'standard', -- basic, standard, premium, comprehensive
  language VARCHAR(10) DEFAULT 'ko',
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_compat_interp_analysis_id ON compatibility_interpretations(compatibility_analysis_id);
CREATE INDEX idx_compat_interp_data_gin ON compatibility_interpretations USING GIN (compatibility_data);
CREATE INDEX idx_compat_level ON compatibility_interpretations ((compatibility_data->'overall_analysis'->>'compatibility_level'));

-- ====================================
-- 🔮 3. 운세 예측 데이터
-- ====================================

/**
 * 상세 운세 예측 결과
 * 월운, 일운 등의 상세 예측 정보
 */
CREATE TABLE fortune_predictions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID NOT NULL, -- core_schema의 saju_charts 참조
  
  -- 예측 범위
  prediction_type VARCHAR(20) NOT NULL, -- daily, weekly, monthly, yearly
  target_date DATE NOT NULL,
  target_period_start DATE NOT NULL,
  target_period_end DATE NOT NULL,
  
  -- 운세 예측 데이터
  prediction_data JSONB NOT NULL,
  /*
  예시 구조:
  {
    "overall_fortune": {
      "score": 7.8,
      "trend": "improving",
      "summary": "이번 달은 전반적으로 상승세를..."
    },
    "categories": {
      "career": {
        "score": 8.2,
        "prediction": "새로운 기회가 찾아올 예정",
        "advice": "적극적인 자세로 임하세요",
        "lucky_colors": ["파란색", "검정색"],
        "lucky_numbers": [3, 7, 9],
        "caution_dates": ["2024-03-15", "2024-03-22"]
      },
      "wealth": {
        "score": 6.5,
        "prediction": "투자는 신중하게 접근",
        "investment_advice": "안정적인 자산 위주로",
        "income_forecast": "steady"
      },
      "health": {
        "score": 7.0,
        "health_focus": ["소화기", "스트레스 관리"],
        "exercise_recommendation": "가벼운 유산소 운동",
        "dietary_advice": "따뜻한 음식 위주"
      },
      "relationships": {
        "score": 8.5,
        "social_forecast": "인간관계 확장의 기회",
        "communication_advice": "진솔한 대화 중요",
        "conflict_resolution": "양보하는 자세"
      }
    },
    "astrological_basis": {
      "current_daewoon": "정관운",
      "monthly_gan_ji": "을미",
      "key_interactions": ["일간과 월간의 합"],
      "wuxing_balance": {
        "강한_오행": "토",
        "약한_오행": "금", 
        "균형_점수": 7.2
      }
    },
    "ai_insights": {
      "pattern_analysis": "과거 유사한 시기 패턴 분석",
      "personalized_tips": ["아침 명상 추천", "녹색 계열 옷차림"],
      "confidence_level": 0.85
    }
  }
  */
  
  -- 메타데이터
  prediction_engine VARCHAR(50), -- traditional_calendar, ai_analysis, hybrid
  accuracy_score DECIMAL(3,2), -- 이전 예측의 정확도 (사용자 피드백 기반)
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP WITH TIME ZONE, -- 예측 만료일
  
  CONSTRAINT valid_date_range CHECK (target_period_start <= target_period_end),
  CONSTRAINT valid_accuracy CHECK (accuracy_score IS NULL OR accuracy_score BETWEEN 0.00 AND 1.00)
);

-- 인덱스
CREATE INDEX idx_fortune_chart_id ON fortune_predictions(saju_chart_id);
CREATE INDEX idx_fortune_type_date ON fortune_predictions(prediction_type, target_date);
CREATE INDEX idx_fortune_period ON fortune_predictions(target_period_start, target_period_end);
CREATE INDEX idx_fortune_data_gin ON fortune_predictions USING GIN (prediction_data);

-- 특정 카테고리별 인덱스
CREATE INDEX idx_fortune_career_score ON fortune_predictions ((prediction_data->'categories'->'career'->>'score')::numeric);

-- ====================================
-- 🔮 4. 사용자 커스터마이제이션 
-- ====================================

/**
 * 사용자 맞춤 설정 및 선호도
 * 개인화된 해석 스타일 및 설정
 */
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  saju_chart_id UUID UNIQUE NOT NULL, -- core_schema의 saju_charts 참조
  
  -- 사용자 선호 설정
  preferences_data JSONB NOT NULL DEFAULT '{}',
  /*
  예시 구조:
  {
    "interpretation_style": {
      "tone": "formal", // formal, casual, friendly
      "detail_level": "comprehensive", // basic, standard, comprehensive
      "focus_areas": ["career", "health"], // 관심 분야
      "traditional_vs_modern": 0.7 // 0=완전 전통, 1=완전 현대적
    },
    "notification_settings": {
      "daily_fortune": true,
      "monthly_forecast": true, 
      "compatibility_updates": false,
      "lucky_timing_alerts": true
    },
    "display_preferences": {
      "preferred_language": "ko",
      "date_format": "lunar", // solar, lunar, both
      "show_technical_terms": false,
      "color_scheme": "traditional" // traditional, modern, minimal
    },
    "privacy_settings": {
      "share_predictions": false,
      "allow_analytics": true,
      "data_retention_period": 365
    },
    "feedback_history": {
      "prediction_ratings": [
        {"date": "2024-03-01", "category": "career", "rating": 4, "actual_outcome": "positive"},
        {"date": "2024-03-05", "category": "health", "rating": 3, "actual_outcome": "neutral"}
      ],
      "interpretation_usefulness": 4.2,
      "overall_satisfaction": 4.5
    }
  }
  */
  
  -- 감사 추적
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_user_prefs_chart_id ON user_preferences(saju_chart_id);
CREATE INDEX idx_user_prefs_data_gin ON user_preferences USING GIN (preferences_data);

-- ====================================
-- 트리거 및 함수
-- ====================================

-- 업데이트 타임스탬프 함수
CREATE OR REPLACE FUNCTION update_jsonb_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- 트리거 적용
CREATE TRIGGER update_saju_interpretations_timestamp
  BEFORE UPDATE ON saju_interpretations
  FOR EACH ROW
  EXECUTE FUNCTION update_jsonb_timestamp();

CREATE TRIGGER update_compatibility_interpretations_timestamp
  BEFORE UPDATE ON compatibility_interpretations  
  FOR EACH ROW
  EXECUTE FUNCTION update_jsonb_timestamp();

CREATE TRIGGER update_user_preferences_timestamp
  BEFORE UPDATE ON user_preferences
  FOR EACH ROW  
  EXECUTE FUNCTION update_jsonb_timestamp();

-- ====================================
-- 유틸리티 함수
-- ====================================

/**
 * JSONB 데이터에서 특정 점수 추출
 */
CREATE OR REPLACE FUNCTION extract_interpretation_score(
  interpretation_jsonb JSONB,
  category TEXT DEFAULT 'overall'
) RETURNS DECIMAL(3,1) AS $$
BEGIN
  RETURN (interpretation_jsonb -> category ->> 'score')::DECIMAL(3,1);
EXCEPTION
  WHEN others THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql IMMUTABLE;