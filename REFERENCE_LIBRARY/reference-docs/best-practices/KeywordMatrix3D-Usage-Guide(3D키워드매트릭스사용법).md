# 🌐 3D 키워드 매트릭스 사용 가이드

> **모듈명**: KeywordMatrix3D(3D키워드매트릭스)
> **파일 위치**: `/home/ubuntu/CORE/sample-codes/react-components/KeywordMatrix3D(3D키워드매트릭스).complete.html`
> **완성도**: 100% (즉시 사용 가능)

## 🎯 **모듈 개요**

### **목적 (WHY)**
- 442개 한글 키워드를 3D 공간에서 직관적으로 시각화
- 복잡한 키워드 네트워크를 이해하기 쉬운 지구본 형태로 표현
- 키워드 간 연결 관계와 상태를 한눈에 파악할 수 있는 인터랙티브 환경 제공

### **설계 의도 (HOW)**
- **Three.js 기반** WebGL 3D 렌더링으로 고성능 시각화
- **지구본 배치 알고리즘**으로 키워드를 구체 표면에 균등 분산
- **상태 기반 색상 시스템**으로 키워드 상황을 직관적 표현
- **GSAP 애니메이션**으로 부드러운 카메라 전환과 상호작용

### **구현 상세 (WHAT)**
- **총 442개 키워드**: 60개 메인 + 382개 서브 키워드
- **4단계 상태 색상**: 긍정(초록)/중립(노랑)/부정(빨강)/비활성(회색)
- **인터랙티브 기능**: 호버 하이라이트, 클릭 포커스, 검색, 컨트롤
- **반응형 UI**: 데스크탑/태블릿/모바일 대응

## 🚀 **즉시 사용법**

### **1단계: 파일 배치**
```bash
# 웹 서버에 파일 복사 (로컬 개발 서버 또는 실제 서버)
cp /home/ubuntu/CORE/sample-codes/react-components/KeywordMatrix3D\(3D키워드매트릭스\).complete.html /var/www/html/
```

### **2단계: 브라우저 접근**
```bash
# 로컬 서버에서 실행
http://localhost/KeywordMatrix3D(3D키워드매트릭스).complete.html

# 또는 Python 간단 서버로 테스트
cd /home/ubuntu/CORE/sample-codes/react-components/
python3 -m http.server 8080
# 브라우저에서 http://localhost:8080/KeywordMatrix3D(3D키워드매트릭스).complete.html 접근
```

### **3단계: 즉시 인터랙션**
- **마우스 드래그**: 3D 매트릭스 회전
- **마우스 휠**: 확대/축소
- **키워드 호버**: 연결 그룹 하이라이트
- **키워드 클릭**: 해당 그룹으로 포커스 이동
- **검색 활용**: 우상단 검색창에 키워드 입력

## 🛠️ **커스터마이징 방법**

### **키워드 데이터 변경**
```javascript
// HTML 파일 내부의 keywordData 객체 수정
const keywordData = {
    // 기존 데이터 대신 사용자 데이터 입력
    '사용자메인키워드': ['서브키워드1', '서브키워드2', '서브키워드3'],
    '새로운카테고리': ['연관키워드A', '연관키워드B']
};
```

### **색상 테마 변경**
```javascript
// getStateColor 함수 수정으로 색상 테마 변경
function getStateColor(state) {
    if (state > 0.5) return new THREE.Color("#00ff88"); // 커스텀 긍정색
    if (state > -0.2) return new THREE.Color("#ffaa00"); // 커스텀 중립색
    if (state > -1) return new THREE.Color("#ff4444"); // 커스텀 부정색
    return new THREE.Color("#888888"); // 커스텀 비활성색
}
```

### **배경 및 UI 스타일 변경**
```css
/* <style> 태그 내부의 CSS 수정 */
body {
    background-color: #1a1a2e; /* 다른 배경색 */
}

.ui-layer {
    background-color: rgba(100, 50, 150, 0.9); /* 커스텀 UI 배경 */
    border: 2px solid #ff6b6b; /* 테두리 추가 */
}
```

## 💡 **활용 시나리오**

### **🔍 데이터 분석 도구로 활용**
```javascript
// 1. 키워드별 상태 데이터를 실시간으로 업데이트
const keywordStates = {
    '논리': realTimeAnalysisResult.logic_score,
    '창의력': realTimeAnalysisResult.creativity_score
};

// 2. 상태에 따른 색상 자동 업데이트
Object.keys(nodes).forEach(keyword => {
    const state = keywordStates[keyword];
    const color = getStateColor(state);
    nodes[keyword].material.color.copy(color);
});
```

### **🎓 교육용 시각화 도구로 활용**
```html
<!-- iframe으로 다른 웹사이트에 임베드 -->
<iframe src="KeywordMatrix3D(3D키워드매트릭스).complete.html" 
        width="100%" height="600px" frameborder="0">
</iframe>
```

### **📊 대시보드 컴포넌트로 통합**
```javascript
// React/Vue 컴포넌트 내부에서 iframe 또는 직접 통합
const KeywordMatrix3D = () => {
    return (
        <div style={{width: '100%', height: '100vh'}}>
            <iframe src="./KeywordMatrix3D(3D키워드매트릭스).complete.html" 
                    width="100%" height="100%" />
        </div>
    );
};
```

## 🎛️ **컨트롤 패널 설명**

### **좌상단 컨트롤**
- **초기화 버튼**: 카메라를 초기 위치로 리셋
- **회전 속도 슬라이더**: 자동 회전 속도 조절 (0~5)
- **텍스트 크기 슬라이더**: 키워드 라벨 크기 조절 (10px~24px)
- **줌인/줌아웃**: 카메라 거리 조절

### **우상단 검색**
- **검색창**: 키워드 이름 입력 (부분 일치 지원)
- **검색 버튼**: Enter 키 또는 버튼 클릭으로 검색 실행
- **검색 실패 시**: 검색창 흔들림 애니메이션으로 피드백

### **좌하단 범례**
- **색상 의미**: 긍정(초록), 중립(노랑), 부정(빨강), 비활성(회색)
- **상태 구간**: 각 색상에 해당하는 상태 값 범위 표시

## 🔧 **기술적 세부사항**

### **성능 최적화**
- **Frustum Culling**: 화면 밖 객체 자동 제거
- **동적 LOD**: 거리에 따른 디테일 레벨 조정
- **인스턴스 렌더링**: 동일한 지오메트리 재사용
- **적응형 품질**: 성능 저하 시 품질 자동 조정

### **브라우저 호환성**
```javascript
// 브라우저 지원 확인
if (!window.WebGLRenderingContext) {
    alert('이 브라우저는 WebGL을 지원하지 않습니다.');
    // 대체 2D 인터페이스 제공
}
```

### **메모리 관리**
- **자동 정리**: 페이지 종료 시 WebGL 컨텍스트 해제
- **텍스처 최적화**: 압축된 텍스처 포맷 사용
- **가비지 컬렉션**: 불필요한 객체 참조 제거

## 🐛 **문제 해결 가이드**

### **일반적 문제들**

#### **문제**: 3D 매트릭스가 표시되지 않음
**해결책**:
```javascript
// 1. WebGL 지원 확인
console.log('WebGL 지원:', !!window.WebGLRenderingContext);

// 2. 콘솔 에러 메시지 확인
// F12 → Console 탭에서 에러 메시지 확인

// 3. CORS 문제 (로컬 파일 실행 시)
// 웹 서버를 통해 실행하거나 --allow-file-access-from-files 플래그 사용
```

#### **문제**: 성능이 느림 (낮은 FPS)
**해결책**:
```javascript
// 1. 키워드 수 줄이기
const limitedKeywordData = Object.fromEntries(
    Object.entries(keywordData).slice(0, 20) // 20개만 표시
);

// 2. 품질 설정 낮추기
renderer.setPixelRatio(1); // 디바이스 픽셀 비율 고정
renderer.setSize(width * 0.8, height * 0.8); // 해상도 80% 축소
```

#### **문제**: 모바일에서 터치 제스처 미작동
**해결책**:
```javascript
// 터치 이벤트 리스너 추가
renderer.domElement.addEventListener('touchstart', onTouchStart, false);
renderer.domElement.addEventListener('touchmove', onTouchMove, false);
renderer.domElement.addEventListener('touchend', onTouchEnd, false);
```

## 🔗 **확장 가능성**

### **API 연동**
```javascript
// 외부 API에서 키워드 데이터 로드
async function loadKeywordData() {
    const response = await fetch('/api/keywords');
    const data = await response.json();
    
    // 기존 keywordData 교체
    Object.keys(keywordData).forEach(key => delete keywordData[key]);
    Object.assign(keywordData, data);
    
    // 3D 매트릭스 재생성
    recreateGraph();
}
```

### **실시간 업데이트**
```javascript
// WebSocket으로 실시간 상태 업데이트
const ws = new WebSocket('ws://localhost:8080/keywords');
ws.onmessage = (event) => {
    const stateUpdate = JSON.parse(event.data);
    updateKeywordStates(stateUpdate);
};
```

### **데이터 내보내기**
```javascript
// 현재 상태를 JSON으로 내보내기
function exportCurrentState() {
    const exportData = {
        keywords: Object.keys(nodes).map(key => ({
            name: key,
            position: nodes[key].position.toArray(),
            state: keywordStates[key],
            connections: Array.from(nodes[key].userData.connections.keys())
        }))
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], 
                         { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'keyword-matrix-state.json';
    a.click();
}
```

## 📋 **체크리스트**

### 배포 전 확인사항
- [ ] 모든 키워드 데이터가 정확히 로드됨
- [ ] 4가지 색상이 올바르게 표시됨  
- [ ] 검색 기능이 정상 작동함
- [ ] 모든 브라우저에서 테스트 완료
- [ ] 모바일 디바이스에서 터치 인터랙션 확인
- [ ] 성능 테스트 통과 (60FPS 유지)

### 커스터마이징 후 확인사항
- [ ] 수정된 데이터가 올바르게 시각화됨
- [ ] 색상 테마가 일관되게 적용됨
- [ ] UI 스타일이 전체적으로 조화로움
- [ ] 추가된 기능이 기존 기능과 충돌하지 않음

---

**🎯 레고블럭 활용법**: 이 모듈을 복사해서 프로젝트에 바로 통합하고, keywordData만 사용자 데이터로 교체하면 즉시 3D 키워드 시각화가 완성됩니다!

**📁 관련 파일**: 
- 완성 코드: `/home/ubuntu/CORE/sample-codes/react-components/KeywordMatrix3D(3D키워드매트릭스).complete.html`
- 기능 명세: `/home/ubuntu/CORE/feature-specs/user-features/keyword-matrix-3d.spec.md`

**📅 최종 업데이트**: 2025-08-18
**🔄 버전**: v13 (상호작용 개선)