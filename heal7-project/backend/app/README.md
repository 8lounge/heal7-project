# 🚀 HEAL7 메인 애플리케이션 - 레거시 호환 유지

> **현재 상태**: ✅ 운영 중 (포트 8004)  
> **역할**: 기존 시스템 호환성 유지 + 사주 엔진 제공  
> **새로운 서비스**: `/services/` 폴더의 6개 서비스와 병행 운영

## 🎯 **구조**

```
app/
├── main.py                    # FastAPI 메인 애플리케이션 (포트 8004)
├── core/                      # 핵심 엔진
│   └── engines/saju_system/   # 🔮 사주 계산 엔진 (KASI API 연동)
├── routers/                   # API 라우터
│   ├── saju.py               # 사주 API
│   ├── dream_interpretation.py # 꿈 해몽 API  
│   ├── paperwork.py          # 서류 처리 API
│   └── ...기타 라우터들
└── services/                  # 기존 서비스 로직
    ├── saju_service.py
    ├── kasi_service.py
    └── ...기타 서비스들
```

## 🔗 **새로운 서비스 구조와의 관계**

### **Legacy App (현재)**
- **포트**: 8004
- **역할**: 기존 API 호환성 유지
- **상태**: ✅ 운영 중

### **New Services (신규)**
- **포트**: 8010-8015
- **역할**: 모듈화된 마이크로서비스
- **오케스트레이션**: cube-dashboard-service (8015)

## 🚀 **실행**

### **메인 앱 실행**
```bash
cd /home/ubuntu/heal7-project/backend
python -m app.main
# → http://localhost:8004
```

### **서비스 상태 확인**
```bash
curl http://localhost:8004/health
curl http://localhost:8004/api/saju/health
```

## 🔮 **사주 엔진 (`core/engines/saju_system/`)**

### **핵심 컴포넌트**
- **kasi_precision_saju_calculator.py**: KASI API 연동 정밀 계산
- **hybrid_saju_engine.py**: 통합 사주 엔진
- **comprehensive_myeongrihak_analyzer.py**: 명리학 분석
- **smart_routing_manager.py**: 지능형 라우팅

### **상수 데이터**
```
constants/
├── gapja_60.json              # 갑자 60간지
├── jijanggan.json             # 지장간 데이터  
├── sidubeop.json              # 시두법 규칙
└── calculation_formulas.json  # 계산 공식
```

## 🔄 **마이그레이션 계획**

현재 `app/` 구조는 점진적으로 `services/saju-service`로 통합될 예정이지만,  
기존 API 호환성을 위해 당분간 병행 운영됩니다.

### **현재 운영**
- **app/main.py** (8004): 레거시 API 서비스
- **services/saju-service** (8012): 새로운 사주 서비스
- **cube-dashboard-service** (8015): 오케스트레이션 허브

---

**💡 참고**: 새로운 기능은 `services/`에서 개발하고, 기존 호환성은 `app/`에서 유지하는 하이브리드 구조입니다.