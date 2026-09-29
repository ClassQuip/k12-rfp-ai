"""Extract plain text from PDF byte payloads."""

from __future__ import annotations

import io
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract readable text from raw PDF bytes using pypdf, with pdfplumber fallback.

    Returns an empty string if no text could be extracted or on failure.
    """
    if not pdf_bytes:
        return ""

    text = _extract_with_pypdf(pdf_bytes)
    if text.strip():
        return _normalize_whitespace(text)

    text = _extract_with_pdfplumber(pdf_bytes)
    return _normalize_whitespace(text)


def _extract_with_pypdf(pdf_bytes: bytes) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(pdf_bytes))
        parts: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                parts.append(page_text)
        return "\n".join(parts)
    except Exception as exc:
        logger.debug("pypdf extraction failed: %s", exc)
        return ""


def _extract_with_pdfplumber(pdf_bytes: bytes) -> str:
    try:
        import pdfplumber

        parts: list[str] = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    parts.append(page_text)
        return "\n".join(parts)
    except Exception as exc:
        logger.warning("pdfplumber extraction failed: %s", exc)
        return ""


def _normalize_whitespace(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)
