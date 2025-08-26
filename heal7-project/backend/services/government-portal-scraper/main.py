#!/usr/bin/env python3
"""
Government Portal Intelligence System
정부 포털 지능화 시스템 - 메인 서버

Author: Paperwork AI Team
Version: 2.0.0  
Date: 2025-08-23
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from scrapers.bizinfo_scraper import BizinfoScraper
from scrapers.kstartup_scraper import KStartupScraper
from analyzers.pattern_analyzer import KoreanPortalPatternAnalyzer
from database.db_manager import DatabaseManager
from utils.scheduler import UpdateScheduler
from utils.rate_limiter import RateLimiter
from config.settings import settings

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/portal_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI 앱 초기화
app = FastAPI(
    title="Government Portal Intelligence System",
    description="정부 포털 실시간 모니터링 및 템플릿 자동 생성 시스템",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정 (Paperwork AI 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://paperwork.heal7.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 글로벌 객체 초기화
db_manager = DatabaseManager(settings.DATABASE_URL)
pattern_analyzer = KoreanPortalPatternAnalyzer()
scheduler = UpdateScheduler()
scrapers = {}

# Pydantic 모델
class ScrapingRequest(BaseModel):
    portal_ids: List[str]
    force_update: bool = False
    include_analysis: bool = True

class TemplateRequest(BaseModel):
    program_ids: List[str]
    institution: Optional[str] = None
    template_type: Optional[str] = None

class ScrapingResult(BaseModel):
    success: bool
    portal_id: str
    programs_found: int
    new_programs: int
    updated_programs: int
    processing_time_seconds: float
    error_message: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """서버 시작시 초기화"""
    logger.info("🚀 Government Portal Intelligence System 시작")
    
    # 데이터베이스 초기화
    await db_manager.initialize()
    logger.info("✅ 데이터베이스 연결 완료")
    
    # 스크래퍼 초기화
    scrapers['bizinfo'] = BizinfoScraper(db_manager, rate_limiter=RateLimiter(20))
    scrapers['kstartup'] = KStartupScraper(db_manager, rate_limiter=RateLimiter(15))
    logger.info("✅ 스크래퍼 초기화 완료")
    
    # 스케줄러 시작
    await scheduler.start()
    
    # 일일 자동 스크래핑 스케줄 설정
    await schedule_daily_scraping()
    logger.info("✅ 자동 스케줄링 시작")

@app.on_event("shutdown") 
async def shutdown_event():
    """서버 종료시 정리"""
    logger.info("🛑 시스템 종료 중...")
    await scheduler.stop()
    await db_manager.close()
    for scraper in scrapers.values():
        if hasattr(scraper, 'close'):
            await scraper.close()

async def schedule_daily_scraping():
    """매일 자동 스크래핑 스케줄 설정"""
    
    # 매일 오전 6시에 기업마당 스크래핑
    await scheduler.schedule_daily(
        hour=6, minute=0,
        func=run_scheduled_scraping,
        args=(['bizinfo'],),
        job_id="daily_bizinfo_scraping"
    )
    
    # 매일 오전 7시에 K-Startup 스크래핑  
    await scheduler.schedule_daily(
        hour=7, minute=0,
        func=run_scheduled_scraping,
        args=(['kstartup'],),
        job_id="daily_kstartup_scraping"
    )
    
    # 매일 오후 1시에 전체 포털 스크래핑
    await scheduler.schedule_daily(
        hour=13, minute=0,
        func=run_scheduled_scraping,
        args=(['bizinfo', 'kstartup'],),
        job_id="daily_full_scraping"
    )

async def run_scheduled_scraping(portal_ids: List[str]):
    """스케줄된 스크래핑 실행"""
    logger.info(f"⏰ 스케줄된 스크래핑 시작: {portal_ids}")
    
    results = []
    for portal_id in portal_ids:
        try:
            result = await execute_single_scraping(portal_id, include_analysis=True)
            results.append(result)
            logger.info(f"✅ {portal_id} 스크래핑 완료: {result.programs_found}개 프로그램 발견")
        except Exception as e:
            logger.error(f"❌ {portal_id} 스크래핑 실패: {str(e)}")
            results.append(ScrapingResult(
                success=False,
                portal_id=portal_id,
                programs_found=0,
                new_programs=0,
                updated_programs=0,
                processing_time_seconds=0,
                error_message=str(e)
            ))
    
    # Paperwork AI에 결과 전송
    await notify_paperwork_ai(results)

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "service": "Government Portal Intelligence System",
        "version": "2.0.0",
        "status": "running",
        "active_scrapers": list(scrapers.keys()),
        "last_update": await get_last_update_time()
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        # 데이터베이스 연결 확인
        await db_manager.test_connection()
        
        # 스크래퍼 상태 확인
        scraper_status = {}
        for name, scraper in scrapers.items():
            scraper_status[name] = await scraper.get_status()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "scrapers": scraper_status
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.post("/scrape/manual", response_model=List[ScrapingResult])
async def manual_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """수동 스크래핑 실행"""
    logger.info(f"🔧 수동 스크래핑 요청: {request.portal_ids}")
    
    if not request.portal_ids:
        raise HTTPException(status_code=400, detail="포털 ID를 지정해주세요")
    
    # 유효한 포털 ID 확인
    invalid_portals = [pid for pid in request.portal_ids if pid not in scrapers]
    if invalid_portals:
        raise HTTPException(
            status_code=400, 
            detail=f"지원하지 않는 포털: {invalid_portals}. 지원 포털: {list(scrapers.keys())}"
        )
    
    results = []
    for portal_id in request.portal_ids:
        try:
            result = await execute_single_scraping(
                portal_id, 
                force_update=request.force_update,
                include_analysis=request.include_analysis
            )
            results.append(result)
        except Exception as e:
            logger.error(f"❌ {portal_id} 수동 스크래핑 실패: {str(e)}")
            results.append(ScrapingResult(
                success=False,
                portal_id=portal_id,
                programs_found=0,
                new_programs=0,
                updated_programs=0,
                processing_time_seconds=0,
                error_message=str(e)
            ))
    
    # 백그라운드에서 Paperwork AI 알림
    background_tasks.add_task(notify_paperwork_ai, results)
    
    return results

async def execute_single_scraping(
    portal_id: str, 
    force_update: bool = False,
    include_analysis: bool = True
) -> ScrapingResult:
    """개별 포털 스크래핑 실행"""
    start_time = datetime.now()
    scraper = scrapers[portal_id]
    
    try:
        # 1. 스크래핑 실행
        scraped_programs = await scraper.scrape_all_programs(force_update=force_update)
        
        # 2. 데이터베이스 저장 및 변경사항 감지
        save_result = await db_manager.save_programs(portal_id, scraped_programs)
        
        # 3. AI 분석 수행 (옵션)
        if include_analysis and save_result['new_programs']:
            await perform_ai_analysis(portal_id, save_result['new_programs'])
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ScrapingResult(
            success=True,
            portal_id=portal_id,
            programs_found=len(scraped_programs),
            new_programs=save_result['new_count'],
            updated_programs=save_result['updated_count'],
            processing_time_seconds=processing_time
        )
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        raise Exception(f"스크래핑 실패: {str(e)}")

async def perform_ai_analysis(portal_id: str, new_programs: List[Dict]):
    """새로운 프로그램에 대한 AI 분석 수행"""
    logger.info(f"🤖 AI 분석 시작: {portal_id}, {len(new_programs)}개 프로그램")
    
    for program in new_programs:
        try:
            # AI 패턴 분석
            analysis_result = await pattern_analyzer.analyze_korean_program_structure(program)
            
            # 분석 결과 저장
            await db_manager.save_analysis_result(program['program_id'], analysis_result)
            
            # 템플릿 자동 생성 (품질 점수 8점 이상시)
            if analysis_result.get('quality_score', 0) >= 8.0:
                await generate_auto_template(program, analysis_result)
                
        except Exception as e:
            logger.error(f"❌ {program['program_id']} AI 분석 실패: {str(e)}")

async def generate_auto_template(program: Dict, analysis_result: Dict):
    """AI 분석 결과를 바탕으로 템플릿 자동 생성"""
    try:
        logger.info(f"📋 템플릿 생성 시작: {program['program_id']}")
        
        # 기본 템플릿 구조 생성
        template_data = {
            'program_id': program['program_id'],
            'title': program.get('title', ''),
            'agency': program.get('agency', ''),
            'support_details': program.get('support_details', {}),
            'application_period': program.get('application_period', ''),
            'target_audience': program.get('target_audience', ''),
            'quality_score': analysis_result.get('quality_score', 0),
            'generated_at': datetime.now().isoformat(),
            'auto_generated': True
        }
        
        # 템플릿 저장 로직 (실제 구현)
        await db_manager.save_auto_generated_template(template_data)
        logger.info(f"✅ 템플릿 생성 완료: {program['program_id']}")
        
    except Exception as e:
        logger.error(f"❌ 템플릿 생성 실패: {program['program_id']} - {str(e)}")

@app.get("/programs/latest")
async def get_latest_programs(
    portal_id: Optional[str] = None,
    limit: int = 50,
    days: int = 7
):
    """최신 지원사업 프로그램 조회"""
    since_date = datetime.now() - timedelta(days=days)
    
    programs = await db_manager.get_programs(
        portal_id=portal_id,
        since_date=since_date,
        limit=limit
    )
    
    return {
        "count": len(programs),
        "programs": programs,
        "filters": {
            "portal_id": portal_id,
            "since_date": since_date.isoformat(),
            "limit": limit
        }
    }

@app.get("/templates/auto-generated")
async def get_auto_generated_templates(
    portal_id: Optional[str] = None,
    status: str = "approved"
):
    """자동 생성된 템플릿 조회"""
    templates = await db_manager.get_auto_generated_templates(
        portal_id=portal_id,
        status=status
    )
    
    return {
        "count": len(templates),
        "templates": templates
    }

@app.post("/paperwork/sync")
async def sync_with_paperwork_ai():
    """Paperwork AI와 수동 동기화"""
    try:
        # 최근 업데이트된 템플릿과 프로그램 정보 전송
        recent_data = await prepare_paperwork_sync_data()
        
        # Paperwork AI에 전송
        sync_result = await send_to_paperwork_ai(recent_data)
        
        return {
            "success": True,
            "sync_result": sync_result,
            "synced_templates": len(recent_data.get('templates', [])),
            "synced_programs": len(recent_data.get('programs', []))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"동기화 실패: {str(e)}")

async def prepare_paperwork_sync_data() -> Dict:
    """Paperwork AI 동기화용 데이터 준비"""
    # 최근 7일간의 데이터
    since_date = datetime.now() - timedelta(days=7)
    
    return {
        "templates": await db_manager.get_auto_generated_templates(
            since_date=since_date,
            status="approved"
        ),
        "programs": await db_manager.get_programs(
            since_date=since_date,
            include_analysis=True
        ),
        "sync_timestamp": datetime.now().isoformat()
    }

async def send_to_paperwork_ai(data: Dict) -> Dict:
    """Paperwork AI에 데이터 전송"""
    import aiohttp
    
    paperwork_api_url = "https://paperwork.heal7.com/api/government-portal/sync"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            paperwork_api_url,
            json=data,
            headers={
                "Authorization": f"Bearer {settings.PAPERWORK_API_KEY}",
                "Content-Type": "application/json"
            }
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Paperwork AI 전송 실패: {response.status}")

async def notify_paperwork_ai(results: List[ScrapingResult]):
    """스크래핑 결과를 Paperwork AI에 알림"""
    try:
        notification_data = {
            "event": "scraping_completed",
            "timestamp": datetime.now().isoformat(),
            "results": [result.dict() for result in results],
            "summary": {
                "total_portals": len(results),
                "successful_portals": len([r for r in results if r.success]),
                "total_new_programs": sum(r.new_programs for r in results if r.success),
                "total_updated_programs": sum(r.updated_programs for r in results if r.success)
            }
        }
        
        await send_to_paperwork_ai(notification_data)
        logger.info("📡 Paperwork AI 알림 전송 완료")
        
    except Exception as e:
        logger.error(f"❌ Paperwork AI 알림 전송 실패: {str(e)}")

async def get_last_update_time() -> Optional[str]:
    """마지막 업데이트 시간 조회"""
    try:
        last_update = await db_manager.get_last_update_time()
        return last_update.isoformat() if last_update else None
    except:
        return None

if __name__ == "__main__":
    import os
    
    # 환경변수 설정
    port = int(os.environ.get("PORT", 8005))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"🌐 Government Portal Intelligence System 시작: {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # 프로덕션에서는 False
        log_level="info",
        access_log=True
    )