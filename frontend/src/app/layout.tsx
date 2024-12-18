import { IBM_Plex_Mono } from 'next/font/google'
import './globals.css'
import type { Metadata } from 'next'

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-ibm-plex-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Starfall: Lost Age of Giants',
  description: 'An autonomously generated graphic novel powered by AI',
  icons: {
    icon: [
      { rel: 'icon', url: '/favicon.ico' },
      { rel: 'icon', url: '/icon.png', type: 'image/png' },
    ],
    apple: {
      url: '/apple-icon.png',
      type: 'image/png'
    }
  }
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${ibmPlexMono.variable} bg-black text-white`}>
        {children}
      </body>
    </html>
  )
}
