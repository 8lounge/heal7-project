#!/usr/bin/env python3
"""
✋ 사용자 승인 워크플로우 시스템
크롤링 작업 전 사용자 검토 및 승인 프로세스

🎯 핵심 기능:
- AI 분석 결과 사용자 승인 요청
- 단계별 승인/거부/수정 프로세스
- 실시간 승인 상태 추적
- 자동 타임아웃 및 폴백

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-09-03
"""

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import websockets
from pathlib import Path

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """승인 상태"""
    PENDING = "pending"           # 승인 대기 중
    APPROVED = "approved"         # 승인됨
    REJECTED = "rejected"         # 거부됨
    MODIFIED = "modified"         # 수정됨
    EXPIRED = "expired"           # 시간 만료
    CANCELLED = "cancelled"       # 취소됨


class ApprovalUrgency(Enum):
    """승인 긴급도"""
    LOW = "low"                   # 낮음 (24시간)
    MEDIUM = "medium"             # 보통 (4시간)
    HIGH = "high"                 # 높음 (1시간)
    CRITICAL = "critical"         # 긴급 (15분)


class CrawlAction(Enum):
    """크롤링 액션 타입"""
    SINGLE_URL = "single_url"
    BATCH_CRAWL = "batch_crawl"
    SCHEDULED_CRAWL = "scheduled_crawl"
    BULK_ANALYSIS = "bulk_analysis"


@dataclass
class ApprovalRequest:
    """승인 요청 데이터"""
    request_id: str
    title: str
    description: str
    action_type: CrawlAction
    
    # 크롤링 설정
    urls: List[str]
    crawler_config: Dict[str, Any]
    ai_recommendation: Dict[str, Any]
    
    # 승인 설정
    urgency: ApprovalUrgency = ApprovalUrgency.MEDIUM
    auto_approve_after: Optional[int] = None  # 초 단위
    required_approvers: List[str] = None
    
    # 메타데이터
    requester: str = "system"
    created_at: str = None
    estimated_duration: str = "알 수 없음"
    estimated_cost: float = 0.0
    risk_level: str = "medium"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.required_approvers is None:
            self.required_approvers = ["admin"]


@dataclass
class ApprovalResponse:
    """승인 응답 데이터"""
    request_id: str
    status: ApprovalStatus
    approver: str
    response_time: str
    
    # 승인 상세
    comment: str = ""
    modified_config: Optional[Dict[str, Any]] = None
    approval_conditions: List[str] = None
    
    def __post_init__(self):
        if self.response_time is None:
            self.response_time = datetime.now().isoformat()
        if self.approval_conditions is None:
            self.approval_conditions = []


class ApprovalWorkflow:
    """✋ 사용자 승인 워크플로우 매니저"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ApprovalWorkflow")
        
        # 승인 요청 저장소
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self.completed_requests: Dict[str, ApprovalResponse] = {}
        
        # WebSocket 연결 관리
        self.connected_clients: Dict[str, Any] = {}
        
        # 승인 통계
        self.stats = {
            "total_requests": 0,
            "approved": 0,
            "rejected": 0,
            "expired": 0,
            "avg_response_time": 0.0,
            "auto_approvals": 0
        }
        
        # 정책 설정
        self.default_timeout = {
            ApprovalUrgency.CRITICAL: 900,    # 15분
            ApprovalUrgency.HIGH: 3600,       # 1시간
            ApprovalUrgency.MEDIUM: 14400,    # 4시간
            ApprovalUrgency.LOW: 86400        # 24시간
        }
        
        # 자동 승인 규칙
        self.auto_approval_rules = [
            {
                "condition": "single_url_low_risk",
                "criteria": {
                    "action_type": CrawlAction.SINGLE_URL,
                    "risk_level": "low",
                    "url_count": 1
                },
                "enabled": True
            },
            {
                "condition": "trusted_domain",
                "criteria": {
                    "domains": [".go.kr", ".gov", "heal7.com"],
                    "risk_level": ["low", "medium"]
                },
                "enabled": True
            }
        ]
        
        self.logger.info("✅ 사용자 승인 워크플로우 시스템 초기화 완료")
    
    async def request_approval(
        self,
        title: str,
        urls: List[str],
        crawler_config: Dict[str, Any],
        ai_recommendation: Dict[str, Any],
        **kwargs
    ) -> str:
        """승인 요청 생성"""
        request_id = str(uuid.uuid4())[:8]
        
        # 위험도 평가
        risk_level = self._assess_risk_level(urls, crawler_config)
        
        # 긴급도 결정
        urgency = self._determine_urgency(urls, crawler_config, risk_level)
        
        approval_request = ApprovalRequest(
            request_id=request_id,
            title=title,
            description=self._generate_description(urls, ai_recommendation),
            action_type=self._determine_action_type(urls),
            urls=urls,
            crawler_config=crawler_config,
            ai_recommendation=ai_recommendation,
            urgency=urgency,
            risk_level=risk_level,
            estimated_duration=self._estimate_duration(urls),
            estimated_cost=self._estimate_cost(urls),
            **kwargs
        )
        
        # 자동 승인 체크
        if await self._check_auto_approval(approval_request):
            self.logger.info(f"🚀 자동 승인 적용: {request_id}")
            await self._auto_approve(approval_request)
            return request_id
        
        # 승인 요청 등록
        self.pending_requests[request_id] = approval_request
        self.stats["total_requests"] += 1
        
        # 타임아웃 스케줄링
        timeout_seconds = self.default_timeout[urgency]
        asyncio.create_task(self._schedule_timeout(request_id, timeout_seconds))
        
        # 알림 발송
        await self._notify_approvers(approval_request)
        
        self.logger.info(
            f"📋 승인 요청 생성: {request_id} "
            f"(긴급도: {urgency.value}, 위험도: {risk_level})"
        )
        
        return request_id
    
    async def submit_approval_response(
        self,
        request_id: str,
        approver: str,
        status: ApprovalStatus,
        comment: str = "",
        modified_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """승인 응답 처리"""
        if request_id not in self.pending_requests:
            self.logger.warning(f"⚠️ 승인 요청을 찾을 수 없음: {request_id}")
            return False
        
        request = self.pending_requests[request_id]
        
        # 승인 권한 체크
        if not self._check_approval_permission(approver, request):
            self.logger.warning(f"❌ 승인 권한 없음: {approver} for {request_id}")
            return False
        
        # 응답 생성
        response = ApprovalResponse(
            request_id=request_id,
            status=status,
            approver=approver,
            response_time=datetime.now().isoformat(),
            comment=comment,
            modified_config=modified_config
        )
        
        # 요청 완료 처리
        self.completed_requests[request_id] = response
        del self.pending_requests[request_id]
        
        # 통계 업데이트
        self._update_stats(response)
        
        # 알림 발송
        await self._notify_response_processed(request, response)
        
        self.logger.info(
            f"✅ 승인 응답 처리: {request_id} → {status.value} by {approver}"
        )
        
        return True
    
    async def get_approval_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """승인 상태 조회"""
        # 대기 중인 요청
        if request_id in self.pending_requests:
            request = self.pending_requests[request_id]
            return {
                "request_id": request_id,
                "status": ApprovalStatus.PENDING.value,
                "request": asdict(request),
                "waiting_time": self._calculate_waiting_time(request.created_at),
                "remaining_timeout": self._calculate_remaining_timeout(request)
            }
        
        # 완료된 요청
        if request_id in self.completed_requests:
            response = self.completed_requests[request_id]
            return {
                "request_id": request_id,
                "status": response.status.value,
                "response": asdict(response)
            }
        
        return None
    
    async def list_pending_requests(self, approver: str = None) -> List[Dict[str, Any]]:
        """대기 중인 승인 요청 목록"""
        pending_list = []
        
        for request_id, request in self.pending_requests.items():
            # 승인자 필터링
            if approver and approver not in request.required_approvers:
                continue
            
            pending_list.append({
                "request_id": request_id,
                "title": request.title,
                "urgency": request.urgency.value,
                "risk_level": request.risk_level,
                "url_count": len(request.urls),
                "created_at": request.created_at,
                "waiting_time": self._calculate_waiting_time(request.created_at),
                "remaining_timeout": self._calculate_remaining_timeout(request)
            })
        
        # 긴급도 순으로 정렬
        urgency_order = {
            ApprovalUrgency.CRITICAL: 0,
            ApprovalUrgency.HIGH: 1,
            ApprovalUrgency.MEDIUM: 2,
            ApprovalUrgency.LOW: 3
        }
        
        pending_list.sort(key=lambda x: urgency_order.get(
            ApprovalUrgency(x["urgency"]), 999
        ))
        
        return pending_list
    
    async def cancel_approval_request(self, request_id: str, reason: str = "") -> bool:
        """승인 요청 취소"""
        if request_id not in self.pending_requests:
            return False
        
        request = self.pending_requests[request_id]
        
        response = ApprovalResponse(
            request_id=request_id,
            status=ApprovalStatus.CANCELLED,
            approver="system",
            response_time=datetime.now().isoformat(),
            comment=f"승인 요청 취소: {reason}"
        )
        
        self.completed_requests[request_id] = response
        del self.pending_requests[request_id]
        
        await self._notify_response_processed(request, response)
        
        self.logger.info(f"🚫 승인 요청 취소: {request_id} - {reason}")
        return True
    
    def get_approval_statistics(self) -> Dict[str, Any]:
        """승인 시스템 통계"""
        return {
            **self.stats,
            "pending_requests": len(self.pending_requests),
            "auto_approval_rate": (
                self.stats["auto_approvals"] / max(1, self.stats["total_requests"]) * 100
            ),
            "approval_rate": (
                self.stats["approved"] / max(1, self.stats["total_requests"]) * 100
            )
        }
    
    # 내부 헬퍼 메서드들
    
    def _assess_risk_level(self, urls: List[str], config: Dict[str, Any]) -> str:
        """위험도 평가"""
        risk_score = 0
        
        # URL 개수
        if len(urls) > 100:
            risk_score += 3
        elif len(urls) > 10:
            risk_score += 2
        elif len(urls) > 1:
            risk_score += 1
        
        # 도메인 체크
        for url in urls:
            if any(domain in url.lower() for domain in ['.go.kr', '.gov', 'heal7.com']):
                risk_score -= 1  # 신뢰할 수 있는 도메인
            elif any(pattern in url.lower() for pattern in ['admin', 'api', 'private']):
                risk_score += 2  # 민감한 경로
        
        # 크롤링 설정
        if config.get('screenshot', False):
            risk_score += 1
        if config.get('retries', 0) > 5:
            risk_score += 1
        
        # 위험도 매핑
        if risk_score >= 5:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _determine_urgency(self, urls: List[str], config: Dict[str, Any], risk_level: str) -> ApprovalUrgency:
        """긴급도 결정"""
        if risk_level == "high":
            return ApprovalUrgency.CRITICAL
        elif len(urls) > 50:
            return ApprovalUrgency.HIGH
        elif risk_level == "medium":
            return ApprovalUrgency.MEDIUM
        else:
            return ApprovalUrgency.LOW
    
    def _determine_action_type(self, urls: List[str]) -> CrawlAction:
        """액션 타입 결정"""
        if len(urls) == 1:
            return CrawlAction.SINGLE_URL
        else:
            return CrawlAction.BATCH_CRAWL
    
    def _generate_description(self, urls: List[str], ai_rec: Dict[str, Any]) -> str:
        """승인 요청 설명 생성"""
        url_count = len(urls)
        primary_crawler = ai_rec.get("primary_crawler", "unknown")
        confidence = ai_rec.get("confidence_score", 0)
        
        description = f"""
🎯 **크롤링 요청**: {url_count}개 URL 처리
🤖 **AI 추천**: {primary_crawler} 크롤러 (신뢰도: {confidence:.1f}%)
🌐 **대상 사이트**: {', '.join(urls[:3])}{"..." if url_count > 3 else ""}
        """.strip()
        
        return description
    
    def _estimate_duration(self, urls: List[str]) -> str:
        """소요 시간 추정"""
        url_count = len(urls)
        if url_count == 1:
            return "1-3분"
        elif url_count <= 10:
            return f"{url_count * 2}-{url_count * 5}분"
        else:
            return f"{url_count // 10}-{url_count // 5}시간"
    
    def _estimate_cost(self, urls: List[str]) -> float:
        """비용 추정"""
        return len(urls) * 0.001  # URL당 0.001달러 가정
    
    async def _check_auto_approval(self, request: ApprovalRequest) -> bool:
        """자동 승인 조건 체크"""
        for rule in self.auto_approval_rules:
            if not rule["enabled"]:
                continue
            
            criteria = rule["criteria"]
            
            # 조건별 체크
            if rule["condition"] == "single_url_low_risk":
                if (request.action_type == CrawlAction.SINGLE_URL and
                    request.risk_level == "low" and
                    len(request.urls) == 1):
                    return True
            
            elif rule["condition"] == "trusted_domain":
                trusted_domains = criteria.get("domains", [])
                allowed_risks = criteria.get("risk_level", [])
                
                if (request.risk_level in allowed_risks and
                    any(domain in url for url in request.urls for domain in trusted_domains)):
                    return True
        
        return False
    
    async def _auto_approve(self, request: ApprovalRequest):
        """자동 승인 처리"""
        response = ApprovalResponse(
            request_id=request.request_id,
            status=ApprovalStatus.APPROVED,
            approver="auto_system",
            response_time=datetime.now().isoformat(),
            comment="자동 승인 규칙에 의한 승인"
        )
        
        self.completed_requests[request.request_id] = response
        self.stats["approved"] += 1
        self.stats["auto_approvals"] += 1
        self.stats["total_requests"] += 1
    
    def _check_approval_permission(self, approver: str, request: ApprovalRequest) -> bool:
        """승인 권한 체크"""
        return approver in request.required_approvers or approver == "admin"
    
    async def _notify_approvers(self, request: ApprovalRequest):
        """승인자에게 알림"""
        notification = {
            "type": "approval_request",
            "request_id": request.request_id,
            "title": request.title,
            "urgency": request.urgency.value,
            "url_count": len(request.urls),
            "created_at": request.created_at
        }
        
        # WebSocket으로 실시간 알림 (구현 예정)
        self.logger.info(f"📢 승인 요청 알림 발송: {request.request_id}")
    
    async def _notify_response_processed(self, request: ApprovalRequest, response: ApprovalResponse):
        """응답 처리 완료 알림"""
        notification = {
            "type": "approval_response",
            "request_id": response.request_id,
            "status": response.status.value,
            "approver": response.approver,
            "response_time": response.response_time
        }
        
        self.logger.info(f"📢 승인 응답 알림 발송: {response.request_id}")
    
    async def _schedule_timeout(self, request_id: str, timeout_seconds: int):
        """타임아웃 스케줄링"""
        await asyncio.sleep(timeout_seconds)
        
        if request_id in self.pending_requests:
            request = self.pending_requests[request_id]
            
            response = ApprovalResponse(
                request_id=request_id,
                status=ApprovalStatus.EXPIRED,
                approver="system",
                response_time=datetime.now().isoformat(),
                comment=f"승인 시간 만료 ({timeout_seconds}초)"
            )
            
            self.completed_requests[request_id] = response
            del self.pending_requests[request_id]
            
            self.stats["expired"] += 1
            
            await self._notify_response_processed(request, response)
            
            self.logger.warning(f"⏰ 승인 요청 시간 만료: {request_id}")
    
    def _calculate_waiting_time(self, created_at: str) -> str:
        """대기 시간 계산"""
        created = datetime.fromisoformat(created_at)
        waiting_seconds = (datetime.now() - created).total_seconds()
        
        if waiting_seconds < 60:
            return f"{int(waiting_seconds)}초"
        elif waiting_seconds < 3600:
            return f"{int(waiting_seconds // 60)}분"
        else:
            return f"{int(waiting_seconds // 3600)}시간"
    
    def _calculate_remaining_timeout(self, request: ApprovalRequest) -> str:
        """남은 타임아웃 시간"""
        created = datetime.fromisoformat(request.created_at)
        elapsed = (datetime.now() - created).total_seconds()
        timeout = self.default_timeout[request.urgency]
        remaining = timeout - elapsed
        
        if remaining <= 0:
            return "만료됨"
        elif remaining < 60:
            return f"{int(remaining)}초 남음"
        elif remaining < 3600:
            return f"{int(remaining // 60)}분 남음"
        else:
            return f"{int(remaining // 3600)}시간 남음"
    
    def _update_stats(self, response: ApprovalResponse):
        """통계 업데이트"""
        if response.status == ApprovalStatus.APPROVED:
            self.stats["approved"] += 1
        elif response.status == ApprovalStatus.REJECTED:
            self.stats["rejected"] += 1
        elif response.status == ApprovalStatus.EXPIRED:
            self.stats["expired"] += 1
        
        # 평균 응답 시간 업데이트 (구현 예정)


# 전역 인스턴스
_approval_workflow = None

async def get_approval_workflow() -> ApprovalWorkflow:
    """승인 워크플로우 인스턴스 조회"""
    global _approval_workflow
    if _approval_workflow is None:
        _approval_workflow = ApprovalWorkflow()
    return _approval_workflow


# 편의 함수들
async def request_crawl_approval(
    title: str,
    urls: List[str], 
    crawler_config: Dict[str, Any],
    ai_recommendation: Dict[str, Any],
    **kwargs
) -> str:
    """크롤링 승인 요청"""
    workflow = await get_approval_workflow()
    return await workflow.request_approval(
        title, urls, crawler_config, ai_recommendation, **kwargs
    )


async def wait_for_approval(request_id: str, check_interval: float = 5.0) -> ApprovalResponse:
    """승인 완료까지 대기"""
    workflow = await get_approval_workflow()
    
    while True:
        status_info = await workflow.get_approval_status(request_id)
        if not status_info:
            raise ValueError(f"승인 요청을 찾을 수 없음: {request_id}")
        
        if status_info["status"] != ApprovalStatus.PENDING.value:
            if request_id in workflow.completed_requests:
                return workflow.completed_requests[request_id]
            break
        
        await asyncio.sleep(check_interval)
    
    raise RuntimeError(f"승인 대기 중 오류 발생: {request_id}")


async def approve_request(
    request_id: str,
    approver: str = "admin",
    comment: str = ""
) -> bool:
    """승인 요청 승인"""
    workflow = await get_approval_workflow()
    return await workflow.submit_approval_response(
        request_id, approver, ApprovalStatus.APPROVED, comment
    )