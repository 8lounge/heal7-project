#!/usr/bin/env python3
"""
Paperwork AI 메인 라우터
레고블럭 구조로 설계된 모듈화 서비스 조합

- 네이버 OCR 서비스 (1순위 핵심)
- 7개 AI 모델 통합 서비스
- HWP/HWPX 파일 지원
- 개별 기능별 테스트 가능
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

# Paperwork 서비스 모듈 임포트
from paperwork_services.ocr_service import ocr_service, process_ocr, process_multi_page_ocr
from paperwork_services.ai_service import ai_service, process_ai_conversion, get_ai_models
from paperwork_services.config import settings
from paperwork_services.api_config import APIConfig
from paperwork_services.utils import FileUtils, ValidationUtils, ResponseUtils

# 로깅 설정
logger = logging.getLogger(__name__)

# 라우터 생성 (prefix 제거 - nginx에서 /api/로 이미 프록시함)
router = APIRouter(tags=["Paperwork"])

# 요청 모델 정의
class DocumentConversionRequest(BaseModel):
    """문서 AI 변환 요청"""
    text: str
    conversion_type: str  # 'md', 'text_table', 'summary'
    ai_model: str  # claude_sonnet4, gpt5, gpt5_mini, gpt4o, gpt41, gemini_flash2
    options: Optional[Dict[str, Any]] = {}

class OCRRequest(BaseModel):
    """OCR 처리 요청"""
    image_data: str  # Base64 encoded image
    lang: str = 'ko'
    enable_table: bool = True

class MultiPageOCRRequest(BaseModel):
    """다중 페이지 OCR 요청"""
    image_list: List[str]  # Base64 encoded images
    lang: str = 'ko'
    enable_table: bool = True


# 핵심 엔드포인트: AI 문서 변환
@router.post("/ai-edit")
async def convert_document(request: DocumentConversionRequest):
    """
    AI 모델을 사용한 문서 변환
    - 7개 AI 모델 지원: Claude Sonnet 4, GPT-5, GPT-5 Mini, GPT-4o, GPT-4.1, Gemini Flash 2.0
    - 변환 타입: md, text_table, summary
    """
    try:
        # 입력 유효성 검사
        text_validation = ValidationUtils.validate_text_input(request.text)
        if not text_validation['valid']:
            return ResponseUtils.validation_error_response(text_validation)
        
        conversion_validation = ValidationUtils.validate_conversion_type(request.conversion_type)
        if not conversion_validation['valid']:
            return ResponseUtils.validation_error_response(conversion_validation)
        
        model_validation = ValidationUtils.validate_ai_model(request.ai_model)
        if not model_validation['valid']:
            return ResponseUtils.validation_error_response(model_validation)
        
        # AI 변환 처리
        result = await process_ai_conversion(
            request.ai_model, 
            request.text, 
            request.conversion_type, 
            request.options
        )
        
        # 결과 응답 생성
        return ResponseUtils.convert_service_result_to_response(result, "ai_conversion")
        
    except Exception as e:
        logger.error(f"AI 문서 변환 오류: {e}")
        return ResponseUtils.service_error_response("AI 변환", str(e))


# 핵심 엔드포인트: 네이버 OCR (1순위)
@router.post("/ocr")
async def process_ocr_endpoint(request: OCRRequest):
    """
    네이버 CLOVA OCR API를 사용한 단일 이미지 OCR 처리 (핵심 기능)
    """
    try:
        # 입력 유효성 검사
        base64_validation = ValidationUtils.validate_base64_image(request.image_data)
        if not base64_validation['valid']:
            return ResponseUtils.validation_error_response(base64_validation)
        
        ocr_options = {
            'lang': request.lang,
            'enable_table': request.enable_table
        }
        
        options_validation = ValidationUtils.validate_ocr_options(ocr_options)
        if not options_validation['valid']:
            return ResponseUtils.validation_error_response(options_validation)
        
        # OCR 처리
        result = await process_ocr(request.image_data, ocr_options)
        
        # 결과 응답 생성
        return ResponseUtils.convert_service_result_to_response(result, "ocr")
        
    except Exception as e:
        logger.error(f"OCR 처리 오류: {e}")
        return ResponseUtils.service_error_response("OCR", str(e))


@router.post("/ocr/multi-page")
async def process_multi_page_ocr_endpoint(request: MultiPageOCRRequest):
    """
    다중 페이지 OCR 처리
    """
    try:
        # 입력 유효성 검사
        file_list_validation = ValidationUtils.validate_file_list(request.image_list, settings.max_pages_per_request)
        if not file_list_validation['valid']:
            return ResponseUtils.validation_error_response(file_list_validation)
        
        ocr_options = {
            'lang': request.lang,
            'enable_table': request.enable_table
        }
        
        # 다중 페이지 OCR 처리
        result = await process_multi_page_ocr(request.image_list, ocr_options)
        
        # 결과 응답 생성
        return ResponseUtils.convert_service_result_to_response(result, "multi_page_ocr")
        
    except Exception as e:
        logger.error(f"다중 페이지 OCR 오류: {e}")
        return ResponseUtils.service_error_response("다중 페이지 OCR", str(e))


# 통합 문서 처리 (개선된 전략)
@router.post("/convert-document")
async def convert_document_file(file: UploadFile = File(...)):
    """
    문서 파일을 최적의 방식으로 텍스트 변환
    - PDF, DOCX: 직접 텍스트 추출 (정확)
    - HWP, HWPX: OCR 처리 권장 안내
    - DOC: 변환 필요 안내
    """
    try:
        # 파일 유효성 검사
        if not settings.is_supported_file_type(file.filename):
            return ResponseUtils.error_response(
                f"지원하지 않는 파일 형식: {FileUtils.get_file_extension(file.filename)}",
                {"supported_types": settings.supported_file_types},
                400
            )
        
        # 파일 저장
        temp_file_path = settings.get_temp_file_path(file.filename)
        content = await file.read()
        
        with open(temp_file_path, 'wb') as f:
            f.write(content)
        
        # 파일 크기 및 유효성 검사
        file_validation = FileUtils.validate_file(
            temp_file_path, 
            settings.supported_file_types, 
            settings.max_file_size
        )
        
        if not file_validation['valid']:
            FileUtils.cleanup_temp_file(temp_file_path)
            return ResponseUtils.validation_error_response(file_validation)
        
        # 문서 타입별 최적 처리
        extraction_result = FileUtils.extract_text_from_document(temp_file_path)
        
        # 임시 파일 정리
        FileUtils.cleanup_temp_file(temp_file_path)
        
        # 결과 응답 생성
        response_data = {
            "filename": file.filename,
            "extraction_result": extraction_result,
            "file_info": file_validation,
            "processing_recommendation": {
                "method": extraction_result.get('method'),
                "recommended": extraction_result.get('recommended', False),
                "note": extraction_result.get('note', ''),
                "should_use_ocr": FileUtils.should_use_ocr(temp_file_path)
            }
        }
        
        if extraction_result['success']:
            return ResponseUtils.file_upload_success_response(file.filename, response_data)
        else:
            return ResponseUtils.error_response(extraction_result['error'], response_data, 400)
        
    except Exception as e:
        logger.error(f"문서 변환 오류: {e}")
        return ResponseUtils.service_error_response("문서 변환", str(e))

# 기존 HWP 전용 엔드포인트 (호환성 유지)
@router.post("/convert-hwp")
async def convert_hwp(file: UploadFile = File(...)):
    """
    HWP/HWPX 파일 변환 (레거시 호환성)
    새로운 /convert-document 사용 권장
    """
    # 새로운 통합 엔드포인트로 리다이렉트
    return await convert_document_file(file)


# 개별 기능 테스트 엔드포인트
@router.get("/test/ocr")
async def test_ocr_service():
    """네이버 OCR 서비스 상태 테스트"""
    try:
        health_result = await ocr_service.health_check()
        return ResponseUtils.health_check_response(
            "OCR 서비스", 
            health_result['status'], 
            health_result
        )
    except Exception as e:
        return ResponseUtils.service_error_response("OCR 테스트", str(e))


@router.get("/test/ai/{model_id}")
async def test_ai_model(model_id: str):
    """개별 AI 모델 상태 테스트"""
    try:
        model_info = ai_service.get_model_info(model_id)
        
        if 'error' in model_info:
            return ResponseUtils.error_response(model_info['error'], {}, 400)
        
        status = "healthy" if model_info['configured'] else "not_configured"
        return ResponseUtils.health_check_response(
            f"AI 모델 {model_id}",
            status,
            model_info
        )
    except Exception as e:
        return ResponseUtils.service_error_response(f"AI 모델 {model_id} 테스트", str(e))


# 서비스 정보 엔드포인트
@router.get("/health")
async def health_check():
    """전체 Paperwork 서비스 상태 확인"""
    try:
        # OCR 서비스 상태
        ocr_health = await ocr_service.health_check()
        
        # AI 서비스 상태
        ai_health = await ai_service.health_check()
        
        # API 설정 상태
        api_config_instance = APIConfig()
        api_status = api_config_instance.get_api_status()
        
        # 전체 상태 결정
        overall_status = "healthy" if (
            ocr_health['status'] == 'healthy' and 
            ai_health['status'] == 'healthy'
        ) else "partial"
        
        health_data = {
            "service": settings.service_name,
            "version": settings.version,
            "overall_status": overall_status,
            "ocr_service": ocr_health,
            "ai_service": ai_health,
            "api_config": api_status,
            "settings": settings.to_dict()
        }
        
        return ResponseUtils.health_check_response(
            settings.service_name,
            overall_status,
            health_data
        )
        
    except Exception as e:
        return ResponseUtils.service_error_response("헬스체크", str(e))


@router.get("/models")
async def get_available_models():
    """사용 가능한 AI 모델 목록 및 상세 정보"""
    try:
        models = await get_ai_models()
        model_details = ai_service.get_model_info()
        
        return ResponseUtils.model_list_response(models, model_details)
        
    except Exception as e:
        return ResponseUtils.service_error_response("모델 목록 조회", str(e))


@router.get("/settings")
async def get_service_settings():
    """서비스 설정 정보"""
    try:
        return ResponseUtils.success_response(
            settings.to_dict(),
            "Paperwork 서비스 설정 정보"
        )
    except Exception as e:
        return ResponseUtils.service_error_response("설정 조회", str(e))


# 스크랩 시스템 상태 확인
@router.get("/scraping/status")
async def get_scraping_status():
    """스크랩 시스템 상태 조회"""
    try:
        # 스케줄러 상태 확인
        from services.scheduler_config import scraping_scheduler
        scheduler_status = scraping_scheduler.get_scheduler_status()
        
        # 중복 필터 상태 확인
        from services.duplicate_filter import duplicate_filter
        filter_stats = duplicate_filter.get_filter_statistics()
        
        status_data = {
            "scraping_system": {
                "enabled": True,
                "schedule": "매일 00:00 (자정)",
                "collection_range": "30-100개 per site",
                "duplicate_filtering": True,
                **scheduler_status
            },
            "duplicate_filter": {
                "enabled": True,
                "algorithm": "multi-layer (hash + similarity)",
                **filter_stats
            },
            "last_updated": datetime.now().isoformat()
        }
        
        return ResponseUtils.success_response(
            status_data,
            "스크랩 시스템 상태 조회 완료"
        )
        
    except Exception as e:
        logger.error(f"스크랩 시스템 상태 조회 오류: {e}")
        return ResponseUtils.service_error_response("스크랩 시스템 상태 조회", str(e))

@router.post("/scraping/test-duplicate-filter")
async def test_duplicate_filter():
    """중복 필터링 테스트"""
    try:
        from services.duplicate_filter import duplicate_filter
        
        # 테스트 데이터
        test_records = [
            {
                "title": "2025년 중소기업 지원사업 공고",
                "implementing_agency": "중소벤처기업부",
                "application_period": "2025.01 ~ 2025.31",
                "detail_url": "https://example.com/program1"
            },
            {
                "title": "2025년 중소기업 지원사업 공고",  # 동일 제목
                "implementing_agency": "중소벤처기업부",
                "application_period": "2025.01 ~ 2025.31",
                "detail_url": "https://example.com/program2"
            },
            {
                "title": "스타트업 창업 지원사업 안내",
                "implementing_agency": "기술보증기금",
                "application_period": "2025.01 ~ 2025.30",
                "detail_url": "https://example.com/program3"
            }
        ]
        
        results = []
        for i, record in enumerate(test_records):
            # 이전 레코드들과 중복 검사
            existing_records = test_records[:i]
            duplicate_result = await duplicate_filter.detect_duplicate(record, existing_records)
            
            results.append({
                "record_index": i,
                "title": record["title"],
                "duplicate_detected": duplicate_result.is_duplicate,
                "confidence_score": duplicate_result.confidence_score,
                "duplicate_type": duplicate_result.duplicate_type,
                "details": duplicate_result.similarity_details
            })
        
        return ResponseUtils.success_response(
            {
                "test_results": results,
                "filter_stats": duplicate_filter.get_filter_statistics()
            },
            "중복 필터링 테스트 완료"
        )
        
    except Exception as e:
        logger.error(f"중복 필터링 테스트 오류: {e}")
        return ResponseUtils.service_error_response("중복 필터링 테스트", str(e))

# 서비스 종료 시 정리 작업
@router.on_event("shutdown")  
async def shutdown_event():
    """Paperwork 서비스 종료 시 정리"""
    logger.info("Paperwork 서비스 종료 중...")
    # 임시 파일 정리 등의 작업 수행 가능