"use client";

import DashboardLayout from "@/components/DashboardLayout";
import { Web3Provider } from "@/components/Web3Provider";
import { AuthProvider } from "@/contexts/AuthContext";
import { StoryQueueProvider } from "@/contexts/StoryQueueContext";
import { StoryProvider } from "@/contexts/StoryContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Web3Provider>
      <AuthProvider>
        <StoryQueueProvider>
          <StoryProvider>
            <DashboardLayout>{children}</DashboardLayout>
          </StoryProvider>
        </StoryQueueProvider>
      </AuthProvider>
    </Web3Provider>
  );
}
