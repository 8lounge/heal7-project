"""
하이브리드 데이터베이스 마이그레이션 엔진
NoSQL (JSONB) → 관계형 DB 3단계 파이프라인

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import asyncpg
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import re
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)

class MigrationStage(Enum):
    """마이그레이션 단계"""
    RAW_COLLECTION = "raw_collection"        # 원본 데이터 수집
    DATA_PROCESSING = "data_processing"      # 데이터 정제 및 검증
    RELATIONAL_MIGRATION = "relational_migration"  # 관계형 테이블 마이그레이션
    QUALITY_ASSURANCE = "quality_assurance"  # 품질 보장
    CLEANUP = "cleanup"                      # 정리 작업

class ProcessingStatus(Enum):
    """처리 상태"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DUPLICATE = "duplicate"
    SKIPPED = "skipped"

@dataclass
class MigrationConfig:
    """마이그레이션 설정"""
    batch_size: int = 100
    max_concurrent: int = 5
    quality_threshold: float = 6.0
    enable_ai_validation: bool = True
    auto_cleanup: bool = True
    retry_failed_records: bool = True
    max_retries: int = 3
    processing_timeout_seconds: int = 300

@dataclass
class MigrationStats:
    """마이그레이션 통계"""
    session_id: UUID = field(default_factory=uuid4)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    # 처리 통계
    total_raw_records: int = 0
    processed_records: int = 0
    migrated_records: int = 0
    failed_records: int = 0
    duplicate_records: int = 0
    
    # 품질 통계
    high_quality_count: int = 0  # 8.0+ 점수
    medium_quality_count: int = 0  # 6.0-7.9 점수
    low_quality_count: int = 0   # 6.0 미만
    
    # 성능 통계
    processing_time_seconds: float = 0.0
    average_processing_time_per_record: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'session_id': str(self.session_id),
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_raw_records': self.total_raw_records,
            'processed_records': self.processed_records,
            'migrated_records': self.migrated_records,
            'failed_records': self.failed_records,
            'duplicate_records': self.duplicate_records,
            'high_quality_count': self.high_quality_count,
            'medium_quality_count': self.medium_quality_count,
            'low_quality_count': self.low_quality_count,
            'processing_time_seconds': self.processing_time_seconds,
            'average_processing_time_per_record': self.average_processing_time_per_record
        }

class DataValidator:
    """데이터 검증기"""
    
    def __init__(self):
        self.required_fields = {
            'bizinfo': ['title', 'implementing_agency', 'application_period'],
            'kstartup': ['title', 'status', 'category']
        }
        
        self.field_patterns = {
            'phone': r'\d{2,3}-\d{3,4}-\d{4}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'url': r'https?://[^\s]+',
            'date': r'\d{4}-\d{2}-\d{2}',
            'amount': r'\d{1,3}(?:,\d{3})*(?:\s*[억만원]+)?'
        }
    
    def validate_raw_data(self, raw_data: Dict, portal_id: str) -> Tuple[bool, List[str], float]:
        """원본 데이터 검증"""
        errors = []
        quality_score = 10.0
        
        # 필수 필드 검증
        required = self.required_fields.get(portal_id, [])
        for field in required:
            if not raw_data.get(field) or raw_data[field] in ['N/A', '', None]:
                errors.append(f"Missing required field: {field}")
                quality_score -= 2.0
        
        # 제목 검증
        title = raw_data.get('title', '')
        if len(title) < 10:
            errors.append("Title too short")
            quality_score -= 1.0
        elif len(title) > 300:
            errors.append("Title too long")
            quality_score -= 0.5
        
        # URL 검증
        detail_url = raw_data.get('detail_url')
        if detail_url and not re.match(self.field_patterns['url'], detail_url):
            errors.append("Invalid detail URL format")
            quality_score -= 0.5
        
        # 날짜 형식 검증
        app_period = raw_data.get('application_period', '')
        if app_period and app_period != 'N/A':
            # 한국어 날짜 패턴도 허용
            if not (re.search(r'\d{4}', app_period) and re.search(r'\d{1,2}', app_period)):
                quality_score -= 0.5
        
        # 기관명 검증
        agency = raw_data.get('implementing_agency', raw_data.get('agency', ''))
        if agency and len(agency) < 3:
            errors.append("Agency name too short")
            quality_score -= 0.5
        
        # 중복 검증 (해시 기반)
        content_hash = self._generate_content_hash(raw_data)
        raw_data['content_hash'] = content_hash
        
        quality_score = max(0.0, min(10.0, quality_score))
        is_valid = len(errors) == 0 or quality_score >= 6.0
        
        return is_valid, errors, quality_score
    
    def _generate_content_hash(self, raw_data: Dict) -> str:
        """콘텐츠 해시 생성 (중복 검출용)"""
        key_fields = ['title', 'implementing_agency', 'agency', 'application_period']
        content = ''.join(str(raw_data.get(field, '')) for field in key_fields)
        return hashlib.sha256(content.encode()).hexdigest()[:32]

class DataProcessor:
    """데이터 처리기"""
    
    def __init__(self, validator: DataValidator):
        self.validator = validator
        
    def process_raw_data(self, raw_data: Dict, portal_id: str) -> Dict[str, Any]:
        """원본 데이터를 처리하여 구조화된 데이터로 변환"""
        processed = {
            'portal_id': portal_id,
            'raw_data': raw_data,
            'processed_at': datetime.now().isoformat(),
        }
        
        # 포털별 처리
        if portal_id == 'bizinfo':
            processed.update(self._process_bizinfo_data(raw_data))
        elif portal_id == 'kstartup':
            processed.update(self._process_kstartup_data(raw_data))
        else:
            processed.update(self._process_generic_data(raw_data))
        
        # 품질 점수 계산
        is_valid, errors, quality_score = self.validator.validate_raw_data(raw_data, portal_id)
        processed.update({
            'validation_errors': errors,
            'quality_score': quality_score,
            'is_valid': is_valid
        })
        
        return processed
    
    def _process_bizinfo_data(self, raw_data: Dict) -> Dict:
        """기업마당 데이터 처리"""
        return {
            'program_id': f"bizinfo_{raw_data.get('content_hash', '')}",
            'title': self._clean_text(raw_data.get('title', '')),
            'implementing_agency': self._clean_text(raw_data.get('implementing_agency', '')),
            'jurisdiction': self._clean_text(raw_data.get('jurisdiction', '')),
            'support_field': self._clean_text(raw_data.get('support_field', '')),
            'application_period': self._clean_text(raw_data.get('application_period', '')),
            'registration_date': self._parse_date(raw_data.get('registration_date', '')),
            'view_count': self._parse_integer(raw_data.get('view_count', 0)),
            'detail_url': raw_data.get('detail_url'),
            'contact_info': self._extract_contact_info(raw_data),
            'support_details': self._extract_support_details(raw_data)
        }
    
    def _process_kstartup_data(self, raw_data: Dict) -> Dict:
        """K-Startup 데이터 처리"""
        return {
            'program_id': f"kstartup_{raw_data.get('content_hash', '')}",
            'title': self._clean_text(raw_data.get('title', '')),
            'implementing_agency': 'K-Startup',
            'support_field': self._clean_text(raw_data.get('category', '')),
            'application_period': self._clean_text(raw_data.get('period', raw_data.get('application_period', ''))),
            'application_status': self._normalize_status(raw_data.get('status', 'active')),
            'target_audience': self._clean_text(raw_data.get('target', '')),
            'description': self._clean_text(raw_data.get('description', '')),
            'detail_url': raw_data.get('detail_url'),
            'support_details': {
                'budget': raw_data.get('budget'),
                'category': raw_data.get('category'),
                'organization': raw_data.get('organization')
            }
        }
    
    def _process_generic_data(self, raw_data: Dict) -> Dict:
        """범용 데이터 처리"""
        return {
            'program_id': f"generic_{raw_data.get('content_hash', '')}",
            'title': self._clean_text(raw_data.get('title', '')),
            'implementing_agency': self._clean_text(raw_data.get('agency', raw_data.get('implementing_agency', ''))),
            'description': self._clean_text(raw_data.get('description', '')),
            'detail_url': raw_data.get('detail_url')
        }
    
    def _clean_text(self, text: str) -> str:
        """텍스트 정리"""
        if not text or text == 'N/A':
            return ''
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', str(text))
        
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        
        # 앞뒤 공백 제거
        return text.strip()
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """날짜 파싱"""
        if not date_str or date_str == 'N/A':
            return None
        
        # YYYY-MM-DD 패턴 찾기
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', str(date_str))
        if match:
            return match.group(0)
        
        return None
    
    def _parse_integer(self, value) -> int:
        """정수 파싱"""
        try:
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                # 콤마 제거 후 숫자 추출
                numbers = re.findall(r'\d+', value.replace(',', ''))
                if numbers:
                    return int(numbers[0])
            return 0
        except:
            return 0
    
    def _normalize_status(self, status: str) -> str:
        """상태 정규화"""
        status_map = {
            '모집중': 'active',
            '모집마감': 'closed',
            '접수중': 'active',
            '마감': 'closed',
            '종료': 'expired',
            'active': 'active',
            'closed': 'closed'
        }
        
        return status_map.get(str(status).strip(), 'active')
    
    def _extract_contact_info(self, raw_data: Dict) -> Dict:
        """연락처 정보 추출"""
        contact = {}
        
        # 전화번호 추출
        for field in ['contact_info', 'phone', 'tel', 'contact']:
            value = raw_data.get(field, '')
            if value:
                phone_match = re.search(r'(\d{2,3}-\d{3,4}-\d{4})', str(value))
                if phone_match:
                    contact['phone'] = phone_match.group(1)
                    break
        
        # 이메일 추출
        for field in ['contact_info', 'email', 'contact']:
            value = raw_data.get(field, '')
            if value:
                email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', str(value))
                if email_match:
                    contact['email'] = email_match.group(1)
                    break
        
        return contact
    
    def _extract_support_details(self, raw_data: Dict) -> Dict:
        """지원 상세 정보 추출"""
        details = {}
        
        # 지원 금액
        for field in ['support_amount', 'budget', 'amount']:
            value = raw_data.get(field, '')
            if value and value != 'N/A':
                details['support_amount'] = str(value)
                break
        
        # 지원 기간
        for field in ['support_period', 'period', 'duration']:
            value = raw_data.get(field, '')
            if value and value != 'N/A':
                details['support_period'] = str(value)
                break
        
        # 지원 방식
        for field in ['support_type', 'type']:
            value = raw_data.get(field, '')
            if value and value != 'N/A':
                details['support_type'] = str(value)
                break
        
        return details

class MigrationEngine:
    """마이그레이션 엔진"""
    
    def __init__(self, db_pool: asyncpg.Pool, config: MigrationConfig = None):
        self.db_pool = db_pool
        self.config = config or MigrationConfig()
        self.validator = DataValidator()
        self.processor = DataProcessor(self.validator)
        self.stats = MigrationStats()
        
    async def run_full_migration_pipeline(self, portal_id: str = None, session_id: UUID = None) -> MigrationStats:
        """전체 마이그레이션 파이프라인 실행"""
        logger.info(f"🚀 전체 마이그레이션 파이프라인 시작: {portal_id or 'ALL'}")
        
        self.stats = MigrationStats()
        if session_id:
            self.stats.session_id = session_id
        
        try:
            # 1단계: 원본 데이터 수집 상태 확인
            await self._log_migration_start(portal_id)
            
            # 2단계: 데이터 처리 (Raw → Processed)
            await self._process_raw_data_batch(portal_id)
            
            # 3단계: 관계형 마이그레이션 (Processed → Relational)
            await self._migrate_to_relational_batch(portal_id)
            
            # 4단계: 품질 보장
            await self._quality_assurance_check(portal_id)
            
            # 5단계: 정리 작업
            if self.config.auto_cleanup:
                await self._cleanup_completed_records(portal_id)
            
            # 통계 업데이트
            self.stats.completed_at = datetime.now()
            self.stats.processing_time_seconds = (
                self.stats.completed_at - self.stats.started_at
            ).total_seconds()
            
            if self.stats.processed_records > 0:
                self.stats.average_processing_time_per_record = (
                    self.stats.processing_time_seconds / self.stats.processed_records
                )
            
            await self._log_migration_completion()
            
            logger.info(f"✅ 마이그레이션 완료: {self.stats.migrated_records}개 레코드")
            
        except Exception as e:
            logger.error(f"❌ 마이그레이션 파이프라인 실패: {str(e)}")
            await self._log_migration_error(str(e))
            raise
        
        return self.stats
    
    async def _process_raw_data_batch(self, portal_id: Optional[str]):
        """원본 데이터 배치 처리"""
        logger.info("📊 2단계: 원본 데이터 배치 처리 시작")
        
        async for batch in self._get_pending_raw_data_batches(portal_id):
            semaphore = asyncio.Semaphore(self.config.max_concurrent)
            
            tasks = [
                self._process_single_raw_record(semaphore, record) 
                for record in batch
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 분석
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"❌ 처리 실패 {batch[i]['id']}: {str(result)}")
                    self.stats.failed_records += 1
                elif result:
                    self.stats.processed_records += 1
    
    async def _get_pending_raw_data_batches(self, portal_id: Optional[str]) -> AsyncGenerator[List[Dict], None]:
        """처리 대기 중인 원본 데이터 배치 생성"""
        query = """
            SELECT id, portal_id, raw_data, url, scraping_session_id
            FROM raw_scraped_data
            WHERE processing_status = 'pending'
        """
        params = []
        
        if portal_id:
            query += " AND portal_id = $1"
            params = [portal_id]
        
        query += " ORDER BY scraped_at ASC LIMIT $" + str(len(params) + 1)
        params.append(self.config.batch_size)
        
        async with self.db_pool.acquire() as conn:
            offset = 0
            while True:
                batch_query = query + f" OFFSET {offset}"
                rows = await conn.fetch(batch_query, *params)
                
                if not rows:
                    break
                
                batch = [dict(row) for row in rows]
                self.stats.total_raw_records += len(batch)
                yield batch
                
                offset += len(batch)
                
                if len(batch) < self.config.batch_size:
                    break
    
    async def _process_single_raw_record(self, semaphore: asyncio.Semaphore, record: Dict) -> bool:
        """개별 원본 레코드 처리"""
        async with semaphore:
            try:
                # 처리 상태 업데이트
                await self._update_raw_record_status(record['id'], ProcessingStatus.PROCESSING)
                
                # 데이터 처리
                processed_data = self.processor.process_raw_data(
                    record['raw_data'], 
                    record['portal_id']
                )
                
                # 품질 점수에 따른 처리
                quality_score = processed_data.get('quality_score', 0.0)
                
                if quality_score >= 8.0:
                    self.stats.high_quality_count += 1
                elif quality_score >= 6.0:
                    self.stats.medium_quality_count += 1
                else:
                    self.stats.low_quality_count += 1
                
                # 검증 오류 저장
                validation_errors = processed_data.get('validation_errors', [])
                
                # 원본 레코드 업데이트
                await self._update_raw_record_processed(
                    record['id'], 
                    quality_score,
                    validation_errors,
                    ProcessingStatus.COMPLETED if processed_data['is_valid'] else ProcessingStatus.FAILED
                )
                
                return processed_data['is_valid']
                
            except Exception as e:
                logger.error(f"❌ 레코드 처리 실패 {record['id']}: {str(e)}")
                await self._update_raw_record_status(record['id'], ProcessingStatus.FAILED)
                return False
    
    async def _migrate_to_relational_batch(self, portal_id: Optional[str]):
        """관계형 테이블로 배치 마이그레이션"""
        logger.info("🔄 3단계: 관계형 테이블 마이그레이션 시작")
        
        async for batch in self._get_processed_data_batches(portal_id):
            semaphore = asyncio.Semaphore(self.config.max_concurrent)
            
            tasks = [
                self._migrate_single_record(semaphore, record) 
                for record in batch
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 분석
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"❌ 마이그레이션 실패 {batch[i]['id']}: {str(result)}")
                elif result:
                    self.stats.migrated_records += 1
    
    async def _get_processed_data_batches(self, portal_id: Optional[str]) -> AsyncGenerator[List[Dict], None]:
        """처리된 데이터 배치 생성"""
        query = """
            SELECT id, portal_id, raw_data, quality_score, processing_status
            FROM raw_scraped_data
            WHERE processing_status = 'completed' AND quality_score >= $1 AND migrated_at IS NULL
        """
        params = [self.config.quality_threshold]
        
        if portal_id:
            query += " AND portal_id = $2"
            params.append(portal_id)
            limit_param = "$3"
        else:
            limit_param = "$2"
        
        query += f" ORDER BY quality_score DESC, scraped_at ASC LIMIT {limit_param}"
        params.append(self.config.batch_size)
        
        async with self.db_pool.acquire() as conn:
            offset = 0
            while True:
                batch_query = query + f" OFFSET {offset}"
                rows = await conn.fetch(batch_query, *params)
                
                if not rows:
                    break
                
                batch = [dict(row) for row in rows]
                yield batch
                
                offset += len(batch)
                
                if len(batch) < self.config.batch_size:
                    break
    
    async def _migrate_single_record(self, semaphore: asyncio.Semaphore, record: Dict) -> bool:
        """개별 레코드 마이그레이션"""
        async with semaphore:
            try:
                processed_data = self.processor.process_raw_data(
                    record['raw_data'], 
                    record['portal_id']
                )
                
                # 중복 확인
                existing_program = await self._check_duplicate_program(processed_data.get('program_id'))
                if existing_program:
                    await self._mark_as_duplicate(record['id'])
                    self.stats.duplicate_records += 1
                    return False
                
                # support_programs 테이블에 삽입
                await self._insert_support_program(processed_data, record['id'])
                
                # 원본 레코드의 마이그레이션 완료 표시
                await self._mark_migration_completed(record['id'])
                
                return True
                
            except Exception as e:
                logger.error(f"❌ 레코드 마이그레이션 실패 {record['id']}: {str(e)}")
                return False
    
    async def _insert_support_program(self, processed_data: Dict, raw_id: int):
        """support_programs 테이블에 데이터 삽입"""
        query = """
            INSERT INTO support_programs (
                program_id, portal_id, original_raw_id, title, description,
                support_field, implementing_agency, jurisdiction, contact_info,
                support_details, support_amount, support_period, support_type,
                application_period, application_status, target_audience,
                evaluation_criteria, required_documents, detail_url, attachments,
                view_count, registration_date, data_quality_score, verification_status
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24
            ) ON CONFLICT (program_id) DO UPDATE SET
                updated_at = CURRENT_TIMESTAMP,
                data_quality_score = EXCLUDED.data_quality_score
        """
        
        support_details = processed_data.get('support_details', {})
        contact_info = processed_data.get('contact_info', {})
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                query,
                processed_data.get('program_id'),
                processed_data.get('portal_id'),
                raw_id,
                processed_data.get('title', ''),
                processed_data.get('description', ''),
                processed_data.get('support_field', ''),
                processed_data.get('implementing_agency', ''),
                processed_data.get('jurisdiction', ''),
                json.dumps(contact_info) if contact_info else None,
                json.dumps(support_details) if support_details else None,
                support_details.get('support_amount'),
                support_details.get('support_period'),
                support_details.get('support_type'),
                processed_data.get('application_period', ''),
                processed_data.get('application_status', 'active'),
                processed_data.get('target_audience', ''),
                None,  # evaluation_criteria (추후 구현)
                None,  # required_documents (추후 구현)
                processed_data.get('detail_url'),
                None,  # attachments (추후 구현)
                processed_data.get('view_count', 0),
                processed_data.get('registration_date'),
                processed_data.get('quality_score', 0.0),
                'unverified'
            )
    
    async def _check_duplicate_program(self, program_id: str) -> bool:
        """중복 프로그램 확인"""
        query = "SELECT 1 FROM support_programs WHERE program_id = $1"
        
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchval(query, program_id)
            return result is not None
    
    async def _update_raw_record_status(self, record_id: int, status: ProcessingStatus):
        """원본 레코드 상태 업데이트"""
        query = "UPDATE raw_scraped_data SET processing_status = $1 WHERE id = $2"
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, status.value, record_id)
    
    async def _update_raw_record_processed(self, record_id: int, quality_score: float, 
                                         validation_errors: List[str], status: ProcessingStatus):
        """원본 레코드 처리 완료 업데이트"""
        query = """
            UPDATE raw_scraped_data 
            SET processing_status = $1, quality_score = $2, validation_errors = $3, processed_at = CURRENT_TIMESTAMP
            WHERE id = $4
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                query, 
                status.value, 
                quality_score, 
                json.dumps(validation_errors),
                record_id
            )
    
    async def _mark_as_duplicate(self, record_id: int):
        """중복으로 마크"""
        await self._update_raw_record_status(record_id, ProcessingStatus.DUPLICATE)
    
    async def _mark_migration_completed(self, record_id: int):
        """마이그레이션 완료 마크"""
        query = "UPDATE raw_scraped_data SET migrated_at = CURRENT_TIMESTAMP WHERE id = $1"
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, record_id)
    
    async def _quality_assurance_check(self, portal_id: Optional[str]):
        """품질 보장 검사"""
        logger.info("🔍 4단계: 품질 보장 검사 시작")
        
        # 마이그레이션된 데이터의 품질 확인
        query = """
            SELECT COUNT(*) as total_count,
                   COUNT(*) FILTER (WHERE data_quality_score >= 8.0) as high_quality,
                   COUNT(*) FILTER (WHERE data_quality_score >= 6.0) as acceptable_quality
            FROM support_programs sp
            JOIN raw_scraped_data rsd ON sp.original_raw_id = rsd.id
            WHERE rsd.migrated_at >= $1
        """
        
        params = [self.stats.started_at]
        if portal_id:
            query += " AND sp.portal_id = $2"
            params.append(portal_id)
        
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(query, *params)
            
            if result:
                total = result['total_count']
                high_quality = result['high_quality']
                acceptable = result['acceptable_quality']
                
                logger.info(f"📊 품질 보장 결과:")
                logger.info(f"  전체: {total}개")
                logger.info(f"  고품질 (8.0+): {high_quality}개 ({high_quality/total*100:.1f}%)")
                logger.info(f"  허용 품질 (6.0+): {acceptable}개 ({acceptable/total*100:.1f}%)")
    
    async def _cleanup_completed_records(self, portal_id: Optional[str]):
        """완료된 레코드 정리"""
        logger.info("🧹 5단계: 정리 작업 시작")
        
        # 30일 이상 된 완료 레코드의 HTML 콘텐츠 제거 (용량 절약)
        cleanup_query = """
            UPDATE raw_scraped_data 
            SET html_content = NULL 
            WHERE processing_status = 'completed' 
              AND migrated_at IS NOT NULL
              AND scraped_at < CURRENT_TIMESTAMP - INTERVAL '30 days'
        """
        
        if portal_id:
            cleanup_query += " AND portal_id = $1"
            params = [portal_id]
        else:
            params = []
        
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(cleanup_query, *params)
            logger.info(f"🧹 HTML 콘텐츠 정리 완료: {result} 건")
    
    async def _log_migration_start(self, portal_id: Optional[str]):
        """마이그레이션 시작 로그"""
        query = """
            INSERT INTO scraping_sessions (id, portal_id, session_type, status)
            VALUES ($1, $2, 'migration', 'running')
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, self.stats.session_id, portal_id or 'all')
    
    async def _log_migration_completion(self):
        """마이그레이션 완료 로그"""
        query = """
            UPDATE scraping_sessions 
            SET completed_at = CURRENT_TIMESTAMP,
                status = 'completed',
                items_found = $1,
                items_processed = $2,
                items_migrated = $3,
                total_duration_seconds = $4
            WHERE id = $5
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                query,
                self.stats.total_raw_records,
                self.stats.processed_records,
                self.stats.migrated_records,
                int(self.stats.processing_time_seconds),
                self.stats.session_id
            )
    
    async def _log_migration_error(self, error_message: str):
        """마이그레이션 오류 로그"""
        query = """
            UPDATE scraping_sessions 
            SET completed_at = CURRENT_TIMESTAMP,
                status = 'failed',
                error_details = $1
            WHERE id = $2
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                query,
                json.dumps({'error': error_message, 'stats': self.stats.to_dict()}),
                self.stats.session_id
            )
    
    async def get_migration_status(self, session_id: UUID) -> Optional[Dict]:
        """마이그레이션 상태 조회"""
        query = """
            SELECT * FROM scraping_sessions WHERE id = $1
        """
        
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(query, session_id)
            return dict(result) if result else None