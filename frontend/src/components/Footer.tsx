import { Github, Instagram, Send } from 'lucide-react'
import XLogo from '@/components/icons/XLogo'

export default function Footer() {
  return (
    <footer className="mt-16 text-center text-green-400 border-t border-green-500 pt-4">
      <p>&gt; &copy; 2024 Starfall: Lost Age of Giants. All rights reserved.</p>
      <p className="mt-2">
        &gt; The $SLAG token has no inherent value and is meant for entertainment purposes only. NFA DYOR.
      </p>
      <div className="flex justify-center space-x-4 mt-4">
        <a 
          href="https://github.com/mango31/SLAG"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-green-300 transition-colors"
        >
          <Github className="w-4 h-4" />
        </a>
        <a 
          href="https://x.com/slag_ai"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-green-300 transition-colors"
        >
          <XLogo className="w-4 h-4" />
        </a>
        <a 
          href="https://t.me/slag_official"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-green-300 transition-colors"
        >
          <Send className="w-4 h-4" />
        </a>
        <a 
          href="https://www.instagram.com/slag_ai"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-green-300 transition-colors"
        >
          <Instagram className="w-4 h-4" />
        </a>
      </div>
    </footer>
  )
} 