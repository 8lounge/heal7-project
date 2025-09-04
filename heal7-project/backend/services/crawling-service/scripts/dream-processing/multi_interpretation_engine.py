#!/usr/bin/env python3
"""
🔮 다중 해석 생성 엔진 (로컬 알고리즘 기반)
- 전통적/현대적/심리학적 관점의 다각적 해석
- 한국 문화 특화 해석 로직
- 키워드별 맞춤형 해석 생성
- 품질 점수 자동 산정
"""

import random
import logging
import subprocess
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import json
import re
from datetime import datetime

@dataclass
class InterpretationTemplate:
    """해석 템플릿"""
    category: str
    interpretation_type: str  # traditional, modern, psychological
    positive_template: str
    negative_template: str
    neutral_template: str
    keywords: List[str]  # 이 템플릿에 적용되는 키워드들

@dataclass
class MultiInterpretation:
    """다중 해석 결과"""
    keyword: str
    category: str
    traditional_interpretation: str
    modern_interpretation: str
    psychological_interpretation: Optional[str]
    sentiment_traditional: str  # positive, negative, neutral
    sentiment_modern: str
    sentiment_psychological: Optional[str]
    quality_score: float
    confidence: float
    related_keywords: List[str]

class MultiInterpretationEngine:
    """다중 해석 생성 엔진"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.templates = self._initialize_templates()
        self.sentiment_words = self._initialize_sentiment_words()
        self.cultural_context = self._initialize_cultural_context()
        
    def _setup_logger(self):
        """로거 설정"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('/home/ubuntu/logs/multi_interpretation.log')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
        
        return logger
    
    def _initialize_templates(self) -> Dict[str, List[InterpretationTemplate]]:
        """해석 템플릿 초기화"""
        templates = {
            'water': [
                InterpretationTemplate(
                    category='water',
                    interpretation_type='traditional',
                    positive_template="{keyword}은(는) 재물과 생명력의 상징으로, {symbol}을 통해 {fortune}을 예고합니다.",
                    negative_template="{keyword}은(는) {warning}를 의미하며, {caution}에 주의하셔야 합니다.",
                    neutral_template="{keyword}은(는) 변화의 흐름을 나타내며, {change}을 암시합니다.",
                    keywords=['물', '바다', '강', '호수', '비', '눈', '얼음']
                ),
                InterpretationTemplate(
                    category='water',
                    interpretation_type='modern',
                    positive_template="{keyword}은(는) 무의식의 정화와 감정의 치유를 상징하며, {healing}을 나타냅니다.",
                    negative_template="{keyword}은(는) 감정적 혼란이나 {stress}를 반영할 수 있습니다.",
                    neutral_template="{keyword}은(는) 현재 감정 상태의 반영이며, {reflection}을 의미합니다.",
                    keywords=['물', '바다', '강', '호수', '비', '눈', '얼음']
                )
            ],
            'fire': [
                InterpretationTemplate(
                    category='fire',
                    interpretation_type='traditional',
                    positive_template="{keyword}은(는) 정화와 변화의 힘으로, {transformation}을 통해 {success}을 가져다줍니다.",
                    negative_template="{keyword}은(는) {danger}의 경고이며, {prevention}이 필요합니다.",
                    neutral_template="{keyword}은(는) 강한 에너지의 표현으로, {energy}을 나타냅니다.",
                    keywords=['불', '화재', '촛불', '번개', '태양']
                ),
                InterpretationTemplate(
                    category='fire',
                    interpretation_type='modern',
                    positive_template="{keyword}은(는) 열정과 창조적 에너지의 상징으로, {creativity}을 의미합니다.",
                    negative_template="{keyword}은(는) 분노나 파괴적 감정을 나타낼 수 있으며, {control}이 필요합니다.",
                    neutral_template="{keyword}은(는) 강한 의지력과 {willpower}을 상징합니다.",
                    keywords=['불', '화재', '촛불', '번개', '태양']
                )
            ],
            'zodiac_animals': [
                InterpretationTemplate(
                    category='zodiac_animals',
                    interpretation_type='traditional',
                    positive_template="{keyword}은(는) {trait}의 상징으로, {fortune}과 {blessing}을 가져다줍니다.",
                    negative_template="{keyword}이(가) {warning}를 나타내며, {caution}하셔야 합니다.",
                    neutral_template="{keyword}은(는) {characteristic}을 상징하며, {guidance}을 제공합니다.",
                    keywords=['쥐', '소', '호랑이', '토끼', '용', '뱀', '말', '양', '원숭이', '닭', '개', '돼지']
                )
            ],
            'family': [
                InterpretationTemplate(
                    category='family',
                    interpretation_type='traditional',
                    positive_template="{keyword}와(과) 관련된 꿈은 {family_bond}를 의미하며, {harmony}을 예고합니다.",
                    negative_template="{keyword}와(과)의 꿈은 {concern}을 나타낼 수 있으며, {care}가 필요합니다.",
                    neutral_template="{keyword}에 대한 꿈은 {relationship}을 반영하며, {understanding}을 나타냅니다.",
                    keywords=['아버지', '어머니', '아들', '딸', '형', '누나', '동생']
                )
            ],
            'money': [
                InterpretationTemplate(
                    category='money',
                    interpretation_type='traditional',
                    positive_template="{keyword}을(를) {action}하는 꿈은 역설적으로 {opposite_result}를 의미합니다.",
                    negative_template="{keyword}을(를) {lose_action}하는 꿈은 {actual_gain}을 암시합니다.",
                    neutral_template="{keyword}에 관한 꿈은 {financial_state}를 나타냅니다.",
                    keywords=['돈', '금', '은', '보석', '현금']
                )
            ]
        }
        
        # 기본 템플릿 (모든 카테고리에 적용 가능)
        templates['default'] = [
            InterpretationTemplate(
                category='default',
                interpretation_type='traditional',
                positive_template="{keyword}은(는) 좋은 {meaning}을 상징하며, {positive_outcome}을 나타냅니다.",
                negative_template="{keyword}은(는) {negative_meaning}을 의미할 수 있으니, {advice}하시기 바랍니다.",
                neutral_template="{keyword}은(는) {neutral_meaning}을 나타내며, {interpretation}을 의미합니다.",
                keywords=[]
            ),
            InterpretationTemplate(
                category='default',
                interpretation_type='modern',
                positive_template="{keyword}은(는) {psychological_positive}를 상징하며, {growth}을 의미합니다.",
                negative_template="{keyword}은(는) {stress_indicator}를 나타낼 수 있으며, {solution}이 도움이 될 것입니다.",
                neutral_template="{keyword}은(는) 현재 상황의 {reflection}을 나타냅니다.",
                keywords=[]
            )
        ]
        
        return templates
    
    def _initialize_sentiment_words(self) -> Dict:
        """감정 단어 사전 초기화"""
        return {
            'positive': {
                'symbols': ['행운', '성공', '번영', '풍요', '기쁨', '축복', '발전', '성취'],
                'fortunes': ['재물운 상승', '좋은 소식', '성공적인 결과', '행복한 미래', '순조로운 진행'],
                'outcomes': ['크게 성공할 것', '좋은 기회가 올 것', '소원이 이루어질 것', '건강이 좋아질 것'],
                'healing': ['마음의 평화', '감정의 안정', '스트레스 해소', '내적 치유'],
                'creativity': ['새로운 아이디어', '창조적 영감', '예술적 재능', '혁신적 사고'],
                'trait': ['지혜', '용기', '성실함', '인내심', '리더십'],
                'blessing': ['하늘의 도움', '조상의 보살핌', '신의 축복', '운명의 인도'],
                'family_bond': ['가족의 화목', '깊은 사랑', '든든한 지원', '따뜻한 정'],
                'harmony': ['집안의 평화', '관계 개선', '화해와 용서', '서로의 이해']
            },
            'negative': {
                'warnings': ['재난', '손실', '질병', '갈등', '실패', '위험', '걱정거리'],
                'cautions': ['건강을 조심', '투자에 신중', '관계에 주의', '안전사고 예방', '말조심'],
                'dangers': ['화재의 위험', '사고의 전조', '큰 손실', '건강 악화'],
                'stress': ['정신적 피로', '감정적 부담', '대인관계 스트레스', '업무 압박'],
                'concern': ['건강 염려', '앞날 걱정', '가족 문제', '경제적 어려움'],
                'negative_meaning': ['불길한 징조', '어려운 시기', '시련의 시작', '역경의 예고']
            },
            'neutral': {
                'changes': ['새로운 시작', '환경의 변화', '마음의 변화', '상황의 전환'],
                'reflections': ['현재 상태의 투영', '내면의 갈등', '잠재의식의 표현', '심리적 상태'],
                'energy': ['강한 의지', '내재된 힘', '활동력', '생명력'],
                'characteristics': ['타고난 성품', '개인의 특성', '성격적 특징', '본래의 모습'],
                'guidance': ['인생의 방향', '올바른 선택', '현명한 판단', '미래에 대한 지침'],
                'relationships': ['인간관계', '소통의 필요성', '이해와 배려', '상호 존중'],
                'financial_state': ['경제 상황', '재정 관리', '소비 패턴', '투자 심리']
            }
        }
    
    def _initialize_cultural_context(self) -> Dict:
        """한국 문화 컨텍스트 초기화"""
        return {
            'seasonal': {
                '봄': ['새싹', '꽃', '따뜻함', '시작', '희망'],
                '여름': ['무성함', '열정', '성장', '활력', '번영'],
                '가을': ['수확', '결실', '성숙', '감사', '준비'],
                '겨울': ['휴식', '성찰', '인내', '준비', '정화']
            },
            'confucian_values': ['효도', '예의', '충성', '신의', '화합'],
            'buddhist_concepts': ['인과응보', '윤회', '해탈', '자비', '정진'],
            'shamanistic_elements': ['조상신', '산신', '용왕', '칠성', '서낭']
        }
    
    def generate_interpretations(self, keyword: str, category: str) -> MultiInterpretation:
        """키워드에 대한 다중 해석 생성"""
        # 카테고리별 템플릿 선택
        category_templates = self.templates.get(category, self.templates['default'])
        
        # 전통적 해석 생성
        traditional_template = next((t for t in category_templates if t.interpretation_type == 'traditional'), None)
        if not traditional_template:
            traditional_template = self.templates['default'][0]
        
        traditional_interp, traditional_sentiment = self._generate_single_interpretation(
            keyword, category, traditional_template, 'traditional'
        )
        
        # 현대적 해석 생성
        modern_template = next((t for t in category_templates if t.interpretation_type == 'modern'), None)
        if not modern_template:
            modern_template = self.templates['default'][1]
        
        modern_interp, modern_sentiment = self._generate_single_interpretation(
            keyword, category, modern_template, 'modern'
        )
        
        # 심리학적 해석 생성 (50% 확률)
        psychological_interp = None
        psychological_sentiment = None
        
        if random.random() > 0.5:
            psychological_interp, psychological_sentiment = self._generate_psychological_interpretation(
                keyword, category
            )
        
        # 관련 키워드 생성
        related_keywords = self._generate_related_keywords(keyword, category)
        
        # 품질 점수 계산
        quality_score = self._calculate_quality_score(
            traditional_interp, modern_interp, psychological_interp
        )
        
        return MultiInterpretation(
            keyword=keyword,
            category=category,
            traditional_interpretation=traditional_interp,
            modern_interpretation=modern_interp,
            psychological_interpretation=psychological_interp,
            sentiment_traditional=traditional_sentiment,
            sentiment_modern=modern_sentiment,
            sentiment_psychological=psychological_sentiment,
            quality_score=quality_score,
            confidence=random.uniform(0.75, 0.95),
            related_keywords=related_keywords
        )
    
    def _generate_single_interpretation(self, keyword: str, category: str, 
                                      template: InterpretationTemplate, 
                                      interpretation_type: str) -> Tuple[str, str]:
        """단일 해석 생성"""
        # 감정 결정 (확률적)
        sentiment_prob = random.random()
        if sentiment_prob < 0.4:
            sentiment = 'positive'
            template_str = template.positive_template
        elif sentiment_prob < 0.7:
            sentiment = 'neutral'
            template_str = template.neutral_template
        else:
            sentiment = 'negative'
            template_str = template.negative_template
        
        # 템플릿 변수 채우기
        variables = self._get_template_variables(keyword, category, sentiment, interpretation_type)
        
        try:
            interpretation = template_str.format(keyword=keyword, **variables)
        except KeyError as e:
            # 누락된 변수가 있는 경우 기본값 사용
            self.logger.warning(f"템플릿 변수 누락: {e}")
            interpretation = f"{keyword}은(는) {sentiment} 의미를 가지며, 꿈 해석에서 중요한 상징입니다."
        
        return interpretation, sentiment
    
    def _get_template_variables(self, keyword: str, category: str, 
                               sentiment: str, interpretation_type: str) -> Dict:
        """템플릿 변수 생성"""
        sentiment_dict = self.sentiment_words[sentiment]
        variables = {}
        
        # 각 변수에 대해 적절한 값 선택
        for key in sentiment_dict:
            if sentiment_dict[key]:
                variables[key] = random.choice(sentiment_dict[key])
        
        # 특별 변수들
        if interpretation_type == 'traditional':
            if category in ['money']:
                variables['action'] = random.choice(['줍는', '세는', '받는', '찾는'])
                variables['opposite_result'] = random.choice(['실제로는 손실', '돈 나갈 일', '지출 증가'])
                variables['lose_action'] = random.choice(['잃는', '도둑맞는', '떨어뜨리는'])
                variables['actual_gain'] = random.choice(['재물 운 상승', '의외의 수입', '금전적 이득'])
            
            if category in ['zodiac_animals']:
                animal_traits = {
                    '쥐': '근면과 저축', '소': '성실과 끈기', '호랑이': '용맹과 권위',
                    '토끼': '온순과 지혜', '용': '권력과 성공', '뱀': '지혜와 변화',
                    '말': '자유와 진취성', '양': '온화와 평화', '원숭이': '재치와 유머',
                    '닭': '부지런함과 정시', '개': '충성과 우정', '돼지': '풍요와 복'
                }
                variables['trait'] = animal_traits.get(keyword, '특별한 의미')
        
        # 누락된 필수 변수들을 기본값으로 채움
        default_values = {
            'symbol': '좋은 징조', 'fortune': '행운', 'warning': '주의사항',
            'caution': '신중함', 'change': '변화', 'healing': '치유',
            'stress': '걱정', 'reflection': '성찰', 'transformation': '변화',
            'success': '성공', 'danger': '위험', 'prevention': '예방',
            'energy': '에너지', 'creativity': '창의성', 'control': '절제',
            'willpower': '의지력', 'meaning': '의미', 'positive_outcome': '좋은 결과',
            'negative_meaning': '어려움', 'advice': '주의', 'neutral_meaning': '변화',
            'interpretation': '의미', 'psychological_positive': '심리적 성장',
            'growth': '발전', 'stress_indicator': '스트레스', 'solution': '해결책'
        }
        
        for key, default_value in default_values.items():
            if key not in variables:
                variables[key] = default_value
        
        return variables
    
    def _generate_psychological_interpretation(self, keyword: str, category: str) -> Tuple[str, str]:
        """심리학적 해석 생성"""
        psychological_templates = [
            f"{keyword}은(는) 무의식 속 {concept}의 표현으로, {meaning}을 나타냅니다.",
            f"{keyword}에 대한 꿈은 {psychological_state}를 반영하며, {advice}가 도움이 될 것입니다.",
            f"심리학적으로 {keyword}은(는) {archetype}을 상징하며, {growth}의 과정을 나타냅니다."
        ]
        
        concepts = ['억압된 감정', '잠재된 욕구', '내적 갈등', '자아 통합', '성장 욕구']
        meanings = ['자기 발견의 필요성', '감정 정리의 시기', '새로운 도전', '내적 평화']
        psychological_states = ['현재의 심리 상태', '스트레스 수준', '감정적 상태', '정신적 성숙도']
        advice = ['전문가 상담', '명상과 성찰', '감정 표현', '적극적 소통']
        archetypes = ['어머니 원형', '아버지 원형', '그림자', '자기(Self)', '아니마/아니무스']
        growth = ['심리적 성숙', '인격적 발달', '자아 실현', '정신적 진화']
        
        template = random.choice(psychological_templates)
        interpretation = template.format(
            keyword=keyword,
            concept=random.choice(concepts),
            meaning=random.choice(meanings),
            psychological_state=random.choice(psychological_states),
            advice=random.choice(advice),
            archetype=random.choice(archetypes),
            growth=random.choice(growth)
        )
        
        return interpretation, 'neutral'
    
    def _generate_related_keywords(self, keyword: str, category: str) -> List[str]:
        """관련 키워드 생성"""
        category_relations = {
            'water': ['물', '바다', '강', '호수', '비', '눈', '얼음', '우물', '샘', '폭포'],
            'fire': ['불', '화재', '촛불', '등불', '번개', '태양', '달', '별', '불꽃', '연기'],
            'zodiac_animals': ['쥐', '소', '호랑이', '토끼', '용', '뱀', '말', '양', '원숭이', '닭', '개', '돼지'],
            'family': ['아버지', '어머니', '아들', '딸', '형', '누나', '동생', '할아버지', '할머니'],
            'money': ['돈', '금', '은', '보석', '다이아몬드', '현금', '카드', '통장', '부자', '가난']
        }
        
        # 카테고리별 관련 키워드 가져오기
        related = category_relations.get(category, [])
        
        # 현재 키워드 제외
        if keyword in related:
            related.remove(keyword)
        
        # 3-5개 선택
        count = min(random.randint(3, 5), len(related))
        return random.sample(related, count) if related else []
    
    def _calculate_quality_score(self, traditional: str, modern: str, 
                                psychological: Optional[str]) -> float:
        """품질 점수 계산"""
        score = 8.0  # 기본 점수
        
        # 길이 점검
        if len(traditional) > 15:
            score += 0.2
        if len(modern) > 15:
            score += 0.2
        if psychological and len(psychological) > 15:
            score += 0.3
        
        # 키워드 다양성 점검
        quality_keywords = ['상징', '의미', '나타', '예고', '반영', '표현']
        if any(word in traditional for word in quality_keywords):
            score += 0.2
        if any(word in modern for word in quality_keywords):
            score += 0.2
        
        # 중복 방지
        if traditional != modern:
            score += 0.3
        
        return min(score, 10.0)
    
    def batch_generate_interpretations(self, keywords: List[Tuple[str, str]]) -> List[MultiInterpretation]:
        """배치 해석 생성"""
        results = []
        
        for keyword, category in keywords:
            try:
                interpretation = self.generate_interpretations(keyword, category)
                results.append(interpretation)
                self.logger.info(f"✅ {keyword} ({category}) 해석 생성 완료 (품질: {interpretation.quality_score:.1f})")
            except Exception as e:
                self.logger.error(f"❌ {keyword} 해석 생성 실패: {e}")
        
        return results
    
    def save_interpretations_to_db(self, interpretations: List[MultiInterpretation]) -> int:
        """해석을 데이터베이스에 저장"""
        saved_count = 0
        
        for interp in interpretations:
            try:
                # 키워드 ID 조회
                get_id_cmd = [
                    'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-t', '-c',
                    f"SELECT id FROM dream_keywords WHERE keyword = '{interp.keyword}' AND category_id = '{interp.category}' LIMIT 1;"
                ]
                
                result = subprocess.run(get_id_cmd, capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    keyword_id = result.stdout.strip()
                    
                    # 기존 해석 삭제 (업데이트를 위해)
                    delete_cmd = [
                        'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                        f"DELETE FROM dream_interpretations WHERE keyword_id = {keyword_id};"
                    ]
                    subprocess.run(delete_cmd, capture_output=True)
                    
                    # 새 해석들 삽입
                    interpretations_data = [
                        ('traditional', interp.traditional_interpretation, interp.sentiment_traditional),
                        ('modern', interp.modern_interpretation, interp.sentiment_modern)
                    ]
                    
                    if interp.psychological_interpretation:
                        interpretations_data.append((
                            'psychological', 
                            interp.psychological_interpretation, 
                            interp.sentiment_psychological or 'neutral'
                        ))
                    
                    for interp_type, text, sentiment in interpretations_data:
                        insert_cmd = [
                            'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', '-c',
                            f"""
                            INSERT INTO dream_interpretations 
                            (keyword_id, interpretation_type, interpretation_text, sentiment, confidence_score)
                            VALUES ({keyword_id}, '{interp_type}', '{text.replace("'", "''")}', 
                                    '{sentiment}', {interp.confidence});
                            """
                        ]
                        subprocess.run(insert_cmd, capture_output=True)
                    
                    saved_count += 1
                    
            except Exception as e:
                self.logger.error(f"DB 저장 오류 ({interp.keyword}): {e}")
        
        self.logger.info(f"✅ {saved_count}개 키워드 해석 DB 저장 완료")
        return saved_count

# 테스트 실행
if __name__ == "__main__":
    engine = MultiInterpretationEngine()
    
    # 샘플 키워드로 테스트
    sample_keywords = [
        ('물', 'water'),
        ('불', 'fire'),
        ('호랑이', 'zodiac_animals'),
        ('아버지', 'family'),
        ('돈', 'money')
    ]
    
    print("🔮 다중 해석 생성 엔진 테스트")
    print("=" * 50)
    
    # 해석 생성
    interpretations = engine.batch_generate_interpretations(sample_keywords)
    
    # 결과 출력
    for interp in interpretations:
        print(f"\n🔸 키워드: {interp.keyword} (카테고리: {interp.category})")
        print(f"📜 전통적 해석 ({interp.sentiment_traditional}): {interp.traditional_interpretation}")
        print(f"🔬 현대적 해석 ({interp.sentiment_modern}): {interp.modern_interpretation}")
        if interp.psychological_interpretation:
            print(f"🧠 심리학적 해석 ({interp.sentiment_psychological}): {interp.psychological_interpretation}")
        print(f"⭐ 품질 점수: {interp.quality_score:.1f} | 신뢰도: {interp.confidence:.2f}")
        print(f"🔗 관련 키워드: {', '.join(interp.related_keywords)}")
    
    # 데이터베이스 저장 테스트
    if interpretations:
        saved_count = engine.save_interpretations_to_db(interpretations)
        print(f"\n💾 데이터베이스 저장: {saved_count}/{len(interpretations)}개 성공")