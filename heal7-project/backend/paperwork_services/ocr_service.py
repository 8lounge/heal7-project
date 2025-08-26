#!/usr/bin/env python3
"""
네이버 CLOVA OCR 서비스 모듈 (1순위 핵심)
- 네이버 OCR API 연동
- 다중 페이지 처리
- 표 인식 지원
- HWP/HWPX 파일 지원
"""

import os
import json
import logging
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

class NaverOCRService:
    """네이버 CLOVA OCR 서비스 클래스"""
    
    def __init__(self):
        # API 키 로드
        api_keys = self._load_api_keys()
        
        self.api_url = os.getenv('NAVER_OCR_URL', 'https://your-ocr-api.apigw.ntruss.com/custom/v1/your-model/general')
        self.secret_key = api_keys.get('NAVER_OCR_API_KEY') or os.getenv('NAVER_OCR_SECRET_KEY')
        self.domain_code = api_keys.get('NAVER_OCR_DOMAIN_CODE', 'HealingSpace')
        self.invoke_url = os.getenv('NAVER_OCR_INVOKE_URL')
        
        if not self.secret_key:
            logger.warning("네이버 OCR SECRET KEY가 설정되지 않았습니다")
        else:
            logger.info(f"네이버 OCR API 설정 완료: {self.domain_code}")
    
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
    
    async def process_image_ocr(self, image_data: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        이미지 OCR 처리 (핵심 기능)
        
        Args:
            image_data: Base64 인코딩된 이미지 데이터
            options: OCR 옵션 (언어, 표 인식 등)
        
        Returns:
            OCR 결과 딕셔너리
        """
        try:
            if not self.secret_key:
                return {
                    'success': False,
                    'error': 'OCR API 키가 설정되지 않았습니다',
                    'text': ''
                }
            
            # 기본 옵션 설정
            default_options = {
                'lang': 'ko',
                'enable_table': True,
                'format': 'png'
            }
            
            if options:
                default_options.update(options)
            
            # OCR API 요청 데이터 구성
            request_data = {
                "version": "V2",
                "requestId": f"paperwork-{datetime.now().timestamp()}",
                "timestamp": int(datetime.now().timestamp() * 1000),
                "lang": default_options['lang'],
                "images": [{
                    "format": default_options['format'],
                    "name": "document_image",
                    "data": image_data
                }],
                "enableTableDetection": default_options['enable_table']
            }
            
            # API 호출
            async with aiohttp.ClientSession() as session:
                headers = {
                    'X-OCR-SECRET': self.secret_key,
                    'Content-Type': 'application/json'
                }
                
                async with session.post(
                    self.api_url,
                    json=request_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"OCR API 오류 {response.status}: {error_text}")
                        return {
                            'success': False,
                            'error': f'OCR API 호출 실패: {response.status}',
                            'text': ''
                        }
                    
                    result_data = await response.json()
                    
                    # 텍스트 추출
                    extracted_text = self._extract_text_from_response(result_data)
                    
                    return {
                        'success': True,
                        'text': extracted_text,
                        'raw_data': result_data,
                        'timestamp': datetime.now().isoformat()
                    }
                    
        except asyncio.TimeoutError:
            logger.error("OCR API 타임아웃")
            return {
                'success': False,
                'error': 'OCR 처리 시간 초과',
                'text': ''
            }
        except Exception as e:
            logger.error(f"OCR 처리 오류: {e}")
            return {
                'success': False,
                'error': f'OCR 처리 중 오류: {str(e)}',
                'text': ''
            }
    
    def _extract_text_from_response(self, ocr_response: Dict[str, Any]) -> str:
        """
        OCR 응답에서 텍스트 추출
        
        Args:
            ocr_response: 네이버 OCR API 응답
        
        Returns:
            추출된 텍스트
        """
        try:
            if not ocr_response.get('images'):
                return ""
            
            full_text_lines = []
            
            for image in ocr_response['images']:
                # 일반 텍스트 필드 처리
                if image.get('fields'):
                    for field in image['fields']:
                        line_text = field.get('inferText', '').strip()
                        if line_text:
                            full_text_lines.append(line_text)
                
                # 표 데이터 처리
                if image.get('tables'):
                    for table in image['tables']:
                        full_text_lines.append("\n[표 시작]")
                        
                        # 테이블 셀 처리
                        for cell in table.get('cells', []):
                            cell_text = []
                            for line in cell.get('cellTextLines', []):
                                for word in line.get('cellWords', []):
                                    word_text = word.get('inferText', '').strip()
                                    if word_text:
                                        cell_text.append(word_text)
                            
                            if cell_text:
                                full_text_lines.append(' '.join(cell_text))
                        
                        full_text_lines.append("[표 끝]\n")
            
            return '\n'.join(full_text_lines)
            
        except Exception as e:
            logger.error(f"텍스트 추출 오류: {e}")
            return ""
    
    async def process_multi_page_ocr(self, image_list: List[str], options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        다중 페이지 OCR 처리
        
        Args:
            image_list: Base64 인코딩된 이미지 데이터 리스트
            options: OCR 옵션
        
        Returns:
            다중 페이지 OCR 결과
        """
        try:
            all_texts = []
            all_raw_data = []
            
            for i, image_data in enumerate(image_list):
                logger.info(f"페이지 {i+1}/{len(image_list)} 처리 중...")
                
                page_result = await self.process_image_ocr(image_data, options)
                
                if page_result['success']:
                    all_texts.append(f"=== 페이지 {i+1} ===\n{page_result['text']}\n")
                    all_raw_data.append(page_result['raw_data'])
                else:
                    all_texts.append(f"=== 페이지 {i+1} (오류) ===\n{page_result['error']}\n")
                
                # 페이지 간 대기 (API 호출 제한 방지)
                if i < len(image_list) - 1:
                    await asyncio.sleep(0.5)
            
            combined_text = '\n'.join(all_texts)
            
            return {
                'success': True,
                'text': combined_text,
                'page_count': len(image_list),
                'raw_data': all_raw_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"다중 페이지 OCR 처리 오류: {e}")
            return {
                'success': False,
                'error': f'다중 페이지 OCR 처리 중 오류: {str(e)}',
                'text': ''
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """OCR 서비스 상태 확인"""
        return {
            'service': 'naver_ocr',
            'status': 'healthy' if self.secret_key else 'error',
            'configured': bool(self.secret_key),
            'api_url': self.api_url[:50] + '...' if len(self.api_url) > 50 else self.api_url,
            'timestamp': datetime.now().isoformat()
        }


# 전역 OCR 서비스 인스턴스
ocr_service = NaverOCRService()


# 편의 함수들
async def process_ocr(image_data: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
    """OCR 처리 편의 함수"""
    return await ocr_service.process_image_ocr(image_data, options)


async def process_multi_page_ocr(image_list: List[str], options: Dict[str, Any] = None) -> Dict[str, Any]:
    """다중 페이지 OCR 처리 편의 함수"""
    return await ocr_service.process_multi_page_ocr(image_list, options)


async def ocr_health_check() -> Dict[str, Any]:
    """OCR 서비스 헬스체크 편의 함수"""
    return await ocr_service.health_check()