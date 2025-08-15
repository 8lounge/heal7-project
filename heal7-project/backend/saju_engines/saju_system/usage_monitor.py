#!/usr/bin/env python3
"""
KASI API 사용량 모니터링 시스템
실시간 사용량 추적 및 예측 시스템
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import sqlite3

logger = logging.getLogger(__name__)

class UsageMonitor:
    """KASI API 사용량 모니터링 및 예측 시스템"""
    
    def __init__(self, db_path: str = "/tmp/kasi_usage.db"):
        self.db_path = db_path
        self.monthly_limit = 10000
        self.safety_margin = 500  # 안전 여유분
        self.effective_limit = self.monthly_limit - self.safety_margin
        
        self._init_database()
    
    def _init_database(self):
        """사용량 추적 데이터베이스 초기화"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS usage_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        date TEXT NOT NULL,
                        hour INTEGER NOT NULL,
                        endpoint TEXT NOT NULL,
                        success BOOLEAN NOT NULL,
                        response_time REAL,
                        user_info TEXT
                    )
                ''')
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS daily_stats (
                        date TEXT PRIMARY KEY,
                        total_requests INTEGER DEFAULT 0,
                        success_requests INTEGER DEFAULT 0,
                        failed_requests INTEGER DEFAULT 0,
                        avg_response_time REAL DEFAULT 0,
                        peak_hour INTEGER DEFAULT 0,
                        last_updated TEXT NOT NULL
                    )
                ''')
                conn.commit()
                logger.info("📊 사용량 모니터링 DB 초기화 완료")
        except Exception as e:
            logger.error(f"❌ DB 초기화 오류: {e}")
    
    def log_usage(self, endpoint: str = "calculate_saju", success: bool = True, 
                  response_time: float = 0, user_info: str = ""):
        """API 사용량 로깅"""
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 개별 로그 저장
                conn.execute('''
                    INSERT INTO usage_log 
                    (timestamp, date, hour, endpoint, success, response_time, user_info)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    now.isoformat(), date_str, now.hour, 
                    endpoint, success, response_time, user_info
                ))
                
                # 일별 통계 업데이트
                conn.execute('''
                    INSERT OR REPLACE INTO daily_stats 
                    (date, total_requests, success_requests, failed_requests, last_updated)
                    VALUES (
                        ?, 
                        COALESCE((SELECT total_requests FROM daily_stats WHERE date = ?), 0) + 1,
                        COALESCE((SELECT success_requests FROM daily_stats WHERE date = ?), 0) + ?,
                        COALESCE((SELECT failed_requests FROM daily_stats WHERE date = ?), 0) + ?,
                        ?
                    )
                ''', (date_str, date_str, date_str, 1 if success else 0, 
                      date_str, 0 if success else 1, now.isoformat()))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"❌ 사용량 로깅 오류: {e}")
    
    def get_current_usage(self) -> Dict[str, Any]:
        """현재 사용량 현황 조회"""
        
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        month_start = now.replace(day=1).strftime("%Y-%m-%d")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 오늘 사용량
                cursor = conn.execute('''
                    SELECT total_requests, success_requests, failed_requests 
                    FROM daily_stats WHERE date = ?
                ''', (today,))
                today_stats = cursor.fetchone()
                today_usage = today_stats[0] if today_stats else 0
                
                # 월간 사용량
                cursor = conn.execute('''
                    SELECT SUM(total_requests), SUM(success_requests), SUM(failed_requests)
                    FROM daily_stats WHERE date >= ?
                ''', (month_start,))
                month_stats = cursor.fetchone()
                month_usage = month_stats[0] if month_stats and month_stats[0] else 0
                
                # 시간대별 패턴 (오늘)
                cursor = conn.execute('''
                    SELECT hour, COUNT(*) as count
                    FROM usage_log 
                    WHERE date = ?
                    GROUP BY hour
                    ORDER BY count DESC
                    LIMIT 3
                ''', (today,))
                peak_hours = cursor.fetchall()
                
                return {
                    "today": {
                        "usage": today_usage,
                        "success_rate": (today_stats[1] / today_stats[0] * 100) if today_stats and today_stats[0] > 0 else 0
                    },
                    "monthly": {
                        "usage": month_usage,
                        "limit": self.monthly_limit,
                        "remaining": self.monthly_limit - month_usage,
                        "usage_percentage": (month_usage / self.monthly_limit) * 100,
                        "safety_remaining": self.effective_limit - month_usage
                    },
                    "peak_hours": [{"hour": h, "count": c} for h, c in peak_hours],
                    "last_updated": now.isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ 사용량 조회 오류: {e}")
            return {"error": str(e)}
    
    def predict_monthly_usage(self) -> Dict[str, Any]:
        """월말 사용량 예측"""
        
        now = datetime.now()
        days_passed = now.day
        days_in_month = (now.replace(month=now.month+1, day=1) - timedelta(days=1)).day
        
        current = self.get_current_usage()
        monthly_usage = current.get("monthly", {}).get("usage", 0)
        
        if days_passed == 0:
            return {"prediction": "insufficient_data"}
        
        # 선형 예측
        daily_average = monthly_usage / days_passed
        linear_prediction = daily_average * days_in_month
        
        # 주말 효과 고려 (주말에 사용량 감소 가정)
        weekdays_passed = sum(1 for i in range(1, days_passed + 1) 
                            if datetime(now.year, now.month, i).weekday() < 5)
        weekdays_in_month = sum(1 for i in range(1, days_in_month + 1) 
                              if datetime(now.year, now.month, i).weekday() < 5)
        
        weekday_average = monthly_usage / max(weekdays_passed, 1)
        adjusted_prediction = weekday_average * weekdays_in_month * 0.85  # 주말 할인
        
        # 안전 예측 (보수적)
        safety_prediction = max(linear_prediction, adjusted_prediction) * 1.2
        
        return {
            "current_usage": monthly_usage,
            "days_passed": days_passed,
            "days_remaining": days_in_month - days_passed,
            "predictions": {
                "linear": round(linear_prediction),
                "adjusted": round(adjusted_prediction), 
                "safety": round(safety_prediction)
            },
            "risk_level": self._assess_risk_level(safety_prediction),
            "recommendations": self._get_recommendations(safety_prediction)
        }
    
    def _assess_risk_level(self, predicted_usage: float) -> str:
        """위험도 평가"""
        
        if predicted_usage < self.effective_limit * 0.8:
            return "low"
        elif predicted_usage < self.effective_limit:
            return "medium"
        elif predicted_usage < self.monthly_limit:
            return "high"
        else:
            return "critical"
    
    def _get_recommendations(self, predicted_usage: float) -> List[str]:
        """사용량 최적화 권장사항"""
        
        recommendations = []
        
        if predicted_usage > self.effective_limit:
            recommendations.extend([
                "🚨 하이브리드 모드 즉시 활성화 권장",
                "📦 캐시 시스템 확장 검토",
                "⏰ 피크 시간대 제한 고려"
            ])
        
        if predicted_usage > self.monthly_limit * 0.8:
            recommendations.extend([
                "📊 사용 패턴 분석 강화",
                "🤖 AI 폴백 시스템 준비",
                "👥 사용량 많은 사용자 모니터링"
            ])
        
        if predicted_usage > self.monthly_limit * 0.6:
            recommendations.extend([
                "💾 자주 사용되는 날짜 미리 캐싱",
                "🔄 중복 요청 방지 시스템 점검"
            ])
        
        return recommendations
    
    def get_usage_report(self) -> Dict[str, Any]:
        """종합 사용량 리포트"""
        
        current = self.get_current_usage()
        prediction = self.predict_monthly_usage()
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "current_status": current,
            "predictions": prediction,
            "system_recommendations": {
                "immediate_actions": prediction.get("recommendations", []),
                "mode_suggestion": self._suggest_operation_mode(prediction),
                "monitoring_alerts": self._generate_alerts(current, prediction)
            }
        }
    
    def _suggest_operation_mode(self, prediction: Dict[str, Any]) -> str:
        """운영 모드 제안"""
        
        risk_level = prediction.get("risk_level", "low")
        
        if risk_level == "critical":
            return "hybrid_primary"  # 하이브리드 모드 우선
        elif risk_level == "high":
            return "kasi_limited"    # KASI 제한적 사용
        else:
            return "kasi_primary"    # KASI 우선 사용
    
    def _generate_alerts(self, current: Dict[str, Any], prediction: Dict[str, Any]) -> List[str]:
        """모니터링 알림 생성"""
        
        alerts = []
        monthly = current.get("monthly", {})
        usage_pct = monthly.get("usage_percentage", 0)
        
        if usage_pct > 90:
            alerts.append("🚨 CRITICAL: 월간 사용량 90% 초과")
        elif usage_pct > 80:
            alerts.append("⚠️ WARNING: 월간 사용량 80% 초과")
        elif usage_pct > 70:
            alerts.append("📈 INFO: 월간 사용량 70% 도달")
        
        risk_level = prediction.get("risk_level")
        if risk_level == "critical":
            alerts.append("🚨 CRITICAL: 월말 한계 초과 예상")
        elif risk_level == "high":  
            alerts.append("⚠️ WARNING: 월말 사용량 위험 수준")
        
        return alerts


# 전역 모니터 인스턴스
usage_monitor = UsageMonitor()

def log_kasi_usage(success: bool = True, response_time: float = 0, user_info: str = ""):
    """KASI API 사용 로깅"""
    usage_monitor.log_usage("kasi_api", success, response_time, user_info)

def get_usage_dashboard() -> Dict[str, Any]:
    """사용량 대시보드 데이터"""
    return usage_monitor.get_usage_report()


if __name__ == "__main__":
    print("📊 KASI API 사용량 모니터링 시스템")
    print("=" * 50)
    
    # 테스트 로깅
    monitor = UsageMonitor()
    monitor.log_usage("test", True, 1.5, "test_user")
    
    # 현황 조회
    report = monitor.get_usage_report()
    
    print(f"오늘 사용량: {report['current_status']['today']['usage']}건")
    print(f"월간 사용량: {report['current_status']['monthly']['usage']}건")
    print(f"사용률: {report['current_status']['monthly']['usage_percentage']:.1f}%")
    
    if report['predictions']['risk_level'] != 'low':
        print(f"⚠️ 위험도: {report['predictions']['risk_level']}")
        for rec in report['predictions']['recommendations']:
            print(f"  - {rec}")