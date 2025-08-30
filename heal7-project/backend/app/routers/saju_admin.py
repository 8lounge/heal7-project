"""
HEAL7 사주명리학 관리자 API
사주 계산 로직의 모든 설정을 관리하는 관리자 전용 API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path

# 실제 사주 admin 설정 시스템 연동 - 하드코딩 제거 완료
try:
    from ..core.config.saju_admin_settings import (
        SajuAdminSettings,
        get_admin_settings as get_real_admin_settings,
        update_admin_settings
    )
except ImportError:
    # 상대경로 임포트 실패 시 절대경로로 시도
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core', 'config'))
    from saju_admin_settings import (
        SajuAdminSettings,
        get_admin_settings as get_real_admin_settings,
        update_admin_settings
    )
from datetime import datetime

def get_admin_settings():
    """실제 사주 관리자 설정 반환 (하드코딩 제거)"""
    return get_real_admin_settings()

router = APIRouter(prefix="/admin/saju", tags=["사주 관리자"])
security = HTTPBearer()

# 설정 파일 경로
SETTINGS_FILE_PATH = "/home/ubuntu/heal7-project/backend/data/saju_admin_settings.json"

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """관리자 토큰 검증 (임시로 간단한 토큰 체크)"""
    # 실제 환경에서는 JWT 토큰 검증 등 보안 로직 구현 필요
    if credentials.credentials != "heal7-admin-2025":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token"
        )
    return credentials.credentials

# --- 전체 설정 관리 ---

@router.get("/settings", summary="전체 사주 관리자 설정 조회")
async def get_all_settings(token: str = Depends(verify_admin_token)):
    """전체 사주 관리자 설정을 조회합니다."""
    try:
        # 실제 설정 반환 (하드코딩 제거)
        settings = get_admin_settings()
        
        # 딕셔너리 형태로 변환하여 API 응답
        if hasattr(settings, 'dict'):
            return settings.dict()
        else:
            # 기존 방식 호환성 유지
            return {
                "version": getattr(settings, 'version', '5.0.0'),
                "last_updated": getattr(settings, 'last_updated', datetime.now().isoformat()),
                "updated_by": getattr(settings, 'updated_by', 'admin'),
                "time_settings": getattr(settings, 'time_settings', {}),
                "logic_settings": getattr(settings, 'logic_settings', {}),
                "geographic_settings": getattr(settings, 'geographic_settings', {}),
                "kasi_settings": getattr(settings, 'kasi_settings', {}),
                "cheongan_interpretations": getattr(settings, 'cheongan_interpretations', {}),
                "jiji_interpretations": getattr(settings, 'jiji_interpretations', {}),
                "gapja_interpretations": getattr(settings, 'gapja_interpretations', {})
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 조회 실패: {str(e)}")

@router.post("/settings", summary="전체 사주 관리자 설정 저장")
async def save_all_settings(
    settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """전체 사주 관리자 설정을 저장합니다."""
    try:
        # 데이터 디렉토리 생성
        os.makedirs(os.path.dirname(SETTINGS_FILE_PATH), exist_ok=True)
        
        # 실제 설정 인스턴스가 아닌 경우 변환 필요
        if not isinstance(settings, SajuAdminSettings):
            settings = SajuAdminSettings(**settings)
        
        # 파일로 저장
        settings.save_to_file(SETTINGS_FILE_PATH)
        
        # 메모리에도 업데이트
        update_admin_settings(settings)
        
        return {"message": "설정이 성공적으로 저장되었습니다.", "file_path": SETTINGS_FILE_PATH}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 저장 실패: {str(e)}")

# --- 개별 설정 섹션 관리 ---

@router.get("/settings/time", summary="시간 설정 조회")
async def get_time_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """시간 관련 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.time_settings

@router.put("/settings/time", summary="시간 설정 업데이트")
async def update_time_settings(
    time_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """시간 관련 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.time_settings = time_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "시간 설정이 업데이트되었습니다."}

@router.get("/settings/geographic", summary="지리적 설정 조회") 
async def get_geographic_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """지리적 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.geographic_settings

@router.put("/settings/geographic", summary="지리적 설정 업데이트")
async def update_geographic_settings(
    geographic_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """지리적 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.geographic_settings = geographic_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "지리적 설정이 업데이트되었습니다."}

@router.get("/settings/logic", summary="사주 로직 설정 조회")
async def get_logic_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """사주 로직 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.logic_settings

@router.put("/settings/logic", summary="사주 로직 설정 업데이트")
async def update_logic_settings(
    logic_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """사주 로직 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.logic_settings = logic_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "사주 로직 설정이 업데이트되었습니다."}

@router.get("/settings/kasi", summary="KASI 설정 조회")
async def get_kasi_settings(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """KASI API 설정을 조회합니다."""
    settings = get_admin_settings()
    return settings.kasi_settings

@router.put("/settings/kasi", summary="KASI 설정 업데이트")
async def update_kasi_settings(
    kasi_settings: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """KASI API 설정을 업데이트합니다."""
    settings = get_admin_settings()
    settings.kasi_settings = kasi_settings
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": "KASI 설정이 업데이트되었습니다."}

# --- 해석 데이터 관리 ---

@router.get("/interpretations/cheongan", summary="천간 해석 조회")
async def get_cheongan_interpretations(
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """천간 해석 데이터를 조회합니다."""
    settings = get_admin_settings()
    return settings.cheongan_interpretations

@router.put("/interpretations/cheongan/{cheongan_name}", summary="천간 해석 업데이트")
async def update_cheongan_interpretation(
    cheongan_name: str,
    interpretation: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 천간의 해석을 업데이트합니다."""
    settings = get_admin_settings()
    settings.cheongan_interpretations[cheongan_name] = interpretation
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": f"천간 '{cheongan_name}' 해석이 업데이트되었습니다."}

@router.delete("/interpretations/cheongan/{cheongan_name}", summary="천간 해석 삭제")
async def delete_cheongan_interpretation(
    cheongan_name: str,
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 천간의 해석을 삭제합니다."""
    settings = get_admin_settings()
    if cheongan_name in settings.cheongan_interpretations:
        del settings.cheongan_interpretations[cheongan_name]
        settings.save_to_file(SETTINGS_FILE_PATH)
        return {"message": f"천간 '{cheongan_name}' 해석이 삭제되었습니다."}
    else:
        raise HTTPException(status_code=404, detail=f"천간 '{cheongan_name}'을 찾을 수 없습니다.")

@router.get("/interpretations/jiji", summary="지지 해석 조회")
async def get_jiji_interpretations(
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """지지 해석 데이터를 조회합니다."""
    settings = get_admin_settings()
    return settings.jiji_interpretations

@router.put("/interpretations/jiji/{jiji_name}", summary="지지 해석 업데이트")
async def update_jiji_interpretation(
    jiji_name: str,
    interpretation: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 지지의 해석을 업데이트합니다."""
    settings = get_admin_settings()
    settings.jiji_interpretations[jiji_name] = interpretation
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": f"지지 '{jiji_name}' 해석이 업데이트되었습니다."}

@router.get("/interpretations/gapja", summary="60갑자 해석 조회")
async def get_gapja_interpretations(
    token: str = Depends(verify_admin_token)
) -> Dict[str, Any]:
    """60갑자 해석 데이터를 조회합니다."""
    settings = get_admin_settings()
    return settings.gapja_interpretations

@router.put("/interpretations/gapja/{gapja_name}", summary="60갑자 해석 업데이트")
async def update_gapja_interpretation(
    gapja_name: str,
    interpretation: Dict[str, Any],
    token: str = Depends(verify_admin_token)
) -> Dict[str, str]:
    """특정 60갑자의 해석을 업데이트합니다."""
    settings = get_admin_settings()
    settings.gapja_interpretations[gapja_name] = interpretation
    settings.save_to_file(SETTINGS_FILE_PATH)
    return {"message": f"60갑자 '{gapja_name}' 해석이 업데이트되었습니다."}

# --- 시스템 상태 조회 ---

@router.get("/status", summary="사주 시스템 상태 조회")
async def get_system_status(token: str = Depends(verify_admin_token)) -> Dict[str, Any]:
    """사주 계산 시스템의 현재 상태를 조회합니다."""
    settings = get_admin_settings()
    
    return {
        "version": settings.version,
        "last_updated": settings.last_updated,
        "updated_by": settings.updated_by,
        "settings_file_exists": os.path.exists(SETTINGS_FILE_PATH),
        "settings_file_path": SETTINGS_FILE_PATH,
        "current_config": {
            "timezone_system": getattr(settings.time_settings, 'timezone_system', 'standard'),
            "logic_type": getattr(settings.logic_settings, 'logic_type', 'hybrid'),
            "default_country": getattr(settings.geographic_settings, 'default_country', 'KR'),
            "use_kasi_precision": getattr(settings.logic_settings, 'use_kasi_precision', True),
            "manseeryeok_count": getattr(settings.logic_settings, 'manseeryeok_count', 60000),
            "cheongan_count": len(settings.cheongan_interpretations) if settings.cheongan_interpretations else 0,
            "jiji_count": len(settings.jiji_interpretations) if settings.jiji_interpretations else 0,
            "gapja_count": len(settings.gapja_interpretations) if settings.gapja_interpretations else 0
        }
    }

# --- 데이터 초기화 및 백업 ---

@router.post("/initialize", summary="기본 설정 데이터 초기화")
async def initialize_default_settings(token: str = Depends(verify_admin_token)) -> Dict[str, str]:
    """기본 설정 데이터로 초기화합니다."""
    try:
        # 기본 설정 생성
        settings = get_admin_settings()
        
        # 파일로 저장
        settings.save_to_file(SETTINGS_FILE_PATH)
        
        return {"message": "기본 설정으로 초기화가 완료되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"초기화 실패: {str(e)}")

@router.post("/backup", summary="현재 설정 백업")
async def backup_current_settings(token: str = Depends(verify_admin_token)) -> Dict[str, str]:
    """현재 설정을 백업합니다."""
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"/home/ubuntu/heal7-project/backend/data/backup/saju_settings_{timestamp}.json"
        
        # 백업 디렉토리 생성
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        settings = get_admin_settings()
        settings.save_to_file(backup_path)
        
        return {"message": "설정이 백업되었습니다.", "backup_path": backup_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"백업 실패: {str(e)}")