"""
Health Check Router
사주 서비스 상태 확인 엔드포인트
"""
from fastapi import APIRouter
import yaml
from pathlib import Path

# 설정 로드
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": config["service"]["name"],
        "purpose": config["service"]["purpose"], 
        "port": config["service"]["port"],
        "functions": config["service"]["functions"]
    }

@router.get("/info")
async def service_info():
    """서비스 정보 엔드포인트"""
    return {
        "service": config["service"]["name"],
        "purpose": config["service"]["purpose"],
        "functions": config["service"]["functions"],
        "version": config["service"]["version"],
        "api_docs": f"http://localhost:{config['server']['port']}/docs"
    }

@router.get("/api/health")
async def health_endpoint():
    """API 헬스체크 엔드포인트 (호환성)"""
    return {
        "status": "healthy",
        "service": config["service"]["name"],
        "timestamp": "2025-09-06T09:46:00Z"
    }