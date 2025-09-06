#!/bin/bash

# 🚀 HEAL7 사주앱 최적화된 빌드 스크립트 (2GB 메모리 대응)
# 작성일: 2025-09-05
# 메모리 상황: 1.9GB 총 메모리 (506MB 여유)

set -e

echo "🚀 HEAL7 사주앱 최적화 빌드 시작"
echo "📊 현재 시간: $(date)"

# 현재 메모리 상태 확인
echo "💾 현재 메모리 상태:"
free -h

# 메모리가 충분하므로 더 관대한 설정
export NODE_OPTIONS="--max-old-space-size=1500"  # 1.5GB 허용
export NODE_ENV=production

echo "⚙️  Node.js 메모리 제한: 1.5GB"

echo ""
echo "📋 1단계: 빌드 환경 준비"

# 작업 디렉토리로 이동
cd /home/ubuntu/heal7-project/frontend/packages/saju-app

# 이전 빌드 정리
if [ -d "dist" ]; then
    echo "🗑️  이전 빌드 결과 정리 중..."
    rm -rf dist
    echo "✅ 정리 완료"
fi

# 임시 파일 정리
echo "🧹 임시 파일 정리..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name ".vite" -type d -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "📋 2단계: 의존성 확인"

# 빠른 의존성 체크
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules 없음. 의존성 설치 필요:"
    echo "   cd /home/ubuntu/heal7-project/frontend/packages/saju-app"
    echo "   pnpm install"
    exit 1
fi

echo "✅ 의존성 확인 완료"

echo ""
echo "📋 3단계: 실제 빌드 수행"

BUILD_START=$(date +%s)

# 메모리 모니터링 (백그라운드)
(
    while true; do
        MEMORY_USAGE=$(free | awk '/^Mem:/ {printf "%.1f", $3/$2 * 100}')
        AVAILABLE_MB=$(free -m | awk '/^Mem:/ {print $7}')
        
        if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
            echo "⚠️  메모리 사용률: ${MEMORY_USAGE}% (여유: ${AVAILABLE_MB}MB)"
        fi
        
        if [ "$AVAILABLE_MB" -lt 200 ]; then
            echo "🚨 메모리 부족 경고! 여유 메모리: ${AVAILABLE_MB}MB"
        fi
        
        sleep 15
    done
) &
MONITOR_PID=$!

echo "🔨 Vite 빌드 시작 (타임아웃: 8분)..."

# 빌드 실행 (더 여유로운 타임아웃)
timeout 480s pnpm build 2>&1 | tee /tmp/saju-build-$(date +%Y%m%d-%H%M%S).log || {
    EXIT_CODE=$?
    kill $MONITOR_PID 2>/dev/null || true
    
    if [ $EXIT_CODE -eq 124 ]; then
        echo "❌ 빌드 타임아웃 (8분 초과)"
        echo "💡 대안:"
        echo "   1. GitHub Actions 원격 빌드 권장"
        echo "   2. 빌드 최적화 설정 조정 필요"
    else
        echo "❌ 빌드 실패 (코드: $EXIT_CODE)"
        echo "📝 로그 확인: ls /tmp/saju-build-*.log"
    fi
    exit 1
}

kill $MONITOR_PID 2>/dev/null || true

BUILD_END=$(date +%s)
BUILD_DURATION=$((BUILD_END - BUILD_START))

echo "✅ 빌드 완료!"
echo "⏱️  빌드 시간: ${BUILD_DURATION}초"

echo ""
echo "📋 4단계: 빌드 검증 및 배포 준비"

# 빌드 결과 검증
if [ ! -d "dist" ]; then
    echo "❌ dist 폴더 생성 실패"
    exit 1
fi

# 파일 크기 및 구조 확인
DIST_SIZE=$(du -sh dist | cut -f1)
FILE_COUNT=$(find dist -type f | wc -l)

echo "📦 빌드 결과:"
echo "   - 크기: $DIST_SIZE"
echo "   - 파일 수: $FILE_COUNT"
echo "   - 주요 파일:"

ls -la dist/ | head -10

# 핵심 파일 존재 확인
CORE_FILES=("dist/index.html" "dist/assets")
for file in "${CORE_FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo "❌ 핵심 파일 누락: $file"
        exit 1
    fi
done

echo "✅ 빌드 검증 완료"

echo ""
echo "📋 5단계: 배포 명령어 제공"

echo "🚀 이제 다음 명령어로 배포하세요:"
echo ""
echo "# 1. 기존 파일 백업"
echo "sudo cp -r /var/www/saju.heal7.com /var/www/saju.heal7.com.backup-\$(date +%Y%m%d-%H%M%S)"
echo ""
echo "# 2. 새 빌드 배포"
echo "sudo cp -r dist/* /var/www/saju.heal7.com/"
echo ""
echo "# 3. 권한 설정"
echo "sudo chown -R www-data:www-data /var/www/saju.heal7.com/"
echo ""
echo "# 4. 서비스 재시작"
echo "sudo systemctl reload nginx"
echo ""
echo "# 5. 상태 확인"
echo "curl -I https://saju.heal7.com"

echo ""
echo "💾 최종 메모리 상태:"
free -h

echo ""
echo "🎉 최적화된 빌드 완료!"
echo "📊 완료 시간: $(date)"
echo "🔗 배포 후 확인: https://saju.heal7.com"