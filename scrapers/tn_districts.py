"""Tennessee public school district procurement scraper."""

from __future__ import annotations

from scrapers.district_seeds import TN_DISTRICT_SEEDS
from scrapers.district_sites import DistrictSitesScraper


class TNDistrictScraper(DistrictSitesScraper):
    """Crawl seeded TN district sites for bids and RFP PDFs."""

    def __init__(self) -> None:
        super().__init__(state_code="TN", seeds=TN_DISTRICT_SEEDS)
