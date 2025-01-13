"use client";

import { createContext, useContext, useState, useEffect } from "react";
import { setToken, removeToken } from "@/utils/auth";

interface User {
  id: string;
  username: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  profile_picture: string | null;
  web3_wallet: string | null;
  bio: string | null;
  created_at: string;
  login_methods: string[];
}

interface AuthContextType {
  user: User | null;
  authMethod: string | null;
  setUser: (user: User | null) => void;
  signIn: (token: string, userData: User) => void;
  signOut: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [authMethod, setAuthMethod] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    if (token) {
      console.log("Found auth token, verifying...");
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/verify`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error("Token invalid");
          }
          return res.json();
        })
        .then((data) => {
          if (data.user) {
            console.log("User data received:", data.user);
            setUser(data.user);
            setAuthMethod(data.user.login_methods?.[0] || "email");
          } else {
            throw new Error("No user data");
          }
        })
        .catch((error) => {
          console.error("Session verification failed:", error);
          removeToken();
          setUser(null);
          setAuthMethod(null);
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      console.log("No auth token found");
      setIsLoading(false);
    }
  }, []);

  const signIn = (token: string, userData: User) => {
    console.log("Signing in user:", userData);
    setToken(token);
    setUser(userData);
    setAuthMethod(userData.login_methods?.[0] || "email");
  };

  const signOut = () => {
    console.log("Signing out user");
    removeToken();
    setUser(null);
    setAuthMethod(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, authMethod, setUser, signIn, signOut, isLoading }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
