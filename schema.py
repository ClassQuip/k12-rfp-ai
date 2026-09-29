"""Pydantic schemas for structured RFP extraction."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class RFPAnalysis(BaseModel):
    """Structured metadata extracted from a K-12 procurement RFP document."""

    organization_name: str = Field(
        ...,
        description="District, State Department of Education, or cyber charter name.",
    )
    rfp_title: str = Field(
        ...,
        description="Official bid title or reference / solicitation ID.",
    )
    due_date: Optional[str] = Field(
        default=None,
        description="Response due date as YYYY-MM-DD when known, otherwise raw text.",
    )
    is_k12_relevant: bool = Field(
        ...,
        description=(
            "True if related to virtual classroom, video, LMS, attendance "
            "compliance, or other EdTech software."
        ),
    )
    summary: str = Field(
        ...,
        description="Two to three sentence executive summary of the opportunity.",
    )
    matched_keywords: List[str] = Field(
        default_factory=list,
        description="Keywords that indicate EdTech relevance (e.g. WebRTC, LMS).",
    )
    estimated_value: Optional[str] = Field(
        default=None,
        description="Estimated contract value if stated in the document.",
    )
    submission_instructions: Optional[str] = Field(
        default=None,
        description="How and where to submit proposals.",
    )
    source_url: str = Field(
        ...,
        description="Canonical URL of the scraped RFP or document.",
    )
