"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Mail, Lock, Loader2 } from "lucide-react";
import Link from "next/link";

interface SignInModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSignIn: (credentials: { email: string; password: string }) => Promise<any>;
  onRegisterClick: () => void;
  children?: React.ReactNode;
}

interface FormData {
  email: string;
  password: string;
}

export default function SignInModal({
  isOpen,
  onClose,
  onSignIn,
  onRegisterClick,
  children,
}: SignInModalProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (error) setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      await onSignIn(formData);
      onClose();
    } catch (err) {
      // Handle API error responses
      if (err instanceof Error) {
        // Check if it's an API error response
        const apiError = err as any;
        if (apiError.detail) {
          setError(apiError.detail);
        } else if (typeof apiError === "object" && apiError.message) {
          setError(apiError.message);
        } else {
          setError(err.message || "Failed to sign in");
        }
      } else if (typeof err === "string") {
        setError(err);
      } else {
        setError("An unexpected error occurred");
      }
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
                <div className="relative">
                  <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Email address"
                    className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                  />
                  <Mail className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                </div>
              </div>

              <div>
                <div className="relative">
                  <input
                    type="password"
                    name="password"
                    required
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="Password"
                    className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                  />
                  <Lock className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-green-500 text-white font-medium p-2 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Signing in...</span>
                  </>
                ) : (
                  "Sign in"
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={onRegisterClick}
                className="text-sm text-gray-400 hover:text-white"
              >
                Don't have an account? Sign up
              </button>
            </div>

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