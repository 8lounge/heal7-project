"""
파일 검증 원자 모듈 (Atomic File Validation Module)
목적: 업로드된 파일의 유효성을 검증하는 단일 책임 모듈
사용법: validate_file(file_data, filename) -> ValidationResult
"""

from typing import NamedTuple, Optional, Dict, Any
import magic
import fitz  # PyMuPDF
from PIL import Image
import io
import hashlib


class ValidationResult(NamedTuple):
    """파일 검증 결과"""
    is_valid: bool
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class FileValidator:
    """
    파일 검증기 - 단일 책임 원칙 적용
    
    책임:
    1. 파일 크기 검증
    2. 파일 형식 검증  
    3. PDF 페이지 수 검증 (10페이지 미만만 허용)
    4. 파일 무결성 검증
    """
    
    # 상수 정의
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_PAGES = 9  # 10페이지 미만만 허용
    
    SUPPORTED_FORMATS = {
        'pdf': ['application/pdf'],
        'doc': ['application/msword'],
        'docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        'jpg': ['image/jpeg'],
        'png': ['image/png']
    }
    
    def __init__(self):
        """초기화 - MIME 타입 검사기 준비"""
        try:
            self.magic_mime = magic.Magic(mime=True)
        except Exception:
            # python-magic이 없는 경우 대체 방법 사용
            self.magic_mime = None
    
    def validate_file(self, file_data: bytes, filename: str) -> ValidationResult:
        """
        파일 검증 메인 함수
        
        Args:
            file_data: 파일의 바이너리 데이터
            filename: 파일명
            
        Returns:
            ValidationResult: 검증 결과 (성공/실패, 오류 메시지, 메타데이터)
        """
        try:
            # 1. 기본 검증
            basic_check = self._validate_basic(file_data, filename)
            if not basic_check.is_valid:
                return basic_check
            
            # 2. 파일 형식 검증
            file_type = self._get_file_type(filename)
            format_check = self._validate_format(file_data, file_type)
            if not format_check.is_valid:
                return format_check
            
            # 3. 메타데이터 추출
            metadata = self._extract_metadata(file_data, file_type)
            
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
        """기본 검증: 크기, 파일명, 확장자"""
        
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
    
    def _get_file_type(self, filename: str) -> str:
        """파일명에서 파일 타입 추출"""
        extension = filename.split('.')[-1].lower()
        return extension
    
    def _validate_format(self, file_data: bytes, file_type: str) -> ValidationResult:
        """형식별 상세 검증"""
        
        if file_type == 'pdf':
            return self._validate_pdf(file_data)
        elif file_type in ['jpg', 'png']:
            return self._validate_image(file_data)
        elif file_type in ['doc', 'docx']:
            return self._validate_word(file_data)
        
        return ValidationResult(True)
    
    def _validate_pdf(self, file_data: bytes) -> ValidationResult:
        """PDF 파일 검증"""
        
        try:
            doc = fitz.open(stream=file_data, filetype="pdf")
            
            # 페이지 수 검증 - 핵심 비즈니스 로직
            page_count = doc.page_count
            if page_count >= 10:  # 10페이지 이상 거부
                doc.close()
                return ValidationResult(
                    False,
                    f"파일이 너무 큽니다. 10페이지 미만의 문서만 업로드 가능합니다. (현재: {page_count}페이지)"
                )
            
            # PDF 무결성 검증
            try:
                # 첫 번째 페이지 렌더링 테스트
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.1, 0.1))  # 작은 해상도로 테스트
                pix = None  # 메모리 해제
            except Exception:
                doc.close()
                return ValidationResult(False, "PDF 파일이 손상되었습니다.")
            
            # 암호화 검증
            if doc.needs_pass:
                doc.close()
                return ValidationResult(False, "암호화된 PDF 파일은 지원하지 않습니다.")
            
            doc.close()
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(False, f"PDF 파일 형식이 올바르지 않습니다: {str(e)}")
    
    def _validate_image(self, file_data: bytes) -> ValidationResult:
        """이미지 파일 검증"""
        
        try:
            image = Image.open(io.BytesIO(file_data))
            
            # 이미지 크기 검증
            width, height = image.size
            
            if width < 100 or height < 100:
                return ValidationResult(
                    False,
                    f"이미지 크기가 너무 작습니다. 최소 100x100px 이상이어야 합니다. (현재: {width}x{height}px)"
                )
            
            if width > 5000 or height > 5000:
                return ValidationResult(
                    False,
                    f"이미지 크기가 너무 큽니다. 최대 5000x5000px까지 지원합니다. (현재: {width}x{height}px)"
                )
            
            # 이미지 무결성 검증
            try:
                image.verify()
            except Exception:
                return ValidationResult(False, "손상된 이미지 파일입니다.")
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(False, f"이미지 파일 형식이 올바르지 않습니다: {str(e)}")
    
    def _validate_word(self, file_data: bytes) -> ValidationResult:
        """Word 문서 검증"""
        
        try:
            # python-docx를 사용한 기본 검증
            from docx import Document
            
            doc = Document(io.BytesIO(file_data))
            
            # 문서 구조 기본 검증
            paragraph_count = len(doc.paragraphs)
            if paragraph_count == 0:
                return ValidationResult(False, "빈 Word 문서입니다.")
            
            # 대략적인 페이지 수 추정
            estimated_pages = max(1, paragraph_count // 10)  # 단락 10개당 1페이지로 추정
            if estimated_pages >= 10:
                return ValidationResult(
                    False,
                    f"문서가 너무 깁니다. 예상 페이지 수: {estimated_pages}페이지 (10페이지 미만만 허용)"
                )
            
            return ValidationResult(True)
            
        except Exception as e:
            return ValidationResult(False, f"Word 문서 형식이 올바르지 않습니다: {str(e)}")
    
    def _extract_metadata(self, file_data: bytes, file_type: str) -> Dict[str, Any]:
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
                })
                doc.close()
                
            elif file_type in ['jpg', 'png']:
                image = Image.open(io.BytesIO(file_data))
                metadata.update({
                    'width': image.size[0],
                    'height': image.size[1],
                    'mode': image.mode,
                })
                
        except Exception as e:
            metadata['metadata_extraction_error'] = str(e)
        
        return metadata


# 편의 함수 - 모듈 외부에서 간단하게 사용할 수 있도록
def validate_file(file_data: bytes, filename: str) -> ValidationResult:
    """
    파일 검증 편의 함수
    
    Usage:
        result = validate_file(file_data, "document.pdf")
        if result.is_valid:
            print("파일이 유효합니다.")
            print(f"메타데이터: {result.metadata}")
        else:
            print(f"오류: {result.error_message}")
    """
    validator = FileValidator()
    return validator.validate_file(file_data, filename)


# 테스트 코드 (개발 시에만 실행)
if __name__ == "__main__":
    # 테스트용 더미 데이터
    test_cases = [
        # (파일 데이터, 파일명, 예상 결과)
        (b"", "empty.pdf", False),  # 빈 파일
        (b"x" * (11 * 1024 * 1024), "large.pdf", False),  # 너무 큰 파일
        (b"dummy pdf data", "test.txt", False),  # 지원하지 않는 형식
        (b"valid pdf content", "test.pdf", True),  # 유효한 파일 (실제로는 PDF 검증 필요)
    ]
    
    validator = FileValidator()
    
    for file_data, filename, expected in test_cases:
        result = validator.validate_file(file_data, filename)
        status = "✓" if result.is_valid == expected else "✗"
        print(f"{status} {filename}: {result.error_message or 'Valid'}")