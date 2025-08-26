#!/bin/bash

# HEAL7 REFERENCE_LIBRARY 로컬 백업 시스템 v1.0
# 매일 백업 + 7일 보관 정책
# 작성일: 2025-08-23
# 담당: HEAL7 개발팀

SOURCE_PATH="/home/ubuntu/REFERENCE_LIBRARY/"
BACKUP_BASE="/home/ubuntu/backups"
BACKUP_NAME="REFERENCE_LIBRARY"
LOG_FILE="/home/ubuntu/logs/reference-library-backup.log"
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
DATE_TODAY=$(date '+%Y-%m-%d')

log() {
    echo "[$DATE_TODAY $(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 백업 디렉토리 생성
setup_backup_dirs() {
    mkdir -p "$BACKUP_BASE"
    mkdir -p "/home/ubuntu/logs"
    
    if [ ! -d "$SOURCE_PATH" ]; then
        log "❌ 소스 디렉토리 없음: $SOURCE_PATH"
        exit 1
    fi
    
    log "✅ 백업 디렉토리 준비 완료"
}

# 백업 실행
create_backup() {
    local backup_path="${BACKUP_BASE}/${BACKUP_NAME}_${TIMESTAMP}.tar.gz"
    
    log "🎯 백업 시작: $SOURCE_PATH → $backup_path"
    
    # 소스 정보 로깅
    local file_count=$(find "$SOURCE_PATH" -type f | wc -l)
    local dir_size=$(du -sh "$SOURCE_PATH" 2>/dev/null | cut -f1 || echo "Unknown")
    
    log "📊 백업 대상 정보:"
    log "  - 파일 수: ${file_count}개"
    log "  - 디렉토리 크기: $dir_size"
    
    # tar 백업 실행 (.git 제외)
    cd "$(dirname "$SOURCE_PATH")"
    
    if tar -czf "$backup_path" \
        --exclude='*.tmp' \
        --exclude='*.log' \
        --exclude='.git' \
        --exclude='.gitignore' \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='.DS_Store' \
        "$(basename "$SOURCE_PATH")" 2>/dev/null; then
        
        local backup_size=$(du -sh "$backup_path" | cut -f1)
        log "✅ 백업 생성 완료"
        log "  - 백업 파일: $(basename "$backup_path")"
        log "  - 백업 크기: $backup_size"
        
        # 압축률 계산
        local original_size_kb=$(du -sk "$SOURCE_PATH" | cut -f1)
        local backup_size_kb=$(du -sk "$backup_path" | cut -f1)
        local compression_ratio=$((100 - (backup_size_kb * 100 / original_size_kb)))
        
        log "  - 압축률: ${compression_ratio}%"
        
        return 0
    else
        log "❌ 백업 생성 실패"
        return 1
    fi
}

# 7일 보관 정책 적용
cleanup_old_backups() {
    log "🧹 이전 백업 정리 시작 (7일 이상)"
    
    local deleted_count=0
    local total_freed=0
    
    # 7일 이상 된 백업 파일 찾아서 삭제
    find "$BACKUP_BASE" -name "${BACKUP_NAME}_*.tar.gz" -mtime +7 -type f | while read backup_file; do
        if [ -f "$backup_file" ]; then
            local file_size=$(du -sk "$backup_file" | cut -f1)
            local file_name=$(basename "$backup_file")
            
            rm -f "$backup_file"
            log "🗑️  삭제: $file_name (${file_size}KB)"
            
            deleted_count=$((deleted_count + 1))
            total_freed=$((total_freed + file_size))
        fi
    done
    
    # 현재 백업 파일 상태
    local current_backups=$(ls -1 "$BACKUP_BASE"/${BACKUP_NAME}_*.tar.gz 2>/dev/null | wc -l)
    local total_backup_size=$(du -sh "$BACKUP_BASE" 2>/dev/null | cut -f1 || echo "0")
    
    log "📊 백업 정리 결과:"
    log "  - 현재 백업 수: ${current_backups}개"
    log "  - 전체 백업 크기: $total_backup_size"
    
    if [ $deleted_count -gt 0 ]; then
        log "  - 삭제된 파일: ${deleted_count}개"
        log "  - 확보된 공간: $((total_freed / 1024))MB"
    else
        log "  - 삭제할 백업 없음"
    fi
}

# 백업 무결성 검증
verify_backup() {
    local latest_backup=$(ls -t "$BACKUP_BASE"/${BACKUP_NAME}_*.tar.gz 2>/dev/null | head -1)
    
    if [ -f "$latest_backup" ]; then
        log "🔍 백업 무결성 검증: $(basename "$latest_backup")"
        
        if tar -tzf "$latest_backup" >/dev/null 2>&1; then
            log "✅ 백업 파일 무결성 확인 완료"
            
            # 백업 내용 간단 검증
            local backup_file_count=$(tar -tzf "$latest_backup" | wc -l)
            log "  - 백업 내 파일 수: ${backup_file_count}개"
            
            return 0
        else
            log "❌ 백업 파일 손상 감지"
            return 1
        fi
    else
        log "❌ 백업 파일 없음"
        return 1
    fi
}

# 백업 목록 표시
show_backup_status() {
    log "📋 현재 백업 상태:"
    
    if [ -d "$BACKUP_BASE" ] && [ "$(ls -A "$BACKUP_BASE"/${BACKUP_NAME}_*.tar.gz 2>/dev/null)" ]; then
        ls -lah "$BACKUP_BASE"/${BACKUP_NAME}_*.tar.gz | while read line; do
            log "  $line"
        done
    else
        log "  백업 파일 없음"
    fi
}

# 메인 실행 함수
main() {
    log "🎯 REFERENCE_LIBRARY 로컬 백업 v1.0 시작"
    
    # 1. 백업 환경 준비
    setup_backup_dirs
    
    # 2. 백업 실행
    if create_backup; then
        log "✅ 백업 생성 성공"
    else
        log "❌ 백업 생성 실패"
        exit 1
    fi
    
    # 3. 백업 검증
    verify_backup
    
    # 4. 이전 백업 정리 (7일 보관)
    cleanup_old_backups
    
    # 5. 최종 상태 표시
    show_backup_status
    
    log "🎉 백업 프로세스 완료"
}

# 스크립트 실행
main "$@"