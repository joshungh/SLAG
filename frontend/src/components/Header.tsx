'use client'

import { Terminal, Github } from 'lucide-react'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { usePathname } from 'next/navigation'

export default function Header() {
  const [showCursor, setShowCursor] = useState(true)
  const pathname = usePathname()
  const isHomePage = pathname === '/'

  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev)
    }, 500)
    return () => clearInterval(interval)
  }, [])

  const scrollToSection = (sectionId: string) => {
    if (!isHomePage) {
      window.location.href = `/#${sectionId}`
      return
    }
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      })
    }
  }

  const scrollToTop = () => {
    if (!isHomePage) {
      window.location.href = '/'
      return
    }
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }

  return (
    <header className="border-b border-green-500 pb-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Image
            src="/images/logo1.png"
            alt="SLAG Logo"
            width={24}
            height={24}
            className="rounded-sm"
          />
          <button 
            onClick={scrollToTop}
            className="flex items-center space-x-2 hover:text-green-300 transition-colors"
          >
            <Terminal className="w-5 h-5" />
            <span className="font-['IBM_Plex_Mono'] text-sm tracking-tight">
              SLAG.exe<span className={showCursor ? 'opacity-100' : 'opacity-0'}>▋</span>
            </span>
          </button>
        </div>
        <nav>
          <ul className="flex space-x-6 font-['IBM_Plex_Mono'] text-sm">
            <li className="flex items-center">
              <a 
                href="https://github.com/mango31/SLAG"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-green-300 transition-colors mr-6"
              >
                <Github className="w-4 h-4" />
              </a>
              <button 
                onClick={() => scrollToSection('story')}
                className="hover:text-green-300 transition-colors"
              >
                Story
              </button>
            </li>
            <li>
              <Link 
                href="/gallery"
                className="hover:text-green-300 transition-colors"
              >
                Gallery
              </Link>
            </li>
            <li>
              <button 
                onClick={() => scrollToSection('info')}
                className="hover:text-green-300 transition-colors"
              >
                About
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  )
} 