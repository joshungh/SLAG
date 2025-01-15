"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { Connection, PublicKey, clusterApiUrl } from "@solana/web3.js";
import UserRegistrationModal from "@/components/UserRegistrationModal";
import { useAuth } from "./AuthContext";

// Initialize Solana connection
const connection = new Connection(clusterApiUrl("devnet"), "confirmed");

type Web3ContextType = {
  connected: boolean;
  publicKey: string | null;
  balance: number | null;
  connect: () => Promise<void>;
  disconnect: () => void;
  isNewUser: boolean;
  userProfile: any | null;
};

const Web3Context = createContext<Web3ContextType>({
  connected: false,
  publicKey: null,
  balance: null,
  connect: async () => {},
  disconnect: () => {},
  isNewUser: false,
  userProfile: null,
});

export function Web3Provider({ children }: { children: React.ReactNode }) {
  const { signIn, signOut } = useAuth();
  const [connected, setConnected] = useState(false);
  const [publicKey, setPublicKey] = useState<string | null>(null);
  const [balance, setBalance] = useState<number | null>(null);
  const [isNewUser, setIsNewUser] = useState(false);
  const [showRegistration, setShowRegistration] = useState(false);
  const [userProfile, setUserProfile] = useState<any | null>(null);

  const fetchBalance = async (pubKey: string) => {
    try {
      const balance = await connection.getBalance(new PublicKey(pubKey));
      setBalance(balance / 1e9); // Convert lamports to SOL
    } catch (error) {
      console.error("Error fetching balance:", error);
    }
  };

  const checkUserExists = async (walletAddress: string) => {
    try {
      const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
      if (!BACKEND_URL) {
        throw new Error("NEXT_PUBLIC_API_URL environment variable is not set");
      }

      const response = await fetch(
        `${BACKEND_URL}/api/users/wallet/${walletAddress}`
      );
      if (response.ok) {
        const userData = await response.json();
        setUserProfile(userData);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Error checking user:", error);
      return false;
    }
  };

  const handleUserRegistration = async (formData: any) => {
    try {
      const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
      if (!BACKEND_URL) {
        throw new Error("NEXT_PUBLIC_API_URL environment variable is not set");
      }

      const userData = {
        username: formData.username || `user_${publicKey?.slice(0, 8)}`,
        email: formData.email || null,
        first_name: formData.first_name || null,
        last_name: formData.last_name || null,
        web3_wallet: publicKey,
        login_method: "web3",
        created_at: new Date().toISOString(),
      };

      const response = await fetch(`${BACKEND_URL}/api/users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create user");
      }

      signIn(data.token, data.user);
      setUserProfile(data.user);
      setShowRegistration(false);
      localStorage.setItem("wallet_disconnected", "false");
      return data;
    } catch (error) {
      console.error("Error creating user:", error);
      throw error;
    }
  };

  const handleUserLogin = async (walletAddress: string) => {
    try {
      const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
      if (!BACKEND_URL) {
        throw new Error("NEXT_PUBLIC_API_URL environment variable is not set");
      }

      const response = await fetch(`${BACKEND_URL}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          web3_wallet: walletAddress,
          login_method: "web3",
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to login");
      }

      signIn(data.token, data.user);
      setUserProfile(data.user);
      return data;
    } catch (error) {
      console.error("Error logging in:", error);
      throw error;
    }
  };

  const checkAndUpdateConnection = async () => {
    try {
      const wasDisconnected =
        localStorage.getItem("wallet_disconnected") === "true";
      if (wasDisconnected) {
        setConnected(false);
        setPublicKey(null);
        setBalance(null);
        setUserProfile(null);
        return;
      }

      const provider = window?.phantom?.solana;
      if (provider?.isPhantom) {
        if (provider.isConnected && provider.publicKey) {
          const pubKey = provider.publicKey.toString();

          // Check if user exists first
          const userExists = await checkUserExists(pubKey);

          if (userExists) {
            // If user exists, log them in
            await handleUserLogin(pubKey);
            setConnected(true);
            setPublicKey(pubKey);
            await fetchBalance(pubKey);
          } else {
            // Only show registration for new users
            setConnected(true);
            setPublicKey(pubKey);
            await fetchBalance(pubKey);
            setShowRegistration(true);
          }
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
    if (typeof window === "undefined") return;
    checkAndUpdateConnection();

    const handleConnect = async () => {
      const wasDisconnected =
        localStorage.getItem("wallet_disconnected") === "true";
      if (wasDisconnected) {
        const provider = window?.phantom?.solana;
        if (provider?.isPhantom) {
          await provider.disconnect();
        }
        return;
      }
      localStorage.removeItem("wallet_disconnected");
      checkAndUpdateConnection();
    };

    const handleDisconnect = () => {
      setConnected(false);
      setPublicKey(null);
      setBalance(null);
      setUserProfile(null);
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

        // First check if user exists
        const userExists = await checkUserExists(pubKey);

        if (userExists) {
          // If user exists, log them in
          await handleUserLogin(pubKey);
          setConnected(true);
          setPublicKey(pubKey);
          await fetchBalance(pubKey);
        } else {
          // If user doesn't exist, show registration
          setConnected(true);
          setPublicKey(pubKey);
          await fetchBalance(pubKey);
          setShowRegistration(true);
        }
      }
    } catch (error) {
      console.error("Error connecting to Phantom wallet:", error);
      await disconnect(); // Disconnect if anything fails
    }
  };

  const disconnect = async () => {
    try {
      const provider = window?.phantom?.solana;
      if (provider?.isPhantom) {
        localStorage.setItem("wallet_disconnected", "true");
        await provider.disconnect();
        setConnected(false);
        setPublicKey(null);
        setBalance(null);
        setUserProfile(null);
        signOut(); // Sign out from AuthContext when disconnecting wallet
      }
    } catch (error) {
      console.error("Error disconnecting from Phantom wallet:", error);
      localStorage.setItem("wallet_disconnected", "true");
      setConnected(false);
      setPublicKey(null);
      setBalance(null);
      setUserProfile(null);
      signOut(); // Sign out from AuthContext even if disconnect fails
    }
  };

  return (
    <Web3Context.Provider
      value={{
        connected,
        publicKey,
        balance,
        connect,
        disconnect,
        isNewUser,
        userProfile,
      }}
    >
      {children}
      <UserRegistrationModal
        isOpen={showRegistration}
        onClose={() => {
          setShowRegistration(false);
          disconnect(); // Disconnect if they cancel registration
        }}
        walletAddress={publicKey}
        onSubmit={handleUserRegistration}
        mode="web3"
        onSignInClick={() => {}}
      />
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