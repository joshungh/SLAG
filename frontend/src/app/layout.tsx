import { IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import { metadata } from "./metadata";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-ibm-plex-mono",
  display: "swap",
});

export { metadata };

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="text-[16px]">
      <body
        className={`
          ${ibmPlexMono.variable} 
          bg-black 
          text-white 
          text-lg
          antialiased
        `}
      >
        {children}
      </body>
    </html>
  );
}
