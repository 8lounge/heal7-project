"""
HEAL7 관리자 회원관리 시스템 API
사용자 조회, 수정, 삭제, 통계 등 관리자 전용 기능
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import jwt
from .auth import verify_token, SECRET_KEY, ALGORITHM, fake_users_db
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/users", tags=["관리자-회원관리"])

# Pydantic 모델들
class AdminUserList(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: str
    last_login_at: Optional[str]

class UserStats(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    admin_users: int
    new_users_today: int
    new_users_this_month: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

def verify_admin_token(current_user: dict = Depends(verify_token)):
    """관리자 토큰 검증"""
    user_id = current_user["user_id"]
    
    # 사용자 찾기
    user = None
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            user = user_data
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    if not user.get("is_admin", False):
        raise HTTPException(
            status_code=403, 
            detail="관리자 권한이 필요합니다"
        )
    
    return user

@router.get("/", response_model=List[AdminUserList], summary="전체 회원 목록 조회")
async def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    admin_user: dict = Depends(verify_admin_token)
):
    """관리자용 전체 회원 목록 조회 (페이지네이션 지원)"""
    
    users_list = []
    
    for email, user_data in fake_users_db.items():
        # 검색 필터
        if search:
            search_lower = search.lower()
            if not (search_lower in user_data.get("username", "").lower() or 
                   search_lower in user_data.get("email", "").lower() or
                   search_lower in user_data.get("full_name", "").lower()):
                continue
        
        # 활성 상태 필터
        if is_active is not None and user_data.get("is_active") != is_active:
            continue
        
        users_list.append(AdminUserList(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data.get("email", ""),
            full_name=user_data.get("full_name"),
            is_active=user_data.get("is_active", True),
            is_admin=user_data.get("is_admin", False),
            created_at=user_data.get("created_at", ""),
            last_login_at=user_data.get("last_login_at")
        ))
    
    # 페이지네이션
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    logger.info(f"관리자 {admin_user['username']}가 회원 목록 조회 (페이지: {page})")
    
    return users_list[start_idx:end_idx]

@router.get("/stats", response_model=UserStats, summary="회원 통계 조회")
async def get_user_stats(admin_user: dict = Depends(verify_admin_token)):
    """관리자용 회원 통계 조회"""
    
    total_users = len(fake_users_db)
    active_users = sum(1 for user in fake_users_db.values() if user.get("is_active", True))
    inactive_users = total_users - active_users
    admin_users = sum(1 for user in fake_users_db.values() if user.get("is_admin", False))
    
    # 오늘/이번달 신규 가입자 (임시 데이터)
    new_users_today = 0
    new_users_this_month = 1  # admin 계정
    
    today = date.today()
    current_month = today.replace(day=1)
    
    for user in fake_users_db.values():
        try:
            created_date = datetime.fromisoformat(user.get("created_at", "")).date()
            if created_date == today:
                new_users_today += 1
            if created_date >= current_month:
                new_users_this_month += 1
        except:
            continue
    
    logger.info(f"관리자 {admin_user['username']}가 회원 통계 조회")
    
    return UserStats(
        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users,
        admin_users=admin_users,
        new_users_today=new_users_today,
        new_users_this_month=new_users_this_month
    )

@router.get("/{user_id}", response_model=AdminUserList, summary="특정 회원 상세 조회")
async def get_user_by_id(
    user_id: str,
    admin_user: dict = Depends(verify_admin_token)
):
    """특정 회원의 상세 정보 조회"""
    
    # 사용자 찾기
    target_user = None
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            target_user = user_data
            break
    
    if not target_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    logger.info(f"관리자 {admin_user['username']}가 사용자 {target_user['username']} 상세 조회")
    
    return AdminUserList(
        id=target_user["id"],
        username=target_user["username"],
        email=target_user.get("email", ""),
        full_name=target_user.get("full_name"),
        is_active=target_user.get("is_active", True),
        is_admin=target_user.get("is_admin", False),
        created_at=target_user.get("created_at", ""),
        last_login_at=target_user.get("last_login_at")
    )

@router.put("/{user_id}", response_model=Dict[str, str], summary="회원 정보 수정")
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    admin_user: dict = Depends(verify_admin_token)
):
    """특정 회원의 정보 수정"""
    
    # 사용자 찾기
    target_email = None
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            target_email = email
            break
    
    if not target_email:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 업데이트 적용
    updates = user_update.dict(exclude_unset=True)
    for field, value in updates.items():
        fake_users_db[target_email][field] = value
    
    fake_users_db[target_email]["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"관리자 {admin_user['username']}가 사용자 {user_id} 정보 수정: {updates}")
    
    return {"message": "사용자 정보가 성공적으로 수정되었습니다"}

@router.delete("/{user_id}", response_model=Dict[str, str], summary="회원 삭제")
async def delete_user(
    user_id: str,
    admin_user: dict = Depends(verify_admin_token)
):
    """특정 회원 삭제 (실제론 비활성화)"""
    
    # 자기 자신은 삭제할 수 없음
    if user_id == admin_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="자기 자신의 계정은 삭제할 수 없습니다"
        )
    
    # 사용자 찾기
    target_email = None
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            target_email = email
            break
    
    if not target_email:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 실제 삭제 대신 비활성화
    fake_users_db[target_email]["is_active"] = False
    fake_users_db[target_email]["deleted_at"] = datetime.utcnow().isoformat()
    
    logger.warning(f"관리자 {admin_user['username']}가 사용자 {user_id} 삭제/비활성화")
    
    return {"message": "사용자가 성공적으로 삭제되었습니다"}

@router.post("/{user_id}/toggle-admin", response_model=Dict[str, str], summary="관리자 권한 토글")
async def toggle_admin_status(
    user_id: str,
    admin_user: dict = Depends(verify_admin_token)
):
    """특정 회원의 관리자 권한 추가/제거"""
    
    # 자기 자신의 관리자 권한은 제거할 수 없음
    if user_id == admin_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="자기 자신의 관리자 권한은 변경할 수 없습니다"
        )
    
    # 사용자 찾기
    target_email = None
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            target_email = email
            break
    
    if not target_email:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 관리자 권한 토글
    current_admin_status = fake_users_db[target_email].get("is_admin", False)
    new_admin_status = not current_admin_status
    fake_users_db[target_email]["is_admin"] = new_admin_status
    
    action = "부여" if new_admin_status else "제거"
    logger.warning(f"관리자 {admin_user['username']}가 사용자 {user_id}에게 관리자 권한 {action}")
    
    return {
        "message": f"관리자 권한이 성공적으로 {'부여' if new_admin_status else '제거'}되었습니다"
    }

@router.post("/{user_id}/reset-password", response_model=Dict[str, str], summary="비밀번호 재설정")
async def reset_user_password(
    user_id: str,
    admin_user: dict = Depends(verify_admin_token)
):
    """특정 회원의 비밀번호 재설정 (임시 비밀번호 발급)"""
    
    # 사용자 찾기
    target_email = None
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            target_email = email
            break
    
    if not target_email:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 임시 비밀번호 생성 (실제론 이메일로 발송)
    temp_password = f"heal7temp{user_id[:8]}"
    
    from .auth import hash_password
    fake_users_db[target_email]["password_hash"] = hash_password(temp_password)
    fake_users_db[target_email]["password_reset_required"] = True
    
    logger.warning(f"관리자 {admin_user['username']}가 사용자 {user_id}의 비밀번호 재설정")
    
    return {
        "message": "비밀번호가 재설정되었습니다",
        "temp_password": temp_password  # 실제론 이메일로만 전송
    }