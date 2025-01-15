"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Mail, Lock, Loader2 } from "lucide-react";
import Link from "next/link";

interface SignInModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSignIn: (credentials: {
    identifier: string;
    password: string;
  }) => Promise<any>;
  onRegisterClick: () => void;
  children?: React.ReactNode;
}

interface FormData {
  identifier: string;
  password: string;
}

export default function SignInModal({
  isOpen,
  onClose,
  onSignIn,
  onRegisterClick,
  children,
}: SignInModalProps) {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await onSignIn({ identifier, password });
    } catch (error: any) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence mode="wait">
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="relative bg-[#1a1a1a] rounded-lg shadow-xl w-full max-w-md p-8 z-10"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={onClose}
              className="absolute top-4 right-4 p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">
                Sign in to SLAG
              </h2>
              <p className="text-gray-400">
                Welcome back! Please sign in to continue.
              </p>
            </div>

            {error && (
              <div className="mb-4 p-2 bg-red-500/10 border border-red-500/20 rounded">
                <p className="text-sm text-red-400">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label
                  htmlFor="identifier"
                  className="block text-sm font-medium text-gray-300 mb-1"
                >
                  Email or Username
                </label>
                <input
                  type="text"
                  id="identifier"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white"
                  placeholder="Enter your email or username"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-300 mb-1"
                >
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-2 px-4 rounded-lg font-medium flex items-center justify-center space-x-2 ${
                  isLoading
                    ? "bg-gray-600 cursor-not-allowed"
                    : "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700"
                } text-white transition-all`}
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-t-2 border-b-2 border-white rounded-full animate-spin" />
                    <span>Signing in...</span>
                  </>
                ) : (
                  "Sign in"
                )}
              </button>

              <div className="text-center mt-4">
                <p className="text-gray-400">
                  Don't have an account?{" "}
                  <button
                    onClick={onRegisterClick}
                    className="text-green-500 hover:text-green-400 font-medium"
                  >
                    Sign up
                  </button>
                </p>
              </div>
            </form>

            <p className="mt-4 text-xs text-center text-gray-500">
              By continuing, you accept our{" "}
              <Link
                href="/privacy"
                className="text-gray-400 hover:text-white"
                onClick={onClose}
              >
                Privacy Policy
              </Link>{" "}
              and{" "}
              <Link
                href="/terms"
                className="text-gray-400 hover:text-white"
                onClick={onClose}
              >
                Terms of Use
              </Link>
            </p>

            {children}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
