#!/usr/bin/env python3
"""
HEAL7 큐브 운영 자동화 도구
큐브 시작/정지, 헬스체크, 성능 모니터링 등 통합 운영

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-26
"""

import asyncio
import aiohttp
import json
import subprocess
import time
import psutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse
import sys

class HEAL7CubeOperations:
    """HEAL7 큐브 시스템 운영 도구"""
    
    def __init__(self, backend_path: str = "/home/ubuntu/heal7-project/backend"):
        self.backend_path = Path(backend_path)
        self.cubes_path = self.backend_path / "cubes"
        self.registry_path = self.cubes_path / "interfaces" / "cube_registry.json"
        
        # 큐브 레지스트리 로드
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                self.cube_registry = json.load(f)
        else:
            print("⚠️ 큐브 레지스트리를 찾을 수 없습니다.")
            self.cube_registry = {"cubes": {}}
    
    async def health_check_all(self, timeout: int = 5) -> Dict[str, Any]:
        """모든 큐브 헬스체크"""
        print("🏥 HEAL7 큐브 헬스체크 시작...")
        
        health_results = {
            "timestamp": datetime.now().isoformat(),
            "total_cubes": len(self.cube_registry["cubes"]),
            "healthy_cubes": 0,
            "unhealthy_cubes": 0,
            "cube_status": {},
            "overall_status": "UNKNOWN"
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            tasks = []
            
            for cube_name, cube_info in self.cube_registry["cubes"].items():
                health_url = cube_info["health_url"]
                task = self._check_cube_health(session, cube_name, health_url, cube_info)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, dict):
                    cube_name = result["cube_name"]
                    health_results["cube_status"][cube_name] = result
                    
                    if result["status"] == "HEALTHY":
                        health_results["healthy_cubes"] += 1
                    else:
                        health_results["unhealthy_cubes"] += 1
        
        # 전체 상태 결정
        if health_results["unhealthy_cubes"] == 0:
            health_results["overall_status"] = "ALL_HEALTHY"
        elif health_results["healthy_cubes"] > health_results["unhealthy_cubes"]:
            health_results["overall_status"] = "MOSTLY_HEALTHY"
        else:
            health_results["overall_status"] = "SYSTEM_DEGRADED"
        
        # 결과 출력
        self._print_health_summary(health_results)
        
        return health_results
    
    async def _check_cube_health(self, session: aiohttp.ClientSession, 
                                cube_name: str, health_url: str, 
                                cube_info: Dict) -> Dict[str, Any]:
        """개별 큐브 헬스체크"""
        try:
            start_time = time.time()
            
            async with session.get(health_url) as response:
                response_time = (time.time() - start_time) * 1000  # ms
                
                if response.status == 200:
                    data = await response.json()
                    return {
                        "cube_name": cube_name,
                        "status": "HEALTHY",
                        "response_time_ms": round(response_time, 2),
                        "color": cube_info["color"],
                        "type": cube_info["type"],
                        "port": cube_info["port"],
                        "details": data
                    }
                else:
                    return {
                        "cube_name": cube_name,
                        "status": "UNHEALTHY",
                        "response_time_ms": round(response_time, 2),
                        "color": cube_info["color"],
                        "error": f"HTTP {response.status}"
                    }
                    
        except Exception as e:
            return {
                "cube_name": cube_name,
                "status": "UNREACHABLE",
                "response_time_ms": 0,
                "color": cube_info["color"],
                "error": str(e)
            }
    
    def _print_health_summary(self, health_results: Dict[str, Any]):
        """헬스체크 결과 요약 출력"""
        print(f"\\n🏥 HEAL7 큐브 헬스체크 결과 ({health_results['timestamp']})")
        print("=" * 80)
        
        # 전체 상태
        status_emoji = {
            "ALL_HEALTHY": "✅",
            "MOSTLY_HEALTHY": "⚠️",
            "SYSTEM_DEGRADED": "❌",
            "UNKNOWN": "❓"
        }
        
        overall_emoji = status_emoji.get(health_results["overall_status"], "❓")
        print(f"{overall_emoji} 전체 상태: {health_results['overall_status']}")
        print(f"📊 건강한 큐브: {health_results['healthy_cubes']}/{health_results['total_cubes']}")
        
        # 큐브별 상세 상태
        print(f"\\n{'큐브명':<25} {'상태':<12} {'응답시간':<10} {'색상':<8} {'타입'}")
        print("-" * 80)
        
        for cube_name, status in health_results["cube_status"].items():
            status_str = status["status"]
            response_time = f"{status['response_time_ms']:.1f}ms"
            color = status["color"]
            cube_type = status.get("type", "unknown")
            
            # 상태별 이모지
            if status_str == "HEALTHY":
                emoji = "✅"
            elif status_str == "UNHEALTHY":
                emoji = "⚠️"
            else:
                emoji = "❌"
            
            print(f"{emoji} {cube_name:<23} {status_str:<10} {response_time:<9} {color:<7} {cube_type}")
    
    def start_all_cubes(self, mode: str = "development"):
        """모든 큐브 시작"""
        print(f"🚀 HEAL7 큐브 시스템 시작 ({mode} 모드)...")
        
        if mode == "development":
            self._start_cubes_development()
        elif mode == "production":
            self._start_cubes_production()
        else:
            print(f"❌ 지원하지 않는 모드: {mode}")
            return False
        
        return True
    
    def _start_cubes_development(self):
        """개발 모드로 큐브 시작"""
        print("🔧 개발 모드로 큐브들을 시작합니다...")
        
        for cube_name, cube_info in self.cube_registry["cubes"].items():
            cube_path = self.cubes_path / cube_name
            main_py = cube_path / "main.py"
            
            if main_py.exists():
                port = cube_info["port"]
                print(f"  ▶️ {cube_name} 시작 (포트 {port})")
                
                try:
                    # 백그라운드에서 실행
                    cmd = f"cd {cube_path} && python main.py > /tmp/{cube_name}.log 2>&1 &"
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"     ✅ 시작됨 - 로그: /tmp/{cube_name}.log")
                    time.sleep(1)  # 순차 시작
                    
                except subprocess.CalledProcessError as e:
                    print(f"     ❌ 시작 실패: {e}")
            else:
                print(f"  ⚠️ {cube_name}: main.py 파일 없음")
    
    def _start_cubes_production(self):
        """프로덕션 모드로 큐브 시작 (systemd 사용)"""
        print("🏭 프로덕션 모드로 큐브들을 시작합니다...")
        
        for cube_name in self.cube_registry["cubes"].keys():
            service_name = f"heal7-{cube_name}"
            
            try:
                # systemd 서비스 시작
                subprocess.run(
                    ["sudo", "systemctl", "start", service_name],
                    check=True, capture_output=True
                )
                print(f"  ✅ {cube_name} 서비스 시작됨")
                
            except subprocess.CalledProcessError:
                print(f"  ⚠️ {cube_name}: systemd 서비스 없음 - 수동 시작 필요")
    
    def stop_all_cubes(self, mode: str = "development"):
        """모든 큐브 정지"""
        print(f"🛑 HEAL7 큐브 시스템 정지 ({mode} 모드)...")
        
        if mode == "development":
            self._stop_cubes_development()
        elif mode == "production":
            self._stop_cubes_production()
        else:
            print(f"❌ 지원하지 않는 모드: {mode}")
            return False
        
        return True
    
    def _stop_cubes_development(self):
        """개발 모드 큐브 정지"""
        print("🔧 개발 모드 큐브들을 정지합니다...")
        
        for cube_name, cube_info in self.cube_registry["cubes"].items():
            port = cube_info["port"]
            
            try:
                # 포트를 사용하는 프로세스 찾기
                result = subprocess.run(
                    ["lsof", "-t", f"-i:{port}"],
                    capture_output=True, text=True
                )
                
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\\n')
                    for pid in pids:
                        if pid:
                            subprocess.run(["kill", pid], check=True)
                            print(f"  🛑 {cube_name} (PID {pid}) 정지됨")
                else:
                    print(f"  ℹ️ {cube_name}: 실행 중인 프로세스 없음")
                    
            except subprocess.CalledProcessError:
                print(f"  ⚠️ {cube_name}: 정지 중 오류 발생")
    
    def _stop_cubes_production(self):
        """프로덕션 모드 큐브 정지"""
        print("🏭 프로덕션 모드 큐브들을 정지합니다...")
        
        for cube_name in self.cube_registry["cubes"].keys():
            service_name = f"heal7-{cube_name}"
            
            try:
                subprocess.run(
                    ["sudo", "systemctl", "stop", service_name],
                    check=True, capture_output=True
                )
                print(f"  🛑 {cube_name} 서비스 정지됨")
                
            except subprocess.CalledProcessError:
                print(f"  ⚠️ {cube_name}: systemd 서비스 정지 실패")
    
    def restart_cube(self, cube_name: str, mode: str = "development"):
        """개별 큐브 재시작"""
        print(f"🔄 {cube_name} 큐브 재시작 중...")
        
        if cube_name not in self.cube_registry["cubes"]:
            print(f"❌ 알 수 없는 큐브: {cube_name}")
            return False
        
        cube_info = self.cube_registry["cubes"][cube_name]
        port = cube_info["port"]
        
        # 정지
        try:
            result = subprocess.run(
                ["lsof", "-t", f"-i:{port}"],
                capture_output=True, text=True
            )
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\\n')
                for pid in pids:
                    if pid:
                        subprocess.run(["kill", pid], check=True)
                        print(f"  🛑 기존 프로세스 (PID {pid}) 정지")
        except:
            pass
        
        time.sleep(2)  # 잠시 대기
        
        # 시작
        cube_path = self.cubes_path / cube_name
        main_py = cube_path / "main.py"
        
        if main_py.exists():
            try:
                cmd = f"cd {cube_path} && python main.py > /tmp/{cube_name}.log 2>&1 &"
                subprocess.run(cmd, shell=True, check=True)
                print(f"  ✅ {cube_name} 재시작 완료 (포트 {port})")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"  ❌ 재시작 실패: {e}")
                return False
        else:
            print(f"  ❌ main.py 파일 없음: {main_py}")
            return False
    
    def monitor_performance(self, duration: int = 60):
        """큐브 성능 모니터링"""
        print(f"📊 HEAL7 큐브 성능 모니터링 시작 ({duration}초간)...")
        
        start_time = time.time()
        samples = []
        
        try:
            while time.time() - start_time < duration:
                sample = {
                    "timestamp": datetime.now().isoformat(),
                    "system_metrics": {
                        "cpu_percent": psutil.cpu_percent(interval=1),
                        "memory_percent": psutil.virtual_memory().percent,
                        "disk_usage_percent": psutil.disk_usage('/').percent
                    },
                    "cube_processes": {}
                }
                
                # 큐브별 프로세스 메트릭
                for cube_name, cube_info in self.cube_registry["cubes"].items():
                    port = cube_info["port"]
                    
                    try:
                        # 포트를 사용하는 프로세스 찾기
                        result = subprocess.run(
                            ["lsof", "-t", f"-i:{port}"],
                            capture_output=True, text=True
                        )
                        
                        if result.stdout.strip():
                            pid = int(result.stdout.strip().split('\\n')[0])
                            proc = psutil.Process(pid)
                            
                            sample["cube_processes"][cube_name] = {
                                "pid": pid,
                                "cpu_percent": proc.cpu_percent(),
                                "memory_mb": proc.memory_info().rss / 1024 / 1024,
                                "status": proc.status()
                            }
                    except:
                        sample["cube_processes"][cube_name] = {
                            "status": "NOT_RUNNING"
                        }
                
                samples.append(sample)
                print(f"  📊 샘플 수집... ({len(samples)}/{duration}초)")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\\n⏹️ 모니터링 중단됨")
        
        # 결과 분석 및 출력
        self._analyze_performance_samples(samples)
        
        return samples
    
    def _analyze_performance_samples(self, samples: List[Dict]):
        """성능 샘플 분석"""
        if not samples:
            print("📊 분석할 데이터가 없습니다.")
            return
        
        print(f"\\n📊 성능 분석 결과 ({len(samples)}개 샘플)")
        print("=" * 60)
        
        # 시스템 평균
        cpu_avg = sum(s["system_metrics"]["cpu_percent"] for s in samples) / len(samples)
        mem_avg = sum(s["system_metrics"]["memory_percent"] for s in samples) / len(samples)
        
        print(f"🖥️ 시스템 평균 - CPU: {cpu_avg:.1f}%, 메모리: {mem_avg:.1f}%")
        
        # 큐브별 분석
        print(f"\\n{'큐브명':<25} {'평균 CPU':<10} {'평균 메모리':<12} {'상태'}")
        print("-" * 60)
        
        for cube_name in self.cube_registry["cubes"].keys():
            running_samples = [
                s["cube_processes"].get(cube_name, {})
                for s in samples
                if cube_name in s["cube_processes"] and 
                   s["cube_processes"][cube_name].get("status") != "NOT_RUNNING"
            ]
            
            if running_samples:
                cpu_avg = sum(s.get("cpu_percent", 0) for s in running_samples) / len(running_samples)
                mem_avg = sum(s.get("memory_mb", 0) for s in running_samples) / len(running_samples)
                status = "✅ 실행 중"
            else:
                cpu_avg = 0
                mem_avg = 0
                status = "❌ 중단됨"
            
            print(f"{cube_name:<25} {cpu_avg:.1f}%{'':<6} {mem_avg:.1f}MB{'':<7} {status}")
    
    def backup_cubes(self):
        """큐브 설정 백업"""
        backup_name = f"heal7-cubes-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.tar.gz"
        backup_path = self.backend_path / backup_name
        
        print(f"💾 HEAL7 큐브 백업 중...")
        
        try:
            cmd = [
                "tar", "-czf", str(backup_path),
                "-C", str(self.backend_path),
                "cubes/"
            ]
            
            subprocess.run(cmd, check=True)
            
            # 백업 파일 크기 확인
            size_mb = backup_path.stat().st_size / 1024 / 1024
            
            print(f"✅ 백업 완료: {backup_name} ({size_mb:.1f}MB)")
            print(f"📁 백업 위치: {backup_path}")
            
            return str(backup_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 백업 실패: {e}")
            return None

async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="HEAL7 큐브 운영 도구")
    parser.add_argument("command", choices=[
        "health", "start", "stop", "restart", "monitor", "backup"
    ], help="실행할 명령")
    parser.add_argument("--cube", help="특정 큐브 이름 (restart 명령용)")
    parser.add_argument("--mode", choices=["development", "production"], 
                       default="development", help="실행 모드")
    parser.add_argument("--duration", type=int, default=60, 
                       help="모니터링 시간 (초)")
    
    args = parser.parse_args()
    
    ops = HEAL7CubeOperations()
    
    if args.command == "health":
        await ops.health_check_all()
        
    elif args.command == "start":
        ops.start_all_cubes(args.mode)
        
    elif args.command == "stop":
        ops.stop_all_cubes(args.mode)
        
    elif args.command == "restart":
        if not args.cube:
            print("❌ --cube 옵션이 필요합니다")
            sys.exit(1)
        ops.restart_cube(args.cube, args.mode)
        
    elif args.command == "monitor":
        ops.monitor_performance(args.duration)
        
    elif args.command == "backup":
        ops.backup_cubes()

if __name__ == "__main__":
    asyncio.run(main())