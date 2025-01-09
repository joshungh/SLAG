import { Metadata } from "next";
import DashboardLayout from "@/components/DashboardLayout";
import { Web3Provider } from "@/components/Web3Provider";
import ConnectButton from "@/components/ConnectButton";

export const metadata: Metadata = {
  title: "Dashboard | SLAG",
  description: "SLAG Dashboard",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Web3Provider>
      <DashboardLayout>
        <div className="fixed top-4 right-4 z-50">
          <ConnectButton />
        </div>
        {children}
      </DashboardLayout>
    </Web3Provider>
  );
}
