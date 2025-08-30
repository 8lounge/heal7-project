#!/usr/bin/env python3
"""
🔐 AI 크롤링 시스템 API 키 설정 관리
실제 API 키 설정 및 환경변수 관리 시스템

Author: HEAL7 Development Team
Version: 1.0.0  
Date: 2025-08-29
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional, Any
import json

logger = logging.getLogger(__name__)


class APIKeysManager:
    """🔐 API 키 관리자"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "api_keys.json"
        self.api_keys = {}
        self._load_api_keys()
    
    def _load_api_keys(self):
        """API 키 로드 (환경변수 → 파일 → 기본값 순)"""
        
        # 1. 환경변수에서 로드
        env_keys = {
            "gemini_api_key": os.getenv("GEMINI_API_KEY"),
            "google_api_key": os.getenv("GOOGLE_API_KEY"), 
            "claude_api_key": os.getenv("CLAUDE_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY")
        }
        
        # 2. 설정 파일에서 로드 (존재하는 경우)
        file_keys = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_keys = json.load(f)
                logger.info("✅ API 키 설정 파일 로드 완료")
            except Exception as e:
                logger.warning(f"⚠️ API 키 설정 파일 로드 실패: {e}")
        
        # 3. 우선순위: 환경변수 → 파일 → None
        self.api_keys = {
            "gemini": (env_keys.get("gemini_api_key") or 
                      env_keys.get("google_api_key") or 
                      file_keys.get("gemini_api_key") or 
                      file_keys.get("google_api_key")),
            
            "claude": (env_keys.get("claude_api_key") or 
                      env_keys.get("anthropic_api_key") or
                      file_keys.get("claude_api_key") or 
                      file_keys.get("anthropic_api_key")),
        }
        
        # 4. 유효한 키 확인
        valid_keys = {k: v for k, v in self.api_keys.items() if v and v != "your-api-key-here"}
        
        if valid_keys:
            logger.info(f"✅ 유효한 API 키 발견: {', '.join(valid_keys.keys())}")
        else:
            logger.warning("⚠️ 유효한 API 키가 없음 - 로컬 패턴 모드로 실행")
    
    def get_gemini_api_key(self) -> Optional[str]:
        """Gemini Flash 2.0 API 키 반환"""
        key = self.api_keys.get("gemini")
        if key and key != "your-api-key-here":
            return key
        return None
    
    def get_claude_api_key(self) -> Optional[str]:
        """Claude API 키 반환"""
        key = self.api_keys.get("claude")
        if key and key != "your-api-key-here":
            return key
        return None
    
    def has_valid_api_keys(self) -> bool:
        """유효한 API 키 존재 여부"""
        return any([
            self.get_gemini_api_key(),
            self.get_claude_api_key()
        ])
    
    def get_api_status(self) -> Dict[str, Any]:
        """API 키 상태 정보"""
        return {
            "gemini_configured": bool(self.get_gemini_api_key()),
            "claude_configured": bool(self.get_claude_api_key()),
            "has_any_valid_keys": self.has_valid_api_keys(),
            "fallback_mode_required": not self.has_valid_api_keys()
        }
    
    def create_sample_config_file(self):
        """샘플 설정 파일 생성"""
        sample_config = {
            "gemini_api_key": "your-gemini-flash-2.0-api-key-here",
            "claude_api_key": "your-claude-api-key-here",
            "_instructions": {
                "1": "이 파일에 실제 API 키를 입력하세요",
                "2": "또는 환경변수 GEMINI_API_KEY, CLAUDE_API_KEY 사용",
                "3": "보안을 위해 git에 커밋하지 마세요 (.gitignore 추가)"
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📝 샘플 API 키 설정 파일 생성: {self.config_file}")
    
    def set_api_key(self, provider: str, api_key: str):
        """런타임에 API 키 설정"""
        if provider.lower() in ["gemini", "google"]:
            self.api_keys["gemini"] = api_key
        elif provider.lower() in ["claude", "anthropic"]:
            self.api_keys["claude"] = api_key
        
        logger.info(f"✅ {provider} API 키 설정 완료")


def create_api_keys_manager() -> APIKeysManager:
    """API 키 관리자 인스턴스 생성"""
    manager = APIKeysManager()
    
    # 설정 파일이 없으면 샘플 생성
    if not manager.config_file.exists():
        manager.create_sample_config_file()
    
    return manager


def setup_api_keys_environment():
    """API 키 환경 설정 가이드"""
    print("\n" + "="*60)
    print("🔐 AI 크롤링 시스템 API 키 설정 가이드")
    print("="*60)
    
    manager = create_api_keys_manager()
    status = manager.get_api_status()
    
    print(f"✅ Gemini Flash 2.0: {'설정됨' if status['gemini_configured'] else '❌ 미설정'}")
    print(f"✅ Claude API: {'설정됨' if status['claude_configured'] else '❌ 미설정'}")
    
    if not status['has_any_valid_keys']:
        print("\n⚠️ 실제 API 키가 설정되지 않음")
        print("📋 설정 방법:")
        print("   1. 환경변수 설정:")
        print("      export GEMINI_API_KEY='your-actual-gemini-key'")
        print("      export CLAUDE_API_KEY='your-actual-claude-key'")
        print(f"   2. 설정 파일 편집: {manager.config_file}")
        print("   3. 런타임 설정: manager.set_api_key('gemini', 'key')")
        print("\n🔄 로컬 패턴 모드로 계속 실행...")
    else:
        print("\n🚀 API 키 설정 완료 - AI 모델 사용 가능!")
    
    return manager


if __name__ == "__main__":
    setup_api_keys_environment()