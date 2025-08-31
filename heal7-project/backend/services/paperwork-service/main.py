#!/usr/bin/env python3
"""
HEAL7 Paperwork Service
AI 기반 서류 자동 처리

포트: 8010
기능: ocr, ai_analysis, document_generation, classification
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml
from pathlib import Path

# 설정 로드
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# FastAPI 앱 생성
app = FastAPI(
    title=config["api"]["title"],
    version=config["service"]["version"], 
    docs_url=config["api"]["docs_url"],
    redoc_url=config["api"]["redoc_url"]
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
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": config["service"]["name"],
        "purpose": config["service"]["purpose"], 
        "port": config["service"]["port"],
        "functions": config["service"]["functions"]
    }

@app.get("/info")
async def service_info():
    """서비스 정보 엔드포인트"""
    return {
        "service": config["service"]["name"],
        "purpose": config["service"]["purpose"],
        "functions": config["service"]["functions"],
        "version": config["service"]["version"],
        "api_docs": f"http://localhost:{config['server']['port']}/docs"
    }

# 기능별 라우터 등록 (추후 구현)
# from ocr.routes import router as ocr_router
# app.include_router(ocr_router, prefix="/ocr", tags=["ocr"])
# from ai_analysis.routes import router as ai_analysis_router
# app.include_router(ai_analysis_router, prefix="/ai_analysis", tags=["ai_analysis"])
# from document_generation.routes import router as document_generation_router
# app.include_router(document_generation_router, prefix="/document_generation", tags=["document_generation"])
# from classification.routes import router as classification_router
# app.include_router(classification_router, prefix="/classification", tags=["classification"])

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 {config['service']['name']} 시작...")
    print(f"📖 API 문서: http://localhost:{config['server']['port']}/docs")
    
    uvicorn.run(
        "main:app",
        host=config["server"]["host"],
        port=config["server"]["port"], 
        workers=config["server"]["workers"],
        reload=config["server"]["reload"]
    )
