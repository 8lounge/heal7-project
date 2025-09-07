#!/bin/bash
# Playwright 모니터링 스크립트
# 실시간으로 Playwright 사용량을 모니터링하고 이상 상황 감지

LOG_FILE="/home/ubuntu/logs/playwright_monitor.log"
ALERT_LOG="/home/ubuntu/logs/playwright_alerts.log"

mkdir -p "$(dirname "$LOG_FILE")"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

alert_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🚨 ALERT: $1" | tee -a "$ALERT_LOG"
    log_message "🚨 ALERT: $1"
}

# 임계값 설정
MAX_BROWSER_PROCESSES=5
MAX_CACHE_SIZE_MB=200
MAX_MEMORY_USAGE=90.0

# 1. 브라우저 프로세스 수 확인
BROWSER_COUNT=$(ps aux | grep -E "(chrome|chromium|firefox)" | grep -v grep | wc -l)
if [ "$BROWSER_COUNT" -gt "$MAX_BROWSER_PROCESSES" ]; then
    alert_message "브라우저 프로세스 과다: $BROWSER_COUNT 개 (임계값: $MAX_BROWSER_PROCESSES)"
    
    # 자동 정리 실행
    ~/scripts/playwright_cleanup.sh >/dev/null 2>&1 &
else
    log_message "브라우저 프로세스 수 정상: $BROWSER_COUNT 개"
fi

# 2. Playwright 캐시 크기 확인
CACHE_SIZE=$(du -sm ~/.cache/ms-playwright 2>/dev/null | cut -f1 || echo "0")
if [ "$CACHE_SIZE" -gt "$MAX_CACHE_SIZE_MB" ]; then
    alert_message "Playwright 캐시 과다: ${CACHE_SIZE}MB (임계값: ${MAX_CACHE_SIZE_MB}MB)"
    
    # 자동 정리 실행
    ~/scripts/playwright_cleanup.sh >/dev/null 2>&1 &
else
    log_message "Playwright 캐시 크기 정상: ${CACHE_SIZE}MB"
fi

# 3. 메모리 사용률 확인
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
if (( $(echo "$MEMORY_USAGE > $MAX_MEMORY_USAGE" | bc -l) )); then
    alert_message "메모리 사용률 과다: ${MEMORY_USAGE}% (임계값: ${MAX_MEMORY_USAGE}%)"
else
    log_message "메모리 사용률 정상: ${MEMORY_USAGE}%"
fi

# 4. NPX 캐시 확인  
NPX_COUNT=$(find ~/.npm/_npx -name "*playwright*" -type d 2>/dev/null | wc -l)
if [ "$NPX_COUNT" -gt 2 ]; then
    alert_message "NPX Playwright 캐시 과다: $NPX_COUNT 개"
    
    # 자동 정리 실행
    ~/scripts/playwright_cleanup.sh >/dev/null 2>&1 &
else
    log_message "NPX Playwright 캐시 정상: $NPX_COUNT 개"
fi

log_message "모니터링 체크 완료 - 브라우저:$BROWSER_COUNT, 캐시:${CACHE_SIZE}MB, 메모리:${MEMORY_USAGE}%, NPX:$NPX_COUNT"