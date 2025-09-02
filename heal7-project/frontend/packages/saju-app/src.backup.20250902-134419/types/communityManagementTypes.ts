// 커뮤니티 관리 시스템 타입 정의

export type ContentType = 'magazine' | 'notice' | 'consultation' | 'review';
export type ContentStatus = 'draft' | 'review' | 'published' | 'archived';
export type Priority = 'low' | 'medium' | 'high' | 'urgent';

export interface MagazineContent {
  content_id: string;
  title: string;
  subtitle?: string;
  content: string; // Rich text HTML
  excerpt: string; // 요약
  
  // 분류
  category: string;
  tags: string[];
  content_type: 'article' | 'interview' | 'tutorial' | 'news';
  
  // 상태 관리
  status: ContentStatus;
  priority: Priority;
  is_featured: boolean;
  is_premium: boolean; // 프리미엄 회원만 열람
  
  // 작성자 정보
  author_id: string;
  author_name: string;
  editor_id?: string;
  editor_name?: string;
  
  // 미디어
  featured_image?: string;
  gallery_images?: string[];
  video_url?: string;
  
  // SEO
  seo_title?: string;
  seo_description?: string;
  seo_keywords?: string[];
  
  // 통계
  views: number;
  likes: number;
  shares: number;
  comments_count: number;
  avg_reading_time_minutes: number;
  
  // 발행 관리
  scheduled_publish_at?: string;
  published_at?: string;
  expires_at?: string;
  
  // 메타데이터
  created_at: string;
  updated_at: string;
}

export interface NoticeContent {
  notice_id: string;
  title: string;
  content: string;
  
  // 공지 유형
  notice_type: 'general' | 'urgent' | 'maintenance' | 'event' | 'policy';
  priority: Priority;
  
  // 노출 설정
  is_pinned: boolean;
  is_popup: boolean; // 팝업으로 노출
  target_grades: ('free' | 'premium' | 'vip' | 'all')[];
  
  // 작성자
  author_id: string;
  author_name: string;
  
  // 첨부파일
  attachments?: {
    file_name: string;
    file_url: string;
    file_size: number;
    file_type: string;
  }[];
  
  // 통계
  views: number;
  
  // 발행 관리
  status: ContentStatus;
  published_at?: string;
  expires_at?: string;
  
  created_at: string;
  updated_at: string;
}

export interface ConsultationManagement {
  consultation_id: string;
  user_id: string;
  user_name: string;
  user_grade: string;
  
  // 상담 내용
  consultation_type: string;
  title: string;
  content: string;
  birth_info?: {
    birth_date: string;
    birth_time: string;
    birth_location: string;
    is_lunar: boolean;
  };
  
  // 상담 관리
  status: 'pending' | 'assigned' | 'in_progress' | 'completed' | 'cancelled';
  priority: Priority;
  assigned_admin_id?: string;
  assigned_admin_name?: string;
  
  // 결제 정보
  payment_method: 'point' | 'cash' | 'free';
  amount_paid: number;
  payment_status: 'pending' | 'completed' | 'refunded';
  
  // 응답 관리
  responses: {
    response_id: string;
    admin_id: string;
    admin_name: string;
    content: string;
    is_public: boolean;
    attachments?: string[];
    created_at: string;
  }[];
  
  // 만족도 평가
  satisfaction_rating?: number;
  satisfaction_comment?: string;
  
  // SLA 관리
  sla_deadline: string; // 응답 기한
  response_time_hours?: number;
  is_overdue: boolean;
  
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface ReviewManagement {
  review_id: string;
  user_id: string;
  user_name: string;
  user_grade: string;
  
  // 리뷰 내용
  service_type: string;
  service_date: string;
  rating: number; // 1-5
  title: string;
  content: string;
  images?: string[];
  
  // 리뷰 관리
  status: 'pending' | 'approved' | 'rejected' | 'hidden';
  moderation_reason?: string;
  is_featured: boolean;
  is_verified: boolean; // 실제 서비스 이용 확인
  
  // 관리자 액션
  admin_response?: string;
  admin_response_author?: string;
  admin_response_at?: string;
  moderated_by?: string;
  moderated_at?: string;
  
  // 통계
  helpful_votes: number;
  report_count: number;
  
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface CommunityStats {
  content_overview: {
    total_contents: number;
    published_contents: number;
    draft_contents: number;
    pending_review: number;
  };
  
  magazine_stats: {
    total_articles: number;
    featured_articles: number;
    total_views: number;
    avg_views_per_article: number;
    top_performing_articles: {
      title: string;
      views: number;
      likes: number;
    }[];
  };
  
  consultation_stats: {
    pending_consultations: number;
    overdue_consultations: number;
    completed_today: number;
    avg_response_time_hours: number;
    satisfaction_rate: number;
  };
  
  review_stats: {
    pending_reviews: number;
    approved_reviews: number;
    featured_reviews: number;
    avg_rating: number;
    review_moderation_rate: number;
  };
  
  notice_stats: {
    active_notices: number;
    pinned_notices: number;
    urgent_notices: number;
    total_notice_views: number;
  };
}

export interface ContentSearchFilter {
  content_type?: ContentType[];
  status?: ContentStatus[];
  priority?: Priority[];
  author_id?: string;
  category?: string;
  tags?: string[];
  created_from?: string;
  created_to?: string;
  published_from?: string;
  published_to?: string;
  search_query?: string;
}

// Workflow 관리
export interface ContentWorkflow {
  workflow_id: string;
  content_id: string;
  content_type: ContentType;
  
  current_stage: 'draft' | 'review' | 'approval' | 'published';
  workflow_steps: {
    step_id: string;
    step_name: string;
    assignee_id?: string;
    assignee_name?: string;
    status: 'pending' | 'in_progress' | 'completed' | 'rejected';
    comments?: string;
    completed_at?: string;
  }[];
  
  created_at: string;
  updated_at: string;
  deadline?: string;
}

export interface BulkContentAction {
  action_type: 'publish' | 'unpublish' | 'archive' | 'delete' | 'change_category' | 'add_tags';
  target_content_ids: string[];
  parameters: {
    category?: string;
    tags?: string[];
    publish_date?: string;
  };
  reason: string;
}