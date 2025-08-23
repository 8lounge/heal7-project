#!/bin/bash

# HEAL7 REFERENCE_LIBRARY 경량화 관리 시스템
# Git LFS 없이 효율적 용량 관리 + 양방향 동기화
# 작성일: 2025-08-22
# 담당: HEAL7 개발팀

# 설정
LOCAL_PATH="/home/ubuntu/REFERENCE_LIBRARY/"
REMOTE_HOST="heal7-remote-private"
REMOTE_PATH="/home/ubuntu/REFERENCE_LIBRARY/"
LOG_FILE="/home/ubuntu/logs/reference-library-lightweight.log"
ARCHIVE_PATH="/home/ubuntu/REFERENCE_LIBRARY_ARCHIVE"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
MAX_GIT_SIZE_MB=20  # .git 폴더 최대 크기 (더 엄격하게)
LARGE_FILE_THRESHOLD="50k"  # 대용량 파일 기준

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# 대용량 파일 분리 아카이브 관리
manage_large_files() {
    cd "$LOCAL_PATH"
    
    log "📦 대용량 파일 아카이브 관리..."
    
    # 아카이브 디렉토리 생성
    mkdir -p "$ARCHIVE_PATH"
    
    # 50KB 이상 파일 찾기
    find . -type f -size +$LARGE_FILE_THRESHOLD -not -path './.git/*' | while read file; do
        local file_size=$(du -h "$file" | cut -f1)
        log "📋 대용량 파일 발견: $file ($file_size)"
        
        # HTML, PDF 등은 아카이브로 이동
        if [[ "$file" == *.html ]] || [[ "$file" == *.pdf ]] || [[ "$file" == *.zip ]]; then
            local archive_file="$ARCHIVE_PATH/$file"
            mkdir -p "$(dirname "$archive_file")"
            
            # 파일을 아카이브로 복사 후 Git에서 심볼릭 링크로 교체
            cp "$file" "$archive_file"
            rm "$file"
            ln -s "$archive_file" "$file"
            
            log "🔗 아카이브 링크 생성: $file → $archive_file"
        fi
    done
    
    # .gitignore에 아카이브 제외 추가
    if ! grep -q "REFERENCE_LIBRARY_ARCHIVE" .gitignore 2>/dev/null; then
        echo "# Large files archive" >> .gitignore
        echo "../REFERENCE_LIBRARY_ARCHIVE/" >> .gitignore
        git add .gitignore
        log "✅ .gitignore 업데이트 완료"
    fi
}

# Git 히스토리 압축 (Shallow 방식)
compress_git_history() {
    cd "$LOCAL_PATH"
    
    log "🗜️ Git 히스토리 스마트 압축..."
    
    local commit_count=$(git rev-list --count HEAD)
    
    if [ "$commit_count" -gt 5 ]; then
        log "📦 히스토리 압축 필요 (${commit_count}개 커밋)"
        
        # 백업 생성
        git bundle create "/tmp/full-history-backup-$(date +%Y%m%d).bundle" --all
        mv "/tmp/full-history-backup-$(date +%Y%m%d).bundle" /home/ubuntu/backups/
        log "💾 전체 히스토리 백업 생성"
        
        # 최근 3개 커밋만 유지하는 새 저장소 생성
        local temp_repo="/tmp/reference_library_compressed"
        rm -rf "$temp_repo"
        
        # 현재 상태 기준으로 새 저장소 생성
        git clone --depth 3 "file://$LOCAL_PATH" "$temp_repo"
        
        # .git 폴더 교체
        rm -rf .git
        mv "$temp_repo/.git" .
        rm -rf "$temp_repo"
        
        # Git 설정 복원
        git config user.name "HEAL7 System"
        git config user.email "system@heal7.com"
        git config pull.rebase false
        
        log "✅ 히스토리 압축 완료 (최근 3개 커밋 유지)"
    else
        log "ℹ️  히스토리 압축 불필요 (${commit_count}개 커밋)"
    fi
    
    # 기본 Git 최적화
    git gc --aggressive --prune=now
    git repack -ad
}

# 양방향 동기화 (경량화 버전)
lightweight_sync() {
    cd "$LOCAL_PATH"
    
    log "🔄 경량화 양방향 동기화 시작"
    
    # 로컬 변경사항 처리
    if ! git diff --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        git add .
        git commit -m "Auto-sync: Local changes - $TIMESTAMP" 2>/dev/null || true
        local_changed="true"
        log "📝 로컬 변경사항 커밋"
    else
        local_changed="false"
    fi
    
    # 원격 변경사항 처리 (rsync 백업 전략)
    log "📡 원격 상태 확인..."
    
    # 원격에서 변경사항이 있는지 간단히 체크
    local remote_timestamp=$(ssh "$REMOTE_HOST" "find $REMOTE_PATH -type f -not -path '*/.git/*' -printf '%T@\n' | sort -n | tail -1")
    local local_timestamp=$(find . -type f -not -path './.git/*' -printf '%T@\n' | sort -n | tail -1)
    
    if (( $(echo "$remote_timestamp > $local_timestamp" | bc -l) )); then
        log "📥 원격에서 새로운 변경사항 감지 - 풀 실행"
        
        # 간단한 rsync 동기화 (Git 부담 최소화)
        rsync -avz --exclude='.git' \
            "$REMOTE_HOST:$REMOTE_PATH" \
            "/home/ubuntu/REFERENCE_LIBRARY_TEMP/"
        
        # 변경된 파일만 선택적 병합
        rsync -avz --exclude='.git' \
            "/home/ubuntu/REFERENCE_LIBRARY_TEMP/REFERENCE_LIBRARY/" \
            "$LOCAL_PATH"
        
        rm -rf "/home/ubuntu/REFERENCE_LIBRARY_TEMP"
        
        # Git 커밋 (변경사항이 있을 때만)
        if ! git diff --quiet; then
            git add .
            git commit -m "Auto-sync: Remote changes - $TIMESTAMP"
            log "✅ 원격 변경사항 병합 완료"
        fi
    elif [[ "$local_changed" == "true" ]]; then
        log "📤 로컬 → 원격 동기화"
        rsync -avz --exclude='.git' "$LOCAL_PATH" "$REMOTE_HOST:$REMOTE_PATH"
        log "✅ 로컬 변경사항 전송 완료"
    else
        log "✅ 변경사항 없음"
    fi
}

# 용량 모니터링 및 자동 최적화
monitor_and_optimize() {
    cd "$LOCAL_PATH"
    
    local total_size=$(du -sm . | cut -f1)
    local git_size=$(du -sm .git | cut -f1)
    local git_percentage=$((git_size * 100 / total_size))
    
    log "📊 용량 모니터링:"
    log "  - 전체: ${total_size}MB"
    log "  - .git: ${git_size}MB (${git_percentage}%)"
    
    # 자동 최적화 트리거
    if [ "$git_size" -gt "$MAX_GIT_SIZE_MB" ] || [ "$git_percentage" -gt 30 ]; then
        log "🔧 자동 최적화 트리거 (${git_size}MB > ${MAX_GIT_SIZE_MB}MB)"
        
        # 1. 대용량 파일 아카이브
        manage_large_files
        
        # 2. 히스토리 압축
        compress_git_history
        
        # 3. 최종 압축
        git gc --aggressive
        
        # 4. 최적화 후 상태 확인
        local new_git_size=$(du -sm .git | cut -f1)
        local optimization_saved=$((git_size - new_git_size))
        
        log "✅ 최적화 완료: ${optimization_saved}MB 절약"
        log "  - 최적화 전: ${git_size}MB → 최적화 후: ${new_git_size}MB"
        
    else
        log "✅ Git 용량 정상 - 최적화 불필요"
    fi
}

# 주간 백업 및 아카이브
weekly_maintenance() {
    local last_maintenance="/home/ubuntu/logs/.last_weekly_maintenance"
    
    if [ ! -f "$last_maintenance" ] || \
       [ $(find "$last_maintenance" -mtime +7 | wc -l) -gt 0 ]; then
        
        log "🗓️  주간 유지보수 실행..."
        
        # 1. 전체 백업 생성
        cd /home/ubuntu
        tar -czf "backups/REFERENCE_LIBRARY_full_$(date +%Y%m%d).tar.gz" \
            --exclude='.git' \
            "REFERENCE_LIBRARY"
        
        # 2. Git bundle 백업
        cd "$LOCAL_PATH"
        git bundle create "/home/ubuntu/backups/reference-library-$(date +%Y%m%d).bundle" --all
        
        # 3. 아카이브 백업
        if [ -d "$ARCHIVE_PATH" ]; then
            tar -czf "/home/ubuntu/backups/REFERENCE_LIBRARY_ARCHIVE_$(date +%Y%m%d).tar.gz" \
                "$ARCHIVE_PATH"
        fi
        
        # 4. 오래된 백업 정리 (60일 이상)
        find /home/ubuntu/backups -name "REFERENCE_LIBRARY*" -mtime +60 -delete
        
        touch "$last_maintenance"
        log "✅ 주간 유지보수 완료"
    fi
}

# 메인 실행
main() {
    log "🎯 REFERENCE_LIBRARY 경량화 관리 시작"
    
    # SSH 연결 확인
    if ! ssh "$REMOTE_HOST" "echo 'SSH OK'" >/dev/null 2>&1; then
        log "❌ SSH 연결 실패"
        exit 1
    fi
    
    # 1. 용량 모니터링 및 최적화
    monitor_and_optimize
    
    # 2. 경량화 동기화
    lightweight_sync
    
    # 3. 주간 유지보수
    weekly_maintenance
    
    # 4. 최종 상태 리포트
    local final_total=$(du -sh . | cut -f1)
    local final_git=$(du -sh .git | cut -f1)
    local file_count=$(find . -type f -not -path './.git/*' | wc -l)
    
    log "📋 최종 상태:"
    log "  - 전체 크기: $final_total"
    log "  - .git 크기: $final_git" 
    log "  - 파일 수: ${file_count}개"
    log "  - 커밋 수: $(git rev-list --count HEAD)개"
    
    log "🎉 경량화 관리 완료"
}

# 스크립트 실행
main "$@"