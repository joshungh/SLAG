"use client";

import { useState } from "react";
import { useWeb3 } from "@/hooks/useWeb3";

interface RegisterFormProps {
  onSuccess?: () => void;
}

export default function RegisterForm({ onSuccess }: RegisterFormProps) {
  const { connected, publicKey } = useWeb3();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isEmailRegistration, setIsEmailRegistration] = useState(!connected);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    firstName: "",
    lastName: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    // Validate password match for email registration
    if (isEmailRegistration && formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: formData.username,
            email: isEmailRegistration ? formData.email : null,
            password: isEmailRegistration ? formData.password : null,
            first_name: formData.firstName,
            last_name: formData.lastName,
            web3_wallet: isEmailRegistration ? null : publicKey,
            login_method: isEmailRegistration ? "email" : "web3",
            confirmPassword: formData.confirmPassword,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || "Registration failed");
      }

      // Clear form
      setFormData({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        firstName: "",
        lastName: "",
      });

      // Call success callback if provided
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to register");
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 text-sm bg-red-500/10 border border-red-500 text-red-500 rounded-lg">
          {error}
        </div>
      )}

      {connected && (
        <div className="p-3 bg-green-500/10 border border-green-500 text-green-500 rounded-lg text-sm">
          Wallet Connected: {publicKey?.slice(0, 4)}...{publicKey?.slice(-4)}
        </div>
      )}

      {isEmailRegistration ? (
        <>
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-1">
              Email*
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full p-2 bg-black/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Enter email"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium mb-1"
            >
              Password*
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full p-2 bg-black/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Enter password"
            />
          </div>

          <div>
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-medium mb-1"
            >
              Confirm Password*
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="w-full p-2 bg-black/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Confirm password"
            />
          </div>
        </>
      ) : null}

      <div>
        <label htmlFor="username" className="block text-sm font-medium mb-1">
          Username{isEmailRegistration ? "*" : " (Optional)"}
        </label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required={isEmailRegistration}
          className="w-full p-2 bg-black/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          placeholder="Enter username"
        />
      </div>

      <div>
        <label htmlFor="firstName" className="block text-sm font-medium mb-1">
          First Name (Optional)
        </label>
        <input
          type="text"
          id="firstName"
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          className="w-full p-2 bg-black/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          placeholder="Enter first name"
        />
      </div>

      <div>
        <label htmlFor="lastName" className="block text-sm font-medium mb-1">
          Last Name (Optional)
        </label>
        <input
          type="text"
          id="lastName"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          className="w-full p-2 bg-black/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          placeholder="Enter last name"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading || (!isEmailRegistration && !connected)}
        className="w-full py-2 px-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? "Registering..." : "Register"}
      </button>

      {!connected && (
        <div className="text-center">
          <button
            type="button"
            onClick={() => setIsEmailRegistration(!isEmailRegistration)}
            className="text-sm text-gray-400 hover:text-white"
          >
            {isEmailRegistration
              ? "Register with Web3 Wallet Instead"
              : "Register with Email Instead"}
          </button>
        </div>
      )}
    </form>
  );
}