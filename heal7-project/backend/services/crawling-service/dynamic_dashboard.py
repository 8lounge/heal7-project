#!/usr/bin/env python3
"""
🕷️ 역동적 실시간 크롤링 모니터링 시스템
화려한 그래프와 실시간 애니메이션이 포함된 크롤링 대시보드
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid

class CrawlingStats(BaseModel):
    """실시간 크롤링 통계"""
    service_id: str
    service_name: str
    target_url: str
    status: str  # running, stopped, error
    collected_count: int
    success_rate: float
    avg_response_time: float
    last_update: str
    errors_count: int
    data_quality_score: float

class RealTimeMonitor:
    """실시간 모니터링 데이터 관리"""
    
    def __init__(self):
        self.services: Dict[str, CrawlingStats] = {}
        self.historical_data: Dict[str, List[Dict]] = {}
        self.websocket_connections: List[WebSocket] = []
        
        # 기본 서비스 설정 (꿈풀이 + 정부지원사업 2개 사이트)
        self._setup_default_services()
    
    def _setup_default_services(self):
        """기본 크롤링 서비스 설정"""
        dream_service = CrawlingStats(
            service_id="dream_collector",
            service_name="🌙 꿈풀이 데이터 수집",
            target_url="www.co.kr, sajuforum.com, kaloo.kr",
            status="running",
            collected_count=23941,
            success_rate=94.5,
            avg_response_time=1.2,
            last_update=datetime.now().isoformat(),
            errors_count=127,
            data_quality_score=96.8
        )
        
        gov1_service = CrawlingStats(
            service_id="gov_bizinfo",
            service_name="📄 BizInfo 정부지원사업",
            target_url="www.go.kr",
            status="running",
            collected_count=156,
            success_rate=89.2,
            avg_response_time=2.8,
            last_update=datetime.now().isoformat(),
            errors_count=18,
            data_quality_score=92.4
        )
        
        gov2_service = CrawlingStats(
            service_id="gov_kstartup",
            service_name="🚀 K-Startup 창업지원",
            target_url="www.k-startup.kr",
            status="running",
            collected_count=89,
            success_rate=91.7,
            avg_response_time=2.1,
            last_update=datetime.now().isoformat(),
            errors_count=8,
            data_quality_score=94.1
        )
        
        self.services = {
            "dream_collector": dream_service,
            "gov_bizinfo": gov1_service,
            "gov_kstartup": gov2_service
        }
        
        # 히스토리컬 데이터 초기화
        for service_id in self.keys():
            self.historical_data[service_id] = []
    
    async def connect_websocket(self, websocket: WebSocket):
        """WebSocket 연결 관리"""
        await websocket.accept()
        self.append(websocket)
    
    def disconnect_websocket(self, websocket: WebSocket):
        """WebSocket 연결 해제"""
        if websocket in self.websocket_connections:
            self.remove(websocket)
    
    async def broadcast_update(self, data: Dict):
        """모든 연결된 클라이언트에 실시간 업데이트 전송"""
        dead_connections = []
        for connection in self.websocket_connections:
            try:
                await connection.send_text(json.dumps(data))
            except:
                dead_connections.append(connection)
        
        # 죽은 연결 제거
        for dead in dead_connections:
            self.disconnect_websocket(dead)
    
    async def simulate_real_time_data(self):
        """실시간 데이터 시뮬레이션"""
        while True:
            for service_id, service in self.items():
                # 동적 데이터 업데이트
                if service.status == "running":
                    # 수집 개수 증가 (랜덤)
                    increment = random.randint(0, 3)
                    service.collected_count += increment
                    
                    # 성공률 변화
                    service.success_rate += random.uniform(-0.5, 0.5)
                    service.success_rate = max(80.0, min(100.0, service.success_rate))
                    
                    # 응답 시간 변화
                    service.avg_response_time += random.uniform(-0.3, 0.3)
                    service.avg_response_time = max(0.5, min(5.0, service.avg_response_time))
                    
                    # 품질 점수 변화
                    service.data_quality_score += random.uniform(-0.2, 0.2)
                    service.data_quality_score = max(85.0, min(100.0, service.data_quality_score))
                    
                    # 에러 카운트 (가끔 증가)
                    if random.random() < 0.1:
                        service.errors_count += 1
                    
                    service.last_update = datetime.now().isoformat()
                    
                    # 히스토리컬 데이터 저장
                    self.historical_data[service_id].append({
                        'timestamp': int(time.time()),
                        'collected_count': service.collected_count,
                        'success_rate': service.success_rate,
                        'response_time': service.avg_response_time,
                        'quality_score': service.data_quality_score
                    })
                    
                    # 최대 100개 히스토리 유지
                    if len(self.historical_data[service_id]) > 100:
                        self.historical_data[service_id].pop(0)
            
            # 실시간 업데이트 브로드캐스트
            await self.broadcast_update({
                'type': 'stats_update',
                'services': [service.dict() for service in self.values()],
                'historical_data': self.historical_data,
                'timestamp': datetime.now().isoformat()
            })
            
            await asyncio.sleep(2)  # 2초마다 업데이트

# 전역 모니터 인스턴스
monitor = RealTimeMonitor()

def get_dynamic_dashboard_html():
    """역동적 대시보드 HTML 생성"""
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🕷️ 실시간 크롤링 모니터링 시스템</title>
    <link href="https://fonts.com/css2?family=Pretendard:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.com"></script>
    <script src="https://cdn.net/npm/chart.js"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        body {
            font-family: 'Pretendard', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            overflow-x: hidden;
        }
        
        /* 화려한 버튼 스타일 */
        .dynamic-btn {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
            background-size: 300% 300%;
            animation: gradientShift 3s ease infinite;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .dynamic-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .dynamic-btn:hover::before {
            left: 100%;
        }
        
        .dynamic-btn:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* 펄싱 효과 */
        .pulse-ring {
            animation: pulseRing 2s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite;
        }
        
        @keyframes pulseRing {
            0% { transform: scale(0.33); opacity: 1; }
            80%, 100% { transform: scale(2.33); opacity: 0; }
        }
        
        /* 실시간 데이터 애니메이션 */
        .data-pulse {
            animation: dataPulse 1.5s ease-in-out infinite alternate;
        }
        
        @keyframes dataPulse {
            from { opacity: 0.7; transform: scale(1); }
            to { opacity: 1; transform: scale(1.05); }
        }
        
        /* 상태 표시기 */
        .status-indicator {
            animation: statusBlink 1s ease-in-out infinite;
        }
        
        @keyframes statusBlink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* 그래프 컨테이너 애니메이션 */
        .chart-container {
            animation: slideInUp 0.8s ease-out;
        }
        
        @keyframes slideInUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        /* 카운터 애니메이션 */
        .counter {
            font-variant-numeric: tabular-nums;
        }
        
        /* 글로우 효과 */
        .glow-effect {
            box-shadow: 0 0 20px rgba(103, 232, 249, 0.5);
            animation: glowPulse 2s ease-in-out infinite alternate;
        }
        
        @keyframes glowPulse {
            from { box-shadow: 0 0 20px rgba(103, 232, 249, 0.5); }
            to { box-shadow: 0 0 30px rgba(103, 232, 249, 0.8); }
        }
        
        /* 회전 애니메이션 */
        .spin-slow {
            animation: spin 3s linear infinite;
        }
        
        /* 파도 효과 */
        .wave-effect {
            position: relative;
            overflow: hidden;
        }
        
        .wave-effect::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: wave 2s infinite;
        }
        
        @keyframes wave {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* 3D 효과 */
        .card-3d {
            transform-style: preserve-3d;
            transition: transform 0.3s ease;
        }
        
        .card-3d:hover {
            transform: rotateX(5deg) rotateY(5deg) translateZ(10px);
        }
        
        /* 실시간 로그 스크롤 */
        .log-container {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .log-item {
            animation: slideInLeft 0.5s ease-out;
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
</head>
<body class="min-h-screen">
    <div class="container mx-auto p-6">
        <!-- 헤더 -->
        <div class="mb-8 text-center">
            <h1 class="text-5xl font-bold text-white mb-4 data-pulse">
                🕷️ 실시간 크롤링 모니터링 시스템
            </h1>
            <p class="text-white/80 text-xl">
                역동적이고 화려한 데이터 수집 현황 · AI 기반 품질 관리
            </p>
            <div class="mt-4 flex justify-center space-x-4">
                <button class="dynamic-btn px-6 py-3 rounded-full text-white font-bold" onclick="toggleAllServices()">
                    ⚡ 전체 제어
                </button>
                <button class="dynamic-btn px-6 py-3 rounded-full text-white font-bold" onclick="refreshData()">
                    🔄 데이터 갱신
                </button>
                <button class="dynamic-btn px-6 py-3 rounded-full text-white font-bold" onclick="exportData()">
                    📊 데이터 내보내기
                </button>
            </div>
        </div>

        <!-- 전체 통계 대시보드 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 card-3d wave-effect">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="text-white font-semibold">총 수집 데이터</h3>
                    <div class="w-3 h-3 bg-green-400 rounded-full status-indicator"></div>
                </div>
                <div class="text-3xl font-bold text-white counter" id="total-collected">24,186</div>
                <div class="text-green-200 text-sm mt-1">+127 (지난 1시간)</div>
            </div>
            
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 card-3d wave-effect">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="text-white font-semibold">평균 성공률</h3>
                    <div class="w-3 h-3 bg-blue-400 rounded-full status-indicator"></div>
                </div>
                <div class="text-3xl font-bold text-white counter" id="avg-success-rate">91.8%</div>
                <div class="text-blue-200 text-sm mt-1">↑ 2.3% (개선)</div>
            </div>
            
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 card-3d wave-effect">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="text-white font-semibold">평균 응답시간</h3>
                    <div class="w-3 h-3 bg-yellow-400 rounded-full status-indicator"></div>
                </div>
                <div class="text-3xl font-bold text-white counter" id="avg-response-time">2.0초</div>
                <div class="text-yellow-200 text-sm mt-1">~ 0.2초 (안정)</div>
            </div>
            
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 card-3d wave-effect">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="text-white font-semibold">데이터 품질</h3>
                    <div class="w-3 h-3 bg-purple-400 rounded-full status-indicator"></div>
                </div>
                <div class="text-3xl font-bold text-white counter" id="data-quality">94.4%</div>
                <div class="text-purple-200 text-sm mt-1">A+ 등급</div>
            </div>
        </div>

        <!-- 서비스별 상세 모니터링 -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div id="service-cards-container">
                <!-- 서비스 카드들이 동적으로 생성됨 -->
            </div>
        </div>

        <!-- 실시간 차트 및 그래프 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 chart-container glow-effect">
                <h3 class="text-white font-bold text-xl mb-4">📈 수집 현황 실시간 차트</h3>
                <canvas id="realtime-chart" width="400" height="200"></canvas>
            </div>
            
            <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 chart-container glow-effect">
                <h3 class="text-white font-bold text-xl mb-4">🎯 성공률 분석</h3>
                <canvas id="success-rate-chart" width="400" height="200"></canvas>
            </div>
        </div>

        <!-- 실시간 로그 및 활동 -->
        <div class="bg-white/10 backdrop-blur-md rounded-xl p-6 glow-effect">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-white font-bold text-xl">📋 실시간 활동 로그</h3>
                <div class="text-white/60 text-sm">실시간 업데이트 중 <span class="animate-ping">●</span></div>
            </div>
            <div id="real-time-logs" class="log-container space-y-2">
                <!-- 실시간 로그가 여기에 표시됨 -->
            </div>
        </div>
    </div>

    <!-- JavaScript 실시간 기능 -->
    <script>
        let realtimeChart, successRateChart;
        let websocket;
        let services = {};
        let historicalData = {};
        
        // 초기화
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            connectWebSocket();
            startCounterAnimations();
        });
        
        // WebSocket 연결
        function connectWebSocket() {
            const protocol = window.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.host}/ws/monitor`;
            
            websocket = new WebSocket(wsUrl);
            
            websocket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === 'stats_update') {
                    updateServices(data.services);
                    updateHistoricalData(data.historical_data);
                    updateCharts();
                    addRealTimeLog(`📊 데이터 업데이트: ${new Date().toLocaleTimeString()}`);
                }
            };
            
            websocket.onerror = function(error) {
                console.error('WebSocket error:', error);
                addRealTimeLog(`❌ 연결 오류: ${error.message}`);
            };
            
            websocket.onclose = function() {
                addRealTimeLog('🔌 연결이 끊어졌습니다. 재연결 시도 중...');
                setTimeout(connectWebSocket, 3000);
            };
        }
        
        // 서비스 데이터 업데이트
        function updateServices(newServices) {
            newServices.forEach(service => {
                services[service.service_id] = service;
            });
            
            renderServiceCards();
            updateOverallStats();
        }
        
        // 전체 통계 업데이트
        function updateOverallStats() {
            const serviceList = Object.values(services);
            const totalCollected = serviceList.reduce((sum, s) => sum + s.collected_count, 0);
            const avgSuccessRate = serviceList.reduce((sum, s) => sum + s.success_rate, 0) / serviceList.length;
            const avgResponseTime = serviceList.reduce((sum, s) => sum + s.avg_response_time, 0) / serviceList.length;
            const avgQuality = serviceList.reduce((sum, s) => sum + s.data_quality_score, 0) / serviceList.length;
            
            animateCounter('total-collected', totalCollected.toLocaleString());
            animateCounter('avg-success-rate', avgSuccessRate.toFixed(1) + '%');
            animateCounter('avg-response-time', avgResponseTime.toFixed(1) + '초');
            animateCounter('data-quality', avgQuality.toFixed(1) + '%');
        }
        
        // 서비스 카드 렌더링
        function renderServiceCards() {
            const container = document.getElementById('service-cards-container');
            container.innerHTML = '';
            
            Object.values(services).forEach(service => {
                const statusColor = getStatusColor(service.status);
                const qualityGrade = getQualityGrade(service.data_quality_score);
                
                const card = document.createElement('div');
                card.className = 'bg-white/10 backdrop-blur-md rounded-xl p-6 card-3d wave-effect';
                card.innerHTML = `
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-white font-bold text-lg">${service.service_name}</h3>
                        <div class="flex items-center space-x-2">
                            <div class="w-3 h-3 ${statusColor} rounded-full status-indicator"></div>
                            <span class="text-white text-sm">${service.toUpperCase()}</span>
                        </div>
                    </div>
                    
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="text-white/70">수집량</span>
                            <span class="text-white font-bold data-pulse">${service.toLocaleString()}</span>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-white/70">성공률</span>
                            <span class="text-green-300 font-bold">${service.toFixed(1)}%</span>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-white/70">응답시간</span>
                            <span class="text-blue-300 font-bold">${service.toFixed(1)}초</span>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-white/70">품질등급</span>
                            <span class="text-purple-300 font-bold">${qualityGrade}</span>
                        </div>
                    </div>
                    
                    <div class="mt-4 flex space-x-2">
                        <button class="dynamic-btn px-3 py-1 rounded text-sm text-white" onclick="controlService('${service.service_id}', '${service.status === 'running' ? 'stop' : 'start'}')">
                            ${service.status === 'running' ? '⏸️ 중지' : '▶️ 시작'}
                        </button>
                        <button class="dynamic-btn px-3 py-1 rounded text-sm text-white" onclick="showServiceDetails('${service.service_id}')">
                            📊 상세
                        </button>
                    </div>
                    
                    <div class="mt-3 text-white/50 text-xs">
                        대상: ${service.target_url}
                    </div>
                `;
                
                container.appendChild(card);
            });
        }
        
        // 차트 초기화
        function initCharts() {
            // 실시간 수집 차트
            const realtimeCtx = document.getElementById('realtime-chart').getContext('2d');
            realtimeChart = new Chart(realtimeCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: '꿈풀이',
                        data: [],
                        borderColor: '#ff6b6b',
                        backgroundColor: 'rgba(255, 107, 107, 0.1)',
                        tension: 0.4
                    }, {
                        label: 'BizInfo',
                        data: [],
                        borderColor: '#4ecdc4',
                        backgroundColor: 'rgba(78, 205, 196, 0.1)',
                        tension: 0.4
                    }, {
                        label: 'K-Startup',
                        data: [],
                        borderColor: '#45b7d1',
                        backgroundColor: 'rgba(69, 183, 209, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    },
                    scales: {
                        y: {
                            ticks: { color: 'white' },
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        },
                        x: {
                            ticks: { color: 'white' },
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        }
                    },
                    animation: {
                        duration: 1000,
                        easing: 'easeInOutQuart'
                    }
                }
            });
            
            // 성공률 차트
            const successCtx = document.getElementById('success-rate-chart').getContext('2d');
            successRateChart = new Chart(successCtx, {
                type: 'doughnut',
                data: {
                    labels: ['성공', '실패'],
                    datasets: [{
                        data: [91.8, 8.2],
                        backgroundColor: ['#4ade80', '#f87171'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    },
                    animation: {
                        animateRotate: true,
                        duration: 2000
                    }
                }
            });
        }
        
        // 차트 업데이트
        function updateCharts() {
            if (!historicalData) return;
            
            const now = new Date();
            const labels = [];
            for (let i = 9; i >= 0; i--) {
                const time = new Date(now - i * 2000);
                labels.push(time.toLocaleTimeString().slice(0, 5));
            }
            
            realtimeChart.labels = labels;
            
            // 각 서비스별 데이터 업데이트
            const serviceIds = ['dream_collector', 'gov_bizinfo', 'gov_kstartup'];
            serviceIds.forEach((serviceId, index) => {
                const data = historicalData[serviceId] || [];
                const recentData = data.slice(-10).map(d => d.collected_count);
                realtimeChart.datasets[index].data = recentData;
            });
            
            realtimeChart.update('none');
        }
        
        // 유틸리티 함수들
        function getStatusColor(status) {
            const colors = {
                'running': 'bg-green-400',
                'stopped': 'bg-red-400',
                'error': 'bg-orange-400'
            };
            return colors[status] || 'bg-gray-400';
        }
        
        function getQualityGrade(score) {
            if (score >= 95) return 'A+';
            if (score >= 90) return 'A';
            if (score >= 85) return 'B+';
            if (score >= 80) return 'B';
            return 'C';
        }
        
        function animateCounter(elementId, targetValue) {
            const element = document.getElementById(elementId);
            if (element && element.textContent !== targetValue) {
                element.add('data-pulse');
                element.textContent = targetValue;
                setTimeout(() => element.remove('data-pulse'), 1500);
            }
        }
        
        function addRealTimeLog(message) {
            const logsContainer = document.getElementById('real-time-logs');
            const logItem = document.createElement('div');
            logItem.className = 'log-item text-white/80 text-sm p-2 bg-white/5 rounded';
            logItem.innerHTML = `<span class="text-white/60">${new Date().toLocaleTimeString()}</span> ${message}`;
            
            logsContainer.insertBefore(logItem, logsContainer.firstChild);
            
            // 최대 50개 로그 유지
            while (logsContainer.length > 50) {
                logsContainer.removeChild(logsContainer.lastChild);
            }
        }
        
        // 컨트롤 함수들
        function toggleAllServices() {
            addRealTimeLog('⚡ 전체 서비스 제어 명령 실행');
        }
        
        function refreshData() {
            addRealTimeLog('🔄 수동 데이터 갱신 요청');
        }
        
        function exportData() {
            addRealTimeLog('📊 데이터 내보내기 시작');
        }
        
        function controlService(serviceId, action) {
            addRealTimeLog(`🎛️ 서비스 ${serviceId}: ${action} 명령`);
        }
        
        function showServiceDetails(serviceId) {
            addRealTimeLog(`📊 서비스 ${serviceId} 상세 정보 요청`);
        }
        
        // 히스토리컬 데이터 업데이트
        function updateHistoricalData(data) {
            historicalData = data;
        }
        
        // 카운터 애니메이션 시작
        function startCounterAnimations() {
            // 초기 애니메이션 효과
            setTimeout(() => {
                document.querySelectorAll('.counter').forEach(el => {
                    el.add('data-pulse');
                });
            }, 500);
        }
    </script>
</body>
</html>
"""

# FastAPI 앱에 추가할 함수들
async def setup_dynamic_routes(app: FastAPI):
    """동적 라우트 설정"""
    
    @app.get("/", response_class=HTMLResponse)
    async def get_dynamic_dashboard():
        """새로운 역동적 대시보드"""
        return HTMLResponse(content=get_dynamic_dashboard_html())
    
    @app.websocket("/ws/monitor")
    async def websocket_monitor_endpoint(websocket: WebSocket):
        """실시간 모니터링 WebSocket"""
        await monitor.connect_websocket(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            monitor.disconnect_websocket(websocket)
    
    # 실시간 데이터 시뮬레이션 시작
    asyncio.create_task(monitor.simulate_real_time_data())