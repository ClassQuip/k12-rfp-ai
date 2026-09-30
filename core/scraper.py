"""High-level scraping orchestration helpers."""

from __future__ import annotations

import logging
from typing import Iterator

from core.parser import extract_text_from_pdf
from scrapers.base import BaseScraper, ScrapedOpportunity

logger = logging.getLogger(__name__)


def gather_document_text(scraper: BaseScraper, opportunity: ScrapedOpportunity) -> str:
    """
    Build a single text blob from HTML snippet and downloaded PDF/HTML documents.
    """
    parts: list[str] = []
    if opportunity.html_snippet:
        parts.append(opportunity.html_snippet)
    if opportunity.title:
        parts.append(f"Title: {opportunity.title}")
    if opportunity.organization_name:
        parts.append(f"Organization: {opportunity.organization_name}")

    urls = list(opportunity.document_urls)
    if opportunity.detail_url and opportunity.detail_url not in urls:
        urls.insert(0, opportunity.detail_url)

    for url in urls[:5]:
        content, content_type = scraper.download_document(url)
        if not content:
            continue
        if (
            "pdf" in content_type
            or url.lower().endswith(".pdf")
            or "/fs/resource-manager/view/" in url
            or "cloudfront.net" in url
        ):
            pdf_text = extract_text_from_pdf(content)
            if pdf_text:
                parts.append(pdf_text)
        elif "html" in content_type or content_type.startswith("text/"):
            try:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(content.decode("utf-8", errors="replace"), "lxml")
                parts.append(soup.get_text("\n", strip=True)[:8000])
            except Exception as exc:
                logger.debug("HTML parse skip for %s: %s", url, exc)

    return "\n\n".join(parts)


def iter_scraper_opportunities(scraper: BaseScraper) -> Iterator[ScrapedOpportunity]:
    """Safely iterate fetch_opportunities with logging."""
    logger.info(
        "Running scraper %s (%s)",
        scraper.portal_name,
        scraper.state_code,
    )
    try:
        yield from scraper.fetch_opportunities()
    except Exception as exc:
        logger.exception("Scraper %s failed: %s", scraper.portal_name, exc)
