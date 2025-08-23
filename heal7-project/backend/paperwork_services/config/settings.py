#!/usr/bin/env python3
"""
Paperwork 서비스 통합 설정
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

class PaperworkSettings:
    """Paperwork 서비스 설정 클래스"""
    
    def __init__(self):
        # 기본 설정
        self.service_name = "Paperwork AI"
        self.version = "1.0.0"
        
        # 파일 경로 설정
        self.api_keys_file = "/home/ubuntu/.env.ai"
        self.temp_dir = "/tmp/paperwork"
        self.log_dir = "/tmp/paperwork/logs"
        
        # API 설정
        self.api_timeout = 60  # seconds
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.supported_file_types = ['.pdf', '.png', '.jpg', '.jpeg', '.hwp', '.hwpx']
        
        # OCR 설정
        self.ocr_default_lang = 'ko'
        self.ocr_enable_table = True
        self.ocr_batch_delay = 0.5  # seconds between API calls
        
        # AI 모델 기본 설정
        self.ai_default_max_tokens = 4096
        self.ai_default_temperature = 0.7
        self.ai_supported_conversion_types = ['md', 'text_table', 'summary']
        
        # 멀티 페이지 설정
        self.max_pages_per_request = 20
        self.page_processing_delay = 0.5
        
        # 로깅 설정
        self.log_level = "INFO"
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # 임시 디렉토리 생성
        self._ensure_directories()
    
    def _ensure_directories(self):
        """필요한 디렉토리 생성"""
        dirs = [self.temp_dir, self.log_dir]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def get_api_keys(self) -> Dict[str, str]:
        """API 키 파일에서 키들을 로드"""
        keys = {}
        try:
            if os.path.exists(self.api_keys_file):
                with open(self.api_keys_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            keys[key] = value.strip('"\'')
        except Exception as e:
            print(f"API 키 로드 실패: {e}")
        return keys
    
    def get_temp_file_path(self, filename: str) -> str:
        """임시 파일 경로 생성"""
        return os.path.join(self.temp_dir, filename)
    
    def is_supported_file_type(self, filename: str) -> bool:
        """지원하는 파일 타입인지 확인"""
        file_ext = Path(filename).suffix.lower()
        return file_ext in self.supported_file_types
    
    def get_conversion_settings(self, conversion_type: str) -> Dict[str, Any]:
        """변환 타입별 설정 반환"""
        settings = {
            'md': {
                'max_tokens': 4096,
                'temperature': 0.7,
                'description': 'Markdown 형식으로 변환'
            },
            'text_table': {
                'max_tokens': 3072,
                'temperature': 0.5,
                'description': '텍스트와 표 구조화'
            },
            'summary': {
                'max_tokens': 2048,
                'temperature': 0.6,
                'description': '문서 요약'
            }
        }
        
        return settings.get(conversion_type, {
            'max_tokens': self.ai_default_max_tokens,
            'temperature': self.ai_default_temperature,
            'description': f'{conversion_type} 변환'
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """설정을 딕셔너리로 변환"""
        return {
            'service_name': self.service_name,
            'version': self.version,
            'api_timeout': self.api_timeout,
            'max_file_size': self.max_file_size,
            'supported_file_types': self.supported_file_types,
            'ocr_default_lang': self.ocr_default_lang,
            'ocr_enable_table': self.ocr_enable_table,
            'ai_default_max_tokens': self.ai_default_max_tokens,
            'ai_default_temperature': self.ai_default_temperature,
            'ai_supported_conversion_types': self.ai_supported_conversion_types,
            'max_pages_per_request': self.max_pages_per_request
        }


# 전역 설정 인스턴스
settings = PaperworkSettings()