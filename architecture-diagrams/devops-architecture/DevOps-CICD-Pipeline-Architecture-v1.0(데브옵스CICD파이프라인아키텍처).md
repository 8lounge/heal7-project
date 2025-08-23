# ⚙️ HEAL7 DevOps CI/CD 파이프라인 아키텍처 v1.0

> **프로젝트**: HEAL7 옴니버스 플랫폼 DevOps 전략  
> **버전**: v1.0.0  
> **작성일**: 2025-08-18  
> **목적**: 빠른 개발 주기와 안정적 배포를 위한 완전 자동화 파이프라인  
> **범위**: CI/CD, IaC, 컨테이너화, 모니터링, 품질 게이트

---

## 🎯 **DevOps 철학 및 전략**

### **🚀 핵심 DevOps 원칙**
```yaml
devops_principles:
  shift_left_security: "개발 초기 단계부터 보안 내재화"
  everything_as_code: "인프라, 구성, 정책 모든 것을 코드로 관리"
  fail_fast_principle: "빠른 실패를 통한 신속한 학습"
  continuous_improvement: "지속적 개선과 최적화"
  observability_first: "관찰가능성 우선 설계"
  
delivery_metrics: # DORA 메트릭 기반
  deployment_frequency: "일 10회 이상 배포"
  lead_time: "커밋부터 배포까지 < 30분"
  mttr: "장애 복구 시간 < 1시간"
  change_failure_rate: "배포 실패율 < 5%"
```

### **🏗️ 레고블럭 모듈형 파이프라인**
```yaml
modular_pipeline_philosophy:
  pipeline_as_lego_blocks: "재사용 가능한 파이프라인 컴포넌트"
  environment_agnostic: "환경 독립적 파이프라인 설계"
  service_specific_pipelines: "서비스별 맞춤형 파이프라인"
  shared_pipeline_libraries: "공통 파이프라인 라이브러리"
```

---

## 🔄 **전체 CI/CD 파이프라인 아키텍처**

### **📊 파이프라인 전체 흐름**

#### **1. 소스 코드 → 프로덕션 전체 여정**
```mermaid
graph TD
    A[개발자 커밋] --> B{PR 생성}
    B --> C[CI Pipeline 시작]
    
    C --> D[코드 품질 검사]
    C --> E[보안 스캔]
    C --> F[단위 테스트]
    C --> G[통합 테스트]
    
    D --> H{품질 게이트 통과?}
    E --> H
    F --> H
    G --> H
    
    H -->|Pass| I[아티팩트 빌드]
    H -->|Fail| J[PR 블로킹]
    
    I --> K[컨테이너 이미지 빌드]
    K --> L[보안 스캔 (이미지)]
    L --> M[레지스트리 Push]
    
    M --> N[CD Pipeline 시작]
    N --> O[Dev 환경 배포]
    O --> P[E2E 테스트]
    P --> Q{테스트 통과?}
    
    Q -->|Pass| R[Staging 배포]
    Q -->|Fail| S[롤백 & 알림]
    
    R --> T[성능 테스트]
    R --> U[보안 테스트]
    R --> V[UAT]
    
    T --> W{배포 승인?}
    U --> W
    V --> W
    
    W -->|Approved| X[Production 배포]
    W -->|Rejected| Y[수정 요청]
    
    X --> Z[배포 후 모니터링]
```

#### **2. 파이프라인 구성 요소**
```yaml
pipeline_components:
  source_control: # 소스 코드 관리
    platform: "GitHub Enterprise"
    branching_strategy: "GitHub Flow + Environment Branches"
    protection_rules: "main branch 보호, 필수 리뷰"
    
  ci_platform: # 지속적 통합
    primary: "GitHub Actions"
    secondary: "Jenkins (복잡한 워크플로우)"
    runners: "Self-hosted + GitHub-hosted"
    
  cd_platform: # 지속적 배포
    gitops_tool: "ArgoCD"
    deployment_tool: "Helm + Kustomize"
    approval_system: "GitHub Environments"
    
  artifact_storage: # 아티팩트 저장소
    container_registry: "Amazon ECR"
    package_registry: "GitHub Packages"
    dependency_cache: "GitHub Actions Cache"
    
  infrastructure: # 인프라
    iac_tool: "Terraform + Terragrunt"
    container_platform: "Amazon EKS"
    service_mesh: "Istio"
    secrets_management: "AWS Secrets Manager + External Secrets"
```

---

## 🔧 **CI (Continuous Integration) 상세 설계**

### **📋 GitHub Actions 워크플로우**

#### **1. 메인 CI 워크플로우**
```yaml
# .github/workflows/ci-main.yml
name: 🚀 HEAL7 Main CI Pipeline

on:
  pull_request:
    branches: [main, develop]
    paths-ignore: ['docs/**', '*.md']
  push:
    branches: [main]

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'
  DOCKER_BUILDKIT: 1

jobs:
  # 🔍 코드 품질 및 보안 검사
  code-quality:
    name: 📊 Code Quality & Security
    runs-on: ubuntu-latest
    steps:
      - name: 🛒 Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # SonarQube 분석용
          
      - name: 🔍 Run SonarQube Scan
        uses: sonarqube-quality-gate-action@master
        with:
          scanMetadataReportFile: target/sonar/report-task.txt
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
          
      - name: 🛡️ Security Scan (Bandit)
        run: |
          pip install bandit[toml]
          bandit -r backend/ -f json -o security-report.json
          
      - name: 🔐 Dependency Security Scan
        uses: pypa/gh-action-pip-audit@v1.0.8
        with:
          inputs: backend/requirements.txt
          
      - name: 📤 Upload Security Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            security-report.json
            pip-audit-report.json

  # 🧪 프론트엔드 테스트
  frontend-tests:
    name: 🎨 Frontend Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend
    steps:
      - name: 🛒 Checkout code
        uses: actions/checkout@v4
        
      - name: 📦 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
          
      - name: 📥 Install dependencies
        run: npm ci
        
      - name: 🔍 ESLint
        run: npm run lint
        
      - name: 🎯 TypeScript Check
        run: npm run type-check
        
      - name: 🧪 Unit Tests
        run: npm run test:unit -- --coverage
        
      - name: 🎭 Component Tests (Playwright)
        run: npm run test:component
        
      - name: 📊 Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/lcov.info
          flags: frontend

  # 🐍 백엔드 테스트
  backend-tests:
    name: 🔧 Backend Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: heal7_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    defaults:
      run:
        working-directory: ./backend
    steps:
      - name: 🛒 Checkout code
        uses: actions/checkout@v4
        
      - name: 🐍 Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
          
      - name: 📥 Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: 🔍 Flake8 Linting
        run: flake8 --config setup.cfg
        
      - name: 🧪 Unit Tests
        run: |
          pytest tests/unit/ --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost/heal7_test
          REDIS_URL: redis://localhost:6379
          
      - name: 🔗 Integration Tests
        run: |
          pytest tests/integration/ --cov-append --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost/heal7_test
          REDIS_URL: redis://localhost:6379
          
      - name: 📊 Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
          flags: backend

  # 🏗️ 빌드 및 컨테이너화
  build-and-containerize:
    name: 🐳 Build & Containerize
    needs: [code-quality, frontend-tests, backend-tests]
    runs-on: ubuntu-latest
    outputs:
      frontend-image: ${{ steps.meta-frontend.outputs.tags }}
      backend-image: ${{ steps.meta-backend.outputs.tags }}
    steps:
      - name: 🛒 Checkout code
        uses: actions/checkout@v4
        
      - name: 🔐 Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-northeast-2
          
      - name: 🔑 Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2
        
      - name: 🏷️ Extract metadata (Frontend)
        id: meta-frontend
        uses: docker/metadata-action@v5
        with:
          images: ${{ steps.login-ecr.outputs.registry }}/heal7-frontend
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            
      - name: 🏷️ Extract metadata (Backend)
        id: meta-backend
        uses: docker/metadata-action@v5
        with:
          images: ${{ steps.login-ecr.outputs.registry }}/heal7-backend
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            
      - name: 🔨 Build and push Frontend image
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: true
          tags: ${{ steps.meta-frontend.outputs.tags }}
          labels: ${{ steps.meta-frontend.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          
      - name: 🔨 Build and push Backend image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: true
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          
      - name: 🔍 Container Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta-backend.outputs.tags }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          
      - name: 📤 Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

#### **2. E2E 테스트 워크플로우**
```yaml
# .github/workflows/e2e-tests.yml
name: 🎭 E2E Tests

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      frontend-image:
        required: true
        type: string
      backend-image:
        required: true
        type: string

jobs:
  e2e-tests:
    name: 🎭 End-to-End Tests
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: 🛒 Checkout code
        uses: actions/checkout@v4
        
      - name: 🚀 Deploy to test environment
        run: |
          # Helm을 사용한 임시 환경 배포
          helm upgrade --install heal7-e2e ./k8s/helm/heal7 \
            --namespace e2e-${{ github.run_id }} \
            --create-namespace \
            --set frontend.image=${{ inputs.frontend-image }} \
            --set backend.image=${{ inputs.backend-image }} \
            --set ingress.enabled=false \
            --wait --timeout=10m
            
      - name: 📦 Setup Node.js for E2E
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: e2e/package-lock.json
          
      - name: 📥 Install E2E dependencies
        working-directory: ./e2e
        run: npm ci
        
      - name: 🎭 Install Playwright
        working-directory: ./e2e
        run: npx playwright install --with-deps
        
      - name: 🧪 Run E2E tests
        working-directory: ./e2e
        run: |
          export BASE_URL=http://heal7-frontend.e2e-${{ github.run_id }}.svc.cluster.local
          npm run test:e2e
        env:
          CI: true
          
      - name: 📊 Upload E2E artifacts
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: e2e-results
          path: |
            e2e/test-results/
            e2e/playwright-report/
            
      - name: 🧹 Cleanup test environment
        if: always()
        run: |
          helm uninstall heal7-e2e --namespace e2e-${{ github.run_id }}
          kubectl delete namespace e2e-${{ github.run_id }} --ignore-not-found
```

### **🔍 품질 게이트 및 검증**

#### **1. 종합 품질 게이트**
```yaml
quality_gates:
  code_coverage:
    frontend_threshold: "80%"
    backend_threshold: "85%"
    integration_threshold: "70%"
    
  security_requirements:
    vulnerability_threshold: "none (high/critical)"
    dependency_updates: "weekly"
    security_scan_required: true
    
  performance_requirements:
    build_time_max: "10 minutes"
    test_time_max: "15 minutes"
    image_size_max: "500MB"
    
  code_quality:
    sonarqube_gate: "passed"
    complexity_threshold: "10"
    duplication_threshold: "3%"
    
  accessibility:
    wcag_compliance: "AA"
    lighthouse_score: "> 90"
    automated_testing: true
```

#### **2. 자동화된 품질 검사**
```python
# scripts/quality-gate-checker.py
#!/usr/bin/env python3
"""
종합 품질 게이트 검사 스크립트
"""
import json
import sys
from typing import Dict, List, Any
import requests

class QualityGateChecker:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)
        self.results = []
        
    def check_code_coverage(self) -> bool:
        """코드 커버리지 검사"""
        try:
            with open('coverage/coverage-summary.json') as f:
                coverage = json.load(f)
            
            frontend_coverage = coverage.get('total', {}).get('lines', {}).get('pct', 0)
            backend_coverage = self._get_backend_coverage()
            
            frontend_pass = frontend_coverage >= self.config['coverage']['frontend_threshold']
            backend_pass = backend_coverage >= self.config['coverage']['backend_threshold']
            
            self.results.append({
                'check': 'code_coverage',
                'status': 'pass' if (frontend_pass and backend_pass) else 'fail',
                'details': {
                    'frontend': f"{frontend_coverage}%",
                    'backend': f"{backend_coverage}%"
                }
            })
            
            return frontend_pass and backend_pass
            
        except Exception as e:
            self.results.append({
                'check': 'code_coverage',
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def check_security_vulnerabilities(self) -> bool:
        """보안 취약점 검사"""
        try:
            # Trivy 결과 파싱
            with open('security-reports/trivy-results.json') as f:
                trivy_results = json.load(f)
            
            high_critical_vulns = []
            for result in trivy_results.get('Results', []):
                for vuln in result.get('Vulnerabilities', []):
                    if vuln.get('Severity') in ['HIGH', 'CRITICAL']:
                        high_critical_vulns.append(vuln)
            
            has_critical_vulns = len(high_critical_vulns) > 0
            
            self.results.append({
                'check': 'security_vulnerabilities',
                'status': 'fail' if has_critical_vulns else 'pass',
                'details': {
                    'high_critical_count': len(high_critical_vulns),
                    'vulnerabilities': high_critical_vulns[:5]  # 상위 5개만
                }
            })
            
            return not has_critical_vulns
            
        except Exception as e:
            self.results.append({
                'check': 'security_vulnerabilities',
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def check_performance_benchmarks(self) -> bool:
        """성능 벤치마크 검사"""
        try:
            # Lighthouse 결과 확인
            with open('lighthouse-results.json') as f:
                lighthouse = json.load(f)
            
            performance_score = lighthouse.get('lhr', {}).get('categories', {}).get('performance', {}).get('score', 0) * 100
            accessibility_score = lighthouse.get('lhr', {}).get('categories', {}).get('accessibility', {}).get('score', 0) * 100
            
            performance_pass = performance_score >= self.config['performance']['lighthouse_threshold']
            accessibility_pass = accessibility_score >= self.config['accessibility']['lighthouse_threshold']
            
            self.results.append({
                'check': 'performance_benchmarks',
                'status': 'pass' if (performance_pass and accessibility_pass) else 'fail',
                'details': {
                    'performance_score': f"{performance_score}%",
                    'accessibility_score': f"{accessibility_score}%"
                }
            })
            
            return performance_pass and accessibility_pass
            
        except Exception as e:
            self.results.append({
                'check': 'performance_benchmarks',
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def run_all_checks(self) -> bool:
        """모든 품질 검사 실행"""
        checks = [
            self.check_code_coverage(),
            self.check_security_vulnerabilities(),
            self.check_performance_benchmarks()
        ]
        
        all_passed = all(checks)
        
        # 결과 출력
        print("📊 Quality Gate Results:")
        print("=" * 50)
        
        for result in self.results:
            status_emoji = "✅" if result['status'] == 'pass' else "❌" if result['status'] == 'fail' else "⚠️"
            print(f"{status_emoji} {result['check']}: {result['status']}")
            
            if 'details' in result:
                for key, value in result['details'].items():
                    print(f"   {key}: {value}")
            
            if 'error' in result:
                print(f"   Error: {result['error']}")
        
        print("=" * 50)
        print(f"Overall Result: {'✅ PASSED' if all_passed else '❌ FAILED'}")
        
        return all_passed

if __name__ == "__main__":
    checker = QualityGateChecker("quality-gate-config.json")
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
```

---

## 🚀 **CD (Continuous Deployment) 상세 설계**

### **🎯 GitOps 기반 배포 전략**

#### **1. ArgoCD GitOps 워크플로우**
```yaml
# argocd/applications/heal7-frontend-dev.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: heal7-frontend-dev
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: heal7
  source:
    repoURL: https://github.com/heal7/k8s-manifests
    path: environments/dev/frontend
    targetRevision: HEAD
    helm:
      valueFiles:
        - values.yaml
        - values-dev.yaml
      parameters:
        - name: image.tag
          value: $ARGOCD_ENV_IMAGE_TAG
  destination:
    server: https://kubernetes.default.svc
    namespace: heal7-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

#### **2. 환경별 배포 전략**
```yaml
deployment_environments:
  development: # 개발 환경
    trigger: "모든 커밋 (자동)"
    approval: "불필요"
    deployment_strategy: "rolling_update"
    rollback_policy: "자동 (실패 시)"
    resource_limits: "최소 리소스"
    monitoring_level: "기본"
    
  staging: # 스테이징 환경
    trigger: "develop 브랜치 (자동)"
    approval: "팀 리드 승인"
    deployment_strategy: "blue_green"
    rollback_policy: "수동 승인"
    resource_limits: "프로덕션의 50%"
    monitoring_level: "상세"
    
  production: # 프로덕션 환경
    trigger: "main 브랜치 (수동)"
    approval: "CTO + DevOps 팀장"
    deployment_strategy: "canary"
    rollback_policy: "즉시 가능"
    resource_limits: "최대 리소스"
    monitoring_level: "전체"
```

#### **3. Canary 배포 구현**
```yaml
# k8s/canary-deployment.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: heal7-backend
  namespace: heal7-prod
spec:
  # 대상 서비스
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: heal7-backend
  
  # 프로그레시브 배포 설정
  progressDeadlineSeconds: 60
  
  # HPA 참조
  autoscalerRef:
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    name: heal7-backend
  
  # 서비스 포트
  service:
    port: 8080
    targetPort: 8080
    gateways:
      - heal7-gateway
    hosts:
      - api.heal7.com
  
  # 분석 설정
  analysis:
    # 분석 간격
    interval: 1m
    # 분석 최대 시간
    threshold: 5
    # 최대 가중치
    maxWeight: 50
    # 가중치 증가 단계
    stepWeight: 10
    
    # 성공 메트릭
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
      - name: error-rate
        thresholdRange:
          max: 1
        interval: 30s
    
    # 웹훅 (Slack 알림)
    webhooks:
      - name: send-to-slack
        type: pre-rollout
        url: http://slack-webhook.default/
        timeout: 15s
        metadata:
          type: "info"
          cmd: "Canary deployment started for heal7-backend"
      - name: send-to-slack-success
        type: post-rollout
        url: http://slack-webhook.default/
        timeout: 15s
        metadata:
          type: "success"
          cmd: "Canary deployment completed successfully"
      - name: send-to-slack-failure
        type: rollback
        url: http://slack-webhook.default/
        timeout: 15s
        metadata:
          type: "error"
          cmd: "Canary deployment failed and rolled back"

# Istio VirtualService for traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: heal7-backend
  namespace: heal7-prod
spec:
  hosts:
    - api.heal7.com
  gateways:
    - heal7-gateway
  http:
    - match:
        - headers:
            canary:
              exact: "true"
      route:
        - destination:
            host: heal7-backend-canary
    - route:
        - destination:
            host: heal7-backend-primary
          weight: 90
        - destination:
            host: heal7-backend-canary
          weight: 10
```

### **🔄 자동화된 롤백 시스템**

#### **1. 스마트 롤백 로직**
```python
# scripts/smart-rollback.py
#!/usr/bin/env python3
"""
스마트 롤백 시스템 - 메트릭 기반 자동 롤백
"""
import time
import requests
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from prometheus_api_client import PrometheusConnect

@dataclass
class RollbackCriteria:
    metric_name: str
    threshold: float
    comparison: str  # 'gt', 'lt', 'eq'
    evaluation_period: int  # seconds
    
@dataclass
class DeploymentHealth:
    error_rate: float
    response_time_p95: float
    cpu_usage: float
    memory_usage: float
    success_rate: float

class SmartRollbackManager:
    def __init__(self, prometheus_url: str, app_name: str):
        self.prometheus = PrometheusConnect(url=prometheus_url)
        self.app_name = app_name
        self.rollback_criteria = [
            RollbackCriteria("error_rate", 5.0, "gt", 300),  # 5% 이상 에러율
            RollbackCriteria("response_time_p95", 2000, "gt", 300),  # 2초 이상 응답시간
            RollbackCriteria("success_rate", 95.0, "lt", 180),  # 95% 미만 성공률
            RollbackCriteria("cpu_usage", 90.0, "gt", 600),  # 90% 이상 CPU 사용률
        ]
        
    def get_deployment_health(self) -> DeploymentHealth:
        """현재 배포 상태 건강도 조회"""
        queries = {
            'error_rate': f'rate(http_requests_total{{app="{self.app_name}",status=~"5.."}}[5m]) / rate(http_requests_total{{app="{self.app_name}"}}[5m]) * 100',
            'response_time_p95': f'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{app="{self.app_name}"}}[5m])) * 1000',
            'cpu_usage': f'rate(container_cpu_usage_seconds_total{{app="{self.app_name}"}}[5m]) * 100',
            'memory_usage': f'container_memory_usage_bytes{{app="{self.app_name}"}} / container_spec_memory_limit_bytes{{app="{self.app_name}"}} * 100',
            'success_rate': f'rate(http_requests_total{{app="{self.app_name}",status!~"5.."}}[5m]) / rate(http_requests_total{{app="{self.app_name}"}}[5m]) * 100'
        }
        
        metrics = {}
        for name, query in queries.items():
            result = self.prometheus.custom_query(query)
            if result:
                metrics[name] = float(result[0]['value'][1])
            else:
                metrics[name] = 0.0
                
        return DeploymentHealth(
            error_rate=metrics['error_rate'],
            response_time_p95=metrics['response_time_p95'],
            cpu_usage=metrics['cpu_usage'],
            memory_usage=metrics['memory_usage'],
            success_rate=metrics['success_rate']
        )
    
    def evaluate_rollback_criteria(self, health: DeploymentHealth) -> List[str]:
        """롤백 기준 평가"""
        violations = []
        
        health_dict = {
            'error_rate': health.error_rate,
            'response_time_p95': health.response_time_p95,
            'cpu_usage': health.cpu_usage,
            'memory_usage': health.memory_usage,
            'success_rate': health.success_rate
        }
        
        for criteria in self.rollback_criteria:
            metric_value = health_dict.get(criteria.metric_name, 0)
            
            if criteria.comparison == 'gt' and metric_value > criteria.threshold:
                violations.append(f"{criteria.metric_name}: {metric_value} > {criteria.threshold}")
            elif criteria.comparison == 'lt' and metric_value < criteria.threshold:
                violations.append(f"{criteria.metric_name}: {metric_value} < {criteria.threshold}")
                
        return violations
    
    def execute_rollback(self, reason: str) -> bool:
        """롤백 실행"""
        try:
            # ArgoCD를 통한 롤백
            rollback_cmd = f"""
            kubectl rollout undo deployment/{self.app_name} -n heal7-prod
            kubectl rollout status deployment/{self.app_name} -n heal7-prod --timeout=300s
            """
            
            import subprocess
            result = subprocess.run(rollback_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.send_alert(f"🔄 자동 롤백 성공: {reason}", "success")
                return True
            else:
                self.send_alert(f"❌ 자동 롤백 실패: {result.stderr}", "error")
                return False
                
        except Exception as e:
            self.send_alert(f"❌ 롤백 실행 중 오류: {str(e)}", "error")
            return False
    
    def send_alert(self, message: str, level: str):
        """알림 발송"""
        slack_webhook = "https://hooks.slack.com/services/xxx"  # 실제 웹훅 URL
        
        color_map = {
            'success': 'good',
            'warning': 'warning', 
            'error': 'danger'
        }
        
        payload = {
            "attachments": [{
                "color": color_map.get(level, 'warning'),
                "title": f"HEAL7 {self.app_name} - 자동 롤백 시스템",
                "text": message,
                "ts": int(time.time())
            }]
        }
        
        requests.post(slack_webhook, json=payload)
    
    def monitor_and_rollback(self, monitoring_duration: int = 900):  # 15분 모니터링
        """배포 후 모니터링 및 자동 롤백"""
        print(f"🔍 배포 후 모니터링 시작: {self.app_name} ({monitoring_duration}초)")
        
        start_time = time.time()
        check_interval = 60  # 1분마다 체크
        
        while time.time() - start_time < monitoring_duration:
            health = self.get_deployment_health()
            violations = self.evaluate_rollback_criteria(health)
            
            print(f"📊 현재 상태: 에러율 {health.error_rate:.2f}%, 응답시간 {health.response_time_p95:.0f}ms, 성공률 {health.success_rate:.2f}%")
            
            if violations:
                print(f"⚠️ 롤백 기준 위반 감지: {violations}")
                
                # 30초 대기 후 재확인
                time.sleep(30)
                health_recheck = self.get_deployment_health()
                violations_recheck = self.evaluate_rollback_criteria(health_recheck)
                
                if violations_recheck:
                    print("🚨 롤백 기준 위반 재확인됨. 자동 롤백 실행...")
                    reason = "; ".join(violations_recheck)
                    success = self.execute_rollback(reason)
                    
                    if success:
                        print("✅ 자동 롤백 완료")
                        return True
                    else:
                        print("❌ 자동 롤백 실패 - 수동 개입 필요")
                        return False
                else:
                    print("✅ 일시적 이상으로 판단, 모니터링 계속")
            
            time.sleep(check_interval)
        
        print("✅ 모니터링 완료 - 배포 안정적")
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("사용법: python smart-rollback.py <app-name>")
        sys.exit(1)
    
    app_name = sys.argv[1]
    prometheus_url = "http://prometheus.monitoring.svc.cluster.local:9090"
    
    manager = SmartRollbackManager(prometheus_url, app_name)
    success = manager.monitor_and_rollback()
    
    sys.exit(0 if success else 1)
```

---

## 🏗️ **Infrastructure as Code (IaC)**

### **🌍 Terraform 기반 인프라 관리**

#### **1. 모듈화된 Terraform 구조**
```hcl
# terraform/environments/prod/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
  }
  
  backend "s3" {
    bucket         = "heal7-terraform-state"
    key            = "environments/prod/terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# 공통 모듈 사용
module "vpc" {
  source = "../../modules/vpc"
  
  environment = "prod"
  vpc_cidr = "10.0.0.0/16"
  availability_zones = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnet_cidrs = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
  
  tags = local.common_tags
}

module "eks" {
  source = "../../modules/eks"
  
  cluster_name = "heal7-prod"
  cluster_version = "1.28"
  
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_size = 3
      max_size     = 10
      min_size     = 3
      
      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"
      
      k8s_labels = {
        Environment = "prod"
        NodePool    = "general"
      }
      
      taints = []
    }
    
    compute_intensive = {
      desired_size = 2
      max_size     = 5
      min_size     = 2
      
      instance_types = ["c5.xlarge"]
      capacity_type  = "ON_DEMAND"
      
      k8s_labels = {
        Environment = "prod"
        NodePool    = "compute"
      }
      
      taints = [
        {
          key    = "compute-intensive"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  }
  
  tags = local.common_tags
}

module "rds" {
  source = "../../modules/rds"
  
  identifier = "heal7-prod"
  engine     = "postgres"
  engine_version = "16.1"
  
  instance_class = "db.r6g.xlarge"
  allocated_storage = 100
  max_allocated_storage = 1000
  
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.database_subnet_ids
  
  backup_retention_period = 30
  backup_window = "03:00-04:00"
  maintenance_window = "sun:04:00-sun:05:00"
  
  monitoring_interval = 60
  performance_insights_enabled = true
  
  tags = local.common_tags
}

module "elasticache" {
  source = "../../modules/elasticache"
  
  cluster_id = "heal7-prod"
  node_type = "cache.r6g.large"
  num_cache_nodes = 3
  
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  tags = local.common_tags
}

# 로컬 변수
locals {
  common_tags = {
    Environment = "prod"
    Project     = "heal7"
    ManagedBy   = "terraform"
    Owner       = "devops-team"
  }
}

# 출력값
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  value = module.rds.endpoint
  sensitive = true
}

output "elasticache_endpoint" {
  value = module.elasticache.endpoint
  sensitive = true
}
```

#### **2. EKS 모듈 상세 구현**
```hcl
# terraform/modules/eks/main.tf
data "aws_caller_identity" "current" {}

# EKS 클러스터
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.cluster_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.public_access_cidrs
    
    security_group_ids = [aws_security_group.cluster.id]
  }

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }

  enabled_cluster_log_types = [
    "api",
    "audit", 
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
    aws_cloudwatch_log_group.cluster,
  ]

  tags = var.tags
}

# CloudWatch 로그 그룹
resource "aws_cloudwatch_log_group" "cluster" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 30
  kms_key_id       = aws_kms_key.eks.arn

  tags = var.tags
}

# KMS 키 (암호화용)
resource "aws_kms_key" "eks" {
  description             = "EKS Secret Encryption Key"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = merge(var.tags, {
    Name = "${var.cluster_name}-encryption-key"
  })
}

resource "aws_kms_alias" "eks" {
  name          = "alias/${var.cluster_name}-encryption-key"
  target_key_id = aws_kms_key.eks.key_id
}

# IAM 역할 - 클러스터
resource "aws_iam_role" "cluster" {
  name = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}

# 보안 그룹 - 클러스터
resource "aws_security_group" "cluster" {
  name_prefix = "${var.cluster_name}-cluster-"
  vpc_id      = var.vpc_id

  tags = merge(var.tags, {
    Name = "${var.cluster_name}-cluster-sg"
  })
}

resource "aws_security_group_rule" "cluster_egress" {
  description       = "Allow all egress"
  from_port         = 0
  protocol          = "-1"
  security_group_id = aws_security_group.cluster.id
  to_port           = 0
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
}

# 노드 그룹
resource "aws_eks_node_group" "main" {
  for_each = var.node_groups

  cluster_name    = aws_eks_cluster.main.name
  node_group_name = each.key
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.subnet_ids

  capacity_type  = each.value.capacity_type
  instance_types = each.value.instance_types

  scaling_config {
    desired_size = each.value.desired_size
    max_size     = each.value.max_size
    min_size     = each.value.min_size
  }

  update_config {
    max_unavailable_percentage = 25
  }

  # Kubernetes 라벨
  labels = each.value.k8s_labels

  # Taints
  dynamic "taint" {
    for_each = each.value.taints
    content {
      key    = taint.value.key
      value  = taint.value.value
      effect = taint.value.effect
    }
  }

  # Launch template
  launch_template {
    id      = aws_launch_template.node_group[each.key].id
    version = aws_launch_template.node_group[each.key].latest_version
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_group_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_group_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_group_AmazonEC2ContainerRegistryReadOnly,
  ]

  tags = var.tags
}

# Launch Template (사용자 데이터 및 추가 설정용)
resource "aws_launch_template" "node_group" {
  for_each = var.node_groups

  name_prefix   = "${var.cluster_name}-${each.key}-"
  image_id      = data.aws_ssm_parameter.eks_ami_release_version.value
  instance_type = each.value.instance_types[0]

  vpc_security_group_ids = [aws_security_group.node_group.id]

  user_data = base64encode(templatefile("${path.module}/userdata.sh", {
    cluster_name = aws_eks_cluster.main.name
    endpoint     = aws_eks_cluster.main.endpoint
    ca_data      = aws_eks_cluster.main.certificate_authority[0].data
  }))

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = 100
      volume_type           = "gp3"
      encrypted             = true
      delete_on_termination = true
    }
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(var.tags, {
      Name = "${var.cluster_name}-${each.key}-node"
    })
  }

  tags = var.tags
}

# IAM 역할 - 노드 그룹
resource "aws_iam_role" "node_group" {
  name = "${var.cluster_name}-node-group-role"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "node_group_AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_group_AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_group_AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_group.name
}

# AWS Load Balancer Controller용 IAM 역할
resource "aws_iam_role" "load_balancer_controller" {
  name = "${var.cluster_name}-aws-load-balancer-controller"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRoleWithWebIdentity"
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.cluster.arn
      }
      Condition = {
        StringEquals = {
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:sub" = "system:serviceaccount:kube-system:aws-load-balancer-controller"
          "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:aud" = "sts.amazonaws.com"
        }
      }
    }]
    Version = "2012-10-17"
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "load_balancer_controller" {
  policy_arn = aws_iam_policy.load_balancer_controller.arn
  role       = aws_iam_role.load_balancer_controller.name
}

# OIDC Identity Provider
resource "aws_iam_openid_connect_provider" "cluster" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.cluster.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer

  tags = var.tags
}

data "tls_certificate" "cluster" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

# 보안 그룹 - 노드 그룹
resource "aws_security_group" "node_group" {
  name_prefix = "${var.cluster_name}-node-group-"
  vpc_id      = var.vpc_id

  tags = merge(var.tags, {
    Name = "${var.cluster_name}-node-group-sg"
  })
}

resource "aws_security_group_rule" "node_group_egress" {
  description       = "Allow all egress"
  from_port         = 0
  protocol          = "-1"
  security_group_id = aws_security_group.node_group.id
  to_port           = 0
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
}

# AMI 데이터 소스
data "aws_ssm_parameter" "eks_ami_release_version" {
  name = "/aws/service/eks/optimized-ami/${aws_eks_cluster.main.version}/amazon-linux-2/recommended/image_id"
}
```

### **📦 Helm Charts 관리**

#### **1. HEAL7 메인 애플리케이션 Helm Chart**
```yaml
# k8s/helm/heal7/Chart.yaml
apiVersion: v2
name: heal7
description: HEAL7 옴니버스 플랫폼 Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: 17.x.x  
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
  - name: ingress-nginx
    version: 4.x.x
    repository: https://kubernetes.github.io/ingress-nginx
    condition: ingress.nginx.enabled

# k8s/helm/heal7/values.yaml
global:
  environment: production
  imageRegistry: 123456789012.dkr.ecr.ap-northeast-2.amazonaws.com
  imagePullSecrets:
    - name: ecr-secret

# 프론트엔드 서비스
frontend:
  enabled: true
  replicaCount: 3
  
  image:
    repository: heal7-frontend
    tag: latest
    pullPolicy: IfNotPresent
  
  service:
    type: ClusterIP
    port: 80
    targetPort: 3000
  
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
  
  nodeSelector:
    NodePool: general
  
  tolerations: []
  
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchExpressions:
                - key: app.kubernetes.io/name
                  operator: In
                  values:
                    - heal7-frontend
            topologyKey: kubernetes.io/hostname

# 백엔드 서비스  
backend:
  enabled: true
  replicaCount: 5
  
  image:
    repository: heal7-backend
    tag: latest
    pullPolicy: IfNotPresent
  
  service:
    type: ClusterIP
    port: 8080
    targetPort: 8000
  
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 200m
      memory: 256Mi
  
  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 50
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
    behavior:
      scaleUp:
        stabilizationWindowSeconds: 60
        policies:
          - type: Percent
            value: 100
            periodSeconds: 15
      scaleDown:
        stabilizationWindowSeconds: 300
        policies:
          - type: Percent
            value: 10
            periodSeconds: 60
  
  # 환경 변수
  env:
    DATABASE_URL:
      valueFrom:
        secretKeyRef:
          name: heal7-secrets
          key: database-url
    REDIS_URL:
      valueFrom:
        secretKeyRef:
          name: heal7-secrets
          key: redis-url
    SECRET_KEY:
      valueFrom:
        secretKeyRef:
          name: heal7-secrets
          key: secret-key
  
  # 설정 파일 마운트
  configMaps:
    - name: heal7-config
      mountPath: /app/config
  
  # Health checks
  livenessProbe:
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
  
  readinessProbe:
    httpGet:
      path: /ready
      port: 8000
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3
  
  nodeSelector:
    NodePool: general
  
  tolerations: []

# 사주 계산 특화 서비스 (고성능)
saju-calculator:
  enabled: true
  replicaCount: 3
  
  image:
    repository: heal7-saju-calculator
    tag: latest
    pullPolicy: IfNotPresent
  
  service:
    type: ClusterIP
    port: 8080
    targetPort: 8001
  
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 512Mi
  
  nodeSelector:
    NodePool: compute
  
  tolerations:
    - key: compute-intensive
      operator: Equal
      value: "true"
      effect: NoSchedule
  
  # 전용 리소스 보장
  priorityClassName: high-priority

# 데이터베이스 설정
postgresql:
  enabled: false  # 외부 RDS 사용
  
redis:
  enabled: false  # 외부 ElastiCache 사용

# Ingress 설정
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
  
  hosts:
    - host: heal7.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: backend
        - path: /saju-api
          pathType: Prefix
          service: saju-calculator
  
  tls:
    - secretName: heal7-com-tls
      hosts:
        - heal7.com

# 모니터링 설정
monitoring:
  enabled: true
  
  serviceMonitor:
    enabled: true
    interval: 30s
    path: /metrics
    
  prometheusRule:
    enabled: true
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"

# 보안 설정
security:
  networkPolicies:
    enabled: true
  
  podSecurityPolicy:
    enabled: true
  
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  
  containerSecurityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities:
      drop:
        - ALL
```

---

## 📊 **모니터링 및 관찰가능성**

### **🔍 Observability Stack**

#### **1. Prometheus + Grafana 모니터링**
```yaml
# monitoring/prometheus/values.yaml
prometheus:
  prometheusSpec:
    retention: 30d
    retentionSize: 100GB
    
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi
    
    resources:
      limits:
        cpu: 2000m
        memory: 8Gi
      requests:
        cpu: 500m
        memory: 2Gi
    
    # HEAL7 특화 메트릭 수집 규칙
    additionalScrapeConfigs:
      - job_name: 'heal7-saju-metrics'
        kubernetes_sd_configs:
          - role: endpoints
            namespaces:
              names:
                - heal7-prod
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)

grafana:
  adminPassword: ${GRAFANA_ADMIN_PASSWORD}
  
  # HEAL7 대시보드 자동 프로비저닝
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'heal7-dashboards'
          orgId: 1
          folder: 'HEAL7'
          type: file
          disableDeletion: false
          editable: true
          options:
            path: /var/lib/grafana/dashboards/heal7
  
  dashboards:
    heal7-dashboards:
      heal7-overview:
        gnetId: 1860
        revision: 27
        datasource: Prometheus
      heal7-saju-performance:
        file: dashboards/saju-performance.json
      heal7-user-analytics:
        file: dashboards/user-analytics.json
      heal7-infrastructure:
        file: dashboards/infrastructure.json

# monitoring/grafana/dashboards/saju-performance.json
{
  "dashboard": {
    "title": "HEAL7 사주 시스템 성능",
    "panels": [
      {
        "title": "사주 계산 요청량",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(saju_calculations_total[5m])",
            "legendFormat": "초당 사주 계산 수"
          }
        ],
        "yAxes": [
          {
            "label": "Requests/sec"
          }
        ]
      },
      {
        "title": "사주 계산 응답 시간",
        "type": "graph", 
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(saju_calculation_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.95, rate(saju_calculation_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(saju_calculation_duration_seconds_bucket[5m]))",
            "legendFormat": "99th percentile"
          }
        ],
        "yAxes": [
          {
            "label": "Seconds"
          }
        ]
      },
      {
        "title": "오행 분석 정확도",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(saju_analysis_accuracy_score)",
            "legendFormat": "평균 정확도"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 100
          }
        }
      }
    ]
  }
}
```

#### **2. 분산 추적 (Jaeger)**
```yaml
# monitoring/jaeger/values.yaml
jaeger:
  strategy: production
  
  collector:
    resources:
      limits:
        cpu: 1000m
        memory: 1Gi
      requests:
        cpu: 100m
        memory: 256Mi
  
  query:
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 100m
        memory: 128Mi
  
  storage:
    type: elasticsearch
    elasticsearch:
      host: elasticsearch.monitoring.svc.cluster.local
      port: 9200
      
  # HEAL7 애플리케이션 추적 설정
  agent:
    annotations:
      sidecar.jaegertracing.io/inject: "true"
    daemonset:
      useHostNetwork: true
      useHostPort: true
```

#### **3. 로그 집계 (ELK Stack)**
```yaml
# monitoring/elastic/values.yaml
elasticsearch:
  replicas: 3
  minimumMasterNodes: 2
  
  esConfig:
    elasticsearch.yml: |
      cluster.name: "heal7-logs"
      network.host: 0.0.0.0
      discovery.seed_hosts: "elasticsearch-master-headless"
      cluster.initial_master_nodes: "elasticsearch-master-0,elasticsearch-master-1,elasticsearch-master-2"
      
  resources:
    requests:
      cpu: "1000m"
      memory: "2Gi"
    limits:
      cpu: "2000m"
      memory: "4Gi"
  
  volumeClaimTemplate:
    accessModes: [ "ReadWriteOnce" ]
    storageClassName: "gp3"
    resources:
      requests:
        storage: 100Gi

logstash:
  logstashConfig:
    logstash.yml: |
      http.host: 0.0.0.0
      pipeline.ecs_compatibility: disabled
      
  logstashPipeline:
    heal7-logs.conf: |
      input {
        beats {
          port => 5044
        }
      }
      
      filter {
        # HEAL7 애플리케이션 로그 파싱
        if [fields][app] == "heal7-backend" {
          grok {
            match => { 
              "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" 
            }
          }
          
          # 사주 계산 관련 로그 특별 처리
          if [message] =~ /saju_calculation/ {
            grok {
              match => { 
                "message" => "saju_calculation user_id=%{UUID:user_id} duration=%{NUMBER:duration:float} accuracy=%{NUMBER:accuracy:float}" 
              }
            }
            
            mutate {
              add_tag => ["saju_performance"]
            }
          }
        }
        
        # 민감 정보 마스킹
        mutate {
          gsub => [
            "message", "\d{4}-\d{2}-\d{2}", "****-**-**",  # 생년월일 마스킹
            "message", "\d{10,11}", "***-****-****"        # 전화번호 마스킹
          ]
        }
      }
      
      output {
        elasticsearch {
          hosts => ["elasticsearch-master:9200"]
          index => "heal7-logs-%{+YYYY.MM.dd}"
        }
      }

kibana:
  elasticsearchHosts: "http://elasticsearch-master:9200"
  
  resources:
    requests:
      cpu: "500m"
      memory: "1Gi"
    limits:
      cpu: "1000m"
      memory: "2Gi"
```

---

## 🏆 **결론**

### **✨ DevOps CI/CD 아키텍처 핵심 가치**

이 DevOps CI/CD 파이프라인 아키텍처는 **레고블럭 모듈형 설계**와 **완전 자동화**를 통해 다음을 달성합니다:

#### **⚙️ 핵심 DevOps 성과**
1. **🚀 빠른 배포 주기**: 커밋부터 배포까지 30분 이내, 일 10회 이상 배포
2. **🛡️ 보안 우선 설계**: Shift-Left 보안, 모든 단계 보안 스캔 및 검증
3. **📊 완전한 관찰가능성**: 메트릭, 로그, 추적 통합 모니터링 시스템
4. **🔄 자동화된 품질 관리**: 코드부터 배포까지 전 단계 품질 게이트
5. **⚡ 스마트 롤백**: AI 기반 자동 롤백 및 장애 대응 시스템

#### **🎯 즉시 실행 가능**
```bash
# ⚙️ DevOps 파이프라인 아키텍처 확인
cat CORE/architecture-diagrams/devops-architecture/DevOps-CICD-Pipeline-Architecture-v1.0*.md

# 🚀 파이프라인 구축 시작
# 1단계: GitHub Actions 워크플로우 설정
# 2단계: Terraform 인프라 프로비저닝
# 3단계: Kubernetes 클러스터 구성
# 4단계: ArgoCD GitOps 설정
# 5단계: 모니터링 스택 배포
```

**이제 현대적인 DevOps 베스트 프랙티스가 완전히 구현된 자동화 파이프라인이 완성되었습니다!** ⚙️✨

---

*📅 DevOps CI/CD 아키텍처 완성일: 2025-08-18 19:15 KST*  
*⚙️ 파이프라인: GitHub Actions + ArgoCD + Kubernetes*  
*🎯 다음 단계: 상세 UI 컴포넌트 라이브러리 설계*