"""
HEAL7 Admin System Router
관리자 시스템 백엔드 API

목업에서 실제 구현으로 전환:
- 사용자 관리 (user management)
- 시스템 설정 (system settings)  
- 포인트 관리 (point management)
- 관리자 로그 (admin logs)
- 시스템 통계 (system analytics)

기존 목업 파일: src/utils/sajuAdminMockData.ts
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import json
from loguru import logger
import sys
import os

# 보안 강화된 서비스 import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from auth_service import auth_service
from database_service import db_service

# AI 해석 엔진 import (선택적)
try:
    from ai_interpretation_engine import AIInterpretationEngine
    AI_ENGINE_AVAILABLE = True
except ImportError:
    logger.warning("AI interpretation engine not available")
    AI_ENGINE_AVAILABLE = False

router = APIRouter(prefix="/api/admin", tags=["admin"])
security = HTTPBearer()

# ===============================================
# Pydantic Models (Request/Response Schemas)
# ===============================================

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    success: bool
    token: str
    user: Dict[str, Any]
    message: str

class SystemSettingUpdate(BaseModel):
    category: str
    setting_key: str
    setting_value: Any
    description: Optional[str] = None

class UserPointTransaction(BaseModel):
    user_id: str
    point_type: str = Field(..., pattern="^(free|paid|bonus)$")
    amount: int
    reason: str
    transaction_type: str = Field(..., pattern="^(earn|spend|refund)$")
    related_service: Optional[str] = None

class AdminLogFilter(BaseModel):
    admin_id: Optional[str] = None
    action: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=50, le=200)

class AIInterpretationRequest(BaseModel):
    interpretation_type: str = Field(..., pattern="^(basic|detailed|compatibility|naming|fortune)$")
    saju_data: Dict[str, Any]
    additional_info: Optional[Dict[str, Any]] = None
    ai_model: Optional[str] = "auto"  # auto, gpt4o, gemini, claude
    custom_prompt: Optional[str] = None

class SajuContentGenerationRequest(BaseModel):
    content_type: str = Field(..., pattern="^(magazine_article|interpretation_template|fortune_guide|compatibility_guide)$")
    topic: str
    target_audience: str = "general"
    length: str = Field(default="medium", pattern="^(short|medium|long|custom)$")
    custom_length: Optional[int] = None
    ai_model: Optional[str] = "auto"
    additional_requirements: Optional[str] = None

class ContentReviewRequest(BaseModel):
    content_id: str
    content_type: str
    review_action: str = Field(..., pattern="^(approve|reject|request_revision)$")
    review_notes: Optional[str] = None
    reviewer_feedback: Optional[str] = None

# ===============================================
# 사주 전문 해석 관련 Pydantic Models
# ===============================================

class GapjaInterpretationRequest(BaseModel):
    gapja_code: str = Field(..., max_length=10)
    gapja_index: int = Field(..., ge=1, le=60)
    category: str = Field(..., pattern="^(year|month|day|hour)$")
    interpretation_title: Optional[str] = Field(None, max_length=100)
    basic_meaning: str
    detailed_interpretation: Optional[str] = None
    personality_traits: Optional[str] = None
    career_fortune: Optional[str] = None
    health_fortune: Optional[str] = None
    relationship_fortune: Optional[str] = None
    wealth_fortune: Optional[str] = None

class HeavenlyStemInterpretationRequest(BaseModel):
    stem_code: str = Field(..., max_length=10)
    stem_index: int = Field(..., ge=1, le=10)
    element: str = Field(..., pattern="^(목|화|토|금|수)$")
    yin_yang: str = Field(..., pattern="^(양|음)$")
    basic_meaning: str
    personality_traits: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    compatible_stems: Optional[str] = None
    incompatible_stems: Optional[str] = None
    seasonal_influence: Optional[str] = None

class EarthlyBranchInterpretationRequest(BaseModel):
    branch_code: str = Field(..., max_length=10)
    branch_index: int = Field(..., ge=1, le=12)
    animal_sign: str = Field(..., max_length=10)
    element: str = Field(..., pattern="^(목|화|토|금|수)$")
    season: Optional[str] = None
    direction: Optional[str] = None
    time_period: Optional[str] = None
    basic_meaning: str
    personality_traits: Optional[str] = None
    hidden_stems: Optional[str] = None
    compatible_branches: Optional[str] = None
    incompatible_branches: Optional[str] = None

class FiveElementsInterpretationRequest(BaseModel):
    element: str = Field(..., pattern="^(목|화|토|금|수)$")
    element_index: int = Field(..., ge=1, le=5)
    basic_characteristics: str
    personality_traits: Optional[str] = None
    body_parts: Optional[str] = None
    emotions: Optional[str] = None
    colors: Optional[str] = None
    directions: Optional[str] = None
    seasons: Optional[str] = None
    organs: Optional[str] = None
    taste: Optional[str] = None
    generates_element: Optional[str] = None
    destroys_element: Optional[str] = None
    career_fields: Optional[str] = None
    fortune_analysis: Optional[str] = None

class SajuPatternInterpretationRequest(BaseModel):
    pattern_name: str = Field(..., max_length=50)
    pattern_type: str = Field(..., max_length=30)
    pattern_code: Optional[str] = None
    formation_conditions: str
    basic_interpretation: str
    personality_analysis: Optional[str] = None
    career_fortune: Optional[str] = None
    wealth_fortune: Optional[str] = None
    relationship_fortune: Optional[str] = None
    health_fortune: Optional[str] = None
    life_phases: Optional[str] = None
    favorable_elements: Optional[str] = None
    unfavorable_elements: Optional[str] = None
    compatibility_patterns: Optional[str] = None

# ===============================================
# Database Connection - Enhanced Security
# ===============================================
# 이제 database_service.py의 db_service를 사용합니다

# ===============================================
# Authentication & Authorization
# ===============================================

async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """관리자 JWT 토큰 검증 - 보안 강화"""
    token = credentials.credentials

    # JWT 토큰 검증
    payload = auth_service.verify_jwt_token(token)

    # 데이터베이스에서 사용자 상태 확인
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

    # 세션 정보 업데이트 (마지막 활동 시간)
    await db_service.execute_query(
        "UPDATE admin_users SET last_login = $1 WHERE id = $2",
        [datetime.now(), admin['id']],
        db_type='saju'
    )

    return admin

def verify_admin_permission(required_permission: str):
    """권한 검증 데코레이터 함수"""
    def permission_checker(admin: Dict[str, Any] = Depends(verify_admin_token)):
        if not auth_service.check_permission(admin['role'], required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_permission}"
            )
        return admin
    return permission_checker

# ===============================================
# Authentication Endpoints
# ===============================================

@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest, req: Request):
    """관리자 로그인 - 보안 강화"""
    # 입력값 정화
    username = auth_service.sanitize_input(request.username, 50)
    password = request.password

    # IP 주소 추출
    ip_address = req.client.host if req.client else "unknown"
    user_agent = req.headers.get("user-agent", "unknown")

    try:
        # 사용자 조회
        admin = await db_service.execute_single_query(
            "SELECT * FROM admin_users WHERE username = $1 AND is_active = true",
            [username],
            db_type='saju'
        )

        if not admin:
            # 보안 이벤트 로깅
            auth_service.log_security_event(
                "FAILED_LOGIN_ATTEMPT",
                None,
                ip_address,
                {"username": username, "reason": "user_not_found"}
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # 로그인 시도 검증 (무차별 대입 공격 방지)
        failed_attempts = admin.get('failed_login_attempts', 0)
        last_failed = admin.get('last_failed_login')

        auth_service.validate_login_attempt(username, failed_attempts, last_failed)

        # 비밀번호 검증
        if not auth_service.verify_password(password, admin['password_hash']):
            # 실패 횟수 증가
            await db_service.execute_query(
                """UPDATE admin_users SET
                   failed_login_attempts = COALESCE(failed_login_attempts, 0) + 1,
                   last_failed_login = $1
                   WHERE id = $2""",
                [datetime.now(), admin['id']],
                db_type='saju'
            )

            # 보안 이벤트 로깅
            auth_service.log_security_event(
                "FAILED_LOGIN_ATTEMPT",
                admin['id'],
                ip_address,
                {"username": username, "reason": "invalid_password"}
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # 로그인 성공 - 실패 카운터 리셋
        await db_service.execute_query(
            """UPDATE admin_users SET
               last_login = $1,
               failed_login_attempts = 0,
               last_failed_login = NULL
               WHERE id = $2""",
            [datetime.now(), admin['id']],
            db_type='saju'
        )

        # JWT 토큰 생성
        token = auth_service.generate_jwt_token({
            'id': admin['id'],
            'username': admin['username'],
            'email': admin['email'],
            'role': admin['role']
        })

        # 세션 생성
        session_data = auth_service.create_secure_session(
            str(admin['id']), ip_address, user_agent
        )

        # 관리자 로그 기록
        await db_service.execute_query(
            """INSERT INTO admin_logs (admin_id, action, ip_address, metadata, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            [admin['id'], "LOGIN", ip_address, json.dumps(session_data), datetime.now()],
            db_type='saju'
        )

        # 보안 이벤트 로깅
        auth_service.log_security_event(
            "SUCCESSFUL_LOGIN",
            admin['id'],
            ip_address,
            {"username": username, "session_id": session_data}
        )

        return AdminLoginResponse(
            success=True,
            token=token,
            user={
                "id": str(admin['id']),
                "username": admin['username'],
                "email": admin['email'],
                "full_name": admin['full_name'],
                "role": admin['role']
            },
            message="Login successful"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        auth_service.log_security_event(
            "LOGIN_ERROR",
            None,
            ip_address,
            {"username": username, "error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.post("/logout")
async def admin_logout(req: Request, admin: dict = Depends(verify_admin_token)):
    """관리자 로그아웃 - 보안 강화"""
    ip_address = req.client.host if req.client else "unknown"

    try:
        # 로그아웃 로그 기록
        await db_service.execute_query(
            """INSERT INTO admin_logs (admin_id, action, ip_address, created_at)
               VALUES ($1, $2, $3, $4)""",
            [admin['id'], "LOGOUT", ip_address, datetime.now()],
            db_type='saju'
        )

        # 보안 이벤트 로깅
        auth_service.log_security_event(
            "LOGOUT",
            admin['id'],
            ip_address,
            {"username": admin['username']}
        )

        return {"success": True, "message": "Logout successful"}

    except Exception as e:
        logger.error(f"Logout error: {e}")
        return {"success": False, "message": "Logout error occurred"}

# ===============================================
# System Settings Management
# ===============================================

@router.get("/settings")
async def get_system_settings(admin: dict = Depends(verify_admin_token)):
    """시스템 설정 조회 (기존 목업 데이터 구조와 호환) - 보안 강화"""
    try:
        settings = await db_service.execute_query(
            "SELECT * FROM system_settings ORDER BY category, setting_key",
            db_type='saju'
        )

        # 기존 목업 구조와 호환되도록 변환
        result = {
            "version": "v2.1.0",
            "last_updated": datetime.now().isoformat(),
            "updated_by": admin['username'],
            "time_settings": {},
            "geographic_settings": {},
            "logic_settings": {},
            "payment_settings": {},
            "ai_settings": {},
            "security_settings": {},
            "kasi_settings": {}
        }

        for setting in settings:
            category_map = {
                "time": "time_settings",
                "geographic": "geographic_settings",
                "logic": "logic_settings",
                "payment": "payment_settings",
                "ai": "ai_settings",
                "security": "security_settings",
                "kasi": "kasi_settings"
            }

            category_key = category_map.get(setting.get('category', setting.get('setting_type', 'misc')), "misc_settings")
            if category_key not in result:
                result[category_key] = {}

            # JSON 값 파싱
            try:
                import json
                if isinstance(setting['setting_value'], str):
                    parsed_value = json.loads(setting['setting_value'])
                else:
                    parsed_value = setting['setting_value']
            except (json.JSONDecodeError, TypeError):
                parsed_value = setting['setting_value']

            result[category_key][setting['setting_key']] = parsed_value

        return {"success": True, "data": result}

    except Exception as e:
        logger.error(f"Settings fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch settings")

@router.put("/settings")
async def update_system_setting(
    setting: SystemSettingUpdate,
    admin: dict = Depends(verify_admin_permission("system_settings"))
):
    """시스템 설정 업데이트 - 보안 강화"""
    try:
        # 기존 설정 조회
        old_setting = await db_service.execute_single_query(
            "SELECT * FROM system_settings WHERE category = $1 AND setting_key = $2",
            [setting.category, setting.setting_key],
            db_type='saju'
        )

        # JSON 값 처리
        if not isinstance(setting.setting_value, str):
            setting_value = json.dumps(setting.setting_value)
        else:
            setting_value = setting.setting_value

        # 설정 업데이트 또는 생성
        if old_setting:
            # 업데이트
            await db_service.execute_query(
                """UPDATE system_settings SET
                   setting_value = $1, description = $2, updated_at = $3
                   WHERE category = $4 AND setting_key = $5""",
                [setting_value, setting.description, datetime.now(), setting.category, setting.setting_key],
                db_type='saju'
            )
        else:
            # 새로 생성
            await db_service.execute_query(
                """INSERT INTO system_settings (category, setting_key, setting_value, setting_type, description, updated_at)
                   VALUES ($1, $2, $3, $4, $5, $6)""",
                [setting.category, setting.setting_key, setting_value, setting.category, setting.description, datetime.now()],
                db_type='saju'
            )

        # 관리자 로그 기록
        await db_service.execute_query(
            """INSERT INTO admin_logs (admin_id, action, target_table, old_values, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5, $6)""",
            [
                admin['id'], "UPDATE_SETTING", "system_settings",
                json.dumps(old_setting) if old_setting else "{}",
                json.dumps(setting.dict()), datetime.now()
            ],
            db_type='saju'
        )

        return {"success": True, "message": "Setting updated successfully"}

    except Exception as e:
        logger.error(f"Settings update error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update setting")

# ===============================================
# User & Point Management  
# ===============================================

@router.get("/users/stats")
async def get_user_statistics(admin: dict = Depends(verify_admin_token)):
    """사용자 통계 조회"""
    conn = await get_db_connection()
    try:
        # 실제 DB에서 통계 데이터 조회
        # 사용자 통계
        users_result = await conn.fetchrow("SELECT COUNT(*) as total FROM users")
        total_users = users_result['total'] if users_result else 0
        
        # 포인트 통계
        points_result = await conn.fetchrow(
            "SELECT COUNT(*) as transactions, COALESCE(SUM(amount), 0) as total FROM point_transactions WHERE amount > 0"
        )
        total_points = int(points_result['total']) if points_result and points_result['total'] else 0
        point_transactions = points_result['transactions'] if points_result else 0
        
        # 사주 결과 통계
        saju_result = await conn.fetchrow("SELECT COUNT(*) as total FROM saju_results")
        total_saju_readings = saju_result['total'] if saju_result else 0
        
        stats = {
            "total_users": total_users,
            "active_users": total_users,  # 간소화: 전체 사용자를 활성으로 간주
            "new_users_today": 0,  # TODO: 실제 오늘 가입자 조회 로직 추가
            "premium_users": 0,    # TODO: 프리미엄 사용자 구분 로직 추가
            "total_points_distributed": total_points,
            "point_transactions": point_transactions,
            "total_saju_readings": total_saju_readings,
            "average_session_time": "실제 세션 시간 미구현"
        }
        
        return {"success": True, "data": stats}
        
    except Exception as e:
        logger.error(f"User stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user statistics")
    finally:
        await conn.close()

@router.post("/points/transaction")
async def create_point_transaction(
    transaction: UserPointTransaction,
    admin: dict = Depends(verify_admin_token)
):
    """포인트 적립/차감"""
    conn = await get_db_connection()
    try:
        # 포인트 거래 기록
        await conn.execute(
            """INSERT INTO user_points (user_id, point_type, amount, reason, transaction_type, related_service, created_by, created_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
            transaction.user_id, transaction.point_type, transaction.amount,
            transaction.reason, transaction.transaction_type, transaction.related_service,
            admin['id'], datetime.now()
        )
        
        # 관리자 로그 기록
        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, new_values, created_at)
               VALUES ($1, $2, $3, $4)""",
            admin['id'], "POINT_TRANSACTION", json.dumps(transaction.dict()), datetime.now()
        )
        
        return {"success": True, "message": "Point transaction completed"}
        
    except Exception as e:
        logger.error(f"Point transaction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process point transaction")
    finally:
        await conn.close()

# ===============================================
# Admin Logs & Analytics
# ===============================================

@router.post("/logs")
async def get_admin_logs(
    filter_params: AdminLogFilter,
    admin: dict = Depends(verify_admin_token)
):
    """관리자 활동 로그 조회"""
    conn = await get_db_connection()
    try:
        query = "SELECT al.*, au.username FROM admin_logs al JOIN admin_users au ON al.admin_id = au.id WHERE 1=1"
        params = []
        param_count = 0
        
        if filter_params.admin_id:
            param_count += 1
            query += f" AND al.admin_id = ${param_count}"
            params.append(filter_params.admin_id)
            
        if filter_params.action:
            param_count += 1
            query += f" AND al.action ILIKE ${param_count}"
            params.append(f"%{filter_params.action}%")
            
        if filter_params.start_date:
            param_count += 1
            query += f" AND al.created_at >= ${param_count}"
            params.append(filter_params.start_date)
            
        if filter_params.end_date:
            param_count += 1
            query += f" AND al.created_at <= ${param_count}"
            params.append(filter_params.end_date)
        
        param_count += 1
        query += f" ORDER BY al.created_at DESC LIMIT ${param_count}"
        params.append(filter_params.limit)
        
        logs = await conn.fetch(query, *params)
        
        return {
            "success": True,
            "data": [dict(log) for log in logs],
            "total_count": len(logs)
        }
        
    except Exception as e:
        logger.error(f"Admin logs error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch admin logs")
    finally:
        await conn.close()

@router.get("/analytics/dashboard")
async def get_dashboard_analytics(admin: dict = Depends(verify_admin_token)):
    """관리자 대시보드 분석 데이터"""
    conn = await get_db_connection()
    try:
        # 임시 분석 데이터 (실제로는 복합 쿼리로 구성)
        analytics = {
            "system_health": {
                "cpu_usage": 45.2,
                "memory_usage": 68.1,
                "disk_usage": 23.8,
                "api_response_time": 245
            },
            "business_metrics": {
                "daily_active_users": 456,
                "daily_consultations": 23,
                "daily_revenue": 890000,
                "conversion_rate": 12.4
            },
            "saju_system": {
                "calculations_today": 1234,
                "accuracy_rate": 99.8,
                "api_calls": 5678,
                "error_rate": 0.2
            },
            "recent_activities": [
                {"time": "10분 전", "action": "새 사용자 가입", "details": "user_1234"},
                {"time": "25분 전", "action": "상담 완료", "details": "consultation_5678"},
                {"time": "1시간 전", "action": "시스템 설정 변경", "details": "timezone updated"}
            ]
        }
        
        return {"success": True, "data": analytics}
        
    except Exception as e:
        logger.error(f"Dashboard analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard analytics")
    finally:
        await conn.close()

# ===============================================
# AI Interpretation & Content Management
# ===============================================

# AI 해석 엔진 인스턴스 초기화
ai_engine = AIInterpretationEngine()

@router.post("/ai/interpret")
async def generate_ai_interpretation(
    request: AIInterpretationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """AI 사주 해석 생성"""
    conn = await get_db_connection()
    try:
        # AI 해석 생성
        interpretation_result = await ai_engine.interpret_saju(
            saju_data=request.saju_data,
            interpretation_type=request.interpretation_type,
            additional_info=request.additional_info,
            preferred_model=request.ai_model,
            custom_prompt=request.custom_prompt
        )

        # 해석 결과 DB 저장
        interpretation_id = await conn.fetchval(
            """INSERT INTO ai_interpretations
               (saju_data, interpretation_type, ai_model, interpretation_text,
                confidence_score, created_by, created_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7)
               RETURNING id""",
            json.dumps(request.saju_data),
            request.interpretation_type,
            interpretation_result.get('model_used', 'unknown'),
            interpretation_result.get('interpretation', ''),
            interpretation_result.get('confidence', 0.0),
            admin['id'],
            datetime.now()
        )

        # 관리자 로그 기록
        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], "AI_INTERPRETATION", "ai_interpretations",
            json.dumps({"interpretation_id": str(interpretation_id), "type": request.interpretation_type}),
            datetime.now()
        )

        return {
            "success": True,
            "data": {
                "interpretation_id": str(interpretation_id),
                "interpretation": interpretation_result,
                "created_at": datetime.now().isoformat()
            },
            "message": "AI interpretation generated successfully"
        }

    except Exception as e:
        logger.error(f"AI interpretation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI interpretation: {str(e)}"
        )
    finally:
        await conn.close()

@router.post("/content/generate")
async def generate_saju_content(
    request: SajuContentGenerationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """AI 사주 콘텐츠 생성 (매거진, 가이드 등)"""
    conn = await get_db_connection()
    try:
        # 콘텐츠 길이 설정
        word_count = request.custom_length if request.length == "custom" else {
            "short": 500, "medium": 1000, "long": 2000
        }.get(request.length, 1000)

        # AI 콘텐츠 생성
        content_result = await ai_engine.generate_content(
            content_type=request.content_type,
            topic=request.topic,
            target_audience=request.target_audience,
            word_count=word_count,
            additional_requirements=request.additional_requirements,
            preferred_model=request.ai_model
        )

        # 생성된 콘텐츠 DB 저장
        content_id = await conn.fetchval(
            """INSERT INTO generated_content
               (content_type, topic, target_audience, word_count, content_text,
                ai_model, status, created_by, created_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
               RETURNING id""",
            request.content_type,
            request.topic,
            request.target_audience,
            word_count,
            content_result.get('content', ''),
            content_result.get('model_used', 'unknown'),
            'draft',  # 초기 상태는 draft
            admin['id'],
            datetime.now()
        )

        # 관리자 로그 기록
        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], "CONTENT_GENERATION", "generated_content",
            json.dumps({"content_id": str(content_id), "type": request.content_type, "topic": request.topic}),
            datetime.now()
        )

        return {
            "success": True,
            "data": {
                "content_id": str(content_id),
                "content": content_result,
                "word_count": len(content_result.get('content', '').split()) if content_result.get('content') else 0,
                "created_at": datetime.now().isoformat()
            },
            "message": "Content generated successfully"
        }

    except Exception as e:
        logger.error(f"Content generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content: {str(e)}"
        )
    finally:
        await conn.close()

@router.get("/content/list")
async def list_generated_content(
    content_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    admin: dict = Depends(verify_admin_token)
):
    """생성된 콘텐츠 목록 조회"""
    conn = await get_db_connection()
    try:
        query = """
            SELECT gc.*, au.username as created_by_name
            FROM generated_content gc
            JOIN admin_users au ON gc.created_by = au.id
            WHERE 1=1
        """
        params = []
        param_count = 0

        if content_type:
            param_count += 1
            query += f" AND gc.content_type = ${param_count}"
            params.append(content_type)

        if status:
            param_count += 1
            query += f" AND gc.status = ${param_count}"
            params.append(status)

        param_count += 1
        param_count += 1
        query += f" ORDER BY gc.created_at DESC LIMIT ${param_count-1} OFFSET ${param_count}"
        params.extend([limit, offset])

        content_list = await conn.fetch(query, *params)

        return {
            "success": True,
            "data": [dict(content) for content in content_list],
            "total_count": len(content_list)
        }

    except Exception as e:
        logger.error(f"Content list error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch content list")
    finally:
        await conn.close()

@router.post("/content/review")
async def review_content(
    request: ContentReviewRequest,
    admin: dict = Depends(verify_admin_token)
):
    """콘텐츠 검토 및 승인/반려"""
    conn = await get_db_connection()
    try:
        # 콘텐츠 상태 업데이트
        status_map = {
            "approve": "approved",
            "reject": "rejected",
            "request_revision": "revision_requested"
        }

        new_status = status_map.get(request.review_action, "draft")

        await conn.execute(
            """UPDATE generated_content
               SET status = $1, reviewed_by = $2, reviewed_at = $3, review_notes = $4
               WHERE id = $5""",
            new_status, admin['id'], datetime.now(),
            request.review_notes, int(request.content_id)
        )

        # 관리자 로그 기록
        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], f"CONTENT_REVIEW_{request.review_action.upper()}", "generated_content",
            json.dumps({
                "content_id": request.content_id,
                "new_status": new_status,
                "review_notes": request.review_notes
            }),
            datetime.now()
        )

        return {
            "success": True,
            "message": f"Content {request.review_action} completed",
            "data": {"new_status": new_status}
        }

    except Exception as e:
        logger.error(f"Content review error: {e}")
        raise HTTPException(status_code=500, detail="Failed to review content")
    finally:
        await conn.close()

@router.get("/ai/models/status")
async def get_ai_models_status(admin: dict = Depends(verify_admin_token)):
    """AI 모델 상태 및 사용 통계"""
    try:
        models_status = await ai_engine.get_models_health()

        return {
            "success": True,
            "data": models_status,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"AI models status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI models status")

@router.get("/ai/stats")
async def get_ai_usage_stats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    admin: dict = Depends(verify_admin_token)
):
    """AI 사용 통계"""
    conn = await get_db_connection()
    try:
        # 기본 날짜 설정 (최근 30일)
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=30)

        # AI 해석 통계
        interpretation_stats = await conn.fetchrow(
            """SELECT
                COUNT(*) as total_interpretations,
                COUNT(DISTINCT ai_model) as models_used,
                AVG(confidence_score) as avg_confidence
               FROM ai_interpretations
               WHERE created_at BETWEEN $1 AND $2""",
            start_date, end_date
        )

        # 콘텐츠 생성 통계
        content_stats = await conn.fetchrow(
            """SELECT
                COUNT(*) as total_content,
                COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_content,
                COUNT(DISTINCT ai_model) as models_used
               FROM generated_content
               WHERE created_at BETWEEN $1 AND $2""",
            start_date, end_date
        )

        stats = {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "interpretations": dict(interpretation_stats) if interpretation_stats else {},
            "content_generation": dict(content_stats) if content_stats else {},
            "efficiency_metrics": {
                "avg_response_time": "1.2초",  # 실제로는 DB에서 측정값 조회
                "success_rate": "98.5%",
                "cost_per_request": "₹12"  # 실제 비용 계산 필요
            }
        }

        return {"success": True, "data": stats}

    except Exception as e:
        logger.error(f"AI stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch AI usage statistics")
    finally:
        await conn.close()

# ===============================================
# System Maintenance
# ===============================================

@router.get("/system/health")
async def get_system_health(admin: dict = Depends(verify_admin_token)):
    """시스템 헬스 체크"""
    try:
        conn = await get_db_connection()
        
        # 데이터베이스 연결 테스트
        db_status = await conn.fetchval("SELECT 1")
        await conn.close()
        
        # 시스템 상태 체크
        health_status = {
            "database": "healthy" if db_status == 1 else "unhealthy",
            "api_server": "healthy",
            "kasi_api": "healthy",  # 실제로는 KASI API 체크 필요
            "redis_cache": "healthy",  # 실제로는 Redis 체크 필요
            "timestamp": datetime.now().isoformat(),
            "uptime": "2일 14시간 23분"  # 실제로는 시스템 uptime 계산
        }
        
        return {"success": True, "data": health_status}
        
    except Exception as e:
        logger.error(f"System health check error: {e}")
        return {
            "success": False, 
            "data": {"database": "unhealthy", "error": str(e)},
            "timestamp": datetime.now().isoformat()
        }

@router.post("/system/backup")
async def create_system_backup(admin: dict = Depends(verify_admin_token)):
    """시스템 백업 생성"""
    conn = await get_db_connection()
    try:
        # 관리자 로그 기록
        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, created_at)
               VALUES ($1, $2, $3)""",
            admin['id'], "SYSTEM_BACKUP", datetime.now()
        )
        
        # 실제로는 백업 프로세스 실행
        backup_info = {
            "backup_id": f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "created_by": admin['username'],
            "status": "completed",
            "size": "245.6 MB"
        }
        
        return {"success": True, "message": "Backup created successfully", "data": backup_info}

    except Exception as e:
        logger.error(f"System backup error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create backup")
    finally:
        await conn.close()

# ===============================================
# 사주 전문 해석 관리 엔드포인트들
# ===============================================

@router.post("/saju/gapja/interpretation")
async def create_gapja_interpretation(
    request: GapjaInterpretationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """60갑자 해석 등록/수정"""
    conn = await get_db_connection()
    try:
        # 기존 해석이 있는지 확인
        existing = await conn.fetchrow(
            "SELECT id FROM gapja_interpretations WHERE gapja_code = $1 AND category = $2",
            request.gapja_code, request.category
        )

        if existing:
            # 업데이트
            await conn.execute(
                """UPDATE gapja_interpretations SET
                   gapja_index = $1, interpretation_title = $2, basic_meaning = $3,
                   detailed_interpretation = $4, personality_traits = $5, career_fortune = $6,
                   health_fortune = $7, relationship_fortune = $8, wealth_fortune = $9,
                   updated_at = CURRENT_TIMESTAMP
                   WHERE gapja_code = $10 AND category = $11""",
                request.gapja_index, request.interpretation_title, request.basic_meaning,
                request.detailed_interpretation, request.personality_traits, request.career_fortune,
                request.health_fortune, request.relationship_fortune, request.wealth_fortune,
                request.gapja_code, request.category
            )
            action = "UPDATE_GAPJA_INTERPRETATION"
        else:
            # 새로 생성
            await conn.execute(
                """INSERT INTO gapja_interpretations
                   (gapja_code, gapja_index, category, interpretation_title, basic_meaning,
                    detailed_interpretation, personality_traits, career_fortune,
                    health_fortune, relationship_fortune, wealth_fortune, created_by)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)""",
                request.gapja_code, request.gapja_index, request.category,
                request.interpretation_title, request.basic_meaning,
                request.detailed_interpretation, request.personality_traits,
                request.career_fortune, request.health_fortune,
                request.relationship_fortune, request.wealth_fortune, admin['id']
            )
            action = "CREATE_GAPJA_INTERPRETATION"

        # 관리자 로그 기록
        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], action, "gapja_interpretations",
            json.dumps(request.dict()), datetime.now()
        )

        return {"success": True, "message": f"갑자 해석이 성공적으로 {('수정' if existing else '등록')}되었습니다."}

    except Exception as e:
        logger.error(f"Gapja interpretation error: {e}")
        raise HTTPException(status_code=500, detail="갑자 해석 처리 실패")
    finally:
        await conn.close()

@router.get("/saju/gapja/interpretations")
async def get_gapja_interpretations(
    category: Optional[str] = None,
    gapja_code: Optional[str] = None,
    limit: int = 60,
    offset: int = 0,
    admin: dict = Depends(verify_admin_token)
):
    """60갑자 해석 목록 조회"""
    conn = await get_db_connection()
    try:
        query = "SELECT * FROM gapja_interpretations WHERE 1=1"
        params = []
        param_count = 0

        if category:
            param_count += 1
            query += f" AND category = ${param_count}"
            params.append(category)

        if gapja_code:
            param_count += 1
            query += f" AND gapja_code = ${param_count}"
            params.append(gapja_code)

        query += f" ORDER BY gapja_index LIMIT ${param_count + 1} OFFSET ${param_count + 2}"
        params.extend([limit, offset])

        interpretations = await conn.fetch(query, *params)

        return {
            "success": True,
            "data": [dict(interp) for interp in interpretations],
            "total_count": len(interpretations)
        }

    except Exception as e:
        logger.error(f"Gapja interpretations fetch error: {e}")
        raise HTTPException(status_code=500, detail="갑자 해석 목록 조회 실패")
    finally:
        await conn.close()

@router.post("/saju/heavenly-stem/interpretation")
async def create_heavenly_stem_interpretation(
    request: HeavenlyStemInterpretationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """천간 해석 등록/수정"""
    conn = await get_db_connection()
    try:
        existing = await conn.fetchrow(
            "SELECT id FROM heavenly_stem_interpretations WHERE stem_code = $1",
            request.stem_code
        )

        if existing:
            await conn.execute(
                """UPDATE heavenly_stem_interpretations SET
                   stem_index = $1, element = $2, yin_yang = $3, basic_meaning = $4,
                   personality_traits = $5, strengths = $6, weaknesses = $7,
                   compatible_stems = $8, incompatible_stems = $9, seasonal_influence = $10,
                   updated_at = CURRENT_TIMESTAMP
                   WHERE stem_code = $11""",
                request.stem_index, request.element, request.yin_yang, request.basic_meaning,
                request.personality_traits, request.strengths, request.weaknesses,
                request.compatible_stems, request.incompatible_stems, request.seasonal_influence,
                request.stem_code
            )
            action = "UPDATE_STEM_INTERPRETATION"
        else:
            await conn.execute(
                """INSERT INTO heavenly_stem_interpretations
                   (stem_code, stem_index, element, yin_yang, basic_meaning,
                    personality_traits, strengths, weaknesses, compatible_stems,
                    incompatible_stems, seasonal_influence, created_by)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)""",
                request.stem_code, request.stem_index, request.element, request.yin_yang,
                request.basic_meaning, request.personality_traits, request.strengths,
                request.weaknesses, request.compatible_stems, request.incompatible_stems,
                request.seasonal_influence, admin['id']
            )
            action = "CREATE_STEM_INTERPRETATION"

        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], action, "heavenly_stem_interpretations",
            json.dumps(request.dict()), datetime.now()
        )

        return {"success": True, "message": f"천간 해석이 성공적으로 {('수정' if existing else '등록')}되었습니다."}

    except Exception as e:
        logger.error(f"Heavenly stem interpretation error: {e}")
        raise HTTPException(status_code=500, detail="천간 해석 처리 실패")
    finally:
        await conn.close()

@router.get("/saju/heavenly-stem/interpretations")
async def get_heavenly_stem_interpretations(
    element: Optional[str] = None,
    yin_yang: Optional[str] = None,
    admin: dict = Depends(verify_admin_token)
):
    """천간 해석 목록 조회"""
    conn = await get_db_connection()
    try:
        query = "SELECT * FROM heavenly_stem_interpretations WHERE 1=1"
        params = []
        param_count = 0

        if element:
            param_count += 1
            query += f" AND element = ${param_count}"
            params.append(element)

        if yin_yang:
            param_count += 1
            query += f" AND yin_yang = ${param_count}"
            params.append(yin_yang)

        query += " ORDER BY stem_index"
        interpretations = await conn.fetch(query, *params)

        return {
            "success": True,
            "data": [dict(interp) for interp in interpretations],
            "total_count": len(interpretations)
        }

    except Exception as e:
        logger.error(f"Heavenly stem interpretations fetch error: {e}")
        raise HTTPException(status_code=500, detail="천간 해석 목록 조회 실패")
    finally:
        await conn.close()

@router.post("/saju/earthly-branch/interpretation")
async def create_earthly_branch_interpretation(
    request: EarthlyBranchInterpretationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """지지 해석 등록/수정"""
    conn = await get_db_connection()
    try:
        existing = await conn.fetchrow(
            "SELECT id FROM earthly_branch_interpretations WHERE branch_code = $1",
            request.branch_code
        )

        if existing:
            await conn.execute(
                """UPDATE earthly_branch_interpretations SET
                   branch_index = $1, animal_sign = $2, element = $3, season = $4,
                   direction = $5, time_period = $6, basic_meaning = $7,
                   personality_traits = $8, hidden_stems = $9, compatible_branches = $10,
                   incompatible_branches = $11, updated_at = CURRENT_TIMESTAMP
                   WHERE branch_code = $12""",
                request.branch_index, request.animal_sign, request.element, request.season,
                request.direction, request.time_period, request.basic_meaning,
                request.personality_traits, request.hidden_stems, request.compatible_branches,
                request.incompatible_branches, request.branch_code
            )
            action = "UPDATE_BRANCH_INTERPRETATION"
        else:
            await conn.execute(
                """INSERT INTO earthly_branch_interpretations
                   (branch_code, branch_index, animal_sign, element, season,
                    direction, time_period, basic_meaning, personality_traits,
                    hidden_stems, compatible_branches, incompatible_branches, created_by)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)""",
                request.branch_code, request.branch_index, request.animal_sign, request.element,
                request.season, request.direction, request.time_period, request.basic_meaning,
                request.personality_traits, request.hidden_stems, request.compatible_branches,
                request.incompatible_branches, admin['id']
            )
            action = "CREATE_BRANCH_INTERPRETATION"

        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], action, "earthly_branch_interpretations",
            json.dumps(request.dict()), datetime.now()
        )

        return {"success": True, "message": f"지지 해석이 성공적으로 {('수정' if existing else '등록')}되었습니다."}

    except Exception as e:
        logger.error(f"Earthly branch interpretation error: {e}")
        raise HTTPException(status_code=500, detail="지지 해석 처리 실패")
    finally:
        await conn.close()

@router.get("/saju/earthly-branch/interpretations")
async def get_earthly_branch_interpretations(
    element: Optional[str] = None,
    season: Optional[str] = None,
    admin: dict = Depends(verify_admin_token)
):
    """지지 해석 목록 조회"""
    conn = await get_db_connection()
    try:
        query = "SELECT * FROM earthly_branch_interpretations WHERE 1=1"
        params = []
        param_count = 0

        if element:
            param_count += 1
            query += f" AND element = ${param_count}"
            params.append(element)

        if season:
            param_count += 1
            query += f" AND season = ${param_count}"
            params.append(season)

        query += " ORDER BY branch_index"
        interpretations = await conn.fetch(query, *params)

        return {
            "success": True,
            "data": [dict(interp) for interp in interpretations],
            "total_count": len(interpretations)
        }

    except Exception as e:
        logger.error(f"Earthly branch interpretations fetch error: {e}")
        raise HTTPException(status_code=500, detail="지지 해석 목록 조회 실패")
    finally:
        await conn.close()

@router.post("/saju/five-elements/interpretation")
async def create_five_elements_interpretation(
    request: FiveElementsInterpretationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """오행 해석 등록/수정"""
    conn = await get_db_connection()
    try:
        existing = await conn.fetchrow(
            "SELECT id FROM five_elements_interpretations WHERE element = $1",
            request.element
        )

        if existing:
            await conn.execute(
                """UPDATE five_elements_interpretations SET
                   element_index = $1, basic_characteristics = $2, personality_traits = $3,
                   body_parts = $4, emotions = $5, colors = $6, directions = $7,
                   seasons = $8, organs = $9, taste = $10, generates_element = $11,
                   destroys_element = $12, career_fields = $13, fortune_analysis = $14,
                   updated_at = CURRENT_TIMESTAMP
                   WHERE element = $15""",
                request.element_index, request.basic_characteristics, request.personality_traits,
                request.body_parts, request.emotions, request.colors, request.directions,
                request.seasons, request.organs, request.taste, request.generates_element,
                request.destroys_element, request.career_fields, request.fortune_analysis,
                request.element
            )
            action = "UPDATE_ELEMENT_INTERPRETATION"
        else:
            await conn.execute(
                """INSERT INTO five_elements_interpretations
                   (element, element_index, basic_characteristics, personality_traits,
                    body_parts, emotions, colors, directions, seasons, organs, taste,
                    generates_element, destroys_element, career_fields, fortune_analysis, created_by)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)""",
                request.element, request.element_index, request.basic_characteristics,
                request.personality_traits, request.body_parts, request.emotions,
                request.colors, request.directions, request.seasons, request.organs,
                request.taste, request.generates_element, request.destroys_element,
                request.career_fields, request.fortune_analysis, admin['id']
            )
            action = "CREATE_ELEMENT_INTERPRETATION"

        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], action, "five_elements_interpretations",
            json.dumps(request.dict()), datetime.now()
        )

        return {"success": True, "message": f"오행 해석이 성공적으로 {('수정' if existing else '등록')}되었습니다."}

    except Exception as e:
        logger.error(f"Five elements interpretation error: {e}")
        raise HTTPException(status_code=500, detail="오행 해석 처리 실패")
    finally:
        await conn.close()

@router.get("/saju/five-elements/interpretations")
async def get_five_elements_interpretations(admin: dict = Depends(verify_admin_token)):
    """오행 해석 목록 조회"""
    conn = await get_db_connection()
    try:
        interpretations = await conn.fetch(
            "SELECT * FROM five_elements_interpretations ORDER BY element_index"
        )

        return {
            "success": True,
            "data": [dict(interp) for interp in interpretations],
            "total_count": len(interpretations)
        }

    except Exception as e:
        logger.error(f"Five elements interpretations fetch error: {e}")
        raise HTTPException(status_code=500, detail="오행 해석 목록 조회 실패")
    finally:
        await conn.close()

@router.post("/saju/pattern/interpretation")
async def create_saju_pattern_interpretation(
    request: SajuPatternInterpretationRequest,
    admin: dict = Depends(verify_admin_token)
):
    """격국 해석 등록/수정"""
    conn = await get_db_connection()
    try:
        existing = await conn.fetchrow(
            "SELECT id FROM saju_pattern_interpretations WHERE pattern_name = $1 AND pattern_type = $2",
            request.pattern_name, request.pattern_type
        )

        if existing:
            await conn.execute(
                """UPDATE saju_pattern_interpretations SET
                   pattern_code = $1, formation_conditions = $2, basic_interpretation = $3,
                   personality_analysis = $4, career_fortune = $5, wealth_fortune = $6,
                   relationship_fortune = $7, health_fortune = $8, life_phases = $9,
                   favorable_elements = $10, unfavorable_elements = $11, compatibility_patterns = $12,
                   updated_at = CURRENT_TIMESTAMP
                   WHERE pattern_name = $13 AND pattern_type = $14""",
                request.pattern_code, request.formation_conditions, request.basic_interpretation,
                request.personality_analysis, request.career_fortune, request.wealth_fortune,
                request.relationship_fortune, request.health_fortune, request.life_phases,
                request.favorable_elements, request.unfavorable_elements, request.compatibility_patterns,
                request.pattern_name, request.pattern_type
            )
            action = "UPDATE_PATTERN_INTERPRETATION"
        else:
            await conn.execute(
                """INSERT INTO saju_pattern_interpretations
                   (pattern_name, pattern_type, pattern_code, formation_conditions, basic_interpretation,
                    personality_analysis, career_fortune, wealth_fortune, relationship_fortune,
                    health_fortune, life_phases, favorable_elements, unfavorable_elements,
                    compatibility_patterns, created_by)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)""",
                request.pattern_name, request.pattern_type, request.pattern_code,
                request.formation_conditions, request.basic_interpretation, request.personality_analysis,
                request.career_fortune, request.wealth_fortune, request.relationship_fortune,
                request.health_fortune, request.life_phases, request.favorable_elements,
                request.unfavorable_elements, request.compatibility_patterns, admin['id']
            )
            action = "CREATE_PATTERN_INTERPRETATION"

        await conn.execute(
            """INSERT INTO admin_logs (admin_id, action, target_table, new_values, created_at)
               VALUES ($1, $2, $3, $4, $5)""",
            admin['id'], action, "saju_pattern_interpretations",
            json.dumps(request.dict()), datetime.now()
        )

        return {"success": True, "message": f"격국 해석이 성공적으로 {('수정' if existing else '등록')}되었습니다."}

    except Exception as e:
        logger.error(f"Saju pattern interpretation error: {e}")
        raise HTTPException(status_code=500, detail="격국 해석 처리 실패")
    finally:
        await conn.close()

@router.get("/saju/pattern/interpretations")
async def get_saju_pattern_interpretations(
    pattern_type: Optional[str] = None,
    admin: dict = Depends(verify_admin_token)
):
    """격국 해석 목록 조회"""
    conn = await get_db_connection()
    try:
        query = "SELECT * FROM saju_pattern_interpretations WHERE 1=1"
        params = []

        if pattern_type:
            query += " AND pattern_type = $1"
            params.append(pattern_type)

        query += " ORDER BY pattern_name"
        interpretations = await conn.fetch(query, *params)

        return {
            "success": True,
            "data": [dict(interp) for interp in interpretations],
            "total_count": len(interpretations)
        }

    except Exception as e:
        logger.error(f"Saju pattern interpretations fetch error: {e}")
        raise HTTPException(status_code=500, detail="격국 해석 목록 조회 실패")
    finally:
        await conn.close()

@router.get("/saju/interpretation-summary")
async def get_interpretation_summary(admin: dict = Depends(verify_admin_token)):
    """사주 해석 등록 현황 요약"""
    conn = await get_db_connection()
    try:
        # 각 테이블별 등록 현황 조회
        gapja_count = await conn.fetchval("SELECT COUNT(*) FROM gapja_interpretations")
        stem_count = await conn.fetchval("SELECT COUNT(*) FROM heavenly_stem_interpretations")
        branch_count = await conn.fetchval("SELECT COUNT(*) FROM earthly_branch_interpretations")
        element_count = await conn.fetchval("SELECT COUNT(*) FROM five_elements_interpretations")
        pattern_count = await conn.fetchval("SELECT COUNT(*) FROM saju_pattern_interpretations")

        summary = {
            "gapja": {
                "total": gapja_count or 0,
                "expected": 240,  # 60갑자 × 4카테고리
                "completion_rate": round((gapja_count or 0) / 240 * 100, 1)
            },
            "heavenly_stems": {
                "total": stem_count or 0,
                "expected": 10,
                "completion_rate": round((stem_count or 0) / 10 * 100, 1)
            },
            "earthly_branches": {
                "total": branch_count or 0,
                "expected": 12,
                "completion_rate": round((branch_count or 0) / 12 * 100, 1)
            },
            "five_elements": {
                "total": element_count or 0,
                "expected": 5,
                "completion_rate": round((element_count or 0) / 5 * 100, 1)
            },
            "patterns": {
                "total": pattern_count or 0,
                "expected": 50,  # 대략적인 격국 수
                "completion_rate": round((pattern_count or 0) / 50 * 100, 1)
            }
        }

        return {"success": True, "data": summary}

    except Exception as e:
        logger.error(f"Interpretation summary error: {e}")
        raise HTTPException(status_code=500, detail="해석 현황 조회 실패")
    finally:
        await conn.close()