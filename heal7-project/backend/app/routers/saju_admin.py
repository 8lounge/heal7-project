"""
HEAL7 사주명리학 관리자 API
사주 계산 로직의 모든 설정을 관리하는 관리자 전용 API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path

# 실제 사주 admin 설정 시스템 연동 - 하드코딩 제거 완료
try:
    from ..core.config.saju_admin_settings import (
        SajuAdminSettings,
        get_admin_settings as get_real_admin_settings,
        update_admin_settings
    )
except ImportError:
    # 상대경로 임포트 실패 시 절대경로로 시도
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core', 'config'))
    from saju_admin_settings import (
        SajuAdminSettings,
        get_admin_settings as get_real_admin_settings,
        update_admin_settings
    )
from datetime import datetime

def get_admin_settings():
    """실제 사주 관리자 설정 반환 (하드코딩 제거)"""
    return get_real_admin_settings()

router = APIRouter(prefix="/api/admin/saju", tags=["사주 관리자"])
security = HTTPBearer()

# 설정 파일 경로
SETTINGS_FILE_PATH = "/home/ubuntu/heal7-project/backend/data/saju_admin_settings.json"

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """관리자 토큰 검증 (임시로 간단한 토큰 체크)"""
    # 실제 환경에서는 JWT 토큰 검증 등 보안 로직 구현 필요
    if credentials.credentials != "heal7-admin-2025":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token"
        )
    return credentials.credentials

# --- 전체 설정 관리 ---

@router.get("/settings", summary="전체 사주 관리자 설정 조회")
async def get_all_settings(token: str = Depends(verify_admin_token)):
    """전체 사주 관리자 설정을 조회합니다."""
    try:
        # 실제 설정 반환 (하드코딩 제거)
        settings = get_admin_settings()
        
        # 딕셔너리 형태로 변환하여 API 응답
        if hasattr(settings, 'dict'):
            return settings.dict()
        else:
            # 기존 방식 호환성 유지
            return {
                "version": getattr(settings, 'version', '5.0.0'),
                "last_updated": getattr(settings, 'last_updated', datetime.now().isoformat()),
                "updated_by": getattr(settings, 'updated_by', 'admin'),
                "time_settings": getattr(settings, 'time_settings', {}),
                "logic_settings": getattr(settings, 'logic_settings', {}),
                "geographic_settings": getattr(settings, 'geographic_settings', {}),
                "kasi_settings": getattr(settings, 'kasi_settings', {}),
                "cheongan_interpretations": getattr(settings, 'cheongan_interpretations', {}),
                "jiji_interpretations": getattr(settings, 'jiji_interpretations', {}),
                "gapja_interpretations": getattr(settings, 'gapja_interpretations', {})
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 조회 실패: {str(e)}")

@router.post("/settings", summary="전체 사주 관리자 설정 저장")
async def save_all_settings(
    settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """전체 사주 관리자 설정을 저장합니다."""
    try:
        # 데이터 디렉토리 생성
        os.makedirs(os.path.dirname(SETTINGS_FILE_PATH), exist_ok=True)
        
        # 실제 설정 인스턴스가 아닌 경우 변환 필요
        if not isinstance(settings, SajuAdminSettings):
            settings = SajuAdminSettings(**settings)
        
        # 파일로 저장
        settings.save_to_file(SETTINGS_FILE_PATH)
        
        # 메모리에도 업데이트
        update_admin_settings(settings)
        
        return {"message": "설정이 성공적으로 저장되었습니다.", "file_path": SETTINGS_FILE_PATH}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 저장 실패: {str(e)}")

# --- 개별 설정 섹션 관리 ---

@router.get("/settings/time", summary="시간 설정 조회")
async def get_time_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """시간 관련 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.time_settings

@router.put("/settings/time", summary="시간 설정 업데이트")
async def update_time_settings(
    time_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """시간 관련 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.time_settings = time_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "시간 설정이 업데이트되었습니다."}

@router.get("/settings/geographic", summary="지리적 설정 조회") 
async def get_geographic_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """지리적 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.geographic_settings

@router.put("/settings/geographic", summary="지리적 설정 업데이트")
async def update_geographic_settings(
    geographic_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """지리적 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.geographic_settings = geographic_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "지리적 설정이 업데이트되었습니다."}

@router.get("/settings/logic", summary="사주 로직 설정 조회")
async def get_logic_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """사주 로직 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.logic_settings

@router.put("/settings/logic", summary="사주 로직 설정 업데이트")
async def update_logic_settings(
    logic_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """사주 로직 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.logic_settings = logic_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "사주 로직 설정이 업데이트되었습니다."}

@router.get("/settings/kasi", summary="KASI 설정 조회")
async def get_kasi_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """KASI API 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.kasi_settings

@router.put("/settings/kasi", summary="KASI 설정 업데이트")
async def update_kasi_settings(
    kasi_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """KASI API 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.kasi_settings = kasi_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "KASI 설정이 업데이트되었습니다."}

# --- 해석 데이터 관리 ---

@router.get("/interpretations/cheongan", summary="천간 해석 조회")
async def get_cheongan_interpretations(
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """천간 해석 데이터를 조회합니다."""
    settings = get_admin_settings()
    return settings.cheongan_interpretations

@router.put("/interpretations/cheongan/{cheongan_name}", summary="천간 해석 업데이트")
async def update_cheongan_interpretation(
    cheongan_name: str,
    interpretation: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 천간의 해석을 업데이트합니다."""
    settings = get_admin_settings()
    settings.cheongan_interpretations[cheongan_name] = interpretation
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": f"천간 '{cheongan_name}' 해석이 업데이트되었습니다."}

@router.delete("/interpretations/cheongan/{cheongan_name}", summary="천간 해석 삭제")
async def delete_cheongan_interpretation(
    cheongan_name: str,
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 천간의 해석을 삭제합니다."""
    settings = get_admin_settings()
    if cheongan_name in settings.cheongan_interpretations:
        del settings.cheongan_interpretations[cheongan_name]
        settings.save_to_file(SETTINGS_FILE_PATH)
        return {"message": f"천간 '{cheongan_name}' 해석이 삭제되었습니다."}
    else:
        raise HTTPException(status_code=404, detail=f"천간 '{cheongan_name}'을 찾을 수 없습니다.")

@router.get("/interpretations/jiji", summary="지지 해석 조회")
async def get_jiji_interpretations(
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """지지 해석 데이터를 조회합니다."""
    settings = get_admin_settings()
    return settings.jiji_interpretations

@router.put("/interpretations/jiji/{jiji_name}", summary="지지 해석 업데이트")
async def update_jiji_interpretation(
    jiji_name: str,
    interpretation: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 지지의 해석을 업데이트합니다."""
    settings = get_admin_settings()
    settings.jiji_interpretations[jiji_name] = interpretation
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": f"지지 '{jiji_name}' 해석이 업데이트되었습니다."}

@router.get("/interpretations/gapja", summary="60갑자 해석 조회")
async def get_gapja_interpretations(
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """60갑자 해석 데이터를 조회합니다."""
    settings = get_admin_settings()
    return settings.gapja_interpretations

@router.put("/interpretations/gapja/{gapja_name}", summary="60갑자 해석 업데이트")
async def update_gapja_interpretation(
    gapja_name: str,
    interpretation: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 60갑자의 해석을 업데이트합니다."""
    settings = get_admin_settings()
    settings.gapja_interpretations[gapja_name] = interpretation
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": f"60갑자 '{gapja_name}' 해석이 업데이트되었습니다."}

# --- 시스템 상태 조회 ---

@router.get("/status", summary="사주 시스템 상태 조회")
async def get_system_status(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """사주 계산 시스템의 현재 상태를 조회합니다."""
    settings = get_admin_settings()
    
    return {
        "version": settings.version,
        "last_updated": settings.last_updated,
        "updated_by": settings.updated_by,
        "settings_file_exists": os.path.exists(SETTINGS_FILE_PATH),
        "settings_file_path": SETTINGS_FILE_PATH,
        "current_config": {
            "timezone_system": getattr(settings.time_settings, 'timezone_system', 'standard'),
            "logic_type": getattr(settings.logic_settings, 'logic_type', 'hybrid'),
            "default_country": getattr(settings.geographic_settings, 'default_country', 'KR'),
            "use_kasi_precision": getattr(settings.logic_settings, 'use_kasi_precision', True),
            "manseeryeok_count": getattr(settings.logic_settings, 'manseeryeok_count', 60000),
            "cheongan_count": len(settings.cheongan_interpretations) if settings.cheongan_interpretations else 0,
            "jiji_count": len(settings.jiji_interpretations) if settings.jiji_interpretations else 0,
            "gapja_count": len(settings.gapja_interpretations) if settings.gapja_interpretations else 0
        }
    }

# --- 포인트/결제 시스템 관리 ---

@router.get("/points/overview", summary="포인트 시스템 현황")
async def get_points_overview(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """포인트 시스템 전체 현황을 조회합니다."""
    try:
        import asyncpg
        import asyncio
        
        # 데이터베이스 연결 (실제 환경에서는 connection pool 사용 권장)
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user", 
            host="localhost"
        )
        
        # 포인트 시스템 통계 조회
        stats = await conn.fetchrow("""
            SELECT 
                SUM(CASE WHEN points > 0 THEN points ELSE 0 END) as total_issued,
                SUM(CASE WHEN points < 0 THEN ABS(points) ELSE 0 END) as total_used,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_revenue,
                COUNT(*) as total_transactions
            FROM point_transactions
            WHERE created_at > NOW() - INTERVAL '30 days'
        """)
        
        # 결제 수단별 현황
        payment_methods = await conn.fetch("""
            SELECT 
                payment_method,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_amount,
                COUNT(*) as transaction_count
            FROM point_transactions 
            WHERE amount > 0 AND created_at > NOW() - INTERVAL '30 days'
            GROUP BY payment_method
            ORDER BY total_amount DESC
        """)
        
        # 포인트 사용 패턴
        usage_patterns = await conn.fetch("""
            SELECT 
                description,
                SUM(ABS(points)) as total_points_used,
                COUNT(*) as usage_count
            FROM point_transactions 
            WHERE points < 0 AND created_at > NOW() - INTERVAL '30 days'
            GROUP BY description
            ORDER BY total_points_used DESC
        """)
        
        await conn.close()
        
        return {
            "overview": {
                "total_issued": int(stats['total_issued'] or 0),
                "total_used": int(stats['total_used'] or 0), 
                "total_revenue": int(stats['total_revenue'] or 0),
                "remaining_points": int((stats['total_issued'] or 0) - (stats['total_used'] or 0)),
                "total_transactions": int(stats['total_transactions'] or 0)
            },
            "payment_methods": [
                {
                    "method": row['payment_method'],
                    "amount": int(row['total_amount']),
                    "count": int(row['transaction_count'])
                } for row in payment_methods
            ],
            "usage_patterns": [
                {
                    "service": row['description'],
                    "points_used": int(row['total_points_used']),
                    "usage_count": int(row['usage_count'])
                } for row in usage_patterns
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"포인트 현황 조회 실패: {str(e)}")

@router.get("/points/transactions", summary="포인트 거래 내역 조회")
async def get_point_transactions(
    page: int = 1,
    limit: int = 20,
    search: str = "",
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """포인트 거래 내역을 페이징하여 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        offset = (page - 1) * limit
        where_clause = ""
        params = []
        
        if search:
            where_clause = "WHERE (u.name ILIKE $1 OR pt.description ILIKE $1)"
            params.append(f"%{search}%")
        
        # 총 개수 조회
        count_query = f"""
            SELECT COUNT(*) 
            FROM point_transactions pt 
            LEFT JOIN users u ON pt.user_id = u.id 
            {where_clause}
        """
        
        if params:
            total_count = await conn.fetchval(count_query, *params)
        else:
            total_count = await conn.fetchval(count_query)
        
        # 거래 내역 조회
        transactions_query = f"""
            SELECT 
                pt.id,
                u.name as user_name,
                u.email,
                pt.transaction_type,
                pt.amount,
                pt.points,
                pt.payment_method,
                pt.status,
                pt.description,
                pt.created_at
            FROM point_transactions pt
            LEFT JOIN users u ON pt.user_id = u.id
            {where_clause}
            ORDER BY pt.created_at DESC
            LIMIT ${ len(params) + 1} OFFSET ${ len(params) + 2}
        """
        
        params.extend([limit, offset])
        
        transactions = await conn.fetch(transactions_query, *params)
        
        await conn.close()
        
        return {
            "transactions": [
                {
                    "id": row['id'],
                    "user_name": row['user_name'],
                    "email": row['email'],
                    "transaction_type": row['transaction_type'],
                    "amount": int(row['amount']),
                    "points": int(row['points']),
                    "payment_method": row['payment_method'],
                    "status": row['status'],
                    "description": row['description'],
                    "created_at": row['created_at'].isoformat()
                } for row in transactions
            ],
            "pagination": {
                "current_page": page,
                "per_page": limit,
                "total_count": int(total_count),
                "total_pages": (int(total_count) + limit - 1) // limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"거래 내역 조회 실패: {str(e)}")

@router.get("/points/policies", summary="포인트 정책 조회")
async def get_point_policies(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """포인트 정책 설정을 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        policies = await conn.fetch("""
            SELECT policy_name, policy_value, policy_type, grade, is_active
            FROM point_policies
            WHERE is_active = true
            ORDER BY policy_type, grade
        """)
        
        await conn.close()
        
        # 정책을 카테고리별로 그룹화
        result = {}
        for row in policies:
            policy_type = row['policy_type']
            if policy_type not in result:
                result[policy_type] = []
            
            result[policy_type].append({
                "name": row['policy_name'],
                "value": float(row['policy_value']),
                "grade": row['grade'],
                "is_active": row['is_active']
            })
        
        return {"policies": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"정책 조회 실패: {str(e)}")

@router.put("/points/policies", summary="포인트 정책 업데이트")
async def update_point_policies(
    policies: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """포인트 정책을 업데이트합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # 정책별로 업데이트
        for policy_name, policy_value in policies.items():
            await conn.execute("""
                UPDATE point_policies 
                SET policy_value = $1, updated_at = NOW()
                WHERE policy_name = $2
            """, float(policy_value), policy_name)
        
        await conn.close()
        
        return {"message": "포인트 정책이 성공적으로 업데이트되었습니다."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"정책 업데이트 실패: {str(e)}")

# --- 1:1 문의 시스템 관리 ---

@router.get("/inquiries/overview", summary="문의 시스템 현황")
async def get_inquiries_overview(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """1:1 문의 시스템 전체 현황을 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # 문의 상태별 통계
        status_stats = await conn.fetch("""
            SELECT 
                status,
                COUNT(*) as count
            FROM inquiries 
            GROUP BY status
            ORDER BY status
        """)
        
        # 카테고리별 통계
        category_stats = await conn.fetch("""
            SELECT 
                category,
                COUNT(*) as count
            FROM inquiries 
            GROUP BY category
            ORDER BY count DESC
        """)
        
        # 평균 응답 시간 (답변 완료된 문의 기준)
        avg_response_time = await conn.fetchval("""
            SELECT AVG(EXTRACT(epoch FROM (replied_at - created_at))/3600) as avg_hours
            FROM inquiries 
            WHERE replied_at IS NOT NULL
        """)
        
        # 우선순위별 통계
        priority_stats = await conn.fetch("""
            SELECT 
                priority,
                COUNT(*) as count
            FROM inquiries 
            WHERE status = 'pending'
            GROUP BY priority
            ORDER BY 
                CASE priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'normal' THEN 3 
                    WHEN 'low' THEN 4 
                END
        """)
        
        await conn.close()
        
        return {
            "status_stats": [
                {
                    "status": row['status'],
                    "count": int(row['count'])
                } for row in status_stats
            ],
            "category_stats": [
                {
                    "category": row['category'],
                    "count": int(row['count'])
                } for row in category_stats
            ],
            "priority_stats": [
                {
                    "priority": row['priority'],
                    "count": int(row['count'])
                } for row in priority_stats
            ],
            "avg_response_time": round(float(avg_response_time or 0), 1),
            "total_pending": sum(int(row['count']) for row in status_stats if row['status'] == 'pending')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문의 현황 조회 실패: {str(e)}")

@router.get("/inquiries", summary="1:1 문의 목록 조회")
async def get_inquiries(
    status: str = "all",
    category: str = "all", 
    priority: str = "all",
    page: int = 1,
    limit: int = 20,
    search: str = "",
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """1:1 문의 목록을 필터링하여 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # WHERE 절 구성
        where_conditions = []
        params = []
        param_count = 0
        
        if status != "all":
            param_count += 1
            where_conditions.append(f"i.status = ${param_count}")
            params.append(status)
            
        if category != "all":
            param_count += 1
            where_conditions.append(f"i.category = ${param_count}")
            params.append(category)
            
        if priority != "all":
            param_count += 1
            where_conditions.append(f"i.priority = ${param_count}")
            params.append(priority)
            
        if search:
            param_count += 1
            where_conditions.append(f"(i.subject ILIKE ${param_count} OR i.content ILIKE ${param_count} OR u.name ILIKE ${param_count})")
            params.append(f"%{search}%")
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        # 총 개수 조회
        count_query = f"""
            SELECT COUNT(*) 
            FROM inquiries i
            LEFT JOIN users u ON i.user_id = u.id
            WHERE {where_clause}
        """
        
        total_count = await conn.fetchval(count_query, *params)
        
        # 문의 목록 조회
        offset = (page - 1) * limit
        param_count += 1
        limit_param = param_count
        param_count += 1
        offset_param = param_count
        params.extend([limit, offset])
        
        inquiries_query = f"""
            SELECT 
                i.id,
                i.subject,
                i.content,
                i.category,
                i.status,
                i.priority,
                i.admin_reply,
                i.created_at,
                i.replied_at,
                u.name as user_name,
                u.email as user_email
            FROM inquiries i
            LEFT JOIN users u ON i.user_id = u.id
            WHERE {where_clause}
            ORDER BY 
                CASE i.priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'normal' THEN 3 
                    WHEN 'low' THEN 4 
                END,
                i.created_at DESC
            LIMIT ${limit_param} OFFSET ${offset_param}
        """
        
        inquiries = await conn.fetch(inquiries_query, *params)
        
        await conn.close()
        
        return {
            "inquiries": [
                {
                    "id": row['id'],
                    "subject": row['subject'],
                    "content": row['content'],
                    "category": row['category'],
                    "status": row['status'],
                    "priority": row['priority'],
                    "admin_reply": row['admin_reply'],
                    "user_name": row['user_name'],
                    "user_email": row['user_email'],
                    "created_at": row['created_at'].isoformat(),
                    "replied_at": row['replied_at'].isoformat() if row['replied_at'] else None
                } for row in inquiries
            ],
            "pagination": {
                "current_page": page,
                "per_page": limit,
                "total_count": int(total_count),
                "total_pages": (int(total_count) + limit - 1) // limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문의 목록 조회 실패: {str(e)}")

@router.get("/inquiries/{inquiry_id}", summary="특정 문의 상세 조회")
async def get_inquiry_detail(
    inquiry_id: int,
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """특정 문의의 상세 정보를 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        inquiry = await conn.fetchrow("""
            SELECT 
                i.*,
                u.name as user_name,
                u.email as user_email,
                u.grade as user_grade
            FROM inquiries i
            LEFT JOIN users u ON i.user_id = u.id
            WHERE i.id = $1
        """, inquiry_id)
        
        await conn.close()
        
        if not inquiry:
            raise HTTPException(status_code=404, detail="문의를 찾을 수 없습니다.")
        
        return {
            "id": inquiry['id'],
            "subject": inquiry['subject'],
            "content": inquiry['content'],
            "category": inquiry['category'],
            "status": inquiry['status'],
            "priority": inquiry['priority'],
            "admin_reply": inquiry['admin_reply'],
            "user_name": inquiry['user_name'],
            "user_email": inquiry['user_email'],
            "user_grade": inquiry['user_grade'],
            "created_at": inquiry['created_at'].isoformat(),
            "replied_at": inquiry['replied_at'].isoformat() if inquiry['replied_at'] else None,
            "updated_at": inquiry['updated_at'].isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문의 상세 조회 실패: {str(e)}")

@router.post("/inquiries/{inquiry_id}/reply", summary="문의 답변")
async def reply_to_inquiry(
    inquiry_id: int,
    reply_data: Dict[str, str],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """문의에 답변을 작성합니다."""
    try:
        import asyncpg
        
        admin_reply = reply_data.get("admin_reply")
        if not admin_reply or not admin_reply.strip():
            raise HTTPException(status_code=400, detail="답변 내용을 입력해주세요.")
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # 문의가 존재하는지 확인
        inquiry_exists = await conn.fetchval("""
            SELECT EXISTS(SELECT 1 FROM inquiries WHERE id = $1)
        """, inquiry_id)
        
        if not inquiry_exists:
            await conn.close()
            raise HTTPException(status_code=404, detail="문의를 찾을 수 없습니다.")
        
        # 답변 저장
        await conn.execute("""
            UPDATE inquiries 
            SET admin_reply = $1, 
                status = 'replied', 
                replied_at = NOW(),
                updated_at = NOW()
            WHERE id = $2
        """, admin_reply.strip(), inquiry_id)
        
        await conn.close()
        
        return {"message": "답변이 성공적으로 저장되었습니다."}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"답변 저장 실패: {str(e)}")

@router.put("/inquiries/{inquiry_id}/status", summary="문의 상태 변경")
async def update_inquiry_status(
    inquiry_id: int,
    status_data: Dict[str, str],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """문의 상태를 변경합니다."""
    try:
        import asyncpg
        
        new_status = status_data.get("status")
        allowed_statuses = ["pending", "replied", "closed"]
        
        if new_status not in allowed_statuses:
            raise HTTPException(status_code=400, detail=f"허용되지 않는 상태입니다. 가능한 상태: {', '.join(allowed_statuses)}")
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # 문의가 존재하는지 확인
        inquiry_exists = await conn.fetchval("""
            SELECT EXISTS(SELECT 1 FROM inquiries WHERE id = $1)
        """, inquiry_id)
        
        if not inquiry_exists:
            await conn.close()
            raise HTTPException(status_code=404, detail="문의를 찾을 수 없습니다.")
        
        # 상태 업데이트
        await conn.execute("""
            UPDATE inquiries 
            SET status = $1, updated_at = NOW()
            WHERE id = $2
        """, new_status, inquiry_id)
        
        await conn.close()
        
        return {"message": f"문의 상태가 '{new_status}'로 변경되었습니다."}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 변경 실패: {str(e)}")

# --- 대시보드 실시간 통계 ---

@router.get("/dashboard/stats", summary="대시보드 실시간 통계")
async def get_dashboard_stats(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """대시보드 실시간 통계 데이터를 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # 총 회원수
        total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
        
        # 활성 회원 (최근 30일 내 로그인)
        active_users = await conn.fetchval("""
            SELECT COUNT(*) FROM users 
            WHERE updated_at > NOW() - INTERVAL '30 days'
        """)
        
        # 신규 가입 (최근 7일)
        new_users = await conn.fetchval("""
            SELECT COUNT(*) FROM users 
            WHERE created_at > NOW() - INTERVAL '7 days'
        """)
        
        # 일일 매출 (최근 24시간)
        daily_revenue = await conn.fetchval("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM point_transactions 
            WHERE amount > 0 AND created_at > NOW() - INTERVAL '24 hours'
        """)
        
        # 월간 매출 (현재 달)
        monthly_revenue = await conn.fetchval("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM point_transactions 
            WHERE amount > 0 
            AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())
            AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW())
        """)
        
        # 미답변 문의 수
        pending_inquiries = await conn.fetchval("""
            SELECT COUNT(*) FROM inquiries WHERE status = 'pending'
        """)
        
        # 사주 해석 통계 (최근 7일)
        interpretations_this_week = await conn.fetchval("""
            SELECT COUNT(*) FROM saju_results 
            WHERE created_at > NOW() - INTERVAL '7 days'
        """) or 0
        
        # 평균 응답 시간 (시간 단위)
        avg_response_time = await conn.fetchval("""
            SELECT AVG(EXTRACT(epoch FROM (replied_at - created_at))/3600) 
            FROM inquiries 
            WHERE replied_at IS NOT NULL 
            AND created_at > NOW() - INTERVAL '30 days'
        """) or 0
        
        await conn.close()
        
        # 시스템 가동시간 (임시로 고정값, 실제로는 시스템 모니터링 툴에서 가져와야 함)
        system_uptime = 99.8
        
        return {
            "total_users": int(total_users or 0),
            "active_users": int(active_users or 0),
            "new_users": int(new_users or 0),
            "daily_revenue": int(daily_revenue or 0),
            "monthly_revenue": int(monthly_revenue or 0),
            "system_uptime": system_uptime,
            "pending_inquiries": int(pending_inquiries or 0),
            "interpretations_this_week": int(interpretations_this_week),
            "avg_response_time": round(float(avg_response_time), 1),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대시보드 통계 조회 실패: {str(e)}")

@router.get("/dashboard/recent-activities", summary="최근 활동 조회")
async def get_recent_activities(
    limit: int = 20,
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """최근 활동 내역을 조회합니다."""
    try:
        import asyncpg
        
        conn = await asyncpg.connect(
            database="heal7_saju",
            user="heal7_user",
            host="localhost"
        )
        
        # 최근 사용자 활동 (가입, 로그인 등)
        recent_users = await conn.fetch("""
            SELECT 
                name, 
                email,
                created_at,
                'user_signup' as activity_type
            FROM users 
            WHERE created_at > NOW() - INTERVAL '7 days'
            ORDER BY created_at DESC 
            LIMIT $1
        """, limit // 2)
        
        # 최근 문의
        recent_inquiries = await conn.fetch("""
            SELECT 
                i.subject,
                u.name as user_name,
                i.created_at,
                i.status,
                'inquiry' as activity_type
            FROM inquiries i
            LEFT JOIN users u ON i.user_id = u.id
            WHERE i.created_at > NOW() - INTERVAL '7 days'
            ORDER BY i.created_at DESC 
            LIMIT $1
        """, limit // 2)
        
        await conn.close()
        
        activities = []
        
        # 사용자 활동 추가
        for user in recent_users:
            activities.append({
                "type": "user_signup",
                "title": "신규 회원가입",
                "description": f"{user['name']}님이 회원가입했습니다",
                "timestamp": user['created_at'].isoformat(),
                "icon": "user"
            })
        
        # 문의 활동 추가
        for inquiry in recent_inquiries:
            activities.append({
                "type": "inquiry",
                "title": "새로운 문의",
                "description": f"{inquiry['user_name']}: {inquiry['subject'][:50]}{'...' if len(inquiry['subject']) > 50 else ''}",
                "timestamp": inquiry['created_at'].isoformat(),
                "status": inquiry['status'],
                "icon": "message"
            })
        
        # 시간순 정렬
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "activities": activities[:limit],
            "total_count": len(activities)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"최근 활동 조회 실패: {str(e)}")

# --- 데이터 초기화 및 백업 ---

@router.post("/initialize", summary="기본 설정 데이터 초기화")
async def initialize_default_settings(token: str = Depends(verify_admin_token)) -> Dict[str, str]:
    """기본 설정 데이터로 초기화합니다."""
    try:
        # 기본 설정 생성
        settings = get_admin_settings()
        
        # 파일로 저장
        settings.save_to_file(SETTINGS_FILE_PATH)
        
        return {"message": "기본 설정으로 초기화가 완료되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"초기화 실패: {str(e)}")

@router.post("/backup", summary="현재 설정 백업")
async def backup_current_settings(token: str = Depends(verify_admin_token)) -> Dict[str, str]:
    """현재 설정을 백업합니다."""
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"/home/ubuntu/heal7-project/backend/data/backup/saju_settings_{timestamp}.json"
        
        # 백업 디렉토리 생성
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        settings = get_admin_settings()
        settings.save_to_file(backup_path)
        
        return {"message": "설정이 백업되었습니다.", "backup_path": backup_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"백업 실패: {str(e)}")

# Dashboard API 엔드포인트 추가
@router.get("/dashboard/stats", summary="관리자 대시보드 통계")
async def get_dashboard_stats(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """관리자 대시보드용 통계 데이터를 반환합니다."""
    try:
        # Mock 데이터 (실제 데이터베이스 연동 시 교체)
        return {
            "today_users": 142,
            "total_users": 8567,
            "today_calculations": 89,
            "total_calculations": 45238,
            "system_status": "healthy",
            "api_calls_today": 534,
            "error_rate": 0.012,
            "average_response_time": 125,
            "active_sessions": 23,
            "revenue_today": 89400,
            "popular_services": [
                {"name": "사주계산", "count": 234},
                {"name": "꿈해몽", "count": 156},
                {"name": "운세보기", "count": 98}
            ],
            "recent_alerts": [
                {"level": "info", "message": "시스템 정상 운영 중", "time": "10분 전"},
                {"level": "warning", "message": "KASI API 응답 지연", "time": "2시간 전"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

@router.get("/dashboard/recent-activities", summary="최근 활동 내역")
async def get_recent_activities(
    limit: int = 10,
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """최근 시스템 활동 내역을 반환합니다."""
    try:
        # Mock 데이터 (실제 데이터베이스 연동 시 교체)
        activities = [
            {
                "id": f"act_{i}",
                "type": "calculation" if i % 3 == 0 else "user_register" if i % 3 == 1 else "payment",
                "user_id": f"user_{1000 + i}",
                "description": f"{'사주 계산 요청' if i % 3 == 0 else '신규 사용자 가입' if i % 3 == 1 else '포인트 결제'}",
                "timestamp": f"2025-09-10T{14 - (i // 4):02d}:{45 - (i % 4) * 15:02d}:00Z",
                "status": "completed" if i % 5 != 4 else "failed",
                "details": {
                    "ip": f"192.168.1.{100 + i}",
                    "user_agent": "Mozilla/5.0",
                    "duration_ms": 120 + i * 10
                }
            }
            for i in range(limit)
        ]
        
        return {
            "activities": activities,
            "total_count": 156,
            "page": 1,
            "per_page": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"활동 내역 조회 실패: {str(e)}")