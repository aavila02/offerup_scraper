"""
Configuration settings for OfferUp scraper
"""

# HTTP Request Settings
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.0.0 Safari/537.36"
)

REQUEST_HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Timeout settings (in seconds)
REQUEST_TIMEOUT = 15
CONNECT_TIMEOUT = 10

# Retry settings
MAX_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff: 1s, 2s, 4s

# Rate limiting (seconds between requests)
REQUEST_DELAY = 1.0

# Image download settings
IMAGE_DOWNLOAD_TIMEOUT = 30
DEFAULT_IMAGE_DIR = "downloaded_images"

# OfferUp specific
OFFERUP_BASE_URL = "https://offerup.com"
JSON_SCRIPT_ID = "__NEXT_DATA__"

# Output settings
DEFAULT_OUTPUT_FORMAT = "json"
VALID_OUTPUT_FORMATS = ["json", "text", "csv"]