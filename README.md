# OfferUp Web Scraper

A full-stack web application for extracting listing data from OfferUp item pages. Built with Python Flask backend and React frontend.

![OfferUp Scraper Demo](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey)

## 🌟 Features

- 🔍 **Real-time scraping** - Extract data from OfferUp listings instantly
- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS
- 📊 **Complete data extraction** - Title, price, description, images, location, and seller info
- 🛡️ **Error handling** - Robust error handling and retry logic
- 🚀 **REST API** - Clean Flask API with JSON responses
- ⚡ **Fast & efficient** - Optimized JSON parsing from embedded data

## 📸 Screenshots

### Main Interface
Beautiful gradient UI with input field and real-time results display

### Results Display
- High-quality images
- Formatted pricing and location
- Full description with preserved formatting
- Seller information

## 🏗️ Architecture

```
┌─────────────────┐         HTTP           ┌─────────────────┐
│                 │  ──────────────────►   │                 │
│  React Frontend │      (REST API)        │  Flask Backend  │
│  (Port 5173)    │  ◄──────────────────   │  (Port 5000)    │
│                 │       JSON data        │                 │
└─────────────────┘                        └─────────────────┘
                                                    │
                                                    │ imports
                                                    ▼
                                           ┌─────────────────┐
                                           │  scraper.py     │
                                           │  (Core Logic)   │
                                           └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Node.js 16 or higher
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/offerup-scraper.git
cd offerup-scraper
```

2. **Set up the backend**
```bash
cd backend

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Set up the frontend**
```bash
cd ../frontend

# Install dependencies
npm install
```

### Running the Application

You'll need **two terminal windows**:

**Terminal 1 - Start the Flask backend:**
```bash
cd backend
source venv/bin/activate  # If using virtual environment
python api.py
```
Backend will run on `http://127.0.0.1:5000`

**Terminal 2 - Start the React frontend:**
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:5173`

**Open your browser to `http://localhost:5173`** and start scraping!!!

## 📖 Usage

### Web Interface

1. Open `http://localhost:5173` in your browser
2. Paste an OfferUp listing URL (e.g., `https://offerup.com/item/detail/...`)
3. Click "Scrape"
4. View the extracted data including images, description, and pricing

### API Endpoints

The Flask backend provides these REST API endpoints:

**Health Check**
```bash
GET http://127.0.0.1:5000/api/health
```

**Test Scrape** (uses sample listing)
```bash
GET http://127.0.0.1:5000/api/test
```

**Scrape Listing**
```bash
POST http://127.0.0.1:5000/api/scrape
Content-Type: application/json

{
  "url": "https://offerup.com/item/detail/YOUR-LISTING-ID",
  "download_image": false
}
```

**Example with curl:**
```bash
curl -X POST http://127.0.0.1:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://offerup.com/item/detail/4bc65998-e110-3dc8-b0d9-89bbbafd8994"}' \
  | python3 -m json.tool
```

### Command Line Interface (CLI)

You can also use the scraper from the command line:

```bash
cd backend

# Basic usage (JSON output)
python scraper.py "https://offerup.com/item/detail/YOUR-LISTING-ID"

# Human-readable text output
python scraper.py "https://offerup.com/item/detail/YOUR-LISTING-ID" -o text

# Download image
python scraper.py "https://offerup.com/item/detail/YOUR-LISTING-ID" -d

# CSV format
python scraper.py "https://offerup.com/item/detail/YOUR-LISTING-ID" -o csv

# Verbose mode (show scraping progress)
python scraper.py "https://offerup.com/item/detail/YOUR-LISTING-ID" -v

# Save to file
python scraper.py "https://offeup.com/item/detail/YOUR-LISTING-ID" > output.json
```

**All CLI options:**
```bash
python scraper.py --help
```

## 🛠️ Technology Stack

### Backend
- **Python 3.7+** - Core language
- **Flask** - Web framework
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript ES6+** - Modern JavaScript

## 📁 Project Structure

```
offerup-scraper/
├── backend/
│   ├── api.py              # Flask REST API
│   ├── scraper.py          # Core scraping logic + CLI
│   ├── config.py           # Configuration settings
│   ├── utils.py            # Helper functions
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Tailwind CSS imports
│   ├── public/             # Static assets
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   └── tailwind.config.js  # Tailwind configuration
│
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔒 Legal & Ethical Considerations

- ✅ This scraper only accesses individual item pages allowed per OfferUp's `robots.txt`
- ✅ Implements rate limiting to avoid server overload
- ✅ Respects OfferUp's Terms of Service

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built as an educational project to learn full-stack development
- Thanks to the React, Flask, and Tailwind CSS communities
