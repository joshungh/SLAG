import { Metadata } from "next";
import DashboardLayout from "@/components/DashboardLayout";
import { Web3Provider } from "@/components/Web3Provider";

export const metadata: Metadata = {
  title: "Dashboard | SLAG",
  description: "SLAG Dashboard",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Web3Provider>
      <DashboardLayout>{children}</DashboardLayout>
    </Web3Provider>
  );
}