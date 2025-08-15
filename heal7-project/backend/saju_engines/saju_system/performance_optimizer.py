#!/usr/bin/env python3
"""
사주 시스템 성능 최적화 설계
REDIS/PostgreSQL/SQLite/파일시스템 통합 아키텍처

최적화 전략:
1. 메모리 캐시 (REDIS) - 자주 조회되는 계산 결과
2. 관계형 DB (PostgreSQL) - 사용자 데이터, 통계
3. 로컬 DB (SQLite) - 사용량 추적, 임시 데이터  
4. 파일 시스템 - 명리학 상수, 로직 방정식
"""

import json
import sqlite3
import redis
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pickle
import hashlib
import logging

from .myeongrihak_constants import CHEONGAN, JIJI

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """다층 캐시 및 성능 최적화 시스템"""
    
    def __init__(self):
        # 캐시 레이어 설정
        self.redis_client = None
        self.sqlite_path = "/tmp/saju_cache.db"
        self.constants_path = "/home/ubuntu/project/backend/api/saju_system/constants"
        
        # 캐시 TTL 설정
        self.cache_ttl = {
            "saju_result": 86400,      # 사주 결과: 24시간
            "lunar_conversion": 2592000, # 음력 변환: 30일
            "frequent_dates": 604800,   # 자주 사용 날짜: 7일  
            "system_stats": 3600       # 시스템 통계: 1시간
        }
        
        self._init_cache_systems()
        self._load_constants()
    
    def _init_cache_systems(self):
        """캐시 시스템 초기화"""
        
        # Redis 연결 시도
        try:
            self.redis_client = redis.Redis(
                host='localhost', 
                port=6379, 
                db=0, 
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.redis_client.ping()
            logger.info("✅ Redis 캐시 연결 성공")
            self.redis_available = True
        except Exception as e:
            logger.warning(f"⚠️ Redis 연결 실패: {e}")
            self.redis_available = False
        
        # SQLite 로컬 캐시 초기화
        try:
            with sqlite3.connect(self.sqlite_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS saju_cache (
                        cache_key TEXT PRIMARY KEY,
                        data BLOB NOT NULL,
                        created_at TEXT NOT NULL,
                        expires_at TEXT NOT NULL,
                        access_count INTEGER DEFAULT 1,
                        last_accessed TEXT NOT NULL
                    )
                ''')
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_expires_at ON saju_cache(expires_at)
                ''')
                conn.commit()
                logger.info("✅ SQLite 캐시 초기화 완료")
        except Exception as e:
            logger.error(f"❌ SQLite 초기화 실패: {e}")
    
    def _load_constants(self):
        """명리학 상수 파일 로드"""
        
        constants_dir = Path(self.constants_path)
        constants_dir.mkdir(exist_ok=True)
        
        # 상수 파일들이 없으면 생성
        self._ensure_constants_files()
        
        try:
            # 60갑자 로드
            with open(constants_dir / "gapja_60.json", "r", encoding="utf-8") as f:
                self.gapja_60 = json.load(f)
            
            # 지장간 로드  
            with open(constants_dir / "jijanggan.json", "r", encoding="utf-8") as f:
                self.jijanggan_data = json.load(f)
            
            # 시두법 로드
            with open(constants_dir / "sidubeop.json", "r", encoding="utf-8") as f:
                self.sidubeop_data = json.load(f)
            
            # 계산 공식 로드
            with open(constants_dir / "calculation_formulas.json", "r", encoding="utf-8") as f:
                self.formulas = json.load(f)
                
            logger.info("✅ 명리학 상수 파일 로드 완료")
            
        except Exception as e:
            logger.error(f"❌ 상수 파일 로드 실패: {e}")
            self._fallback_to_hardcoded()
    
    def _ensure_constants_files(self):
        """상수 파일들이 없으면 생성"""
        
        constants_dir = Path(self.constants_path)
        
        # 60갑자 생성
        gapja_file = constants_dir / "gapja_60.json"
        if not gapja_file.exists():
            gapja_60 = []
            for i in range(60):
                cheongan = CHEONGAN[i % 10]
                jiji = JIJI[i % 12]
                gapja_60.append({
                    "index": i,
                    "gapja": cheongan + jiji,
                    "cheongan": cheongan,
                    "jiji": jiji,
                    "cheongan_index": i % 10,
                    "jiji_index": i % 12
                })
            
            with open(gapja_file, "w", encoding="utf-8") as f:
                json.dump(gapja_60, f, ensure_ascii=False, indent=2)
        
        # 지장간 데이터 생성
        jijanggan_file = constants_dir / "jijanggan.json"
        if not jijanggan_file.exists():
            from .myeongrihak_constants import JIJANGGAN
            
            jijanggan_formatted = {}
            for jiji, data in JIJANGGAN.items():
                jijanggan_formatted[jiji] = [
                    {"gan": gan, "ratio": ratio} for gan, ratio in data
                ]
            
            with open(jijanggan_file, "w", encoding="utf-8") as f:
                json.dump(jijanggan_formatted, f, ensure_ascii=False, indent=2)
        
        # 시두법 데이터 생성
        sidubeop_file = constants_dir / "sidubeop.json"
        if not sidubeop_file.exists():
            # 시두법 공식 및 규칙
            sidubeop_data = {
                "description": "시두법 - 일간에 따른 시천간 결정법",
                "formula": "각 일간별로 자시부터 시작하는 천간 순서 정의",
                "rules": {
                    "甲": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],
                    "己": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],
                    "乙": ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],
                    "庚": ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],
                    "丙": ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],
                    "辛": ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],
                    "丁": ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
                    "壬": ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
                    "戊": ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
                    "癸": ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
                },
                "time_mapping": {
                    "자시": {"index": 0, "time_range": "23:30-01:30"},
                    "축시": {"index": 1, "time_range": "01:30-03:30"},
                    "인시": {"index": 2, "time_range": "03:30-05:30"},
                    "묘시": {"index": 3, "time_range": "05:30-07:30"},
                    "진시": {"index": 4, "time_range": "07:30-09:30"},
                    "사시": {"index": 5, "time_range": "09:30-11:30"},
                    "오시": {"index": 6, "time_range": "11:30-13:30"},
                    "미시": {"index": 7, "time_range": "13:30-15:30"},
                    "신시": {"index": 8, "time_range": "15:30-17:30"},
                    "유시": {"index": 9, "time_range": "17:30-19:30"},
                    "술시": {"index": 10, "time_range": "19:30-21:30"},
                    "해시": {"index": 11, "time_range": "21:30-23:30"}
                }
            }
            
            with open(sidubeop_file, "w", encoding="utf-8") as f:
                json.dump(sidubeop_data, f, ensure_ascii=False, indent=2)
        
        # 계산 공식 생성
        formulas_file = constants_dir / "calculation_formulas.json"
        if not formulas_file.exists():
            calculation_formulas = {
                "일주_계산": {
                    "description": "일진 계산 공식",
                    "base_formula": "(기준일_갑자_인덱스 + 날짜차이) % 60",
                    "reference_points": [
                        {
                            "date": "1985-02-24",
                            "gapja": "甲午",
                            "index": 30,
                            "verified": "KASI_API"
                        },
                        {
                            "date": "1955-05-06", 
                            "gapja": "丁卯",
                            "index": 3,
                            "verified": "KASI_API"
                        }
                    ],
                    "corrections": {
                        "solar_time": -32,
                        "description": "진태양시 보정 (한국 경도 127도 기준)"
                    }
                },
                "월주_계산": {
                    "description": "월주 계산 - 24절기 기준",
                    "formula": "절기 기준으로 월 천간 결정",
                    "base_rule": "년간에 따른 월간 시작점 결정"
                },
                "년주_계산": {
                    "description": "년주 계산 - 입춘 기준",
                    "formula": "입춘 이전은 전년도 간지 사용",
                    "base_year": "서기 4년을 갑자년으로 설정"
                },
                "시주_계산": {
                    "description": "시주 계산 - 시두법 적용",
                    "formula": "일간에 따른 시천간 배열 + 시지 결정",
                    "time_correction": "진태양시 기준으로 시간 보정"
                }
            }
            
            with open(formulas_file, "w", encoding="utf-8") as f:
                json.dump(calculation_formulas, f, ensure_ascii=False, indent=2)
    
    def _fallback_to_hardcoded(self):
        """파일 로드 실패 시 하드코딩 폴백"""
        
        logger.warning("⚠️ 파일 로드 실패 - 하드코딩 데이터 사용")
        
        # 기본 60갑자
        self.gapja_60 = []
        for i in range(60):
            cheongan = CHEONGAN[i % 10]
            jiji = JIJI[i % 12]
            self.gapja_60.append({
                "index": i,
                "gapja": cheongan + jiji,
                "cheongan": cheongan,
                "jiji": jiji
            })
    
    def generate_cache_key(self, **kwargs) -> str:
        """캐시 키 생성"""
        
        # 정렬된 키-값으로 일관된 해시 생성
        sorted_items = sorted(kwargs.items())
        data_string = json.dumps(sorted_items, sort_keys=True)
        return hashlib.md5(data_string.encode()).hexdigest()
    
    def get_from_cache(self, cache_key: str, cache_type: str = "saju_result") -> Optional[Any]:
        """다층 캐시에서 데이터 조회"""
        
        # 1순위: Redis 캐시
        if self.redis_available:
            try:
                data = self.redis_client.get(f"saju:{cache_key}")
                if data:
                    logger.debug(f"📦 Redis 캐시 히트: {cache_key}")
                    return json.loads(data)
            except Exception as e:
                logger.warning(f"Redis 조회 오류: {e}")
        
        # 2순위: SQLite 로컬 캐시
        try:
            with sqlite3.connect(self.sqlite_path) as conn:
                cursor = conn.execute('''
                    SELECT data, expires_at FROM saju_cache 
                    WHERE cache_key = ? AND expires_at > ?
                ''', (cache_key, datetime.now().isoformat()))
                
                row = cursor.fetchone()
                if row:
                    # 접근 카운트 업데이트
                    conn.execute('''
                        UPDATE saju_cache 
                        SET access_count = access_count + 1, last_accessed = ?
                        WHERE cache_key = ?
                    ''', (datetime.now().isoformat(), cache_key))
                    conn.commit()
                    
                    logger.debug(f"🗃️ SQLite 캐시 히트: {cache_key}")
                    return pickle.loads(row[0])
                    
        except Exception as e:
            logger.warning(f"SQLite 조회 오류: {e}")
        
        return None
    
    def set_to_cache(self, cache_key: str, data: Any, cache_type: str = "saju_result"):
        """다층 캐시에 데이터 저장"""
        
        ttl = self.cache_ttl.get(cache_type, 3600)
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        # Redis 저장
        if self.redis_available:
            try:
                self.redis_client.setex(
                    f"saju:{cache_key}",
                    ttl,
                    json.dumps(data, default=str)
                )
                logger.debug(f"💾 Redis 캐시 저장: {cache_key}")
            except Exception as e:
                logger.warning(f"Redis 저장 오류: {e}")
        
        # SQLite 저장
        try:
            with sqlite3.connect(self.sqlite_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO saju_cache
                    (cache_key, data, created_at, expires_at, last_accessed)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    cache_key,
                    pickle.dumps(data),
                    datetime.now().isoformat(),
                    expires_at.isoformat(),
                    datetime.now().isoformat()
                ))
                conn.commit()
                logger.debug(f"🗃️ SQLite 캐시 저장: {cache_key}")
        except Exception as e:
            logger.warning(f"SQLite 저장 오류: {e}")
    
    def cleanup_expired_cache(self):
        """만료된 캐시 정리"""
        
        try:
            with sqlite3.connect(self.sqlite_path) as conn:
                cursor = conn.execute('DELETE FROM saju_cache WHERE expires_at < ?', 
                                    (datetime.now().isoformat(),))
                deleted = cursor.rowcount
                conn.commit()
                
                if deleted > 0:
                    logger.info(f"🧹 만료된 캐시 {deleted}개 정리 완료")
                    
        except Exception as e:
            logger.error(f"캐시 정리 오류: {e}")
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """캐시 사용 통계"""
        
        stats = {
            "redis_status": "connected" if self.redis_available else "disconnected",
            "sqlite_status": "available",
            "cache_counts": {},
            "hit_rates": {},
            "storage_usage": {}
        }
        
        # SQLite 통계
        try:
            with sqlite3.connect(self.sqlite_path) as conn:
                # 전체 캐시 수
                cursor = conn.execute('SELECT COUNT(*) FROM saju_cache')
                stats["cache_counts"]["total"] = cursor.fetchone()[0]
                
                # 유효한 캐시 수
                cursor = conn.execute('SELECT COUNT(*) FROM saju_cache WHERE expires_at > ?', 
                                    (datetime.now().isoformat(),))
                stats["cache_counts"]["valid"] = cursor.fetchone()[0]
                
                # 자주 사용되는 캐시
                cursor = conn.execute('''
                    SELECT cache_key, access_count 
                    FROM saju_cache 
                    WHERE expires_at > ? 
                    ORDER BY access_count DESC 
                    LIMIT 10
                ''', (datetime.now().isoformat(),))
                stats["frequent_keys"] = cursor.fetchall()
                
        except Exception as e:
            logger.error(f"통계 조회 오류: {e}")
        
        return stats
    
    def optimize_performance(self) -> Dict[str, Any]:
        """성능 최적화 실행"""
        
        optimization_results = {
            "cleanup_performed": False,
            "cache_reorganized": False,
            "constants_refreshed": False,
            "recommendations": []
        }
        
        # 1. 만료된 캐시 정리
        self.cleanup_expired_cache()
        optimization_results["cleanup_performed"] = True
        
        # 2. 상수 파일 갱신 확인
        try:
            self._load_constants()
            optimization_results["constants_refreshed"] = True
        except Exception as e:
            logger.error(f"상수 갱신 실패: {e}")
        
        # 3. 성능 권장사항 생성
        stats = self.get_cache_statistics()
        
        if not self.redis_available:
            optimization_results["recommendations"].append(
                "Redis 서버 설치로 메모리 캐시 성능 향상 가능"
            )
        
        if stats["cache_counts"].get("valid", 0) < 100:
            optimization_results["recommendations"].append(
                "캐시 사용량이 적음 - 더 적극적인 캐싱 전략 고려"
            )
        
        return optimization_results


# 전역 최적화 인스턴스
performance_optimizer = PerformanceOptimizer()

def get_optimized_cache(cache_key: str, cache_type: str = "saju_result") -> Optional[Any]:
    """최적화된 캐시 조회"""
    return performance_optimizer.get_from_cache(cache_key, cache_type)

def set_optimized_cache(cache_key: str, data: Any, cache_type: str = "saju_result"):
    """최적화된 캐시 저장"""
    performance_optimizer.set_to_cache(cache_key, data, cache_type)

def generate_saju_cache_key(year: int, month: int, day: int, hour: int, minute: int, 
                           is_lunar: bool = False) -> str:
    """사주 계산용 캐시 키 생성"""
    return performance_optimizer.generate_cache_key(
        year=year, month=month, day=day, hour=hour, minute=minute, is_lunar=is_lunar
    )


if __name__ == "__main__":
    print("🚀 사주 시스템 성능 최적화 도구")
    print("=" * 50)
    
    optimizer = PerformanceOptimizer()
    
    # 시스템 상태 확인
    stats = optimizer.get_cache_statistics()
    print(f"Redis 상태: {stats['redis_status']}")
    print(f"캐시 수: {stats['cache_counts'].get('valid', 0)}/{stats['cache_counts'].get('total', 0)}")
    
    # 최적화 실행
    results = optimizer.optimize_performance()
    print(f"\n최적화 결과:")
    for key, value in results.items():
        if key != "recommendations":
            print(f"  {key}: {'✅' if value else '❌'}")
    
    if results["recommendations"]:
        print(f"\n권장사항:")
        for rec in results["recommendations"]:
            print(f"  - {rec}")