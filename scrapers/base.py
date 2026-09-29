"""Abstract base for district / state procurement portal scrapers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class ScrapedOpportunity:
    """One procurement listing discovered by a scraper."""

    title: str
    detail_url: str
    organization_name: str
    document_urls: list[str] = field(default_factory=list)
    html_snippet: str = ""
    state_code: str = ""


class BaseScraper(ABC):
    """
    Subclasses implement portal-specific HTML/API logic.

    state_code: two-letter US state (or 'US' for national portals).
    portal_name: human-readable identifier for logs and S3 metadata.
    """

    state_code: str = "US"
    portal_name: str = "base"

    @abstractmethod
    def fetch_opportunities(self) -> Iterator[ScrapedOpportunity]:
        """Yield opportunities found on the portal listing page(s)."""
        ...

    @abstractmethod
    def download_document(self, url: str) -> tuple[bytes | None, str]:
        """
        Download a document from url.

        Returns (content_bytes, content_type) where content_type is a MIME hint
        such as 'application/pdf' or 'text/html'. content_bytes may be None on failure.
        """
        ...
