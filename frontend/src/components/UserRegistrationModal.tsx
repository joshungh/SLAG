"use client";

import { useState } from "react";
import { Loader2 } from "lucide-react";

interface UserRegistrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: any) => Promise<void>;
  mode: "web3" | "traditional";
  walletAddress: string | null;
}

export default function UserRegistrationModal({
  isOpen,
  onClose,
  onSubmit,
  mode,
  walletAddress,
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

  if (!isOpen) return null;

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
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
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
    <div className="fixed inset-0 bg-black/90 flex items-center justify-center p-4 z-50">
      <div className="bg-[#1a1a1a] rounded-lg p-6 max-w-md w-full">
        <h2 className="text-xl font-semibold mb-4">Create Account</h2>
        {mode === "web3" && walletAddress && (
          <div className="mb-4 p-2 bg-green-500/10 border border-green-500/20 rounded">
            <p className="text-sm text-gray-300">
              Connected Wallet: {walletAddress}
            </p>
          </div>
        )}

        {error && (
          <div className="mb-4 p-2 bg-red-500/10 border border-red-500/20 rounded">
            <p className="text-sm text-red-400">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full bg-black/50 border border-white/10 rounded px-3 py-2 text-white"
              placeholder="Enter username"
              required
            />
          </div>

          {mode === "traditional" && (
            <>
              <div>
                <label className="block text-sm text-gray-400 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-black/50 border border-white/10 rounded px-3 py-2 text-white"
                  placeholder="Enter email"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full bg-black/50 border border-white/10 rounded px-3 py-2 text-white"
                  placeholder="Enter password"
                  required
                />
              </div>
            </>
          )}

          <div>
            <label className="block text-sm text-gray-400 mb-1">
              First Name (Optional)
            </label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              className="w-full bg-black/50 border border-white/10 rounded px-3 py-2 text-white"
              placeholder="Enter first name"
            />
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">
              Last Name (Optional)
            </label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              className="w-full bg-black/50 border border-white/10 rounded px-3 py-2 text-white"
              placeholder="Enter last name"
            />
          </div>

          <div className="flex gap-3 mt-6">
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-lg py-2 px-4 flex items-center justify-center space-x-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Creating Profile...</span>
                </>
              ) : (
                <span>Register</span>
              )}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-white/10 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
