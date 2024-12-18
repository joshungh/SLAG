'use client'

import { useState, useEffect } from 'react'

export default function CloudwatchLogsBox() {
  const [iframeUrl, setIframeUrl] = useState('')

  useEffect(() => {
    // In a real application, this URL would be fetched from an environment variable
    // or an API call to get a secure, temporary URL for the Cloudwatch logs
    setIframeUrl('https://example.com/cloudwatch-logs-embed')
  }, [])

  return (
    <div className="border border-green-500 rounded-lg overflow-hidden">
      <div className="bg-gray-800 text-green-400 px-4 py-2 font-bold">
        &gt; Live Cloudwatch Logs
      </div>
      {iframeUrl ? (
        <iframe
          src={iframeUrl}
          className="w-full h-64 bg-black"
          title="Cloudwatch Logs"
        />
      ) : (
        <div className="w-full h-64 bg-black flex items-center justify-center text-green-400">
          Loading Cloudwatch logs...
        </div>
      )}
    </div>
  )
} 