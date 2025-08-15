#!/bin/bash
# Heal7 통합 플랫폼 배포 스크립트
# React 19 + Next.js + FastAPI 통합 배포

set -e

HEAL7_ROOT="/home/ubuntu/heal7-unified"
LOG_FILE="/tmp/heal7-unified-deploy.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# 메모리 사용량 체크
check_memory() {
    log "메모리 사용량 체크 중..."
    local available_mb=$(free -m | awk 'NR==2{printf "%.0f", $7}')
    
    if [ "$available_mb" -lt 300 ]; then
        warning "사용 가능한 메모리가 부족합니다 (${available_mb}MB). 배포를 계속하시겠습니까? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            error "배포를 중단합니다."
            exit 1
        fi
    fi
    
    success "메모리 체크 완료: ${available_mb}MB 사용 가능"
}

# 프론트엔드 빌드 (GitHub Actions 우선)
build_frontend() {
    log "프론트엔드 빌드 시작..."
    cd "$HEAL7_ROOT/frontend"
    
    # GitHub Actions으로 빌드된 파일이 있는지 확인
    if [ -d ".next" ] && [ -f ".next/BUILD_ID" ]; then
        success "기존 빌드 파일 발견, 빌드 건너뜀"
        return 0
    fi
    
    # 로컬 빌드 (최소 메모리 사용)
    warning "로컬에서 빌드를 시작합니다. 메모리 사용량이 높을 수 있습니다."
    
    export NODE_OPTIONS="--max-old-space-size=400"
    
    if npm run build; then
        success "프론트엔드 빌드 완료"
    else
        error "프론트엔드 빌드 실패"
        exit 1
    fi
}

# 백엔드 설정
setup_backend() {
    log "백엔드 설정 중..."
    cd "$HEAL7_ROOT/backend"
    
    # Python 가상환경 확인
    if [ ! -d "venv" ]; then
        log "Python 가상환경 생성 중..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # 의존성 설치
    if pip install -r requirements.txt --quiet; then
        success "백엔드 의존성 설치 완료"
    else
        error "백엔드 의존성 설치 실패"
        exit 1
    fi
}

# 서비스 배포
deploy_services() {
    log "서비스 배포 시작..."
    
    # 1. 백엔드 서버 시작
    cd "$HEAL7_ROOT/backend"
    source venv/bin/activate
    
    log "FastAPI 서버 시작 (포트 8000)..."
    nohup python main.py > "/tmp/heal7-unified-backend.log" 2>&1 &
    echo $! > "/tmp/heal7-unified-backend.pid"
    
    # 백엔드 시작 대기
    sleep 5
    
    if curl -s http://localhost:8000/health > /dev/null; then
        success "백엔드 서버 시작 완료"
    else
        error "백엔드 서버 시작 실패"
        exit 1
    fi
    
    # 2. 프론트엔드 정적 파일 배포
    log "프론트엔드 정적 파일 배포 중..."
    
    # Next.js 빌드 파일을 Nginx 디렉터리로 복사
    local services=("index" "saju" "test" "admin")
    
    for service in "${services[@]}"; do
        local domain_dir="/var/www/${service}.heal7.com"
        
        if [ "$service" = "index" ]; then
            domain_dir="/var/www/heal7.com"
        fi
        
        log "${service} 서비스 정적 파일 배포..."
        
        sudo mkdir -p "$domain_dir"
        sudo cp -r "$HEAL7_ROOT/frontend/.next/static" "$domain_dir/_next/"
        sudo cp -r "$HEAL7_ROOT/frontend/public"/* "$domain_dir/" 2>/dev/null || true
        
        # 서비스별 HTML 생성
        cat > "/tmp/${service}-index.html" << EOF
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heal7 ${service^} Service</title>
    <link rel="icon" href="/favicon.ico">
</head>
<body>
    <div id="__next"></div>
    <script>
        // 서비스별 라우팅
        window.location.replace('/${service}');
    </script>
</body>
</html>
EOF
        sudo cp "/tmp/${service}-index.html" "$domain_dir/index.html"
        sudo chown -R www-data:www-data "$domain_dir"
        
        success "${service} 서비스 배포 완료"
    done
}

# Nginx 설정 업데이트
update_nginx() {
    log "Nginx 설정 업데이트 중..."
    
    # 통합 Nginx 설정 생성
    cat > "/tmp/heal7-unified.conf" << 'EOF'
# Heal7 통합 플랫폼 Nginx 설정
upstream heal7_backend {
    server 127.0.0.1:8000;
}

# heal7.com (메인)
server {
    listen 443 ssl http2;
    server_name heal7.com www.heal7.com;
    
    ssl_certificate /etc/letsencrypt/live/heal7.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/heal7.com/privkey.pem;
    
    root /var/www/heal7.com;
    index index.html;
    
    location / {
        try_files $uri $uri/ @backend;
    }
    
    location /api/ {
        proxy_pass http://heal7_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location @backend {
        proxy_pass http://heal7_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# saju.heal7.com
server {
    listen 443 ssl http2;
    server_name saju.heal7.com;
    
    ssl_certificate /etc/letsencrypt/live/saju.heal7.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/saju.heal7.com/privkey.pem;
    
    location / {
        proxy_pass http://heal7_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# test.heal7.com  
server {
    listen 443 ssl http2;
    server_name test.heal7.com;
    
    ssl_certificate /etc/letsencrypt/live/test.heal7.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/test.heal7.com/privkey.pem;
    
    location / {
        proxy_pass http://heal7_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# admin.heal7.com
server {
    listen 443 ssl http2;
    server_name admin.heal7.com;
    
    ssl_certificate /etc/letsencrypt/live/admin.heal7.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/admin.heal7.com/privkey.pem;
    
    location / {
        proxy_pass http://heal7_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
    
    sudo cp "/tmp/heal7-unified.conf" "/etc/nginx/sites-available/heal7-unified.conf"
    sudo ln -sf "/etc/nginx/sites-available/heal7-unified.conf" "/etc/nginx/sites-enabled/"
    
    if sudo nginx -t; then
        sudo systemctl reload nginx
        success "Nginx 설정 업데이트 완료"
    else
        error "Nginx 설정 오류"
        exit 1
    fi
}

# 배포 후 확인
verify_deployment() {
    log "배포 상태 확인 중..."
    
    local urls=(
        "https://heal7.com"
        "https://saju.heal7.com"
        "https://test.heal7.com" 
        "https://admin.heal7.com"
    )
    
    for url in "${urls[@]}"; do
        if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|301\|302"; then
            success "$url - 정상 응답"
        else
            warning "$url - 응답 없음"
        fi
    done
}

# 메인 실행
main() {
    log "🚀 Heal7 통합 플랫폼 배포 시작 - $TIMESTAMP"
    
    check_memory
    build_frontend
    setup_backend
    deploy_services
    update_nginx
    verify_deployment
    
    success "🎉 배포 완료!"
    log "로그 파일: $LOG_FILE"
    
    # 메모리 사용량 출력
    echo -e "\n📊 현재 시스템 상태:"
    free -h
}

# 스크립트 실행
main "$@"