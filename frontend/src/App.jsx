import { useState } from 'react'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Reset previous results
    setError(null)
    setResult(null)
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:5000/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          url: url,
          download_image: false 
        }),
      })

      const data = await response.json()

      if (data.success) {
        setResult(data.data)
      } else {
        setError(data.error || 'Failed to scrape listing')
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the Flask backend is running.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setUrl('')
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-3">
            🔍 OfferUp Scraper
          </h1>
          <p className="text-gray-600 text-base md:text-lg">
            Extract listing data from OfferUp item pages instantly
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {/* Input Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="flex flex-col md:flex-row gap-3 max-w-3xl mx-auto">
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Paste OfferUp listing URL here..."
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-base transition-colors"
                  required
              />
                <div className="flex gap-2">
                  <button
                    type="submit"
                    disabled={loading}
                    className={`px-6 py-3 rounded-lg font-semibold text-base transition-all ${
                      loading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
                    } text-white shadow-md whitespace-nowrap`}
                  >
                    {loading ? (
                      <span className="flex items-center gap-2">
                        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                            fill="none"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          />
                        </svg>
                        Scraping...
                      </span>
                    ) : (
                      'Scrape'
                    )}
                  </button>
                  {(result || error) && (
                    <button
                      type="button"
                      onClick={handleClear}
                      className="px-4 py-3 rounded-lg font-semibold text-base bg-gray-200 hover:bg-gray-300 text-gray-700 transition-all"
                    >
                      Clear
                    </button>
                  )}
                </div>
              </div>
            </form>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
                <div className="flex items-start">
                  <svg
                    className="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              </div>
            )}
          </div>

          {/* Results */}
          {result && (
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              {/* Grid Layout: Image on left, Info on right */}
              <div className="grid md:grid-cols-2 gap-6 p-6">
                {/* Left Column - Image */}
                <div className="space-y-4">
                  {result.first_image_url ? (
                    <div className="rounded-lg overflow-hidden shadow-md bg-gray-100">
                      <img
                        src={result.first_image_url}
                        alt={result.title}
                        className="w-full h-auto max-h-[500px] object-contain"
                      />
                    </div>
                  ) : (
                    <div className="rounded-lg bg-gray-100 h-64 flex items-center justify-center">
                      <p className="text-gray-400">No image available</p>
                    </div>
                  )}
                </div>

                {/* Right Column - Details */}
                <div className="space-y-4">
                  {/* Title and Price */}
                  <div className="border-b pb-4">
                    <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-3">
                      {result.title}
                    </h2>
                    <div className="flex flex-wrap items-center gap-3">
                      <span className="text-3xl font-bold text-green-600">
                        ${result.price}
                      </span>
                      {result.location && (
                        <span className="text-gray-600 text-sm flex items-center gap-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                          </svg>
                          {result.location}
                        </span>
                      )}
                    </div>
                    {result.seller_name && (
                      <p className="text-gray-600 text-sm mt-2">
                        Seller: <span className="font-medium">{result.seller_name}</span>
                      </p>
                    )}
                  </div>

                  {/* Description */}
                  <div className="bg-gray-50 rounded-lg p-4 max-h-[400px] overflow-y-auto">
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">
                      Description
                    </h3>
                    <p className="text-gray-700 text-sm whitespace-pre-wrap leading-relaxed">
                      {result.description}
                    </p>
                  </div>

                  {/* Listing ID */}
                  {result.listing_id && (
                    <div className="text-xs text-gray-400 pt-2 border-t">
                      Listing ID: {result.listing_id}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Empty State */}
          {!result && !error && !loading && (
            <div className="bg-white rounded-xl shadow-lg p-12 text-center">
              {/* Removed the SVG magnifying glass icon here */}
              <h3 className="text-xl font-semibold text-gray-600 mb-2">
                Ready to scrape
              </h3>
              <p className="text-gray-400">
                Enter an OfferUp URL above to extract listing data
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500">
          <p className="text-sm">
            Built with React + Flask • For educational purposes only
          </p>
        </div>
      </div>
    </div>
  )
}

export default App