#!/usr/bin/env python3
"""
HEAL7 PERFORMANCE-MONITOR-SYSTEM 큐브
성능 모니터링 및 메트릭

생체 모방: 신경계 - 상태 감지
Color: PURPLE
Port: 8050
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import yaml
from pathlib import Path

# 큐브 설정 로드
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, 'r', encoding='utf-8') as f:
    cube_config = yaml.safe_load(f)

# FastAPI 앱 생성
app = FastAPI(
    title=f"HEAL7 Performance-Monitor-System",
    description=cube_config["cube"]["purpose"],
    version=cube_config["cube"]["version"],
    docs_url=f"/api/performance-monitor/docs"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "cube": cube_config["cube"]["name"],
        "color": cube_config["cube"]["color"],
        "purpose": cube_config["cube"]["purpose"],
        "port": cube_config["cube"]["port"]
    }

@app.get("/api/performance-monitor/status")
async def get_status():
    """큐브 상태 조회"""
    return {
        "cube_name": cube_config["cube"]["name"],
        "type": cube_config["cube"]["type"], 
        "color": cube_config["cube"]["color"],
        "metaphor": cube_config["cube"]["metaphor"],
        "interfaces": cube_config["interfaces"],
        "performance_targets": cube_config["performance_targets"]
    }

# 큐브별 특화 라우터 추가 지점
# TODO: 마이그레이션된 모듈들의 라우터를 여기에 포함

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=cube_config["cube"]["port"],
        reload=True
    )
