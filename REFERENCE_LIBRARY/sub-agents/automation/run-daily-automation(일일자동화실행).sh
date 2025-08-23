#!/bin/bash
"""
🤖 HEAL7 일일 자동화 실행 스크립트
AI 에이전트 팀 자동화 도구들을 순차적으로 실행

Author: AI Agent Team
Created: 2025-08-20
Usage: bash run-daily-automation.sh [option]
Options:
  --full      전체 자동화 실행 (기본값)
  --health    헬스 체크만 실행
  --quality   코드 품질만 실행  
  --entropy   엔트로피만 실행
  --deploy    배포 검증만 실행
  --sync      팀 동기화만 실행
"""

# 스크립트 설정
set -euo pipefail
IFS=$'\n\t'

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 로깅 함수
log_info() {
    echo -e "${CYAN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_header() {
    echo -e "\n${WHITE}========================================${NC}"
    echo -e "${WHITE}🤖 $1${NC}"
    echo -e "${WHITE}========================================${NC}"
}

# 디렉토리 설정
AUTOMATION_DIR="/home/ubuntu/REFERENCE_LIBRARY/sub-agents/automation"
LOG_DIR="/home/ubuntu/logs"
PYTHON_CMD="python3"

# 로그 디렉토리 생성
mkdir -p "$LOG_DIR/automation-runs"

# 실행 옵션 파싱
OPTION="${1:-full}"

# 타임스탬프 생성
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
AUTOMATION_LOG="$LOG_DIR/automation-runs/daily_automation_$TIMESTAMP.log"

# 함수: 스크립트 실행 및 결과 로깅
run_automation_script() {
    local script_name="$1"
    local description="$2"
    local script_path="$AUTOMATION_DIR/$script_name"
    local exit_code=0
    
    log_header "$description"
    
    if [[ ! -f "$script_path" ]]; then
        log_error "스크립트 파일을 찾을 수 없습니다: $script_path"
        return 1
    fi
    
    log_info "실행 중: $script_name"
    
    # 스크립트 실행 (타임아웃 30분)
    if timeout 1800 "$PYTHON_CMD" "$script_path" 2>&1 | tee -a "$AUTOMATION_LOG"; then
        log_success "$description 완료"
        exit_code=0
    else
        exit_code=$?
        if [[ $exit_code -eq 124 ]]; then
            log_error "$description 시간 초과 (30분)"
        else
            log_error "$description 실패 (exit code: $exit_code)"
        fi
    fi
    
    # 결과를 로그에 기록
    echo "---" >> "$AUTOMATION_LOG"
    echo "Script: $script_name" >> "$AUTOMATION_LOG"
    echo "Description: $description" >> "$AUTOMATION_LOG"
    echo "Exit Code: $exit_code" >> "$AUTOMATION_LOG"
    echo "Timestamp: $(date)" >> "$AUTOMATION_LOG"
    echo "---" >> "$AUTOMATION_LOG"
    
    return $exit_code
}

# 함수: 시스템 사전 검사
pre_flight_check() {
    log_header "시스템 사전 검사"
    
    # Python 설치 확인
    if ! command -v python3 &> /dev/null; then
        log_error "Python3가 설치되지 않았습니다"
        exit 1
    fi
    log_info "Python3 버전: $(python3 --version)"
    
    # 필요한 Python 모듈 확인
    local required_modules=("psutil" "requests")
    for module in "${required_modules[@]}"; do
        if ! python3 -c "import $module" &> /dev/null; then
            log_warning "Python 모듈 '$module'이 설치되지 않았습니다. 설치 중..."
            pip3 install "$module" || log_error "모듈 '$module' 설치 실패"
        else
            log_info "Python 모듈 '$module' 확인됨"
        fi
    done
    
    # 로그 디렉토리 권한 확인
    if [[ ! -w "$LOG_DIR" ]]; then
        log_error "로그 디렉토리에 쓰기 권한이 없습니다: $LOG_DIR"
        exit 1
    fi
    
    # 자동화 스크립트 디렉토리 확인
    if [[ ! -d "$AUTOMATION_DIR" ]]; then
        log_error "자동화 스크립트 디렉토리를 찾을 수 없습니다: $AUTOMATION_DIR"
        exit 1
    fi
    
    # 시스템 리소스 확인
    local free_memory=$(free -m | awk 'NR==2{printf "%.1f", $7*100/$2}')
    local free_disk=$(df / | awk 'NR==2{printf "%.1f", 100-$5}')
    
    log_info "사용 가능한 메모리: ${free_memory}%"
    log_info "사용 가능한 디스크: ${free_disk}%"
    
    if (( $(echo "$free_memory < 10" | bc -l) )); then
        log_warning "사용 가능한 메모리가 부족합니다 (${free_memory}%)"
    fi
    
    if (( $(echo "$free_disk < 10" | bc -l) )); then
        log_warning "사용 가능한 디스크 공간이 부족합니다 (${free_disk}%)"
    fi
    
    log_success "시스템 사전 검사 완료"
}

# 함수: 헬스 체크 실행
run_health_check() {
    run_automation_script "daily-health-check.py" "시스템 헬스 체크"
}

# 함수: 코드 품질 스캔 실행
run_code_quality() {
    run_automation_script "code-quality-scanner.py" "코드 품질 스캔"
}

# 함수: 엔트로피 감지 실행
run_entropy_detection() {
    run_automation_script "entropy-detector.py" "엔트로피 감지 및 정리"
}

# 함수: 배포 검증 실행
run_deployment_validation() {
    run_automation_script "deployment-validator.py" "배포 검증"
}

# 함수: 팀 동기화 실행
run_team_sync() {
    run_automation_script "team-sync-orchestrator.py" "팀 동기화 오케스트레이션"
}

# 함수: 실행 결과 요약
generate_summary() {
    log_header "자동화 실행 결과 요약"
    
    local total_scripts=0
    local successful_scripts=0
    local failed_scripts=0
    
    # 로그 파일에서 결과 집계
    if [[ -f "$AUTOMATION_LOG" ]]; then
        total_scripts=$(grep -c "Script:" "$AUTOMATION_LOG" || echo "0")
        successful_scripts=$(grep -c "Exit Code: 0" "$AUTOMATION_LOG" || echo "0")
        failed_scripts=$((total_scripts - successful_scripts))
    fi
    
    echo -e "\n${WHITE}📊 실행 통계${NC}"
    echo -e "   전체 스크립트: $total_scripts"
    echo -e "   성공: ${GREEN}$successful_scripts${NC}"
    echo -e "   실패: ${RED}$failed_scripts${NC}"
    
    if [[ $failed_scripts -gt 0 ]]; then
        echo -e "\n${YELLOW}⚠️  실패한 스크립트가 있습니다. 로그를 확인하세요:${NC}"
        echo -e "   $AUTOMATION_LOG"
    fi
    
    # 최근 리포트 파일들 출력
    echo -e "\n${WHITE}📄 생성된 리포트${NC}"
    local report_dirs=(
        "/home/ubuntu/logs/health-reports"
        "/home/ubuntu/logs/code-quality-reports"
        "/home/ubuntu/logs/entropy-reports"
        "/home/ubuntu/logs/deployment-validation"
        "/home/ubuntu/logs/team-sync-reports"
    )
    
    for report_dir in "${report_dirs[@]}"; do
        if [[ -d "$report_dir" ]]; then
            local latest_report="$report_dir/latest.json"
            if [[ -L "$latest_report" ]]; then
                echo -e "   📋 $(basename "$report_dir"): $latest_report"
            fi
        fi
    done
    
    # 시스템 상태 요약
    echo -e "\n${WHITE}🏥 시스템 상태 요약${NC}"
    local health_latest="/home/ubuntu/logs/health-reports/latest.json"
    if [[ -f "$health_latest" ]]; then
        local overall_status=$(jq -r '.overall_status // "unknown"' "$health_latest" 2>/dev/null || echo "unknown")
        local status_emoji=""
        case "$overall_status" in
            "HEALTHY") status_emoji="✅" ;;
            "HEALTHY_WITH_WARNINGS") status_emoji="⚠️" ;;
            "WARNING") status_emoji="🟡" ;;
            "CRITICAL") status_emoji="🚨" ;;
            *) status_emoji="❓" ;;
        esac
        echo -e "   시스템 상태: $status_emoji $overall_status"
    fi
    
    # 엔트로피 레벨
    local entropy_latest="/home/ubuntu/logs/entropy-reports/latest.json"
    if [[ -f "$entropy_latest" ]]; then
        local entropy_level=$(jq -r '.entropy_level // "unknown"' "$entropy_latest" 2>/dev/null || echo "unknown")
        local entropy_emoji=""
        case "$entropy_level" in
            "low") entropy_emoji="🟢" ;;
            "medium") entropy_emoji="🟡" ;;
            "high") entropy_emoji="🟠" ;;
            "critical") entropy_emoji="🔴" ;;
            *) entropy_emoji="❓" ;;
        esac
        echo -e "   엔트로피 레벨: $entropy_emoji $entropy_level"
    fi
    
    log_success "자동화 실행 완료"
}

# 함수: 정리 작업
cleanup() {
    log_info "정리 작업 시작..."
    
    # 오래된 자동화 로그 정리 (30일 이상)
    find "$LOG_DIR/automation-runs" -name "daily_automation_*.log" -mtime +30 -delete 2>/dev/null || true
    
    # 오래된 리포트 정리 (30일 이상)
    local report_dirs=(
        "/home/ubuntu/logs/health-reports"
        "/home/ubuntu/logs/code-quality-reports"
        "/home/ubuntu/logs/entropy-reports"
        "/home/ubuntu/logs/deployment-validation"
        "/home/ubuntu/logs/team-sync-reports"
    )
    
    for report_dir in "${report_dirs[@]}"; do
        if [[ -d "$report_dir" ]]; then
            find "$report_dir" -name "*.json" ! -name "latest.json" -mtime +30 -delete 2>/dev/null || true
        fi
    done
    
    log_info "정리 작업 완료"
}

# 메인 실행 함수
main() {
    # 트랩 설정 (스크립트 종료 시 정리)
    trap cleanup EXIT
    
    # 시작 로그
    log_header "HEAL7 일일 자동화 시스템 시작"
    log_info "실행 옵션: $OPTION"
    log_info "로그 파일: $AUTOMATION_LOG"
    
    # 시작 시간 기록
    local start_time=$(date +%s)
    
    # 사전 검사
    pre_flight_check
    
    # 옵션에 따른 실행
    case "$OPTION" in
        "--health")
            run_health_check
            ;;
        "--quality")
            run_code_quality
            ;;
        "--entropy")
            run_entropy_detection
            ;;
        "--deploy")
            run_deployment_validation
            ;;
        "--sync")
            run_team_sync
            ;;
        "--full"|*)
            # 전체 자동화 실행 (권장 순서)
            log_info "전체 자동화 시퀀스 시작..."
            
            # 1. 시스템 헬스 체크 (기본 상태 확인)
            run_health_check
            
            # 2. 엔트로피 감지 및 정리 (시스템 정리)
            run_entropy_detection
            
            # 3. 코드 품질 스캔 (코드 분석)
            run_code_quality
            
            # 4. 배포 검증 (배포 준비 상태)
            run_deployment_validation
            
            # 5. 팀 동기화 (최종 조율)
            run_team_sync
            ;;
    esac
    
    # 종료 시간 계산
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local duration_min=$((duration / 60))
    local duration_sec=$((duration % 60))
    
    log_info "총 실행 시간: ${duration_min}분 ${duration_sec}초"
    
    # 결과 요약
    generate_summary
}

# 스크립트 실행
main "$@"