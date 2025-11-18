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

# Import our configuration and utilities
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
    
    Args:
        url: OfferUp listing URL to validate
        
    Returns:
        Validated URL string
        
    Raises:
        InvalidURLError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise InvalidURLError("URL must be a non-empty string")
    
    # Strip whitespace
    url = url.strip()
    
    # Check if valid OfferUp URL
    if not is_valid_offerup_url(url):
        raise InvalidURLError(
            f"Invalid OfferUp URL. Must be in format: "
            f"https://offerup.com/item/detail/[listing-id]"
        )
    
    listing_id = extract_listing_id(url)
    print(f"✓ Valid URL detected. Listing ID: {listing_id}")
    
    return url


def fetch_page(url: str, retry_count: int = 0) -> str:
    """
    Fetch HTML content from URL with retry logic.
    
    Args:
        url: URL to fetch
        retry_count: Current retry attempt (for recursive calls)
        
    Returns:
        HTML content as string
        
    Raises:
        FetchError: If fetch fails after all retries
    """
    try:
        print(f"Fetching page... (attempt {retry_count + 1}/{config.MAX_RETRY_ATTEMPTS})")
        
        response = requests.get(
            url,
            headers=config.REQUEST_HEADERS,
            timeout=config.REQUEST_TIMEOUT
        )
        
        # Check for successful response
        response.raise_for_status()
        
        print(f"✓ Page fetched successfully ({len(response.text)} bytes)")
        return response.text
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        if status_code == 404:
            raise FetchError("Listing not found (404). It may have been removed.")
        elif status_code == 403:
            raise FetchError("Access forbidden (403). You may be rate-limited.")
        elif status_code >= 500:
            raise FetchError(f"Server error ({status_code}). Try again later.")
        else:
            raise FetchError(f"HTTP error {status_code}: {str(e)}")
    
    except requests.exceptions.Timeout:
        # Retry on timeout
        if retry_count < config.MAX_RETRY_ATTEMPTS - 1:
            wait_time = config.RETRY_BACKOFF_FACTOR ** retry_count
            print(f"⏱ Timeout. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            return fetch_page(url, retry_count + 1)
        else:
            raise FetchError("Request timed out after multiple attempts")
    
    except requests.exceptions.ConnectionError:
        raise FetchError("Connection error. Check your internet connection.")
    
    except requests.exceptions.RequestException as e:
        raise FetchError(f"Request failed: {str(e)}")


def extract_json_data(html_content: str) -> Dict[str, Any]:
    """
    Extract __NEXT_DATA__ JSON from HTML.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        ParseError: If JSON extraction or parsing fails
    """
    print("Parsing HTML and extracting JSON data...")
    
    try:
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Find the script tag with id="__NEXT_DATA__"
        script_tag = soup.find('script', {'id': config.JSON_SCRIPT_ID})
        
        if not script_tag:
            raise ParseError(
                f"Could not find script tag with id='{config.JSON_SCRIPT_ID}'. "
                f"Page structure may have changed."
            )
        
        # Extract JSON string from script tag
        json_string = script_tag.string
        
        if not json_string:
            raise ParseError("Script tag found but contains no content")
        
        # Parse JSON string to dictionary
        json_data = json.loads(json_string)
        
        print("✓ JSON data extracted successfully")
        return json_data
        
    except json.JSONDecodeError as e:
        raise ParseError(f"Failed to parse JSON: {str(e)}")
    
    except Exception as e:
        raise ParseError(f"Unexpected error during parsing: {str(e)}")


def parse_listing_data(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse listing data from JSON structure.
    
    Args:
        json_data: Parsed JSON data from __NEXT_DATA__
        
    Returns:
        Dictionary containing cleaned listing data
        
    Raises:
        ParseError: If required data cannot be extracted
    """
    print("Extracting listing information...")
    
    try:
        # Navigate to the listing data in the JSON structure
        # Path: props -> pageProps -> initialApolloState -> ROOT_QUERY -> listing(...)
        initial_state = json_data['props']['pageProps']['initialApolloState']
        root_query = initial_state['ROOT_QUERY']
        
        # Find the listing key (starts with "listing(")
        listing_key = None
        for key in root_query.keys():
            if key.startswith('listing('):
                listing_key = key
                break
        
        if not listing_key:
            raise ParseError("Could not find listing data in JSON structure")
        
        listing = root_query[listing_key]
        
        # Extract required fields
        title = listing.get('title', '')
        description = listing.get('description', '')
        
        # Extract first image URL
        photos = listing.get('photos', [])
        first_image_url = None
        if photos and len(photos) > 0:
            first_photo = photos[0]
            detail_full = first_photo.get('detailFull', {})
            first_image_url = detail_full.get('url', '')
        
        # Validate required fields
        if not title:
            raise ParseError("Title not found in listing data")
        
        # Extract optional but useful fields
        price = listing.get('price', '')
        location = listing.get('locationDetails', {}).get('locationName', '')
        
        # Get seller info if available
        owner_ref = listing.get('owner', {})
        owner_id = owner_ref.get('id', '') if isinstance(owner_ref, dict) else owner_ref.get('__ref', '').split(':')[-1]
        
        seller_name = ''
        if owner_id:
            # Look up owner in the initial state
            owner_key = f"User:{owner_id}"
            if owner_key in initial_state:
                owner_data = initial_state[owner_key]
                profile = owner_data.get('profile', {})
                seller_name = profile.get('name', '')
        
        result = {
            'title': title,
            'description': description,
            'first_image_url': first_image_url,
            'price': price,
            'location': location,
            'seller_name': seller_name,
            'listing_id': listing.get('listingId', ''),
        }
        
        print(f"✓ Successfully extracted listing data")
        print(f"  Title: {title[:50]}..." if len(title) > 50 else f"  Title: {title}")
        print(f"  Image URL: {'Found' if first_image_url else 'Not found'}")
        
        return result
        
    except KeyError as e:
        raise ParseError(f"Missing expected field in JSON structure: {str(e)}")
    
    except Exception as e:
        raise ParseError(f"Error extracting listing data: {str(e)}")


def download_image(image_url: str, save_dir: str = None, filename: str = None) -> Optional[Path]:
    """
    Download image from URL.
    
    Args:
        image_url: URL of image to download
        save_dir: Directory to save image (default: config.DEFAULT_IMAGE_DIR)
        filename: Custom filename (default: derived from listing title)
        
    Returns:
        Path to saved image file, or None if download failed
    """
    if not image_url:
        print("⚠ No image URL provided, skipping download")
        return None
    
    try:
        print(f"Downloading image...")
        
        # Set up save directory
        if save_dir is None:
            save_dir = config.DEFAULT_IMAGE_DIR
        
        save_path = Path(save_dir)
        ensure_directory_exists(save_path)
        
        # Download image
        response = requests.get(
            image_url,
            headers=config.REQUEST_HEADERS,
            timeout=config.IMAGE_DOWNLOAD_TIMEOUT,
            stream=True
        )
        response.raise_for_status()
        
        # Determine filename
        if filename is None:
            # Extract filename from URL or use default
            url_filename = image_url.split('/')[-1].split('?')[0]
            if url_filename and '.' in url_filename:
                filename = url_filename
            else:
                filename = 'image.jpg'
        
        # Sanitize filename
        filename = sanitize_filename(filename)
        
        # Save image
        file_path = save_path / filename
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Image saved to: {file_path}")
        return file_path
        
    except requests.exceptions.RequestException as e:
        print(f"⚠ Failed to download image: {str(e)}")
        return None
    
    except Exception as e:
        print(f"⚠ Unexpected error downloading image: {str(e)}")
        return None


def scrape_listing(url: str, download_img: bool = False) -> Dict[str, Any]:
    """
    Main scraper function - orchestrates the entire scraping process.
    
    Args:
        url: OfferUp listing URL
        download_img: Whether to download the image
        
    Returns:
        Dictionary containing scraped listing data
        
    Raises:
        OfferUpScraperError: If scraping fails at any step
    """
    print(f"\n{'='*60}")
    print("OfferUp Listing Scraper")
    print(f"{'='*60}\n")
    
    # Step 1: Validate URL
    validated_url = validate_url(url)
    
    # Step 2: Fetch page
    html_content = fetch_page(validated_url)
    
    # Step 3: Extract JSON data
    json_data = extract_json_data(html_content)
    
    # Step 4: Parse listing data
    listing_data = parse_listing_data(json_data)
    
    # Step 5: Download image (optional)
    if download_img and listing_data.get('first_image_url'):
        # Create filename from title and listing ID
        title = listing_data.get('title', 'image')
        listing_id = listing_data.get('listing_id', '')
        filename = f"{sanitize_filename(title)}_{listing_id}.jpg"
        
        image_path = download_image(
            listing_data['first_image_url'],
            filename=filename
        )
        listing_data['downloaded_image_path'] = str(image_path) if image_path else None
    
    print(f"\n{'='*60}")
    print("✓ Scraping completed successfully!")
    print(f"{'='*60}\n")
    
    return listing_data


def format_output_json(data: Dict[str, Any]) -> str:
    """Format output as pretty JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_output_text(data: Dict[str, Any]) -> str:
    """Format output as human-readable text."""
    output = []
    output.append("\n" + "="*60)
    output.append("LISTING DETAILS")
    output.append("="*60)
    
    output.append(f"\nTitle: {data.get('title', 'N/A')}")
    output.append(f"Price: ${data.get('price', 'N/A')}")
    output.append(f"Location: {data.get('location', 'N/A')}")
    output.append(f"Seller: {data.get('seller_name', 'N/A')}")
    output.append(f"Listing ID: {data.get('listing_id', 'N/A')}")
    
    output.append(f"\nDescription:")
    output.append("-" * 60)
    output.append(data.get('description', 'N/A'))
    
    output.append(f"\nImage URL:")
    output.append(data.get('first_image_url', 'N/A'))
    
    if data.get('downloaded_image_path'):
        output.append(f"\nDownloaded Image:")
        output.append(data.get('downloaded_image_path'))
    
    output.append("\n" + "="*60)
    
    return "\n".join(output)


def format_output_csv(data: Dict[str, Any]) -> str:
    """Format output as CSV (single row)."""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header row
    headers = ['title', 'price', 'location', 'seller_name', 'listing_id', 
               'description', 'first_image_url', 'downloaded_image_path']
    writer.writerow(headers)
    
    # Data row
    row = [
        data.get('title', ''),
        data.get('price', ''),
        data.get('location', ''),
        data.get('seller_name', ''),
        data.get('listing_id', ''),
        data.get('description', '').replace('\n', ' '),  # Remove newlines for CSV
        data.get('first_image_url', ''),
        data.get('downloaded_image_path', '')
    ]
    writer.writerow(row)
    
    return output.getvalue()


def format_output(data: Dict[str, Any], output_format: str) -> str:
    """
    Format scraped data according to specified format.
    
    Args:
        data: Scraped listing data
        output_format: One of 'json', 'text', 'csv'
        
    Returns:
        Formatted string output
    """
    if output_format == 'json':
        return format_output_json(data)
    elif output_format == 'text':
        return format_output_text(data)
    elif output_format == 'csv':
        return format_output_csv(data)
    else:
        raise ValueError(f"Unknown output format: {output_format}")


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='OfferUp Web Scraper - Extract listing data from OfferUp item pages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - scrape listing and display as JSON
  python scraper.py https://offerup.com/item/detail/abc-123
  
  # Display as human-readable text
  python scraper.py https://offerup.com/item/detail/abc-123 --output text
  
  # Download the image
  python scraper.py https://offerup.com/item/detail/abc-123 --download-image
  
  # Save output to file
  python scraper.py https://offerup.com/item/detail/abc-123 -o json > listing.json
  
  # CSV format with image download
  python scraper.py https://offerup.com/item/detail/abc-123 -o csv -d

For more information, visit: https://github.com/yourusername/offerup-scraper
        """
    )
    
    # Required argument
    parser.add_argument(
        'url',
        type=str,
        help='OfferUp listing URL (e.g., https://offerup.com/item/detail/...)'
    )
    
    # Optional arguments
    parser.add_argument(
        '-o', '--output',
        type=str,
        choices=['json', 'text', 'csv'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '-d', '--download-image',
        action='store_true',
        help='Download the first image to local directory'
    )
    
    parser.add_argument(
        '--image-dir',
        type=str,
        default=config.DEFAULT_IMAGE_DIR,
        help=f'Directory to save downloaded images (default: {config.DEFAULT_IMAGE_DIR})'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output (show scraping progress)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='OfferUp Scraper v1.0.0'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Suppress progress output if not verbose (except for errors)
    import sys
    if not args.verbose:
        # Redirect stdout to null, keep stderr for errors
        original_stdout = sys.stdout
        sys.stdout = open('/dev/null', 'w') if sys.platform != 'win32' else open('nul', 'w')
    
    try:
        # Scrape the listing
        result = scrape_listing(
            args.url,
            download_img=args.download_image
        )
        
        # Restore stdout if it was suppressed
        if not args.verbose:
            sys.stdout.close()
            sys.stdout = original_stdout
        
        # Format and output the results
        formatted_output = format_output(result, args.output)
        print(formatted_output)
        
        # Exit successfully
        sys.exit(0)
        
    except OfferUpScraperError as e:
        # Restore stdout if it was suppressed
        if not args.verbose:
            sys.stdout.close()
            sys.stdout = original_stdout
        
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        if not args.verbose:
            sys.stdout.close()
            sys.stdout = original_stdout
        
        print("\n\n⚠ Scraping interrupted by user", file=sys.stderr)
        sys.exit(130)
        
    except Exception as e:
        # Restore stdout if it was suppressed
        if not args.verbose:
            sys.stdout.close()
            sys.stdout = original_stdout
        
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()