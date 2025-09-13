#!/usr/bin/env python3
"""
HEAL7 Admin 초기화 스크립트
관리자 계정 생성 및 초기 데이터 설정

실행: python init_admin.py
"""

import asyncio
import sys
import os
from datetime import datetime

# 프로젝트 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.auth_service import auth_service
from core.database_service import db_service

async def create_default_admin():
    """기본 관리자 계정 생성"""
    try:
        # 데이터베이스 연결 풀 초기화
        await db_service.initialize_pools()

        # 기존 관리자 확인
        existing_admin = await db_service.execute_single_query(
            "SELECT id FROM admin_users WHERE username = $1",
            ['admin'],
            db_type='saju'
        )

        if existing_admin:
            print("✅ 기본 관리자 계정이 이미 존재합니다.")

            # 비밀번호 해시 업데이트 (평문인 경우)
            admin_data = await db_service.execute_single_query(
                "SELECT password_hash FROM admin_users WHERE username = $1",
                ['admin'],
                db_type='saju'
            )

            if admin_data['password_hash'] == 'admin123':
                print("🔒 비밀번호를 해시로 업데이트하는 중...")
                hashed_password = auth_service.hash_password('heal7admin2025!')

                await db_service.execute_query(
                    "UPDATE admin_users SET password_hash = $1 WHERE username = $2",
                    [hashed_password, 'admin'],
                    db_type='saju'
                )
                print("✅ 비밀번호가 안전하게 해시로 업데이트되었습니다.")
                print(f"🔑 새 비밀번호: heal7admin2025!")

            return

        # 새 관리자 계정 생성
        print("👤 새 관리자 계정을 생성합니다...")

        # 비밀번호 해시 생성
        default_password = 'heal7admin2025!'
        hashed_password = auth_service.hash_password(default_password)

        # 관리자 계정 생성
        admin_id = await db_service.execute_single_query(
            """INSERT INTO admin_users
               (username, email, password_hash, full_name, role, is_active, created_at, updated_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
               RETURNING id""",
            [
                'admin',
                'admin@heal7.com',
                hashed_password,
                'HEAL7 Administrator',
                'super_admin',
                True,
                datetime.now(),
                datetime.now()
            ],
            db_type='saju'
        )

        if admin_id:
            print("✅ 관리자 계정이 성공적으로 생성되었습니다!")
            print(f"📧 이메일: admin@heal7.com")
            print(f"👤 사용자명: admin")
            print(f"🔑 비밀번호: {default_password}")
            print("⚠️ 보안을 위해 첫 로그인 후 비밀번호를 변경해주세요.")
        else:
            print("❌ 관리자 계정 생성에 실패했습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        await db_service.close_pools()

async def check_database_health():
    """데이터베이스 상태 확인"""
    try:
        print("🔍 데이터베이스 상태를 확인합니다...")

        await db_service.initialize_pools()
        health_status = await db_service.health_check()

        print("📊 데이터베이스 상태:")
        for db_name, status in health_status.items():
            status_emoji = "✅" if status['status'] == 'healthy' else "❌"
            print(f"  {status_emoji} {db_name}: {status['status']}")
            if 'response_time' in status:
                print(f"    응답 시간: {status['response_time']:.3f}초")
            if 'error' in status:
                print(f"    오류: {status['error']}")

        await db_service.close_pools()

    except Exception as e:
        print(f"❌ 데이터베이스 상태 확인 실패: {e}")

async def main():
    """메인 함수"""
    print("🚀 HEAL7 Admin 초기화 시작")
    print("=" * 50)

    # 데이터베이스 상태 확인
    await check_database_health()

    print("\n" + "=" * 50)

    # 관리자 계정 생성/업데이트
    await create_default_admin()

    print("\n" + "=" * 50)
    print("🎉 초기화 완료!")

if __name__ == "__main__":
    # 환경변수 확인
    required_env_vars = ['JWT_SECRET_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        print("⚠️ 다음 환경변수가 설정되지 않았습니다:")
        for var in missing_vars:
            print(f"  - {var}")
        print("📝 .env 파일을 확인하거나 환경변수를 설정해주세요.")
        print("💡 JWT_SECRET_KEY가 없으면 임시 키가 생성됩니다.")
        print()

    asyncio.run(main())