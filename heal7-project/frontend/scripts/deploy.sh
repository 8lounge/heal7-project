#!/bin/bash

# 배포 스크립트

deploy_service() {
  local service=$1
  echo "🚀 Deploying $service..."
  
  # 빌드
  echo "🔨 Building $service..."
  pnpm build:$service
  
  if [ $? -ne 0 ]; then
    echo "❌ Build failed for $service"
    exit 1
  fi
  
  # 배포 (MANUAL MODE - AUTO DEPLOYMENT DISABLED)
  case $service in
    "saju")
      echo "📦 Build ready for manual deployment to saju.heal7.com..."
      echo "🔧 Manual deployment commands:"
      echo "   sudo cp -r packages/saju-app/dist/* /var/www/saju.heal7.com/"
      # zodiac-images 보존 참고사항
      echo "📝 Note: Preserve zodiac-images from backup if needed"
      echo "   sudo cp -r /var/www/saju.heal7.com.backup/zodiac-images /var/www/saju.heal7.com/"
      ;;
    "crawling")
      echo "📦 Build ready for manual deployment to crawling.heal7.com..."
      echo "🔧 Manual deployment commands:"
      echo "   sudo cp -r packages/crawling-app/dist/* /var/www/crawling.heal7.com/"
      ;;
    "admin")
      echo "📦 Build ready for manual deployment to admin.heal7.com..."
      echo "🔧 Manual deployment commands:"
      echo "   sudo cp -r packages/admin-app/dist/* /var/www/admin.heal7.com/"
      ;;
    "cube")
      echo "📦 Build ready for manual deployment to cube module service..."
      echo "🔧 Manual deployment will be configured separately"
      ;;
  esac
  
  echo ""
  echo "⚠️  AUTO DEPLOYMENT DISABLED - USE MANUAL DEPLOYMENT"
  echo "🔧 After manual file copy, run:"
  echo "   sudo chown -R www-data:www-data /var/www/$service.heal7.com/"
  echo "   sudo chmod -R 755 /var/www/$service.heal7.com/"
  echo "   sudo systemctl reload nginx"
  echo "✅ $service deployment completed"
}

trigger_github_deploy() {
  local service=$1
  echo "🚀 Triggering GitHub Actions deployment for $service..."
  
  if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Install with: sudo apt install gh"
    exit 1
  fi
  
  gh workflow run "$service-app.yml" \
    --field deploy=true \
    --ref main
    
  echo "✅ GitHub Actions workflow triggered"
  echo "👀 Check status: gh workflow list"
}

case ${1:-"help"} in
  "saju"|"crawling"|"admin"|"cube")
    if [[ "$2" == "--github" ]]; then
      trigger_github_deploy $1
    else
      deploy_service $1
    fi
    ;;
  *)
    echo "Usage: $0 [saju|crawling|admin|cube] [--github]"
    echo ""
    echo "Examples:"
    echo "  $0 saju           # Local deployment"
    echo "  $0 saju --github  # GitHub Actions deployment"
    echo "  $0 crawling       # Local crawling deployment"
    echo "  $0 admin          # Local admin deployment"
    ;;
esac