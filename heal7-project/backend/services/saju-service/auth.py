"""
HEAL7 사주명리학 인증 시스템 API
로그인, 회원가입, JWT 토큰 관리
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import bcrypt
import uuid
import os
import logging
logger = logging.getLogger(__name__)

# JWT 설정
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "heal7-saju-secret-key-2025")
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

router = APIRouter(prefix="/api/auth", tags=["인증"])
security = HTTPBearer()

# Pydantic 모델들
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    birth_date: Optional[str] = None  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM:SS
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: Dict[str, Any]

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str]
    birth_date: Optional[str]
    is_active: bool
    created_at: str

# JWT 토큰 유틸리티 함수들
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """액세스 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """리프레시 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    """비밀번호 해시"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT 토큰 검증"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {"user_id": user_id, "username": payload.get("username")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 임시 인메모리 사용자 저장소 (실제론 PostgreSQL 연동)
fake_users_db = {
    "admin@heal7.com": {
        "id": "admin-uuid-123",
        "username": "admin",
        "email": "admin@heal7.com",
        "password_hash": hash_password("admin123"),
        "full_name": "HEAL7 관리자",
        "is_active": True,
        "is_admin": True,
        "created_at": datetime.utcnow().isoformat()
    }
}

@router.post("/register", response_model=TokenResponse, summary="회원가입")
async def register(user_data: UserRegister):
    """새 사용자 회원가입"""
    
    # 중복 이메일 체크
    if user_data.email in fake_users_db:
        raise HTTPException(
            status_code=400, 
            detail="이미 등록된 이메일입니다"
        )
    
    # 사용자 생성
    user_id = str(uuid.uuid4())
    hashed_pw = hash_password(user_data.password)
    
    new_user = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "password_hash": hashed_pw,
        "full_name": user_data.full_name,
        "birth_date": user_data.birth_date,
        "birth_time": user_data.birth_time,
        "gender": user_data.gender,
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow().isoformat()
    }
    
    fake_users_db[user_data.email] = new_user
    logger.info(f"새 사용자 등록: {user_data.email}")
    
    # 토큰 생성
    access_token = create_access_token(data={"sub": user_id, "username": user_data.username})
    refresh_token = create_refresh_token(data={"sub": user_id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info={
            "id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name
        }
    )

@router.post("/login", response_model=TokenResponse, summary="로그인")
async def login(user_credentials: UserLogin):
    """사용자 로그인"""
    
    user = fake_users_db.get(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="이메일 또는 비밀번호가 잘못되었습니다"
        )
    
    if not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="이메일 또는 비밀번호가 잘못되었습니다"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=401,
            detail="비활성화된 계정입니다"
        )
    
    # 토큰 생성
    access_token = create_access_token(data={"sub": user["id"], "username": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["id"]})
    
    logger.info(f"사용자 로그인: {user_credentials.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user.get("full_name")
        }
    )

@router.get("/profile", response_model=UserProfile, summary="내 프로필 조회")
async def get_my_profile(current_user: dict = Depends(verify_token)):
    """현재 로그인한 사용자의 프로필 정보 조회"""
    
    user_id = current_user["user_id"]
    user = None
    
    # 사용자 찾기
    for email, user_data in fake_users_db.items():
        if user_data["id"] == user_id:
            user = user_data
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    return UserProfile(
        id=user["id"],
        username=user["username"],
        email=user.get("email", ""),
        full_name=user.get("full_name"),
        birth_date=user.get("birth_date"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at", "")
    )

@router.post("/refresh", summary="토큰 갱신")
async def refresh_token_endpoint(request_data: Dict[str, str]):
    """리프레시 토큰으로 새 액세스 토큰 발급"""
    
    refresh_token = request_data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is required")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # 새 액세스 토큰 생성
        new_access_token = create_access_token(data={"sub": user_id})
        
        return {"access_token": new_access_token, "token_type": "bearer"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout", summary="로그아웃")
async def logout(current_user: dict = Depends(verify_token)):
    """사용자 로그아웃 (토큰 무효화)"""
    
    # 실제 구현시엔 토큰을 블랙리스트에 추가하거나 세션 DB에서 제거
    logger.info(f"사용자 로그아웃: {current_user['username']}")
    
    return {"message": "성공적으로 로그아웃되었습니다"}

# 테스트용 엔드포인트
@router.get("/test-protected", summary="토큰 인증 테스트")
async def test_protected_route(current_user: dict = Depends(verify_token)):
    """JWT 토큰 인증이 필요한 테스트 엔드포인트"""
    return {
        "message": "인증된 사용자입니다",
        "user_info": current_user
    }