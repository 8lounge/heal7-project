#!/usr/bin/env python3
"""
응답 처리 유틸리티
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi.responses import JSONResponse

class ResponseUtils:
    """응답 처리 유틸리티 클래스"""
    
    @staticmethod
    def success_response(data: Any, message: str = "성공", status_code: int = 200) -> JSONResponse:
        """성공 응답 생성"""
        response_data = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(content=response_data, status_code=status_code)
    
    @staticmethod
    def error_response(error: str, details: Dict[str, Any] = None, status_code: int = 400) -> JSONResponse:
        """오류 응답 생성"""
        response_data = {
            "success": False,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            response_data["details"] = details
        
        return JSONResponse(content=response_data, status_code=status_code)
    
    @staticmethod
    def ocr_success_response(text: str, metadata: Dict[str, Any] = None) -> JSONResponse:
        """OCR 성공 응답"""
        data = {
            "text": text,
            "text_length": len(text),
            "service": "naver_ocr"
        }
        
        if metadata:
            data.update(metadata)
        
        return ResponseUtils.success_response(data, "OCR 처리 완료")
    
    @staticmethod
    def ai_conversion_success_response(result: str, model: str, conversion_type: str, usage: Dict[str, Any] = None) -> JSONResponse:
        """AI 변환 성공 응답"""
        data = {
            "result": result,
            "result_length": len(result),
            "model": model,
            "conversion_type": conversion_type,
            "service": "ai_conversion"
        }
        
        if usage:
            data["usage"] = usage
        
        return ResponseUtils.success_response(data, "AI 변환 완료")
    
    @staticmethod
    def multi_page_success_response(results: List[Dict[str, Any]], total_pages: int) -> JSONResponse:
        """다중 페이지 처리 성공 응답"""
        combined_text = "\n\n".join([r.get("text", "") for r in results if r.get("text")])
        
        data = {
            "combined_text": combined_text,
            "total_pages": total_pages,
            "processed_pages": len(results),
            "page_results": results,
            "service": "multi_page_ocr"
        }
        
        return ResponseUtils.success_response(data, f"{total_pages}페이지 처리 완료")
    
    @staticmethod
    def validation_error_response(validation_result: Dict[str, Any]) -> JSONResponse:
        """유효성 검사 오류 응답"""
        error_message = validation_result.get('error', '유효성 검사 실패')
        details = {k: v for k, v in validation_result.items() if k != 'error'}
        
        return ResponseUtils.error_response(error_message, details, 400)
    
    @staticmethod
    def service_error_response(service_name: str, error: str, status_code: int = 500) -> JSONResponse:
        """서비스 오류 응답"""
        return ResponseUtils.error_response(
            f"{service_name} 서비스 오류: {error}",
            {"service": service_name},
            status_code
        )
    
    @staticmethod
    def api_key_error_response(service_name: str) -> JSONResponse:
        """API 키 오류 응답"""
        return ResponseUtils.error_response(
            f"{service_name} API 키가 설정되지 않았습니다",
            {"service": service_name, "required": "api_key"},
            401
        )
    
    @staticmethod
    def timeout_error_response(service_name: str, timeout_seconds: int) -> JSONResponse:
        """타임아웃 오류 응답"""
        return ResponseUtils.error_response(
            f"{service_name} 처리 시간 초과 ({timeout_seconds}초)",
            {"service": service_name, "timeout": timeout_seconds},
            408
        )
    
    @staticmethod
    def health_check_response(service_name: str, status: str, details: Dict[str, Any] = None) -> JSONResponse:
        """헬스체크 응답"""
        data = {
            "service": service_name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            data.update(details)
        
        status_code = 200 if status == "healthy" else 503
        
        return JSONResponse(content=data, status_code=status_code)
    
    @staticmethod
    def model_list_response(models: List[str], details: Dict[str, Any] = None) -> JSONResponse:
        """모델 목록 응답"""
        data = {
            "models": models,
            "total_models": len(models)
        }
        
        if details:
            data["details"] = details
        
        return ResponseUtils.success_response(data, "모델 목록 조회 완료")
    
    @staticmethod
    def file_upload_success_response(filename: str, file_info: Dict[str, Any]) -> JSONResponse:
        """파일 업로드 성공 응답"""
        data = {
            "filename": filename,
            "file_info": file_info,
            "service": "file_upload"
        }
        
        return ResponseUtils.success_response(data, "파일 업로드 완료")
    
    @staticmethod
    def convert_service_result_to_response(service_result: Dict[str, Any], service_name: str) -> JSONResponse:
        """서비스 결과를 HTTP 응답으로 변환"""
        if service_result.get('success', False):
            # 성공 응답
            if service_name == "ocr":
                return ResponseUtils.ocr_success_response(
                    service_result.get('text', ''),
                    {k: v for k, v in service_result.items() if k not in ['success', 'text']}
                )
            elif service_name == "ai_conversion":
                return ResponseUtils.ai_conversion_success_response(
                    service_result.get('result', ''),
                    service_result.get('model', ''),
                    service_result.get('conversion_type', ''),
                    service_result.get('usage', {})
                )
            else:
                return ResponseUtils.success_response(service_result.get('data', service_result))
        else:
            # 오류 응답
            error_message = service_result.get('error', f'{service_name} 처리 실패')
            
            # 특정 오류 타입에 따른 상태 코드 설정
            if 'API 키' in error_message or 'api_key' in error_message.lower():
                status_code = 401
            elif '시간 초과' in error_message or 'timeout' in error_message.lower():
                status_code = 408
            elif '지원하지 않는' in error_message:
                status_code = 400
            else:
                status_code = 500
            
            return ResponseUtils.error_response(error_message, service_result, status_code)
    
    @staticmethod
    def add_cors_headers(response: JSONResponse) -> JSONResponse:
        """CORS 헤더 추가"""
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response