"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { Connection, PublicKey, clusterApiUrl } from "@solana/web3.js";

// Initialize Solana connection
const connection = new Connection(clusterApiUrl("devnet"));

interface Web3ContextType {
  connected: boolean;
  publicKey: string | null;
  balance: number | null;
  connect: () => Promise<void>;
  disconnect: () => void;
}

const Web3Context = createContext<Web3ContextType>({
  connected: false,
  publicKey: null,
  balance: null,
  connect: async () => {},
  disconnect: () => {},
});

export function Web3Provider({ children }: { children: ReactNode }) {
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
      // Check if user explicitly disconnected
      const wasDisconnected =
        localStorage.getItem("wallet_disconnected") === "true";
      if (wasDisconnected) {
        return;
      }

      const provider = (window as any).phantom?.solana;
      if (provider?.isPhantom) {
        // Check if already connected
        if (provider.isConnected && provider.publicKey) {
          const pubKey = provider.publicKey.toString();
          setConnected(true);
          setPublicKey(pubKey);
          await fetchBalance(pubKey);
        }
      }
    } catch (error) {
      console.error("Error checking wallet connection:", error);
    }
  };

  useEffect(() => {
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

    if (typeof window !== "undefined") {
      (window as any).phantom?.solana?.on("connect", handleConnect);
      (window as any).phantom?.solana?.on("disconnect", handleDisconnect);
      (window as any).phantom?.solana?.on("accountChanged", handleConnect);

      return () => {
        (window as any).phantom?.solana?.removeListener(
          "connect",
          handleConnect
        );
        (window as any).phantom?.solana?.removeListener(
          "disconnect",
          handleDisconnect
        );
        (window as any).phantom?.solana?.removeListener(
          "accountChanged",
          handleConnect
        );
      };
    }
  }, []);

  const connect = async () => {
    try {
      const provider = (window as any).phantom?.solana;
      if (provider?.isPhantom) {
        const response = await provider.connect();
        const pubKey = response.publicKey.toString();
        localStorage.removeItem("wallet_disconnected"); // Remove disconnected flag when user explicitly connects
        setConnected(true);
        setPublicKey(pubKey);
        await fetchBalance(pubKey);
      }
    } catch (error) {
      console.error("Error connecting to Phantom wallet:", error);
    }
  };

  const disconnect = () => {
    const provider = (window as any).phantom?.solana;
    if (provider?.isPhantom) {
      provider.disconnect();
      localStorage.setItem("wallet_disconnected", "true"); // Set disconnected flag when user explicitly disconnects
      setConnected(false);
      setPublicKey(null);
      setBalance(null);
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
