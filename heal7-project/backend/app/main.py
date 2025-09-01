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
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 백엔드 루트 경로 추가 (paperwork_services 모듈용)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 큐브 시스템 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cubes"))

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
    version="3.0.0",
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

# 큐브 레지스트리 (오케스트레이터와 동일)
CUBE_REGISTRY = {
    "ai-dashboard": "ai.heal7.com",
    "paperwork-system": "paperwork.heal7.com",
    "saju-fortune-system": "saju.heal7.com",
    "test-environment": "test.heal7.com",
    "crawling-api": "crawling.heal7.com"
}

CUBE_PORTS = {
    "paperwork-system": 8001,
    "test-environment": 8002,
    "saju-fortune-system": 8003,
    "crawling-api": 8004,
    "ai-monitoring-system": 8005,
    "dashboard-system": 8006,
    "ai-dashboard": 8080
}

# 루트 엔드포인트 - HTML 대시보드
@app.get("/", response_class=HTMLResponse)
async def root():
    import httpx
    
    # 큐브 상태 확인
    cube_status = {}
    for cube_name, port in CUBE_PORTS.items():
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"http://localhost:{port}/health")
                cube_status[cube_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "port": port,
                    "domain": CUBE_REGISTRY.get(cube_name, "N/A")
                }
        except:
            cube_status[cube_name] = {
                "status": "offline",
                "port": port,
                "domain": CUBE_REGISTRY.get(cube_name, "N/A")
            }
    
    healthy_cubes = sum(1 for cube in cube_status.values() if cube["status"] == "healthy")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 HEAL7 큐브모듈러 대시보드</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .stat-card h3 {{
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 1.2rem;
        }}
        .stat-card .number {{
            font-size: 2rem;
            font-weight: bold;
            color: #2d3748;
        }}
        .cubes-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .cube-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}
        .cube-card:hover {{
            transform: translateY(-5px);
        }}
        .cube-header {{
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .cube-name {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #2d3748;
        }}
        .status-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-healthy {{
            background: #c6f6d5;
            color: #22543d;
        }}
        .status-offline {{
            background: #fed7d7;
            color: #742a2a;
        }}
        .status-unhealthy {{
            background: #fef5e7;
            color: #744210;
        }}
        .cube-info {{
            color: #4a5568;
            margin-bottom: 10px;
        }}
        .cube-info strong {{
            color: #2d3748;
        }}
        .cube-links {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}
        .cube-link {{
            padding: 8px 16px;
            background: #4299e1;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9rem;
            transition: background 0.3s ease;
        }}
        .cube-link:hover {{
            background: #3182ce;
        }}
        .refresh-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 20px;
            background: #48bb78;
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: background 0.3s ease;
        }}
        .refresh-btn:hover {{
            background: #38a169;
        }}
        .timestamp {{
            text-align: center;
            margin-top: 30px;
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 HEAL7 큐브모듈러 대시보드</h1>
            <p>큐브 기반 모듈러 아키텍처 | 버전 3.0.0</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>📊 총 큐브</h3>
                <div class="number">{len(CUBE_REGISTRY)}</div>
            </div>
            <div class="stat-card">
                <h3>✅ 정상 큐브</h3>
                <div class="number">{healthy_cubes}</div>
            </div>
            <div class="stat-card">
                <h3>⚡ 시스템 상태</h3>
                <div class="number">운영 중</div>
            </div>
            <div class="stat-card">
                <h3>🏗️ 아키텍처</h3>
                <div class="number">큐브모듈러</div>
            </div>
        </div>
        
        <div class="cubes-grid">"""

    for cube_name, cube_info in cube_status.items():
        status_class = f"status-{cube_info['status']}"
        status_icon = "✅" if cube_info['status'] == "healthy" else "🔴" if cube_info['status'] == "offline" else "⚠️"
        
        html_content += f"""
            <div class="cube-card">
                <div class="cube-header">
                    <div class="cube-name">{cube_name}</div>
                    <span class="{status_class} status-badge">{status_icon} {cube_info['status']}</span>
                </div>
                <div class="cube-info">
                    <strong>포트:</strong> {cube_info['port']}<br>
                    <strong>도메인:</strong> {cube_info['domain']}<br>
                    <strong>URL:</strong> http://localhost:{cube_info['port']}
                </div>
                <div class="cube-links">
                    <a href="http://localhost:{cube_info['port']}/health" class="cube-link" target="_blank">헬스체크</a>
                    <a href="http://localhost:{cube_info['port']}/docs" class="cube-link" target="_blank">API 문서</a>
                </div>
            </div>"""

    html_content += f"""
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 새로고침</button>
        
        <div class="timestamp">
            마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} KST
        </div>
    </div>
    
    <script>
        // 5분마다 자동 새로고침
        setTimeout(() => location.reload(), 300000);
        
        // 큐브 상태에 따른 실시간 업데이트 (선택적)
        setInterval(async () => {{
            try {{
                const response = await fetch('/health');
                const data = await response.json();
                // 상태 업데이트 로직 (필요시 구현)
            }} catch(e) {{
                console.log('헬스체크 실패:', e);
            }}
        }}, 30000); // 30초마다 체크
    </script>
</body>
</html>"""
    
    return html_content

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
        "version": "2.0.0",
        "uptime": "서버 운영 중"
    }

# API 정보 엔드포인트 (큐브 정보 포함)
@app.get("/api")
async def api_info():
    return {
        "api_version": "3.0.0",
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

# 인증 시스템 라우터 등록
try:
    from routers.auth import router as auth_router
    app.include_router(auth_router, tags=["인증"])
    logger.info("✅ 인증 라우터 등록 완료") 
except ImportError as e:
    logger.warning(f"⚠️ 인증 라우터 임포트 실패: {e}")

try:
    from routers.user_management import router as user_management_router
    app.include_router(user_management_router, tags=["관리자-회원관리"])
    logger.info("✅ 회원관리 라우터 등록 완료") 
except ImportError as e:
    logger.warning(f"⚠️ 회원관리 라우터 임포트 실패: {e}")

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

try:
    from routers.fortune_contents import router as fortune_router
    app.include_router(fortune_router, prefix="/api", tags=["Fortune"])
    logger.info("✅ 운세 콘텐츠 라우터 등록 완료")
except ImportError as e:
    logger.warning(f"⚠️ 운세 콘텐츠 라우터 임포트 실패: {e}")

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
    # 환경별 설정 (큐브모듈러 대시보드 - 포트 8000)
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