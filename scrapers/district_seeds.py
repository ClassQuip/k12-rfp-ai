"""Curated entry points for K-12 district procurement / bid pages."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DistrictSeed:
    """One school district (or charter authorizer) procurement crawl target."""

    organization_name: str
    state_code: str
    entry_urls: list[str] = field(default_factory=list)


# Verified or reachable HTTP entry points. Add districts here; crawl logic lives in district_sites.py.
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
        organization_name="Hamilton County Schools",
        state_code="TN",
        entry_urls=[
            "https://hcde.org/finance/purchasing/",
        ],
    ),
    DistrictSeed(
        organization_name="Blount County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.blountk12.org/departments/finance/purchasing",
            "https://www.blountk12.org/about-us/departments/finance/invitation-to-bid",
        ],
    ),
    DistrictSeed(
        organization_name="Arlington Community Schools",
        state_code="TN",
        entry_urls=[
            "https://www.acsk12.org/about/departments/finance/invitation-to-bid",
        ],
    ),
    DistrictSeed(
        organization_name="Bristol Tennessee City Schools",
        state_code="TN",
        entry_urls=[
            "https://www.btcs.org/about/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Cleveland City Schools",
        state_code="TN",
        entry_urls=[
            "https://www.clevelandschools.org/about/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Dickson County Schools",
        state_code="TN",
        entry_urls=[
            "https://www.dcstn.org/about/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Collierville Schools",
        state_code="TN",
        entry_urls=[
            "https://www.colliervilleschools.org/departments/finance/purchasing",
            "https://www.colliervilleschools.org/about/departments/finance/invitation-to-bid",
        ],
    ),
    DistrictSeed(
        organization_name="Bartlett City Schools",
        state_code="TN",
        entry_urls=[
            "https://www.bartlettschools.org/departments/finance/purchasing",
            "https://www.bartlettschools.org/about-us/departments/finance/invitation-to-bid",
        ],
    ),
    DistrictSeed(
        organization_name="Germantown Municipal School District",
        state_code="TN",
        entry_urls=[
            "https://www.gmsdk12.org/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Maryville City Schools",
        state_code="TN",
        entry_urls=[
            "https://www.maryville-schools.org/about/departments/finance/invitation-to-bid",
            "https://www.maryville-schools.org/departments/finance/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Johnson City Schools",
        state_code="TN",
        entry_urls=[
            "https://www.jcschools.org/about-us/departments/finance/purchasing",
            "https://www.jcschools.org/about-us/departments/finance/invitation-to-bid",
        ],
    ),
    DistrictSeed(
        organization_name="Kingsport City Schools",
        state_code="TN",
        entry_urls=[
            "https://www.k12k.com/about/departments/finance/purchasing",
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
        organization_name="Garden Grove Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.ggusd.us/departments/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Orange Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.orangeusd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="San Dieguito Union High School District",
        state_code="CA",
        entry_urls=[
            "https://www.sduhsd.net/departments/business-services/purchasing/",
        ],
    ),
    DistrictSeed(
        organization_name="Manhattan Beach Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.mbusd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Glendale Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.gusd.net/departments/business-services/purchasing",
            "https://www.gusd.net/departments/business-services/purchasing/bids",
        ],
    ),
    DistrictSeed(
        organization_name="Grossmont Union High School District",
        state_code="CA",
        entry_urls=[
            "https://www.guhsd.net/departments/business-services/purchasing/",
        ],
    ),
    DistrictSeed(
        organization_name="Riverside Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.rusd.org/departments/business-services/purchasing",
            "https://www.rusd.org/departments/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="San Marcos Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.smusd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Chino Valley Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.chino.k12.ca.us/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Clovis Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.cusd.com/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Modesto City Schools",
        state_code="CA",
        entry_urls=[
            "https://www.mcs4kids.com/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Anaheim Union High School District",
        state_code="CA",
        entry_urls=[
            "https://www.auhsd.us/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Los Angeles Unified School District",
        state_code="CA",
        entry_urls=[
            "https://achieve.lausd.net/purchasing",
            "https://www.lausd.org/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="San Diego Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.sandiegounified.org/departments/business_services/purchasing",
            "https://www.sandiegounified.org/about/business_services/procurement_and_contracts",
        ],
    ),
    DistrictSeed(
        organization_name="Sacramento City Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.scusd.edu/department/purchasing-warehouse",
            "https://www.scusd.edu/department/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Oakland Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.ousd.org/departments/business-services/contracts-and-procurement",
            "https://www.ousd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Elk Grove Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.egusd.net/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Twin Rivers Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.twinriversusd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="West Contra Costa Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.wccusd.net/departments/business-services/purchasing-department",
            "https://www.wccusd.net/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Mt. Diablo Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.mdusd.org/departments/business-services/purchasing",
        ],
    ),
    DistrictSeed(
        organization_name="Palo Alto Unified School District",
        state_code="CA",
        entry_urls=[
            "https://www.pausd.org/departments/business-services/purchasing",
        ],
    ),
]
