"""OpenAI structured extraction for RFP documents."""

from __future__ import annotations

import logging
import os

from openai import OpenAI

from schema import RFPAnalysis

logger = logging.getLogger(__name__)

MAX_INPUT_CHARS = 12_000
SYSTEM_PROMPT = """You are an expert analyst for K-12 EdTech procurement in the United States.
Extract structured metadata from the provided RFP or bid document text.
Set is_k12_relevant to true when the opportunity relates to virtual classroom, video conferencing,
learning management systems (LMS), student information systems, attendance compliance, assessment,
Chromebooks/devices for instruction, cybersecurity for schools, or other educational software/services.
Populate matched_keywords with specific terms found in the document.
Use YYYY-MM-DD for due_date when a clear date is present; otherwise preserve the raw date phrase.
Keep summary to 2-3 concise sentences."""


def extract_rfp_data(raw_text: str, source_url: str) -> RFPAnalysis:
    """
    Parse RFP text with OpenAI Structured Outputs (gpt-4o-mini) into RFPAnalysis.

    Truncates input safely and returns sensible defaults on API or parse errors.
    """
    truncated = _truncate_text(raw_text or "")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        logger.error("OPENAI_API_KEY is not set")
        return _fallback_analysis(
            source_url,
            summary="OpenAI API key missing; extraction skipped.",
        )

    if not truncated.strip():
        return _fallback_analysis(
            source_url,
            summary="No extractable text from document.",
        )

    try:
        client = OpenAI(api_key=api_key)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Source URL: {source_url}\n\n"
                        f"Document text:\n\n{truncated}"
                    ),
                },
            ],
            response_format=RFPAnalysis,
        )
        message = completion.choices[0].message
        if message.parsed is not None:
            parsed = message.parsed
            parsed.source_url = source_url
            return parsed
        logger.warning("OpenAI returned no parsed object; using fallback")
    except Exception as exc:
        logger.exception("OpenAI extraction failed: %s", exc)

    return _fallback_analysis(
        source_url,
        summary="Automated extraction failed; review source document manually.",
    )


def _truncate_text(text: str) -> str:
    if len(text) <= MAX_INPUT_CHARS:
        return text
    head = MAX_INPUT_CHARS // 2
    tail = MAX_INPUT_CHARS - head - 40
    return (
        text[:head]
        + "\n\n[... truncated for token limit ...]\n\n"
        + text[-tail:]
    )


def _fallback_analysis(source_url: str, summary: str) -> RFPAnalysis:
    return RFPAnalysis(
        organization_name="Unknown",
        rfp_title="Untitled RFP",
        due_date=None,
        is_k12_relevant=False,
        summary=summary,
        matched_keywords=[],
        estimated_value=None,
        submission_instructions=None,
        source_url=source_url,
    )
