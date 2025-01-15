import { useState, useRef, useEffect } from "react";
import { User, Settings, LogOut, Edit } from "lucide-react";
import Link from "next/link";

interface UserMenuProps {
  user: {
    username?: string;
    email?: string;
  };
  onSignOut: () => void;
  truncateAddress: (address: string) => string;
  balance: number | null;
  publicKey: string | null;
  authMethod: string | null;
}

export default function UserMenu({
  user,
  onSignOut,
  truncateAddress,
  balance,
  publicKey,
  authMethod,
}: UserMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      {/* Avatar Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-2 rounded-full hover:bg-white/5 transition-colors"
      >
        <div className="w-10 h-10 rounded-full bg-[#4CAF50] flex items-center justify-center text-white text-lg">
          {user.username ? user.username[0].toUpperCase() : "U"}
        </div>
        <span className="text-sm text-gray-300">{user.username}</span>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute bottom-full left-0 mb-2 w-64 rounded-lg shadow-lg bg-[#1a1a1a] border border-white/10 overflow-hidden">
          {/* User Info */}
          <div className="p-4 border-b border-white/10">
            <div>
              <p className="text-base font-medium text-white">
                {user.username}
              </p>
              <p className="text-sm text-gray-400 truncate">{user.email}</p>
              {publicKey && (
                <div className="mt-2 text-sm text-gray-400">
                  <p className="truncate">
                    Wallet: {truncateAddress(publicKey)}
                  </p>
                  {balance !== null && (
                    <p className="mt-1">Balance: {balance} SOL</p>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-2">
            <Link
              href="/dashboard/profile"
              className="flex items-center px-4 py-3 text-sm text-gray-300 hover:bg-white/5 transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <User className="w-4 h-4 mr-3" />
              View Profile
            </Link>

            <button
              onClick={() => {
                onSignOut();
                setIsOpen(false);
              }}
              className="flex items-center w-full px-4 py-3 text-sm text-gray-300 hover:bg-white/5 transition-colors"
            >
              <LogOut className="w-4 h-4 mr-3" />
              Sign Out
            </button>
          </div>

          {/* Footer Links */}
          <div className="px-4 py-3 bg-black/20 flex items-center justify-between text-xs text-gray-500">
            <Link href="/terms" className="hover:text-gray-300">
              Terms of Service
            </Link>
            <Link href="/privacy" className="hover:text-gray-300">
              Privacy
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}