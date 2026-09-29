"""Upload RFP JSON records and PDF binaries to a private S3 bucket."""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import date, datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError

from schema import RFPAnalysis

logger = logging.getLogger(__name__)


def slugify(value: str, max_length: int = 80) -> str:
    """Create a safe S3 key segment from arbitrary text."""
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    value = value.strip("-")
    if not value:
        value = "unknown"
    return value[:max_length]


class S3Storage:
    """Store extracted RFP metadata and source PDFs in S3."""

    def __init__(
        self,
        bucket_name: str | None = None,
        region_name: str | None = None,
    ) -> None:
        self.bucket_name = bucket_name or os.getenv("AWS_S3_BUCKET_NAME", "")
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self._client = None

        if not self.bucket_name:
            logger.warning(
                "AWS_S3_BUCKET_NAME not set; S3Storage uploads will be no-ops"
            )

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client("s3", region_name=self.region_name)
        return self._client

    def upload_rfp_json(
        self,
        analysis: RFPAnalysis,
        extra: dict[str, Any] | None = None,
        run_date: date | None = None,
    ) -> str | None:
        """Upload structured RFP record as JSON. Returns S3 key or None."""
        if not self.bucket_name:
            return None

        run_date = run_date or date.today()
        org_slug = slugify(analysis.organization_name)
        title_slug = slugify(analysis.rfp_title)
        key = f"rfps/{run_date.isoformat()}/{org_slug}_{title_slug}.json"

        payload: dict[str, Any] = {
            **analysis.model_dump(),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }
        if extra:
            payload["scraper_meta"] = extra

        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=body,
                ContentType="application/json",
            )
            logger.info("Uploaded JSON to s3://%s/%s", self.bucket_name, key)
            return key
        except ClientError as exc:
            logger.error("Failed to upload JSON to S3: %s", exc)
            return None

    def upload_pdf(
        self,
        pdf_bytes: bytes,
        organization_name: str,
        rfp_title: str,
        run_date: date | None = None,
    ) -> str | None:
        """Upload PDF binary. Returns S3 key or None."""
        if not self.bucket_name or not pdf_bytes:
            return None

        run_date = run_date or date.today()
        org_slug = slugify(organization_name)
        title_slug = slugify(rfp_title)
        key = f"pdfs/{run_date.isoformat()}/{org_slug}_{title_slug}.pdf"

        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=pdf_bytes,
                ContentType="application/pdf",
            )
            logger.info("Uploaded PDF to s3://%s/%s", self.bucket_name, key)
            return key
        except ClientError as exc:
            logger.error("Failed to upload PDF to S3: %s", exc)
            return None
