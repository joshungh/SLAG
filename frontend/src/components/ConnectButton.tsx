"use client";

import { useWeb3 } from "@/contexts/Web3Context";
import { Wallet } from "lucide-react";
import React from "react";

export default function ConnectButton() {
  const { connected, connect, disconnect, publicKey } = useWeb3();

  // Memoize the truncated address
  const truncatedAddress = React.useMemo(() => {
    if (!connected || !publicKey) return "Connect Wallet";
    return `${publicKey.slice(0, 4)}...${publicKey.slice(-4)}`;
  }, [connected, publicKey]);

  // Memoize the click handler
  const handleClick = React.useCallback(() => {
    if (connected) {
      disconnect();
    } else {
      connect();
    }
  }, [connected, connect, disconnect]);

  return (
    <button
      onClick={handleClick}
      className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-lg font-medium transition-colors"
    >
      <Wallet className="w-5 h-5" />
      <span>{truncatedAddress}</span>
    </button>
  );
}
