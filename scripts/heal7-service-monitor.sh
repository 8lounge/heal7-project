#!/bin/bash
# HEAL7 서비스 자동 모니터링 및 재시작 스크립트
# 작성일: 2025-08-29
# 용도: 중요 서비스들의 상태를 모니터링하고 필요시 자동 재시작

LOG_FILE="/var/log/heal7-monitor.log"
HEAL7_BACKEND_DIR="/home/ubuntu/heal7-project/backend"
DASHBOARD_SERVICE_DIR="/home/ubuntu/heal7-project/backend/services/dashboard-service"

# 로그 함수
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 포트에서 실행 중인 프로세스 확인
check_port() {
    local port=$1
    lsof -i ":$port" > /dev/null 2>&1
    return $?
}

# 서비스 재시작 함수
restart_saju_service() {
    log "🔄 사주 서비스 (포트 8003) 재시작 중..."
    cd "$HEAL7_BACKEND_DIR/services/saju-service" || return 1
    nohup python3 main.py > /dev/null 2>&1 &
    sleep 3
    if check_port 8003; then
        log "✅ 사주 서비스 재시작 성공"
        return 0
    else
        log "❌ 사주 서비스 재시작 실패"
        return 1
    fi
}

restart_dashboard_service() {
    log "🔄 관리자 서비스 (포트 8006) 재시작 중..."
    cd "$DASHBOARD_SERVICE_DIR" || return 1
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8006 > /dev/null 2>&1 &
    sleep 3
    if check_port 8006; then
        log "✅ 관리자 서비스 재시작 성공"
        return 0
    else
        log "❌ 관리자 서비스 재시작 실패"
        return 1
    fi
}

# 메인 모니터링 로직
main() {
    log "🔍 HEAL7 서비스 상태 점검 시작"
    
    local restart_needed=false
    
    # 사주 서비스 (포트 8003) 점검
    if ! check_port 8003; then
        log "⚠️ 사주 서비스가 중단되었습니다."
        restart_saju_service
        restart_needed=true
    else
        log "✅ 사주 서비스 정상 (포트 8003)"
    fi
    
    # 관리자 서비스 (포트 8006) 점검
    if ! check_port 8006; then
        log "⚠️ 관리자 서비스가 중단되었습니다."
        restart_dashboard_service
        restart_needed=true
    else
        log "✅ 관리자 서비스 정상 (포트 8006)"
    fi
    
    # Nginx 상태 점검
    if ! systemctl is-active --quiet nginx; then
        log "⚠️ Nginx가 중단되었습니다. 재시작 중..."
        sudo systemctl restart nginx
        if systemctl is-active --quiet nginx; then
            log "✅ Nginx 재시작 성공"
            restart_needed=true
        else
            log "❌ Nginx 재시작 실패"
        fi
    else
        log "✅ Nginx 정상"
    fi
    
    if [ "$restart_needed" = false ]; then
        log "🎉 모든 서비스가 정상적으로 실행 중입니다."
    fi
    
    log "📊 점검 완료\n"
}

# 사용법 출력
usage() {
    echo "사용법: $0 [옵션]"
    echo "옵션:"
    echo "  --once     한 번만 실행"
    echo "  --monitor  지속적 모니터링 (30초 간격)"
    echo "  --status   현재 서비스 상태만 확인"
    echo "  --help     도움말 출력"
}

# 상태만 확인하는 함수
check_status() {
    echo "🔍 HEAL7 서비스 상태 확인"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if check_port 8003; then
        echo "✅ 사주 서비스 (포트 8003): 실행 중"
    else
        echo "❌ 사주 서비스 (포트 8003): 중단됨"
    fi
    
    if check_port 8006; then
        echo "✅ 관리자 서비스 (포트 8006): 실행 중"
    else
        echo "❌ 관리자 서비스 (포트 8006): 중단됨"
    fi
    
    if systemctl is-active --quiet nginx; then
        echo "✅ Nginx: 실행 중"
    else
        echo "❌ Nginx: 중단됨"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 인자 처리
case "${1:-}" in
    --once)
        main
        ;;
    --monitor)
        log "🚀 HEAL7 서비스 모니터링 시작 (30초 간격)"
        while true; do
            main
            sleep 30
        done
        ;;
    --status)
        check_status
        ;;
    --help)
        usage
        ;;
    *)
        echo "기본 모드: 한 번 실행"
        main
        ;;
esac