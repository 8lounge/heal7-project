"""
HEAL7 database-manager-system 큐브 테스트
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """헬스 체크 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["cube"] == "database-manager-system"

def test_status_endpoint():
    """상태 조회 테스트"""
    response = client.get("/api/database-manager/status")
    assert response.status_code == 200
    data = response.json()
    assert data["cube_name"] == "database-manager-system"
    assert data["color"] == "yellow"

def test_performance_targets():
    """성능 목표 검증"""
    # 응답 시간 테스트
    import time
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()
    
    response_time_ms = (end_time - start_time) * 1000
    assert response_time_ms < 100  # 100ms 이내
    assert response.status_code == 200

# TODO: 큐브별 특화 테스트 추가
