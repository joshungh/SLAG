"use client";

import { useWeb3 } from "@/components/Web3Provider";

export default function ConnectButton() {
  const { connected, connect, disconnect, publicKey } = useWeb3();

  return (
    <button
      onClick={connected ? disconnect : connect}
      className="flex items-center gap-2 px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
    >
      <svg
        className="w-5 h-5"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
          stroke="currentColor"
          strokeWidth="2"
        />
        <path
          d="M12 8V16M8 12H16"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
      <span>{connected ? "Connected" : "Connect"}</span>
      {connected && publicKey && (
        <span className="text-xs opacity-50">
          {`${publicKey.slice(0, 4)}...${publicKey.slice(-4)}`}
        </span>
      )}
    </button>
  );
}
