"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useWeb3 } from "@/contexts/Web3Context";
import { Wallet } from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { connected, connect, disconnect, publicKey, balance } = useWeb3();

  return (
    <div className="flex min-h-screen bg-black">
      {/* Sidebar */}
      <div className="fixed top-0 left-0 w-64 h-screen border-r border-white/10 flex flex-col">
        <div className="p-6">
          <Link
            href="/"
            className="flex items-center space-x-2 text-xl font-mono text-green-400"
          >
            <span className="text-green-400">_</span>
            <span>SLAG.exe</span>
          </Link>
        </div>

        <nav className="mt-6">
          <Link
            href="/dashboard/create"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard/create" || pathname === "/dashboard"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
            }`}
          >
            Create
          </Link>
        </nav>

        {/* Wallet Status */}
        <div className="mt-auto border-t border-white/10">
          <div className="p-4 space-y-4">
            <div className="flex flex-col space-y-2">
              <div className="flex items-center space-x-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    connected ? "bg-green-400" : "bg-gray-500"
                  }`}
                />
                <span className="text-sm text-gray-400">
                  {connected ? "Connected" : "Not Connected"}
                </span>
              </div>
              {connected && (
                <>
                  <div className="text-sm text-gray-400">
                    {balance?.toFixed(4)} SOL
                  </div>
                  <div className="text-sm text-gray-400">
                    {publicKey?.slice(0, 4)}...{publicKey?.slice(-4)}
                  </div>
                </>
              )}
            </div>
            <button
              onClick={connected ? disconnect : connect}
              className={`w-full py-2 px-4 text-white rounded-lg font-medium flex items-center justify-center space-x-2 transition-all ${
                connected
                  ? "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700"
                  : "bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700"
              }`}
            >
              <Wallet className="w-4 h-4" />
              <span>{connected ? "Connected" : "Connect"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 ml-64">
        <div className="p-8">{children}</div>
      </div>
    </div>
  );
}
