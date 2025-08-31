#!/bin/bash
# HEAL7 서비스 오케스트레이션 시작 스크립트

echo "🎼 HEAL7 서비스 오케스트레이션 시작..."

# 1. 오케스트레이션 허브 시작 (포트 8015)
echo "🚀 오케스트레이션 허브 시작..."
cd services/dashboard-service
python main.py &
ORCHESTRATOR_PID=$!

# 허브 시작 대기
sleep 5

# 2. 오케스트레이션을 통한 서비스 자동 시작
echo "🔧 관리 서비스들 자동 시작..."
curl -X POST http://localhost:8015/orchestration/start-all

echo "✅ HEAL7 오케스트레이션 시스템 준비 완료"
echo "🌐 오케스트레이션 대시보드: http://localhost:8015/dashboard"
echo "📊 서비스 상태: http://localhost:8015/orchestration/status"

echo "오케스트레이터 PID: $ORCHESTRATOR_PID"
