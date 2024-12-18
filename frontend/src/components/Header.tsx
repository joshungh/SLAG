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
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Terminal className="w-5 h-5" />
          <span className="font-['IBM_Plex_Mono'] text-sm tracking-tight">
            SLAG.exe<span className={showCursor ? 'opacity-100' : 'opacity-0'}>▋</span>
          </span>
        </div>
        <nav>
          <ul className="flex space-x-6 font-['IBM_Plex_Mono'] text-sm">
            <li><a href="#story" className="hover:text-green-300 transition-colors">Story</a></li>
            <li><a href="#gallery" className="hover:text-green-300 transition-colors">Gallery</a></li>
            <li><a href="#about" className="hover:text-green-300 transition-colors">About</a></li>
          </ul>
        </nav>
      </div>
    </header>
  )
} 