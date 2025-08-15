import { API_BASE_URL } from './config'

export interface AcademyProject {
  id: number
  title: string
  description: string
  category: string
  instructor_name: string
  target_amount: number
  current_amount: number
  target_participants: number
  current_participants: number
  duration_days: number
  price: number
  image_url?: string
  difficulty_level: string
  status: string
  funding_percentage: number
  days_remaining: number
  created_at?: string
  updated_at?: string
  start_date?: string
  end_date?: string
}

export interface AcademyProjectsResponse {
  success: boolean
  projects: AcademyProject[]
  total: number
  limit: number
  offset: number
  category?: string
  status?: string
}

export interface AcademyProjectResponse {
  success: boolean
  project: AcademyProject
}

export interface AcademyCategoriesResponse {
  success: boolean
  categories: Array<{
    name: string
    project_count: number
  }>
}

export interface AcademyStatsResponse {
  success: boolean
  stats: {
    total_projects: number
    active_projects: number
    completed_projects: number
    total_funding: number
    total_participants: number
    categories: Array<{
      category: string
      project_count: number
      total_funding: number
    }>
  }
}

export const academyApi = {
  // 프로젝트 목록 조회
  async getProjects(params?: {
    category?: string
    status?: string
    limit?: number
    offset?: number
  }): Promise<AcademyProjectsResponse> {
    const searchParams = new URLSearchParams()
    
    if (params?.category) searchParams.append('category', params.category)
    if (params?.status) searchParams.append('status', params.status)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE_URL}/api/academy/projects?${searchParams}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response.json()
  },

  // 특정 프로젝트 조회
  async getProject(projectId: number): Promise<AcademyProjectResponse> {
    const response = await fetch(`${API_BASE_URL}/api/academy/projects/${projectId}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response.json()
  },

  // 카테고리 목록 조회
  async getCategories(): Promise<AcademyCategoriesResponse> {
    const response = await fetch(`${API_BASE_URL}/api/academy/categories`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response.json()
  },

  // 통계 조회
  async getStats(): Promise<AcademyStatsResponse> {
    const response = await fetch(`${API_BASE_URL}/api/academy/stats`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response.json()
  },

  // 프로젝트 등록/후원
  async enrollProject(projectId: number, enrollmentData: {
    user_name: string
    user_email: string
    user_phone: string
    payment_method?: string
  }) {
    const response = await fetch(`${API_BASE_URL}/api/academy/projects/${projectId}/enroll`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(enrollmentData),
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response.json()
  }
}