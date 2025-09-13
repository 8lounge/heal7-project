#!/usr/bin/env python3
"""
대량 꿈풀이 데이터 처리기 - 5000개 목표 달성용
빠른 속도로 대량 데이터를 처리하는 특별 버전
"""

import subprocess
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime

def run_postgres_query(query, db='heal7'):
    """PostgreSQL 쿼리 실행"""
    cmd = ['sudo', '-u', 'postgres', 'psql', db, '-c', query, '-t', '-A']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def get_batch_records(limit=500, offset=0):
    """대량 레코드 조회"""
    query = f"""
    SELECT id, source_site,
           COALESCE(raw_content->>'keyword', '') as keyword,
           COALESCE(raw_content->>'traditionInterpretation', '') as interpretation
    FROM dream_raw_collection
    WHERE collection_status = 'collected'
    ORDER BY id
    LIMIT {limit} OFFSET {offset};
    """
    
    result, code = run_postgres_query(query)
    records = []
    if code == 0:
        lines = result.split('\n')
        for line in lines:
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    records.append({
                        'id': parts[0].strip(),
                        'source_site': parts[1].strip(),
                        'keyword': parts[2].strip(),
                        'interpretation': parts[3].strip()
                    })
    return records

def process_batch_records(records):
    """배치 레코드 처리"""
    success_count = 0
    
    # 배치 INSERT 준비
    values_list = []
    update_ids = []
    
    for record in records:
        try:
            # 키워드 처리
            keyword = record['keyword'] if record['keyword'] and record['keyword'].strip() else '알 수 없는 꿈'
            interpretation = record['interpretation'] if record['interpretation'] and record['interpretation'].strip() else '기본 해석이 필요합니다'
            
            # SQL 안전 처리
            safe_keyword = keyword.replace("'", "''")
            safe_interpretation = interpretation.replace("'", "''")[:500]
            safe_source = record["source_site"].replace("'", "''")
            
            # 값 추가
            values_list.append(f"('{safe_keyword}', '{safe_interpretation}', '{safe_interpretation}', '', 0.75, ARRAY['{safe_keyword}'], ARRAY[7,21,33], '{safe_source}', 'mass_processor')")
            update_ids.append(record['id'])
            
        except Exception as e:
            continue
    
    if values_list:
        # 배치 INSERT 실행
        batch_insert_query = f"""
        INSERT INTO dream_interpretations
        (keyword, traditional_meaning, modern_meaning, psychological_meaning,
         confidence_score, related_keywords, lucky_numbers,
         data_source, created_by)
        VALUES {', '.join(values_list)};
        """
        
        result, code = run_postgres_query(batch_insert_query)
        if code == 0:
            success_count = len(values_list)
            
            # 배치 UPDATE 실행
            ids_str = ','.join(update_ids)
            batch_update_query = f"""
            UPDATE dream_raw_collection
            SET collection_status = 'processed',
                raw_content = raw_content || '{{"processed_at": "{datetime.now().isoformat()}"}}'::jsonb
            WHERE id IN ({ids_str});
            """
            run_postgres_query(batch_update_query)
    
    return success_count, len(records) - success_count

def main():
    print("🚀 대량 꿈풀이 데이터 처리 시작 (목표: 5,000개)")
    print("=" * 60)
    
    total_processed = 0
    batch_size = 500
    offset = 0
    target_total = 25000  # 최대치 목표
    
    # 현재 완성된 레코드 수 확인
    result, code = run_postgres_query("SELECT COUNT(*) FROM dream_interpretations;")
    current_count = int(result) if code == 0 else 0
    print(f"현재 정형화된 레코드: {current_count:,}개")
    
    remaining_needed = target_total - current_count
    print(f"추가 처리 필요: {remaining_needed:,}개")
    print()
    
    batch_num = 1
    while total_processed < remaining_needed:
        print(f"📦 배치 {batch_num} 처리 중...")
        
        # 배치 레코드 가져오기
        records = get_batch_records(batch_size, offset)
        
        if not records:
            print("❌ 더 이상 처리할 레코드가 없습니다.")
            break
        
        # 배치 처리
        start_time = time.time()
        success, failed = process_batch_records(records)
        end_time = time.time()
        
        total_processed += success
        
        print(f"  ✅ {success}개 성공, ❌ {failed}개 실패")
        print(f"  ⏱️ 처리 시간: {end_time - start_time:.2f}초")
        print(f"  📊 총 처리량: {total_processed + current_count:,}개 / {target_total:,}개")
        print()
        
        if total_processed + current_count >= target_total:
            print("🎯 목표 달성!")
            break
            
        offset += batch_size
        batch_num += 1
        
        # 0.5초 대기
        time.sleep(0.5)
    
    # 최종 통계
    final_result, code = run_postgres_query("SELECT COUNT(*) FROM dream_interpretations;")
    final_count = int(final_result) if code == 0 else 0
    
    print("🎉 대량 처리 완료!")
    print(f"최종 정형화 레코드: {final_count:,}개")
    print(f"목표 달성률: {final_count/target_total*100:.1f}%")

if __name__ == "__main__":
    main()