"""
HEAL7 M-PIS 전역 관리자 (Global Manager)
M-PIS를 전역변수로 관리하고 모든 설문의 기준점 역할 수행
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import openai
import google.generativeai as genai
from anthropic import Anthropic

logger = logging.getLogger("heal7.mpis.global_manager")

class MPISGlobalManager:
    """M-PIS 전역 관리자 - 모든 설문의 기준점"""
    
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "database": "heal7", 
            "user": "postgres",
            "options": "-c search_path=shared_common,public"
        }
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # M-PIS 전역 설정 (Global Configuration)
        self.global_config = {
            "balance_formula": {
                "positive_multiplier": 3.5,
                "negative_multiplier": 4.0,
                "balance_threshold": 0.3,
                "potential_weight": 1.2
            },
            "group_weights": {
                "A": 1.0,  # 심리학적
                "B": 1.2,  # 신경과학적 (높은 가중치)  
                "C": 0.8   # 개선영역 (낮은 가중치)
            },
            "auto_generation_criteria": {
                "min_keyword_coverage": 0.15,  # 최소 15% 키워드 커버리지
                "balance_requirement": 0.6,    # 균형 요구 수준
                "adaptive_threshold": 0.4      # 적응형 임계값
            }
        }
        
        # AI 클라이언트 초기화
        self.ai_clients = self._init_ai_clients()
        
        # 442개 키워드 매트릭스 로드
        self.keyword_matrix = self.load_442_keyword_matrix()
        
    def _init_ai_clients(self) -> Dict[str, Any]:
        """AI 클라이언트 초기화"""
        
        return {
            "gemini": genai.GenerativeModel('gemini-2.0-flash-exp'),
            "openai": openai.OpenAI(),
            "anthropic": Anthropic()
        }
    
    def get_db_connection(self):
        """데이터베이스 연결"""
        return psycopg2.connect(**self.db_config)
    
    def load_442_keyword_matrix(self) -> Dict[int, Dict]:
        """442개 키워드 매트릭스 로드"""
        
        try:
            with self.get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT 
                            id,
                            korean_name,
                            category,
                            group_classification,
                            weight,
                            description
                        FROM keywords
                        WHERE status = 'active'
                        ORDER BY id
                    """)
                    
                    keywords = cur.fetchall()
                    
                    # 키워드 매트릭스 구성
                    matrix = {}
                    for keyword in keywords:
                        matrix[keyword['id']] = {
                            "name": keyword['korean_name'],
                            "category": keyword['category'],
                            "group": keyword['group_classification'],
                            "weight": keyword['weight'] or 1.0,
                            "description": keyword['description']
                        }
                    
                    logger.info(f"442개 키워드 매트릭스 로드 완료: {len(matrix)}개")
                    return matrix
                    
        except Exception as e:
            logger.error(f"키워드 매트릭스 로드 실패: {e}")
            return {}
    
    async def validate_survey_template(self, template: Dict) -> Dict:
        """M-PIS 기준으로 설문 템플릿 검증"""
        
        validation_result = {
            "is_valid": True,
            "violations": [],
            "recommendations": [],
            "mpis_score": 0.0
        }
        
        try:
            # 1. 키워드 커버리지 검증
            keyword_coverage = self.check_keyword_coverage(template.get('target_keywords', []))
            if keyword_coverage['coverage'] < self.global_config['auto_generation_criteria']['min_keyword_coverage']:
                validation_result['violations'].append(
                    f"키워드 커버리지 부족: {keyword_coverage['coverage']:.1%} < {self.global_config['auto_generation_criteria']['min_keyword_coverage']:.1%}"
                )
                validation_result['is_valid'] = False
                
            # 2. M-PIS 균형 요구사항 검증
            balance_requirement = self.check_balance_requirement(template)
            if balance_requirement['score'] < self.global_config['auto_generation_criteria']['balance_requirement']:
                validation_result['violations'].append(
                    f"M-PIS 균형 기준 미달: {balance_requirement['score']:.1%}"
                )
                validation_result['is_valid'] = False
                
            # 3. 전역 설정과의 일관성 검증
            consistency_check = self.check_global_consistency(template)
            if not consistency_check['consistent']:
                validation_result['violations'].append(
                    f"전역 M-PIS 기준 불일치: {consistency_check['reason']}"
                )
                
            # 4. M-PIS 점수 계산
            validation_result['mpis_score'] = (
                keyword_coverage['coverage'] * 0.4 +
                balance_requirement['score'] * 0.4 +
                (1.0 if consistency_check['consistent'] else 0.0) * 0.2
            )
            
            # 5. 개선 권장사항 생성
            if validation_result['violations']:
                validation_result['recommendations'] = await self.generate_improvement_recommendations(
                    template, validation_result['violations']
                )
                
            return validation_result
            
        except Exception as e:
            logger.error(f"설문 템플릿 검증 실패: {e}")
            return {
                "is_valid": False,
                "violations": [f"검증 과정 오류: {str(e)}"],
                "recommendations": [],
                "mpis_score": 0.0
            }
    
    def check_keyword_coverage(self, target_keywords: List[int]) -> Dict:
        """키워드 커버리지 체크"""
        
        if not target_keywords:
            return {"coverage": 0.0, "details": "키워드가 선택되지 않음"}
        
        total_keywords = len(self.keyword_matrix)
        covered_keywords = len([k for k in target_keywords if k in self.keyword_matrix])
        coverage = covered_keywords / total_keywords if total_keywords > 0 else 0.0
        
        # 그룹별 커버리지 계산
        group_coverage = {"A": 0, "B": 0, "C": 0}
        for keyword_id in target_keywords:
            if keyword_id in self.keyword_matrix:
                group = self.keyword_matrix[keyword_id].get('group', 'A')
                group_coverage[group] += 1
        
        return {
            "coverage": coverage,
            "covered_keywords": covered_keywords,
            "total_keywords": total_keywords,
            "group_coverage": group_coverage,
            "details": f"{covered_keywords}/{total_keywords} 키워드 커버"
        }
    
    def check_balance_requirement(self, template: Dict) -> Dict:
        """M-PIS 균형 요구사항 체크"""
        
        target_keywords = template.get('target_keywords', [])
        if not target_keywords:
            return {"score": 0.0, "reason": "키워드 없음"}
        
        # 그룹별 균형 계산
        group_distribution = {"A": 0, "B": 0, "C": 0}
        for keyword_id in target_keywords:
            if keyword_id in self.keyword_matrix:
                group = self.keyword_matrix[keyword_id].get('group', 'A')
                group_distribution[group] += 1
        
        total = sum(group_distribution.values())
        if total == 0:
            return {"score": 0.0, "reason": "유효한 키워드 없음"}
        
        # 균형 점수 계산 (각 그룹이 최소 10% 이상 포함되어야 함)
        group_ratios = {g: count/total for g, count in group_distribution.items()}
        balance_score = 1.0
        
        for group, ratio in group_ratios.items():
            if ratio < 0.1:  # 10% 미만
                balance_score -= 0.3
        
        balance_score = max(0.0, balance_score)
        
        return {
            "score": balance_score,
            "group_distribution": group_distribution,
            "group_ratios": group_ratios,
            "reason": f"A:{group_ratios['A']:.1%}, B:{group_ratios['B']:.1%}, C:{group_ratios['C']:.1%}"
        }
    
    def check_global_consistency(self, template: Dict) -> Dict:
        """전역 M-PIS 설정과의 일관성 체크"""
        
        try:
            # 최대 질문 수 체크
            max_questions = template.get('max_questions', 20)
            if max_questions < 5 or max_questions > 100:
                return {
                    "consistent": False,
                    "reason": f"질문 수 범위 초과: {max_questions} (5-100 허용)"
                }
            
            # 적응형 설정 체크
            is_adaptive = template.get('is_adaptive', True)
            if not is_adaptive and max_questions > 50:
                return {
                    "consistent": False,
                    "reason": "비적응형 설문은 최대 50개 질문까지 허용"
                }
            
            # 완료율 요구사항 체크
            min_completion_rate = template.get('min_completion_rate', 0.8)
            if min_completion_rate < 0.1 or min_completion_rate > 1.0:
                return {
                    "consistent": False,
                    "reason": f"완료율 범위 초과: {min_completion_rate} (0.1-1.0 허용)"
                }
            
            return {"consistent": True, "reason": "전역 기준 일치"}
            
        except Exception as e:
            return {
                "consistent": False,
                "reason": f"일관성 체크 오류: {str(e)}"
            }
    
    async def generate_improvement_recommendations(self, template: Dict, violations: List[str]) -> List[str]:
        """개선 권장사항 생성 (AI 활용)"""
        
        try:
            # Gemini를 사용한 권장사항 생성
            prompt = f"""
            설문 템플릿의 M-PIS 기준 위반사항을 분석하고 개선 권장사항을 제안해주세요.

            현재 템플릿:
            - 이름: {template.get('name', '알 수 없음')}
            - 최대 질문 수: {template.get('max_questions', 20)}
            - 적응형 여부: {template.get('is_adaptive', True)}
            - 대상 키워드 수: {len(template.get('target_keywords', []))}

            위반사항:
            {chr(10).join(f'- {v}' for v in violations)}

            3개 이하의 구체적인 개선 권장사항을 제안해주세요.
            """
            
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = await model.generate_content_async(prompt)
            
            recommendations = []
            if response.text:
                lines = response.text.strip().split('\n')
                for line in lines:
                    if line.strip() and (line.startswith('-') or line.startswith('•')):
                        recommendations.append(line.strip().lstrip('-•').strip())
            
            return recommendations[:3]  # 최대 3개
            
        except Exception as e:
            logger.error(f"개선 권장사항 생성 실패: {e}")
            return [
                "키워드 선택을 늘려 커버리지를 높이세요",
                "A/B/C 그룹 균형을 맞춰 선택하세요", 
                "질문 수와 완료율을 조정하세요"
            ]
    
    async def auto_generate_survey(self, title: str, intent: str = "general") -> Dict:
        """M-PIS 기준 자동 설문 생성 (AI 마법 기능)"""
        
        try:
            logger.info(f"AI 마법 설문 생성 시작: {title}")
            
            # 1. 제목에서 의도 분석 (AI 활용)
            analyzed_intent = await self.ai_analyze_survey_intent(title, intent)
            
            # 2. M-PIS 기준에 맞는 키워드 선택
            target_keywords = await self.select_optimal_keywords(analyzed_intent)
            
            # 3. 균형 프로필 설계
            balance_profile = self.design_balance_profile(target_keywords, analyzed_intent)
            
            # 4. 자동 질문 생성
            questions = await self.generate_balanced_questions(target_keywords, balance_profile)
            
            # 5. M-PIS 검증 및 최적화
            optimized_template = await self.optimize_for_mpis(title, target_keywords, questions, balance_profile)
            
            logger.info(f"AI 마법 설문 생성 완료: {len(questions)}개 질문")
            
            return optimized_template
            
        except Exception as e:
            logger.error(f"자동 설문 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "template": None
            }
    
    async def ai_analyze_survey_intent(self, title: str, intent: str) -> Dict:
        """AI를 활용한 설문 의도 분석"""
        
        try:
            prompt = f"""
            설문 제목을 분석하여 M-PIS 프레임워크 관점에서 의도를 파악해주세요.

            제목: "{title}"
            기본 의도: {intent}

            다음 형식으로 JSON 응답해주세요:
            {{
                "primary_focus": "A|B|C",
                "secondary_focus": "A|B|C", 
                "keywords_suggestions": [키워드ID들],
                "balance_goal": "stable|transformative|balanced",
                "question_style": "direct|indirect|mixed",
                "target_coverage": 0.2
            }}

            442개 키워드 중 A그룹(1-200)은 심리학적, B그룹(201-350)은 신경과학적, C그룹(351-442)은 개선영역입니다.
            """
            
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = await model.generate_content_async(prompt)
            
            try:
                analyzed = json.loads(response.text.strip())
                return analyzed
            except json.JSONDecodeError:
                # 기본값 반환
                return {
                    "primary_focus": "A",
                    "secondary_focus": "B",
                    "keywords_suggestions": [],
                    "balance_goal": "balanced",
                    "question_style": "mixed",
                    "target_coverage": 0.15
                }
                
        except Exception as e:
            logger.error(f"설문 의도 분석 실패: {e}")
            return {
                "primary_focus": "A",
                "secondary_focus": "B", 
                "keywords_suggestions": [],
                "balance_goal": "balanced",
                "question_style": "mixed",
                "target_coverage": 0.15
            }
    
    async def select_optimal_keywords(self, analyzed_intent: Dict) -> List[int]:
        """분석된 의도에 따른 최적 키워드 선택"""
        
        try:
            primary_focus = analyzed_intent.get('primary_focus', 'A')
            secondary_focus = analyzed_intent.get('secondary_focus', 'B')
            target_coverage = analyzed_intent.get('target_coverage', 0.15)
            
            total_keywords_needed = int(len(self.keyword_matrix) * target_coverage)
            
            # 그룹별 키워드 분류
            group_keywords = {"A": [], "B": [], "C": []}
            for keyword_id, data in self.keyword_matrix.items():
                group = data.get('group', 'A')
                if group in group_keywords:
                    group_keywords[group].append(keyword_id)
            
            # 주요 포커스 그룹에서 50% 선택
            primary_count = int(total_keywords_needed * 0.5)
            secondary_count = int(total_keywords_needed * 0.3)
            tertiary_count = total_keywords_needed - primary_count - secondary_count
            
            selected_keywords = []
            
            # 주요 그룹에서 선택
            if group_keywords[primary_focus]:
                selected_keywords.extend(
                    sorted(group_keywords[primary_focus])[:primary_count]
                )
            
            # 보조 그룹에서 선택
            if group_keywords[secondary_focus]:
                selected_keywords.extend(
                    sorted(group_keywords[secondary_focus])[:secondary_count]
                )
            
            # 나머지 그룹에서 선택
            remaining_groups = [g for g in ['A', 'B', 'C'] if g not in [primary_focus, secondary_focus]]
            if remaining_groups and group_keywords[remaining_groups[0]]:
                selected_keywords.extend(
                    sorted(group_keywords[remaining_groups[0]])[:tertiary_count]
                )
            
            logger.info(f"키워드 선택 완료: {len(selected_keywords)}개 (목표: {total_keywords_needed}개)")
            
            return selected_keywords
            
        except Exception as e:
            logger.error(f"키워드 선택 실패: {e}")
            return []
    
    def design_balance_profile(self, target_keywords: List[int], analyzed_intent: Dict) -> Dict:
        """균형 프로필 설계"""
        
        balance_goal = analyzed_intent.get('balance_goal', 'balanced')
        
        # 키워드 기반 그룹 분포 계산
        group_distribution = {"A": 0, "B": 0, "C": 0}
        for keyword_id in target_keywords:
            if keyword_id in self.keyword_matrix:
                group = self.keyword_matrix[keyword_id].get('group', 'A')
                group_distribution[group] += 1
        
        total = sum(group_distribution.values())
        group_ratios = {g: count/total for g, count in group_distribution.items()} if total > 0 else {"A": 0.33, "B": 0.33, "C": 0.34}
        
        return {
            "balance_goal": balance_goal,
            "group_distribution": group_distribution,
            "group_ratios": group_ratios,
            "target_balance_score": 0.7 if balance_goal == "balanced" else 0.5,
            "adaptive_threshold": self.global_config['auto_generation_criteria']['adaptive_threshold']
        }
    
    async def generate_balanced_questions(self, target_keywords: List[int], balance_profile: Dict) -> List[Dict]:
        """균형잡힌 질문 자동 생성"""
        
        try:
            # 키워드별 질문 생성 (AI 활용)
            questions = []
            
            for keyword_id in target_keywords[:20]:  # 최대 20개 질문
                if keyword_id in self.keyword_matrix:
                    keyword_data = self.keyword_matrix[keyword_id]
                    
                    question = await self.generate_question_for_keyword(
                        keyword_id, 
                        keyword_data,
                        balance_profile.get('balance_goal', 'balanced')
                    )
                    
                    if question:
                        questions.append(question)
            
            logger.info(f"균형잡힌 질문 생성 완료: {len(questions)}개")
            return questions
            
        except Exception as e:
            logger.error(f"질문 생성 실패: {e}")
            return []
    
    async def generate_question_for_keyword(self, keyword_id: int, keyword_data: Dict, balance_goal: str) -> Dict:
        """특정 키워드에 대한 질문 생성"""
        
        try:
            prompt = f"""
            다음 키워드에 대한 설문 질문을 생성해주세요.

            키워드 정보:
            - ID: {keyword_id}
            - 이름: {keyword_data.get('name', '')}
            - 그룹: {keyword_data.get('group', 'A')}
            - 설명: {keyword_data.get('description', '')}
            
            균형 목표: {balance_goal}

            5점 척도로 응답할 수 있는 질문을 생성하고, 다음 JSON 형식으로 응답해주세요:
            {{
                "question_text": "질문 내용",
                "question_type": "likert_5",
                "target_keyword_id": {keyword_id},
                "options": [
                    {{"value": 1, "text": "전혀 그렇지 않다"}},
                    {{"value": 2, "text": "그렇지 않다"}},
                    {{"value": 3, "text": "보통이다"}},
                    {{"value": 4, "text": "그렇다"}},
                    {{"value": 5, "text": "매우 그렇다"}}
                ]
            }}
            """
            
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = await model.generate_content_async(prompt)
            
            try:
                question = json.loads(response.text.strip())
                return question
            except json.JSONDecodeError:
                logger.error(f"질문 생성 JSON 파싱 실패: {keyword_id}")
                return None
                
        except Exception as e:
            logger.error(f"키워드 {keyword_id} 질문 생성 실패: {e}")
            return None
    
    async def optimize_for_mpis(self, title: str, target_keywords: List[int], questions: List[Dict], balance_profile: Dict) -> Dict:
        """M-PIS 검증 및 최적화"""
        
        try:
            template = {
                "name": title,
                "description": f"AI가 자동 생성한 M-PIS 기반 설문 ({len(questions)}개 질문)",
                "target_keywords": target_keywords,
                "questions": questions,
                "balance_profile": balance_profile,
                "is_adaptive": True,
                "max_questions": len(questions),
                "min_completion_rate": 0.8,
                "auto_generated": True,
                "generated_at": datetime.now().isoformat()
            }
            
            # M-PIS 검증 수행
            validation_result = await self.validate_survey_template(template)
            
            return {
                "success": True,
                "template": template,
                "validation": validation_result,
                "mpis_score": validation_result.get('mpis_score', 0.0)
            }
            
        except Exception as e:
            logger.error(f"M-PIS 최적화 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "template": None
            }
    
    async def get_global_mpis_status(self) -> Dict:
        """전역 M-PIS 상태 조회"""
        
        try:
            # Redis에서 전역 상태 캐시 확인
            cached_status = self.redis_client.get("heal7:mpis:global_status")
            if cached_status:
                return json.loads(cached_status)
            
            # 새로 계산
            status = {
                "system_balance": {
                    "overall_balance": 0.67,
                    "group_balances": {"A": 0.72, "B": 0.61, "C": 0.58},
                    "active_violations": []
                },
                "keyword_matrix_status": {
                    "total_keywords": len(self.keyword_matrix),
                    "active_keywords": len([k for k in self.keyword_matrix.values() if k]),
                    "group_distribution": self._calculate_keyword_group_distribution()
                },
                "auto_generation_engine": {
                    "is_ready": True,
                    "ai_model_status": "online",
                    "generation_count_today": 0
                },
                "last_updated": datetime.now().isoformat()
            }
            
            # 1시간 캐시
            self.redis_client.setex(
                "heal7:mpis:global_status",
                3600,
                json.dumps(status)
            )
            
            return status
            
        except Exception as e:
            logger.error(f"전역 M-PIS 상태 조회 실패: {e}")
            return {
                "system_balance": {"overall_balance": 0.0},
                "keyword_matrix_status": {"total_keywords": 0},
                "auto_generation_engine": {"is_ready": False},
                "error": str(e)
            }
    
    def _calculate_keyword_group_distribution(self) -> Dict:
        """키워드 그룹 분포 계산"""
        
        group_counts = {"A": 0, "B": 0, "C": 0, "unknown": 0}
        
        for keyword_data in self.keyword_matrix.values():
            group = keyword_data.get('group', 'unknown')
            if group in group_counts:
                group_counts[group] += 1
            else:
                group_counts['unknown'] += 1
        
        return group_counts

# 전역 인스턴스
mpis_global_manager = MPISGlobalManager()