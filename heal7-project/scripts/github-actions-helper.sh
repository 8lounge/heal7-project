#!/bin/bash

# 🎼 HEAL7 GitHub Actions Helper Script
# ====================================
# GitHub Actions 워크플로우를 쉽게 실행할 수 있는 도우미 스크립트

set -e

echo "🎼 HEAL7 GitHub Actions Helper"
echo "============================="
echo ""

# 사용법 표시
show_usage() {
    echo "사용법: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  frontend          - Frontend 빌드 실행"
    echo "  backend           - Backend 서비스들 빌드 실행"
    echo "  deploy            - 배포 오케스트레이션 실행"
    echo "  select <service>  - 특정 서비스만 배포"
    echo "  status            - 워크플로우 상태 확인"
    echo "  list              - 사용 가능한 워크플로우 목록"
    echo "  help              - 이 도움말 표시"
    echo ""
    echo "Service options for 'select':"
    echo "  all-services, frontend-only, saju-service-only,"
    echo "  crawling-service-only, paperwork-service-only,"
    echo "  ai-monitoring-only, dashboard-service-only, backend-services-only"
    echo ""
    echo "Examples:"
    echo "  $0 frontend"
    echo "  $0 select saju-service-only"
    echo "  $0 deploy"
}

# GitHub CLI 설치 확인
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        echo "❌ GitHub CLI (gh)가 설치되어 있지 않습니다."
        echo "설치 방법: https://cli.github.com/"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo "❌ GitHub CLI에 로그인되어 있지 않습니다."
        echo "실행: gh auth login"
        exit 1
    fi
}

# 워크플로우 실행
run_workflow() {
    local workflow_name="$1"
    local inputs="$2"
    
    echo "🚀 워크플로우 실행중: $workflow_name"
    
    if [[ -n "$inputs" ]]; then
        gh workflow run "$workflow_name" $inputs
    else
        gh workflow run "$workflow_name"
    fi
    
    echo "✅ 워크플로우가 시작되었습니다."
    echo "📊 상태 확인: gh workflow list"
    echo "📋 로그 확인: gh run list --workflow=\"$workflow_name\""
}

# 워크플로우 상태 확인
check_status() {
    echo "📊 워크플로우 상태:"
    gh workflow list
    echo ""
    echo "최근 실행 로그:"
    gh run list --limit 5
}

# 워크플로우 목록 표시
list_workflows() {
    echo "📋 사용 가능한 워크플로우:"
    echo ""
    echo "🎨 frontend-build-deploy.yml"
    echo "   - Frontend 빌드 및 배포"
    echo "   - 트리거: heal7-project/frontend/ 경로 변경시 자동"
    echo ""
    echo "🎼 backend-services-build.yml"
    echo "   - Backend 서비스들 빌드 및 테스트"  
    echo "   - 5개 서비스 (saju, crawling, paperwork, ai-monitoring, dashboard)"
    echo ""
    echo "🚀 service-deployment.yml"
    echo "   - 서비스 배포 오케스트레이션"
    echo "   - 빌드 완료 후 자동 실행 또는 수동 실행"
    echo ""
    echo "🎯 service-selector.yml"
    echo "   - 수동 서비스 선택 및 배포"
    echo "   - 개별 서비스 또는 그룹 배포 가능"
    echo ""
    echo "⚠️  build-and-deploy.yml (Deprecated)"
    echo "   - 레거시 워크플로우 (사용 비권장)"
}

# 메인 로직
main() {
    check_gh_cli
    
    case "$1" in
        "frontend")
            run_workflow "frontend-build-deploy.yml"
            ;;
        "backend") 
            run_workflow "backend-services-build.yml"
            ;;
        "deploy")
            run_workflow "service-deployment.yml"
            ;;
        "select")
            if [[ -z "$2" ]]; then
                echo "❌ 서비스를 선택해주세요."
                echo "예: $0 select saju-service-only"
                exit 1
            fi
            run_workflow "service-selector.yml" "--field target_service=$2"
            ;;
        "status")
            check_status
            ;;
        "list")
            list_workflows
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        "")
            echo "❌ 명령어를 입력해주세요."
            show_usage
            exit 1
            ;;
        *)
            echo "❌ 알 수 없는 명령어: $1"
            show_usage
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@"