"""Utility helpers for SafeClick."""
from __future__ import annotations

import json
import logging
import re
from datetime import timedelta
from typing import Iterable, List, Optional
from urllib.parse import urlparse

import aiohttp

from .database import Database

LOGGER = logging.getLogger(__name__)

URL_REGEX = re.compile(
    r"((?:https?://)?(?:[\w-]+\.)+[\w]{2,}(?:/[\w\-._~:/?#\[\]@!$&'()*+,;=%]*)?)",
    re.IGNORECASE,
)


def extract_urls(text: str, limit: int = 3) -> List[str]:
    """Extract up to `limit` URLs from text."""
    urls = []
    for match in URL_REGEX.finditer(text):
        url = match.group(1)
        if not url.lower().startswith("http"):
            url = "http://" + url
        if validate_url(url):
            urls.append(url)
        if len(urls) >= limit:
            break
    return urls


def validate_url(url: str) -> bool:
    """Validate URL structure."""
    parsed = urlparse(url)
    return bool(parsed.scheme in {"http", "https"} and parsed.netloc)


class PhishTankClient:
    """Client for interacting with the PhishTank API with caching."""

    API_URL = "https://checkurl.phishtank.com/checkurl/"
    CACHE_TTL = timedelta(hours=24)

    def __init__(self, api_key: str, database: Database) -> None:
        self._api_key = api_key
        self._database = database

    async def check_url(self, url: str) -> Optional[dict]:
        """Check URL against PhishTank, returning response dict."""
        cached = await self._database.get_cached_url_result(url, max_age=self.CACHE_TTL)
        if cached:
            result, verified, detail_url = cached
            return {
                "in_database": result == "phishing",
                "verified": verified,
                "detail_url": detail_url,
                "cached": True,
            }
        payload = {"url": url, "format": "json"}
        if self._api_key:
            payload["app_key"] = self._api_key
        headers = {"Content-Type": "application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.API_URL, data=json.dumps(payload), headers=headers, timeout=15
                ) as response:
                    if response.status == 429:
                        LOGGER.warning("PhishTank rate limit reached")
                        return None
                    if response.status >= 500:
                        LOGGER.error("PhishTank server error: %s", response.status)
                        return None
                    response.raise_for_status()
                    data = await response.json()
        except aiohttp.ClientError as exc:
            LOGGER.exception("PhishTank request failed: %s", exc)
            return None

        in_database = bool(data.get("in_database"))
        verified = bool(data.get("verified"))
        detail_url = data.get("phish_detail_page")
        await self._database.cache_url_result(
            url,
            "phishing" if in_database else "safe",
            verified=verified,
            detail_url=detail_url,
        )
        data["cached"] = False
        return data


async def ensure_cache_cleanup(database: Database) -> None:
    """Periodically purge stale cache entries."""
    await database.purge_old_cache(older_than=timedelta(days=2))


def chunked(iterable: Iterable, size: int) -> Iterable[List]:
    """Yield successive chunks from iterable."""
    chunk: List = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


__all__ = ["extract_urls", "validate_url", "PhishTankClient", "ensure_cache_cleanup", "chunked"]
