"""Portal-specific scrapers for K-12 procurement sites."""

from scrapers.base import BaseScraper, ScrapedOpportunity
from scrapers.ca_districts import CADistrictScraper
from scrapers.tn_districts import TNDistrictScraper

SCRAPER_REGISTRY: dict[str, type[BaseScraper]] = {
    "tn_districts": TNDistrictScraper,
    "ca_districts": CADistrictScraper,
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
    "SCRAPER_REGISTRY",
    "get_scrapers_for_state",
]
