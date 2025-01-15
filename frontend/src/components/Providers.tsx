"use client";

import { WalletContextProvider } from "@/contexts/WalletContext";

export default function Providers({ children }: { children: React.ReactNode }) {
  return <WalletContextProvider>{children}</WalletContextProvider>;
}