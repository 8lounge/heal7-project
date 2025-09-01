#!/usr/bin/env python3
"""
🤖 멀티모달 AI 분석기
Gemini Flash, GPT-4o, Claude Sonnet 통합 이미지/문서 분석

Features:
- 우선순위 기반 모델 선택
- 자동 폴백 시스템
- 이미지 OCR 및 분석
- 테이블 추출
- 문서 요약

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import os
import asyncio
import base64
import json
import logging
from typing import Dict, Any, Optional, List, Union, BinaryIO
from dataclasses import dataclass
from enum import Enum
from PIL import Image
import io

# AI SDK imports (with fallback)
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


logger = logging.getLogger(__name__)


class AIModel(Enum):
    """AI 모델 타입"""
    GEMINI_FLASH = "gemini_flash"
    GPT4O = "gpt4o"  
    CLAUDE_SONNET = "claude_sonnet"


@dataclass
class AIModelConfig:
    """AI 모델 설정"""
    name: str
    provider: str
    api_key: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.1
    rate_limit_per_minute: int = 60
    max_image_size_mb: int = 20
    priority: int = 1
    enabled: bool = True


class MultimodalAnalyzer:
    """🤖 멀티모달 AI 분석기"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.MultimodalAnalyzer")
        
        # API 키 로드
        self._load_api_keys()
        
        # 모델 설정
        self.models = self._initialize_models()
        
        # AI 클라이언트 인스턴스
        self.clients = {}
        
        # 통계
        self.usage_stats = {model.value: {'requests': 0, 'successes': 0, 'failures': 0} 
                          for model in AIModel}
    
    def _load_api_keys(self):
        """환경변수에서 API 키 로드"""
        self.api_keys = {
            'gemini': os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'),
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY')
        }
        
        # API 키 상태 로깅
        available_keys = [k for k, v in self.api_keys.items() if v and v != 'your-api-key']
        self.logger.info(f"사용 가능한 API 키: {available_keys}")
    
    def _initialize_models(self) -> Dict[AIModel, AIModelConfig]:
        """모델 설정 초기화"""
        models = {
            AIModel.GEMINI_FLASH: AIModelConfig(
                name="gemini-1.5-flash",
                provider="google",
                api_key=self.api_keys['gemini'],
                max_tokens=8000,
                rate_limit_per_minute=60,
                max_image_size_mb=20,
                priority=1,  # 최우선 (무료)
                enabled=bool(self.api_keys['gemini'])
            ),
            
            AIModel.GPT4O: AIModelConfig(
                name="gpt-4o",
                provider="openai",
                api_key=self.api_keys['openai'], 
                max_tokens=4000,
                rate_limit_per_minute=20,
                max_image_size_mb=20,
                priority=2,  # 2순위
                enabled=bool(self.api_keys['openai'])
            ),
            
            AIModel.CLAUDE_SONNET: AIModelConfig(
                name="claude-3-5-sonnet-20241022",
                provider="anthropic",
                api_key=self.api_keys['anthropic'],
                max_tokens=4000,
                rate_limit_per_minute=30,
                max_image_size_mb=5,
                priority=3,  # 3순위
                enabled=bool(self.api_keys['anthropic'])
            )
        }
        
        # 활성화된 모델만 반환
        return {k: v for k, v in models.items() if v.enabled}
    
    async def initialize(self):
        """AI 클라이언트 초기화"""
        self.logger.info("🤖 멀티모달 AI 분석기 초기화")
        
        for model_type, config in self.models.items():
            try:
                if config.provider == "google" and genai:
                    genai.configure(api_key=config.api_key)
                    self.clients[model_type] = genai.GenerativeModel(config.name)
                    
                elif config.provider == "openai" and OpenAI:
                    self.clients[model_type] = OpenAI(api_key=config.api_key)
                    
                elif config.provider == "anthropic" and Anthropic:
                    self.clients[model_type] = Anthropic(api_key=config.api_key)
                
                self.logger.info(f"✅ {config.name} 클라이언트 초기화 완료")
                    
            except Exception as e:
                self.logger.error(f"❌ {config.name} 초기화 실패: {e}")
                config.enabled = False
        
        enabled_models = [config.name for config in self.models.values() if config.enabled]
        self.logger.info(f"사용 가능한 모델: {enabled_models}")
    
    async def analyze_image(
        self, 
        image_data: Union[bytes, str], 
        prompt: str,
        preferred_model: Optional[AIModel] = None
    ) -> Dict[str, Any]:
        """이미지 분석"""
        
        # 이미지 전처리
        if isinstance(image_data, str):
            # 파일 경로인 경우
            with open(image_data, 'rb') as f:
                image_bytes = f.read()
        else:
            image_bytes = image_data
        
        # 이미지 크기 확인 및 최적화
        image_bytes = await self._optimize_image(image_bytes)
        
        # 모델 선택 및 시도
        models_to_try = self._get_model_priority_order(preferred_model)
        
        for model_type in models_to_try:
            try:
                self.logger.info(f"🎯 이미지 분석 시도: {model_type.value}")
                
                result = await self._analyze_with_model(model_type, image_bytes, prompt, "image")
                
                if result['success']:
                    self._update_stats(model_type, True)
                    return result
                    
            except Exception as e:
                self.logger.warning(f"❌ {model_type.value} 실패: {e}")
                self._update_stats(model_type, False)
                continue
        
        return {
            'success': False,
            'error': '모든 AI 모델 실패',
            'content': ''
        }
    
    async def extract_table_from_image(self, image_data: Union[bytes, str]) -> Dict[str, Any]:
        """이미지에서 테이블 추출"""
        
        prompt = """
        이 이미지에서 테이블을 찾아 구조화된 JSON으로 변환해주세요.
        
        요구사항:
        1. 모든 테이블을 찾아 분석
        2. 헤더와 데이터 행을 구분
        3. 빈 셀은 null로 표시
        4. 숫자는 숫자형으로, 텍스트는 문자열로
        
        출력 형식:
        {
            "tables": [
                {
                    "table_index": 1,
                    "headers": ["컬럼1", "컬럼2", "컬럼3"],
                    "rows": [
                        ["값1", "값2", "값3"],
                        ["값4", "값5", "값6"]
                    ]
                }
            ],
            "summary": "테이블 요약 설명"
        }
        """
        
        result = await self.analyze_image(image_data, prompt, AIModel.CLAUDE_SONNET)
        
        if result['success']:
            try:
                # JSON 파싱 시도
                content = result['content']
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0]
                
                parsed_data = json.loads(content)
                result['parsed_tables'] = parsed_data
                
            except json.JSONDecodeError:
                result['parsed_tables'] = None
                result['parse_error'] = 'JSON 파싱 실패'
        
        return result
    
    async def analyze_webpage_screenshot(self, image_data: Union[bytes, str]) -> Dict[str, Any]:
        """웹페이지 스크린샷 분석"""
        
        prompt = """
        이 웹페이지 스크린샷을 분석하여 다음 정보를 추출하세요:
        
        1. 주요 콘텐츠:
           - 제목과 헤딩 텍스트
           - 중요한 데이터나 수치
           - 목록이나 테이블의 항목들
        
        2. 인터페이스 요소:
           - 버튼 텍스트
           - 링크 텍스트  
           - 폼 필드 레이블
           - 메뉴 항목
        
        3. 구조적 정보:
           - 페이지 레이아웃 설명
           - 주요 섹션 구분
           - 네비게이션 구조
        
        한국어로 답변하고, 가능한 한 구체적이고 정확하게 추출하세요.
        """
        
        return await self.analyze_image(image_data, prompt, AIModel.GEMINI_FLASH)
    
    async def ocr_extract_text(self, image_data: Union[bytes, str]) -> Dict[str, Any]:
        """OCR 텍스트 추출"""
        
        prompt = """
        이 이미지에서 모든 텍스트를 정확하게 추출하세요.
        
        요구사항:
        1. 읽을 수 있는 모든 텍스트를 추출
        2. 원본의 레이아웃과 순서를 최대한 유지
        3. 표나 목록의 구조도 보존
        4. 흐릿하거나 작은 텍스트도 최대한 추출
        
        출력은 순수 텍스트로만 하되, 구조적 정보(제목, 목록 등)는 
        마크다운 형식으로 표현하세요.
        """
        
        return await self.analyze_image(image_data, prompt, AIModel.GEMINI_FLASH)
    
    async def _analyze_with_model(
        self, 
        model_type: AIModel, 
        image_bytes: bytes, 
        prompt: str,
        task_type: str
    ) -> Dict[str, Any]:
        """특정 모델로 분석 실행"""
        
        config = self.models[model_type]
        client = self.clients[model_type]
        
        if config.provider == "google":
            return await self._analyze_with_gemini(client, image_bytes, prompt)
            
        elif config.provider == "openai":
            return await self._analyze_with_gpt4o(client, image_bytes, prompt)
            
        elif config.provider == "anthropic":
            return await self._analyze_with_claude(client, image_bytes, prompt)
        
        else:
            raise ValueError(f"지원하지 않는 제공자: {config.provider}")
    
    async def _analyze_with_gemini(self, client, image_bytes: bytes, prompt: str) -> Dict[str, Any]:
        """Gemini Flash로 분석"""
        try:
            # PIL Image 생성
            image = Image.open(io.BytesIO(image_bytes))
            
            # Gemini에 전송
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: client.generate_content([prompt, image])
            )
            
            return {
                'success': True,
                'content': response.text,
                'model_used': 'gemini-1.5-flash'
            }
            
        except Exception as e:
            raise Exception(f"Gemini 분석 실패: {e}")
    
    async def _analyze_with_gpt4o(self, client, image_bytes: bytes, prompt: str) -> Dict[str, Any]:
        """GPT-4o로 분석"""
        try:
            # Base64 인코딩
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=4000
                )
            )
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'model_used': 'gpt-4o'
            }
            
        except Exception as e:
            raise Exception(f"GPT-4o 분석 실패: {e}")
    
    async def _analyze_with_claude(self, client, image_bytes: bytes, prompt: str) -> Dict[str, Any]:
        """Claude Sonnet으로 분석"""
        try:
            # Base64 인코딩
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": image_base64
                                    }
                                },
                                {
                                    "type": "text", 
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )
            )
            
            return {
                'success': True,
                'content': response.content[0].text,
                'model_used': 'claude-3-5-sonnet'
            }
            
        except Exception as e:
            raise Exception(f"Claude 분석 실패: {e}")
    
    async def _optimize_image(self, image_bytes: bytes) -> bytes:
        """이미지 최적화"""
        try:
            # PIL로 이미지 열기
            image = Image.open(io.BytesIO(image_bytes))
            
            # 이미지 크기 확인
            if len(image_bytes) > 10 * 1024 * 1024:  # 10MB 이상
                # 크기 조정
                max_dimension = 2048
                image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                
                # JPEG로 압축
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=85, optimize=True)
                return output.getvalue()
            
            return image_bytes
            
        except Exception as e:
            self.logger.warning(f"이미지 최적화 실패: {e}")
            return image_bytes
    
    def _get_model_priority_order(self, preferred_model: Optional[AIModel] = None) -> List[AIModel]:
        """모델 우선순위 순서 결정"""
        available_models = [model for model in self.models.keys() if self.models[model].enabled]
        
        if preferred_model and preferred_model in available_models:
            # 선호 모델을 첫 번째로
            other_models = [m for m in available_models if m != preferred_model]
            other_models.sort(key=lambda m: self.models[m].priority)
            return [preferred_model] + other_models
        else:
            # 우선순위 순으로 정렬
            available_models.sort(key=lambda m: self.models[m].priority)
            return available_models
    
    def _update_stats(self, model_type: AIModel, success: bool):
        """사용 통계 업데이트"""
        stats = self.usage_stats[model_type.value]
        stats['requests'] += 1
        
        if success:
            stats['successes'] += 1
        else:
            stats['failures'] += 1
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """사용 통계 반환"""
        return {
            'model_stats': self.usage_stats,
            'available_models': [config.name for config in self.models.values() if config.enabled],
            'total_requests': sum(stats['requests'] for stats in self.usage_stats.values())
        }


# 유틸리티 함수들

async def quick_image_analysis(image_path: str, prompt: str) -> str:
    """빠른 이미지 분석"""
    analyzer = MultimodalAnalyzer()
    await analyzer.initialize()
    
    result = await analyzer.analyze_image(image_path, prompt)
    
    if result['success']:
        return result['content']
    else:
        return f"분석 실패: {result.get('error', '알 수 없는 오류')}"


async def extract_table_data(image_path: str) -> Dict:
    """테이블 데이터 추출"""
    analyzer = MultimodalAnalyzer()
    await analyzer.initialize()
    
    return await analyzer.extract_table_from_image(image_path)