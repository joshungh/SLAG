import { useState, useEffect } from "react";

interface PhantomWindow extends Window {
  phantom?: {
    solana?: {
      connect(): Promise<{ publicKey: { toString(): string } }>;
      disconnect(): Promise<void>;
      isConnected: boolean;
      publicKey: { toString(): string } | null;
    };
  };
}

export function useWeb3() {
  const [connected, setConnected] = useState(false);
  const [publicKey, setPublicKey] = useState<string | null>(null);

  useEffect(() => {
    // Check if Phantom is installed
    const phantom = (window as PhantomWindow).phantom?.solana;
    if (phantom?.isConnected) {
      setConnected(true);
      setPublicKey(phantom.publicKey?.toString() || null);
    }
  }, []);

  const connect = async () => {
    try {
      const phantom = (window as PhantomWindow).phantom?.solana;
      if (!phantom) {
        throw new Error(
          "Phantom wallet not found! Get it from https://phantom.app/"
        );
      }

      const response = await phantom.connect();
      setConnected(true);
      setPublicKey(response.publicKey.toString());
    } catch (error) {
      console.error("Error connecting to wallet:", error);
      throw error;
    }
  };

  const disconnect = async () => {
    try {
      const phantom = (window as PhantomWindow).phantom?.solana;
      if (phantom) {
        await phantom.disconnect();
        setConnected(false);
        setPublicKey(null);
      }
    } catch (error) {
      console.error("Error disconnecting wallet:", error);
      throw error;
    }
  };

  return {
    connected,
    publicKey,
    connect,
    disconnect,
  };
}