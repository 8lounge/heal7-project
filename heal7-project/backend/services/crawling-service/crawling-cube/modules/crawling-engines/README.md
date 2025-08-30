# 🕷️ HEAL7 크롤링 엔진

> **통합 크롤링 시스템** - 모든 데이터 수집 작업을 위한 중앙 집중형 크롤링 엔진

## 📋 **엔진 구성**

### 🔮 **Dream Collection Engine**
- **위치**: `dream-collection/`
- **목적**: 꿈 해몽 데이터 수집 및 분류
- **핵심 파일들**:
  - `dream_collector_integrated.py` - 메인 수집기
  - `dream_data_classifier.py` - 데이터 분류기  
  - `dream_status_check.py` - 상태 점검기
  - `create_raw_dream_table.sql` - DB 스키마
  - `protected/` - 운영 중인 핵심 6개 파일 (절대 보존)

### 🏛️ **Government Portal Engine**
- **위치**: `government-portal/`  
- **목적**: 정부 지원사업 정보 수집
- **핵심 기능**:
  - 비즈니스정보 스크래핑
  - K-스타트업 정보 수집
  - 중복 제거 및 정제
  - 안전한 수집 간격 제어

## 🚀 **사용법**

### Dream Collection 실행
```bash
cd /home/ubuntu/heal7-project/backend/crawling-engines/dream-collection
python3 dream_collector_integrated.py
```

### Government Portal 실행  
```bash
cd /home/ubuntu/heal7-project/backend/crawling-engines/government-portal
python3 main.py
```

## 🔒 **보호 구역**
- `dream-collection/protected/` 6개 파일 **절대 수정 금지**
- 현재 운영 중인 꿈 수집 시스템의 핵심 파일들

## 📊 **통합 모니터링**
- 각 엔진별 독립적인 로그 시스템
- 통합 상태 확인 대시보드 (추후 구현)
- 오류 복구 자동화 시스템

---
*🕷️ 마지막 업데이트: 2025-08-26 | 큐브모듈러 아키텍처 통합*