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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            OfferUp Scraper
          </h1>
          <p className="text-gray-600 text-lg">
            Extract listing data from OfferUp item pages
          </p>
        </div>

        {/* Main Card */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            {/* Input Form */}
            <form onSubmit={handleSubmit} className="mb-8">
              <div className="flex flex-col md:flex-row gap-4">
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Paste OfferUp listing URL here..."
                  className="flex-1 px-6 py-4 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 text-lg transition-colors"
                  required
                />
                <button
                  type="submit"
                  disabled={loading}
                  className={`px-8 py-4 rounded-xl font-semibold text-lg transition-all ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
                  } text-white shadow-lg`}
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
              </div>
            </form>

            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
                <div className="flex items-center">
                  <svg
                    className="w-6 h-6 text-red-500 mr-3"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </div>
            )}

            {/* Results */}
            {result && (
              <div className="space-y-6 animate-fade-in">
                {/* Title and Price */}
                <div className="border-b pb-6">
                  <h2 className="text-3xl font-bold text-gray-800 mb-3">
                    {result.title}
                  </h2>
                  <div className="flex items-center gap-4 text-lg">
                    <span className="text-3xl font-bold text-green-600">
                      ${result.price}
                    </span>
                    {result.location && (
                      <span className="text-gray-600">
                        📍 {result.location}
                      </span>
                    )}
                  </div>
                  {result.seller_name && (
                    <p className="text-gray-600 mt-2">
                      Seller: {result.seller_name}
                    </p>
                  )}
                </div>

                {/* Image */}
                {result.first_image_url && (
                  <div className="rounded-xl overflow-hidden shadow-lg">
                    <img
                      src={result.first_image_url}
                      alt={result.title}
                      className="w-full h-auto"
                    />
                  </div>
                )}

                {/* Description */}
                <div className="bg-gray-50 rounded-xl p-6">
                  <h3 className="text-xl font-semibold text-gray-800 mb-3">
                    Description
                  </h3>
                  <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                    {result.description}
                  </p>
                </div>

                {/* Listing ID */}
                {result.listing_id && (
                  <div className="text-sm text-gray-500 text-center">
                    Listing ID: {result.listing_id}
                  </div>
                )}
              </div>
            )}

            {/* Empty State */}
            {!result && !error && !loading && (
              <div className="text-center py-12 text-gray-400">
                <svg
                  className="w-24 h-24 mx-auto mb-4 opacity-50"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <p className="text-xl">Enter an OfferUp URL to get started</p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="text-center mt-8 text-gray-600">
            <p className="text-sm">
              Built with React + Flask • For educational purposes only
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App