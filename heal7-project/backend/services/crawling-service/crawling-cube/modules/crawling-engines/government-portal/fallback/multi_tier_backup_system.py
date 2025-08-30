"""
다중 티어 폴백 및 백업 시스템
데이터 수집 실패 시 다중 백업을 통한 완전한 데이터 보호

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import aiofiles
import asyncpg
import json
import logging
import os
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum
import aioredis
import boto3
from uuid import UUID, uuid4
import gzip
import shutil

logger = logging.getLogger(__name__)

class BackupTier(Enum):
    """백업 티어 정의"""
    PRIMARY = "primary"           # PostgreSQL JSONB
    SECONDARY = "secondary"       # File System JSON
    TERTIARY = "tertiary"         # Redis Cache
    QUATERNARY = "quaternary"     # Remote Backup (S3)

class BackupStatus(Enum):
    """백업 상태"""
    ACTIVE = "active"
    CORRUPTED = "corrupted"
    EXPIRED = "expired"
    RESTORING = "restoring"
    RESTORED = "restored"

@dataclass
class BackupRecord:
    """백업 레코드"""
    backup_id: UUID = field(default_factory=uuid4)
    source_id: str = ""
    tier: BackupTier = BackupTier.PRIMARY
    data: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=30))
    status: BackupStatus = BackupStatus.ACTIVE
    checksum: str = ""
    
    def __post_init__(self):
        """백업 레코드 생성 후 체크섬 계산"""
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """데이터 체크섬 계산"""
        data_str = json.dumps(self.data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """데이터 무결성 검증"""
        current_checksum = self._calculate_checksum()
        return current_checksum == self.checksum

@dataclass
class BackupConfig:
    """백업 설정"""
    # 파일 시스템 설정
    filesystem_root: Path = Path("/var/backups/government-scraper")
    max_files_per_directory: int = 1000
    compression_enabled: bool = True
    
    # Redis 설정
    redis_url: str = "redis://localhost:6379/1"
    redis_key_prefix: str = "gov_scraper:backup:"
    redis_ttl_seconds: int = 86400 * 7  # 7일
    
    # 원격 백업 설정 (S3)
    s3_bucket: Optional[str] = None
    s3_prefix: str = "government-scraper-backups/"
    s3_storage_class: str = "STANDARD_IA"
    
    # 정리 설정
    cleanup_interval_hours: int = 24
    max_backup_age_days: int = 30
    max_total_size_gb: float = 10.0

class FileSystemBackupManager:
    """파일 시스템 백업 매니저"""
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.root_path = config.filesystem_root
        self._ensure_directories()
    
    def _ensure_directories(self):
        """필요한 디렉토리 생성"""
        directories = [
            self.root_path,
            self.root_path / "daily",
            self.root_path / "weekly", 
            self.root_path / "monthly",
            self.root_path / "recovery"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        logger.info(f"✅ 파일 시스템 백업 디렉토리 준비 완료: {self.root_path}")
    
    async def save_backup(self, record: BackupRecord) -> str:
        """백업을 파일 시스템에 저장"""
        try:
            # 날짜별 디렉토리 구성
            date_str = record.created_at.strftime("%Y-%m-%d")
            daily_dir = self.root_path / "daily" / date_str
            daily_dir.mkdir(parents=True, exist_ok=True)
            
            # 파일명 생성 (충돌 방지를 위한 UUID 포함)
            filename = f"{record.source_id}_{record.backup_id.hex[:8]}.json"
            if self.config.compression_enabled:
                filename += ".gz"
            
            file_path = daily_dir / filename
            
            # 백업 데이터 준비
            backup_data = {
                'backup_id': str(record.backup_id),
                'source_id': record.source_id,
                'tier': record.tier.value,
                'data': record.data,
                'metadata': record.metadata,
                'created_at': record.created_at.isoformat(),
                'expires_at': record.expires_at.isoformat(),
                'status': record.status.value,
                'checksum': record.checksum
            }
            
            # 파일 저장 (압축 여부에 따라)
            if self.config.compression_enabled:
                await self._save_compressed(file_path, backup_data)
            else:
                await self._save_json(file_path, backup_data)
            
            logger.info(f"📁 파일 시스템 백업 저장 완료: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"❌ 파일 시스템 백업 실패: {str(e)}")
            raise
    
    async def _save_compressed(self, file_path: Path, data: Dict):
        """압축된 JSON 파일 저장"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        compressed_data = gzip.compress(json_str.encode('utf-8'))
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(compressed_data)
    
    async def _save_json(self, file_path: Path, data: Dict):
        """일반 JSON 파일 저장"""
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    
    async def load_backup(self, file_path: str) -> Optional[BackupRecord]:
        """파일 시스템에서 백업 로드"""
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"⚠️ 백업 파일 없음: {file_path}")
                return None
            
            # 파일 로드 (압축 여부 확인)
            if path.name.endswith('.gz'):
                data = await self._load_compressed(path)
            else:
                data = await self._load_json(path)
            
            # BackupRecord 객체로 변환
            return self._dict_to_backup_record(data)
            
        except Exception as e:
            logger.error(f"❌ 파일 시스템 백업 로드 실패 {file_path}: {str(e)}")
            return None
    
    async def _load_compressed(self, file_path: Path) -> Dict:
        """압축된 JSON 파일 로드"""
        async with aiofiles.open(file_path, 'rb') as f:
            compressed_data = await f.read()
            
        json_str = gzip.decompress(compressed_data).decode('utf-8')
        return json.loads(json_str)
    
    async def _load_json(self, file_path: Path) -> Dict:
        """일반 JSON 파일 로드"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
    
    def _dict_to_backup_record(self, data: Dict) -> BackupRecord:
        """딕셔너리를 BackupRecord로 변환"""
        return BackupRecord(
            backup_id=UUID(data['backup_id']),
            source_id=data['source_id'],
            tier=BackupTier(data['tier']),
            data=data['data'],
            metadata=data['metadata'],
            created_at=datetime.fromisoformat(data['created_at']),
            expires_at=datetime.fromisoformat(data['expires_at']),
            status=BackupStatus(data['status']),
            checksum=data['checksum']
        )
    
    async def list_backups(self, date_range: Optional[tuple] = None) -> List[str]:
        """백업 파일 목록 조회"""
        backup_files = []
        
        daily_dir = self.root_path / "daily"
        if not daily_dir.exists():
            return backup_files
        
        for date_dir in daily_dir.iterdir():
            if not date_dir.is_dir():
                continue
            
            # 날짜 필터링
            if date_range:
                try:
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d").date()
                    start_date, end_date = date_range
                    if not (start_date <= dir_date <= end_date):
                        continue
                except ValueError:
                    continue
            
            # 파일 목록 수집
            for file_path in date_dir.glob("*.json*"):
                backup_files.append(str(file_path))
        
        return sorted(backup_files)
    
    async def cleanup_expired_backups(self) -> int:
        """만료된 백업 정리"""
        cleaned_count = 0
        cutoff_date = datetime.now() - timedelta(days=self.config.max_backup_age_days)
        
        for backup_file in await self.list_backups():
            try:
                backup_record = await self.load_backup(backup_file)
                if backup_record and backup_record.expires_at < cutoff_date:
                    os.remove(backup_file)
                    cleaned_count += 1
                    logger.info(f"🧹 만료된 백업 삭제: {backup_file}")
                    
            except Exception as e:
                logger.error(f"❌ 백업 정리 실패 {backup_file}: {str(e)}")
        
        return cleaned_count

class RedisBackupManager:
    """Redis 캐시 백업 매니저"""
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.redis_client = None
        self.key_prefix = config.redis_key_prefix
    
    async def initialize(self):
        """Redis 클라이언트 초기화"""
        try:
            self.redis_client = await aioredis.from_url(
                self.config.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info("✅ Redis 백업 시스템 초기화 완료")
            
        except Exception as e:
            logger.error(f"❌ Redis 초기화 실패: {str(e)}")
            self.redis_client = None
    
    async def save_backup(self, record: BackupRecord) -> str:
        """Redis에 백업 저장"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        try:
            key = f"{self.key_prefix}{record.backup_id}"
            
            backup_data = {
                'backup_id': str(record.backup_id),
                'source_id': record.source_id,
                'tier': record.tier.value,
                'data': json.dumps(record.data, ensure_ascii=False),
                'metadata': json.dumps(record.metadata, ensure_ascii=False),
                'created_at': record.created_at.isoformat(),
                'expires_at': record.expires_at.isoformat(),
                'status': record.status.value,
                'checksum': record.checksum
            }
            
            # Hash로 저장하고 TTL 설정
            await self.redis_client.hset(key, mapping=backup_data)
            await self.redis_client.expire(key, self.config.redis_ttl_seconds)
            
            logger.info(f"📋 Redis 백업 저장 완료: {key}")
            return key
            
        except Exception as e:
            logger.error(f"❌ Redis 백업 저장 실패: {str(e)}")
            raise
    
    async def load_backup(self, backup_id: UUID) -> Optional[BackupRecord]:
        """Redis에서 백업 로드"""
        if not self.redis_client:
            logger.warning("⚠️ Redis 클라이언트 없음")
            return None
        
        try:
            key = f"{self.key_prefix}{backup_id}"
            data = await self.redis_client.hgetall(key)
            
            if not data:
                return None
            
            # BackupRecord 객체로 변환
            return BackupRecord(
                backup_id=UUID(data['backup_id']),
                source_id=data['source_id'],
                tier=BackupTier(data['tier']),
                data=json.loads(data['data']),
                metadata=json.loads(data['metadata']),
                created_at=datetime.fromisoformat(data['created_at']),
                expires_at=datetime.fromisoformat(data['expires_at']),
                status=BackupStatus(data['status']),
                checksum=data['checksum']
            )
            
        except Exception as e:
            logger.error(f"❌ Redis 백업 로드 실패 {backup_id}: {str(e)}")
            return None
    
    async def list_backup_keys(self) -> List[str]:
        """Redis 백업 키 목록 조회"""
        if not self.redis_client:
            return []
        
        pattern = f"{self.key_prefix}*"
        return await self.redis_client.keys(pattern)
    
    async def close(self):
        """Redis 연결 종료"""
        if self.redis_client:
            await self.redis_client.close()

class RemoteBackupManager:
    """원격 백업 매니저 (S3)"""
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.s3_client = None
        
        if config.s3_bucket:
            try:
                import boto3
                self.s3_client = boto3.client('s3')
                logger.info(f"✅ S3 백업 시스템 초기화: {config.s3_bucket}")
            except Exception as e:
                logger.warning(f"⚠️ S3 초기화 실패: {str(e)}")
    
    async def save_backup(self, record: BackupRecord) -> Optional[str]:
        """S3에 백업 저장"""
        if not self.s3_client or not self.config.s3_bucket:
            logger.debug("S3 백업 비활성화됨")
            return None
        
        try:
            # S3 키 생성
            date_str = record.created_at.strftime("%Y/%m/%d")
            s3_key = f"{self.config.s3_prefix}{date_str}/{record.source_id}_{record.backup_id.hex}.json.gz"
            
            # 데이터 준비 및 압축
            backup_data = {
                'backup_id': str(record.backup_id),
                'source_id': record.source_id,
                'data': record.data,
                'metadata': record.metadata,
                'created_at': record.created_at.isoformat(),
                'checksum': record.checksum
            }
            
            json_str = json.dumps(backup_data, ensure_ascii=False)
            compressed_data = gzip.compress(json_str.encode('utf-8'))
            
            # S3에 업로드
            self.s3_client.put_object(
                Bucket=self.config.s3_bucket,
                Key=s3_key,
                Body=compressed_data,
                StorageClass=self.config.s3_storage_class,
                Metadata={
                    'source-id': record.source_id,
                    'backup-id': str(record.backup_id),
                    'created-at': record.created_at.isoformat()
                }
            )
            
            logger.info(f"☁️ S3 백업 저장 완료: {s3_key}")
            return s3_key
            
        except Exception as e:
            logger.error(f"❌ S3 백업 저장 실패: {str(e)}")
            return None
    
    async def load_backup(self, s3_key: str) -> Optional[BackupRecord]:
        """S3에서 백업 로드"""
        if not self.s3_client or not self.config.s3_bucket:
            return None
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.config.s3_bucket,
                Key=s3_key
            )
            
            compressed_data = response['Body'].read()
            json_str = gzip.decompress(compressed_data).decode('utf-8')
            data = json.loads(json_str)
            
            return BackupRecord(
                backup_id=UUID(data['backup_id']),
                source_id=data['source_id'],
                data=data['data'],
                metadata=data['metadata'],
                created_at=datetime.fromisoformat(data['created_at']),
                checksum=data['checksum']
            )
            
        except Exception as e:
            logger.error(f"❌ S3 백업 로드 실패 {s3_key}: {str(e)}")
            return None

class MultiTierBackupSystem:
    """다중 티어 백업 시스템 통합 매니저"""
    
    def __init__(self, db_pool: asyncpg.Pool, config: BackupConfig = None):
        self.db_pool = db_pool
        self.config = config or BackupConfig()
        
        # 티어별 매니저 초기화
        self.filesystem_manager = FileSystemBackupManager(self.config)
        self.redis_manager = RedisBackupManager(self.config)
        self.remote_manager = RemoteBackupManager(self.config)
        
        # 통계
        self.stats = {
            'backups_created': 0,
            'backups_restored': 0,
            'backup_failures': 0,
            'integrity_checks': 0,
            'corruption_detected': 0
        }
    
    async def initialize(self):
        """모든 백업 시스템 초기화"""
        await self.redis_manager.initialize()
        logger.info("🚀 다중 티어 백업 시스템 초기화 완료")
    
    async def create_full_backup(self, source_id: str, data: Dict, metadata: Dict = None) -> BackupRecord:
        """모든 티어에 백업 생성"""
        backup_record = BackupRecord(
            source_id=source_id,
            data=data,
            metadata=metadata or {}
        )
        
        backup_locations = {}
        
        try:
            # Primary: PostgreSQL에 기록
            await self._save_to_database(backup_record)
            backup_locations[BackupTier.PRIMARY.value] = "database"
            
            # Secondary: 파일 시스템
            fs_location = await self.filesystem_manager.save_backup(backup_record)
            backup_locations[BackupTier.SECONDARY.value] = fs_location
            
            # Tertiary: Redis
            redis_key = await self.redis_manager.save_backup(backup_record)
            backup_locations[BackupTier.TERTIARY.value] = redis_key
            
            # Quaternary: 원격 백업 (S3)
            s3_location = await self.remote_manager.save_backup(backup_record)
            if s3_location:
                backup_locations[BackupTier.QUATERNARY.value] = s3_location
            
            # 백업 위치 메타데이터에 추가
            backup_record.metadata['backup_locations'] = backup_locations
            await self._update_database_backup_locations(backup_record)
            
            self.stats['backups_created'] += 1
            logger.info(f"✅ 다중 티어 백업 완료: {backup_record.backup_id}")
            
            return backup_record
            
        except Exception as e:
            self.stats['backup_failures'] += 1
            logger.error(f"❌ 다중 티어 백업 실패 {source_id}: {str(e)}")
            raise
    
    async def restore_from_any_tier(self, backup_id: UUID) -> Optional[BackupRecord]:
        """모든 티어에서 백업 복구 시도"""
        logger.info(f"🔄 백업 복구 시도: {backup_id}")
        
        # Primary: PostgreSQL 먼저 시도
        try:
            record = await self._load_from_database(backup_id)
            if record and record.verify_integrity():
                logger.info(f"✅ Primary(DB)에서 복구 성공: {backup_id}")
                self.stats['backups_restored'] += 1
                return record
        except Exception as e:
            logger.warning(f"⚠️ Primary 복구 실패: {str(e)}")
        
        # Tertiary: Redis 시도 (빠른 액세스)
        try:
            record = await self.redis_manager.load_backup(backup_id)
            if record and record.verify_integrity():
                logger.info(f"✅ Tertiary(Redis)에서 복구 성공: {backup_id}")
                # Primary에 복원
                await self._save_to_database(record)
                self.stats['backups_restored'] += 1
                return record
        except Exception as e:
            logger.warning(f"⚠️ Tertiary 복구 실패: {str(e)}")
        
        # Secondary: 파일 시스템 검색
        try:
            backup_files = await self.filesystem_manager.list_backups()
            for file_path in backup_files:
                if backup_id.hex in file_path:
                    record = await self.filesystem_manager.load_backup(file_path)
                    if record and record.backup_id == backup_id and record.verify_integrity():
                        logger.info(f"✅ Secondary(FS)에서 복구 성공: {backup_id}")
                        # Primary와 Tertiary에 복원
                        await self._save_to_database(record)
                        await self.redis_manager.save_backup(record)
                        self.stats['backups_restored'] += 1
                        return record
        except Exception as e:
            logger.warning(f"⚠️ Secondary 복구 실패: {str(e)}")
        
        # Quaternary: S3에서 시도 (마지막 수단)
        # TODO: S3에서 백업 ID로 검색하는 로직 추가
        
        logger.error(f"❌ 모든 티어에서 복구 실패: {backup_id}")
        return None
    
    async def verify_backup_integrity(self, backup_id: UUID) -> Dict[str, Any]:
        """모든 티어의 백업 무결성 검증"""
        verification_result = {
            'backup_id': str(backup_id),
            'timestamp': datetime.now().isoformat(),
            'tiers_checked': {},
            'corruption_detected': False,
            'recommendations': []
        }
        
        # 각 티어별 검증
        tiers_to_check = [
            (BackupTier.PRIMARY, self._verify_database_backup),
            (BackupTier.TERTIARY, self._verify_redis_backup),
            (BackupTier.SECONDARY, self._verify_filesystem_backup)
        ]
        
        for tier, verify_func in tiers_to_check:
            try:
                tier_result = await verify_func(backup_id)
                verification_result['tiers_checked'][tier.value] = tier_result
                
                if not tier_result.get('integrity_ok', False):
                    verification_result['corruption_detected'] = True
                    
            except Exception as e:
                verification_result['tiers_checked'][tier.value] = {
                    'error': str(e),
                    'integrity_ok': False
                }
        
        # 권장사항 생성
        if verification_result['corruption_detected']:
            verification_result['recommendations'] = [
                "Backup corruption detected",
                "Consider restoring from alternate tier",
                "Run full backup verification"
            ]
        
        self.stats['integrity_checks'] += 1
        if verification_result['corruption_detected']:
            self.stats['corruption_detected'] += 1
        
        return verification_result
    
    async def _save_to_database(self, record: BackupRecord):
        """데이터베이스에 백업 레코드 저장"""
        query = """
            INSERT INTO backup_data_registry (
                backup_id, source_table, source_record_id, backup_method,
                backup_location, backup_data, metadata, backup_status,
                created_at, expires_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (backup_id) DO UPDATE SET
                backup_data = EXCLUDED.backup_data,
                metadata = EXCLUDED.metadata
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                query,
                record.backup_id,
                'raw_scraped_data',  # 소스 테이블
                record.source_id,
                'hybrid',
                'database',
                json.dumps(record.data),
                json.dumps(record.metadata),
                record.status.value,
                record.created_at,
                record.expires_at
            )
    
    async def _load_from_database(self, backup_id: UUID) -> Optional[BackupRecord]:
        """데이터베이스에서 백업 레코드 로드"""
        query = """
            SELECT backup_id, source_record_id, backup_data, metadata,
                   created_at, expires_at, backup_status
            FROM backup_data_registry
            WHERE backup_id = $1 AND backup_status = 'active'
        """
        
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, backup_id)
            
            if not row:
                return None
            
            return BackupRecord(
                backup_id=UUID(str(row['backup_id'])),
                source_id=str(row['source_record_id']),
                tier=BackupTier.PRIMARY,
                data=json.loads(row['backup_data']),
                metadata=json.loads(row['metadata']),
                created_at=row['created_at'],
                expires_at=row['expires_at'],
                status=BackupStatus(row['backup_status'])
            )
    
    async def _update_database_backup_locations(self, record: BackupRecord):
        """데이터베이스의 백업 위치 정보 업데이트"""
        query = """
            UPDATE backup_data_registry 
            SET metadata = $1
            WHERE backup_id = $2
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                query,
                json.dumps(record.metadata),
                record.backup_id
            )
    
    async def _verify_database_backup(self, backup_id: UUID) -> Dict:
        """데이터베이스 백업 무결성 검증"""
        record = await self._load_from_database(backup_id)
        
        if not record:
            return {'integrity_ok': False, 'error': 'Backup not found in database'}
        
        integrity_ok = record.verify_integrity()
        
        return {
            'integrity_ok': integrity_ok,
            'checksum_match': integrity_ok,
            'found': True
        }
    
    async def _verify_redis_backup(self, backup_id: UUID) -> Dict:
        """Redis 백업 무결성 검증"""
        record = await self.redis_manager.load_backup(backup_id)
        
        if not record:
            return {'integrity_ok': False, 'error': 'Backup not found in Redis'}
        
        integrity_ok = record.verify_integrity()
        
        return {
            'integrity_ok': integrity_ok,
            'checksum_match': integrity_ok,
            'found': True
        }
    
    async def _verify_filesystem_backup(self, backup_id: UUID) -> Dict:
        """파일 시스템 백업 무결성 검증"""
        backup_files = await self.filesystem_manager.list_backups()
        
        for file_path in backup_files:
            if backup_id.hex in file_path:
                record = await self.filesystem_manager.load_backup(file_path)
                if record and record.backup_id == backup_id:
                    integrity_ok = record.verify_integrity()
                    return {
                        'integrity_ok': integrity_ok,
                        'checksum_match': integrity_ok,
                        'found': True,
                        'file_path': file_path
                    }
        
        return {'integrity_ok': False, 'error': 'Backup not found in filesystem'}
    
    async def run_cleanup_cycle(self) -> Dict[str, int]:
        """정리 사이클 실행"""
        logger.info("🧹 백업 정리 사이클 시작")
        
        cleanup_results = {
            'filesystem_cleaned': 0,
            'database_cleaned': 0,
            'redis_cleaned': 0
        }
        
        try:
            # 파일 시스템 정리
            fs_cleaned = await self.filesystem_manager.cleanup_expired_backups()
            cleanup_results['filesystem_cleaned'] = fs_cleaned
            
            # 데이터베이스 정리
            db_cleaned = await self._cleanup_database_backups()
            cleanup_results['database_cleaned'] = db_cleaned
            
            # Redis는 TTL로 자동 정리됨
            
            logger.info(f"✅ 백업 정리 완료: {cleanup_results}")
            
        except Exception as e:
            logger.error(f"❌ 백업 정리 실패: {str(e)}")
        
        return cleanup_results
    
    async def _cleanup_database_backups(self) -> int:
        """데이터베이스의 만료된 백업 정리"""
        query = """
            DELETE FROM backup_data_registry
            WHERE backup_status = 'expired' OR expires_at < CURRENT_TIMESTAMP
        """
        
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(query)
            # PostgreSQL의 경우 "DELETE n" 형태로 반환
            count = int(result.split()[-1]) if result.startswith('DELETE') else 0
            return count
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """백업 통계 조회"""
        return {
            'statistics': self.stats.copy(),
            'config': {
                'filesystem_root': str(self.config.filesystem_root),
                'max_backup_age_days': self.config.max_backup_age_days,
                'compression_enabled': self.config.compression_enabled,
                's3_enabled': self.config.s3_bucket is not None
            }
        }
    
    async def close(self):
        """모든 연결 종료"""
        await self.redis_manager.close()
        logger.info("🔒 다중 티어 백업 시스템 종료")