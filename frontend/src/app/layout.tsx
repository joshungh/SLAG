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
      { url: '/favicon.ico' },
      { url: '/icons/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/icons/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      { url: '/icons/apple-touch-icon.png' }
    ],
    other: [
      {
        rel: 'manifest',
        url: '/icons/site.webmanifest'
      }
    ]
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
