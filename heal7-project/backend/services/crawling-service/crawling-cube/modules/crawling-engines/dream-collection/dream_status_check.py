#!/usr/bin/env python3
"""
꿈풀이 시스템 상태 확인 스크립트
원시 데이터 수집부터 구조화된 해석까지 전체 현황 확인
"""

import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_query(query: str) -> str:
    """PostgreSQL 쿼리 실행"""
    result = subprocess.run(['sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-c', query], 
                          capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else f"오류: {result.stderr}"

def main():
    """메인 상태 확인 함수"""
    print("=" * 80)
    print(" 🌙 꿈풀이 데이터 수집 & 분류 시스템 현황")
    print("=" * 80)
    
    # 1. 원시 데이터 현황
    print("\n📦 원시 데이터 수집 현황")
    print("-" * 40)
    
    total_raw = run_query("SELECT COUNT(*) as total FROM dream_raw_collection;")
    print(f"총 원시 데이터: {total_raw}")
    
    by_status = run_query("""
        SELECT processing_status, COUNT(*) 
        FROM dream_raw_collection 
        GROUP BY processing_status 
        ORDER BY processing_status;
    """)
    print(f"처리 상태별 현황:\n{by_status}")
    
    by_site = run_query("""
        SELECT source_site, COUNT(*) as count 
        FROM dream_raw_collection 
        GROUP BY source_site 
        ORDER BY count DESC;
    """)
    print(f"사이트별 수집 현황:\n{by_site}")
    
    # 2. 구조화된 해석 데이터 현황
    print("\n🔮 구조화된 해석 데이터 현황")
    print("-" * 40)
    
    total_interpretations = run_query("SELECT COUNT(*) as total FROM dream_interpretations;")
    print(f"총 해석 데이터: {total_interpretations}")
    
    by_category = run_query("""
        SELECT dc.korean_name as category, COUNT(di.id) as count 
        FROM dream_interpretations di 
        LEFT JOIN dream_categories dc ON di.category_id = dc.id 
        GROUP BY dc.korean_name 
        ORDER BY count DESC;
    """)
    print(f"카테고리별 현황:\n{by_category}")
    
    by_fortune = run_query("""
        SELECT fortune_aspect, COUNT(*) as count 
        FROM dream_interpretations 
        GROUP BY fortune_aspect;
    """)
    print(f"길흉별 현황:\n{by_fortune}")
    
    # 3. 품질 분포
    print("\n⭐ 데이터 품질 분포")
    print("-" * 40)
    
    quality_dist = run_query("""
        SELECT 
            CASE 
                WHEN confidence_score >= 0.8 THEN 'High (0.8+)'
                WHEN confidence_score >= 0.6 THEN 'Medium (0.6-0.8)'
                ELSE 'Low (<0.6)'
            END as quality_level,
            COUNT(*) as count,
            ROUND(AVG(confidence_score)::numeric, 3) as avg_confidence
        FROM dream_interpretations 
        GROUP BY 
            CASE 
                WHEN confidence_score >= 0.8 THEN 'High (0.8+)'
                WHEN confidence_score >= 0.6 THEN 'Medium (0.6-0.8)'
                ELSE 'Low (<0.6)'
            END
        ORDER BY avg_confidence DESC;
    """)
    print(f"품질 분포:\n{quality_dist}")
    
    # 4. 최근 처리된 데이터 샘플
    print("\n📝 최근 처리된 데이터 (샘플)")
    print("-" * 40)
    
    recent_samples = run_query("""
        SELECT 
            di.id,
            di.keyword,
            dc.korean_name as category,
            di.fortune_aspect,
            ROUND(di.confidence_score::numeric, 2) as confidence,
            di.data_source
        FROM dream_interpretations di
        LEFT JOIN dream_categories dc ON di.category_id = dc.id
        ORDER BY di.id DESC
        LIMIT 10;
    """)
    print(recent_samples)
    
    # 5. 시스템 통계 요약
    print("\n📊 시스템 통계 요약")
    print("-" * 40)
    
    # 처리율 계산
    try:
        result = subprocess.run(['sudo', '-u', 'postgres', 'psql', '-d', 'heal7', '-c', 
                               """SELECT 
                                    (SELECT COUNT(*) FROM dream_raw_collection) as raw_total,
                                    (SELECT COUNT(*) FROM dream_interpretations) as processed_total;"""], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if '|' in line and any(c.isdigit() for c in line):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 2:
                        try:
                            raw_total = int(parts[0])
                            processed_total = int(parts[1])
                            processing_rate = (processed_total / raw_total * 100) if raw_total > 0 else 0
                            
                            print(f"원시 데이터: {raw_total}개")
                            print(f"처리 완료: {processed_total}개")
                            print(f"처리율: {processing_rate:.1f}%")
                            
                            # 목표 달성률 (10,000개 목표)
                            target = 10000
                            achievement_rate = (processed_total / target * 100) if target > 0 else 0
                            print(f"목표 달성률: {achievement_rate:.2f}% (목표: {target:,}개)")
                            break
                        except (ValueError, ZeroDivisionError):
                            continue
    except Exception as e:
        print(f"통계 계산 오류: {e}")
    
    print("\n" + "=" * 80)
    print("🎯 다음 단계: 더 많은 웹사이트에서 대량 수집 후 분류 진행")
    print("=" * 80)

if __name__ == "__main__":
    main()