"""
Utility functions for SafeClick bot
URL extraction and checking (API placeholder)
"""

import re
import logging

logger = logging.getLogger(__name__)


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


def check_url(url: str) -> dict:
    """
    Check if URL is safe or phishing

    PLACEHOLDER FUNCTION - API not implemented yet!
    Replace this function with actual API integration later.

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
    # TODO: Add actual API integration here
    # Options: PhishTank, VirusTotal, Google Safe Browsing, URLScan.io, etc.

    logger.info(f"Checking URL (placeholder): {url}")

    # For now, return a mock "safe" response
    return {
        'is_phishing': False,
        'verified': None,
        'detail_url': None,
        'error': None
    }

    # Future API integration example:
    # try:
    #     response = requests.post('API_ENDPOINT', data={'url': url})
    #     data = response.json()
    #     return {
    #         'is_phishing': data.get('is_phishing'),
    #         'verified': data.get('verified'),
    #         'detail_url': data.get('detail_url'),
    #         'error': None
    #     }
    # except Exception as e:
    #     return {
    #         'is_phishing': None,
    #         'verified': None,
    #         'detail_url': None,
    #         'error': str(e)
    #     }


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