'use client'

import { useState } from 'react'

export default function DocsSearch() {
  const [query, setQuery] = useState('')
  
  const handleSearch = () => {
    window.location.href = `https://docs.lostage.io/?q=${encodeURIComponent(query)}`
  }

  return (
    <div className="relative">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search docs..."
        className="w-full px-4 py-2 bg-black border border-green-500 rounded-lg text-green-400"
        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
      />
    </div>
  )
} 