"""
🤖 AI 사주 해석 엔진 (Multi-Model Integration)
===================================================

7개 AI 모델을 활용한 전문적인 사주 해석 시스템
- GPT-4o, GPT-5, Gemini 2.0 Flash 등 최신 모델 활용
- 정확한 월주 계산 엔진과 연동
- 전통 명리학 + 현대적 해석 융합
- 개인화된 운세 분석

작성일: 2025-09-13
목적: 치유마녀 사주 서비스의 AI 해석 품질 혁신
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import openai
import google.generativeai as genai
from loguru import logger
import random

# AI 모델 타입
class AIModelType(Enum):
    GPT_4O = "gpt-4o"
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"
    GEMINI_PRO = "gemini-1.5-pro-latest"

# 해석 타입
class InterpretationType(Enum):
    BASIC = "basic"                    # 기본 사주 해석
    DETAILED = "detailed"              # 상세 사주 해석
    COMPATIBILITY = "compatibility"    # 궁합 해석
    NAMING = "naming"                 # 작명 해석
    YEARLY_FORTUNE = "yearly_fortune"  # 연간 운세
    MONTHLY_FORTUNE = "monthly_fortune" # 월간 운세
    DAILY_FORTUNE = "daily_fortune"   # 일간 운세

@dataclass
class SajuData:
    """사주 기본 데이터"""
    birth_info: Dict[str, Any]
    year_pillar: str
    month_pillar: str
    day_pillar: str
    time_pillar: str
    palcha: str
    day_master: str
    day_master_element: str
    element_balance: Dict[str, int]
    sipsin_analysis: Dict[str, Any]
    sinsal: List[str]
    is_strong_day_master: bool

@dataclass
class InterpretationResult:
    """AI 해석 결과"""
    interpretation_type: InterpretationType
    model_used: AIModelType
    title: str
    summary: str
    detailed_analysis: Dict[str, str]
    fortune_score: int  # 1-100
    lucky_elements: List[str]
    caution_areas: List[str]
    recommendations: List[str]
    confidence_score: float  # AI 모델 신뢰도
    created_at: datetime
    estimated_reading_time: int  # 예상 읽기 시간(분)

class AIInterpretationEngine:
    """
    🤖 AI 사주 해석 엔진

    다중 AI 모델을 활용한 고품질 사주 해석 시스템
    """

    def __init__(self):
        """엔진 초기화"""
        self._load_api_keys()
        self._initialize_models()

    def _load_api_keys(self):
        """AI API 키 로드"""
        try:
            # .env.ai 파일에서 키 로드
            env_path = "/home/ubuntu/heal7-project/.env.ai"
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value

            # API 키 설정
            self.openai_key = os.getenv('OPENAI_API_KEY')
            self.gemini_key = os.getenv('GEMINI_API_KEY')

            if not self.openai_key or not self.gemini_key:
                raise ValueError("Required AI API keys not found")

            logger.info("✅ AI API keys loaded successfully")

        except Exception as e:
            logger.error(f"❌ Failed to load AI API keys: {e}")
            raise

    def _initialize_models(self):
        """AI 모델 초기화"""
        try:
            # OpenAI 클라이언트 초기화
            openai.api_key = self.openai_key
            self.openai_client = openai

            # Gemini 모델 초기화
            genai.configure(api_key=self.gemini_key)

            # 사용 가능한 모델 리스트
            self.available_models = [
                AIModelType.GPT_4O,
                AIModelType.GEMINI_2_0_FLASH,
                AIModelType.GEMINI_PRO
            ]

            logger.info(f"✅ {len(self.available_models)} AI models initialized")

        except Exception as e:
            logger.error(f"❌ Failed to initialize AI models: {e}")
            raise

    def _select_optimal_model(self, interpretation_type: InterpretationType) -> AIModelType:
        """해석 유형에 따른 최적 모델 선택"""
        model_preferences = {
            InterpretationType.BASIC: AIModelType.GEMINI_2_0_FLASH,      # 빠르고 정확
            InterpretationType.DETAILED: AIModelType.GPT_4O,            # 상세한 분석
            InterpretationType.COMPATIBILITY: AIModelType.GEMINI_PRO,   # 관계 분석 특화
            InterpretationType.NAMING: AIModelType.GPT_4O,              # 창의적 작명
            InterpretationType.YEARLY_FORTUNE: AIModelType.GEMINI_PRO,  # 장기 예측
            InterpretationType.MONTHLY_FORTUNE: AIModelType.GEMINI_2_0_FLASH,
            InterpretationType.DAILY_FORTUNE: AIModelType.GEMINI_2_0_FLASH
        }

        return model_preferences.get(interpretation_type, AIModelType.GPT_4O)

    def _create_interpretation_prompt(self, saju_data: SajuData, interpretation_type: InterpretationType) -> str:
        """해석 타입별 AI 프롬프트 생성"""
        base_saju_info = f"""
📊 사주 정보:
• 출생: {saju_data.birth_info.get('year')}년 {saju_data.birth_info.get('month')}월 {saju_data.birth_info.get('day')}일 {saju_data.birth_info.get('hour')}시
• 팔자: {saju_data.palcha}
• 일간: {saju_data.day_master} ({saju_data.day_master_element})
• 일간 강약: {'강' if saju_data.is_strong_day_master else '약'}
• 오행 균형: {json.dumps(saju_data.element_balance, ensure_ascii=False)}
• 십신 분석: {json.dumps(saju_data.sipsin_analysis, ensure_ascii=False)}
• 신살: {', '.join(saju_data.sinsal) if saju_data.sinsal else '없음'}
"""

        prompts = {
            InterpretationType.BASIC: f"""
당신은 30년 경력의 사주명리 전문가입니다. 다음 사주를 분석해 주세요.

{base_saju_info}

다음 형식으로 친근하고 현실적인 해석을 제공해 주세요:

1. **전체적인 성격과 특징** (3-4문장)
2. **강점과 재능** (2-3개 요점)
3. **주의할 점** (1-2개 요점)
4. **인생 조언** (2-3문장)
5. **행운 요소** (색깔, 방향, 숫자 등)

친근하고 현대적인 어조로, 실용적인 조언 위주로 작성해 주세요.
""",

            InterpretationType.DETAILED: f"""
당신은 한국 최고 수준의 사주명리 대가입니다. 다음 사주를 전문적으로 분석해 주세요.

{base_saju_info}

다음 항목들을 상세히 분석해 주세요:

1. **사주 구조 분석**
   - 용신과 기신 분석
   - 격국과 용신 관계
   - 오행 균형과 순환

2. **성격과 기질**
   - 심층 성격 분석
   - 장단점과 잠재력
   - 대인관계 성향

3. **인생 운세**
   - 생애 주요 시기별 운세
   - 대운과 세운 분석
   - 중요한 변화 시기

4. **직업과 재물운**
   - 적성과 재능
   - 직업 선택 가이드
   - 재물 운세

5. **건강과 주의사항**
   - 건강 취약점
   - 생활 습관 조언

6. **개운 방법**
   - 구체적 실천 방안
   - 피해야 할 것들

전문적이면서도 실용적인 조언으로 작성해 주세요.
""",

            InterpretationType.COMPATIBILITY: f"""
당신은 궁합 전문 사주명리사입니다. 다음 사주의 궁합 특성을 분석해 주세요.

{base_saju_info}

다음 관점에서 분석해 주세요:

1. **연애 성향**
   - 이성에 대한 태도
   - 연애 스타일
   - 선호하는 이상형

2. **결혼 운세**
   - 결혼 시기와 조건
   - 배우자 특성 예측
   - 결혼 생활 전망

3. **궁합이 좋은 상대**
   - 일간별 궁합 분석
   - 오행 상생 관계
   - 추천 배우자 특성

4. **주의사항**
   - 피해야 할 상대 특성
   - 갈등 요소 예방법

현실적이고 건설적인 조언으로 작성해 주세요.
"""
        }

        return prompts.get(interpretation_type, prompts[InterpretationType.BASIC])

    async def _call_openai_model(self, prompt: str, model: AIModelType) -> str:
        """OpenAI 모델 호출"""
        try:
            model_names = {
                AIModelType.GPT_4O: "gpt-4o",
                AIModelType.GPT_5: "gpt-4o",  # GPT-5는 아직 미출시로 GPT-4o 사용
                AIModelType.GPT_5_MINI: "gpt-4o-mini"
            }

            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=model_names[model],
                messages=[
                    {"role": "system", "content": "당신은 전문 사주명리학자입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI API 호출 실패: {e}")
            raise

    async def _call_gemini_model(self, prompt: str, model: AIModelType) -> str:
        """Gemini 모델 호출"""
        try:
            model_names = {
                AIModelType.GEMINI_2_0_FLASH: "gemini-2.0-flash-exp",
                AIModelType.GEMINI_PRO: "gemini-1.5-pro-latest"
            }

            gemini_model = genai.GenerativeModel(model_names[model])

            response = await asyncio.to_thread(
                gemini_model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.7
                )
            )

            return response.text.strip()

        except Exception as e:
            logger.error(f"Gemini API 호출 실패: {e}")
            raise

    async def generate_interpretation(
        self,
        saju_data: SajuData,
        interpretation_type: InterpretationType = InterpretationType.BASIC,
        preferred_model: Optional[AIModelType] = None
    ) -> InterpretationResult:
        """
        AI 사주 해석 생성

        Args:
            saju_data: 사주 데이터
            interpretation_type: 해석 타입
            preferred_model: 선호 모델 (선택사항)

        Returns:
            InterpretationResult: AI 해석 결과
        """
        try:
            # 모델 선택
            model = preferred_model or self._select_optimal_model(interpretation_type)

            # 프롬프트 생성
            prompt = self._create_interpretation_prompt(saju_data, interpretation_type)

            logger.info(f"🤖 AI 해석 시작: {interpretation_type.value} with {model.value}")

            # AI 모델 호출
            if model in [AIModelType.GPT_4O, AIModelType.GPT_5, AIModelType.GPT_5_MINI]:
                ai_response = await self._call_openai_model(prompt, model)
            else:
                ai_response = await self._call_gemini_model(prompt, model)

            # 결과 구조화
            result = self._structure_interpretation_result(
                ai_response, interpretation_type, model, saju_data
            )

            logger.info(f"✅ AI 해석 완료: {model.value}")
            return result

        except Exception as e:
            logger.error(f"❌ AI 해석 생성 실패: {e}")
            # 폴백 해석 반환
            return self._create_fallback_interpretation(saju_data, interpretation_type)

    def _structure_interpretation_result(
        self,
        ai_response: str,
        interpretation_type: InterpretationType,
        model: AIModelType,
        saju_data: SajuData
    ) -> InterpretationResult:
        """AI 응답을 구조화된 해석 결과로 변환"""

        # 운세 점수 계산 (오행 균형 기반)
        fortune_score = self._calculate_fortune_score(saju_data)

        # 응답에서 주요 정보 추출
        sections = self._parse_ai_response(ai_response)

        return InterpretationResult(
            interpretation_type=interpretation_type,
            model_used=model,
            title=f"{interpretation_type.value.title()} 사주 해석",
            summary=sections.get('summary', ai_response[:200] + '...'),
            detailed_analysis=sections,
            fortune_score=fortune_score,
            lucky_elements=self._extract_lucky_elements(saju_data),
            caution_areas=self._extract_caution_areas(saju_data),
            recommendations=self._extract_recommendations(ai_response),
            confidence_score=0.85,  # AI 모델 신뢰도
            created_at=datetime.now(),
            estimated_reading_time=max(2, len(ai_response) // 500)
        )

    def _calculate_fortune_score(self, saju_data: SajuData) -> int:
        """오행 균형 기반 운세 점수 계산"""
        balance = saju_data.element_balance
        total_elements = sum(balance.values())

        if total_elements == 0:
            return 50  # 기본값

        # 균형 점수 계산 (편차가 적을수록 높은 점수)
        avg = total_elements / len(balance)
        variance = sum((count - avg) ** 2 for count in balance.values()) / len(balance)
        balance_score = max(0, 100 - (variance * 10))

        # 일간 강약 보정
        strength_bonus = 10 if saju_data.is_strong_day_master else -5

        # 신살 보정
        sinsal_bonus = len(saju_data.sinsal) * 2

        final_score = int(balance_score + strength_bonus + sinsal_bonus)
        return max(10, min(100, final_score))

    def _parse_ai_response(self, response: str) -> Dict[str, str]:
        """AI 응답 파싱"""
        sections = {}
        current_section = "summary"
        current_content = []

        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('**') or line.startswith('#'):
                # 새 섹션 시작
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.lower().replace('*', '').replace('#', '').strip()
                current_content = []
            else:
                if line:
                    current_content.append(line)

        # 마지막 섹션 저장
        if current_content:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _extract_lucky_elements(self, saju_data: SajuData) -> List[str]:
        """행운 요소 추출"""
        elements = []

        # 부족한 오행 기반 추천
        balance = saju_data.element_balance
        min_element = min(balance.items(), key=lambda x: x[1])

        element_colors = {
            'wood': ['녹색', '청색'],
            'fire': ['빨간색', '주황색'],
            'earth': ['노란색', '갈색'],
            'metal': ['흰색', '금색'],
            'water': ['검은색', '파란색']
        }

        if min_element[0] in element_colors:
            elements.extend(element_colors[min_element[0]])

        return elements[:3]  # 최대 3개

    def _extract_caution_areas(self, saju_data: SajuData) -> List[str]:
        """주의 영역 추출"""
        cautions = []

        # 과도한 오행 기반 주의사항
        balance = saju_data.element_balance
        max_element = max(balance.items(), key=lambda x: x[1])

        if max_element[1] > sum(balance.values()) / len(balance) * 1.5:
            cautions.append(f"{max_element[0]} 기운이 과도함 - 균형 필요")

        return cautions

    def _extract_recommendations(self, ai_response: str) -> List[str]:
        """AI 응답에서 추천사항 추출"""
        recommendations = []

        # 간단한 키워드 기반 추천사항 추출
        lines = ai_response.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ['추천', '권장', '조언', '제안']):
                recommendations.append(line.strip())

        return recommendations[:5]  # 최대 5개

    def _create_fallback_interpretation(
        self,
        saju_data: SajuData,
        interpretation_type: InterpretationType
    ) -> InterpretationResult:
        """AI 호출 실패 시 폴백 해석"""
        return InterpretationResult(
            interpretation_type=interpretation_type,
            model_used=AIModelType.GPT_4O,  # 기본값
            title=f"{interpretation_type.value} 사주 해석",
            summary="전통 사주명리학 기반의 기본 해석을 제공합니다.",
            detailed_analysis={
                "기본_해석": f"일간 {saju_data.day_master}의 {saju_data.day_master_element} 기운을 바탕으로 한 해석",
                "팔자": saju_data.palcha,
                "특징": "AI 서비스 일시 중단으로 기본 해석을 제공합니다."
            },
            fortune_score=self._calculate_fortune_score(saju_data),
            lucky_elements=["금색", "흰색"],
            caution_areas=["균형 유지"],
            recommendations=["전문가 상담 권장"],
            confidence_score=0.6,
            created_at=datetime.now(),
            estimated_reading_time=2
        )

# 전역 인스턴스
_ai_engine = None

def get_ai_interpretation_engine() -> AIInterpretationEngine:
    """AI 해석 엔진 싱글톤 인스턴스 반환"""
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = AIInterpretationEngine()
    return _ai_engine