#!/usr/bin/env python3
"""
🔗 AI 크롤링 시스템 대시보드 통합 API
대시보드에서 AI 기반 동적 크롤링 요청 및 실시간 모니터링

Author: HEAL7 Development Team
Version: 1.0
Date: 2025-08-29
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

logger = logging.getLogger(__name__)


# ================================
# 요청/응답 모델들
# ================================

class CollectionRequest(BaseModel):
    """수집 요청 모델"""
    site_url: str = Field(..., description="수집할 사이트 URL")
    target_data_types: List[str] = Field(
        default=["title", "content", "links"],
        description="수집할 데이터 타입"
    )
    user_id: str = Field(default="dashboard_user", description="요청 사용자 ID")
    collection_name: str = Field(default="", description="수집 작업 이름")
    priority: str = Field(default="normal", description="우선순위: low, normal, high")


class CollectionResponse(BaseModel):
    """수집 응답 모델"""
    session_id: str
    message: str
    estimated_duration_minutes: int = Field(default=5, description="예상 소요 시간(분)")
    websocket_endpoint: str = Field(description="실시간 모니터링 WebSocket 엔드포인트")


class SessionStatusResponse(BaseModel):
    """세션 상태 응답 모델"""
    session_id: str
    site_url: str
    current_stage: str
    current_status: str
    progress_percentage: int
    created_at: str
    updated_at: str
    extracted_items_count: int
    error_count: int
    has_strategy: bool
    performance_metrics: Dict[str, Any]


class UserConfirmationRequest(BaseModel):
    """사용자 확인 요청 모델"""
    session_id: str
    action: str = Field(..., description="confirm_completion 또는 cancel")
    user_feedback: str = Field(default="", description="사용자 피드백")


# ================================
# FastAPI 애플리케이션
# ================================

app = FastAPI(
    title="AI 크롤링 대시보드 통합 API",
    description="대시보드에서 AI 기반 동적 크롤링 요청 및 실시간 모니터링",
    version="1.0"
)

# WebSocket 연결 관리자
class ConnectionManager:
    """WebSocket 연결 관리자"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"🔌 WebSocket 연결: {session_id}")
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"🔌 WebSocket 연결 해제: {session_id}")
    
    async def send_personal_message(self, session_id: str, message: Dict[str, Any]):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"메시지 전송 실패 {session_id}: {e}")
                self.disconnect(session_id)

# 전역 연결 관리자
connection_manager = ConnectionManager()


# ================================
# API 엔드포인트들
# ================================

@app.post("/api/ai-collection/request", response_model=CollectionResponse)
async def request_ai_collection(
    request: CollectionRequest,
    background_tasks: BackgroundTasks
):
    """🚀 AI 기반 동적 크롤링 요청"""
    
    try:
        # 인터랙티브 컨트롤러 가져오기
        import sys
        from pathlib import Path
        
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.insert(0, str(parent_dir))
        
        from user_flow.interactive_collection_controller import get_interactive_controller
        
        controller = get_interactive_controller()
        
        # 새 수집 세션 생성
        session_id = controller.create_collection_session(
            site_url=request.site_url,
            target_data_types=request.target_data_types,
            user_id=request.user_id
        )
        
        # WebSocket 콜백 등록
        async def progress_callback(status_data):
            await connection_manager.send_personal_message(
                session_id, 
                {"type": "progress_update", "data": status_data}
            )
        
        async def completion_callback(status_data):
            await connection_manager.send_personal_message(
                session_id,
                {"type": "collection_completed", "data": status_data}
            )
        
        async def error_callback(error_data):
            await connection_manager.send_personal_message(
                session_id,
                {"type": "error_occurred", "data": error_data}
            )
        
        controller.register_session_callbacks(
            session_id=session_id,
            progress_callback=progress_callback,
            completion_callback=completion_callback,
            error_callback=error_callback
        )
        
        # 백그라운드에서 수집 플로우 실행
        background_tasks.add_task(
            controller.execute_collection_flow,
            session_id
        )
        
        logger.info(f"🎯 수집 요청 접수: {session_id} ({request.site_url})")
        
        return CollectionResponse(
            session_id=session_id,
            message=f"AI 크롤링 세션이 시작되었습니다. 실시간 진행상황을 모니터링하세요.",
            estimated_duration_minutes=5,
            websocket_endpoint=f"/api/ai-collection/ws/{session_id}"
        )
        
    except Exception as e:
        logger.error(f"수집 요청 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"수집 요청 실패: {str(e)}")


@app.get("/api/ai-collection/status/{session_id}", response_model=SessionStatusResponse)
async def get_collection_status(session_id: str):
    """📊 수집 세션 상태 조회"""
    
    try:
        import sys
        from pathlib import Path
        
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.insert(0, str(parent_dir))
        
        from user_flow.interactive_collection_controller import get_interactive_controller
        
        controller = get_interactive_controller()
        status = controller.get_session_status(session_id)
        
        if not status:
            raise HTTPException(status_code=404, detail=f"세션을 찾을 수 없음: {session_id}")
        
        return SessionStatusResponse(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"상태 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"상태 조회 실패: {str(e)}")


@app.post("/api/ai-collection/user-action")
async def user_action(request: UserConfirmationRequest):
    """👤 사용자 액션 처리 (완료 확인 또는 취소)"""
    
    try:
        import sys
        from pathlib import Path
        
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.insert(0, str(parent_dir))
        
        from user_flow.interactive_collection_controller import get_interactive_controller
        
        controller = get_interactive_controller()
        
        if request.action == "confirm_completion":
            # 완료 확인
            success = controller.complete_session(request.session_id)
            
            if success:
                # 완료 알림 전송
                await connection_manager.send_personal_message(
                    request.session_id,
                    {
                        "type": "user_confirmed", 
                        "data": {
                            "action": "completed",
                            "message": "사용자가 완료를 확인했습니다. 세션이 종료됩니다.",
                            "feedback": request.user_feedback
                        }
                    }
                )
                
                return {"status": "success", "message": "수집 완료가 확인되었습니다."}
            else:
                return {"status": "error", "message": "완료 확인 실패: 세션이 완료되지 않았거나 존재하지 않습니다."}
        
        elif request.action == "cancel":
            # 취소 처리
            success = controller.cancel_session(request.session_id)
            
            if success:
                await connection_manager.send_personal_message(
                    request.session_id,
                    {
                        "type": "user_cancelled",
                        "data": {
                            "action": "cancelled", 
                            "message": "사용자가 수집을 취소했습니다.",
                            "feedback": request.user_feedback
                        }
                    }
                )
                
                return {"status": "success", "message": "수집이 취소되었습니다."}
            else:
                return {"status": "error", "message": "취소 실패: 세션을 찾을 수 없습니다."}
        
        else:
            raise HTTPException(status_code=400, detail=f"지원되지 않는 액션: {request.action}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"사용자 액션 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"사용자 액션 처리 실패: {str(e)}")


@app.get("/api/ai-collection/sessions")
async def list_active_sessions():
    """📋 활성 세션 목록 조회"""
    
    try:
        import sys
        from pathlib import Path
        
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.insert(0, str(parent_dir))
        
        from user_flow.interactive_collection_controller import get_interactive_controller
        
        controller = get_interactive_controller()
        sessions = controller.list_active_sessions()
        
        return {
            "total_sessions": len(sessions),
            "sessions": sessions,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"세션 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"세션 목록 조회 실패: {str(e)}")


@app.websocket("/api/ai-collection/ws/{session_id}")
async def websocket_monitor(websocket: WebSocket, session_id: str):
    """🔴 실시간 수집 진행상황 WebSocket 모니터링"""
    
    await connection_manager.connect(websocket, session_id)
    
    try:
        # 초기 연결 메시지
        await connection_manager.send_personal_message(
            session_id,
            {
                "type": "connection_established",
                "data": {
                    "session_id": session_id,
                    "message": "실시간 모니터링이 시작되었습니다.",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
        
        # 연결 유지 (클라이언트 연결이 끊어질 때까지)
        while True:
            try:
                # 클라이언트로부터 메시지 수신 대기
                data = await websocket.receive_text()
                
                # Ping-Pong 메시지 처리
                if data == "ping":
                    await connection_manager.send_personal_message(
                        session_id,
                        {"type": "pong", "timestamp": datetime.now().isoformat()}
                    )
                
            except WebSocketDisconnect:
                logger.info(f"🔌 클라이언트 연결 해제: {session_id}")
                break
            except Exception as e:
                logger.error(f"WebSocket 오류: {str(e)}")
                break
    
    except Exception as e:
        logger.error(f"WebSocket 연결 오류: {str(e)}")
    
    finally:
        connection_manager.disconnect(session_id)


@app.get("/api/ai-collection/health")
async def health_check():
    """🏥 서비스 상태 확인"""
    
    return {
        "status": "healthy",
        "service": "AI 크롤링 대시보드 통합 API",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """📖 API 정보"""
    
    return {
        "service": "AI 크롤링 대시보드 통합 API",
        "version": "1.0", 
        "description": "대시보드에서 AI 기반 동적 크롤링 요청 및 실시간 모니터링",
        "docs": "/docs",
        "health": "/api/ai-collection/health"
    }


# ================================
# 서버 실행
# ================================

def run_dashboard_api(host: str = "0.0.0", port: int = 8005):
    """대시보드 통합 API 서버 실행"""
    
    print("🔗 AI 크롤링 대시보드 통합 API 서버 시작")
    print(f"📡 서버: http://{host}:{port}")
    print(f"📚 API 문서: http://{host}:{port}/docs")
    print(f"🏥 헬스 체크: http://{host}:{port}/api/ai-collection/health")
    
    uvicorn.run(
        "dashboard_integration_api:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    # 환경변수에서 포트 설정 가능
    import os
    port = int(os.getenv("DASHBOARD_API_PORT", 8005))
    run_dashboard_api(port=port)