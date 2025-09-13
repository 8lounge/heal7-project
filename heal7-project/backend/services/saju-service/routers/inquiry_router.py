"""
HEAL7 1:1 문의 관리 시스템
관리자 대시보드에서 사용할 실제 문의 관리 API

기능:
- 문의 목록 조회 (필터링, 검색, 페이징)
- 문의 상세 조회
- 문의 답변 작성/수정
- 문의 통계 조회
- 문의 상태 관리
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum
import sys
import os
from loguru import logger

# 보안 강화된 서비스 import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from auth_service import auth_service
from database_service import db_service

router = APIRouter(prefix="/api/admin/saju/inquiries", tags=["admin-inquiries"])
security = HTTPBearer()

# ===============================================
# Enums
# ===============================================

class InquiryStatus(str, Enum):
    pending = "pending"
    replied = "replied"
    closed = "closed"

class InquiryPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"

class InquiryCategory(str, Enum):
    service = "서비스문의"
    payment = "결제문의"
    account = "계정문의"
    general = "일반문의"
    technical = "기술문의"
    complaint = "불만사항"

# ===============================================
# Pydantic Models
# ===============================================

class InquiryOverview(BaseModel):
    status_stats: List[Dict[str, Any]]
    category_stats: List[Dict[str, Any]]
    priority_stats: List[Dict[str, Any]]
    avg_response_time: float
    total_pending: int

class InquiryDetail(BaseModel):
    id: int
    subject: str
    content: str
    category: str
    status: str
    priority: str
    admin_reply: Optional[str] = None
    user_name: str
    user_email: str
    created_at: datetime
    replied_at: Optional[datetime] = None
    admin_id: Optional[int] = None

class InquiryListResponse(BaseModel):
    inquiries: List[InquiryDetail]
    pagination: Dict[str, Any]

class InquiryReplyRequest(BaseModel):
    admin_reply: str = Field(..., min_length=1, max_length=2000)

# ===============================================
# Authentication
# ===============================================

async def verify_admin_token_inquiry(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """문의 관리 권한이 있는 관리자 토큰 검증"""
    token = credentials.credentials
    payload = auth_service.verify_jwt_token(token)

    # 데이터베이스에서 관리자 정보 확인
    admin = await db_service.execute_single_query(
        "SELECT * FROM admin_users WHERE id = $1 AND is_active = true",
        [payload['user_id']],
        db_type='saju'
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found or inactive"
        )

    # 권한 확인
    if not auth_service.check_permission(admin['role'], 'user_management'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions for inquiry management"
        )

    return admin

# ===============================================
# API Endpoints
# ===============================================

@router.get("/overview", response_model=InquiryOverview)
async def get_inquiry_overview(admin: dict = Depends(verify_admin_token_inquiry)):
    """문의 현황 통계 조회"""
    try:
        # 상태별 통계
        status_stats = await db_service.execute_query(
            """SELECT status, COUNT(*) as count
               FROM inquiries
               GROUP BY status
               ORDER BY count DESC""",
            db_type='main'
        )

        # 분류별 통계
        category_stats = await db_service.execute_query(
            """SELECT category, COUNT(*) as count
               FROM inquiries
               WHERE created_at >= NOW() - INTERVAL '30 days'
               GROUP BY category
               ORDER BY count DESC""",
            db_type='main'
        )

        # 우선순위별 통계
        priority_stats = await db_service.execute_query(
            """SELECT priority, COUNT(*) as count
               FROM inquiries
               WHERE status = 'pending'
               GROUP BY priority
               ORDER BY count DESC""",
            db_type='main'
        )

        # 평균 응답 시간 (시간 단위)
        avg_response_result = await db_service.execute_single_query(
            """SELECT AVG(EXTRACT(EPOCH FROM (replied_at - created_at))/3600) as avg_hours
               FROM inquiries
               WHERE replied_at IS NOT NULL
               AND created_at >= NOW() - INTERVAL '30 days'""",
            db_type='main'
        )

        avg_response_time = float(avg_response_result['avg_hours'] or 0)

        # 미답변 문의 수
        total_pending = await db_service.execute_count_query(
            "SELECT COUNT(*) FROM inquiries WHERE status = 'pending'",
            db_type='main'
        )

        return InquiryOverview(
            status_stats=status_stats,
            category_stats=category_stats,
            priority_stats=priority_stats,
            avg_response_time=round(avg_response_time, 1),
            total_pending=total_pending
        )

    except Exception as e:
        logger.error(f"Error fetching inquiry overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch inquiry overview"
        )

@router.get("", response_model=InquiryListResponse)
async def get_inquiries(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query("all"),
    category: str = Query("all"),
    priority: str = Query("all"),
    search: str = Query(""),
    admin: dict = Depends(verify_admin_token_inquiry)
):
    """문의 목록 조회 (필터링, 검색, 페이징)"""
    try:
        # WHERE 조건 구성
        where_conditions = []
        params = []
        param_count = 0

        if status != "all":
            param_count += 1
            where_conditions.append(f"status = ${param_count}")
            params.append(status)

        if category != "all":
            param_count += 1
            where_conditions.append(f"category = ${param_count}")
            params.append(category)

        if priority != "all":
            param_count += 1
            where_conditions.append(f"priority = ${param_count}")
            params.append(priority)

        if search:
            param_count += 1
            where_conditions.append(f"(subject ILIKE ${param_count} OR content ILIKE ${param_count} OR user_name ILIKE ${param_count})")
            params.append(f"%{search}%")

        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""

        # 전체 개수 조회
        count_query = f"SELECT COUNT(*) FROM inquiries {where_clause}"
        total_count = await db_service.execute_count_query(count_query, params, db_type='main')

        # 페이징 계산
        offset = (page - 1) * limit
        total_pages = (total_count + limit - 1) // limit

        # 문의 목록 조회
        param_count += 1
        params.append(limit)
        param_count += 1
        params.append(offset)

        list_query = f"""
            SELECT id, subject, content, category, status, priority, admin_reply,
                   user_name, user_email, created_at, replied_at, admin_id
            FROM inquiries
            {where_clause}
            ORDER BY
                CASE WHEN priority = 'urgent' THEN 1
                     WHEN priority = 'high' THEN 2
                     WHEN priority = 'normal' THEN 3
                     ELSE 4 END,
                created_at DESC
            LIMIT ${param_count-1} OFFSET ${param_count}
        """

        inquiries_data = await db_service.execute_query(list_query, params, db_type='main')

        inquiries = [InquiryDetail(**inquiry) for inquiry in inquiries_data]

        pagination = {
            "current_page": page,
            "per_page": limit,
            "total_count": total_count,
            "total_pages": total_pages
        }

        return InquiryListResponse(
            inquiries=inquiries,
            pagination=pagination
        )

    except Exception as e:
        logger.error(f"Error fetching inquiries: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch inquiries"
        )

@router.post("/{inquiry_id}/reply")
async def reply_to_inquiry(
    inquiry_id: int,
    reply_request: InquiryReplyRequest,
    admin: dict = Depends(verify_admin_token_inquiry)
):
    """문의에 답변 작성/수정"""
    try:
        # 문의 존재 확인
        inquiry = await db_service.execute_single_query(
            "SELECT * FROM inquiries WHERE id = $1",
            [inquiry_id],
            db_type='main'
        )

        if not inquiry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inquiry not found"
            )

        # 답변 저장
        await db_service.execute_query(
            """UPDATE inquiries SET
               admin_reply = $1,
               admin_id = $2,
               replied_at = $3,
               status = $4
               WHERE id = $5""",
            [
                reply_request.admin_reply,
                admin['id'],
                datetime.now(),
                'replied',
                inquiry_id
            ],
            db_type='main'
        )

        # 관리자 로그 기록
        await db_service.execute_query(
            """INSERT INTO admin_logs (admin_id, action, target_table, target_id, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            [admin['id'], "REPLY_INQUIRY", "inquiries", inquiry_id, datetime.now()],
            db_type='main'
        )

        return {
            "success": True,
            "message": "Reply submitted successfully",
            "inquiry_id": inquiry_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error replying to inquiry {inquiry_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit reply"
        )

@router.get("/{inquiry_id}")
async def get_inquiry_detail(
    inquiry_id: int,
    admin: dict = Depends(verify_admin_token_inquiry)
):
    """문의 상세 조회"""
    try:
        inquiry = await db_service.execute_single_query(
            """SELECT id, subject, content, category, status, priority, admin_reply,
                      user_name, user_email, created_at, replied_at, admin_id
               FROM inquiries WHERE id = $1""",
            [inquiry_id],
            db_type='main'
        )

        if not inquiry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inquiry not found"
            )

        return InquiryDetail(**inquiry)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching inquiry detail {inquiry_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch inquiry detail"
        )

@router.put("/{inquiry_id}/status")
async def update_inquiry_status(
    inquiry_id: int,
    status: InquiryStatus,
    admin: dict = Depends(verify_admin_token_inquiry)
):
    """문의 상태 변경"""
    try:
        # 문의 존재 확인
        inquiry = await db_service.execute_single_query(
            "SELECT id, status FROM inquiries WHERE id = $1",
            [inquiry_id],
            db_type='main'
        )

        if not inquiry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inquiry not found"
            )

        # 상태 업데이트
        await db_service.execute_query(
            "UPDATE inquiries SET status = $1 WHERE id = $2",
            [status.value, inquiry_id],
            db_type='main'
        )

        # 관리자 로그 기록
        await db_service.execute_query(
            """INSERT INTO admin_logs (admin_id, action, target_table, target_id, old_values, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            [
                admin['id'], "UPDATE_INQUIRY_STATUS", "inquiries", inquiry_id,
                f'{{"status": "{inquiry["status"]}"}}',
                f'{{"status": "{status.value}"}}',
                datetime.now()
            ],
            db_type='main'
        )

        return {
            "success": True,
            "message": f"Inquiry status updated to {status.value}",
            "inquiry_id": inquiry_id,
            "new_status": status.value
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating inquiry status {inquiry_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update inquiry status"
        )