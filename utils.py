"""
Utility functions for Offerup Scraper.
"""

import re
from pathlib import Path
from typing import Optional

def extract_listing_id(url: str) -> Optional[str]:
    """
    Extracts listing ID from OfferUp URL.

    ARGS:
        url (str): The OfferUp listing URL.
    RETURNS:
        Listing ID string or None if not found.
    """

    pattern = r'/item/detail/([a-f0-9-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None





def is_valid_offerup_url(url: str) -> bool:
    """
    Check if URL is a valid OfferUp item listing URL.
    ARGS:
        url: URL string to validate
    RETURNS:
        True if valid OfferUp listing URL, False Otherwise
    """
    if not url:
        return False
    
    #Check if it is an offerup.com domain
    if 'offerup.com' not in url.lower():
        return False
    #Check if it has the item/detail path
    return extract_listing_id(url) is not None





def sanitize_filename(filename: str, max_length: int = 200) -> str: 
    """
    Sanitize filename by removing invalid characters.
    ARGS: 
        filename: Original filename
        max_length: Maximum filename length

    RETURNS:
        Sanitized filename for filesystem
    """

#remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
#replace spaces with underscors
    filename = filename.replace(" ", "_")
#remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
#truncate if too long
    if len(filename) > max_length:
        filename = filename[:max_length]

    return filename.strip('_')





def ensure_directory_exists(directory: Path) -> None:
    """
    Ensure directory exsists, create if it does not
    
    ARGS:
        directory: Path object for directory
    """

    directory.mkdir(parents=True, exist_ok=True)





def format_price(price: str) -> str:
    """
    Format price string consistently

    ARGS:
        price: Price string (4000)
    RETURNS:
        Formatted Price: $4,000
    """

    try: 
        price_num = float(price)
        return f"${price_num:,.0f}"
    except (ValueError, TypeError):
        return price