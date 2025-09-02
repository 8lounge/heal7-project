// 캐시/포인트 제도 관리 타입 정의

export interface PointPolicy {
  version: string;
  last_updated: string;
  updated_by: string;
  
  // 기본 포인트 지급 정책
  earning_policy: {
    signup_bonus: number;           // 가입 시 지급
    daily_login: number;           // 일일 로그인
    first_content_view: number;    // 첫 콘텐츠 이용
    review_writing: number;        // 리뷰 작성
    share_content: number;         // 콘텐츠 공유
    referral_bonus: number;        // 추천인 보너스
    monthly_loyalty: number;       // 월간 충성도 보너스
  };
  
  // 포인트 차감 정책
  consumption_policy: {
    basic_saju: number;            // 기본 사주
    premium_saju: number;          // 프리미엄 사주
    compatibility: number;         // 궁합 분석
    tarot_reading: number;         // 타로 카드
    dream_interpretation: number;  // 꿈풀이
    personal_consultation: number; // 개인 상담
    group_consultation: number;    // 그룹 상담
  };
  
  // 유효기간 및 제한
  validity_settings: {
    point_expiry_days: number;     // 포인트 유효기간 (일)
    daily_earning_limit: number;   // 일일 적립 한도
    daily_usage_limit: number;     // 일일 사용 한도
    min_usage_amount: number;      // 최소 사용 포인트
    max_usage_amount: number;      // 최대 사용 포인트
  };
  
  // 등급별 혜택
  grade_benefits: {
    [key: string]: {
      grade_name: string;
      point_multiplier: number;    // 포인트 적립 배수
      discount_rate: number;       // 할인율 (%)
      daily_bonus: number;         // 일일 보너스 포인트
      special_privileges: string[]; // 특별 혜택 목록
    };
  };
}

export interface CashPolicy {
  version: string;
  last_updated: string;
  updated_by: string;
  
  // 충전 정책
  charge_policy: {
    min_charge_amount: number;     // 최소 충전 금액
    max_charge_amount: number;     // 최대 충전 금액
    bonus_rates: {                 // 충전 보너스율
      [amount: string]: number;    // 충전액별 보너스 %
    };
    payment_methods: string[];     // 결제 방법
  };
  
  // 환율 및 교환
  exchange_policy: {
    cash_to_point_rate: number;    // 캐시 → 포인트 환율
    point_to_cash_rate: number;    // 포인트 → 캐시 환율 (0이면 불가)
    exchange_fee_rate: number;     // 교환 수수료율
    min_exchange_amount: number;   // 최소 교환 금액
  };
  
  // 환불 정책
  refund_policy: {
    refund_available: boolean;     // 환불 가능 여부
    refund_fee_rate: number;       // 환불 수수료율
    refund_deadline_days: number;  // 환불 신청 기한
    min_refund_amount: number;     // 최소 환불 금액
    excluded_amounts: number[];    // 환불 불가 금액 (보너스 등)
  };
}

export interface OperationalPolicy {
  version: string;
  last_updated: string;
  updated_by: string;
  
  // 서비스 운영 정책
  service_policy: {
    free_trial_enabled: boolean;   // 무료 체험 제공
    free_trial_limit: number;      // 무료 체험 횟수
    guest_access_enabled: boolean; // 비회원 접근 허용
    maintenance_mode: boolean;     // 점검 모드
  };
  
  // 보안 및 제재
  security_policy: {
    suspicious_activity_threshold: number; // 의심 활동 임계값
    auto_block_enabled: boolean;          // 자동 차단 활성화
    max_failed_attempts: number;          // 최대 실패 시도 횟수
    temp_block_duration_hours: number;    // 임시 차단 지속 시간
    report_admin_threshold: number;       // 관리자 신고 임계값
  };
  
  // 이벤트 및 프로모션
  event_policy: {
    current_events: EventSettings[];
    scheduled_events: EventSettings[];
    auto_apply_best_discount: boolean;    // 최적 할인 자동 적용
  };
  
  // 고객 지원
  support_policy: {
    support_hours: string;               // 지원 시간
    response_time_hours: number;         // 응답 시간 목표
    escalation_threshold_hours: number;  // 에스컬레이션 임계값
    auto_response_enabled: boolean;      // 자동 응답 활성화
  };
}

export interface EventSettings {
  id: string;
  name: string;
  description: string;
  event_type: 'discount' | 'bonus_point' | 'free_service' | 'special_price';
  start_date: string;
  end_date: string;
  target_users: 'all' | 'new' | 'returning' | 'vip';
  conditions: {
    min_usage_amount?: number;
    target_services?: string[];
    user_grade_required?: string;
  };
  benefits: {
    discount_rate?: number;
    bonus_points?: number;
    free_services?: string[];
    special_price?: number;
  };
  usage_limit: {
    per_user: number;
    total: number;
    current_usage: number;
  };
  is_active: boolean;
}

// 통계 및 모니터링 타입
export interface PointCashStats {
  overview: {
    total_users: number;
    active_users_today: number;
    total_points_issued: number;
    total_points_used: number;
    total_cash_charged: number;
    total_revenue_today: number;
  };
  
  usage_analytics: {
    popular_services: {
      service_name: string;
      usage_count: number;
      revenue: number;
    }[];
    point_earning_sources: {
      source: string;
      count: number;
      total_points: number;
    }[];
    cash_charge_statistics: {
      charge_amount_range: string;
      user_count: number;
      total_amount: number;
    }[];
  };
  
  financial_summary: {
    daily_revenue: number;
    weekly_revenue: number;
    monthly_revenue: number;
    refund_amount: number;
    net_revenue: number;
  };
  
  user_behavior: {
    avg_points_per_user: number;
    avg_cash_per_user: number;
    retention_rate: number;
    churn_indicators: {
      low_usage_users: number;
      dormant_users: number;
      high_refund_users: number;
    };
  };
  
  alerts: {
    suspicious_activities: number;
    system_errors: number;
    policy_violations: number;
    pending_refunds: number;
  };
}

// API 요청/응답 타입
export interface PolicyUpdateRequest {
  policy_type: 'point' | 'cash' | 'operational';
  updates: Partial<PointPolicy | CashPolicy | OperationalPolicy>;
  reason: string;
  scheduled_apply_time?: string;
}

export interface PolicyUpdateResponse {
  success: boolean;
  message: string;
  applied_at: string;
  previous_version: string;
  new_version: string;
  affected_users?: number;
}

// 사용자별 포인트/캐시 관리 타입
export interface UserPointCashInfo {
  user_id: string;
  username: string;
  grade: string;
  current_points: number;
  current_cash: number;
  total_earned_points: number;
  total_used_points: number;
  total_charged_cash: number;
  recent_transactions: Transaction[];
  account_status: 'active' | 'suspended' | 'restricted';
  restrictions?: {
    reason: string;
    until: string;
    restricted_actions: string[];
  };
}

export interface Transaction {
  id: string;
  type: 'earn' | 'spend' | 'charge' | 'refund' | 'exchange';
  amount: number;
  currency: 'point' | 'cash';
  service_name?: string;
  description: string;
  created_at: string;
  status: 'completed' | 'pending' | 'failed' | 'cancelled';
  reference_id?: string;
}