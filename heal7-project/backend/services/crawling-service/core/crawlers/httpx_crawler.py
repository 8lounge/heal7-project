#!/usr/bin/env python3
"""
🚀 HTTPX 크롤러 (Tier 1)
빠르고 효율적인 정적 사이트 및 API 크롤링

Features:
- 비동기 HTTP/2 지원
- 자동 리다이렉트 처리
- 세션 및 쿠키 관리
- 응답 스트리밍 지원

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import asyncio
import time
import json
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from .base_crawler import (
    BaseCrawler, CrawlResult, CrawlConfig, CrawlerType,
    CrawlingError, TimeoutError, create_default_headers, is_valid_url
)


class HttpxCrawler(BaseCrawler):
    """🚀 HTTPX 기반 고성능 크롤러"""
    
    def __init__(self):
        super().__init__("httpx")
        self.client: Optional[httpx.AsyncClient] = None
        self.default_limits = httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100,
            keepalive_expiry=30
        )
        
    async def initialize(self):
        """HTTPX 클라이언트 초기화"""
        if self.is_initialized:
            return
            
        try:
            self.client = httpx.AsyncClient(
                limits=self.default_limits,
                timeout=httpx.Timeout(30.0),
                follow_redirects=True,
                http2=True,
                headers=create_default_headers()
            )
            
            self.is_initialized = True
            self.logger.info("✅ HTTPX 크롤러 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"❌ HTTPX 초기화 실패: {e}")
            raise CrawlingError(f"HTTPX 초기화 실패: {e}")
    
    async def cleanup(self):
        """리소스 정리"""
        if self.client:
            await self.client.aclose()
            self.client = None
        self.is_initialized = False
        self.logger.info("🛑 HTTPX 크롤러 정리 완료")
    
    async def crawl(self, config: CrawlConfig) -> CrawlResult:
        """메인 크롤링 함수"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        
        try:
            # URL 유효성 검사
            if not is_valid_url(config.url):
                raise CrawlingError(f"잘못된 URL: {config.url}")
            
            # 요청 헤더 설정
            headers = {**create_default_headers(), **config.headers}
            if config.user_agent:
                headers['User-Agent'] = config.user_agent
            
            # HTTP 요청 실행
            response = await self._make_request(config.url, headers, config.timeout)
            
            # 응답 처리
            result = await self._process_response(response, config, start_time)
            
            # 통계 업데이트
            self.update_stats(result)
            
            return result
            
        except httpx.TimeoutException:
            error_msg = f"요청 타임아웃: {config.url}"
            self.logger.warning(error_msg)
            return CrawlResult(
                success=False,
                error=error_msg,
                error_type="timeout",
                crawler_used=CrawlerType.HTTPX,
                url=config.url,
                response_time=time.time() - start_time
            )
            
        except httpx.RequestError as e:
            error_msg = f"네트워크 오류: {e}"
            self.logger.error(error_msg)
            return CrawlResult(
                success=False,
                error=error_msg,
                error_type="network_error",
                crawler_used=CrawlerType.HTTPX,
                url=config.url,
                response_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"예상치 못한 오류: {e}"
            self.logger.error(error_msg)
            return CrawlResult(
                success=False,
                error=error_msg,
                error_type="unexpected_error",
                crawler_used=CrawlerType.HTTPX,
                url=config.url,
                response_time=time.time() - start_time
            )
    
    async def _make_request(self, url: str, headers: Dict[str, str], timeout: int) -> httpx.Response:
        """HTTP 요청 실행"""
        try:
            response = await self.client.get(
                url,
                headers=headers,
                timeout=timeout
            )
            
            # 상태 코드 확인
            if response.status_code >= 400:
                self.logger.warning(f"HTTP {response.status_code}: {url}")
            
            return response
            
        except httpx.TimeoutException:
            raise
        except Exception as e:
            raise CrawlingError(f"요청 실행 실패: {e}")
    
    async def _process_response(self, response: httpx.Response, config: CrawlConfig, start_time: float) -> CrawlResult:
        """응답 처리"""
        response_time = time.time() - start_time
        
        try:
            # 콘텐츠 타입 확인
            content_type = response.headers.get('content-type', '').lower()
            
            # JSON 응답 처리
            if 'application/json' in content_type:
                content = await self._process_json_response(response)
            else:
                # HTML/텍스트 응답 처리
                content = response.text
            
            # 메타데이터 수집
            metadata = {
                'content_type': content_type,
                'content_length': len(content) if content else 0,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'final_url': str(response.url),
                'redirect_count': len(response.history),
                'encoding': response.encoding
            }
            
            # 성공 결과 반환
            return CrawlResult(
                success=True,
                html=content,
                status_code=response.status_code,
                metadata=metadata,
                crawler_used=CrawlerType.HTTPX,
                url=config.url,
                response_time=response_time
            )
            
        except Exception as e:
            self.logger.error(f"응답 처리 실패: {e}")
            return CrawlResult(
                success=False,
                error=f"응답 처리 실패: {e}",
                error_type="response_processing_error",
                status_code=response.status_code,
                crawler_used=CrawlerType.HTTPX,
                url=config.url,
                response_time=response_time
            )
    
    async def _process_json_response(self, response: httpx.Response) -> str:
        """JSON 응답 처리"""
        try:
            json_data = response.json()
            # JSON을 예쁘게 포맷팅해서 반환
            return json.dumps(json_data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # JSON 파싱 실패시 원본 텍스트 반환
            return response.text
    
    async def can_handle(self, url: str) -> bool:
        """URL 처리 가능 여부 판단"""
        if not is_valid_url(url):
            return False
        
        url_lower = url.lower()
        
        # API 엔드포인트 (최우선)
        if any(keyword in url_lower for keyword in [
            'api', '.json', '/rest/', '/graphql', '/v1/', '/v2/'
        ]):
            return True
        
        # 정적 파일
        if any(ext in url_lower for ext in [
            '.html', '.htm', '.xml', '.txt', '.css', '.js'
        ]):
            return True
        
        # 문서 파일 (다운로드)
        if any(ext in url_lower for ext in [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip'
        ]):
            return True
        
        # 기본적으로 대부분의 HTTP 요청 처리 가능
        return True
    
    async def download_file(self, url: str, save_path: str = None) -> CrawlResult:
        """파일 다운로드 전용 함수"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        
        try:
            async with self.client.stream('GET', url) as response:
                if response.status_code >= 400:
                    raise CrawlingError(f"다운로드 실패 HTTP {response.status_code}")
                
                content = b''
                async for chunk in response.aiter_bytes():
                    content += chunk
                
                # 파일 저장 (선택사항)
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(content)
                
                metadata = {
                    'file_size': len(content),
                    'content_type': response.headers.get('content-type'),
                    'filename': save_path or url.split('/')[-1]
                }
                
                return CrawlResult(
                    success=True,
                    html=f"Downloaded {len(content)} bytes",
                    status_code=response.status_code,
                    metadata=metadata,
                    crawler_used=CrawlerType.HTTPX,
                    url=url,
                    response_time=time.time() - start_time
                )
                
        except Exception as e:
            return CrawlResult(
                success=False,
                error=f"파일 다운로드 실패: {e}",
                crawler_used=CrawlerType.HTTPX,
                url=url,
                response_time=time.time() - start_time
            )
    
    async def get_page_info(self, url: str) -> Dict[str, Any]:
        """페이지 기본 정보 수집 (HEAD 요청)"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            response = await self.client.head(url, timeout=10)
            
            return {
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type'),
                'content_length': response.headers.get('content-length'),
                'last_modified': response.headers.get('last-modified'),
                'server': response.headers.get('server'),
                'final_url': str(response.url),
                'success': response.status_code < 400
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def batch_crawl(self, urls: List[str], max_concurrent: int = 10) -> List[CrawlResult]:
        """배치 크롤링 (여러 URL 동시 처리)"""
        if not self.is_initialized:
            await self.initialize()
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def crawl_single(url: str) -> CrawlResult:
            async with semaphore:
                config = CrawlConfig(url=url)
                return await self.crawl(config)
        
        tasks = [crawl_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 예외 처리
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(CrawlResult(
                    success=False,
                    error=str(result),
                    crawler_used=CrawlerType.HTTPX,
                    url=urls[i]
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_supported_features(self) -> List[str]:
        """지원하는 기능 목록"""
        return [
            "static_html",
            "json_api", 
            "file_download",
            "batch_crawling",
            "http2_support",
            "auto_redirect",
            "cookie_management",
            "streaming_download"
        ]


# 유틸리티 함수

async def quick_crawl(url: str, **kwargs) -> CrawlResult:
    """빠른 크롤링 (원샷 함수)"""
    crawler = HttpxCrawler()
    try:
        await crawler.initialize()
        config = CrawlConfig(url=url, **kwargs)
        return await crawler.crawl(config)
    finally:
        await crawler.cleanup()


async def is_url_accessible(url: str, timeout: int = 5) -> bool:
    """URL 접근 가능성 빠른 체크"""
    crawler = HttpxCrawler()
    try:
        await crawler.initialize()
        info = await crawler.get_page_info(url)
        return info.get('success', False)
    except:
        return False
    finally:
        await crawler.cleanup()