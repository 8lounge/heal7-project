#!/usr/bin/env python3
"""
꿈풀이 다각도 해석 데이터 마이그레이션 스크립트
마크다운 문서에서 50개 키워드 × 6개 관점 해석 데이터를 PostgreSQL로 삽입
"""

import re
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
import sys

# 데이터베이스 연결 설정  
DB_CONFIG = {
    'database': 'heal7_saju',
    'user': 'ubuntu'  # 현재 시스템 사용자
}

# 카테고리 매핑
CATEGORY_MAP = {
    range(1, 21): "동물",      # 1-20: 동물
    range(21, 33): "자연현상",  # 21-32: 자연현상  
    range(33, 41): "인간관계",  # 33-40: 인간관계
    range(41, 47): "상황감정",  # 41-46: 상황/감정
    range(47, 51): "사물"       # 47-50: 사물
}

# 길흉 매핑 함수
def parse_fortune_type(text):
    """해석 텍스트에서 길흉 판별 추출"""
    if "길몽" in text and "%" in text:
        match = re.search(r'길몽\s*(\d+)%', text)
        if match:
            percentage = int(match.group(1))
            if percentage >= 80:
                return "길몽"
            elif percentage >= 60:
                return "길흉반반"
    elif "흉몽" in text and "%" in text:
        match = re.search(r'흉몽\s*(\d+)%', text)
        if match:
            percentage = int(match.group(1))
            if percentage >= 60:
                return "흉몽"
            else:
                return "길흉반반"
    elif "길흉반반" in text:
        return "길흉반반"
    else:
        return "중립"

def parse_confidence_score(text):
    """신뢰도 점수 추출"""
    match = re.search(r'신뢰도:\s*(\d+\.?\d*)', text)
    if match:
        return float(match.group(1))
    return 8.0  # 기본값

def get_category_for_id(keyword_id):
    """키워드 ID로 카테고리 반환"""
    for id_range, category in CATEGORY_MAP.items():
        if keyword_id in id_range:
            return category
    return "기타"

def extract_interpretation_data(content):
    """마크다운 텍스트에서 해석 데이터 추출"""
    data = []
    
    # 키워드 블록 패턴 매칭
    keyword_pattern = r'### [^*]+ \*\*(\d+)\. ([^(]+) \([^)]+\)\*\*\s*\n\s*\*\*키워드: "([^"]+)"\*\*\s*\n(.*?)(?=###|\Z)'
    
    matches = re.finditer(keyword_pattern, content, re.DOTALL)
    
    for match in matches:
        keyword_id = int(match.group(1))
        keyword_name = match.group(2).strip()
        keyword = match.group(3)
        interpretation_block = match.group(4)
        
        # 6개 관점 해석 추출
        perspectives = {}
        perspective_pattern = r'(\d+)\.\s+\*\*([^*]+)\*\*:\s+"([^"]+)"\s+\*\(([^)]+)\s*/\s*신뢰도:\s*(\d+\.?\d*)\)\*'
        
        perspective_matches = re.finditer(perspective_pattern, interpretation_block)
        
        for p_match in perspective_matches:
            perspective_num = int(p_match.group(1))
            perspective_name = p_match.group(2)
            interpretation_text = p_match.group(3)
            fortune_info = p_match.group(4)
            confidence = float(p_match.group(5))
            
            # 관점별 매핑
            perspective_key = None
            if perspective_num == 1 or "한국전통" in perspective_name:
                perspective_key = "korean_traditional"
            elif perspective_num == 2 or "중국전통" in perspective_name:
                perspective_key = "chinese_traditional" 
            elif perspective_num == 3 or "서구심리학" in perspective_name:
                perspective_key = "western_psychology"
            elif perspective_num == 4 or "이슬람" in perspective_name:
                perspective_key = "islamic_perspective"
            elif perspective_num == 5 or "불교" in perspective_name:
                perspective_key = "buddhist_perspective"
            elif perspective_num == 6 or "과학적" in perspective_name:
                perspective_key = "scientific_perspective"
            
            if perspective_key:
                fortune_type = parse_fortune_type(fortune_info)
                perspectives[perspective_key] = {
                    "interpretation": interpretation_text,
                    "fortune_type": fortune_type,
                    "confidence_score": confidence
                }
        
        # 평균 신뢰도 및 주요 길흉 계산
        if perspectives:
            confidence_scores = [p["confidence_score"] for p in perspectives.values()]
            average_confidence = sum(confidence_scores) / len(confidence_scores)
            
            # 주요 길흉 판별 (가장 높은 신뢰도 관점 기준)
            max_confidence_perspective = max(perspectives.values(), key=lambda x: x["confidence_score"])
            primary_fortune_type = max_confidence_perspective["fortune_type"]
            
            data.append({
                "keyword_id": keyword_id,
                "keyword": keyword,
                "category": get_category_for_id(keyword_id),
                "perspectives": perspectives,
                "average_confidence": round(average_confidence, 1),
                "primary_fortune_type": primary_fortune_type,
                "quality_score": 8.5  # 기본 품질 점수
            })
    
    return data

def insert_data_to_db(data):
    """데이터베이스에 데이터 삽입"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print(f"📊 총 {len(data)}개 키워드 데이터 삽입 시작...")
        
        for item in data:
            # JSONB 형태로 각 관점 데이터 준비
            perspectives = item["perspectives"]
            
            insert_query = """
            INSERT INTO dream_service.multi_perspective_interpretations (
                keyword_id, keyword, category,
                korean_traditional, chinese_traditional, western_psychology,
                islamic_perspective, buddhist_perspective, scientific_perspective,
                primary_fortune_type, average_confidence, quality_score
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) ON CONFLICT (keyword_id) DO UPDATE SET
                korean_traditional = EXCLUDED.korean_traditional,
                chinese_traditional = EXCLUDED.chinese_traditional,
                western_psychology = EXCLUDED.western_psychology,
                islamic_perspective = EXCLUDED.islamic_perspective,
                buddhist_perspective = EXCLUDED.buddhist_perspective,
                scientific_perspective = EXCLUDED.scientific_perspective,
                primary_fortune_type = EXCLUDED.primary_fortune_type,
                average_confidence = EXCLUDED.average_confidence,
                quality_score = EXCLUDED.quality_score,
                updated_at = CURRENT_TIMESTAMP;
            """
            
            cursor.execute(insert_query, (
                item["keyword_id"],
                item["keyword"],
                item["category"],
                json.dumps(perspectives.get("korean_traditional", {}), ensure_ascii=False),
                json.dumps(perspectives.get("chinese_traditional", {}), ensure_ascii=False),
                json.dumps(perspectives.get("western_psychology", {}), ensure_ascii=False),
                json.dumps(perspectives.get("islamic_perspective", {}), ensure_ascii=False),
                json.dumps(perspectives.get("buddhist_perspective", {}), ensure_ascii=False),
                json.dumps(perspectives.get("scientific_perspective", {}), ensure_ascii=False),
                item["primary_fortune_type"],
                item["average_confidence"],
                item["quality_score"]
            ))
            
            print(f"✅ {item['keyword_id']:2d}. {item['keyword']} ({item['category']}) - 삽입 완료")
        
        conn.commit()
        print(f"\n🎉 데이터 삽입 완료! 총 {len(data)}개 키워드 처리됨")
        
        # 통계 조회
        cursor.execute("""
        SELECT 
            category,
            COUNT(*) as count,
            AVG(average_confidence) as avg_confidence,
            AVG(quality_score) as avg_quality
        FROM dream_service.multi_perspective_interpretations 
        GROUP BY category 
        ORDER BY category;
        """)
        
        print("\n📈 카테고리별 통계:")
        for row in cursor.fetchall():
            print(f"  {row[0]:>6s}: {row[1]:2d}개 | 평균 신뢰도: {row[2]:.1f} | 평균 품질: {row[3]:.1f}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 삽입 오류: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def main():
    """메인 실행 함수"""
    # 마크다운 파일 경로
    markdown_file = Path("/home/ubuntu/docs/project_docs/dream-system/dream_interpretation_multi_perspective_system.md")
    
    if not markdown_file.exists():
        print(f"❌ 마크다운 파일을 찾을 수 없습니다: {markdown_file}")
        sys.exit(1)
    
    print("🔮 꿈풀이 다각도 해석 데이터 마이그레이션 시작")
    print("=" * 60)
    
    # 마크다운 파일 읽기
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📄 마크다운 파일 로드 완료 ({len(content):,} 문자)")
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        sys.exit(1)
    
    # 데이터 추출
    print("\n🔍 해석 데이터 추출 중...")
    data = extract_interpretation_data(content)
    
    if not data:
        print("❌ 추출된 데이터가 없습니다.")
        sys.exit(1)
    
    print(f"📊 추출 완료: {len(data)}개 키워드")
    
    # 샘플 출력
    if data:
        sample = data[0]
        print(f"\n📋 샘플 데이터 - {sample['keyword']}:")
        for perspective, details in sample['perspectives'].items():
            print(f"  {perspective}: {details['fortune_type']} ({details['confidence_score']}점)")
    
    # 데이터베이스 삽입
    print(f"\n💾 PostgreSQL 삽입 시작...")
    success = insert_data_to_db(data)
    
    if success:
        print("\n🎉 마이그레이션 완료!")
        print("🔮 이제 6개 관점별 꿈풀이 해석 서비스를 사용할 수 있습니다.")
    else:
        print("\n❌ 마이그레이션 실패")
        sys.exit(1)

if __name__ == "__main__":
    main()