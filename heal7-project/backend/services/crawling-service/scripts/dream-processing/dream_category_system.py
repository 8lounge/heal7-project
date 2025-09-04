#!/usr/bin/env python3
"""
🔮 한국 전통 꿈해몽 카테고리 체계 설계
전문서적 3권 수준의 체계적 분류 시스템

📚 참조: 동양 꿈해몽학, 한국 전통 꿈풀이, 현대 심리학적 꿈해석
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json

class CategoryType(Enum):
    """카테고리 유형"""
    TRADITIONAL = "traditional"  # 전통적 해석
    MODERN = "modern"           # 현대적 해석
    PSYCHOLOGICAL = "psychological"  # 심리학적 해석
    CULTURAL = "cultural"       # 문화적 해석

class InterpretationLevel(Enum):
    """해석 강도 레벨"""
    VERY_POSITIVE = 5  # 매우 긍정적
    POSITIVE = 4       # 긍정적
    NEUTRAL = 3        # 중립적
    NEGATIVE = 2       # 부정적
    VERY_NEGATIVE = 1  # 매우 부정적

@dataclass
class DreamCategory:
    """꿈 카테고리 구조체"""
    id: str
    name: str
    name_en: str
    description: str
    parent_category: Optional[str] = None
    subcategories: List[str] = None
    estimated_keywords: int = 0
    cultural_weight: int = 1  # 1-10, 한국 문화적 중요도

@dataclass
class KeywordTemplate:
    """키워드 템플릿"""
    base_keyword: str
    variations: List[str]
    traditional_interpretation: str
    modern_interpretation: str
    psychological_aspect: str
    related_keywords: List[str]
    category: str
    quality_score: float = 8.0

class DreamCategorySystem:
    """꿈해몽 카테고리 시스템"""
    
    def __init__(self):
        self.categories = self._initialize_categories()
        self.keyword_templates = []
    
    def _initialize_categories(self) -> Dict[str, DreamCategory]:
        """전문서적 수준의 카테고리 체계 초기화"""
        categories = {}
        
        # 1. 자연계 관련 (Nature & Elements) - 2,000개 목표
        categories["nature"] = DreamCategory(
            id="nature",
            name="자연계",
            name_en="nature_elements",
            description="물, 불, 바람, 땅 등 자연 현상과 요소들",
            estimated_keywords=2000,
            cultural_weight=10
        )
        
        categories["water"] = DreamCategory(
            id="water",
            name="물 관련",
            name_en="water_related",
            description="강, 바다, 비, 눈, 얼음 등 모든 물 관련 꿈",
            parent_category="nature",
            estimated_keywords=300,
            cultural_weight=9
        )
        
        categories["fire"] = DreamCategory(
            id="fire",
            name="불 관련",
            name_en="fire_related",
            description="불, 화재, 촛불, 번개 등 불 관련 꿈",
            parent_category="nature",
            estimated_keywords=200,
            cultural_weight=8
        )
        
        categories["earth"] = DreamCategory(
            id="earth",
            name="땅 관련",
            name_en="earth_related",
            description="산, 들판, 흙, 돌, 지진 등 땅 관련 꿈",
            parent_category="nature",
            estimated_keywords=250,
            cultural_weight=8
        )
        
        categories["air"] = DreamCategory(
            id="air",
            name="바람 관련",
            name_en="air_wind",
            description="바람, 태풍, 구름, 하늘 등 공기 관련 꿈",
            parent_category="nature",
            estimated_keywords=180,
            cultural_weight=7
        )
        
        # 2. 동물계 (Animals) - 1,500개 목표
        categories["animals"] = DreamCategory(
            id="animals",
            name="동물",
            name_en="animals",
            description="모든 동물 관련 꿈, 십이지신 포함",
            estimated_keywords=1500,
            cultural_weight=9
        )
        
        categories["zodiac_animals"] = DreamCategory(
            id="zodiac_animals",
            name="십이지신",
            name_en="zodiac_animals",
            description="쥐, 소, 호랑이, 토끼, 용, 뱀, 말, 양, 원숭이, 닭, 개, 돼지",
            parent_category="animals",
            estimated_keywords=240,
            cultural_weight=10
        )
        
        categories["wild_animals"] = DreamCategory(
            id="wild_animals",
            name="야생동물",
            name_en="wild_animals",
            description="사자, 곰, 늑대, 여우 등 야생동물",
            parent_category="animals",
            estimated_keywords=300,
            cultural_weight=8
        )
        
        categories["domestic_animals"] = DreamCategory(
            id="domestic_animals",
            name="가축",
            name_en="domestic_animals",
            description="소, 말, 돼지, 닭, 개, 고양이 등 가축",
            parent_category="animals",
            estimated_keywords=200,
            cultural_weight=7
        )
        
        categories["birds"] = DreamCategory(
            id="birds",
            name="조류",
            name_en="birds",
            description="독수리, 까마귀, 학, 까치, 비둘기 등 새들",
            parent_category="animals",
            estimated_keywords=250,
            cultural_weight=8
        )
        
        categories["insects"] = DreamCategory(
            id="insects",
            name="곤충",
            name_en="insects",
            description="나비, 벌, 개미, 거미 등 곤충류",
            parent_category="animals",
            estimated_keywords=150,
            cultural_weight=6
        )
        
        categories["aquatic_animals"] = DreamCategory(
            id="aquatic_animals",
            name="수생동물",
            name_en="aquatic_animals",
            description="물고기, 거북이, 고래, 상어 등 물속 동물",
            parent_category="animals",
            estimated_keywords=200,
            cultural_weight=7
        )
        
        # 3. 인간관계 (Relationships) - 1,200개 목표
        categories["people"] = DreamCategory(
            id="people",
            name="사람",
            name_en="people_relationships",
            description="가족, 친구, 연인, 직장 동료 등 인간관계",
            estimated_keywords=1200,
            cultural_weight=10
        )
        
        categories["family"] = DreamCategory(
            id="family",
            name="가족",
            name_en="family",
            description="부모, 형제자매, 조상, 후손 등 가족 관련",
            parent_category="people",
            estimated_keywords=300,
            cultural_weight=10
        )
        
        categories["romance"] = DreamCategory(
            id="romance",
            name="연애/결혼",
            name_en="romance_marriage",
            description="연인, 배우자, 결혼식, 이별 등 연애 관련",
            parent_category="people",
            estimated_keywords=250,
            cultural_weight=9
        )
        
        categories["social"] = DreamCategory(
            id="social",
            name="사회관계",
            name_en="social_relationships",
            description="친구, 동료, 상사, 선생님 등 사회적 관계",
            parent_category="people",
            estimated_keywords=200,
            cultural_weight=8
        )
        
        categories["strangers"] = DreamCategory(
            id="strangers",
            name="낯선 사람",
            name_en="strangers",
            description="모르는 사람, 유명인, 역사적 인물 등",
            parent_category="people",
            estimated_keywords=180,
            cultural_weight=6
        )
        
        # 4. 신체/건강 (Body & Health) - 800개 목표
        categories["body"] = DreamCategory(
            id="body",
            name="신체",
            name_en="body_health",
            description="신체 부위, 건강, 질병, 치료 등",
            estimated_keywords=800,
            cultural_weight=9
        )
        
        categories["body_parts"] = DreamCategory(
            id="body_parts",
            name="신체 부위",
            name_en="body_parts",
            description="머리, 눈, 손, 발 등 신체 각 부위",
            parent_category="body",
            estimated_keywords=200,
            cultural_weight=8
        )
        
        categories["health"] = DreamCategory(
            id="health",
            name="건강/질병",
            name_en="health_disease",
            description="병, 치료, 의료, 약 등 건강 관련",
            parent_category="body",
            estimated_keywords=200,
            cultural_weight=9
        )
        
        categories["death_birth"] = DreamCategory(
            id="death_birth",
            name="생사",
            name_en="death_birth",
            description="죽음, 탄생, 임신, 장례 등 생사 관련",
            parent_category="body",
            estimated_keywords=150,
            cultural_weight=10
        )
        
        # 5. 행동/활동 (Actions & Activities) - 1,000개 목표
        categories["actions"] = DreamCategory(
            id="actions",
            name="행동/활동",
            name_en="actions_activities",
            description="움직임, 일, 놀이, 운동 등 모든 행동",
            estimated_keywords=1000,
            cultural_weight=8
        )
        
        categories["movement"] = DreamCategory(
            id="movement",
            name="이동/움직임",
            name_en="movement",
            description="걷기, 뛰기, 날기, 떨어지기 등 움직임",
            parent_category="actions",
            estimated_keywords=200,
            cultural_weight=8
        )
        
        categories["work"] = DreamCategory(
            id="work",
            name="일/노동",
            name_en="work_labor",
            description="직업, 일하기, 공부, 창작 등 노동 활동",
            parent_category="actions",
            estimated_keywords=250,
            cultural_weight=8
        )
        
        categories["leisure"] = DreamCategory(
            id="leisure",
            name="여가/놀이",
            name_en="leisure_play",
            description="게임, 여행, 스포츠, 춤 등 여가 활동",
            parent_category="actions",
            estimated_keywords=200,
            cultural_weight=7
        )
        
        categories["communication"] = DreamCategory(
            id="communication",
            name="소통",
            name_en="communication",
            description="말하기, 듣기, 전화, 편지 등 의사소통",
            parent_category="actions",
            estimated_keywords=150,
            cultural_weight=7
        )
        
        # 6. 물질/재물 (Objects & Wealth) - 1,200개 목표
        categories["objects"] = DreamCategory(
            id="objects",
            name="물건/재물",
            name_en="objects_wealth",
            description="돈, 보석, 도구, 의복 등 물질적 요소",
            estimated_keywords=1200,
            cultural_weight=9
        )
        
        categories["money"] = DreamCategory(
            id="money",
            name="돈/재물",
            name_en="money_wealth",
            description="현금, 금, 은, 보석, 부동산 등 재산",
            parent_category="objects",
            estimated_keywords=200,
            cultural_weight=10
        )
        
        categories["clothing"] = DreamCategory(
            id="clothing",
            name="의복",
            name_en="clothing",
            description="옷, 신발, 모자, 액세서리 등 착용물",
            parent_category="objects",
            estimated_keywords=180,
            cultural_weight=7
        )
        
        categories["food"] = DreamCategory(
            id="food",
            name="음식",
            name_en="food",
            description="밥, 고기, 과일, 술 등 모든 음식물",
            parent_category="objects",
            estimated_keywords=300,
            cultural_weight=8
        )
        
        categories["tools"] = DreamCategory(
            id="tools",
            name="도구/기계",
            name_en="tools_machines",
            description="칼, 망치, 자동차, 전자기기 등 도구류",
            parent_category="objects",
            estimated_keywords=250,
            cultural_weight=6
        )
        
        # 7. 장소/공간 (Places & Spaces) - 1,000개 목표
        categories["places"] = DreamCategory(
            id="places",
            name="장소/공간",
            name_en="places_spaces",
            description="집, 학교, 회사, 자연 장소 등 공간",
            estimated_keywords=1000,
            cultural_weight=8
        )
        
        categories["home"] = DreamCategory(
            id="home",
            name="집/가정",
            name_en="home_domestic",
            description="집, 방, 침실, 부엌 등 가정 공간",
            parent_category="places",
            estimated_keywords=200,
            cultural_weight=9
        )
        
        categories["public_places"] = DreamCategory(
            id="public_places",
            name="공공장소",
            name_en="public_places",
            description="학교, 병원, 은행, 시장 등 공공 시설",
            parent_category="places",
            estimated_keywords=250,
            cultural_weight=7
        )
        
        categories["natural_places"] = DreamCategory(
            id="natural_places",
            name="자연 장소",
            name_en="natural_places",
            description="산, 바다, 강, 숲, 들판 등 자연 공간",
            parent_category="places",
            estimated_keywords=200,
            cultural_weight=8
        )
        
        categories["religious_places"] = DreamCategory(
            id="religious_places",
            name="종교적 장소",
            name_en="religious_places",
            description="절, 교회, 사찰, 제단 등 종교 공간",
            parent_category="places",
            estimated_keywords=120,
            cultural_weight=8
        )
        
        # 8. 종교/신화 (Religion & Mythology) - 800개 목표
        categories["religion"] = DreamCategory(
            id="religion",
            name="종교/신화",
            name_en="religion_mythology",
            description="불교, 기독교, 무속, 신화적 존재 등",
            estimated_keywords=800,
            cultural_weight=9
        )
        
        categories["buddhism"] = DreamCategory(
            id="buddhism",
            name="불교",
            name_en="buddhism",
            description="부처, 스님, 절, 법당, 염주 등 불교 관련",
            parent_category="religion",
            estimated_keywords=150,
            cultural_weight=9
        )
        
        categories["christianity"] = DreamCategory(
            id="christianity",
            name="기독교",
            name_en="christianity",
            description="예수, 천사, 교회, 십자가 등 기독교 관련",
            parent_category="religion",
            estimated_keywords=120,
            cultural_weight=7
        )
        
        categories["shamanism"] = DreamCategory(
            id="shamanism",
            name="무속/민간신앙",
            name_en="shamanism",
            description="무당, 굿, 조상신, 산신 등 무속 관련",
            parent_category="religion",
            estimated_keywords=200,
            cultural_weight=10
        )
        
        categories["mythology"] = DreamCategory(
            id="mythology",
            name="신화/전설",
            name_en="mythology",
            description="용, 봉황, 신선, 도깨비 등 신화적 존재",
            parent_category="religion",
            estimated_keywords=180,
            cultural_weight=9
        )
        
        # 9. 상황/사건 (Situations & Events) - 1,200개 목표
        categories["situations"] = DreamCategory(
            id="situations",
            name="상황/사건",
            name_en="situations_events",
            description="특별한 상황, 사건, 위기, 축하 등",
            estimated_keywords=1200,
            cultural_weight=8
        )
        
        categories["crisis"] = DreamCategory(
            id="crisis",
            name="위기/위험",
            name_en="crisis_danger",
            description="화재, 지진, 사고, 추락 등 위험한 상황",
            parent_category="situations",
            estimated_keywords=200,
            cultural_weight=8
        )
        
        categories["celebration"] = DreamCategory(
            id="celebration",
            name="축하/기쁨",
            name_en="celebration_joy",
            description="결혼식, 생일, 승진, 합격 등 기쁜 일",
            parent_category="situations",
            estimated_keywords=180,
            cultural_weight=8
        )
        
        categories["conflict"] = DreamCategory(
            id="conflict",
            name="갈등/다툼",
            name_en="conflict_fight",
            description="싸움, 전쟁, 논쟁, 경쟁 등 갈등 상황",
            parent_category="situations",
            estimated_keywords=150,
            cultural_weight=7
        )
        
        categories["test"] = DreamCategory(
            id="test",
            name="시험/평가",
            name_en="test_evaluation",
            description="시험, 면접, 경연, 평가 등 시험 상황",
            parent_category="situations",
            estimated_keywords=120,
            cultural_weight=8
        )
        
        # 10. 감정/심리 (Emotions & Psychology) - 500개 목표
        categories["emotions"] = DreamCategory(
            id="emotions",
            name="감정/심리",
            name_en="emotions_psychology",
            description="기쁨, 슬픔, 분노, 두려움 등 감정 상태",
            estimated_keywords=500,
            cultural_weight=9
        )
        
        categories["positive_emotions"] = DreamCategory(
            id="positive_emotions",
            name="긍정 감정",
            name_en="positive_emotions",
            description="기쁨, 행복, 평화, 만족 등 긍정적 감정",
            parent_category="emotions",
            estimated_keywords=120,
            cultural_weight=8
        )
        
        categories["negative_emotions"] = DreamCategory(
            id="negative_emotions",
            name="부정 감정",
            name_en="negative_emotions",
            description="슬픔, 분노, 두려움, 절망 등 부정적 감정",
            parent_category="emotions",
            estimated_keywords=150,
            cultural_weight=8
        )
        
        return categories
    
    def generate_keyword_templates(self) -> List[KeywordTemplate]:
        """카테고리별 키워드 템플릿 생성"""
        templates = []
        
        # 물 관련 키워드들 (샘플)
        water_templates = [
            KeywordTemplate(
                base_keyword="물",
                variations=["맑은 물", "더러운 물", "흐르는 물", "고인 물"],
                traditional_interpretation="물은 재물과 생명력을 상징합니다. 맑은 물을 마시면 좋은 일이 생기고, 더러운 물은 병이나 근심을 의미합니다.",
                modern_interpretation="물은 무의식과 감정을 나타냅니다. 물의 상태는 현재 심리 상태를 반영하며, 정화와 재생의 의미를 가집니다.",
                psychological_aspect="물은 생명의 근원이자 무의식의 상징으로, 꿈속의 물은 감정적 상태와 정신적 정화 욕구를 나타냅니다.",
                related_keywords=["바다", "강", "비", "샘물", "우물"],
                category="water",
                quality_score=9.5
            ),
            KeywordTemplate(
                base_keyword="바다",
                variations=["잔잔한 바다", "파도치는 바다", "깊은 바다", "바닷가"],
                traditional_interpretation="바다는 큰 재물이나 넓은 세상을 의미합니다. 잔잔한 바다는 평안을, 거친 바다는 시련을 나타냅니다.",
                modern_interpretation="바다는 무한한 가능성과 무의식의 깊이를 상징합니다. 인생의 큰 변화나 새로운 시작을 암시합니다.",
                psychological_aspect="바다는 집단무의식과 어머니 원형을 나타내며, 감정의 깊이와 삶의 근본적 변화를 상징합니다.",
                related_keywords=["물", "파도", "해변", "배", "물고기"],
                category="water",
                quality_score=9.0
            )
        ]
        
        templates.extend(water_templates)
        return templates
    
    def get_category_hierarchy(self) -> Dict:
        """카테고리 계층 구조 반환"""
        hierarchy = {}
        for cat_id, category in self.categories.items():
            if category.parent_category is None:
                hierarchy[cat_id] = {
                    'name': category.name,
                    'estimated_keywords': category.estimated_keywords,
                    'children': []
                }
        
        # 자식 카테고리 추가
        for cat_id, category in self.categories.items():
            if category.parent_category:
                parent_id = category.parent_category
                if parent_id in hierarchy:
                    hierarchy[parent_id]['children'].append({
                        'id': cat_id,
                        'name': category.name,
                        'estimated_keywords': category.estimated_keywords
                    })
        
        return hierarchy
    
    def export_to_json(self, filepath: str):
        """카테고리 시스템을 JSON으로 내보내기"""
        data = {
            'categories': {
                cat_id: {
                    'id': cat.id,
                    'name': cat.name,
                    'name_en': cat.name_en,
                    'description': cat.description,
                    'parent_category': cat.parent_category,
                    'estimated_keywords': cat.estimated_keywords,
                    'cultural_weight': cat.cultural_weight
                }
                for cat_id, cat in self.categories.items()
            },
            'hierarchy': self.get_category_hierarchy(),
            'total_estimated_keywords': sum(cat.estimated_keywords for cat in self.categories.values() if cat.parent_category is None),
            'metadata': {
                'created_at': '2025-09-04',
                'version': '1.0',
                'description': '한국 전통 꿈해몽 카테고리 체계 - 전문서적 3권 수준'
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 카테고리 시스템 초기화 및 테스트
    system = DreamCategorySystem()
    
    # 계층 구조 출력
    hierarchy = system.get_category_hierarchy()
    print("🔮 한국 전통 꿈해몽 카테고리 체계")
    print("=" * 50)
    
    total_keywords = 0
    for main_cat, info in hierarchy.items():
        print(f"\n📂 {info['name']} ({info['estimated_keywords']}개)")
        total_keywords += info['estimated_keywords']
        
        for child in info['children']:
            print(f"   └── {child['name']} ({child['estimated_keywords']}개)")
    
    print(f"\n🎯 총 예상 키워드: {total_keywords:,}개")
    print("✅ 목표 10,000개 키워드 달성 가능")
    
    # JSON으로 내보내기
    system.export_to_json('/home/ubuntu/heal7-project/backend/services/crawling-service/scripts/dream-processing/dream_category_system.json')
    print("\n💾 카테고리 시스템이 JSON으로 저장되었습니다.")