"use client";

import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { useWeb3 } from "@/contexts/Web3Context";
import { Wallet, LogIn, PlusCircle, Menu, X } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import SignInModal from "./SignInModal";
import UserRegistrationModal from "./UserRegistrationModal";
import { setToken, getToken, removeToken } from "@/utils/auth";
import UserMenu from "./UserMenu";

interface User {
  username?: string;
}

interface ConnectedUserViewProps {
  user: User | null;
  publicKey: string | null;
  balance: number | null;
  onDisconnect: () => void;
  truncateAddress: (address: string) => string;
}

interface ConnectedWalletViewProps {
  publicKey: string | null;
  balance: number | null;
  onDisconnect: () => void;
  truncateAddress: (address: string) => string;
}

interface DisconnectedViewProps {
  onConnect: () => void;
  disabled: boolean;
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { connected, publicKey, balance, connect, disconnect } = useWeb3();
  const { user, authMethod, signOut, signIn, isLoading } = useAuth();
  const [isSignInModalOpen, setIsSignInModalOpen] = useState(false);
  const [isRegistrationModalOpen, setIsRegistrationModalOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Close sidebar when route changes on mobile
  useEffect(() => {
    setIsSidebarOpen(false);
  }, [pathname]);

  // Function to truncate wallet address
  const truncateAddress = (address: string) => {
    if (!address) return "";
    return `${address.slice(0, 4)}...${address.slice(-4)}`;
  };

  const handleConnect = () => {
    if (authMethod === "email") {
      // Show warning or confirmation before switching
      if (
        window.confirm(
          "Switching to wallet will sign you out of your current session. Continue?"
        )
      ) {
        signOut();
        connect();
      }
    } else {
      connect();
    }
  };

  const handleDisconnect = () => {
    disconnect();
    signOut();
  };

  const handleSignOut = () => {
    signOut();
    router.push("/dashboard/create");
  };

  const handleOpenSignIn = () => {
    if (authMethod === "wallet") {
      // Show warning or confirmation before switching
      if (
        window.confirm(
          "Switching to email sign in will disconnect your wallet. Continue?"
        )
      ) {
        disconnect();
        signOut();
        setIsSignInModalOpen(true);
      }
    } else {
      setIsSignInModalOpen(true);
    }
  };

  const handleSignIn = async (credentials: {
    email: string;
    password: string;
  }) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
            login_method: "email",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to sign in");
      }

      signIn(data.token, data.user);
      setIsSignInModalOpen(false);

      return data;
    } catch (error) {
      console.error("Error signing in:", error);
      throw error;
    }
  };

  const handleOpenRegistration = () => {
    setIsSignInModalOpen(false);
    setIsRegistrationModalOpen(true);
  };

  const handleRegister = async (data: any) => {
    try {
      const registrationData = {
        username: data.username,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
        web3_wallet: publicKey || null,
        login_method: publicKey ? "web3" : "email",
        password: data.password,
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(registrationData),
        }
      );

      const responseData = await response.json();

      if (!response.ok) {
        throw responseData;
      }

      if (responseData?.user) {
        // Use the signIn function from AuthContext
        if (responseData.token) {
          signIn(responseData.token, responseData.user);
        }
      } else {
        throw new Error("No user data received");
      }

      setIsRegistrationModalOpen(false);

      return responseData;
    } catch (error: any) {
      console.error("Error registering:", error);
      if (error.detail) {
        throw new Error(error.detail);
      }
      throw error;
    }
  };

  // Modal handlers
  const handleCloseSignIn = () => setIsSignInModalOpen(false);
  const handleCloseRegistration = () => setIsRegistrationModalOpen(false);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-green-500"></div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen">
      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="fixed top-4 left-4 z-50 md:hidden text-white hover:text-green-400 transition-colors"
      >
        {isSidebarOpen ? (
          <X className="w-6 h-6" />
        ) : (
          <Menu className="w-6 h-6" />
        )}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 w-64 h-screen border-r border-white/10 flex flex-col bg-black transform transition-transform duration-300 ease-in-out z-50 ${
          isSidebarOpen ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0`}
      >
        {/* Logo */}
        <div className="p-6">
          <Link
            href="/"
            className="flex items-center space-x-2 text-xl font-mono text-green-400"
          >
            <span className="text-green-400">_</span>
            <span>SLAG.exe</span>
          </Link>
        </div>

        {/* Main Navigation */}
        <nav className="flex-1">
          <Link
            href="/dashboard/create"
            className={`flex items-center px-6 py-3 text-base font-medium ${
              pathname === "/dashboard/create" || pathname === "/dashboard"
                ? "bg-white/10 text-white"
                : "text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
            }`}
          >
            Create
          </Link>
        </nav>

        {/* Auth Section */}
        <div className="mt-auto px-4 space-y-4">
          {user && (
            <div className="mb-4">
              <UserMenu
                user={user}
                onSignOut={handleSignOut}
                truncateAddress={truncateAddress}
                balance={balance}
                publicKey={publicKey}
                authMethod={authMethod}
              />
            </div>
          )}

          {!user && (
            <button
              onClick={handleOpenSignIn}
              disabled={connected && authMethod === "wallet"}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                connected && authMethod === "wallet"
                  ? "opacity-50 cursor-not-allowed text-gray-600"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              <LogIn className="w-5 h-5" />
              <span>Sign In</span>
            </button>
          )}

          {/* Wallet Section */}
          <div className="border-t border-white/10 pt-4">
            {connected ? (
              <ConnectedWalletView
                publicKey={publicKey}
                balance={balance}
                onDisconnect={handleDisconnect}
                truncateAddress={truncateAddress}
              />
            ) : (
              <DisconnectedView
                onConnect={handleConnect}
                disabled={!!user || authMethod === "traditional"}
              />
            )}
          </div>
        </div>

        {/* Bottom padding */}
        <div className="p-4" />
      </div>

      {/* Main Content */}
      <div className="flex-1 md:ml-64">
        <div className="p-4 sm:p-8">{children}</div>
      </div>

      {/* Modals */}
      <SignInModal
        isOpen={isSignInModalOpen}
        onClose={handleCloseSignIn}
        onSignIn={handleSignIn}
        onRegisterClick={handleOpenRegistration}
      ></SignInModal>

      <UserRegistrationModal
        isOpen={isRegistrationModalOpen}
        onClose={handleCloseRegistration}
        onSubmit={handleRegister}
        mode={publicKey ? "web3" : "traditional"}
        walletAddress={publicKey}
        onSignInClick={handleOpenSignIn}
      />
    </div>
  );
}

// Component for connected user view
function ConnectedUserView({
  user,
  publicKey,
  balance,
  onDisconnect,
  truncateAddress,
}: ConnectedUserViewProps) {
  return (
    <>
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
          <span className="text-lg font-medium">
            {user?.username?.[0]?.toUpperCase() || (publicKey && publicKey[0])}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">
            {user?.username || (publicKey && truncateAddress(publicKey))}
          </p>
          <p className="text-xs text-gray-400 truncate">
            {balance?.toFixed(4)} SOL
          </p>
        </div>
      </div>
      <button
        onClick={onDisconnect}
        className="w-full py-2 px-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-lg font-medium flex items-center justify-center space-x-2 transition-all"
      >
        <Wallet className="w-4 h-4" />
        <span>Disconnect</span>
      </button>
    </>
  );
}

// Component for connected wallet view
function ConnectedWalletView({
  publicKey,
  balance,
  onDisconnect,
  truncateAddress,
}: ConnectedWalletViewProps) {
  return (
    <>
      <div className="flex flex-col space-y-2 mb-3">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-400" />
          <span className="text-sm text-gray-400">Connected</span>
        </div>
        <div className="text-sm text-gray-400">{balance?.toFixed(4)} SOL</div>
        <div className="text-sm text-gray-400">
          {publicKey ? truncateAddress(publicKey) : ""}
        </div>
      </div>
      <button
        onClick={onDisconnect}
        className="w-full py-2 px-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-lg font-medium flex items-center justify-center space-x-2 transition-all"
      >
        <Wallet className="w-4 h-4" />
        <span>Disconnect</span>
      </button>
    </>
  );
}

// Component for disconnected view
function DisconnectedView({ onConnect, disabled }: DisconnectedViewProps) {
  return (
    <>
      <div className="flex flex-col space-y-2 mb-3">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-gray-500" />
          <span className="text-sm text-gray-400">Not Connected</span>
        </div>
      </div>
      <button
        onClick={onConnect}
        disabled={disabled}
        className={`w-full py-2 px-4 rounded-lg font-medium flex items-center justify-center space-x-2 transition-all ${
          disabled
            ? "bg-gray-700 cursor-not-allowed opacity-50"
            : "bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white"
        }`}
      >
        <Wallet className="w-4 h-4" />
        <span>Connect</span>
      </button>
    </>
  );
}
