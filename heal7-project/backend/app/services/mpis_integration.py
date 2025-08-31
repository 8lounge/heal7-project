"""
HEAL7 M-PIS 통합 엔진
설문 결과와 M-PIS 프레임워크 연동 분석
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import redis
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger("heal7.mpis.integration")

class MPISIntegrationEngine:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "database": "heal7", 
            "user": "postgres",
            "options": "-c search_path=shared_common,public"
        }
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        self.mpis_config = {
            "positive_multiplier": 3.5,
            "negative_multiplier": 4.0, 
            "balance_threshold": 0.3,
            "potential_weight": 1.2
        }
        
    def get_db_connection(self):
        """데이터베이스 연결"""
        return psycopg2.connect(**self.db_config)
    
    async def update_session_profile(self, session_uuid: str):
        """세션의 M-PIS 프로필 업데이트 (백그라운드 작업)"""
        
        try:
            # 현재 키워드 점수 기반으로 M-PIS 프로필 계산
            mpis_profile = await self.calculate_mpis_profile(session_uuid)
            
            # Redis에 캐시
            self.redis_client.setex(
                f"heal7:survey:session:{session_uuid}:mpis",
                3600,  # 1시간 TTL
                json.dumps(mpis_profile)
            )
            
            logger.info(f"세션 {session_uuid} M-PIS 프로필 업데이트 완료")
            
        except Exception as e:
            logger.error(f"M-PIS 프로필 업데이트 실패: {e}")
    
    async def calculate_mpis_profile(self, session_uuid: str) -> dict:
        """현재 키워드 점수 기반 M-PIS 프로필 계산"""
        
        try:
            # 1. 세션의 현재 키워드 점수 로드 (Redis에서)
            keyword_scores = await self.load_session_keyword_scores(session_uuid)
            
            # 2. A/B/C 그룹별 점수 집계
            group_scores = self.aggregate_by_groups(keyword_scores)
            
            # 3. 동적 균형 모델 적용
            balance_analysis = self.apply_dynamic_balance_model(group_scores)
            
            # 4. 에너지 상태 분석
            energy_state = self.analyze_energy_state(balance_analysis)
            
            # 5. 성장 잠재력 분석
            growth_potential = self.analyze_growth_potential(keyword_scores, balance_analysis)
            
            mpis_profile = {
                "group_scores": group_scores,
                "balance_analysis": balance_analysis,
                "energy_state": energy_state,
                "growth_potential": growth_potential,
                "profile_confidence": self.calculate_profile_confidence(keyword_scores),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return mpis_profile
            
        except Exception as e:
            logger.error(f"M-PIS 프로필 계산 실패: {e}")
            return {}
    
    async def load_session_keyword_scores(self, session_uuid: str) -> dict:
        """세션의 키워드 점수 로드"""
        
        try:
            scores_data = self.redis_client.hgetall(
                f"heal7:survey:session:{session_uuid}:keywords"
            )
            
            scores = {}
            for key, value in scores_data.items():
                if key.startswith('keyword_') and not key.endswith('_count'):
                    scores[key] = json.loads(value)
            
            return scores
            
        except Exception as e:
            logger.error(f"세션 키워드 점수 로드 실패: {e}")
            return {}
    
    def aggregate_by_groups(self, keyword_scores: dict) -> dict:
        """키워드 점수를 A/B/C 그룹별로 집계"""
        
        group_aggregation = {
            "A": {"positive": 0.0, "negative": 0.0, "count": 0},  # 심리학적
            "B": {"positive": 0.0, "negative": 0.0, "count": 0},  # 신경과학적  
            "C": {"positive": 0.0, "negative": 0.0, "count": 0}   # 개선영역
        }
        
        # 임시 구현 - 실제로는 keywords 테이블과 연동하여 그룹 분류
        for keyword_id, score_data in keyword_scores.items():
            if isinstance(score_data, dict) and 'score' in score_data:
                # 임시로 키워드 ID 기반 그룹 분류
                keyword_num = int(keyword_id.replace('keyword_', ''))
                if keyword_num <= 200:
                    group = "A"
                elif keyword_num <= 350:
                    group = "B"
                else:
                    group = "C"
                
                score = score_data['score']
                confidence = score_data.get('confidence', 1.0)
                
                # 신뢰도 가중치 적용
                weighted_score = score * confidence
                
                if weighted_score > 0:
                    group_aggregation[group]["positive"] += weighted_score
                else:
                    group_aggregation[group]["negative"] += abs(weighted_score)
                
                group_aggregation[group]["count"] += 1
        
        # 그룹별 평균 점수 계산
        for group in group_aggregation:
            if group_aggregation[group]["count"] > 0:
                count = group_aggregation[group]["count"]
                group_aggregation[group]["avg_positive"] = group_aggregation[group]["positive"] / count
                group_aggregation[group]["avg_negative"] = group_aggregation[group]["negative"] / count
                group_aggregation[group]["net_score"] = group_aggregation[group]["avg_positive"] - group_aggregation[group]["avg_negative"]
        
        return group_aggregation
    
    def apply_dynamic_balance_model(self, group_scores: dict) -> dict:
        """P = N × (3~4) + Potential Analysis 공식 적용"""
        
        balance_analysis = {}
        
        for group, scores in group_scores.items():
            positive = scores.get("avg_positive", 0.0)
            negative = scores.get("avg_negative", 0.0)
            
            # 동적 균형 공식 적용
            if negative > 0:
                # 부정 상태: P = N × 4.0 + 잠재력 분석
                transformation_potential = negative * self.mpis_config["negative_multiplier"]
                balance_state = "transformative"
            else:
                # 긍정 상태: P = N × 3.5 + 안정성 분석  
                stability_factor = positive * self.mpis_config["positive_multiplier"]
                transformation_potential = stability_factor
                balance_state = "stable"
            
            # 균형점 계산
            balance_point = positive / (positive + negative) if (positive + negative) > 0 else 0.5
            
            balance_analysis[f"group_{group}"] = {
                "positive_energy": positive,
                "negative_energy": negative,
                "transformation_potential": transformation_potential,
                "balance_point": balance_point,
                "balance_state": balance_state,
                "group_weight": self.get_group_weight(group)
            }
        
        # 전체 균형 점수 계산
        overall_balance = self.calculate_overall_balance(balance_analysis)
        balance_analysis["overall"] = overall_balance
        
        return balance_analysis
    
    def get_group_weight(self, group: str) -> float:
        """그룹별 가중치 반환"""
        
        weights = {
            "A": 1.0,  # 심리학적
            "B": 1.2,  # 신경과학적 (조금 더 높은 가중치)
            "C": 0.8   # 개선영역 (부정적 요소이므로 낮은 가중치)
        }
        
        return weights.get(group, 1.0)
    
    def calculate_overall_balance(self, balance_analysis: dict) -> dict:
        """전체 균형 점수 계산"""
        
        total_positive = 0.0
        total_negative = 0.0
        total_potential = 0.0
        
        for key, data in balance_analysis.items():
            if key.startswith("group_"):
                weight = data.get("group_weight", 1.0)
                total_positive += data.get("positive_energy", 0.0) * weight
                total_negative += data.get("negative_energy", 0.0) * weight
                total_potential += data.get("transformation_potential", 0.0) * weight
        
        overall_balance_point = total_positive / (total_positive + total_negative) if (total_positive + total_negative) > 0 else 0.5
        
        return {
            "total_positive_energy": total_positive,
            "total_negative_energy": total_negative,
            "total_transformation_potential": total_potential,
            "overall_balance_point": overall_balance_point,
            "balance_state": "stable" if overall_balance_point > 0.6 else "transformative" if overall_balance_point < 0.4 else "balanced",
            "confidence": min(1.0, (total_positive + total_negative) / 10.0)  # 데이터량 기반 신뢰도
        }
    
    def analyze_energy_state(self, balance_analysis: dict) -> dict:
        """에너지 상태 분석"""
        
        overall = balance_analysis.get("overall", {})
        balance_point = overall.get("overall_balance_point", 0.5)
        
        if balance_point > 0.7:
            energy_state = "high_positive"
            description = "강한 긍정 에너지 상태"
        elif balance_point > 0.5:
            energy_state = "positive"
            description = "긍정 에너지 우세"
        elif balance_point > 0.3:
            energy_state = "balanced"
            description = "균형잡힌 에너지 상태"
        else:
            energy_state = "transformative"
            description = "변화 잠재력이 큰 상태"
        
        return {
            "state": energy_state,
            "description": description,
            "balance_score": balance_point,
            "stability": 1.0 - abs(balance_point - 0.5) * 2  # 0.5에서 멀수록 불안정
        }
    
    def analyze_growth_potential(self, keyword_scores: dict, balance_analysis: dict) -> dict:
        """성장 잠재력 분석"""
        
        overall = balance_analysis.get("overall", {})
        transformation_potential = overall.get("total_transformation_potential", 0.0)
        
        # 성장 영역 식별
        growth_areas = []
        for group in ["A", "B", "C"]:
            group_data = balance_analysis.get(f"group_{group}", {})
            negative_energy = group_data.get("negative_energy", 0.0)
            
            if negative_energy > 0.3:  # 임계값 이상의 부정 에너지
                growth_areas.append({
                    "group": group,
                    "potential": negative_energy * 4.0,  # P = N × 4 공식
                    "priority": "high" if negative_energy > 0.6 else "medium"
                })
        
        return {
            "total_potential": transformation_potential,
            "growth_areas": growth_areas,
            "readiness_score": min(1.0, transformation_potential / 5.0),
            "recommendation": "focus_on_growth" if transformation_potential > 2.0 else "maintain_balance"
        }
    
    def calculate_profile_confidence(self, keyword_scores: dict) -> float:
        """프로필 신뢰도 계산"""
        
        if not keyword_scores:
            return 0.0
        
        total_confidence = 0.0
        count = 0
        
        for score_data in keyword_scores.values():
            if isinstance(score_data, dict) and 'confidence' in score_data:
                total_confidence += score_data['confidence']
                count += 1
        
        if count == 0:
            return 0.0
        
        avg_confidence = total_confidence / count
        
        # 데이터량에 따른 신뢰도 조정
        data_factor = min(1.0, count / 20.0)  # 20개 데이터에서 최대 신뢰도
        
        return avg_confidence * data_factor
    
    async def get_session_profile(self, session_uuid: str) -> dict:
        """세션의 현재 M-PIS 프로필 조회"""
        
        try:
            cached_profile = self.redis_client.get(
                f"heal7:survey:session:{session_uuid}:mpis"
            )
            
            if cached_profile:
                return json.loads(cached_profile)
            else:
                # 캐시가 없으면 새로 계산
                return await self.calculate_mpis_profile(session_uuid)
                
        except Exception as e:
            logger.error(f"M-PIS 프로필 조회 실패: {e}")
            return {}
    
    async def finalize_session_profile(self, session_uuid: str) -> dict:
        """세션 완료 시 최종 M-PIS 프로필 생성"""
        
        try:
            # 최종 프로필 계산
            final_profile = await self.calculate_mpis_profile(session_uuid)
            
            # 추가 분석 수행
            final_profile["completion_analysis"] = {
                "total_responses": await self.count_session_responses(session_uuid),
                "analysis_completeness": self.calculate_completeness(final_profile),
                "finalized_at": datetime.now().isoformat()
            }
            
            return final_profile
            
        except Exception as e:
            logger.error(f"최종 M-PIS 프로필 생성 실패: {e}")
            return {}
    
    async def count_session_responses(self, session_uuid: str) -> int:
        """세션의 총 응답 수 계산"""
        
        # 임시 구현
        return 0
    
    def calculate_completeness(self, profile: dict) -> float:
        """분석 완성도 계산"""
        
        # 프로필의 각 섹션이 얼마나 완성되었는지 계산
        sections = ["group_scores", "balance_analysis", "energy_state", "growth_potential"]
        completed_sections = sum(1 for section in sections if section in profile and profile[section])
        
        return completed_sections / len(sections)