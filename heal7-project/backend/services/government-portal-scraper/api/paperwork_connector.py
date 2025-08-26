"""
Paperwork AI Integration API Gateway
정부 포털 스크래핑 시스템과 Paperwork AI 연동 게이트웨이

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import hmac

import aiohttp
from pydantic import BaseModel, validator
import backoff

logger = logging.getLogger(__name__)

class DataType(Enum):
    PROGRAM = "program"
    TEMPLATE = "template" 
    PATTERN = "pattern"
    ANALYSIS = "analysis"
    NOTIFICATION = "notification"

class SyncStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"

@dataclass
class SyncData:
    """동기화할 데이터 구조"""
    data_type: DataType
    data_id: str
    institution_id: str
    content: Dict
    metadata: Dict
    priority: int = 1  # 1=높음, 2=보통, 3=낮음
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class PaperworkConnector:
    """Paperwork AI 연동 커넥터"""
    
    def __init__(self, base_url: str, api_key: str, secret_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.secret_key = secret_key
        
        # API 엔드포인트
        self.endpoints = {
            'sync': '/api/government-portal/sync',
            'templates': '/api/government-portal/templates',
            'programs': '/api/government-portal/programs',
            'patterns': '/api/government-portal/patterns',
            'health': '/api/government-portal/health',
            'webhook': '/api/government-portal/webhook'
        }
        
        # HTTP 세션
        self.session = None
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'GovernmentPortalScraper/2.0',
            'Authorization': f'Bearer {api_key}'
        }
        
        # 동기화 큐
        self.sync_queue: List[SyncData] = []
        self.max_queue_size = 1000
        self.batch_size = 50  # 한 번에 전송할 최대 항목 수
        
        # 재시도 설정
        self.max_retries = 3
        self.retry_delay = 5  # 초
        
        # 통계
        self.stats = {
            'total_syncs': 0,
            'successful_syncs': 0,
            'failed_syncs': 0,
            'queue_size': 0,
            'last_sync_time': None,
            'connection_errors': 0
        }
        
        logger.info(f"📡 Paperwork AI Connector 초기화: {base_url}")
    
    async def initialize(self):
        """커넥터 초기화"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            connector = aiohttp.TCPConnector(limit=10)
            
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout,
                connector=connector
            )
            
            # 연결 테스트
            await self.test_connection()
            
            logger.info("✅ Paperwork AI 커넥터 초기화 완료")
    
    async def close(self):
        """커넥터 정리"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("🔒 Paperwork AI 커넥터 세션 정리 완료")
    
    async def test_connection(self) -> bool:
        """Paperwork AI 연결 테스트"""
        try:
            url = f"{self.base_url}{self.endpoints['health']}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("✅ Paperwork AI 연결 성공")
                    return True
                else:
                    logger.warning(f"⚠️ Paperwork AI 연결 이상: HTTP {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Paperwork AI 연결 실패: {str(e)}")
            self.stats['connection_errors'] += 1
            return False
    
    def add_to_sync_queue(self, sync_data: SyncData):
        """동기화 큐에 데이터 추가"""
        if len(self.sync_queue) >= self.max_queue_size:
            # 오래된 항목 제거 (FIFO)
            removed = self.sync_queue.pop(0)
            logger.warning(f"⚠️ 큐 오버플로우, 항목 제거: {removed.data_id}")
        
        self.sync_queue.append(sync_data)
        self.stats['queue_size'] = len(self.sync_queue)
        
        logger.debug(f"📥 동기화 큐 추가: {sync_data.data_type.value}/{sync_data.data_id}")
    
    async def sync_programs(self, programs: List[Dict], institution_id: str) -> Dict:
        """지원사업 프로그램 동기화"""
        logger.info(f"📊 프로그램 동기화 시작: {len(programs)}개 ({institution_id})")
        
        # 우선순위별 분류
        priority_programs = self.classify_by_priority(programs)
        
        sync_results = {
            'total_programs': len(programs),
            'successful_syncs': 0,
            'failed_syncs': 0,
            'sync_details': []
        }
        
        # 우선순위별 동기화
        for priority, program_list in priority_programs.items():
            batch_results = await self.sync_program_batch(program_list, institution_id, priority)
            
            sync_results['successful_syncs'] += batch_results['successful']
            sync_results['failed_syncs'] += batch_results['failed']
            sync_results['sync_details'].extend(batch_results['details'])
        
        logger.info(f"✅ 프로그램 동기화 완료: {sync_results['successful_syncs']}/{len(programs)} 성공")
        return sync_results
    
    def classify_by_priority(self, programs: List[Dict]) -> Dict[int, List[Dict]]:
        """프로그램 우선순위 분류"""
        priority_programs = {1: [], 2: [], 3: []}
        
        for program in programs:
            # 우선순위 결정 로직
            priority = self.determine_program_priority(program)
            priority_programs[priority].append(program)
        
        return priority_programs
    
    def determine_program_priority(self, program: Dict) -> int:
        """프로그램 우선순위 결정"""
        # 1순위: 새로운 프로그램이거나 중요한 변경사항
        if program.get('is_new', False):
            return 1
        
        # 마감 임박한 프로그램
        period = program.get('application_period', '')
        if '마감' in period or '종료' in period or '임박' in period:
            return 1
        
        # 주요 기관의 프로그램
        agency = program.get('agency', '')
        major_agencies = ['중소벤처기업부', '중소기업진흥공단', 'NIPA', '기술보증기금']
        if any(major in agency for major in major_agencies):
            return 1
        
        # 2순위: 일반적인 업데이트
        if program.get('hash_value') != program.get('previous_hash'):
            return 2
        
        # 3순위: 변경사항 없음
        return 3
    
    async def sync_program_batch(self, programs: List[Dict], institution_id: str, priority: int) -> Dict:
        """프로그램 배치 동기화"""
        if not programs:
            return {'successful': 0, 'failed': 0, 'details': []}
        
        url = f"{self.base_url}{self.endpoints['programs']}"
        
        sync_payload = {
            'institution_id': institution_id,
            'programs': programs,
            'priority': priority,
            'sync_timestamp': datetime.now().isoformat(),
            'batch_info': {
                'total_count': len(programs),
                'batch_priority': priority,
                'scraper_version': '2.0.0'
            }
        }
        
        # 서명 생성 (보안)
        if self.secret_key:
            sync_payload['signature'] = self.generate_signature(sync_payload)
        
        return await self.send_batch_data(url, sync_payload)
    
    async def sync_templates(self, templates: List[Dict], institution_id: str) -> Dict:
        """템플릿 동기화"""
        logger.info(f"📋 템플릿 동기화 시작: {len(templates)}개 ({institution_id})")
        
        url = f"{self.base_url}{self.endpoints['templates']}"
        
        sync_payload = {
            'institution_id': institution_id,
            'templates': templates,
            'sync_timestamp': datetime.now().isoformat(),
            'template_metadata': {
                'total_count': len(templates),
                'generation_method': 'ai_auto',
                'quality_threshold': 8.0
            }
        }
        
        if self.secret_key:
            sync_payload['signature'] = self.generate_signature(sync_payload)
        
        result = await self.send_batch_data(url, sync_payload)
        
        logger.info(f"✅ 템플릿 동기화 완료: {result['successful']}/{len(templates)} 성공")
        return result
    
    async def sync_patterns(self, patterns: Dict, institution_id: str) -> Dict:
        """패턴 분석 결과 동기화"""
        logger.info(f"🧠 패턴 동기화 시작: {institution_id}")
        
        url = f"{self.base_url}{self.endpoints['patterns']}"
        
        sync_payload = {
            'institution_id': institution_id,
            'patterns': patterns,
            'sync_timestamp': datetime.now().isoformat(),
            'analysis_metadata': {
                'pattern_count': len(patterns),
                'confidence_scores': self.extract_confidence_scores(patterns),
                'analyzer_version': '2.0.0'
            }
        }
        
        if self.secret_key:
            sync_payload['signature'] = self.generate_signature(sync_payload)
        
        result = await self.send_batch_data(url, sync_payload)
        
        logger.info(f"✅ 패턴 동기화 완료")
        return result
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=60
    )
    async def send_batch_data(self, url: str, payload: Dict) -> Dict:
        """배치 데이터 전송 (재시도 포함)"""
        if not self.session:
            await self.initialize()
        
        try:
            self.stats['total_syncs'] += 1
            
            async with self.session.post(url, json=payload) as response:
                response_data = await response.json()
                
                if response.status == 200:
                    self.stats['successful_syncs'] += 1
                    self.stats['last_sync_time'] = datetime.now()
                    
                    return {
                        'successful': response_data.get('processed_count', 0),
                        'failed': response_data.get('failed_count', 0),
                        'details': response_data.get('details', []),
                        'response_data': response_data
                    }
                else:
                    self.stats['failed_syncs'] += 1
                    error_msg = f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    
                    logger.error(f"❌ 배치 전송 실패: {error_msg}")
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=error_msg
                    )
                    
        except Exception as e:
            self.stats['failed_syncs'] += 1
            logger.error(f"❌ 배치 전송 예외: {str(e)}")
            raise
    
    def generate_signature(self, payload: Dict) -> str:
        """요청 서명 생성 (보안)"""
        if not self.secret_key:
            return ""
        
        # 페이로드를 정렬된 JSON 문자열로 변환
        payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        
        # HMAC-SHA256 서명 생성
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def extract_confidence_scores(self, patterns: Dict) -> Dict:
        """패턴에서 신뢰도 점수 추출"""
        scores = {}
        
        for pattern_type, pattern_data in patterns.items():
            if isinstance(pattern_data, dict) and 'confidence_score' in pattern_data:
                scores[pattern_type] = pattern_data['confidence_score']
        
        return scores
    
    async def send_notification(self, notification_type: str, message: str, metadata: Dict = None) -> bool:
        """알림 전송"""
        try:
            url = f"{self.base_url}{self.endpoints['webhook']}"
            
            notification_payload = {
                'type': notification_type,
                'message': message,
                'metadata': metadata or {},
                'timestamp': datetime.now().isoformat(),
                'source': 'government_portal_scraper'
            }
            
            if self.secret_key:
                notification_payload['signature'] = self.generate_signature(notification_payload)
            
            if not self.session:
                await self.initialize()
            
            async with self.session.post(url, json=notification_payload) as response:
                if response.status == 200:
                    logger.info(f"📡 알림 전송 성공: {notification_type}")
                    return True
                else:
                    logger.warning(f"⚠️ 알림 전송 실패: HTTP {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ 알림 전송 예외: {str(e)}")
            return False
    
    async def process_sync_queue(self):
        """동기화 큐 처리"""
        if not self.sync_queue:
            return
        
        logger.info(f"🔄 동기화 큐 처리 시작: {len(self.sync_queue)}개 항목")
        
        # 우선순위별 정렬
        self.sync_queue.sort(key=lambda x: (x.priority, x.created_at))
        
        # 배치별 처리
        while self.sync_queue:
            batch = self.sync_queue[:self.batch_size]
            self.sync_queue = self.sync_queue[self.batch_size:]
            
            await self.process_sync_batch(batch)
            
            # 배치간 딜레이
            await asyncio.sleep(1)
        
        self.stats['queue_size'] = 0
        logger.info("✅ 동기화 큐 처리 완료")
    
    async def process_sync_batch(self, batch: List[SyncData]):
        """동기화 배치 처리"""
        grouped_data = self.group_sync_data_by_type(batch)
        
        for data_type, items in grouped_data.items():
            try:
                if data_type == DataType.PROGRAM:
                    await self.sync_programs_from_queue(items)
                elif data_type == DataType.TEMPLATE:
                    await self.sync_templates_from_queue(items)
                elif data_type == DataType.PATTERN:
                    await self.sync_patterns_from_queue(items)
                elif data_type == DataType.NOTIFICATION:
                    await self.send_notifications_from_queue(items)
                    
            except Exception as e:
                logger.error(f"❌ {data_type.value} 배치 처리 실패: {str(e)}")
    
    def group_sync_data_by_type(self, batch: List[SyncData]) -> Dict[DataType, List[SyncData]]:
        """동기화 데이터를 타입별로 그룹화"""
        grouped = {}
        
        for item in batch:
            if item.data_type not in grouped:
                grouped[item.data_type] = []
            grouped[item.data_type].append(item)
        
        return grouped
    
    async def sync_programs_from_queue(self, items: List[SyncData]):
        """큐의 프로그램 데이터 동기화"""
        programs_by_institution = {}
        
        for item in items:
            institution = item.institution_id
            if institution not in programs_by_institution:
                programs_by_institution[institution] = []
            programs_by_institution[institution].append(item.content)
        
        for institution, programs in programs_by_institution.items():
            await self.sync_programs(programs, institution)
    
    async def sync_templates_from_queue(self, items: List[SyncData]):
        """큐의 템플릿 데이터 동기화"""
        templates_by_institution = {}
        
        for item in items:
            institution = item.institution_id
            if institution not in templates_by_institution:
                templates_by_institution[institution] = []
            templates_by_institution[institution].append(item.content)
        
        for institution, templates in templates_by_institution.items():
            await self.sync_templates(templates, institution)
    
    async def sync_patterns_from_queue(self, items: List[SyncData]):
        """큐의 패턴 데이터 동기화"""
        for item in items:
            await self.sync_patterns(item.content, item.institution_id)
    
    async def send_notifications_from_queue(self, items: List[SyncData]):
        """큐의 알림 전송"""
        for item in items:
            await self.send_notification(
                notification_type=item.metadata.get('type', 'info'),
                message=item.content.get('message', ''),
                metadata=item.metadata
            )
    
    def get_stats(self) -> Dict:
        """커넥터 통계 조회"""
        return {
            **self.stats,
            'success_rate': (self.stats['successful_syncs'] / max(1, self.stats['total_syncs'])) * 100,
            'queue_size': len(self.sync_queue),
            'is_connected': bool(self.session),
            'last_connection_test': datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict:
        """커넥터 상태 확인"""
        health_status = {
            'connector_status': 'healthy',
            'paperwork_connection': False,
            'queue_health': 'normal',
            'stats': self.get_stats(),
            'last_check': datetime.now().isoformat()
        }
        
        # Paperwork AI 연결 확인
        health_status['paperwork_connection'] = await self.test_connection()
        
        # 큐 건강도 확인
        queue_size = len(self.sync_queue)
        if queue_size > self.max_queue_size * 0.8:
            health_status['queue_health'] = 'warning'
        elif queue_size >= self.max_queue_size:
            health_status['queue_health'] = 'critical'
        
        # 전체 상태 판정
        if not health_status['paperwork_connection'] or health_status['queue_health'] == 'critical':
            health_status['connector_status'] = 'unhealthy'
        elif health_status['queue_health'] == 'warning':
            health_status['connector_status'] = 'warning'
        
        return health_status