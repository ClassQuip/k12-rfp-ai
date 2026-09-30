#!/usr/bin/env python3
"""CLI orchestrator for K-12 RFP crawling, extraction, and S3 upload."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from dotenv import load_dotenv

from core.extractor import extract_rfp_data
from core.s3_uploader import S3Storage
from core.scraper import gather_document_text, iter_scraper_opportunities
from scrapers import get_scrapers_for_state

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("k12-rfp-ai")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crawl K-12 procurement portals, extract RFP metadata with AI, upload to S3.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--state",
        type=str,
        help="Two-letter state code to run matching scrapers only (e.g. PA).",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Run all registered scrapers.",
    )
    parser.add_argument(
        "--include-non-relevant",
        action="store_true",
        help="Print and upload all RFPs, not only K-12-relevant matches.",
    )
    parser.add_argument(
        "--max-per-scraper",
        type=int,
        default=int(os.getenv("MAX_OPPORTUNITIES_PER_SCRAPER", "10")),
        help="Cap opportunities processed per scraper (default: 10).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = None if args.all else args.state
    scrapers = get_scrapers_for_state(state)

    if not scrapers:
        logger.error("No scrapers found for state=%s", state)
        return 1

    skip_s3 = os.getenv("SKIP_S3_UPLOAD", "0").strip() in ("1", "true", "yes")
    storage = S3Storage() if not skip_s3 else None

    relevant_count = 0
    processed = 0

    for scraper in scrapers:
        count = 0
        for opportunity in iter_scraper_opportunities(scraper):
            if count >= args.max_per_scraper:
                break
            count += 1
            processed += 1

            raw_text = gather_document_text(scraper, opportunity)
            source_url = opportunity.detail_url or (
                opportunity.document_urls[0] if opportunity.document_urls else ""
            )
            if not source_url:
                logger.warning("Skipping opportunity without URL: %s", opportunity.title)
                continue

            analysis = extract_rfp_data(raw_text, source_url)
            if opportunity.organization_name and analysis.organization_name == "Unknown":
                analysis = analysis.model_copy(
                    update={"organization_name": opportunity.organization_name}
                )
            if opportunity.title and analysis.rfp_title == "Untitled RFP":
                analysis = analysis.model_copy(update={"rfp_title": opportunity.title})

            show = analysis.is_k12_relevant or args.include_non_relevant
            if analysis.is_k12_relevant:
                relevant_count += 1
                _print_relevant_rfp(analysis)

            if storage and show:
                meta = {
                    "portal": scraper.portal_name,
                    "state": scraper.state_code,
                    "detail_url": opportunity.detail_url,
                }
                storage.upload_rfp_json(analysis, extra=meta)
                for doc_url in opportunity.document_urls[:3]:
                    pdf_bytes, ctype = scraper.download_document(doc_url)
                    if pdf_bytes and (
                        "pdf" in ctype
                        or doc_url.lower().endswith(".pdf")
                        or "/fs/resource-manager/view/" in doc_url
                        or "cloudfront.net" in doc_url
                    ):
                        storage.upload_pdf(
                            pdf_bytes,
                            analysis.organization_name,
                            analysis.rfp_title,
                        )
                    elif pdf_bytes and "html" in ctype:
                        text = gather_document_text(scraper, opportunity)
                        if text:
                            storage.upload_rfp_json(
                                analysis.model_copy(
                                    update={"summary": analysis.summary + " [HTML doc]"}
                                ),
                                extra={**meta, "html_source": doc_url},
                            )

    logger.info(
        "Done. Processed %s opportunities; %s K-12-relevant.",
        processed,
        relevant_count,
    )
    return 0


def _print_relevant_rfp(analysis) -> None:
    """Emit compact JSON for relevant RFPs to stdout."""
    payload = analysis.model_dump()
    print(json.dumps(payload, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    sys.exit(main())
