# 📚 Reference Docs - 개발 표준 및 가이드

## 🎯 목적
- **개발 표준** 문서화 및 일관성 유지
- **외부 API** 통합 가이드 제공
- **모범 사례** 수집 및 공유
- **문제 해결** 가이드 제공

## 📂 구조

### **technical-standards/** - 기술 표준
```
heal7-coding-standards.md      # HEAL7 코딩 표준
api-design-principles.md       # API 설계 원칙
database-conventions.md        # 데이터베이스 명명 규칙
security-guidelines.md         # 보안 가이드라인
```

### **external-apis/** - 외부 API 문서
```
kasi-api-documentation.md      # KASI API 사용법
gemini-ai-guide.md            # Gemini AI 통합 가이드
openai-integration.md         # OpenAI 통합 가이드
payment-gateway-docs.md       # 결제 게이트웨이 문서
```

### **best-practices/** - 모범 사례
```
react-best-practices.md       # React 개발 모범 사례
fastapi-patterns.md           # FastAPI 패턴
postgresql-optimization.md     # PostgreSQL 최적화
nginx-configuration.md         # Nginx 설정 모범 사례
```

### **troubleshooting/** - 문제 해결
```
common-issues-solutions.md     # 일반적 문제 해결
performance-debugging.md       # 성능 디버깅 가이드
deployment-problems.md         # 배포 문제 해결
database-issues.md            # 데이터베이스 문제 해결
```

### **compliance/** - 컴플라이언스
```
privacy-policy-template.md     # 개인정보 보호정책 템플릿
terms-of-service.md           # 서비스 이용약관
korean-privacy-law.md         # 한국 개인정보보호법 가이드
```

## 📝 문서 작성 표준

### **표준 문서 템플릿**
```markdown
# [문서 제목]

> **목적**: [이 문서의 목적]
> **대상**: [대상 독자]
> **최종 업데이트**: [날짜]

## 📋 개요
[문서의 전체적인 개요]

## 🎯 핵심 내용
### 주요 포인트 1
[상세 설명]

### 주요 포인트 2
[상세 설명]

## 💻 코드 예시
```javascript
// 명확하고 실용적인 예시 코드
const example = () => {
    return "실제 사용 가능한 코드";
};
```

## ⚠️ 주의사항
- [중요한 주의사항 1]
- [중요한 주의사항 2]

## 🔗 관련 자료
- [Link 1: 관련 문서]
- [Link 2: 외부 리소스]

## 📅 변경 이력
- **v1.1** (2025-08-18): [변경 내용]
- **v1.0** (2025-08-15): 초기 작성
```

## 🔧 기술 표준 가이드

### **코딩 스타일**
```typescript
// HEAL7 TypeScript 코딩 표준
interface SajuResult {
  userId: string;           // camelCase 사용
  birthData: BirthData;     // 명확한 타입 정의
  calculationResult: {      // 중첩 객체 구조화
    pillars: Pillar[];
    elements: Element[];
  };
  createdAt: Date;         // 표준 날짜 타입
}

// 함수명은 동사로 시작
const calculateSaju = async (birthData: BirthData): Promise<SajuResult> => {
  // 에러 처리 필수
  if (!validateBirthData(birthData)) {
    throw new Error('Invalid birth data');
  }
  
  // 명확한 변수명 사용
  const calculationResult = await performCalculation(birthData);
  
  return {
    userId: birthData.userId,
    birthData,
    calculationResult,
    createdAt: new Date()
  };
};
```

### **API 설계 원칙**
```yaml
# RESTful API 설계 표준
paths:
  /api/v1/saju:
    post:
      summary: "사주 계산 요청"
      operationId: "calculateSaju"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SajuRequest'
      responses:
        '200':
          description: "계산 성공"
        '400':
          description: "잘못된 요청"
        '500':
          description: "서버 오류"
```

## 📊 데이터베이스 표준

### **명명 규칙**
```sql
-- 테이블명: snake_case, 복수형
CREATE TABLE saju_results (
  id UUID PRIMARY KEY,                    -- UUID 사용
  user_id UUID NOT NULL,                 -- 외래키 명확 표시
  birth_data JSONB NOT NULL,             -- JSON 데이터는 JSONB
  calculation_result JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),  -- 타임존 포함
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스명: idx_[테이블명]_[컬럼명]
CREATE INDEX idx_saju_results_user_id ON saju_results(user_id);
CREATE INDEX idx_saju_results_created_at ON saju_results(created_at);
```

## 🛡️ 보안 가이드라인

### **API 보안**
```python
# JWT 토큰 검증
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### **데이터 검증**
```python
# Pydantic을 사용한 데이터 검증
from pydantic import BaseModel, validator
from datetime import datetime

class BirthData(BaseModel):
    birth_year: int
    birth_month: int  
    birth_day: int
    birth_hour: int
    
    @validator('birth_year')
    def validate_year(cls, v):
        if not (1900 <= v <= datetime.now().year):
            raise ValueError('유효하지 않은 연도입니다')
        return v
```

## 🚀 성능 최적화

### **데이터베이스 최적화**
```sql
-- 쿼리 최적화 예시
EXPLAIN ANALYZE
SELECT sr.*, u.name
FROM saju_results sr
JOIN users u ON sr.user_id = u.id
WHERE sr.created_at >= '2025-01-01'
  AND u.active = true
ORDER BY sr.created_at DESC
LIMIT 20;

-- 인덱스 활용 최적화
CREATE INDEX idx_saju_results_active_users 
ON saju_results(created_at DESC) 
WHERE user_id IN (SELECT id FROM users WHERE active = true);
```

## 📱 프론트엔드 표준

### **React 컴포넌트**
```tsx
// HEAL7 React 컴포넌트 표준
interface SajuCalculatorProps {
  onCalculate: (result: SajuResult) => void;
  loading?: boolean;
}

export const SajuCalculator: React.FC<SajuCalculatorProps> = ({
  onCalculate,
  loading = false
}) => {
  const [birthData, setBirthData] = useState<BirthData | null>(null);
  
  const handleSubmit = useCallback(async (data: BirthData) => {
    try {
      const result = await calculateSaju(data);
      onCalculate(result);
    } catch (error) {
      // 에러 처리는 상위 컴포넌트로 전파
      throw error;
    }
  }, [onCalculate]);
  
  return (
    <div className="saju-calculator">
      {/* JSX 구조 */}
    </div>
  );
};
```

## 🔍 트러블슈팅 가이드

### **일반적 문제들**
```markdown
## 문제: CORS 에러
**증상**: 브라우저에서 API 호출 시 CORS 에러 발생
**원인**: 백엔드에서 CORS 설정 누락
**해결책**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
```

## ✅ 문서 품질 기준
- [ ] 목적과 대상이 명확히 명시됨
- [ ] 실용적인 예시 코드 포함
- [ ] 단계별 가이드 제공
- [ ] 주의사항과 한계점 명시
- [ ] 관련 자료와 링크 제공
- [ ] 정기적 업데이트 이력 관리