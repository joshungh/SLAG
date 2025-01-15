"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useWeb3 } from "@/hooks/useWeb3";
import React from "react";

export default function UserProfileSection() {
  const { connected, publicKey, connect, disconnect } = useWeb3();
  const [user, setUser] = useState<any>(null);

  // Function to truncate wallet address - memoize it
  const truncateAddress = React.useCallback((address: string) => {
    if (!address) return "";
    return `${address.slice(0, 4)}...${address.slice(-4)}`;
  }, []);

  // Check if user exists when wallet is connected - memoize it
  const checkExistingUser = React.useCallback(async (walletAddress: string) => {
    try {
      const response = await fetch(`/api/auth/wallet/${walletAddress}`);
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (error) {
      console.error("Error checking user:", error);
    }
  }, []);

  // Effect to check user when wallet connects - with proper dependencies
  useEffect(() => {
    let mounted = true;

    if (connected && publicKey) {
      checkExistingUser(publicKey).then(() => {
        if (!mounted) return;
      });
    } else {
      setUser(null);
    }

    return () => {
      mounted = false;
    };
  }, [connected, publicKey, checkExistingUser]);

  // Memoize the connect button section
  const ConnectSection = React.useMemo(
    () => (
      <div className="p-4 border-t border-gray-800">
        <div className="flex flex-col gap-2">
          <button
            onClick={connect}
            className="w-full py-2 px-4 bg-green-500 hover:bg-green-600 rounded-lg text-white text-sm font-medium transition-colors"
          >
            Connect Wallet
          </button>
          <Link
            href="/login"
            className="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-white text-sm font-medium text-center transition-colors"
          >
            Email Sign In
          </Link>
        </div>
      </div>
    ),
    [connect]
  );

  if (!connected) {
    return ConnectSection;
  }

  if (connected && !user) {
    return (
      <div className="p-4 border-t border-gray-800">
        <div className="flex flex-col gap-2">
          <p className="text-sm text-gray-400">Wallet Connected</p>
          <p className="text-sm font-medium">
            {truncateAddress(publicKey || "")}
          </p>
          <Link
            href="/register"
            className="w-full py-2 px-4 bg-green-500 hover:bg-green-600 rounded-lg text-white text-sm font-medium text-center transition-colors"
          >
            Complete Registration
          </Link>
          <button
            onClick={disconnect}
            className="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-white text-sm font-medium transition-colors"
          >
            Disconnect
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 border-t border-gray-800">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
          <span className="text-lg font-medium">
            {user?.username?.[0]?.toUpperCase() || publicKey?.[0]}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">
            {user?.username || truncateAddress(publicKey || "")}
          </p>
          <p className="text-xs text-gray-400 truncate">
            {user?.email || "Web3 User"}
          </p>
        </div>
      </div>
      <button
        onClick={disconnect}
        className="mt-2 w-full py-1.5 px-3 bg-gray-800 hover:bg-gray-700 rounded text-sm transition-colors"
      >
        Sign Out
      </button>
    </div>
  );
}
