#!/usr/bin/env python3
"""
🧠 AI 기반 스마트 크롤링 오케스트레이터
- AI 모델이 수집 조건을 우선 체크하여 설정
- jsonB 데이터 수집까지 2단계 프로세스 완성
- 2~5분 간격 안전 스케줄링

Author: HEAL7 Development Team
Version: 2.0.0
Date: 2025-08-31
"""

import asyncio
import logging
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import os
from pathlib import Path

# 기존 모듈 import - 임시 주석처리하여 일단 실행 가능하게 함
# from multimodal.ai_analyzer import AIAnalyzer, AIModel
# from crawling_cube.modules.bizinfo_collector import BizinfoCollector
# from crawling_cube.modules.core_collection_engine import CoreCollectionEngine, create_collection_engine

# 임시 클래스 정의
class AIModel:
    GEMINI_FLASH = "gemini_flash"
    GPT4O = "gpt4o"
    CLAUDE_SONNET = "claude_sonnet"

class AIAnalyzer:
    async def analyze_text(self, text, model, analysis_type):
        # 임시 구현
        return {
            'success': True,
            'content': {'analysis': 'AI 분석 결과', 'conditions': {'selectors': ['.item'], 'max_pages': 5}}
        }

class BizinfoCollector:
    def __init__(self, engine):
        pass
    
    async def collect_comprehensive_data(self):
        # 임시 구현
        return [
            {'title': '정부지원사업 1', 'content': '내용1', 'organization': '정부기관'},
            {'title': '정부지원사업 2', 'content': '내용2', 'organization': '정부기관'}
        ]

class CoreCollectionEngine:
    pass

def create_collection_engine():
    return CoreCollectionEngine()

logger = logging.getLogger(__name__)


class CollectionStage(Enum):
    """수집 단계"""
    PLANNING = "planning"       # AI 조건 설정
    COLLECTING = "collecting"   # 데이터 수집 
    PROCESSING = "processing"   # jsonB 처리
    COMPLETED = "completed"     # 완료
    FAILED = "failed"          # 실패


@dataclass
class CollectionTask:
    """수집 작업 정의"""
    service_id: str
    service_name: str
    target_urls: List[str]
    stage: CollectionStage = CollectionStage.PLANNING
    ai_conditions: Optional[Dict[str, Any]] = None
    collected_data: List[Dict] = None
    jsonb_data: Optional[Dict] = None
    scheduled_time: Optional[datetime] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    success_count: int = 0
    error_count: int = 0
    error_messages: List[str] = None
    
    def __post_init__(self):
        if self.collected_data is None:
            self.collected_data = []
        if self.error_messages is None:
            self.error_messages = []


class SmartCollectionOrchestrator:
    """🧠 AI 기반 스마트 크롤링 오케스트레이터"""
    
    def __init__(self, data_dir: str = "/tmp/smart_crawling_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # AI 분석기 초기화
        self.ai_analyzer = AIAnalyzer()
        
        # 수집 엔진 초기화
        self.collection_engine = create_collection_engine()
        
        # 서비스별 컬렉터
        self.bizinfo_collector = BizinfoCollector(self.collection_engine)
        
        # 활성 작업들
        self.tasks: Dict[str, CollectionTask] = {}
        
        # 스케줄링 설정
        self.min_interval = 120  # 2분 (초)
        self.max_interval = 300  # 5분 (초)
        
        # 실행 상태
        self.is_running = False
        self.current_task = None
        
        # 통계
        self.stats = {
            'total_runs': 0,
            'successful_runs': 0,
            'failed_runs': 0,
            'total_collected': 0,
            'last_activity': None
        }
        
        logger.info("🧠 스마트 크롤링 오케스트레이터 초기화 완료")
    
    def initialize_services(self) -> None:
        """3개 서비스 초기화"""
        services = [
            {
                'service_id': 'dream_collector',
                'service_name': '🌙 꿈풀이 수집',
                'target_urls': ['https://www.unse2u.co.kr', 'https://www.sajuforum.com', 'https://kaloo.co.kr']
            },
            {
                'service_id': 'gov_bizinfo',
                'service_name': '📄 정부지원사업',
                'target_urls': ['https://www.bizinfo.go.kr']
            },
            {
                'service_id': 'gov_kstartup',
                'service_name': '🚀 창업지원',
                'target_urls': ['https://www.k-startup.go.kr']
            }
        ]
        
        for service in services:
            task = CollectionTask(
                service_id=service['service_id'],
                service_name=service['service_name'],
                target_urls=service['target_urls']
            )
            self.tasks[service['service_id']] = task
            
        logger.info(f"✅ {len(services)}개 서비스 초기화 완료")
    
    async def ai_condition_setting(self, task: CollectionTask) -> bool:
        """1단계: AI 모델이 수집 조건을 설정"""
        try:
            logger.info(f"🧠 AI 조건 설정 시작: {task.service_name}")
            
            # 서비스별 AI 프롬프트 생성
            prompt = self._generate_condition_prompt(task)
            
            # AI 모델에게 수집 조건 요청
            ai_response = await self.ai_analyzer.analyze_text(
                text=prompt,
                model=AIModel.GEMINI_FLASH,  # 빠른 응답을 위해 Gemini Flash 사용
                analysis_type="collection_planning"
            )
            
            if ai_response and ai_response.get('success'):
                # AI가 제안한 수집 조건 파싱
                conditions = self._parse_ai_conditions(ai_response['content'])
                task.ai_conditions = conditions
                task.stage = CollectionStage.COLLECTING
                
                logger.info(f"✅ AI 조건 설정 완료: {task.service_name}")
                logger.debug(f"조건: {conditions}")
                return True
            else:
                # AI 실패 시 기본 조건 사용
                task.ai_conditions = self._get_default_conditions(task.service_id)
                task.stage = CollectionStage.COLLECTING
                logger.warning(f"⚠️ AI 조건 설정 실패, 기본 조건 사용: {task.service_name}")
                return True
                
        except Exception as e:
            logger.error(f"❌ AI 조건 설정 오류 - {task.service_name}: {str(e)}")
            task.error_messages.append(f"AI 조건 설정 오류: {str(e)}")
            # 기본 조건으로 폴백
            task.ai_conditions = self._get_default_conditions(task.service_id)
            task.stage = CollectionStage.COLLECTING
            return True
    
    async def data_collection(self, task: CollectionTask) -> bool:
        """2단계: 실제 데이터 수집 (1차)"""
        try:
            logger.info(f"📡 데이터 수집 시작: {task.service_name}")
            
            collected_items = []
            
            if task.service_id == 'gov_bizinfo':
                # 기업마당 수집
                collected_items = await self._collect_bizinfo_data(task)
            elif task.service_id == 'gov_kstartup':
                # K-스타트업 수집
                collected_items = await self._collect_kstartup_data(task)
            elif task.service_id == 'dream_collector':
                # 꿈풀이 수집
                collected_items = await self._collect_dream_data(task)
            
            if collected_items:
                task.collected_data.extend(collected_items)
                task.stage = CollectionStage.PROCESSING
                
                logger.info(f"✅ 데이터 수집 완료: {task.service_name} ({len(collected_items)}건)")
                return True
            else:
                logger.warning(f"⚠️ 수집된 데이터 없음: {task.service_name}")
                task.stage = CollectionStage.FAILED
                return False
                
        except Exception as e:
            logger.error(f"❌ 데이터 수집 오류 - {task.service_name}: {str(e)}")
            task.error_messages.append(f"데이터 수집 오류: {str(e)}")
            task.stage = CollectionStage.FAILED
            return False
    
    async def jsonb_processing(self, task: CollectionTask) -> bool:
        """3단계: jsonB 데이터 처리 완성"""
        try:
            logger.info(f"🔄 jsonB 처리 시작: {task.service_name}")
            
            if not task.collected_data:
                logger.warning(f"⚠️ 처리할 데이터 없음: {task.service_name}")
                task.stage = CollectionStage.FAILED
                return False
            
            # AI를 통한 데이터 정제 및 구조화
            processed_data = await self._ai_process_to_jsonb(task)
            
            if processed_data:
                task.jsonb_data = processed_data
                
                # 파일로 저장
                await self._save_jsonb_data(task)
                
                task.stage = CollectionStage.COMPLETED
                task.success_count += 1
                
                logger.info(f"✅ jsonB 처리 완료: {task.service_name}")
                return True
            else:
                logger.error(f"❌ jsonB 처리 실패: {task.service_name}")
                task.stage = CollectionStage.FAILED
                return False
                
        except Exception as e:
            logger.error(f"❌ jsonB 처리 오류 - {task.service_name}: {str(e)}")
            task.error_messages.append(f"jsonB 처리 오류: {str(e)}")
            task.stage = CollectionStage.FAILED
            return False
    
    async def run_single_task(self, service_id: str) -> bool:
        """단일 작업 실행 (전체 2단계 프로세스)"""
        if service_id not in self.tasks:
            logger.error(f"❌ 알 수 없는 서비스: {service_id}")
            return False
        
        task = self.tasks[service_id]
        self.current_task = task
        
        try:
            logger.info(f"🚀 작업 시작: {task.service_name}")
            task.last_run = datetime.now()
            
            # 1단계: AI 조건 설정
            if task.stage == CollectionStage.PLANNING:
                success = await self.ai_condition_setting(task)
                if not success:
                    return False
            
            # 2단계: 데이터 수집
            if task.stage == CollectionStage.COLLECTING:
                success = await self.data_collection(task)
                if not success:
                    return False
            
            # 3단계: jsonB 처리
            if task.stage == CollectionStage.PROCESSING:
                success = await self.jsonb_processing(task)
                if not success:
                    task.error_count += 1
                    return False
            
            # 완료 후 다음 실행 시간 계산
            if task.stage == CollectionStage.COMPLETED:
                interval = random.randint(self.min_interval, self.max_interval)
                task.next_run = datetime.now() + timedelta(seconds=interval)
                task.stage = CollectionStage.PLANNING  # 다음 사이클을 위해 리셋
                
                self.stats['successful_runs'] += 1
                self.stats['total_collected'] += len(task.collected_data)
                
                # 수집된 데이터 초기화 (다음 사이클 준비)
                task.collected_data = []
                task.jsonb_data = None
                
                logger.info(f"🎉 작업 완료: {task.service_name} (다음 실행: {task.next_run.strftime('%H:%M:%S')})")
                return True
            
        except Exception as e:
            logger.error(f"❌ 작업 실행 오류 - {task.service_name}: {str(e)}")
            task.error_messages.append(f"작업 실행 오류: {str(e)}")
            task.error_count += 1
            task.stage = CollectionStage.FAILED
            return False
        finally:
            self.current_task = None
            self.stats['total_runs'] += 1
            self.stats['last_activity'] = datetime.now()
    
    async def start_orchestrator(self) -> None:
        """오케스트레이터 시작 - 2~5분 간격 스케줄링"""
        logger.info("🎼 스마트 크롤링 오케스트레이터 시작")
        self.is_running = True
        
        # 서비스 초기화
        self.initialize_services()
        
        # 첫 실행을 위한 스케줄 설정
        for task in self.tasks.values():
            # 각 서비스마다 다른 시간에 시작하도록 분산
            delay = random.randint(10, 60)  # 10-60초 후 시작
            task.next_run = datetime.now() + timedelta(seconds=delay)
        
        while self.is_running:
            try:
                current_time = datetime.now()
                
                # 실행할 작업 찾기
                ready_tasks = [
                    task for task in self.tasks.values() 
                    if task.next_run and task.next_run <= current_time
                ]
                
                if ready_tasks:
                    # 가장 오래된 작업부터 실행
                    task = min(ready_tasks, key=lambda t: t.next_run)
                    await self.run_single_task(task.service_id)
                
                # 1초마다 체크
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ 오케스트레이터 오류: {str(e)}")
                await asyncio.sleep(5)
    
    def stop_orchestrator(self) -> None:
        """오케스트레이터 중지"""
        logger.info("🛑 스마트 크롤링 오케스트레이터 중지")
        self.is_running = False
    
    def get_status(self) -> Dict[str, Any]:
        """현재 상태 반환"""
        return {
            'is_running': self.is_running,
            'current_task': self.current_task.service_name if self.current_task else None,
            'tasks': {
                service_id: {
                    'service_name': task.service_name,
                    'stage': task.stage.value,
                    'next_run': task.next_run.isoformat() if task.next_run else None,
                    'success_count': task.success_count,
                    'error_count': task.error_count,
                    'collected_items': len(task.collected_data),
                    'has_jsonb': bool(task.jsonb_data)
                }
                for service_id, task in self.tasks.items()
            },
            'stats': self.stats
        }
    
    # Private helper methods
    def _generate_condition_prompt(self, task: CollectionTask) -> str:
        """서비스별 AI 조건 설정 프롬프트 생성"""
        base_prompt = f"""
서비스명: {task.service_name}
대상 URL: {', '.join(task.target_urls)}

다음 웹사이트에서 데이터를 안전하고 효율적으로 수집하기 위한 조건을 설정해주세요:

1. 수집 대상 페이지 유형
2. 핵심 CSS 선택자
3. 데이터 추출 필드
4. 페이지네이션 처리 방법
5. 수집 제외 조건

JSON 형식으로 응답해주세요.
        """
        return base_prompt.strip()
    
    def _parse_ai_conditions(self, ai_content: str) -> Dict[str, Any]:
        """AI 응답을 수집 조건으로 파싱"""
        try:
            # JSON 파싱 시도
            if '{' in ai_content and '}' in ai_content:
                json_start = ai_content.find('{')
                json_end = ai_content.rfind('}') + 1
                json_str = ai_content[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        # 파싱 실패 시 기본 구조 반환
        return {
            'selectors': ['article', '.content', '.list-item'],
            'fields': ['title', 'content', 'date', 'url'],
            'max_pages': 5,
            'delay': 2
        }
    
    def _get_default_conditions(self, service_id: str) -> Dict[str, Any]:
        """서비스별 기본 수집 조건"""
        defaults = {
            'gov_bizinfo': {
                'selectors': ['.board-list tr', '.list-item'],
                'fields': ['title', 'organization', 'deadline', 'category'],
                'max_pages': 3,
                'delay': 3
            },
            'gov_kstartup': {
                'selectors': ['.notice-list li', '.board-item'],
                'fields': ['title', 'content', 'date', 'category'],
                'max_pages': 3,
                'delay': 3
            },
            'dream_collector': {
                'selectors': ['.dream-item', '.content-box'],
                'fields': ['dream_content', 'interpretation', 'category'],
                'max_pages': 5,
                'delay': 2
            }
        }
        return defaults.get(service_id, {})
    
    async def _collect_bizinfo_data(self, task: CollectionTask) -> List[Dict]:
        """기업마당 데이터 수집"""
        try:
            # bizinfo_collector를 사용한 실제 수집
            results = await self.bizinfo_collector.collect_comprehensive_data()
            
            # 결과 포맷팅
            formatted_results = []
            for result in results[:10]:  # 안전을 위해 최대 10개로 제한
                formatted_results.append({
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'organization': result.get('organization', ''),
                    'category': result.get('category', '정부지원사업'),
                    'collected_at': datetime.now().isoformat(),
                    'source': 'bizinfo.go.kr'
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"기업마당 수집 오류: {str(e)}")
            return []
    
    async def _collect_kstartup_data(self, task: CollectionTask) -> List[Dict]:
        """K-스타트업 데이터 수집"""
        # 임시 구현 - 실제 수집기 연동 필요
        return [
            {
                'title': f'창업지원사업 {i+1}',
                'content': f'창업지원 내용 {i+1}',
                'category': '창업지원',
                'collected_at': datetime.now().isoformat(),
                'source': 'k-startup.go.kr'
            }
            for i in range(3)
        ]
    
    async def _collect_dream_data(self, task: CollectionTask) -> List[Dict]:
        """꿈풀이 데이터 수집"""
        # 임시 구현 - 실제 수집기 연동 필요
        return [
            {
                'dream_content': f'꿈 내용 {i+1}',
                'interpretation': f'꿈 해석 {i+1}',
                'category': '꿈풀이',
                'collected_at': datetime.now().isoformat(),
                'source': 'dream_sites'
            }
            for i in range(5)
        ]
    
    async def _ai_process_to_jsonb(self, task: CollectionTask) -> Dict[str, Any]:
        """AI를 통한 jsonB 데이터 처리"""
        try:
            # AI에게 데이터 정제 요청
            data_summary = {
                'service_id': task.service_id,
                'service_name': task.service_name,
                'total_items': len(task.collected_data),
                'collected_at': datetime.now().isoformat(),
                'conditions': task.ai_conditions,
                'data': task.collected_data[:5] if task.collected_data else []  # 샘플 데이터
            }
            
            prompt = f"""
다음 수집된 데이터를 분석하여 구조화된 jsonB 형태로 정리해주세요:

{json.dumps(data_summary, ensure_ascii=False, indent=2)}

1. 데이터 품질 분석
2. 주요 카테고리 분류
3. 중복 제거
4. 핵심 정보 추출
5. 메타데이터 생성

구조화된 JSON 형식으로 응답해주세요.
            """
            
            ai_response = await self.ai_analyzer.analyze_text(
                text=prompt,
                model=AIModel.GEMINI_FLASH,
                analysis_type="data_processing"
            )
            
            if ai_response and ai_response.get('success'):
                # AI 처리 결과와 원본 데이터 통합
                return {
                    'service_info': {
                        'service_id': task.service_id,
                        'service_name': task.service_name,
                        'processed_at': datetime.now().isoformat()
                    },
                    'ai_analysis': ai_response.get('content', {}),
                    'statistics': {
                        'total_items': len(task.collected_data),
                        'processing_time': datetime.now().isoformat(),
                        'ai_model_used': 'gemini_flash'
                    },
                    'raw_data': task.collected_data
                }
            else:
                # AI 처리 실패 시 기본 구조 생성
                return {
                    'service_info': {
                        'service_id': task.service_id,
                        'service_name': task.service_name,
                        'processed_at': datetime.now().isoformat()
                    },
                    'statistics': {
                        'total_items': len(task.collected_data),
                        'processing_time': datetime.now().isoformat(),
                        'ai_model_used': 'fallback'
                    },
                    'raw_data': task.collected_data
                }
                
        except Exception as e:
            logger.error(f"AI jsonB 처리 오류: {str(e)}")
            return None
    
    async def _save_jsonb_data(self, task: CollectionTask) -> None:
        """jsonB 데이터 파일 저장"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{task.service_id}_{timestamp}.jsonb"
            filepath = self.data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(task.jsonb_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 jsonB 파일 저장 완료: {filepath}")
            
        except Exception as e:
            logger.error(f"jsonB 저장 오류: {str(e)}")


# 전역 오케스트레이터 인스턴스
orchestrator = SmartCollectionOrchestrator()


async def main():
    """메인 실행 함수"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        await orchestrator.start_orchestrator()
    except KeyboardInterrupt:
        logger.info("🛑 사용자에 의해 중지됨")
    finally:
        orchestrator.stop_orchestrator()


if __name__ == "__main__":
    asyncio.run(main())