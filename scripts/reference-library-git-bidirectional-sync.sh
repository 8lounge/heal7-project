#!/bin/bash

# HEAL7 REFERENCE_LIBRARY 진정한 양방향 Git 동기화 v2.0
# Git 기반 양방향 동기화로 rsync 방식을 완전 대체
# 작성일: 2025-08-23
# 담당: HEAL7 개발팀

LOCAL_PATH="/home/ubuntu/REFERENCE_LIBRARY/"
REMOTE_NAME="remote-server"
BRANCH="main"
LOG_FILE="/home/ubuntu/logs/reference-library-git-sync.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Git 상태 체크 및 자동 복구
git_health_check() {
    cd "$LOCAL_PATH"
    
    log "🔍 Git 상태 체크..."
    
    # Git 저장소 유효성 확인
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        log "❌ Git 저장소가 손상되었습니다!"
        exit 1
    fi
    
    # Remote 연결 확인
    if ! git ls-remote "$REMOTE_NAME" >/dev/null 2>&1; then
        log "❌ 원격 서버 연결 실패: $REMOTE_NAME"
        
        # SSH 연결 재시도
        log "🔄 SSH 키 복원 및 재연결 시도..."
        bash /home/ubuntu/scripts/ssh_key_monitor.sh
        
        # Remote 재설정
        git remote remove "$REMOTE_NAME" 2>/dev/null || true
        git remote add "$REMOTE_NAME" heal7-remote-private:/home/ubuntu/REFERENCE_LIBRARY
        
        if ! git ls-remote "$REMOTE_NAME" >/dev/null 2>&1; then
            log "❌ 원격 서버 복구 실패"
            exit 1
        fi
        log "✅ 원격 서버 연결 복구 완료"
    fi
    
    log "✅ Git 상태 정상"
}

# 로컬 변경사항 커밋
commit_local_changes() {
    cd "$LOCAL_PATH"
    
    log "📝 로컬 변경사항 확인..."
    
    if ! git diff --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        # 변경된 파일 리스트 로깅
        local changed_files=$(git diff --name-only; git ls-files --others --exclude-standard)
        log "📋 변경된 파일들: $(echo $changed_files | tr '\n' ' ')"
        
        git add .
        git commit -m "Local changes - $TIMESTAMP

변경된 파일:
$changed_files" 2>/dev/null || {
            log "⚠️  커밋 실패 - 변경사항이 없거나 오류 발생"
            return 1
        }
        
        log "✅ 로컬 변경사항 커밋 완료"
        return 0
    else
        log "ℹ️  로컬 변경사항 없음"
        return 1
    fi
}

# 원격 변경사항 fetch 및 분석
fetch_remote_changes() {
    cd "$LOCAL_PATH"
    
    log "📡 원격 변경사항 fetch..."
    
    local local_commit=$(git rev-parse HEAD)
    
    git fetch "$REMOTE_NAME" "$BRANCH" 2>/dev/null || {
        log "❌ 원격 fetch 실패"
        return 1
    }
    
    local remote_commit=$(git rev-parse "$REMOTE_NAME/$BRANCH")
    
    if [ "$local_commit" = "$remote_commit" ]; then
        log "✅ 로컬과 원격이 동일 - 동기화 불필요"
        return 1
    fi
    
    # 분기 상태 분석
    local ahead=$(git rev-list --count HEAD.."$REMOTE_NAME/$BRANCH" 2>/dev/null || echo "0")
    local behind=$(git rev-list --count "$REMOTE_NAME/$BRANCH"..HEAD 2>/dev/null || echo "0")
    
    log "📊 동기화 분석:"
    log "  - 로컬 앞서는 커밋: $behind개"
    log "  - 원격 앞서는 커밋: $ahead개"
    
    if [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
        log "🔀 양쪽에 변경사항 존재 - merge 필요"
        return 2
    elif [ "$ahead" -gt 0 ]; then
        log "📥 원격에만 변경사항 존재 - pull 필요"
        return 3
    elif [ "$behind" -gt 0 ]; then
        log "📤 로컬에만 변경사항 존재 - push 필요"
        return 4
    fi
    
    return 0
}

# 양방향 Git merge
bidirectional_merge() {
    cd "$LOCAL_PATH"
    local sync_type=$1
    
    case $sync_type in
        2)  # 양방향 merge
            log "🔄 양방향 merge 시작..."
            
            # 원격 변경사항 미리 확인
            local remote_files=$(git diff --name-only HEAD "$REMOTE_NAME/$BRANCH")
            log "📋 원격에서 변경된 파일: $(echo $remote_files | tr '\n' ' ')"
            
            # 자동 merge 시도
            if git merge "$REMOTE_NAME/$BRANCH" -m "Auto-merge: Bidirectional sync - $TIMESTAMP"; then
                log "✅ 자동 merge 성공"
            else
                log "⚠️  Merge 충돌 발생 - 수동 해결 필요"
                
                # 충돌 파일 리스트
                local conflict_files=$(git diff --name-only --diff-filter=U)
                log "🚨 충돌 파일: $(echo $conflict_files | tr '\n' ' ')"
                
                # 간단한 자동 해결 (현재 브랜치 우선)
                git checkout --ours . 2>/dev/null || true
                git add .
                git commit -m "Resolve conflicts: Keep local changes - $TIMESTAMP

충돌 해결된 파일:
$conflict_files" 2>/dev/null || true
                
                log "⚠️  충돌 자동 해결 (로컬 우선) - 검토 필요"
            fi
            ;;
        3)  # 원격 변경사항만 pull
            log "📥 원격 변경사항 pull..."
            git merge "$REMOTE_NAME/$BRANCH" --ff-only -m "Pull remote changes - $TIMESTAMP" || {
                git merge "$REMOTE_NAME/$BRANCH" -m "Pull remote changes (non-ff) - $TIMESTAMP"
            }
            log "✅ 원격 변경사항 적용 완료"
            ;;
        4)  # 로컬 변경사항만 있음 (push 대기)
            log "📤 로컬 변경사항 push 대기..."
            ;;
    esac
}

# 원격으로 push
push_to_remote() {
    cd "$LOCAL_PATH"
    
    log "📤 원격 서버로 push..."
    
    if git push "$REMOTE_NAME" "$BRANCH" 2>/dev/null; then
        log "✅ Push 완료"
    else
        log "⚠️  Push 실패 - force push 시도..."
        
        # 백업 생성 후 force push
        git tag "backup-before-force-push-$(date +%Y%m%d-%H%M%S)" HEAD
        
        if git push "$REMOTE_NAME" "$BRANCH" --force-with-lease 2>/dev/null; then
            log "✅ Force push 완료 (백업 태그 생성됨)"
        else
            log "❌ Force push도 실패"
            return 1
        fi
    fi
}

# 동기화 후 상태 검증
verify_sync_status() {
    cd "$LOCAL_PATH"
    
    log "🔍 동기화 결과 검증..."
    
    local local_commit=$(git rev-parse HEAD)
    local remote_commit=$(git rev-parse "$REMOTE_NAME/$BRANCH" 2>/dev/null || echo "unknown")
    
    if [ "$local_commit" = "$remote_commit" ]; then
        log "✅ 동기화 완료: 로컬과 원격이 일치"
    else
        log "⚠️  동기화 불완전: 수동 확인 필요"
        log "  - 로컬: $local_commit"
        log "  - 원격: $remote_commit"
    fi
    
    # 통계
    local file_count=$(find . -type f -not -path './.git/*' | wc -l)
    local total_size=$(du -sh . | cut -f1)
    local git_size=$(du -sh .git | cut -f1)
    
    log "📊 최종 상태:"
    log "  - 파일 수: ${file_count}개"
    log "  - 전체 크기: $total_size"
    log "  - .git 크기: $git_size"
    log "  - 최신 커밋: $(git log -1 --pretty=format:'%h - %s (%cr)')"
}

# 메인 실행 함수
main() {
    log "🎯 REFERENCE_LIBRARY 진정한 양방향 Git 동기화 v2.0 시작"
    
    # 1. Git 상태 체크
    git_health_check
    
    # 2. 로컬 변경사항 커밋
    local local_changed=$?
    commit_local_changes
    local_changed=$?
    
    # 3. 원격 변경사항 분석
    fetch_remote_changes
    local sync_type=$?
    
    # 4. 양방향 동기화 실행
    if [ $sync_type -eq 1 ]; then
        log "✅ 동기화 불필요"
    else
        bidirectional_merge $sync_type
        push_to_remote
    fi
    
    # 5. 동기화 결과 검증
    verify_sync_status
    
    # 6. Git 최적화 (주간 1회)
    local last_optimization="/home/ubuntu/logs/.last_git_optimization"
    if [ ! -f "$last_optimization" ] || \
       [ $(find "$last_optimization" -mtime +7 | wc -l) -gt 0 ]; then
        
        log "🔧 주간 Git 최적화..."
        git gc --aggressive --prune=now >/dev/null 2>&1
        git repack -ad >/dev/null 2>&1
        touch "$last_optimization"
        log "✅ Git 최적화 완료"
    fi
    
    log "🎉 양방향 Git 동기화 완료"
}

# 스크립트 실행
main "$@"