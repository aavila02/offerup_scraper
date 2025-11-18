"""
Flask API for OfferUp Scraper
Wraps the scraper functionality in a REST API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Import our scraper
from scraper import scrape_listing, OfferUpScraperError

app = Flask(__name__)

# Enable CORS for React frontend (running on different port)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],  # Vite default port + CRA fallback
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'OfferUp Scraper API is running'
    }), 200


@app.route('/api/scrape', methods=['POST'])
def scrape():
    """
    Scrape OfferUp listing endpoint.
    
    Expected JSON body:
    {
        "url": "https://offerup.com/item/detail/...",
        "download_image": false  (optional)
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "title": "...",
            "description": "...",
            "first_image_url": "...",
            "price": "...",
            "location": "...",
            "seller_name": "...",
            "listing_id": "..."
        }
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Extract parameters
        url = data.get('url')
        download_image = data.get('download_image', False)
        
        # Validate URL parameter
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL parameter is required'
            }), 400
        
        # Suppress print statements for cleaner API responses
        # But keep them in console for debugging
        print(f"\n[API] Scraping request received for: {url}")
        print(f"[API] Download image: {download_image}")
        
        # Call the scraper
        result = scrape_listing(url, download_img=download_image)
        
        print(f"[API] Scraping successful: {result['title']}")
        
        # Return successful response
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except OfferUpScraperError as e:
        # Handle known scraper errors
        print(f"[API] Scraper error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': 'scraper_error'
        }), 400
        
    except Exception as e:
        # Handle unexpected errors
        print(f"[API] Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'error_type': 'server_error'
        }), 500


@app.route('/api/test', methods=['GET'])
def test():
    """
    Test endpoint with a sample OfferUp listing.
    """
    test_url = "https://offerup.com/item/detail/4bc65998-e110-3dc8-b0d9-89bbbafd8994"
    
    try:
        result = scrape_listing(test_url, download_img=False)
        return jsonify({
            'success': True,
            'message': 'Test scrape successful',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("OfferUp Scraper API Server")
    print("="*60)
    print("\nEndpoints:")
    print("  GET  /api/health  - Health check")
    print("  POST /api/scrape  - Scrape listing")
    print("  GET  /api/test    - Test with sample listing")
    print("\nStarting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True  # Auto-reload on code changes
    )