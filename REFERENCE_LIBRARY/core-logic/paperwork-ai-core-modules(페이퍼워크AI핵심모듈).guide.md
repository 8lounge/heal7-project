# 🧠 Paperwork AI 핵심 로직 모듈

> **프로젝트**: AI 기반 문서 편집 플랫폼 핵심 비즈니스 로직  
> **버전**: v2.0.0  
> **작성일**: 2025-08-19  
> **목적**: 완전한 구현을 위한 원자 단위 모듈 설계

---

## 🎯 **1. 핵심 비즈니스 로직 개요**

### **1.1 도메인 모델 (Domain Model)**

#### **주요 엔티티 및 관계**
```mermaid
classDiagram
    class User {
        +UUID id
        +String email
        +String name
        +SubscriptionTier tier
        +int apiUsageCount
        +UserPreferences preferences
        +authenticate()
        +updateUsage()
        +checkLimits()
    }
    
    class Document {
        +UUID id
        +UUID userId
        +String filename
        +FileType type
        +int pageCount
        +ProcessingStatus status
        +validate()
        +updateStatus()
        +checkPageLimit()
    }
    
    class OCRResult {
        +UUID id
        +UUID documentId
        +int pageNumber
        +String extractedText
        +float confidence
        +combinePages()
        +validateQuality()
    }
    
    class AIProcessingJob {
        +UUID id
        +UUID documentId
        +AIModel model
        +JobType type
        +String inputText
        +String outputText
        +execute()
        +retry()
        +cancel()
    }
    
    class AIModel {
        +String name
        +String apiKey
        +ModelConfig config
        +processText()
        +validateInput()
        +handleError()
    }
    
    User ||--o{ Document : owns
    Document ||--o{ OCRResult : contains
    Document ||--o{ AIProcessingJob : processes
    AIProcessingJob }o--|| AIModel : uses
```

### **1.2 핵심 워크플로우 (Core Workflows)**

#### **문서 처리 파이프라인**
```python
"""
Paperwork AI 문서 처리 핵심 워크플로우
File: core/workflows/document_processing.py
"""

from typing import List, Optional, Dict, Any
from enum import Enum
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
import uuid

class ProcessingStatus(Enum):
    UPLOADED = "uploaded"
    VALIDATING = "validating"
    CONVERTING = "converting"
    OCR_PROCESSING = "ocr_processing"
    OCR_COMPLETED = "ocr_completed"
    AI_PROCESSING = "ai_processing"
    AI_COMPLETED = "ai_completed"
    COMPLETED = "completed"
    FAILED = "failed"

class JobType(Enum):
    SUMMARIZE = "summarize"
    IMPROVE = "improve"
    EXPAND = "expand"
    TRANSLATE = "translate"

@dataclass
class DocumentMetadata:
    """문서 메타데이터 모델"""
    file_size: int
    page_count: int
    file_type: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def validate(self) -> bool:
        """메타데이터 유효성 검증"""
        if self.file_size <= 0:
            raise ValueError("파일 크기가 유효하지 않습니다")
        
        if self.page_count >= 10:  # 10페이지 이상 거부
            raise ValueError(f"파일이 너무 큽니다. 10페이지 미만의 문서만 업로드 가능합니다. (현재: {self.page_count}페이지)")
        
        if self.file_type not in ['pdf', 'doc', 'docx', 'jpg', 'png']:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {self.file_type}")
        
        return True

@dataclass
class DocumentProcessingContext:
    """문서 처리 컨텍스트"""
    document_id: str
    user_id: str
    metadata: DocumentMetadata
    status: ProcessingStatus = ProcessingStatus.UPLOADED
    progress: float = 0.0
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def update_status(self, new_status: ProcessingStatus, progress: float = None, error: str = None):
        """상태 업데이트"""
        self.status = new_status
        if progress is not None:
            self.progress = progress
        if error:
            self.error_message = error
        self.updated_at = datetime.utcnow()

class DocumentProcessor:
    """문서 처리 오케스트레이터"""
    
    def __init__(self, 
                 file_validator: 'FileValidator',
                 pdf_converter: 'PDFConverter', 
                 ocr_service: 'OCRService',
                 ai_service: 'AIService',
                 storage_service: 'StorageService',
                 notification_service: 'NotificationService'):
        self.file_validator = file_validator
        self.pdf_converter = pdf_converter
        self.ocr_service = ocr_service
        self.ai_service = ai_service
        self.storage_service = storage_service
        self.notification_service = notification_service
    
    async def process_document(self, 
                             file_data: bytes, 
                             filename: str,
                             user_id: str) -> DocumentProcessingContext:
        """완전한 문서 처리 워크플로우"""
        
        # 1. 컨텍스트 초기화
        document_id = str(uuid.uuid4())
        context = DocumentProcessingContext(
            document_id=document_id,
            user_id=user_id,
            metadata=DocumentMetadata(
                file_size=len(file_data),
                page_count=0,  # 임시값, 후에 업데이트
                file_type=filename.split('.')[-1].lower()
            )
        )
        
        try:
            # 2. 파일 검증
            await self._validate_file(context, file_data, filename)
            
            # 3. 저장소 업로드
            await self._upload_to_storage(context, file_data, filename)
            
            # 4. PDF 변환 (필요시)
            await self._convert_to_pdf(context)
            
            # 5. 이미지 변환
            await self._convert_to_images(context)
            
            # 6. OCR 처리
            await self._process_ocr(context)
            
            # 7. 완료 알림
            await self._notify_completion(context)
            
            return context
            
        except Exception as e:
            context.update_status(ProcessingStatus.FAILED, error=str(e))
            await self._notify_error(context, e)
            raise
    
    async def _validate_file(self, context: DocumentProcessingContext, 
                           file_data: bytes, filename: str):
        """1단계: 파일 검증"""
        context.update_status(ProcessingStatus.VALIDATING, 5.0)
        
        # 파일 유효성 검증
        validation_result = await self.file_validator.validate(
            file_data, filename, context.metadata.file_type
        )
        
        if not validation_result.is_valid:
            raise ValueError(f"파일 검증 실패: {validation_result.error_message}")
        
        # 페이지 수 추출 및 검증
        if context.metadata.file_type == 'pdf':
            page_count = await self.pdf_converter.get_page_count(file_data)
            context.metadata.page_count = page_count
            context.metadata.validate()  # 페이지 수 제한 검증
    
    async def _upload_to_storage(self, context: DocumentProcessingContext, 
                               file_data: bytes, filename: str):
        """2단계: 저장소 업로드"""
        context.update_status(ProcessingStatus.UPLOADING, 15.0)
        
        storage_path = f"documents/{context.user_id}/{context.document_id}/{filename}"
        await self.storage_service.upload(storage_path, file_data)
        
        # 컨텍스트에 저장 경로 추가
        context.storage_path = storage_path
    
    async def _convert_to_pdf(self, context: DocumentProcessingContext):
        """3단계: PDF 변환 (Word 문서 등)"""
        if context.metadata.file_type in ['doc', 'docx']:
            context.update_status(ProcessingStatus.CONVERTING, 25.0)
            
            # Word 문서를 PDF로 변환
            file_data = await self.storage_service.download(context.storage_path)
            pdf_data = await self.pdf_converter.convert_to_pdf(file_data, context.metadata.file_type)
            
            # 변환된 PDF 저장
            pdf_path = context.storage_path.replace('.docx', '.pdf').replace('.doc', '.pdf')
            await self.storage_service.upload(pdf_path, pdf_data)
            context.storage_path = pdf_path
            context.metadata.file_type = 'pdf'
    
    async def _convert_to_images(self, context: DocumentProcessingContext):
        """4단계: 이미지 변환"""
        context.update_status(ProcessingStatus.CONVERTING, 40.0)
        
        if context.metadata.file_type == 'pdf':
            # PDF를 고해상도 이미지로 변환
            file_data = await self.storage_service.download(context.storage_path)
            images = await self.pdf_converter.convert_to_images(
                file_data, 
                dpi=300,  # 고해상도
                format='png'
            )
            
            # 이미지들을 저장
            image_paths = []
            for i, image_data in enumerate(images):
                image_path = f"images/{context.document_id}/page_{i+1}.png"
                await self.storage_service.upload(image_path, image_data)
                image_paths.append(image_path)
            
            context.image_paths = image_paths
        elif context.metadata.file_type in ['jpg', 'png']:
            # 이미 이미지인 경우 그대로 사용
            context.image_paths = [context.storage_path]
    
    async def _process_ocr(self, context: DocumentProcessingContext):
        """5단계: OCR 처리"""
        context.update_status(ProcessingStatus.OCR_PROCESSING, 60.0)
        
        ocr_results = []
        total_images = len(context.image_paths)
        
        for i, image_path in enumerate(context.image_paths):
            # 진행률 업데이트
            progress = 60.0 + (30.0 * (i + 1) / total_images)
            context.update_status(ProcessingStatus.OCR_PROCESSING, progress)
            
            # OCR 실행
            image_data = await self.storage_service.download(image_path)
            ocr_result = await self.ocr_service.extract_text(
                image_data, 
                page_number=i+1,
                document_id=context.document_id
            )
            ocr_results.append(ocr_result)
        
        context.ocr_results = ocr_results
        context.update_status(ProcessingStatus.OCR_COMPLETED, 90.0)
    
    async def _notify_completion(self, context: DocumentProcessingContext):
        """6단계: 완료 알림"""
        context.update_status(ProcessingStatus.COMPLETED, 100.0)
        
        await self.notification_service.notify_user(
            user_id=context.user_id,
            message="문서 업로드 및 OCR 처리가 완료되었습니다.",
            document_id=context.document_id
        )
    
    async def _notify_error(self, context: DocumentProcessingContext, error: Exception):
        """오류 알림"""
        await self.notification_service.notify_error(
            user_id=context.user_id,
            error_message=str(error),
            document_id=context.document_id
        )
```

---

## 🔧 **2. 파일 처리 모듈**

### **2.1 파일 검증 서비스**

```python
"""
파일 검증 및 메타데이터 추출 서비스
File: core/services/file_validation.py
"""

from typing import Dict, List, Optional, NamedTuple
import magic
import fitz  # PyMuPDF
from PIL import Image
import io
import hashlib

class ValidationResult(NamedTuple):
    is_valid: bool
    error_message: Optional[str] = None
    metadata: Optional[Dict] = None

class FileValidator:
    """파일 검증 서비스"""
    
    # 지원 파일 형식 및 MIME 타입
    SUPPORTED_FORMATS = {
        'pdf': ['application/pdf'],
        'doc': ['application/msword'],
        'docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        'jpg': ['image/jpeg'],
        'png': ['image/png']
    }
    
    # 파일 크기 제한 (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # 페이지 수 제한 (10페이지 미만만 허용)
    MAX_PAGES = 9
    
    def __init__(self):
        self.magic_mime = magic.Magic(mime=True)
    
    async def validate(self, file_data: bytes, filename: str, expected_type: str) -> ValidationResult:
        """종합적인 파일 검증"""
        
        try:
            # 1. 기본 검증
            basic_validation = self._validate_basic(file_data, filename)
            if not basic_validation.is_valid:
                return basic_validation
            
            # 2. MIME 타입 검증
            mime_validation = self._validate_mime_type(file_data, expected_type)
            if not mime_validation.is_valid:
                return mime_validation
            
            # 3. 형식별 상세 검증
            format_validation = await self._validate_format_specific(file_data, expected_type)
            if not format_validation.is_valid:
                return format_validation
            
            # 4. 보안 검증
            security_validation = self._validate_security(file_data, expected_type)
            if not security_validation.is_valid:
                return security_validation
            
            # 5. 메타데이터 추출
            metadata = await self._extract_metadata(file_data, expected_type)
            
            return ValidationResult(
                is_valid=True,
                metadata=metadata
            )
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"파일 검증 중 오류 발생: {str(e)}"
            )
    
    def _validate_basic(self, file_data: bytes, filename: str) -> ValidationResult:
        """기본 검증 (크기, 이름 등)"""
        
        # 파일 크기 검증
        if len(file_data) == 0:
            return ValidationResult(False, "빈 파일은 업로드할 수 없습니다.")
        
        if len(file_data) > self.MAX_FILE_SIZE:
            size_mb = len(file_data) / (1024 * 1024)
            return ValidationResult(
                False, 
                f"파일 크기가 너무 큽니다. 최대 10MB까지 지원합니다. (현재: {size_mb:.1f}MB)"
            )
        
        # 파일명 검증
        if not filename or len(filename.strip()) == 0:
            return ValidationResult(False, "유효한 파일명이 필요합니다.")
        
        if len(filename) > 255:
            return ValidationResult(False, "파일명이 너무 깁니다. (최대 255자)")
        
        # 확장자 검증
        if '.' not in filename:
            return ValidationResult(False, "파일 확장자가 필요합니다.")
        
        extension = filename.split('.')[-1].lower()
        if extension not in self.SUPPORTED_FORMATS:
            supported = ", ".join(self.SUPPORTED_FORMATS.keys())
            return ValidationResult(
                False, 
                f"지원하지 않는 파일 형식입니다. 지원 형식: {supported}"
            )
        
        return ValidationResult(True)
    
    def _validate_mime_type(self, file_data: bytes, expected_type: str) -> ValidationResult:
        """MIME 타입 검증"""
        
        try:
            detected_mime = self.magic_mime.from_buffer(file_data)
            expected_mimes = self.SUPPORTED_FORMATS.get(expected_type, [])
            
            if detected_mime not in expected_mimes:
                return ValidationResult(
                    False,
                    f"파일 형식이 일치하지 않습니다. 예상: {expected_type}, 실제: {detected_mime}"
                )
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(
                False,
                f"MIME 타입 검증 실패: {str(e)}"
            )
    
    async def _validate_format_specific(self, file_data: bytes, file_type: str) -> ValidationResult:
        """형식별 상세 검증"""
        
        try:
            if file_type == 'pdf':
                return await self._validate_pdf(file_data)
            elif file_type in ['jpg', 'png']:
                return await self._validate_image(file_data)
            elif file_type in ['doc', 'docx']:
                return await self._validate_word(file_data)
            else:
                return ValidationResult(True)
                
        except Exception as e:
            return ValidationResult(
                False,
                f"{file_type.upper()} 파일 검증 실패: {str(e)}"
            )
    
    async def _validate_pdf(self, file_data: bytes) -> ValidationResult:
        """PDF 파일 검증"""
        
        try:
            doc = fitz.open(stream=file_data, filetype="pdf")
            
            # 페이지 수 검증
            page_count = doc.page_count
            if page_count >= 10:  # 10페이지 이상 거부
                doc.close()
                return ValidationResult(
                    False,
                    f"파일이 너무 큽니다. 10페이지 미만의 문서만 업로드 가능합니다. (현재: {page_count}페이지)"
                )
            
            # PDF 손상 검증
            for page_num in range(page_count):
                try:
                    page = doc[page_num]
                    # 페이지 렌더링 테스트
                    pix = page.get_pixmap(matrix=fitz.Matrix(0.1, 0.1))  # 작은 해상도로 테스트
                    pix = None  # 메모리 해제
                except Exception:
                    doc.close()
                    return ValidationResult(
                        False,
                        f"PDF 파일이 손상되었습니다. (페이지 {page_num + 1})"
                    )
            
            # 암호화 검증
            if doc.needs_pass:
                doc.close()
                return ValidationResult(
                    False,
                    "암호화된 PDF 파일은 지원하지 않습니다."
                )
            
            doc.close()
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(
                False,
                f"PDF 파일 형식이 올바르지 않습니다: {str(e)}"
            )
    
    async def _validate_image(self, file_data: bytes) -> ValidationResult:
        """이미지 파일 검증"""
        
        try:
            image = Image.open(io.BytesIO(file_data))
            
            # 이미지 기본 정보 확인
            width, height = image.size
            
            # 최소 크기 검증
            if width < 100 or height < 100:
                return ValidationResult(
                    False,
                    f"이미지 크기가 너무 작습니다. 최소 100x100px 이상이어야 합니다. (현재: {width}x{height}px)"
                )
            
            # 최대 크기 검증 (OCR 처리 고려)
            if width > 5000 or height > 5000:
                return ValidationResult(
                    False,
                    f"이미지 크기가 너무 큽니다. 최대 5000x5000px까지 지원합니다. (현재: {width}x{height}px)"
                )
            
            # 이미지 손상 검증
            try:
                image.verify()
            except Exception:
                return ValidationResult(
                    False,
                    "손상된 이미지 파일입니다."
                )
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(
                False,
                f"이미지 파일 형식이 올바르지 않습니다: {str(e)}"
            )
    
    async def _validate_word(self, file_data: bytes) -> ValidationResult:
        """Word 문서 검증"""
        
        try:
            # python-docx를 사용한 Word 문서 검증
            from docx import Document
            
            doc = Document(io.BytesIO(file_data))
            
            # 문서 구조 기본 검증
            paragraph_count = len(doc.paragraphs)
            if paragraph_count == 0:
                return ValidationResult(
                    False,
                    "빈 Word 문서입니다."
                )
            
            # 대략적인 페이지 수 추정 (단락 수 기반)
            estimated_pages = max(1, paragraph_count // 10)  # 단락 10개당 1페이지로 추정
            if estimated_pages >= 10:
                return ValidationResult(
                    False,
                    f"문서가 너무 깁니다. 예상 페이지 수: {estimated_pages}페이지 (10페이지 미만만 허용)"
                )
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(
                False,
                f"Word 문서 형식이 올바르지 않습니다: {str(e)}"
            )
    
    def _validate_security(self, file_data: bytes, file_type: str) -> ValidationResult:
        """보안 검증 (바이러스, 악성코드 등)"""
        
        try:
            # 파일 해시 생성
            file_hash = hashlib.sha256(file_data).hexdigest()
            
            # 악성 파일 패턴 검사 (간단한 예시)
            suspicious_patterns = [
                b'<script',
                b'javascript:',
                b'vbscript:',
                b'onload=',
                b'onerror='
            ]
            
            for pattern in suspicious_patterns:
                if pattern in file_data.lower():
                    return ValidationResult(
                        False,
                        "의심스러운 콘텐츠가 포함된 파일입니다."
                    )
            
            # TODO: 실제 환경에서는 VirusTotal API 등을 사용하여 검증
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(
                False,
                f"보안 검증 실패: {str(e)}"
            )
    
    async def _extract_metadata(self, file_data: bytes, file_type: str) -> Dict:
        """메타데이터 추출"""
        
        metadata = {
            'file_size': len(file_data),
            'file_type': file_type,
            'file_hash': hashlib.sha256(file_data).hexdigest()
        }
        
        try:
            if file_type == 'pdf':
                doc = fitz.open(stream=file_data, filetype="pdf")
                metadata.update({
                    'page_count': doc.page_count,
                    'title': doc.metadata.get('title', ''),
                    'author': doc.metadata.get('author', ''),
                    'subject': doc.metadata.get('subject', ''),
                    'creator': doc.metadata.get('creator', ''),
                    'producer': doc.metadata.get('producer', ''),
                    'creation_date': doc.metadata.get('creationDate', ''),
                    'modification_date': doc.metadata.get('modDate', '')
                })
                doc.close()
                
            elif file_type in ['jpg', 'png']:
                image = Image.open(io.BytesIO(file_data))
                metadata.update({
                    'width': image.size[0],
                    'height': image.size[1],
                    'mode': image.mode,
                    'format': image.format
                })
                
                # EXIF 데이터 추출 (JPEG만)
                if hasattr(image, '_getexif') and image._getexif():
                    exif = image._getexif()
                    metadata['exif'] = {k: str(v) for k, v in exif.items() if isinstance(v, (str, int, float))}
                
            elif file_type in ['doc', 'docx']:
                from docx import Document
                doc = Document(io.BytesIO(file_data))
                
                metadata.update({
                    'paragraph_count': len(doc.paragraphs),
                    'estimated_pages': max(1, len(doc.paragraphs) // 10)
                })
                
                # 문서 속성 추출
                props = doc.core_properties
                if props:
                    metadata.update({
                        'title': props.title or '',
                        'author': props.author or '',
                        'subject': props.subject or '',
                        'created': props.created.isoformat() if props.created else '',
                        'modified': props.modified.isoformat() if props.modified else ''
                    })
            
        except Exception as e:
            # 메타데이터 추출 실패는 치명적이지 않음
            metadata['metadata_extraction_error'] = str(e)
        
        return metadata
```

### **2.2 PDF 변환 서비스**

```python
"""
PDF 변환 및 이미지 추출 서비스
File: core/services/pdf_conversion.py
"""

from typing import List, Tuple, Optional
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile
import os
from pathlib import Path

class PDFConverter:
    """PDF 변환 서비스"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    async def get_page_count(self, pdf_data: bytes) -> int:
        """PDF 페이지 수 반환"""
        try:
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            page_count = doc.page_count
            doc.close()
            return page_count
        except Exception as e:
            raise ValueError(f"PDF 페이지 수 확인 실패: {str(e)}")
    
    async def convert_to_images(self, 
                              pdf_data: bytes, 
                              dpi: int = 300,
                              format: str = 'PNG') -> List[bytes]:
        """PDF를 고해상도 이미지로 변환"""
        
        images = []
        doc = None
        
        try:
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            
            # 스케일링 매트릭스 계산 (DPI 기반)
            zoom = dpi / 72.0  # 72 DPI가 기본값
            matrix = fitz.Matrix(zoom, zoom)
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # 페이지를 이미지로 렌더링
                pix = page.get_pixmap(matrix=matrix, alpha=False)
                
                # PIL Image로 변환
                img_data = pix.tobytes(format.lower())
                pil_image = Image.frombytes("RGB", [pix.width, pix.height], img_data)
                
                # 이미지 후처리 (OCR 최적화)
                processed_image = await self._optimize_for_ocr(pil_image)
                
                # 바이트로 변환
                img_buffer = io.BytesIO()
                processed_image.save(img_buffer, format=format, quality=95, optimize=True)
                images.append(img_buffer.getvalue())
                
                # 메모리 정리
                pix = None
                img_buffer.close()
            
            return images
            
        except Exception as e:
            raise ValueError(f"PDF 이미지 변환 실패: {str(e)}")
        finally:
            if doc:
                doc.close()
    
    async def _optimize_for_ocr(self, image: Image.Image) -> Image.Image:
        """OCR을 위한 이미지 최적화"""
        
        try:
            # 1. 그레이스케일 변환
            if image.mode != 'L':
                image = image.convert('L')
            
            # 2. 대비 향상
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)  # 대비 20% 향상
            
            # 3. 선명도 향상
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)  # 선명도 10% 향상
            
            # 4. 노이즈 제거 (간단한 미디안 필터)
            # 실제 환경에서는 OpenCV 등을 사용하여 더 정교한 처리
            
            return image
            
        except Exception as e:
            # 최적화 실패 시 원본 반환
            return image
    
    async def convert_to_pdf(self, file_data: bytes, source_format: str) -> bytes:
        """다른 형식을 PDF로 변환"""
        
        try:
            if source_format in ['doc', 'docx']:
                return await self._convert_word_to_pdf(file_data)
            elif source_format in ['jpg', 'png']:
                return await self._convert_image_to_pdf(file_data)
            else:
                raise ValueError(f"지원하지 않는 변환 형식: {source_format}")
                
        except Exception as e:
            raise ValueError(f"PDF 변환 실패: {str(e)}")
    
    async def _convert_word_to_pdf(self, word_data: bytes) -> bytes:
        """Word 문서를 PDF로 변환"""
        
        try:
            # python-docx와 reportlab을 사용한 변환
            from docx import Document
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            
            # Word 문서 읽기
            doc = Document(io.BytesIO(word_data))
            
            # PDF 생성
            pdf_buffer = io.BytesIO()
            pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    para = Paragraph(paragraph.text, styles['Normal'])
                    story.append(para)
                    story.append(Spacer(1, 12))
            
            pdf_doc.build(story)
            return pdf_buffer.getvalue()
            
        except Exception as e:
            raise ValueError(f"Word to PDF 변환 실패: {str(e)}")
    
    async def _convert_image_to_pdf(self, image_data: bytes) -> bytes:
        """이미지를 PDF로 변환"""
        
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # PDF 생성
            pdf_buffer = io.BytesIO()
            
            # RGB 모드로 변환 (PDF 호환성)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # PDF로 저장
            image.save(pdf_buffer, format='PDF', quality=95, optimize=True)
            
            return pdf_buffer.getvalue()
            
        except Exception as e:
            raise ValueError(f"Image to PDF 변환 실패: {str(e)}")
    
    async def extract_text_direct(self, pdf_data: bytes) -> List[str]:
        """PDF에서 직접 텍스트 추출 (OCR 보완용)"""
        
        try:
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            texts = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text()
                texts.append(text.strip())
            
            doc.close()
            return texts
            
        except Exception as e:
            raise ValueError(f"PDF 텍스트 추출 실패: {str(e)}")
    
    async def get_pdf_info(self, pdf_data: bytes) -> dict:
        """PDF 정보 추출"""
        
        try:
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            
            info = {
                'page_count': doc.page_count,
                'metadata': doc.metadata,
                'is_encrypted': doc.needs_pass,
                'is_pdf_a': doc.is_pdf,
                'pages_info': []
            }
            
            # 각 페이지 정보
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_info = {
                    'page_number': page_num + 1,
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'rotation': page.rotation,
                    'has_images': len(page.get_images()) > 0,
                    'text_length': len(page.get_text())
                }
                info['pages_info'].append(page_info)
            
            doc.close()
            return info
            
        except Exception as e:
            raise ValueError(f"PDF 정보 추출 실패: {str(e)}")
```

---

## 👁️ **3. OCR 처리 모듈**

### **3.1 통합 OCR 서비스**

```python
"""
통합 OCR 처리 서비스
File: core/services/ocr_service.py
"""

from typing import List, Optional, Dict, Any, NamedTuple
from enum import Enum
import asyncio
import base64
import json
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod

class OCREngine(Enum):
    TESSERACT = "tesseract"
    GOOGLE_VISION = "google_vision"
    AZURE_COGNITIVE = "azure_cognitive"
    AWS_TEXTRACT = "aws_textract"

class OCRQuality(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"

@dataclass
class OCRResult:
    """OCR 결과 모델"""
    document_id: str
    page_number: int
    extracted_text: str
    confidence_score: float
    processing_time_ms: int
    engine_used: OCREngine
    bounding_boxes: Optional[List[Dict]] = None
    language_detected: Optional[str] = None
    error_message: Optional[str] = None

class BaseOCREngine(ABC):
    """OCR 엔진 기본 클래스"""
    
    @abstractmethod
    async def extract_text(self, 
                          image_data: bytes, 
                          language: str = 'kor+eng',
                          quality: OCRQuality = OCRQuality.HIGH) -> OCRResult:
        pass
    
    @abstractmethod
    def get_engine_name(self) -> OCREngine:
        pass

class TesseractEngine(BaseOCREngine):
    """Tesseract OCR 엔진"""
    
    def __init__(self):
        import pytesseract
        from PIL import Image
        self.pytesseract = pytesseract
        self.Image = Image
    
    def get_engine_name(self) -> OCREngine:
        return OCREngine.TESSERACT
    
    async def extract_text(self, 
                          image_data: bytes, 
                          language: str = 'kor+eng',
                          quality: OCRQuality = OCRQuality.HIGH) -> OCRResult:
        
        start_time = time.time()
        
        try:
            # 이미지 전처리
            image = self.Image.open(io.BytesIO(image_data))
            processed_image = await self._preprocess_image(image, quality)
            
            # OCR 설정
            config = self._get_tesseract_config(quality)
            
            # 텍스트 추출
            extracted_text = self.pytesseract.image_to_string(
                processed_image, 
                lang=language,
                config=config
            )
            
            # 신뢰도 추출
            confidence_data = self.pytesseract.image_to_data(
                processed_image, 
                lang=language,
                config=config,
                output_type=self.pytesseract.Output.DICT
            )
            
            # 평균 신뢰도 계산
            confidences = [int(conf) for conf in confidence_data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # 바운딩 박스 정보
            bounding_boxes = self._extract_bounding_boxes(confidence_data)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return OCRResult(
                document_id="",  # 호출자에서 설정
                page_number=0,   # 호출자에서 설정
                extracted_text=extracted_text.strip(),
                confidence_score=avg_confidence / 100.0,  # 0-1 범위로 정규화
                processing_time_ms=processing_time,
                engine_used=self.get_engine_name(),
                bounding_boxes=bounding_boxes
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return OCRResult(
                document_id="",
                page_number=0,
                extracted_text="",
                confidence_score=0.0,
                processing_time_ms=processing_time,
                engine_used=self.get_engine_name(),
                error_message=f"Tesseract OCR 실패: {str(e)}"
            )
    
    async def _preprocess_image(self, image: 'Image.Image', quality: OCRQuality) -> 'Image.Image':
        """OCR을 위한 이미지 전처리"""
        
        try:
            # 그레이스케일 변환
            if image.mode != 'L':
                image = image.convert('L')
            
            if quality in [OCRQuality.HIGH, OCRQuality.ULTRA]:
                # 고품질 전처리
                from PIL import ImageEnhance, ImageFilter
                
                # 대비 향상
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.5)
                
                # 선명도 향상
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(1.2)
                
                if quality == OCRQuality.ULTRA:
                    # 노이즈 제거
                    image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
            
        except Exception:
            # 전처리 실패 시 원본 반환
            return image
    
    def _get_tesseract_config(self, quality: OCRQuality) -> str:
        """품질별 Tesseract 설정"""
        
        base_config = '--oem 3 --psm 6'  # LSTM + 단일 블록 텍스트
        
        if quality == OCRQuality.LOW:
            return f"{base_config} -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ가-힣"
        elif quality == OCRQuality.MEDIUM:
            return f"{base_config} -c preserve_interword_spaces=1"
        elif quality == OCRQuality.HIGH:
            return f"{base_config} -c preserve_interword_spaces=1 -c tessedit_do_invert=0"
        else:  # ULTRA
            return f"{base_config} -c preserve_interword_spaces=1 -c tessedit_do_invert=0 -c classify_bln_numeric_mode=0"
    
    def _extract_bounding_boxes(self, data: Dict) -> List[Dict]:
        """바운딩 박스 정보 추출"""
        
        boxes = []
        n_boxes = len(data['level'])
        
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0:  # 신뢰도가 있는 항목만
                box = {
                    'text': data['text'][i],
                    'confidence': int(data['conf'][i]),
                    'left': int(data['left'][i]),
                    'top': int(data['top'][i]),
                    'width': int(data['width'][i]),
                    'height': int(data['height'][i])
                }
                boxes.append(box)
        
        return boxes

class GoogleVisionEngine(BaseOCREngine):
    """Google Cloud Vision OCR 엔진"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Google Vision API 클라이언트 초기화"""
        try:
            from google.cloud import vision
            import os
            
            # API 키 설정
            if self.api_key:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.api_key
            
            self.client = vision.ImageAnnotatorClient()
        except Exception as e:
            raise ValueError(f"Google Vision API 초기화 실패: {str(e)}")
    
    def get_engine_name(self) -> OCREngine:
        return OCREngine.GOOGLE_VISION
    
    async def extract_text(self, 
                          image_data: bytes, 
                          language: str = 'ko+en',
                          quality: OCRQuality = OCRQuality.HIGH) -> OCRResult:
        
        start_time = time.time()
        
        try:
            from google.cloud import vision
            
            # 이미지 객체 생성
            image = vision.Image(content=image_data)
            
            # 언어 힌트 설정
            language_hints = ['ko', 'en'] if language == 'ko+en' else [language]
            image_context = vision.ImageContext(language_hints=language_hints)
            
            # 텍스트 감지 실행
            response = self.client.text_detection(
                image=image,
                image_context=image_context
            )
            
            if response.error.message:
                raise Exception(response.error.message)
            
            # 결과 처리
            texts = response.text_annotations
            
            if not texts:
                extracted_text = ""
                confidence = 0.0
                bounding_boxes = []
            else:
                # 첫 번째 annotation이 전체 텍스트
                extracted_text = texts[0].description
                
                # 평균 신뢰도 계산 (Google Vision은 confidence를 직접 제공하지 않음)
                # 대신 detection의 개수와 품질로 추정
                confidence = min(0.95, 0.5 + (len(texts) * 0.05))
                
                # 바운딩 박스 추출
                bounding_boxes = []
                for text in texts[1:]:  # 첫 번째 제외 (전체 텍스트)
                    vertices = text.bounding_poly.vertices
                    box = {
                        'text': text.description,
                        'confidence': int(confidence * 100),
                        'left': min(v.x for v in vertices),
                        'top': min(v.y for v in vertices),
                        'width': max(v.x for v in vertices) - min(v.x for v in vertices),
                        'height': max(v.y for v in vertices) - min(v.y for v in vertices)
                    }
                    bounding_boxes.append(box)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return OCRResult(
                document_id="",
                page_number=0,
                extracted_text=extracted_text.strip(),
                confidence_score=confidence,
                processing_time_ms=processing_time,
                engine_used=self.get_engine_name(),
                bounding_boxes=bounding_boxes,
                language_detected=language
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return OCRResult(
                document_id="",
                page_number=0,
                extracted_text="",
                confidence_score=0.0,
                processing_time_ms=processing_time,
                engine_used=self.get_engine_name(),
                error_message=f"Google Vision OCR 실패: {str(e)}"
            )

class OCRService:
    """통합 OCR 서비스"""
    
    def __init__(self, 
                 primary_engine: BaseOCREngine,
                 fallback_engines: List[BaseOCREngine] = None):
        self.primary_engine = primary_engine
        self.fallback_engines = fallback_engines or []
        self.min_confidence_threshold = 0.7
    
    async def extract_text(self, 
                          image_data: bytes,
                          page_number: int,
                          document_id: str,
                          language: str = 'kor+eng',
                          quality: OCRQuality = OCRQuality.HIGH) -> OCRResult:
        """메인 OCR 처리 메서드"""
        
        # 1차: 기본 엔진 시도
        result = await self.primary_engine.extract_text(image_data, language, quality)
        result.document_id = document_id
        result.page_number = page_number
        
        # 결과가 만족스럽지 않으면 폴백 엔진들 시도
        if (result.confidence_score < self.min_confidence_threshold or 
            result.error_message or 
            len(result.extracted_text.strip()) < 10):
            
            for fallback_engine in self.fallback_engines:
                try:
                    fallback_result = await fallback_engine.extract_text(image_data, language, quality)
                    fallback_result.document_id = document_id
                    fallback_result.page_number = page_number
                    
                    # 더 좋은 결과인지 확인
                    if (fallback_result.confidence_score > result.confidence_score and
                        not fallback_result.error_message):
                        result = fallback_result
                        break
                        
                except Exception:
                    continue
        
        # 후처리
        result.extracted_text = await self._post_process_text(result.extracted_text)
        
        return result
    
    async def _post_process_text(self, text: str) -> str:
        """OCR 결과 후처리"""
        
        if not text:
            return text
        
        # 1. 기본 정리
        text = text.strip()
        
        # 2. 연속된 공백 정리
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # 3. 한글-영어 사이 공백 정리
        text = re.sub(r'([가-힣])\s+([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])\s+([가-힣])', r'\1 \2', text)
        
        # 4. 숫자 주변 공백 정리
        text = re.sub(r'(\d)\s+([가-힣a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([가-힣a-zA-Z])\s+(\d)', r'\1 \2', text)
        
        # 5. 일반적인 OCR 오류 수정
        corrections = {
            'O': '0',  # 숫자 컨텍스트에서
            'l': '1',  # 숫자 컨텍스트에서
            '｜': '|',
            '．': '.',
            '，': ',',
            '？': '?',
            '！': '!',
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        return text
    
    async def batch_extract_text(self, 
                                images_data: List[bytes],
                                document_id: str,
                                language: str = 'kor+eng',
                                quality: OCRQuality = OCRQuality.HIGH) -> List[OCRResult]:
        """배치 OCR 처리"""
        
        tasks = []
        for i, image_data in enumerate(images_data):
            task = self.extract_text(
                image_data=image_data,
                page_number=i + 1,
                document_id=document_id,
                language=language,
                quality=quality
            )
            tasks.append(task)
        
        # 병렬 처리
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 예외 처리
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = OCRResult(
                    document_id=document_id,
                    page_number=i + 1,
                    extracted_text="",
                    confidence_score=0.0,
                    processing_time_ms=0,
                    engine_used=self.primary_engine.get_engine_name(),
                    error_message=f"OCR 처리 실패: {str(result)}"
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results
    
    def combine_ocr_results(self, results: List[OCRResult]) -> str:
        """여러 페이지 OCR 결과 결합"""
        
        valid_results = [r for r in results if r.extracted_text and not r.error_message]
        
        if not valid_results:
            return ""
        
        # 페이지 순서로 정렬
        valid_results.sort(key=lambda x: x.page_number)
        
        # 텍스트 결합
        combined_text = ""
        for result in valid_results:
            combined_text += f"\n--- 페이지 {result.page_number} ---\n"
            combined_text += result.extracted_text
            combined_text += "\n"
        
        return combined_text.strip()
    
    def get_ocr_statistics(self, results: List[OCRResult]) -> Dict[str, Any]:
        """OCR 처리 통계"""
        
        total_pages = len(results)
        successful_pages = len([r for r in results if not r.error_message])
        failed_pages = total_pages - successful_pages
        
        if successful_pages > 0:
            avg_confidence = sum(r.confidence_score for r in results if not r.error_message) / successful_pages
            avg_processing_time = sum(r.processing_time_ms for r in results if not r.error_message) / successful_pages
            total_text_length = sum(len(r.extracted_text) for r in results if not r.error_message)
        else:
            avg_confidence = 0.0
            avg_processing_time = 0.0
            total_text_length = 0
        
        return {
            'total_pages': total_pages,
            'successful_pages': successful_pages,
            'failed_pages': failed_pages,
            'success_rate': successful_pages / total_pages if total_pages > 0 else 0,
            'average_confidence': avg_confidence,
            'average_processing_time_ms': avg_processing_time,
            'total_text_length': total_text_length,
            'engines_used': list(set(r.engine_used.value for r in results))
        }
```

---

## 🤖 **4. AI 처리 모듈**

### **4.1 AI 서비스 추상화**

```python
"""
AI 처리 서비스 통합 모듈
File: core/services/ai_service.py
"""

from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
import asyncio
import time
import json
from datetime import datetime

class AIModel(Enum):
    GEMINI = "gemini"
    GPT4 = "gpt4"
    CLAUDE = "claude"
    PERPLEXITY = "perplexity"
    CLOVA = "clova"

class JobType(Enum):
    SUMMARIZE = "summarize"
    IMPROVE = "improve"
    EXPAND = "expand"
    TRANSLATE = "translate"

@dataclass
class AIRequest:
    """AI 요청 모델"""
    job_type: JobType
    input_text: str
    reference_text: Optional[str] = None
    target_language: Optional[str] = None
    custom_prompt: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AIResponse:
    """AI 응답 모델"""
    processed_text: str
    model_used: AIModel
    processing_time_ms: int
    token_usage: Dict[str, int] = field(default_factory=dict)
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseAIProvider(ABC):
    """AI 프로바이더 기본 클래스"""
    
    @abstractmethod
    async def process_text(self, request: AIRequest) -> AIResponse:
        """텍스트 처리 메인 메서드"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> AIModel:
        """모델 이름 반환"""
        pass
    
    @abstractmethod
    def get_max_tokens(self) -> int:
        """최대 토큰 수 반환"""
        pass
    
    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """비용 추정"""
        pass

class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT-4 프로바이더"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """OpenAI 클라이언트 초기화"""
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"OpenAI 클라이언트 초기화 실패: {str(e)}")
    
    def get_model_name(self) -> AIModel:
        return AIModel.GPT4
    
    def get_max_tokens(self) -> int:
        return 4096
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # GPT-4 가격 (2024년 기준, 실제 가격은 변동될 수 있음)
        input_cost = input_tokens * 0.00003  # $0.03 per 1K tokens
        output_cost = output_tokens * 0.00006  # $0.06 per 1K tokens
        return input_cost + output_cost
    
    async def process_text(self, request: AIRequest) -> AIResponse:
        """OpenAI를 통한 텍스트 처리"""
        
        start_time = time.time()
        
        try:
            # 프롬프트 생성
            messages = self._build_messages(request)
            
            # API 호출
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.get_max_tokens(),
                temperature=self._get_temperature(request.job_type),
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # 응답 처리
            processed_text = response.choices[0].message.content
            
            # 토큰 사용량
            token_usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return AIResponse(
                processed_text=processed_text,
                model_used=self.get_model_name(),
                processing_time_ms=processing_time,
                token_usage=token_usage,
                confidence_score=0.9,  # OpenAI는 confidence를 직접 제공하지 않음
                metadata={
                    'model_version': self.model,
                    'finish_reason': response.choices[0].finish_reason
                }
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return AIResponse(
                processed_text="",
                model_used=self.get_model_name(),
                processing_time_ms=processing_time,
                error_message=f"OpenAI 처리 실패: {str(e)}"
            )
    
    def _build_messages(self, request: AIRequest) -> List[Dict[str, str]]:
        """메시지 구성"""
        
        system_message = self._get_system_message(request.job_type)
        user_message = self._get_user_message(request)
        
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
    def _get_system_message(self, job_type: JobType) -> str:
        """작업 유형별 시스템 메시지"""
        
        messages = {
            JobType.SUMMARIZE: "당신은 전문적인 문서 요약 전문가입니다. 주어진 문서의 핵심 내용을 간결하고 정확하게 요약해주세요.",
            JobType.IMPROVE: "당신은 문서 편집 전문가입니다. 주어진 텍스트의 문체, 구조, 가독성을 개선해주세요.",
            JobType.EXPAND: "당신은 콘텐츠 작성 전문가입니다. 주어진 텍스트를 더 상세하고 풍부하게 확장해주세요.",
            JobType.TRANSLATE: "당신은 전문 번역가입니다. 문맥과 뉘앙스를 고려하여 자연스럽게 번역해주세요."
        }
        
        return messages.get(job_type, "당신은 도움이 되는 AI 어시스턴트입니다.")
    
    def _get_user_message(self, request: AIRequest) -> str:
        """사용자 메시지 구성"""
        
        if request.custom_prompt:
            return request.custom_prompt
        
        prompts = {
            JobType.SUMMARIZE: f"""
다음 문서를 핵심 내용 중심으로 요약해주세요:

{request.input_text}

요약:""",
            JobType.IMPROVE: f"""
다음 문서의 문체와 구조를 개선해주세요:

{request.input_text}

개선된 문서:""",
            JobType.EXPAND: f"""
다음 문서를 더 상세하고 풍부하게 확장해주세요:
{f"참고자료: {request.reference_text}" if request.reference_text else ""}

원본 문서:
{request.input_text}

확장된 문서:""",
            JobType.TRANSLATE: f"""
다음 텍스트를 {request.target_language or '영어'}로 번역해주세요:

{request.input_text}

번역:"""
        }
        
        return prompts.get(request.job_type, request.input_text)
    
    def _get_temperature(self, job_type: JobType) -> float:
        """작업 유형별 temperature 설정"""
        
        temperatures = {
            JobType.SUMMARIZE: 0.3,    # 정확성 중시
            JobType.IMPROVE: 0.4,      # 약간의 창의성
            JobType.EXPAND: 0.6,       # 창의성 필요
            JobType.TRANSLATE: 0.2     # 정확성 최우선
        }
        
        return temperatures.get(job_type, 0.5)

class GoogleGeminiProvider(BaseAIProvider):
    """Google Gemini 프로바이더"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Gemini 클라이언트 초기화"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        except Exception as e:
            raise ValueError(f"Gemini 클라이언트 초기화 실패: {str(e)}")
    
    def get_model_name(self) -> AIModel:
        return AIModel.GEMINI
    
    def get_max_tokens(self) -> int:
        return 4096
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # Gemini 가격 (무료 tier도 있음)
        return 0.0  # 무료 사용량 내에서는 비용 없음
    
    async def process_text(self, request: AIRequest) -> AIResponse:
        """Gemini를 통한 텍스트 처리"""
        
        start_time = time.time()
        
        try:
            # 프롬프트 생성
            prompt = self._build_prompt(request)
            
            # API 호출
            response = await self.client.generate_content_async(
                prompt,
                generation_config={
                    'temperature': self._get_temperature(request.job_type),
                    'top_p': 0.9,
                    'top_k': 40,
                    'max_output_tokens': self.get_max_tokens(),
                }
            )
            
            processed_text = response.text
            processing_time = int((time.time() - start_time) * 1000)
            
            return AIResponse(
                processed_text=processed_text,
                model_used=self.get_model_name(),
                processing_time_ms=processing_time,
                confidence_score=0.85,
                metadata={
                    'model_version': self.model,
                    'safety_ratings': response.prompt_feedback.safety_ratings if hasattr(response, 'prompt_feedback') else []
                }
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return AIResponse(
                processed_text="",
                model_used=self.get_model_name(),
                processing_time_ms=processing_time,
                error_message=f"Gemini 처리 실패: {str(e)}"
            )
    
    def _build_prompt(self, request: AIRequest) -> str:
        """프롬프트 구성"""
        
        if request.custom_prompt:
            return request.custom_prompt
        
        system_context = self._get_system_context(request.job_type)
        user_message = self._get_user_message(request)
        
        return f"{system_context}\n\n{user_message}"
    
    def _get_system_context(self, job_type: JobType) -> str:
        """시스템 컨텍스트"""
        
        contexts = {
            JobType.SUMMARIZE: "당신은 전문적인 문서 요약 전문가입니다. 한국어 문서의 핵심 내용을 정확하고 간결하게 요약하는 것이 전문 분야입니다.",
            JobType.IMPROVE: "당신은 한국어 문서 편집 전문가입니다. 문체 개선, 구조 최적화, 가독성 향상이 전문 분야입니다.",
            JobType.EXPAND: "당신은 한국어 콘텐츠 작성 전문가입니다. 기존 내용을 바탕으로 풍부하고 상세한 문서를 작성하는 것이 전문 분야입니다.",
            JobType.TRANSLATE: "당신은 전문 번역가입니다. 한국어와 외국어 간의 정확하고 자연스러운 번역이 전문 분야입니다."
        }
        
        return contexts.get(job_type, "당신은 도움이 되는 AI 어시스턴트입니다.")
    
    def _get_user_message(self, request: AIRequest) -> str:
        """사용자 메시지 (OpenAI와 동일한 로직 재사용)"""
        
        prompts = {
            JobType.SUMMARIZE: f"""
다음 문서를 핵심 내용 중심으로 요약해주세요. 한국어로 자연스럽게 작성해주세요:

{request.input_text}

요약:""",
            JobType.IMPROVE: f"""
다음 문서의 문체와 구조를 개선해주세요. 가독성을 높이고 논리적 흐름을 개선해주세요:

{request.input_text}

개선된 문서:""",
            JobType.EXPAND: f"""
다음 문서를 더 상세하고 풍부하게 확장해주세요. 한국어 문맥에 맞게 자연스럽게 작성해주세요:
{f"참고자료: {request.reference_text}" if request.reference_text else ""}

원본 문서:
{request.input_text}

확장된 문서:""",
            JobType.TRANSLATE: f"""
다음 한국어 텍스트를 {request.target_language or '영어'}로 자연스럽게 번역해주세요:

{request.input_text}

번역:"""
        }
        
        return prompts.get(request.job_type, request.input_text)
    
    def _get_temperature(self, job_type: JobType) -> float:
        """작업 유형별 temperature (OpenAI와 동일)"""
        
        temperatures = {
            JobType.SUMMARIZE: 0.3,
            JobType.IMPROVE: 0.4,
            JobType.EXPAND: 0.6,
            JobType.TRANSLATE: 0.2
        }
        
        return temperatures.get(job_type, 0.5)

class ClovaXProvider(BaseAIProvider):
    """네이버 ClovaX 프로바이더"""
    
    def __init__(self, api_key: str, request_id: str):
        self.api_key = api_key
        self.request_id = request_id
        self.model = "HCX-005"
        self.host = "https://clovastudio.stream.ntruss.com"
    
    def get_model_name(self) -> AIModel:
        return AIModel.CLOVA
    
    def get_max_tokens(self) -> int:
        return 4096
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # ClovaX 가격 정보가 필요
        return 0.0  # 임시
    
    async def process_text(self, request: AIRequest) -> AIResponse:
        """ClovaX를 통한 텍스트 처리"""
        
        start_time = time.time()
        
        try:
            import aiohttp
            
            # 요청 데이터 구성
            request_data = {
                "messages": [
                    {
                        "role": "system",
                        "content": self._get_system_message(request.job_type)
                    },
                    {
                        "role": "user",
                        "content": self._get_user_message(request)
                    }
                ],
                "topP": 0.8,
                "topK": 0,
                "maxTokens": self.get_max_tokens(),
                "temperature": self._get_temperature(request.job_type),
                "repeatPenalty": 1.1,
                "stopBefore": [],
                "includeAiFilters": True,
                "seed": 0
            }
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'X-NCP-CLOVASTUDIO-REQUEST-ID': self.request_id,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json'
            }
            
            # API 호출
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.host}/v3/chat-completions/{self.model}",
                    headers=headers,
                    json=request_data
                ) as response:
                    
                    if response.status != 200:
                        raise Exception(f"ClovaX API 오류: {response.status}")
                    
                    result = await response.json()
            
            # 응답 처리
            if result.get('choices') and len(result['choices']) > 0:
                processed_text = result['choices'][0]['message']['content']
            else:
                raise Exception("ClovaX API 응답 형식 오류")
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return AIResponse(
                processed_text=processed_text,
                model_used=self.get_model_name(),
                processing_time_ms=processing_time,
                confidence_score=0.88,  # ClovaX 한국어 특화
                metadata={
                    'model_version': self.model,
                    'request_id': self.request_id
                }
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return AIResponse(
                processed_text="",
                model_used=self.get_model_name(),
                processing_time_ms=processing_time,
                error_message=f"ClovaX 처리 실패: {str(e)}"
            )
    
    def _get_system_message(self, job_type: JobType) -> str:
        """ClovaX 한국어 특화 시스템 메시지"""
        
        messages = {
            JobType.SUMMARIZE: "당신은 한국어 문서 처리 전문가입니다. 한국어 문서의 핵심 내용을 정확하고 자연스러운 한국어로 요약해주세요.",
            JobType.IMPROVE: "당신은 한국어 문체 개선 전문가입니다. 한국어 표현을 더 자연스럽고 읽기 쉽게 개선해주세요.",
            JobType.EXPAND: "당신은 한국어 콘텐츠 확장 전문가입니다. 한국어 문맥에 맞는 적절한 표현으로 내용을 풍부하게 확장해주세요.",
            JobType.TRANSLATE: "당신은 한국어 번역 전문가입니다. 문화적 맥락을 고려하여 자연스럽게 번역해주세요."
        }
        
        return messages.get(job_type, "당신은 한국어 문서 처리 전문가입니다.")
    
    def _get_user_message(self, request: AIRequest) -> str:
        """ClovaX용 사용자 메시지"""
        
        if request.custom_prompt:
            return request.custom_prompt
        
        prompts = {
            JobType.SUMMARIZE: f"""
다음 문서를 핵심 내용 중심으로 요약해주세요. 한국어 문맥에 맞게 자연스럽게 작성해주세요:

{request.input_text}

요약:""",
            JobType.IMPROVE: f"""
다음 문서의 문체와 구조를 개선해주세요. 한국어 표현을 더 자연스럽고 읽기 쉽게 만들어주세요:

{request.input_text}

개선된 문서:""",
            JobType.EXPAND: f"""
다음 문서를 더 상세하고 풍부하게 확장해주세요. 한국어 문맥에 맞는 적절한 표현을 사용해주세요:
{f"참고자료: {request.reference_text}" if request.reference_text else ""}

원본 문서:
{request.input_text}

확장된 문서:""",
            JobType.TRANSLATE: f"""
다음 한국어 문서를 {request.target_language or 'English'}로 자연스럽게 번역해주세요. 문화적 맥락도 고려해주세요:

{request.input_text}

번역:"""
        }
        
        return prompts.get(request.job_type, request.input_text)
    
    def _get_temperature(self, job_type: JobType) -> float:
        """작업 유형별 temperature"""
        
        temperatures = {
            JobType.SUMMARIZE: 0.3,
            JobType.IMPROVE: 0.4,
            JobType.EXPAND: 0.6,
            JobType.TRANSLATE: 0.2
        }
        
        return temperatures.get(job_type, 0.5)

class AIService:
    """통합 AI 서비스"""
    
    def __init__(self):
        self.providers: Dict[AIModel, BaseAIProvider] = {}
        self.default_model = AIModel.GEMINI
    
    def register_provider(self, provider: BaseAIProvider):
        """AI 프로바이더 등록"""
        self.providers[provider.get_model_name()] = provider
    
    def set_default_model(self, model: AIModel):
        """기본 모델 설정"""
        if model in self.providers:
            self.default_model = model
        else:
            raise ValueError(f"등록되지 않은 모델: {model}")
    
    async def process_document(self,
                             document_id: str,
                             job_type: JobType,
                             input_text: str,
                             ai_model: AIModel = None,
                             reference_text: str = None,
                             target_language: str = None,
                             custom_prompt: str = None) -> AIResponse:
        """문서 처리 메인 메서드"""
        
        # 모델 선택
        model = ai_model or self.default_model
        provider = self.providers.get(model)
        
        if not provider:
            raise ValueError(f"사용할 수 없는 AI 모델: {model}")
        
        # 요청 구성
        request = AIRequest(
            job_type=job_type,
            input_text=input_text,
            reference_text=reference_text,
            target_language=target_language,
            custom_prompt=custom_prompt
        )
        
        # AI 처리 실행
        response = await provider.process_text(request)
        
        # 메타데이터 추가
        response.metadata.update({
            'document_id': document_id,
            'job_type': job_type.value,
            'input_length': len(input_text),
            'output_length': len(response.processed_text),
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return response
    
    async def compare_models(self,
                           input_text: str,
                           job_type: JobType,
                           models: List[AIModel] = None) -> Dict[AIModel, AIResponse]:
        """여러 모델 비교"""
        
        if not models:
            models = list(self.providers.keys())
        
        tasks = []
        for model in models:
            if model in self.providers:
                request = AIRequest(job_type=job_type, input_text=input_text)
                task = self.providers[model].process_text(request)
                tasks.append((model, task))
        
        results = {}
        completed_tasks = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        for (model, _), result in zip(tasks, completed_tasks):
            if isinstance(result, Exception):
                results[model] = AIResponse(
                    processed_text="",
                    model_used=model,
                    processing_time_ms=0,
                    error_message=str(result)
                )
            else:
                results[model] = result
        
        return results
    
    def get_available_models(self) -> List[AIModel]:
        """사용 가능한 모델 목록"""
        return list(self.providers.keys())
    
    def get_model_info(self, model: AIModel) -> Dict[str, Any]:
        """모델 정보 조회"""
        
        provider = self.providers.get(model)
        if not provider:
            return {}
        
        return {
            'model_name': model.value,
            'max_tokens': provider.get_max_tokens(),
            'estimated_cost_per_1k_tokens': provider.estimate_cost(1000, 1000),
            'supported_languages': ['ko', 'en'],  # 모든 모델이 한영 지원
            'specialties': self._get_model_specialties(model)
        }
    
    def _get_model_specialties(self, model: AIModel) -> List[str]:
        """모델별 특화 분야"""
        
        specialties = {
            AIModel.GEMINI: ['일반 문서', '빠른 처리', '무료 사용'],
            AIModel.GPT4: ['창의적 편집', '복잡한 구조', '높은 품질'],
            AIModel.CLAUDE: ['정확한 분석', '긴 문서', '안전한 처리'],
            AIModel.PERPLEXITY: ['실시간 정보', '팩트체크', '최신 데이터'],
            AIModel.CLOVA: ['한국어 특화', '로컬 컨텍스트', '문화적 이해']
        }
        
        return specialties.get(model, ['범용 처리'])
```

---

이제 마지막으로 완전 구현 가능한 코드 샘플을 정리하겠습니다.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "\uc0ac\uc6a9\uc790/\uace0\uac1d \uad00\uc810 \uae30\ub2a5 \uba85\uc138\uc11c \uc791\uc131", "status": "completed", "id": "1"}, {"content": "\uac1c\ubc1c\uc790 \uad00\uc810 \uc544\ud0a4\ud14d\ucc98 \uc124\uacc4\uc548 \uc791\uc131", "status": "completed", "id": "2"}, {"content": "\ub514\uc790\uc774\ub108 \uad00\uc810 UI/UX/AX \uac00\uc774\ub4dc \uc791\uc131", "status": "completed", "id": "3"}, {"content": "\ud575\uc2ec \ub85c\uc9c1 \ubc0f \ubaa8\ub4c8 \uad6c\uc870 \ubb38\uc11c\ud654", "status": "completed", "id": "4"}, {"content": "\uc644\uc804 \uad6c\ud604 \uac00\ub2a5\ud55c \ucf54\ub4dc \uc0d8\ud50c \uc815\ub9ac", "status": "in_progress", "id": "5"}]