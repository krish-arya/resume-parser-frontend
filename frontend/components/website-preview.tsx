"use client"

import { useState, useEffect } from "react"
import { ExternalLink, Edit3, RefreshCw, AlertCircle } from "lucide-react"

interface WebsitePreviewProps {
  websiteId: string
}

export default function WebsitePreview({ websiteId }: WebsitePreviewProps) {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [iframeKey, setIframeKey] = useState(0)

  const previewUrl = `/api/preview/${websiteId}`

  const handleIframeLoad = () => {
    setIsLoading(false)
    setError(null)
  }

  const handleIframeError = () => {
    setIsLoading(false)
    setError("Failed to load website preview")
  }

  const refreshPreview = () => {
    setIsLoading(true)
    setError(null)
    setIframeKey((prev) => prev + 1)
  }

  useEffect(() => {
    // Reset loading state when websiteId changes
    setIsLoading(true)
    setError(null)
    setIframeKey((prev) => prev + 1)
  }, [websiteId])

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      {/* Preview Header */}
      <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex gap-1">
              <div className="w-3 h-3 bg-red-400 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
              <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            </div>
            <span className="text-sm text-gray-600">Portfolio Preview</span>
            {isLoading && (
              <div className="flex items-center gap-2 text-sm text-blue-600">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                Loading...
              </div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={refreshPreview}
              className="flex items-center gap-2 px-3 py-1 text-sm text-gray-600 hover:text-gray-700 border border-gray-300 rounded hover:bg-gray-50"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
            <a
              href={previewUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-3 py-1 text-sm text-blue-600 hover:text-blue-700 border border-blue-300 rounded hover:bg-blue-50"
            >
              <ExternalLink className="w-4 h-4" />
              Open in New Tab
            </a>
          </div>
        </div>
      </div>

      {/* Preview Content */}
      <div className="relative bg-gray-100">
        {error ? (
          <div className="h-96 flex items-center justify-center">
            <div className="text-center">
              <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Preview Error</h3>
              <p className="text-gray-600 mb-4">{error}</p>
              <button
                onClick={refreshPreview}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Try Again
              </button>
            </div>
          </div>
        ) : (
          <>
            {isLoading && (
              <div className="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading your website...</p>
                </div>
              </div>
            )}
            <iframe
              key={iframeKey}
              src={previewUrl}
              className="w-full h-[600px] border-0"
              title="Website Preview"
              onLoad={handleIframeLoad}
              onError={handleIframeError}
              sandbox="allow-scripts allow-same-origin"
            />
          </>
        )}
      </div>

      {/* Instructions */}
      <div className="px-6 py-4 bg-blue-50 border-t border-blue-200">
        <div className="flex items-start gap-3">
          <Edit3 className="w-5 h-5 text-blue-600 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-900">AI-Powered Editing</h4>
            <p className="text-sm text-blue-700 mt-1">
              Click on any component in the preview above to edit it with AI assistance. You can modify colors, text,
              layout, and more using natural language instructions.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
