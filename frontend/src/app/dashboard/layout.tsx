"use client";

import DashboardLayout from "@/components/DashboardLayout";
import { Web3Provider } from "@/components/Web3Provider";
import { AuthProvider } from "@/contexts/AuthContext";
import { StoryQueueProvider } from "@/contexts/StoryQueueContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Web3Provider>
      <AuthProvider>
        <StoryQueueProvider>
          <DashboardLayout>{children}</DashboardLayout>
        </StoryQueueProvider>
      </AuthProvider>
    </Web3Provider>
  );
}
