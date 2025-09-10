#!/usr/bin/env python3
"""
HEAL7 Saju Service - Refactored
사주명리학 계산 및 해석 - 모듈화된 버전

포트: 8002
기능: saju_calculation, myeongrihak_analysis, dream_interpretation, fortune_reading
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml
from pathlib import Path
from datetime import datetime
import sys

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

# 라우터 Import 및 등록
try:
    from routers.health_router import router as health_router
    app.include_router(health_router)
    print("✅ Health router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import health router: {e}")

try:
    from routers.saju_router import router as saju_router
    app.include_router(saju_router)
    print("✅ Saju router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import saju router: {e}")

try:
    from routers.kasi_router import router as kasi_router
    app.include_router(kasi_router)
    print("✅ KASI router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import kasi router: {e}")

# 인증 라우터 (기존 유지)
try:
    from auth import router as auth_router
    app.include_router(auth_router)
    print("✅ Auth router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import auth router: {e}")

# 꿈풀이 라우터 (메인 백엔드의 작동하는 라우터 사용)
sys.path.append("/home/ubuntu/heal7-project/backend/app/routers")

try:
    from dream_interpretation import router as dream_saju_router
    app.include_router(dream_saju_router)
    print("✅ Dream interpretation router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import dream router: {e}")

try:
    from dream_interpretation_advanced import router as advanced_dream_router
    app.include_router(advanced_dream_router)
    print("✅ Advanced dream interpretation router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import advanced dream router: {e}")

try:
    from routers.weather import router as weather_router
    app.include_router(weather_router)
    print("✅ Weather router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import weather router: {e}")

# 메인 백엔드의 사주 서비스 로직 추가 (필요한 경우)
sys.path.append(str(Path(__file__).parent.parent / "app"))

# 사주 관리자 라우터 추가
try:
    # 메인 백엔드의 routers 경로에서 import
    import sys
    sys.path.append("/home/ubuntu/heal7-project/backend/app/routers")
    from saju_admin import router as admin_router
    app.include_router(admin_router)
    print("✅ Saju admin router loaded successfully")
except ImportError as e:
    print(f"⚠️ WARNING: Could not import saju admin router: {e}")

# TODO: 나머지 라우터들 (point-cash, customer, community, interpretation 등)
# 현재는 기존 main.py에 남겨두고 점진적으로 분리 예정

print(f"🚀 {config['service']['name']} (모듈화 버전) 시작...")
print(f"📖 API 문서: http://localhost:{config['server']['port']}/docs")
print(f"📦 분리된 라우터: health, saju, kasi + 기존 auth, dream")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config["server"]["host"],
        port=config["server"]["port"], 
        workers=config["server"]["workers"],
        reload=config["server"]["reload"]
    )