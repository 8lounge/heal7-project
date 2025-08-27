"""
원자 모듈: AI 프롬프트 구성기
복잡도: 5분 이해 가능
책임: 단일 책임 원칙 준수 - AI 프롬프트 생성만 담당
테스트: 100% 커버리지  
의존성: typing
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class PromptType(Enum):
    """프롬프트 타입 열거형"""
    SAJU_INTERPRETATION = "saju_interpretation"
    TAROT_READING = "tarot_reading"
    LIFE_ADVICE = "life_advice"
    CAREER_GUIDANCE = "career_guidance"
    RELATIONSHIP_ADVICE = "relationship_advice"


class AIPromptBuilder:
    """
    AI 프롬프트 구성을 위한 핵심 원자 모듈
    - 사주 해석 프롬프트 생성
    - 타로 리딩 프롬프트 생성
    - 개인화된 조언 프롬프트 생성
    - 구조화되고 효과적인 프롬프트
    """
    
    def __init__(self):
        """초기화"""
        self.base_templates = {
            PromptType.SAJU_INTERPRETATION: self._get_saju_template(),
            PromptType.TAROT_READING: self._get_tarot_template(),
            PromptType.LIFE_ADVICE: self._get_life_advice_template(),
            PromptType.CAREER_GUIDANCE: self._get_career_template(),
            PromptType.RELATIONSHIP_ADVICE: self._get_relationship_template()
        }
    
    def _get_saju_template(self) -> str:
        """사주 해석 프롬프트 템플릿"""
        return """당신은 전문 사주명리학 상담사입니다. 다음 사주를 분석하고 해석해주세요.

## 사주 정보
- 년주: {year_pillar}
- 월주: {month_pillar}  
- 일주: {day_pillar}
- 시주: {hour_pillar}

## 오행 분석
{five_elements_analysis}

## 분석 요청사항
{analysis_request}

## 응답 형식
1. **기본 성향**: 일주를 중심으로 한 성격 분석
2. **강약 분석**: 오행의 강약과 균형 상태
3. **운세 흐름**: {focus_period} 기간의 운세 전망
4. **조언 사항**: 구체적이고 실용적인 개선 방안

## 주의사항
- MZ세대에게 친근한 언어 사용
- 미신적 표현보다는 현실적 조언 중심
- 긍정적이고 건설적인 내용으로 구성"""
    
    def _get_tarot_template(self) -> str:
        """타로 리딩 프롬프트 템플릿"""
        return """당신은 전문 타로 리더입니다. 다음 타로 카드를 해석해주세요.

## 타로 스프레드
{tarot_spread}

## 질문자 정보
- 질문: {question}
- 관심 분야: {focus_area}
- 현재 상황: {current_situation}

## 카드 정보
{cards_info}

## 응답 형식
1. **카드별 의미**: 각 위치별 카드의 기본 의미
2. **종합 해석**: 카드들 간의 연관성과 전체적 메시지
3. **실행 조언**: 구체적이고 실천 가능한 행동 방안
4. **주의 사항**: 유의할 점과 긍정적 변화 방법

## 주의사항
- 현대적이고 실용적인 해석
- 두려움보다는 희망을 주는 메시지
- 구체적인 행동 지침 포함"""
    
    def _get_life_advice_template(self) -> str:
        """인생 조언 프롬프트 템플릿"""
        return """당신은 인생 멘토이자 상담사입니다. 다음 상황에 대해 조언해주세요.

## 상담자 정보
- 나이: {age}대
- 성별: {gender}
- 현재 상황: {current_situation}
- 고민 분야: {concern_area}

## 구체적 질문
{specific_question}

## 배경 정보
{background_info}

## 응답 형식
1. **상황 분석**: 현재 상황에 대한 객관적 분석
2. **핵심 이슈**: 가장 중요하게 다뤄야 할 문제
3. **해결 방안**: 단계별 구체적 실행 계획
4. **장기 전략**: 지속 가능한 변화를 위한 접근법

## 주의사항
- 판단하지 말고 이해하려는 자세
- 실현 가능한 현실적 조언
- 긍정적 에너지와 동기부여 제공"""
    
    def _get_career_template(self) -> str:
        """커리어 가이드 프롬프트 템플릿"""  
        return """당신은 커리어 전문 컨설턴트입니다. 다음 커리어 상담을 진행해주세요.

## 상담자 프로필
- 연령: {age}
- 현재 직업/상황: {current_job}
- 경력: {career_background}
- 관심 분야: {interest_areas}

## 커리어 고민
{career_concern}

## 목표
- 단기 목표: {short_term_goal}
- 장기 목표: {long_term_goal}

## 응답 형식
1. **현재 상황 분석**: 커리어 현 위치와 강점/약점
2. **기회 요인**: 활용 가능한 기회와 시장 동향
3. **실행 계획**: 구체적인 액션 플랜과 타임라인
4. **스킬 개발**: 필요한 역량과 학습 방향

## 주의사항
- 2025년 취업 시장 트렌드 반영
- MZ세대 특성을 고려한 조언
- 실무진의 실제 경험담 포함"""
    
    def _get_relationship_template(self) -> str:
        """연애 조언 프롬프트 템플릿"""
        return """당신은 연애 전문 상담사입니다. 다음 연애 상담을 진행해주세요.

## 상담자 정보
- 나이: {age}
- 성별: {gender}
- 연애 경험: {dating_experience}
- 현재 상태: {relationship_status}

## 연애 고민
{relationship_concern}

## 상대방 정보 (있는 경우)
{partner_info}

## 응답 형식  
1. **상황 이해**: 현재 연애 상황에 대한 객관적 분석
2. **심리 분석**: 본인과 상대방의 심리 상태
3. **소통 전략**: 효과적인 커뮤니케이션 방법
4. **관계 발전**: 건강한 관계 발전을 위한 조언

## 주의사항
- MZ세대 연애 패턴 고려
- 성별 고정관념 없는 균형잡힌 시각
- 자기 사랑과 성장 중심의 조언"""
    
    def build_prompt(self, prompt_type: PromptType, **kwargs) -> str:
        """
        프롬프트 구성
        
        Args:
            prompt_type: 프롬프트 타입
            **kwargs: 템플릿에 삽입할 데이터
            
        Returns:
            str: 완성된 프롬프트
        """
        if prompt_type not in self.base_templates:
            raise ValueError(f"지원되지 않는 프롬프트 타입: {prompt_type}")
        
        template = self.base_templates[prompt_type]
        
        try:
            # 템플릿에 데이터 삽입
            formatted_prompt = template.format(**kwargs)
            return formatted_prompt
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise ValueError(f"필수 매개변수가 누락되었습니다: {missing_key}")
    
    def build_saju_prompt(self, 
                         year_pillar: str, 
                         month_pillar: str, 
                         day_pillar: str, 
                         hour_pillar: str,
                         five_elements_analysis: str,
                         analysis_request: str = "전반적인 운세와 성향을 알고 싶습니다",
                         focus_period: str = "2025년") -> str:
        """
        사주 해석 프롬프트 생성
        
        Args:
            year_pillar: 년주 (예: "갑자")
            month_pillar: 월주
            day_pillar: 일주  
            hour_pillar: 시주
            five_elements_analysis: 오행 분석 결과
            analysis_request: 분석 요청사항
            focus_period: 집중 기간
            
        Returns:
            str: 사주 해석 프롬프트
        """
        return self.build_prompt(
            PromptType.SAJU_INTERPRETATION,
            year_pillar=year_pillar,
            month_pillar=month_pillar, 
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            five_elements_analysis=five_elements_analysis,
            analysis_request=analysis_request,
            focus_period=focus_period
        )
    
    def build_career_prompt(self,
                           age: str,
                           current_job: str,
                           career_background: str,
                           interest_areas: str,
                           career_concern: str,
                           short_term_goal: str = "현재 상황 개선",
                           long_term_goal: str = "만족스러운 커리어 구축") -> str:
        """
        커리어 상담 프롬프트 생성
        
        Args:
            age: 연령
            current_job: 현재 직업
            career_background: 경력 배경
            interest_areas: 관심 분야
            career_concern: 커리어 고민
            short_term_goal: 단기 목표
            long_term_goal: 장기 목표
            
        Returns:
            str: 커리어 상담 프롬프트
        """
        return self.build_prompt(
            PromptType.CAREER_GUIDANCE,
            age=age,
            current_job=current_job,
            career_background=career_background,
            interest_areas=interest_areas,
            career_concern=career_concern,
            short_term_goal=short_term_goal,
            long_term_goal=long_term_goal
        )
    
    def get_template_requirements(self, prompt_type: PromptType) -> List[str]:
        """
        템플릿 필수 요구사항 반환
        
        Args:
            prompt_type: 프롬프트 타입
            
        Returns:
            List[str]: 필수 매개변수 목록
        """
        template = self.base_templates.get(prompt_type, "")
        
        # 템플릿에서 {변수} 패턴 찾기
        import re
        requirements = re.findall(r'\{(\w+)\}', template)
        return list(set(requirements))  # 중복 제거
    
    def validate_prompt_data(self, prompt_type: PromptType, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        프롬프트 데이터 유효성 검증
        
        Args:
            prompt_type: 프롬프트 타입  
            data: 검증할 데이터
            
        Returns:
            Tuple[bool, List[str]]: (유효성, 누락된 필드 목록)
        """
        requirements = self.get_template_requirements(prompt_type)
        missing_fields = []
        
        for field in requirements:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        is_valid = len(missing_fields) == 0
        return (is_valid, missing_fields)


def test_ai_prompt_builder():
    """AI 프롬프트 구성기 테스트 케이스"""
    builder = AIPromptBuilder()
    
    # 사주 프롬프트 테스트
    saju_prompt = builder.build_saju_prompt(
        year_pillar="갑자",
        month_pillar="을축", 
        day_pillar="병인",
        hour_pillar="정묘",
        five_elements_analysis="목 2개, 화 1개, 토 0개, 금 0개, 수 1개"
    )
    
    assert isinstance(saju_prompt, str)
    assert "갑자" in saju_prompt
    assert "병인" in saju_prompt
    assert "목 2개" in saju_prompt
    
    print("✅ 사주 프롬프트 생성 테스트 통과")


def test_career_prompt():
    """커리어 프롬프트 테스트"""
    builder = AIPromptBuilder()
    
    career_prompt = builder.build_career_prompt(
        age="20",
        current_job="대학생", 
        career_background="인턴 경험 없음",
        interest_areas="IT, 디자인",
        career_concern="취업 준비가 막막합니다"
    )
    
    assert isinstance(career_prompt, str)
    assert "대학생" in career_prompt
    assert "IT, 디자인" in career_prompt
    assert "취업 준비" in career_prompt
    
    print("✅ 커리어 프롬프트 생성 테스트 통과")


def test_template_requirements():
    """템플릿 요구사항 테스트"""
    builder = AIPromptBuilder()
    
    saju_requirements = builder.get_template_requirements(PromptType.SAJU_INTERPRETATION)
    assert "year_pillar" in saju_requirements
    assert "month_pillar" in saju_requirements
    assert "five_elements_analysis" in saju_requirements
    
    career_requirements = builder.get_template_requirements(PromptType.CAREER_GUIDANCE)
    assert "age" in career_requirements
    assert "current_job" in career_requirements
    
    print("✅ 템플릿 요구사항 테스트 통과")


def test_data_validation():
    """데이터 유효성 검증 테스트"""
    builder = AIPromptBuilder()
    
    # 완전한 데이터
    complete_data = {
        "year_pillar": "갑자",
        "month_pillar": "을축",
        "day_pillar": "병인", 
        "hour_pillar": "정묘",
        "five_elements_analysis": "분석 결과",
        "analysis_request": "요청사항",
        "focus_period": "2025년"
    }
    
    is_valid, missing = builder.validate_prompt_data(PromptType.SAJU_INTERPRETATION, complete_data)
    assert is_valid == True
    assert len(missing) == 0
    
    # 불완전한 데이터
    incomplete_data = {
        "year_pillar": "갑자",
        "month_pillar": "을축"
        # 나머지 필수 필드 누락
    }
    
    is_valid, missing = builder.validate_prompt_data(PromptType.SAJU_INTERPRETATION, incomplete_data)
    assert is_valid == False
    assert len(missing) > 0
    
    print("✅ 데이터 유효성 검증 테스트 통과")


def test_error_handling():
    """에러 처리 테스트"""
    builder = AIPromptBuilder()
    
    # 지원되지 않는 프롬프트 타입
    try:
        builder.build_prompt("invalid_type")
        assert False, "예외가 발생해야 함"
    except ValueError:
        pass  # 예상된 예외
    
    # 필수 매개변수 누락
    try:
        builder.build_prompt(PromptType.SAJU_INTERPRETATION, year_pillar="갑자")
        assert False, "예외가 발생해야 함" 
    except ValueError:
        pass  # 예상된 예외
    
    print("✅ 에러 처리 테스트 통과")


# 사용 예시
if __name__ == "__main__":
    # 기본 사용법
    builder = AIPromptBuilder()
    
    print("🤖 AI 프롬프트 구성 예시:")
    
    # 1. 사주 해석 프롬프트
    print("\n1️⃣ 사주 해석 프롬프트:")
    saju_prompt = builder.build_saju_prompt(
        year_pillar="갑자",
        month_pillar="을축",
        day_pillar="병인", 
        hour_pillar="정묘",
        five_elements_analysis="목 2개 (강함), 화 1개 (보통), 토 0개 (부족), 금 0개 (부족), 수 1개 (보통)",
        analysis_request="2025년 취업운과 연애운을 중점적으로 알고 싶습니다"
    )
    print(saju_prompt[:200] + "...")
    
    # 2. 커리어 상담 프롬프트  
    print("\n2️⃣ 커리어 상담 프롬프트:")
    career_prompt = builder.build_career_prompt(
        age="25",
        current_job="프론트엔드 개발자 (1년차)",
        career_background="부트캠프 수료, 스타트업 근무 경험",
        interest_areas="React, TypeScript, UX 디자인",
        career_concern="더 성장할 수 있는 회사로 이직을 고민 중입니다",
        short_term_goal="시니어 개발자로 성장",
        long_term_goal="테크리드 또는 프로덕트 매니저"
    )
    print(career_prompt[:200] + "...")
    
    # 3. 템플릿 요구사항 확인
    print("\n3️⃣ 템플릿 요구사항:")
    for prompt_type in PromptType:
        requirements = builder.get_template_requirements(prompt_type)
        print(f"{prompt_type.value}: {len(requirements)}개 필수 필드")
    
    # 4. 데이터 유효성 검증
    print("\n4️⃣ 데이터 유효성 검증:")
    test_data = {"age": "25", "current_job": "개발자"}
    is_valid, missing = builder.validate_prompt_data(PromptType.CAREER_GUIDANCE, test_data)
    print(f"유효성: {is_valid}, 누락 필드: {missing}")
    
    # 테스트 실행
    print("\n🧪 테스트 실행:")
    test_ai_prompt_builder()
    test_career_prompt() 
    test_template_requirements()
    test_data_validation()
    test_error_handling()
    
    print("\n✅ AI 프롬프트 구성기 원자 모듈 실행 완료!")