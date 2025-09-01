#!/usr/bin/env python3
"""
📄 페이퍼워크 시스템 큐브 - 완전 독립 실행

Usage:
    python3 main.py  # 포트 8002에서 독립 실행
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn
import sys
import os
import logging

# 현재 큐브를 Python path에 추가
sys.insert(0, os.dirname(os.abspath(__file__)))

logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="📄 HEAL7 페이퍼워크 시스템",
    description="문서 AI 처리 및 스크래핑 대시보드 독립 실행 큐브",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델들
class DocumentInfo(BaseModel):
    id: str
    title: str
    content: str
    source: str
    created_at: datetime
    status: str

class CollectionStats(BaseModel):
    total_documents: int
    processed_documents: int
    pending_documents: int
    last_updated: datetime

class ScrapingTask(BaseModel):
    task_id: str
    url: str
    status: str  # "pending", "running", "completed", "failed"
    created_at: datetime
    completed_at: Optional[datetime] = None
    result_count: int = 0

# 큐브 메인 엔드포인트
@app.get("/")
async def root():
    """페이퍼워크 시스템 큐브 메인"""
    return {
        "cube": "paperwork-system",
        "service": "paperwork.com",
        "status": "running",
        "port": 8001,
        "version": "1.0",
        "description": "📄 HEAL7 페이퍼워크 시스템 큐브",
        "features": [
            "문서 AI 처리",
            "스크래핑 대시보드",
            "컬렉션 관리",
            "환경 설정 API"
        ]
    }

@app.get("/health")
async def health_check():
    """헬스체크"""
    return {
        "status": "healthy",
        "cube": "paperwork-system",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/env-config")
async def get_env_config():
    """환경 설정 조회"""
    return {
        "app_name": "HEAL7 Paperwork AI",
        "version": "1.0",
        "environment": "production",
        "database_status": "connected",
        "scraping_enabled": True,
        "ai_processing_enabled": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/scraping-dashboard", response_model=Dict[str, Any])
async def get_scraping_dashboard(
    action: str = Query("status", description="Action to perform"),
    limit: int = Query(10, description="Number of items to return")
):
    """스크래핑 대시보드 API"""
    
    if action == "status":
        return {
            "status": "active",
            "total_collections": 15,
            "active_tasks": 3,
            "completed_today": 127,
            "timestamp": datetime.now().isoformat()
        }
    
    elif action == "collection_list":
        # 시뮬레이션 데이터
        collections = []
        for i in range(min(limit, 15)):
            collections.append({
                "id": f"collection_{i+1}",
                "name": f"Collection {i+1}",
                "source": f"source_{i+1}.com",
                "status": "active" if i % 3 != 0 else "pending",
                "document_count": 50 + (i * 10),
                "last_updated": datetime.now().isoformat()
            })
        
        return {
            "collections": collections,
            "total_count": len(collections),
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }
    
    elif action == "recent_tasks":
        tasks = []
        statuses = ["completed", "running", "pending", "failed"]
        
        for i in range(min(limit, 20)):
            status = statuses[i % len(statuses)]
            tasks.append(ScrapingTask(
                task_id=f"task_{i+1:03d}",
                url=f"https://example{i+1}.com/documents",
                status=status,
                created_at=datetime.now(),
                completed_at=datetime.now() if status == "completed" else None,
                result_count=25 + (i * 3) if status == "completed" else 0
            ))
        
        return {
            "tasks": [task.dict() for task in tasks],
            "total_count": len(tasks),
            "timestamp": datetime.now().isoformat()
        }
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action parameter")

@app.get("/api/collections/stats", response_model=CollectionStats)
async def get_collection_stats():
    """컬렉션 통계 정보"""
    return CollectionStats(
        total_documents=1250,
        processed_documents=1100,
        pending_documents=150,
        last_updated=datetime.now()
    )

@app.post("/api/documents/process")
async def process_document(document_id: str):
    """문서 AI 처리 시작"""
    try:
        # 문서 처리 시뮬레이션
        return {
            "document_id": document_id,
            "status": "processing_started",
            "estimated_completion": datetime.now().isoformat(),
            "message": "문서 AI 처리가 시작되었습니다."
        }
    except Exception as e:
        logger.error(f"문서 처리 오류: {e}")
        raise HTTPException(status_code=500, detail="문서 처리 중 오류가 발생했습니다.")

@app.get("/api/documents/{document_id}")
async def get_document(document_id: str):
    """문서 정보 조회"""
    return {
        "id": document_id,
        "title": f"Document {document_id}",
        "content": "This is a sample document content...",
        "source": "sample_source.com",
        "status": "processed",
        "ai_summary": "This document contains important information about...",
        "created_at": datetime.now().isoformat(),
        "processed_at": datetime.now().isoformat()
    }

@app.post("/api/scraping/start")
async def start_scraping_task(url: str, collection_name: str = "default"):
    """새로운 스크래핑 작업 시작"""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "task_id": task_id,
        "url": url,
        "collection_name": collection_name,
        "status": "started",
        "message": "스크래핑 작업이 시작되었습니다.",
        "timestamp": datetime.now().isoformat()
    }

# 독립 실행 시
if __name__ == "__main__":
    print("📄 페이퍼워크 시스템 큐브 시작...")
    print("📍 URL: http://localhost:8002")
    print("📋 Docs: http://localhost:8002/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )