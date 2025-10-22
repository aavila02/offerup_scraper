"""
OfferUp Web Scraper - Main scraper module
Extracts listing data from OfferUp item pages
"""

import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional, Dict, Any

# import config and utils
import config
from utils import (
    is_valid_offerup_url,
    extract_listing_id,
    sanitize_filename,
    ensure_directory_exists
)

class OfferUpScraperError(Exception):
    """Base exception for scraper errors"""
    pass
class InvalidURLError(OfferUpScraperError):
    """Raised when URL is invalid"""
    pass
class FetchError(OfferUpScraperError):
    """Raised when page fetch fails"""
    pass
class ParseError(OfferUpScraperError):
    """Raised when data parsing fails"""
    pass


def validate_url(url: str) -> str:
    """
    Validate OfferUp URL format.
    ARGS:
        url: OfferUp listing URL to validate
    RETURNS:
        Validated URL string
    RAISES:
        InvalidURLError: if url is invalid
    """
    if not url or not isinstance(url, str):
        raise InvalidURLError("URL must be a non-empty string")
    
    #Strip whitespace
    url = url.strip()

    #Check if invalid OfferUp URL
    if not is_valid_offerup_url(url):
        raise InvalidURLError(
            f"Invalid OfferUp URL. Must be in format: "
            f"https://offerup.com/item/detail/[listing-id]"
        )
    
    listing_id = extract_listing_id(url)
    print(f"Valid url. Listing ID: {listing_id}")

    return url




def scrape_listing(url: str, download_img: bool = False) -> Dict[str, Any]:
    """
    Main scraper function: orchestrates the entire scraping process
    ARGS:
        url: OfferUp listing URL
        download_img: Whether to download the image
    RETURNS:
        Dictionary containing scraped listing data
    RAISES:
        OfferupScraperError: If scraping fails at any step
    """
    print(f"\n{'='*60}")
    print("OfferUp Listing Scraper")
    print(f"\n{'='*60}")
    #Step 1: Validate URL
    #Step 2: Fetch page
    #Step 3: Extract JSON data
    #Step 4: Parse listing data
    #Step 5: Download image (optional)




if __name__ == "__main__":
    test_url = "https://offerup.com/item/detail/4bc65998-e110-3dc8-b0d9-89bbbafd8994"
    
    try:
        result = scrape_listing(test_url, download_img=True)
        
        print("\n--- Scraped Data ---")
        print(f"Title: {result['title']}")
        print(f"Price: {result['price']}")
        print(f"Location: {result['location']}")
        print(f"Seller: {result['seller_name']}")
        print(f"\nDescription:\n{result['description'][:200]}...")
        print(f"\nImage URL: {result['first_image_url']}")
        
    except OfferUpScraperError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")