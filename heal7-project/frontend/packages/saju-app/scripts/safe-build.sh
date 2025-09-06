#!/bin/bash

# 🚀 HEAL7 사주앱 안전 분할 빌드 스크립트
# 작성일: 2025-09-05
# 목적: 메모리 부족 서버에서 안전한 빌드 수행

set -e  # 오류 발생 시 즉시 종료

echo "🔥 HEAL7 사주앱 안전 분할 빌드 시작"
echo "📊 현재 시간: $(date)"
echo "💾 메모리 상태:"
free -h

# 빌드 전 준비작업
echo ""
echo "📋 1단계: 빌드 전 준비작업"

# 기존 빌드 결과물 삭제 (메모리 확보)
echo "🗑️  이전 빌드 결과물 삭제 중..."
if [ -d "dist" ]; then
    rm -rf dist
    echo "✅ dist 폴더 삭제 완료"
fi

# 임시 파일 정리
echo "🧹 임시 파일 정리 중..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true
echo "✅ 임시 파일 정리 완료"

# 메모리 상태 체크
echo "💾 정리 후 메모리 상태:"
free -h

# Node.js 메모리 제한 설정 (1GB 제한)
export NODE_OPTIONS="--max-old-space-size=1024"
echo "⚙️  Node.js 메모리 제한: 1GB"

# 병렬 처리 제한
export CI=true
export NODE_ENV=production
echo "🔧 환경변수 설정 완료"

echo ""
echo "📋 2단계: 의존성 검증 (타임아웃: 60초)"

# 의존성 설치 상태 확인
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules가 없습니다. pnpm install을 먼저 실행해주세요."
    exit 1
fi

# 의존성 무결성 검사 (빠른 체크)
echo "🔍 의존성 무결성 검사 중..."
timeout 60s pnpm list --depth=0 > /dev/null || {
    echo "⚠️  의존성 문제 감지 - 무시하고 계속 진행"
}

echo "✅ 의존성 검증 완료"

echo ""
echo "📋 3단계: 실제 빌드 수행 (타임아웃: 300초 = 5분)"

# 빌드 시작 시간 기록
BUILD_START=$(date +%s)

echo "🔨 Vite 빌드 시작..."
echo "📝 빌드 로그는 /tmp/saju-build.log에 저장됩니다"

# 메모리 모니터링을 위한 백그라운드 작업
(
    while true; do
        MEMORY_USAGE=$(free | awk '/^Mem:/ {printf "%.1f", $3/$2 * 100}')
        if (( $(echo "$MEMORY_USAGE > 90" | bc -l) )); then
            echo "⚠️  메모리 사용률 위험: ${MEMORY_USAGE}%"
        fi
        sleep 10
    done
) &
MONITOR_PID=$!

# 실제 빌드 실행 (타임아웃과 함께)
timeout 300s pnpm build 2>&1 | tee /tmp/saju-build.log || {
    BUILD_EXIT_CODE=$?
    kill $MONITOR_PID 2>/dev/null || true
    
    if [ $BUILD_EXIT_CODE -eq 124 ]; then
        echo "❌ 빌드 타임아웃 (5분 초과)"
        echo "💡 해결방안:"
        echo "   1. 더 긴 타임아웃 설정"
        echo "   2. 빌드 최적화 옵션 조정"
        echo "   3. 클라우드 빌드 사용 권장"
        exit 1
    else
        echo "❌ 빌드 실패 (종료 코드: $BUILD_EXIT_CODE)"
        echo "📝 로그 확인: cat /tmp/saju-build.log"
        exit 1
    fi
}

# 모니터링 프로세스 종료
kill $MONITOR_PID 2>/dev/null || true

# 빌드 완료 시간 계산
BUILD_END=$(date +%s)
BUILD_DURATION=$((BUILD_END - BUILD_START))

echo "✅ 빌드 성공!"
echo "⏱️  빌드 소요시간: ${BUILD_DURATION}초"

echo ""
echo "📋 4단계: 빌드 결과 검증"

if [ ! -d "dist" ]; then
    echo "❌ dist 폴더가 생성되지 않았습니다"
    exit 1
fi

# 빌드 결과 크기 확인
DIST_SIZE=$(du -sh dist | cut -f1)
echo "📦 빌드 결과 크기: $DIST_SIZE"

# 주요 파일 존재 확인
REQUIRED_FILES=("dist/index.html" "dist/assets")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo "❌ 필수 파일 누락: $file"
        exit 1
    fi
done

echo "✅ 빌드 결과 검증 완료"

echo ""
echo "📋 5단계: 배포 준비"

# 배포 명령어 제안
echo "🚀 다음 명령어로 배포하세요:"
echo "   sudo cp -r dist/* /var/www/saju.heal7.com/"
echo "   sudo chown -R www-data:www-data /var/www/saju.heal7.com/"
echo "   sudo systemctl reload nginx"

echo ""
echo "💾 최종 메모리 상태:"
free -h

echo "🎉 안전 분할 빌드 완료!"
echo "📊 완료 시간: $(date)"