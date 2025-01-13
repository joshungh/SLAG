"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { Connection, PublicKey, clusterApiUrl } from "@solana/web3.js";

// Initialize Solana connection
const connection = new Connection(clusterApiUrl("devnet"), "confirmed");

type Web3ContextType = {
  connected: boolean;
  publicKey: string | null;
  balance: number | null;
  connect: () => Promise<void>;
  disconnect: () => void;
};

const Web3Context = createContext<Web3ContextType>({
  connected: false,
  publicKey: null,
  balance: null,
  connect: async () => {},
  disconnect: () => {},
});

export function Web3Provider({ children }: { children: React.ReactNode }) {
  const [connected, setConnected] = useState(false);
  const [publicKey, setPublicKey] = useState<string | null>(null);
  const [balance, setBalance] = useState<number | null>(null);

  const fetchBalance = async (pubKey: string) => {
    try {
      const balance = await connection.getBalance(new PublicKey(pubKey));
      setBalance(balance / 1e9); // Convert lamports to SOL
    } catch (error) {
      console.error("Error fetching balance:", error);
    }
  };

  const checkAndUpdateConnection = async () => {
    try {
      const provider = window?.phantom?.solana;
      if (provider?.isPhantom) {
        // Check if user explicitly disconnected
        const wasDisconnected =
          localStorage.getItem("wallet_disconnected") === "true";
        if (wasDisconnected) {
          setConnected(false);
          setPublicKey(null);
          setBalance(null);
          return;
        }

        // If not explicitly disconnected, check if wallet is connected
        if (provider.isConnected && provider.publicKey) {
          const pubKey = provider.publicKey.toString();
          setConnected(true);
          setPublicKey(pubKey);
          await fetchBalance(pubKey);
        }
      }
    } catch (error) {
      console.error("Error checking wallet connection:", error);
      setConnected(false);
      setPublicKey(null);
      setBalance(null);
    }
  };

  useEffect(() => {
    // Only run in browser environment
    if (typeof window === "undefined") return;

    // Check connection on mount
    checkAndUpdateConnection();

    // Listen for Phantom connection events
    const handleConnect = () => {
      localStorage.removeItem("wallet_disconnected");
      checkAndUpdateConnection();
    };

    const handleDisconnect = () => {
      setConnected(false);
      setPublicKey(null);
      setBalance(null);
      localStorage.setItem("wallet_disconnected", "true");
    };

    const provider = window.phantom?.solana;
    if (provider) {
      provider.on("connect", handleConnect);
      provider.on("disconnect", handleDisconnect);
      provider.on("accountChanged", handleConnect);

      return () => {
        provider.removeListener("connect", handleConnect);
        provider.removeListener("disconnect", handleDisconnect);
        provider.removeListener("accountChanged", handleConnect);
      };
    }
  }, []);

  const connect = async () => {
    try {
      const provider = window?.phantom?.solana;
      if (provider?.isPhantom) {
        localStorage.removeItem("wallet_disconnected");
        const response = await provider.connect();
        const pubKey = response.publicKey.toString();
        setConnected(true);
        setPublicKey(pubKey);
        await fetchBalance(pubKey);
      }
    } catch (error) {
      console.error("Error connecting to Phantom wallet:", error);
      setConnected(false);
      setPublicKey(null);
      setBalance(null);
    }
  };

  const disconnect = async () => {
    try {
      const provider = window?.phantom?.solana;
      if (provider?.isPhantom) {
        await provider.disconnect();
        localStorage.setItem("wallet_disconnected", "true");
        setConnected(false);
        setPublicKey(null);
        setBalance(null);
      }
    } catch (error) {
      console.error("Error disconnecting from Phantom wallet:", error);
    }
  };

  return (
    <Web3Context.Provider
      value={{ connected, publicKey, balance, connect, disconnect }}
    >
      {children}
    </Web3Context.Provider>
  );
}

export const useWeb3 = () => useContext(Web3Context);

// Add TypeScript declarations for Phantom wallet
declare global {
  interface Window {
    phantom?: {
      solana: {
        isPhantom?: boolean;
        isConnected?: boolean;
        publicKey?: { toString: () => string };
        connect: (params?: { onlyIfTrusted?: boolean }) => Promise<{
          publicKey: { toString: () => string };
        }>;
        disconnect: () => Promise<void>;
        on: (event: string, callback: () => void) => void;
        removeListener: (event: string, callback: () => void) => void;
      };
    };
  }
}
