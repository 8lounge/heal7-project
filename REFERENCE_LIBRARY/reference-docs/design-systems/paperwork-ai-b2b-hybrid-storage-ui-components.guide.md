# 🔄 Paperwork AI B2B 하이브리드 저장소 UI 컴포넌트 가이드

> **프로젝트**: B2B 하이브리드 저장소 시스템 UI 컴포넌트  
> **버전**: v1.0.0  
> **작성일**: 2025-08-22  
> **대상**: 프론트엔드 개발자, UI/UX 디자이너  
> **목적**: 하이브리드 저장소 선택 및 관리 인터페이스 구현 가이드

---

## 🎯 **1. 하이브리드 저장소 컴포넌트 개요**

### **1.1 핵심 컴포넌트**

#### **저장소 선택기 (Storage Selector)**
- **용도**: 사용자가 문서 저장 위치를 선택하는 인터페이스
- **옵션**: 서버 저장소, 클라우드 연동, AI 자동 선택
- **시각적 구분**: 각 저장소별 고유 아이콘과 색상

#### **민감도 분석기 (Sensitivity Analyzer)**
- **용도**: AI가 문서 민감도를 실시간 분석하여 표시
- **표시 방식**: 진행 바와 점수로 민감도 레벨 시각화
- **권장 사항**: 분석 결과에 따른 저장소 권장

#### **클라우드 연동 관리자 (Cloud Connection Manager)**
- **용도**: 다중 클라우드 서비스 연결 상태 관리
- **지원 서비스**: Google Drive, Dropbox, OneDrive, iCloud
- **연결 상태**: OAuth 인증 상태와 용량 정보 표시

### **1.2 B2B 요금제별 차별화**

#### **스타터 플랜 (29,000원/월)**
- 서버 저장소: 20MB 할당
- 클라우드 연동: Google Drive 1개
- AI 분석: 기본 민감도 분석

#### **프로페셔널 플랜 (59,000원/월)**  
- 서버 저장소: 50MB 할당
- 클라우드 연동: 3개 서비스 (Drive, Dropbox, OneDrive)
- AI 분석: 고급 민감도 분석 + 권장 시스템

#### **엔터프라이즈 플랜 (99,000원/월)**
- 서버 저장소: 100MB 할당
- 클라우드 연동: 무제한 (iCloud 포함)
- AI 분석: 프리미엄 분석 + 정책 기반 자동 라우팅

---

## 🎨 **2. UI 컴포넌트 디자인 명세**

### **2.1 저장소 선택 패널**

#### **HTML 구조**
```html
<div class="storage-selector-panel glass-container">
    <h3 class="section-title">📁 저장소 선택</h3>
    
    <!-- 저장소 옵션들 -->
    <div class="storage-options grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <!-- 서버 저장소 옵션 -->
        <div class="storage-option server-storage" data-storage="server">
            <div class="storage-icon">
                <div class="icon-container">
                    🔒
                </div>
            </div>
            <div class="storage-info">
                <h4 class="storage-title">서버 저장소</h4>
                <p class="storage-description">민감한 문서 보안 저장</p>
                <div class="storage-features">
                    <span class="feature-tag">AES-256 암호화</span>
                    <span class="feature-tag">완전 격리</span>
                </div>
                <div class="storage-usage">
                    <div class="usage-bar">
                        <div class="usage-fill" style="width: 45%"></div>
                    </div>
                    <span class="usage-text">9MB / 20MB 사용 중</span>
                </div>
            </div>
            <div class="selection-indicator">
                <input type="radio" name="storage" value="server" id="server-radio">
                <label for="server-radio" class="radio-label"></label>
            </div>
        </div>
        
        <!-- 클라우드 저장소 옵션 -->
        <div class="storage-option cloud-storage" data-storage="cloud">
            <div class="storage-icon">
                <div class="icon-container">
                    ☁️
                </div>
            </div>
            <div class="storage-info">
                <h4 class="storage-title">클라우드 연동</h4>
                <p class="storage-description">일반 문서 클라우드 저장</p>
                <div class="storage-features">
                    <span class="feature-tag">자동 동기화</span>
                    <span class="feature-tag">대용량 지원</span>
                </div>
                <div class="cloud-services">
                    <div class="service-icons">
                        <span class="service-icon google-drive connected" title="Google Drive 연결됨">
                            <img src="/icons/google-drive.svg" alt="Google Drive">
                        </span>
                        <span class="service-icon dropbox disconnected" title="Dropbox 미연결">
                            <img src="/icons/dropbox.svg" alt="Dropbox">
                        </span>
                        <span class="service-icon onedrive locked" title="프로 플랜 전용">
                            <img src="/icons/onedrive.svg" alt="OneDrive">
                        </span>
                    </div>
                </div>
            </div>
            <div class="selection-indicator">
                <input type="radio" name="storage" value="cloud" id="cloud-radio">
                <label for="cloud-radio" class="radio-label"></label>
            </div>
        </div>
        
        <!-- AI 자동 선택 옵션 -->
        <div class="storage-option auto-routing selected" data-storage="auto">
            <div class="storage-icon">
                <div class="icon-container">
                    🤖
                </div>
            </div>
            <div class="storage-info">
                <h4 class="storage-title">AI 자동 선택</h4>
                <p class="storage-description">민감도 기반 스마트 라우팅</p>
                <div class="storage-features">
                    <span class="feature-tag">실시간 분석</span>
                    <span class="feature-tag">최적 라우팅</span>
                </div>
                <div class="ai-analysis-preview">
                    <div class="sensitivity-meter">
                        <div class="meter-bar">
                            <div class="meter-fill low" style="width: 25%"></div>
                        </div>
                        <span class="sensitivity-label">민감도: 낮음 (25%)</span>
                    </div>
                </div>
            </div>
            <div class="selection-indicator">
                <input type="radio" name="storage" value="auto" id="auto-radio" checked>
                <label for="auto-radio" class="radio-label"></label>
            </div>
        </div>
    </div>
    
    <!-- 선택 상태에 따른 추가 정보 -->
    <div class="storage-details" id="storageDetails">
        <div class="detail-content" data-storage="auto">
            <h4>🧠 AI 민감도 분석</h4>
            <p>업로드된 문서를 자동 분석하여 최적의 저장소를 선택합니다.</p>
            <ul class="feature-list">
                <li>민감한 정보 탐지 (주민번호, 계좌번호, 개인정보)</li>
                <li>문서 유형별 정책 적용</li>
                <li>사용자 설정 기반 우선순위 적용</li>
            </ul>
        </div>
    </div>
</div>
```

#### **CSS 스타일링**
```css
/* 저장소 선택 패널 기본 스타일 */
.storage-selector-panel {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 24px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 저장소 옵션 카드 */
.storage-option {
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.storage-option:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
}

.storage-option.selected {
    border-color: var(--primary-500);
    background: rgba(59, 130, 246, 0.15);
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

/* 저장소 아이콘 */
.storage-icon {
    text-align: center;
    margin-bottom: 16px;
}

.icon-container {
    font-size: 3rem;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

/* 저장소 정보 */
.storage-info {
    color: white;
    text-align: center;
}

.storage-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 8px;
}

.storage-description {
    font-size: 0.875rem;
    opacity: 0.8;
    margin-bottom: 12px;
}

/* 기능 태그 */
.storage-features {
    display: flex;
    gap: 6px;
    justify-content: center;
    margin-bottom: 12px;
    flex-wrap: wrap;
}

.feature-tag {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    font-size: 0.75rem;
    padding: 4px 8px;
    border-radius: 12px;
    white-space: nowrap;
}

/* 용량 사용률 바 */
.storage-usage {
    margin-top: 12px;
}

.usage-bar {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 6px;
}

.usage-fill {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #059669);
    border-radius: 3px;
    transition: width 0.5s ease;
}

.usage-fill.warning {
    background: linear-gradient(90deg, #f59e0b, #d97706);
}

.usage-fill.critical {
    background: linear-gradient(90deg, #ef4444, #dc2626);
}

.usage-text {
    font-size: 0.75rem;
    opacity: 0.8;
}

/* 클라우드 서비스 아이콘 */
.cloud-services {
    margin-top: 12px;
}

.service-icons {
    display: flex;
    justify-content: center;
    gap: 8px;
}

.service-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.service-icon img {
    width: 16px;
    height: 16px;
}

.service-icon.connected {
    background: rgba(16, 185, 129, 0.2);
    border: 2px solid #10b981;
}

.service-icon.disconnected {
    background: rgba(107, 114, 128, 0.2);
    border: 2px solid #6b7280;
    opacity: 0.5;
}

.service-icon.locked {
    background: rgba(239, 68, 68, 0.2);
    border: 2px solid #ef4444;
    opacity: 0.5;
}

.service-icon.locked::after {
    content: "🔒";
    position: absolute;
    top: -8px;
    right: -8px;
    font-size: 10px;
    background: #ef4444;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* AI 분석 미리보기 */
.ai-analysis-preview {
    margin-top: 12px;
}

.sensitivity-meter {
    text-align: center;
}

.meter-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 6px;
}

.meter-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

.meter-fill.low {
    background: linear-gradient(90deg, #10b981, #059669);
}

.meter-fill.medium {
    background: linear-gradient(90deg, #f59e0b, #d97706);
}

.meter-fill.high {
    background: linear-gradient(90deg, #ef4444, #dc2626);
}

.sensitivity-label {
    font-size: 0.75rem;
    opacity: 0.8;
}

/* 선택 인디케이터 */
.selection-indicator {
    position: absolute;
    top: 16px;
    right: 16px;
}

.selection-indicator input[type="radio"] {
    display: none;
}

.radio-label {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    background: transparent;
    cursor: pointer;
    position: relative;
    display: block;
    transition: all 0.3s ease;
}

.radio-label::after {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--primary-500);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    transition: transform 0.2s ease;
}

.selection-indicator input[type="radio"]:checked + .radio-label {
    border-color: var(--primary-500);
    background: rgba(59, 130, 246, 0.2);
}

.selection-indicator input[type="radio"]:checked + .radio-label::after {
    transform: translate(-50%, -50%) scale(1);
}

/* 저장소 상세 정보 */
.storage-details {
    margin-top: 20px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-content {
    color: white;
}

.detail-content h4 {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.detail-content p {
    font-size: 0.875rem;
    opacity: 0.8;
    margin-bottom: 12px;
}

.feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.feature-list li {
    font-size: 0.875rem;
    opacity: 0.8;
    margin-bottom: 6px;
    padding-left: 20px;
    position: relative;
}

.feature-list li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #10b981;
    font-weight: bold;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    .storage-selector-panel {
        padding: 16px;
    }
    
    .storage-options {
        grid-template-columns: 1fr;
        gap: 16px;
    }
    
    .storage-option {
        padding: 16px;
    }
    
    .icon-container {
        font-size: 2.5rem;
        height: 60px;
    }
    
    .service-icons {
        gap: 6px;
    }
    
    .service-icon {
        width: 20px;
        height: 20px;
    }
    
    .service-icon img {
        width: 14px;
        height: 14px;
    }
}
```

### **2.2 클라우드 연동 관리 패널**

#### **HTML 구조**
```html
<div class="cloud-connection-manager glass-container">
    <div class="section-header">
        <h3 class="section-title">☁️ 클라우드 연동 관리</h3>
        <div class="plan-indicator">
            <span class="plan-badge professional">프로페셔널 플랜</span>
        </div>
    </div>
    
    <!-- 연결된 서비스 목록 -->
    <div class="cloud-services-list">
        
        <!-- Google Drive -->
        <div class="cloud-service-item connected">
            <div class="service-icon-large google-drive">
                <img src="/icons/google-drive.svg" alt="Google Drive">
            </div>
            <div class="service-info">
                <h4 class="service-name">Google Drive</h4>
                <p class="service-description">15GB 무료 저장공간</p>
                <div class="connection-details">
                    <span class="account-info">user@example.com</span>
                    <span class="connection-time">2시간 전 동기화</span>
                </div>
            </div>
            <div class="service-usage">
                <div class="usage-circle">
                    <svg class="usage-ring" width="60" height="60">
                        <circle cx="30" cy="30" r="25" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="4"/>
                        <circle cx="30" cy="30" r="25" fill="none" stroke="#10b981" stroke-width="4" 
                                stroke-dasharray="157" stroke-dashoffset="78.5" 
                                transform="rotate(-90 30 30)"/>
                    </svg>
                    <span class="usage-percentage">50%</span>
                </div>
                <span class="usage-text">7.5GB / 15GB</span>
            </div>
            <div class="service-actions">
                <button class="action-btn sync" onclick="syncCloudService('google_drive')">
                    <span class="btn-icon">🔄</span>
                    <span class="btn-text">동기화</span>
                </button>
                <button class="action-btn disconnect" onclick="disconnectCloud('google_drive')">
                    <span class="btn-icon">🔗</span>
                    <span class="btn-text">연결 해제</span>
                </button>
            </div>
        </div>
        
        <!-- Dropbox -->
        <div class="cloud-service-item connected">
            <div class="service-icon-large dropbox">
                <img src="/icons/dropbox.svg" alt="Dropbox">
            </div>
            <div class="service-info">
                <h4 class="service-name">Dropbox</h4>
                <p class="service-description">2GB 무료 저장공간</p>
                <div class="connection-details">
                    <span class="account-info">user@company.com</span>
                    <span class="connection-time">1일 전 동기화</span>
                </div>
            </div>
            <div class="service-usage">
                <div class="usage-circle">
                    <svg class="usage-ring" width="60" height="60">
                        <circle cx="30" cy="30" r="25" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="4"/>
                        <circle cx="30" cy="30" r="25" fill="none" stroke="#f59e0b" stroke-width="4" 
                                stroke-dasharray="157" stroke-dashoffset="47.1" 
                                transform="rotate(-90 30 30)"/>
                    </svg>
                    <span class="usage-percentage">70%</span>
                </div>
                <span class="usage-text">1.4GB / 2GB</span>
            </div>
            <div class="service-actions">
                <button class="action-btn sync" onclick="syncCloudService('dropbox')">
                    <span class="btn-icon">🔄</span>
                    <span class="btn-text">동기화</span>
                </button>
                <button class="action-btn disconnect" onclick="disconnectCloud('dropbox')">
                    <span class="btn-icon">🔗</span>
                    <span class="btn-text">연결 해제</span>
                </button>
            </div>
        </div>
        
        <!-- OneDrive - 사용 가능 -->
        <div class="cloud-service-item available">
            <div class="service-icon-large onedrive">
                <img src="/icons/onedrive.svg" alt="OneDrive">
            </div>
            <div class="service-info">
                <h4 class="service-name">Microsoft OneDrive</h4>
                <p class="service-description">5GB 무료 저장공간</p>
                <div class="connection-details">
                    <span class="availability-info">프로페셔널 플랜에서 이용 가능</span>
                </div>
            </div>
            <div class="service-usage">
                <div class="connect-indicator">
                    <div class="connect-icon">
                        <span>+</span>
                    </div>
                </div>
            </div>
            <div class="service-actions">
                <button class="action-btn connect" onclick="connectCloud('onedrive')">
                    <span class="btn-icon">🔗</span>
                    <span class="btn-text">연결하기</span>
                </button>
            </div>
        </div>
        
        <!-- iCloud - 잠금 (엔터프라이즈 전용) -->
        <div class="cloud-service-item locked">
            <div class="service-icon-large icloud">
                <img src="/icons/icloud.svg" alt="iCloud">
                <div class="lock-overlay">🔒</div>
            </div>
            <div class="service-info">
                <h4 class="service-name">Apple iCloud</h4>
                <p class="service-description">5GB 무료 저장공간</p>
                <div class="connection-details">
                    <span class="upgrade-info">엔터프라이즈 플랜 전용</span>
                </div>
            </div>
            <div class="service-usage">
                <div class="upgrade-indicator">
                    <div class="upgrade-icon">
                        <span>⬆️</span>
                    </div>
                </div>
            </div>
            <div class="service-actions">
                <button class="action-btn upgrade" onclick="showUpgradeModal()">
                    <span class="btn-icon">⭐</span>
                    <span class="btn-text">업그레이드</span>
                </button>
            </div>
        </div>
    </div>
    
    <!-- 연동 요약 정보 -->
    <div class="connection-summary">
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-icon">🔗</div>
                <div class="summary-content">
                    <span class="summary-label">연결된 서비스</span>
                    <span class="summary-value">2개</span>
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-icon">☁️</div>
                <div class="summary-content">
                    <span class="summary-label">총 클라우드 용량</span>
                    <span class="summary-value">17GB</span>
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-icon">📊</div>
                <div class="summary-content">
                    <span class="summary-label">사용 중인 용량</span>
                    <span class="summary-value">8.9GB</span>
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-icon">📈</div>
                <div class="summary-content">
                    <span class="summary-label">이번 달 업로드</span>
                    <span class="summary-value">1.2GB</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

#### **CSS 스타일링**
```css
/* 클라우드 연동 관리 패널 */
.cloud-connection-manager {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 24px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.plan-badge {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.plan-badge.starter {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.plan-badge.professional {
    background: linear-gradient(135deg, #10b981, #059669);
}

.plan-badge.enterprise {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

/* 클라우드 서비스 목록 */
.cloud-services-list {
    display: grid;
    gap: 16px;
    margin-bottom: 24px;
}

.cloud-service-item {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    display: grid;
    grid-template-columns: auto 1fr auto auto;
    gap: 16px;
    align-items: center;
    transition: all 0.3s ease;
}

.cloud-service-item:hover {
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-2px);
}

.cloud-service-item.connected {
    border-color: rgba(16, 185, 129, 0.3);
}

.cloud-service-item.locked {
    opacity: 0.6;
    border-color: rgba(239, 68, 68, 0.3);
}

/* 서비스 아이콘 */
.service-icon-large {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.service-icon-large.google-drive {
    background: rgba(66, 133, 244, 0.2);
}

.service-icon-large.dropbox {
    background: rgba(0, 97, 255, 0.2);
}

.service-icon-large.onedrive {
    background: rgba(0, 120, 212, 0.2);
}

.service-icon-large.icloud {
    background: rgba(0, 122, 255, 0.2);
}

.service-icon-large img {
    width: 32px;
    height: 32px;
}

.lock-overlay {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #ef4444;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
}

/* 서비스 정보 */
.service-info {
    color: white;
}

.service-name {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 4px;
}

.service-description {
    font-size: 0.875rem;
    opacity: 0.7;
    margin-bottom: 8px;
}

.connection-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.account-info {
    font-size: 0.75rem;
    color: #10b981;
    font-weight: 500;
}

.connection-time {
    font-size: 0.75rem;
    opacity: 0.6;
}

.availability-info,
.upgrade-info {
    font-size: 0.75rem;
    opacity: 0.8;
}

/* 사용량 표시 */
.service-usage {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.usage-circle {
    position: relative;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.usage-percentage {
    position: absolute;
    font-size: 0.875rem;
    font-weight: 600;
    color: white;
}

.usage-text {
    font-size: 0.75rem;
    opacity: 0.8;
    white-space: nowrap;
}

.connect-indicator,
.upgrade-indicator {
    width: 60px;
    height: 60px;
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.connect-icon,
.upgrade-icon {
    font-size: 1.5rem;
    opacity: 0.6;
}

/* 액션 버튼 */
.service-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.action-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
}

.action-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
}

.action-btn.sync {
    border-color: rgba(16, 185, 129, 0.5);
}

.action-btn.sync:hover {
    background: rgba(16, 185, 129, 0.2);
}

.action-btn.connect {
    border-color: rgba(59, 130, 246, 0.5);
}

.action-btn.connect:hover {
    background: rgba(59, 130, 246, 0.2);
}

.action-btn.upgrade {
    border-color: rgba(139, 92, 246, 0.5);
}

.action-btn.upgrade:hover {
    background: rgba(139, 92, 246, 0.2);
}

.action-btn.disconnect {
    border-color: rgba(239, 68, 68, 0.5);
}

.action-btn.disconnect:hover {
    background: rgba(239, 68, 68, 0.2);
}

.btn-icon {
    font-size: 0.875rem;
}

/* 연동 요약 */
.connection-summary {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 20px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.summary-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.05);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-icon {
    font-size: 1.5rem;
    opacity: 0.8;
}

.summary-content {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.summary-label {
    font-size: 0.75rem;
    opacity: 0.7;
    color: white;
}

.summary-value {
    font-size: 1rem;
    font-weight: 600;
    color: white;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    .cloud-connection-manager {
        padding: 16px;
    }
    
    .section-header {
        flex-direction: column;
        gap: 12px;
        align-items: flex-start;
    }
    
    .cloud-service-item {
        grid-template-columns: 1fr;
        gap: 12px;
        text-align: center;
    }
    
    .service-actions {
        flex-direction: row;
        justify-content: center;
    }
    
    .summary-grid {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .summary-item {
        padding: 12px;
    }
}
```

---

## 🔧 **3. JavaScript 인터랙션 로직**

### **3.1 저장소 선택 관리**

```javascript
class HybridStorageManager {
    constructor() {
        this.selectedStorage = 'auto';
        this.sensitivityScore = 0;
        this.userPreferences = this.loadUserPreferences();
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        // 저장소 옵션 선택 이벤트
        document.querySelectorAll('.storage-option').forEach(option => {
            option.addEventListener('click', (e) => {
                const storageType = e.currentTarget.dataset.storage;
                this.selectStorage(storageType);
            });
        });
        
        // 파일 업로드 시 민감도 분석
        document.addEventListener('fileUploaded', (e) => {
            if (this.selectedStorage === 'auto') {
                this.analyzeSensitivity(e.detail.fileContent);
            }
        });
    }
    
    selectStorage(storageType) {
        this.selectedStorage = storageType;
        
        // UI 업데이트
        document.querySelectorAll('.storage-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        document.querySelector(`[data-storage="${storageType}"]`).classList.add('selected');
        
        // 라디오 버튼 업데이트
        document.querySelector(`input[value="${storageType}"]`).checked = true;
        
        // 상세 정보 표시
        this.showStorageDetails(storageType);
        
        // 알림 표시
        this.showNotification(`${this.getStorageDisplayName(storageType)} 저장소가 선택되었습니다.`, 'info');
    }
    
    async analyzeSensitivity(fileContent) {
        try {
            // 로딩 상태 표시
            this.showSensitivityAnalyzing();
            
            // AI 민감도 분석 API 호출
            const response = await fetch('/api/analyze-sensitivity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.getAuthToken()}`
                },
                body: JSON.stringify({
                    content: fileContent.substring(0, 2000), // 처음 2000자만 분석
                    userId: this.getCurrentUserId()
                })
            });
            
            const result = await response.json();
            this.sensitivityScore = result.sensitivityScore;
            
            // UI 업데이트
            this.updateSensitivityMeter(this.sensitivityScore);
            
            // 추천 저장소 결정
            const recommendedStorage = this.getRecommendedStorage(this.sensitivityScore);
            this.showStorageRecommendation(recommendedStorage, this.sensitivityScore);
            
        } catch (error) {
            console.error('민감도 분석 실패:', error);
            this.showNotification('민감도 분석에 실패했습니다. 수동으로 저장소를 선택해주세요.', 'error');
        }
    }
    
    getRecommendedStorage(sensitivityScore) {
        const { securityFirst, convenienceFirst } = this.userPreferences;
        
        if (sensitivityScore > 0.7) {
            return 'server'; // 고민감도 - 무조건 서버
        } else if (sensitivityScore < 0.3) {
            return 'cloud';  // 저민감도 - 무조건 클라우드
        } else {
            // 중간민감도 - 사용자 설정에 따라
            return securityFirst ? 'server' : 'cloud';
        }
    }
    
    updateSensitivityMeter(score) {
        const meter = document.querySelector('.meter-fill');
        const label = document.querySelector('.sensitivity-label');
        
        if (meter && label) {
            // 진행바 업데이트
            meter.style.width = `${score * 100}%`;
            
            // 색상 및 라벨 업데이트
            meter.className = 'meter-fill ' + this.getSensitivityLevel(score);
            label.textContent = `민감도: ${this.getSensitivityText(score)} (${Math.round(score * 100)}%)`;
        }
    }
    
    getSensitivityLevel(score) {
        if (score < 0.3) return 'low';
        if (score < 0.7) return 'medium';
        return 'high';
    }
    
    getSensitivityText(score) {
        if (score < 0.3) return '낮음';
        if (score < 0.7) return '보통';
        return '높음';
    }
    
    showStorageRecommendation(recommendedStorage, score) {
        const recommendation = document.createElement('div');
        recommendation.className = 'storage-recommendation';
        recommendation.innerHTML = `
            <div class="recommendation-content">
                <h4>🤖 AI 추천</h4>
                <p>문서 분석 결과, <strong>${this.getStorageDisplayName(recommendedStorage)}</strong> 저장소를 추천합니다.</p>
                <div class="recommendation-actions">
                    <button class="btn-accept" onclick="hybridStorage.acceptRecommendation('${recommendedStorage}')">
                        추천 사용
                    </button>
                    <button class="btn-dismiss" onclick="hybridStorage.dismissRecommendation()">
                        무시
                    </button>
                </div>
            </div>
        `;
        
        // 기존 추천 제거
        const existing = document.querySelector('.storage-recommendation');
        if (existing) existing.remove();
        
        // 새 추천 추가
        document.querySelector('.storage-selector-panel').appendChild(recommendation);
        
        // 3초 후 자동 사라짐
        setTimeout(() => {
            if (recommendation.parentNode) {
                recommendation.remove();
            }
        }, 8000);
    }
    
    acceptRecommendation(storageType) {
        this.selectStorage(storageType);
        this.dismissRecommendation();
        this.showNotification('AI 추천을 적용했습니다.', 'success');
    }
    
    dismissRecommendation() {
        const recommendation = document.querySelector('.storage-recommendation');
        if (recommendation) {
            recommendation.remove();
        }
    }
    
    getStorageDisplayName(storageType) {
        const names = {
            'server': '서버 저장소',
            'cloud': '클라우드 연동',
            'auto': 'AI 자동 선택'
        };
        return names[storageType] || storageType;
    }
    
    loadUserPreferences() {
        return JSON.parse(localStorage.getItem('paperwork_storage_preferences') || JSON.stringify({
            securityFirst: true,
            convenienceFirst: false,
            autoAnalysis: true
        }));
    }
    
    showNotification(message, type) {
        // 기존 알림 시스템 활용
        if (window.uiComponents) {
            window.uiComponents.showNotification(message, type);
        }
    }
    
    getCurrentUserId() {
        return localStorage.getItem('current_user_id') || 'anonymous';
    }
    
    getAuthToken() {
        return localStorage.getItem('auth_token') || '';
    }
}

// 전역 인스턴스 생성
const hybridStorage = new HybridStorageManager();
```

### **3.2 클라우드 연동 관리**

```javascript
class CloudConnectionManager {
    constructor() {
        this.connectedServices = this.loadConnectedServices();
        this.supportedServices = {
            'google_drive': {
                name: 'Google Drive',
                icon: '/icons/google-drive.svg',
                freeStorage: '15GB',
                authUrl: 'https://accounts.google.com/oauth/authorize'
            },
            'dropbox': {
                name: 'Dropbox',
                icon: '/icons/dropbox.svg',
                freeStorage: '2GB',
                authUrl: 'https://www.dropbox.com/oauth2/authorize'
            },
            'onedrive': {
                name: 'Microsoft OneDrive',
                icon: '/icons/onedrive.svg',
                freeStorage: '5GB',
                authUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
            },
            'icloud': {
                name: 'Apple iCloud',
                icon: '/icons/icloud.svg',
                freeStorage: '5GB',
                requiresPlan: 'enterprise'
            }
        };
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        // 동기화 버튼 이벤트
        document.addEventListener('click', (e) => {
            if (e.target.closest('.action-btn.sync')) {
                const serviceId = e.target.closest('.cloud-service-item').dataset.service;
                this.syncCloudService(serviceId);
            }
        });
    }
    
    async connectCloud(serviceId) {
        try {
            const service = this.supportedServices[serviceId];
            if (!service) {
                throw new Error('지원하지 않는 서비스입니다.');
            }
            
            // 요금제 확인
            if (service.requiresPlan && !this.checkPlanAccess(service.requiresPlan)) {
                this.showUpgradeModal(service.requiresPlan);
                return;
            }
            
            // OAuth 인증 프로세스 시작
            this.showLoadingState(serviceId, '연결 중...');
            
            const authResult = await this.performOAuthFlow(serviceId);
            
            if (authResult.success) {
                // 연결 정보 저장
                this.connectedServices[serviceId] = {
                    accessToken: authResult.accessToken,
                    refreshToken: authResult.refreshToken,
                    accountInfo: authResult.accountInfo,
                    connectedAt: new Date().toISOString()
                };
                
                this.saveConnectedServices();
                this.updateServiceUI(serviceId, 'connected');
                this.showNotification(`${service.name} 연결이 완료되었습니다.`, 'success');
                
                // 초기 동기화
                await this.syncCloudService(serviceId);
                
            } else {
                throw new Error(authResult.error || '연결에 실패했습니다.');
            }
            
        } catch (error) {
            console.error('클라우드 연결 실패:', error);
            this.showNotification(`연결 실패: ${error.message}`, 'error');
            this.hideLoadingState(serviceId);
        }
    }
    
    async syncCloudService(serviceId) {
        try {
            const service = this.connectedServices[serviceId];
            if (!service) {
                throw new Error('연결되지 않은 서비스입니다.');
            }
            
            this.showSyncingState(serviceId);
            
            // API를 통해 클라우드 파일 목록 가져오기
            const response = await fetch('/api/cloud/sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.getAuthToken()}`
                },
                body: JSON.stringify({
                    serviceId,
                    accessToken: service.accessToken
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // 동기화 결과 UI 업데이트
                this.updateSyncStatus(serviceId, result.data);
                this.showNotification(`${this.supportedServices[serviceId].name} 동기화 완료`, 'success');
            } else {
                throw new Error(result.error || '동기화에 실패했습니다.');
            }
            
        } catch (error) {
            console.error('동기화 실패:', error);
            this.showNotification(`동기화 실패: ${error.message}`, 'error');
        } finally {
            this.hideSyncingState(serviceId);
        }
    }
    
    async disconnectCloud(serviceId) {
        const service = this.supportedServices[serviceId];
        
        const confirmed = await this.showConfirmDialog(
            `${service.name} 연결 해제`,
            `${service.name} 연결을 해제하시겠습니까? 로컬에 저장된 파일은 그대로 유지됩니다.`
        );
        
        if (confirmed) {
            try {
                // 서버에서 연결 해제
                await fetch('/api/cloud/disconnect', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.getAuthToken()}`
                    },
                    body: JSON.stringify({ serviceId })
                });
                
                // 로컬 연결 정보 삭제
                delete this.connectedServices[serviceId];
                this.saveConnectedServices();
                
                // UI 업데이트
                this.updateServiceUI(serviceId, 'available');
                this.showNotification(`${service.name} 연결이 해제되었습니다.`, 'info');
                
            } catch (error) {
                console.error('연결 해제 실패:', error);
                this.showNotification('연결 해제에 실패했습니다.', 'error');
            }
        }
    }
    
    updateServiceUI(serviceId, status) {
        const serviceItem = document.querySelector(`[data-service="${serviceId}"]`);
        if (!serviceItem) return;
        
        // 클래스 업데이트
        serviceItem.className = `cloud-service-item ${status}`;
        
        // 액션 버튼 업데이트
        const actionsContainer = serviceItem.querySelector('.service-actions');
        actionsContainer.innerHTML = this.generateActionButtons(serviceId, status);
        
        // 사용량 정보 업데이트
        if (status === 'connected') {
            this.updateUsageDisplay(serviceId);
        }
    }
    
    generateActionButtons(serviceId, status) {
        switch (status) {
            case 'connected':
                return `
                    <button class="action-btn sync" onclick="cloudManager.syncCloudService('${serviceId}')">
                        <span class="btn-icon">🔄</span>
                        <span class="btn-text">동기화</span>
                    </button>
                    <button class="action-btn disconnect" onclick="cloudManager.disconnectCloud('${serviceId}')">
                        <span class="btn-icon">🔗</span>
                        <span class="btn-text">연결 해제</span>
                    </button>
                `;
            case 'available':
                return `
                    <button class="action-btn connect" onclick="cloudManager.connectCloud('${serviceId}')">
                        <span class="btn-icon">🔗</span>
                        <span class="btn-text">연결하기</span>
                    </button>
                `;
            case 'locked':
                return `
                    <button class="action-btn upgrade" onclick="cloudManager.showUpgradeModal()">
                        <span class="btn-icon">⭐</span>
                        <span class="btn-text">업그레이드</span>
                    </button>
                `;
            default:
                return '';
        }
    }
    
    async updateUsageDisplay(serviceId) {
        try {
            const usage = await this.getCloudUsage(serviceId);
            const usageCircle = document.querySelector(`[data-service="${serviceId}"] .usage-circle`);
            
            if (usageCircle && usage) {
                const percentage = Math.round((usage.used / usage.total) * 100);
                const circumference = 2 * Math.PI * 25; // r=25
                const strokeDashoffset = circumference - (percentage / 100) * circumference;
                
                // SVG 업데이트
                const circle = usageCircle.querySelector('circle:last-child');
                circle.style.strokeDashoffset = strokeDashoffset;
                
                // 텍스트 업데이트
                usageCircle.querySelector('.usage-percentage').textContent = `${percentage}%`;
                
                // 사용량 텍스트 업데이트
                const usageText = usageCircle.parentNode.querySelector('.usage-text');
                usageText.textContent = `${this.formatBytes(usage.used)} / ${this.formatBytes(usage.total)}`;
                
                // 색상 업데이트 (사용량에 따라)
                const color = percentage > 80 ? '#ef4444' : percentage > 60 ? '#f59e0b' : '#10b981';
                circle.style.stroke = color;
            }
            
        } catch (error) {
            console.error('사용량 정보 업데이트 실패:', error);
        }
    }
    
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    loadConnectedServices() {
        return JSON.parse(localStorage.getItem('connected_cloud_services') || '{}');
    }
    
    saveConnectedServices() {
        localStorage.setItem('connected_cloud_services', JSON.stringify(this.connectedServices));
    }
    
    checkPlanAccess(requiredPlan) {
        const currentPlan = localStorage.getItem('current_plan') || 'starter';
        const planLevels = { 'starter': 1, 'professional': 2, 'enterprise': 3 };
        
        return planLevels[currentPlan] >= planLevels[requiredPlan];
    }
    
    showUpgradeModal(requiredPlan = 'enterprise') {
        // 업그레이드 모달 표시 로직
        console.log(`${requiredPlan} 플랜으로 업그레이드가 필요합니다.`);
    }
    
    getAuthToken() {
        return localStorage.getItem('auth_token') || '';
    }
}

// 전역 인스턴스 생성
const cloudManager = new CloudConnectionManager();
```

---

## 🎨 **4. 컴포넌트 사용 가이드**

### **4.1 기본 구현 단계**

1. **HTML 구조 복사**: 위의 HTML 코드를 기존 editor.html에 통합
2. **CSS 스타일 적용**: 기존 Glassmorphism 스타일과 조화되도록 CSS 추가
3. **JavaScript 초기화**: HybridStorageManager와 CloudConnectionManager 인스턴스 생성
4. **API 엔드포인트 연결**: 백엔드 민감도 분석 및 클라우드 연동 API 구현

### **4.2 커스터마이징 옵션**

#### **색상 테마 변경**
```css
:root {
    --hybrid-primary: #3b82f6;     /* 메인 테마 색상 */
    --hybrid-success: #10b981;     /* 성공/연결 상태 */
    --hybrid-warning: #f59e0b;     /* 경고/중간 상태 */
    --hybrid-danger: #ef4444;      /* 위험/차단 상태 */
}
```

#### **요금제별 기능 제한**
```javascript
const planFeatures = {
    starter: {
        serverStorage: 20, // MB
        cloudServices: ['google_drive'],
        aiAnalysis: 'basic'
    },
    professional: {
        serverStorage: 50,
        cloudServices: ['google_drive', 'dropbox', 'onedrive'],
        aiAnalysis: 'advanced'
    },
    enterprise: {
        serverStorage: 100,
        cloudServices: ['google_drive', 'dropbox', 'onedrive', 'icloud'],
        aiAnalysis: 'premium'
    }
};
```

### **4.3 접근성 고려사항**

- **키보드 내비게이션**: Tab 키로 모든 컴포넌트 접근 가능
- **스크린 리더**: aria-label과 role 속성으로 의미 전달
- **색상 대비**: WCAG 2.1 AA 기준 4.5:1 이상 대비율
- **포커스 표시**: 명확한 포커스 링과 상태 표시

---

## 🚀 **5. 배포 및 통합 가이드**

### **5.1 기존 시스템과의 통합**

현재 운영 중인 paperwork.heal7.com/editor.html에 하이브리드 저장소 컴포넌트를 통합하는 방법:

1. **2단계 워크플로우 수정**: "추출 옵션" → "저장소 선택"으로 변경
2. **Quill.js 에디터 연동**: 문서 저장 시 선택된 저장소 정보 활용
3. **AI 모델 선택과 연계**: 저장소별 AI 모델 추천 기능 추가

### **5.2 성능 최적화**

- **레이지 로딩**: 클라우드 연동 컴포넌트는 필요 시에만 로드
- **캐싱**: 민감도 분석 결과와 클라우드 사용량 정보 캐싱
- **압축**: CSS/JS 파일 최소화 및 Gzip 압축

---

이 가이드를 통해 기존 Paperwork AI 시스템에 B2B 하이브리드 저장소 기능을 완벽하게 통합할 수 있습니다. 각 컴포넌트는 독립적으로 작동하면서도 전체 시스템과 조화를 이루도록 설계되었습니다.