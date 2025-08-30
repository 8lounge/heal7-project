#!/usr/bin/env python3
"""
User Management API - Dashboard Service Integration
기존 포트 8000에 통합된 사용자 관리 API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

# 라우터 생성
router = APIRouter(prefix="/api/user-management", tags=["사용자 관리"])

# 데이터 모델
class UserGrade(str, Enum):
    FREE = "free"
    PREMIUM = "premium" 
    VIP = "vip"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(BaseModel):
    id: Optional[int] = None
    email: str
    username: str
    grade: UserGrade
    status: UserStatus
    cash_balance: int = 0
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    subscription_expires: Optional[datetime] = None

class CashTransaction(BaseModel):
    id: Optional[int] = None
    user_id: int
    amount: int
    transaction_type: str  # "charge", "use", "refund"
    description: str
    created_at: Optional[datetime] = None

# 목업 데이터
mock_users = [
    {
        "id": 1,
        "email": "mz@example.com",
        "username": "MZ세대운세러",
        "grade": "premium",
        "status": "active",
        "cash_balance": 50000,
        "created_at": "2024-07-15T00:00:00",
        "last_login": "2024-08-28T14:30:00",
        "subscription_expires": "2024-09-15T23:59:59"
    },
    {
        "id": 2,
        "email": "admin@heal7.com",
        "username": "관리자",
        "grade": "vip",
        "status": "active", 
        "cash_balance": 100000,
        "created_at": "2024-01-01T00:00:00",
        "last_login": "2024-08-28T15:00:00",
        "subscription_expires": "2025-01-01T23:59:59"
    },
    {
        "id": 3,
        "email": "user1@test.com",
        "username": "일반사용자1",
        "grade": "free",
        "status": "active",
        "cash_balance": 0,
        "created_at": "2024-08-01T00:00:00",
        "last_login": "2024-08-27T10:00:00",
        "subscription_expires": None
    }
]

mock_transactions = [
    {
        "id": 1,
        "user_id": 1,
        "amount": 10000,
        "transaction_type": "charge",
        "description": "캐시 충전",
        "created_at": "2024-08-25T10:00:00"
    },
    {
        "id": 2, 
        "user_id": 1,
        "amount": -5000,
        "transaction_type": "use",
        "description": "프리미엄 상담 이용",
        "created_at": "2024-08-26T14:30:00"
    }
]

@router.get("/users", response_model=dict)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    grade: Optional[UserGrade] = None,
    status: Optional[UserStatus] = None
):
    """사용자 목록 조회"""
    users = mock_users.copy()
    
    # 필터링
    if grade:
        users = [u for u in users if u["grade"] == grade]
    if status:
        users = [u for u in users if u["status"] == status]
    
    # 페이징
    total = len(users)
    users = users[skip:skip + limit]
    
    return {
        "users": users,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """특정 사용자 조회"""
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    """사용자 정보 수정"""
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 업데이트
    user.update(user_data)
    return {"message": "사용자 정보가 수정되었습니다", "user": user}

@router.post("/users/{user_id}/grade")
async def change_user_grade(user_id: int, new_grade: UserGrade, reason: str):
    """사용자 등급 변경"""
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    old_grade = user["grade"]
    user["grade"] = new_grade
    
    # 등급 변경 히스토리 기록
    grade_change = {
        "user_id": user_id,
        "from_grade": old_grade,
        "to_grade": new_grade,
        "reason": reason,
        "changed_at": datetime.now().isoformat()
    }
    
    return {
        "message": f"사용자 등급이 {old_grade}에서 {new_grade}로 변경되었습니다",
        "grade_change": grade_change
    }

@router.get("/users/{user_id}/cash")
async def get_user_cash(user_id: int):
    """사용자 캐시 정보 조회"""
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    transactions = [t for t in mock_transactions if t["user_id"] == user_id]
    
    return {
        "user_id": user_id,
        "cash_balance": user["cash_balance"],
        "recent_transactions": transactions[-10:]  # 최근 10건
    }

@router.post("/users/{user_id}/cash/charge")
async def charge_cash(user_id: int, amount: int, description: str = "캐시 충전"):
    """캐시 충전"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="충전 금액은 0보다 커야 합니다")
    
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    user["cash_balance"] += amount
    
    # 트랜잭션 기록
    transaction = {
        "id": len(mock_transactions) + 1,
        "user_id": user_id,
        "amount": amount,
        "transaction_type": "charge",
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    mock_transactions.append(transaction)
    
    return {
        "message": f"{amount:,}원이 충전되었습니다",
        "new_balance": user["cash_balance"],
        "transaction": transaction
    }

@router.post("/users/{user_id}/cash/use")
async def use_cash(user_id: int, amount: int, description: str = "캐시 사용"):
    """캐시 사용"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="사용 금액은 0보다 커야 합니다")
    
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    if user["cash_balance"] < amount:
        raise HTTPException(status_code=400, detail="잔액이 부족합니다")
    
    user["cash_balance"] -= amount
    
    # 트랜잭션 기록
    transaction = {
        "id": len(mock_transactions) + 1,
        "user_id": user_id,
        "amount": -amount,
        "transaction_type": "use",
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    mock_transactions.append(transaction)
    
    return {
        "message": f"{amount:,}원이 사용되었습니다",
        "new_balance": user["cash_balance"],
        "transaction": transaction
    }

@router.get("/stats")
async def get_user_stats():
    """사용자 통계"""
    total_users = len(mock_users)
    grade_stats = {}
    status_stats = {}
    
    for user in mock_users:
        grade = user["grade"]
        status = user["status"]
        
        grade_stats[grade] = grade_stats.get(grade, 0) + 1
        status_stats[status] = status_stats.get(status, 0) + 1
    
    total_cash = sum(user["cash_balance"] for user in mock_users)
    
    return {
        "total_users": total_users,
        "grade_distribution": grade_stats,
        "status_distribution": status_stats,
        "total_cash_balance": total_cash,
        "active_premium_users": len([u for u in mock_users if u["grade"] in ["premium", "vip"] and u["status"] == "active"])
    }