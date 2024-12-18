import './globals.css'
import type { Metadata } from 'next'

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
      <body className="text-lg">{children}</body>
    </html>
  )
}
