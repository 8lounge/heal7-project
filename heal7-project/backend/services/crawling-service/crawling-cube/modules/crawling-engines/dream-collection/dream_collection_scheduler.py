#!/usr/bin/env python3
"""
⏰ 꿈풀이 데이터 스마트 수집 스케줄러
- 5분 간격으로 키워드 기반 수집
- 일일 5,000개 목표 달성
- 시간대별 수집량 조절
"""

import time
import schedule
import logging
import json
import subprocess
from datetime import datetime, timedelta
from smart_keyword_collector import SmartKeywordCollector
import threading
import signal
import sys

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/logs/dream_collection_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DreamCollectionScheduler:
    def __init__(self):
        self.collector = SmartKeywordCollector()
        self.daily_target = 5000
        self.daily_collected = 0
        self.last_reset_date = datetime.now().date()
        self.is_running = True
        self.collection_stats = {
            'total_collected': 0,
            'total_batches': 0,
            'success_batches': 0,
            'average_per_batch': 0
        }
        
        # 시간대별 수집 강도 설정
        self.hourly_intensity = {
            # 새벽 (조용한 시간) - 높은 강도
            0: 25, 1: 25, 2: 25, 3: 25, 4: 25, 5: 20,
            # 오전 (보통) - 중간 강도  
            6: 15, 7: 15, 8: 12, 9: 12, 10: 15, 11: 15,
            # 점심 (활동적) - 낮은 강도
            12: 10, 13: 10, 14: 12, 15: 12, 16: 15, 17: 15,
            # 저녁 (보통) - 중간 강도
            18: 15, 19: 15, 20: 12, 21: 12, 22: 20, 23: 25
        }
        
        # 종료 시그널 핸들러
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """종료 시그널 처리"""
        logger.info("🛑 종료 시그널 수신. 안전하게 종료 중...")
        self.is_running = False
        self.save_daily_stats()
        sys.exit(0)

    def get_current_target_count(self) -> int:
        """현재 시간대에 맞는 수집 목표 개수 계산"""
        current_hour = datetime.now().hour
        base_count = self.hourly_intensity.get(current_hour, 15)
        
        # 일일 목표 달성도에 따른 조정
        progress = self.daily_collected / self.daily_target
        
        if progress < 0.3:  # 30% 미만이면 증가
            base_count = int(base_count * 1.2)
        elif progress > 0.8:  # 80% 이상이면 감소
            base_count = int(base_count * 0.8)
        
        # 하루 남은 시간 고려
        remaining_hours = 24 - datetime.now().hour
        remaining_target = self.daily_target - self.daily_collected
        
        if remaining_hours > 0 and remaining_target > 0:
            recommended = remaining_target // (remaining_hours * 12)  # 시간당 12회 실행
            base_count = min(base_count, max(recommended, 5))
        
        return max(base_count, 3)  # 최소 3개

    def reset_daily_stats(self):
        """일일 통계 초기화"""
        today = datetime.now().date()
        if today != self.last_reset_date:
            logger.info(f"📅 새로운 날짜: {today}. 일일 통계 초기화")
            
            # 어제 결과 저장
            if self.daily_collected > 0:
                self.save_daily_stats()
            
            self.daily_collected = 0
            self.last_reset_date = today

    def save_daily_stats(self):
        """일일 통계 저장"""
        stats_file = f"/home/ubuntu/logs/dream_collection_daily_{self.last_reset_date}.json"
        
        daily_stats = {
            "date": str(self.last_reset_date),
            "target": self.daily_target,
            "collected": self.daily_collected,
            "achievement_rate": (self.daily_collected / self.daily_target * 100) if self.daily_target > 0 else 0,
            "total_batches": self.collection_stats['total_batches'],
            "success_batches": self.collection_stats['success_batches'],
            "success_rate": (self.collection_stats['success_batches'] / max(self.collection_stats['total_batches'], 1) * 100),
            "average_per_batch": self.collection_stats['average_per_batch'],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(daily_stats, f, ensure_ascii=False, indent=2)
            logger.info(f"📊 일일 통계 저장 완료: {daily_stats['achievement_rate']:.1f}% ({self.daily_collected}/{self.daily_target})")
        except Exception as e:
            logger.error(f"❌ 통계 저장 실패: {e}")

    def collect_batch_job(self):
        """5분마다 실행되는 배치 수집 작업"""
        if not self.is_running:
            return
            
        self.reset_daily_stats()
        
        # 목표 달성 확인
        if self.daily_collected >= self.daily_target:
            logger.info(f"🎉 일일 목표 달성! ({self.daily_collected}/{self.daily_target})")
            return
        
        # 현재 시간대 수집 목표 계산
        target_count = self.get_current_target_count()
        
        logger.info(f"🎯 배치 수집 시작: 목표 {target_count}개 (일일: {self.daily_collected}/{self.daily_target})")
        
        try:
            # 배치 수집 실행
            result = self.collector.collect_batch(target_count)
            
            # 통계 업데이트
            self.collection_stats['total_batches'] += 1
            collected = result.get('collected', 0)
            
            if collected > 0:
                self.collection_stats['success_batches'] += 1
                self.daily_collected += collected
                self.collection_stats['total_collected'] += collected
                
                # 평균 계산
                self.collection_stats['average_per_batch'] = (
                    self.collection_stats['total_collected'] / 
                    max(self.collection_stats['success_batches'], 1)
                )
            
            # 결과 로깅
            success_rate = result.get('success_rate', 0)
            elapsed = result.get('elapsed_seconds', 0)
            
            logger.info(f"✅ 배치 완료: {collected}/{target_count}개 수집 "
                       f"({success_rate:.1f}%, {elapsed:.1f}초) "
                       f"일일진행: {self.daily_collected}/{self.daily_target} "
                       f"({self.daily_collected/self.daily_target*100:.1f}%)")
                       
        except Exception as e:
            logger.error(f"❌ 배치 수집 오류: {e}")
            self.collection_stats['total_batches'] += 1

    def get_database_status(self) -> dict:
        """데이터베이스 현재 상태 조회"""
        try:
            result = subprocess.run([
                'sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-t', '-c',
                "SELECT COUNT(*) FROM dream_raw_collection WHERE source_site = 'smart_keyword_search';"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                keyword_count = int(result.stdout.strip())
            else:
                keyword_count = 0
                
            # 전체 데이터 수
            result = subprocess.run([
                'sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-t', '-c',
                "SELECT COUNT(*) FROM dream_raw_collection;"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                total_count = int(result.stdout.strip())
            else:
                total_count = 0
                
            return {
                'keyword_based_count': keyword_count,
                'total_count': total_count,
                'keyword_percentage': (keyword_count / max(total_count, 1) * 100)
            }
            
        except Exception as e:
            logger.error(f"DB 상태 조회 실패: {e}")
            return {'keyword_based_count': 0, 'total_count': 0, 'keyword_percentage': 0}

    def print_status_report(self):
        """30분마다 상태 리포트 출력"""
        db_status = self.get_database_status()
        
        report = f"""
🔍 스마트 키워드 수집 현황 리포트
════════════════════════════════════
📅 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}
🎯 일일 목표: {self.daily_collected:,}/{self.daily_target:,}개 ({self.daily_collected/self.daily_target*100:.1f}%)
📊 배치 통계: {self.collection_stats['success_batches']}/{self.collection_stats['total_batches']}회 성공
📈 배치당 평균: {self.collection_stats['average_per_batch']:.1f}개
💾 DB 현황: 키워드기반 {db_status['keyword_based_count']:,}개 / 전체 {db_status['total_count']:,}개
🔄 다음 목표: {self.get_current_target_count()}개 (현재 시간대 기준)
════════════════════════════════════
        """
        
        logger.info(report)

    def start(self):
        """스케줄러 시작"""
        logger.info("🚀 꿈풀이 스마트 수집 스케줄러 시작")
        logger.info(f"📊 설정: 5분 간격, 일일 {self.daily_target:,}개 목표")
        
        # 스케줄 등록
        schedule.every(5).minutes.do(self.collect_batch_job)  # 5분마다 수집
        schedule.every(30).minutes.do(self.print_status_report)  # 30분마다 리포트
        schedule.every().day.at("00:00").do(self.save_daily_stats)  # 자정에 통계 저장
        
        # 초기 상태 리포트
        self.print_status_report()
        
        # 메인 루프
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(30)  # 30초마다 스케줄 체크
            except KeyboardInterrupt:
                logger.info("🛑 사용자 중단 요청")
                break
            except Exception as e:
                logger.error(f"⚠️ 스케줄러 오류: {e}")
                time.sleep(60)  # 1분 대기 후 재시도
        
        logger.info("🏁 스케줄러 종료")
        self.save_daily_stats()

def main():
    """메인 함수"""
    scheduler = DreamCollectionScheduler()
    
    try:
        # 즉시 테스트 실행
        logger.info("🧪 즉시 테스트 배치 실행...")
        scheduler.collect_batch_job()
        
        # 스케줄러 시작
        scheduler.start()
        
    except Exception as e:
        logger.error(f"❌ 시스템 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()