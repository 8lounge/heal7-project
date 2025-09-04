#!/bin/bash
# 일일 꿈풀이 데이터 수집 스크립트 (500개/일)
# 목표: 25,000개 달성 (50일간 수집)

LOG_FILE="/home/ubuntu/logs/daily-dream-collection.log"
COLLECTION_SCRIPT="/home/ubuntu/heal7-project/backend/services/crawling-service/crawling-cube/modules/crawling-engines/dream-collection/dream_collector_integrated.py"

# 로그 디렉터리 생성
mkdir -p /home/ubuntu/logs

# 시작 로그
echo "$(date): 일일 꿈풀이 데이터 수집 시작 (목표: 500개)" >> "$LOG_FILE"

# 현재 데이터 수 확인
CURRENT_COUNT=$(sudo -u postgres psql -d heal7 -t -c "SELECT COUNT(*) FROM dream_raw_collection;" | tr -d ' ')
echo "$(date): 현재 데이터 수: $CURRENT_COUNT" >> "$LOG_FILE"

# 목표 확인 (25,000개 이하인 경우에만 수집)
if [ "$CURRENT_COUNT" -lt 25000 ]; then
    echo "$(date): 수집 시작 (남은 목표: $((25000 - CURRENT_COUNT))개)" >> "$LOG_FILE"
    
    # Python 가상환경 활성화 후 수집 실행
    cd /home/ubuntu/heal7-project/backend/services/crawling-service/crawling-cube/modules/crawling-engines/dream-collection
    
    # 500개 수집 실행 (백그라운드)
    timeout 1800 python3 "$COLLECTION_SCRIPT" >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "$(date): 수집 성공 완료" >> "$LOG_FILE"
    else
        echo "$(date): 수집 중 오류 발생 (타임아웃 또는 시스템 오류)" >> "$LOG_FILE"
    fi
    
    # 수집 후 데이터 수 확인
    NEW_COUNT=$(sudo -u postgres psql -d heal7 -t -c "SELECT COUNT(*) FROM dream_raw_collection;" | tr -d ' ')
    COLLECTED=$((NEW_COUNT - CURRENT_COUNT))
    echo "$(date): 수집 완료. 신규 데이터: ${COLLECTED}개, 총 데이터: ${NEW_COUNT}개" >> "$LOG_FILE"
else
    echo "$(date): 목표 달성 (25,000개). 수집 중단" >> "$LOG_FILE"
fi

echo "$(date): 일일 수집 프로세스 완료" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"