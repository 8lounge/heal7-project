#!/usr/bin/env python3
"""
통합 AI 모델 서비스
7개 AI 모델을 하나의 서비스로 관리
- Claude Sonnet 4
- GPT-5
- GPT-5 Mini  
- GPT-4o
- GPT-4.1
- Gemini Flash 2.0
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

class UnifiedAIService:
    """통합 AI 모델 서비스 클래스"""
    
    def __init__(self):
        # API 키 로드
        self.api_keys = self._load_api_keys()
        
        # 지원하는 AI 모델 설정
        self.models = {
            'claude_sonnet4': {
                'name': 'Claude Sonnet 4',
                'endpoint': 'https://api.anthropic.com/v1/messages',
                'api_key': self.api_keys.get('ANTHROPIC_API_KEY'),
                'max_tokens': 4096,
                'temperature': 0.7,
                'model_id': 'claude-3-5-sonnet-20241022'
            },
            'gpt5': {
                'name': 'GPT-5',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key': self.api_keys.get('OPENAI_API_KEY'),
                'max_tokens': 4096,
                'temperature': 0.7,
                'model_id': 'gpt-5'
            },
            'gpt5_mini': {
                'name': 'GPT-5 Mini',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key': self.api_keys.get('OPENAI_API_KEY'),
                'max_tokens': 2048,
                'temperature': 0.7,
                'model_id': 'gpt-5-mini'
            },
            'gpt4o': {
                'name': 'GPT-4o',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key': self.api_keys.get('OPENAI_API_KEY'),
                'max_tokens': 4096,
                'temperature': 0.7,
                'model_id': 'gpt-4o'
            },
            'gpt41': {
                'name': 'GPT-4.1',
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key': self.api_keys.get('OPENAI_API_KEY'),
                'max_tokens': 4096,
                'temperature': 0.7,
                'model_id': 'gpt-4.1'
            },
            'gemini_flash2': {
                'name': 'Gemini Flash 2.0',
                'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
                'api_key': self.api_keys.get('GEMINI_API_KEY'),
                'max_tokens': 4096,
                'temperature': 0.7,
                'model_id': 'gemini-2.0-flash'
            }
        }
    
    def _load_api_keys(self) -> Dict[str, str]:
        """API 키 파일에서 키들을 로드"""
        keys = {}
        api_keys_file = "/home/ubuntu/.env.ai"
        
        try:
            if os.path.exists(api_keys_file):
                with open(api_keys_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            keys[key] = value.strip('"\'')
        except Exception as e:
            logger.error(f"API 키 로드 실패: {e}")
        
        return keys
    
    def get_available_models(self) -> List[str]:
        """사용 가능한 AI 모델 목록 반환"""
        return list(self.models.keys())
    
    def get_model_info(self, model_id: str = None) -> Dict[str, Any]:
        """모델 정보 반환"""
        if model_id:
            if model_id not in self.models:
                return {'error': f'지원하지 않는 모델: {model_id}'}
            
            model = self.models[model_id]
            return {
                'id': model_id,
                'name': model['name'],
                'configured': bool(model['api_key']),
                'max_tokens': model['max_tokens'],
                'temperature': model['temperature']
            }
        else:
            # 모든 모델 정보 반환
            return {
                model_id: {
                    'name': model['name'],
                    'configured': bool(model['api_key']),
                    'max_tokens': model['max_tokens'],
                    'temperature': model['temperature']
                }
                for model_id, model in self.models.items()
            }
    
    def create_prompt(self, text: str, conversion_type: str, options: Dict[str, Any] = None) -> str:
        """변환 타입에 따른 프롬프트 생성"""
        
        if conversion_type == 'md':
            prompt = f"""
다음 텍스트를 깔끔한 Markdown 형식으로 변환해주세요.
- 제목은 적절한 레벨의 헤딩(#, ##, ###)을 사용하세요
- 목록은 - 또는 1. 형식을 사용하세요  
- 표가 있다면 Markdown 표 형식으로 변환하세요
- 중요한 내용은 **굵게** 표시하세요
- 코드나 특수 형식은 적절한 마크다운 문법을 사용하세요

원본 텍스트:
{text}

Markdown 변환 결과:
"""
        
        elif conversion_type == 'text_table':
            prompt = f"""
다음 텍스트에서 주요 내용과 표를 구조화하여 정리해주세요.
- 표는 명확하게 구분하여 표시하세요
- 주요 정보를 체계적으로 정리하세요
- 불필요한 내용은 제거하고 핵심만 추출하세요

원본 텍스트:
{text}

정리된 결과:
"""
        
        elif conversion_type == 'summary':
            prompt = f"""
다음 문서의 내용을 요약해주세요.
- 핵심 내용만 간결하게 정리하세요
- 중요한 수치나 데이터는 포함하세요
- 3-5개의 주요 포인트로 구성하세요

원본 텍스트:
{text}

요약 결과:
"""
        
        else:
            prompt = f"""
다음 텍스트를 {conversion_type} 형식으로 변환해주세요.

원본 텍스트:
{text}

변환 결과:
"""
        
        return prompt
    
    async def process_with_claude(self, model_config: Dict[str, Any], prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Claude API 처리"""
        try:
            max_tokens = options.get('max_tokens', model_config['max_tokens']) if options else model_config['max_tokens']
            temperature = options.get('temperature', model_config['temperature']) if options else model_config['temperature']
            
            request_data = {
                "model": model_config['model_id'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'x-api-key': model_config['api_key'],
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                }
                
                async with session.post(
                    model_config['endpoint'],
                    json=request_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Claude API 오류 {response.status}: {error_text}',
                            'result': ''
                        }
                    
                    result_data = await response.json()
                    
                    if 'content' in result_data and len(result_data['content']) > 0:
                        return {
                            'success': True,
                            'result': result_data['content'][0]['text'],
                            'usage': result_data.get('usage', {})
                        }
                    else:
                        return {
                            'success': False,
                            'error': '응답에서 텍스트를 찾을 수 없습니다',
                            'result': ''
                        }
                        
        except Exception as e:
            logger.error(f"Claude API 오류: {e}")
            return {
                'success': False,
                'error': f'Claude 처리 중 오류: {str(e)}',
                'result': ''
            }
    
    async def process_with_openai(self, model_config: Dict[str, Any], prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """OpenAI API 처리 (GPT-5, GPT-5 Mini, GPT-4o, GPT-4.1)"""
        try:
            max_tokens = options.get('max_tokens', model_config['max_tokens']) if options else model_config['max_tokens']
            temperature = options.get('temperature', model_config['temperature']) if options else model_config['temperature']
            
            request_data = {
                "model": model_config['model_id'],
                "messages": [
                    {
                        "role": "system",
                        "content": "당신은 문서 변환 전문가입니다. 정확하고 깔끔하게 변환해주세요."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {model_config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                
                async with session.post(
                    model_config['endpoint'],
                    json=request_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'OpenAI API 오류 {response.status}: {error_text}',
                            'result': ''
                        }
                    
                    result_data = await response.json()
                    
                    if 'choices' in result_data and len(result_data['choices']) > 0:
                        return {
                            'success': True,
                            'result': result_data['choices'][0]['message']['content'],
                            'usage': result_data.get('usage', {})
                        }
                    else:
                        return {
                            'success': False,
                            'error': '응답에서 텍스트를 찾을 수 없습니다',
                            'result': ''
                        }
                        
        except Exception as e:
            logger.error(f"OpenAI API 오류: {e}")
            return {
                'success': False,
                'error': f'OpenAI 처리 중 오류: {str(e)}',
                'result': ''
            }
    
    async def process_with_gemini(self, model_config: Dict[str, Any], prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Gemini API 처리"""
        try:
            max_tokens = options.get('max_tokens', model_config['max_tokens']) if options else model_config['max_tokens']
            temperature = options.get('temperature', model_config['temperature']) if options else model_config['temperature']
            
            request_data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{model_config['endpoint']}?key={model_config['api_key']}",
                    json=request_data,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Gemini API 오류 {response.status}: {error_text}',
                            'result': ''
                        }
                    
                    result_data = await response.json()
                    
                    if 'candidates' in result_data and len(result_data['candidates']) > 0:
                        return {
                            'success': True,
                            'result': result_data['candidates'][0]['content']['parts'][0]['text'],
                            'usage': result_data.get('usageMetadata', {})
                        }
                    else:
                        return {
                            'success': False,
                            'error': '응답에서 텍스트를 찾을 수 없습니다',
                            'result': ''
                        }
                        
        except Exception as e:
            logger.error(f"Gemini API 오류: {e}")
            return {
                'success': False,
                'error': f'Gemini 처리 중 오류: {str(e)}',
                'result': ''
            }
    
    async def process_text_conversion(self, model_id: str, text: str, conversion_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        통합 텍스트 변환 처리 (핵심 메서드)
        
        Args:
            model_id: AI 모델 ID
            text: 변환할 텍스트
            conversion_type: 변환 타입 ('md', 'text_table', 'summary' 등)
            options: 추가 옵션
        
        Returns:
            변환 결과
        """
        try:
            # 모델 확인
            if model_id not in self.models:
                return {
                    'success': False,
                    'error': f'지원하지 않는 AI 모델: {model_id}',
                    'result': ''
                }
            
            model_config = self.models[model_id]
            
            # API 키 확인
            if not model_config['api_key']:
                return {
                    'success': False,
                    'error': f'{model_config["name"]} API 키가 설정되지 않았습니다',
                    'result': ''
                }
            
            # 프롬프트 생성
            prompt = self.create_prompt(text, conversion_type, options)
            
            # 모델별 처리
            if 'claude' in model_id:
                result = await self.process_with_claude(model_config, prompt, options)
            elif 'gpt' in model_id:
                result = await self.process_with_openai(model_config, prompt, options)
            elif 'gemini' in model_id:
                result = await self.process_with_gemini(model_config, prompt, options)
            else:
                return {
                    'success': False,
                    'error': f'처리기가 구현되지 않은 모델: {model_id}',
                    'result': ''
                }
            
            # 결과에 추가 정보 포함
            if result['success']:
                result.update({
                    'model': model_config['name'],
                    'model_id': model_id,
                    'conversion_type': conversion_type,
                    'timestamp': datetime.now().isoformat()
                })
            
            return result
            
        except Exception as e:
            logger.error(f"텍스트 변환 처리 오류: {e}")
            return {
                'success': False,
                'error': f'텍스트 변환 중 오류: {str(e)}',
                'result': ''
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """AI 서비스 상태 확인"""
        model_status = {}
        
        for model_id, model_config in self.models.items():
            model_status[model_id] = {
                'name': model_config['name'],
                'configured': bool(model_config['api_key']),
                'status': 'ready' if model_config['api_key'] else 'not_configured'
            }
        
        return {
            'service': 'unified_ai_service',
            'status': 'healthy',
            'models': model_status,
            'total_models': len(self.models),
            'configured_models': sum(1 for m in self.models.values() if m['api_key']),
            'timestamp': datetime.now().isoformat()
        }


# 전역 AI 서비스 인스턴스
ai_service = UnifiedAIService()


# 편의 함수들
async def process_ai_conversion(model_id: str, text: str, conversion_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
    """AI 변환 처리 편의 함수"""
    return await ai_service.process_text_conversion(model_id, text, conversion_type, options)


async def get_ai_models() -> List[str]:
    """사용 가능한 AI 모델 목록 편의 함수"""
    return ai_service.get_available_models()


async def get_ai_model_info(model_id: str = None) -> Dict[str, Any]:
    """AI 모델 정보 편의 함수"""
    return ai_service.get_model_info(model_id)


async def ai_health_check() -> Dict[str, Any]:
    """AI 서비스 헬스체크 편의 함수"""
    return await ai_service.health_check()