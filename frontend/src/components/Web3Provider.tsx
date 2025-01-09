"use client";

import { createContext, useContext, useEffect, useState } from "react";

interface Web3ContextType {
  connected: boolean;
  connect: () => Promise<void>;
  disconnect: () => Promise<void>;
  publicKey: string | null;
  balance: number | null;
}

const Web3Context = createContext<Web3ContextType>({
  connected: false,
  connect: async () => {},
  disconnect: async () => {},
  publicKey: null,
  balance: null,
});

export function Web3Provider({ children }: { children: React.ReactNode }) {
  const [connected, setConnected] = useState(false);
  const [publicKey, setPublicKey] = useState<string | null>(null);
  const [balance, setBalance] = useState<number | null>(null);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const phantom = (window as any).solana;
        if (phantom?.isPhantom) {
          const response = await phantom.connect({ onlyIfTrusted: true });
          setConnected(true);
          setPublicKey(response.publicKey.toString());

          // Get balance
          const balance = await phantom.request({
            method: "getBalance",
            params: [response.publicKey.toString()],
          });
          setBalance(balance);
        }
      } catch (error) {
        // Silent error for auto-connection
      }
    };

    if (typeof window !== "undefined") {
      checkConnection();
    }
  }, []);

  const connect = async () => {
    try {
      const phantom = (window as any).solana;
      if (phantom?.isPhantom) {
        const response = await phantom.connect();
        setConnected(true);
        setPublicKey(response.publicKey.toString());

        // Get balance after connection
        const balance = await phantom.request({
          method: "getBalance",
          params: [response.publicKey.toString()],
        });
        setBalance(balance);
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
        setBalance(null);
      }
    } catch (error) {
      console.error("Disconnection error:", error);
    }
  };

  return (
    <Web3Context.Provider
      value={{
        connected,
        connect,
        disconnect,
        publicKey,
        balance,
      }}
    >
      {children}
    </Web3Context.Provider>
  );
}

export const useWeb3 = () => {
  const context = useContext(Web3Context);
  if (context === undefined) {
    throw new Error("useWeb3 must be used within a Web3Provider");
  }
  return context;
};
