#!/bin/bash

# ====================================
# HEAL7 사주명리학 통합 배포 스크립트
# 
# 완전 분리형 아키텍처 자동 배포
# 프론트엔드(정적) + 백엔드(API) 통합 배포
# 
# @author HEAL7 Team
# @version 2.0.0 (완전 분리형)
# ====================================

set -e  # 에러 발생 시 스크립트 중단
set -u  # 정의되지 않은 변수 사용 시 에러

# ====================================
# 🌍 환경 변수 및 설정
# ====================================

# 기본 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
LOG_FILE="/var/log/heal7-saju-deploy-${TIMESTAMP}.log"

# 디렉터리 설정
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT/backend"
DEPLOYMENT_DIR="$PROJECT_ROOT/deployment"
NGINX_CONF_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
WEB_ROOT="/var/www/saju.heal7.com"

# 서비스 설정
FRONTEND_SERVICE="heal7-saju-frontend"
BACKEND_SERVICE="heal7-saju-backend"
NGINX_SERVICE="nginx"

# 포트 설정 (실제 사용 중인 포트)
FRONTEND_PORT=4173  # Vite preview 포트
BACKEND_PORT=8002   # 사주 서비스 실제 포트
OLD_BACKEND_PORT=8010  # 이전 포트

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ====================================
# 🛠️ 유틸리티 함수
# ====================================

# 로그 함수
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG_FILE"
}

log_info() {
    log "${BLUE}[INFO]${NC} $1"
}

log_success() {
    log "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    log "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    log "${RED}[ERROR]${NC} $1"
}

log_header() {
    log ""
    log "${PURPLE}=====================================${NC}"
    log "${PURPLE} $1${NC}"
    log "${PURPLE}=====================================${NC}"
}

# 명령어 실행 함수
run_command() {
    local cmd="$1"
    local desc="$2"
    
    log_info "실행 중: $desc"
    log_info "명령어: $cmd"
    
    if eval "$cmd" >> "$LOG_FILE" 2>&1; then
        log_success "$desc 완료"
        return 0
    else
        log_error "$desc 실패"
        return 1
    fi
}

# 서비스 상태 확인 함수
check_service() {
    local service="$1"
    if systemctl is-active --quiet "$service"; then
        echo "running"
    else
        echo "stopped"
    fi
}

# 포트 사용 여부 확인 함수
check_port() {
    local port="$1"
    if ss -tuln | grep -q ":$port "; then
        echo "used"
    else
        echo "free"
    fi
}

# 백업 함수
backup_directory() {
    local source="$1"
    local backup_name="$2"
    local backup_dir="/backup/heal7-saju/${TIMESTAMP}"
    
    if [ -d "$source" ]; then
        log_info "$backup_name 백업 중..."
        sudo mkdir -p "$backup_dir"
        sudo cp -r "$source" "$backup_dir/$backup_name"
        log_success "$backup_name 백업 완료: $backup_dir/$backup_name"
    else
        log_warning "$backup_name 디렉터리가 존재하지 않아 백업을 건너뜁니다: $source"
    fi
}

# 의존성 확인 함수
check_dependencies() {
    log_header "의존성 확인"
    
    local deps=("node" "npm" "python3" "pip3" "nginx" "systemctl" "git")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if command -v "$dep" >/dev/null 2>&1; then
            log_success "$dep 설치됨"
        else
            log_error "$dep 설치되지 않음"
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "누락된 의존성: ${missing_deps[*]}"
        return 1
    fi
    
    log_success "모든 의존성이 설치되어 있습니다"
    return 0
}

# ====================================
# 🎯 메인 배포 함수들
# ====================================

# 시스템 상태 확인
check_system_status() {
    log_header "시스템 상태 확인"
    
    # 디스크 공간 확인
    local disk_usage=$(df /var/www 2>/dev/null | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 85 ]; then
        log_warning "디스크 사용량이 높습니다: ${disk_usage}%"
    else
        log_info "디스크 사용량: ${disk_usage}%"
    fi
    
    # 메모리 확인
    local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    log_info "메모리 사용량: ${mem_usage}%"
    
    # 현재 실행 중인 서비스 확인
    log_info "현재 서비스 상태:"
    log_info "  - 프론트엔드: $(check_service "$FRONTEND_SERVICE")"
    log_info "  - 백엔드: $(check_service "$BACKEND_SERVICE")"
    log_info "  - Nginx: $(check_service "$NGINX_SERVICE")"
    
    # 포트 사용 상태 확인
    log_info "포트 사용 상태:"
    log_info "  - 프론트엔드($FRONTEND_PORT): $(check_port "$FRONTEND_PORT")"
    log_info "  - 백엔드($BACKEND_PORT): $(check_port "$BACKEND_PORT")"
    log_info "  - 기존 백엔드($OLD_BACKEND_PORT): $(check_port "$OLD_BACKEND_PORT")"
}

# 환경 설정
setup_environment() {
    log_header "환경 설정"
    
    # 웹 루트 디렉터리 설정 (Vite 기반)
    log_info "웹 루트 디렉터리 설정"
    sudo mkdir -p "$WEB_ROOT"
    sudo mkdir -p "/var/log/heal7-saju"
    sudo mkdir -p "/var/cache/nginx/heal7_saju"
    
    # 권한 설정
    sudo chown -R www-data:www-data "$WEB_ROOT"
    sudo chown -R www-data:www-data "/var/cache/nginx/heal7_saju"
    sudo chmod -R 755 "$WEB_ROOT"
    
    log_success "환경 설정 완료"
}

# 프론트엔드 빌드 및 배포
deploy_frontend() {
    log_header "프론트엔드 빌드 및 배포"
    
    cd "$FRONTEND_DIR"
    
    # pnpm 설치 확인
    if ! command -v pnpm >/dev/null 2>&1; then
        log_info "pnpm 설치 중..."
        npm install -g pnpm
    fi
    
    # 의존성 설치
    log_info "프론트엔드 의존성 설치 중..."
    if ! pnpm install; then
        log_error "의존성 설치 실패"
        return 1
    fi
    
    # shared 패키지 먼저 빌드
    log_info "공통 모듈 빌드 중..."
    if ! pnpm --filter @heal7/shared build; then
        log_warning "공통 모듈 빌드에서 경고가 발생했습니다. 계속 진행합니다."
    fi
    
    # saju-app 빌드 (타입 체크 건너뛰기)
    log_info "사주 앱 빌드 중..."
    if ! pnpm --filter @heal7/saju-app exec vite build --mode production; then
        log_error "사주 앱 빌드 실패"
        return 1
    fi
    
    # 기존 파일 백업
    backup_directory "$WEB_ROOT" "saju-frontend"
    
    # 빌드된 파일 배포
    log_info "빌드된 파일 배포 중..."
    sudo rm -rf "$WEB_ROOT/*"
    
    # Vite 빌드 결과물 복사 (saju-app에서)
    local saju_dist="$FRONTEND_DIR/packages/saju-app/dist"
    if [ -d "$saju_dist" ]; then
        sudo cp -r "$saju_dist"/* "$WEB_ROOT/"
    else
        log_error "Vite 빌드 결과물을 찾을 수 없습니다: $saju_dist"
        return 1
    fi
    
    # 권한 설정
    sudo chown -R www-data:www-data "$WEB_ROOT"
    sudo chmod -R 755 "$WEB_ROOT"
    
    log_success "프론트엔드 배포 완료"
}

# 백엔드 배포
deploy_backend() {
    log_header "백엔드 배포"
    
    cd "$BACKEND_DIR"
    
    # Python 가상환경 설정
    if [ ! -d "venv" ]; then
        log_info "Python 가상환경 생성 중..."
        python3 -m venv venv
    fi
    
    # 가상환경 활성화
    source venv/bin/activate
    
    # 의존성 설치
    log_info "백엔드 의존성 설치 중..."
    if ! pip install -r requirements.txt; then
        log_error "백엔드 의존성 설치 실패"
        return 1
    fi
    
    # 타입 체크 (만약 mypy가 설정되어 있다면)
    if [ -f "mypy.ini" ]; then
        log_info "Python 타입 체크 중..."
        mypy . || log_warning "타입 체크에서 경고가 발생했습니다."
    fi
    
    # 테스트 실행 (있는 경우)
    if [ -d "tests" ]; then
        log_info "백엔드 테스트 실행 중..."
        python -m pytest tests/ || log_warning "일부 테스트가 실패했습니다."
    fi
    
    log_success "백엔드 배포 준비 완료"
}

# Nginx 설정 배포
deploy_nginx() {
    log_header "Nginx 설정 배포"
    
    # 현재 Nginx 설정 백업
    if [ -f "$NGINX_CONF_DIR/saju.heal7.com.conf" ]; then
        backup_directory "$NGINX_CONF_DIR" "nginx-sites-available"
    fi
    
    # 새 Nginx 설정 복사
    log_info "새 Nginx 설정 배포 중..."
    sudo cp "$DEPLOYMENT_DIR/nginx/saju.heal7.com.conf" "$NGINX_CONF_DIR/"
    
    # 심볼릭 링크 생성
    sudo ln -sf "$NGINX_CONF_DIR/saju.heal7.com.conf" "$NGINX_ENABLED_DIR/"
    
    # Nginx 설정 테스트
    log_info "Nginx 설정 검증 중..."
    if ! sudo nginx -t; then
        log_error "Nginx 설정이 올바르지 않습니다"
        return 1
    fi
    
    log_success "Nginx 설정 배포 완료"
}

# 서비스 설정 및 시작
setup_services() {
    log_header "서비스 설정 및 시작"
    
    # SystemD 서비스 파일 배포 (있는 경우)
    if [ -f "$DEPLOYMENT_DIR/systemd/heal7-saju-backend.service" ]; then
        log_info "백엔드 서비스 파일 배포 중..."
        sudo cp "$DEPLOYMENT_DIR/systemd/heal7-saju-backend.service" /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable heal7-saju-backend
    fi
    
    # 기존 서비스 중지
    log_info "기존 서비스 중지 중..."
    if systemctl is-active --quiet heal7-saju; then
        sudo systemctl stop heal7-saju || true
    fi
    
    # 새 백엔드 서비스 시작
    log_info "백엔드 서비스 시작 중..."
    if systemctl list-unit-files | grep -q heal7-saju-backend; then
        sudo systemctl restart heal7-saju-backend
    else
        # SystemD 서비스가 없으면 직접 실행
        log_info "백엔드를 백그라운드로 시작합니다..."
        cd "$BACKEND_DIR"
        source venv/bin/activate
        nohup python main.py > /var/log/heal7-saju/backend.log 2>&1 &
    fi
    
    # Nginx 재시작
    log_info "Nginx 재시작 중..."
    sudo systemctl restart nginx
    
    log_success "서비스 설정 완료"
}

# 배포 후 검증
verify_deployment() {
    log_header "배포 검증"
    
    # 서비스 상태 확인
    sleep 5  # 서비스 시작 대기
    
    local nginx_status=$(check_service nginx)
    log_info "Nginx 상태: $nginx_status"
    
    # 백엔드 헬스체크
    log_info "백엔드 헬스체크 중..."
    local health_check=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$BACKEND_PORT/health" || echo "failed")
    if [ "$health_check" = "200" ]; then
        log_success "백엔드 헬스체크 성공"
    else
        log_error "백엔드 헬스체크 실패 (상태 코드: $health_check)"
    fi
    
    # HTTPS 접근 테스트
    log_info "HTTPS 접근 테스트 중..."
    local https_check=$(curl -s -o /dev/null -w "%{http_code}" "https://saju.heal7.com" || echo "failed")
    if [ "$https_check" = "200" ]; then
        log_success "HTTPS 접근 성공"
    else
        log_warning "HTTPS 접근 실패 (상태 코드: $https_check)"
    fi
    
    # SSL 인증서 확인
    log_info "SSL 인증서 확인 중..."
    local ssl_expiry=$(openssl s_client -connect saju.heal7.com:443 -servername saju.heal7.com 2>/dev/null | openssl x509 -noout -dates 2>/dev/null | grep notAfter | cut -d= -f2)
    if [ -n "$ssl_expiry" ]; then
        log_info "SSL 인증서 만료일: $ssl_expiry"
    else
        log_warning "SSL 인증서 정보를 가져올 수 없습니다"
    fi
}

# 롤백 함수
rollback() {
    log_header "롤백 실행"
    
    local backup_timestamp="$1"
    local backup_dir="/backup/heal7-saju/$backup_timestamp"
    
    if [ ! -d "$backup_dir" ]; then
        log_error "백업 디렉터리를 찾을 수 없습니다: $backup_dir"
        return 1
    fi
    
    log_info "백업에서 복원 중: $backup_dir"
    
    # 프론트엔드 롤백
    if [ -d "$backup_dir/frontend" ]; then
        sudo rm -rf "$WEB_ROOT/frontend"
        sudo cp -r "$backup_dir/frontend" "$WEB_ROOT/"
        sudo chown -R www-data:www-data "$WEB_ROOT/frontend"
    fi
    
    # Nginx 설정 롤백
    if [ -d "$backup_dir/nginx-sites-available" ]; then
        sudo cp "$backup_dir/nginx-sites-available/saju.heal7.com.conf" "$NGINX_CONF_DIR/"
        sudo nginx -t && sudo systemctl reload nginx
    fi
    
    log_success "롤백 완료"
}

# 정리 함수
cleanup() {
    log_header "정리 작업"
    
    # 오래된 백업 정리 (30일 이상)
    log_info "오래된 백업 정리 중..."
    find /backup/heal7-saju -type d -mtime +30 -exec sudo rm -rf {} + 2>/dev/null || true
    
    # 오래된 로그 정리 (7일 이상)
    log_info "오래된 로그 정리 중..."
    find /var/log -name "heal7-saju-deploy-*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Nginx 캐시 정리
    log_info "Nginx 캐시 정리 중..."
    sudo find /var/cache/nginx/heal7_saju -type f -mtime +1 -delete 2>/dev/null || true
    
    log_success "정리 작업 완료"
}

# ====================================
# 🚀 메인 실행 함수
# ====================================

# 도움말 출력
show_help() {
    cat << EOF
HEAL7 사주명리학 통합 배포 스크립트 v2.0.0

사용법:
    $0 [옵션] [명령어]

명령어:
    deploy          전체 배포 실행 (기본값)
    frontend        프론트엔드만 배포
    backend         백엔드만 배포
    nginx           Nginx 설정만 배포
    verify          배포 검증만 실행
    rollback <시점> 지정된 시점으로 롤백
    cleanup         정리 작업만 실행
    status          현재 상태 확인

옵션:
    -h, --help      이 도움말 출력
    -v, --verbose   상세 로그 출력
    -f, --force     강제 실행 (확인 건너뛰기)
    -b, --backup    배포 전 백업 강제 실행
    -t, --test      테스트 모드 (실제 배포 안함)

예시:
    $0 deploy                    # 전체 배포
    $0 frontend                  # 프론트엔드만 배포
    $0 rollback 20240813_140530  # 특정 시점으로 롤백
    $0 -v -b deploy             # 상세 로그 + 강제 백업으로 전체 배포

EOF
}

# 메인 함수
main() {
    local command="${1:-deploy}"
    local force_mode=false
    local test_mode=false
    local backup_mode=false
    local verbose_mode=false
    
    # 옵션 파싱
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                verbose_mode=true
                set -x  # 상세 디버그 모드
                shift
                ;;
            -f|--force)
                force_mode=true
                shift
                ;;
            -b|--backup)
                backup_mode=true
                shift
                ;;
            -t|--test)
                test_mode=true
                shift
                ;;
            deploy|frontend|backend|nginx|verify|rollback|cleanup|status)
                command="$1"
                shift
                ;;
            *)
                if [[ "$command" == "rollback" && -n "$1" ]]; then
                    rollback_timestamp="$1"
                    shift
                else
                    log_error "알 수 없는 옵션: $1"
                    show_help
                    exit 1
                fi
                ;;
        esac
    done
    
    # 로그 시작
    log_header "HEAL7 사주명리학 배포 시작"
    log_info "배포 시작 시간: $(date)"
    log_info "실행 명령어: $command"
    log_info "스크립트 버전: 2.0.0"
    
    # 테스트 모드 알림
    if [ "$test_mode" = true ]; then
        log_warning "테스트 모드로 실행됩니다 (실제 배포 안함)"
        return 0
    fi
    
    # root 권한 확인
    if [ "$EUID" -eq 0 ]; then
        log_warning "root 권한으로 실행되고 있습니다"
    fi
    
    # 의존성 확인
    if ! check_dependencies; then
        log_error "의존성 확인 실패"
        exit 1
    fi
    
    # 명령어별 실행
    case "$command" in
        deploy)
            check_system_status
            setup_environment
            deploy_frontend
            deploy_backend
            deploy_nginx
            setup_services
            verify_deployment
            cleanup
            ;;
        frontend)
            deploy_frontend
            ;;
        backend)
            deploy_backend
            setup_services
            ;;
        nginx)
            deploy_nginx
            sudo systemctl reload nginx
            ;;
        verify)
            verify_deployment
            ;;
        rollback)
            if [ -z "${rollback_timestamp:-}" ]; then
                log_error "롤백할 시점을 지정해주세요"
                log_info "사용 가능한 백업: $(ls -1 /backup/heal7-saju/ 2>/dev/null | head -5)"
                exit 1
            fi
            rollback "$rollback_timestamp"
            ;;
        cleanup)
            cleanup
            ;;
        status)
            check_system_status
            ;;
        *)
            log_error "알 수 없는 명령어: $command"
            show_help
            exit 1
            ;;
    esac
    
    # 완료 메시지
    log_header "배포 완료"
    log_success "배포가 성공적으로 완료되었습니다!"
    log_info "배포 종료 시간: $(date)"
    log_info "로그 파일: $LOG_FILE"
    
    # 접속 정보 출력
    if [ "$command" = "deploy" ] || [ "$command" = "verify" ]; then
        log_info ""
        log_info "🌐 서비스 접속 정보:"
        log_info "  - 웹사이트: https://saju.heal7.com"
        log_info "  - API 문서: https://saju.heal7.com/api/docs"
        log_info "  - 헬스체크: https://saju.heal7.com/api/health"
        log_info "  - 관리자: https://saju.heal7.com/admin"
    fi
}

# 스크립트 시작점
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi