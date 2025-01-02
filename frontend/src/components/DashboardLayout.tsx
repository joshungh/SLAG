"use client";

import Link from "next/link";
import { ReactNode } from "react";
import { useWallet } from "@solana/wallet-adapter-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";
import { useConnection } from "@solana/wallet-adapter-react";
import { useState, useEffect } from "react";
import { LAMPORTS_PER_SOL } from "@solana/web3.js";
import { Wallet, CircleDot, Menu, X } from "lucide-react";

interface DashboardLayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const { publicKey, connected } = useWallet();
  const { connection } = useConnection();
  const [balance, setBalance] = useState<number | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    async function getBalance() {
      if (publicKey && connected) {
        try {
          const bal = await connection.getBalance(publicKey);
          setBalance(bal / LAMPORTS_PER_SOL);
        } catch (error) {
          console.error("Error fetching balance:", error);
          setBalance(null);
        }
      } else {
        setBalance(null);
      }
    }

    getBalance();
  }, [publicKey, connected, connection]);

  const NavLinks = () => (
    <div className="space-y-8">
      <Link
        href="/dashboard"
        className="block text-gray-300 hover:text-green-400 text-xl font-medium tracking-tight"
        onClick={() => setIsMobileMenuOpen(false)}
      >
        Home
      </Link>
      <Link
        href="/dashboard/create"
        className="block text-gray-300 hover:text-green-400 text-xl font-medium tracking-tight"
        onClick={() => setIsMobileMenuOpen(false)}
      >
        Create
      </Link>
      <Link
        href="/dashboard/library"
        className="block text-gray-300 hover:text-green-400 text-xl font-medium tracking-tight"
        onClick={() => setIsMobileMenuOpen(false)}
      >
        Library
      </Link>
      <Link
        href="/dashboard/explore"
        className="block text-gray-300 hover:text-green-400 text-xl font-medium tracking-tight"
        onClick={() => setIsMobileMenuOpen(false)}
      >
        Explore
      </Link>
      <Link
        href="/dashboard/search"
        className="block text-gray-300 hover:text-green-400 text-xl font-medium tracking-tight"
        onClick={() => setIsMobileMenuOpen(false)}
      >
        Search
      </Link>
    </div>
  );

  const WalletInfo = () => (
    <div className="space-y-4">
      {/* Wallet Status Indicator */}
      <div className="flex items-center space-x-2 text-sm">
        <CircleDot
          className={`w-3 h-3 ${
            connected ? "text-green-400" : "text-gray-500"
          }`}
        />
        <span className={`${connected ? "text-green-400" : "text-gray-500"}`}>
          {connected ? "Connected" : "Not Connected"}
        </span>
      </div>

      {/* Balance Display */}
      {connected && balance !== null && (
        <div className="flex items-center space-x-2 text-gray-400 text-base">
          <Wallet className="w-4 h-4" />
          <span className="font-medium">{balance.toFixed(2)} SOL</span>
        </div>
      )}
    </div>
  );

  return (
    <div className="h-screen flex flex-col md:flex-row">
      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between p-4 border-b border-gray-800/30">
        <Link href="/" className="text-2xl font-bold text-green-400">
          SLAG
        </Link>
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="text-gray-400 hover:text-white"
        >
          {isMobileMenuOpen ? (
            <X className="w-6 h-6" />
          ) : (
            <Menu className="w-6 h-6" />
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden fixed inset-0 top-[73px] bg-black z-50 p-6">
          <div className="flex flex-col h-full">
            <NavLinks />
            <div className="mt-auto">
              <WalletInfo />
            </div>
          </div>
        </div>
      )}

      {/* Desktop Sidebar */}
      <nav className="hidden md:flex w-44 bg-black border-r border-gray-800/30 p-6 flex-col">
        <Link href="/" className="text-3xl font-bold text-green-400 mb-16">
          SLAG
        </Link>
        <NavLinks />
        <div className="mt-auto">
          <WalletInfo />
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="flex justify-end items-center px-6 py-4 border-b border-gray-800/30">
          <WalletMultiButton
            className={`
              !py-2 !px-4 !rounded-lg !transition-all !font-medium !text-base md:!text-lg
              ${
                connected
                  ? "!bg-green-400/10 !text-green-400 hover:!bg-green-400/20"
                  : "!bg-gray-800 !text-gray-300 hover:!bg-gray-700"
              }
            `}
          />
        </header>

        {/* Scrollable Content Area */}
        <main className="flex-1 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
