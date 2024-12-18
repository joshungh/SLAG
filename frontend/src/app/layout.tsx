import { IBM_Plex_Mono } from 'next/font/google'
import './globals.css'
import type { Metadata } from 'next'

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-ibm-plex-mono'
})

export const metadata: Metadata = {
  title: 'Starfall: Lost Age of Giants',
  description: 'An autonomously generated graphic novel powered by AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className={`${ibmPlexMono.variable} bg-black text-white`}>
        {children}
      </body>
    </html>
  )
}
