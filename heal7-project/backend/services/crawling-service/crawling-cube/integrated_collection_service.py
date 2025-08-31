#!/usr/bin/env python3
"""
🎯 통합 크롤링 수집 서비스
실제 구동 가능한 전체 시스템 통합

Author: HEAL7 Development Team
Version: 1.0
Date: 2025-08-29
"""

import asyncio
import logging
import os
import signal
from datetime import datetime
from typing import Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.cors import CORSMiddleware

# 내부 모듈 import
from modules.core_collection_engine import create_collection_engine, CoreCollectionEngine  
from modules.bizinfo_collector import BizinfoCollector, KStartupCollector, run_comprehensive_collection
from modules.real_time_monitor import initialize_monitor, monitor_router, real_time_monitor

logger = logging.getLogger(__name__)


class IntegratedCollectionService:
    """🎯 통합 크롤링 수집 서비스"""
    
    def __init__(self):
        # 설정
        self.db_connection_string = os.getenv(
            'DATABASE_URL', 
            'postgresql://postgres:@localhost:5432/paperworkdb'
        )
        self.service_port = int(os.getenv('COLLECTION_SERVICE_PORT', '8004'))
        self.service_host = os.getenv('COLLECTION_SERVICE_HOST', '0.0.0')
        
        # 핵심 구성 요소
        self.collection_engine: CoreCollectionEngine = None
        self.bizinfo_collector: BizinfoCollector = None
        self.kstartup_collector: KStartupCollector = None
        
        # FastAPI 앱
        self.app = self.create_app()
        
        # 서비스 상태
        self.is_running = False
        self.startup_time = None
        
        # 자동 스케줄링
        self.auto_schedule_enabled = True
        self.scheduled_tasks = []
    
    def create_app(self) -> FastAPI:
        """FastAPI 애플리케이션 생성"""
        app = FastAPI(
            title="🎯 HEAL7 통합 크롤링 수집 서비스",
            description="실시간 정부 포털 데이터 수집 및 모니터링 시스템",
            version="1.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # CORS 설정
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "https://crawling.com",
                "https://admin.com", 
                "http://localhost:3000",
                "http://localhost:4173"
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        # 라우터 등록
        self.register_routes(app)
        
        # 이벤트 핸들러 등록
        app.add_event_handler("startup", self.startup_event)
        app.add_event_handler("shutdown", self.shutdown_event)
        
        return app
    
    def register_routes(self, app: FastAPI):
        """라우터 등록"""
        
        # 실시간 모니터링 라우터
        app.include_router(
            monitor_router, 
            prefix="/monitor", 
            tags=["실시간 모니터링"]
        )
        
        # 기본 서비스 라우터들
        @app.get("/")
        async def root():
            """서비스 상태 확인"""
            return {
                "service": "HEAL7 통합 크롤링 수집 서비스",
                "version": "1.0",
                "status": "running" if self.is_running else "initializing",
                "startup_time": self.isoformat() if self.startup_time else None,
                "available_portals": ["bizinfo", "kstartup"],
                "endpoints": {
                    "manual_collection": "/collect",
                    "collection_status": "/status", 
                    "service_stats": "/stats",
                    "real_time_monitor": "/monitor/ws/live-monitoring",
                    "trigger_monitoring_event": "/monitor/trigger-event"
                }
            }
        
        @app.get("/health")
        async def health_check():
            """상세 헬스 체크"""
            try:
                health_status = {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "components": {}
                }
                
                # 데이터베이스 연결 확인
                if self.collection_engine:
                    try:
                        stats = await self.get_collection_statistics()
                        health_status["components"]["database"] = {
                            "status": "connected",
                            "total_portals": len(stats.get('portals', {}))
                        }
                    except Exception as e:
                        health_status["components"]["database"] = {
                            "status": "error", 
                            "error": str(e)
                        }
                        health_status["status"] = "degraded"
                
                # 실시간 모니터링 확인
                if real_time_monitor:
                    monitor_summary = await real_time_monitor.get_monitoring_summary()
                    health_status["components"]["real_time_monitor"] = {
                        "status": "active" if monitor_summary.get('monitoring_active') else "inactive",
                        "active_connections": monitor_summary.get('active_connections', 0)
                    }
                
                # 수집기 상태
                health_status["components"]["collectors"] = {
                    "bizinfo": "ready" if self.bizinfo_collector else "not_initialized",
                    "kstartup": "ready" if self.kstartup_collector else "not_initialized"
                }
                
                return health_status
                
            except Exception as e:
                return {
                    "status": "unhealthy",
                    "timestamp": datetime.now().isoformat(), 
                    "error": str(e)
                }
        
        @app.post("/collect")
        async def manual_collection(
            portals: List[str],
            max_pages: int = 5,
            force_update: bool = False
        ):
            """수동 데이터 수집 실행"""
            if not self.is_running:
                raise HTTPException(status_code=503, detail="서비스가 초기화 중입니다")
            
            try:
                logger.info(f"🚀 수동 수집 시작: {portals} (페이지: {max_pages})")
                
                # 수집 실행
                results = await run_comprehensive_collection(
                    db_connection_string=self.db_connection_string,
                    portals=portals,
                    max_pages=max_pages
                )
                
                # 결과 정리
                response = {
                    "success": True,
                    "collected_at": datetime.now().isoformat(),
                    "results": [
                        {
                            "portal_id": r.portal_id,
                            "success": r.success,
                            "new_items": r.new_items,
                            "duplicates": r.duplicates,
                            "processing_time": r.processing_time,
                            "errors": r.errors
                        } for r in results
                    ],
                    "summary": {
                        "total_portals": len(results),
                        "successful_portals": len([r for r in results if r.success]),
                        "total_new_items": sum(r.new_items for r in results),
                        "total_processing_time": sum(r.processing_time for r in results)
                    }
                }
                
                logger.info(f"✅ 수동 수집 완료: 신규 {response['summary']['total_new_items']}개")
                return response
                
            except Exception as e:
                logger.error(f"❌ 수동 수집 실패: {e}")
                raise HTTPException(status_code=500, detail=f"수집 실패: {str(e)}")
        
        @app.get("/stats")
        async def get_service_stats():
            """서비스 통계 조회"""
            if not self.collection_engine:
                raise HTTPException(status_code=503, detail="수집 엔진이 초기화되지 않았습니다")
            
            try:
                # 전체 통계
                collection_stats = await self.get_collection_statistics()
                
                # 실시간 모니터링 통계
                monitor_stats = {}
                if real_time_monitor:
                    monitor_stats = await real_time_monitor.get_monitoring_summary()
                
                return {
                    "service": {
                        "status": "running" if self.is_running else "initializing",
                        "startup_time": self.isoformat() if self.startup_time else None,
                        "uptime_hours": (datetime.now() - self.startup_time).total_seconds() / 3600 if self.startup_time else 0
                    },
                    "collection": collection_stats,
                    "real_time_monitoring": monitor_stats,
                    "last_updated": datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"❌ 통계 조회 실패: {e}")
                raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")
        
        @app.post("/schedule/daily-auto")
        async def setup_daily_auto_collection():
            """일일 자동 수집 스케줄 설정"""
            if not self.auto_schedule_enabled:
                raise HTTPException(status_code=400, detail="자동 스케줄링이 비활성화되어 있습니다")
            
            try:
                # 스케줄 설정 (매일 오전 6시, 오후 1시)
                await self.setup_auto_schedule()
                
                return {
                    "success": True,
                    "message": "일일 자동 수집 스케줄이 설정되었습니다",
                    "schedules": [
                        {"time": "06:00", "portals": ["bizinfo"]},
                        {"time": "13:00", "portals": ["bizinfo", "kstartup"]}
                    ]
                }
                
            except Exception as e:
                logger.error(f"❌ 자동 스케줄 설정 실패: {e}")
                raise HTTPException(status_code=500, detail=f"스케줄 설정 실패: {str(e)}")
    
    async def startup_event(self):
        """서비스 시작 이벤트"""
        logger.info("🚀 통합 크롤링 수집 서비스 초기화 시작")
        
        try:
            # 1. 핵심 수집 엔진 초기화
            self.collection_engine = await create_collection_engine(self.db_connection_string)
            logger.info("✅ 핵심 수집 엔진 초기화 완료")
            
            # 2. 개별 수집기 초기화
            self.bizinfo_collector = BizinfoCollector(self.collection_engine)
            self.kstartup_collector = KStartupCollector(self.collection_engine)
            logger.info("✅ 개별 수집기 초기화 완료")
            
            # 3. 실시간 모니터링 초기화
            await initialize_monitor(self.db_connection_string)
            logger.info("✅ 실시간 모니터링 초기화 완료")
            
            # 4. 자동 스케줄링 설정 (옵션)
            if self.auto_schedule_enabled:
                await self.setup_auto_schedule()
                logger.info("✅ 자동 스케줄링 설정 완료")
            
            # 서비스 상태 업데이트
            self.is_running = True
            self.startup_time = datetime.now()
            
            logger.info("🎯 통합 크롤링 수집 서비스 초기화 완료")
            logger.info(f"🌐 서비스 접속: http://{self.service_host}:{self.service_port}")
            logger.info(f"📚 API 문서: http://{self.service_host}:{self.service_port}/docs")
            
        except Exception as e:
            logger.error(f"❌ 서비스 초기화 실패: {e}")
            raise
    
    async def shutdown_event(self):
        """서비스 종료 이벤트"""
        logger.info("🛑 통합 크롤링 수집 서비스 종료 시작")
        
        self.is_running = False
        
        # 스케줄된 작업 취소
        for task in self.scheduled_tasks:
            task.cancel()
        
        # 실시간 모니터링 종료
        if real_time_monitor:
            await real_time_monitor.close()
        
        # 수집 엔진 종료
        if self.collection_engine:
            await self.close()
        
        logger.info("✅ 통합 크롤링 수집 서비스 종료 완료")
    
    async def setup_auto_schedule(self):
        """자동 스케줄링 설정"""
        from datetime import time
        
        schedules = [
            (time(6, 0), ["bizinfo"], 10),      # 오전 6시, 기업마당, 10페이지
            (time(13, 0), ["bizinfo", "kstartup"], 15),  # 오후 1시, 전체, 15페이지
        ]
        
        for schedule_time, portals, max_pages in schedules:
            task = asyncio.create_task(
                self.scheduled_collection_task(schedule_time, portals, max_pages)
            )
            self.append(task)
            
        logger.info(f"📅 {len(schedules)}개의 자동 수집 스케줄 설정됨")
    
    async def scheduled_collection_task(self, target_time: time, portals: List[str], max_pages: int):
        """스케줄된 수집 작업"""
        while self.is_running:
            try:
                now = datetime.now().time()
                
                # 목표 시간까지 대기
                if now.hour == target_time.hour and now.minute == target_time.minute:
                    logger.info(f"⏰ 자동 수집 시작: {target_time} - {portals}")
                    
                    # 수집 실행
                    await run_comprehensive_collection(
                        db_connection_string=self.db_connection_string,
                        portals=portals,
                        max_pages=max_pages
                    )
                    
                    # 하루 대기 (중복 실행 방지)
                    await asyncio.sleep(86400)  # 24시간
                else:
                    # 1분 대기 후 재확인
                    await asyncio.sleep(60)
                    
            except Exception as e:
                logger.error(f"❌ 자동 수집 오류: {e}")
                await asyncio.sleep(300)  # 5분 대기 후 재시도
    
    def run(self):
        """서비스 실행"""
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/ubuntu/logs/integrated_collection_service.log'),
                logging.StreamHandler()
            ]
        )
        
        # 신호 처리 설정
        def signal_handler(signum, frame):
            logger.info(f"🛑 종료 신호 수신: {signum}")
            # FastAPI의 정상적인 종료 프로세스를 위해 여기서는 로깅만
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        logger.info("🎯 통합 크롤링 수집 서비스 시작")
        logger.info(f"🔧 데이터베이스: {self.db_connection_string}")
        logger.info(f"🌐 서비스 주소: {self.service_host}:{self.service_port}")
        
        # uvicorn으로 서비스 실행
        uvicorn.run(
            self.app,
            host=self.service_host,
            port=self.service_port,
            log_level="info",
            access_log=True
        )


def main():
    """메인 실행 함수"""
    service = IntegratedCollectionService()
    service.run()


if __name__ == "__main__":
    main()