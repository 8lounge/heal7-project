# 💳 HEAL7 구독 & 결제 시스템 아키텍처 v1.0

> **프로젝트**: HEAL7 사주사이트 구독 및 결제 시스템  
> **버전**: v1.0.0  
> **설계일**: 2025-08-18  
> **최종 수정**: 2025-08-18 15:30 KST  
> **설계자**: HEAL7 Payment & Subscription Team  
> **목표**: 유연하고 확장 가능한 구독 기반 수익 모델 구축

## 🎯 **비즈니스 모델 개요**

### **💎 구독 플랜 체계**
```yaml
# 💰 Subscription Plans
subscription_tiers:
  free:
    name: "무료 체험"
    price: 0
    duration: "unlimited"
    features:
      - "월 3회 기본 사주 분석"
      - "간단한 타로 리딩"
      - "커뮤니티 읽기 전용"
      - "광고 포함"
    limits:
      saju_calculations: 3
      tarot_readings: 5
      community_posts: 0
      ai_interpretations: false
      
  basic:
    name: "기본 운세"
    price: 9900
    currency: "KRW"
    duration: "monthly"
    features:
      - "월 50회 사주 분석"
      - "무제한 타로 리딩"
      - "12지신 운세 포함"
      - "커뮤니티 참여"
      - "광고 제거"
    limits:
      saju_calculations: 50
      tarot_readings: -1  # unlimited
      zodiac_analyses: 10
      community_posts: 10
      ai_interpretations: true
      
  premium:
    name: "프리미엄 운세"
    price: 19900
    currency: "KRW"
    duration: "monthly"
    features:
      - "무제한 사주 분석"
      - "프리미엄 타로 + 12지신"
      - "별자리 + 풍수지리"
      - "AI 상세 해석"
      - "1:1 상담 월 2회"
      - "프리미엄 매거진"
    limits:
      saju_calculations: -1  # unlimited
      tarot_readings: -1
      zodiac_analyses: -1
      astrology_readings: 20
      fengshui_analyses: 10
      consultation_sessions: 2
      ai_interpretations: true
      premium_content: true
      
  master:
    name: "마스터 운세"
    price: 39900
    currency: "KRW" 
    duration: "monthly"
    features:
      - "모든 서비스 무제한"
      - "전문가 1:1 상담 무제한"
      - "개인 맞춤 리포트"
      - "우선 고객지원"
      - "특별 이벤트 접근"
      - "API 접근 권한"
    limits:
      all_services: -1  # unlimited
      consultation_sessions: -1
      priority_support: true
      custom_reports: true
      api_access: true

# 🎁 연간 구독 할인
annual_discounts:
  basic: 20%    # 2개월 무료
  premium: 25%  # 3개월 무료
  master: 30%   # 3.6개월 무료
```

### **🪙 포인트 시스템**
```yaml
# 💰 Point System
point_system:
  # 💵 충전 패키지
  purchase_packages:
    starter:
      points: 1000
      price: 1000
      bonus: 0
      
    regular:
      points: 5000
      price: 5000
      bonus: 500  # 10% 보너스
      
    premium:
      points: 10000
      price: 10000
      bonus: 1500  # 15% 보너스
      
    mega:
      points: 50000
      price: 50000
      bonus: 10000  # 20% 보너스

  # 🎯 서비스별 포인트 소모
  service_costs:
    saju_basic: 100
    saju_detailed: 300
    saju_premium: 500
    tarot_single: 200
    tarot_three: 500
    tarot_celtic: 1000
    zodiac_basic: 150
    zodiac_compatibility: 300
    astrology_reading: 400
    fengshui_analysis: 600
    consultation_30min: 5000
    consultation_60min: 9000
    custom_report: 3000

  # 🎁 포인트 적립 (리워드)
  earning_activities:
    daily_login: 10
    first_review: 100
    referral_signup: 500
    community_post: 20
    community_comment: 5
    social_share: 30
    survey_complete: 50
```

## 🏗️ **시스템 아키텍처**

### **📊 구독 관리 서비스**
```python
# 💎 Subscription Management Service
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import asyncio

app = FastAPI(
    title="HEAL7 Subscription Service",
    version="1.0.0",
    description="구독 및 플랜 관리 서비스"
)

# 📋 구독 플랜 모델
class SubscriptionPlan(BaseModel):
    id: str  # "free", "basic", "premium", "master"
    name: str
    description: str
    price: Decimal
    currency: str = "KRW"
    duration: str  # "monthly", "annually", "lifetime"
    trial_days: int = 7
    features: List[str]
    limits: Dict[str, Any]
    is_active: bool = True
    sort_order: int = 0

# 👤 사용자 구독 모델
class UserSubscription(BaseModel):
    id: int
    user_id: int
    plan_id: str
    status: str  # "active", "cancelled", "expired", "trial", "suspended"
    
    # ⏰ 구독 기간
    started_at: datetime
    expires_at: datetime
    trial_ends_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    
    # 💳 결제 정보
    payment_method: str
    auto_renew: bool = True
    next_billing_date: datetime
    
    # 📊 사용량 추적
    usage_limits: Dict[str, int]  # 플랜별 제한
    usage_current: Dict[str, int]  # 현재 사용량
    usage_reset_date: datetime
    
    # 💰 가격 정보 (구독 시점 고정)
    price: Decimal
    currency: str
    discount_applied: Optional[str]
    
    created_at: datetime
    updated_at: datetime

# 🚀 구독 생성
@app.post("/subscriptions", response_model=UserSubscription)
async def create_subscription(
    user_id: int,
    plan_id: str,
    payment_method: str,
    promo_code: Optional[str] = None,
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 플랜 정보 조회
    plan = await get_subscription_plan(plan_id)
    if not plan or not plan.is_active:
        raise HTTPException(status_code=404, detail="Invalid subscription plan")
    
    # 2️⃣ 기존 구독 확인
    existing_sub = await get_active_subscription(user_id)
    if existing_sub:
        raise HTTPException(status_code=400, detail="User already has active subscription")
    
    # 3️⃣ 프로모션 코드 적용
    final_price = plan.price
    discount_info = None
    if promo_code:
        discount_info = await apply_promo_code(promo_code, plan.price)
        final_price = discount_info.discounted_price
    
    # 4️⃣ 트라이얼 기간 설정
    now = datetime.utcnow()
    trial_ends_at = now + timedelta(days=plan.trial_days) if plan.trial_days > 0 else None
    
    # 5️⃣ 구독 생성
    subscription = UserSubscription(
        user_id=user_id,
        plan_id=plan_id,
        status="trial" if trial_ends_at else "active",
        started_at=now,
        expires_at=now + timedelta(days=30),  # 월간 기준
        trial_ends_at=trial_ends_at,
        payment_method=payment_method,
        next_billing_date=trial_ends_at or now + timedelta(days=30),
        usage_limits=plan.limits.copy(),
        usage_current={key: 0 for key in plan.limits.keys()},
        usage_reset_date=now + timedelta(days=30),
        price=final_price,
        currency=plan.currency,
        discount_applied=promo_code
    )
    
    # 6️⃣ 결제 설정 (트라이얼이 아닌 경우)
    if not trial_ends_at and final_price > 0:
        payment_result = await process_initial_payment(
            user_id, final_price, payment_method
        )
        if payment_result.status != "completed":
            raise HTTPException(status_code=400, detail="Payment failed")
    
    # 7️⃣ 데이터베이스 저장
    db_subscription = await save_subscription(subscription, db)
    
    # 8️⃣ 사용자 권한 업데이트
    await update_user_permissions(user_id, plan.features)
    
    # 9️⃣ 환영 이메일 발송 (백그라운드)
    asyncio.create_task(
        send_subscription_welcome_email(user_id, plan.name, trial_ends_at)
    )
    
    return db_subscription

# 🔄 구독 변경
@app.put("/subscriptions/{subscription_id}/change-plan")
async def change_subscription_plan(
    subscription_id: int,
    new_plan_id: str,
    proration_policy: str = "immediate",  # "immediate", "next_cycle"
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 구독 플랜 변경 로직 (프로레이션 처리 포함)
    pass

# ❌ 구독 취소
@app.post("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: int,
    cancel_at_period_end: bool = True,
    cancellation_reason: Optional[str] = None,
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 구독 정보 조회
    subscription = await get_subscription(subscription_id, current_user["user_id"])
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # 2️⃣ 취소 처리
    if cancel_at_period_end:
        # 현재 구독 기간 만료 시 취소
        subscription.auto_renew = False
        subscription.cancelled_at = datetime.utcnow()
        subscription.status = "cancelled"
    else:
        # 즉시 취소 (환불 처리)
        subscription.status = "cancelled"
        subscription.expires_at = datetime.utcnow()
        subscription.cancelled_at = datetime.utcnow()
        
        # 프로레이션 환불 계산
        refund_amount = await calculate_prorated_refund(subscription)
        if refund_amount > 0:
            await process_refund(subscription.user_id, refund_amount)
    
    # 3️⃣ 데이터베이스 업데이트
    await update_subscription(subscription, db)
    
    # 4️⃣ 사용자 권한 업데이트 (즉시 취소인 경우)
    if not cancel_at_period_end:
        await update_user_permissions(subscription.user_id, ["free"])
    
    # 5️⃣ 취소 알림 이메일
    asyncio.create_task(
        send_subscription_cancellation_email(
            subscription.user_id, 
            subscription.plan_id,
            cancel_at_period_end
        )
    )
    
    return {"message": "Subscription cancelled successfully"}

# 📊 사용량 추적
@app.post("/subscriptions/{subscription_id}/usage")
async def track_usage(
    subscription_id: int,
    service_type: str,  # "saju_calculations", "tarot_readings", etc.
    amount: int = 1,
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 구독 정보 조회
    subscription = await get_subscription(subscription_id, current_user["user_id"])
    
    # 2️⃣ 사용량 제한 확인
    current_usage = subscription.usage_current.get(service_type, 0)
    usage_limit = subscription.usage_limits.get(service_type, -1)
    
    if usage_limit > 0 and current_usage + amount > usage_limit:
        raise HTTPException(
            status_code=403, 
            detail=f"Usage limit exceeded for {service_type}"
        )
    
    # 3️⃣ 사용량 업데이트
    subscription.usage_current[service_type] = current_usage + amount
    await update_subscription(subscription, db)
    
    # 4️⃣ 사용량 알림 (80% 도달 시)
    if usage_limit > 0:
        usage_percentage = (current_usage + amount) / usage_limit
        if usage_percentage >= 0.8:
            asyncio.create_task(
                send_usage_warning_notification(
                    subscription.user_id, service_type, usage_percentage
                )
            )
    
    return {
        "service_type": service_type,
        "current_usage": current_usage + amount,
        "usage_limit": usage_limit,
        "remaining": max(0, usage_limit - current_usage - amount) if usage_limit > 0 else "unlimited"
    }

# 🔄 사용량 리셋 (월간 갱신)
@app.post("/subscriptions/reset-usage")
async def reset_monthly_usage():
    # 스케줄러에서 호출되는 월간 사용량 리셋
    pass
```

### **🪙 포인트 관리 서비스**
```python
# 💰 Point Management Service
app = FastAPI(
    title="HEAL7 Point Service",
    version="1.0.0",
    description="포인트 충전 및 관리 서비스"
)

# 💳 포인트 거래 모델
class PointTransaction(BaseModel):
    id: int
    user_id: int
    transaction_type: str  # "purchase", "usage", "reward", "refund", "adjustment"
    amount: int  # 양수: 적립, 음수: 차감
    balance_before: int
    balance_after: int
    
    # 📝 거래 상세
    description: str
    reference_type: Optional[str] = None  # "order", "service", "promotion"
    reference_id: Optional[str] = None
    
    # 📊 메타데이터
    metadata: Dict[str, Any] = {}
    
    # ⏰ 시간 정보
    created_at: datetime
    expires_at: Optional[datetime] = None  # 포인트 만료일

# 👤 사용자 포인트 잔액
class UserPoints(BaseModel):
    user_id: int
    total_balance: int
    usable_balance: int  # 만료되지 않은 포인트
    pending_balance: int  # 대기 중인 포인트
    lifetime_earned: int  # 평생 적립 포인트
    lifetime_spent: int   # 평생 사용 포인트
    
    # 📊 만료 예정 포인트
    expiring_soon: List[Dict[str, Any]]  # [{"amount": 1000, "expires_at": "2025-09-01"}]
    
    updated_at: datetime

# 💳 포인트 충전
@app.post("/points/purchase")
async def purchase_points(
    package_id: str,  # "starter", "regular", "premium", "mega"
    payment_method: str,
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 패키지 정보 조회
    package = get_point_package(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Invalid package")
    
    # 2️⃣ 결제 처리
    payment_result = await process_payment(
        user_id=current_user["user_id"],
        amount=package["price"],
        currency="KRW",
        payment_method=payment_method,
        description=f"포인트 충전 - {package['points']}P"
    )
    
    if payment_result.status != "completed":
        raise HTTPException(status_code=400, detail="Payment failed")
    
    # 3️⃣ 포인트 적립
    total_points = package["points"] + package.get("bonus", 0)
    await add_points(
        user_id=current_user["user_id"],
        amount=total_points,
        transaction_type="purchase",
        description=f"포인트 충전 ({package_id})",
        reference_type="payment",
        reference_id=payment_result.payment_id,
        expires_at=datetime.utcnow() + timedelta(days=365)  # 1년 만료
    )
    
    # 4️⃣ 거래 기록
    await record_point_transaction(
        user_id=current_user["user_id"],
        amount=total_points,
        transaction_type="purchase",
        reference_id=payment_result.payment_id
    )
    
    return {
        "package": package_id,
        "points_purchased": package["points"],
        "bonus_points": package.get("bonus", 0),
        "total_points": total_points,
        "payment_id": payment_result.payment_id
    }

# 💸 포인트 사용
@app.post("/points/spend")
async def spend_points(
    amount: int,
    service_type: str,
    service_id: str,
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 잔액 확인
    user_points = await get_user_points(current_user["user_id"])
    if user_points.usable_balance < amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient points. Available: {user_points.usable_balance}, Required: {amount}"
        )
    
    # 2️⃣ 포인트 차감 (FIFO - 먼저 만료되는 것부터)
    await deduct_points(
        user_id=current_user["user_id"],
        amount=amount,
        transaction_type="usage",
        description=f"{service_type} 서비스 이용",
        reference_type="service",
        reference_id=service_id
    )
    
    # 3️⃣ 서비스 접근 권한 부여
    access_token = await grant_service_access(
        user_id=current_user["user_id"],
        service_type=service_type,
        service_id=service_id
    )
    
    return {
        "points_spent": amount,
        "remaining_balance": user_points.usable_balance - amount,
        "service_access_token": access_token
    }

# 🎁 포인트 적립 (리워드)
@app.post("/points/reward")
async def reward_points(
    user_id: int,
    amount: int,
    activity_type: str,  # "daily_login", "referral", "review", etc.
    current_user = Depends(require_scope(Scopes.USER_ADMIN)),
    db: Session = Depends(get_db)
):
    # 1️⃣ 중복 적립 방지 확인
    today = datetime.utcnow().date()
    if activity_type == "daily_login":
        existing_reward = await check_daily_reward(user_id, today)
        if existing_reward:
            raise HTTPException(status_code=400, detail="Daily reward already claimed")
    
    # 2️⃣ 포인트 적립
    await add_points(
        user_id=user_id,
        amount=amount,
        transaction_type="reward",
        description=f"{activity_type} 리워드",
        expires_at=datetime.utcnow() + timedelta(days=365)
    )
    
    # 3️⃣ 알림 발송
    asyncio.create_task(
        send_point_reward_notification(user_id, amount, activity_type)
    )
    
    return {"message": f"Rewarded {amount} points for {activity_type}"}

# 📊 포인트 내역 조회
@app.get("/points/history")
async def get_point_history(
    transaction_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 50,
    offset: int = 0,
    current_user = Depends(require_scope(Scopes.USER_PROFILE)),
    db: Session = Depends(get_db)
):
    # 포인트 거래 내역 조회
    pass

# ⏰ 포인트 만료 처리
@app.post("/points/process-expiration")
async def process_point_expiration():
    # 스케줄러에서 호출되는 포인트 만료 처리
    expired_points = await get_expired_points()
    
    for expired in expired_points:
        await deduct_points(
            user_id=expired.user_id,
            amount=expired.amount,
            transaction_type="expiration",
            description="포인트 만료",
            reference_id=str(expired.id)
        )
        
        # 만료 알림
        asyncio.create_task(
            send_point_expiration_notification(expired.user_id, expired.amount)
        )
```

### **🏦 결제 게이트웨이 통합**
```python
# 💳 Payment Gateway Integration
from abc import ABC, abstractmethod

class PaymentProvider(ABC):
    @abstractmethod
    async def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        pass
    
    @abstractmethod
    async def verify_payment(self, transaction_id: str) -> PaymentVerification:
        pass
    
    @abstractmethod
    async def cancel_payment(self, transaction_id: str, reason: str) -> PaymentCancellation:
        pass

# 💰 카카오페이 연동
class KakaoPayProvider(PaymentProvider):
    def __init__(self, cid: str, secret_key: str):
        self.cid = cid
        self.secret_key = secret_key
        self.base_url = "https://kapi.kakao.com"
    
    async def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        # 1️⃣ 결제 준비
        prepare_response = await self._prepare_payment(payment_request)
        
        # 2️⃣ 사용자 승인 대기
        approval_url = prepare_response["next_redirect_pc_url"]
        
        return PaymentResult(
            payment_id=prepare_response["tid"],
            status="pending_approval",
            approval_url=approval_url,
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )
    
    async def _prepare_payment(self, payment_request: PaymentRequest):
        headers = {
            "Authorization": f"KakaoAK {self.secret_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "cid": self.cid,
            "partner_order_id": payment_request.order_id,
            "partner_user_id": str(payment_request.user_id),
            "item_name": payment_request.description,
            "quantity": 1,
            "total_amount": int(payment_request.amount),
            "tax_free_amount": 0,
            "approval_url": payment_request.return_url,
            "cancel_url": payment_request.cancel_url,
            "fail_url": payment_request.cancel_url
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/payment/ready",
                headers=headers,
                data=data
            )
            return response.json()

# 💸 토스페이먼츠 연동
class TossPayProvider(PaymentProvider):
    def __init__(self, client_key: str, secret_key: str):
        self.client_key = client_key
        self.secret_key = secret_key
        self.base_url = "https://api.tosspayments.com"
    
    async def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        # 토스페이먼츠 결제 처리 로직
        pass

# 💳 결제 관리자
class PaymentManager:
    def __init__(self):
        self.providers = {
            "kakao_pay": KakaoPayProvider(
                cid=settings.KAKAO_CID,
                secret_key=settings.KAKAO_SECRET_KEY
            ),
            "toss_pay": TossPayProvider(
                client_key=settings.TOSS_CLIENT_KEY,
                secret_key=settings.TOSS_SECRET_KEY
            ),
            "naver_pay": NaverPayProvider(
                client_id=settings.NAVER_CLIENT_ID,
                client_secret=settings.NAVER_CLIENT_SECRET
            )
        }
    
    async def process_payment(
        self, 
        payment_method: str, 
        payment_request: PaymentRequest
    ) -> PaymentResult:
        provider = self.providers.get(payment_method)
        if not provider:
            raise ValueError(f"Unsupported payment method: {payment_method}")
        
        try:
            # 1️⃣ 결제 처리
            result = await provider.process_payment(payment_request)
            
            # 2️⃣ 결제 로그 기록
            await self._log_payment_attempt(payment_request, result)
            
            return result
            
        except Exception as e:
            # ❌ 결제 실패 로그
            await self._log_payment_error(payment_request, str(e))
            raise PaymentException(f"Payment processing failed: {str(e)}")
    
    async def _log_payment_attempt(
        self, 
        request: PaymentRequest, 
        result: PaymentResult
    ):
        log_data = {
            "payment_id": result.payment_id,
            "user_id": request.user_id,
            "amount": request.amount,
            "payment_method": request.payment_method,
            "status": result.status,
            "timestamp": datetime.utcnow()
        }
        
        # 결제 로그를 데이터베이스나 로그 시스템에 기록
        await save_payment_log(log_data)
```

### **📊 구독 생명주기 관리**
```python
# 🔄 Subscription Lifecycle Manager
class SubscriptionLifecycleManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.setup_scheduled_tasks()
    
    def setup_scheduled_tasks(self):
        # 🕐 매일 자정에 실행되는 작업들
        self.scheduler.add_job(
            self.process_subscription_renewals,
            'cron',
            hour=0,
            minute=0,
            id='subscription_renewals'
        )
        
        self.scheduler.add_job(
            self.process_trial_expirations,
            'cron',
            hour=0,
            minute=30,
            id='trial_expirations'
        )
        
        self.scheduler.add_job(
            self.send_renewal_reminders,
            'cron',
            hour=9,
            minute=0,
            id='renewal_reminders'
        )
        
        # 🔄 매월 1일에 사용량 리셋
        self.scheduler.add_job(
            self.reset_usage_limits,
            'cron',
            day=1,
            hour=0,
            minute=0,
            id='usage_reset'
        )
    
    async def process_subscription_renewals(self):
        """구독 갱신 처리"""
        # 1️⃣ 오늘 갱신될 구독들 조회
        today = datetime.utcnow().date()
        renewals = await get_subscriptions_for_renewal(today)
        
        for subscription in renewals:
            try:
                # 2️⃣ 자동 갱신 설정 확인
                if not subscription.auto_renew:
                    await self._expire_subscription(subscription)
                    continue
                
                # 3️⃣ 결제 처리
                payment_result = await self._process_renewal_payment(subscription)
                
                if payment_result.status == "completed":
                    # ✅ 구독 갱신 성공
                    await self._renew_subscription(subscription)
                    await self._send_renewal_success_notification(subscription)
                else:
                    # ❌ 결제 실패 - 재시도 스케줄링
                    await self._schedule_payment_retry(subscription)
                    await self._send_payment_failed_notification(subscription)
                    
            except Exception as e:
                logger.error(f"Subscription renewal failed for {subscription.id}: {str(e)}")
                await self._handle_renewal_error(subscription, str(e))
    
    async def process_trial_expirations(self):
        """트라이얼 만료 처리"""
        today = datetime.utcnow().date()
        expiring_trials = await get_expiring_trials(today)
        
        for subscription in expiring_trials:
            if subscription.auto_renew:
                # 자동 결제로 전환
                await self._convert_trial_to_paid(subscription)
            else:
                # 무료 플랜으로 다운그레이드
                await self._downgrade_to_free(subscription)
    
    async def send_renewal_reminders(self):
        """갱신 알림 발송"""
        # 7일, 3일, 1일 전 알림
        for days_before in [7, 3, 1]:
            reminder_date = datetime.utcnow().date() + timedelta(days=days_before)
            subscriptions = await get_subscriptions_for_renewal(reminder_date)
            
            for subscription in subscriptions:
                await self._send_renewal_reminder(subscription, days_before)
    
    async def reset_usage_limits(self):
        """월간 사용량 리셋"""
        await reset_all_subscription_usage()
        
        # 사용량 리셋 알림
        active_subscriptions = await get_active_subscriptions()
        for subscription in active_subscriptions:
            await self._send_usage_reset_notification(subscription)
    
    async def _process_renewal_payment(self, subscription: UserSubscription):
        """갱신 결제 처리"""
        payment_request = PaymentRequest(
            user_id=subscription.user_id,
            amount=subscription.price,
            currency=subscription.currency,
            payment_method=subscription.payment_method,
            description=f"구독 갱신 - {subscription.plan_id}",
            metadata={"subscription_id": subscription.id}
        )
        
        payment_manager = PaymentManager()
        return await payment_manager.process_payment(
            subscription.payment_method, 
            payment_request
        )
    
    async def _renew_subscription(self, subscription: UserSubscription):
        """구독 갱신"""
        # 만료일 연장
        if subscription.plan_id.endswith("_annual"):
            extension = timedelta(days=365)
        else:
            extension = timedelta(days=30)
        
        subscription.expires_at += extension
        subscription.next_billing_date += extension
        subscription.usage_reset_date += extension
        
        # 사용량 리셋
        subscription.usage_current = {
            key: 0 for key in subscription.usage_limits.keys()
        }
        
        await update_subscription(subscription)
```

### **📈 분석 및 리포팅**
```python
# 📊 Subscription Analytics Service
class SubscriptionAnalytics:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
    
    async def get_subscription_metrics(
        self, 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """구독 지표 조회"""
        return {
            # 💰 수익 지표
            "revenue": {
                "total": await self._get_total_revenue(start_date, end_date),
                "by_plan": await self._get_revenue_by_plan(start_date, end_date),
                "mrr": await self._get_monthly_recurring_revenue(),
                "arr": await self._get_annual_recurring_revenue()
            },
            
            # 👥 구독자 지표
            "subscribers": {
                "total_active": await self._get_active_subscribers(),
                "new_subscribers": await self._get_new_subscribers(start_date, end_date),
                "churned_subscribers": await self._get_churned_subscribers(start_date, end_date),
                "churn_rate": await self._calculate_churn_rate(start_date, end_date),
                "retention_rate": await self._calculate_retention_rate(start_date, end_date)
            },
            
            # 📈 전환 지표
            "conversions": {
                "trial_to_paid": await self._get_trial_conversion_rate(start_date, end_date),
                "plan_upgrades": await self._get_plan_upgrades(start_date, end_date),
                "plan_downgrades": await self._get_plan_downgrades(start_date, end_date)
            },
            
            # 💳 결제 지표
            "payments": {
                "success_rate": await self._get_payment_success_rate(start_date, end_date),
                "failed_payments": await self._get_failed_payments(start_date, end_date),
                "refunds": await self._get_refunds(start_date, end_date)
            }
        }
    
    async def get_user_lifetime_value(self, user_id: int) -> Dict[str, Any]:
        """사용자 생애 가치 계산"""
        user_data = await self._get_user_subscription_history(user_id)
        
        return {
            "total_revenue": sum(sub.price for sub in user_data.subscriptions),
            "subscription_months": self._calculate_subscription_months(user_data),
            "average_monthly_value": user_data.total_revenue / max(1, user_data.subscription_months),
            "predicted_ltv": await self._predict_lifetime_value(user_data),
            "churn_probability": await self._predict_churn_probability(user_data)
        }
    
    async def generate_subscription_report(
        self, 
        report_type: str,
        start_date: date,
        end_date: date
    ) -> str:
        """구독 리포트 생성"""
        if report_type == "revenue":
            return await self._generate_revenue_report(start_date, end_date)
        elif report_type == "churn":
            return await self._generate_churn_report(start_date, end_date)
        elif report_type == "cohort":
            return await self._generate_cohort_report(start_date, end_date)
        else:
            raise ValueError(f"Unknown report type: {report_type}")
```

---

## 🔒 **보안 및 규정 준수**

### **💳 PCI DSS 준수**
```yaml
# 🛡️ Payment Security Standards
pci_compliance:
  # 🔐 결제 정보 보안
  card_data_handling:
    storage: "never_store_card_data"
    transmission: "tls_1.2_minimum"
    tokenization: "pg_provider_tokens_only"
    
  # 🔒 접근 제어
  access_control:
    principle: "least_privilege"
    mfa_required: true
    session_timeout: 15  # minutes
    
  # 📊 모니터링
  monitoring:
    payment_anomalies: true
    failed_login_attempts: true
    suspicious_transactions: true
    
  # 🔍 감사
  audit_logging:
    payment_attempts: true
    admin_actions: true
    data_access: true
    retention_period: 7  # years
```

### **📋 개인정보보호**
```python
# 🔐 Privacy & Data Protection
class PrivacyManager:
    async def anonymize_payment_data(self, user_id: int):
        """결제 데이터 익명화"""
        # 사용자 탈퇴 시 결제 정보 익명화
        await self._anonymize_user_payments(user_id)
        await self._anonymize_subscription_history(user_id)
        
    async def export_user_data(self, user_id: int) -> Dict[str, Any]:
        """사용자 데이터 내보내기 (GDPR 준수)"""
        return {
            "subscriptions": await self._get_user_subscriptions(user_id),
            "payments": await self._get_user_payments(user_id),
            "points": await self._get_user_points_history(user_id),
            "usage": await self._get_user_usage_data(user_id)
        }
    
    async def delete_user_data(self, user_id: int):
        """사용자 데이터 삭제 (잊혀질 권리)"""
        # 법적 보관 기간 확인 후 삭제
        await self._delete_expired_user_data(user_id)
```

---

## 📝 **구현 체크리스트**

### **1단계: 기본 구독 시스템** ✅
- [x] 구독 플랜 정의
- [x] 사용자 구독 모델 설계
- [ ] 구독 생성/변경/취소 API
- [ ] 사용량 추적 시스템
- [ ] 기본 결제 연동

### **2단계: 결제 시스템** 🔄
- [ ] 다중 PG사 연동
- [ ] 결제 실패 처리
- [ ] 환불 시스템
- [ ] 정기 결제 관리

### **3단계: 포인트 시스템** 📋
- [ ] 포인트 충전/사용
- [ ] 리워드 시스템
- [ ] 포인트 만료 처리
- [ ] 포인트 내역 관리

### **4단계: 고급 기능** 📋
- [ ] 구독 분석 대시보드
- [ ] 고객 생애 가치 분석
- [ ] 이탈 예측 모델
- [ ] 개인화된 플랜 추천

---

*📅 설계 완료일: 2025-08-18*  
*💳 설계자: HEAL7 Payment & Subscription Team*  
*📝 문서 위치: `/home/ubuntu/CORE/feature-specs/api-specifications/`*  
*🔄 다음 버전: v1.1 (2025-08-25 예정)*