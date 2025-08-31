# 🔴 HEAL7 사주서비스 Redis 캐시 스키마

> **목적**: 사주 계산 결과 및 자주 조회되는 데이터의 고속 캐싱
> **DB**: Redis (키-밸류 스토어)
> **TTL**: Time To Live (자동 만료)

## 🔑 **키 네이밍 컨벤션**

### 기본 패턴
```
saju:{category}:{identifier}:{sub_key}
```

- **saju**: 서비스 네임스페이스
- **category**: 데이터 카테고리 (chart, fortune, kasi 등)
- **identifier**: 고유 식별자 (user_id, chart_id 등)
- **sub_key**: 상세 분류 (optional)

## 📊 **캐시 데이터 구조**

### 1. 🔮 **사주 계산 결과 캐시**

#### 사주 차트 기본 정보
```redis
KEY: saju:chart:{chart_id}
TYPE: Hash
TTL: 7 days
VALUE: {
  "birth_year": "1990",
  "birth_month": "5", 
  "birth_day": "15",
  "birth_hour": "14",
  "year_gan": "경",
  "year_ji": "오",
  "month_gan": "신",  
  "month_ji": "사",
  "day_gan": "갑",
  "day_ji": "인", 
  "hour_gan": "신",
  "hour_ji": "미",
  "calculated_at": "2024-03-15T10:30:00Z"
}
```

#### 사주 해석 요약
```redis
KEY: saju:interpretation:{chart_id}:{type}
TYPE: String (JSON)
TTL: 1 day
VALUE: {
  "overall_score": 8.5,
  "personality_summary": "강한 의지력과 창의성을 가진...",
  "career_advice": "리더십을 발휘할 수 있는 분야...",  
  "keywords": ["리더십", "창의성", "독립성"],
  "cached_at": "2024-03-15T10:30:00Z"
}

# type 예시: personality, career, health, wealth
```

### 2. 🎯 **운세 예측 캐시**

#### 일일 운세
```redis
KEY: saju:fortune:daily:{chart_id}:{date}
TYPE: Hash
TTL: 1 day (자정에 만료)
VALUE: {
  "overall_score": "7.8",
  "career_score": "8.2", 
  "wealth_score": "6.5",
  "health_score": "7.0",
  "relationship_score": "8.5",
  "lucky_color": "파란색",
  "lucky_number": "3,7,9",
  "caution_time": "14:00-16:00",
  "advice": "오전에 중요한 결정을 내리세요"
}
```

#### 월운세 
```redis
KEY: saju:fortune:monthly:{chart_id}:{year_month}
TYPE: String (JSON) 
TTL: 30 days
VALUE: {
  "monthly_theme": "발전과 성장의 시기",
  "career_forecast": "새로운 기회 도래",
  "wealth_trend": "안정적 증가", 
  "health_focus": ["소화기", "스트레스"],
  "relationship_advice": "소통 중시",
  "lucky_dates": ["3", "12", "21"],
  "caution_dates": ["7", "16", "25"]
}
```

### 3. ⚖️ **궁합 분석 캐시**

#### 궁합 점수
```redis
KEY: saju:compatibility:{chart_id1}:{chart_id2}
TYPE: Hash
TTL: 7 days
VALUE: {
  "overall_score": "8.7",
  "personality_score": "8.5",
  "career_score": "7.2",
  "health_score": "8.0", 
  "wealth_score": "7.8",
  "compatibility_level": "excellent",
  "key_strength": "가치관 일치",
  "potential_issue": "고집 충돌",
  "analysis_type": "romantic"
}
```

### 4. 🗓️ **KASI 절기 정보 캐시**

#### 절기 데이터
```redis
KEY: saju:kasi:solar_term:{year}:{term_index}
TYPE: Hash  
TTL: 365 days (1년)
VALUE: {
  "term_name": "입춘",
  "term_date": "2024-02-04",
  "term_time": "16:27:00",
  "next_term": "우수",
  "next_date": "2024-02-19", 
  "gan_ji": "갑인년 을축월"
}
```

#### 음력 변환 캐시
```redis
KEY: saju:kasi:lunar:{solar_date}
TYPE: String (JSON)
TTL: 180 days
VALUE: {
  "solar_date": "2024-03-15",
  "lunar_year": 2024,
  "lunar_month": 2,
  "lunar_day": 6,
  "is_leap_month": false,
  "gan_ji_year": "갑진",
  "gan_ji_month": "정묘", 
  "gan_ji_day": "기축"
}
```

### 5. 🚀 **성능 최적화 캐시**

#### 자주 조회되는 사주 조합
```redis
KEY: saju:popular:{gan_ji_combination}
TYPE: Sorted Set (점수순 정렬)
TTL: 1 week
VALUE: {
  chart_id1: score1,
  chart_id2: score2,
  chart_id3: score3
}
```

#### API 응답 캐시
```redis  
KEY: saju:api:{endpoint}:{params_hash}
TYPE: String (JSON)
TTL: 1 hour
VALUE: {
  "data": {...},
  "timestamp": "2024-03-15T10:30:00Z",
  "cache_version": "2.0"
}
```

### 6. 🔐 **세션 및 인증 캐시**

#### 사용자 세션
```redis
KEY: saju:session:{user_id}
TYPE: Hash
TTL: 24 hours
VALUE: {
  "session_id": "uuid-string",
  "last_activity": "2024-03-15T10:30:00Z",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "permissions": "user,premium"
}
```

#### JWT 토큰 블랙리스트
```redis
KEY: saju:blacklist:token:{token_jti}
TYPE: String
TTL: token의 남은 만료시간
VALUE: "revoked_at:2024-03-15T10:30:00Z"
```

## ⚡ **성능 최적화 전략**

### 1. Pipeline 사용
```python
# 여러 캐시 데이터 한번에 조회
pipe = redis.pipeline()
pipe.hgetall(f"saju:chart:{chart_id}")
pipe.get(f"saju:fortune:daily:{chart_id}:{today}")  
pipe.hgetall(f"saju:session:{user_id}")
results = pipe.execute()
```

### 2. 캐시 워밍 (Cache Warming)
```python
# 인기 있는 사주 조합 미리 캐싱
popular_combinations = get_popular_saju_combinations()
for combo in popular_combinations:
    calculate_and_cache_saju(combo)
```

### 3. 캐시 무효화 (Cache Invalidation)
```python
# 사주 데이터 수정 시 관련 캐시 삭제
def invalidate_saju_cache(chart_id):
    keys_to_delete = [
        f"saju:chart:{chart_id}",
        f"saju:interpretation:{chart_id}:*",
        f"saju:fortune:*:{chart_id}:*"  
    ]
    redis.delete(*keys_to_delete)
```

## 📊 **모니터링 메트릭**

### Redis 성능 지표
```redis
# 캐시 히트율 추적
KEY: saju:metrics:hit_rate:{date}
TYPE: Hash
VALUE: {
  "total_requests": "10000",
  "cache_hits": "8500", 
  "hit_rate": "85.0",
  "miss_rate": "15.0"
}

# 자주 사용되는 키 추적  
KEY: saju:metrics:popular_keys:{date}
TYPE: Sorted Set
VALUE: {
  "saju:chart:*": 5000,
  "saju:fortune:daily:*": 3000,
  "saju:kasi:*": 1500
}
```

## 🔧 **운영 가이드**

### 메모리 관리
- **Max Memory**: 2GB 
- **Eviction Policy**: allkeys-lru (가장 오래된 키 자동 삭제)
- **Persistence**: AOF enabled (데이터 안정성)

### 백업 전략
- **일일 백업**: 매일 새벽 3시 자동 백업  
- **실시간 백업**: AOF 파일을 통한 실시간 백업
- **클러스터링**: 고가용성을 위한 Redis Cluster 구성 (추후)