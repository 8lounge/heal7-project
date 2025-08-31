# HEAL7 서비스 모니터링 스크립트

## 📋 개요
`heal7-service-monitor.sh`는 HEAL7 프로젝트의 핵심 서비스들을 자동으로 모니터링하고 필요시 재시작하는 스크립트입니다.

## 🎯 모니터링 대상
- **사주 서비스** (포트 8003)
- **관리자 서비스** (포트 8006) 
- **Nginx 웹서버**

## 🚀 사용법

### 기본 사용법
```bash
# 한 번 점검 및 필요시 재시작
./heal7-service-monitor.sh

# 또는
./heal7-service-monitor.sh --once
```

### 상태 확인만
```bash
./heal7-service-monitor.sh --status
```

### 지속적 모니터링
```bash
# 30초마다 자동 점검 (백그라운드 실행 권장)
nohup ./heal7-service-monitor.sh --monitor > /dev/null 2>&1 &
```

### 도움말
```bash
./heal7-service-monitor.sh --help
```

## 📝 로그 파일
- 위치: `/var/log/heal7-monitor.log`
- 모든 점검 결과와 재시작 로그가 기록됩니다.

## ⚙️ Cron 설정 (선택사항)
5분마다 자동 점검하려면:
```bash
# crontab 편집
crontab -e

# 다음 라인 추가
*/5 * * * * /home/ubuntu/scripts/heal7-service-monitor.sh --once
```

## 🔧 트러블슈팅

### 권한 문제
```bash
chmod +x /home/ubuntu/scripts/heal7-service-monitor.sh
```

### 로그 파일 확인
```bash
tail -f /var/log/heal7-monitor.log
```

### 수동 서비스 시작
```bash
# 사주 서비스
cd /home/ubuntu/heal7-project/backend/services/saju-service
python3 main.py &

# 관리자 서비스  
cd /home/ubuntu/heal7-project/backend/services/dashboard-service
python3 -m uvicorn main:app --host 0.0.0.0 --port 8006 &
```

## 📞 지원
문제 발생 시 개발팀에 연락: arne40@heal7.com