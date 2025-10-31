"""
Utility functions for SafeClick bot
URL extraction and URLScan.io API integration
"""

import re
import time
import logging
import requests
from typing import Dict, Optional
from bot.config import URLSCAN_API_KEY

logger = logging.getLogger(__name__)

# URLScan.io API endpoints
URLSCAN_SUBMIT_URL = "https://urlscan.io/api/v1/scan/"
URLSCAN_RESULT_URL = "https://urlscan.io/api/v1/result/{uuid}/"


def extract_urls(text: str) -> list:
    """
    Extract all URLs from text

    Args:
        text: Message text

    Returns:
        List of URLs found
    """
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls


def is_valid_url(url: str) -> bool:
    """
    Check if string is a valid URL

    Args:
        url: String to validate

    Returns:
        bool: True if valid URL
    """
    url_pattern = r'^https?://.+'
    return bool(re.match(url_pattern, url))


def check_url(url: str) -> dict:
    """
    Check if URL is safe or phishing using URLScan.io API

    Args:
        url: URL to check

    Returns:
        dict: {
            'is_phishing': True/False/None,
            'verified': 'Yes'/'No'/None,
            'detail_url': str or None,
            'error': str or None
        }
    """
    if not URLSCAN_API_KEY:
        logger.error("URLScan API key not configured")
        return {
            'is_phishing': None,
            'verified': None,
            'detail_url': None,
            'error': 'API key not configured'
        }

    try:
        # Step 1: Submit URL for scanning
        headers = {
            'API-Key': URLSCAN_API_KEY,
            'Content-Type': 'application/json'
        }

        payload = {
            'url': url,
            'visibility': 'public'  # Using public scans (5,000/day free)
        }

        logger.info(f"🔍 Submitting URL to URLScan.io: {url}")

        response = requests.post(
            URLSCAN_SUBMIT_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        # Check for rate limit
        if response.status_code == 429:
            logger.warning("⚠️ Rate limit exceeded")
            return {
                'is_phishing': None,
                'verified': None,
                'detail_url': None,
                'error': 'Rate limit exceeded. Please try again later.'
            }

        # Check for other errors
        if response.status_code != 200:
            logger.error(f"❌ URLScan API error: {response.status_code} - {response.text}")
            return {
                'is_phishing': None,
                'verified': None,
                'detail_url': None,
                'error': f'Scan submission failed: {response.status_code}'
            }

        # Get scan UUID
        result = response.json()
        scan_uuid = result.get('uuid')
        result_url = result.get('result')

        if not scan_uuid:
            logger.error("No UUID in response")
            return {
                'is_phishing': None,
                'verified': None,
                'detail_url': None,
                'error': 'Invalid API response'
            }

        logger.info(f"✅ Scan submitted. UUID: {scan_uuid}")

        # Step 2: Wait for scan to complete (URLScan takes 10-30 seconds)
        logger.info("⏳ Waiting for scan results...")
        time.sleep(15)  # Initial wait

        # Step 3: Poll for results (max 5 attempts = ~40 seconds total)
        for attempt in range(5):
            try:
                result_response = requests.get(
                    URLSCAN_RESULT_URL.format(uuid=scan_uuid),
                    headers=headers,
                    timeout=10
                )

                # Scan still processing
                if result_response.status_code == 404:
                    logger.info(f"⏳ Scan still processing... (attempt {attempt + 1}/5)")
                    time.sleep(5)
                    continue

                # Scan complete
                if result_response.status_code == 200:
                    scan_result = result_response.json()

                    # Analyze results
                    verdicts = scan_result.get('verdicts', {})
                    overall_verdict = verdicts.get('overall', {})

                    # Check if malicious
                    is_malicious = overall_verdict.get('malicious', False)
                    categories = overall_verdict.get('categories', [])

                    # Determine if phishing
                    is_phishing = is_malicious or 'phishing' in categories or 'malicious' in categories

                    logger.info(f"✅ Scan complete. Phishing: {is_phishing}")

                    return {
                        'is_phishing': is_phishing,
                        'verified': 'Yes',
                        'detail_url': result_url,
                        'error': None
                    }

                # Unexpected status code
                logger.warning(f"⚠️ Unexpected status code: {result_response.status_code}")
                break

            except requests.RequestException as e:
                logger.error(f"❌ Error fetching results: {e}")
                break

        # If we get here, scan timed out
        logger.warning("⏱️ Scan timeout - returning partial result")
        return {
            'is_phishing': None,
            'verified': 'No',
            'detail_url': result_url if result_url else None,
            'error': 'Scan timeout. Check result URL manually.'
        }

    except requests.RequestException as e:
        logger.error(f"❌ Network error during scan: {e}")
        return {
            'is_phishing': None,
            'verified': None,
            'detail_url': None,
            'error': f'Network error: {str(e)}'
        }

    except Exception as e:
        logger.error(f"❌ Unexpected error during scan: {e}")
        return {
            'is_phishing': None,
            'verified': None,
            'detail_url': None,
            'error': f'Unexpected error: {str(e)}'
        }