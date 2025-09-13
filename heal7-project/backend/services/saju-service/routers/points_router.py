"""
HEAL7 Point System Router
포인트/캐시 시스템 백엔드 API

포스텔러 운영정책 참고하여 구현:
- 포인트 충전 (point charging)
- 포인트 사용 (point usage)
- 포인트 잔액 조회 (balance inquiry)
- 포인트 내역 조회 (transaction history)
- 포인트 정책 관리 (policy management)
- 포인트 환불 (refund processing)

연관 스키마: /docs/database/point_system_schema.sql
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from decimal import Decimal
import json
import uuid
import sys
import os
from loguru import logger

# 보안 강화된 서비스 import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from auth_service import auth_service
from database_service import db_service

router = APIRouter(prefix="/api/points", tags=["points"])
security = HTTPBearer()

# ===============================================
# Pydantic Models (Request/Response Schemas)
# ===============================================

class PointBalanceResponse(BaseModel):
    user_id: str
    free_points: int = 0
    paid_points: int = 0
    bonus_points: int = 0
    referral_points: int = 0
    total_points: int = 0
    total_earned: int = 0
    total_spent: int = 0
    total_charged: int = 0
    user_grade: str = "normal"
    monthly_spending: int = 0

class PointChargeRequest(BaseModel):
    user_id: str
    charge_amount: int  # 충전 금액 (원)
    payment_method: str = Field(..., pattern="^(card|bank_transfer|mobile|kakao_pay|toss_pay)$")
    payment_id: Optional[str] = None  # 외부 결제 시스템 ID
    pg_name: Optional[str] = None  # PG사 이름

class PointChargeResponse(BaseModel):
    success: bool
    charge_id: str
    point_amount: int  # 지급된 포인트
    bonus_amount: int = 0  # 보너스 포인트
    payment_status: str
    message: str

class PointUsageRequest(BaseModel):
    user_id: str
    service_type: str = Field(..., pattern="^(saju_basic|saju_detail|compatibility|naming|consultation_phone|consultation_chat)$")
    amount: int  # 사용할 포인트
    description: Optional[str] = None

class PointUsageResponse(BaseModel):
    success: bool
    transaction_id: str
    remaining_balance: int
    used_points: Dict[str, int]  # 포인트 타입별 사용량
    message: str

class PointTransactionHistory(BaseModel):
    id: str
    point_type: str
    transaction_type: str
    amount: int
    balance_after: int
    source: Optional[str]
    related_service: Optional[str]
    description: Optional[str]
    expires_at: Optional[datetime]
    created_at: datetime

class PointHistoryResponse(BaseModel):
    transactions: List[PointTransactionHistory]
    total_count: int
    page: int
    page_size: int

class PointPolicyResponse(BaseModel):
    id: str
    policy_type: str
    category: Optional[str]
    service_type: Optional[str]
    rate_value: Optional[float]
    amount_value: Optional[int]
    period_value: Optional[int]
    description: Optional[str]
    is_active: bool

class PointRefundRequest(BaseModel):
    user_id: str
    refund_amount: int  # 환불할 포인트
    refund_reason: str

# ===============================================
# Database Connection
# ===============================================

async def get_db_connection():
    """PostgreSQL 데이터베이스 연결 - database_service 사용"""
    try:
        conn = await db_service.get_connection('main')
        return conn
    except Exception as e:
        logger.error(f"데이터베이스 연결 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 연결 실패"
        )

# ===============================================
# Authentication Helper
# ===============================================

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT 토큰 검증 (간단한 구현)"""
    token = credentials.credentials
    # 실제 구현에서는 JWT 토큰 검증 로직 필요
    if not token or len(token) < 10:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰"
        )
    return token

# ===============================================
# Point Business Logic Functions
# ===============================================

async def calculate_charge_bonus(charge_amount: int) -> int:
    """충전 금액에 따른 보너스 포인트 계산"""
    if charge_amount >= 300000:  # 30만원 이상
        return int(charge_amount * 0.10)  # 10% 보너스
    elif charge_amount >= 100000:  # 10만원 이상
        return int(charge_amount * 0.08)  # 8% 보너스
    elif charge_amount >= 50000:  # 5만원 이상
        return int(charge_amount * 0.06)  # 6% 보너스
    elif charge_amount >= 30000:  # 3만원 이상
        return int(charge_amount * 0.03)  # 3% 보너스
    else:
        return 0  # 보너스 없음

async def get_service_price(service_type: str, conn) -> int:
    """서비스별 포인트 가격 조회"""
    query = """
    SELECT amount_value FROM point_policies 
    WHERE policy_type = 'service_price' AND service_type = $1 AND is_active = true
    """
    result = await conn.fetchval(query, service_type)
    if result is None:
        # 기본 가격 설정 (스키마의 초기 데이터 참고)
        default_prices = {
            'saju_basic': 3000,
            'saju_detail': 5000,
            'compatibility': 4000,
            'naming': 6000,
            'consultation_phone': 300,  # 분당
            'consultation_chat': 200   # 분당
        }
        return default_prices.get(service_type, 1000)
    return result

async def use_points_with_priority(user_id: str, amount: int, conn) -> Dict[str, int]:
    """포인트 사용 우선순위에 따른 차감 (무료 → 보너스 → 유료 순)"""
    # 현재 잔액 조회
    balance_query = """
    SELECT free_points, bonus_points, paid_points, referral_points 
    FROM user_point_balances WHERE user_id = $1
    """
    balance = await conn.fetchrow(balance_query, user_id)
    if not balance:
        raise HTTPException(status_code=404, detail="사용자 포인트 정보를 찾을 수 없습니다")
    
    remaining = amount
    used_points = {'free': 0, 'bonus': 0, 'paid': 0, 'referral': 0}
    
    # 1. 무료 포인트부터 사용
    if remaining > 0 and balance['free_points'] > 0:
        use_free = min(remaining, balance['free_points'])
        used_points['free'] = use_free
        remaining -= use_free
    
    # 2. 보너스 포인트 사용
    if remaining > 0 and balance['bonus_points'] > 0:
        use_bonus = min(remaining, balance['bonus_points'])
        used_points['bonus'] = use_bonus
        remaining -= use_bonus
    
    # 3. 추천 포인트 사용
    if remaining > 0 and balance['referral_points'] > 0:
        use_referral = min(remaining, balance['referral_points'])
        used_points['referral'] = use_referral
        remaining -= use_referral
    
    # 4. 유료 포인트 사용
    if remaining > 0 and balance['paid_points'] > 0:
        use_paid = min(remaining, balance['paid_points'])
        used_points['paid'] = use_paid
        remaining -= use_paid
    
    if remaining > 0:
        raise HTTPException(status_code=400, detail="포인트 잔액이 부족합니다")
    
    return used_points

# ===============================================
# API Endpoints
# ===============================================

@router.get("/balance/{user_id}", response_model=PointBalanceResponse)
async def get_point_balance(user_id: str, token: str = Depends(verify_token)):
    """사용자 포인트 잔액 조회"""
    conn = await get_db_connection()
    try:
        query = """
        SELECT user_id, free_points, paid_points, bonus_points, referral_points,
               total_points, total_earned, total_spent, total_charged, 
               user_grade, monthly_spending
        FROM user_point_balances 
        WHERE user_id = $1
        """
        result = await conn.fetchrow(query, user_id)
        
        if not result:
            # 사용자가 없으면 기본 잔액으로 생성
            insert_query = """
            INSERT INTO user_point_balances (user_id) VALUES ($1)
            RETURNING user_id, free_points, paid_points, bonus_points, referral_points,
                     total_points, total_earned, total_spent, total_charged,
                     user_grade, monthly_spending
            """
            result = await conn.fetchrow(insert_query, user_id)
        
        return PointBalanceResponse(
            user_id=str(result['user_id']),
            free_points=result['free_points'],
            paid_points=result['paid_points'],
            bonus_points=result['bonus_points'],
            referral_points=result['referral_points'],
            total_points=result['total_points'],
            total_earned=result['total_earned'],
            total_spent=result['total_spent'],
            total_charged=result['total_charged'],
            user_grade=result['user_grade'],
            monthly_spending=result['monthly_spending']
        )
    
    except Exception as e:
        logger.error(f"포인트 잔액 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="포인트 잔액 조회 실패")
    finally:
        await conn.close()

@router.post("/charge", response_model=PointChargeResponse)
async def charge_points(request: PointChargeRequest, token: str = Depends(verify_token)):
    """포인트 충전"""
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            # 보너스 포인트 계산
            bonus_amount = await calculate_charge_bonus(request.charge_amount)
            point_amount = request.charge_amount + bonus_amount
            
            # 충전 내역 기록
            charge_id = str(uuid.uuid4())
            charge_query = """
            INSERT INTO point_charges 
            (id, user_id, charge_amount, point_amount, bonus_amount, 
             payment_method, payment_id, pg_name, payment_status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'completed')
            """
            await conn.execute(
                charge_query, charge_id, request.user_id, request.charge_amount,
                point_amount, bonus_amount, request.payment_method,
                request.payment_id, request.pg_name
            )
            
            # 포인트 거래 내역 기록 (유료 포인트)
            transaction_query = """
            INSERT INTO point_transactions 
            (user_id, point_type, transaction_type, amount, balance_after, 
             source, description, metadata)
            VALUES ($1, 'paid', 'charge', $2, 
                   (SELECT COALESCE(paid_points, 0) + $2 FROM user_point_balances WHERE user_id = $1),
                   'charge', '포인트 충전', $3)
            """
            metadata = json.dumps({
                "charge_id": charge_id,
                "payment_method": request.payment_method,
                "charge_amount": request.charge_amount
            })
            await conn.execute(transaction_query, request.user_id, point_amount, metadata)
            
            # 보너스 포인트가 있으면 별도 기록
            if bonus_amount > 0:
                bonus_transaction_query = """
                INSERT INTO point_transactions 
                (user_id, point_type, transaction_type, amount, balance_after,
                 source, description, metadata)
                VALUES ($1, 'bonus', 'earn', $2,
                       (SELECT COALESCE(bonus_points, 0) + $2 FROM user_point_balances WHERE user_id = $1),
                       'charge_bonus', '충전 보너스', $3)
                """
                await conn.execute(bonus_transaction_query, request.user_id, bonus_amount, metadata)
            
            return PointChargeResponse(
                success=True,
                charge_id=charge_id,
                point_amount=point_amount,
                bonus_amount=bonus_amount,
                payment_status="completed",
                message=f"{request.charge_amount:,}원 충전 완료 (보너스: {bonus_amount:,}P)"
            )
    
    except Exception as e:
        logger.error(f"포인트 충전 실패: {e}")
        raise HTTPException(status_code=500, detail="포인트 충전 처리 실패")
    finally:
        await conn.close()

@router.post("/use", response_model=PointUsageResponse)
async def use_points(request: PointUsageRequest, token: str = Depends(verify_token)):
    """포인트 사용"""
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            # 서비스 가격 확인 (선택사항)
            service_price = await get_service_price(request.service_type, conn)
            
            # 사용할 포인트가 서비스 가격과 일치하는지 확인 (경고만)
            if request.amount != service_price:
                logger.warning(f"서비스 가격 불일치: 요청={request.amount}, 정책={service_price}")
            
            # 포인트 우선순위에 따른 차감
            used_points = await use_points_with_priority(request.user_id, request.amount, conn)
            
            # 각 포인트 타입별로 거래 내역 기록
            transaction_id = str(uuid.uuid4())
            for point_type, amount in used_points.items():
                if amount > 0:
                    transaction_query = """
                    INSERT INTO point_transactions 
                    (id, user_id, point_type, transaction_type, amount, balance_after,
                     source, related_service, description, metadata)
                    VALUES ($1::uuid, $2::uuid, $3::varchar, 'spend', $4::integer,
                           (SELECT CASE 
                                WHEN $3::varchar = 'free' THEN COALESCE(free_points, 0) - $4::integer
                                WHEN $3::varchar = 'bonus' THEN COALESCE(bonus_points, 0) - $4::integer
                                WHEN $3::varchar = 'paid' THEN COALESCE(paid_points, 0) - $4::integer
                                WHEN $3::varchar = 'referral' THEN COALESCE(referral_points, 0) - $4::integer
                            END FROM user_point_balances WHERE user_id = $2::uuid),
                           'purchase', $5::varchar, $6::text, $7::jsonb)
                    """
                    metadata = json.dumps({
                        "transaction_group": transaction_id,
                        "total_amount": request.amount,
                        "used_breakdown": used_points
                    })
                    sub_transaction_id = str(uuid.uuid4())
                    await conn.execute(
                        transaction_query, sub_transaction_id,
                        request.user_id, str(point_type), -amount, str(request.service_type),
                        str(request.description or f"{request.service_type} 서비스 이용"),
                        metadata
                    )
            
            # 잔액 조회
            balance_query = """
            SELECT total_points FROM user_point_balances WHERE user_id = $1
            """
            remaining_balance = await conn.fetchval(balance_query, request.user_id) or 0
            
            return PointUsageResponse(
                success=True,
                transaction_id=transaction_id,
                remaining_balance=remaining_balance,
                used_points=used_points,
                message=f"{request.amount:,}P 사용 완료"
            )
    
    except Exception as e:
        logger.error(f"포인트 사용 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@router.get("/history/{user_id}", response_model=PointHistoryResponse)
async def get_point_history(
    user_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    point_type: Optional[str] = Query(None, pattern="^(free|paid|bonus|referral)$"),
    transaction_type: Optional[str] = Query(None, pattern="^(earn|spend|refund|expire|charge)$"),
    token: str = Depends(verify_token)
):
    """포인트 사용 내역 조회"""
    conn = await get_db_connection()
    try:
        # 조건 구성
        conditions = ["user_id = $1"]
        params = [user_id]
        param_count = 1
        
        if point_type:
            param_count += 1
            conditions.append(f"point_type = ${param_count}")
            params.append(point_type)
        
        if transaction_type:
            param_count += 1
            conditions.append(f"transaction_type = ${param_count}")
            params.append(transaction_type)
        
        where_clause = " AND ".join(conditions)
        
        # 전체 개수 조회
        count_query = f"SELECT COUNT(*) FROM point_transactions WHERE {where_clause}"
        total_count = await conn.fetchval(count_query, *params)
        
        # 페이징된 결과 조회
        offset = (page - 1) * page_size
        history_query = f"""
        SELECT id, point_type, transaction_type, amount, balance_after,
               source, related_service, description, expires_at, created_at
        FROM point_transactions 
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        params.extend([page_size, offset])
        
        rows = await conn.fetch(history_query, *params)
        
        transactions = [
            PointTransactionHistory(
                id=str(row['id']),
                point_type=row['point_type'],
                transaction_type=row['transaction_type'],
                amount=row['amount'],
                balance_after=row['balance_after'],
                source=row['source'],
                related_service=row['related_service'],
                description=row['description'],
                expires_at=row['expires_at'],
                created_at=row['created_at']
            ) for row in rows
        ]
        
        return PointHistoryResponse(
            transactions=transactions,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    
    except Exception as e:
        logger.error(f"포인트 내역 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="포인트 내역 조회 실패")
    finally:
        await conn.close()

@router.get("/policies", response_model=List[PointPolicyResponse])
async def get_point_policies(
    policy_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    is_active: bool = Query(True),
    token: str = Depends(verify_token)
):
    """포인트 정책 조회"""
    conn = await get_db_connection()
    try:
        # 조건 구성
        conditions = ["is_active = $1"]
        params = [is_active]
        param_count = 1
        
        if policy_type:
            param_count += 1
            conditions.append(f"policy_type = ${param_count}")
            params.append(policy_type)
        
        if category:
            param_count += 1
            conditions.append(f"category = ${param_count}")
            params.append(category)
        
        where_clause = " AND ".join(conditions)
        
        query = f"""
        SELECT id, policy_type, category, service_type, rate_value, 
               amount_value, period_value, description, is_active
        FROM point_policies 
        WHERE {where_clause}
        ORDER BY policy_type, category
        """
        
        rows = await conn.fetch(query, *params)
        
        policies = [
            PointPolicyResponse(
                id=str(row['id']),
                policy_type=row['policy_type'],
                category=row['category'],
                service_type=row['service_type'],
                rate_value=float(row['rate_value']) if row['rate_value'] else None,
                amount_value=row['amount_value'],
                period_value=row['period_value'],
                description=row['description'],
                is_active=row['is_active']
            ) for row in rows
        ]
        
        return policies
    
    except Exception as e:
        logger.error(f"포인트 정책 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="포인트 정책 조회 실패")
    finally:
        await conn.close()

@router.post("/refund")
async def request_point_refund(request: PointRefundRequest, token: str = Depends(verify_token)):
    """포인트 환불 요청 (관리자 승인 필요)"""
    conn = await get_db_connection()
    try:
        # 환불 가능한 유료 포인트 확인
        balance_query = """
        SELECT paid_points FROM user_point_balances WHERE user_id = $1
        """
        paid_points = await conn.fetchval(balance_query, request.user_id) or 0
        
        if request.refund_amount > paid_points:
            raise HTTPException(
                status_code=400, 
                detail=f"환불 가능한 포인트가 부족합니다. (보유: {paid_points:,}P)"
            )
        
        # 환불 요청 기록 (실제 환불은 관리자 승인 후)
        refund_id = str(uuid.uuid4())
        refund_log = {
            "refund_id": refund_id,
            "user_id": request.user_id,
            "requested_amount": request.refund_amount,
            "reason": request.refund_reason,
            "status": "pending",
            "requested_at": datetime.now().isoformat()
        }
        
        # 임시로 시스템 로그에 기록 (실제로는 별도 환불 테이블 필요)
        logger.info(f"포인트 환불 요청: {json.dumps(refund_log, ensure_ascii=False)}")
        
        return {
            "success": True,
            "refund_id": refund_id,
            "message": "환불 요청이 접수되었습니다. 관리자 검토 후 처리됩니다.",
            "status": "pending"
        }
    
    except Exception as e:
        logger.error(f"포인트 환불 요청 실패: {e}")
        raise HTTPException(status_code=500, detail="환불 요청 처리 실패")
    finally:
        await conn.close()

# ===============================================
# Health Check
# ===============================================

@router.get("/health")
async def health_check():
    """포인트 시스템 상태 확인"""
    try:
        conn = await get_db_connection()
        # 간단한 DB 연결 테스트
        await conn.fetchval("SELECT 1")
        await conn.close()
        
        return {
            "status": "healthy",
            "service": "point_system",
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"포인트 시스템 헬스체크 실패: {e}")
        return {
            "status": "unhealthy",
            "service": "point_system", 
            "timestamp": datetime.now().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }