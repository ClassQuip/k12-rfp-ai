"""Core pipeline: parse PDFs, extract with OpenAI, upload to S3."""

from core.extractor import extract_rfp_data
from core.parser import extract_text_from_pdf
from core.s3_uploader import S3Storage

__all__ = ["extract_rfp_data", "extract_text_from_pdf", "S3Storage"]
