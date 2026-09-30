"""Curated entry points for K-12 district procurement / bid pages."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DistrictSeed:
    """One school district (or charter authorizer) procurement crawl target."""

    organization_name: str
    state_code: str
    entry_urls: list[str] = field(default_factory=list)


# Verified HTTP 200 entry points (Sep 2026). Expand by adding seeds, not hard-coded logic.
TN_DISTRICT_SEEDS: list[DistrictSeed] = [
    DistrictSeed(
        organization_name="Memphis-Shelby County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.scsk12.org/procurement",
            "https://www.scsk12.org/procurement25/?PN=232",
        ],
    ),
    DistrictSeed(
        organization_name="Oak Ridge Schools",
        state_code="TN",
        entry_urls=[
            "https://www.ortn.edu/central-office/business-and-operations/bid-information/",
            "https://www.ortn.edu/central-office/business-and-operations/open-rfps/",
        ],
    ),
    DistrictSeed(
        organization_name="Wilson County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.wcschools.com/departments/finance/bidrfp-information",
        ],
    ),
    DistrictSeed(
        organization_name="Sumner County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.sumnerschools.org/about-us/departments/finance/invitation-to-bid",
        ],
    ),
    DistrictSeed(
        organization_name="Rutherford County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.rcschools.net/departments/finance/purchasing/bids",
            "https://www.rcschools.net/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Knox County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.knoxschools.org/about/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Hamilton County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.hcde.org/about/business-and-operations/purchasing",
        ],
    ),
]

CA_DISTRICT_SEEDS: list[DistrictSeed] = [
    DistrictSeed(
        organization_name="Fresno Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.fresnounified.org/departments/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Irvine Unified School District",
        state_code="CA",
        entry_urls=[
            "https://iusd.org/department/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Newport-Mesa Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.nmusd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Los Angeles Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.lausd.org/site/default.aspx?PageType=1&SiteID=4&ChannelID=58",
        ],
    ),
    DistrictSeed(
        organization_name="San Diego Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.sandiegounified.org/about/business_services/procurement_and_contracts",
        ],
    ),
    DistrictSeed(
        organization_name="Sacramento City Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.scusd.edu/department/purchasing-warehouse",
        ],
    ),
    DistrictSeed(
        organization_name="Oakland Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.ousd.org/departments/business-services/contracts-and-procurement",
        ],
    ),
]
