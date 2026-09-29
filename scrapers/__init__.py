"""Portal-specific scrapers for K-12 procurement sites."""

from scrapers.base import BaseScraper, ScrapedOpportunity
from scrapers.sample_portal import SamplePortalScraper

SCRAPER_REGISTRY: dict[str, type[BaseScraper]] = {
    "sample": SamplePortalScraper,
}


def get_scrapers_for_state(state: str | None) -> list[BaseScraper]:
    """Instantiate scrapers filtered by state code (case-insensitive) or all."""
    instances: list[BaseScraper] = []
    for cls in SCRAPER_REGISTRY.values():
        scraper = cls()
        if state is None or scraper.state_code.upper() == state.upper():
            instances.append(scraper)
    return instances


__all__ = [
    "BaseScraper",
    "ScrapedOpportunity",
    "SamplePortalScraper",
    "SCRAPER_REGISTRY",
    "get_scrapers_for_state",
]
