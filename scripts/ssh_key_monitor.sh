#!/bin/bash
# SSH 키 모니터링 및 복원 스크립트

SSH_DIR="/home/ubuntu/.ssh"
AUTH_KEYS="$SSH_DIR/authorized_keys"
BACKUP_KEYS="$SSH_DIR/authorized_keys.backup"
LOG_FILE="/home/ubuntu/logs/ssh_monitor.log"

# 로그 디렉토리 생성
mkdir -p /home/ubuntu/logs

# 현재 시간
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# authorized_keys 파일 존재 확인
if [ ! -f "$AUTH_KEYS" ]; then
    echo "[$TIMESTAMP] ERROR: authorized_keys 파일이 없습니다!" >> "$LOG_FILE"
    
    # 백업에서 복원 시도
    if [ -f "$BACKUP_KEYS" ]; then
        cp "$BACKUP_KEYS" "$AUTH_KEYS"
        chmod 600 "$AUTH_KEYS"
        echo "[$TIMESTAMP] INFO: 백업에서 authorized_keys를 복원했습니다." >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] CRITICAL: 백업 파일도 존재하지 않습니다!" >> "$LOG_FILE"
    fi
else
    echo "[$TIMESTAMP] OK: authorized_keys 파일 정상 존재" >> "$LOG_FILE"
fi

# 권한 확인 및 수정
if [ -f "$AUTH_KEYS" ]; then
    CURRENT_PERMS=$(stat -c "%a" "$AUTH_KEYS")
    if [ "$CURRENT_PERMS" != "600" ]; then
        chmod 600 "$AUTH_KEYS"
        echo "[$TIMESTAMP] FIXED: authorized_keys 권한을 600으로 수정" >> "$LOG_FILE"
    fi
fi

# SSH 디렉토리 권한 확인
SSH_DIR_PERMS=$(stat -c "%a" "$SSH_DIR")
if [ "$SSH_DIR_PERMS" != "700" ]; then
    chmod 700 "$SSH_DIR"
    echo "[$TIMESTAMP] FIXED: .ssh 디렉토리 권한을 700으로 수정" >> "$LOG_FILE"
fi