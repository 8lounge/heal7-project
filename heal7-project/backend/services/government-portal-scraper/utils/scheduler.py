"""
Daily Auto-Update Scheduler for Government Portal Scraping
정부 포털 매일 자동 업데이트 스케줄러

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import logging
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Callable, Any
import json
from dataclasses import dataclass
from enum import Enum

import schedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

logger = logging.getLogger(__name__)

class ScheduleType(Enum):
    DAILY = "daily"
    HOURLY = "hourly"
    WEEKLY = "weekly"
    INTERVAL = "interval"
    CRON = "cron"

@dataclass
class ScheduledJob:
    """스케줄된 작업 정보"""
    job_id: str
    name: str
    schedule_type: ScheduleType
    func: Callable
    args: tuple
    kwargs: dict
    schedule_config: dict
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    success_count: int = 0
    error_count: int = 0
    last_error: Optional[str] = None

class UpdateScheduler:
    """정부 포털 자동 업데이트 스케줄러"""
    
    def __init__(self):
        # APScheduler 설정
        self.scheduler = AsyncIOScheduler(
            jobstores={'default': MemoryJobStore()},
            executors={'default': AsyncIOExecutor()},
            job_defaults={
                'coalesce': True,  # 중복 실행 방지
                'max_instances': 1,  # 최대 1개 인스턴스만 실행
                'misfire_grace_time': 300  # 5분 지연 허용
            }
        )
        
        # 작업 관리
        self.jobs: Dict[str, ScheduledJob] = {}
        self.running = False
        
        # 기본 스케줄 설정
        self.default_schedules = {
            # 주요 포털 매일 모니터링
            'bizinfo_daily': {
                'name': '기업마당 일일 모니터링',
                'schedule_type': ScheduleType.DAILY,
                'time': '06:00',
                'timezone': 'Asia/Seoul'
            },
            'kstartup_daily': {
                'name': 'K-Startup 일일 모니터링',
                'schedule_type': ScheduleType.DAILY,
                'time': '07:00',
                'timezone': 'Asia/Seoul'
            },
            # 전체 포털 종합 점검
            'full_check_daily': {
                'name': '전체 포털 종합 점검',
                'schedule_type': ScheduleType.DAILY,
                'time': '13:00',
                'timezone': 'Asia/Seoul'
            },
            # 시간대별 빠른 체크
            'quick_check_hourly': {
                'name': '신속 업데이트 체크',
                'schedule_type': ScheduleType.HOURLY,
                'interval': 2,  # 2시간마다
                'start_time': '08:00',
                'end_time': '18:00'
            },
            # 주간 종합 분석
            'weekly_analysis': {
                'name': '주간 종합 분석',
                'schedule_type': ScheduleType.WEEKLY,
                'day': 'sunday',
                'time': '23:00',
                'timezone': 'Asia/Seoul'
            }
        }
        
        logger.info("📅 UpdateScheduler 초기화 완료")
    
    async def start(self):
        """스케줄러 시작"""
        if not self.running:
            self.scheduler.start()
            self.running = True
            logger.info("🚀 스케줄러 시작됨")
            
            # 기본 작업들 로드
            await self.load_default_schedules()
        
    async def stop(self):
        """스케줄러 정지"""
        if self.running:
            self.scheduler.shutdown(wait=True)
            self.running = False
            logger.info("🛑 스케줄러 정지됨")
    
    async def load_default_schedules(self):
        """기본 스케줄들 로드"""
        logger.info("📋 기본 스케줄 로드 중...")
        
        for job_id, config in self.default_schedules.items():
            # 실제 작업 함수가 등록될 때까지 대기하는 플레이스홀더
            await self.add_placeholder_job(job_id, config)
    
    async def add_placeholder_job(self, job_id: str, config: Dict):
        """플레이스홀더 작업 추가 (실제 함수는 나중에 등록)"""
        placeholder_func = self.create_placeholder_function(job_id)
        
        await self.schedule_job(
            job_id=job_id,
            name=config['name'],
            func=placeholder_func,
            schedule_type=ScheduleType(config['schedule_type']),
            schedule_config=config
        )
    
    def create_placeholder_function(self, job_id: str):
        """플레이스홀더 함수 생성"""
        async def placeholder():
            logger.warning(f"⚠️ 플레이스홀더 실행: {job_id} - 실제 함수가 등록되지 않음")
        return placeholder
    
    async def schedule_job(
        self,
        job_id: str,
        name: str,
        func: Callable,
        schedule_type: ScheduleType,
        schedule_config: Dict,
        args: tuple = (),
        kwargs: Dict = None,
        enabled: bool = True
    ):
        """새로운 작업 스케줄링"""
        
        if kwargs is None:
            kwargs = {}
        
        # 기존 작업 제거 (있다면)
        if job_id in self.jobs:
            await self.remove_job(job_id)
        
        # 트리거 생성
        trigger = self.create_trigger(schedule_type, schedule_config)
        if not trigger:
            logger.error(f"❌ 트리거 생성 실패: {job_id}")
            return False
        
        # 래핑된 함수 생성 (실행 통계 추적용)
        wrapped_func = self.wrap_job_function(job_id, func)
        
        # 스케줄러에 작업 추가
        try:
            self.scheduler.add_job(
                func=wrapped_func,
                trigger=trigger,
                id=job_id,
                name=name,
                args=args,
                kwargs=kwargs,
                replace_existing=True
            )
            
            # 작업 정보 저장
            job = ScheduledJob(
                job_id=job_id,
                name=name,
                schedule_type=schedule_type,
                func=func,
                args=args,
                kwargs=kwargs,
                schedule_config=schedule_config,
                enabled=enabled,
                next_run=self.scheduler.get_job(job_id).next_run_time if enabled else None
            )
            
            self.jobs[job_id] = job
            
            logger.info(f"✅ 작업 스케줄링 완료: {name} ({job_id})")
            if job.next_run:
                logger.info(f"   다음 실행: {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 작업 스케줄링 실패 {job_id}: {str(e)}")
            return False
    
    def create_trigger(self, schedule_type: ScheduleType, config: Dict):
        """스케줄 타입에 따른 트리거 생성"""
        
        try:
            if schedule_type == ScheduleType.DAILY:
                time_str = config.get('time', '09:00')
                hour, minute = map(int, time_str.split(':'))
                return CronTrigger(
                    hour=hour, 
                    minute=minute,
                    timezone=config.get('timezone', 'Asia/Seoul')
                )
            
            elif schedule_type == ScheduleType.HOURLY:
                interval_hours = config.get('interval', 1)
                start_time = config.get('start_time')
                end_time = config.get('end_time')
                
                if start_time and end_time:
                    # 특정 시간대에만 실행
                    start_hour, start_min = map(int, start_time.split(':'))
                    end_hour, end_min = map(int, end_time.split(':'))
                    
                    return CronTrigger(
                        minute=0,  # 매 정시
                        hour=f"{start_hour}-{end_hour}/{interval_hours}",
                        timezone=config.get('timezone', 'Asia/Seoul')
                    )
                else:
                    return IntervalTrigger(hours=interval_hours)
            
            elif schedule_type == ScheduleType.WEEKLY:
                day = config.get('day', 'monday')
                time_str = config.get('time', '09:00')
                hour, minute = map(int, time_str.split(':'))
                
                day_map = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                
                return CronTrigger(
                    day_of_week=day_map.get(day.lower(), 0),
                    hour=hour,
                    minute=minute,
                    timezone=config.get('timezone', 'Asia/Seoul')
                )
            
            elif schedule_type == ScheduleType.INTERVAL:
                interval_seconds = config.get('seconds', 3600)  # 기본 1시간
                return IntervalTrigger(seconds=interval_seconds)
            
            elif schedule_type == ScheduleType.CRON:
                return CronTrigger.from_crontab(
                    config.get('cron_expression', '0 9 * * *'),
                    timezone=config.get('timezone', 'Asia/Seoul')
                )
            
        except Exception as e:
            logger.error(f"❌ 트리거 생성 오류: {str(e)}")
            return None
    
    def wrap_job_function(self, job_id: str, original_func: Callable):
        """작업 함수 래핑 (실행 통계 및 오류 처리)"""
        
        async def wrapped_function(*args, **kwargs):
            job = self.jobs.get(job_id)
            if not job:
                logger.error(f"❌ 작업 정보 없음: {job_id}")
                return
            
            # 실행 시작
            start_time = datetime.now()
            job.last_run = start_time
            job.run_count += 1
            
            logger.info(f"🔄 작업 시작: {job.name} ({job_id})")
            
            try:
                # 원본 함수 실행
                if asyncio.iscoroutinefunction(original_func):
                    result = await original_func(*args, **kwargs)
                else:
                    result = original_func(*args, **kwargs)
                
                # 성공 통계 업데이트
                job.success_count += 1
                job.last_error = None
                
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"✅ 작업 완료: {job.name} ({execution_time:.1f}초)")
                
                return result
                
            except Exception as e:
                # 오류 통계 업데이트
                job.error_count += 1
                job.last_error = str(e)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"❌ 작업 실패: {job.name} ({execution_time:.1f}초) - {str(e)}")
                
                # 오류 알림 (필요시)
                await self.handle_job_error(job_id, e)
                
                raise e
            
            finally:
                # 다음 실행 시간 업데이트
                scheduler_job = self.scheduler.get_job(job_id)
                if scheduler_job:
                    job.next_run = scheduler_job.next_run_time
        
        return wrapped_function
    
    async def handle_job_error(self, job_id: str, error: Exception):
        """작업 오류 처리"""
        job = self.jobs.get(job_id)
        if not job:
            return
        
        # 연속 실패 횟수 체크
        consecutive_failures = job.error_count - job.success_count
        
        if consecutive_failures >= 3:
            logger.critical(f"🚨 연속 실패 알림: {job.name} - {consecutive_failures}회 연속 실패")
            
            # 심각한 경우 작업 비활성화
            if consecutive_failures >= 5:
                await self.disable_job(job_id)
                logger.critical(f"🔒 작업 자동 비활성화: {job.name}")
    
    async def disable_job(self, job_id: str):
        """작업 비활성화"""
        if job_id in self.jobs:
            self.jobs[job_id].enabled = False
            self.scheduler.pause_job(job_id)
            logger.warning(f"⏸️ 작업 비활성화: {job_id}")
    
    async def enable_job(self, job_id: str):
        """작업 활성화"""
        if job_id in self.jobs:
            self.jobs[job_id].enabled = True
            self.scheduler.resume_job(job_id)
            logger.info(f"▶️ 작업 활성화: {job_id}")
    
    async def remove_job(self, job_id: str):
        """작업 제거"""
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]
            logger.info(f"🗑️ 작업 제거: {job_id}")
            return True
        except Exception as e:
            logger.error(f"❌ 작업 제거 실패 {job_id}: {str(e)}")
            return False
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """작업 상태 조회"""
        job = self.jobs.get(job_id)
        if not job:
            return None
        
        scheduler_job = self.scheduler.get_job(job_id)
        
        return {
            'job_id': job.job_id,
            'name': job.name,
            'enabled': job.enabled,
            'schedule_type': job.schedule_type.value,
            'last_run': job.last_run.isoformat() if job.last_run else None,
            'next_run': job.next_run.isoformat() if job.next_run else None,
            'run_count': job.run_count,
            'success_count': job.success_count,
            'error_count': job.error_count,
            'success_rate': (job.success_count / max(1, job.run_count)) * 100,
            'last_error': job.last_error,
            'is_running': bool(scheduler_job and scheduler_job.next_run_time)
        }
    
    def get_all_jobs_status(self) -> List[Dict]:
        """모든 작업 상태 조회"""
        return [self.get_job_status(job_id) for job_id in self.jobs.keys()]
    
    async def run_job_now(self, job_id: str) -> bool:
        """작업 즉시 실행"""
        if job_id not in self.jobs:
            logger.error(f"❌ 작업 없음: {job_id}")
            return False
        
        try:
            job = self.scheduler.get_job(job_id)
            if job:
                job.modify(next_run_time=datetime.now())
                logger.info(f"🚀 즉시 실행 예약: {job_id}")
                return True
        except Exception as e:
            logger.error(f"❌ 즉시 실행 실패 {job_id}: {str(e)}")
        
        return False
    
    async def update_job_function(self, job_id: str, new_func: Callable):
        """작업 함수 업데이트 (플레이스홀더 대체용)"""
        if job_id not in self.jobs:
            logger.error(f"❌ 작업 없음: {job_id}")
            return False
        
        job = self.jobs[job_id]
        
        # 새로운 함수로 작업 재등록
        success = await self.schedule_job(
            job_id=job_id,
            name=job.name,
            func=new_func,
            schedule_type=job.schedule_type,
            schedule_config=job.schedule_config,
            args=job.args,
            kwargs=job.kwargs,
            enabled=job.enabled
        )
        
        if success:
            logger.info(f"🔄 작업 함수 업데이트: {job.name}")
        
        return success
    
    # 편의 메서드들
    async def schedule_daily(self, hour: int, minute: int, func: Callable, args: tuple = (), job_id: str = None):
        """일일 작업 스케줄링"""
        if not job_id:
            job_id = f"daily_{func.__name__}_{hour:02d}{minute:02d}"
        
        return await self.schedule_job(
            job_id=job_id,
            name=f"Daily {func.__name__}",
            func=func,
            schedule_type=ScheduleType.DAILY,
            schedule_config={'time': f"{hour:02d}:{minute:02d}"},
            args=args
        )
    
    async def schedule_hourly(self, interval: int, func: Callable, args: tuple = (), job_id: str = None):
        """시간별 작업 스케줄링"""
        if not job_id:
            job_id = f"hourly_{func.__name__}_{interval}h"
        
        return await self.schedule_job(
            job_id=job_id,
            name=f"Hourly {func.__name__} ({interval}h)",
            func=func,
            schedule_type=ScheduleType.HOURLY,
            schedule_config={'interval': interval},
            args=args
        )
    
    async def schedule_weekly(self, day: str, hour: int, minute: int, func: Callable, args: tuple = (), job_id: str = None):
        """주간 작업 스케줄링"""
        if not job_id:
            job_id = f"weekly_{func.__name__}_{day}"
        
        return await self.schedule_job(
            job_id=job_id,
            name=f"Weekly {func.__name__} ({day})",
            func=func,
            schedule_type=ScheduleType.WEEKLY,
            schedule_config={'day': day, 'time': f"{hour:02d}:{minute:02d}"},
            args=args
        )

class SchedulerMonitor:
    """스케줄러 모니터링 및 건강성 체크"""
    
    def __init__(self, scheduler: UpdateScheduler):
        self.scheduler = scheduler
        self.health_checks = {}
        self.alerts = []
    
    async def health_check(self) -> Dict:
        """스케줄러 건강성 체크"""
        now = datetime.now()
        health_status = {
            'status': 'healthy',
            'scheduler_running': self.scheduler.running,
            'total_jobs': len(self.scheduler.jobs),
            'active_jobs': 0,
            'failed_jobs': 0,
            'alerts': [],
            'last_check': now.isoformat()
        }
        
        for job_id, job in self.scheduler.jobs.items():
            if job.enabled:
                health_status['active_jobs'] += 1
            
            # 실패율 체크
            if job.run_count > 0:
                failure_rate = (job.error_count / job.run_count) * 100
                if failure_rate > 50:  # 50% 이상 실패
                    health_status['failed_jobs'] += 1
                    health_status['alerts'].append(f"{job.name}: 높은 실패율 ({failure_rate:.1f}%)")
            
            # 장시간 미실행 체크
            if job.last_run and (now - job.last_run).days > 2:
                health_status['alerts'].append(f"{job.name}: 2일 이상 미실행")
        
        # 전체 상태 판정
        if health_status['alerts'] or not health_status['scheduler_running']:
            health_status['status'] = 'warning' if health_status['alerts'] else 'critical'
        
        return health_status