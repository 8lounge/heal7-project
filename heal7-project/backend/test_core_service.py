#!/usr/bin/env python3
"""
핵심 서비스 테스트 스크립트
"""
import sys
import os
import asyncio

# 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.saju_service import SajuService, BirthInfo, Gender

async def test_core_service():
    """핵심 서비스 테스트"""
    print("🔍 사주 서비스 핵심 기능 테스트 시작...")
    
    service = SajuService()
    
    try:
        # 1. 서비스 초기화 테스트
        print("1️⃣ 서비스 초기화 테스트...")
        await service.initialize()
        print("✅ 사주 서비스 초기화 성공")
        
        # 2. 헬스체크 테스트
        print("2️⃣ 헬스체크 테스트...")
        health = await service.health_check()
        print(f"✅ 헬스체크 결과: {health}")
        
        # 3. 기본 계산 능력 확인
        print("3️⃣ 기본 사주 계산 능력 확인...")
        
        birth_info = BirthInfo(
            year=1990,
            month=5,
            day=15,
            hour=10,
            minute=30,
            gender=Gender.MALE,
            name="테스트",
            is_lunar=False
        )
        
        result = await service.calculate_saju(birth_info)
        print(f"✅ 기본 사주 계산 성공: {result.palcha}")
        
        # 4. 서비스 정리
        print("4️⃣ 서비스 정리...")
        await service.cleanup()
        print("✅ 서비스 정리 완료")
        
        print("\n🎉 모든 핵심 기능 테스트 성공!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_core_service())
    sys.exit(0 if success else 1)