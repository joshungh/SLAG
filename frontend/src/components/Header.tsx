'use client'

import { Terminal } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function Header() {
  const [showCursor, setShowCursor] = useState(true)

  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev)
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="border-b border-green-500 pb-4">
      <div className="flex flex-col sm:flex-row items-center justify-between">
        <div className="flex items-center space-x-2 mb-4 sm:mb-0">
          <Terminal className="h-8 w-8 text-green-500" />
          <h1 className="text-2xl font-bold tracking-tight text-green-400">
            Starfall: Lost Age of Giants
            <span className={`ml-2 ${showCursor ? 'opacity-100' : 'opacity-0'}`}>
              ▋
            </span>
          </h1>
        </div>
        <nav>
          <ul className="flex space-x-4">
            <li><a href="#story" className="hover:text-green-300 transition-colors">Story</a></li>
            <li><a href="#gallery" className="hover:text-green-300 transition-colors">Gallery</a></li>
            <li><a href="#about" className="hover:text-green-300 transition-colors">About</a></li>
          </ul>
        </nav>
      </div>
      <p className="mt-4 text-sm text-green-400">
        &gt; Autonomously generated graphic novel // AI-powered storytelling
      </p>
    </header>
  )
} 