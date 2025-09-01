# MCP 도구 통합 가이드

## 🏗️ 설치 완료 상태

### ✅ 완료된 구성
- **통합 폴더 구조**: `/home/ubuntu/mcp-tools/`
- **공통 캡처 폴더**: `/home/ubuntu/mcp-tools/shared-captures/`
- **폴백 순서 설계**: 메모리/IO 효율성 기준
- **Claude CLI 서버 등록**: puppeteer, selenium

### 📂 폴더 구조
```
/home/ubuntu/mcp-tools/
├── shared-captures/          # 🎯 모든 도구 공통 캡처 저장소
├── configs/                  # 각 도구별 설정 파일
│   ├── puppeteer-config.json
│   ├── selenium-config.json
│   └── playwright-config.json
├── logs/                     # 로그 저장소
├── skyvern/                  # Skyvern 가상환경 및 파일
├── puppeteer/                # Puppeteer 관련 파일
├── selenium/                 # Selenium 관련 파일
├── playwright/               # Playwright 관련 파일
└── fallback-config.json      # 폴백 우선순위 설정
```

## 🎯 폴백 우선순위 (메모리/IO 효율성 기준)

### 1순위: Playwright (최우선)
- **장점**: 가장 효율적, 이미 설치됨
- **리소스**: 메모리/IO 낮음, 빠른 시작
- **용도**: 일반적인 브라우저 자동화

### 2순위: Puppeteer 
- **장점**: Node.js 기반, Chromium 사용
- **리소스**: 메모리/IO 중간, 빠른 시작
- **용도**: Chrome 특화 자동화

### 3순위: Selenium
- **장점**: 크로스 브라우저 지원
- **리소스**: 메모리/IO 높음, 느린 시작
- **용도**: 다양한 브라우저 호환성 필요시

### 4순위: Skyvern (최후순위)
- **장점**: AI 기반 브라우저 제어
- **리소스**: 메모리/IO 높음, 가장 느린 시작
- **용도**: 복잡한 AI 기반 자동화

## 🔧 사용법

### Claude CLI에서 활용
```bash
# MCP 서버 상태 확인
claude mcp list

# 크롤링 작업 시 자동 폴백 적용
claude "웹사이트를 스크래핑해줘" --mcp-config /home/ubuntu/mcp-tools/fallback-config.json
```

### 크롤링 서비스 통합
- **포트**: 8003
- **캡처 경로**: `/home/ubuntu/mcp-tools/shared-captures/`
- **폴백 로직**: 자동으로 1순위→2순위→...→5순위 시도

## ⚠️ 현재 이슈

### MCP 서버 연결 실패
```
puppeteer: ✗ Failed to connect  
selenium: ✗ Failed to connect
```

**원인**: MCP 서버 설정 미완료
**해결방안**: 
1. Claude CLI 설정에서 MCP 서버 등록
2. 필요한 의존성 패키지 설치 확인

## 🚀 다음 단계
1. Skyvern 설치 완료 (가상환경 생성됨)
2. 실제 크롤링 테스트 진행
3. 폴백 로직 검증

---
*생성일: $(date '+%Y-%m-%d %H:%M:%S')*