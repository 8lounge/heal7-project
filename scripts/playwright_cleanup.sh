#!/bin/bash
# Playwright 자동 정리 스크립트
# 정기적으로 실행하여 불필요한 캐시와 프로세스를 정리

set -e

LOG_FILE="/home/ubuntu/logs/playwright_cleanup.log"
mkdir -p "$(dirname "$LOG_FILE")"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_message "🧹 Playwright 정리 스크립트 시작"

# 1. 오래된 브라우저 프로세스 확인 및 정리
OLD_BROWSER_PROCESSES=$(ps aux | grep -E "(chrome|chromium|firefox)" | grep -v grep | wc -l)
if [ "$OLD_BROWSER_PROCESSES" -gt 0 ]; then
    log_message "⚠️ $OLD_BROWSER_PROCESSES 개의 브라우저 프로세스 발견"
    
    # 10분 이상 실행된 브라우저 프로세스 종료
    pkill -f -9 "chrome.*--remote-debugging" 2>/dev/null || true
    pkill -f -9 "chromium.*--remote-debugging" 2>/dev/null || true
    log_message "🔥 오래된 브라우저 프로세스 정리 완료"
else
    log_message "✅ 실행 중인 브라우저 프로세스 없음"
fi

# 2. Playwright 캐시 크기 확인 및 정리
CACHE_SIZE=$(du -sm ~/.cache/ms-playwright 2>/dev/null | cut -f1 || echo "0")
MAX_CACHE_SIZE_MB=100

log_message "📊 현재 Playwright 캐시 크기: ${CACHE_SIZE}MB"

if [ "$CACHE_SIZE" -gt "$MAX_CACHE_SIZE_MB" ]; then
    log_message "🗑️ 캐시 크기 제한 초과 (${CACHE_SIZE}MB > ${MAX_CACHE_SIZE_MB}MB), 정리 시작"
    rm -rf ~/.cache/ms-playwright/* 2>/dev/null || true
    log_message "✅ Playwright 캐시 정리 완료"
else
    log_message "✅ 캐시 크기 정상 범위"
fi

# 3. NPX 캐시 정리 (playwright 관련만)
NPX_PLAYWRIGHT_COUNT=$(find ~/.npm/_npx -name "*playwright*" -type d 2>/dev/null | wc -l)
if [ "$NPX_PLAYWRIGHT_COUNT" -gt 0 ]; then
    log_message "🗑️ $NPX_PLAYWRIGHT_COUNT 개의 NPX Playwright 캐시 발견, 정리 시작"
    rm -rf ~/.npm/_npx/*playwright* 2>/dev/null || true
    log_message "✅ NPX Playwright 캐시 정리 완료"
else
    log_message "✅ NPX Playwright 캐시 없음"
fi

# 4. 임시 파일 정리
TEMP_FILES=$(find /tmp -name "*playwright*" -o -name "*chrome*" -o -name "*chromium*" 2>/dev/null | wc -l)
if [ "$TEMP_FILES" -gt 0 ]; then
    log_message "🗑️ $TEMP_FILES 개의 임시 파일 발견, 정리 시작"
    find /tmp -name "*playwright*" -exec rm -rf {} \; 2>/dev/null || true
    find /tmp -name "*chrome*" -exec rm -rf {} \; 2>/dev/null || true
    find /tmp -name "*chromium*" -exec rm -rf {} \; 2>/dev/null || true
    log_message "✅ 임시 파일 정리 완료"
else
    log_message "✅ 정리할 임시 파일 없음"
fi

# 5. 시스템 리소스 상태 확인
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
log_message "📊 현재 메모리 사용률: ${MEMORY_USAGE}%"

# 6. 메모리 사용률이 높으면 추가 정리
if (( $(echo "$MEMORY_USAGE > 85.0" | bc -l) )); then
    log_message "⚠️ 메모리 사용률 높음 (${MEMORY_USAGE}%), 추가 정리 실행"
    
    # 페이지 캐시 정리
    sync && echo 1 | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1 || true
    
    log_message "✅ 추가 메모리 정리 완료"
fi

log_message "🎉 Playwright 정리 스크립트 완료"

# 7. 정리 결과 요약
FINAL_CACHE_SIZE=$(du -sm ~/.cache/ms-playwright 2>/dev/null | cut -f1 || echo "0")
FINAL_MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')

log_message "📈 정리 결과 요약:"
log_message "   캐시 크기: ${CACHE_SIZE}MB → ${FINAL_CACHE_SIZE}MB"
log_message "   메모리 사용률: ${MEMORY_USAGE}% → ${FINAL_MEMORY_USAGE}%"