#!/bin/bash

# HEAL7 REFERENCE_LIBRARY 최종 관리 시스템
# 경량화 + 양방향 동기화 + 자동 최적화 통합 솔루션
# 작성일: 2025-08-22
# 담당: HEAL7 개발팀

LOCAL_PATH="/home/ubuntu/REFERENCE_LIBRARY/"
LOG_FILE="/home/ubuntu/logs/reference-library-final.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# 메인 실행 함수
main() {
    cd "$LOCAL_PATH"
    
    log "🎯 REFERENCE_LIBRARY 최종 관리 시작"
    
    # Git 설정 확인
    git config user.name "HEAL7 System" 2>/dev/null || true
    git config user.email "system@heal7.com" 2>/dev/null || true
    git config pull.rebase false 2>/dev/null || true
    
    # 1. 현재 상태 체크
    local total_size=$(du -sm . | cut -f1)
    local git_size=$(du -sm .git | cut -f1)
    local git_percentage=$((git_size * 100 / total_size))
    
    log "📊 현재 상태: 전체 ${total_size}MB, .git ${git_size}MB (${git_percentage}%)"
    
    # 2. 로컬 변경사항 처리
    if ! git diff --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        git add .
        git commit -m "Daily sync - $TIMESTAMP"
        log "📝 로컬 변경사항 커밋 완료"
    else
        log "✅ 로컬 변경사항 없음"
    fi
    
    # 3. Git 최적화 (주간 1회)
    local last_optimization="/home/ubuntu/logs/.last_git_optimization"
    if [ ! -f "$last_optimization" ] || \
       [ $(find "$last_optimization" -mtime +7 | wc -l) -gt 0 ]; then
        
        log "🔧 주간 Git 최적화 실행..."
        
        # Git 압축
        git gc --aggressive --prune=now
        git repack -ad
        
        # Reflog 정리
        git reflog expire --expire=30.days.ago --all
        
        # 히스토리 제한 (최근 10개 커밋만 유지)
        local commit_count=$(git rev-list --count HEAD)
        if [ "$commit_count" -gt 10 ]; then
            # 백업 생성
            git bundle create "/home/ubuntu/backups/full-history-$(date +%Y%m%d).bundle" --all
            
            # 히스토리 압축 (최근 5개 커밋 유지)
            git reset --hard HEAD~$((commit_count - 5))
            git gc --aggressive --prune=now
            
            log "✅ 히스토리 압축: ${commit_count}개 → 5개"
        fi
        
        touch "$last_optimization"
        log "✅ Git 최적화 완료"
    fi
    
    # 4. 백업 관리 (월간)
    local last_backup="/home/ubuntu/logs/.last_monthly_backup"
    if [ ! -f "$last_backup" ] || \
       [ $(find "$last_backup" -mtime +30 | wc -l) -gt 0 ]; then
        
        log "💾 월간 백업 실행..."
        
        # 압축 백업 생성
        tar -czf "/home/ubuntu/backups/REFERENCE_LIBRARY_monthly_$(date +%Y%m).tar.gz" \
            --exclude='.git' \
            "REFERENCE_LIBRARY"
        
        # 오래된 백업 정리 (90일 이상)
        find /home/ubuntu/backups -name "REFERENCE_LIBRARY*" -mtime +90 -delete
        
        touch "$last_backup"
        log "✅ 월간 백업 완료"
    fi
    
    # 5. 최종 상태 리포트
    local final_total=$(du -sm . | cut -f1)
    local final_git=$(du -sm .git | cut -f1)
    local final_percentage=$((final_git * 100 / final_total))
    
    log "📋 최종 상태:"
    log "  - 전체: ${final_total}MB"
    log "  - .git: ${final_git}MB (${final_percentage}%)"
    log "  - 파일 수: $(find . -type f -not -path './.git/*' | wc -l)개"
    log "  - 커밋 수: $(git rev-list --count HEAD)개"
    
    # 6. 건강도 평가
    if [ "$final_git" -lt 20 ] && [ "$final_percentage" -lt 40 ]; then
        log "💚 시스템 상태: 최적화됨"
    elif [ "$final_git" -lt 50 ] && [ "$final_percentage" -lt 60 ]; then
        log "💛 시스템 상태: 양호"
    else
        log "🔴 시스템 상태: 최적화 필요"
    fi
    
    log "🎉 REFERENCE_LIBRARY 최종 관리 완료"
}

main "$@"