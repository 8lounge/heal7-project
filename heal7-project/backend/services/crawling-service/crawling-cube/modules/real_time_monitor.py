#!/usr/bin/env python3
"""
⚡ 실시간 크롤링 모니터링 시스템
WebSocket 기반 실시간 대시보드 업데이트

Author: HEAL7 Development Team
Version: 1.0.0  
Date: 2025-08-29
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict

import asyncpg
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter


logger = logging.getLogger(__name__)


@dataclass
class MonitoringEvent:
    """모니터링 이벤트 데이터 구조"""
    event_type: str  # 'collection_start', 'collection_complete', 'new_item', 'stats_update'
    portal_id: Optional[str] = None
    data: Dict = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.data is None:
            self.data = {}


class RealTimeMonitor:
    """⚡ 실시간 모니터링 관리자"""
    
    def __init__(self, db_connection_string: str):
        self.db_connection_string = db_connection_string
        self.db_pool = None
        
        # WebSocket 연결 관리
        self.active_connections: Set[WebSocket] = set()
        self.connection_portals: Dict[WebSocket, List[str]] = {}  # 클라이언트별 관심 포털
        
        # 모니터링 설정
        self.stats_update_interval = 30  # 30초마다 통계 업데이트
        self.is_monitoring = False
        
        # 최신 통계 캐시
        self.latest_stats = {}
        self.latest_events = []
        self.max_events = 100
    
    async def initialize(self):
        """모니터링 시스템 초기화"""
        logger.info("⚡ 실시간 모니터링 시스템 초기화")
        
        # 데이터베이스 연결
        try:
            self.db_pool = await asyncpg.create_pool(
                self.db_connection_string,
                min_size=1,
                max_size=3,
                command_timeout=30
            )
            logger.info("✅ 모니터링 DB 연결 완료")
        except Exception as e:
            logger.error(f"❌ 모니터링 DB 연결 실패: {e}")
            raise
        
        # 백그라운드 모니터링 시작
        asyncio.create_task(self.start_background_monitoring())
        
        logger.info("🚀 실시간 모니터링 시스템 준비 완료")
    
    async def close(self):
        """모니터링 시스템 종료"""
        self.is_monitoring = False
        
        # 모든 WebSocket 연결 종료
        for ws in self.active_connections.copy():
            try:
                await ws.close()
            except:
                pass
        
        # 데이터베이스 연결 종료
        if self.db_pool:
            await self.db_pool.close()
        
        logger.info("🛑 실시간 모니터링 시스템 종료 완료")
    
    async def connect_websocket(self, websocket: WebSocket, portal_filter: List[str] = None):
        """새 WebSocket 클라이언트 연결"""
        await websocket.accept()
        self.active_connections.add(websocket)
        
        if portal_filter:
            self.connection_portals[websocket] = portal_filter
            logger.info(f"📡 WebSocket 연결: 포털 필터 {portal_filter}")
        else:
            logger.info(f"📡 WebSocket 연결: 전체 모니터링")
        
        # 연결 즉시 최신 통계 전송
        if self.latest_stats:
            await self.send_to_client(websocket, {
                'type': 'initial_stats',
                'data': self.latest_stats,
                'timestamp': datetime.now().isoformat()
            })
        
        # 최근 이벤트 전송
        recent_events = self.latest_events[-20:] if self.latest_events else []
        if recent_events:
            await self.send_to_client(websocket, {
                'type': 'recent_events',
                'data': {'events': recent_events},
                'timestamp': datetime.now().isoformat()
            })
    
    async def disconnect_websocket(self, websocket: WebSocket):
        """WebSocket 클라이언트 연결 해제"""
        self.active_connections.discard(websocket)
        self.connection_portals.pop(websocket, None)
        logger.info("📡 WebSocket 연결 해제")
    
    async def send_to_client(self, websocket: WebSocket, message: Dict):
        """개별 클라이언트에게 메시지 전송"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.debug(f"WebSocket 전송 실패 (연결 끊김): {e}")
            await self.disconnect_websocket(websocket)
    
    async def broadcast_event(self, event: MonitoringEvent):
        """모든 연결된 클라이언트에게 이벤트 브로드캐스트"""
        if not self.active_connections:
            return
        
        # 이벤트 기록
        self.latest_events.append(asdict(event))
        if len(self.latest_events) > self.max_events:
            self.latest_events = self.latest_events[-self.max_events:]
        
        message = {
            'type': 'live_event',
            'event': asdict(event)
        }
        
        # 모든 활성 연결에 전송
        disconnected = set()
        for ws in self.active_connections:
            try:
                # 포털 필터 확인
                portal_filter = self.connection_portals.get(ws)
                if portal_filter and event.portal_id and event.portal_id not in portal_filter:
                    continue  # 필터에 맞지 않으면 전송 안함
                
                await ws.send_json(message)
            except Exception as e:
                logger.debug(f"브로드캐스트 실패: {e}")
                disconnected.add(ws)
        
        # 끊어진 연결 정리
        for ws in disconnected:
            await self.disconnect_websocket(ws)
    
    async def start_background_monitoring(self):
        """백그라운드 모니터링 루프"""
        logger.info("🔄 백그라운드 모니터링 시작")
        self.is_monitoring = True
        
        while self.is_monitoring:
            try:
                # 통계 업데이트
                await self.update_live_statistics()
                
                # 새로운 수집 데이터 확인
                await self.check_new_collections()
                
                await asyncio.sleep(self.stats_update_interval)
                
            except Exception as e:
                logger.error(f"❌ 백그라운드 모니터링 오류: {e}")
                await asyncio.sleep(10)  # 오류 시 잠시 대기
    
    async def update_live_statistics(self):
        """실시간 통계 업데이트"""
        try:
            async with self.db_pool.acquire() as conn:
                # 실시간 통계 쿼리
                stats_query = """
                    SELECT 
                        portal_id,
                        COUNT(*) FILTER (WHERE scraped_at >= NOW() - INTERVAL '1 hour') as recent_hour,
                        COUNT(*) FILTER (WHERE scraped_at >= NOW() - INTERVAL '10 minutes') as recent_10min,
                        AVG(quality_score) FILTER (WHERE scraped_at >= NOW() - INTERVAL '1 hour') as recent_quality,
                        MAX(scraped_at) as last_activity
                    FROM raw_scraped_data
                    WHERE processing_status = 'completed'
                    GROUP BY portal_id
                """
                
                rows = await conn.fetch(stats_query)
                
                current_stats = {}
                for row in rows:
                    current_stats[row['portal_id']] = {
                        'recent_hour': int(row['recent_hour']),
                        'recent_10min': int(row['recent_10min']),
                        'recent_quality': round(float(row['recent_quality'] or 0), 1),
                        'last_activity': row['last_activity'].strftime('%Y-%m-%d %H:%M:%S') if row['last_activity'] else None
                    }
                
                # 변경사항이 있으면 브로드캐스트
                if current_stats != self.latest_stats:
                    self.latest_stats = current_stats
                    
                    event = MonitoringEvent(
                        event_type='stats_update',
                        data={'stats': current_stats}
                    )
                    
                    await self.broadcast_event(event)
                
        except Exception as e:
            logger.error(f"❌ 실시간 통계 업데이트 실패: {e}")
    
    async def check_new_collections(self):
        """새로운 수집 데이터 확인"""
        try:
            async with self.db_pool.acquire() as conn:
                # 최근 5분간 새로운 데이터 확인
                new_items_query = """
                    SELECT 
                        id, portal_id, title, agency, quality_score, scraped_at
                    FROM raw_scraped_data
                    WHERE scraped_at >= NOW() - INTERVAL '5 minutes'
                    AND processing_status = 'completed'
                    ORDER BY scraped_at DESC
                    LIMIT 10
                """
                
                rows = await conn.fetch(new_items_query)
                
                for row in rows:
                    # 각 새 항목에 대해 이벤트 생성
                    event = MonitoringEvent(
                        event_type='new_item',
                        portal_id=row['portal_id'],
                        data={
                            'id': row['id'],
                            'title': row['title'],
                            'agency': row['agency'],
                            'quality_score': float(row['quality_score']),
                            'scraped_at': row['scraped_at'].strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                    
                    await self.broadcast_event(event)
                
        except Exception as e:
            logger.error(f"❌ 새 수집 데이터 확인 실패: {e}")
    
    async def trigger_collection_event(self, portal_id: str, event_type: str, data: Dict = None):
        """외부에서 호출하는 수집 이벤트 트리거"""
        event = MonitoringEvent(
            event_type=event_type,
            portal_id=portal_id,
            data=data or {}
        )
        
        await self.broadcast_event(event)
        logger.info(f"🔔 수집 이벤트 트리거: {event_type} - {portal_id}")
    
    async def get_monitoring_summary(self) -> Dict:
        """모니터링 현황 요약"""
        return {
            'active_connections': len(self.active_connections),
            'portal_filters': {str(id(ws))[:8]: portals for ws, portals in self.connection_portals.items()},
            'monitoring_active': self.is_monitoring,
            'latest_stats': self.latest_stats,
            'recent_events_count': len(self.latest_events),
            'update_interval_seconds': self.stats_update_interval
        }


# FastAPI WebSocket 라우터 설정
monitor_router = APIRouter()

# 전역 모니터링 인스턴스
real_time_monitor: Optional[RealTimeMonitor] = None


async def initialize_monitor(db_connection_string: str):
    """모니터링 시스템 초기화"""
    global real_time_monitor
    real_time_monitor = RealTimeMonitor(db_connection_string)
    await real_time_monitor.initialize()


@monitor_router.websocket("/ws/live-monitoring")
async def websocket_endpoint(
    websocket: WebSocket,
    portals: str = None  # 쿼리 파라미터로 포털 필터
):
    """⚡ 실시간 모니터링 WebSocket 엔드포인트"""
    if not real_time_monitor:
        await websocket.close(code=1003, reason="Monitoring system not initialized")
        return
    
    # 포털 필터 파싱
    portal_filter = None
    if portals:
        portal_filter = [p.strip() for p in portals.split(',') if p.strip()]
    
    # 연결 수락
    await real_time_monitor.connect_websocket(websocket, portal_filter)
    
    try:
        while True:
            # 클라이언트 메시지 수신 (Keep-alive 등)
            try:
                message = await websocket.receive_text()
                data = json.loads(message)
                
                # Keep-alive 응답
                if data.get('type') == 'ping':
                    await real_time_monitor.send_to_client(websocket, {
                        'type': 'pong',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # 포털 필터 변경
                elif data.get('type') == 'update_filter':
                    new_portals = data.get('portals', [])
                    real_time_monitor.connection_portals[websocket] = new_portals
                    logger.info(f"📡 포털 필터 업데이트: {new_portals}")
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.debug(f"WebSocket 메시지 처리 오류: {e}")
                break
    
    except WebSocketDisconnect:
        pass
    finally:
        await real_time_monitor.disconnect_websocket(websocket)


@monitor_router.get("/monitoring-summary")
async def get_monitoring_summary():
    """모니터링 시스템 현황 조회"""
    if not real_time_monitor:
        return {"error": "Monitoring system not initialized"}
    
    return await real_time_monitor.get_monitoring_summary()


@monitor_router.post("/trigger-event")
async def trigger_monitoring_event(
    event_type: str,
    portal_id: str,
    data: Dict = None
):
    """외부에서 모니터링 이벤트 트리거"""
    if not real_time_monitor:
        return {"error": "Monitoring system not initialized"}
    
    await real_time_monitor.trigger_collection_event(event_type, portal_id, data)
    
    return {
        "success": True,
        "message": f"Event '{event_type}' triggered for portal '{portal_id}'"
    }


# 유틸리티 함수들

async def notify_collection_start(portal_id: str, max_pages: int):
    """수집 시작 알림"""
    if real_time_monitor:
        await real_time_monitor.trigger_collection_event(
            portal_id=portal_id,
            event_type='collection_start',
            data={'max_pages': max_pages}
        )


async def notify_collection_complete(portal_id: str, result_data: Dict):
    """수집 완료 알림"""
    if real_time_monitor:
        await real_time_monitor.trigger_collection_event(
            portal_id=portal_id,
            event_type='collection_complete',
            data=result_data
        )


async def notify_new_item(portal_id: str, item_data: Dict):
    """새 항목 수집 알림"""
    if real_time_monitor:
        await real_time_monitor.trigger_collection_event(
            portal_id=portal_id,
            event_type='new_item',
            data=item_data
        )


# 예제: 실시간 모니터링 초기화 코드
async def setup_real_time_monitoring():
    """실시간 모니터링 설정 예제"""
    db_connection = "postgresql://postgres:@localhost:5432/paperworkdb"
    
    try:
        await initialize_monitor(db_connection)
        logger.info("🎯 실시간 모니터링 시스템 설정 완료")
        return True
    except Exception as e:
        logger.error(f"❌ 실시간 모니터링 설정 실패: {e}")
        return False


if __name__ == "__main__":
    # 독립 실행 테스트
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI(title="Real-Time Monitoring Test")
    app.include_router(monitor_router, prefix="/monitor", tags=["real-time-monitoring"])
    
    @app.on_event("startup")
    async def startup():
        await setup_real_time_monitoring()
    
    uvicorn.run(app, host="0.0.0.0", port=8007)