#!/usr/bin/env python3
"""
🤖 AI 기반 꿈풀이 키워드 생성 및 품질 검증 시스템
- OpenAI GPT-4, Anthropic Claude, Google Gemini 통합
- 한국 전통 꿈해몽 전문 지식 활용
- 자동 품질 검증 및 중복 제거
- 다중 해석 생성 (전통/현대/심리학적)
"""

import os
import json
import logging
import asyncio
import aiohttp
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import time
import random
from datetime import datetime
import subprocess
import re

@dataclass
class AIKeywordRequest:
    """AI 키워드 생성 요청"""
    category: str
    base_keywords: List[str]
    count: int
    style: str = "traditional"  # traditional, modern, creative
    quality_threshold: float = 8.0

@dataclass
class GeneratedKeyword:
    """생성된 키워드"""
    keyword: str
    category: str
    traditional_interpretation: str
    modern_interpretation: str
    psychological_interpretation: Optional[str] = None
    related_keywords: List[str] = None
    quality_score: float = 8.0
    confidence: float = 0.8
    source: str = "ai"

class AIKeywordGenerator:
    """AI 기반 키워드 생성기"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.ai_clients = self._initialize_ai_clients()
        self.korean_dream_context = self._load_korean_dream_context()
        
    def _setup_logger(self):
        """로거 설정"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('/home/ubuntu/logs/ai_keyword_generator.log')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
        
        return logger
    
    def _initialize_ai_clients(self) -> Dict:
        """AI 클라이언트 초기화"""
        clients = {}
        
        # API 키 로드
        env_path = "/home/ubuntu/.env.ai"
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # OpenAI 클라이언트
        if os.getenv('OPENAI_API_KEY'):
            clients['openai'] = {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': 'gpt-4',
                'endpoint': 'https://api.openai.com/v1/chat/completions'
            }
            self.logger.info("✅ OpenAI 클라이언트 초기화 완료")
        
        # Anthropic Claude 클라이언트  
        if os.getenv('ANTHROPIC_API_KEY'):
            clients['anthropic'] = {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'model': 'claude-3-sonnet-20240229',
                'endpoint': 'https://api.anthropic.com/v1/messages'
            }
            self.logger.info("✅ Anthropic 클라이언트 초기화 완료")
        
        # Google Gemini 클라이언트
        if os.getenv('GEMINI_API_KEY'):
            clients['gemini'] = {
                'api_key': os.getenv('GEMINI_API_KEY'),
                'model': 'gemini-pro',
                'endpoint': f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
            }
            self.logger.info("✅ Gemini 클라이언트 초기화 완료")
        
        if not clients:
            self.logger.error("❌ AI API 키가 설정되지 않았습니다.")
        
        return clients
    
    def _load_korean_dream_context(self) -> str:
        """한국 전통 꿈풀이 컨텍스트 로드"""
        return """
        당신은 한국 전통 꿈해몽 전문가입니다. 다음 지식을 바탕으로 키워드를 생성해주세요:

        ## 한국 전통 꿈풀이 원리
        1. 꿈은 현실의 반대: 좋은 꿈이 나쁜 결과를, 나쁜 꿈이 좋은 결과를 가져옴
        2. 상징과 은유: 직접적 표현보다 상징적 의미가 중요
        3. 음양오행 사상: 물(水), 불(火), 나무(木), 금(金), 흙(土)의 조화
        4. 십이지신: 쥐, 소, 호랑이, 토끼, 용, 뱀, 말, 양, 원숭이, 닭, 개, 돼지

        ## 꿈풀이 해석 방식
        - 전통적 해석: 조상 대대로 전해오는 민속 지혜
        - 현대적 해석: 심리학적, 과학적 관점
        - 상황별 해석: 같은 꿈이라도 꿈꾸는 사람의 상황에 따라 달라짐

        ## 키워드 생성 규칙
        1. 한국어 고유 표현 우선 사용
        2. 일상생활에서 자주 꿈꾸는 내용 포함
        3. 문화적 특수성 반영 (제사, 차례, 효도 등)
        4. 계절감과 절기 고려 (봄꿈, 가을꿈 등)
        """
    
    async def generate_keywords_with_ai(self, request: AIKeywordRequest) -> List[GeneratedKeyword]:
        """AI를 활용한 키워드 생성"""
        results = []
        
        # 여러 AI 모델에서 키워드 생성
        for ai_name, client_info in self.ai_clients.items():
            try:
                keywords = await self._generate_with_specific_ai(ai_name, request)
                results.extend(keywords)
                self.logger.info(f"✅ {ai_name}에서 {len(keywords)}개 키워드 생성")
            except Exception as e:
                self.logger.error(f"❌ {ai_name} 키워드 생성 실패: {e}")
        
        # 품질 검증 및 중복 제거
        validated_keywords = self._validate_and_deduplicate(results, request.quality_threshold)
        
        return validated_keywords[:request.count]
    
    async def _generate_with_specific_ai(self, ai_name: str, request: AIKeywordRequest) -> List[GeneratedKeyword]:
        """특정 AI로 키워드 생성"""
        prompt = self._create_prompt(request)
        
        if ai_name == 'openai':
            return await self._generate_with_openai(prompt, request)
        elif ai_name == 'anthropic':
            return await self._generate_with_anthropic(prompt, request)
        elif ai_name == 'gemini':
            return await self._generate_with_gemini(prompt, request)
        else:
            return []
    
    def _create_prompt(self, request: AIKeywordRequest) -> str:
        """AI용 프롬프트 생성"""
        base_keywords_str = ", ".join(request.base_keywords)
        
        return f"""
        {self.korean_dream_context}

        ## 요청 사항
        카테고리: {request.category}
        기존 키워드: {base_keywords_str}
        생성 개수: {request.count}
        스타일: {request.style}

        ## 출력 형식 (JSON)
        다음 JSON 형식으로 {request.count}개의 새로운 꿈풀이 키워드를 생성해주세요:

        {{
            "keywords": [
                {{
                    "keyword": "생성된 키워드",
                    "traditional_interpretation": "전통적 해석 (2-3문장)",
                    "modern_interpretation": "현대적 해석 (2-3문장)",
                    "psychological_interpretation": "심리학적 해석 (1-2문장, 선택적)",
                    "related_keywords": ["관련키워드1", "관련키워드2", "관련키워드3"],
                    "quality_score": 8.5
                }}
            ]
        }}

        ## 생성 조건
        1. 기존 키워드와 중복되지 않는 새로운 키워드 생성
        2. 한국 문화와 전통에 맞는 자연스러운 표현 사용
        3. 실제로 사람들이 꿈꿀 수 있는 현실적인 내용
        4. 전통적 해석과 현대적 해석의 균형 유지
        5. 품질 점수 8.0 이상의 고품질 키워드
        """
    
    async def _generate_with_openai(self, prompt: str, request: AIKeywordRequest) -> List[GeneratedKeyword]:
        """OpenAI GPT-4로 키워드 생성"""
        client_info = self.ai_clients['openai']
        
        payload = {
            "model": client_info['model'],
            "messages": [
                {"role": "system", "content": "당신은 한국 전통 꿈해몽 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 2000
        }
        
        headers = {
            "Authorization": f"Bearer {client_info['api_key']}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(client_info['endpoint'], 
                                   json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    return self._parse_ai_response(content, request.category, 'openai')
                else:
                    raise Exception(f"OpenAI API 오류: {response.status}")
    
    async def _generate_with_anthropic(self, prompt: str, request: AIKeywordRequest) -> List[GeneratedKeyword]:
        """Anthropic Claude로 키워드 생성"""
        client_info = self.ai_clients['anthropic']
        
        payload = {
            "model": client_info['model'],
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        headers = {
            "x-api-key": client_info['api_key'],
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(client_info['endpoint'], 
                                   json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['content'][0]['text']
                    return self._parse_ai_response(content, request.category, 'anthropic')
                else:
                    raise Exception(f"Anthropic API 오류: {response.status}")
    
    async def _generate_with_gemini(self, prompt: str, request: AIKeywordRequest) -> List[GeneratedKeyword]:
        """Google Gemini로 키워드 생성"""
        client_info = self.ai_clients['gemini']
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        params = {"key": client_info['api_key']}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(client_info['endpoint'], 
                                   json=payload, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['candidates'][0]['content']['parts'][0]['text']
                    return self._parse_ai_response(content, request.category, 'gemini')
                else:
                    raise Exception(f"Gemini API 오류: {response.status}")
    
    def _parse_ai_response(self, content: str, category: str, source: str) -> List[GeneratedKeyword]:
        """AI 응답 파싱"""
        keywords = []
        
        try:
            # JSON 추출
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # JSON 마커가 없으면 전체 내용에서 JSON 찾기
                json_str = content
            
            # JSON 파싱
            data = json.loads(json_str)
            
            for item in data.get('keywords', []):
                keyword = GeneratedKeyword(
                    keyword=item['keyword'],
                    category=category,
                    traditional_interpretation=item['traditional_interpretation'],
                    modern_interpretation=item['modern_interpretation'],
                    psychological_interpretation=item.get('psychological_interpretation'),
                    related_keywords=item.get('related_keywords', []),
                    quality_score=item.get('quality_score', 8.0),
                    source=source
                )
                keywords.append(keyword)
                
        except Exception as e:
            self.logger.error(f"AI 응답 파싱 오류 ({source}): {e}")
            self.logger.debug(f"응답 내용: {content[:500]}...")
        
        return keywords
    
    def _validate_and_deduplicate(self, keywords: List[GeneratedKeyword], 
                                 quality_threshold: float) -> List[GeneratedKeyword]:
        """품질 검증 및 중복 제거"""
        validated = []
        seen_keywords = set()
        
        for keyword in keywords:
            # 품질 점수 검증
            if keyword.quality_score < quality_threshold:
                continue
            
            # 중복 제거
            normalized_keyword = keyword.keyword.strip().lower()
            if normalized_keyword in seen_keywords:
                continue
            
            # 키워드 유효성 검증
            if not self._is_valid_korean_keyword(keyword.keyword):
                continue
            
            # 해석 품질 검증
            if not self._validate_interpretations(keyword):
                continue
            
            seen_keywords.add(normalized_keyword)
            validated.append(keyword)
        
        # 품질 점수순 정렬
        validated.sort(key=lambda x: x.quality_score, reverse=True)
        
        self.logger.info(f"품질 검증 완료: {len(keywords)}개 → {len(validated)}개")
        return validated
    
    def _is_valid_korean_keyword(self, keyword: str) -> bool:
        """한국어 키워드 유효성 검증"""
        if not keyword or len(keyword) < 2 or len(keyword) > 20:
            return False
        
        # 한글 포함 여부 확인
        korean_pattern = re.compile(r'[가-힣]')
        if not korean_pattern.search(keyword):
            return False
        
        # 부적절한 문자 제외
        invalid_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
        if any(char in keyword for char in invalid_chars):
            return False
        
        return True
    
    def _validate_interpretations(self, keyword: GeneratedKeyword) -> bool:
        """해석 품질 검증"""
        # 해석 길이 검증
        if len(keyword.traditional_interpretation) < 10:
            return False
        if len(keyword.modern_interpretation) < 10:
            return False
        
        # 해석 내용 검증 (기본적인 품질 체크)
        required_words = ['꿈', '의미', '상징', '나타']
        traditional_check = any(word in keyword.traditional_interpretation for word in required_words)
        modern_check = any(word in keyword.modern_interpretation for word in required_words)
        
        return traditional_check and modern_check
    
    async def batch_generate_keywords(self, requests: List[AIKeywordRequest]) -> Dict[str, List[GeneratedKeyword]]:
        """배치 키워드 생성"""
        results = {}
        
        for request in requests:
            self.logger.info(f"🤖 {request.category} 카테고리 AI 키워드 생성 시작 ({request.count}개)")
            keywords = await self.generate_keywords_with_ai(request)
            results[request.category] = keywords
            
            # API 호출 제한 고려 (1초 대기)
            await asyncio.sleep(1)
        
        return results
    
    def save_generated_keywords_to_db(self, keywords: List[GeneratedKeyword]) -> int:
        """생성된 키워드를 데이터베이스에 저장"""
        saved_count = 0
        
        for keyword in keywords:
            try:
                # 키워드 삽입
                insert_cmd = [
                    'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                    f"""
                    INSERT INTO dream_keywords 
                    (keyword, keyword_normalized, category_id, quality_score, status)
                    VALUES ('{keyword.keyword.replace("'", "''")}', 
                            '{keyword.keyword.lower().replace("'", "''")}', 
                            '{keyword.category}', {keyword.quality_score}, 'active')
                    ON CONFLICT (keyword, category_id) DO NOTHING
                    RETURNING id;
                    """
                ]
                
                result = subprocess.run(insert_cmd, capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    keyword_id = result.stdout.strip()
                    
                    # 해석들 삽입
                    self._insert_interpretations(keyword_id, keyword)
                    saved_count += 1
                
            except Exception as e:
                self.logger.error(f"키워드 저장 오류: {keyword.keyword} - {e}")
        
        self.logger.info(f"✅ {saved_count}개 키워드 데이터베이스 저장 완료")
        return saved_count
    
    def _insert_interpretations(self, keyword_id: str, keyword: GeneratedKeyword):
        """해석 데이터 삽입"""
        interpretations = [
            ('traditional', keyword.traditional_interpretation, 'positive'),
            ('modern', keyword.modern_interpretation, 'neutral')
        ]
        
        if keyword.psychological_interpretation:
            interpretations.append(('psychological', keyword.psychological_interpretation, 'neutral'))
        
        for interp_type, text, sentiment in interpretations:
            cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                f"""
                INSERT INTO dream_interpretations 
                (keyword_id, interpretation_type, interpretation_text, sentiment, confidence_score)
                VALUES ({keyword_id}, '{interp_type}', '{text.replace("'", "''")}', 
                        '{sentiment}', {keyword.confidence});
                """
            ]
            subprocess.run(cmd, capture_output=True)

# 실행 함수
async def main():
    """메인 실행 함수"""
    generator = AIKeywordGenerator()
    
    if not generator.ai_clients:
        print("❌ AI API 키가 설정되지 않았습니다.")
        return
    
    # 샘플 요청 생성
    requests = [
        AIKeywordRequest(
            category='water',
            base_keywords=['물', '바다', '강'],
            count=20,
            style='traditional'
        ),
        AIKeywordRequest(
            category='zodiac_animals',
            base_keywords=['용', '호랑이', '뱀'],
            count=15,
            style='creative'
        )
    ]
    
    # AI 키워드 생성
    results = await generator.batch_generate_keywords(requests)
    
    # 결과 출력
    total_generated = 0
    for category, keywords in results.items():
        print(f"\n📂 {category} 카테고리: {len(keywords)}개 생성")
        total_generated += len(keywords)
        
        for keyword in keywords[:3]:  # 처음 3개만 샘플 출력
            print(f"  🔸 {keyword.keyword} (품질: {keyword.quality_score})")
    
    # 데이터베이스 저장
    all_keywords = []
    for keywords in results.values():
        all_keywords.extend(keywords)
    
    if all_keywords:
        saved_count = generator.save_generated_keywords_to_db(all_keywords)
        print(f"\n💾 데이터베이스 저장: {saved_count}/{len(all_keywords)}개 성공")

if __name__ == "__main__":
    asyncio.run(main())