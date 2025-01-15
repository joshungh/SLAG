"use client";

import { createContext, useContext, useEffect, useState } from "react";

interface WalletContextType {
  connected: boolean;
  connect: () => Promise<void>;
  disconnect: () => Promise<void>;
  publicKey: string | null;
}

const WalletContext = createContext<WalletContextType>({
  connected: false,
  connect: async () => {},
  disconnect: async () => {},
  publicKey: null,
});

export function WalletContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [connected, setConnected] = useState(false);
  const [publicKey, setPublicKey] = useState<string | null>(null);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const phantom = (window as any).solana;
        if (phantom?.isPhantom) {
          const response = await phantom.connect({ onlyIfTrusted: true });
          setConnected(true);
          setPublicKey(response.publicKey.toString());
        }
      } catch (error) {
        // Silent error for auto-connection
      }
    };

    if (typeof window !== "undefined") {
      checkConnection();

      // Listen for wallet connection changes
      window.addEventListener("load", checkConnection);
      return () => window.removeEventListener("load", checkConnection);
    }
  }, []);

  const connect = async () => {
    try {
      const phantom = (window as any).solana;
      if (phantom?.isPhantom) {
        const response = await phantom.connect();
        setConnected(true);
        setPublicKey(response.publicKey.toString());
      } else {
        window.open("https://phantom.app/", "_blank");
      }
    } catch (error) {
      console.error("Connection error:", error);
    }
  };

  const disconnect = async () => {
    try {
      const phantom = (window as any).solana;
      if (phantom?.isPhantom) {
        await phantom.disconnect();
        setConnected(false);
        setPublicKey(null);
      }
    } catch (error) {
      console.error("Disconnection error:", error);
    }
  };

  return (
    <WalletContext.Provider
      value={{
        connected,
        connect,
        disconnect,
        publicKey,
      }}
    >
      {children}
    </WalletContext.Provider>
  );
}

export const useWallet = () => useContext(WalletContext);