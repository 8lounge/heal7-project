#!/usr/bin/env python3
"""
Content Management API - Dashboard Service Integration  
기존 포트 8000에 통합된 콘텐츠 관리 API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# 라우터 생성
router = APIRouter(prefix="/api/content-management", tags=["콘텐츠 관리"])

# 데이터 모델
class ContentType(str, Enum):
    MAGAZINE = "magazine"
    NOTICE = "notice"
    CONSULTATION = "consultation"
    FAQ = "faq"

class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"

class ConsultationStatus(str, Enum):
    REQUESTED = "requested"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Content(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    content_type: ContentType
    status: ContentStatus
    author_id: int
    author_name: str
    category_id: Optional[int] = None
    tags: List[str] = []
    views: int = 0
    likes: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

class Category(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    content_type: ContentType
    created_at: Optional[datetime] = None

class ConsultationSession(BaseModel):
    id: Optional[int] = None
    user_id: int
    consultant_id: Optional[int] = None
    title: str
    description: str
    status: ConsultationStatus
    consultation_type: str  # "saju", "tarot", "dream" etc.
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    messages: List[Dict[str, Any]] = []
    rating: Optional[int] = None
    feedback: Optional[str] = None

# 목업 데이터
mock_categories = [
    {"id": 1, "name": "운세 트렌드", "description": "최신 운세 동향", "content_type": "magazine"},
    {"id": 2, "name": "시스템 공지", "description": "시스템 관련 공지", "content_type": "notice"},
    {"id": 3, "name": "사주 상담", "description": "사주명리 상담", "content_type": "consultation"},
    {"id": 4, "name": "타로 상담", "description": "타로카드 상담", "content_type": "consultation"}
]

mock_contents = [
    {
        "id": 1,
        "title": "2024년 하반기 운세 동향",
        "content": "2024년 하반기 전체적인 운세 흐름을 분석해보겠습니다...",
        "content_type": "magazine",
        "status": "published",
        "author_id": 1,
        "author_name": "치유마녀 에디터",
        "category_id": 1,
        "tags": ["운세", "2024년", "트렌드"],
        "views": 1250,
        "likes": 89,
        "created_at": "2024-08-20T10:00:00",
        "published_at": "2024-08-20T14:00:00"
    },
    {
        "id": 2,
        "title": "AI 꿈해몽 서비스 정식 오픈",
        "content": "AI 기반 꿈해몽 서비스가 정식으로 오픈되었습니다...",
        "content_type": "notice",
        "status": "published",
        "author_id": 2,
        "author_name": "관리자",
        "category_id": 2,
        "tags": ["공지", "AI", "꿈해몽"],
        "views": 2100,
        "likes": 45,
        "created_at": "2024-08-25T09:00:00",
        "published_at": "2024-08-25T10:00:00"
    }
]

mock_consultations = [
    {
        "id": 1,
        "user_id": 1,
        "consultant_id": 3,
        "title": "2024년 취업운 상담 요청",
        "description": "올해 하반기 취업 계획이 있어 상담 요청드립니다.",
        "status": "completed",
        "consultation_type": "saju",
        "scheduled_at": "2024-08-26T14:00:00",
        "started_at": "2024-08-26T14:05:00",
        "completed_at": "2024-08-26T15:30:00",
        "messages": [
            {
                "id": 1,
                "sender_type": "user",
                "sender_id": 1,
                "message": "안녕하세요, 취업운 상담 부탁드립니다.",
                "sent_at": "2024-08-26T14:05:00"
            }
        ],
        "rating": 5,
        "feedback": "매우 만족스러운 상담이었습니다!"
    }
]

@router.get("/contents")
async def get_contents(
    content_type: Optional[ContentType] = None,
    status: Optional[ContentStatus] = None,
    category_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200)
):
    """콘텐츠 목록 조회"""
    contents = mock_contents.copy()
    
    # 필터링
    if content_type:
        contents = [c for c in contents if c["content_type"] == content_type]
    if status:
        contents = [c for c in contents if c["status"] == status]
    if category_id:
        contents = [c for c in contents if c["category_id"] == category_id]
    
    total = len(contents)
    contents = contents[skip:skip + limit]
    
    return {
        "contents": contents,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.post("/contents")
async def create_content(content_data: Content):
    """새 콘텐츠 생성"""
    new_content = content_data.dict()
    new_content["id"] = len(mock_contents) + 1
    new_content["created_at"] = datetime.now().isoformat()
    new_content["views"] = 0
    new_content["likes"] = 0
    
    if content_data.status == ContentStatus.PUBLISHED:
        new_content["published_at"] = datetime.now().isoformat()
    
    mock_contents.append(new_content)
    
    return {
        "message": "콘텐츠가 생성되었습니다",
        "content": new_content
    }

@router.get("/contents/{content_id}")
async def get_content(content_id: int):
    """특정 콘텐츠 조회"""
    content = next((c for c in mock_contents if c["id"] == content_id), None)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
    
    # 조회수 증가
    content["views"] += 1
    
    return content

@router.put("/contents/{content_id}")
async def update_content(content_id: int, update_data: Dict[str, Any]):
    """콘텐츠 수정"""
    content = next((c for c in mock_contents if c["id"] == content_id), None)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
    
    # 발행 상태 변경시 발행일 설정
    if update_data.get("status") == "published" and content["status"] != "published":
        update_data["published_at"] = datetime.now().isoformat()
    
    update_data["updated_at"] = datetime.now().isoformat()
    content.update(update_data)
    
    return {
        "message": "콘텐츠가 수정되었습니다",
        "content": content
    }

@router.delete("/contents/{content_id}")
async def delete_content(content_id: int):
    """콘텐츠 삭제 (소프트 삭제)"""
    content = next((c for c in mock_contents if c["id"] == content_id), None)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
    
    content["status"] = "deleted"
    content["updated_at"] = datetime.now().isoformat()
    
    return {"message": "콘텐츠가 삭제되었습니다"}

@router.get("/magazines")
async def get_magazines(
    category_id: Optional[int] = None,
    status: Optional[ContentStatus] = None,
    skip: int = 0,
    limit: int = 20
):
    """매거진 기사 목록"""
    magazines = [c for c in mock_contents if c["content_type"] == "magazine"]
    
    if category_id:
        magazines = [m for m in magazines if m["category_id"] == category_id]
    if status:
        magazines = [m for m in magazines if m["status"] == status]
    
    return {
        "magazines": magazines[skip:skip + limit],
        "total": len(magazines)
    }

@router.get("/notices")
async def get_notices(
    status: Optional[ContentStatus] = None,
    skip: int = 0,
    limit: int = 50
):
    """공지사항 목록"""
    notices = [c for c in mock_contents if c["content_type"] == "notice"]
    
    if status:
        notices = [n for n in notices if n["status"] == status]
    
    # 최신순 정렬
    notices.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return {
        "notices": notices[skip:skip + limit],
        "total": len(notices)
    }

@router.get("/consultations")
async def get_consultations(
    status: Optional[ConsultationStatus] = None,
    consultation_type: Optional[str] = None,
    user_id: Optional[int] = None,
    consultant_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50
):
    """상담 세션 목록"""
    consultations = mock_consultations.copy()
    
    if status:
        consultations = [c for c in consultations if c["status"] == status]
    if consultation_type:
        consultations = [c for c in consultations if c["consultation_type"] == consultation_type]
    if user_id:
        consultations = [c for c in consultations if c["user_id"] == user_id]
    if consultant_id:
        consultations = [c for c in consultations if c["consultant_id"] == consultant_id]
    
    return {
        "consultations": consultations[skip:skip + limit],
        "total": len(consultations)
    }

@router.post("/consultations")
async def create_consultation(consultation_data: ConsultationSession):
    """새 상담 세션 생성"""
    new_consultation = consultation_data.dict()
    new_consultation["id"] = len(mock_consultations) + 1
    
    mock_consultations.append(new_consultation)
    
    return {
        "message": "상담 세션이 생성되었습니다",
        "consultation": new_consultation
    }

@router.put("/consultations/{consultation_id}/status")
async def update_consultation_status(consultation_id: int, new_status: ConsultationStatus):
    """상담 상태 변경"""
    consultation = next((c for c in mock_consultations if c["id"] == consultation_id), None)
    if not consultation:
        raise HTTPException(status_code=404, detail="상담을 찾을 수 없습니다")
    
    old_status = consultation["status"]
    consultation["status"] = new_status
    
    # 상태별 시간 기록
    now = datetime.now().isoformat()
    if new_status == "in_progress":
        consultation["started_at"] = now
    elif new_status == "completed":
        consultation["completed_at"] = now
    
    return {
        "message": f"상담 상태가 {old_status}에서 {new_status}로 변경되었습니다",
        "consultation": consultation
    }

@router.get("/categories")
async def get_categories(content_type: Optional[ContentType] = None):
    """카테고리 목록"""
    categories = mock_categories.copy()
    
    if content_type:
        categories = [c for c in categories if c["content_type"] == content_type]
    
    return {
        "categories": categories,
        "total": len(categories)
    }

@router.post("/categories")
async def create_category(category_data: Category):
    """새 카테고리 생성"""
    new_category = category_data.dict()
    new_category["id"] = len(mock_categories) + 1
    new_category["created_at"] = datetime.now().isoformat()
    
    mock_categories.append(new_category)
    
    return {
        "message": "카테고리가 생성되었습니다",
        "category": new_category
    }

@router.get("/stats")
async def get_content_stats():
    """콘텐츠 통계"""
    stats = {
        "total_contents": len(mock_contents),
        "by_type": {},
        "by_status": {},
        "total_views": sum(c["views"] for c in mock_contents),
        "total_likes": sum(c["likes"] for c in mock_contents),
        "consultation_stats": {
            "total": len(mock_consultations),
            "by_status": {},
            "by_type": {}
        }
    }
    
    # 콘텐츠 타입별 통계
    for content in mock_contents:
        ctype = content["content_type"]
        status = content["status"]
        stats["by_type"][ctype] = stats["by_type"].get(ctype, 0) + 1
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
    
    # 상담 통계
    for consultation in mock_consultations:
        status = consultation["status"]
        ctype = consultation["consultation_type"]
        stats["consultation_stats"]["by_status"][status] = stats["consultation_stats"]["by_status"].get(status, 0) + 1
        stats["consultation_stats"]["by_type"][ctype] = stats["consultation_stats"]["by_type"].get(ctype, 0) + 1
    
    return stats