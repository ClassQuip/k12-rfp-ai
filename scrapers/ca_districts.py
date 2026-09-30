"""California public school district procurement scraper."""

from __future__ import annotations

from scrapers.district_seeds import CA_DISTRICT_SEEDS
from scrapers.district_sites import DistrictSitesScraper


class CADistrictScraper(DistrictSitesScraper):
    """Crawl seeded CA district sites for bids and RFP PDFs."""

    def __init__(self) -> None:
        super().__init__(state_code="CA", seeds=CA_DISTRICT_SEEDS)
