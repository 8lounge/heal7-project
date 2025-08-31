// 회원 관리 시스템 타입 정의

export type UserGrade = 'free' | 'premium' | 'vip' | 'operator' | 'super_admin';
export type UserStatus = 'active' | 'inactive' | 'suspended' | 'withdrawn';
export type ConsultationStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled';
export type ReviewStatus = 'pending' | 'approved' | 'rejected';

export interface CustomerProfile {
  user_id: string;
  email: string;
  username: string;
  display_name?: string;
  phone?: string;
  birth_date?: string;
  gender?: 'male' | 'female' | 'other';
  
  // 회원 정보
  grade: UserGrade;
  status: UserStatus;
  signup_date: string;
  last_login_date?: string;
  login_count: number;
  
  // 재정 정보
  current_points: number;
  current_cash: number;
  total_spent: number;
  total_earned_points: number;
  
  // 활동 정보
  consultation_count: number;
  review_count: number;
  content_views: number;
  activity_score: number;
  
  // 추가 정보
  referral_code?: string;
  referred_by?: string;
  marketing_consent: boolean;
  notification_settings: {
    email: boolean;
    sms: boolean;
    push: boolean;
  };
  
  // 메타데이터
  created_at: string;
  updated_at: string;
  last_activity_at?: string;
}

export interface ConsultationRecord {
  consultation_id: string;
  user_id: string;
  consultation_type: 'basic_saju' | 'premium_saju' | 'compatibility' | 'tarot' | 'dream' | 'custom';
  title: string;
  content: string;
  status: ConsultationStatus;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  
  // 답변 정보
  responses: ConsultationResponse[];
  assigned_admin?: string;
  response_count: number;
  
  // 결제 정보
  payment_method: 'point' | 'cash';
  amount_paid: number;
  
  // 메타데이터
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface ConsultationResponse {
  response_id: string;
  consultation_id: string;
  admin_id: string;
  admin_name: string;
  content: string;
  attachments?: string[];
  is_public: boolean;
  created_at: string;
}

export interface ReviewRecord {
  review_id: string;
  user_id: string;
  service_type: string;
  rating: number; // 1-5
  title: string;
  content: string;
  status: ReviewStatus;
  is_featured: boolean;
  
  // 관리 정보
  admin_notes?: string;
  moderation_reason?: string;
  moderated_by?: string;
  moderated_at?: string;
  
  // 메타데이터
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface CustomerStats {
  total_customers: number;
  active_customers: number;
  new_signups_today: number;
  new_signups_this_month: number;
  
  grade_distribution: {
    [K in UserGrade]: number;
  };
  
  consultation_stats: {
    pending_consultations: number;
    completed_today: number;
    avg_response_time_hours: number;
    satisfaction_rate: number;
  };
  
  review_stats: {
    pending_reviews: number;
    approved_reviews: number;
    avg_rating: number;
    featured_reviews: number;
  };
  
  financial_stats: {
    total_points_balance: number;
    total_cash_balance: number;
    revenue_today: number;
    revenue_this_month: number;
  };
}

export interface CustomerSearchFilter {
  grade?: UserGrade[];
  status?: UserStatus[];
  signup_date_from?: string;
  signup_date_to?: string;
  last_login_from?: string;
  last_login_to?: string;
  min_activity_score?: number;
  max_activity_score?: number;
  has_consultations?: boolean;
  has_reviews?: boolean;
  min_spent_amount?: number;
  max_spent_amount?: number;
  search_query?: string; // 이메일, 이름 검색
}

export interface CustomerAction {
  action_type: 'upgrade_grade' | 'downgrade_grade' | 'suspend' | 'reactivate' | 'add_points' | 'add_cash' | 'send_notification';
  target_users: string[];
  parameters: {
    grade?: UserGrade;
    points_amount?: number;
    cash_amount?: number;
    suspension_reason?: string;
    notification_message?: string;
    notification_type?: 'email' | 'sms' | 'push' | 'all';
  };
  scheduled_at?: string;
  reason: string;
}

// API 요청/응답 타입
export interface CustomerListRequest {
  page: number;
  limit: number;
  filters?: CustomerSearchFilter;
  sort_by?: 'signup_date' | 'last_login' | 'activity_score' | 'total_spent';
  sort_order?: 'asc' | 'desc';
}

export interface CustomerListResponse {
  customers: CustomerProfile[];
  total_count: number;
  page_info: {
    current_page: number;
    total_pages: number;
    items_per_page: number;
  };
  stats: CustomerStats;
}