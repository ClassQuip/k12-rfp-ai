"""Crawl public school district sites for bid/RFP documents."""

from __future__ import annotations

import logging
import os
import random
import re
from typing import Iterator
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from scrapers.base import BaseScraper, ScrapedOpportunity
from scrapers.district_seeds import DistrictSeed
from scrapers.http_tools import DEFAULT_USER_AGENT, download_bytes, fetch_html

logger = logging.getLogger(__name__)

PROCUREMENT_TEXT = re.compile(
    r"\b(rfp|rfq|ifb|bid|bids|solicit|proposal|procurement|purchasing|"
    r"invitation\s+to\s+bid|specification|vendor|contract)\b",
    re.I,
)

EXCLUDE_TEXT = re.compile(
    r"\b(handbook|bell\s*time|district\s+map|calendar|nondiscrimination|"
    r"parent\s+portal|report\s+card|user\s+manual|master\s+plan|"
    r"graduation\s+schedule|organizational\s+chart|benefits|dental|vision)\b",
    re.I,
)

FOLLOW_PATH = re.compile(
    r"(bid|rfp|solicit|procurement|purchasing|business[- ]?office|"
    r"finance|vendor|open-rfp|invitation-to-bid|contracts?)",
    re.I,
)


class DistrictSitesScraper(BaseScraper):
    """
    Walk district procurement pages (same registrable domain), collect PDFs and
    Finalsite resource-manager documents linked from bid/RFP pages.
    """

    portal_name = "district_sites"

    def __init__(
        self,
        state_code: str,
        seeds: list[DistrictSeed],
        *,
        shuffle_seeds: bool = True,
        max_pages_per_district: int | None = None,
        max_depth: int | None = None,
        max_opportunities: int | None = None,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.state_code = state_code
        self.seeds = [s for s in seeds if s.state_code.upper() == state_code.upper()]
        self.shuffle_seeds = shuffle_seeds
        self.max_pages_per_district = max_pages_per_district or int(
            os.getenv("DISTRICT_MAX_PAGES", "12")
        )
        self.max_depth = max_depth or int(os.getenv("DISTRICT_MAX_DEPTH", "2"))
        self.max_opportunities = max_opportunities or int(
            os.getenv("DISTRICT_MAX_OPPORTUNITIES", "120")
        )
        self.max_opportunities_per_seed = int(
            os.getenv("DISTRICT_MAX_OPPORTUNITIES_PER_SEED", "8")
        )
        self.user_agent = user_agent
        self.portal_name = f"district_sites_{state_code.lower()}"

    def fetch_opportunities(self) -> Iterator[ScrapedOpportunity]:
        seeds = list(self.seeds)
        if self.shuffle_seeds:
            random.shuffle(seeds)

        seen_docs: set[str] = set()
        yielded = 0

        for seed in seeds:
            if yielded >= self.max_opportunities:
                break
            per_seed = 0
            for opp in self._crawl_district(seed):
                key = opp.detail_url
                if key in seen_docs:
                    continue
                seen_docs.add(key)
                yielded += 1
                per_seed += 1
                yield opp
                if yielded >= self.max_opportunities:
                    break
                if per_seed >= self.max_opportunities_per_seed:
                    break

    def _crawl_district(self, seed: DistrictSeed) -> Iterator[ScrapedOpportunity]:
        registrable = _registrable_domain(seed.entry_urls[0])
        queue: list[tuple[str, int]] = [(url, 0) for url in seed.entry_urls]
        visited: set[str] = set()
        pages_fetched = 0

        while queue and pages_fetched < self.max_pages_per_district:
            page_url, depth = queue.pop(0)
            if page_url in visited:
                continue
            visited.add(page_url)

            html = fetch_html(page_url, user_agent=self.user_agent)
            if not html:
                continue
            pages_fetched += 1

            soup = BeautifulSoup(html, "lxml")
            for opp in _extract_opportunities(soup, page_url, seed):
                yield opp

            if depth >= self.max_depth:
                continue

            for link in _follow_links(soup, page_url, registrable):
                if link not in visited:
                    queue.append((link, depth + 1))

    def download_document(self, url: str) -> tuple[bytes | None, str]:
        return download_bytes(url, user_agent=self.user_agent)


def _extract_opportunities(
    soup: BeautifulSoup,
    page_url: str,
    seed: DistrictSeed,
) -> Iterator[ScrapedOpportunity]:
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith("#") or href.lower().startswith("mailto:"):
            continue

        absolute = urljoin(page_url, href)
        text = anchor.get_text(" ", strip=True)
        combined = f"{text} {absolute}"

        if EXCLUDE_TEXT.search(combined):
            continue

        if not _is_procurement_asset(absolute, text):
            continue

        title = text or _title_from_url(absolute)
        document_urls = [absolute]
        snippet = _snippet_from_anchor(anchor)

        yield ScrapedOpportunity(
            title=title[:500],
            detail_url=absolute,
            organization_name=seed.organization_name,
            document_urls=document_urls,
            html_snippet=snippet,
            state_code=seed.state_code,
        )


def _is_procurement_asset(url: str, link_text: str) -> bool:
    lower_url = url.lower()
    combined = f"{link_text} {url}"

    if "/fs/resource-manager/view/" in lower_url:
        return bool(PROCUREMENT_TEXT.search(link_text)) and not EXCLUDE_TEXT.search(
            link_text
        )

    if (
        "cloudfront.net" in lower_url
        and PROCUREMENT_TEXT.search(combined)
        and not EXCLUDE_TEXT.search(combined)
    ):
        return True

    if (
        "/media/" in lower_url
        and PROCUREMENT_TEXT.search(combined)
        and not EXCLUDE_TEXT.search(combined)
    ):
        return True

    if lower_url.endswith(".pdf") or ".pdf?" in lower_url:
        if EXCLUDE_TEXT.search(combined):
            return False
        if PROCUREMENT_TEXT.search(combined):
            return True
        if any(
            part in lower_url
            for part in (
                "/procurement/",
                "/purchasing/",
                "/business-office/",
                "/bid",
                "/rfp",
                "/media/",
            )
        ):
            return True
        if re.search(r"\b(RFP|RFQ|IFB|Bid)[-_#\d]", url, re.I):
            return True
        return False

    if re.search(r"/(RFP|RFQ|IFB|Bid)[^/]*\.pdf", url, re.I):
        return True

    return False


def _follow_links(
    soup: BeautifulSoup,
    page_url: str,
    registrable: str,
) -> list[str]:
    links: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith("#"):
            continue
        absolute = urljoin(page_url, href)
        parsed = urlparse(absolute)
        if _registrable_domain(absolute) != registrable:
            continue
        path_query = f"{parsed.path}?{parsed.query}"
        text = anchor.get_text(" ", strip=True)
        if FOLLOW_PATH.search(path_query) or PROCUREMENT_TEXT.search(text):
            if "drive.google.com" in absolute:
                links.append(absolute)
            elif not absolute.lower().endswith(".pdf"):
                links.append(absolute)
    return links


def _snippet_from_anchor(anchor) -> str:
    parent = anchor.find_parent(["li", "tr", "p", "div", "article"])
    if not parent:
        return anchor.get_text(" ", strip=True)[:2000]
    return parent.get_text(" ", strip=True)[:2000]


def _title_from_url(url: str) -> str:
    path = urlparse(url).path
    name = path.rsplit("/", 1)[-1] if path else "District procurement document"
    return name.replace("-", " ").replace("_", " ")[:200]


def _registrable_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host
