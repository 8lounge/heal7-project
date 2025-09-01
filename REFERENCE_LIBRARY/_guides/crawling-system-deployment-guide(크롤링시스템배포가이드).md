# 🚀 크롤링 시스템 완전 배포 가이드 v2.0

> **Zero-to-Production**: 문서 한 장으로 완전 재현  
> **플랫폼**: Ubuntu 24.04 + NGINX + SSL  
> **자동화**: GitHub Actions CI/CD

## 🎯 배포 아키텍처

```
GitHub Repository
    ↓ push to main
GitHub Actions
    ↓ build & deploy
Ubuntu Server
    ↓ NGINX reverse proxy  
https://crawling.heal7.com
```

## 📋 사전 요구사항

### 시스템 환경
```bash
# OS: Ubuntu 24.04 LTS
# Node.js: 24.0.0+
# NGINX: 1.24.0+
# SSL: Let's Encrypt
# Domain: crawling.heal7.com
```

### 필수 디렉터리 구조
```bash
/home/ubuntu/heal7-project/
├── frontend/                 # React 앱
├── backend/                  # FastAPI 서버
└── .github/workflows/        # CI/CD 파이프라인

/var/www/crawling.heal7.com/  # NGINX 웹루트
└── (빌드 결과물)

/etc/nginx/sites-enabled/     # NGINX 설정
└── crawling.heal7.com
```

## 🔧 1단계: 프로젝트 설정

### Git Repository 클론
```bash
cd /home/ubuntu
git clone https://github.com/8lounge/heal7-project.git
cd heal7-project/frontend
```

### Node.js 환경 설정
```bash
# Node.js 24 설치 (Ubuntu)
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs

# 버전 확인
node --version  # v24.0.0+
npm --version   # 11.0.0+
```

### 프로젝트 의존성 설치
```bash
cd /home/ubuntu/heal7-project/frontend
npm install

# 필수 의존성 확인
npm list react framer-motion @tanstack/react-query
```

## 🏗️ 2단계: 컴포넌트 구성

### 크롤링 전용 엔트리포인트 생성
```bash
# 1. CrawlingApp.tsx 생성
cat > src/CrawlingApp.tsx << 'EOF'
import { motion } from 'framer-motion'
import CrawlingDashboard from './components/crawling/CrawlingDashboard'

function CrawlingApp() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900/50 to-slate-900">
      <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-blue-900/40 to-black/70" />
      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <CrawlingDashboard />
        </motion.div>
      </div>
    </div>
  )
}

export default CrawlingApp
EOF

# 2. main.tsx 수정
sed -i 's/import App from .\/App/import CrawlingApp from .\/CrawlingApp/' src/main.tsx
sed -i 's/<App \/>/<CrawlingApp \/>/' src/main.tsx
```

### HTML 템플릿 수정
```bash
# index.html을 크롤링 시스템용으로 변경
cat > index.html << 'EOF'
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>🔍 HEAL7 크롤링 시스템 - 3-Tier 데이터 수집 대시보드</title>
    <meta name="description" content="고급 3-Tier 크롤링 시스템과 멀티모달 AI 분석을 통한 데이터 수집 플랫폼" />
    <meta name="keywords" content="크롤링, 데이터 수집, AI 분석, httpx, playwright, selenium, 웹 스크래핑" />
    
    <!-- Open Graph -->
    <meta property="og:title" content="HEAL7 크롤링 시스템 - 3-Tier 데이터 수집" />
    <meta property="og:description" content="고급 3-Tier 크롤링 시스템과 멀티모달 AI 분석 플랫폼" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://crawling.heal7.com" />
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/crystal-ball.svg" sizes="any" />
    
    <!-- PWA -->
    <link rel="manifest" href="/manifest.json" />
    <meta name="theme-color" content="#0F172A" />
    
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body {
        font-family: 'Pretendard', sans-serif;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
        color: #E2E8F0;
        overflow-x: hidden;
        min-height: 100vh;
      }
      .glass-effect {
        backdrop-filter: blur(16px);
        background: rgba(15, 23, 42, 0.3);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered: ', registration))
            .catch(registrationError => console.log('SW registration failed: ', registrationError));
        });
      }
      
      window.CRAWLING_SYSTEM = {
        version: '2.0.0',
        features: ['glassmorphism', 'drag-drop', 'real-time-monitoring', 'system-settings'],
        theme: 'dark',
        api_endpoint: '/api'
      };
    </script>
  </body>
</html>
EOF
```

## ⚡ 3단계: 빌드 & 배포

### 로컬 빌드
```bash
# 1. TypeScript 검사 + Vite 빌드
npm run build

# 2. 빌드 결과 확인
ls -la dist/
# 예상 파일:
# index.html (3KB)
# assets/index-*.css (97KB)
# assets/index-*.js (183KB)  
# assets/react-vendor-*.js (11KB)
# assets/ui-vendor-*.js (114KB)
# assets/three-vendor-*.js (173KB)
```

### 웹서버 배포
```bash
# 1. 웹루트 디렉터리 생성
sudo mkdir -p /var/www/crawling.heal7.com
sudo chown ubuntu:ubuntu /var/www/crawling.heal7.com

# 2. 빌드 결과 복사
cp -r dist/* /var/www/crawling.heal7.com/

# 3. 권한 설정
sudo chown -R www-data:www-data /var/www/crawling.heal7.com
sudo chmod -R 755 /var/www/crawling.heal7.com
```

## 🌐 4단계: NGINX 설정

### SSL 인증서 설정
```bash
# Let's Encrypt 인증서 발급
sudo certbot --nginx -d crawling.heal7.com
```

### NGINX 가상호스트 구성
```bash
# /etc/nginx/sites-available/crawling.heal7.com
sudo tee /etc/nginx/sites-available/crawling.heal7.com << 'EOF'
server {
    server_name crawling.heal7.com;
    
    # Let's Encrypt challenge 경로
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    # React 정적 파일 서빙
    location / {
        try_files $uri $uri/ /index.html;
        root /var/www/crawling.heal7.com;
        
        expires 1y;
        add_header Cache-Control "public, no-transform";
    }

    # API 프록시 (백엔드와 연결)
    location /api/ {
        proxy_pass http://localhost:8003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        proxy_buffer_size 64k;
        proxy_buffers 8 64k;
        proxy_busy_buffers_size 128k;
    }
    
    # WebSocket 전용 프록시
    location /ws {
        proxy_pass http://localhost:8003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
    
    # FastAPI 문서
    location /docs {
        proxy_pass http://localhost:8003/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 헬스체크
    location /health {
        proxy_pass http://localhost:8003/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 로그 설정
    access_log /var/log/nginx/crawling.heal7.com.access.log;
    error_log /var/log/nginx/crawling.heal7.com.error.log;
    
    # gzip 압축
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/crawling.heal7.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/crawling.heal7.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = crawling.heal7.com) {
        return 301 https://$host$request_uri;
    }
    
    listen 80;
    server_name crawling.heal7.com;
    return 404;
}
EOF

# 사이트 활성화
sudo ln -sf /etc/nginx/sites-available/crawling.heal7.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🤖 5단계: GitHub Actions CI/CD

### 워크플로우 파일 생성
```bash
# .github/workflows/frontend-build-deploy.yml
mkdir -p .github/workflows
cat > .github/workflows/frontend-build-deploy.yml << 'EOF'
name: 🎨 Frontend Build & Deploy

on:
  push:
    branches: [ main ]
    paths: 
      - 'heal7-project/frontend/**'
  workflow_dispatch:

jobs:
  frontend-build-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js 24
      uses: actions/setup-node@v4
      with:
        node-version: '24'
        cache: 'npm'
        cache-dependency-path: heal7-project/frontend/package-lock.json
    
    - name: Install dependencies
      working-directory: heal7-project/frontend
      run: npm ci
    
    - name: Type check
      working-directory: heal7-project/frontend
      run: npm run type-check
    
    - name: Build for production
      working-directory: heal7-project/frontend
      run: npm run build
    
    - name: Deploy to server
      working-directory: heal7-project/frontend
      run: |
        # 서버 배포 로직 (실제 서버 설정에 따라 조정)
        echo "Build completed successfully!"
        ls -la dist/
EOF
```

## 🔧 6단계: 백엔드 서비스 설정

### FastAPI 서버 실행
```bash
# 크롤링 서비스 백엔드 실행
cd /home/ubuntu/heal7-project/backend/services/crawling-service
python3 -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload

# 헬스체크 확인  
curl http://localhost:8003/health
```

### 서비스 자동 시작 (Systemd)
```bash
# /etc/systemd/system/crawling-backend.service
sudo tee /etc/systemd/system/crawling-backend.service << 'EOF'
[Unit]
Description=HEAL7 Crawling Service Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/heal7-project/backend/services/crawling-service
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8003
Restart=always
RestartSec=3

Environment=PYTHONPATH=/home/ubuntu/heal7-project/backend
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# 서비스 활성화
sudo systemctl daemon-reload
sudo systemctl enable crawling-backend
sudo systemctl start crawling-backend
sudo systemctl status crawling-backend
```

## ⚡ 7단계: 자동 배포 스크립트

### 원클릭 배포 스크립트
```bash
# deploy-crawling.sh
cat > /home/ubuntu/scripts/deploy-crawling.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 HEAL7 크롤링 시스템 배포 시작..."

# 1. 코드 업데이트
cd /home/ubuntu/heal7-project
git pull origin main

# 2. 프론트엔드 빌드
cd frontend
npm ci
npm run build

# 3. 백업 생성
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
sudo cp -r /var/www/crawling.heal7.com /var/www/backups/crawling-${TIMESTAMP}

# 4. 새 빌드 배포
sudo cp -r dist/* /var/www/crawling.heal7.com/
sudo chown -R www-data:www-data /var/www/crawling.heal7.com

# 5. 백엔드 재시작 (필요시)
sudo systemctl restart crawling-backend

# 6. NGINX 설정 리로드
sudo nginx -t && sudo systemctl reload nginx

# 7. 배포 완료 확인
sleep 3
curl -f https://crawling.heal7.com/health || echo "❌ 헬스체크 실패"

echo "✅ 크롤링 시스템 배포 완료!"
echo "🔗 https://crawling.heal7.com"
EOF

chmod +x /home/ubuntu/scripts/deploy-crawling.sh
```

## 🧪 8단계: 검증 & 테스트

### 배포 검증 체크리스트
```bash
# ✅ 1. 웹사이트 접근성
curl -I https://crawling.heal7.com
# 응답: HTTP/2 200

# ✅ 2. API 연결성  
curl https://crawling.heal7.com/health
# 응답: {"status": "healthy", "service": "crawling-service"}

# ✅ 3. WebSocket 연결
# 브라우저 개발자 도구에서 확인
# ws://crawling.heal7.com/ws 연결 성공

# ✅ 4. 정적 파일 서빙
curl -I https://crawling.heal7.com/assets/index-*.js
# 응답: HTTP/2 200, Content-Type: text/javascript

# ✅ 5. PWA 매니페스트
curl https://crawling.heal7.com/manifest.json
# 응답: 유효한 PWA 매니페스트
```

### 성능 벤치마크
```bash
# Lighthouse 성능 테스트
npm install -g lighthouse
lighthouse https://crawling.heal7.com --output html --output-path ./lighthouse-report.html

# 목표 스코어:
# Performance: 90+
# Accessibility: 100  
# Best Practices: 100
# SEO: 90+
```

## 🔄 9단계: 유지보수 가이드

### 일상 모니터링
```bash
# 시스템 상태 확인
sudo systemctl status nginx crawling-backend
sudo lsof -i :8003

# 로그 모니터링
sudo tail -f /var/log/nginx/crawling.heal7.com.access.log
sudo journalctl -u crawling-backend -f

# 디스크 용량 확인
df -h /var/www/crawling.heal7.com
```

### 업데이트 프로세스
```bash
# 1. 코드 변경 후
git add . && git commit -m "feat: 새 기능 추가"
git push origin main

# 2. 자동 배포 (GitHub Actions) 또는
/home/ubuntu/scripts/deploy-crawling.sh

# 3. 배포 확인
curl https://crawling.heal7.com/health
```

## 🆘 트러블슈팅

### 일반적인 문제 해결

#### 문제 1: 사주사이트로 리디렉트
```bash
# 원인: 잘못된 빌드 배포
# 해결: HTML 템플릿 확인 후 재빌드
grep -i "saju\|운세" /var/www/crawling.heal7.com/index.html
# 발견되면 올바른 크롤링용 HTML로 교체 후 재배포
```

#### 문제 2: API 연결 실패
```bash
# 백엔드 서비스 상태 확인
sudo systemctl status crawling-backend
sudo lsof -i :8003

# 재시작
sudo systemctl restart crawling-backend
```

#### 문제 3: 빌드 실패
```bash
# Node.js 버전 확인
node --version  # 24.0.0+ 필요

# 캐시 정리 후 재설치
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📋 배포 체크리스트

### 배포 전 확인사항
- [ ] Node.js 24.0.0+ 설치
- [ ] 의존성 설치 완료 (`npm ci`)
- [ ] TypeScript 오류 없음 (`npm run type-check`)
- [ ] 빌드 성공 (`npm run build`)
- [ ] HTML 템플릿 크롤링용으로 설정
- [ ] 백엔드 서비스 (포트 8003) 실행 중

### 배포 후 확인사항
- [ ] 웹사이트 접근 가능 (https://crawling.heal7.com)
- [ ] API 헬스체크 성공 (/health)
- [ ] WebSocket 연결 성공 (/ws)
- [ ] 정적 파일 로딩 성공
- [ ] 브라우저 콘솔 오류 없음
- [ ] 실시간 기능 동작 확인

---

**🎯 배포 목표**: 5분 이내 완료, 무중단 서비스  
**🔄 롤백 계획**: 백업 디렉터리 자동 생성, 즉시 복구 가능  
**📊 성능 기준**: Lighthouse 90+ 스코어 유지

*이 가이드로 완전 동일한 크롤링 시스템 배포 가능*