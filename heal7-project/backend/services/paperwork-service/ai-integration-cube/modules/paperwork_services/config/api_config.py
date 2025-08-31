#!/usr/bin/env python3
"""
API 설정 관리
네이버 OCR API 및 AI 모델 API 설정
"""

import os
from typing import Dict, Any, Optional

class APIConfig:
    """API 설정 관리 클래스"""
    
    def __init__(self):
        # API 키 로드
        self.api_keys = self._load_api_keys()
        
        # 네이버 OCR API 설정
        self.naver_ocr = {
            'url': os.getenv('NAVER_OCR_URL', 'https://your-ocr-api.ntruss.com/custom/v1/your-model/general'),
            'secret_key': self.get('NAVER_OCR_SECRET_KEY'),
            'invoke_url': self.get('NAVER_OCR_INVOKE_URL'),
            'timeout': 60,
            'max_retries': 3
        }
        
        # AI 모델 API 설정
        self.ai_models = {
            'claude_sonnet4': {
                'name': 'Claude Sonnet 4',
                'endpoint': 'https://api.com/v1/messages',
                'api_key': self.get('ANTHROPIC_API_KEY'),
                'model_id': 'claude-3-5-sonnet-20241022',
                'max_tokens': 4096,
                'timeout': 60,
                'headers': {
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                }
            },
            'gpt5': {
                'name': 'GPT-5',
                'endpoint': 'https://api.com/v1/chat/completions',
                'api_key': self.get('OPENAI_API_KEY'),
                'model_id': 'gpt-5',
                'max_tokens': 4096,
                'timeout': 60
            },
            'gpt5_mini': {
                'name': 'GPT-5 Mini',
                'endpoint': 'https://api.com/v1/chat/completions',
                'api_key': self.get('OPENAI_API_KEY'),
                'model_id': 'gpt-5-mini',
                'max_tokens': 2048,
                'timeout': 60
            },
            'gpt4o': {
                'name': 'GPT-4o',
                'endpoint': 'https://api.com/v1/chat/completions',
                'api_key': self.get('OPENAI_API_KEY'),
                'model_id': 'gpt-4o',
                'max_tokens': 4096,
                'timeout': 60
            },
            'gpt41': {
                'name': 'GPT-4.1',
                'endpoint': 'https://api.com/v1/chat/completions',
                'api_key': self.get('OPENAI_API_KEY'),
                'model_id': 'gpt-4.1',
                'max_tokens': 4096,
                'timeout': 60
            },
            'gemini_flash2': {
                'name': 'Gemini Flash 2.0',
                'endpoint': 'https://generativelanguage.com/v1beta/models/gemini-2.0-flash:generateContent',
                'api_key': self.get('GEMINI_API_KEY'),
                'model_id': 'gemini-2.0-flash',
                'max_tokens': 4096,
                'timeout': 60
            }
        }
    
    def _load_api_keys(self) -> Dict[str, str]:
        """API 키 파일에서 키들을 로드"""
        keys = {}
        api_keys_file = "/home/ubuntu/.env.ai"
        
        try:
            if os.exists(api_keys_file):
                with open(api_keys_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            keys[key] = value.strip('"\'')
        except Exception as e:
            print(f"API 키 로드 실패: {e}")
        
        return keys
    
    def get_ocr_config(self) -> Dict[str, Any]:
        """OCR API 설정 반환"""
        return self.copy()
    
    def get_ai_model_config(self, model_id: str) -> Optional[Dict[str, Any]]:
        """AI 모델 설정 반환"""
        return self.get(model_id)
    
    def get_all_ai_models(self) -> Dict[str, Dict[str, Any]]:
        """모든 AI 모델 설정 반환"""
        return self.copy()
    
    def is_ocr_configured(self) -> bool:
        """OCR API가 설정되었는지 확인"""
        return bool(self.naver_ocr['secret_key'])
    
    def is_ai_model_configured(self, model_id: str) -> bool:
        """특정 AI 모델이 설정되었는지 확인"""
        model_config = self.get(model_id)
        return bool(model_config and model_config['api_key'])
    
    def get_configured_models(self) -> list:
        """설정된 AI 모델 목록 반환"""
        configured = []
        for model_id, config in self.items():
            if config['api_key']:
                configured.append(model_id)
        return configured
    
    def get_api_status(self) -> Dict[str, Any]:
        """전체 API 상태 반환"""
        ocr_status = {
            'configured': self.is_ocr_configured(),
            'url_set': bool(self.naver_ocr['url']),
            'secret_key_set': bool(self.naver_ocr['secret_key'])
        }
        
        ai_models_status = {}
        for model_id, config in self.items():
            ai_models_status[model_id] = {
                'name': config['name'],
                'configured': bool(config['api_key']),
                'endpoint': config['endpoint'][:50] + '...' if len(config['endpoint']) > 50 else config['endpoint']
            }
        
        return {
            'ocr': ocr_status,
            'ai_models': ai_models_status,
            'total_configured_models': len(self.get_configured_models())
        }


# 전역 API 설정 인스턴스
api_config = APIConfig()