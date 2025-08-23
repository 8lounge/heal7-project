#!/usr/bin/env python3
"""
유효성 검사 유틸리티
"""

import re
from typing import Dict, Any, List, Optional

class ValidationUtils:
    """유효성 검사 유틸리티 클래스"""
    
    @staticmethod
    def validate_text_input(text: str, min_length: int = 1, max_length: int = 100000) -> Dict[str, Any]:
        """텍스트 입력 유효성 검사"""
        if not text or not isinstance(text, str):
            return {'valid': False, 'error': '텍스트가 비어있거나 올바르지 않습니다'}
        
        text_length = len(text.strip())
        
        if text_length < min_length:
            return {'valid': False, 'error': f'텍스트가 너무 짧습니다 (최소 {min_length}자)'}
        
        if text_length > max_length:
            return {'valid': False, 'error': f'텍스트가 너무 깁니다 (최대 {max_length}자)'}
        
        return {'valid': True, 'length': text_length}
    
    @staticmethod
    def validate_conversion_type(conversion_type: str, allowed_types: List[str] = None) -> Dict[str, Any]:
        """변환 타입 유효성 검사"""
        if not conversion_type or not isinstance(conversion_type, str):
            return {'valid': False, 'error': '변환 타입이 지정되지 않았습니다'}
        
        if allowed_types is None:
            allowed_types = ['md', 'text_table', 'summary']
        
        if conversion_type not in allowed_types:
            return {
                'valid': False, 
                'error': f'지원하지 않는 변환 타입: {conversion_type}',
                'allowed_types': allowed_types
            }
        
        return {'valid': True, 'type': conversion_type}
    
    @staticmethod
    def validate_ai_model(model_id: str, available_models: List[str] = None) -> Dict[str, Any]:
        """AI 모델 ID 유효성 검사"""
        if not model_id or not isinstance(model_id, str):
            return {'valid': False, 'error': 'AI 모델이 지정되지 않았습니다'}
        
        if available_models is None:
            available_models = ['claude_sonnet4', 'gpt5', 'gpt5_mini', 'gpt4o', 'gpt41', 'gemini_flash2']
        
        if model_id not in available_models:
            return {
                'valid': False,
                'error': f'지원하지 않는 AI 모델: {model_id}',
                'available_models': available_models
            }
        
        return {'valid': True, 'model_id': model_id}
    
    @staticmethod
    def validate_ocr_options(options: Dict[str, Any]) -> Dict[str, Any]:
        """OCR 옵션 유효성 검사"""
        if not isinstance(options, dict):
            return {'valid': False, 'error': 'OCR 옵션이 올바르지 않습니다'}
        
        # 언어 코드 검사
        lang = options.get('lang', 'ko')
        allowed_langs = ['ko', 'en', 'ja', 'zh']
        if lang not in allowed_langs:
            return {
                'valid': False,
                'error': f'지원하지 않는 언어: {lang}',
                'allowed_langs': allowed_langs
            }
        
        # 표 인식 옵션 검사
        enable_table = options.get('enable_table', True)
        if not isinstance(enable_table, bool):
            return {'valid': False, 'error': '표 인식 옵션은 boolean 값이어야 합니다'}
        
        return {'valid': True, 'options': options}
    
    @staticmethod
    def validate_ai_options(options: Dict[str, Any]) -> Dict[str, Any]:
        """AI 처리 옵션 유효성 검사"""
        if not isinstance(options, dict):
            return {'valid': False, 'error': 'AI 옵션이 올바르지 않습니다'}
        
        # max_tokens 검사
        max_tokens = options.get('max_tokens')
        if max_tokens is not None:
            if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 8192:
                return {'valid': False, 'error': 'max_tokens는 1~8192 사이의 정수여야 합니다'}
        
        # temperature 검사
        temperature = options.get('temperature')
        if temperature is not None:
            if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 2:
                return {'valid': False, 'error': 'temperature는 0~2 사이의 숫자여야 합니다'}
        
        return {'valid': True, 'options': options}
    
    @staticmethod
    def validate_base64_image(base64_data: str) -> Dict[str, Any]:
        """Base64 이미지 데이터 유효성 검사"""
        if not base64_data or not isinstance(base64_data, str):
            return {'valid': False, 'error': 'Base64 데이터가 비어있습니다'}
        
        # Base64 패턴 검사
        base64_pattern = r'^[A-Za-z0-9+/]*={0,2}$'
        if not re.match(base64_pattern, base64_data.replace('\n', '').replace('\r', '')):
            return {'valid': False, 'error': '올바르지 않은 Base64 형식입니다'}
        
        # 데이터 크기 검사 (대략적)
        data_size = len(base64_data) * 3 / 4  # Base64 디코딩 후 예상 크기
        max_size = 50 * 1024 * 1024  # 50MB
        
        if data_size > max_size:
            return {
                'valid': False,
                'error': f'이미지 데이터가 너무 큽니다 (예상 크기: {int(data_size)} bytes)',
                'estimated_size': int(data_size),
                'max_size': max_size
            }
        
        return {'valid': True, 'estimated_size': int(data_size)}
    
    @staticmethod
    def validate_file_list(file_list: List[str], max_files: int = 20) -> Dict[str, Any]:
        """파일 목록 유효성 검사"""
        if not isinstance(file_list, list):
            return {'valid': False, 'error': '파일 목록이 올바르지 않습니다'}
        
        if len(file_list) == 0:
            return {'valid': False, 'error': '파일 목록이 비어있습니다'}
        
        if len(file_list) > max_files:
            return {
                'valid': False,
                'error': f'파일 개수가 너무 많습니다 (최대 {max_files}개)',
                'file_count': len(file_list),
                'max_files': max_files
            }
        
        return {'valid': True, 'file_count': len(file_list)}
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """파일명 sanitize"""
        if not filename:
            return 'unnamed_file'
        
        # 위험한 문자 제거
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # 연속된 점 제거
        sanitized = re.sub(r'\.{2,}', '.', sanitized)
        
        # 앞뒤 공백 및 점 제거
        sanitized = sanitized.strip(' .')
        
        # 빈 문자열 처리
        if not sanitized:
            return 'unnamed_file'
        
        # 길이 제한
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:255-len(ext)] + ext
        
        return sanitized
    
    @staticmethod
    def validate_request_data(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """요청 데이터 필수 필드 검사"""
        if not isinstance(data, dict):
            return {'valid': False, 'error': '요청 데이터가 올바르지 않습니다'}
        
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            return {
                'valid': False,
                'error': f'필수 필드가 누락되었습니다: {", ".join(missing_fields)}',
                'missing_fields': missing_fields
            }
        
        return {'valid': True, 'data': data}