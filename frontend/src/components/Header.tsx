"use client";

import {
  Terminal,
  Github,
  Menu,
  X as MenuX,
  Send,
  Instagram,
} from "lucide-react";
import XLogo from "@/components/icons/XLogo";
import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Header() {
  const [showCursor, setShowCursor] = useState(true);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();
  const isHomePage = pathname === "/";

  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  const scrollToTop = () => {
    if (!isHomePage) {
      window.location.href = "/";
      return;
    }
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <header className="border-b border-green-500 pb-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <button
            onClick={scrollToTop}
            className="flex items-center space-x-2 hover:text-green-300 transition-colors"
          >
            <Terminal className="w-5 h-5" />
            <span className="font-['IBM_Plex_Mono'] text-sm tracking-tight">
              SLAG.exe
              <span className={showCursor ? "opacity-100" : "opacity-0"}>
                ▋
              </span>
            </span>
          </button>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:block">
          <ul className="flex space-x-4 font-['IBM_Plex_Mono'] text-sm">
            <li className="flex items-center">
              <div className="flex space-x-4">
<<<<<<< HEAD
                <Link
=======
                <Link 
                  href="/dashboard"
                  className="hover:text-green-300 transition-colors"
                >
                  Dashboard
                </Link>
                <Link 
>>>>>>> 689abf8cefcb9bd45b3cf0cb4c74cf2ff1d83785
                  href="https://docs.lostage.io"
                  className="hover:text-green-300 transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Docs
                </Link>
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
            </li>
          </ul>
        </nav>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="md:hidden hover:text-green-300 transition-colors"
        >
          {isMenuOpen ? (
            <MenuX className="w-6 h-6" />
          ) : (
            <Menu className="w-6 h-6" />
          )}
        </button>

        <Link
          href="/dashboard"
          className="bg-green-400 text-black px-4 py-2 rounded hover:bg-green-300 transition-colors"
        >
          Launch App
        </Link>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <nav className="md:hidden mt-4">
          <ul className="flex flex-col space-y-4 font-['IBM_Plex_Mono'] text-sm">
            <li>
<<<<<<< HEAD
              <Link
=======
              <Link 
                href="/dashboard"
                className="hover:text-green-300 transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Dashboard
              </Link>
            </li>
            <li>
              <Link 
>>>>>>> 689abf8cefcb9bd45b3cf0cb4c74cf2ff1d83785
                href="https://docs.lostage.io"
                className="hover:text-green-300 transition-colors"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => setIsMenuOpen(false)}
              >
                Docs
              </Link>
            </li>
            <li>
              <div className="flex space-x-4 items-center">
                <Github className="w-4 h-4" />
                <a
                  href="https://github.com/mango31/SLAG"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-300 transition-colors"
                >
                  GitHub
                </a>
              </div>
            </li>
            <li>
              <div className="flex space-x-4 items-center">
                <XLogo className="w-4 h-4" />
                <a
                  href="https://x.com/slag_ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-300 transition-colors"
                >
                  X
                </a>
              </div>
            </li>
            <li>
              <div className="flex space-x-4 items-center">
                <Send className="w-4 h-4" />
                <a
                  href="https://t.me/slag_official"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-300 transition-colors"
                >
                  Telegram
                </a>
              </div>
            </li>
            <li>
              <div className="flex space-x-4 items-center">
                <Instagram className="w-4 h-4" />
                <a
                  href="https://www.instagram.com/slag_ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-300 transition-colors"
                >
                  Instagram
                </a>
              </div>
            </li>
          </ul>
        </nav>
      )}
    </header>
  );
}
