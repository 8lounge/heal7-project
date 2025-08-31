#!/usr/bin/env python3
"""
Notification API - Dashboard Service Integration
기존 포트 8000에 통합된 알림 시스템 API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# 라우터 생성
router = APIRouter(prefix="/api/notification", tags=["알림 관리"])

# 데이터 모델
class NotificationType(str, Enum):
    EMAIL = "email"
    KAKAO = "kakao"
    BOTH = "both"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RETRY = "retry"

class EmailNotification(BaseModel):
    to_email: EmailStr
    subject: str
    content: str
    content_type: str = "html"  # html or plain
    template_id: Optional[str] = None

class KakaoNotification(BaseModel):
    user_id: int
    message: str
    template_id: Optional[str] = None
    button_title: Optional[str] = None
    button_url: Optional[str] = None

class BulkNotification(BaseModel):
    notification_type: NotificationType
    user_ids: List[int]
    subject: Optional[str] = None
    content: str
    template_id: Optional[str] = None

class NotificationTemplate(BaseModel):
    id: Optional[str] = None
    name: str
    type: NotificationType
    subject_template: Optional[str] = None
    content_template: str
    variables: List[str] = []

class NotificationHistory(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    notification_type: NotificationType
    status: NotificationStatus
    subject: Optional[str] = None
    content: str
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None

# 목업 템플릿
mock_templates = [
    {
        "id": "welcome_email",
        "name": "회원가입 환영 메일",
        "type": "email",
        "subject_template": "[HEAL7] {username}님, 환영합니다!",
        "content_template": """
        <h2>HEAL7에 오신 것을 환영합니다!</h2>
        <p>안녕하세요, {username}님!</p>
        <p>HEAL7 회원가입을 축하드립니다.</p>
        <p>지금부터 다양한 운세 서비스를 이용하실 수 있습니다.</p>
        <a href="{login_url}">로그인하기</a>
        """,
        "variables": ["username", "login_url"]
    },
    {
        "id": "payment_success",
        "name": "결제 완료 알림",
        "type": "both",
        "subject_template": "[HEAL7] 결제가 완료되었습니다",
        "content_template": """
        {username}님의 {plan_name} 결제가 완료되었습니다.
        결제 금액: {amount}원
        유효기간: {expires_at}까지
        """,
        "variables": ["username", "plan_name", "amount", "expires_at"]
    },
    {
        "id": "consultation_reminder",
        "name": "상담 예약 알림",
        "type": "kakao",
        "content_template": """
        {username}님, 예약하신 상담이 {consultation_time}에 시작됩니다.
        상담사: {consultant_name}
        """,
        "variables": ["username", "consultation_time", "consultant_name"]
    }
]

mock_history = [
    {
        "id": 1,
        "user_id": 1,
        "notification_type": "email",
        "status": "sent",
        "subject": "[HEAL7] 프리미엄 업그레이드 완료",
        "content": "프리미엄 서비스 이용이 시작되었습니다.",
        "sent_at": "2024-08-25T10:30:00",
        "error_message": None
    }
]

async def _send_email_task(email_data: EmailNotification):
    """이메일 발송 백그라운드 태스크"""
    try:
        # 실제 구현시 SMTP 서버 사용
        print(f"[EMAIL] To: {email_data.to_email}")
        print(f"[EMAIL] Subject: {email_data.subject}")
        print(f"[EMAIL] Content: {email_data.content[:50]}...")
        
        # 목업: 성공으로 처리
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")
        return False

async def _send_kakao_task(kakao_data: KakaoNotification):
    """카카오톡 발송 백그라운드 태스크"""
    try:
        # 실제 구현시 카카오 API 사용
        print(f"[KAKAO] To User: {kakao_data.user_id}")
        print(f"[KAKAO] Message: {kakao_data.message[:50]}...")
        
        # 목업: 성공으로 처리
        return True
    except Exception as e:
        print(f"[KAKAO ERROR] {str(e)}")
        return False

async def _bulk_send_task(bulk_data: BulkNotification):
    """대량 발송 백그라운드 태스크"""
    success_count = 0
    for user_id in bulk_data.user_ids:
        try:
            print(f"[BULK {bulk_data.upper()}] To User: {user_id}")
            print(f"[BULK] Content: {bulk_data.content[:30]}...")
            success_count += 1
        except Exception as e:
            print(f"[BULK ERROR] User {user_id}: {str(e)}")
    
    print(f"[BULK COMPLETE] {success_count}/{len(bulk_data.user_ids)} 성공")

@router.post("/email/send")
async def send_email(email_data: EmailNotification, background_tasks: BackgroundTasks):
    """이메일 발송"""
    background_tasks.add_task(_send_email_task, email_data)
    
    # 히스토리 기록
    history = {
        "id": len(mock_history) + 1,
        "user_id": None,  # 이메일로만 식별
        "notification_type": "email",
        "status": "pending",
        "subject": email_data.subject,
        "content": email_data.content[:100] + "...",
        "sent_at": datetime.now().isoformat(),
        "error_message": None
    }
    mock_history.append(history)
    
    return {
        "message": "이메일 발송이 예약되었습니다",
        "to": email_data.to_email,
        "subject": email_data.subject,
        "status": "pending"
    }

@router.post("/kakao/send")
async def send_kakao(kakao_data: KakaoNotification, background_tasks: BackgroundTasks):
    """카카오톡 발송"""
    background_tasks.add_task(_send_kakao_task, kakao_data)
    
    # 히스토리 기록
    history = {
        "id": len(mock_history) + 1,
        "user_id": kakao_data.user_id,
        "notification_type": "kakao",
        "status": "pending",
        "subject": None,
        "content": kakao_data.message[:100] + "...",
        "sent_at": datetime.now().isoformat(),
        "error_message": None
    }
    mock_history.append(history)
    
    return {
        "message": "카카오톡 발송이 예약되었습니다",
        "user_id": kakao_data.user_id,
        "status": "pending"
    }

@router.post("/bulk-send")
async def bulk_send(bulk_data: BulkNotification, background_tasks: BackgroundTasks):
    """대량 발송"""
    background_tasks.add_task(_bulk_send_task, bulk_data)
    
    return {
        "message": f"{len(bulk_data.user_ids)}명에게 {bulk_data.notification_type} 발송이 예약되었습니다",
        "user_count": len(bulk_data.user_ids),
        "type": bulk_data.notification_type,
        "status": "pending"
    }

@router.get("/templates")
async def get_templates():
    """알림 템플릿 목록"""
    return {
        "templates": mock_templates,
        "total": len(mock_templates)
    }

@router.post("/templates")
async def create_template(template: NotificationTemplate):
    """알림 템플릿 생성"""
    template_dict = template.dict()
    template_dict["id"] = f"template_{len(mock_templates) + 1}"
    mock_templates.append(template_dict)
    
    return {
        "message": "템플릿이 생성되었습니다",
        "template": template_dict
    }

@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """특정 템플릿 조회"""
    template = next((t for t in mock_templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다")
    return template

@router.post("/templates/{template_id}/send")
async def send_with_template(
    template_id: str, 
    user_id: int,
    variables: Dict[str, str],
    notification_type: Optional[NotificationType] = None
):
    """템플릿을 사용한 알림 발송"""
    template = next((t for t in mock_templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다")
    
    # 변수 치환
    content = template["content_template"]
    subject = template.get("subject_template", "")
    
    for var, value in variables.items():
        content = content.replace(f"{{{var}}}", str(value))
        if subject:
            subject = subject.replace(f"{{{var}}}", str(value))
    
    send_type = notification_type or template["type"]
    
    return {
        "message": f"템플릿 '{template['name']}'을 사용한 {send_type} 발송 완료",
        "template_id": template_id,
        "user_id": user_id,
        "content": content[:100] + "..."
    }

@router.get("/history")
async def get_history(
    user_id: Optional[int] = None,
    notification_type: Optional[NotificationType] = None,
    limit: int = 50
):
    """알림 발송 이력"""
    history = mock_history.copy()
    
    if user_id:
        history = [h for h in history if h["user_id"] == user_id]
    if notification_type:
        history = [h for h in history if h["notification_type"] == notification_type]
    
    return {
        "history": history[-limit:],  # 최근 항목부터
        "total": len(history)
    }

@router.get("/stats")
async def get_notification_stats():
    """알림 발송 통계"""
    total_sent = len([h for h in mock_history if h["status"] == "sent"])
    total_failed = len([h for h in mock_history if h["status"] == "failed"])
    
    type_stats = {}
    for history in mock_history:
        ntype = history["notification_type"]
        type_stats[ntype] = type_stats.get(ntype, 0) + 1
    
    return {
        "total_notifications": len(mock_history),
        "success_rate": (total_sent / len(mock_history) * 100) if mock_history else 0,
        "failed_count": total_failed,
        "type_distribution": type_stats,
        "templates_count": len(mock_templates)
    }