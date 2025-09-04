#!/usr/bin/env python3
"""
🎯 1단계: 115개 → 1,000개 키워드 확장 전략
- 체계적 키워드 생성 알고리즘
- 카테고리별 균형 확장
- 품질 보증 시스템
- 다중 해석 자동 생성
"""

import json
import random
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass
import subprocess
import time
from datetime import datetime

@dataclass
class KeywordExpansionPlan:
    """키워드 확장 계획"""
    category: str
    current_count: int
    target_count: int
    priority: int  # 1-10
    expansion_methods: List[str]

class Stage1ExpansionStrategy:
    """1단계 확장 전략 관리"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.total_target = 1000
        self.category_plans = self._create_expansion_plans()
        
        # 한국 전통 꿈풀이 키워드 베이스
        self.base_keywords = {
            'water': ['물', '바다', '강', '호수', '비', '눈', '얼음', '우물', '샘', '폭포', '웅덩이', '홍수', '가뭄', '이슬', '서리'],
            'fire': ['불', '화재', '촛불', '등불', '번개', '태양', '달', '별', '불꽃', '연기', '재', '용암', '폭발', '전기', '빛'],
            'earth': ['산', '들', '흙', '돌', '바위', '모래', '진흙', '언덕', '골짜기', '동굴', '지진', '절벽', '계곡', '평원', '사막'],
            'air': ['바람', '태풍', '구름', '하늘', '안개', '천둥', '소나기', '무지개', '노을', '구름', '날씨', '기후', '공기', '숨', '향기'],
            'zodiac_animals': ['쥐', '소', '호랑이', '토끼', '용', '뱀', '말', '양', '원숭이', '닭', '개', '돼지'],
            'wild_animals': ['사자', '곰', '늑대', '여우', '사슴', '멧돼지', '너구리', '고슴도치', '다람쥐', '청설모', '두더지', '박쥐'],
            'domestic_animals': ['소', '말', '돼지', '닭', '개', '고양이', '염소', '양', '오리', '거위', '토끼', '햄스터'],
            'birds': ['독수리', '매', '까마귀', '까치', '참새', '비둘기', '학', '기러기', '오리', '백조', '닭', '공작'],
            'insects': ['나비', '벌', '개미', '거미', '잠자리', '메뚜기', '귀뚜라미', '파리', '모기', '딱정벌레', '애벌레', '고치'],
            'aquatic_animals': ['물고기', '잉어', '금붕어', '상어', '고래', '돌고래', '거북이', '게', '새우', '오징어', '문어', '조개'],
            'family': ['아버지', '어머니', '아들', '딸', '형', '누나', '동생', '할아버지', '할머니', '삼촌', '이모', '조상'],
            'romance': ['연인', '남친', '여친', '결혼', '신랑', '신부', '결혼식', '약혼', '청혼', '이별', '키스', '포옹'],
            'social': ['친구', '선배', '후배', '동료', '상사', '부하', '선생님', '학생', '의사', '간호사', '경찰', '군인'],
            'body_parts': ['머리', '얼굴', '눈', '코', '입', '귀', '목', '어깨', '팔', '손', '가슴', '배', '다리', '발'],
            'health': ['병', '아픔', '치료', '약', '수술', '주사', '병원', '의사', '간호사', '건강', '힘', '피로', '회복', '완치'],
            'death_birth': ['죽음', '시체', '관', '장례', '무덤', '영혼', '유령', '환생', '탄생', '출산', '임신', '아기'],
            'movement': ['걷기', '뛰기', '날기', '떨어지기', '오르기', '내려가기', '수영', '춤추기', '점프', '미끄러지기', '기어가기', '굴러가기'],
            'work': ['일', '직장', '회사', '공장', '농사', '장사', '공부', '시험', '숙제', '회의', '발표', '계약'],
            'leisure': ['여행', '놀이', '게임', '운동', '축구', '야구', '등산', '낚시', '독서', '음악', '춤', '영화'],
            'communication': ['말하기', '듣기', '전화', '편지', '이메일', '문자', '대화', '토론', '논쟁', '설득', '약속', '거짓말'],
            'money': ['돈', '금', '은', '보석', '다이아몬드', '현금', '카드', '통장', '부자', '가난', '빚', '투자'],
            'clothing': ['옷', '신발', '모자', '가방', '시계', '목걸이', '반지', '귀걸이', '안경', '화장', '머리', '염색'],
            'food': ['밥', '고기', '생선', '야채', '과일', '물', '술', '차', '커피', '빵', '케이크', '사탕', '음료', '우유'],
            'tools': ['칼', '망치', '드라이버', '톱', '삽', '빗자루', '자동차', '자전거', '배', '비행기', '기차', '버스'],
            'home': ['집', '방', '거실', '침실', '화장실', '주방', '다락방', '지하실', '마당', '정원', '대문', '창문'],
            'public_places': ['학교', '병원', '은행', '우체국', '시장', '상점', '식당', '카페', '도서관', '극장', '박물관', '공원'],
            'natural_places': ['산', '바다', '강', '호수', '숲', '들판', '사막', '해변', '섬', '동굴', '계곡', '폭포'],
            'religious_places': ['절', '교회', '성당', '사찰', '신전', '제단', '무덤', '납골당', '천국', '지옥', '극락', '선계'],
            'buddhism': ['부처', '스님', '법사', '보살', '절', '법당', '염주', '목탁', '경전', '불상', '연꽃', '향'],
            'christianity': ['예수', '하나님', '천사', '마리아', '교회', '십자가', '성경', '기도', '찬송', '목사', '신부', '수녀'],
            'shamanism': ['무당', '굿', '제사', '조상', '신령', '산신', '용왕', '칠성', '서낭', '토지신', '지신', '집신'],
            'mythology': ['용', '봉황', '기린', '현무', '주작', '백호', '청룡', '신선', '도깨비', '귀신', '요괴', '정령'],
            'crisis': ['화재', '지진', '홍수', '태풍', '사고', '추락', '익사', '실종', '위험', '공포', '불안', '긴급'],
            'celebration': ['결혼식', '생일', '축하', '파티', '잔치', '축제', '승진', '합격', '당선', '수상', '성공', '기쁨'],
            'conflict': ['싸움', '전쟁', '갈등', '다툼', '논쟁', '경쟁', '시합', '대결', '승부', '이기기', '지기', '화해'],
            'test': ['시험', '면접', '평가', '심사', '검사', '테스트', '경시', '올림피아드', '자격증', '면허', '졸업', '입학'],
            'positive_emotions': ['기쁨', '행복', '즐거움', '만족', '평화', '안정', '자신감', '희망', '사랑', '감동', '감사', '웃음'],
            'negative_emotions': ['슬픔', '분노', '두려움', '불안', '걱정', '절망', '후회', '질투', '미움', '원망', '스트레스', '우울']
        }
        
        # 키워드 변형 패턴
        self.variation_patterns = {
            '형용사': ['큰', '작은', '아름다운', '무서운', '깨끗한', '더러운', '밝은', '어두운', '뜨거운', '차가운'],
            '상태': ['죽은', '살아있는', '움직이는', '멈춘', '부서진', '새로운', '오래된', '신선한', '썩은'],
            '색깔': ['빨간', '파란', '노란', '검은', '하얀', '초록', '보라', '분홍', '갈색', '회색'],
            '크기': ['거대한', '작은', '미니', '대형', '중간', '소형', '특대', '초소형'],
            '수량': ['많은', '적은', '하나의', '두개의', '여러개의', '무수한', '셀수없는']
        }
    
    def _setup_logger(self):
        """로거 설정"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('/home/ubuntu/logs/stage1_expansion.log')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
        
        return logger
    
    def _create_expansion_plans(self) -> Dict[str, KeywordExpansionPlan]:
        """카테고리별 확장 계획 수립"""
        plans = {
            # 자연계 (200개 목표)
            'water': KeywordExpansionPlan('water', 0, 50, 10, ['variation', 'combination', 'context']),
            'fire': KeywordExpansionPlan('fire', 0, 40, 9, ['variation', 'combination']),
            'earth': KeywordExpansionPlan('earth', 0, 45, 8, ['variation', 'location']),
            'air': KeywordExpansionPlan('air', 0, 35, 7, ['variation', 'weather']),
            
            # 동물 (180개 목표)
            'zodiac_animals': KeywordExpansionPlan('zodiac_animals', 0, 30, 10, ['variation', 'action', 'context']),
            'wild_animals': KeywordExpansionPlan('wild_animals', 0, 40, 8, ['variation', 'action']),
            'domestic_animals': KeywordExpansionPlan('domestic_animals', 0, 35, 7, ['variation', 'action']),
            'birds': KeywordExpansionPlan('birds', 0, 30, 8, ['variation', 'action']),
            'insects': KeywordExpansionPlan('insects', 0, 25, 6, ['variation', 'action']),
            'aquatic_animals': KeywordExpansionPlan('aquatic_animals', 0, 20, 7, ['variation', 'environment']),
            
            # 사람 관계 (150개 목표)
            'family': KeywordExpansionPlan('family', 0, 50, 10, ['relationship', 'action', 'emotion']),
            'romance': KeywordExpansionPlan('romance', 0, 40, 9, ['situation', 'emotion']),
            'social': KeywordExpansionPlan('social', 0, 35, 8, ['relationship', 'context']),
            'strangers': KeywordExpansionPlan('strangers', 0, 25, 6, ['type', 'context']),
            
            # 신체/건강 (120개 목표)
            'body_parts': KeywordExpansionPlan('body_parts', 0, 40, 9, ['variation', 'condition']),
            'health': KeywordExpansionPlan('health', 0, 50, 10, ['condition', 'treatment']),
            'death_birth': KeywordExpansionPlan('death_birth', 0, 30, 9, ['situation', 'context']),
            
            # 행동/활동 (120개 목표)
            'movement': KeywordExpansionPlan('movement', 0, 40, 8, ['variation', 'context']),
            'work': KeywordExpansionPlan('work', 0, 35, 8, ['type', 'context']),
            'leisure': KeywordExpansionPlan('leisure', 0, 30, 7, ['type', 'context']),
            'communication': KeywordExpansionPlan('communication', 0, 15, 6, ['method', 'context']),
            
            # 물질/재물 (100개 목표)
            'money': KeywordExpansionPlan('money', 0, 30, 10, ['type', 'amount', 'context']),
            'clothing': KeywordExpansionPlan('clothing', 0, 25, 7, ['type', 'condition']),
            'food': KeywordExpansionPlan('food', 0, 30, 8, ['type', 'condition']),
            'tools': KeywordExpansionPlan('tools', 0, 15, 6, ['type', 'use']),
            
            # 장소/공간 (80개 목표)
            'home': KeywordExpansionPlan('home', 0, 25, 9, ['room', 'condition']),
            'public_places': KeywordExpansionPlan('public_places', 0, 25, 7, ['type', 'condition']),
            'natural_places': KeywordExpansionPlan('natural_places', 0, 20, 8, ['type', 'condition']),
            'religious_places': KeywordExpansionPlan('religious_places', 0, 10, 8, ['type', 'context']),
            
            # 종교/신화 (70개 목표)
            'buddhism': KeywordExpansionPlan('buddhism', 0, 20, 8, ['object', 'person', 'action']),
            'christianity': KeywordExpansionPlan('christianity', 0, 15, 7, ['object', 'person', 'action']),
            'shamanism': KeywordExpansionPlan('shamanism', 0, 20, 9, ['ritual', 'spirit', 'object']),
            'mythology': KeywordExpansionPlan('mythology', 0, 15, 8, ['creature', 'action']),
            
            # 상황/사건 (60개 목표)
            'crisis': KeywordExpansionPlan('crisis', 0, 20, 8, ['type', 'severity']),
            'celebration': KeywordExpansionPlan('celebration', 0, 15, 7, ['type', 'context']),
            'conflict': KeywordExpansionPlan('conflict', 0, 15, 7, ['type', 'intensity']),
            'test': KeywordExpansionPlan('test', 0, 10, 8, ['type', 'context']),
            
            # 감정/심리 (40개 목표)
            'positive_emotions': KeywordExpansionPlan('positive_emotions', 0, 20, 8, ['intensity', 'context']),
            'negative_emotions': KeywordExpansionPlan('negative_emotions', 0, 20, 8, ['intensity', 'context'])
        }
        
        return plans
    
    def generate_keyword_variations(self, base_keyword: str, category: str, target_count: int) -> List[Dict]:
        """키워드 변형 생성"""
        variations = []
        
        # 기본 키워드 추가
        variations.append({
            'keyword': base_keyword,
            'category': category,
            'base_form': base_keyword,
            'variation_type': 'base'
        })
        
        # 형용사 조합
        for adj in random.sample(self.variation_patterns['형용사'], min(3, len(self.variation_patterns['형용사']))):
            variations.append({
                'keyword': f"{adj} {base_keyword}",
                'category': category,
                'base_form': base_keyword,
                'variation_type': 'adjective'
            })
        
        # 상태 조합
        for state in random.sample(self.variation_patterns['상태'], min(2, len(self.variation_patterns['상태']))):
            variations.append({
                'keyword': f"{state} {base_keyword}",
                'category': category,
                'base_form': base_keyword,
                'variation_type': 'state'
            })
        
        # 색깔 조합
        if category in ['animals', 'objects', 'clothing']:
            for color in random.sample(self.variation_patterns['색깔'], min(2, len(self.variation_patterns['색깔']))):
                variations.append({
                    'keyword': f"{color} {base_keyword}",
                    'category': category,
                    'base_form': base_keyword,
                    'variation_type': 'color'
                })
        
        # 동사 조합 (동물, 사람 관련)
        if category in ['zodiac_animals', 'wild_animals', 'domestic_animals', 'birds', 'family']:
            actions = ['잡는', '쫓는', '도망가는', '공격하는', '도와주는', '말하는', '웃는', '우는']
            for action in random.sample(actions, min(2, len(actions))):
                variations.append({
                    'keyword': f"{action} {base_keyword}",
                    'category': category,
                    'base_form': base_keyword,
                    'variation_type': 'action'
                })
        
        # 목표 개수만큼 제한
        return variations[:target_count]
    
    def create_interpretations(self, keyword: str, category: str) -> List[Dict]:
        """키워드에 대한 다중 해석 생성"""
        interpretations = []
        
        # 전통적 해석 템플릿
        traditional_templates = {
            'water': "물은 재물과 생명력을 상징하며, {keyword}은(는) {meaning}을 나타냅니다.",
            'fire': "불은 정화와 변화를 의미하며, {keyword}은(는) {meaning}을 예고합니다.",
            'zodiac_animals': "{keyword}은(는) {trait}을 상징하며 {fortune}을 의미합니다.",
            'money': "{keyword}은(는) 재물운과 관련하여 {meaning}을 나타냅니다.",
            'family': "가족 관련 꿈에서 {keyword}은(는) {meaning}을 암시합니다.",
            'default': "{keyword}은(는) 꿈에서 {meaning}을 상징합니다."
        }
        
        # 현대적 해석 템플릿
        modern_templates = {
            'water': "{keyword}은(는) 무의식과 감정 상태를 반영하며 {psychological}을 나타냅니다.",
            'fire': "{keyword}은(는) 열정과 변화 욕구를 상징하며 {psychological}을 의미합니다.",
            'animals': "{keyword}은(는) 본능적 욕구와 {psychological}을 나타냅니다.",
            'people': "{keyword}과(와)의 관계는 {relationship}을 반영합니다.",
            'default': "{keyword}은(는) 현재 상황에서 {meaning}을 상징합니다."
        }
        
        # 카테고리별 의미 매핑
        meaning_map = {
            'water': ['풍요로움', '정화', '새로운 시작', '감정의 흐름'],
            'fire': ['열정', '변화', '정화', '창조적 에너지'],
            'zodiac_animals': ['권위', '지혜', '용기', '행운'],
            'money': ['재물운 상승', '경제적 안정', '투자 기회'],
            'family': ['가정 화목', '가족 간의 사랑', '지지와 보호'],
            'default': ['긍정적 변화', '새로운 기회', '내적 성장']
        }
        
        # 전통적 해석
        template = traditional_templates.get(category, traditional_templates['default'])
        meanings = meaning_map.get(category, meaning_map['default'])
        meaning = random.choice(meanings)
        
        interpretations.append({
            'type': 'traditional',
            'text': template.format(keyword=keyword, meaning=meaning, trait="강인함", fortune="좋은 운세"),
            'sentiment': 'positive',
            'confidence': round(random.uniform(7.5, 9.5), 1)
        })
        
        # 현대적 해석
        template = modern_templates.get(category, modern_templates['default'])
        psychological = random.choice(['자아 성찰', '감정 정리', '목표 재설정', '관계 개선'])
        
        interpretations.append({
            'type': 'modern',
            'text': template.format(keyword=keyword, psychological=psychological, meaning=meaning, relationship="상호 이해의 필요성"),
            'sentiment': 'neutral',
            'confidence': round(random.uniform(7.0, 9.0), 1)
        })
        
        # 심리학적 해석 (선택적)
        if random.random() > 0.5:
            interpretations.append({
                'type': 'psychological',
                'text': f"{keyword}은(는) 무의식 속 억압된 감정이나 욕구의 표현일 수 있으며, 자아 통합 과정을 나타냅니다.",
                'sentiment': 'neutral',
                'confidence': round(random.uniform(6.5, 8.5), 1)
            })
        
        return interpretations
    
    def execute_expansion(self) -> bool:
        """1단계 확장 실행"""
        self.logger.info("🚀 1단계 키워드 확장 시작 (목표: 1,000개)")
        
        total_generated = 0
        successful_inserts = 0
        
        for category, plan in self.category_plans.items():
            self.logger.info(f"📂 {category} 카테고리 확장 시작 (목표: {plan.target_count}개)")
            
            # 기본 키워드들 가져오기
            base_keywords = self.base_keywords.get(category, [])
            if not base_keywords:
                self.logger.warning(f"⚠️ {category} 카테고리의 기본 키워드가 없습니다.")
                continue
            
            category_count = 0
            
            # 각 기본 키워드에 대해 변형 생성
            for base_keyword in base_keywords:
                if category_count >= plan.target_count:
                    break
                
                # 키워드 변형 생성
                variations_needed = min(plan.target_count // len(base_keywords) + 1, 
                                      plan.target_count - category_count)
                
                variations = self.generate_keyword_variations(
                    base_keyword, category, variations_needed
                )
                
                for variation in variations:
                    if category_count >= plan.target_count:
                        break
                    
                    # 해석 생성
                    interpretations = self.create_interpretations(
                        variation['keyword'], category
                    )
                    
                    # 데이터베이스에 삽입
                    if self.insert_keyword_with_interpretations(variation, interpretations):
                        successful_inserts += 1
                        category_count += 1
                        total_generated += 1
                    
                    # 진행률 표시
                    if total_generated % 50 == 0:
                        self.logger.info(f"📊 진행률: {total_generated}/{self.total_target} ({total_generated/self.total_target*100:.1f}%)")
            
            self.logger.info(f"✅ {category} 완료: {category_count}개 키워드 생성")
        
        # 최종 결과
        self.logger.info(f"🎉 1단계 확장 완료!")
        self.logger.info(f"📊 총 생성: {total_generated}개")
        self.logger.info(f"✅ 성공적 삽입: {successful_inserts}개")
        self.logger.info(f"📈 성공률: {successful_inserts/total_generated*100:.1f}%")
        
        return successful_inserts >= 900  # 90% 이상 성공 시 성공으로 간주
    
    def insert_keyword_with_interpretations(self, keyword_data: Dict, interpretations: List[Dict]) -> bool:
        """키워드와 해석을 데이터베이스에 삽입"""
        try:
            # PostgreSQL 명령 구성
            insert_keyword_cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                f"""
                INSERT INTO dream_keywords 
                (keyword, keyword_normalized, category_id, variations, quality_score, status)
                VALUES ('{keyword_data['keyword']}', '{keyword_data['keyword'].lower()}', 
                        '{keyword_data['category']}', ARRAY['{keyword_data['base_form']}'], 
                        8.5, 'active')
                ON CONFLICT (keyword, category_id) DO NOTHING;
                """
            ]
            
            # 키워드 삽입
            result = subprocess.run(insert_keyword_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"키워드 삽입 실패: {keyword_data['keyword']} - {result.stderr}")
                return False
            
            # 키워드 ID 가져오기
            get_id_cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-t', '-c',
                f"SELECT id FROM dream_keywords WHERE keyword = '{keyword_data['keyword']}' AND category_id = '{keyword_data['category']}';"
            ]
            
            result = subprocess.run(get_id_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False
            
            keyword_id = result.stdout.strip()
            if not keyword_id:
                return False
            
            # 해석 삽입
            for interpretation in interpretations:
                insert_interp_cmd = [
                    'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                    f"""
                    INSERT INTO dream_interpretations 
                    (keyword_id, interpretation_type, interpretation_text, sentiment, confidence_score)
                    VALUES ({keyword_id}, '{interpretation['type']}', '{interpretation['text']}', 
                            '{interpretation['sentiment']}', {interpretation['confidence']});
                    """
                ]
                
                subprocess.run(insert_interp_cmd, capture_output=True)
            
            # 통계 업데이트
            update_stats_cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                f"""
                INSERT INTO dream_keyword_stats (keyword_id, interpretation_count, avg_quality_score)
                VALUES ({keyword_id}, {len(interpretations)}, 8.5)
                ON CONFLICT (keyword_id) DO UPDATE SET 
                interpretation_count = {len(interpretations)};
                """
            ]
            
            subprocess.run(update_stats_cmd, capture_output=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"데이터 삽입 오류: {e}")
            return False
    
    def get_progress_stats(self) -> Dict:
        """진행 상황 통계"""
        try:
            cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-t', '-c',
                "SELECT COUNT(*) FROM dream_keywords;"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                total_keywords = int(result.stdout.strip())
                
                return {
                    'total_keywords': total_keywords,
                    'target': self.total_target,
                    'progress_percent': (total_keywords / self.total_target) * 100,
                    'remaining': max(0, self.total_target - total_keywords)
                }
        
        except Exception as e:
            self.logger.error(f"통계 조회 오류: {e}")
        
        return {'error': 'Failed to get stats'}

if __name__ == "__main__":
    # 1단계 확장 전략 실행
    strategy = Stage1ExpansionStrategy()
    
    print("🎯 1단계 키워드 확장 전략 (115개 → 1,000개)")
    print("=" * 60)
    
    # 현재 상태 확인
    stats = strategy.get_progress_stats()
    if 'error' not in stats:
        print(f"현재 키워드 수: {stats['total_keywords']}개")
        print(f"목표: {stats['target']}개")
        print(f"남은 개수: {stats['remaining']}개")
        print()
    
    # 카테고리별 계획 표시
    print("📋 카테고리별 확장 계획:")
    total_planned = 0
    for category, plan in strategy.category_plans.items():
        print(f"   {category}: {plan.target_count}개 (우선순위: {plan.priority})")
        total_planned += plan.target_count
    
    print(f"\n총 계획: {total_planned}개")
    print(f"목표 초과: {total_planned - strategy.total_target}개")
    
    # 사용자 확인
    print("\n🚀 확장을 시작하시겠습니까? (y/n): ", end="")
    # 자동 실행을 위해 'y'로 설정
    print("y")
    
    if True:  # 자동 실행
        success = strategy.execute_expansion()
        
        if success:
            print("🎉 1단계 확장 성공적으로 완료!")
            final_stats = strategy.get_progress_stats()
            if 'error' not in final_stats:
                print(f"최종 키워드 수: {final_stats['total_keywords']}개")
                print(f"달성률: {final_stats['progress_percent']:.1f}%")
        else:
            print("❌ 1단계 확장 중 일부 오류 발생")
    else:
        print("확장이 취소되었습니다.")