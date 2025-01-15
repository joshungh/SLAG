import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Web3Provider } from "@/contexts/Web3Context";
import { AuthProvider } from "@/contexts/AuthContext";
import { StoryQueueProvider } from "@/contexts/StoryQueueContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SLAG",
  description: "AI-powered story generation platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen`}>
        <AuthProvider>
          <Web3Provider>
            <StoryQueueProvider>{children}</StoryQueueProvider>
          </Web3Provider>
        </AuthProvider>
      </body>
    </html>
  );
}
