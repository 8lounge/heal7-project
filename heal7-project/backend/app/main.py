#!/usr/bin/env python3
"""
Heal7 통합 FastAPI 백엔드
- React 19 + Next.js 프론트엔드와 연동
- 서비스별 라우터 기반 API 구조
- 메모리 최적화된 단일 서버
"""

import os
import sys
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 백엔드 루트 경로 추가 (paperwork_services 모듈용)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/heal7-unified.log')
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 라이프사이클 관리"""
    logger.info("🚀 Heal7 통합 서버 시작")
    yield
    logger.info("🛑 Heal7 통합 서버 종료")

# FastAPI 앱 생성
app = FastAPI(
    title="Heal7 통합 API",
    description="React 19 + Next.js와 연동된 FastAPI 통합 백엔드",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js 개발 서버
        "https://heal7.com",
        "https://saju.heal7.com", 
        "https://test.heal7.com",
        "https://admin.heal7.com",
        "https://paperwork.heal7.com",  # Paperwork AI 대시보드 추가
        "https://*.heal7.com",
        "*"  # 개발 중에는 모든 오리진 허용
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# 신뢰할 수 있는 호스트 미들웨어
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1", 
        "*.heal7.com",
        "heal7.com"
    ]
)

# 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {process_time:.3f}s"
    )
    return response

# 글로벌 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "서버에서 오류가 발생했습니다.",
            "timestamp": datetime.now().isoformat()
        }
    )

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "service": "Heal7 통합 API 서버",
        "version": "2.0.0", 
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "React 19 + Next.js 연동",
            "서비스별 라우터 구조",
            "메모리 최적화",
            "통합 API 관리"
        ]
    }

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "heal7-unified",
        "timestamp": datetime.now().isoformat(),
        "uptime": "서버 운영 중"
    }

# API 헬스체크 엔드포인트 (프론트엔드용)
@app.get("/api/health")
async def api_health_check():
    return {
        "status": "healthy",
        "service": "heal7-api",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "uptime": "서버 운영 중"
    }

# API 정보 엔드포인트
@app.get("/api")
async def api_info():
    return {
        "api_version": "2.0.0",
        "services": {
            "saju": "/api/saju - 사주명리학 서비스",
            "test": "/api/test - 테스트 환경", 
            "admin": "/api/admin - 관리자 서비스",
            "index": "/api/index - 메인 서비스",
            "paperwork": "/api/paperwork - 문서 AI 변환 서비스"
        },
        "docs": "/api/docs",
        "timestamp": datetime.now().isoformat()
    }

# 서비스별 라우터 등록
try:
    from routers.saju import router as saju_router
    app.include_router(saju_router, prefix="/api/saju", tags=["Saju"])
    logger.info("✅ 사주 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 사주 라우터 임포트 실패: {e}")

try:
    from routers.test import router as test_router  
    app.include_router(test_router, prefix="/api/test", tags=["Test"])
    logger.info("✅ 테스트 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 테스트 라우터 임포트 실패: {e}")

try:
    from routers.admin import router as admin_router
    app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
    logger.info("✅ 관리자 라우터 등록 완료") 
except ImportError as e:
    logger.warning(f"⚠️ 관리자 라우터 임포트 실패: {e}")

try:
    from routers.saju_admin import router as saju_admin_router
    app.include_router(saju_admin_router, prefix="/api", tags=["Saju-Admin"])
    logger.info("✅ 사주 관리자 라우터 등록 완료") 
except ImportError as e:
    logger.warning(f"⚠️ 사주 관리자 라우터 임포트 실패: {e}")

try:
    from routers.index import router as index_router
    app.include_router(index_router, prefix="/api/index", tags=["Index"])
    logger.info("✅ 인덱스 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 인덱스 라우터 임포트 실패: {e}")

try:
    from routers.paperwork import router as paperwork_router
    app.include_router(paperwork_router, tags=["Paperwork"])
    logger.info("✅ Paperwork 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ Paperwork 라우터 임포트 실패: {e}")

try:
    from routers.scraping_dashboard_simple import router as scraping_router
    app.include_router(scraping_router, tags=["Scraping-Dashboard"])
    logger.info("✅ 스크래핑 대시보드 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 스크래핑 대시보드 라우터 임포트 실패: {e}")

try:
    from routers.ai_proxy import router as ai_proxy_router
    app.include_router(ai_proxy_router, tags=["AI-Proxy"])
    logger.info("✅ AI 프록시 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ AI 프록시 라우터 임포트 실패: {e}")

try:
    from routers.env_config import router as env_config_router
    app.include_router(env_config_router, tags=["Env-Config"])
    logger.info("✅ 환경설정 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 환경설정 라우터 임포트 실패: {e}")

if __name__ == "__main__":
    # 환경별 설정
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    workers = int(os.getenv("WORKERS", 1))
    
    logger.info(f"🌐 서버 시작: http://{host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        reload=os.getenv("NODE_ENV") == "development",
        access_log=True,
        log_level="info"
    )