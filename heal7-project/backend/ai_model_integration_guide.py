#!/usr/bin/env python3
"""
AI 모델 통합 사용 가이드 및 예시
각 서비스(사주, 마케팅, 설문)에서 AI 모델 매니저를 사용하는 방법
"""

from ai_model_manager import ai_manager
import asyncio

# ==================== 사주 서비스 통합 예시 ====================

async def saju_ai_analysis(birth_data: dict):
    """사주 분석에 AI 활용"""
    
    # 사주 서비스는 정확성이 중요하므로 기본 폴백 순서: gemini → claude → gpt-4
    prompt = f"""
    다음 사주 정보를 분석해주세요:
    생년월일시: {birth_data['birth_datetime']}
    음양오행: {birth_data['elements']}
    십성: {birth_data['ten_gods']}
    
    1. 전체적인 사주 해석
    2. 성격 및 기질 분석
    3. 인생 운세 흐름
    4. 조언 및 개운법
    
    전통 사주명리학에 근거하여 정확하고 상세하게 분석해주세요.
    """
    
    try:
        # AI 응답 받기 (자동 폴백 적용)
        response, model_used, metadata = await ai_manager.get_ai_response(
            prompt=prompt,
            service="saju",  # 사주 서비스 폴백 순서 사용
            temperature=0.7,  # 적당한 창의성
            max_tokens=3000   # 긴 응답 허용
        )
        
        return {
            "success": True,
            "analysis": response,
            "ai_model": model_used,
            "response_time": metadata["response_time"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback_message": "AI 분석을 일시적으로 사용할 수 없습니다."
        }

# ==================== 마케팅 서비스 통합 예시 ====================

async def marketing_campaign_generator(campaign_brief: dict):
    """마케팅 캠페인 AI 생성"""
    
    # 마케팅은 창의성과 비용 효율이 중요: gemini → gpt-3.5 → claude
    prompt = f"""
    다음 요구사항에 맞는 마케팅 캠페인을 기획해주세요:
    
    타겟 고객: {campaign_brief['target_audience']}
    제품/서비스: {campaign_brief['product']}
    예산 규모: {campaign_brief['budget']}
    캠페인 목표: {campaign_brief['goal']}
    
    다음을 포함해주세요:
    1. 캠페인 컨셉 및 슬로건
    2. 주요 메시지
    3. 채널별 전략 (SNS, 이메일, 광고 등)
    4. 예상 ROI 및 KPI
    5. 실행 타임라인
    """
    
    try:
        response, model_used, metadata = await ai_manager.get_ai_response(
            prompt=prompt,
            service="marketing",
            temperature=0.8,  # 높은 창의성
            max_tokens=2500
        )
        
        # 비용 효율성 체크
        if model_used != "gemini" and metadata.get("fallback_index", 0) > 0:
            print(f"주의: 무료 모델 대신 {model_used} 사용됨. 비용 발생 가능.")
        
        return {
            "success": True,
            "campaign_plan": response,
            "ai_model": model_used,
            "estimated_cost": metadata.get("cost", 0)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ==================== 설문 서비스 통합 예시 ====================

async def survey_analysis_ai(survey_responses: list):
    """설문 응답 AI 분석"""
    
    # 설문 분석은 통찰력이 중요: gemini → claude → gpt-3.5
    prompt = f"""
    다음 설문 응답 데이터를 분석해주세요:
    
    응답 수: {len(survey_responses)}
    설문 주제: 정신 건강 및 스트레스 수준
    
    주요 응답 데이터:
    {survey_responses[:5]}  # 샘플 데이터
    
    다음을 분석해주세요:
    1. 전반적인 응답 경향
    2. 주요 인사이트 3가지
    3. 위험군 식별 및 특성
    4. 개선 제안사항
    5. 후속 조치 권고
    """
    
    try:
        response, model_used, metadata = await ai_manager.get_ai_response(
            prompt=prompt,
            service="survey",
            temperature=0.5,  # 낮은 창의성, 높은 정확성
            max_tokens=2000
        )
        
        return {
            "success": True,
            "analysis": response,
            "ai_model": model_used,
            "confidence_level": "high" if model_used in ["gemini", "claude"] else "medium"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ==================== 리서치 작업 예시 ====================

async def research_latest_trends(topic: str):
    """최신 트렌드 리서치 (Perplexity 우선)"""
    
    prompt = f"""
    {topic}에 대한 최신 트렌드와 동향을 조사해주세요.
    
    다음을 포함해주세요:
    1. 2024-2025년 최신 동향
    2. 주요 통계 및 데이터
    3. 업계 전문가 의견
    4. 미래 전망
    5. 신뢰할 수 있는 출처 목록
    """
    
    try:
        # 리서치는 perplexity 우선 사용
        response, model_used, metadata = await ai_manager.get_ai_response(
            prompt=prompt,
            service="research",  # perplexity → gemini → gpt-4
            preferred_model="perplexity",  # 명시적으로 perplexity 우선
            temperature=0.3,  # 정확성 중시
            max_tokens=3000
        )
        
        return {
            "success": True,
            "research": response,
            "ai_model": model_used,
            "has_realtime_data": model_used == "perplexity"
        }
        
    except Exception as e:
        # Perplexity 실패 시 자동으로 다른 모델로 폴백됨
        return {
            "success": False,
            "error": str(e)
        }

# ==================== 커스텀 폴백 순서 예시 ====================

async def custom_ai_task():
    """특별한 요구사항이 있는 작업"""
    
    # 특정 작업을 위한 커스텀 폴백 순서 설정
    ai_manager.update_service_fallback_order(
        "custom_task",
        ["claude", "gpt-4", "gemini"]  # 품질 최우선
    )
    
    prompt = "복잡하고 정교한 분석이 필요한 작업..."
    
    response, model_used, metadata = await ai_manager.get_ai_response(
        prompt=prompt,
        service="custom_task",
        temperature=0.3
    )
    
    return response

# ==================== 시스템 모니터링 예시 ====================

async def monitor_ai_system():
    """AI 시스템 상태 모니터링"""
    
    # 헬스체크
    health = await ai_manager.perform_health_check()
    
    print("=== AI 시스템 상태 ===")
    print(f"시스템 리소스:")
    print(f"- CPU: {health['system_resources']['cpu_percent']}%")
    print(f"- 메모리: {health['system_resources']['memory_percent']}%")
    
    print(f"\n모델 상태:")
    for model_name, status in health['models'].items():
        print(f"- {model_name}: {status['status']} (성공률: {status['success_rate']:.1f}%)")
    
    # 일일 리포트
    daily_report = await ai_manager.generate_daily_report()
    
    print(f"\n=== 일일 사용 통계 ===")
    print(f"총 요청: {daily_report['summary']['total_requests']}")
    print(f"총 토큰: {daily_report['summary']['total_tokens']}")
    print(f"총 비용: ${daily_report['summary']['total_cost']:.2f}")
    
    # 추천사항 확인
    if daily_report['recommendations']:
        print(f"\n추천사항:")
        for rec in daily_report['recommendations']:
            print(f"- {rec}")

# ==================== 비상 상황 대응 예시 ====================

async def handle_emergency():
    """시스템 과부하 시 대응"""
    
    # 현재 시스템 상태 확인
    health = await ai_manager.perform_health_check()
    cpu_usage = health['system_resources']['cpu_percent']
    
    if cpu_usage > 80:
        print("경고: CPU 사용률이 높습니다!")
        
        # 비필수 모델 비활성화
        await ai_manager.toggle_model("gpt-4", False)  # 비싼 모델 비활성화
        await ai_manager.toggle_model("perplexity", False)  # 리서치 전용 비활성화
        
        print("비필수 AI 모델을 비활성화했습니다.")
        
        # 무료 모델만 사용하도록 폴백 순서 조정
        for service in ["saju", "marketing", "survey"]:
            ai_manager.update_service_fallback_order(
                service,
                ["gemini", "llama"]  # 무료 모델만
            )
        
        print("무료 모델만 사용하도록 전환했습니다.")

# ==================== 실행 예시 ====================

async def main():
    """통합 테스트"""
    
    # AI 모니터링 시작
    await ai_manager.start_monitoring()
    
    print("=== HEAL7 AI 모델 통합 테스트 ===\n")
    
    # 1. 사주 분석 테스트
    print("1. 사주 AI 분석 테스트")
    saju_result = await saju_ai_analysis({
        "birth_datetime": "1990-05-15 14:30",
        "elements": "목화토금수",
        "ten_gods": "정관 정재 식신"
    })
    print(f"- 모델: {saju_result.get('ai_model', 'N/A')}")
    print(f"- 응답시간: {saju_result.get('response_time', 0):.2f}초\n")
    
    # 2. 마케팅 캠페인 생성 테스트
    print("2. 마케팅 캠페인 생성 테스트")
    marketing_result = await marketing_campaign_generator({
        "target_audience": "20-30대 직장인",
        "product": "정신건강 관리 앱",
        "budget": "월 500만원",
        "goal": "신규 가입자 1000명"
    })
    print(f"- 모델: {marketing_result.get('ai_model', 'N/A')}")
    print(f"- 예상 비용: ${marketing_result.get('estimated_cost', 0):.4f}\n")
    
    # 3. 시스템 상태 모니터링
    print("3. 시스템 상태 확인")
    await monitor_ai_system()
    
    # 모니터링 중지
    await ai_manager.stop_monitoring()

if __name__ == "__main__":
    # 실행
    asyncio.run(main())