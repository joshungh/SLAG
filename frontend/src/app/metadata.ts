import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Starfall: Lost Age of Giants",
  description: "An autonomously generated graphic novel powered by AI",
  metadataBase: new URL("https://lostage.io"),
  openGraph: {
    title: "Starfall: Lost Age of Giants",
    description:
      "An autonomously generated, classic sci-fi inspired graphic novel.",
    url: "https://lostage.io",
    siteName: "Starfall: Lost Age of Giants",
    images: [
      {
        url: "/images/og-image.png",
        width: 1200,
        height: 630,
        alt: "Starfall: Lost Age of Giants",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Starfall: Lost Age of Giants",
    description:
      "An autonomously generated, classic sci-fi inspired graphic novel.",
    images: ["/images/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  alternates: {
    canonical: "https://lostage.io",
  },
  icons: {
    icon: [
      { rel: "icon", url: "/favicon.ico" },
      { rel: "icon", url: "/icon.png", type: "image/png" },
    ],
    apple: {
      url: "/apple-icon.png",
      type: "image/png",
    },
  },
};