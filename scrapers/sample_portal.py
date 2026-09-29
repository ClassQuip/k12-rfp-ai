"""Sample scraper using httpx + BeautifulSoup (crawl4ai optional for JS-heavy pages)."""

from __future__ import annotations

import logging
import re
from typing import Iterator
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from scrapers.base import BaseScraper, ScrapedOpportunity

logger = logging.getLogger(__name__)

# Public procurement listing with linked PDF RFPs (demo / integration test target).
SAMPLE_LIST_URL = "https://www.bidnetdirect.com/public/solicitations"
FALLBACK_DEMO_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"


class SamplePortalScraper(BaseScraper):
    """
    Demonstration scraper: fetches HTML via httpx, parses links, detects PDFs.

    For production, copy this module per state/district and set list_url + selectors.
    """

    state_code = "PA"
    portal_name = "sample_portal"

    def __init__(
        self,
        list_url: str = SAMPLE_LIST_URL,
        timeout: float = 30.0,
        user_agent: str = "k12-rfp-ai/1.0 (+https://github.com/classquip/k12-rfp-ai)",
    ) -> None:
        self.list_url = list_url
        self.timeout = timeout
        self.headers = {"User-Agent": user_agent}

    def fetch_opportunities(self) -> Iterator[ScrapedOpportunity]:
        html = self._fetch_html(self.list_url)
        if not html:
            logger.warning(
                "Could not fetch %s; yielding synthetic demo opportunity",
                self.list_url,
            )
            yield ScrapedOpportunity(
                title="Demo EdTech LMS Virtual Classroom RFP",
                detail_url=FALLBACK_DEMO_URL,
                organization_name="Sample K-12 School District",
                document_urls=[FALLBACK_DEMO_URL],
                html_snippet="Virtual classroom LMS attendance compliance software bid.",
                state_code=self.state_code,
            )
            return

        soup = BeautifulSoup(html, "lxml")
        seen: set[str] = set()

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()
            if not href or href.startswith("#"):
                continue
            absolute = urljoin(self.list_url, href)
            if absolute in seen:
                continue
            seen.add(absolute)

            title = anchor.get_text(strip=True) or "Untitled solicitation"
            if len(title) < 5:
                continue

            pdf_links = self._pdf_links_near(anchor, self.list_url)
            if not pdf_links and self._looks_like_pdf(absolute):
                pdf_links = [absolute]

            yield ScrapedOpportunity(
                title=title[:500],
                detail_url=absolute,
                organization_name=self._guess_organization(soup, title),
                document_urls=pdf_links,
                html_snippet=anchor.parent.get_text(" ", strip=True)[:2000]
                if anchor.parent
                else "",
                state_code=self.state_code,
            )

            if len(seen) >= 25:
                break

    def download_document(self, url: str) -> tuple[bytes | None, str]:
        try:
            with httpx.Client(
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                response = client.get(url)
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").split(";")[0]
                if not content_type:
                    content_type = (
                        "application/pdf"
                        if url.lower().endswith(".pdf")
                        else "text/html"
                    )
                return response.content, content_type
        except httpx.HTTPError as exc:
            logger.warning("Download failed for %s: %s", url, exc)
            return None, ""

    def _fetch_html(self, url: str) -> str | None:
        try:
            with httpx.Client(
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                response = client.get(url)
                response.raise_for_status()
                ctype = response.headers.get("content-type", "")
                if "html" not in ctype.lower() and not response.text.strip().startswith(
                    "<"
                ):
                    return None
                return response.text
        except httpx.HTTPError as exc:
            logger.info("httpx fetch failed (%s), trying crawl4ai if available", exc)
            return self._fetch_html_crawl4ai(url)

    def _fetch_html_crawl4ai(self, url: str) -> str | None:
        try:
            import asyncio

            from crawl4ai import AsyncWebCrawler

            async def _run() -> str:
                async with AsyncWebCrawler(verbose=False) as crawler:
                    result = await crawler.arun(url=url)
                    return result.markdown or result.html or ""

            return asyncio.run(_run()) or None
        except Exception as exc:
            logger.debug("crawl4ai unavailable or failed: %s", exc)
            return None

    @staticmethod
    def _looks_like_pdf(url: str) -> bool:
        path = urlparse(url).path.lower()
        return path.endswith(".pdf") or "pdf" in path

    @staticmethod
    def _pdf_links_near(anchor, base_url: str) -> list[str]:
        pdfs: list[str] = []
        parent = anchor.find_parent(["tr", "li", "div", "article"])
        if not parent:
            return pdfs
        for link in parent.find_all("a", href=True):
            href = urljoin(base_url, link["href"])
            if SamplePortalScraper._looks_like_pdf(href):
                pdfs.append(href)
        return pdfs

    @staticmethod
    def _guess_organization(soup: BeautifulSoup, title: str) -> str:
        for tag in ("h1", "title"):
            el = soup.find(tag)
            if el and el.get_text(strip=True):
                text = el.get_text(strip=True)
                if "bid" not in text.lower()[:10]:
                    return text[:200]
        match = re.search(
            r"([A-Z][\w\s]+(?:School District|ISD|USD|County|Department of Education))",
            title,
        )
        if match:
            return match.group(1).strip()
        return "Unknown Organization"
