"use client";

import { useWeb3 } from "@/contexts/Web3Context";
import { Wallet } from "lucide-react";

export default function ConnectButton() {
  const { connected, connect, disconnect, publicKey } = useWeb3();

  return (
    <button
      onClick={connected ? disconnect : connect}
      className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 rounded-lg font-medium transition-colors"
    >
      <Wallet className="w-5 h-5" />
      <span>
        {connected
          ? `${publicKey?.slice(0, 4)}...${publicKey?.slice(-4)}`
          : "Connect Wallet"}
      </span>
    </button>
  );
}
