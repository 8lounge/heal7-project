#!/bin/bash

# ====================================
# HEAL7 서비스 자동 배포 스크립트
# 
# GitHub Actions 빌드 결과물을 받아서
# 실제 서비스를 무중단으로 배포
# ====================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 설정
PROJECT_ROOT="/home/ubuntu/heal7-project"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
SERVICES_DIR="$BACKEND_DIR/services"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 서비스 포트 매핑 (순서대로 8001~8005)
declare -A SERVICE_PORTS=(
    ["paperwork-service"]="8001"
    ["saju-service"]="8002"
    ["crawling-service"]="8003"
    ["ai-monitoring-service"]="8004"
    ["dashboard-service"]="8005"
)

# 로깅 함수
log() {
    echo -e "$(date '+%H:%M:%S') $1"
}

log_info() {
    log "${BLUE}[INFO]${NC} $1"
}

log_success() {
    log "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    log "${RED}[ERROR]${NC} $1"
}

log_warning() {
    log "${YELLOW}[WARNING]${NC} $1"
}

# 서비스 상태 확인
check_service_health() {
    local service_name="$1"
    local port="${SERVICE_PORTS[$service_name]}"
    local max_attempts=30
    local attempt=1

    log_info "$service_name 헬스체크 시작 (포트: $port)"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -sf "http://localhost:$port/health" >/dev/null 2>&1 || \
           curl -sf "http://localhost:$port/" >/dev/null 2>&1; then
            log_success "$service_name 헬스체크 성공 ($attempt/$max_attempts)"
            return 0
        fi
        
        log_info "헬스체크 대기 중... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    log_error "$service_name 헬스체크 실패"
    return 1
}

# 기존 서비스 종료
stop_service() {
    local service_name="$1"
    local port="${SERVICE_PORTS[$service_name]}"
    
    log_info "$service_name 서비스 종료 중 (포트: $port)"
    
    # 포트 사용 프로세스 찾기 및 종료
    local pids=$(sudo lsof -ti:$port 2>/dev/null || echo "")
    if [ -n "$pids" ]; then
        echo "$pids" | xargs -r sudo kill -TERM
        sleep 3
        # 강제 종료가 필요한 경우
        pids=$(sudo lsof -ti:$port 2>/dev/null || echo "")
        if [ -n "$pids" ]; then
            echo "$pids" | xargs -r sudo kill -KILL
            log_warning "$service_name 강제 종료됨"
        else
            log_success "$service_name 정상 종료됨"
        fi
    else
        log_info "$service_name 이미 종료된 상태"
    fi
}

# 서비스 시작
start_service() {
    local service_name="$1"
    local port="${SERVICE_PORTS[$service_name]}"
    local service_dir="$SERVICES_DIR/$service_name"
    
    log_info "$service_name 서비스 시작 중 (포트: $port)"
    
    if [ ! -d "$service_dir" ]; then
        log_error "$service_name 디렉터리가 존재하지 않습니다: $service_dir"
        return 1
    fi
    
    cd "$service_dir"
    
    # 의존성 확인
    if [ -f "requirements.txt" ]; then
        log_info "$service_name 의존성 설치 중..."
        python3 -m pip install --user -r requirements.txt >/dev/null 2>&1 || {
            log_warning "$service_name 의존성 설치 중 일부 오류 발생 (계속 진행)"
        }
    fi
    
    # 서비스 시작 (uvicorn 사용)
    local log_file="/home/ubuntu/logs/${service_name}_${TIMESTAMP}.log"
    mkdir -p /home/ubuntu/logs
    
    # config.yaml에서 포트 읽기
    local port=$(python3 -c "import yaml; print(yaml.safe_load(open('config.yaml'))['server']['port'])")
    
    log_info "$service_name uvicorn으로 백그라운드 실행 시작..."
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port $port > "$log_file" 2>&1 &
    local pid=$!
    
    # PID 저장
    echo $pid > "/tmp/${service_name}.pid"
    log_success "$service_name 시작됨 (PID: $pid, 로그: $log_file)"
    
    sleep 2
    return 0
}

# 무중단 배포 실행
deploy_service() {
    local service_name="$1"
    
    log_info "🚀 $service_name 무중단 배포 시작"
    
    # 1. 기존 서비스 종료
    stop_service "$service_name"
    
    # 2. 새 서비스 시작
    if start_service "$service_name"; then
        # 3. 헬스체크
        if check_service_health "$service_name"; then
            log_success "✅ $service_name 배포 완료"
            return 0
        else
            log_error "❌ $service_name 헬스체크 실패 - 롤백 필요"
            return 1
        fi
    else
        log_error "❌ $service_name 시작 실패"
        return 1
    fi
}

# 전체 백엔드 서비스 배포
deploy_all_backend() {
    log_info "🎼 전체 백엔드 서비스 배포 시작"
    
    local failed_services=()
    
    for service_name in "${!SERVICE_PORTS[@]}"; do
        log_info "=== $service_name 배포 중 ==="
        if ! deploy_service "$service_name"; then
            failed_services+=("$service_name")
            log_error "$service_name 배포 실패"
        fi
        echo ""
    done
    
    # 결과 요약
    if [ ${#failed_services[@]} -eq 0 ]; then
        log_success "🎉 모든 백엔드 서비스 배포 성공!"
    else
        log_error "❌ 실패한 서비스: ${failed_services[*]}"
        return 1
    fi
}

# 프론트엔드 배포
deploy_frontend() {
    log_info "🎨 프론트엔드 배포 시작"
    
    cd "$FRONTEND_DIR"
    
    # 기존 프리뷰 서버 종료
    local pids=$(sudo lsof -ti:4173 2>/dev/null || echo "")
    if [ -n "$pids" ]; then
        echo "$pids" | xargs -r sudo kill -TERM
        sleep 2
        log_info "기존 프론트엔드 서버 종료됨"
    fi
    
    # 빌드 및 시작
    log_info "프론트엔드 빌드 중..."
    if npm run build >/dev/null 2>&1; then
        log_success "프론트엔드 빌드 완료"
    else
        log_error "프론트엔드 빌드 실패"
        return 1
    fi
    
    # 프리뷰 서버 시작
    log_info "프론트엔드 프리뷰 서버 시작 중..."
    nohup npm run preview > "/home/ubuntu/logs/frontend_${TIMESTAMP}.log" 2>&1 &
    local pid=$!
    echo $pid > "/tmp/frontend.pid"
    
    sleep 3
    
    # 헬스체크
    if curl -sf "http://localhost:4173" >/dev/null 2>&1; then
        log_success "✅ 프론트엔드 배포 완료 (PID: $pid)"
        return 0
    else
        log_error "❌ 프론트엔드 헬스체크 실패"
        return 1
    fi
}

# 배포 상태 확인
check_deployment_status() {
    log_info "🔍 배포 상태 확인"
    
    echo "=== 서비스 상태 ==="
    # 프론트엔드
    if curl -sf "http://localhost:4173" >/dev/null 2>&1; then
        echo "✅ Frontend (4173): 정상"
    else
        echo "❌ Frontend (4173): 오류"
    fi
    
    # 백엔드 서비스들
    for service_name in "${!SERVICE_PORTS[@]}"; do
        local port="${SERVICE_PORTS[$service_name]}"
        if curl -sf "http://localhost:$port" >/dev/null 2>&1 || \
           curl -sf "http://localhost:$port/health" >/dev/null 2>&1; then
            echo "✅ $service_name ($port): 정상"
        else
            echo "❌ $service_name ($port): 오류"
        fi
    done
    
    echo ""
    echo "=== 프로세스 현황 ==="
    ps aux | grep -E "(python3 main.py|npm.*preview)" | grep -v grep || echo "실행 중인 서비스 없음"
}

# 메인 실행 함수
main() {
    local command="${1:-all}"
    
    log_info "🏠 HEAL7 서비스 배포 시작 ($command)"
    log_info "시작 시간: $(date)"
    
    case "$command" in
        "all")
            deploy_frontend
            deploy_all_backend
            ;;
        "frontend")
            deploy_frontend
            ;;
        "backend")
            deploy_all_backend
            ;;
        "saju-service"|"crawling-service"|"paperwork-service"|"ai-monitoring-service"|"dashboard-service")
            deploy_service "$command"
            ;;
        "status")
            check_deployment_status
            ;;
        "stop-all")
            # 모든 서비스 종료
            log_info "전체 서비스 종료 중..."
            for service_name in "${!SERVICE_PORTS[@]}"; do
                stop_service "$service_name"
            done
            # 프론트엔드도 종료
            local pids=$(sudo lsof -ti:4173 2>/dev/null || echo "")
            [ -n "$pids" ] && echo "$pids" | xargs -r sudo kill -TERM
            ;;
        *)
            echo "사용법: $0 [all|frontend|backend|service-name|status|stop-all]"
            echo "서비스: saju-service, crawling-service, paperwork-service, ai-monitoring-service, dashboard-service"
            exit 1
            ;;
    esac
    
    echo ""
    log_info "배포 완료 시간: $(date)"
    log_info "상태 확인: $0 status"
}

# 실행
main "$@"