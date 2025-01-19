"use client";

import { WalletContextProvider } from "@/contexts/WalletContext";
import { ToastProvider } from "./ui/use-toast";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WalletContextProvider>
      <ToastProvider>{children}</ToastProvider>
    </WalletContextProvider>
  );
}
