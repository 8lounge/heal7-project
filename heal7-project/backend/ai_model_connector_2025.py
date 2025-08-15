#!/usr/bin/env python3
"""
HEAL7 최신 AI 모델 연동 체크 및 테스트 시스템 (2025)
업데이트된 모델들: Gemini 2.0 Flash, GPT-4o, Claude 3.5 Sonnet, Perplexity, 네이버 Clova X
"""

import asyncio
import aiohttp
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv('/home/ubuntu/project/backend/api/.env.ai')

class AIModelConnector2025:
    """2025년 최신 AI 모델들의 연동 상태 체크"""
    
    def __init__(self):
        self.models = {
            "gemini-2.0-flash": {
                "name": "Gemini 2.0 Flash",
                "provider": "Google",
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent",
                "api_key_env": "GOOGLE_API_KEY",
                "is_free": True,
                "cost_per_1k_tokens": 0.0,
                "features": ["text", "vision", "code", "multimodal"],
                "max_tokens": 32768,
                "speed": "very_fast",
                "status": "unknown"
            },
            "gpt-4o": {
                "name": "GPT-4o",
                "provider": "OpenAI", 
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "api_key_env": "OPENAI_API_KEY",
                "is_free": False,
                "cost_per_1k_tokens": 0.015,  # input cost
                "features": ["text", "vision", "code", "multimodal"],
                "max_tokens": 128000,
                "speed": "fast",
                "status": "unknown"
            },
            "gpt-4o-mini": {
                "name": "GPT-4o Mini", 
                "provider": "OpenAI",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "api_key_env": "OPENAI_API_KEY",
                "is_free": False,
                "cost_per_1k_tokens": 0.00015,  # very cheap!
                "features": ["text", "vision", "code"],
                "max_tokens": 128000,
                "speed": "very_fast",
                "status": "unknown"
            },
            "claude-3.5-sonnet": {
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "endpoint": "https://api.anthropic.com/v1/messages",
                "api_key_env": "ANTHROPIC_API_KEY", 
                "is_free": False,
                "cost_per_1k_tokens": 0.003,
                "features": ["text", "code", "analysis", "safety"],
                "max_tokens": 200000,
                "speed": "medium",
                "status": "unknown"
            },
            "perplexity-sonar": {
                "name": "Perplexity Sonar",
                "provider": "Perplexity AI",
                "endpoint": "https://api.perplexity.ai/chat/completions",
                "api_key_env": "PERPLEXITY_API_KEY",
                "is_free": False,
                "cost_per_1k_tokens": 0.005,
                "features": ["realtime_search", "citations", "web_access"],
                "max_tokens": 4096,
                "speed": "medium",
                "status": "unknown"
            },
            "clova-x": {
                "name": "네이버 Clova X",
                "provider": "Naver",
                "endpoint": "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003",
                "api_key_env": "CLOVAX_API_KEY",
                "is_free": False,
                "cost_per_1k_tokens": 0.002,  # 추정
                "features": ["korean", "text", "conversation"],
                "max_tokens": 4096,
                "speed": "fast",
                "status": "unknown"
            }
        }
        
        self.test_results = {}
    
    async def check_api_keys(self) -> Dict[str, Any]:
        """API 키 설정 상태 확인"""
        key_status = {}
        
        for model_id, config in self.models.items():
            api_key = os.getenv(config["api_key_env"])
            
            if api_key and len(api_key) > 10:
                key_status[model_id] = {
                    "available": True,
                    "key_preview": f"{api_key[:10]}...{api_key[-4:]}",
                    "key_length": len(api_key)
                }
                print(f"✅ {config['name']}: API 키 설정됨 ({api_key[:10]}...)")
            else:
                key_status[model_id] = {
                    "available": False,
                    "key_preview": None,
                    "key_length": 0
                }
                print(f"❌ {config['name']}: API 키 누락")
        
        return key_status
    
    async def test_gemini_2_flash(self) -> Dict[str, Any]:
        """Gemini 2.0 Flash 테스트"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        url = f"{self.models['gemini-2.0-flash']['endpoint']}?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "안녕하세요! Gemini 2.0 Flash 테스트입니다. 간단히 인사해주세요."
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 100
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    elapsed_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data["candidates"][0]["content"]["parts"][0]["text"]
                        
                        return {
                            "success": True,
                            "response": content,
                            "response_time": elapsed_time,
                            "model_version": "gemini-2.0-flash-exp"
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "response_time": elapsed_time
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_gpt_4o(self, model_name: str = "gpt-4o") -> Dict[str, Any]:
        """GPT-4o / GPT-4o-mini 테스트"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": f"안녕하세요! {model_name} 테스트입니다. 간단히 인사해주세요."}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    elapsed_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        
                        return {
                            "success": True,
                            "response": content,
                            "response_time": elapsed_time,
                            "tokens_used": data["usage"]["total_tokens"],
                            "model_version": data["model"]
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "response_time": elapsed_time
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_claude_35_sonnet(self) -> Dict[str, Any]:
        """Claude 3.5 Sonnet 테스트"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-3-5-sonnet-20241022",  # 최신 버전
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "안녕하세요! Claude 3.5 Sonnet 테스트입니다. 간단히 인사해주세요."}
            ],
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    elapsed_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data["content"][0]["text"]
                        
                        return {
                            "success": True,
                            "response": content,
                            "response_time": elapsed_time,
                            "model_version": data["model"],
                            "tokens_used": data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "response_time": elapsed_time
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_perplexity_sonar(self) -> Dict[str, Any]:
        """Perplexity Sonar 테스트"""
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar",  # 최신 웹 검색 모델
            "messages": [
                {"role": "user", "content": "2025년 최신 AI 트렌드를 간단히 알려주세요."}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    elapsed_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        citations = data.get("citations", [])
                        
                        return {
                            "success": True,
                            "response": content,
                            "response_time": elapsed_time,
                            "citations": citations,
                            "has_realtime_data": True,
                            "model_version": data.get("model", "unknown")
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "response_time": elapsed_time
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_clova_x(self) -> Dict[str, Any]:
        """네이버 Clova X 테스트 (추후 구현)"""
        api_key = os.getenv("CLOVAX_API_KEY")
        if not api_key:
            return {
                "success": False, 
                "error": "API 키 설정 안됨 - 추후 네이버 클로바 스튜디오에서 발급 필요",
                "note": "HyperCLOVA X API는 네이버 클로바 스튜디오에서 신청 후 사용 가능"
            }
        
        # TODO: 네이버 Clova X API 연동 구현
        return {
            "success": False,
            "error": "Clova X API 연동 코드 미구현 - 추후 개발 예정",
            "todo": "네이버 클로바 스튜디오 API 문서 참고하여 구현"
        }
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """전체 AI 모델 종합 테스트"""
        print("🚀 HEAL7 최신 AI 모델 연동 테스트 (2025)")
        print("=" * 60)
        
        # 1. API 키 확인
        print("\n1️⃣ API 키 설정 확인")
        key_status = await self.check_api_keys()
        
        # 2. 개별 모델 테스트
        print("\n2️⃣ 모델별 연결 테스트")
        
        # Gemini 2.0 Flash 테스트
        print(f"\n🧪 Gemini 2.0 Flash 테스트...")
        gemini_result = await self.test_gemini_2_flash()
        self.test_results["gemini-2.0-flash"] = gemini_result
        
        if gemini_result["success"]:
            print(f"   ✅ 성공 ({gemini_result['response_time']:.2f}초)")
            print(f"   💬 응답: {gemini_result['response'][:50]}...")
        else:
            print(f"   ❌ 실패: {gemini_result['error']}")
        
        # GPT-4o 테스트
        print(f"\n🧪 GPT-4o 테스트...")
        gpt4o_result = await self.test_gpt_4o("gpt-4o")
        self.test_results["gpt-4o"] = gpt4o_result
        
        if gpt4o_result["success"]:
            print(f"   ✅ 성공 ({gpt4o_result['response_time']:.2f}초)")
            print(f"   💬 응답: {gpt4o_result['response'][:50]}...")
            print(f"   🔢 토큰: {gpt4o_result['tokens_used']}")
        else:
            print(f"   ❌ 실패: {gpt4o_result['error']}")
        
        # GPT-4o Mini 테스트
        print(f"\n🧪 GPT-4o Mini 테스트...")
        gpt4o_mini_result = await self.test_gpt_4o("gpt-4o-mini")
        self.test_results["gpt-4o-mini"] = gpt4o_mini_result
        
        if gpt4o_mini_result["success"]:
            print(f"   ✅ 성공 ({gpt4o_mini_result['response_time']:.2f}초)")
            print(f"   💬 응답: {gpt4o_mini_result['response'][:50]}...")
        else:
            print(f"   ❌ 실패: {gpt4o_mini_result['error']}")
        
        # Claude 3.5 Sonnet 테스트
        print(f"\n🧪 Claude 3.5 Sonnet 테스트...")
        claude_result = await self.test_claude_35_sonnet()
        self.test_results["claude-3.5-sonnet"] = claude_result
        
        if claude_result["success"]:
            print(f"   ✅ 성공 ({claude_result['response_time']:.2f}초)")
            print(f"   💬 응답: {claude_result['response'][:50]}...")
        else:
            print(f"   ❌ 실패: {claude_result['error']}")
        
        # Perplexity 테스트
        print(f"\n🧪 Perplexity Sonar 테스트...")
        perplexity_result = await self.test_perplexity_sonar()
        self.test_results["perplexity-sonar"] = perplexity_result
        
        if perplexity_result["success"]:
            print(f"   ✅ 성공 ({perplexity_result['response_time']:.2f}초)")
            print(f"   💬 응답: {perplexity_result['response'][:50]}...")
            print(f"   🔗 실시간 데이터: {perplexity_result['has_realtime_data']}")
        else:
            print(f"   ❌ 실패: {perplexity_result['error']}")
        
        # Clova X 테스트
        print(f"\n🧪 네이버 Clova X 테스트...")
        clova_result = await self.test_clova_x()
        self.test_results["clova-x"] = clova_result
        
        if clova_result["success"]:
            print(f"   ✅ 성공")
        else:
            print(f"   ⏭️ 스킵: {clova_result['error']}")
        
        # 3. 결과 요약
        print(f"\n3️⃣ 테스트 결과 요약")
        self.print_summary()
        
        # 4. 권장사항
        print(f"\n4️⃣ 권장사항")
        recommendations = self.generate_recommendations()
        for rec in recommendations:
            print(f"💡 {rec}")
        
        # 5. 리포트 저장
        report = {
            "timestamp": datetime.now().isoformat(),
            "api_key_status": key_status,
            "test_results": self.test_results,
            "recommendations": recommendations,
            "summary": self.get_summary_stats()
        }
        
        report_path = f"/home/ubuntu/logs/ai_model_test_2025_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 상세 리포트 저장: {report_path}")
        
        return report
    
    def print_summary(self):
        """테스트 결과 요약 출력"""
        print(f"{'모델':<20} {'상태':<8} {'응답시간':<10} {'특징'}")
        print("-" * 60)
        
        for model_id, result in self.test_results.items():
            model_name = self.models[model_id]["name"]
            
            if result["success"]:
                status = "✅ 정상"
                response_time = f"{result.get('response_time', 0):.2f}초"
                
                # 특징 표시
                features = []
                if model_id == "gemini-2.0-flash":
                    features.append("무료")
                if model_id == "gpt-4o-mini":
                    features.append("저비용")
                if model_id == "perplexity-sonar" and result.get("has_realtime_data"):
                    features.append("실시간")
                if model_id == "claude-3.5-sonnet":
                    features.append("정확성")
                
                feature_str = ", ".join(features) if features else "일반"
            else:
                status = "❌ 실패"
                response_time = "N/A"
                feature_str = "오류"
            
            print(f"{model_name:<20} {status:<8} {response_time:<10} {feature_str}")
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """요약 통계"""
        total_models = len(self.test_results)
        successful_models = sum(1 for result in self.test_results.values() if result["success"])
        
        avg_response_time = 0
        if successful_models > 0:
            total_time = sum(result.get("response_time", 0) for result in self.test_results.values() if result["success"])
            avg_response_time = total_time / successful_models
        
        return {
            "total_models": total_models,
            "successful_models": successful_models,
            "success_rate": (successful_models / total_models) * 100,
            "avg_response_time": avg_response_time
        }
    
    def generate_recommendations(self) -> List[str]:
        """권장사항 생성"""
        recommendations = []
        
        successful_models = [model_id for model_id, result in self.test_results.items() if result["success"]]
        
        if not successful_models:
            recommendations.append("❗ 사용 가능한 AI 모델이 없습니다. API 키 설정을 확인하세요.")
            return recommendations
        
        # Gemini 2.0 Flash 우선 권장
        if "gemini-2.0-flash" in successful_models:
            recommendations.append("🆓 Gemini 2.0 Flash는 무료이므로 1순위로 사용을 권장합니다.")
        else:
            recommendations.append("💰 Gemini 2.0 Flash API 키를 설정하면 무료로 AI 서비스를 이용할 수 있습니다.")
        
        # 비용 효율성
        if "gpt-4o-mini" in successful_models:
            recommendations.append("💰 GPT-4o Mini는 매우 저렴하므로 대용량 작업에 적합합니다.")
        
        # 실시간 데이터
        if "perplexity-sonar" in successful_models:
            recommendations.append("🔍 Perplexity는 실시간 웹 검색이 가능하므로 리서치 작업에 최적입니다.")
        
        # 폴백 순서 권장
        if len(successful_models) >= 2:
            # 무료 모델 우선, 그 다음 저비용 모델 순으로 정렬
            priority_order = []
            
            if "gemini-2.0-flash" in successful_models:
                priority_order.append("gemini-2.0-flash")
            if "gpt-4o-mini" in successful_models:
                priority_order.append("gpt-4o-mini")
            if "claude-3.5-sonnet" in successful_models:
                priority_order.append("claude-3.5-sonnet")
            if "gpt-4o" in successful_models:
                priority_order.append("gpt-4o")
            if "perplexity-sonar" in successful_models:
                priority_order.append("perplexity-sonar")
            
            model_names = [self.models[mid]["name"] for mid in priority_order]
            recommendations.append(f"🔄 권장 폴백 순서: {' → '.join(model_names)}")
        
        # Clova X 추후 연동
        if "clova-x" not in successful_models:
            recommendations.append("🇰🇷 네이버 Clova X 연동 시 한국어 성능을 더욱 향상시킬 수 있습니다.")
        
        return recommendations

async def main():
    """메인 함수"""
    connector = AIModelConnector2025()
    await connector.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())