#!/usr/bin/env python3
"""
🤖 AI Research Engine - 웹사이트 구조 분석 및 수집 전략 생성
AI 모델을 활용한 동적 스크래핑 전략 개발 엔진

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-29
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

import aiohttp
import asyncpg
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin, urlparse


logger = logging.getLogger(__name__)


class StrategyConfidence(Enum):
    """전략 신뢰도 수준"""
    HIGH = "high"       # 95%+ 신뢰도
    MEDIUM = "medium"   # 80-94% 신뢰도
    LOW = "low"         # 60-79% 신뢰도
    UNCERTAIN = "uncertain"  # 60% 미만


@dataclass
class SiteAnalysisResult:
    """사이트 분석 결과"""
    site_url: str
    site_title: str = ""
    site_type: str = ""  # 'government', 'news', 'board', 'listing'
    content_structure: Dict[str, Any] = None
    data_patterns: List[Dict] = None
    recommended_selectors: Dict[str, str] = None
    pagination_info: Dict[str, Any] = None
    confidence_score: float = 0.0
    analysis_timestamp: str = ""
    
    def __post_init__(self):
        if self.content_structure is None:
            self.content_structure = {}
        if self.data_patterns is None:
            self.data_patterns = []
        if self.recommended_selectors is None:
            self.recommended_selectors = {}
        if self.pagination_info is None:
            self.pagination_info = {}
        if not self.analysis_timestamp:
            self.analysis_timestamp = datetime.now().isoformat()


@dataclass
class CollectionStrategy:
    """수집 전략 데이터 구조"""
    strategy_id: str
    site_id: str
    site_url: str
    
    # 핵심 선택자
    selectors: Dict[str, str] = None
    
    # 페이지네이션 전략
    pagination: Dict[str, Any] = None
    
    # 데이터 추출 규칙
    extraction_rules: Dict[str, Any] = None
    
    # 성능 설정
    performance_config: Dict[str, Any] = None
    
    # 메타데이터
    confidence: StrategyConfidence = StrategyConfidence.UNCERTAIN
    created_by: str = "ai_research_engine"
    created_at: str = ""
    last_tested_at: str = ""
    success_rate: float = 0.0
    
    def __post_init__(self):
        if self.selectors is None:
            self.selectors = {}
        if self.pagination is None:
            self.pagination = {}
        if self.extraction_rules is None:
            self.extraction_rules = {}
        if self.performance_config is None:
            self.performance_config = {
                "delay_between_requests": 2.0,
                "max_concurrent": 3,
                "timeout": 30
            }
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class AIResearchEngine:
    """🤖 AI 기반 웹사이트 분석 및 전략 생성 엔진"""
    
    def __init__(self, gemini_api_key: str = None, claude_api_key: str = None):
        # API 키 관리자에서 실제 키 로드
        try:
            from ..config.api_keys_config import create_api_keys_manager
            self.api_manager = create_api_keys_manager()
            
            # 실제 API 키 설정 (매개변수 → 관리자 → None)
            self.gemini_api_key = (gemini_api_key or 
                                 self.api_manager.get_gemini_api_key())
            self.claude_api_key = (claude_api_key or 
                                 self.api_manager.get_claude_api_key())
            
            # API 키 상태 로깅
            status = self.api_manager.get_api_status()
            if status['has_any_valid_keys']:
                logger.info("🔑 실제 API 키 로드 완료")
            else:
                logger.warning("⚠️ 실제 API 키 없음 - 로컬 패턴 모드로 실행")
                
        except ImportError:
            # 폴백: 기본 설정
            logger.warning("API 키 관리자 로드 실패 - 기본 설정 사용")
            self.gemini_api_key = gemini_api_key
            self.claude_api_key = claude_api_key
        
        # HTTP 세션
        self.session = None
        
        # AI 모델 동적 설정 - 사용 가능한 API 키에 따라
        self.ai_models = {}
        
        # Gemini Flash 2.0 (Primary)
        if self.gemini_api_key and self.gemini_api_key != "your-gemini-api-key":
            self.ai_models["primary"] = {
                "name": "gemini-2.0-flash-exp",
                "provider": "google",
                "api_key": self.gemini_api_key,
                "max_tokens": 8000,
                "temperature": 0.1,
                "enabled": True
            }
        
        # Claude (Fallback)  
        if self.claude_api_key and self.claude_api_key != "your-claude-api-key":
            model_key = "fallback" if "primary" in self.ai_models else "primary"
            self.ai_models[model_key] = {
                "name": "claude-3-sonnet",
                "provider": "anthropic", 
                "api_key": self.claude_api_key,
                "max_tokens": 4000,
                "temperature": 0.1,
                "enabled": True
            }
        
        # 로컬 패턴 (Always available)
        self.ai_models["local"] = {
            "name": "pattern-based",
            "provider": "local",
            "api_key": None,
            "enabled": True
        }
        
        # 활성 모델 로깅
        enabled_models = [k for k, v in self.ai_models.items() if v.get("enabled", False)]
        logger.info(f"🤖 활성 AI 모델: {', '.join(enabled_models)}")
        
        # 현재 활성 모델
        self.current_model = "primary"
        
        # 분석 템플릿들
        self.analysis_prompts = {
            "structure_analysis": self._get_structure_analysis_prompt(),
            "selector_generation": self._get_selector_generation_prompt(),
            "pagination_analysis": self._get_pagination_analysis_prompt()
        }
        
        # 사이트 타입별 패턴
        self.site_patterns = {
            "government_portal": {
                "indicators": ["go.kr", "정부", "공고", "지원사업", "신청"],
                "common_selectors": {
                    "item_container": [".board-list tr", ".list-item", ".program-item"],
                    "title": [".title a", ".subject a", "td:first-child a"],
                    "agency": [".agency", ".organ", ".institution"]
                }
            },
            "news_board": {
                "indicators": ["뉴스", "기사", "보도자료", "언론"],
                "common_selectors": {
                    "item_container": [".news-list li", ".article-list .item"],
                    "title": [".headline a", ".title a"],
                    "date": [".date", ".publish-date"]
                }
            }
        }
    
    async def initialize(self):
        """AI 연구 엔진 초기화"""
        logger.info("🤖 AI Research Engine 초기화 시작")
        
        # HTTP 세션 생성
        connector = aiohttp.TCPConnector(limit=5, ttl_dns_cache=300)
        timeout = aiohttp.ClientTimeout(total=60)
        
        self.session = aiohttp.ClientSession(
            headers={
                'User-Agent': 'HEAL7-AI-Research-Bot/1.0 (+https://heal7.com/ai-research)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            },
            connector=connector,
            timeout=timeout
        )
        
        logger.info("✅ AI Research Engine 초기화 완료")
    
    async def close(self):
        """리소스 정리"""
        if self.session:
            await self.session.close()
        logger.info("🛑 AI Research Engine 종료")
    
    async def analyze_website_structure(self, url: str) -> SiteAnalysisResult:
        """🔍 웹사이트 구조 종합 분석"""
        logger.info(f"🔍 웹사이트 구조 분석 시작: {url}")
        
        try:
            # 1. 기본 페이지 가져오기
            html_content = await self._fetch_page_content(url)
            if not html_content:
                raise Exception("페이지 내용을 가져올 수 없습니다")
            
            # 2. 기본 정보 추출
            soup = BeautifulSoup(html_content, 'html.parser')
            site_title = self._extract_site_title(soup)
            
            # 3. 사이트 타입 추론
            site_type = self._infer_site_type(url, soup)
            
            # 4. 컨텐츠 구조 분석
            content_structure = await self._analyze_content_structure(soup, url)
            
            # 5. 데이터 패턴 식별
            data_patterns = await self._identify_data_patterns(soup, site_type)
            
            # 6. AI 모델로 선택자 생성
            recommended_selectors = await self._generate_ai_selectors(html_content, url, site_type)
            
            # 7. 페이지네이션 분석
            pagination_info = await self._analyze_pagination(soup, url)
            
            # 8. 신뢰도 계산
            confidence_score = self._calculate_analysis_confidence(
                content_structure, data_patterns, recommended_selectors
            )
            
            result = SiteAnalysisResult(
                site_url=url,
                site_title=site_title,
                site_type=site_type,
                content_structure=content_structure,
                data_patterns=data_patterns,
                recommended_selectors=recommended_selectors,
                pagination_info=pagination_info,
                confidence_score=confidence_score
            )
            
            logger.info(f"✅ 사이트 분석 완료: {url} (신뢰도: {confidence_score:.1%})")
            return result
            
        except Exception as e:
            logger.error(f"❌ 사이트 분석 실패 {url}: {str(e)}")
            # 기본 분석 결과 반환
            return SiteAnalysisResult(
                site_url=url,
                confidence_score=0.0,
                content_structure={"error": str(e)}
            )
    
    async def generate_collection_strategy(
        self, 
        analysis_result: SiteAnalysisResult,
        target_data_types: List[str] = None
    ) -> CollectionStrategy:
        """📋 분석 결과를 바탕으로 수집 전략 생성"""
        
        if target_data_types is None:
            target_data_types = ["title", "agency", "category", "date", "url"]
        
        logger.info(f"📋 수집 전략 생성: {analysis_result.site_url}")
        
        try:
            # 1. 기본 선택자 맵핑
            selectors = self._map_target_selectors(
                analysis_result.recommended_selectors, 
                target_data_types
            )
            
            # 2. 페이지네이션 전략
            pagination = self._create_pagination_strategy(analysis_result.pagination_info)
            
            # 3. 추출 규칙 생성
            extraction_rules = self._create_extraction_rules(
                analysis_result.data_patterns,
                target_data_types
            )
            
            # 4. 성능 최적화 설정
            performance_config = self._optimize_performance_config(analysis_result.site_type)
            
            # 5. 신뢰도 등급 결정
            confidence = self._determine_confidence_level(analysis_result.confidence_score)
            
            # 6. 전략 ID 생성
            strategy_id = self._generate_strategy_id(analysis_result.site_url)
            site_id = self._extract_site_id(analysis_result.site_url)
            
            strategy = CollectionStrategy(
                strategy_id=strategy_id,
                site_id=site_id,
                site_url=analysis_result.site_url,
                selectors=selectors,
                pagination=pagination,
                extraction_rules=extraction_rules,
                performance_config=performance_config,
                confidence=confidence
            )
            
            logger.info(f"✅ 전략 생성 완료: {strategy_id} (신뢰도: {confidence.value})")
            return strategy
            
        except Exception as e:
            logger.error(f"❌ 전략 생성 실패: {str(e)}")
            # 기본 전략 반환
            return CollectionStrategy(
                strategy_id=f"fallback_{int(datetime.now().timestamp())}",
                site_id=self._extract_site_id(analysis_result.site_url),
                site_url=analysis_result.site_url,
                confidence=StrategyConfidence.UNCERTAIN
            )
    
    async def _fetch_page_content(self, url: str) -> str:
        """페이지 컨텐츠 가져오기"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"HTTP {response.status}: {url}")
                    return ""
        except Exception as e:
            logger.error(f"페이지 가져오기 실패 {url}: {str(e)}")
            return ""
    
    def _extract_site_title(self, soup: BeautifulSoup) -> str:
        """사이트 제목 추출"""
        title_element = soup.find('title')
        if title_element:
            return title_element.get_text(strip=True)
        
        # 대안 제목 추출
        for selector in ['h1', '.site-title', '.logo', '.brand']:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Unknown Site"
    
    def _infer_site_type(self, url: str, soup: BeautifulSoup) -> str:
        """사이트 타입 추론"""
        url_lower = url.lower()
        page_text = soup.get_text().lower()
        
        # 정부 포털 패턴
        if ('go.kr' in url_lower or 
            any(keyword in page_text for keyword in ['정부', '공고', '지원사업', '신청기간'])):
            return "government_portal"
        
        # 뉴스 사이트 패턴
        if (any(keyword in url_lower for keyword in ['news', 'press']) or
            any(keyword in page_text for keyword in ['뉴스', '기사', '보도자료'])):
            return "news_board"
        
        # 일반 게시판 패턴
        if soup.find('table') or soup.select('.board-list, .list-board'):
            return "bulletin_board"
        
        # 목록형 사이트
        if soup.select('ul li, ol li') and len(soup.select('ul li, ol li')) > 10:
            return "listing_site"
        
        return "unknown"
    
    async def _analyze_content_structure(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """컨텐츠 구조 분석"""
        structure = {}
        
        # 테이블 구조 분석
        tables = soup.find_all('table')
        if tables:
            structure['has_tables'] = True
            structure['table_count'] = len(tables)
            structure['main_table_headers'] = []
            
            # 메인 테이블의 헤더 추출
            main_table = max(tables, key=lambda t: len(t.find_all('tr')))
            headers = main_table.find_all(['th', 'td'])[:5]  # 첫 5개 헤더만
            structure['main_table_headers'] = [h.get_text(strip=True) for h in headers]
        
        # 리스트 구조 분석
        lists = soup.select('ul, ol')
        if lists:
            structure['has_lists'] = True
            structure['list_count'] = len(lists)
            
            # 가장 긴 리스트 분석
            longest_list = max(lists, key=lambda l: len(l.find_all('li')))
            structure['max_list_items'] = len(longest_list.find_all('li'))
        
        # 카드/아이템 구조 분석
        item_selectors = ['.item', '.card', '.post', '.entry', '.program']
        for selector in item_selectors:
            items = soup.select(selector)
            if items and len(items) >= 3:  # 최소 3개 이상
                structure['has_items'] = True
                structure['item_selector'] = selector
                structure['item_count'] = len(items)
                break
        
        # 폼 구조 분석
        forms = soup.find_all('form')
        if forms:
            structure['has_forms'] = True
            structure['form_count'] = len(forms)
        
        return structure
    
    async def _identify_data_patterns(self, soup: BeautifulSoup, site_type: str) -> List[Dict]:
        """데이터 패턴 식별"""
        patterns = []
        
        # 사이트 타입별 패턴 식별
        if site_type == "government_portal":
            patterns.extend(self._identify_government_patterns(soup))
        elif site_type == "news_board":
            patterns.extend(self._identify_news_patterns(soup))
        elif site_type == "bulletin_board":
            patterns.extend(self._identify_board_patterns(soup))
        
        # 공통 패턴 식별
        patterns.extend(self._identify_common_patterns(soup))
        
        return patterns
    
    def _identify_government_patterns(self, soup: BeautifulSoup) -> List[Dict]:
        """정부 포털 패턴 식별"""
        patterns = []
        
        # 공고 제목 패턴
        title_patterns = []
        for selector in ['.title a', '.subject a', 'td:first-child a']:
            elements = soup.select(selector)
            if len(elements) >= 3:
                sample_texts = [e.get_text(strip=True) for e in elements[:3]]
                if any('지원' in text or '사업' in text or '공고' in text for text in sample_texts):
                    title_patterns.append({
                        'selector': selector,
                        'sample_count': len(elements),
                        'confidence': 0.8,
                        'samples': sample_texts
                    })
        
        if title_patterns:
            patterns.append({
                'type': 'government_titles',
                'patterns': title_patterns
            })
        
        # 기관명 패턴
        agency_patterns = []
        for selector in ['.agency', '.organ', '.institution', 'td:nth-child(3)']:
            elements = soup.select(selector)
            if len(elements) >= 3:
                sample_texts = [e.get_text(strip=True) for e in elements[:3]]
                if any('부' in text or '청' in text or '원' in text for text in sample_texts):
                    agency_patterns.append({
                        'selector': selector,
                        'sample_count': len(elements),
                        'confidence': 0.7,
                        'samples': sample_texts
                    })
        
        if agency_patterns:
            patterns.append({
                'type': 'government_agencies',
                'patterns': agency_patterns
            })
        
        return patterns
    
    def _identify_news_patterns(self, soup: BeautifulSoup) -> List[Dict]:
        """뉴스 사이트 패턴 식별"""
        patterns = []
        
        # 뉴스 헤드라인 패턴 (구현 필요)
        # 날짜 패턴 (구현 필요)
        
        return patterns
    
    def _identify_board_patterns(self, soup: BeautifulSoup) -> List[Dict]:
        """게시판 패턴 식별"""
        patterns = []
        
        # 게시판 특화 패턴 (구현 필요)
        
        return patterns
    
    def _identify_common_patterns(self, soup: BeautifulSoup) -> List[Dict]:
        """공통 패턴 식별"""
        patterns = []
        
        # 링크 패턴
        links = soup.find_all('a', href=True)
        if len(links) >= 5:
            patterns.append({
                'type': 'links',
                'count': len(links),
                'internal_links': len([l for l in links if not l['href'].startswith('http')]),
                'external_links': len([l for l in links if l['href'].startswith('http')])
            })
        
        # 날짜 패턴
        date_patterns = re.findall(r'\d{4}[-/.]\d{1,2}[-/.]\d{1,2}', soup.get_text())
        if date_patterns:
            patterns.append({
                'type': 'dates',
                'count': len(date_patterns),
                'samples': date_patterns[:3]
            })
        
        return patterns
    
    async def _generate_ai_selectors(self, html_content: str, url: str, site_type: str) -> Dict[str, str]:
        """AI 모델을 사용하여 선택자 생성"""
        try:
            # HTML을 분석 가능한 크기로 축약
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 불필요한 스크립트/스타일 제거
            for tag in soup(['script', 'style', 'meta', 'link']):
                tag.decompose()
            
            # 주요 컨텐츠 영역만 추출 (처음 5000자)
            clean_html = str(soup)[:5000]
            
            # AI 프롬프트 생성
            prompt = self._create_selector_prompt(clean_html, url, site_type)
            
            # AI 모델 호출 (실제 API 호출 시뮬레이션)
            ai_response = await self._call_ai_model(prompt)
            
            # AI 응답 파싱
            selectors = self._parse_ai_selector_response(ai_response)
            
            logger.info(f"AI 선택자 생성 완료: {len(selectors)}개 선택자")
            return selectors
            
        except Exception as e:
            logger.error(f"AI 선택자 생성 실패: {str(e)}")
            # 기본 선택자 반환
            return self._get_fallback_selectors(site_type)
    
    def _create_selector_prompt(self, html_content: str, url: str, site_type: str) -> str:
        """AI 모델용 선택자 생성 프롬프트"""
        return f"""
웹페이지 구조 분석 및 데이터 추출 선택자 생성 요청

URL: {url}
사이트 타입: {site_type}

HTML 구조:
```html
{html_content}
```

요청사항:
1. 이 웹페이지에서 반복적으로 나타나는 데이터 항목들을 식별
2. 다음 정보를 추출할 수 있는 CSS 선택자를 생성:
   - title: 제목/헤드라인
   - agency: 기관명/발행처
   - category: 카테고리/분류
   - date: 날짜/시간
   - url: 상세 페이지 링크
   - content: 내용/요약

3. 각 선택자는 가능한 한 구체적이고 안정적이어야 함
4. 여러 개의 대안 선택자를 제시 (우선순위 순)

응답 형식 (JSON):
{{
    "title": ["selector1", "selector2", "selector3"],
    "agency": ["selector1", "selector2"],
    "category": ["selector1"],
    "date": ["selector1", "selector2"],
    "url": ["selector1"],
    "content": ["selector1"],
    "container": ["selector1", "selector2"],
    "confidence": 0.85,
    "notes": "분석 참고사항"
}}
"""
    
    async def _call_ai_model(self, prompt: str, model_preference: str = "primary") -> str:
        """🤖 AI 모델 API 호출 (Gemini Flash 2.0 우선, 폴백 지원)"""
        
        # 모델 우선순위 설정
        models_to_try = []
        if model_preference == "primary":
            models_to_try = ["primary", "fallback", "local"]
        elif model_preference == "fallback":
            models_to_try = ["fallback", "local"]
        else:
            models_to_try = ["local"]
        
        last_error = None
        
        for model_key in models_to_try:
            try:
                model_config = self.ai_models[model_key]
                logger.info(f"🤖 AI 모델 시도: {model_config['name']} ({model_config['provider']})")
                
                if model_config["provider"] == "google":
                    return await self._call_gemini_model(prompt, model_config)
                elif model_config["provider"] == "anthropic":
                    return await self._call_claude_model(prompt, model_config)
                elif model_config["provider"] == "local":
                    return await self._call_local_pattern_model(prompt)
                    
            except Exception as e:
                last_error = e
                logger.warning(f"❌ {model_config['name']} 모델 실패: {str(e)}")
                continue
        
        # 모든 모델 실패 시 예외 발생
        raise Exception(f"모든 AI 모델 호출 실패. 마지막 오류: {last_error}")
    
    async def _call_gemini_model(self, prompt: str, model_config: Dict) -> str:
        """🚀 Gemini Flash 2.0 API 호출"""
        try:
            # Gemini API 엔드포인트
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_config['name']}:generateContent"
            
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": model_config["api_key"]
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": model_config["temperature"],
                    "maxOutputTokens": model_config["max_tokens"],
                    "candidateCount": 1
                }
            }
            
            async with self.session.post(api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Gemini 응답 구조에서 텍스트 추출
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            text_content = candidate["content"]["parts"][0].get("text", "")
                            logger.info("✅ Gemini Flash 2.0 응답 성공")
                            return text_content
                    
                    raise Exception("Gemini 응답 구조 파싱 실패")
                else:
                    error_text = await response.text()
                    raise Exception(f"Gemini API 오류 {response.status}: {error_text}")
                    
        except Exception as e:
            logger.error(f"❌ Gemini API 호출 실패: {str(e)}")
            raise
    
    async def _call_claude_model(self, prompt: str, model_config: Dict) -> str:
        """🔄 Claude API 호출 (폴백)"""
        try:
            # Claude API 엔드포인트
            api_url = "https://api.anthropic.com/v1/messages"
            
            headers = {
                "Content-Type": "application/json",
                "x-api-key": model_config["api_key"],
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": model_config["name"],
                "max_tokens": model_config["max_tokens"],
                "temperature": model_config["temperature"],
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            }
            
            async with self.session.post(api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Claude 응답 구조에서 텍스트 추출
                    if "content" in result and len(result["content"]) > 0:
                        text_content = result["content"][0].get("text", "")
                        logger.info("✅ Claude API 응답 성공 (폴백)")
                        return text_content
                    
                    raise Exception("Claude 응답 구조 파싱 실패")
                else:
                    error_text = await response.text()
                    raise Exception(f"Claude API 오류 {response.status}: {error_text}")
                    
        except Exception as e:
            logger.error(f"❌ Claude API 호출 실패: {str(e)}")
            raise
    
    async def _call_local_pattern_model(self, prompt: str) -> str:
        """🏠 로컬 패턴 기반 모델 (최종 폴백)"""
        logger.info("🏠 로컬 패턴 기반 분석 실행")
        
        # 간단한 패턴 기반 응답 생성
        # 실제로는 HTML 구조를 분석하여 패턴 매칭
        local_response = {
            "title": [".title a", ".subject a", "td:first-child a", "h1 a", "h2 a"],
            "agency": [".agency", ".organ", ".institution", ".publisher", ".author"],
            "category": [".category", ".type", ".분류", ".classification"],
            "date": [".date", ".regDate", ".등록일", ".created", ".published"],
            "url": [".title a", ".subject a", "a[href*='view']"],
            "content": [".content", ".summary", ".요약", ".description"],
            "container": ["table tbody tr", ".list-item", ".board-item", "li", ".item"],
            "confidence": 0.60,
            "notes": "로컬 패턴 기반 분석 결과 (폴백 모드)"
        }
        
        return json.dumps(local_response, ensure_ascii=False)
    
    def _parse_ai_selector_response(self, ai_response: str) -> Dict[str, str]:
        """AI 응답에서 선택자 파싱"""
        try:
            data = json.loads(ai_response)
            
            # 각 필드의 첫 번째 선택자를 기본으로 사용
            selectors = {}
            for field, selector_list in data.items():
                if field not in ['confidence', 'notes'] and isinstance(selector_list, list):
                    selectors[field] = selector_list[0] if selector_list else ""
            
            return selectors
            
        except Exception as e:
            logger.error(f"AI 응답 파싱 실패: {str(e)}")
            return {}
    
    def _get_fallback_selectors(self, site_type: str) -> Dict[str, str]:
        """기본 선택자 반환"""
        if site_type == "government_portal":
            return {
                "title": ".title a",
                "agency": ".agency",
                "category": ".category",
                "date": ".date",
                "url": ".title a",
                "container": "table tbody tr"
            }
        else:
            return {
                "title": "a",
                "container": "li, tr"
            }
    
    async def _analyze_pagination(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """페이지네이션 분석"""
        pagination_info = {
            "has_pagination": False,
            "method": "none",
            "selectors": {},
            "max_pages": 1
        }
        
        # 페이지 번호 링크 찾기
        page_links = soup.select('a[href*="page"], a[href*="pageNum"], a[href*="currentPage"]')
        if page_links:
            pagination_info["has_pagination"] = True
            pagination_info["method"] = "link_based"
            pagination_info["selectors"]["next_page"] = "a:contains('다음'), a:contains('Next'), a:contains('>')"
            
            # 최대 페이지 수 추정
            try:
                page_numbers = []
                for link in page_links:
                    text = link.get_text(strip=True)
                    if text.isdigit():
                        page_numbers.append(int(text))
                
                if page_numbers:
                    pagination_info["max_pages"] = max(page_numbers)
            except:
                pass
        
        # 버튼 기반 페이지네이션
        next_buttons = soup.select('button:contains("다음"), input[value*="다음"], .next, .page-next')
        if next_buttons and not page_links:
            pagination_info["has_pagination"] = True
            pagination_info["method"] = "button_based"
            pagination_info["selectors"]["next_button"] = ".next, .page-next, button:contains('다음')"
        
        return pagination_info
    
    def _calculate_analysis_confidence(
        self, 
        content_structure: Dict, 
        data_patterns: List[Dict], 
        selectors: Dict[str, str]
    ) -> float:
        """분석 신뢰도 계산"""
        confidence = 0.0
        
        # 컨텐츠 구조 점수 (40%)
        structure_score = 0.0
        if content_structure.get('has_tables'):
            structure_score += 0.3
        if content_structure.get('has_lists'):
            structure_score += 0.2
        if content_structure.get('has_items'):
            structure_score += 0.3
        
        # 데이터 패턴 점수 (30%)
        pattern_score = min(len(data_patterns) * 0.1, 0.3)
        
        # 선택자 품질 점수 (30%)
        selector_score = min(len(selectors) * 0.05, 0.3)
        
        confidence = structure_score + pattern_score + selector_score
        return min(confidence, 1.0)
    
    # 전략 생성 관련 메소드들
    
    def _map_target_selectors(self, ai_selectors: Dict[str, str], target_types: List[str]) -> Dict[str, str]:
        """목표 데이터 타입에 맞는 선택자 매핑"""
        mapped = {}
        for target in target_types:
            if target in ai_selectors:
                mapped[target] = ai_selectors[target]
        return mapped
    
    def _create_pagination_strategy(self, pagination_info: Dict[str, Any]) -> Dict[str, Any]:
        """페이지네이션 전략 생성"""
        if not pagination_info.get('has_pagination'):
            return {"enabled": False}
        
        return {
            "enabled": True,
            "method": pagination_info.get('method', 'link_based'),
            "selectors": pagination_info.get('selectors', {}),
            "max_pages": pagination_info.get('max_pages', 10),
            "delay_between_pages": 3.0
        }
    
    def _create_extraction_rules(self, data_patterns: List[Dict], target_types: List[str]) -> Dict[str, Any]:
        """데이터 추출 규칙 생성"""
        rules = {
            "text_cleaning": {
                "strip_whitespace": True,
                "remove_newlines": True,
                "normalize_spaces": True
            },
            "validation": {
                "min_title_length": 5,
                "max_title_length": 200,
                "required_fields": ["title"]
            },
            "post_processing": {
                "url_resolution": "absolute",
                "date_parsing": "auto",
                "text_encoding": "utf-8"
            }
        }
        
        return rules
    
    def _optimize_performance_config(self, site_type: str) -> Dict[str, Any]:
        """사이트 타입별 성능 최적화 설정"""
        base_config = {
            "delay_between_requests": 2.0,
            "max_concurrent": 3,
            "timeout": 30,
            "max_retries": 2
        }
        
        # 정부 사이트는 더 보수적으로
        if site_type == "government_portal":
            base_config["delay_between_requests"] = 3.0
            base_config["max_concurrent"] = 2
        
        return base_config
    
    def _determine_confidence_level(self, confidence_score: float) -> StrategyConfidence:
        """신뢰도 점수를 등급으로 변환"""
        if confidence_score >= 0.95:
            return StrategyConfidence.HIGH
        elif confidence_score >= 0.80:
            return StrategyConfidence.MEDIUM
        elif confidence_score >= 0.60:
            return StrategyConfidence.LOW
        else:
            return StrategyConfidence.UNCERTAIN
    
    def _generate_strategy_id(self, url: str) -> str:
        """전략 ID 생성"""
        import hashlib
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        timestamp = int(datetime.now().timestamp())
        return f"strategy_{url_hash}_{timestamp}"
    
    def _extract_site_id(self, url: str) -> str:
        """URL에서 사이트 ID 추출"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 서브도메인 제거
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            return '_'.join(domain_parts[-2:]).replace('.', '_')
        
        return domain.replace('.', '_')
    
    # 프롬프트 템플릿 메소드들
    
    def _get_structure_analysis_prompt(self) -> str:
        """구조 분석용 프롬프트 템플릿"""
        return """
웹페이지의 HTML 구조를 분석하여 다음 정보를 제공해주세요:

1. 주요 컨텐츠 영역 식별
2. 데이터 리스트 구조 (테이블, 목록, 카드 등)
3. 반복되는 아이템 패턴
4. 네비게이션 및 페이지네이션 구조

분석 대상 HTML:
{html_content}

응답은 구조화된 JSON 형태로 제공해주세요.
"""
    
    def _get_selector_generation_prompt(self) -> str:
        """선택자 생성용 프롬프트 템플릿"""
        return """
제공된 HTML 구조를 분석하여 데이터 추출을 위한 최적의 CSS 선택자를 생성해주세요.

목표 데이터:
- 제목/헤드라인
- 기관명/발행처  
- 카테고리/분류
- 날짜
- 링크 URL
- 내용/요약

각 선택자는 안정적이고 구체적이어야 하며, 사이트 변경에 대한 내성이 있어야 합니다.
"""
    
    def _get_pagination_analysis_prompt(self) -> str:
        """페이지네이션 분석용 프롬프트 템플릿"""
        return """
웹페이지의 페이지네이션 구조를 분석하여 다음 정보를 제공해주세요:

1. 페이지네이션 존재 여부
2. 페이지네이션 방식 (링크, 버튼, AJAX 등)
3. 다음 페이지 이동 방법
4. 전체 페이지 수 (추정 가능한 경우)

분석 결과를 JSON 형태로 제공해주세요.
"""


# 유틸리티 함수들

def create_ai_research_engine(ai_api_key: str = None) -> AIResearchEngine:
    """AI 연구 엔진 생성 및 초기화"""
    engine = AIResearchEngine(ai_api_key)
    return engine


async def analyze_site_and_generate_strategy(
    url: str, 
    target_data_types: List[str] = None,
    ai_api_key: str = None
) -> Tuple[SiteAnalysisResult, CollectionStrategy]:
    """사이트 분석 및 전략 생성 원스톱 함수"""
    engine = create_ai_research_engine(ai_api_key)
    
    try:
        await engine.initialize()
        
        # 1. 사이트 분석
        analysis_result = await engine.analyze_website_structure(url)
        
        # 2. 전략 생성
        strategy = await engine.generate_collection_strategy(analysis_result, target_data_types)
        
        return analysis_result, strategy
        
    finally:
        await engine.close()


# 테스트 실행 함수
async def test_ai_research_engine():
    """AI 연구 엔진 테스트"""
    test_urls = [
        "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/list.do",
        "https://www.k-startup.go.kr/web/contents/bizListPage.do"
    ]
    
    for url in test_urls:
        logger.info(f"🧪 테스트 시작: {url}")
        
        try:
            analysis, strategy = await analyze_site_and_generate_strategy(url)
            
            logger.info(f"✅ 분석 완료")
            logger.info(f"   - 사이트 타입: {analysis.site_type}")
            logger.info(f"   - 신뢰도: {analysis.confidence_score:.1%}")
            logger.info(f"   - 추천 선택자: {len(analysis.recommended_selectors)}개")
            logger.info(f"   - 전략 신뢰도: {strategy.confidence.value}")
            
        except Exception as e:
            logger.error(f"❌ 테스트 실패: {str(e)}")


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 테스트 실행
    asyncio.run(test_ai_research_engine())