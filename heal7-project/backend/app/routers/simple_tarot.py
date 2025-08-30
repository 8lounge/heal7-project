"""
Simple Tarot API
기본적인 타로 카드 점술 API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import random

router = APIRouter(prefix="/fortune/tarot", tags=["타로"])

class TarotCard(BaseModel):
    """타로 카드 모델"""
    name: str = Field(..., description="카드명")
    meaning: str = Field(..., description="카드 의미")
    reversed: bool = Field(False, description="역방향 여부")
    image_url: str = Field("", description="카드 이미지 URL")

class TarotReading(BaseModel):
    """타로 리딩 결과"""
    question: str = Field(..., description="질문")
    cards: List[TarotCard] = Field(..., description="뽑힌 카드들")
    interpretation: str = Field(..., description="해석")
    advice: str = Field(..., description="조언")
    timestamp: datetime = Field(default_factory=datetime.now)

# 간단한 타로 카드 데이터
TAROT_CARDS = [
    {"name": "바보(The Fool)", "meaning": "새로운 시작, 순수함, 모험"},
    {"name": "마법사(The Magician)", "meaning": "의지력, 창조, 능력"},
    {"name": "여교황(The High Priestess)", "meaning": "직감, 신비, 내면의 지혜"},
    {"name": "여황제(The Empress)", "meaning": "풍요로움, 모성, 창조성"},
    {"name": "황제(The Emperor)", "meaning": "권위, 질서, 안정"},
    {"name": "교황(The Hierophant)", "meaning": "전통, 가르침, 영성"},
    {"name": "연인(The Lovers)", "meaning": "사랑, 선택, 화합"},
    {"name": "전차(The Chariot)", "meaning": "의지력, 승리, 전진"},
    {"name": "힘(Strength)", "meaning": "용기, 인내, 내면의 힘"},
    {"name": "은둔자(The Hermit)", "meaning": "내면 탐구, 지혜, 고독"},
    {"name": "운명의 바퀴(Wheel of Fortune)", "meaning": "변화, 운명, 기회"},
    {"name": "정의(Justice)", "meaning": "균형, 공정함, 진실"},
    {"name": "매달린 사람(The Hanged Man)", "meaning": "희생, 관점 전환, 기다림"},
    {"name": "죽음(Death)", "meaning": "변화, 끝과 시작, 재생"},
    {"name": "절제(Temperance)", "meaning": "조화, 균형, 인내"},
    {"name": "악마(The Devil)", "meaning": "유혹, 속박, 물질주의"},
    {"name": "탑(The Tower)", "meaning": "갑작스런 변화, 파괴, 깨달음"},
    {"name": "별(The Star)", "meaning": "희망, 영감, 치유"},
    {"name": "달(The Moon)", "meaning": "환상, 두려움, 무의식"},
    {"name": "태양(The Sun)", "meaning": "기쁨, 성공, 활력"},
    {"name": "심판(Judgement)", "meaning": "부활, 각성, 결정"},
    {"name": "세계(The World)", "meaning": "완성, 성취, 통합"},
]

@router.get("/draw-card", summary="1장 뽑기")
async def draw_single_card(
    question: str = Query(..., description="질문 또는 고민")
) -> TarotReading:
    """간단한 1장 타로 카드 뽑기"""
    
    # 랜덤하게 카드 선택
    card_data = random.choice(TAROT_CARDS)
    reversed = random.choice([True, False])
    
    card = TarotCard(
        name=card_data["name"],
        meaning=card_data["meaning"],
        reversed=reversed,
        image_url=f"/api/tarot/images/{card_data['name'].split('(')[0].strip()}.jpg"
    )
    
    # 간단한 해석 생성
    if reversed:
        interpretation = f"역방향으로 나온 '{card.name}' 카드는 현재 상황에서 {card.meaning}의 반대적 측면이나 내면의 변화가 필요함을 의미합니다."
        advice = "현재의 접근 방식을 재검토하고 새로운 시각으로 문제를 바라보는 것이 도움이 될 것입니다."
    else:
        interpretation = f"'{card.name}' 카드가 나타내는 {card.meaning}이(가) 현재 상황과 깊은 연관이 있습니다."
        advice = "카드의 에너지를 받아들이고 긍정적인 방향으로 활용해보세요."
    
    return TarotReading(
        question=question,
        cards=[card],
        interpretation=interpretation,
        advice=advice
    )

@router.get("/three-card-spread", summary="3장 스프레드")
async def three_card_spread(
    question: str = Query(..., description="질문 또는 고민")
) -> TarotReading:
    """과거-현재-미래 3장 타로 스프레드"""
    
    # 3장의 서로 다른 카드 선택
    selected_cards_data = random.sample(TAROT_CARDS, 3)
    cards = []
    positions = ["과거", "현재", "미래"]
    
    for i, card_data in enumerate(selected_cards_data):
        reversed = random.choice([True, False])
        card = TarotCard(
            name=f"{positions[i]} - {card_data['name']}",
            meaning=card_data["meaning"],
            reversed=reversed,
            image_url=f"/api/tarot/images/{card_data['name'].split('(')[0].strip()}.jpg"
        )
        cards.append(card)
    
    # 3장 해석 생성
    interpretation = f"""
    과거: {cards[0].name}은(는) 당신의 과거 경험이 {cards[0].meaning}와 관련이 있음을 보여줍니다.
    현재: {cards[1].name}은(는) 현재 상황에서 {cards[1].meaning}이(가) 중요함을 나타냅니다.
    미래: {cards[2].name}은(는) 앞으로 {cards[2].meaning}의 에너지가 영향을 미칠 것을 의미합니다.
    """
    
    advice = "과거의 경험을 바탕으로 현재를 이해하고, 미래를 향한 준비를 하는 것이 중요합니다. 각 카드의 메시지를 종합하여 균형잡힌 관점을 가져보세요."
    
    return TarotReading(
        question=question,
        cards=cards,
        interpretation=interpretation.strip(),
        advice=advice
    )

@router.get("/love-reading", summary="연애 타로")
async def love_reading(
    question: str = Query("현재 나의 연애운은?", description="연애 관련 질문")
) -> TarotReading:
    """연애 운세 전용 타로 리딩"""
    
    # 연애와 관련성 높은 카드들을 우선 선택
    love_related_cards = [
        {"name": "연인(The Lovers)", "meaning": "진정한 사랑, 운명적 만남"},
        {"name": "여교황(The High Priestess)", "meaning": "직감적 사랑, 내면의 목소리"},
        {"name": "여황제(The Empress)", "meaning": "매력적 관계, 풍요로운 사랑"},
        {"name": "별(The Star)", "meaning": "희망적 연애, 이상적 관계"},
        {"name": "태양(The Sun)", "meaning": "행복한 관계, 밝은 연애"},
        {"name": "운명의 바퀴(Wheel of Fortune)", "meaning": "연애 운의 변화"},
    ]
    
    # 일반 카드와 연애 카드 중에서 선택
    all_cards = love_related_cards + random.sample(TAROT_CARDS, 5)
    selected_card_data = random.choice(all_cards)
    reversed = random.choice([True, False])
    
    card = TarotCard(
        name=selected_card_data["name"],
        meaning=selected_card_data["meaning"],
        reversed=reversed,
        image_url=f"/api/tarot/images/{selected_card_data['name'].split('(')[0].strip()}.jpg"
    )
    
    # 연애 특화 해석
    if "연인" in card.name or "사랑" in card.meaning:
        interpretation = f"연애운에서 '{card.name}' 카드는 특별한 의미를 가집니다. {card.meaning}이(가) 당신의 사랑에 긍정적인 영향을 미칠 것입니다."
        advice = "마음을 열고 진실한 감정을 표현하는 것이 좋습니다. 상대방과의 깊은 소통을 통해 관계를 발전시켜보세요."
    else:
        interpretation = f"'{card.name}' 카드를 통해 보는 연애운은 {card.meaning}와 연관되어 있습니다."
        advice = "연애에서도 카드가 제시하는 에너지를 활용해보세요. 자신의 매력을 발견하고 자신감을 가지는 것이 중요합니다."
    
    return TarotReading(
        question=question,
        cards=[card],
        interpretation=interpretation,
        advice=advice
    )

@router.get("/daily-card", summary="오늘의 카드")
async def daily_card() -> TarotReading:
    """오늘의 타로 카드"""
    
    # 날짜 기반으로 시드 설정 (같은 날에는 같은 카드)
    today = datetime.now().date()
    random.seed(str(today))
    
    card_data = random.choice(TAROT_CARDS)
    reversed = random.choice([True, False])
    
    card = TarotCard(
        name=card_data["name"],
        meaning=card_data["meaning"],
        reversed=reversed,
        image_url=f"/api/tarot/images/{card_data['name'].split('(')[0].strip()}.jpg"
    )
    
    interpretation = f"오늘의 카드 '{card.name}'는 {card.meaning}의 에너지를 가지고 있습니다. 오늘 하루 이러한 에너지를 염두에 두고 행동해보세요."
    
    if reversed:
        advice = "역방향 카드는 내면의 변화나 다른 관점이 필요함을 의미합니다. 평소와 다른 접근을 시도해보세요."
    else:
        advice = "카드의 긍정적인 에너지를 받아들이고 적극적으로 활용하는 하루가 되길 바랍니다."
    
    return TarotReading(
        question="오늘의 운세는?",
        cards=[card],
        interpretation=interpretation,
        advice=advice
    )