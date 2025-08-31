#!/usr/bin/env python3
"""
🎛️ HEAL7 통합 관리 대시보드 v1.0
모든 cube 서비스들을 상단 탭으로 통합 관리
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import asyncio
import logging
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import psutil
import subprocess
import os
import signal

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🎛️ HEAL7 통합 관리 대시보드",
    description="모든 큐브 서비스들을 상단 탭으로 통합 관리",
    version="1.0"
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 큐브 서비스 설정
CUBE_SERVICES = {
    "crawling": {
        "name": "🕷️ 크롤링 시스템",
        "url": "http://localhost:8005",
        "icon": "bi-spider",
        "status": "active",
        "description": "웹 크롤링, 데이터 수집 및 관리"
    },
    "paperwork": {
        "name": "📄 Paperwork AI",  
        "url": "http://localhost:8003",
        "icon": "bi-file-earmark-text",
        "status": "active",
        "description": "AI 기반 문서 처리 및 관리"
    },
    "ai_dashboard": {
        "name": "🤖 AI 대시보드",
        "url": "http://localhost:8001", 
        "icon": "bi-robot",
        "status": "active",
        "description": "9개 AI 모델 통합 관리"
    },
    "saju": {
        "name": "🔮 사주 시스템",
        "url": "http://localhost:8002",
        "icon": "bi-stars",
        "status": "active", 
        "description": "사주명리학 해석 및 운세 서비스"
    },
    "test_env": {
        "name": "🧪 테스트 환경",
        "url": "http://localhost:8004",
        "icon": "bi-flask",
        "status": "active",
        "description": "개발 및 테스트 환경 관리"
    }
}

class ServiceManager:
    """서비스 상태 관리자"""
    
    @staticmethod
    async def check_service_status(service_url: str) -> Dict[str, Any]:
        """개별 서비스 상태 확인"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service_url}/")
                return {
                    "status": "online",
                    "response_time": response.total_seconds() * 1000,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "offline", 
                "error": str(e),
                "response_time": None,
                "status_code": None
            }
    
    @staticmethod
    async def get_all_services_status() -> Dict[str, Dict[str, Any]]:
        """모든 서비스 상태 동시 확인"""
        tasks = []
        for service_id, service_info in CUBE_SERVICES.items():
            tasks.append(
                ServiceManager.check_service_status(service_info["url"])
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        status_report = {}
        for i, (service_id, service_info) in enumerate(CUBE_SERVICES.items()):
            try:
                status_report[service_id] = {
                    **service_info,
                    **results[i]
                }
            except Exception as e:
                status_report[service_id] = {
                    **service_info,
                    "status": "error",
                    "error": str(e)
                }
        
        return status_report
    
    @staticmethod
    async def get_system_metrics() -> Dict[str, Any]:
        """시스템 메트릭 수집"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "usage_percent": cpu_percent,
                    "cores": psutil.cpu_count()
                },
                "memory": {
                    "usage_percent": memory.percent,
                    "available_gb": memory.available / (1024**3),
                    "total_gb": memory.total / (1024**3)
                },
                "disk": {
                    "usage_percent": disk.percent,
                    "free_gb": disk.free / (1024**3),
                    "total_gb": disk.total / (1024**3)
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv
                }
            }
        except Exception as e:
            logger.error(f"시스템 메트릭 수집 실패: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def control_service(service_id: str, action: str) -> Dict[str, Any]:
        """서비스 제어 (시작/중단/재시작)"""
        if service_id not in CUBE_SERVICES:
            return {"success": False, "error": "Service not found"}
        
        service_info = CUBE_SERVICES[service_id]
        service_port = service_info["url"].split(":")[-1]
        
        try:
            if action == "stop":
                # 포트에서 실행 중인 프로세스 찾아서 중단
                result = subprocess.run(['sudo', 'lsof', '-ti', f':{service_port}'], 
                                      capture_output=True, text=True)
                if result.strip():
                    pids = result.strip().split('\n')
                    for pid in pids:
                        os.kill(int(pid), signal.SIGTERM)
                    return {"success": True, "message": f"Service {service_id} stopped"}
                else:
                    return {"success": False, "error": "Service not running"}
            
            elif action == "start":
                # 서비스별 시작 명령 실행
                service_paths = {
                    "crawling": "/home/ubuntu/heal7-project/backend/cubes/crawling-api",
                    "ai_dashboard": "/home/ubuntu/heal7-project/backend/cubes/ai-dashboard", 
                    "paperwork": "/home/ubuntu/heal7-project/backend/cubes/paperwork-system",
                    "saju": "/home/ubuntu/heal7-project/backend/cubes/saju-fortune-system",
                    "test_env": "/home/ubuntu/heal7-project/backend/cubes/test-environment"
                }
                
                if service_id in service_paths:
                    cmd = f"cd {service_paths[service_id]} && python3 main.py &"
                    subprocess.run(cmd, shell=True)
                    return {"success": True, "message": f"Service {service_id} started"}
                
            elif action == "restart":
                # 중단 후 시작
                stop_result = await ServiceManager.control_service(service_id, "stop")
                await asyncio.sleep(2)
                start_result = await ServiceManager.control_service(service_id, "start")
                return {"success": True, "message": f"Service {service_id} restarted"}
                
        except Exception as e:
            logger.error(f"서비스 제어 실패 {service_id} {action}: {e}")
            return {"success": False, "error": str(e)}

# API 엔드포인트들
@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """통합 관리 대시보드 메인 페이지"""
    services_status = await ServiceManager.get_all_services_status()
    
    return templates.TemplateResponse("integrated_dashboard.html", {
        "request": request,
        "services": services_status,
        "current_time": datetime.now().isoformat(),
        "total_services": len(CUBE_SERVICES),
        "online_services": len([s for s in services_status.values() if s.get("status") == "online"])
    })

@app.get("/cube-architecture", response_class=HTMLResponse)
async def cube_architecture_dashboard(request: Request):
    """큐브 모듈러 아키텍처 설계 대시보드"""
    services_status = await ServiceManager.get_all_services_status()
    system_metrics = await ServiceManager.get_system_metrics()
    
    return templates.TemplateResponse("cube_architecture_dashboard.html", {
        "request": request,
        "services": services_status,
        "system_metrics": system_metrics,
        "current_time": datetime.now().isoformat()
    })

@app.get("/api/services/status")
async def get_services_status():
    """모든 서비스 상태 API"""
    return await ServiceManager.get_all_services_status()

@app.get("/api/services/{service_id}/proxy/{path:path}")
async def service_proxy(service_id: str, path: str, request: Request):
    """서비스 프록시 - API 호출 중계"""
    if service_id not in CUBE_SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service_url = CUBE_SERVICES[service_id]["url"]
    target_url = f"{service_url}/{path}"
    
    # 쿼리 파라미터 전달
    query_params = str(request.query)
    if query_params:
        target_url += f"?{query_params}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 요청 메서드에 따라 처리
            if request.method == "GET":
                response = await client.get(target_url)
            elif request.method == "POST":
                body = await request.body()
                response = await client.post(target_url, content=body)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            return JSONResponse(
                content=response.json() if response.get('content-type', '').startswith('application/json') else {"data": response.text},
                status_code=response.status_code
            )
    except Exception as e:
        logger.error(f"프록시 오류 {target_url}: {e}")
        raise HTTPException(status_code=502, detail=f"Service proxy error: {str(e)}")

@app.get("/api/system/overview")
async def system_overview():
    """시스템 전체 개요 정보"""
    services_status = await ServiceManager.get_all_services_status()
    
    overview = {
        "timestamp": datetime.now().isoformat(),
        "system_status": "healthy" if all(s.get("status") == "online" for s in services_status.values()) else "degraded",
        "services_summary": {
            "total": len(CUBE_SERVICES),
            "online": len([s for s in services_status.values() if s.get("status") == "online"]),
            "offline": len([s for s in services_status.values() if s.get("status") == "offline"]),
            "error": len([s for s in services_status.values() if s.get("status") == "error"])
        },
        "services_detail": services_status,
        "avg_response_time": sum(s.get("response_time", 0) or 0 for s in services_status.values() if s.get("response_time")) / len([s for s in services_status.values() if s.get("response_time")])
    }
    
    return overview

@app.post("/api/services/{service_id}/control/{action}")
async def control_service_endpoint(service_id: str, action: str):
    """서비스 제어 API (start/stop/restart)"""
    if action not in ["start", "stop", "restart"]:
        raise HTTPException(status_code=400, detail="Invalid action. Use: start, stop, restart")
    
    result = await ServiceManager.control_service(service_id, action)
    return result

@app.get("/api/system/metrics")
async def get_system_metrics():
    """시스템 메트릭 API"""
    return await ServiceManager.get_system_metrics()

@app.get("/api/services/{service_id}/logs")
async def get_service_logs(service_id: str, lines: int = 100):
    """서비스 로그 조회 API"""
    if service_id not in CUBE_SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    try:
        # 서비스별 로그 파일 경로 (실제 환경에 맞게 조정)
        log_paths = {
            "crawling": "/var/log/heal7/crawling.log",
            "ai_dashboard": "/var/log/heal7/ai-dashboard.log",
            "paperwork": "/var/log/heal7/paperwork.log", 
            "saju": "/var/log/heal7/saju.log",
            "test_env": "/var/log/heal7/test-env.log"
        }
        
        # 시뮬레이션 로그 데이터 (실제로는 파일에서 읽어옴)
        import random
        sample_logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Service {service_id} is running normally",
            f"[{datetime.now().strftime('%H:%M:%S')}] DEBUG: Processing request #{random.randint(1000, 9999)}",
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Health check completed successfully",
            f"[{datetime.now().strftime('%H:%M:%S')}] WARN: High memory usage detected",
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Background task completed"
        ]
        
        return {"logs": sample_logs[-lines:], "service": service_id}
        
    except Exception as e:
        return {"error": str(e), "logs": []}

@app.get("/api/cube-architecture/assembly")
async def get_cube_assembly():
    """큐브 조립 패턴 조회"""
    # 시뮬레이션 데이터
    assembly_patterns = {
        "default_pattern": {
            "name": "기본 HEAL7 아키텍처",
            "cubes": ["ai_dashboard", "saju", "paperwork"],
            "connections": [
                {"from": "ai_dashboard", "to": "saju"},
                {"from": "ai_dashboard", "to": "paperwork"}
            ]
        },
        "data_processing": {
            "name": "데이터 처리 파이프라인",
            "cubes": ["crawling", "paperwork", "test_env"],
            "connections": [
                {"from": "crawling", "to": "paperwork"},
                {"from": "paperwork", "to": "test_env"}
            ]
        }
    }
    
    return assembly_patterns

@app.post("/api/cube-architecture/assembly")
async def save_cube_assembly(assembly_data: dict):
    """큐브 조립 패턴 저장"""
    try:
        # 실제로는 데이터베이스나 파일에 저장
        logger.info(f"큐브 조립 패턴 저장: {assembly_data}")
        return {"success": True, "message": "Assembly pattern saved successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/cube-architecture/validate")
async def validate_cube_assembly(assembly_data: dict):
    """큐브 조립 패턴 검증"""
    try:
        cubes = assembly_data.get("cubes", [])
        connections = assembly_data.get("connections", [])
        
        # 검증 로직
        validation_results = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # 큐브 호환성 검사
        for cube in cubes:
            if cube not in CUBE_SERVICES:
                validation_results["errors"].append(f"Unknown cube: {cube}")
                validation_results["valid"] = False
        
        # 연결 검증
        for conn in connections:
            if conn["from"] not in cubes or conn["to"] not in cubes:
                validation_results["warnings"].append(f"Invalid connection: {conn}")
        
        # 성능 제안
        if len(cubes) > 3:
            validation_results["suggestions"].append("많은 큐브 연결로 인한 성능 저하 가능성")
        
        return validation_results
        
    except Exception as e:
        return {"valid": False, "errors": [str(e)]}

@app.get("/api/cube-architecture/3d-data")
async def get_3d_cube_data():
    """3D 큐브 시각화 데이터"""
    cube_positions = {
        "crawling": {"x": -2, "y": 0, "z": 0, "color": 0xff6b35},
        "ai_dashboard": {"x": 0, "y": 2, "z": 0, "color": 0x4285f4},
        "saju": {"x": 2, "y": 0, "z": 0, "color": 0x9c27b0},
        "paperwork": {"x": 0, "y": -2, "z": 0, "color": 0x00c853},
        "test_env": {"x": 0, "y": 0, "z": 2, "color": 0xffc107}
    }
    
    return {"cube_positions": cube_positions, "connections": []}

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "management-dashboard",
        "version": "1.0"
    }

# 시작 이벤트
@app.on_event("startup")
async def startup_event():
    logger.info("🎛️ HEAL7 통합 관리 대시보드 시작!")
    logger.info(f"📍 URL: http://localhost:8008")
    logger.info(f"🎯 통합 관리: {len(CUBE_SERVICES)}개 서비스")
    logger.info(f"📋 API 문서: http://localhost:8008/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0",
        port=8008,
        reload=True,
        log_level="info"
    )