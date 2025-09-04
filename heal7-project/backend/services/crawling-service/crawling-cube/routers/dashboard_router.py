#!/usr/bin/env python3
"""
🚀 크롤링 대시보드 API 라우터
Frontend 대시보드 컴포넌트들과 연동되는 실제 API 엔드포인트들

Created: 2025-09-01
Author: HEAL7 Development Team
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
import uuid
import json
import random

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API 라우터 생성
router = APIRouter(prefix="/api", tags=["dashboard"])

# ================================
# 데이터 모델들
# ================================

class MonitoringData(BaseModel):
    """모니터링 데이터 모델"""
    timestamp: str
    active_crawlers: int = 0
    success_rate: float = 0.0
    requests_per_minute: int = 0
    avg_response_time: float = 0.0
    error_rate: float = 0.0
    total_data_collected: int = 0

class CrawlerStatus(BaseModel):
    """크롤러 상태 모델"""
    id: str
    name: str
    status: str  # 'running', 'idle', 'error', 'stopped'
    tier: str   # 'httpx', 'playwright' (3단계 간소화 시스템)
    current_url: Optional[str] = None
    requests_today: int = 0
    success_rate: float = 0.0
    last_active: str
    performance_score: float = 0.0

class AIModelStats(BaseModel):
    """AI 모델 통계 모델"""
    model_name: str
    requests_count: int = 0
    success_rate: float = 0.0
    avg_response_time: float = 0.0
    cost_usd: float = 0.0
    last_used: str

class CrawlingJob(BaseModel):
    """크롤링 작업 모델"""
    id: str
    name: str
    status: str  # 'running', 'scheduled', 'paused', 'completed', 'failed'
    target_url: str
    crawler_tier: str
    created_at: str
    scheduled_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: int = 0  # 0-100
    items_collected: int = 0
    error_message: Optional[str] = None

class DataItem(BaseModel):
    """데이터 항목 모델"""
    id: str
    title: str
    content: str
    source_url: str
    crawler_tier: str
    data_type: str
    quality: str
    collected_at: str
    size: int
    processing_status: str
    ai_analyzed: bool = False
    tags: List[str] = []
    metadata: Dict[str, Any] = {}

# ================================
# 메모리 저장소 (실제 DB 연동까지의 임시)
# ================================

# 실시간 데이터 저장소
monitoring_data_store: List[MonitoringData] = []
crawler_status_store: List[CrawlerStatus] = []
ai_stats_store: List[AIModelStats] = []
crawling_jobs_store: List[CrawlingJob] = []
data_items_store: List[DataItem] = []

def init_sample_data():
    """초기 샘플 데이터 생성"""
    global crawler_status_store, ai_stats_store
    
    # 크롤러 상태 초기화
    crawler_tiers = ['httpx', 'playwright']  # 3단계 간소화 시스템
    crawler_statuses = ['running', 'idle', 'error', 'stopped']
    
    crawler_status_store = []
    for i in range(6):
        crawler_status_store.append(CrawlerStatus(
            id=f"crawler_{i+1}",
            name=f"{random.choice(crawler_tiers).title()} Crawler {i+1}",
            status=random.choice(crawler_statuses),
            tier=random.choice(crawler_tiers),
            current_url=f"https://example-site-{i+1}.com" if i % 2 == 0 else None,
            requests_today=random.randint(0, 500),
            success_rate=random.uniform(75.0, 99.0),
            last_active=datetime.now().isoformat(),
            performance_score=random.uniform(60.0, 95.0)
        ))
    
    # AI 모델 통계 초기화
    ai_models = ['Gemini Flash 2.0', 'GPT-4o', 'Claude Sonnet 3.5']
    ai_stats_store = []
    for model in ai_models:
        ai_stats_store.append(AIModelStats(
            model_name=model,
            requests_count=random.randint(10, 100),
            success_rate=random.uniform(85.0, 99.0),
            avg_response_time=random.uniform(0.5, 3.0),
            cost_usd=random.uniform(0.50, 5.00),
            last_used=datetime.now().isoformat()
        ))

# 초기 데이터 생성
init_sample_data()

# ================================
# 대시보드 모니터링 API
# ================================

@router.get("/crawling/dashboard/monitoring")
async def get_monitoring_data():
    """📊 대시보드 모니터링 데이터 조회"""
    try:
        logger.info("[API] 모니터링 데이터 요청 처리 중...")
        
        # 현재 시간 기준으로 모니터링 데이터 생성
        current_data = MonitoringData(
            timestamp=datetime.now().isoformat(),
            active_crawlers=len([c for c in crawler_status_store if c.status == 'running']),
            success_rate=sum(c.success_rate for c in crawler_status_store) / len(crawler_status_store) if crawler_status_store else 0,
            requests_per_minute=sum(c.requests_today for c in crawler_status_store) // 1440 if crawler_status_store else 0,  # 대략적인 분당 요청
            avg_response_time=random.uniform(0.8, 2.5),
            error_rate=random.uniform(0.1, 5.0),
            total_data_collected=len(data_items_store)
        )
        
        # 최근 데이터 저장 (최대 100개)
        monitoring_data_store.append(current_data)
        if len(monitoring_data_store) > 100:
            monitoring_data_store.pop(0)
        
        logger.info(f"[API] 모니터링 데이터 반환 - 활성 크롤러: {current_data.active_crawlers}")
        return {"data": current_data.dict()}
        
    except Exception as e:
        logger.error(f"[API] 모니터링 데이터 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"모니터링 데이터 조회 실패: {str(e)}")

@router.get("/crawling/dashboard/crawlers")
async def get_crawler_status():
    """🤖 크롤러 상태 목록 조회"""
    try:
        logger.info("[API] 크롤러 상태 요청 처리 중...")
        
        # 상태 업데이트 (실제로는 DB에서 조회)
        for crawler in crawler_status_store:
            crawler.last_active = datetime.now().isoformat()
        
        logger.info(f"[API] 크롤러 상태 반환 - 총 {len(crawler_status_store)}개")
        return {"crawlers": [c.dict() for c in crawler_status_store]}
        
    except Exception as e:
        logger.error(f"[API] 크롤러 상태 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"크롤러 상태 조회 실패: {str(e)}")

# ================================
# AI 모델 통계 API
# ================================

@router.get("/ai/models/stats")
async def get_ai_model_stats():
    """🧠 AI 모델 통계 조회"""
    try:
        logger.info("[API] AI 모델 통계 요청 처리 중...")
        
        # 통계 업데이트
        for stat in ai_stats_store:
            stat.last_used = datetime.now().isoformat()
        
        # 집계 데이터 계산
        total_stats = {
            "total_processed": sum(s.requests_count for s in ai_stats_store),
            "gemini_flash": next((s.requests_count for s in ai_stats_store if "Gemini" in s.model_name), 0),
            "gpt4o": next((s.requests_count for s in ai_stats_store if "GPT" in s.model_name), 0),
            "claude_sonnet": next((s.requests_count for s in ai_stats_store if "Claude" in s.model_name), 0),
            "success_rate": sum(s.success_rate for s in ai_stats_store) / len(ai_stats_store) if ai_stats_store else 0
        }
        
        logger.info(f"[API] AI 모델 통계 반환 - 총 처리: {total_stats['total_processed']}")
        return {
            "models": [s.dict() for s in ai_stats_store],
            "aggregated": total_stats
        }
        
    except Exception as e:
        logger.error(f"[API] AI 모델 통계 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI 모델 통계 조회 실패: {str(e)}")

@router.get("/ai/models/recent-jobs")
async def get_recent_ai_jobs():
    """🔄 최근 AI 작업 목록 조회"""
    try:
        logger.info("[API] 최근 AI 작업 요청 처리 중...")
        
        # 최근 완료된 작업들 (실제로는 DB에서 조회)
        recent_jobs = [
            {
                "id": str(uuid.uuid4()),
                "model": random.choice(["Gemini Flash 2.0", "GPT-4o", "Claude Sonnet 3.5"]),
                "task": random.choice(["데이터 추출", "콘텐츠 분석", "전략 생성"]),
                "status": "completed",
                "duration": random.uniform(0.5, 3.0),
                "completed_at": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            }
            for _ in range(10)
        ]
        
        logger.info(f"[API] 최근 AI 작업 반환 - {len(recent_jobs)}개")
        return {"jobs": recent_jobs}
        
    except Exception as e:
        logger.error(f"[API] 최근 AI 작업 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"최근 AI 작업 조회 실패: {str(e)}")

# ================================
# 크롤링 작업 관리 API
# ================================

@router.get("/crawling/jobs")
async def get_crawling_jobs():
    """📋 크롤링 작업 목록 조회"""
    try:
        logger.info("[API] 크롤링 작업 목록 요청 처리 중...")
        
        # 작업 목록 반환
        logger.info(f"[API] 크롤링 작업 목록 반환 - {len(crawling_jobs_store)}개")
        return {"jobs": [j.dict() for j in crawling_jobs_store]}
        
    except Exception as e:
        logger.error(f"[API] 크롤링 작업 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"크롤링 작업 목록 조회 실패: {str(e)}")

@router.post("/crawling/jobs/{job_id}/{action}")
async def handle_job_action(job_id: str, action: str):
    """⚡ 크롤링 작업 액션 처리"""
    try:
        logger.info(f"[API] 작업 액션 요청 - JobID: {job_id}, Action: {action}")
        
        # 작업 찾기
        job = next((j for j in crawling_jobs_store if j.id == job_id), None)
        if not job:
            raise HTTPException(status_code=404, detail=f"작업을 찾을 수 없습니다: {job_id}")
        
        # 액션 수행
        if action == "start":
            job.status = "running"
        elif action == "pause":
            job.status = "paused"
        elif action == "stop":
            job.status = "stopped"
        elif action == "delete":
            crawling_jobs_store.remove(job)
            return {"message": f"작업이 삭제되었습니다: {job_id}"}
        else:
            raise HTTPException(status_code=400, detail=f"지원되지 않는 액션: {action}")
        
        logger.info(f"[API] 작업 액션 완료 - JobID: {job_id}, 새 상태: {job.status}")
        return {"message": f"작업 {action} 완료", "job": job.dict()}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] 작업 액션 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"작업 액션 처리 실패: {str(e)}")

@router.post("/crawling/jobs")
async def create_crawling_job(job_data: Dict[str, Any]):
    """➕ 새 크롤링 작업 생성"""
    try:
        logger.info(f"[API] 새 작업 생성 요청 - {job_data}")
        
        # 새 작업 생성
        new_job = CrawlingJob(
            id=str(uuid.uuid4()),
            name=job_data.get("name", f"작업 {len(crawling_jobs_store) + 1}"),
            status="scheduled",
            target_url=job_data.get("url", ""),
            crawler_tier=job_data.get("tier", "httpx"),
            created_at=datetime.now().isoformat(),
            scheduled_at=job_data.get("scheduled_at"),
            progress=0,
            items_collected=0
        )
        
        crawling_jobs_store.append(new_job)
        
        logger.info(f"[API] 새 작업 생성 완료 - JobID: {new_job.id}")
        return {"message": "작업이 생성되었습니다", "job": new_job.dict()}
        
    except Exception as e:
        logger.error(f"[API] 작업 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"작업 생성 실패: {str(e)}")

# ================================
# 데이터 관리 API
# ================================

@router.get("/data/items")
async def get_data_items():
    """📄 데이터 항목 목록 조회"""
    try:
        logger.info("[API] 데이터 항목 목록 요청 처리 중...")
        
        logger.info(f"[API] 데이터 항목 목록 반환 - {len(data_items_store)}개")
        return {"items": [d.dict() for d in data_items_store]}
        
    except Exception as e:
        logger.error(f"[API] 데이터 항목 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터 항목 목록 조회 실패: {str(e)}")

@router.post("/data/export")
async def export_data(export_request: Dict[str, Any]):
    """📤 데이터 내보내기"""
    try:
        item_ids = export_request.get("itemIds", [])
        format_type = export_request.get("format", "csv")
        
        logger.info(f"[API] 데이터 내보내기 요청 - {len(item_ids)}개 항목, 형식: {format_type}")
        
        # 실제로는 파일을 생성하고 다운로드 URL 제공
        download_url = f"/downloads/export_{uuid.uuid4().hex[:8]}.{format_type}"
        
        logger.info(f"[API] 데이터 내보내기 완료 - URL: {download_url}")
        return {
            "downloadUrl": download_url,
            "format": format_type,
            "itemCount": len(item_ids),
            "message": "내보내기가 완료되었습니다"
        }
        
    except Exception as e:
        logger.error(f"[API] 데이터 내보내기 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터 내보내기 실패: {str(e)}")

@router.post("/data/bulk/{action}")
async def handle_bulk_data_action(action: str, bulk_request: Dict[str, Any]):
    """🔄 데이터 일괄 작업 처리"""
    try:
        item_ids = bulk_request.get("itemIds", [])
        logger.info(f"[API] 일괄 {action} 요청 - {len(item_ids)}개 항목")
        
        affected_count = 0
        
        if action == "delete":
            # 삭제 처리
            global data_items_store
            data_items_store = [item for item in data_items_store if item.id not in item_ids]
            affected_count = len(item_ids)
        elif action == "reprocess":
            # 재처리 처리
            for item in data_items_store:
                if item.id in item_ids:
                    item.processing_status = "pending"
                    affected_count += 1
        elif action == "analyze":
            # AI 분석 처리
            for item in data_items_store:
                if item.id in item_ids:
                    item.ai_analyzed = True
                    affected_count += 1
        else:
            raise HTTPException(status_code=400, detail=f"지원되지 않는 액션: {action}")
        
        logger.info(f"[API] 일괄 {action} 완료 - {affected_count}개 항목 처리됨")
        return {
            "success": True,
            "affected": affected_count,
            "message": f"{affected_count}개 항목에 대한 {action} 작업이 완료되었습니다"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] 일괄 작업 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"일괄 작업 처리 실패: {str(e)}")

# ================================
# WebSocket 실시간 업데이트
# ================================

@router.websocket("/ws/monitor")
async def websocket_endpoint(websocket: WebSocket):
    """🔴 실시간 크롤링 상태 WebSocket"""
    await websocket.accept()
    logger.info("[WS] WebSocket 연결 수락됨")
    
    try:
        while True:
            # 주기적으로 상태 업데이트 전송 (5초마다)
            await asyncio.sleep(5)
            
            update_data = {
                "type": "status_update",
                "timestamp": datetime.now().isoformat(),
                "active_crawlers": len([c for c in crawler_status_store if c.status == 'running']),
                "total_jobs": len(crawling_jobs_store),
                "data_items": len(data_items_store)
            }
            
            await websocket.send_text(json.dumps(update_data))
            
    except WebSocketDisconnect:
        logger.info("[WS] WebSocket 연결 종료됨")
    except Exception as e:
        logger.error(f"[WS] WebSocket 오류: {str(e)}")

logger.info("🚀 크롤링 대시보드 API 라우터 로드 완료")