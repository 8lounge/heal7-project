#!/usr/bin/env python3
"""
🎭 Heal7 큐브모듈러 백엔드 - 오케스트레이터 통합
- 큐브 기반 모듈러 아키텍처
- 기존 라우터와 새 큐브 시스템 동시 지원
- 메모리 최적화된 통합 서버
"""

import os
import sys
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.cors import CORSMiddleware
from fastapi.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 프로젝트 루트 경로 추가
sys.insert(0, os.dirname(os.abspath(__file__)))
# 백엔드 루트 경로 추가 (paperwork_services 모듈용)
sys.insert(0, os.dirname(os.dirname(os.abspath(__file__))))
# 큐브 시스템 경로 추가
sys.insert(0, os.join(os.dirname(os.dirname(os.abspath(__file__))), "cubes"))

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
    title="🎭 Heal7 큐브모듈러 API",
    description="큐브 기반 모듈러 아키텍처와 기존 라우터 시스템 통합",
    version="3.0",
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
        "https://saju.com", 
        "https://test.com",
        "https://admin.com",
        "https://paperwork.com",  # Paperwork AI 대시보드 추가
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
        "127.0.1", 
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
        f"{request.method} {request.path} - "
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

# 큐브 레지스트리 (오케스트레이터와 동일)
CUBE_REGISTRY = {
    "ai-dashboard": "ai.com",
    "paperwork-system": "paperwork.com",
    "saju-fortune-system": "saju.com",
    "test-environment": "test.com",
    "crawling-api": "crawling.com"
}

CUBE_PORTS = {
    "ai-dashboard": 8001,
    "paperwork-system": 8002,
    "saju-fortune-system": 8003,
    "test-environment": 8004,
    "crawling-api": 8006
}

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "service": "🎭 Heal7 큐브모듈러 API 서버",
        "version": "3.0", 
        "status": "running",
        "architecture": "cube-modular",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "큐브 모듈러 아키텍처",
            "독립 실행 가능 큐브",
            "오케스트레이터 통합",
            "기존 라우터 호환성",
            "메모리 최적화"
        ],
        "cubes": {
            "total": len(CUBE_REGISTRY),
            "registered": list(CUBE_REGISTRY.keys()),
            "services": CUBE_REGISTRY
        }
    }

# 헬스체크 엔드포인트 (큐브 상태 포함)
@app.get("/health")
async def health_check():
    import httpx
    
    # 큐브 상태 확인 (비동기)
    cube_status = {}
    for cube_name, port in CUBE_PORTS.items():
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"http://localhost:{port}/health")
                cube_status[cube_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "port": port,
                    "url": f"http://localhost:{port}"
                }
        except:
            cube_status[cube_name] = {
                "status": "offline",
                "port": port,
                "url": f"http://localhost:{port}"
            }
    
    healthy_cubes = sum(1 for cube in cube_status.values() if cube["status"] == "healthy")
    total_cubes = len(cube_status)
    
    return {
        "status": "healthy",
        "service": "heal7-cube-modular",
        "architecture": "cube-modular",
        "timestamp": datetime.now().isoformat(),
        "uptime": "서버 운영 중",
        "cubes": {
            "healthy": healthy_cubes,
            "total": total_cubes,
            "status": cube_status
        }
    }

# API 헬스체크 엔드포인트 (프론트엔드용)
@app.get("/api/health")
async def api_health_check():
    return {
        "status": "healthy",
        "service": "heal7-api",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0",
        "uptime": "서버 운영 중"
    }

# API 정보 엔드포인트 (큐브 정보 포함)
@app.get("/api")
async def api_info():
    return {
        "api_version": "3.0",
        "architecture": "cube-modular",
        "legacy_services": {
            "saju": "/api/saju - 사주명리학 서비스 (기존 라우터)",
            "test": "/api/test - 테스트 환경 (기존 라우터)",
            "admin": "/api/admin - 관리자 서비스 (기존 라우터)",
            "index": "/api/index - 메인 서비스 (기존 라우터)",
            "paperwork": "/api/paperwork - 문서 AI 변환 서비스 (기존 라우터)"
        },
        "cube_services": {
            f"{cube_name}": f"http://localhost:{port} - {service_domain}" 
            for cube_name, service_domain in CUBE_REGISTRY.items()
            if cube_name in CUBE_PORTS
            for port in [CUBE_PORTS[cube_name]]
        },
        "cube_management": {
            "health": "/api/cubes/health - 큐브 상태 확인",
            "list": "/api/cubes - 큐브 목록",
            "individual": "/api/cubes/{cube_name} - 개별 큐브 정보"
        },
        "docs": "/api/docs",
        "timestamp": datetime.now().isoformat()
    }

# 큐브 관리 엔드포인트들
@app.get("/api/cubes")
async def list_cubes():
    """등록된 큐브 목록"""
    import httpx
    
    cube_info = []
    for cube_name, service_domain in CUBE_REGISTRY.items():
        port = CUBE_PORTS[cube_name]
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"http://localhost:{port}/health")
                status = "healthy" if response.status_code == 200 else "unhealthy"
        except:
            status = "offline"
        
        cube_info.append({
            "name": cube_name,
            "service": service_domain,
            "port": port,
            "url": f"http://localhost:{port}",
            "status": status,
            "docs": f"http://localhost:{port}/docs"
        })
    
    return {
        "cubes": cube_info,
        "total_count": len(cube_info),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/cubes/health")
async def cubes_health():
    """모든 큐브 상태 확인"""
    return await health_check()

@app.get("/api/cubes/{cube_name}")
async def get_cube_info(cube_name: str):
    """특정 큐브 정보 조회"""
    import httpx
    
    if cube_name not in CUBE_REGISTRY:
        raise HTTPException(status_code=404, detail=f"큐브 '{cube_name}'을 찾을 수 없습니다.")
    
    port = CUBE_PORTS[cube_name]
    service_domain = CUBE_REGISTRY[cube_name]
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            # 큐브의 루트 엔드포인트에서 정보 가져오기
            response = await client.get(f"http://localhost:{port}/")
            cube_data = response.json() if response.status_code == 200 else {}
            
            health_response = await client.get(f"http://localhost:{port}/health")
            health_data = health_response.json() if health_response.status_code == 200 else {}
            
            return {
                "name": cube_name,
                "service": service_domain,
                "port": port,
                "url": f"http://localhost:{port}",
                "status": "healthy" if health_response.status_code == 200 else "unhealthy",
                "info": cube_data,
                "health": health_data,
                "docs": f"http://localhost:{port}/docs",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "name": cube_name,
            "service": service_domain,
            "port": port,
            "url": f"http://localhost:{port}",
            "status": "offline",
            "error": str(e),
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

# try:
#     from routers.fortune_contents import router as fortune_router
#     app.include_router(fortune_router, prefix="/api", tags=["Fortune"])
#     logger.info("✅ 운세 콘텐츠 라우터 등록 완료")
# except ImportError as e:
#     logger.warning(f"⚠️ 운세 콘텐츠 라우터 임포트 실패: {e}")

try:
    from routers.simple_tarot import router as tarot_router
    app.include_router(tarot_router, prefix="/api", tags=["Tarot"])
    logger.info("✅ 타로 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 타로 라우터 임포트 실패: {e}")

try:
    from routers.simple_saju import router as simple_saju_router
    app.include_router(simple_saju_router, prefix="/api", tags=["Simple-Saju"])
    logger.info("✅ 간단 사주 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 간단 사주 라우터 임포트 실패: {e}")

# Dream Interpretation 라우터 등록
try:
    from routers.dream_interpretation import router as dream_router
    app.include_router(dream_router, tags=["Dream-Interpretation"])
    logger.info("✅ Dream Interpretation 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ Dream Interpretation 라우터 임포트 실패: {e}")

if __name__ == "__main__":
    # 환경별 설정
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0")
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