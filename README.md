# OfferUp Web Scraper

A Python-based web scraper for extracting listing data from OfferUp item pages.

## Features

- Extracts item name/title
- Extracts full description
- Extracts first image URL
- Optional image download
- Multiple output formats (JSON, text, CSV)
- Robust error handling
- Respects robots.txt

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7 or higher
- Internet connection

## Usage

### Basic Usage

Scrape a listing (outputs JSON by default):
```bash
python scraper.py "https://offerup.com/item/detail/YOUR-LISTING-ID"
```

### Output Formats

**JSON format (default):**
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" --output json
```

**Human-readable text:**
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" --output text
```

**CSV format (good for spreadsheets):**
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" --output csv
```

### Download Images

Download the first image:
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" --download-image
```

Specify custom image directory:
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" -d --image-dir ./my_images
```

### Save Output to File

```bash
# Save as JSON file
python scraper.py "https://offerup.com/item/detail/abc-123" > listing.json

# Save as text file
python scraper.py "https://offerup.com/item/detail/abc-123" -o text > listing.txt

# Save as CSV file
python scraper.py "https://offerup.com/item/detail/abc-123" -o csv > listing.csv
```

### Verbose Mode

Show scraping progress:
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" --verbose
```

### All Options

```bash
python scraper.py --help
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `url` | - | OfferUp listing URL (required) | - |
| `--output` | `-o` | Output format: json, text, csv | json |
| `--download-image` | `-d` | Download the first image | False |
| `--image-dir` | - | Directory for downloaded images | downloaded_images |
| `--verbose` | `-v` | Show scraping progress | False |
| `--help` | `-h` | Show help message | - |
| `--version` | - | Show version number | - |

## Examples

**Example 1: Quick scrape with text output**
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" -o text
```

**Example 2: Scrape and download image**
```bash
python scraper.py "https://offerup.com/item/detail/abc-123" -d -v
```

**Example 3: Create CSV for multiple listings**
```bash
python scraper.py "https://offerup.com/item/detail/listing1" -o csv >> listings.csv
python scraper.py "https://offerup.com/item/detail/listing2" -o csv >> listings.csv
```

## Project Structure

```
offerup-scraper/
├── scraper.py          # Main scraper script
├── config.py           # Configuration settings
├── utils.py            # Helper functions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Legal & Ethical Considerations

- This scraper only accesses individual item pages that are allowed per OfferUp's robots.txt
- Implements rate limiting to avoid server overload
- For personal/educational use only
- Respects OfferUp's Terms of Service

## License

This project is for educational purposes only.

## Disclaimer

This tool is provided as-is. Users are responsible for ensuring their use complies with OfferUp's Terms of Service and applicable laws.