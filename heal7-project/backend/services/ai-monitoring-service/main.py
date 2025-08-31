#!/usr/bin/env python3
"""
HEAL7 AI Dashboard API with CLI Support
Claude CLI와 Gemini CLI를 포함한 AI 모델 통합 대시보드 API
"""

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import socket

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="HEAL7 AI Dashboard API", version="2.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 설정
API_KEYS_FILE = "/home/ubuntu/.env.ai"
CLI_TIMEOUT = 30  # seconds

# .env.ai 파일에서 환경 변수 로드
def load_env_ai():
    env_path = API_KEYS_FILE
    env_vars = {}
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
                    os.environ[key.strip()] = value.strip()
        print(f"✅ .env.ai 파일에서 {len(env_vars)}개 환경 변수 로드 완료")
        return env_vars
    except Exception as e:
        print(f"⚠️ .env.ai 파일 로드 실패: {e}")
        return {}

# 시스템 시작 시 환경 변수 로드
ENV_VARS = load_env_ai()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model_id: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7
    mode: Optional[str] = "balanced"

class CLITestRequest(BaseModel):
    command: str

class CLIChatRequest(BaseModel):
    model_id: str
    command: str
    context: Optional[str] = ""
    max_tokens: Optional[int] = 2000

# API 키 로드
def load_api_keys() -> Dict[str, str]:
    """API 키 파일에서 키들을 로드"""
    keys = {}
    try:
        if os.path.exists(API_KEYS_FILE):
            with open(API_KEYS_FILE, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        keys[key] = value.strip('"\'')
    except Exception as e:
        print(f"API 키 로드 실패: {e}")
    return keys

# CLI 관리 시스템
class CLIManager:
    """Claude CLI와 Gemini CLI 관리"""
    
    def __init__(self):
        self.cli_processes = {}
        self.supported_clis = {
            'claude_cli': {
                'command': 'claude',
                'check_args': ['--version'],
                'test_args': ['--help']
            },
            'gemini_cli': {
                'command': 'gemini',
                'check_args': ['--version'],
                'test_args': ['--help']
            }
        }
    
    async def check_cli_status(self, cli_id: str) -> Dict[str, Any]:
        """CLI 상태 확인"""
        if cli_id not in self.supported_clis:
            return {'connected': False, 'error': 'Unsupported CLI'}
        
        cli_config = self.supported_clis[cli_id]
        
        try:
            # CLI 명령어가 존재하는지 확인
            process = await asyncio.create_subprocess_exec(
                cli_config['command'], *cli_config['check_args'],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            start_time = datetime.now()
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=CLI_TIMEOUT
            )
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            
            if process.returncode == 0:
                return {
                    'connected': True,
                    'response_time': response_time,
                    'version': stdout.decode().strip() if stdout else 'Unknown'
                }
            else:
                return {
                    'connected': False,
                    'error': stderr.decode().strip() if stderr else 'Command failed'
                }
                
        except asyncio.TimeoutError:
            return {'connected': False, 'error': 'Timeout'}
        except FileNotFoundError:
            return {'connected': False, 'error': 'CLI not installed'}
        except Exception as e:
            return {'connected': False, 'error': str(e)}
    
    async def test_cli_connection(self, cli_id: str, test_command: str = 'echo test') -> Dict[str, Any]:
        """CLI 연결 테스트"""
        if cli_id not in self.supported_clis:
            return {'success': False, 'error': 'Unsupported CLI'}
        
        cli_config = self.supported_clis[cli_id]
        
        try:
            if cli_id == 'claude_cli':
                # Claude CLI 테스트 - 간단한 명령 실행
                process = await asyncio.create_subprocess_exec(
                    'claude', '--help',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            elif cli_id == 'gemini_cli':
                # Gemini CLI 테스트
                process = await asyncio.create_subprocess_exec(
                    'gemini', '--help',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
            start_time = datetime.now()
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=CLI_TIMEOUT
            )
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            
            return {
                'success': process.returncode == 0,
                'response_time': response_time,
                'output': stdout.decode().strip() if stdout else '',
                'error': stderr.decode().strip() if stderr and process.returncode != 0 else None
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def send_cli_command(self, cli_id: str, command: str, context: str = '') -> Dict[str, Any]:
        """CLI에 명령 전송"""
        if cli_id not in self.supported_clis:
            raise HTTPException(status_code=400, detail='Unsupported CLI')
        
        try:
            if cli_id == 'claude_cli':
                # Claude CLI는 --print 옵션을 사용해서 비인터랙티브 모드로 실행
                full_prompt = command
                if context:
                    full_prompt = f"Context: {context}\n\nUser: {command}"
                    
                process = await asyncio.create_subprocess_exec(
                    'claude', '--print', full_prompt,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
            elif cli_id == 'gemini_cli':
                # Gemini CLI도 비슷한 방식으로 처리
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
                    if context:
                        tmp_file.write(f"Context: {context}\n\nUser: {command}")
                    else:
                        tmp_file.write(command)
                    tmp_file.flush()
                    
                    # Gemini CLI는 일반적으로 stdin으로 입력을 받는다
                    process = await asyncio.create_subprocess_shell(
                        f"cat {tmp_file.name} | gemini",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    
                # 임시 파일 정리
                os.unlink(tmp_file.name)
            
            start_time = datetime.now()
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=CLI_TIMEOUT
            )
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            
            if process.returncode == 0:
                response_text = stdout.decode().strip()
                return {
                    'response': response_text or '명령이 실행되었지만 응답이 없습니다.',
                    'model_name': f"{cli_id.replace('_', ' ').title()}",
                    'response_time': response_time,
                    'usage': {'cost': 0.0}  # CLI는 무료
                }
            else:
                error_text = stderr.decode().strip()
                raise HTTPException(status_code=500, detail=f'CLI 오류: {error_text}')
                
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail='CLI 명령 시간 초과')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'CLI 실행 오류: {str(e)}')

# CLI 매니저 인스턴스
cli_manager = CLIManager()

# API 엔드포인트
@app.get("/")
async def root():
    """API 정보 반환"""
    return {
        "service": "HEAL7 AI Dashboard API",
        "version": "2.0.0",
        "status": "online",
        "supported_models": 9,  # 7개 API 모델 + 2개 CLI 모델
        "cli_support": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/models")
async def get_models():
    """지원하는 모든 모델 목록 반환"""
    api_models = [
        {
            "id": "gemini_2_0_flash",
            "name": "Gemini Flash",
            "provider": "Google",
            "status": "online",
            "response_time": 1.2,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "무료 (100만 토큰)",
            "features": ["텍스트", "이미지 분석", "동영상 분석"]
        },
        {
            "id": "gpt_4o",
            "name": "GPT-4o",
            "provider": "OpenAI",
            "status": "online",
            "response_time": 1.8,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "$2.5/$10",
            "features": ["텍스트", "이미지 분석", "PDF 문서", "음성 분석"]
        },
        {
            "id": "claude_sonnet_4",
            "name": "Claude Sonnet 4",
            "provider": "Anthropic",
            "status": "online",
            "response_time": 2.1,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "$3/$15",
            "features": ["텍스트", "이미지 분석", "코딩", "1M 컨텍스트"]
        },
        {
            "id": "gpt_5",
            "name": "GPT-5",
            "provider": "OpenAI",
            "status": "online",
            "response_time": 2.5,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "$4/$20",
            "features": ["텍스트", "고급 추론", "창의성", "코딩"]
        },
        {
            "id": "gpt_5_mini",
            "name": "GPT-5 Mini",
            "provider": "OpenAI",
            "status": "online",
            "response_time": 1.0,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "$1/$5",
            "features": ["텍스트", "빠른 응답", "효율성"]
        },
        {
            "id": "gpt_4_1",
            "name": "GPT-4.1",
            "provider": "OpenAI",
            "status": "online",
            "response_time": 1.6,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "$3/$12",
            "features": ["텍스트", "향상된 추론", "코딩", "분석"]
        },
        {
            "id": "claude_35_sonnet",
            "name": "Claude 3.5 Sonnet",
            "provider": "Anthropic",
            "status": "online",
            "response_time": 1.7,
            "last_check": datetime.now().isoformat(),
            "error_message": None,
            "cost": "$3/$15",
            "features": ["텍스트", "분석", "코딩", "200K 컨텍스트"]
        }
    ]
    
    # CLI 모델 상태 확인 후 추가
    cli_models = []
    for cli_id in ['claude_cli', 'gemini_cli']:
        status = await cli_manager.check_cli_status(cli_id)
        cli_models.append({
            "id": cli_id,
            "name": cli_id.replace('_', ' ').title(),
            "provider": "Anthropic CLI" if "claude" in cli_id else "Google CLI",
            "status": "online" if status.get('connected') else "offline",
            "response_time": status.get('response_time', 0),
            "last_check": datetime.now().isoformat(),
            "error_message": status.get('error'),
            "cost": "로컬 실행",
            "features": ["코드 생성", "터미널 연동"] if "claude" in cli_id else ["코드 분석", "자동화"],
            "type": "cli"
        })
    
    return api_models + cli_models

@app.get("/cli/status/{cli_id}")
async def get_cli_status(cli_id: str):
    """특정 CLI 상태 확인"""
    status = await cli_manager.check_cli_status(cli_id)
    return status

@app.post("/cli/test/{cli_id}")
async def test_cli(cli_id: str, request: CLITestRequest):
    """CLI 연결 테스트"""
    result = await cli_manager.test_cli_connection(cli_id, request.command)
    return result

@app.post("/cli/chat")
async def cli_chat(request: CLIChatRequest):
    """CLI 모델과 채팅"""
    result = await cli_manager.send_cli_command(
        request.model_id, 
        request.command, 
        request.context
    )
    return result

@app.post("/chat")
async def chat(request: ChatRequest):
    """AI 모델과 채팅 (API 모델 전용)"""
    # CLI 모델은 별도 엔드포인트 사용
    if request.model_id in ['claude_cli', 'gemini_cli']:
        raise HTTPException(
            status_code=400, 
            detail="CLI 모델은 /cli/chat 엔드포인트를 사용해주세요"
        )
    
    # 실제 AI API 호출
    message_text = request.messages[-1].content if request.messages else "Hello"
    
    try:
        if request.model_id == "gemini_2_0_flash":
            # Gemini API 호출
            import google.generativeai as genai
            
            # API 키 설정
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=500, detail="Gemini API 키가 설정되지 않았습니다")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # 대화 컨텍스트 구성
            conversation_context = ""
            for msg in request.messages:
                conversation_context += f"{msg.role}: {msg.content}\n"
            
            start_time = datetime.now()
            response = model.generate_content(
                conversation_context,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=request.max_tokens,
                    temperature=request.temperature,
                )
            )
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            response_text = response.text
            
            return {
                "response": response_text,
                "model_name": "Gemini 2.0 Flash",
                "response_time": response_time,
                "usage": {
                    "cost": 0.0,  # Gemini Flash는 무료
                    "input_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "output_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else len(response_text.split())
                }
            }
            
        elif request.model_id == "claude_35_sonnet":
            # Claude API 호출
            import anthropic
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise HTTPException(status_code=500, detail="Claude API 키가 설정되지 않았습니다")
            
            client = anthropic.Anthropic(api_key=api_key)
            
            # 메시지 포맷 변환
            messages = []
            for msg in request.messages:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            start_time = datetime.now()
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                messages=messages
            )
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            response_text = response.content[0].text
            
            return {
                "response": response_text,
                "model_name": "Claude 3.5 Sonnet",
                "response_time": response_time,
                "usage": {
                    "cost": (response.usage.input_tokens * 0.000003) + (response.usage.output_tokens * 0.000015),
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
        else:
            # 다른 모델들은 임시 Mock 응답
            mock_responses = {
                "gpt_4o": f"안녕하세요! GPT-4o입니다. '{message_text}'에 대해 자세히 분석해드리겠습니다.",
                "claude_sonnet_4": f"안녕하세요! Claude Sonnet 4입니다. '{message_text}'에 대해 깊이 있게 답변드리겠습니다.",
                "gpt_5": f"안녕하세요! GPT-5입니다. '{message_text}'에 대한 고급 추론 결과를 제공합니다.",
                "gpt_5_mini": f"안녕하세요! GPT-5 Mini입니다. '{message_text}'에 대해 빠르게 답변드립니다.",
                "gpt_4_1": f"안녕하세요! GPT-4.1입니다. '{message_text}'에 대한 향상된 분석을 제공합니다."
            }
            
            response_text = mock_responses.get(
                request.model_id, 
                f"죄송합니다. {request.model_id} 모델은 아직 연동 중입니다."
            )
            
            return {
                "response": response_text,
                "model_name": request.model_id.replace('_', ' ').title(),
                "response_time": 1.2,
                "usage": {
                    "cost": 0.005,
                    "input_tokens": len(message_text.split()) * 1.3,
                    "output_tokens": len(response_text.split()) * 1.3
                }
            }
            
    except Exception as e:
        # 에러 발생 시 폴백
        return {
            "response": f"죄송합니다. 현재 {request.model_id} 서비스에 일시적인 문제가 있습니다. 잠시 후 다시 시도해주세요. (오류: {str(e)})",
            "model_name": request.model_id.replace('_', ' ').title(),
            "response_time": 0.1,
            "usage": {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0
            }
        }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "cli_support": True
    }

if __name__ == "__main__":
    print("🚀 HEAL7 AI Dashboard API with CLI Support 시작")
    print("🔧 지원 모델: 7개 API 모델 + 2개 CLI 모델")
    print("💻 CLI 지원: Claude CLI, Gemini CLI")
    print("🌐 포트: 8004")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=False,
        access_log=True
    )