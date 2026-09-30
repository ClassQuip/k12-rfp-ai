"""Shared HTTP helpers for portal and district scrapers."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; k12-rfp-ai/1.0; +https://github.com/classquip/k12-rfp-ai)"
)


def fetch_html(
    url: str,
    *,
    timeout: float = 30.0,
    user_agent: str = DEFAULT_USER_AGENT,
) -> str | None:
    headers = {"User-Agent": user_agent}
    try:
        with httpx.Client(
            headers=headers,
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            ctype = response.headers.get("content-type", "")
            if "html" not in ctype.lower() and not response.text.strip().startswith("<"):
                return None
            return response.text
    except httpx.HTTPError as exc:
        logger.debug("fetch_html failed for %s: %s", url, exc)
        return None


def download_bytes(
    url: str,
    *,
    timeout: float = 45.0,
    user_agent: str = DEFAULT_USER_AGENT,
) -> tuple[bytes | None, str]:
    headers = {"User-Agent": user_agent}
    try:
        with httpx.Client(
            headers=headers,
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").split(";")[0].strip()
            if not content_type:
                if url.lower().endswith(".pdf"):
                    content_type = "application/pdf"
                elif "/fs/resource-manager/view/" in url:
                    content_type = "application/pdf"
                else:
                    content_type = "text/html"
            return response.content, content_type
    except httpx.HTTPError as exc:
        logger.warning("download_bytes failed for %s: %s", url, exc)
        return None, ""
