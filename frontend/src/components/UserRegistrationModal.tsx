"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Mail, Lock, User, Loader2 } from "lucide-react";

interface UserRegistrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: any) => Promise<void>;
  mode: "web3" | "traditional";
  walletAddress: string | null;
  onSignInClick: () => void;
}

export default function UserRegistrationModal({
  isOpen,
  onClose,
  onSubmit,
  mode,
  walletAddress,
  onSignInClick,
}: UserRegistrationModalProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      // Validation
      if (mode === "traditional" && (!formData.email || !formData.password)) {
        throw new Error(
          "Email and password are required for traditional registration"
        );
      }

      if (!formData.username) {
        throw new Error("Username is required");
      }

      await onSubmit(formData);
    } catch (err: any) {
      // Handle API error responses
      if (err?.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err?.message) {
        setError(err.message);
      } else if (typeof err === "string") {
        setError(err);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
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
                Create Account
              </h2>
              <p className="text-gray-400">
                Join SLAG to start creating stories
              </p>
            </div>

            {mode === "web3" && walletAddress && (
              <div className="mb-4 p-2 bg-green-500/10 border border-green-500/20 rounded">
                <p className="text-sm text-gray-300">
                  Connected Wallet: {walletAddress}
                </p>
              </div>
            )}

            {error && (
              <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded">
                <p className="text-sm text-red-400">
                  {error === "Username already taken"
                    ? "Username already taken, please try a different one"
                    : error}
                </p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <div className="relative">
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                    placeholder="Username"
                    required
                  />
                  <User className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                </div>
              </div>

              {mode === "traditional" && (
                <>
                  <div>
                    <div className="relative">
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                        placeholder="Email address"
                        required
                      />
                      <Mail className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                    </div>
                  </div>

                  <div>
                    <div className="relative">
                      <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                        placeholder="Password"
                        required
                      />
                      <Lock className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                    </div>
                  </div>
                </>
              )}

              <div>
                <div className="relative">
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                    placeholder="First Name (Optional)"
                  />
                  <User className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                </div>
              </div>

              <div>
                <div className="relative">
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    className="w-full p-2 pl-9 bg-[#2a2a2a] border border-gray-700 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-500"
                    placeholder="Last Name (Optional)"
                  />
                  <User className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 bg-green-500 text-white font-medium p-2 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Creating Account...</span>
                    </>
                  ) : (
                    "Create Account"
                  )}
                </button>
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 border border-gray-700 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={() => {
                  onSignInClick();
                  onClose();
                }}
                className="text-sm text-gray-400 hover:text-white"
              >
                Already have an account? Sign in
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}