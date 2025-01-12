"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useWeb3 } from "./Web3Provider";
import { formatBalance } from "../lib/utils";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { connected, balance } = useWeb3();

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-black border-r border-white/10">
        <div className="p-6">
          <Link href="/dashboard" className="text-xl font-bold text-green-400">
            SLAG
          </Link>
        </div>

        <nav className="mt-6">
          <Link
            href="/dashboard"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Home
          </Link>
          <Link
            href="/dashboard/create"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard/create"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Create
          </Link>
          <Link
            href="/dashboard/library"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard/library"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Library
          </Link>
          <Link
            href="/dashboard/explore"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard/explore"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Explore
          </Link>
          <Link
            href="/dashboard/search"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard/search"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Search
          </Link>
        </nav>

        {/* Wallet Status */}
        <div className="absolute bottom-0 left-0 w-64 p-6 border-t border-white/10">
          <div className="flex items-center space-x-2">
            <div
              className={`w-2 h-2 rounded-full ${
                connected ? "bg-green-400" : "bg-gray-500"
              }`}
            />
            <span className="text-sm text-gray-400">
              {connected
                ? `${formatBalance(balance || 0)} SOL`
                : "Not Connected"}
            </span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">{children}</div>
    </div>
  );
}
