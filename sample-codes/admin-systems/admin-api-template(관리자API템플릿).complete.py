#!/usr/bin/env python3
"""
HEAL7 관리자 API 템플릿 (.complete)
복사-붙여넣기로 즉시 동작하는 완성 코드

기능: FastAPI 기반 관리자 API 서버 기본 구조
사용법: 이 파일을 복사하여 새로운 관리자 기능 구현 시 기본 템플릿으로 활용
"""

import asyncio
import logging
import sys
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="HEAL7 관리자 API",
    description="관리자 기능을 위한 API 서버",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.heal7.com", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 응답 모델 정의
class HealthResponse(BaseModel):
    status: str
    service: str
    port: int
    timestamp: str

class ApiResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: str

# 헬스 체크 엔드포인트
@app.get("/admin-api/health", response_model=HealthResponse)
async def health_check():
    """시스템 헬스 체크"""
    return HealthResponse(
        status="healthy",
        service="heal7-admin",
        port=8001,
        timestamp=datetime.now().isoformat()
    )

# 메인 페이지
@app.get("/")
async def root():
    """관리자 API 루트 페이지"""
    return {"message": "HEAL7 관리자 API 서버", "docs": "/docs"}

# 예외 처리 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ApiResponse(
            success=False,
            message="내부 서버 오류가 발생했습니다.",
            timestamp=datetime.now().isoformat()
        ).dict()
    )

# 인증 의존성 (예시)
async def verify_admin_token(request: Request):
    """관리자 토큰 검증"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 필요합니다."
        )
    
    token = authorization.split(" ")[1]
    # 실제 토큰 검증 로직 구현 필요
    if token != "valid_admin_token":  # 예시용 토큰
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )
    
    return {"user_id": "admin", "role": "admin"}

# 보호된 엔드포인트 예시
@app.get("/admin-api/protected", response_model=ApiResponse)
async def protected_endpoint(user: dict = Depends(verify_admin_token)):
    """인증이 필요한 관리자 엔드포인트"""
    return ApiResponse(
        success=True,
        data={"user": user, "access_granted": True},
        message="관리자 권한으로 접근 성공",
        timestamp=datetime.now().isoformat()
    )

# 데이터 처리 엔드포인트 예시
@app.post("/admin-api/data/process", response_model=ApiResponse)
async def process_data(
    data: Dict[str, Any],
    user: dict = Depends(verify_admin_token)
):
    """데이터 처리 엔드포인트"""
    try:
        # 데이터 처리 로직
        processed_data = {
            "input": data,
            "processed_by": user["user_id"],
            "processed_at": datetime.now().isoformat(),
            "result": "success"
        }
        
        logger.info(f"Data processed by {user['user_id']}")
        
        return ApiResponse(
            success=True,
            data=processed_data,
            message="데이터 처리 완료",
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Data processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터 처리 중 오류가 발생했습니다."
        )

# 관리자 설정 엔드포인트
@app.get("/admin-api/settings", response_model=ApiResponse)
async def get_admin_settings(user: dict = Depends(verify_admin_token)):
    """관리자 설정 조회"""
    settings = {
        "system_name": "HEAL7",
        "version": "5.0.0",
        "features": ["사주", "키워드", "설문", "백업"],
        "maintenance_mode": False,
        "last_updated": datetime.now().isoformat()
    }
    
    return ApiResponse(
        success=True,
        data=settings,
        message="관리자 설정 조회 성공",
        timestamp=datetime.now().isoformat()
    )

@app.put("/admin-api/settings", response_model=ApiResponse)
async def update_admin_settings(
    settings: Dict[str, Any],
    user: dict = Depends(verify_admin_token)
):
    """관리자 설정 업데이트"""
    # 설정 업데이트 로직
    updated_settings = {
        **settings,
        "updated_by": user["user_id"],
        "updated_at": datetime.now().isoformat()
    }
    
    logger.info(f"Settings updated by {user['user_id']}")
    
    return ApiResponse(
        success=True,
        data=updated_settings,
        message="설정 업데이트 완료",
        timestamp=datetime.now().isoformat()
    )

# 시스템 상태 모니터링
@app.get("/admin-api/system/status", response_model=ApiResponse)
async def get_system_status(user: dict = Depends(verify_admin_token)):
    """시스템 상태 조회"""
    import psutil
    
    system_status = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "uptime": datetime.now().isoformat(),
        "active_connections": len(psutil.net_connections()),
        "process_count": len(psutil.pids())
    }
    
    return ApiResponse(
        success=True,
        data=system_status,
        message="시스템 상태 조회 성공",
        timestamp=datetime.now().isoformat()
    )

# 로그 조회 엔드포인트
@app.get("/admin-api/logs", response_model=ApiResponse)
async def get_logs(
    limit: int = 100,
    level: str = "INFO",
    user: dict = Depends(verify_admin_token)
):
    """시스템 로그 조회"""
    # 실제 로그 파일 읽기 로직 구현 필요
    sample_logs = [
        {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": "샘플 로그 메시지",
            "module": "admin_api"
        }
        for _ in range(min(limit, 10))
    ]
    
    return ApiResponse(
        success=True,
        data={"logs": sample_logs, "count": len(sample_logs)},
        message=f"로그 {len(sample_logs)}개 조회 완료",
        timestamp=datetime.now().isoformat()
    )

# 서버 실행부
if __name__ == "__main__":
    uvicorn.run(
        "admin-api-template:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        workers=1,
        log_level="info"
    )

"""
사용법:

1. 기본 사용:
   python admin-api-template.complete.py

2. 개발 모드:
   uvicorn admin-api-template:app --reload --port 8001

3. 프로덕션 배포:
   uvicorn admin-api-template:app --host 0.0.0.0 --port 8001 --workers 4

4. 커스터마이징:
   - verify_admin_token() 함수에 실제 JWT 토큰 검증 로직 구현
   - 데이터베이스 연결 및 모델 추가
   - 비즈니스 로직에 맞는 엔드포인트 추가
   - 로깅 및 모니터링 강화

5. 의존성:
   pip install fastapi uvicorn python-multipart psutil

6. API 문서:
   http://localhost:8001/docs (Swagger UI)
   http://localhost:8001/redoc (ReDoc)
"""