"""
HEAL7 Admin Authentication Service
관리자 인증 보안 강화 모듈

기능:
- 비밀번호 해시 처리 (bcrypt)
- JWT 토큰 생성/검증
- 권한 관리
- 세션 관리
"""

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import secrets
import os
from loguru import logger
from fastapi import HTTPException, status

class AuthService:
    def __init__(self):
        # JWT 설정
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', self._generate_secret_key())
        self.jwt_algorithm = 'HS256'
        self.jwt_expiry_hours = int(os.getenv('JWT_EXPIRY_HOURS', '24'))

        # 세션 설정
        self.max_failed_attempts = int(os.getenv('MAX_FAILED_ATTEMPTS', '3'))
        self.lockout_duration_minutes = int(os.getenv('LOCKOUT_DURATION_MINUTES', '15'))

        logger.info("AuthService initialized with enhanced security")

    def _generate_secret_key(self) -> str:
        """JWT 비밀키 생성"""
        secret_key = secrets.token_urlsafe(32)
        logger.warning(f"Generated new JWT secret key. Please set JWT_SECRET_KEY in environment variables.")
        return secret_key

    def hash_password(self, password: str) -> str:
        """비밀번호 해시 생성"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    def generate_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """JWT 토큰 생성"""
        try:
            payload = {
                'user_id': str(user_data['id']),
                'username': user_data['username'],
                'role': user_data['role'],
                'email': user_data['email'],
                'exp': datetime.now(timezone.utc) + timedelta(hours=self.jwt_expiry_hours),
                'iat': datetime.now(timezone.utc),
                'iss': 'heal7-admin-system'
            }

            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            logger.info(f"JWT token generated for user: {user_data['username']}")
            return token

        except Exception as e:
            logger.error(f"JWT token generation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed"
            )

    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """JWT 토큰 검증"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])

            # 토큰 만료 검사
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        except Exception as e:
            logger.error(f"JWT verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed"
            )

    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """권한 확인"""
        role_permissions = {
            'super_admin': ['all'],
            'admin': ['user_management', 'content_management', 'system_settings'],
            'editor': ['content_management']
        }

        user_permissions = role_permissions.get(user_role, [])

        # super_admin은 모든 권한
        if 'all' in user_permissions:
            return True

        return required_permission in user_permissions

    def create_secure_session(self, user_id: str, ip_address: str, user_agent: str) -> Dict[str, Any]:
        """보안 세션 생성"""
        session_data = {
            'user_id': user_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'created_at': datetime.now(timezone.utc),
            'last_activity': datetime.now(timezone.utc),
            'is_active': True
        }

        return session_data

    def validate_login_attempt(self, username: str, failed_attempts: int, last_failed: Optional[datetime]) -> bool:
        """로그인 시도 검증 (무차별 대입 공격 방지)"""
        if failed_attempts >= self.max_failed_attempts:
            if last_failed:
                lockout_until = last_failed + timedelta(minutes=self.lockout_duration_minutes)
                if datetime.now(timezone.utc) < lockout_until:
                    remaining_minutes = (lockout_until - datetime.now(timezone.utc)).total_seconds() / 60
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Account locked. Try again in {remaining_minutes:.0f} minutes."
                    )

        return True

    def sanitize_input(self, input_str: str, max_length: int = 100) -> str:
        """입력값 정화 (SQL 인젝션 방지)"""
        if not input_str:
            return ""

        # 길이 제한
        sanitized = input_str[:max_length]

        # 위험한 문자 제거
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")

        return sanitized.strip()

    def log_security_event(self, event_type: str, user_id: Optional[str], ip_address: str, details: Dict[str, Any]):
        """보안 이벤트 로깅"""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'ip_address': ip_address,
            'details': details
        }

        logger.info(f"SECURITY_EVENT: {log_entry}")

# 전역 인스턴스
auth_service = AuthService()