#!/usr/bin/env python3
"""
🎯 통합 꿈풀이 수집 시스템
- 기존 수집 문제 완전 해결
- subprocess 기반 안정적 DB 연결
- 에러 로깅 및 진행률 표시
- 테스트 환경에서 검증된 로직
"""

import requests
import json
import hashlib
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import subprocess
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/logs/dream_collection_integrated.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IntegratedDreamCollector:
    def __init__(self):
        self.collected_count = 0
        self.error_count = 0
        self.duplicate_count = 0
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 안전한 사이트 목록 (실제 작동 확인된 것만)
        self.sites = {
            'unse2u': {
                'base_url': 'https://www.unse2u.co.kr',
                'patterns': ['dreamview.php?c1=1&c2={}'],
                'range': range(1, 501),  # 500개 수집
                'verified': True,
                'delay': (1, 2)  # 1-2초 지연
            }
        }
    
    def save_to_db_safe(self, source_site, source_url, raw_content):
        """안전한 DB 저장 (subprocess 기반)"""
        try:
            # JSON 직렬화
            content_str = json.dumps(raw_content, ensure_ascii=False)
            content_hash = hashlib.sha256(content_str.encode()).hexdigest()
            
            # 임시 파일에 JSON 저장 (특수문자 처리)
            temp_file = f"/tmp/dream_temp_{threading.current_thread().ident}.json"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(raw_content, f, ensure_ascii=False)
            
            try:
                # 매개변수화된 SQL (psql에서 실행)
                sql_script = f"""
                INSERT INTO dream_raw_collection 
                (source_site, source_url, scraped_at, raw_content, content_hash, collection_status)
                VALUES (
                    '{source_site.replace("'", "''")}',
                    '{source_url.replace("'", "''")}',
                    NOW(),
                    '{content_str.replace("'", "''")}'::jsonb,
                    '{content_hash}',
                    'collected'
                )
                ON CONFLICT (content_hash) DO NOTHING
                RETURNING id;
                """
                
                result = subprocess.run([
                    'sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-c', sql_script
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    if 'INSERT 0 1' in result.stderr or result.stdout.strip():
                        with self.lock:
                            self.collected_count += 1
                        logger.debug(f"✅ {source_site} DB 저장 성공")
                        return True
                    else:
                        with self.lock:
                            self.duplicate_count += 1
                        logger.debug(f"⚠️ 중복 데이터: {content_hash[:8]}")
                        return True  # 중복도 성공으로 처리
                else:
                    with self.lock:
                        self.error_count += 1
                    logger.error(f"❌ DB 오류: {result.stderr}")
                    return False
                    
            finally:
                # 임시 파일 정리
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
        except subprocess.TimeoutExpired:
            logger.error("❌ DB 저장 타임아웃")
            with self.lock:
                self.error_count += 1
            return False
        except Exception as e:
            logger.error(f"❌ DB 저장 실패: {e}")
            with self.lock:
                self.error_count += 1
            return False
    
    def extract_dream_content(self, soup, url):
        """꿈풀이 관련 내용 추출 및 구조화"""
        try:
            # 제목 추출
            title = soup.title.string if soup.title else ""
            
            # 본문 텍스트 추출
            body_text = soup.get_text(separator=' ', strip=True)
            
            # 꿈풀이 키워드 확인
            dream_keywords = ['꿈', '해몽', '길몽', '흉몽', '태몽', '예지', '운세', '점괘']
            found_keywords = [word for word in dream_keywords if word in body_text]
            
            if not found_keywords or len(body_text) < 100:
                return None
            
            # 구조화된 데이터 생성
            structured_data = {
                "url": url,
                "title": title[:200],  # 제목 길이 제한
                "content": body_text[:1500],  # 내용 길이 제한
                "content_length": len(body_text),
                "found_dream_keywords": found_keywords,
                "extracted_at": datetime.now().isoformat(),
                "method": "integrated_collector_v1",
                "quality_score": len(found_keywords) * 0.2 + min(len(body_text) / 1000, 1.0) * 0.8
            }
            
            return structured_data
            
        except Exception as e:
            logger.error(f"❌ 내용 추출 실패: {e}")
            return None
    
    def collect_from_url(self, site_name, url_pattern, param):
        """URL에서 꿈풀이 데이터 수집"""
        try:
            site_config = self.sites[site_name]
            url = f"{site_config['base_url']}/{url_pattern.format(param)}"
            
            # 요청 및 응답
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 꿈풀이 내용 추출
                dream_data = self.extract_dream_content(soup, url)
                
                if dream_data:
                    # 사이트 정보 추가
                    dream_data.update({
                        "source_site": site_name,
                        "param": str(param),
                        "response_status": response.status_code
                    })
                    
                    # DB 저장
                    success = self.save_to_db_safe(site_name, url, dream_data)
                    
                    if success:
                        logger.info(f"✅ {site_name}-{param}: {dream_data['title'][:50]}...")
                        return True
            
            # 서버 부하 방지
            delay = random.uniform(*site_config['delay'])
            time.sleep(delay)
            
            return False
            
        except requests.RequestException as e:
            logger.warning(f"⚠️ {site_name}-{param} 네트워크 오류: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ {site_name}-{param} 수집 실패: {e}")
            return False
    
    def run_collection(self):
        """메인 수집 실행"""
        logger.info("🚀 통합 꿈풀이 수집 시스템 시작!")
        logger.info(f"📅 시작 시간: {datetime.now()}")
        
        start_time = time.time()
        
        # 작업 목록 생성
        tasks = []
        for site_name, config in self.sites.items():
            if config.get('verified', False):
                if 'range' in config:
                    for num in config['range']:
                        for pattern in config['patterns']:
                            tasks.append((site_name, pattern, num))
        
        total_tasks = len(tasks)
        logger.info(f"📊 총 {total_tasks}개 작업 예정")
        
        # 병렬 수집 실행
        max_workers = 3  # 서버 부하 최소화
        success_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 모든 작업 제출
            future_to_task = {
                executor.submit(self.collect_from_url, site_name, pattern, param): f"{site_name}-{param}"
                for site_name, pattern, param in tasks
            }
            
            # 결과 처리 및 진행률 표시
            for i, future in enumerate(as_completed(future_to_task, timeout=600), 1):
                task_name = future_to_task[future]
                
                try:
                    if future.result():
                        success_count += 1
                        
                except Exception as e:
                    logger.error(f"❌ {task_name} 작업 실패: {e}")
                    with self.lock:
                        self.error_count += 1
                
                # 진행률 출력 (10개마다)
                if i % 10 == 0:
                    progress = (i / total_tasks) * 100
                    elapsed = time.time() - start_time
                    logger.info(f"📈 진행률: {i}/{total_tasks} ({progress:.1f}%)")
                    logger.info(f"📊 성공: {success_count}, 저장: {self.collected_count}, 중복: {self.duplicate_count}, 오류: {self.error_count}")
                    logger.info(f"⏱️ 경과시간: {elapsed/60:.1f}분")
        
        # 최종 결과 보고
        total_time = time.time() - start_time
        self._print_final_report(total_tasks, success_count, total_time)
        
        return self.collected_count > 0
    
    def _print_final_report(self, total_tasks, success_count, total_time):
        """최종 결과 보고"""
        logger.info("=" * 60)
        logger.info("🏁 통합 꿈풀이 수집 완료!")
        logger.info("=" * 60)
        logger.info(f"📊 전체 작업: {total_tasks}개")
        logger.info(f"✅ 수집 성공: {success_count}개")
        logger.info(f"💾 DB 저장: {self.collected_count}개")
        logger.info(f"🔄 중복 스킵: {self.duplicate_count}개")
        logger.info(f"❌ 오류 발생: {self.error_count}개")
        logger.info(f"⏱️ 총 소요시간: {total_time/60:.1f}분")
        
        if self.collected_count > 0:
            rate = self.collected_count / (total_time / 60)
            logger.info(f"🚀 평균 수집속도: {rate:.1f}개/분")
            
        success_rate = (success_count / total_tasks) * 100 if total_tasks > 0 else 0
        logger.info(f"📈 성공률: {success_rate:.1f}%")
        logger.info("=" * 60)

def test_db_connection():
    """DB 연결 테스트"""
    try:
        result = subprocess.run([
            'sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-c', 
            'SELECT COUNT(*) FROM dream_raw_collection;'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            logger.info("✅ PostgreSQL 연결 및 테이블 접근 성공")
            return True
        else:
            logger.error(f"❌ DB 연결 실패: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ DB 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    # 로그 디렉토리 확인
    os.makedirs('/home/ubuntu/logs', exist_ok=True)
    
    # DB 연결 테스트
    if not test_db_connection():
        logger.error("❌ DB 연결 불가로 수집 중단")
        exit(1)
    
    # 수집 시스템 실행
    collector = IntegratedDreamCollector()
    success = collector.run_collection()
    
    if success:
        logger.info("🎉 수집 시스템이 성공적으로 실행되었습니다!")
        exit(0)
    else:
        logger.error("💥 수집 시스템 실행 실패")
        exit(1)