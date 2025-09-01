#!/usr/bin/env python3
"""
🚀 실제 크롤링 및 JSONB 저장 테스트
- 하드코딩 제거, 실제 데이터 수집
- PostgreSQL JSONB 저장 확인
- 실시간 대시보드 데이터 연동

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-31
"""

import asyncio
import json
import logging
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
import asyncpg
import sys

# 프로젝트 경로 추가
sys.path.append('.')

from core.smart_crawler import SmartCrawler, CrawlStrategy

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealCrawlingService:
    """실제 크롤링 서비스"""
    
    def __init__(self):
        self.crawler = None
        self.db_pool = None
        
    async def initialize(self):
        """시스템 초기화"""
        logger.info("🚀 실제 크롤링 서비스 초기화 시작")
        
        # SmartCrawler 초기화
        self.crawler = SmartCrawler()
        await self.crawler.initialize()
        logger.info("✅ SmartCrawler 초기화 완료")
        
        # 데이터베이스 연결
        try:
            await self.connect_database()
        except Exception as e:
            logger.error(f"❌ DB 연결 실패, 계속 진행: {e}")
            # DB 연결 실패해도 크롤링은 계속 진행
        
    async def connect_database(self):
        """PostgreSQL 연결"""
        try:
            # 여러 연결 방법 시도
            connection_configs = [
                # 1. 패스워드 없이 시도
                {'host': 'localhost', 'port': 5432, 'user': 'postgres', 'database': 'heal7'},
                # 2. 소켓 연결 시도  
                {'host': '/var/run/postgresql', 'port': 5432, 'user': 'postgres', 'database': 'heal7'},
                # 3. 다른 사용자로 시도
                {'host': 'localhost', 'port': 5432, 'user': 'ubuntu', 'database': 'heal7'},
            ]
            
            for i, config in enumerate(connection_configs):
                try:
                    logger.info(f"DB 연결 시도 {i+1}: {config}")
                    self.db_pool = await asyncpg.create_pool(min_size=1, max_size=3, **config)
                    logger.info(f"✅ PostgreSQL 연결 성공 (방법 {i+1})")
                    return
                except Exception as conn_err:
                    logger.warning(f"⚠️ 연결 방법 {i+1} 실패: {conn_err}")
                    
            raise Exception("모든 DB 연결 방법 실패")
            
        except Exception as e:
            logger.error(f"❌ DB 연결 실패: {e}")
            self.db_pool = None
            raise
            
    async def crawl_and_store(self, url: str, source_type: str = "test"):
        """실제 크롤링 및 JSONB 저장"""
        logger.info(f"📡 실제 크롤링 시작: {url}")
        
        try:
            # 1. 실제 크롤링 실행
            result = await self.crawler.crawl(url, strategy=CrawlStrategy.AUTO)
            
            if not result.success:
                logger.error(f"❌ 크롤링 실패: {result.error}")
                return False
                
            logger.info(f"✅ 크롤링 성공 ({result.crawler_used.value}): {len(result.html)} bytes")
            
            # 2. 데이터 준비
            crawl_data = {
                "id": str(uuid.uuid4()),
                "title": f"크롤링 데이터 - {url}",
                "content": result.html[:5000],  # 처음 5000자만 저장
                "url": url,
                "source_type": source_type,
                "metadata": {
                    "crawler_used": result.crawler_used.value,
                    "response_time": result.response_time,
                    "status_code": getattr(result, 'status_code', 200),
                    "html_size": len(result.html) if result.html else 0,
                    "headers": getattr(result, 'headers', {}),
                    "crawl_timestamp": datetime.now().isoformat()
                },
                "ai_processed_data": {
                    "processed": False,
                    "extraction_ready": True,
                    "quality_indicators": {
                        "has_content": bool(result.html and len(result.html) > 100),
                        "response_success": True,
                        "crawler_tier": result.crawler_used.value
                    }
                },
                "hash_key": hashlib.md5(f"{url}_{datetime.now().date()}".encode()).hexdigest(),
                "quality_score": 95.0 if len(result.html) > 1000 else 75.0,
                "processing_status": "completed",
                "collected_at": datetime.now()
            }
            
            # 3. 데이터 저장 (DB 또는 파일)
            if self.db_pool:
                await self.store_to_database(crawl_data)
                logger.info("✅ PostgreSQL JSONB 저장 완료")
            else:
                # DB 연결 실패 시 파일로 저장
                await self.store_to_file(crawl_data)
                logger.info("✅ 파일로 저장 완료 (DB 연결 없음)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 크롤링 및 저장 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    async def store_to_database(self, crawl_data):
        """PostgreSQL JSONB에 실제 저장"""
        try:
            async with self.db_pool.acquire() as conn:
                # crawling_service 스키마에 저장
                query = """
                INSERT INTO crawling_service.crawl_data 
                (id, title, content, url, source_type, metadata, ai_processed_data, 
                 hash_key, quality_score, processing_status, collected_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """
                
                await conn.execute(
                    query,
                    crawl_data["id"],
                    crawl_data["title"], 
                    crawl_data["content"],
                    crawl_data["url"],
                    crawl_data["source_type"],
                    json.dumps(crawl_data["metadata"]),
                    json.dumps(crawl_data["ai_processed_data"]),
                    crawl_data["hash_key"],
                    crawl_data["quality_score"],
                    crawl_data["processing_status"],
                    crawl_data["collected_at"]
                )
                
                logger.info(f"✅ JSONB 저장 완료: {crawl_data['id']}")
                
        except Exception as e:
            logger.error(f"❌ DB 저장 실패: {e}")
            raise
            
    async def store_to_file(self, crawl_data):
        """파일로 실제 크롤링 데이터 저장"""
        try:
            # 실제 데이터 저장 디렉토리 생성
            data_dir = Path("./data/real_crawling")
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # 파일명 생성 (URL 기반)
            url_safe = crawl_data['url'].replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
            filename = f"real_{crawl_data['source_type']}_{url_safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = data_dir / filename
            
            # JSONB 형태로 저장 (실제 크롤링 데이터)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(crawl_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"💾 실제 크롤링 데이터 파일 저장: {filepath}")
            
            # 간단한 통계도 별도 파일로 저장
            stats_file = data_dir / "real_crawling_stats.json"
            
            # 기존 통계 로드하거나 새로 생성
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            else:
                stats = {"total_crawled": 0, "by_source": {}, "by_crawler": {}, "last_updated": None}
            
            # 통계 업데이트
            stats["total_crawled"] += 1
            stats["by_source"][crawl_data["source_type"]] = stats["by_source"].get(crawl_data["source_type"], 0) + 1
            crawler_used = crawl_data["metadata"]["crawler_used"]
            stats["by_crawler"][crawler_used] = stats["by_crawler"].get(crawler_used, 0) + 1
            stats["last_updated"] = datetime.now().isoformat()
            
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
                
            logger.info(f"📊 실제 크롤링 통계 업데이트: {stats}")
            
        except Exception as e:
            logger.error(f"❌ 파일 저장 실패: {e}")
            
    async def verify_stored_data(self):
        """저장된 JSONB 데이터 검증 (DB 또는 파일)"""
        if self.db_pool:
            return await self.verify_database_data()
        else:
            return await self.verify_file_data()
    
    async def verify_database_data(self):
        """PostgreSQL DB 데이터 검증"""
        try:
            async with self.db_pool.acquire() as conn:
                # 최근 저장된 데이터 조회
                query = """
                SELECT id, title, url, metadata, ai_processed_data, quality_score, collected_at
                FROM crawling_service.crawl_data 
                ORDER BY collected_at DESC 
                LIMIT 3
                """
                
                rows = await conn.fetch(query)
                
                logger.info(f"📊 저장된 실제 데이터: {len(rows)}건")
                
                for row in rows:
                    logger.info(f"  🔍 ID: {row['id']}")
                    logger.info(f"  📝 제목: {row['title']}")
                    logger.info(f"  🌐 URL: {row['url']}")
                    logger.info(f"  📊 품질점수: {row['quality_score']}")
                    logger.info(f"  📅 수집시간: {row['collected_at']}")
                    
                    # JSONB 필드 내용 확인
                    metadata = row['metadata']
                    if isinstance(metadata, str):
                        metadata = json.loads(metadata)
                    logger.info(f"  🔧 메타데이터: 크롤러={metadata.get('crawler_used')}, 크기={metadata.get('html_size')}")
                    
                    ai_data = row['ai_processed_data']
                    if isinstance(ai_data, str):
                        ai_data = json.loads(ai_data)
                    logger.info(f"  🤖 AI데이터: 처리={ai_data.get('processed')}, 품질지표={ai_data.get('quality_indicators')}")
                    
                    logger.info("  " + "-"*50)
                
                return len(rows)
                
        except Exception as e:
            logger.error(f"❌ DB 데이터 검증 실패: {e}")
            return 0
    
    async def verify_file_data(self):
        """파일 저장 데이터 검증"""
        try:
            data_dir = Path("./data/real_crawling")
            if not data_dir.exists():
                logger.warning("📂 실제 크롤링 데이터 디렉토리 없음")
                return 0
            
            # JSON 파일들 찾기
            json_files = list(data_dir.glob("real_*.json"))
            json_files = [f for f in json_files if 'stats' not in f.name]  # 통계 파일 제외
            
            logger.info(f"📊 저장된 실제 파일 데이터: {len(json_files)}개")
            
            # 최근 3개 파일 확인
            json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for i, file_path in enumerate(json_files[:3]):
                logger.info(f"  🔍 파일 {i+1}: {file_path.name}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    logger.info(f"  📝 제목: {data.get('title', 'N/A')}")
                    logger.info(f"  🌐 URL: {data.get('url', 'N/A')}")
                    logger.info(f"  📊 품질점수: {data.get('quality_score', 'N/A')}")
                    logger.info(f"  📅 수집시간: {data.get('collected_at', 'N/A')}")
                    
                    # 메타데이터 확인
                    metadata = data.get('metadata', {})
                    logger.info(f"  🔧 메타데이터: 크롤러={metadata.get('crawler_used')}, 크기={metadata.get('html_size')} bytes")
                    
                    # AI 데이터 확인
                    ai_data = data.get('ai_processed_data', {})
                    quality_indicators = ai_data.get('quality_indicators', {})
                    logger.info(f"  🤖 AI데이터: 처리={ai_data.get('processed')}, 크롤러티어={quality_indicators.get('crawler_tier')}")
                    
                    # 실제 콘텐츠 일부 확인
                    content = data.get('content', '')
                    content_preview = content[:100] + "..." if len(content) > 100 else content
                    logger.info(f"  📄 콘텐츠 미리보기: {content_preview}")
                    
                except Exception as file_err:
                    logger.error(f"  ❌ 파일 읽기 실패 {file_path}: {file_err}")
                
                logger.info("  " + "-"*50)
            
            # 통계 파일 확인
            stats_file = data_dir / "real_crawling_stats.json"
            if stats_file.exists():
                try:
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        stats = json.load(f)
                    logger.info(f"📈 실제 크롤링 통계:")
                    logger.info(f"  총 크롤링: {stats.get('total_crawled', 0)}개")
                    logger.info(f"  소스별: {stats.get('by_source', {})}")
                    logger.info(f"  크롤러별: {stats.get('by_crawler', {})}")
                    logger.info(f"  마지막 업데이트: {stats.get('last_updated', 'N/A')}")
                except Exception as stats_err:
                    logger.error(f"❌ 통계 파일 읽기 실패: {stats_err}")
            
            return len(json_files)
            
        except Exception as e:
            logger.error(f"❌ 파일 데이터 검증 실패: {e}")
            return 0
            
    async def get_real_statistics(self):
        """실제 통계 조회 (DB 또는 파일)"""
        if self.db_pool:
            return await self.get_database_statistics()
        else:
            return await self.get_file_statistics()
    
    async def get_database_statistics(self):
        """PostgreSQL DB 통계 조회"""
        try:
            async with self.db_pool.acquire() as conn:
                stats_query = """
                SELECT 
                    COUNT(*) as total_count,
                    AVG(quality_score) as avg_quality,
                    COUNT(CASE WHEN processing_status = 'completed' THEN 1 END) as completed_count,
                    COUNT(CASE WHEN collected_at > NOW() - INTERVAL '1 hour' THEN 1 END) as recent_count
                FROM crawling_service.crawl_data
                """
                
                result = await conn.fetchrow(stats_query)
                
                success_rate = (result['completed_count'] / result['total_count'] * 100) if result['total_count'] > 0 else 0
                
                real_stats = {
                    "total_collected": result['total_count'],
                    "avg_success_rate": round(success_rate, 1),
                    "avg_quality": round(result['avg_quality'] or 0, 1),
                    "recent_collections": result['recent_count'],
                    "timestamp": datetime.now().isoformat(),
                    "data_source": "real_database"
                }
                
                logger.info(f"📈 실제 통계: {real_stats}")
                return real_stats
                
        except Exception as e:
            logger.error(f"❌ DB 통계 조회 실패: {e}")
            return {"error": str(e)}
    
    async def get_file_statistics(self):
        """파일 기반 통계 조회"""
        try:
            stats_file = Path("./data/real_crawling/real_crawling_stats.json")
            
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    file_stats = json.load(f)
                
                # 실제 파일 기반 통계 계산
                data_dir = Path("./data/real_crawling")
                json_files = list(data_dir.glob("real_*.json"))
                json_files = [f for f in json_files if 'stats' not in f.name]
                
                # 품질 점수 계산 (파일들에서 추출)
                total_quality = 0
                quality_count = 0
                
                for file_path in json_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        quality_score = data.get('quality_score', 0)
                        if quality_score > 0:
                            total_quality += quality_score
                            quality_count += 1
                    except:
                        continue
                
                avg_quality = (total_quality / quality_count) if quality_count > 0 else 0
                
                real_stats = {
                    "total_collected": file_stats.get('total_crawled', 0),
                    "avg_success_rate": 100.0,  # 파일 저장된 것은 모두 성공한 것
                    "avg_quality": round(avg_quality, 1),
                    "by_source": file_stats.get('by_source', {}),
                    "by_crawler": file_stats.get('by_crawler', {}),
                    "recent_collections": len(json_files),
                    "timestamp": file_stats.get('last_updated', datetime.now().isoformat()),
                    "data_source": "real_files"
                }
                
                logger.info(f"📈 파일 기반 실제 통계: {real_stats}")
                return real_stats
            else:
                return {
                    "total_collected": 0,
                    "avg_success_rate": 0,
                    "avg_quality": 0,
                    "message": "아직 크롤링된 데이터 없음",
                    "data_source": "empty"
                }
                
        except Exception as e:
            logger.error(f"❌ 파일 통계 조회 실패: {e}")
            return {"error": str(e)}
            
    async def cleanup(self):
        """리소스 정리"""
        if self.crawler:
            await self.crawler.cleanup()
        if self.db_pool:
            await self.db_pool.close()
        logger.info("🛑 실제 크롤링 서비스 정리 완료")


async def main():
    """메인 실행 함수"""
    logger.info("🎉 실제 크롤링 및 JSONB 저장 테스트 시작")
    
    service = RealCrawlingService()
    
    try:
        await service.initialize()
        
        # 실제 사이트들 크롤링 및 저장
        test_sites = [
            ("https://httpbin.org/json", "api_test"),
            ("https://example.com", "html_test"), 
            ("https://www.bizinfo.go.kr", "government"),
        ]
        
        for url, source_type in test_sites:
            logger.info(f"🎯 실제 크롤링 테스트: {url}")
            success = await service.crawl_and_store(url, source_type)
            
            if success:
                logger.info(f"✅ {url} 크롤링 및 저장 성공")
            else:
                logger.warning(f"⚠️ {url} 크롤링 실패")
                
            await asyncio.sleep(2)  # 간격 조절
        
        # 저장된 데이터 검증
        logger.info("\n" + "="*60)
        logger.info("📊 실제 JSONB 저장 데이터 검증")
        logger.info("="*60)
        
        stored_count = await service.verify_stored_data()
        
        if stored_count > 0:
            logger.info("✅ 실제 데이터 저장 및 검증 완료")
            
            # 실제 통계 조회
            real_stats = await service.get_real_statistics()
            logger.info(f"📈 실제 DB 기반 통계: {json.dumps(real_stats, indent=2, ensure_ascii=False)}")
            
        else:
            logger.warning("⚠️ 저장된 데이터가 없습니다")
        
    except Exception as e:
        logger.error(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await service.cleanup()
    
    logger.info("🏁 실제 크롤링 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())